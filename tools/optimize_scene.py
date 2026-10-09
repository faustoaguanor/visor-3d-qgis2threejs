"""Compacta la escena exportada por Qgis2threejs (data/index/scene.js).

- Recodifica las texturas (ortofoto) de PNG a JPEG de alta calidad (4:4:4).
- Redondea a centímetros las cotas del MDS y las coordenadas de las geometrías.
- Elimina la indentación del JSON.

Es idempotente: se puede ejecutar de nuevo sobre una escena ya optimizada.

Uso:  python tools/optimize_scene.py [ruta_scene.js] [calidad_jpeg]
"""
import base64
import io
import json
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PREFIX = "app.loadJSONObject("
SUFFIX = '); window.setTimeout(function () { app.dispatchEvent({type: "sceneLoaded"}); }, 0);'


def png_to_jpeg(data_uri, quality):
    header, b64 = data_uri.split(",", 1)
    if "jpeg" in header:
        return data_uri
    img = Image.open(io.BytesIO(base64.b64decode(b64)))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality, subsampling=0, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def round_floats(node, ndigits=2):
    """Redondea recursivamente los flotantes de listas y diccionarios."""
    if isinstance(node, float):
        value = round(node, ndigits)
        return int(value) if value.is_integer() else value
    if isinstance(node, list):
        return [round_floats(v, ndigits) for v in node]
    if isinstance(node, dict):
        return {k: round_floats(v, ndigits) for k, v in node.items()}
    return node


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/index/scene.js"
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 95

    src = open(path, encoding="utf-8").read().strip()
    start, end = src.index(PREFIX) + len(PREFIX), src.rindex(SUFFIX)
    scene = json.loads(src[start:end])

    for layer in scene.get("layers", []):
        data = layer.get("data", [])
        # Capas DEM: lista de bloques. Capas vectoriales: {"materials", "blocks"}.
        blocks = data if isinstance(data, list) else data.get("blocks", [])
        materials = [m for b in blocks for m in b.get("materials", [])]
        if isinstance(data, dict):
            materials += data.get("materials", [])

        for mtl in materials:
            img = mtl.get("image")
            if img and "base64" in img:
                img["base64"] = png_to_jpeg(img["base64"], quality)

        for block in blocks:
            grid = block.get("grid")
            if grid and "array" in grid:
                grid["array"] = round_floats(grid["array"])
            if "features" in block:
                block["features"] = round_floats(block["features"])

    body = json.dumps(scene, separators=(",", ":"), ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        f.write(PREFIX + body + SUFFIX + "\n")
    print("Escena optimizada:", path)


if __name__ == "__main__":
    main()

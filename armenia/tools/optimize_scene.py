"""Compacta la escena exportada por Qgis2threejs (data/index/scene.js).

- Recodifica la textura (ortofoto) de PNG a JPEG de alta calidad (4:4:4).
- Redondea las cotas del MDS a centímetros.
- Elimina la indentación del JSON.

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


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/index/scene.js"
    quality = int(sys.argv[2]) if len(sys.argv) > 2 else 95

    src = open(path, encoding="utf-8").read().strip()
    start, end = src.index(PREFIX) + len(PREFIX), src.rindex(SUFFIX)
    scene = json.loads(src[start:end])

    for layer in scene.get("layers", []):
        for block in layer.get("data", []):
            for mtl in block.get("materials", []):
                img = mtl.get("image")
                if img and "base64" in img:
                    img["base64"] = png_to_jpeg(img["base64"], quality)
            grid = block.get("grid")
            if grid and "array" in grid:
                grid["array"] = [round(v, 2) for v in grid["array"]]

    body = json.dumps(scene, separators=(",", ":"), ensure_ascii=False)
    body = body.replace(".0,", ",").replace(".0]", "]")
    with open(path, "w", encoding="utf-8") as f:
        f.write(PREFIX + body + SUFFIX + "\n")
    print("Escena optimizada:", path)


if __name__ == "__main__":
    main()

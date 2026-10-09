"""Compacta la escena exportada por Qgis2threejs (data/index/scene.js).

- Recodifica las texturas (ortofoto) de PNG a JPEG de alta calidad (4:4:4).
- Redondea a centímetros las cotas del MDS y las coordenadas de las geometrías.
- Elimina la indentación del JSON.

Es idempotente: se puede ejecutar de nuevo sobre una escena ya optimizada.

Opcional: --rellenar-sin-dato VALOR reemplaza las celdas del MDS iguales a VALOR
(típicamente 0, fuera de la cobertura del ráster) por la mediana de las celdas válidas.
Evita el "muro" entre el terreno y el plano cero, que desorienta la cámara.

--fondo RRGGBB define el color con que se rellenan las zonas transparentes de la textura
(por defecto blanco). Con --fondo, además, el margen blanco opaco que rodea la imagen
se pinta de ese color; usa el del fondo del visor para que se funda con él.

Uso:  python tools/optimize_scene.py [ruta_scene.js] [calidad_jpeg] [--rellenar-sin-dato VALOR] [--fondo RRGGBB]
"""
import base64
import io
import json
import sys

from PIL import Image, ImageDraw

Image.MAX_IMAGE_PIXELS = None

PREFIX = "app.loadJSONObject("
SUFFIX = '); window.setTimeout(function () { app.dispatchEvent({type: "sceneLoaded"}); }, 0);'


def png_to_jpeg(data_uri, quality, background=None):
    header, b64 = data_uri.split(",", 1)
    if "jpeg" in header:
        return data_uri
    img = Image.open(io.BytesIO(base64.b64decode(b64)))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, background or (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.convert("RGB")
    if background:
        recolor_margin(img, background)
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


def recolor_margin(img, background):
    """Pinta con `background` el margen blanco opaco que rodea la imagen (relleno por
    inundación desde los bordes; no toca el blanco que quede dentro de la ortofoto)."""
    w, h = img.size
    seeds = [(x, y) for x in (0, w // 2, w - 1) for y in (0, h // 2, h - 1)]
    seeds += [(w // 4, 0), (3 * w // 4, 0), (w // 4, h - 1), (3 * w // 4, h - 1),
              (0, h // 4), (0, 3 * h // 4), (w - 1, h // 4), (w - 1, 3 * h // 4)]
    for seed in seeds:
        if img.getpixel(seed) == (255, 255, 255):
            ImageDraw.floodfill(img, seed, background)


def fill_nodata(grid, nodata):
    """Reemplaza las celdas == nodata por la mediana de las celdas válidas.
    Un relleno constante evita las rayas que produce copiar el vecino más cercano."""
    arr = grid["array"]
    valid = sorted(v for v in arr if v != nodata)
    if not valid or len(valid) == len(arr):
        return 0
    fill = valid[len(valid) // 2]
    grid["array"] = [fill if v == nodata else v for v in arr]
    return len(arr) - len(valid)


def main():
    args = sys.argv[1:]
    nodata = None
    if "--rellenar-sin-dato" in args:
        k = args.index("--rellenar-sin-dato")
        nodata = float(args[k + 1])
        del args[k:k + 2]
    background = None
    if "--fondo" in args:
        k = args.index("--fondo")
        hexcolor = args[k + 1].lstrip("#")
        background = tuple(int(hexcolor[i:i + 2], 16) for i in (0, 2, 4))
        del args[k:k + 2]
    path = args[0] if len(args) > 0 else "data/index/scene.js"
    quality = int(args[1]) if len(args) > 1 else 95

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
                img["base64"] = png_to_jpeg(img["base64"], quality, background)

        for block in blocks:
            grid = block.get("grid")
            if grid and "array" in grid:
                if nodata is not None:
                    n = fill_nodata(grid, nodata)
                    print("Celdas sin dato rellenadas:", n)
                grid["array"] = round_floats(grid["array"])
            if "features" in block:
                block["features"] = round_floats(block["features"])

    body = json.dumps(scene, separators=(",", ":"), ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        f.write(PREFIX + body + SUFFIX + "\n")
    print("Escena optimizada:", path)


if __name__ == "__main__":
    main()

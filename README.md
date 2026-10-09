# Visor 3D Qgis2threejs

Visores web 3D generados con QGIS + [Qgis2threejs](https://github.com/minorua/Qgis2threejs) y renderizados con [three.js](https://threejs.org/). Reúne dos proyectos que antes vivían en repos separados.

| Visor | Carpeta | Descripción |
|---|---|---|
| MDS Armenia | [`armenia/`](armenia/) | Modelo Digital de Superficie del sector Armenia (v2.7 del plugin; incluye `tools/optimize_scene.py`). |
| Edificaciones de Quito | [`quito-edificaciones/`](quito-edificaciones/) | Edificaciones 3D de Quito en UTM (v2.7.1 del plugin). |

Cada carpeta es independiente y usa su propia versión de las bibliotecas, porque el código exportado difiere entre ambos. Su README describe características, controles y estructura.

## Uso

Los visores son estáticos pero cargan `scene.js` por ruta relativa, así que sírvelos con un servidor local:

```bash
python -m http.server 8000
# http://localhost:8000/
```

## Origen

Fusión de `MDS_ARMENIA` y `3d_edificaciones` (archivados). Licencia MIT.

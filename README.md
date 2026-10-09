# Visor 3D Qgis2threejs

Visores web 3D generados con QGIS + [Qgis2threejs](https://github.com/minorua/Qgis2threejs) y renderizados con [three.js](https://threejs.org/). Reúne dos proyectos que antes vivían en repos separados.

| Visor | Carpeta | Descripción |
|---|---|---|
| MDS Armenia | [`armenia/`](armenia/) | Modelo Digital de Superficie del sector Armenia (plugin v2.7). |
| Edificaciones de Quito | [`quito-edificaciones/`](quito-edificaciones/) | Edificaciones 3D de Quito en UTM (plugin v2.7.1). |

Cada carpeta conserva su propia versión de las bibliotecas, porque el código exportado difiere entre ambos. Su README describe características, controles y estructura.

```
.
├── index.html            # Portada con la lista de visores
├── shared/               # Tema (theme.css, viewer.css) y lógica común (viewer.js)
├── tools/                # optimize_scene.py: compacta la escena exportada
├── armenia/
└── quito-edificaciones/
```

## Optimizar una escena

Tras exportar de nuevo desde QGIS, compacta `data/index/scene.js` (texturas PNG → JPEG, coordenadas a centímetros, JSON minificado):

```bash
python tools/optimize_scene.py armenia/data/index/scene.js 90
```

Para Quito se usó además `--rellenar-sin-dato 0 --fondo ebebeb`: el MDS tenía celdas en 0 m fuera de la cobertura del ráster (el terreno está a ~2 800 m), lo que formaba un muro de 2,8 km y desorientaba la cámara. Se rellenan con la mediana de las celdas válidas y el margen blanco de la ortofoto se pinta del color de fondo.

Con esto la escena de Quito pasó de 10,0 MB a 2,0 MB. Requiere Pillow.

## Uso

Los visores son estáticos pero cargan `scene.js` por ruta relativa, así que sírvelos con un servidor local:

```bash
python -m http.server 8000
# http://localhost:8000/
```

## Origen

Fusión de `MDS_ARMENIA` y `3d_edificaciones` (archivados). Licencia MIT.

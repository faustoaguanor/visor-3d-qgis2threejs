# MDS_ARMENIA - Modelo Digital de Superficie del Sector Armenia

Un visualizador web interactivo 3D del Modelo Digital de Superficie (MDS) del sector Armenia, desarrollado con tecnologías GIS y WebGL para representación precisa de datos topográficos y urbanos.

## Descripción

Este proyecto implementa un visualizador 3D web para el Modelo Digital de Superficie del sector Armenia, utilizando tecnologías de sistemas de información geográfica (GIS) y gráficos 3D en navegadores. La aplicación permite la exploración interactiva de datos topográficos, edificaciones y elementos urbanos con precisión geoespacial.

## Características principales

- **Visualización 3D precisa**: Representación detallada del Modelo Digital de Superficie
- **Sistema de coordenadas georreferenciadas**: Datos ubicados en sistema de coordenadas UTM real
- **Interfaz de usuario completa**: Panel de control para ajustar parámetros de visualización
- **Herramientas de medición**: Distancias lineales entre puntos en el espacio 3D
- **Consulta de atributos**: Información detallada de elementos al hacer clic
- **Navegación avanzada**: Controles de órbita, zoom, panorámica y orientación norte
- **Modos de visualización**: Wireframe, sólido, con etiquetas
- **Soporte multi-dispositivo**: Compatible con dispositivos táctiles y de escritorio

## Tecnologías utilizadas

### Visualización 3D y GIS
- **[Three.js](https://threejs.org/)**: Motor de gráficos 3D para WebGL
- **[QGIS](https://www.qgis.org/)**: Sistema de Información Geográfica para procesamiento de datos
- **[Qgis2threejs](https://github.com/minorua/Qgis2threejs)**: Plugin de QGIS para exportar escenas 3D a WebGL (v2.7)
- **[Proj4js](https://github.com/proj4js/proj4js)**: Biblioteca de transformaciones de sistemas de coordenadas

### Interfaz de Usuario
- **[dat.GUI](https://github.com/dataarts/dat.gui)**: Interfaz de controles para parámetros de la escena
- **[OrbitControls](https://threejs.org/docs/#examples/en/controls/OrbitControls)**: Controles de navegación 3D
- **[ViewHelper](https://threejs.org/docs/#examples/en/helpers/ViewHelper)**: Ayuda visual para orientación en el espacio 3D

### Desarrollo Web
- **HTML5**: Estructura de la aplicación web
- **CSS3**: Estilos personalizados para interfaz de usuario
- **JavaScript ES6+**: Lógica de la aplicación y manipulación 3D

## Estructura del proyecto

```
armenia/
├── index.html                  # Aplicación web principal (estilos en ../shared/)
├── Qgis2threejs.js             # Script principal de Qgis2threejs
├── dat-gui_panel.js            # Configuración del panel de control dat.GUI
├── dat-gui/                    # Librería dat.GUI
│   └── dat.gui.min.js
├── threejs/                    # Librería Three.js y dependencias
│   ├── three.min.js
│   ├── OrbitControls.js
│   └── ViewHelper.js
├── data/                       # Datos y escenas 3D
│   └── index/
│       └── scene.js            # Archivo de escena principal generado por QGIS
└── [otros recursos de datos]
```

## Instalación y uso

### Requisitos previos
- Servidor web local (Apache, Nginx, o servidor de desarrollo como `http-server`)
- Navegador web moderno con soporte WebGL (Chrome 60+, Firefox 55+, Edge 79+)
- Acceso a datos GIS procesados con QGIS

### Instalación local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/faustoaguanor/MDS_ARMENIA.git
   cd MDS_ARMENIA
   ```

2. Inicia un servidor web local:
   ```bash
   # Con Python 3
   python -m http.server 8000
   
   # O con Node.js http-server
   npx http-server
   ```

3. Abre tu navegador en `http://localhost:8000`

### Generación de datos con QGIS
Para actualizar o crear nuevos datos:

1. **Instalar QGIS** y el plugin **Qgis2threejs**
2. **Cargar datos vectoriales** (edificios, terreno, infraestructura)
3. **Configurar propiedades 3D**:
   - Extrucción de polígonos según atributos
   - Asignación de materiales y colores
   - Configuración de texturas y transparencias
4. **Exportar a WebGL** usando el plugin Qgis2threejs
5. **Copiar los archivos generados** al directorio `data/`
6. **Optimizar la escena** (recomendado):
   ```bash
   pip install pillow
   python ../tools/optimize_scene.py data/index/scene.js 95
   ```
   Convierte la ortofoto embebida de PNG a JPEG 4:4:4 (calidad 95), redondea las cotas a
   centímetros y minifica el JSON. En este proyecto la escena pasó de 38 MB a 11 MB.

## Funcionalidades

### Navegación 3D
- **Orbitar**: Click izquierdo + arrastrar para rotar alrededor del punto focal
- **Zoom**: Rueda del ratón o gestos táctiles
- **Panorámica**: Click derecho + arrastrar para desplazar la vista
- **Orientación norte**: Flecha de orientación geográfica
- **Controles de vista**: Ayuda visual para navegación

### Herramientas de análisis
- **Medición de distancias**: Herramienta para medir distancias lineales en 3D
- **Consulta de atributos**: Información detallada de elementos seleccionados
- **Zoom a puntos**: Navegación rápida a coordenadas específicas
- **Zoom a capas**: Enfoque en elementos de capas específicas

### Configuración de visualización
- **Ajustes de imagen**: Brillo, contraste y saturación de la ortofoto en tiempo real
- **Iluminación**: Azimut, altura e intensidad del sol, y luz ambiente, para resaltar el relieve
- **Fondo**: Degradado, claro u oscuro
- **Control de capas**: Activación/desactivación de diferentes tipos de elementos
- **Ajuste de parámetros**: Modificación de propiedades visuales en tiempo real
- **Modos de renderizado**: Alternar entre modo sólido y wireframe
- **Visibilidad de etiquetas**: Control de información textual sobre elementos

## Formatos de datos soportados

### Entrada (QGIS)
- **Shapefiles (.shp)**: Formato vectorial estándar
- **GeoTIFF (.tif)**: Datos raster y modelos digitales de elevación
- **GeoJSON (.geojson)**: Formato JSON para datos geoespaciales
- **KML/KMZ**: Formato de Google Earth
- **PostGIS**: Bases de datos espaciales

### Salida (WebGL)
- **JavaScript/JSON**: Estructura optimizada para navegadores web
- **Texturas**: Imágenes optimizadas para renderizado WebGL
- **Geometrías 3D**: Mallas triangulares optimizadas

## Parámetros técnicos

### Sistema de coordenadas
- **Sistema de referencia**: Transversa de Mercator con coordenadas planas (X ≈ 504 000, Y ≈ 9 971 000).
  Por su posición coincide con la proyección local TM Quito (SIRES-DMQ, meridiano central 78°30' O);
  verificar contra el proyecto QGIS de origen.
- **Unidades**: Metros
- **Rango de cotas del MDS**: 2376,3 m – 2620,5 m (los valores 0 se tratan como *NoData* y no se dibujan)

### Configuración de visualización
- **Color de fondo**: Degradado por CSS (lienzo WebGL transparente)
- **Punto de vista inicial**: Vista oblicua general de todo el sector desde el sur
- **Iluminación**: Luz hemisférica (cielo/suelo) + sol direccional (azimut 315°, altura 50°)
- **Color**: Flujo de color sRGB correcto (textura decodificada a lineal, salida con gamma 2.2)
- **Sombreado**: Iluminación por píxel (Phong sin especular) para un relieve suave
- **Texturas**: Filtrado anisotrópico máximo disponible y *dithering* para evitar bandas
- **Navegación**: Inercia (*damping*) y límite para que la cámara no pase bajo el horizonte
- Todos estos valores se configuran en `Q3D.Config` (`Qgis2threejs.js`): `renderer`, `imageAdjust`,
  `lights`, `dem.noDataValue`, `material.perPixelLighting`

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.

```
MIT License

Copyright (c) 2025 faustoaguanor

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y los archivos de documentación asociados (el "Software"), para
utilizar el Software sin restricción, incluyendo sin limitación los derechos
de uso, copia, modificación, fusión, publicación, distribución, sublicencia y/o
venta de copias del Software, y para permitir a las personas a las que se les
proporcione el Software hacer lo mismo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas
las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN,
DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O
CUALQUIER OTRO MOTIVO, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U
OTRO TIPO DE ACCIONES EN EL SOFTWARE.
```

## Créditos

### Desarrollo y Mantenimiento
- **Desarrollador principal**: faustoaguanor

### Plataformas y Herramientas
- **QGIS**: QGIS Development Team - Sistema de Información Geográfica
- **Qgis2threejs**: Minoru Akagi - Plugin para exportación 3D
- **Three.js**: Mr.doob y colaboradores - Motor de gráficos 3D
- **dat.GUI**: Data Arts Team - Interfaz de controles gráficos

### Estándares y Formatos
- **Shapefile**: Esri - Formato vectorial estándar
- **GeoJSON**: Internet Engineering Task Force (IETF) - Formato JSON para datos geoespaciales
- **WebGL**: Khronos Group - API de gráficos 3D para navegadores

### Tecnologías Relacionadas
- **Proj4js**: Mike Adair, Richard Marsden - Transformaciones de coordenadas
- **OpenStreetMap**: Comunidad OSM - Datos cartográficos de base
- **GDAL/OGR**: Open Source Geospatial Foundation - Bibliotecas de traducción de datos geoespaciales

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Abre un issue para discutir cambios significativos antes de realizar un pull request
2. Sigue las convenciones de código existentes
3. Incluye documentación actualizada para nuevas funcionalidades
4. Prueba los cambios en diferentes navegadores y dispositivos

## Soporte técnico

Para problemas o preguntas:

1. Consulta la [documentación de Qgis2threejs](https://github.com/minorua/Qgis2threejs/wiki)
2. Revisa los [issues del repositorio](https://github.com/faustoaguanor/MDS_ARMENIA/issues)
3. Para problemas con datos GIS, consulta la [documentación de QGIS](https://www.qgis.org/en/docs/)

## Aplicaciones y casos de uso

Este proyecto está diseñado para:

- **Planificación urbana**: Visualización 3D de desarrollo urbano en Armenia
- **Análisis topográfico**: Estudio de pendientes y modelado del terreno
- **Gestión de riesgos**: Evaluación de susceptibilidad a deslizamientos e inundaciones
- **Infraestructura**: Planificación de redes viales y servicios públicos
- **Educación**: Herramienta de enseñanza de conceptos de topografía y urbanismo
- **Participación ciudadana**: Visualización accesible de proyectos de desarrollo

---

*Proyecto desarrollado para la visualización 3D del Modelo Digital de Superficie del sector Armenia, integrando tecnologías GIS modernas para representación territorial precisa.*
# Edificaciones 3D de Quito

Un visualizador 3D web interactivo de edificaciones de Quito, Ecuador, desarrollado con tecnologías GIS y WebGL.


## Descripción

Este proyecto permite la visualización tridimensional de edificaciones de Quito utilizando datos geoespaciales procesados con QGIS y renderizados en un navegador web mediante Three.js. La aplicación incluye funcionalidades de navegación, medición, y consulta de atributos de los elementos del modelo 3D.

## Características principales

- **Visualización 3D interactiva**: Navegación libre con controles de órbita, zoom y panorámica
- **Sistema de coordenadas georreferenciadas**: Modelos ubicados en coordenadas UTM reales
- **Interfaz de usuario intuitiva**: Panel de control con controles de capas y parámetros de visualización
- **Herramientas de medición**: Medición de distancias en el modelo 3D
- **Consulta de atributos**: Información detallada de edificios al hacer clic
- **Soporte multi-dispositivo**: Compatible con dispositivos táctiles y de escritorio
- **Navegación avanzada**: Flecha de orientación norte y controles de vista

## Tecnologías utilizadas

- **[Three.js](https://threejs.org/)**: Motor de gráficos 3D para WebGL (vía CDN)
- **[QGIS](https://www.qgis.org/)**: Sistema de Información Geográfica para procesamiento de datos
- **[Qgis2threejs](https://github.com/minorua/Qgis2threejs)**: Plugin de QGIS para exportar escenas 3D (v2.7.1)
- **[dat.GUI](https://github.com/dataarts/dat.gui)**: Interfaz de controles para parámetros de la escena
- **[OrbitControls](https://threejs.org/docs/#examples/en/controls/OrbitControls)**: Controles de navegación 3D
- **[ViewHelper](https://threejs.org/docs/#examples/en/helpers/ViewHelper)**: Ayuda de navegación visual

## Estructura del proyecto

```
├── index.html                 # Archivo principal HTML (estilos en ../shared/)
├── Qgis2threejs.js            # Script principal del visualizador
├── dat-gui_panel.js           # Configuración del panel de controles
├── threejs/                   # Librerías de Three.js
│   ├── three.min.js
│   ├── OrbitControls.js
│   └── ViewHelper.js
├── dat-gui/                   # Librería dat.GUI
│   └── dat.gui.min.js
└── data/index/                # Datos de la escena 3D
    └── scene.js               # Escena 3D generada por Qgis2threejs
```

## Instalación y uso

### Requisitos previos
- Servidor web local (como [Python HTTP Server](https://docs.python.org/3/library/http.server.html), [Node.js http-server](https://www.npmjs.com/package/http-server), o similar)
- Navegador web moderno con soporte WebGL (Chrome, Firefox, Edge, Safari)

### Instalación local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/faustoaguanor/3d_edificaiones.git
   cd 3d_edificaiones
   ```

2. Inicia un servidor web local:
   ```bash
   # Con Python 3
   python -m http.server 8000
   
   # O con Node.js http-server
   npx http-server
   ```

3. Abre tu navegador en `http://localhost:8000`

### Acceso en línea
El proyecto está diseñado para funcionar directamente desde GitHub Pages o cualquier servidor web estático.

## Controles de navegación

### Ratón
- **Botón izquierdo + arrastrar**: Orbitar alrededor del punto de interés
- **Rueda del ratón**: Zoom in/out
- **Botón derecho + arrastrar**: Panorámica

### Teclado
- **Flechas**: Movimiento horizontal
- **Shift + Flechas**: Orbitar
- **Ctrl + Flechas**: Rotar
- **Shift + Ctrl + Arriba/Abajo**: Zoom in/out
- **L**: Activar/desactivar etiquetas
- **R**: Iniciar/detener animación de rotación
- **W**: Cambiar a modo wireframe
- **Shift + R**: Resetear posición de la cámara
- **Shift + S**: Guardar imagen

## Generación de datos

Los datos 3D se generan mediante el plugin Qgis2threejs para QGIS, que permite:
1. Importar datos vectoriales (edificios, calles, terreno)
2. Configurar extrucciones y materiales
3. Exportar la escena a formato web-compatible
4. Generar archivos de datos optimizados para visualización web

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

- **Desarrollador principal**: faustoaguanor
- **Herramientas GIS**: QGIS Team
- **Plugin Qgis2threejs**: Minoru Akagi
- **Motor 3D**: Three.js Team
- **Interfaz de controles**: dat.GUI Team

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de realizar un pull request.

## Soporte

Para problemas técnicos, abre un issue en el [repositorio GitHub](https://github.com/faustoaguanor/3d_edificaiones/issues).

---

*Este proyecto es parte de una iniciativa para visualizar datos urbanos en 3D de manera accesible y educativa.*

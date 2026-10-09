/*
Comportamiento común de los visores 3D: barra superior y pantalla de carga.
Requiere Q3D (Qgis2threejs.js) y una página con los elementos de shared/viewer.css.
*/
var ViewerUI = (function () {

  // Botones de la barra superior
  function initAppbar(app, gui) {
    document.getElementById("btn-home").onclick = function () { app.controls.reset(); };
    document.getElementById("btn-rotate").onclick = function () {
      app.setRotateAnimationMode(!app.controls.autoRotate);
      this.classList.toggle("active", app.controls.autoRotate);
    };
    document.getElementById("btn-shot").onclick = function () { gui.showPrintDialog(); };
    document.getElementById("btn-help").onclick = function () { gui.showInfo(); };
  }

  // Oculta la pantalla de carga cuando todas las texturas están listas
  // (o tras 20 s, para no bloquear la vista si alguna falla).
  function hideLoaderWhenReady(app, scene) {
    var started = Date.now();
    (function wait() {
      var ready = true;
      for (var id in scene.mapLayers) {
        (scene.mapLayers[id].blocks || []).forEach(function (b) {
          (b.materials || []).forEach(function (m) { if (m && !m.loaded) ready = false; });
        });
      }
      if (ready || Date.now() - started > 20000) {
        app.render();
        document.getElementById("loader").classList.add("done");
      }
      else setTimeout(wait, 100);
    })();
  }

  // Rango de cotas de las capas DEM (ignora celdas sin dato)
  function elevationRange(scene) {
    var noData = Q3D.Config.dem.noDataValue, zMin = Infinity, zMax = -Infinity;
    for (var id in scene.mapLayers) {
      (scene.mapLayers[id].blocks || []).forEach(function (b) {
        var a = (b.data && b.data.grid) ? b.data.grid.array : [];
        for (var i = 0; i < a.length; i++) {
          if (a[i] === noData) continue;
          if (a[i] < zMin) zMin = a[i];
          if (a[i] > zMax) zMax = a[i];
        }
      });
    }
    return zMin <= zMax ? { min: zMin, max: zMax } : null;
  }

  return { initAppbar: initAppbar, hideLoaderWhenReady: hideLoaderWhenReady, elevationRange: elevationRange };
})();

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

  // Ajusta los controles de cámara: inercia, límites de distancia y de inclinación.
  // Con renderizado bajo demanda, la inercia necesita un bucle que llame a controls.update()
  // mientras dura el arrastre y un instante después.
  function tuneControls(app, opts) {
    var c = app.controls;
    if (!c) return;
    opts = opts || {};
    c.maxPolarAngle = Math.PI * 0.495;   // la cámara no pasa del horizonte
    c.rotateSpeed = opts.rotateSpeed || 0.6;
    c.zoomSpeed = opts.zoomSpeed || 0.6;
    c.panSpeed = opts.panSpeed || 0.8;
    c.minDistance = opts.minDistance || 0;
    c.maxDistance = opts.maxDistance || Infinity;
    c.enableDamping = true;
    c.dampingFactor = 0.15;

    var dragging = false, lastActive = 0, looping = false;
    function loop() {
      if (app.animation.isActive || !c.enabled) { looping = false; return; }
      c.update();
      if (dragging || performance.now() - lastActive < 800) requestAnimationFrame(loop);
      else looping = false;
    }
    function kick() {
      lastActive = performance.now();
      if (!looping) { looping = true; requestAnimationFrame(loop); }
    }
    c.addEventListener("start", function () { dragging = true; kick(); });
    c.addEventListener("end", function () { dragging = false; kick(); });
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

  return { initAppbar: initAppbar, tuneControls: tuneControls, hideLoaderWhenReady: hideLoaderWhenReady, elevationRange: elevationRange };
})();

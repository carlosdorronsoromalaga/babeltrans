// Babel Translations — el poco JavaScript que hace falta. La web funciona
// entera sin él (menús por :hover/:focus-within, formularios por POST normal);
// esto añade el menú del móvil, el aviso tras enviar un formulario y las tres
// piezas de traducción: la alineación de la portada, los modismos y la torre.
(function () {
  var boton = document.querySelector(".menu-abrir");
  if (boton) {
    boton.addEventListener("click", function () {
      var abierto = document.body.classList.toggle("menu-abierto");
      boton.setAttribute("aria-expanded", abierto);
    });
  }
  document.querySelectorAll(".sub-abrir").forEach(function (b) {
    b.addEventListener("click", function () {
      var abierto = b.nextElementSibling.classList.toggle("abierta");
      b.setAttribute("aria-expanded", abierto);
    });
  });

  // Selector de idioma: se abre con clic o teclado, se cierra fuera o con Esc.
  // Al elegir idioma se deja una marca para que la página nueva haga el
  // barrido de traducción (ver SCRIPT_BARRIDO en construir.py).
  document.querySelectorAll("[data-selector]").forEach(function (sel) {
    var b = sel.querySelector(".selector-boton");
    function abre(si) { sel.classList.toggle("abierto", si); b.setAttribute("aria-expanded", si); }
    b.addEventListener("click", function (e) { e.stopPropagation(); abre(!sel.classList.contains("abierto")); });
    document.addEventListener("click", function (e) { if (!sel.contains(e.target)) abre(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { abre(false); b.focus(); } });
    sel.querySelectorAll("a[data-idioma]").forEach(function (a) {
      a.addEventListener("click", function () {
        if (a.getAttribute("aria-current")) return;
        try { sessionStorage.setItem("traduciendo", document.documentElement.lang); } catch (x) {}
      });
    });
  });
  // Las líneas de la edición paralela también cambian de idioma: mismo barrido.
  document.querySelectorAll(".paralelo .codigo").forEach(function (a) {
    a.addEventListener("click", function () {
      try { sessionStorage.setItem("traduciendo", document.documentElement.lang); } catch (x) {}
    });
  });

  // enviar.php vuelve con ?enviado=ok o ?enviado=error
  var m = location.search.match(/[?&]enviado=(ok|error)/);
  if (m) {
    var aviso = document.querySelector('[data-aviso="' + m[1] + '"]');
    if (aviso) {
      aviso.hidden = false;
      if (m[1] === "ok") {
        var form = document.querySelector(".formulario");
        if (form) form.hidden = true;
      }
      aviso.scrollIntoView({ block: "center" });
    }
  }
  // Alineación: al señalar un trozo de la frase se iluminan sus equivalentes
  document.querySelectorAll("[data-alinear]").forEach(function (fig) {
    var fijo = null;
    function marca(n) {
      fig.classList.toggle("alineando", !!n);
      fig.querySelectorAll(".seg").forEach(function (s) {
        s.classList.toggle("on", s.getAttribute("data-a") === n);
      });
    }
    fig.addEventListener("mouseover", function (e) {
      var s = e.target.closest(".seg");
      if (s) marca(s.getAttribute("data-a"));
    });
    fig.addEventListener("mouseleave", function () { marca(fijo); });
    fig.addEventListener("focusin", function (e) {
      if (e.target.classList.contains("seg")) marca(e.target.getAttribute("data-a"));
    });
    fig.addEventListener("focusout", function () { marca(fijo); });
    // En el móvil no hay ratón: un toque fija la alineación, otro la quita
    fig.addEventListener("click", function (e) {
      var s = e.target.closest(".seg");
      if (!s) return;
      var n = s.getAttribute("data-a");
      fijo = fijo === n ? null : n;
      marca(fijo);
    });
  });

  // Modismos: «Otro ejemplo» tacha la versión literal y escribe la buena
  document.querySelectorAll("[data-modismos]").forEach(function (fig) {
    var ejemplos = JSON.parse(fig.getAttribute("data-modismos"));
    var i = 0;
    var boton = fig.querySelector(".modismo-otro");
    boton.addEventListener("click", function () {
      i = (i + 1) % ejemplos.length;
      var e = ejemplos[i];
      fig.querySelector(".codigo").textContent = e[0];
      var q = fig.querySelector("q");
      q.textContent = e[1];
      q.setAttribute("lang", e[0]);
      fig.querySelector("del").textContent = e[2];
      fig.querySelector("ins").textContent = e[3];
      fig.classList.remove("corrigiendo");
      void fig.offsetWidth;  // reinicia la animación
      fig.classList.add("corrigiendo");
    });
  });

  // Torre de Babel: el nombre de cada idioma, en el idioma de la página
  document.querySelectorAll("[data-torre]").forEach(function (torre) {
    var pie = torre.parentNode.querySelector(".torre-pie");
    var nombres = null;
    try { nombres = new Intl.DisplayNames([document.documentElement.lang], { type: "language" }); } catch (e) {}
    function muestra(e) {
      var s = e.target.closest("[data-idioma]");
      if (!s || !nombres) return;
      var n = nombres.of(s.getAttribute("data-idioma"));
      pie.textContent = s.textContent + " — " + n.charAt(0).toLocaleUpperCase() + n.slice(1);
    }
    function vuelve() { pie.textContent = pie.getAttribute("data-pie"); }
    torre.addEventListener("mouseover", muestra);
    torre.addEventListener("focusin", muestra);
    torre.addEventListener("click", muestra);
    torre.addEventListener("mouseleave", vuelve);
  });
})();

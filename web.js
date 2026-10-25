// Babel Translations — el poco JavaScript que hace falta. La web funciona
// entera sin él (menús por :hover/:focus-within, formularios por POST normal,
// banderas como enlaces normales); esto añade el menú del móvil, el aviso tras
// enviar un formulario, la transformación del texto al cambiar de idioma y las
// piezas de traducción: la alineación de la portada, los modismos y la torre.
(function () {
  var reducido = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Menú del móvil
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

  // ------------------------------------------------------------------
  // Cambio de idioma: el texto de la página se transforma, palabra a palabra
  // y de arriba abajo, en el del otro idioma; al acabar se carga la página
  // nueva, que ya es igual a lo que se ve. Funciona porque las cuatro
  // versiones salen de la misma plantilla: cada texto tiene su equivalente en
  // la misma posición. Lo que no casa (la torre, la edición paralela, párrafos
  // que solo existen en un idioma) cambia al cargar la página nueva.
  var LETRAS = "abcdefghijklmnopqrstuvwxyzáéíóúäöüßñçëij";
  var FUERA = "script,style,svg,.torre,.paralelo,.banderas,[data-modismos] q,[data-modismos] del,[data-modismos] ins";

  function textos(raiz) {
    var lista = [];
    var w = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = n.parentNode;
        if (!p || (p.closest && p.closest(FUERA))) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var n;
    while ((n = w.nextNode())) lista.push(n);
    return lista;
  }

  // Posición de un texto en el árbol: etiqueta e índice de cada antepasado
  function clave(n, raiz) {
    var partes = [];
    var hijo = n;
    var i = 0;
    for (var h = n.parentNode.firstChild; h; h = h.nextSibling) {
      if (h === n) break;
      if (h.nodeType === 3 && h.nodeValue.trim()) i++;
    }
    partes.push("t" + i);
    var e = n.parentNode;
    while (e && e !== raiz) {
      var j = 0;
      for (var s = e.previousElementSibling; s; s = s.previousElementSibling) j++;
      partes.push(e.tagName + j);
      e = e.parentNode;
    }
    return partes.join("/");
  }

  function revuelve(palabra) {
    var r = "";
    for (var k = 0; k < palabra.length; k++) {
      r += /[\s.,;:!?¿¡()«»“”"'’-]/.test(palabra[k]) ? palabra[k]
        : LETRAS[Math.floor(Math.random() * LETRAS.length)];
    }
    return r;
  }

  function transforma(nodo, destino, retraso, dur) {
    var pre = (destino.match(/^\s*/) || [""])[0];
    var post = (destino.match(/\s*$/) || [""])[0];
    var va = nodo.nodeValue.trim().split(/\s+/);
    var vb = destino.trim().split(/\s+/);
    var padre = nodo.parentNode;
    setTimeout(function () {
      var t0 = performance.now();
      padre.classList.add("traduciendo-texto");
      (function paso() {
        // performance.now() y no la marca de requestAnimationFrame: esa puede
        // ser anterior a t0, dar un índice negativo y cortar la animación
        // con la palabra a medio revolver (pasó el 24/10/2026 en el menú).
        var p = Math.max(0, Math.min(1, (performance.now() - t0) / dur));
        var k = Math.min(vb.length - 1, Math.floor(p * vb.length));
        if (p >= 1) {
          nodo.nodeValue = destino;
          padre.classList.remove("traduciendo-texto");
          return;
        }
        var trozo = vb.slice(0, k);
        trozo.push(revuelve(vb[k]));
        nodo.nodeValue = pre + trozo.concat(va.slice(k + 1)).join(" ") + post;
        // Temporizador y no requestAnimationFrame: este se pausa si la pestaña
        // no está a la vista y la palabra se quedaría revuelta.
        setTimeout(paso, 33);
      })();
    }, retraso);
  }

  function cambiaIdioma(e) {
    var a = e.currentTarget;
    if (a.getAttribute("aria-current") || reducido || !window.fetch || !window.DOMParser) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;   // abrir en pestaña nueva, normal
    e.preventDefault();
    document.body.classList.remove("menu-abierto");
    var destino = a.href;
    var vete = function () { location.href = destino; };
    fetch(destino).then(function (r) { return r.ok ? r.text() : Promise.reject(); }).then(function (html) {
      var nuevo = new DOMParser().parseFromString(html, "text/html");
      var mapa = {};
      textos(nuevo.body).forEach(function (n) { mapa[clave(n, nuevo.body)] = n.nodeValue; });
      var alto = window.innerHeight;
      var fin = 0;
      textos(document.body).forEach(function (n) {
        var otro = mapa[clave(n, document.body)];
        if (otro === undefined || otro === n.nodeValue) return;
        var caja = n.parentNode.getBoundingClientRect();
        if (caja.bottom < 0 || caja.top > alto) { n.nodeValue = otro; return; }
        var retraso = Math.max(0, caja.top) / alto * 420;
        var palabras = otro.trim().split(/\s+/).length;
        var dur = Math.min(620, Math.max(240, palabras * 42));
        fin = Math.max(fin, retraso + dur);
        transforma(n, otro, retraso, dur);
      });
      setTimeout(vete, fin + 150);
    }).catch(vete);
  }
  document.querySelectorAll(".banderas a[hreflang], .paralelo a[hreflang]").forEach(function (a) {
    a.addEventListener("click", cambiaIdioma);
  });

  // ------------------------------------------------------------------
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
    var b = fig.querySelector(".modismo-otro");
    b.addEventListener("click", function () {
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

  // Torre de Babel: el nombre de cada idioma, en el de la página, como rótulo
  // emergente al pasar el ratón (sin título ni pie, Carlos 24/10/2026)
  document.querySelectorAll("[data-torre]").forEach(function (torre) {
    var nombres = null;
    try { nombres = new Intl.DisplayNames([document.documentElement.lang], { type: "language" }); } catch (e) {}
    if (!nombres) return;
    torre.querySelectorAll("[data-idioma]").forEach(function (s) {
      var n = nombres.of(s.getAttribute("data-idioma"));
      if (n) s.title = n.charAt(0).toLocaleUpperCase() + n.slice(1);
    });
  });
})();

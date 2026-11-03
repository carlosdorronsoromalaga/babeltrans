// Babel Translations — el poco JavaScript que hace falta. La web funciona
// entera sin él (menús por :hover/:focus-within, formularios por POST normal,
// banderas como enlaces normales); esto añade el menú del móvil, el aviso tras
// enviar un formulario, la traducción en el sitio al cambiar de idioma y las
// piezas de traducción: la alineación de la portada, los modismos y la torre.
//
// Todo va con eventos delegados en el documento: el cambio de idioma sustituye
// trozos de la página y lo que se sustituye tiene que seguir funcionando.
(function () {
  var reducido = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target : e.target.parentNode;
    var b;
    // Menú del móvil
    if ((b = t.closest(".menu-abrir"))) {
      b.setAttribute("aria-expanded", document.body.classList.toggle("menu-abierto"));
    } else if ((b = t.closest(".sub-abrir"))) {
      b.setAttribute("aria-expanded", b.nextElementSibling.classList.toggle("abierta"));
    } else if ((b = t.closest(".banderas a[hreflang], .paralelo a[hreflang]"))) {
      cambiaIdioma(e, b);
    } else if ((b = t.closest(".modismo-otro"))) {
      otroModismo(b.closest("[data-modismos]"));
    } else if ((b = t.closest("[data-alinear] .seg"))) {
      // En el móvil no hay ratón: un toque fija la alineación, otro la quita
      var fig = b.closest("[data-alinear]");
      var n = b.getAttribute("data-a");
      fig.dataset.fijo = fig.dataset.fijo === n ? "" : n;
      alinea(fig, fig.dataset.fijo);
    }
  });

  // ------------------------------------------------------------------
  // Cambio de idioma: la página se traduce en el sitio, sin recargarse.
  // Se descarga la versión en el otro idioma y se compara pieza a pieza con la
  // que se ve. Donde las dos tienen la misma forma (casi todo: cabecera, menú,
  // pie, títulos, formularios), cada texto se funde palabra a palabra con el
  // suyo: la palabra vieja se desenfoca y se va, y la nueva aparece en la
  // tinta azul de los enlaces y se asienta en su color. Donde no la tienen (un
  // párrafo que solo existe en un idioma, la edición paralela), el bloque
  // entero se funde y ajusta su altura. Todo baja de arriba abajo como una
  // ola. Al acabar se cambian la dirección, el título y los datos para
  // buscadores; la página ya es igual a la que se habría cargado.
  //
  // Sustituye (03/11/2026) a la versión del 24/10, que revolvía las letras y
  // al acabar recargaba la página: Carlos la encontró brusca, con razón. El
  // parpadeo de letras al azar cansaba, la recarga devolvía la página arriba
  // del todo y en la portada repetía la animación de entrada.
  var SALE = [{ opacity: 1, filter: "blur(0)" }, { opacity: 0, filter: "blur(3px)" }];
  var CURVA_SALE = "cubic-bezier(.4, 0, 1, 1)";
  var CURVA_ENTRA = "cubic-bezier(.2, .7, .2, 1)";
  var T_SALE = 200, T_ENTRA = 420, OLA = 320;
  var CABEZA = 'meta[name="description"],meta[property^="og:"],meta[name^="twitter:"],' +
    'link[rel="canonical"],link[rel="alternate"],script[type="application/ld+json"]';
  var ocupado = false;
  var mostrada = location.pathname;

  function cambiaIdioma(e, a) {
    if (a.getAttribute("aria-current") || !window.fetch || !window.DOMParser ||
        !history.pushState || !document.body.animate) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;   // abrir en pestaña nueva, normal
    e.preventDefault();
    if (ocupado) return;
    ocupado = true;
    document.body.classList.remove("menu-abierto");
    var destino = a.href;
    var vete = function () { location.href = destino; };
    fetch(destino).then(function (r) { return r.ok ? r.text() : Promise.reject(); }).then(function (html) {
      traduce(new DOMParser().parseFromString(html, "text/html"), destino);
    }).catch(vete);
  }

  function traduce(nuevo, destino) {
    var alto = window.innerHeight;
    var mueve = !reducido && document.visibilityState === "visible";
    var fin = 0;
    var pares = [];
    var conFoco = document.activeElement && document.activeElement.closest &&
      document.activeElement.closest(".banderas");

    // Cuándo le llega la ola a un elemento; -1 si está fuera de la vista (o no
    // hay movimiento) y se cambia de golpe, sin que nadie lo vea.
    function retraso(el) {
      if (!mueve) return -1;
      var c = el.getBoundingClientRect();
      if (c.bottom < 0 || c.top > alto || (!c.width && !c.height)) return -1;
      return Math.max(0, c.top) / alto * OLA;
    }

    function piezas(el) {
      var l = [];
      for (var n = el.firstChild; n; n = n.nextSibling) {
        if (n.nodeType === 1 || (n.nodeType === 3 && n.nodeValue.trim())) l.push(n);
      }
      return l;
    }
    function forma(n) { return n.nodeType === 3 ? "#" : n.tagName; }

    function casa(a, b) {
      if (a.matches(".banderas")) { a.replaceWith(document.importNode(b, true)); return; }
      if (a.matches(".paralelo")) { sustituye(a, b); return; }
      var pa = piezas(a), pb = piezas(b);
      var igual = pa.length === pb.length;
      for (var i = 0; igual && i < pa.length; i++) igual = forma(pa[i]) === forma(pb[i]);
      if (!igual) { sustituye(a, b); return; }
      pares.push([a, b]);
      pa.forEach(function (n, i) {
        if (n.nodeType === 1) casa(n, pb[i]);
        else if (n.nodeValue !== pb[i].nodeValue) funde(n, pb[i].nodeValue);
      });
    }

    // Un texto, palabra a palabra
    function funde(nodo, texto) {
      var r = retraso(nodo.parentNode);
      if (r < 0) { nodo.nodeValue = texto; return; }
      var caja = document.createElement("span");
      nodo.replaceWith(caja);
      caja.appendChild(nodo);
      var color = getComputedStyle(caja).color;
      var trozos = texto.split(/(\s+)/);
      var palabras = trozos.filter(function (t) { return t && !/^\s+$/.test(t); }).length || 1;
      var paso = Math.min(30, 240 / palabras);
      fin = Math.max(fin, r + T_SALE + (palabras - 1) * paso + T_ENTRA);
      var sale = caja.animate(SALE, { duration: T_SALE, delay: r, easing: CURVA_SALE, fill: "forwards" });
      sale.onfinish = function () {
        var frag = document.createDocumentFragment();
        var k = 0, ultima = null;
        trozos.forEach(function (t) {
          if (!t) return;
          if (/^\s+$/.test(t)) { frag.appendChild(document.createTextNode(t)); return; }
          var s = document.createElement("span");
          s.textContent = t;
          frag.appendChild(s);
          ultima = s.animate([
            { opacity: 0, filter: "blur(4px)", color: "#2b44a8" },
            { opacity: 1, filter: "blur(0)", color: color }
          ], { duration: T_ENTRA, delay: k++ * paso, easing: CURVA_ENTRA, fill: "backwards" });
        });
        caja.replaceChildren(frag);
        sale.cancel();
        // Al acabar, otra vez un texto sin envoltorios: el DOM queda igual
        // que el de la página cargada de cero
        var limpia = function () { if (caja.parentNode) caja.replaceWith(document.createTextNode(texto)); };
        if (ultima) ultima.onfinish = limpia; else limpia();
      };
    }

    // Un bloque entero, cuando las dos versiones no tienen la misma forma
    function sustituye(a, b) {
      var nuevoEl = document.importNode(b, true);
      var r = retraso(a);
      if (r < 0) { a.replaceWith(nuevoEl); return; }
      fin = Math.max(fin, r + T_SALE + T_ENTRA);
      var h0 = a.offsetHeight;
      var sale = a.animate(SALE, { duration: T_SALE, delay: r, easing: CURVA_SALE, fill: "forwards" });
      sale.onfinish = function () {
        a.replaceWith(nuevoEl);
        nuevoEl.animate([{ opacity: 0, filter: "blur(4px)" }, { opacity: 1, filter: "blur(0)" }],
          { duration: T_ENTRA, easing: CURVA_ENTRA });
        var h1 = nuevoEl.offsetHeight;
        if (h0 !== h1 && getComputedStyle(nuevoEl).display !== "inline") {
          // Lo de debajo se desliza a su sitio en vez de saltar
          nuevoEl.style.overflow = "hidden";
          nuevoEl.animate([{ height: h0 + "px" }, { height: h1 + "px" }],
            { duration: T_ENTRA, easing: CURVA_ENTRA }).onfinish = function () {
            nuevoEl.style.overflow = "";
            if (!nuevoEl.getAttribute("style")) nuevoEl.removeAttribute("style");
          };
        }
      };
    }

    function copiaAtributos(a, b) {
      Array.prototype.slice.call(a.attributes).forEach(function (at) {
        if (!b.hasAttribute(at.name)) a.removeAttribute(at.name);
      });
      Array.prototype.slice.call(b.attributes).forEach(function (at) {
        if (a.getAttribute(at.name) !== at.value) a.setAttribute(at.name, at.value);
      });
    }

    try {
      // El idioma de la página, ya: el guionado de lo que va entrando es el
      // del idioma nuevo y no hay reajuste de líneas al final
      document.documentElement.lang = nuevo.documentElement.lang;
      casa(document.body, nuevo.body);
    } catch (err) {
      location.href = destino;
      return;
    }

    setTimeout(function () {
      pares.forEach(function (p) { copiaAtributos(p[0], p[1]); });
      copiaAtributos(document.documentElement, nuevo.documentElement);
      document.title = nuevo.title;
      document.head.querySelectorAll(CABEZA).forEach(function (n) { n.remove(); });
      var ancla = document.head.querySelector('link[rel="icon"]');
      nuevo.head.querySelectorAll(CABEZA).forEach(function (n) {
        document.head.insertBefore(document.importNode(n, true), ancla);
      });
      history.pushState(null, "", destino);
      mostrada = location.pathname;
      titulosTorre(document);
      if (conFoco) {
        var actual = document.querySelector(".banderas a[aria-current]");
        if (actual) actual.focus({ preventScroll: true });
      }
      ocupado = false;
    }, fin + 60);
  }

  // Atrás y adelante entre idiomas: la página de esa dirección, cargada de
  // nuevo. Los saltos dentro de la misma página (#contenido) no recargan.
  window.addEventListener("popstate", function () {
    if (location.pathname !== mostrada) location.reload();
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
  function alinea(fig, n) {
    fig.classList.toggle("alineando", !!n);
    fig.querySelectorAll(".seg").forEach(function (s) {
      s.classList.toggle("on", !!n && s.getAttribute("data-a") === n);
    });
  }
  var señalada = null;
  document.addEventListener("mouseover", function (e) {
    var t = e.target.closest ? e.target : e.target.parentNode;
    var fig = t.closest("[data-alinear]");
    if (señalada && señalada !== fig) alinea(señalada, señalada.dataset.fijo);
    señalada = fig;
    var s = fig && t.closest(".seg");
    if (s) alinea(fig, s.getAttribute("data-a"));
  });
  document.addEventListener("focusin", function (e) {
    var s = e.target.closest && e.target.closest("[data-alinear] .seg");
    if (s) alinea(s.closest("[data-alinear]"), s.getAttribute("data-a"));
  });
  document.addEventListener("focusout", function (e) {
    var fig = e.target.closest && e.target.closest("[data-alinear]");
    if (fig) alinea(fig, fig.dataset.fijo);
  });

  // Modismos: «Otro ejemplo» tacha la versión literal y escribe la buena
  function otroModismo(fig) {
    var ejemplos = JSON.parse(fig.getAttribute("data-modismos"));
    var i = ((+fig.dataset.i || 0) + 1) % ejemplos.length;
    fig.dataset.i = i;
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
  }

  // Torre de Babel: el nombre de cada idioma, en el de la página, como rótulo
  // emergente al pasar el ratón (sin título ni pie, Carlos 24/10/2026)
  function titulosTorre(raiz) {
    var nombres = null;
    try { nombres = new Intl.DisplayNames([document.documentElement.lang], { type: "language" }); } catch (e) {}
    if (!nombres) return;
    raiz.querySelectorAll("[data-torre] [data-idioma]").forEach(function (s) {
      var n = nombres.of(s.getAttribute("data-idioma"));
      if (n) s.title = n.charAt(0).toLocaleUpperCase() + n.slice(1);
    });
  }
  titulosTorre(document);
})();

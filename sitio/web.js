// Babel Translations — el poco JavaScript que hace falta. La web funciona
// entera sin él (menús por :hover/:focus-within, formularios por POST normal);
// esto solo mejora el menú del móvil, el nombre del archivo adjunto, el aviso
// tras enviar un formulario y la aparición suave al hacer scroll.
(function () {
  document.documentElement.classList.add("js");

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
      var sub = b.nextElementSibling;
      var abierto = sub.classList.toggle("abierta");
      b.setAttribute("aria-expanded", abierto);
    });
  });

  // Nombre del archivo elegido
  document.querySelectorAll(".archivo input").forEach(function (input) {
    input.addEventListener("change", function () {
      var span = input.parentNode.querySelector("span");
      var nombres = Array.prototype.map.call(input.files, function (f) { return f.name; });
      span.textContent = nombres.length ? nombres.join(", ") : span.getAttribute("data-vacio");
    });
  });

  // Aviso tras enviar (enviar.php vuelve con ?enviado=ok o ?enviado=error)
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

  // Aparición suave
  if ("IntersectionObserver" in window) {
    var piezas = document.querySelectorAll(".pilar, .servicio, .tarjeta, .quienes");
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("visto"); obs.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -40px 0px" });
    piezas.forEach(function (p, i) {
      p.classList.add("aparece");
      p.style.transitionDelay = (i % 4) * 60 + "ms";
      obs.observe(p);
    });
  }
})();

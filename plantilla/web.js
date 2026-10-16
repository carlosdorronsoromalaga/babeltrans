// Babel Translations — el poco JavaScript que hace falta. La web funciona
// entera sin él (menús por :hover/:focus-within, formularios por POST normal);
// esto solo añade el menú del móvil y el aviso tras enviar un formulario.
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
})();

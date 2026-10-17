# babeltrans.es — web nueva

La web de Babel Translations (www.babeltrans.es), rehecha en octubre de 2026.

**Por qué:** la web original era un Joomla 1.5 de 2008. Cuando el hosting
(Webempresa) subió el servidor a PHP 8.5, dejó de funcionar: daba un error 500
con la página en blanco (comprobado el 13/10/2026). Joomla 1.5 solo funciona
con PHP 5.6, que el hosting está retirando y solo mantiene pagando el
«PHP Legacy Addon». En vez de pagar para seguir con un CMS sin parches desde
2012, la web pasa a ser **estática**: HTML + CSS, sin base de datos y sin nada
que actualizar, más un único `enviar.php` para los formularios.

**El contenido es el mismo.** Cada texto sale de la última versión publicada
de cada página (capturas de 2023-2024 de archive.org). Lo que cambia es el
diseño, la estructura del código y que ahora se ve bien en el móvil.

## Qué hay aquí

| Carpeta | Qué es |
|---|---|
| `original/` | La web vieja tal cual la guardó archive.org (313 ficheros). Solo lectura: es la fuente |
| `contenido/` | El texto de cada página en cada idioma, ya limpio (`es.json`, `en.json`, `de.json`, `nl.json`) |
| `plantilla/` | Estilos, JavaScript, favicon, `.htaccess` y `enviar.php` |
| `scripts/` | `descargar_wayback.py` → `extraer.py` → `construir.py` |
| `sitio/` | **La web lista para subir.** Se genera; no se edita a mano |

## Cómo se regenera

```bash
python3 scripts/descargar_wayback.py original    # solo si hay que volver a bajar la web vieja
python3 -m venv .venv && .venv/bin/pip install beautifulsoup4
.venv/bin/python scripts/extraer.py              # original/ -> contenido/
python3 scripts/construir.py                     # contenido/ + plantilla/ -> sitio/
```

Para verla en local:

```bash
cd sitio && python3 -m http.server 8765          # y abrir http://localhost:8765
```

(Los formularios no funcionan en local: necesitan PHP y correo, que sí hay en
el hosting.)

**Para cambiar un texto:** se edita en `contenido/<idioma>.json` y se vuelve a
lanzar `construir.py`. Los pocos rótulos que no venían de la web vieja
(«Leer más», «Menú»…) están en `scripts/textos_ui.py`.

## Qué cambia respecto a la original

- **Diseño nuevo, pensado para un traductor** (detalle en
  [`docs/DISENO.md`](docs/DISENO.md)): la portada es una edición paralela con la
  frase de la propia web en los cuatro idiomas, los servicios se presentan
  como entradas de diccionario y las páginas interiores tienen forma de página
  de libro, con notas al margen. Tinta azul sobre papel y el rojo del corrector.
  Tipografías Literata y Public Sans, alojadas en la propia web (licencia OFL).
- **Tres piezas del oficio** (v3):
  - *Alineación*: en la frase de la portada, al señalar una palabra se
    iluminan sus equivalentes en los otros tres idiomas, como en una
    herramienta de traducción asistida. En el móvil, con un toque.
  - *Literal frente a traducido*: un modismo traducido palabra por palabra,
    tachado en rojo, con la buena traducción corregida encima. Ilustra la frase
    de la propia web sobre evitar las traducciones demasiado literales. Está en
    la portada y en la página de traducción.
  - *La torre de Babel*: «traducción» en 36 idiomas y alfabetos, en pisos cada
    vez más anchos. Al señalar una palabra se ve el nombre del idioma.
- **Se ve bien en el móvil.** La vieja tenía una «versión móvil» aparte.
- **Las mismas direcciones (URL).** `es/servicios-traducciones.html` sigue
  siendo `es/servicios-traducciones.html`: Google y los enlaces de otras webs
  siguen llegando. Las URL todavía más antiguas (2013-2017) redirigen a su
  página equivalente (`.htaccess`, 92 reglas generadas solas).
- **Formularios** (presupuestos, contacto, trabaja con nosotros, CV, CP):
  conservan los mismos campos, pero ahora los recibe `enviar.php` (PHP 8) y
  llegan por e-mail a info@babeltrans.es con los archivos adjuntos. El captcha
  de imagen se cambia por un campo trampa invisible para los robots.
- **Se quita**: el acceso de usuarios y el registro (no se usaban), el buscador,
  las fotos de 110 px y el pase de diapositivas.
- **SEO básico**: `sitemap.xml`, `robots.txt`, etiquetas `hreflang` entre los 4
  idiomas, descripción por página y dirección canónica.
- **Sin cookies ni servicios de terceros**: las fuentes están en la propia web
  y no hay analítica, así que no hace falta banner de cookies.

## Pendiente de revisar con Martijn

Estas cosas son **así en la web original**. No las he tocado porque cambiarlas
sería cambiar el contenido, pero conviene decidirlas antes de publicar:

1. **Dos teléfonos distintos.** En castellano sale el **91 504 77 74** y en
   inglés y alemán el **91 314 79 19**. En holandés no sale ninguno. ¿Cuál es el
   bueno?
2. **Textos sin traducir.** La portada holandesa tenía el título en castellano
   (se usa el subtítulo holandés en su lugar), y la página de formación en
   holandés («Seminars in het Engels») tiene todo el texto en castellano.
3. **Fechas viejas.** Los seminarios en inglés y alemán dicen «throughout
   2011» e «in 2011».
4. **Textos legales anticuados.** El aviso legal y la política de privacidad
   citan la Ley 15/1999 (LOPD), sustituida por el RGPD y la LOPDGDD de 2018.
   Habría que actualizarlos.
5. **CV y CP.** Hay dos páginas en el menú, «CV» y «CP», que son formularios
   para subir un currículum y una carta para traducirlos. ¿Siguen ofreciéndose?
6. **Contenido nuevo para revisar.** Los modismos de «literal frente a
   traducido» y las palabras de la torre de Babel no estaban en la web vieja.
   Están en `scripts/textos_ui.py` (`MODISMOS`, `TORRE`) para cambiarlos o
   quitarlos. Conviene que un nativo revise los de alemán y holandés.
7. **Correo del remitente.** `enviar.php` manda los mensajes desde
   `web@babeltrans.es`. Conviene que esa dirección exista, o cambiarla por
   otra del dominio, para que los correos no acaben en spam.

## Cómo se publica (Webempresa)

1. **Copia de seguridad** de lo que hay ahora en el hosting (desde cPanel:
   ficheros y base de datos). Así no se pierde nada.
2. Dejar el PHP en **8.2 o superior** (el actual 8.5 vale). Ya no hace falta
   el PHP Legacy Addon.
3. Mover la web vieja a una carpeta aparte (p. ej. `public_html/_joomla_viejo/`)
   y subir **el contenido** de `sitio/` a `public_html/`, incluido el
   `.htaccess` (es un fichero oculto).
4. Probar un formulario de verdad y comprobar que llega el correo.
5. Cuando todo funcione, borrar la carpeta de Joomla y su base de datos.

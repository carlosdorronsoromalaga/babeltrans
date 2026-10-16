# Qué se miró antes de construir (16/10/2026)

**Bajar la web de archive.org.** La herramienta de referencia es
`hartator/wayback-machine-downloader` (Ruby, MIT, la más conocida). No se usó
por tres motivos: necesita Ruby, que no está en esta máquina; lleva años sin
mantenimiento; y aquí había que hacer cosas a medida, como quedarse con la
captura más reciente de cada URL, descartar el ruido de Joomla (registro de
usuarios, feeds, captchas) y descomprimir las capturas guardadas en gzip.
Sale un script de 70 líneas con la biblioteca estándar
(`scripts/descargar_wayback.py`) que usa la API CDX y el sufijo `id_` para
bajar cada página en crudo.

**Generar la web.** Se valoraron Hugo y Eleventy. Se descartaron porque son 84
páginas con 6 plantillas y el hosting es un FTP: un generador obliga a quien
mantenga la web a instalar Go o Node. `scripts/construir.py` solo usa la
biblioteca estándar de Python. BeautifulSoup se necesita únicamente para
extraer el contenido de la web vieja, una vez.

**Formularios.** Formspree, Netlify Forms y similares mandan los datos de los
clientes (y sus documentos) a un tercero fuera de la UE y tienen límites en el
plan gratuito. El hosting ya tiene PHP y correo, así que basta un `enviar.php`
propio.

**Diseño (v2).** En GitHub, las plantillas de «translation agency» (la mejor
tenía 4 estrellas) y las editoriales de html5up y sus versiones para
Hugo/Astro son genéricas: habrían devuelto la web a lo mismo que se quería
dejar atrás. Lo que sí sirvió fue la guía `frontend-design` de anthropics/skills,
que enumera los tics de las webs generadas (crema con terracota, el kit de
tarjetas con sombra, etiquetas en mayúsculas, flechas → y animaciones en cada
bloque) y propone sacar el diseño del vocabulario del propio oficio. De ahí
sale `DISENO.md`.

**Fuentes.** Google Fonts se descartó: incrustarlo en una web europea manda la
IP del visitante a Google (sentencia del LG München, 20/01/2022). Literata y
Public Sans (OFL) se alojan en `plantilla/fuentes/`: se bajaron de
`@fontsource-variable` en jsDelivr, solo el juego de caracteres latino, que
cubre castellano, inglés, alemán y holandés. Pesan 250 KB entre las tres.

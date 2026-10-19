# SEO y GEO: que la encuentren Google y los asistentes de IA

**Prioridad número uno de la web** (Carlos, 19/10/2026). SEO es aparecer en
Google; GEO (*generative engine optimization*) es que ChatGPT, Claude,
Perplexity o Gemini la conozcan y la citen cuando alguien les pregunta «¿quién
me hace una traducción jurada en Madrid?».

## Lo que ya hace la web (y comprueba el generador)

**Estructura**
- **Las mismas direcciones que la web vieja**, y las antiguas (2013-2017) con
  redirección 301 a su equivalente. Es lo más valioso: conserva la
  antigüedad y los enlaces que Google ya conoce de babeltrans.es desde 2013.
- Un solo `<h1>` por página, títulos con jerarquía y texto real (no imágenes).
- `<html lang>` correcto en cada idioma y **hreflang** entre las cuatro
  versiones de cada página, más `x-default` → castellano.
- **Dirección canónica** en cada página. Las páginas puente sin contenido
  propio («Solicite presupuesto», «Trabaja con nosotros») llevan `noindex,
  follow`, para que Google no las vea como contenido pobre.
- Página 404 propia; «Mapa web» retirado (lo sustituye `sitemap.xml`).

**Etiquetas**
- **Título y descripción escritos para buscar** en las páginas que más se
  buscan, en los cuatro idiomas (`SEO` en `scripts/textos_ui.py`): portada,
  traducción, interpretación, presupuestos, quiénes somos y contacto. El resto
  usa su título y su primer párrafo. El generador comprueba que ninguna
  descripción baje de 50 caracteres ni pase de 165, y que ningún título pase
  de 70.
- **Open Graph y Twitter** con imagen propia (`img/compartir.png`, 1200×630):
  así se ve la web al compartirla en WhatsApp, LinkedIn o redes.

**Datos estructurados (schema.org, JSON-LD)**, en todas las páginas:
- `ProfessionalService`: nombre, logo, contacto, Madrid, fundación (1999),
  idiomas y catálogo de servicios (técnica, jurídica, jurada, comercial,
  económica, revisión, transcripción; interpretación consecutiva, simultánea,
  jurada, por videoconferencia; locuciones).
- `WebSite` con los cuatro idiomas.
- `Service` en las páginas de traducción e interpretación.
- `BreadcrumbList` (migas) en las páginas interiores.

**Archivos para buscadores e IA**
- `sitemap.xml` con prioridades y, en cada URL, sus versiones en los otros
  idiomas.
- `robots.txt` abierto a todo, y explícitamente a los rastreadores de IA:
  GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot,
  PerplexityBot, Google-Extended y Applebot-Extended.
- **`llms.txt`**: resumen en texto llano de quién es Babel Translations, qué
  hace y sus páginas principales (propuesta llmstxt.org). Es lo que un
  asistente lee para responder con datos correctos.

**Velocidad y calidad** (Google lo mide): web estática, sin bases de datos ni
programas de terceros; fuentes propias precargadas; imágenes con tamaño
declarado; CSS y JS con caché larga y huella de versión; HTML siempre fresco;
apta para móvil.

## Lo que hay que hacer al publicar (no depende del código)

1. **Google Search Console**: dar de alta `https://www.babeltrans.es`, enviar
   `sitemap.xml` y revisar a las dos semanas que las páginas están indexadas
   y las redirecciones funcionan.
2. **Bing Webmaster Tools**: lo mismo (importando desde Search Console, dos
   clics). Bing alimenta ChatGPT y Copilot.
3. **Perfil de empresa en Google (Google Business Profile)**: lo que más pesa
   para «traductor en Madrid». Nombre, dirección, teléfono **idénticos** a los
   de la web (cuando estén en `empresa.json`), categoría «Servicio de
   traducción», horario, fotos y la web. Pedir reseñas a clientes contentos.
4. **El mismo nombre, dirección y teléfono en todas partes**: directorios
   (Páginas Amarillas, colegios o asociaciones de traductores como ASETRAD o
   APTIC si son miembros, LinkedIn). La incoherencia de teléfonos de la web
   vieja (dos números) es justo lo que hay que evitar.

## Lo que más subiría el posicionamiento (necesita a Martijn)

Por orden de impacto:
1. **Página de traducción jurada**: es lo más buscado del sector y ya la
   ofrecen. Necesito idiomas, plazos, cómo se entrega (papel, firma
   electrónica), precio orientativo o por qué varía, y la lista de documentos
   habituales (títulos, partidas de nacimiento, escrituras, poderes).
2. **Preguntas frecuentes reales** (¿cuánto tarda?, ¿cómo se calcula el
   precio?, ¿qué formatos aceptan?, ¿hacen urgencias?). Se marcan con
   `FAQPage` y es el contenido que más citan los asistentes de IA. Con sus
   respuestas, no inventadas.
3. **Una página por idioma o par de idiomas fuerte** («traducción jurada de
   inglés», «traductor de neerlandés en Madrid»), solo de los que trabajen de
   verdad.
4. **Reseñas** en Google y, con permiso, clientes o sectores en la web.
5. **Más idiomas de la web** (francés, italiano, portugués…): el selector y el
   generador ya escalan solos, basta con el contenido traducido. Siendo
   traductores, es un escaparate y abre búsquedas en esos idiomas.

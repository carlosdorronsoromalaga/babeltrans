# Pendientes antes de publicar

La web no se puede empaquetar mientras falte algo del primer bloque:
`scripts/empaquetar.sh` se niega y lo dice. El resto son decisiones que
mejoran la web pero no la bloquean.

## 1. Datos que solo tiene Martijn (bloquean la publicación)

Van en `contenido/empresa.json`. La ley (LSSI, art. 10) obliga a que el aviso
legal identifique al titular, y la web vieja no lo hacía.

| Dato | Para qué | Nota |
|---|---|---|
| Titular | Aviso legal, privacidad, formularios | Nombre fiscal: la persona si es autónomo, o la razón social si es sociedad |
| NIF | Aviso legal, privacidad | |
| Domicilio | Aviso legal, privacidad | La web vieja daba **dos**: Villa de Marín 26 (28029) y Luis Martínez Feduchi 74 (28055) |
| Registro Mercantil | Aviso legal | Solo si es sociedad (tomo, folio, hoja) |
| Teléfono | Toda la web | La vieja tenía **dos**: 91 504 77 74 (castellano) y 91 314 79 19 (inglés y alemán) |
| Ubicación de los servidores | Privacidad | Preguntar a Webempresa (¿UE?) |

## 2. Decisiones de contenido

1. **Formación en inglés.** La página «Consultoría de formación en inglés»
   habla de seminarios «throughout 2011» (inglés) e «in 2011» (alemán), y en
   holandés está en castellano. Se ha quitado de la portada y sigue existiendo
   solo para los enlaces viejos. ¿Se sigue ofreciendo? Si no, se retira como
   CV y CP.
2. **Textos sin traducir en holandés**: el título de la portada y la página
   de formación.
3. **Revisar las traducciones nuevas.** Son traductores: que revisen las
   versiones en inglés, alemán y holandés del aviso legal y la privacidad
   (`contenido/legal/`), los refranes de «literal frente a traducido» y los
   rótulos nuevos (`scripts/textos_ui.py`).
4. **Idiomas reales.** La web dice «todos los idiomas». Una lista de los pares
   de idiomas con los que trabajan de verdad vende más que la torre de Babel
   sola.

## 3. Hecho el 18/10/2026

- **Logo original**, sin retocar, en una cabecera oscura como la de la web
  vieja. Se ve algo borroso en pantallas de alta densidad porque el original
  mide 640×73 px. **Pedir a Martijn el archivo original del logo** (.ai, .eps,
  .svg o .pdf, del diseñador o de la imprenta): con él se ve nítido en
  cualquier pantalla.
- **Aviso legal y política de privacidad reescritos** según la normativa
  vigente (LSSI-CE, RGPD y LOPDGDD), en los 4 idiomas. La versión vieja citaba
  la Ley 15/1999, derogada en 2018, y no identificaba al titular.
- **Información básica de protección de datos bajo cada formulario**, como
  recomienda la AEPD: responsable, finalidad, legitimación, destinatarios,
  derechos y enlace a la política.
- **Sin cookies ni rastreo**, así que no hace falta banner de cookies. Si un
  día se añade Google Analytics o similar, entonces sí: banner con opción de
  rechazar y política de cookies.
- **CV y CP retirados.** Eran una campaña de hacia 2015 para traducir
  currículums y cartas de presentación. Sus direcciones redirigen al
  presupuesto de traducción.
- **«Trabaja con nosotros» se queda**: una agencia vive de su red de
  traductores. Sale en la portada y en el pie, y su formulario de candidatura
  tiene su propia información de privacidad (consentimiento, un año de
  conservación).
- **«Mediación»** se había quedado sin enlaces; ahora está en la sección de
  Servicios.
- **El «Mail: Esta dirección electrónica está protegida contra spam bots…»**
  de Joomla ha desaparecido. El generador falla si vuelve a aparecer ese texto
  o la ley de 1999.
- **Página 404** propia, con las secciones de los cuatro idiomas.
- **Datos estructurados** (schema.org) para que Google muestre bien el
  nombre, el teléfono y el correo.

## 4. Lo legal que no es la web (para Martijn)

- **Contrato de encargado del tratamiento con Webempresa** (hosting y correo).
  Suelen incluirlo en sus condiciones; basta con comprobarlo y guardarlo.
- **Acuerdos de confidencialidad con los traductores colaboradores**, que
  acceden a documentos de clientes. La política de privacidad lo da por hecho.
- **Registro de actividades de tratamiento**: obligatorio en la práctica si
  tratan datos de clientes de forma habitual. La herramienta gratuita
  *Facilita RGPD* de la AEPD lo genera en diez minutos.
- Accesibilidad: la Ley 11/2023 (Acta Europea de Accesibilidad) exime a las
  microempresas que prestan servicios. Aun así, la web cumple lo básico:
  contraste, teclado, textos alternativos y movimiento reducido.

*Nota: esto es una adaptación razonable a la normativa, no un dictamen. Si
quieren tranquilidad total, que un abogado o una gestoría revise
`contenido/legal/es.txt` una vez rellenados los datos.*

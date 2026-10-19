"""Genera la web nueva en sitio/ a partir de contenido/<idioma>.json.

Web estática (HTML + CSS + un poco de JS) más un único enviar.php para los
formularios. Sin Joomla, sin base de datos y sin nada que actualizar: lo que
tumbó la web vieja fue precisamente un CMS de 2008 que dejó de funcionar al
subir PHP.

Las rutas son LAS MISMAS que tenía la web original (es/servicios-traducciones.html,
en/services/translation.html...), para que los enlaces de Google y de otras webs
sigan llegando. Las rutas antiguas que ya no existían en 2024 se redirigen con
.htaccess.

Uso:  python3 scripts/construir.py        (solo biblioteca estándar)
"""
import datetime, html, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textos_ui import (UI, UI2, UI3, UI4, ENTRADAS, RETOQUES, ALINEACION, MODISMOS,  # noqa: E402
                       INFO_FORM, LEMA, PALABRAS_TORRE, NOMBRES_IDIOMA, UI5, SEO)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONT = os.path.join(RAIZ, "contenido")
PLANT = os.path.join(RAIZ, "plantilla")
SALIDA = os.path.join(RAIZ, "sitio")
DOMINIO = "https://www.babeltrans.es"
IDIOMAS = ["es", "en", "de", "nl"]
ANIO = datetime.date.today().year

esc = html.escape


# Páginas que se retiran (18/10/2026): «CV» y «CP» eran una campaña de hacia
# 2015 para traducir currículums y cartas de presentación, con su propio
# formulario. Ya no tenían sentido como apartados del menú: sus direcciones
# redirigen al presupuesto de traducción, que cubre lo mismo.
RETIRADAS = {"cv": "presupuesto-traduccion", "cp": "presupuesto-traduccion", "mapa": "home"}
# «Mapa web» (19/10/2026): Google y los asistentes usan sitemap.xml; la página
# HTML solo repetía el menú.

# Huella de cada fichero en su URL (?v=...): sin ella, el navegador sigue
# usando la hoja de estilos vieja que tiene guardada y la web se ve rota
# (pasó el 18/10/2026: cabecera clara con el logo blanco encima).
import hashlib  # noqa: E402
VERSION = {f: hashlib.sha1(open(os.path.join(PLANT, f), "rb").read()).hexdigest()[:8]
           for f in ("estilos.css", "web.js")}

EMPRESA = json.load(open(os.path.join(CONT, "empresa.json"), encoding="utf-8"))
PENDIENTES = set()


def dato(clave):
    """Un dato legal de la empresa, o una marca [PENDIENTE] bien visible."""
    v = EMPRESA.get(clave)
    if v is None:
        PENDIENTES.add(clave)
        return f'<mark class="pendiente">[PENDIENTE: {clave}]</mark>'
    if clave == "telefono":
        return f'<a href="tel:{v}">{tel_bonito(v)}</a>'
    if clave == "email":
        return f'<a href="mailto:{v}">{v}</a>'
    return esc(v)


def rellena(texto):
    return re.sub(r"\{\{(\w+)\}\}", lambda m: dato(m.group(1)), texto)


def carga():
    todo = {l: json.load(open(os.path.join(CONT, f"{l}.json"), encoding="utf-8")) for l in IDIOMAS}
    for d in todo.values():
        rutas_fuera = {d["paginas"][pid]["ruta"] for pid in RETIRADAS}
        d["menu"] = [it for it in d["menu"] if it["ruta"] not in rutas_fuera]
        d["pie"] = [x for x in d["pie"] if x["ruta"] not in rutas_fuera]
        for pid in RETIRADAS:
            d["paginas"].pop(pid)
    return todo


def retoca(t):
    for a, b in RETOQUES.items():
        t = t.replace(a, b)
    return t


def url(ruta):
    """Ruta interna -> URL absoluta desde la raíz del sitio."""
    if ruta in ("", "es.html"):
        return "/"
    if ruta.startswith(("http", "mailto:", "tel:")):
        return ruta
    return "/" + ruta


def enlaces(html_txt):
    return re.sub(r'href="(?!https?:|mailto:|tel:|/)([^"]*)"', lambda m: f'href="{url(m.group(1))}"', html_txt)


def contacto(d):
    """Teléfono y e-mail. Si empresa.json ya tiene teléfono, ese para toda la
    web; si no, el que aparecía en la página de contacto de ese idioma."""
    if EMPRESA.get("telefono"):
        return EMPRESA["telefono"], EMPRESA.get("email") or "info@babeltrans.es"
    f = d["paginas"]["contacto"]["formulario"]
    texto = " ".join(f["intro"] + f["datos"])
    tel = re.search(r"Tel\.?:?\s*([+\d][\d ]{8,})", texto)
    mail = re.search(r"[\w.]+@[\w.]+\.\w+", texto)
    tel = re.sub(r"\s", "", tel.group(1)) if tel else ""
    if tel and not tel.startswith("+"):
        tel = "+34" + tel
    return tel, (mail.group(0) if mail else "info@babeltrans.es")


def tel_bonito(tel):
    t = tel.replace("+34", "")
    return f"+34 {t[:2]} {t[2:5]} {t[5:7]} {t[7:]}" if len(t) == 9 else tel


def nombre_pagina(d, pid):
    """El nombre con el que la página salía en el menú; si no, su título."""
    p = d["paginas"][pid]
    for item in d["menu"]:
        for x in [item] + item["hijos"]:
            if x["ruta"] == p["ruta"]:
                return x["texto"]
    for x in d["pie"]:
        if x["ruta"] == p["ruta"]:
            return x["texto"]
    return p["titulo"] or re.sub(r"\s*-\s*babeltrans$", "", p.get("titulo_html", ""))


# --------------------------------------------------------------- piezas
# Diseño v2: ver docs/DISENO.md. Sin iconos ni tarjetas: el texto manda.

def sin_tags(t):
    return re.sub(r"<[^>]+>", "", t).strip()


def caso(t):
    """«MetHOdologIE:», «ARBEITSWEISE:», «tools:» -> «Methodologie», «Arbeitsweise», «Tools».

    Eran mayúsculas y minúsculas de adorno de Joomla (una letra de otro color),
    no parte del texto. Solo se toca si el texto está claramente roto.
    """
    t = t.strip().rstrip(":").strip()
    if re.search(r"[a-zäöüéíóú][A-ZÄÖÜ]", t) or (t.isupper() and len(t) > 3) or t[:1].islower():
        return t[:1].upper() + t[1:].lower()
    return t


def home_url(d):
    return "/" if d["idioma"] == "es" else url(d["paginas"]["home"]["ruta"])


def bloques_html(bloques, lang, pid):
    sal = []
    for tipo, cont in bloques:
        if tipo in ("ul", "ol"):
            items = "".join(f"<li>{enlaces(retoca(i))}</li>" for i in cont)
            sal.append(f'<{tipo} class="lista">{items}</{tipo}>')
            continue
        cont = enlaces(retoca(re.sub(r"\s*<br>\s*(</a>)?\s*$", r"\1", cont)))
        cont = re.sub(r"<br>\s*</a>", "</a>", cont)
        texto = sin_tags(cont)
        if tipo == "cita" or (tipo == "h3" and texto[:1] in "\"“"):
            if pid == "quienes" and lang != "es":
                # En los otros idiomas esta frase estaba SIN traducir y en blanco
                # sobre blanco (era el pie de una foto): nadie la veía.
                continue
            sal.append(f'<blockquote class="cita"><p>{esc(texto.strip(chr(34) + "“”"))}</p></blockquote>')
        elif tipo == "h3":
            if "<a " in cont:
                sal.append(f"<h2>{cont}</h2>")
            else:
                sal.append(f"<h2>{esc(caso(texto))}</h2>")
        else:
            sal.append(f"<p>{cont}</p>")
    return "\n".join(sal)


def menu_html(d, actual):
    items = []
    for it in d["menu"]:
        activo = any(x["ruta"] == actual for x in [it] + it["hijos"])
        cls = ' class="activo"' if activo else ""
        if it["hijos"]:
            sub = "".join(f'<li><a href="{url(h["ruta"])}"{" aria-current=page" if h["ruta"] == actual else ""}>'
                          f'{esc(h["texto"])}</a></li>' for h in it["hijos"])
            items.append(f'<li{cls}><a href="{url(it["ruta"])}">{esc(it["texto"])}</a>'
                         f'<button class="sub-abrir" aria-expanded="false" aria-label="{esc(it["texto"])}">'
                         f'<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
                         f'</button><ul class="sub">{sub}</ul></li>')
        else:
            items.append(f'<li{cls}><a href="{url(it["ruta"])}"'
                         f'{" aria-current=page" if it["ruta"] == actual else ""}>{esc(it["texto"])}</a></li>')
    return "".join(items)


def ruta_en(todo, l, pid):
    return "/" if (l == "es" and pid == "home") else url(todo[l]["paginas"][pid]["ruta"])


def selector_idioma(todo, lang, pid):
    """Selector de idioma desplegable. Escala solo: sale de IDIOMAS."""
    opciones = "".join(
        f'<li><a href="{ruta_en(todo, l, pid)}" hreflang="{l}" lang="{l}" data-idioma="{l}"'
        f'{" aria-current=true" if l == lang else ""}><span class="sel-nombre">{NOMBRES_IDIOMA[l]}</span>'
        f'<span class="sel-codigo">{l}</span></a></li>' for l in IDIOMAS)
    return (f'<div class="selector" data-selector>'
            f'<button class="selector-boton" type="button" aria-expanded="false" aria-haspopup="true" '
            f'aria-label="{esc(UI5[lang]["idioma"])}: {NOMBRES_IDIOMA[lang]}">'
            f'<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8"/>'
            f'<path d="M2 10h16M10 2c2.5 2.2 3.8 5 3.8 8s-1.3 5.8-3.8 8M10 2C7.5 4.2 6.2 7 6.2 10s1.3 5.8 3.8 8"/></svg>'
            f'<span class="selector-actual">{NOMBRES_IDIOMA[lang]}</span>'
            f'<svg class="selector-flecha" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3"/></svg>'
            f'</button><ul class="selector-lista">{opciones}</ul></div>')


# Barrido de traducción al cambiar de idioma (View Transitions entre páginas).
# Va en línea en el <head> porque «pagereveal» salta antes del primer pintado:
# un script diferido llegaría tarde. Solo anima si se vino desde el selector.
SCRIPT_BARRIDO = """<script>
addEventListener("pagereveal", function (e) {
  var de = null;
  try { de = sessionStorage.getItem("traduciendo"); sessionStorage.removeItem("traduciendo"); } catch (x) {}
  if (!e.viewTransition) return;
  if (!de || matchMedia("(prefers-reduced-motion: reduce)").matches) { e.viewTransition.skipTransition(); return; }
  var r = document.documentElement;
  r.classList.add("traduciendo");
  r.style.setProperty("--ruta", JSON.stringify(de + " \u2192 " + r.lang));
  e.viewTransition.finished.finally(function () { r.classList.remove("traduciendo"); });
});
</script>"""


def pagina(todo, lang, pid, cuerpo, titulo, descripcion, clase="", indexar=True, extra_head=""):
    d = todo[lang]
    ui = UI[lang]
    ruta = d["paginas"][pid]["ruta"]
    tel, mail = contacto(d)
    alternas = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}{ruta_en(todo, l, pid)}">'
                       for l in IDIOMAS)
    alternas += f'<link rel="alternate" hreflang="x-default" href="{DOMINIO}{ruta_en(todo, "es", pid)}">'
    trabaja = d["paginas"]["trabaja"]
    pie_links = (f'<li><a href="{url(trabaja["ruta"])}">{esc(nombre_pagina(d, "trabaja"))}</a></li>'
                 + "".join(f'<li><a href="{url(x["ruta"])}">{esc(x["texto"])}</a></li>' for x in d["pie"]))
    copy = d["paginas"]["home"]["home"]["copyright"].replace("2024", str(ANIO))
    canon = DOMINIO + ruta_en(todo, lang, pid)
    og_locale = {"es": "es_ES", "en": "en_GB", "de": "de_DE", "nl": "nl_NL"}
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
{'' if indexar else '<meta name="robots" content="noindex, follow">'}
<link rel="canonical" href="{canon}">
{alternas}
<meta property="og:site_name" content="Babel Translations">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="{og_locale[lang]}">
<meta property="og:image" content="{DOMINIO}/img/compartir.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1a1f36">
{datos_estructurados(todo, lang, pid)}
{extra_head}
<link rel="icon" href="/favicon.ico" sizes="16x16">
<link rel="preload" href="/fuentes/literata-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/estilos.css?v={VERSION["estilos.css"]}">
{SCRIPT_BARRIDO}
<script src="/web.js?v={VERSION["web.js"]}" defer></script>
</head>
<body class="{clase}">
<a class="saltar" href="#contenido">{ui["saltar"]}</a>
<div class="linea-traduccion" aria-hidden="true"><span>{esc(UI5[lang]["traduciendo"])}</span></div>
<header class="cabecera">
  <div class="env cabecera-in">
    <a class="marca" href="{home_url(d)}">
      <span class="globos" aria-hidden="true"><span class="globo globo-1"></span><span class="globo globo-2"></span></span>
      <span class="marca-textos">
        <img class="marca-nombre" src="/img/logo-nombre.png" width="222" height="20" alt="Babel Translations">
        <span class="marca-lema">{esc(LEMA[lang])}</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="{ui["menu"]}"><ul class="nav-lista">{menu_html(d, ruta)}</ul></nav>
    {selector_idioma(todo, lang, pid)}
    <button class="menu-abrir" aria-expanded="false" aria-controls="nav">{ui["menu"]}</button>
  </div>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie">
  <div class="env pie-in">
    <p class="pie-marca">Babel Translations</p>
    <address class="pie-contacto">
      {f'<a href="tel:{tel}">{tel_bonito(tel)}</a>' if tel else ''}
      <a href="mailto:{mail}">{mail}</a>
    </address>
    <ul class="pie-legal">{pie_links}</ul>
    <p class="pie-copy">{esc(copy)}</p>
  </div>
</footer>
</body>
</html>
"""


def seccion_de(d, pid):
    """El elemento del menú al que pertenece la página (para las notas al margen)."""
    ruta = d["paginas"][pid]["ruta"]
    for it in d["menu"]:
        if it["ruta"] == ruta or any(h["ruta"] == ruta for h in it["hijos"]):
            return it
    return None


def cabecera_pagina(d, pid, titulo, sub=""):
    sec = seccion_de(d, pid)
    if sec is None and pid == "mediacion":
        sec = seccion_de(d, "servicios")
    cab = (f'<a class="cabecera-seccion" href="{url(sec["ruta"])}">{esc(sec["texto"])}</a>'
           if sec and sec["ruta"] != d["paginas"][pid]["ruta"] else "")
    return (f'<header class="titulo-pagina"><div class="env libro">'
            f'<div class="margen">{cab}</div>'
            f'<div><h1>{esc(retoca(titulo))}</h1>{sub}</div></div></header>')


def notas_margen(d, pid, con_presupuesto=True, con_contacto=True):
    """Notas al margen: las páginas hermanas y cómo pedir presupuesto."""
    lang = d["idioma"]; P = d["paginas"]; ui2 = UI2[lang]
    tel, mail = contacto(d)
    sal = []
    sec = seccion_de(d, pid)
    if sec and sec["hijos"]:
        items = [sec] + sec["hijos"]
        if sec["ruta"] == P["servicios"]["ruta"]:
            # Mediación solo se enlazaba desde la portada vieja; sin esto se
            # quedaría huérfana.
            items = items + [{"ruta": P["mediacion"]["ruta"], "texto": P["mediacion"]["titulo"]}]
        lis = "".join(
            f'<li><a href="{url(x["ruta"])}"{" aria-current=page" if x["ruta"] == P[pid]["ruta"] else ""}>{esc(x["texto"])}</a></li>'
            for x in items)
        sal.append(f'<nav class="nota" aria-label="{esc(ui2["en_seccion"])}"><ul class="nota-lista">{lis}</ul></nav>')
    tel_html = f'<a href="tel:{tel}">{tel_bonito(tel)}</a><br>' if tel else ""
    if con_presupuesto:
        sal.append(f'''<div class="nota">
  <p class="nota-tit">{esc(nombre_pagina(d, "presupuesto"))}</p>
  <ul class="nota-lista">
    <li><a href="{url(P["presupuesto-traduccion"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto-traduccion"))}</a></li>
    <li><a href="{url(P["presupuesto-interpretacion"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto-interpretacion"))}</a></li>
  </ul>
  {f'<p class="nota-contacto">{tel_html}<a href="mailto:{mail}">{mail}</a></p>' if con_contacto else ''}
</div>''')
    return "\n".join(sal)


def descripcion_de(bloques, por_defecto):
    for t, c in bloques:
        if t == "p":
            txt = sin_tags(c)
            if len(txt) > 60:
                return txt[:155].rsplit(" ", 1)[0] + ("…" if len(txt) > 155 else "")
    return por_defecto


def parrafos(d, pid):
    """Los párrafos de una página, partidos también por los <br> de Joomla."""
    sal = []
    for t, c in d["paginas"][pid]["bloques"]:
        if t == "p":
            sal += [x.strip() for x in c.split("<br>") if sin_tags(x)]
    return sal


def primer_parrafo(d, pid):
    p = parrafos(d, pid)
    return sin_tags(p[0]) if p else ""


def entrada(todo, lang, pid, titulo_como="h3", completa=True):
    """Un servicio como entrada de diccionario."""
    d = todo[lang]; P = d["paginas"]
    palabra, afi, cat = ENTRADAS[lang][pid]
    lista = next((c for t, c in P[pid]["bloques"] if t == "ul"), [])
    acep = []
    for x in lista:
        x = sin_tags(retoca(x))
        if ":" in x and x.index(":") < 60:
            a, b = x.split(":", 1)
            acep.append(f"<li><b>{esc(a.strip())}.</b> {esc(b.strip())}</li>")
        else:
            acep.append(f"<li>{esc(x)}</li>")
    definicion = primer_parrafo(d, pid)
    return f"""<article class="entrada">
  <{titulo_como} class="entrada-palabra"><a href="{url(P[pid]["ruta"])}">{esc(palabra)}</a></{titulo_como}>
  <p class="entrada-gram"><span class="afi">{esc(afi)}</span> <i>{esc(cat)}</i></p>
  <p class="entrada-def">{esc(definicion)}</p>
  {f'<ol class="acepciones">{"".join(acep)}</ol>' if completa and acep else ''}
  <a class="enlace" href="{url(P[pid]["ruta"])}">{esc(retoca(P[pid]["titulo"]))}</a>
</article>"""


# --------------------------------------------------------------- piezas de traducción (v3)

def frase_alineada(lang):
    """La frase con cada trozo marcado para iluminar sus equivalentes."""
    def trozo(m):
        return f'<span class="seg" data-a="{m.group(2)}" tabindex="0">{esc(m.group(1))}</span>'
    partes = re.split(r"(\[[^|\]]+\|\d\])", ALINEACION[lang])
    return "".join(re.sub(r"\[([^|\]]+)\|(\d)\]", trozo, x) if x.startswith("[") else esc(x) for x in partes)


def paralelo(todo, lang):
    orden = [lang] + [l for l in IDIOMAS if l != lang]
    lineas = "".join(
        f'<li{" class=actual" if l == lang else ""}>'
        f'<a class="codigo" href="{ruta_en(todo, l, "home")}" hreflang="{l}" title="{UI[l]["idioma"]}"'
        f'{" aria-current=true" if l == lang else ""}>{l}</a>'
        f'<span class="frase" lang="{l}">{frase_alineada(l)}</span></li>'
        for l in orden)
    u = UI3[lang]
    return (f'<figure class="paralelo" data-alinear><ul>{lineas}</ul>'
            f'<figcaption class="pista"><span class="pista-raton">{esc(u["alinear"])}</span>'
            f'<span class="pista-tactil">{esc(u["alinear_tactil"])}</span></figcaption></figure>')


def modismo(d, lang):
    """Traducción literal tachada y la buena encima, como la corregiría un revisor."""
    u = UI3[lang]
    ejemplos = MODISMOS[lang]
    datos = esc(json.dumps(ejemplos, ensure_ascii=False))
    origen, orig, literal, bien = ejemplos[0]
    return f"""<figure class="modismo" data-modismos="{datos}">
  <p class="modismo-orig"><span class="codigo">{origen}</span> <q lang="{origen}">{esc(orig)}</q></p>
  <p class="modismo-fila"><span class="etq">{esc(u["literal"])}</span> <del lang="{lang}">{esc(literal)}</del></p>
  <p class="modismo-fila"><span class="etq">{esc(u["bien"])}</span> <ins lang="{lang}">{esc(bien)}</ins></p>
  <button type="button" class="modismo-otro">{esc(u["otro"])}</button>
</figure>"""


# Ancho de cada palabra de la torre en Literata, en centésimas de em (medido en
# Chrome el 19/10/2026). Con esto los pisos se reparten solos.
ANCHOS = {"es": 508, "en": 515, "de": 594, "nl": 421, "fr": 497, "it": 509, "pt": 417, "ca": 445, "eu": 438,
          "gl": 459, "la": 453, "el": 509, "ru": 376, "pl": 567, "ar": 199, "zh": 200, "ja": 200, "ko": 200,
          "hi": 272, "he": 265, "tr": 263, "da": 578, "fa": 199, "sw": 283, "fi": 392, "hu": 366, "cs": 357,
          "ro": 453, "uk": 434, "sv": 589, "vi": 403, "id": 540, "bn": 289, "bg": 327, "no": 550, "ga": 535,
          "th": 340, "hr": 389, "sk": 361, "sl": 327, "lt": 408, "lv": 475, "et": 232, "is": 320, "mt": 537,
          "cy": 497, "sq": 441, "hy": 829, "ka": 484, "ur": 211, "ta": 658, "tl": 493, "eo": 374, "am": 331,
          "zu": 617}
TORRE_LETRA = [52, 30, 25, 22, 20, 19, 18, 18, 17, 17, 17, 17]  # px por piso; debe casar con estilos.css
TORRE_HUECO = 22


def _ancho_piso(i, p):
    letra = TORRE_LETRA[min(i, len(TORRE_LETRA) - 1)]
    return sum(ANCHOS.get(l, 450) * letra / 100 for l, _ in p) + TORRE_HUECO * (len(p) - 1)


def _reparte(lang, inicio, paso):
    cima = next(x for x in PALABRAS_TORRE if x[0] == lang)
    resto = [x for x in PALABRAS_TORRE if x[0] != lang]
    pisos, i = [[cima]], 1
    while resto:
        letra = TORRE_LETRA[min(i, len(TORRE_LETRA) - 1)]
        piso, ancho = [], 0
        for x in list(resto):
            w = ANCHOS.get(x[0], 450) * letra / 100 + (TORRE_HUECO if piso else 0)
            if not piso or ancho + w <= inicio + paso * i:
                piso.append(x); ancho += w; resto.remove(x)
        pisos.append(piso); i += 1
    return pisos


def pisos_torre(lang, maximo=1080):
    """Reparte las palabras en pisos con la del idioma de la página en la cima.
    Prueba varios anchos de partida y de crecimiento y se queda con el reparto
    en que cada piso es más ancho que el de encima y la base cabe en la página
    (si ninguno lo cumple del todo, el que menos se aparta)."""
    mejor, nota_mejor = None, None
    for inicio in range(240, 420, 20):
        for paso in range(50, 130, 5):
            pisos = _reparte(lang, inicio, paso)
            anchos = [_ancho_piso(i, p) for i, p in enumerate(pisos)]
            fallos = sum(max(0, anchos[k - 1] - anchos[k] + 20) for k in range(2, len(anchos)))
            nota = (fallos + 10 * max(0, max(anchos) - maximo), abs(len(pisos) - 9))
            if nota_mejor is None or nota < nota_mejor:
                mejor, nota_mejor = pisos, nota
    return mejor


def torre(lang):
    """La torre de Babel: «traducción» en muchos idiomas."""
    pisos = pisos_torre(lang)
    html_pisos = "".join(
        f'<ul class="piso" style="--t:{TORRE_LETRA[min(i, len(TORRE_LETRA) - 1)]}">' + "".join(
            f'<li><span lang="{l}" dir="auto" tabindex="0" data-idioma="{l}">{esc(w)}</span></li>' for l, w in p)
        + "</ul>" for i, p in enumerate(pisos))
    total = sum(len(p) for p in pisos)
    u = UI3[lang]
    pie = re.sub(r"\d+", str(total), u["torre_pie"])
    return (f'<div class="torre" data-torre>{html_pisos}</div>'
            f'<p class="torre-pie" aria-live="polite" data-pie="{esc(pie)}">{esc(pie)}</p>')


# --------------------------------------------------------------- tipos de página

HUBS = {"servicios": ["traduccion", "interpretacion"],
        "presupuesto": ["presupuesto-traduccion", "presupuesto-interpretacion"],
        "trabaja": ["como-traductor", "como-interprete"]}


def pag_hub(todo, lang, pid):
    """Páginas que en la original eran solo dos enlaces."""
    d = todo[lang]; P = d["paginas"]
    titulo = nombre_pagina(d, pid)
    if pid == "servicios":
        dentro = f'<div class="entradas">{"".join(entrada(todo, lang, x, "h2") for x in HUBS[pid])}</div>'
    else:
        titulos = [sin_tags(c) for t, c in P[pid]["bloques"]]
        enl = "".join(
            f'<li><a href="{url(P[x]["ruta"])}">{esc(titulos[i] if i < len(titulos) else nombre_pagina(d, x))}</a></li>'
            for i, x in enumerate(HUBS[pid]))
        dentro = f'<ul class="indice">{enl}</ul>'
    cuerpo = cabecera_pagina(d, pid, titulo) + f"""
<section class="env libro cuerpo-pagina">
  <aside class="margen">{notas_margen(d, pid, pid != "presupuesto")}</aside>
  <div>{dentro}</div>
</section>"""
    if pid == "servicios":
        desc = SEO[lang]["home"][1]
    elif pid == "presupuesto":
        desc = SEO[lang]["presupuesto-traduccion"][1]
    else:
        desc = UI4[lang]["trabaja_txt"]
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations", desc, indexar=pid == "servicios")


def legal(lang, pid):
    """Título y bloques de un texto legal de contenido/legal/<idioma>.txt."""
    texto = open(os.path.join(CONT, "legal", f"{lang}.txt"), encoding="utf-8").read()
    trozo = texto.split(f"=== {pid}\n", 1)[1].split("\n=== ", 1)[0].strip().splitlines()
    titulo, bloques, lista = trozo[0], [], []
    for linea in trozo[1:] + [""]:
        linea = linea.strip()
        if linea.startswith("- "):
            lista.append(rellena(esc(linea[2:])))
            continue
        if lista:
            bloques.append(("ul", lista)); lista = []
        if not linea:
            continue
        if linea.startswith("## "):
            bloques.append(("h2", esc(linea[3:])))
        else:
            bloques.append(("p", rellena(esc(linea))))
    return titulo, bloques


def bloques_legal(bloques):
    sal = []
    for t, c in bloques:
        if t == "ul":
            sal.append('<ul class="lista">' + "".join(f"<li>{x}</li>" for x in c) + "</ul>")
        elif t == "h2":
            sal.append(f"<h2>{c}</h2>")
        elif c.strip():
            sal.append(f"<p>{c}</p>")
    return "\n".join(sal)


def pag_legal(todo, lang, pid):
    d = todo[lang]
    titulo, bloques = legal(lang, pid)
    cuerpo = cabecera_pagina(d, pid, titulo) + f"""
<section class="env libro cuerpo-pagina">
  <aside class="margen"></aside>
  <article class="prosa prosa-legal">
{bloques_legal(bloques)}
  </article>
</section>"""
    desc = next((sin_tags(c) for t, c in bloques if t == "p" and "PENDIENTE" not in c and len(sin_tags(c)) > 60), titulo)
    desc = desc[:155].rsplit(" ", 1)[0] + "…" if len(desc) > 155 else desc
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations", desc)


def seo(lang, pid, titulo, descripcion):
    """Título y descripción de SEO si la página los tiene; si no, los de siempre."""
    return SEO.get(lang, {}).get(pid, (titulo, descripcion))


def pag_articulo(todo, lang, pid):
    d = todo[lang]; p = d["paginas"][pid]
    titulo = p["titulo"] or nombre_pagina(d, pid)
    sub = ""
    if pid in ("traduccion", "interpretacion"):
        palabra, afi, cat = ENTRADAS[lang][pid]
        sub = f'<p class="entrada-gram titulo-gram">{esc(palabra)} <span class="afi">{esc(afi)}</span> <i>{esc(cat)}</i></p>'
    legal = pid in ("aviso-legal", "privacidad")
    cuerpo = cabecera_pagina(d, pid, titulo, sub) + f"""
<section class="env libro cuerpo-pagina">
  <aside class="margen">{"" if legal else notas_margen(d, pid)}</aside>
  <article class="prosa{" prosa-legal" if legal else ""}">
{bloques_html(p["bloques"], lang, pid)}
{modismo(d, lang) if pid == "traduccion" else ""}
  </article>
</section>"""
    return pagina(todo, lang, pid, cuerpo, *seo(lang, pid, f"{retoca(titulo)} · Babel Translations",
                                                descripcion_de(p["bloques"], retoca(titulo))))


def campo_html(c, ui, privacidad_url):
    nombre = c["nombre"]
    obligatorio = nombre.lower() in ("nombre", "persona", "mail", "privacidad")
    req = " required" if obligatorio else ""
    marca = f'<abbr class="req" title="{ui["obligatorio"]}">*</abbr>' if obligatorio else ""
    ide = f"f-{nombre.lower()}"
    etiqueta = esc(c["etiqueta"] or nombre.replace("_", " "))
    tipo = c["tipo"]
    if tipo == "checkbox":
        txt = re.sub(r"(Pol[ií]tica de privacidad|Privacy policy|Datenschutz\w*|Privacyverklaring|privacybeleid)",
                     lambda m: f'<a href="{privacidad_url}" target="_blank">{m.group(1)}</a>', etiqueta, flags=re.I)
        return (f'<div class="campo ancho campo-check"><input type="checkbox" id="{ide}" name="{nombre}" value="Sí"{req}>'
                f'<label for="{ide}">{txt} {marca}</label></div>')
    if tipo == "textarea":
        return (f'<div class="campo ancho"><label for="{ide}">{etiqueta} {marca}</label>'
                f'<textarea id="{ide}" name="{nombre}" rows="5"{req}></textarea></div>')
    if tipo == "select":
        # "Seleccione tipo" es un rótulo, no una respuesta: va con valor vacío
        vacio = ' value=""'
        ops = "".join(f'<option{vacio if j == 0 and len(c["opciones"]) > 2 else ""}>{esc(o)}</option>'
                      for j, o in enumerate(c["opciones"]))
        return (f'<div class="campo"><label for="{ide}">{etiqueta} {marca}</label>'
                f'<select id="{ide}" name="{nombre}">{ops}</select></div>')
    if tipo == "file":
        return (f'<div class="campo ancho"><label for="{ide}">{etiqueta}</label>'
                f'<input class="archivo" type="file" id="{ide}" name="{nombre}[]" multiple></div>')
    html_tipo = "email" if nombre.lower() == "mail" else "tel" if nombre.lower() == "telefono" else \
        "date" if nombre.lower() in ("fecha", "fecha_entrega") else "text"
    auto = {"nombre": "name", "persona": "name", "mail": "email", "telefono": "tel", "pais": "country-name",
            "poblacion": "address-level2", "empresa": "organization", "cp": "postal-code",
            "direccion": "street-address", "apellidos": "family-name"}.get(nombre.lower(), "off")
    return (f'<div class="campo"><label for="{ide}">{etiqueta} {marca}</label>'
            f'<input type="{html_tipo}" id="{ide}" name="{nombre}" autocomplete="{auto}"{req}></div>')


def pag_formulario(todo, lang, pid):
    d = todo[lang]; ui = UI[lang]; p = d["paginas"][pid]; f = p["formulario"]
    tel, mail = contacto(d)
    titulo = nombre_pagina(d, pid)
    intro = [t for t in f["intro"] if not t.startswith("BABELTRANS")]
    campos = "\n".join(campo_html(c, ui, url(d["paginas"]["privacidad"]["ruta"])) for c in f["campos"])
    gracias = f["gracias"] if f["gracias"] and not (lang != "es" and f["gracias"].startswith("Gracias")) else ui["enviado"]
    boton = f["boton"] if not (lang != "es" and f["boton"] == "Enviar") else ui["enviar"]
    margen = notas_margen(d, pid, pid not in ("presupuesto-traduccion", "presupuesto-interpretacion"),
                          con_contacto=pid != "contacto")
    if pid in ("presupuesto-traduccion", "presupuesto-interpretacion", "contacto"):
        margen += (f'<div class="nota"><p class="nota-contacto">'
                   f'{f"<a href=tel:{tel}>{tel_bonito(tel)}</a><br>" if tel else ""}<a href="mailto:{mail}">{mail}</a></p></div>'
                   if pid != "contacto" else "")
    cuerpo = cabecera_pagina(d, pid, titulo) + f"""
<section class="env libro cuerpo-pagina">
  <aside class="margen">{margen}</aside>
  <div class="columna-form">
    {"".join(f'<p class="entradilla">{esc(t)}</p>' for t in intro)}
    {f'<p class="contacto-grande"><a href="tel:{tel}">{tel_bonito(tel)}</a><a href="mailto:{mail}">{mail}</a></p>' if pid == "contacto" else ""}
    <div class="aviso aviso-ok" role="status" hidden data-aviso="ok"><p>{esc(gracias)}</p></div>
    <div class="aviso aviso-error" role="alert" hidden data-aviso="error"><p>{esc(ui["error"])} <a href="mailto:{mail}">{mail}</a></p></div>
    <form class="formulario" action="/enviar.php" method="post" enctype="multipart/form-data">
      <input type="hidden" name="_formulario" value="{esc(titulo)}">
      <input type="hidden" name="_idioma" value="{lang}">
      <input type="hidden" name="_volver" value="{url(p["ruta"])}">
      <div class="trampa" aria-hidden="true"><label>Web <input type="text" name="_web" tabindex="-1" autocomplete="off"></label></div>
      <div class="campos">
{campos}
      </div>
      <button class="boton" type="submit">{esc(boton)}</button>
      {info_privacidad(d, lang, pid)}
    </form>
  </div>
</section>"""
    return pagina(todo, lang, pid, cuerpo, *seo(lang, pid, f"{titulo} · Babel Translations",
                                                intro[0][:155] if intro else f"{titulo} · Babel Translations"))


def info_privacidad(d, lang, pid):
    i = INFO_FORM[lang]
    cand = pid in ("como-traductor", "como-interprete")
    filas = [
        (i["responsable"], dato("titular")),
        (i["finalidad"], esc(i["fin_candidatura" if cand else "fin_solicitud"])),
        (i["legitimacion"], esc(i["leg_candidatura" if cand else "leg_solicitud"])),
        (i["destinatarios"], esc(i["dest"])),
        (i["derechos"], f'{esc(i["der"])} {dato("email")}.'),
        (i["mas"], f'<a href="{url(d["paginas"]["privacidad"]["ruta"])}">{esc(i["ver"])}</a>.'),
    ]
    return (f'<details class="info-datos"><summary>{esc(i["tit"])}</summary><dl>'
            + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in filas) + "</dl></details>")


SERVICIOS_SCHEMA = {
    "traduccion": ["Traducción técnica", "Traducción jurídica", "Traducción jurada", "Traducción comercial",
                   "Traducción económica", "Revisión de textos", "Transcripciones"],
    "interpretacion": ["Interpretación consecutiva", "Interpretación simultánea", "Interpretación jurada",
                       "Interpretación por videoconferencia", "Locuciones"],
}


def datos_estructurados(todo, lang, pid):
    """schema.org: quién es el negocio (en todas las páginas), qué servicio es
    (en traducción e interpretación) y dónde está la página (migas). Es lo que
    leen Google y los asistentes de IA para entender y citar la web."""
    d = todo[lang]; P = d["paginas"]
    tel, mail = contacto(d)
    negocio = {"@type": "ProfessionalService", "@id": DOMINIO + "/#negocio",
               "name": "Babel Translations", "alternateName": "BABELTRANS",
               "url": DOMINIO + "/", "logo": DOMINIO + "/img/logo.png", "image": DOMINIO + "/img/compartir.png",
               "email": mail, "foundingDate": "1999",
               "description": SEO["es"]["home"][1],
               "knowsLanguage": [l for l, _ in PALABRAS_TORRE[:11]],
               "areaServed": "Worldwide",
               "address": {"@type": "PostalAddress", "addressLocality": "Madrid", "addressCountry": "ES"},
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Servicios lingüísticos",
                                   "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
                                                       for v in SERVICIOS_SCHEMA.values() for n in v]}}
    if tel:
        negocio["telephone"] = tel
    if EMPRESA.get("domicilio"):
        negocio["address"]["streetAddress"] = EMPRESA["domicilio"]
    grafo = [negocio, {"@type": "WebSite", "@id": DOMINIO + "/#web", "url": DOMINIO + "/",
                       "name": "Babel Translations", "inLanguage": IDIOMAS, "publisher": {"@id": DOMINIO + "/#negocio"}}]
    if pid in SERVICIOS_SCHEMA:
        grafo.append({"@type": "Service", "name": sin_tags(retoca(P[pid]["titulo"])),
                      "serviceType": SERVICIOS_SCHEMA[pid], "provider": {"@id": DOMINIO + "/#negocio"},
                      "areaServed": "Worldwide", "url": DOMINIO + url(P[pid]["ruta"]), "inLanguage": lang})
    if pid != "home" and pid in P:
        migas = [("Babel Translations", DOMINIO + home_url(d))]
        sec = seccion_de(d, pid)
        if sec and sec["ruta"] != P[pid]["ruta"]:
            migas.append((sec["texto"], DOMINIO + url(sec["ruta"])))
        migas.append((nombre_pagina(d, pid), DOMINIO + url(P[pid]["ruta"])))
        grafo.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(migas)]})
    datos = {"@context": "https://schema.org", "@graph": grafo}
    return f'<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False)}</script>'


def pag_404(todo):
    """Página de «no existe» en castellano con las secciones de cada idioma."""
    d = todo["es"]; u = UI4["es"]
    listas = "".join(
        f'<li lang="{l}"><a href="{ruta_en(todo, l, "home")}">{UI[l]["idioma"]}</a>: '
        + ", ".join(f'<a href="{url(it["ruta"])}">{esc(it["texto"])}</a>' for it in todo[l]["menu"][1:])
        + "</li>" for l in IDIOMAS)
    cuerpo = (f'<header class="titulo-pagina"><div class="env libro"><div class="margen"></div>'
              f'<div><h1>{esc(u["error404"])}</h1></div></div></header>'
              f'<section class="env libro cuerpo-pagina"><div class="margen"></div><div class="prosa">'
              f'<p>{esc(u["error404_txt"])}</p><ul class="lista">{listas}</ul></div></section>')
    return pagina(todo, "es", "home", cuerpo, u["error404"] + " · Babel Translations", u["error404"])


def pag_mapa(todo, lang, pid):
    d = todo[lang]
    items = []
    for it in d["menu"]:
        sub = "".join(f'<li><a href="{url(h["ruta"])}">{esc(h["texto"])}</a></li>' for h in it["hijos"])
        items.append(f'<li><a href="{url(it["ruta"])}">{esc(it["texto"])}</a>{f"<ul>{sub}</ul>" if sub else ""}</li>')
    titulo = d["paginas"][pid]["titulo"] or nombre_pagina(d, pid)
    cuerpo = cabecera_pagina(d, pid, titulo) + \
        f'<section class="env libro cuerpo-pagina"><div class="margen"></div><ul class="mapa">{"".join(items)}</ul></section>'
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations", titulo)


def pag_home(todo, lang):
    d = todo[lang]; ui = UI[lang]; ui2 = UI2[lang]; P = d["paginas"]; h = P["home"]["home"]
    tel, mail = contacto(d)
    titulos = h["titulos"]
    # La portada holandesa tenía el título principal sin traducir (en
    # castellano); su subtítulo sí estaba en holandés y hace de título.
    h1 = titulos[1].rstrip(":") if lang == "nl" else titulos[0]
    intro_lista = titulos[1].rstrip(":") if lang != "nl" and len(titulos) > 1 and titulos[1] != "Babeltrans" else ""
    # La frase de confidencialidad es la ÚLTIMA en mayúsculas (en inglés, la
    # primera era «SUPERB TECHNICAL AND SPECIALISED TRANSLATIONS:»)
    confid = next((x for x in reversed(h["fuertes"]) if x.isupper() and len(x) > 12 and not x.endswith(":")), "")
    confid = confid[:1] + confid[1:].lower()

    q = [sin_tags(x) for x in parrafos(d, "quienes")]
    lema = q[0] if q else ""
    resto_quienes = q[1] if len(q) > 1 else ""
    cita_q = next((c for t, c in P["quienes"]["bloques"] if t == "cita"), "") if lang == "es" else ""

    met = P["metodologia"]["bloques"]
    listas = [c for t, c in met if t == "ul"]
    pasos = "".join(f"<li>{esc(sin_tags(x))}</li>" for x in (listas[0] if listas else []))
    herramientas = "".join(f"<li>{esc(sin_tags(x).rstrip('.'))}</li>" for x in (listas[1] if len(listas) > 1 else []))
    met_intro = parrafos(d, "metodologia")
    met_intro = sin_tags(met_intro[1]) if len(met_intro) > 1 else ""

    lit = parrafos(d, "traduccion")
    lit = sin_tags(lit[1]) if len(lit) > 1 else ""
    cita_colab = next((sin_tags(c).strip('"“” ') for t, c in P["colaboradores"]["bloques"]
                       if sin_tags(c)[:1] in "\"“"), "")
    campos = "".join(f"<li>{esc(t.rstrip('.… ').rstrip('.'))}</li>" for t in h["lista"])

    cuerpo = f"""
<section class="portada">
  <div class="env portada-in">
    <div class="portada-txt">
      <h1>{esc(h1)}</h1>
      <p class="portada-lema">{esc(lema)}</p>
      <div class="botones">
        <a class="boton" href="{url(P["presupuesto"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto"))}</a>
        {f'<a class="boton boton-sec" href="tel:{tel}">{tel_bonito(tel)}</a>' if tel else f'<a class="boton boton-sec" href="mailto:{mail}">{mail}</a>'}
      </div>
    </div>
    {paralelo(todo, lang)}
  </div>
</section>

<section class="bloque">
  <div class="env libro">
    <p class="margen nota-margen">{esc(confid)}.</p>
    <div>
      {f'<h2 class="vh">{esc(intro_lista)}</h2>' if intro_lista else ''}
      <ul class="campos-lista">{campos}</ul>
    </div>
  </div>
</section>

<section class="bloque bloque-calco">
  <div class="env libro">
    <h2 class="margen tit-margen"><a href="{url(P["servicios"]["ruta"])}">{esc(nombre_pagina(d, "servicios"))}</a></h2>
    <div class="entradas">{entrada(todo, lang, "traduccion")}{entrada(todo, lang, "interpretacion")}</div>
  </div>
</section>

<section class="bloque bloque-modismo">
  <div class="env libro">
    <p class="margen nota-margen">{esc(lit)}</p>
    <div>{modismo(d, lang)}</div>
  </div>
</section>

<section class="bloque">
  <div class="env libro">
    <h2 class="margen tit-margen"><a href="{url(P["quienes"]["ruta"])}">{esc(nombre_pagina(d, "quienes"))}</a></h2>
    <div class="prosa">
      <p class="grande">{esc(resto_quienes)}</p>
      {f'<blockquote class="cita"><p>{esc(cita_q)}</p></blockquote>' if cita_q else ''}
    </div>
  </div>
</section>

<section class="bloque">
  <div class="env libro">
    <h2 class="margen tit-margen"><a href="{url(P["metodologia"]["ruta"])}">{esc(nombre_pagina(d, "metodologia"))}</a></h2>
    <div class="metodo">
      <div>
        <p class="metodo-intro">{esc(met_intro)}</p>
        <ol class="pasos">{pasos}</ol>
      </div>
      {f'<div class="herramientas"><h3>{esc(ui2["herramientas"])}</h3><ul>{herramientas}</ul></div>' if herramientas else ''}
    </div>
  </div>
</section>

<section class="bloque">
  <div class="env libro">
    <div class="margen"></div>
    <div class="dos">
      <div>
        <h2 class="tit-pequeno"><a href="{url(P["colaboradores"]["ruta"])}">{esc(nombre_pagina(d, "colaboradores"))}</a></h2>
        {f'<blockquote class="cita cita-pequena"><p>{esc(cita_colab)}</p></blockquote>' if cita_colab else ''}
        <p>{esc(primer_parrafo(d, "colaboradores"))}</p>
      </div>
      <div>
        <h2 class="tit-pequeno"><a href="{url(P["trabaja"]["ruta"])}">{esc(nombre_pagina(d, "trabaja"))}</a></h2>
        <p>{esc(UI4[lang]["trabaja_txt"])}</p>
        <ul class="indice indice-mini">
          <li><a href="{url(P["como-traductor"]["ruta"])}">{esc(sin_tags(P["trabaja"]["bloques"][0][1]))}</a></li>
          <li><a href="{url(P["como-interprete"]["ruta"])}">{esc(sin_tags(P["trabaja"]["bloques"][1][1]))}</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="bloque bloque-torre">
  <div class="env">
    <h2 class="tit-torre">{esc(UI3[lang]["torre"])}</h2>
    {torre(lang)}
  </div>
</section>

<section class="final">
  <div class="env libro">
    <h2 class="margen tit-margen">{esc(ui2["llame"])}</h2>
    <div>
      <p class="contacto-grande">{f'<a href="tel:{tel}">{tel_bonito(tel)}</a>' if tel else ''}<a href="mailto:{mail}">{mail}</a></p>
      <ul class="indice indice-pequeno">
        <li><a href="{url(P["presupuesto-traduccion"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto-traduccion"))}</a></li>
        <li><a href="{url(P["presupuesto-interpretacion"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto-interpretacion"))}</a></li>
      </ul>
    </div>
  </div>
</section>"""
    titulo, desc = seo(lang, "home", f"Babel Translations · {h1}", lema[:155])
    return pagina(todo, lang, "home", cuerpo, titulo, desc, "portada-pagina")


# --------------------------------------------------------------- redirecciones

def redirecciones(todo):
    """Rutas viejas (2013-2017) -> la página equivalente de la web nueva.

    Se casan por idioma y título de la página: la web vieja cambió de URLs dos
    veces (…-holandes en 2013, …-traducciones en 2017, y versiones sin prefijo
    de idioma) y Google aún puede tener alguna.
    """
    indice = json.load(open(os.path.join(RAIZ, "original", "_indice.json")))
    nuevas = {}
    for l in IDIOMAS:
        for pid, p in todo[l]["paginas"].items():
            nuevas[p["ruta"]] = (l, pid)
    por_titulo = {}
    for l in IDIOMAS:
        for pid, p in todo[l]["paginas"].items():
            por_titulo.setdefault((l, p.get("titulo_html", "")), p["ruta"])
    lineas = []
    vistas = set()
    for e in indice:
        f = e["fichero"]
        if e["mime"] != "text/html" or "__" in f or f in nuevas or f == "index.html" or not f.endswith(".html") or f in vistas:
            continue
        vistas.add(f)
        cab = open(os.path.join(RAIZ, "original", f), "rb").read(4000).decode("utf-8", "replace")
        lang = re.search(r'<html[^>]*lang="(\w\w)', cab)
        tit = re.search(r"<title>(.*?)</title>", cab, re.S)
        if not lang or not tit:
            continue
        destino = por_titulo.get((lang.group(1), html.unescape(re.sub(r"\s+", " ", tit.group(1)).strip())))
        if f.endswith(("/71.html", "/72.html")):
            destino = todo[lang.group(1)]["paginas"]["mediacion" if f.endswith("71.html") else "formacion"]["ruta"]
        if destino and destino != f:
            lineas.append(f"RedirectMatch 301 ^/{re.escape(f)}$ {url(destino)}")
    return lineas


# --------------------------------------------------------------- principal

def escribe(ruta, texto):
    destino = os.path.join(SALIDA, ruta)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(texto)


def main():
    todo = carga()
    if os.path.isdir(SALIDA):
        shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)
    for f in os.listdir(PLANT):
        origen = os.path.join(PLANT, f)
        if os.path.isdir(origen):
            shutil.copytree(origen, os.path.join(SALIDA, f))
        else:
            shutil.copy(origen, os.path.join(SALIDA, f))
    urls = []
    for lang in IDIOMAS:
        d = todo[lang]
        for pid, p in d["paginas"].items():
            if pid == "home":
                html_txt = pag_home(todo, lang)
            elif pid in ("aviso-legal", "privacidad"):
                html_txt = pag_legal(todo, lang, pid)
            elif pid in HUBS:
                html_txt = pag_hub(todo, lang, pid)
            elif "formulario" in p:
                html_txt = pag_formulario(todo, lang, pid)
            else:
                html_txt = pag_articulo(todo, lang, pid)
            escribe(p["ruta"], html_txt)
            if pid == "home" and lang == "es":
                escribe("index.html", html_txt)
            urls.append(DOMINIO + ("/" if (pid == "home" and lang == "es") else url(p["ruta"])))
    escribe("404.html", pag_404(todo))
    hoy = datetime.date.today().isoformat()
    escribe("sitemap.xml", mapa_xml(todo, hoy))
    # Robots: todo abierto, también a los rastreadores de los asistentes de IA
    # (GEO: que ChatGPT, Claude, Perplexity o Gemini puedan leer y citar la web).
    escribe("robots.txt", "User-agent: *\nAllow: /\n\n"
            + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in
                      ("GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
                       "PerplexityBot", "Google-Extended", "Applebot-Extended"))
            + f"Sitemap: {DOMINIO}/sitemap.xml\n")
    escribe("llms.txt", llms_txt(todo))
    ht = open(os.path.join(PLANT, ".htaccess"), encoding="utf-8").read() if os.path.exists(os.path.join(PLANT, ".htaccess")) else ""
    retiradas = []
    for l in IDIOMAS:
        crudo = json.load(open(os.path.join(CONT, f"{l}.json"), encoding="utf-8"))
        for pid, destino in RETIRADAS.items():
            retiradas.append(f"RedirectMatch 301 ^/{re.escape(crudo['paginas'][pid]['ruta'])}$ "
                             f"{url(todo[l]['paginas'][destino]['ruta'])}")
    escribe(".htaccess", ht + "\n# Páginas retiradas en la web nueva (CV y CP)\n" + "\n".join(retiradas)
            + "\n\n# Rutas de la web vieja (generado por scripts/construir.py)\n"
            + "\n".join(r for r in redirecciones(todo) if r not in retiradas) + "\n")
    comprueba(urls)
    print(len(urls), "páginas en", SALIDA)


NO_INDEXAR = {"presupuesto", "trabaja"}  # dos enlaces cada una: contenido fino


def mapa_xml(todo, hoy):
    """sitemap.xml con las versiones de cada página en los otros idiomas."""
    filas = []
    for l in IDIOMAS:
        for pid in todo[l]["paginas"]:
            if pid in NO_INDEXAR:
                continue
            alt = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{DOMINIO}{ruta_en(todo, x, pid)}"/>'
                          for x in IDIOMAS if pid in todo[x]["paginas"])
            prio = "1.0" if pid == "home" else "0.8" if pid in ("traduccion", "interpretacion", "presupuesto-traduccion") else "0.5"
            filas.append(f"  <url><loc>{DOMINIO}{ruta_en(todo, l, pid)}</loc><lastmod>{hoy}</lastmod>"
                         f"<priority>{prio}</priority>{alt}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(filas) + "\n</urlset>\n")


def llms_txt(todo):
    """/llms.txt: resumen en texto llano para asistentes de IA (propuesta
    llmstxt.org). Es lo primero que leen para responder «¿quién traduce
    documentos jurados en Madrid?» y citar la web."""
    d = todo["es"]; P = d["paginas"]; tel, mail = contacto(d)
    def enlace(l, pid, txt=None):
        return f"- [{txt or nombre_pagina(todo[l], pid)}]({DOMINIO}{ruta_en(todo, l, pid)})"
    servicios = [sin_tags(retoca(x)) for t, c in P["traduccion"]["bloques"] if t == "ul" for x in c][:5]
    interp = [sin_tags(x) for t, c in P["interpretacion"]["bloques"] if t == "ul" for x in c][:5]
    return "\n".join([
        "# Babel Translations (BABELTRANS)", "",
        "> " + SEO["es"]["home"][1], "",
        "Agencia de traducción e interpretación con sede en Madrid (España), desde 1999. Trabaja en todos los "
        "idiomas con traductores que solo traducen a su lengua materna; cada traducción la revisa un traductor "
        "independiente y toda la información se trata con confidencialidad. Web en castellano, inglés, alemán y neerlandés.",
        "", f"Contacto: {mail}" + (f" · {tel_bonito(tel)}" if tel else ""), "",
        "## Traducción", *[f"- {x}" for x in servicios], "",
        "## Interpretación", *[f"- {x}" for x in interp], "",
        "## Páginas principales",
        enlace("es", "traduccion"), enlace("es", "interpretacion"), enlace("es", "metodologia"),
        enlace("es", "quienes"), enlace("es", "presupuesto-traduccion"), enlace("es", "presupuesto-interpretacion"),
        enlace("es", "contacto"), "",
        "## Other languages",
        *[enlace(l, "home", f"{NOMBRES_IDIOMA[l]}") for l in IDIOMAS if l != "es"], "",
    ])


def comprueba(urls):
    """Lo que no puede llegar a la web publicada."""
    prohibido = ["spam bots", "activar JavaScript", "15/1999", "Mail: Esta"]
    malos = []
    for raiz, _, ficheros in os.walk(SALIDA):
        for f in ficheros:
            if f.endswith(".html"):
                t = open(os.path.join(raiz, f), encoding="utf-8").read()
                malos += [f"{os.path.relpath(os.path.join(raiz, f), SALIDA)}: «{x}»" for x in prohibido if x in t]
    # SEO: cada página indexable con título <=70, descripción 50-165 y un h1
    for raiz, _, ficheros in os.walk(SALIDA):
        for f in ficheros:
            if f.endswith(".html") and f != "404.html":
                t = open(os.path.join(raiz, f), encoding="utf-8").read()
                tit = re.search(r"<title>(.*?)</title>", t).group(1)
                desc = re.search(r'name="description" content="(.*?)"', t).group(1)
                if len(html.unescape(tit)) > 70 or not 50 <= len(html.unescape(desc)) <= 165 or t.count("<h1") != 1:
                    malos.append(f"{os.path.relpath(os.path.join(raiz, f), SALIDA)}: SEO (título {len(tit)}, "
                                 f"descripción {len(desc)}, h1 {t.count('<h1')})")
    if malos:
        print("ERROR: lo siguiente no puede publicarse:\n  " + "\n  ".join(malos))
        sys.exit(1)
    if PENDIENTES:
        print("AVISO: faltan datos en contenido/empresa.json:", ", ".join(sorted(PENDIENTES)))
        if "--publicar" in sys.argv:
            print("No se puede publicar con datos pendientes (salen como [PENDIENTE] en la web).")
            sys.exit(1)


if __name__ == "__main__":
    main()

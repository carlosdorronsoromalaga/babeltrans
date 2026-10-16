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
from textos_ui import UI, RETOQUES  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONT = os.path.join(RAIZ, "contenido")
PLANT = os.path.join(RAIZ, "plantilla")
SALIDA = os.path.join(RAIZ, "sitio")
DOMINIO = "https://www.babeltrans.es"
IDIOMAS = ["es", "en", "de", "nl"]
ANIO = datetime.date.today().year

esc = html.escape


def carga():
    return {l: json.load(open(os.path.join(CONT, f"{l}.json"), encoding="utf-8")) for l in IDIOMAS}


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
    """Teléfono y e-mail tal y como aparecían en la página de contacto de ese idioma."""
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

ICONOS = {
    "globo": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "edificio": '<path d="M4 21V5l8-3v19M12 21V9l8 3v9M2 21h20M7 8h2M7 12h2M7 16h2M15 14h2M15 17h2"/>',
    "matraz": '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3M7 15h10"/>',
    "balanza": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "pantalla": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4M7 9h6M7 12h10"/>',
    "candado": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "micro": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8"/>',
    "pluma": '<path d="M20 4c-6 0-12 4-14 12l-2 4 4-2c8-2 12-8 12-14z"/><path d="M6 16l6-6"/>',
    "apreton": '<path d="M2 12l5-5 4 2 3-2 3 1 5 4-5 5-3-2-2 2-3-1-2-2z"/><path d="M11 9l-3 3 2 2 3-3"/>',
    "birrete": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
    "engranaje": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "personas": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c3 0 6 2 6 5"/>',
    "telefono": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "sobre": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "documento": '<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h6"/>',
}


def icono(nombre, clase="ico"):
    return (f'<svg class="{clase}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONOS[nombre]}</svg>')


LOGO = ('<svg class="logo-globo" viewBox="0 0 40 40" aria-hidden="true">'
        '<circle cx="20" cy="20" r="18" fill="var(--tinta)"/>'
        '<g fill="none" stroke="var(--acento)" stroke-width="1.4">'
        '<ellipse cx="20" cy="20" rx="7.5" ry="18"/><path d="M2 20h36M5 11h30M5 29h30"/></g>'
        '<circle cx="20" cy="20" r="18" fill="none" stroke="var(--acento)" stroke-width="1.4"/></svg>')


def bloques_html(bloques, lang, pid):
    sal = []
    for tipo, cont in bloques:
        if tipo in ("ul", "ol"):
            items = "".join(f"<li>{enlaces(retoca(i))}</li>" for i in cont)
            sal.append(f'<{tipo} class="lista">{items}</{tipo}>')
            continue
        cont = enlaces(retoca(re.sub(r"\s*<br>\s*(</a>)?\s*$", r"\1", cont)))
        cont = re.sub(r"<br>\s*</a>", "</a>", cont)
        texto = re.sub(r"<[^>]+>", "", cont).strip()
        if tipo == "cita" or (tipo == "h3" and texto[:1] in "\"“"):
            if pid == "quienes" and lang != "es":
                # En los otros idiomas esta frase estaba SIN traducir y en blanco
                # sobre blanco (era el pie de una foto): nadie la veía.
                continue
            sal.append(f'<blockquote class="cita"><p>{texto.strip(chr(34) + "“”")}</p></blockquote>')
        elif tipo == "h3":
            sal.append(f"<h2>{cont}</h2>")
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
                         f'<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
                         f'</button><ul class="sub">{sub}</ul></li>')
        else:
            items.append(f'<li{cls}><a href="{url(it["ruta"])}"'
                         f'{" aria-current=page" if it["ruta"] == actual else ""}>{esc(it["texto"])}</a></li>')
    return "".join(items)


def pagina(todo, lang, pid, cuerpo, titulo, descripcion, clase=""):
    d = todo[lang]
    ui = UI[lang]
    ruta = d["paginas"][pid]["ruta"]
    tel, mail = contacto(d)
    alternas = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}{url(todo[l]["paginas"][pid]["ruta"]) if not (l == "es" and pid == "home") else "/"}">'
        for l in IDIOMAS)
    idiomas = "".join(
        f'<li><a href="{url(todo[l]["paginas"][pid]["ruta"]) if not (l == "es" and pid == "home") else "/"}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=true" if l == lang else ""} title="{UI[l]["idioma"]}">{l.upper()}</a></li>'
        for l in IDIOMAS)
    pie_links = "".join(f'<li><a href="{url(x["ruta"])}">{esc(x["texto"])}</a></li>' for x in d["pie"])
    servicios = "".join(
        f'<li><a href="{url(d["paginas"][p]["ruta"])}">{esc(nombre_pagina(d, p))}</a></li>'
        for p in ("traduccion", "interpretacion", "metodologia", "quienes", "colaboradores"))
    copy = d["paginas"]["home"]["home"]["copyright"].replace("2024", str(ANIO))
    canon = DOMINIO + ("/" if pid == "home" and lang == "es" else url(ruta))
    tel_html = (f'<a href="tel:{tel}">{icono("telefono")}<span>{tel_bonito(tel)}</span></a>' if tel else "")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{canon}">
{alternas}
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0f2a44">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/estilos.css">
<script src="/web.js" defer></script>
</head>
<body class="{clase}">
<a class="saltar" href="#contenido">{ui["saltar"]}</a>
<div class="barra-sup">
  <div class="envoltorio barra-sup-in">
    <div class="barra-contacto">
      {tel_html}
      <a href="mailto:{mail}">{icono("sobre")}<span>{mail}</span></a>
    </div>
    <ul class="idiomas" aria-label="{ui["idiomas"]}">{idiomas}</ul>
  </div>
</div>
<header class="cabecera">
  <div class="envoltorio cabecera-in">
    <a class="marca" href="{url(d["paginas"]["home"]["ruta"]) if lang != "es" else "/"}" aria-label="Babel Translations">
      {LOGO}<span class="marca-txt"><strong>Babel</strong> Translations</span>
    </a>
    <button class="menu-abrir" aria-expanded="false" aria-controls="nav">
      <span class="hamb" aria-hidden="true"></span><span class="vh">{ui["menu"]}</span>
    </button>
    <nav id="nav" class="nav" aria-label="{ui["menu"]}">
      <ul class="nav-lista">{menu_html(d, ruta)}</ul>
    </nav>
  </div>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie">
  <div class="envoltorio pie-rejilla">
    <div class="pie-marca">
      <a class="marca marca-clara" href="{url(d["paginas"]["home"]["ruta"]) if lang != "es" else "/"}">{LOGO}<span class="marca-txt"><strong>Babel</strong> Translations</span></a>
      <p>{esc(d["paginas"]["home"]["home"]["titulos"][0] if lang != "nl" else d["paginas"]["home"]["home"]["titulos"][1].rstrip(":"))}</p>
    </div>
    <div>
      <h2 class="pie-tit">{ui["servicios"]}</h2>
      <ul class="pie-lista">{servicios}</ul>
    </div>
    <div>
      <h2 class="pie-tit">{ui["contacto"]}</h2>
      <ul class="pie-lista pie-contacto">
        {f'<li>{tel_html}</li>' if tel else ''}
        <li><a href="mailto:{mail}">{icono("sobre")}<span>{mail}</span></a></li>
        <li><a href="{url(d["paginas"]["contacto"]["ruta"])}">{icono("flecha")}<span>{esc(nombre_pagina(d, "contacto"))}</span></a></li>
      </ul>
    </div>
  </div>
  <div class="envoltorio pie-legal">
    <p>{esc(copy)}</p>
    <ul>{pie_links}</ul>
  </div>
</footer>
</body>
</html>
"""


def cabecera_pagina(d, pid, titulo, ui):
    """Banda de título con la miga de pan."""
    p = d["paginas"][pid]
    miga = [f'<a href="{url(d["paginas"]["home"]["ruta"]) if d["idioma"] != "es" else "/"}">{ui["inicio"]}</a>']
    for it in d["menu"]:
        if any(h["ruta"] == p["ruta"] for h in it["hijos"]):
            miga.append(f'<a href="{url(it["ruta"])}">{esc(it["texto"])}</a>')
    return (f'<section class="cab-pagina"><div class="envoltorio">'
            f'<nav class="miga" aria-label="breadcrumb">{" <span aria-hidden=true>/</span> ".join(miga)}</nav>'
            f'<h1>{esc(retoca(titulo))}</h1></div></section>')


def aside(d, ui, tel, mail):
    """Columna lateral de las páginas interiores: pedir presupuesto."""
    P = d["paginas"]
    return f"""<aside class="lateral">
  <div class="tarjeta-cta">
    <h2>{esc(nombre_pagina(d, "presupuesto"))}</h2>
    <ul class="cta-enlaces">
      <li><a href="{url(P["presupuesto-traduccion"]["ruta"])}">{icono("documento")}<span>{esc(nombre_pagina(d, "presupuesto-traduccion"))}</span></a></li>
      <li><a href="{url(P["presupuesto-interpretacion"]["ruta"])}">{icono("micro")}<span>{esc(nombre_pagina(d, "presupuesto-interpretacion"))}</span></a></li>
    </ul>
    <div class="cta-contacto">
      {f'<a href="tel:{tel}">{icono("telefono")}<span>{tel_bonito(tel)}</span></a>' if tel else ''}
      <a href="mailto:{mail}">{icono("sobre")}<span>{mail}</span></a>
    </div>
  </div>
</aside>"""


def descripcion_de(bloques, por_defecto):
    for t, c in bloques:
        if t == "p":
            txt = re.sub(r"<[^>]+>", "", c).strip()
            if len(txt) > 60:
                return txt[:155].rsplit(" ", 1)[0] + ("…" if len(txt) > 155 else "")
    return por_defecto


def primer_parrafo(d, pid):
    for t, c in d["paginas"][pid]["bloques"]:
        if t == "p":
            return re.sub(r"<[^>]+>", "", c).strip()
    return ""


# --------------------------------------------------------------- tipos de página

HUBS = {"servicios": [("traduccion", "pluma"), ("interpretacion", "micro")],
        "presupuesto": [("presupuesto-traduccion", "documento"), ("presupuesto-interpretacion", "micro")],
        "trabaja": [("como-traductor", "pluma"), ("como-interprete", "micro")]}


def pag_hub(todo, lang, pid):
    """Páginas que en la original eran solo dos enlaces: ahora, dos tarjetas."""
    d = todo[lang]; ui = UI[lang]; P = d["paginas"]
    titulos = [re.sub(r"<[^>]+>", "", c).strip() for t, c in P[pid]["bloques"]]
    tarjetas = []
    for i, (destino, ic) in enumerate(HUBS[pid]):
        txt = primer_parrafo(d, destino) if destino in ("traduccion", "interpretacion") else ""
        tit = titulos[i] if i < len(titulos) else nombre_pagina(d, destino)
        tarjetas.append(
            f'<a class="tarjeta tarjeta-grande" href="{url(P[destino]["ruta"])}">{icono(ic, "ico ico-grande")}'
            f'<h2>{esc(tit)}</h2>{f"<p>{esc(txt)}</p>" if txt else ""}'
            f'<span class="mas">{ui["leer"] if txt else nombre_pagina(d, destino)} {icono("flecha")}</span></a>')
    titulo = nombre_pagina(d, pid)
    cuerpo = cabecera_pagina(d, pid, titulo, ui) + \
        f'<section class="seccion"><div class="envoltorio rejilla-2">{"".join(tarjetas)}</div></section>'
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations",
                  descripcion_de([], titulo + " · Babel Translations"))


def pag_articulo(todo, lang, pid):
    d = todo[lang]; ui = UI[lang]; p = d["paginas"][pid]
    tel, mail = contacto(d)
    titulo = p["titulo"] or nombre_pagina(d, pid)
    legal = pid in ("aviso-legal", "privacidad")
    cuerpo = cabecera_pagina(d, pid, titulo, ui) + f"""
<section class="seccion">
  <div class="envoltorio {"legal" if legal else "con-lateral"}">
    <article class="prosa">
{bloques_html(p["bloques"], lang, pid)}
    </article>
    {"" if legal else aside(d, ui, tel, mail)}
  </div>
</section>"""
    return pagina(todo, lang, pid, cuerpo, f"{retoca(titulo)} · Babel Translations",
                  descripcion_de(p["bloques"], retoca(titulo)))


def campo_html(c, i, ui, privacidad_url):
    nombre = c["nombre"]
    obligatorio = nombre.lower() in ("nombre", "persona", "mail", "privacidad")
    req = " required" if obligatorio else ""
    marca = f' <span class="req" title="{ui["obligatorio"]}">*</span>' if obligatorio else ""
    ide = f"f-{nombre.lower()}"
    etiqueta = esc(c["etiqueta"] or nombre.replace("_", " "))
    tipo = c["tipo"]
    if tipo == "checkbox":
        txt = re.sub(r"(Pol[ií]tica de privacidad|Privacy policy|Datenschutz\w*|Privacyverklaring|privacybeleid)",
                     lambda m: f'<a href="{privacidad_url}" target="_blank">{m.group(1)}</a>', etiqueta, flags=re.I)
        return (f'<div class="campo campo-ancho campo-check"><input type="checkbox" id="{ide}" name="{nombre}" value="Sí"{req}>'
                f'<label for="{ide}">{txt}{marca}</label></div>')
    if tipo == "textarea":
        return (f'<div class="campo campo-ancho"><label for="{ide}">{etiqueta}{marca}</label>'
                f'<textarea id="{ide}" name="{nombre}" rows="5"{req}></textarea></div>')
    if tipo == "select":
        # "Seleccione tipo" es un rótulo, no una respuesta: va con valor vacío
        vacio = ' value=""'
        ops = "".join(f'<option{vacio if j == 0 and len(c["opciones"]) > 2 else ""}>{esc(o)}</option>'
                      for j, o in enumerate(c["opciones"]))
        return (f'<div class="campo"><label for="{ide}">{etiqueta}{marca}</label>'
                f'<select id="{ide}" name="{nombre}">{ops}</select></div>')
    if tipo == "file":
        return (f'<div class="campo campo-ancho"><label for="{ide}">{etiqueta}</label>'
                f'<label class="archivo"><input type="file" id="{ide}" name="{nombre}[]" multiple>'
                f'{icono("documento")}<span data-vacio="{ui["elegir_archivo"]}">{ui["elegir_archivo"]}</span></label></div>')
    html_tipo = "email" if nombre.lower() == "mail" else "tel" if nombre.lower() == "telefono" else \
        "date" if nombre.lower() in ("fecha", "fecha_entrega") else "text"
    auto = {"nombre": "name", "persona": "name", "mail": "email", "telefono": "tel", "pais": "country-name",
            "poblacion": "address-level2", "empresa": "organization", "cp": "postal-code",
            "direccion": "street-address", "apellidos": "family-name"}.get(nombre.lower(), "off")
    return (f'<div class="campo"><label for="{ide}">{etiqueta}{marca}</label>'
            f'<input type="{html_tipo}" id="{ide}" name="{nombre}" autocomplete="{auto}"{req}></div>')


def pag_formulario(todo, lang, pid):
    d = todo[lang]; ui = UI[lang]; p = d["paginas"][pid]; f = p["formulario"]
    tel, mail = contacto(d)
    titulo = nombre_pagina(d, pid)
    intro = [t for t in f["intro"] if not t.startswith("BABELTRANS")]
    campos = "\n".join(campo_html(c, i, ui, url(d["paginas"]["privacidad"]["ruta"])) for i, c in enumerate(f["campos"]))
    gracias = f["gracias"] if f["gracias"] and not (lang != "es" and f["gracias"].startswith("Gracias")) else ui["enviado"]
    boton = f["boton"] if not (lang != "es" and f["boton"] == "Enviar") else ui["enviar"]
    cuerpo = cabecera_pagina(d, pid, titulo, ui) + f"""
<section class="seccion">
  <div class="envoltorio con-lateral">
    <div>
      {"".join(f'<p class="intro">{esc(t)}</p>' for t in intro)}
      <div class="aviso aviso-ok" role="status" hidden data-aviso="ok">{icono("check")}<p>{esc(gracias)}</p></div>
      <div class="aviso aviso-error" role="alert" hidden data-aviso="error"><p>{esc(ui["error"])} <a href="mailto:{mail}">{mail}</a></p></div>
      <form class="formulario" action="/enviar.php" method="post" enctype="multipart/form-data">
        <input type="hidden" name="_formulario" value="{esc(titulo)}">
        <input type="hidden" name="_idioma" value="{lang}">
        <input type="hidden" name="_volver" value="{url(p["ruta"])}">
        <div class="trampa" aria-hidden="true"><label>Web <input type="text" name="_web" tabindex="-1" autocomplete="off"></label></div>
        <div class="rejilla-campos">
{campos}
        </div>
        <button class="boton boton-acento" type="submit">{esc(boton)} {icono("flecha")}</button>
      </form>
    </div>
    {aside(d, ui, tel, mail) if pid != "contacto" else aside_contacto(d, ui, tel, mail)}
  </div>
</section>"""
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations",
                  intro[0][:155] if intro else f"{titulo} · Babel Translations")


def aside_contacto(d, ui, tel, mail):
    return f"""<aside class="lateral">
  <div class="tarjeta-cta">
    <h2>BABELTRANS</h2>
    <div class="cta-contacto cta-contacto-grande">
      {f'<a href="tel:{tel}">{icono("telefono")}<span>{tel_bonito(tel)}</span></a>' if tel else ''}
      <a href="mailto:{mail}">{icono("sobre")}<span>{mail}</span></a>
    </div>
  </div>
</aside>"""


def pag_mapa(todo, lang, pid):
    d = todo[lang]; ui = UI[lang]
    items = []
    for it in d["menu"]:
        sub = "".join(f'<li><a href="{url(h["ruta"])}">{esc(h["texto"])}</a></li>' for h in it["hijos"])
        items.append(f'<li><a href="{url(it["ruta"])}">{esc(it["texto"])}</a>{f"<ul>{sub}</ul>" if sub else ""}</li>')
    titulo = d["paginas"][pid]["titulo"] or nombre_pagina(d, pid)
    cuerpo = cabecera_pagina(d, pid, titulo, ui) + \
        f'<section class="seccion"><div class="envoltorio legal"><ul class="mapa">{"".join(items)}</ul></div></section>'
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations", titulo)


def pag_home(todo, lang):
    d = todo[lang]; ui = UI[lang]; P = d["paginas"]; h = P["home"]["home"]
    tel, mail = contacto(d)
    titulos = h["titulos"]
    if lang == "nl":
        # La portada holandesa tenía el título principal sin traducir (en
        # castellano); el subtítulo sí estaba en holandés y hace de título.
        h1, sub = titulos[1].rstrip(":"), ""
    else:
        h1 = titulos[0]
        sub = titulos[1].rstrip(":") if len(titulos) > 1 and titulos[1] != "Babeltrans" else ""
    confid = next((x for x in h["fuertes"] if x.isupper() and len(x) > 12), "")
    iconos_lista = ["edificio", "matraz", "balanza", "pantalla"]
    especialidades = "".join(
        f'<li class="espec">{icono(iconos_lista[i % 4], "ico ico-espec")}<span>{esc(t.rstrip(". …").rstrip("."))}…</span></li>'
        for i, t in enumerate(h["lista"]))
    frases = h["frases"][:3]
    destinos = [("interpretacion", "micro"), ("traduccion", "pluma"), ("mediacion", "apreton")]
    pilares = "".join(
        f'<a class="pilar" href="{url(P[dest]["ruta"])}">{icono(ic, "ico ico-pilar")}'
        f'<p>{esc(frases[i])}</p><span class="mas">{ui["leer"]} {icono("flecha")}</span></a>'
        for i, (dest, ic) in enumerate(destinos) if i < len(frases))
    servicios = ""
    for dest, ic in (("traduccion", "pluma"), ("interpretacion", "micro")):
        lista = next((c for t, c in P[dest]["bloques"] if t == "ul"), [])
        items = "".join(f"<li>{icono('check')}<span>{esc(re.split(r':', re.sub(r'<[^>]+>', '', x))[0])}</span></li>"
                        for x in lista[:5])
        servicios += (f'<article class="servicio">{icono(ic, "ico ico-grande")}'
                      f'<h3>{esc(retoca(P[dest]["titulo"]))}</h3><p>{esc(primer_parrafo(d, dest))}</p>'
                      f'<ul class="mini-lista">{items}</ul>'
                      f'<a class="boton boton-linea" href="{url(P[dest]["ruta"])}">{ui["leer"]} {icono("flecha")}</a></article>')
    cita_colab = next((re.sub(r"<[^>]+>", "", c).strip('"“” ') for t, c in P["colaboradores"]["bloques"]
                       if re.sub(r"<[^>]+>", "", c).strip()[:1] in "\"“"), "")
    colab_txt = primer_parrafo(d, "colaboradores")
    metod = primer_parrafo(d, "metodologia").split("<br>")[0]
    metod = re.split(r"(?<=\.)\s", re.sub(r"<[^>]+>", "", metod))[0]
    form_txt = primer_parrafo(d, "formacion")
    quienes = primer_parrafo(d, "quienes")
    anio = re.search(r"(19|20)\d\d", " ".join(re.sub(r"<[^>]+>", "", c) for t, c in P["quienes"]["bloques"] if t == "p"))

    cuerpo = f"""
<section class="hero">
  <div class="hero-fondo" aria-hidden="true"></div>
  <div class="envoltorio hero-in">
    <div class="hero-txt">
      {f'<p class="antetitulo">{icono("candado")} {esc(confid)}</p>' if confid else ''}
      <h1>{esc(h1)}</h1>
      {f'<p class="hero-sub">{esc(sub)}</p>' if sub else ''}
      <div class="hero-botones">
        <a class="boton boton-acento" href="{url(P["presupuesto"]["ruta"])}">{esc(nombre_pagina(d, "presupuesto"))} {icono("flecha")}</a>
        {f'<a class="boton boton-claro" href="tel:{tel}">{icono("telefono")} {tel_bonito(tel)}</a>' if tel else f'<a class="boton boton-claro" href="mailto:{mail}">{icono("sobre")} {mail}</a>'}
      </div>
    </div>
    <ul class="especialidades">{especialidades}</ul>
  </div>
</section>

<section class="seccion seccion-pilares">
  <div class="envoltorio pilares">{pilares}</div>
</section>

<section class="seccion">
  <div class="envoltorio">
    <div class="quienes">
      {f'<div class="sello"><span class="sello-txt">{ui["desde"]}</span><span class="sello-anio">{anio.group(0)}</span></div>' if anio else ''}
      <div>
        <h2 class="tit-seccion">{esc(nombre_pagina(d, "quienes"))}</h2>
        <p class="destacado">{esc(re.sub(r"<[^>]+>", "", quienes))}</p>
        <a class="enlace-mas" href="{url(P["quienes"]["ruta"])}">{ui["leer"]} {icono("flecha")}</a>
      </div>
    </div>
  </div>
</section>

<section class="seccion seccion-suave">
  <div class="envoltorio">
    <h2 class="tit-seccion tit-centro">{esc(nombre_pagina(d, "servicios"))}</h2>
    <div class="rejilla-2">{servicios}</div>
  </div>
</section>

<section class="seccion">
  <div class="envoltorio rejilla-3">
    <a class="tarjeta" href="{url(P["colaboradores"]["ruta"])}">{icono("personas", "ico ico-grande")}
      <h3>{esc(nombre_pagina(d, "colaboradores"))}</h3>
      {f'<p class="cita-mini">“{esc(cita_colab)}”</p>' if cita_colab else ''}
      <p>{esc(colab_txt)}</p><span class="mas">{ui["leer"]} {icono("flecha")}</span></a>
    <a class="tarjeta" href="{url(P["metodologia"]["ruta"])}">{icono("engranaje", "ico ico-grande")}
      <h3>{esc(nombre_pagina(d, "metodologia"))}</h3><p>{esc(metod)}</p>
      <span class="mas">{ui["leer"]} {icono("flecha")}</span></a>
    <a class="tarjeta" href="{url(P["formacion"]["ruta"])}">{icono("birrete", "ico ico-grande")}
      <h3>{esc(P["formacion"]["titulo"])}</h3><p>{esc(re.sub(r"<[^>]+>", "", form_txt))}</p>
      <span class="mas">{ui["leer"]} {icono("flecha")}</span></a>
  </div>
</section>

<section class="banda-cta">
  <div class="envoltorio banda-cta-in">
    <h2>{esc(nombre_pagina(d, "presupuesto"))}</h2>
    <div class="banda-botones">
      <a class="boton boton-acento" href="{url(P["presupuesto-traduccion"]["ruta"])}">{icono("documento")} {esc(nombre_pagina(d, "presupuesto-traduccion"))}</a>
      <a class="boton boton-claro" href="{url(P["presupuesto-interpretacion"]["ruta"])}">{icono("micro")} {esc(nombre_pagina(d, "presupuesto-interpretacion"))}</a>
    </div>
  </div>
</section>"""
    titulo = f"Babel Translations · {h1}"
    return pagina(todo, lang, "home", cuerpo, titulo, re.sub(r"<[^>]+>", "", quienes)[:155], "es-home")


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
        shutil.copy(os.path.join(PLANT, f), os.path.join(SALIDA, f))
    urls = []
    for lang in IDIOMAS:
        d = todo[lang]
        for pid, p in d["paginas"].items():
            if pid == "home":
                html_txt = pag_home(todo, lang)
            elif pid in HUBS:
                html_txt = pag_hub(todo, lang, pid)
            elif pid == "mapa":
                html_txt = pag_mapa(todo, lang, pid)
            elif "formulario" in p:
                html_txt = pag_formulario(todo, lang, pid)
            else:
                html_txt = pag_articulo(todo, lang, pid)
            escribe(p["ruta"], html_txt)
            if pid == "home" and lang == "es":
                escribe("index.html", html_txt)
            urls.append(DOMINIO + ("/" if (pid == "home" and lang == "es") else url(p["ruta"])))
    hoy = datetime.date.today().isoformat()
    escribe("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{u}</loc><lastmod>{hoy}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    escribe("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    ht = open(os.path.join(PLANT, ".htaccess"), encoding="utf-8").read() if os.path.exists(os.path.join(PLANT, ".htaccess")) else ""
    escribe(".htaccess", ht + "\n# Rutas de la web vieja (generado por scripts/construir.py)\n" + "\n".join(redirecciones(todo)) + "\n")
    print(len(urls), "páginas en", SALIDA)


if __name__ == "__main__":
    main()

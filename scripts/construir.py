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
from textos_ui import UI, UI2, ENTRADAS, RETOQUES  # noqa: E402

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


def pagina(todo, lang, pid, cuerpo, titulo, descripcion, clase=""):
    d = todo[lang]
    ui = UI[lang]
    ruta = d["paginas"][pid]["ruta"]
    tel, mail = contacto(d)
    alternas = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}{ruta_en(todo, l, pid)}">'
                       for l in IDIOMAS)
    idiomas = "".join(
        f'<li><a href="{ruta_en(todo, l, pid)}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=true" if l == lang else ""} title="{UI[l]["idioma"]}">{l}</a></li>'
        for l in IDIOMAS)
    pie_links = "".join(f'<li><a href="{url(x["ruta"])}">{esc(x["texto"])}</a></li>' for x in d["pie"])
    copy = d["paginas"]["home"]["home"]["copyright"].replace("2024", str(ANIO))
    canon = DOMINIO + ruta_en(todo, lang, pid)
    lema = '<span class="marca-lema">Expertos en Traducción e Interpretación</span>' if lang == "es" else ""
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
<meta name="theme-color" content="#fcfcfa">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fuentes/literata-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/estilos.css">
<script src="/web.js" defer></script>
</head>
<body class="{clase}">
<a class="saltar" href="#contenido">{ui["saltar"]}</a>
<header class="cabecera">
  <div class="env cabecera-in">
    <a class="marca" href="{home_url(d)}"><span class="marca-nombre">Babel <i>Translations</i></span>{lema}</a>
    <button class="menu-abrir" aria-expanded="false" aria-controls="nav">{ui["menu"]}</button>
    <div class="nav-caja" id="nav">
      <nav class="nav" aria-label="{ui["menu"]}"><ul class="nav-lista">{menu_html(d, ruta)}</ul></nav>
      <ul class="idiomas" aria-label="{ui["idiomas"]}">{idiomas}</ul>
    </div>
  </div>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie">
  <div class="env pie-in">
    <p class="pie-marca">Babel <i>Translations</i></p>
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
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations", f"{titulo} · Babel Translations")


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
  </article>
</section>"""
    return pagina(todo, lang, pid, cuerpo, f"{retoca(titulo)} · Babel Translations",
                  descripcion_de(p["bloques"], retoca(titulo)))


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
    </form>
  </div>
</section>"""
    return pagina(todo, lang, pid, cuerpo, f"{titulo} · Babel Translations",
                  intro[0][:155] if intro else f"{titulo} · Babel Translations")


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
    confid = next((x for x in h["fuertes"] if x.isupper() and len(x) > 12), "")
    confid = confid[:1] + confid[1:].lower()

    # La edición paralela: la misma frase de la web en los cuatro idiomas,
    # empezando por el de la página. Cada línea lleva a ese idioma.
    orden = [lang] + [l for l in IDIOMAS if l != lang]
    paralelo = "".join(
        f'<li{" class=actual" if l == lang else ""}><a href="{ruta_en(todo, l, "home")}" hreflang="{l}" lang="{l}"'
        f'{" aria-current=true" if l == lang else ""}><span class="codigo">{l}</span>'
        f'<span class="frase">{esc(todo[l]["paginas"]["home"]["home"]["frases"][1])}</span></a></li>'
        for l in orden)

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
    <figure class="paralelo">
      <ul>{paralelo}</ul>
    </figure>
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
        <h2 class="tit-pequeno"><a href="{url(P["formacion"]["ruta"])}">{esc(P["formacion"]["titulo"])}</a></h2>
        <p>{esc(primer_parrafo(d, "formacion"))}</p>
        <a class="enlace" href="{url(P["formacion"]["ruta"])}">{esc(ui["leer"])}</a>
      </div>
    </div>
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
    titulo = f"Babel Translations · {h1}"
    return pagina(todo, lang, "home", cuerpo, titulo, lema[:155], "portada-pagina")


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

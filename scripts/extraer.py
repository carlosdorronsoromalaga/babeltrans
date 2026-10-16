"""Saca el contenido de la web original (original/) a contenido/<idioma>.json.

El texto se conserva TAL CUAL estaba publicado. Lo único que se quita es el
formato de Joomla: estilos en línea, <span> de colores y tamaños, imágenes de
110 px, párrafos vacíos y los trucos de maquetación que partían palabras
("N uestras metas", "TraduccioneS") para pintar una letra de otro color.

De cada idioma se coge la captura MÁS RECIENTE de cada página (2023-2024 casi
todas), que es la última versión que vio un visitante antes de la caída.

Uso:  .venv/bin/python scripts/extraer.py
"""
import json, os, re
from bs4 import BeautifulSoup, NavigableString, Tag

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RAIZ, "original")
DEST = os.path.join(RAIZ, "contenido")

# id de página -> ruta en la web original. Las rutas se CONSERVAN en la web
# nueva para que los enlaces de Google y de otras webs sigan funcionando.
# "fuente" solo cuando la captura está en otra ruta (la home cambió de nombre
# en 2017 y sus artículos 71/72 solo se guardaron con la ruta vieja).
PAGINAS = {
 "es": {
  "home": "es.html",
  "quienes": "es/quienessomos-traducciones.html",
  "colaboradores": "es/quienessomos-traducciones/nuestros-colaboradores-traducciones.html",
  "trabaja": "es/quienessomos-traducciones/trabaja-con-nosotros-traducciones.html",
  "servicios": "es/servicios-traducciones.html",
  "traduccion": "es/servicios-traducciones/traduccion-tecnica-manuales.html",
  "interpretacion": "es/servicios-traducciones/interpretacion-holandes.html",
  "metodologia": "es/metodologia-herramientas-traduccion.html",
  "presupuesto": "es/solicite-presupuesto-traduccion.html",
  "presupuesto-traduccion": "es/solicite-presupuesto-traduccion/presupuesto-traduccion.html",
  "presupuesto-interpretacion": "es/solicite-presupuesto-traduccion/presupuesto-interpretacion.html",
  "contacto": "es/contacto-traduccion.html",
  "cv": "es/cv-ingles.html",
  "cp": "es/cp-ingles-aleman.html",
  "como-traductor": "es/trabajar-como-traductor.html",
  "como-interprete": "es/trabajar-como-interprete.html",
  "aviso-legal": "es/aviso-legal.html",
  "privacidad": "es/politica-de-privacidad.html",
  "mapa": "es/mapa-web.html",
  "mediacion": ("es/home-traducciones/71.html", "es/home-traduccion-holandes/71.html"),
  "formacion": ("es/home-traducciones/72.html", "es/home-traduccion-holandes/72.html"),
 },
 "en": {
  "home": "en.html",
  "quienes": "en/who-we-are.html",
  "colaboradores": "en/who-we-are/our-collaborators.html",
  "trabaja": "en/who-we-are/work-with-us.html",
  "servicios": "en/services.html",
  "traduccion": "en/services/translation.html",
  "interpretacion": "en/services/interpreting.html",
  "metodologia": "en/methodology-and-tools.html",
  "presupuesto": "en/request-a-quote.html",
  "presupuesto-traduccion": "en/request-a-quote/translation-quote.html",
  "presupuesto-interpretacion": "en/request-a-quote/interpretation-quote.html",
  "contacto": "en/contact.html",
  "cv": "en/cv-ingles.html",
  "cp": "en/cp-ingles-aleman.html",
  "como-traductor": "en/as-a-translator.html",
  "como-interprete": "en/as-an-interpreter.html",
  "aviso-legal": "en/disclaimer.html",
  "privacidad": "en/privacy-policy.html",
  "mapa": "en/webmap.html",
  "mediacion": "en/home/71.html",
  "formacion": "en/home/72.html",
 },
 "de": {
  "home": "de.html",
  "quienes": "de/wer-sind-wir.html",
  "colaboradores": "de/wer-sind-wir/unsere-mitarbeiter.html",
  "trabaja": "de/wer-sind-wir/arbeiten-sie-mit-uns.html",
  "servicios": "de/dienste.html",
  "traduccion": "de/dienste/uebersetzungen.html",
  "interpretacion": "de/dienste/dolmetschen.html",
  "metodologia": "de/arbeitsweise-und-werkzeuge.html",
  "presupuesto": "de/kostenvoranschlag.html",
  "presupuesto-traduccion": "de/kostenvoranschlag/kostenvoranschlag-uebersetzen.html",
  "presupuesto-interpretacion": "de/kostenvoranschlag/kostenvoranschlag-dolmetschen.html",
  "contacto": "de/kontakt.html",
  "cv": "de/cv-ingles.html",
  "cp": "de/cp-ingles-aleman.html",
  "como-traductor": "de/als-uebersetzer.html",
  "como-interprete": "de/als-dolmetscher.html",
  "aviso-legal": "de/rechtliche-hinweise.html",
  "privacidad": "de/datenschutz.html",
  "mapa": "de/sitemap.html",
  "mediacion": "de/home/71.html",
  "formacion": "de/home/72.html",
 },
 "nl": {
  "home": "nl.html",
  "quienes": "nl/over-ons.html",
  "colaboradores": "nl/over-ons/onze-medewerkers.html",
  "trabaja": "nl/over-ons/bij-ons-werken.html",
  "servicios": "nl/onze-diensten.html",
  "traduccion": "nl/onze-diensten/vertalen.html",
  "interpretacion": "nl/onze-diensten/tolken.html",
  "metodologia": "nl/methodologie-en-werktuigen.html",
  "presupuesto": "nl/vrijblijvende-offerte.html",
  "presupuesto-traduccion": "nl/vrijblijvende-offerte/vertaalofferte.html",
  "presupuesto-interpretacion": "nl/vrijblijvende-offerte/tolkofferte.html",
  "contacto": "nl/contact.html",
  "cv": "nl/vertalen-cv.html",
  "cp": "nl/cp-ingles-aleman.html",
  "como-traductor": "nl/werken-als-vertaler.html",
  "como-interprete": "nl/werken-als-tolk.html",
  "aviso-legal": "nl/disclaimer.html",
  "privacidad": "nl/privacyverklaring.html",
  "mapa": "nl/sitemap.html",
  "mediacion": "nl/home/71.html",
  "formacion": "nl/home/72.html",
 },
}

BLOQUES = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "blockquote", "table", "div"}
EN_LINEA = {"strong": "strong", "b": "strong", "em": "em", "i": "em", "a": "a", "br": "br"}


def sopa(ruta):
    return BeautifulSoup(open(os.path.join(ORIG, ruta), "rb").read(), "html.parser")


def espacios(t):
    # \xad es un guion blando que Joomla dejó dentro de "Polí­tica"
    return re.sub(r"\s+", " ", t.replace("\xa0", " ").replace("\xad", ""))


def ruta_interna(href, rutas):
    """Convierte un enlace de Joomla en una ruta de la web nueva, o None."""
    if not href:
        return None
    h = re.sub(r"^https?://(www\.)?babeltrans\.es", "", href).split("#")[0].split("?")[0]
    if h.startswith("mailto:") or h.startswith("tel:"):
        return h
    if h.startswith("http"):
        return href
    h = h.lstrip("/")
    return h if h in rutas else None


def en_linea(nodo, rutas):
    """HTML en línea limpio: solo texto, <strong>, <em>, <a> y <br>."""
    if isinstance(nodo, NavigableString):
        if nodo.__class__.__name__ in ("Comment", "Doctype"):
            return ""
        return espacios(str(nodo)).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if not isinstance(nodo, Tag) or nodo.name in ("script", "style", "img", "form", "input"):
        return ""
    dentro = "".join(en_linea(h, rutas) for h in nodo.children)
    etiqueta = EN_LINEA.get(nodo.name)
    if etiqueta == "br":
        return "<br>"
    if not etiqueta or not dentro.strip():
        return dentro
    if etiqueta == "a":
        destino = ruta_interna(nodo.get("href"), rutas)
        if not destino:
            return dentro
        return f'<a href="{destino}">{dentro}</a>'
    return f"<{etiqueta}>{dentro}</{etiqueta}>"


def ordena_espacios(html):
    # Los espacios fuera de las etiquetas, para no dejar "<strong>texto </strong>de"
    html = re.sub(r"<(strong|em)>(\s+)", r"\2<\1>", html)
    html = re.sub(r"(\s+)</(strong|em)>", r"</\2>\1", html)
    html = re.sub(r"</strong><strong>|</em><em>", "", html)
    html = re.sub(r"(<br>\s*)+$", "", re.sub(r"^(\s*<br>)+", "", html.strip()))
    return re.sub(r" {2,}", " ", html).strip()


def es_titulo(p, texto):
    """Joomla no usaba <h3>: los subtítulos eran párrafos en negrita y grandes."""
    if len(texto) > 70 or texto.endswith((".", ",", ";")):
        return False
    negrita = "".join(x.get_text() for x in p.find_all(["strong", "b"]))
    grande = re.search(r"font-size:\s*(1[2-9]|[2-9]\d)pt|font-size:\s*(large|x-large)", str(p))
    return espacios(negrita).strip() == texto or bool(grande and len(texto) < 50)


def articulo(s, rutas):
    """Bloques limpios del cuerpo de un artículo."""
    cuerpo = s.select_one(".article-content") or s.select_one("#ja-current-content")
    salida = []

    def visita(nodo):
        for hijo in nodo.children:
            if not isinstance(hijo, Tag):
                if isinstance(hijo, NavigableString) and espacios(str(hijo)).strip() and nodo is cuerpo:
                    salida.append(("p", en_linea(hijo, rutas)))
                continue
            if hijo.name in ("script", "style", "form"):
                continue
            if hijo.name in ("ul", "ol"):
                items = [ordena_espacios(en_linea(li, rutas)) for li in hijo.find_all("li")]
                items = [i for i in items if re.sub("<[^>]+>", "", i).strip()]
                if items:
                    salida.append((hijo.name, items))
                continue
            if hijo.name == "table" or (hijo.name == "div" and hijo.find(BLOQUES - {"div"})):
                visita(hijo)
                continue
            if hijo.name in BLOQUES or hijo.name == "span":
                html = ordena_espacios(en_linea(hijo, rutas))
                texto = espacios(hijo.get_text()).strip()
                if not texto:
                    continue
                if hijo.name in ("h1", "h2", "h3", "h4", "h5", "h6") or es_titulo(hijo, texto):
                    salida.append(("h3", re.sub(r"</?strong>", "", html)))
                elif texto[:1] in "\"“«" and texto[-1:] in "\"”»":
                    salida.append(("cita", re.sub(r"</?(strong|em)>", "", html).strip("\"“”«» ")))
                else:
                    salida.append(("p", html))
                continue
            visita(hijo)

    visita(cuerpo)
    return salida


def titulo(s):
    h = s.select_one(".contentheading")
    return espacios(h.get_text()).strip() if h else ""


def formulario(s):
    """Campos de un formulario de BreezingForms con su etiqueta.

    BreezingForms no usaba <label>: cada texto y cada campo es un <div> con
    posición absoluta. La etiqueta de un campo es el texto que está a la
    misma altura y más a su izquierda.
    """
    # Solo el del cuerpo: la columna derecha llevaba un "Contacto rápido" en todas.
    form = s.select_one("#ja-current-content form.bfQuickMode")
    if not form:
        return None

    def pos(div):
        m = re.search(r"left:(\d+)px;top:(\d+)px", div.get("style", ""))
        return (int(m.group(1)), int(m.group(2))) if m else None

    textos, campos, intro, extra = [], [], [], []
    for div in form.find_all("div", id=re.compile(r"^ff_div")):
        p = pos(div)
        if not p or "visibility:hidden" in div.get("style", ""):
            continue
        control = div.find(["input", "select", "textarea"])
        if control is None:
            t = espacios(div.get_text(" ")).strip()
            if not t:
                continue
            if div.find("p") or div.find("strong") and len(t) > 40:
                intro.append(t)
            elif div.find("br") and "@" in t:
                extra.append([espacios(x).strip() for x in div.get_text("\n").split("\n") if x.strip()])
            else:
                textos.append((p, t))
            continue
        nombre = control.get("name", "")
        if not nombre.startswith("ff_nm_") or nombre == "ff_nm_botonenviar":
            continue
        campos.append((p, control))

    salida = []
    for (x, y), c in sorted(campos, key=lambda e: (e[0][1], e[0][0])):
        cerca = [(tx, t) for (tx, ty), t in textos if abs(ty - y) <= 6 and tx < x]
        etiqueta = max(cerca)[1] if cerca else ""
        if not etiqueta:  # etiqueta encima del campo (textareas en columnas)
            encima = [(ty, t) for (tx, ty), t in textos if abs(tx - x) <= 10 and 0 < y - ty <= 40]
            etiqueta = max(encima)[1] if encima else ""
        tipo = c.name if c.name != "input" else c.get("type", "text")
        campo = {"nombre": c["name"][6:].rstrip("[]"), "tipo": tipo,
                 "etiqueta": etiqueta.rstrip(": ").strip()}
        if tipo == "checkbox":
            lbl = c.find_next("label")
            campo["etiqueta"] = espacios(lbl.get_text(" ")).strip() if lbl else etiqueta
        if c.name == "select":
            campo["opciones"] = [espacios(o.get_text()).strip() for o in c.find_all("option")]
        salida.append(campo)

    gracias = form.find("div", style=re.compile("visibility:hidden"))
    boton = form.find("input", attrs={"name": "ff_nm_botonenviar"})
    return {
        "intro": intro,
        "datos": extra[0] if extra else [],
        "campos": salida,
        "boton": boton.get("value", "") if boton else "",
        "gracias": espacios(gracias.get_text(" ")).strip() if gracias else "",
    }


def home(s, rutas):
    """Los trozos de la portada, que eran módulos sueltos de Joomla."""
    c = s.select_one("#ja-current-content")
    lista = [espacios(li.get_text()).strip() for li in c.find_all("li")]
    titulos = [espacios(h.get_text()).strip() for h in c.find_all(["h1", "h2", "h3"])]
    fuertes = [espacios(x.get_text()).strip() for x in c.find_all(["strong", "b"])]
    frases = [espacios(a.get_text()).strip() for a in c.find_all("a") if a.get_text(strip=True)]
    derecha = s.select_one("#ja-right")
    servicios = []
    for item in derecha.select(".ja-sidenews, .ja-sidenews-list > div, li") if derecha else []:
        a = item.find("a")
        txt = espacios(item.get_text(" ")).strip()
        if a and txt:
            servicios.append({"titulo": espacios(a.get_text()).strip(), "texto": txt})
    modulos = []
    for m in (s.select("#ja-botsl .moduletable, #ja-botsl .ja-box-ct, #ja-botsl > div > div") or []):
        h = m.find(["h3", "h2"])
        if h:
            modulos.append({"titulo": espacios(h.get_text()).strip(),
                            "texto": [espacios(x).strip() for x in m.get_text("\n").split("\n")
                                      if x.strip() and espacios(x).strip() != espacios(h.get_text()).strip()]})
    pie = s.select_one("#ja-footer")
    copy = re.search(r"Copyright.*", pie.get_text(" ")) if pie else None
    return {"titulos": titulos, "lista": lista, "fuertes": fuertes, "frases": frases,
            "derecha": [espacios(x).strip() for x in derecha.get_text("\n").split("\n") if x.strip()] if derecha else [],
            "modulos": modulos, "copyright": espacios(copy.group(0)).strip() if copy else ""}


def menu(s, rutas):
    nav = s.select_one("#ja-mainnav")
    salida = []
    for li in nav.find("ul").find_all("li", recursive=False):
        a = li.find("a")
        item = {"texto": espacios(a.get_text()).strip(), "ruta": ruta_interna(a.get("href"), rutas) or "",
                "hijos": []}
        sub = li.find("ul")
        if sub:
            for a2 in sub.find_all("a"):
                item["hijos"].append({"texto": espacios(a2.get_text()).strip(),
                                      "ruta": ruta_interna(a2.get("href"), rutas) or ""})
        salida.append(item)
    pie = [{"texto": espacios(a.get_text()).strip(), "ruta": ruta_interna(a.get("href"), rutas)}
           for a in s.select("#ja-footer a") if ruta_interna(a.get("href"), rutas)]
    usuario = [{"texto": espacios(a.get_text()).strip(), "ruta": ruta_interna(a.get("href"), rutas)}
               for a in s.select("#ja-right a, #ja-left a, .moduletable_menu a")
               if ruta_interna(a.get("href"), rutas) and "trabaj" in (a.get("href") or "")
               or ruta_interna(a.get("href"), rutas) in ("en/as-a-translator.html",)]
    return salida, pie


def main():
    os.makedirs(DEST, exist_ok=True)
    todas = set()
    for paginas in PAGINAS.values():
        for v in paginas.values():
            todas.add(v[0] if isinstance(v, tuple) else v)
    for idioma, paginas in PAGINAS.items():
        datos = {"idioma": idioma, "paginas": {}}
        for pid, v in paginas.items():
            ruta, fuente = (v if isinstance(v, tuple) else (v, v))
            s = sopa(fuente)
            p = {"ruta": ruta, "fuente": fuente, "titulo": titulo(s)}
            if s.title:
                p["titulo_html"] = espacios(s.title.get_text()).strip()
            if pid == "home":
                p["home"] = home(s, todas)
                datos["menu"], datos["pie"] = menu(s, todas)
            else:
                f = formulario(s)
                if f:
                    p["formulario"] = f
                    p["bloques"] = []
                else:
                    p["bloques"] = articulo(s, todas)
            datos["paginas"][pid] = p
        with open(os.path.join(DEST, f"{idioma}.json"), "w", encoding="utf-8") as fh:
            json.dump(datos, fh, ensure_ascii=False, indent=1)
        print(idioma, len(datos["paginas"]), "páginas")


if __name__ == "__main__":
    main()

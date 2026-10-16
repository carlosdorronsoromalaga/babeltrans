"""Descarga la web original de babeltrans.es desde archive.org.

La web real está caída (error 500: Joomla 1.5 sobre PHP 8.5), así que la
fuente es la Wayback Machine. Para cada URL se coge la captura MÁS RECIENTE
con estado 200 y se baja en crudo (sufijo id_, sin la barra de archive.org).
Se descarta lo que es ruido de Joomla: registro de usuarios, feeds, noticias
de ejemplo con lorem ipsum y rutas basura de jceutilities.
"""
import gzip, json, os, re, sys, time, urllib.request
from urllib.parse import urlsplit

DEST = sys.argv[1] if len(sys.argv) > 1 else "original"
CDX = ("https://web.archive.org/cdx/search/cdx?url=babeltrans.es&matchType=domain"
       "&output=json&fl=timestamp,original,mimetype,statuscode&filter=statuscode:200")
RUIDO = re.compile(r"component/user|jceutilities|pellentesque|donec-hendrerit|"
                   r"format=feed|type=rss|type=atom|[?&](ui|tmpl|print|format)=")

def get(url, intentos=4):
    for i in range(intentos):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                b = r.read()
            # archive.org a veces sirve la captura tal cual se guardó: en gzip.
            return gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b
        except Exception as e:
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"no se pudo bajar {url}")

def clave(u):
    p = urlsplit(u)
    host = p.hostname.removeprefix("www.") if p.hostname else ""
    return host + (p.path or "/") + (("?" + p.query) if p.query else "")

filas = json.loads(get(CDX))[1:]
ultimas = {}
for ts, orig, mime, _ in filas:
    k = clave(orig)
    if RUIDO.search(k):
        continue
    if k not in ultimas or ts > ultimas[k][0]:
        ultimas[k] = (ts, orig, mime)

indice = []
for k, (ts, orig, mime) in sorted(ultimas.items()):
    ruta = k.split("/", 1)[1] if "/" in k else ""
    ruta = ruta.split("?")[0].lstrip("/") or "index.html"
    if ruta.endswith("/"):
        ruta += "index.html"
    if "?" in k:  # variantes con query (?lang=..) aparte, para no pisar
        ruta += "__" + re.sub(r"[^a-zA-Z0-9]+", "_", k.split("?", 1)[1])
    destino = os.path.join(DEST, ruta)
    if not os.path.exists(destino):
        os.makedirs(os.path.dirname(destino) or DEST, exist_ok=True)
        try:
            datos = get(f"https://web.archive.org/web/{ts}id_/{orig}")
        except RuntimeError as e:
            print("FALLO", e); continue
        open(destino, "wb").write(datos)
        time.sleep(0.5)
    indice.append({"url": orig, "captura": ts, "mime": mime, "fichero": ruta})
    print(ts, ruta)

json.dump(indice, open(os.path.join(DEST, "_indice.json"), "w"), indent=1)
print(len(indice), "ficheros")

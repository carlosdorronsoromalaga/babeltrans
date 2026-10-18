"""Sirve sitio/ en http://localhost:8765 SIN caché.

El http.server de Python deja que el navegador guarde las páginas, y al
regenerar la web Chrome mezclaba HTML nuevo con estilos viejos (18/10/2026).
Uso:  python3 scripts/servir.py
"""
import functools, http.server, os

class SinCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass

raiz = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sitio")
print("http://localhost:8765")
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(SinCache, directory=raiz)).serve_forever()

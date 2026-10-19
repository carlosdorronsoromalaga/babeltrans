"""Publica una VISTA PREVIA de la web en GitHub Pages (rama gh-pages).

Sirve para enseñar la web antes de subirla al hosting de verdad:
https://carlosdorronsoromalaga.github.io/babeltrans/

Diferencias con la web definitiva (sitio/):
- Vive en una subcarpeta (/babeltrans/), así que las rutas que empiezan por
  «/» se reescriben.
- No se indexa (noindex + robots.txt cerrado): si Google la indexara,
  competiría con babeltrans.es cuando esta se publique.
- Los formularios no envían: GitHub Pages no ejecuta PHP. Avisa al pulsar.

Uso:  python3 scripts/previa.py        (construye, reescribe y hace push a gh-pages)
"""
import os, re, shutil, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/babeltrans"
AVISO_FORM = ("<script>document.addEventListener('submit',function(e){e.preventDefault();"
              "alert('Vista previa: los formularios funcionarán cuando la web esté en babeltrans.es.');});</script>")


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True)


def main():
    sh(sys.executable, os.path.join(RAIZ, "scripts", "construir.py"))
    tmp = tempfile.mkdtemp(prefix="babeltrans-previa-")
    destino = os.path.join(tmp, "web")
    shutil.copytree(os.path.join(RAIZ, "sitio"), destino)
    for quitar in (".htaccess", "enviar.php", "llms.txt", "sitemap.xml"):
        ruta = os.path.join(destino, quitar)
        if os.path.exists(ruta):
            os.remove(ruta)
    for raiz, _, ficheros in os.walk(destino):
        for f in ficheros:
            if not f.endswith(".html"):
                continue
            p = os.path.join(raiz, f)
            t = open(p, encoding="utf-8").read()
            # Rutas absolutas internas -> bajo /babeltrans (no toca //, https:, mailto:)
            t = re.sub(r'((?:href|src|action|content)=")/(?!/)', rf"\1{BASE}/", t)
            t = t.replace('<meta name="robots" content="noindex, follow">', "")
            t = t.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
            t = t.replace("</body>", AVISO_FORM + "\n</body>", 1)
            open(p, "w", encoding="utf-8").write(t)
    open(os.path.join(destino, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    open(os.path.join(destino, ".nojekyll"), "w").close()   # que Pages sirva todo tal cual

    remoto = subprocess.run(["git", "remote", "get-url", "origin"], cwd=RAIZ,
                            capture_output=True, text=True, check=True).stdout.strip()
    correo = subprocess.run(["git", "config", "user.email"], cwd=RAIZ,
                            capture_output=True, text=True).stdout.strip()
    sh("git", "init", "-q", "-b", "gh-pages", cwd=destino)
    if correo:
        sh("git", "config", "user.email", correo, cwd=destino)
    sh("git", "add", "-A", cwd=destino)
    sh("git", "commit", "-q", "-m", "Vista previa de la web", cwd=destino)
    sh("git", "push", "-q", "-f", remoto, "gh-pages", cwd=destino)
    shutil.rmtree(tmp)
    print("Vista previa: https://carlosdorronsoromalaga.github.io/babeltrans/")


if __name__ == "__main__":
    main()

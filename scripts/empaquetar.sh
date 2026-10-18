#!/bin/sh
# Prepara el .zip que se sube al hosting (ver docs/PUBLICAR.md).
# Falla, a propósito, si falta algún dato legal en contenido/empresa.json:
# una web con «[PENDIENTE: NIF]» en el aviso legal no se publica.
set -e
cd "$(dirname "$0")/.."
python3 scripts/construir.py --publicar
nombre="babeltrans-web-$(date +%Y%m%d).zip"
rm -f "$nombre"
(cd sitio && zip -qr "../$nombre" . -x '.DS_Store')   # el «.» incluye el .htaccess, que es oculto
echo "Listo: $nombre ($(du -h "$nombre" | cut -f1)). Se sube a public_html/ y se descomprime allí."

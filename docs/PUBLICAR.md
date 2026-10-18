# Cómo se publica la web

## Quién tiene qué

| Dónde | Qué hay | Qué hace falta |
|---|---|---|
| **Ordenador de Martijn** | Nada de la web | Nada. Solo da los datos pendientes y el acceso al hosting, una vez |
| **Ordenador de Carlos** | Este repositorio: el código fuente y el generador | Python 3 (ya está). Cambiar, generar, empaquetar y subir |
| **Hosting (Webempresa)** | La web publicada: el contenido de `sitio/` en `public_html/` | Nada que instalar ni actualizar. PHP 8 para `enviar.php` |
| **GitHub** (propuesto) | Copia privada del repositorio | Que no dependa de un único portátil |

**La regla:** la web se cambia en el repositorio, nunca editando ficheros
directamente en el hosting. Lo que se edite allí se pierde en la siguiente
subida.

## La primera vez

### Lo que hace Martijn, una vez

1. Rellenar los datos legales (lista en `PENDIENTES.md`) y decidir el teléfono.
2. Darle a Carlos acceso al hosting. Lo mejor **no** es pasar la contraseña de
   cPanel, sino crear una **cuenta FTP solo para la web**: en cPanel →
   *Cuentas FTP* → crear `web@babeltrans.es` con directorio `public_html`. Así
   Carlos solo puede tocar la web, no el correo ni la facturación, y el acceso
   se puede borrar cuando se quiera. La contraseña se pasa por teléfono o en
   persona, nunca por WhatsApp ni por correo.
3. Comprobar que existe el buzón `web@babeltrans.es`, desde el que `enviar.php`
   manda los formularios. Si no existe, se crea en cPanel → *Cuentas de correo*,
   o se cambia la dirección en `plantilla/enviar.php`.

### Lo que hace Carlos

1. **Copia de seguridad completa** de lo que hay ahora: cPanel → *JetBackup* (o
   *Copia de seguridad*) → descargar ficheros y base de datos. Guardarla fuera
   del hosting. Con eso, volver atrás siempre es posible.
2. `./scripts/empaquetar.sh` genera `babeltrans-web-AAAAMMDD.zip`. Se niega a
   generarlo si falta algún dato legal.
3. En el hosting, **apartar el Joomla sin borrarlo**: en el administrador de
   archivos, crear `public_html/_joomla_2008/` y mover allí todo lo de
   `public_html/`.
4. Subir el `.zip` a `public_html/` y **descomprimirlo allí** (administrador de
   archivos → *Extraer*). Comprobar que está el `.htaccess`: es un fichero
   oculto (activar «mostrar archivos ocultos»).
5. La versión de PHP puede quedarse en 8.x. **Ya no hace falta el PHP Legacy
   Addon**: si lo llegaron a contratar, se puede dar de baja.
6. **Probar en el móvil y en el ordenador:**
   - la portada en los cuatro idiomas;
   - un formulario de verdad, con un adjunto, y que llega a info@babeltrans.es;
   - que una dirección vieja redirige (p. ej. `/es/cv-ingles.html` → presupuesto);
   - que una dirección inventada muestra la página 404.
7. Cuando todo lleve **dos semanas funcionando**: borrar `_joomla_2008/` y su
   base de datos (cPanel → *Bases de datos MySQL*). Es código de 2008 con
   agujeros conocidos: no debe quedarse en el servidor aunque no se use.

### Después de publicar

- **Google Search Console** (gratis): dar de alta babeltrans.es y enviar
  `https://www.babeltrans.es/sitemap.xml`. Así Google ve antes las páginas
  nuevas y avisa si algo se rompe.
- **Correo que no acabe en spam**: comprobar en cPanel → *Entregabilidad de
  correo* que SPF y DKIM están en verde para babeltrans.es. Si no, se activan
  ahí con un clic.

## Los cambios de después

1. Martijn pide el cambio (WhatsApp, correo…).
2. Carlos edita `contenido/` o `scripts/textos_ui.py`, y ejecuta
   `python3 scripts/construir.py` para verlo en local.
3. `./scripts/empaquetar.sh` y se sube el `.zip` como en el paso 4. Sobrescribe
   los ficheros, así que no hace falta borrar nada antes.

**Si se quiere automatizar** (recomendable cuando los cambios sean frecuentes):
repositorio privado en GitHub y una GitHub Action que, al fusionar en `main`,
sube `sitio/` por FTPS con la cuenta FTP de arriba, guardada como secreto del
repositorio (`SamKirkland/FTP-Deploy-Action`, MIT, la más usada). Publicar
pasaría a ser fusionar un PR. No se ha montado todavía: necesita que la cuenta
FTP exista y que Carlos dé el visto bueno a crear el repositorio.

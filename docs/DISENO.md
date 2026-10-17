# Diseño de la web (v2, 16/10/2026)

## Por qué se rehízo la v1

La primera versión era el «kit por defecto» de una web generada: azul marino
con dorado, fondo de puntitos, tarjetas redondeadas con un icono en un cuadrado
y la misma sombra, pastillas de «GARANTIZAMOS…», flechas → en cada enlace y
una animación de entrada en cada sección. Valía para cualquier negocio, y por
eso no le decía nada a nadie. Carlos lo vio en cuanto lo abrió.

Referencias usadas: la guía `frontend-design` de anthropics/skills (lista de
los tics que delatan una web hecha por IA) y la búsqueda en GitHub de
plantillas de agencias de traducción y editoriales (html5up, temas de
Hugo/Astro), que solo daba plantillas genéricas, así que no sirvió de base.
Detalle en `INVESTIGACION.md`.

## La idea

**El material del oficio es el texto.** Un traductor trabaja con un original
y su versión, con diccionarios, con marcas de corrección en rojo y con tinta
sobre papel. La web usa ese vocabulario visual y nada más:

- **La portada es una edición paralela.** La frase de la propia web, «Todo lo
  verdaderamente excelente es traducible», aparece en los cuatro idiomas en
  que estaba publicada, una debajo de otra con su código de idioma al margen,
  como en una edición bilingüe. Cada línea lleva a la web en ese idioma: el
  selector de idioma ES la pieza principal del diseño. Es el único momento con
  movimiento: al cargar, las versiones aparecen una tras otra.
- **Los servicios son entradas de diccionario.** «tra·duc·ción /tɾa.ðukˈθjon/
  f.», y debajo las acepciones numeradas, que son la propia lista de servicios
  de la web. Aquí la numeración sí significa algo: son acepciones.
- **Las páginas interiores son páginas de libro**: una columna de texto de
  menos de 70 caracteres y un margen ancho a la izquierda con la cabecera de
  sección y las notas al margen (las otras páginas de la sección y cómo pedir
  presupuesto).
- **El rojo es el del corrector**, y solo aparece donde lo pondría un
  corrector: las comillas de las citas colgadas en el margen, el asterisco de
  los campos obligatorios y el texto seleccionado.

## Fichas

| | |
|---|---|
| Papel | `#FCFCFA` (blanco frío, no crema) |
| Tinta | `#1A1F36` (azul negro de pluma; el texto) |
| Azul tinta | `#2B44A8` (enlaces y botones) |
| Rojo corrector | `#C42B2B` (solo los usos de arriba) |
| Gris lápiz | `#646A80` (texto secundario) |
| Calco | `#EEF0F5` (fondos de bloque, como papel vegetal) |

- **Literata** (variable, con tamaño óptico): titulares y texto. Pensada para
  leer libros largos en pantalla, que es justo lo que se vende aquí.
- **Public Sans**: menú, botones, etiquetas de formulario. Neutra y clara, para
  que la interfaz no compita con el texto.
- Escala tipográfica 16 / 19 / 23 / 29 / 36 / 45 / 64. Texto a 19 px con
  interlineado 1,6.
- Radios de 3 px en botones y campos. Sin sombras. Sin tarjetas.

## Lo que se evita a propósito

Etiquetas en mayúsculas sobre cada título, una palabra resaltada en otro color
dentro del titular, numeraciones 01/02/03 que no son una secuencia, flechas en
los botones, tarjetas idénticas con sombra, degradados de adorno, animaciones
en cada bloque, crema con terracota y negro con verde ácido.

## v3 (17/10/2026): tres piezas del oficio

Carlos pidió «cosas chulas y específicas de traducción». Se añadieron tres,
todas sacadas de herramientas o situaciones reales del trabajo de un traductor:

1. **Alineación** en la frase de la portada: es lo que muestran las herramientas
   de traducción asistida (Trados, memoQ) al alinear un original con su
   traducción. Las palabras sin equivalente («is» en inglés y holandés) se
   quedan sin iluminar a propósito: también eso es traducir.
2. **Literal frente a traducido**: el modismo palabra por palabra, tachado, y la
   corrección encima en el rojo del revisor, con el signo ‸ de inserción de las
   marcas de corrección. «Otro ejemplo» vuelve a tachar y corregir. Ese es el
   único movimiento además del de la portada, y solo ocurre al pulsar.
3. **La torre de Babel**, por el nombre de la empresa: «traducción» en 36
   idiomas, cada piso más ancho que el de encima. Los nombres de los idiomas
   salen de `Intl.DisplayNames`, del propio navegador y en el idioma de la
   página, sin traducirlos a mano.

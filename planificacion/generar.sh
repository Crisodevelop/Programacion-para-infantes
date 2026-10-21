#!/bin/sh
# Regenera todo desde contenido.py, que es la única fuente.
# Tras editar el temario: ./generar.sh
set -e
cd "$(dirname "$0")"
# Un .pyc viejo sirvió una vez la versión anterior de una página sin avisar.
# Borrarlo cuesta nada y evita perseguir un fantasma.
rm -rf __pycache__
echo "· página suelta";      python3 build_web.py
echo "· presentación";       python3 build_deck.py
echo "· documento Word";     python3 build_docx.py
# El cocurricular (build_taller.py, build_makers.py, plegado.py, circuitos.py)
# no se genera en esta copia: MAKER_PROGRAMAS está vacío y la app no tiene
# rutas donde servirlo. Los scripts siguen aquí, listos para volver.
echo "· clases";            python3 build_curso.py
echo "· kahoot";            python3 build_kahoot.py
echo "· rutas de la app";    python3 exportar_nextjs.py
echo
echo "Para el PDF: abre el .docx en Pages o Word y expórtalo."

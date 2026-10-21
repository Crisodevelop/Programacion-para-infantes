# -*- coding: utf-8 -*-
"""
Las cuatro fuerzas del vuelo, dibujadas: un avión de perfil con una flecha por
fuerza. Lo usan la guía de los aviones (build_makers.py) y la presentación del
Makers Space (build_taller.py), así que vive aparte y ninguno importa al otro.

El avión va hacia la derecha: el empuje apunta adelante y la resistencia atrás.
Los colores son fijos y se leen sobre fondo claro y oscuro; el texto toma el
color de la página con currentColor.
"""

FLECHAS = {"arriba": "↑", "abajo": "↓", "adelante": "→", "atras": "←"}
COLORES = {"arriba": "#3B82F6", "abajo": "#EF4444", "adelante": "#22C55E", "atras": "#F59E0B"}


def svg_fuerzas(fuerzas, prefijo="fz"):
    """fuerzas: [(nombre, texto, direccion)] con direccion en FLECHAS."""
    nombre = {d: n for n, _, d in fuerzas}
    flechas = {
        "arriba": ((160, 92), (160, 26), (160, 16, "middle")),
        "abajo": ((160, 128), (160, 192), (160, 214, "middle")),
        "adelante": ((238, 110), (304, 110), (304, 96, "end")),
        "atras": ((82, 110), (16, 110), (16, 96, "start")),
    }
    marcas = "".join(
        f'<marker id="{prefijo}-{d}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
        f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{COLORES[d]}"/></marker>'
        for d in flechas)
    lineas = []
    for d, ((x1, y1), (x2, y2), (tx, ty, ancla)) in flechas.items():
        if d not in nombre:
            continue
        lineas.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COLORES[d]}" stroke-width="5" '
            f'stroke-linecap="round" marker-end="url(#{prefijo}-{d})"/>'
            f'<text x="{tx}" y="{ty}" text-anchor="{ancla}" font-size="14" font-weight="700" '
            f'fill="currentColor">{nombre[d]}</text>')
    avion = ('<path d="M84 112 L240 106 L84 98 L112 108 Z" fill="currentColor" opacity=".9"/>'
             '<path d="M112 108 L146 126 L240 106 Z" fill="currentColor" opacity=".45"/>')
    return (f'<svg viewBox="0 0 320 224" role="img" aria-label="Las cuatro fuerzas que actúan sobre un avión">'
            f'<defs>{marcas}</defs>{avion}{"".join(lineas)}</svg>')

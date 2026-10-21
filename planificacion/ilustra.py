# -*- coding: utf-8 -*-
"""
Las ilustraciones del quiz, dibujadas con código.

Del mismo tipo que plegado.py: este módulo no sabe nada del Kahoot ni de las
preguntas, solo dibuja. Cada escena devuelve el SVG de un lienzo de 1200×675 y
recibe el color de acento del nivel, así que la misma caja sale azul en 1ro,
verde en 2do y morada en 3ro sin duplicar un solo trazo.

No se reutiliza el `_svg` de plegado.py aunque el plan lo previera: aquel emite
`<svg class="dg">` y delega el color en la hoja de estilo de la página de los
aviones. Aquí el color va en el propio dibujo, porque el destino es un PNG
suelto que no lleva CSS detrás.

Dos reglas de composición, y las dos vienen del sitio donde se van a ver:

  · Formas grandes y pocas. Esto se proyecta y se mira desde la última fila,
    no se examina de cerca. Lo que no se entiende en miniatura no se entiende.
  · La escena de la pregunta, nunca la respuesta. Para «¿qué es un algoritmo?»
    va un signo de interrogación y no una lista numerada, porque la lista
    numerada es la opción correcta y el dibujo la regalaría.
"""

ANCHO, ALTO = 1200.0, 675.0
CX, CY = ANCHO / 2, ALTO / 2

TINTA = "#14213D"
BLANCO = "#FFFFFF"
GRIS = "#CBD5E1"
GRIS2 = "#94A3B8"
GROSOR = 10.0

FUENTE = ('-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,'
          'Helvetica,Arial,sans-serif')


def _n(v):
    """Números cortos, como en plegado.py: seis decimales no dibujan mejor."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def lienzo(piezas, fondo):
    return (f'<svg viewBox="0 0 {_n(ANCHO)} {_n(ALTO)}" width="{_n(ANCHO)}" '
            f'height="{_n(ALTO)}" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<rect width="{_n(ANCHO)}" height="{_n(ALTO)}" fill="{fondo}"/>'
            f'{"".join(piezas)}</svg>')


# ---------------------------------------------------------------- PRIMITIVAS
def caja(x, y, w, h, relleno=BLANCO, borde=TINTA, r=14.0, grosor=GROSOR):
    b = f' stroke="{borde}" stroke-width="{_n(grosor)}"' if borde else ""
    return (f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" '
            f'rx="{_n(r)}" fill="{relleno}"{b}/>')


def circulo(cx, cy, r, relleno=BLANCO, borde=TINTA, grosor=GROSOR):
    b = f' stroke="{borde}" stroke-width="{_n(grosor)}"' if borde else ""
    return f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}" fill="{relleno}"{b}/>'


def linea(x1, y1, x2, y2, color=TINTA, grosor=GROSOR):
    return (f'<path d="M{_n(x1)} {_n(y1)}L{_n(x2)} {_n(y2)}" stroke="{color}" '
            f'stroke-width="{_n(grosor)}" stroke-linecap="round" fill="none"/>')


def ruta(d, relleno="none", borde=TINTA, grosor=GROSOR, cierre="round"):
    b = f' stroke="{borde}" stroke-width="{_n(grosor)}"' if borde else ""
    return (f'<path d="{d}" fill="{relleno}"{b} stroke-linecap="{cierre}" '
            f'stroke-linejoin="round"/>')


def texto(x, y, t, tam, color=TINTA, peso=800, anclaje="middle", fuente=None):
    # El código lleva < y > —`i <= 3`— y en SVG hay que escaparlos o el
    # dibujo se rompe sin decir nada.
    t = (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
         .replace(" ", "&#160;"))
    return (f'<text x="{_n(x)}" y="{_n(y)}" font-family="{fuente or FUENTE}" '
            f'font-size="{_n(tam)}" font-weight="{peso}" fill="{color}" '
            f'text-anchor="{anclaje}" dominant-baseline="central">{t}</text>')


def flecha(x1, y1, x2, y2, color=TINTA, grosor=GROSOR, punta=26.0):
    """Flecha recta horizontal o vertical: las diagonales no hacen falta aquí."""
    piezas = [linea(x1, y1, x2, y2, color, grosor)]
    if y1 == y2:
        s = 1 if x2 > x1 else -1
        piezas.append(ruta(f"M{_n(x2)} {_n(y2)}L{_n(x2 - s * punta)} {_n(y2 - punta * .62)}"
                           f"L{_n(x2 - s * punta)} {_n(y2 + punta * .62)}Z", color, color, grosor))
    else:
        s = 1 if y2 > y1 else -1
        piezas.append(ruta(f"M{_n(x2)} {_n(y2)}L{_n(x2 - punta * .62)} {_n(y2 - s * punta)}"
                           f"L{_n(x2 + punta * .62)} {_n(y2 - s * punta)}Z", color, color, grosor))
    return "".join(piezas)


def _monitor(cx, cy, w, h, acento, dentro):
    """La carcasa compartida por todas las escenas de pantalla."""
    x, y = cx - w / 2, cy - h / 2
    return [caja(x, y, w, h, BLANCO, TINTA, 20.0),
            *dentro,
            caja(cx - 28, y + h, 56, 44, TINTA, None, 6.0),
            caja(cx - 96, y + h + 38, 192, 24, TINTA, None, 12.0)]


# -------------------------------------------------------------------- 1RO
def duda(acento):
    """¿Qué es un algoritmo? — la duda, no la lista de pasos."""
    piezas = [
        ruta(f"M{_n(CX - 210)} {_n(CY - 190)}h420a34 34 0 0 1 34 34v250a34 34 0 0 1-34 34"
             f"h-210l-96 96v-96h-114a34 34 0 0 1-34-34v-250a34 34 0 0 1 34-34z",
             BLANCO, TINTA, 12.0),
        texto(CX + 12, CY - 20, "?", 260, acento),
    ]
    return piezas


def robot_pan(acento):
    """El robot literal y el pan: la escena de «pon el pan»."""
    return _robot(CX - 250, CY, 0.9, acento) + _pan(CX + 250, CY + 20, acento)


def robot(acento):
    return _robot(CX, CY, 1.15, acento)


def _robot(cx, cy, k, acento):
    """Cuerpo entero y no una cabeza suelta.

    Con la cabeza sola había que leer la pregunta para saber que era un robot.
    Ahora tiene cuello, tronco, brazos y patas, y una boca curva en vez de la
    barra recta: a esta edad una cara que sonríe se mira más que una que no.

    El orden importa. Orejas, cuello, patas y brazos van antes que la cabeza y
    el tronco, para que el relleno blanco de estos los recorte por dentro y no
    se vean las juntas."""
    alto = 410 * k
    arriba = cy - alto / 2
    hw, hh = 250 * k, 180 * k
    hx, hy = cx - hw / 2, arriba + 46 * k
    bw, bh = 196 * k, 132 * k
    bx, by = cx - bw / 2, hy + hh + 14 * k
    g = 7 * k
    return [
        linea(cx, arriba + 16 * k, cx, hy, TINTA, 8 * k),
        circulo(cx, arriba + 16 * k, 20 * k, acento),
        caja(hx - 30 * k, hy + hh * .34, 28 * k, 62 * k, GRIS, TINTA, 13 * k, g),
        caja(hx + hw + 2 * k, hy + hh * .34, 28 * k, 62 * k, GRIS, TINTA, 13 * k, g),
        caja(cx - 26 * k, hy + hh - 6 * k, 52 * k, 26 * k, GRIS, TINTA, 6 * k, g),
        caja(cx - 58 * k, by + bh - 8 * k, 34 * k, 40 * k, GRIS, TINTA, 10 * k, g),
        caja(cx + 24 * k, by + bh - 8 * k, 34 * k, 40 * k, GRIS, TINTA, 10 * k, g),
        caja(bx - 34 * k, by + 18 * k, 30 * k, 84 * k, GRIS, TINTA, 15 * k, g),
        caja(bx + bw + 4 * k, by + 18 * k, 30 * k, 84 * k, GRIS, TINTA, 15 * k, g),
        caja(hx, hy, hw, hh, BLANCO, TINTA, 38 * k),
        circulo(cx - 54 * k, hy + hh * .42, 26 * k, acento),
        circulo(cx + 54 * k, hy + hh * .42, 26 * k, acento),
        ruta(f"M{_n(cx - 44 * k)} {_n(hy + hh * .68)}"
             f"q{_n(44 * k)} {_n(36 * k)} {_n(88 * k)} 0", "none", TINTA, 9 * k),
        caja(bx, by, bw, bh, BLANCO, TINTA, 26 * k),
        circulo(cx, by + bh * .40, 22 * k, acento),
        caja(cx - 46 * k, by + bh * .72, 92 * k, 14 * k, GRIS, None, 7 * k),
    ]


def _pan(cx, cy, acento):
    w, h = 300.0, 150.0
    x, y = cx - w / 2, cy - h / 2
    return [
        ruta(f"M{_n(x)} {_n(y + h)}v-40a{_n(w / 2)} 96 0 0 1 {_n(w)} 0v40z", "#EFD9AE", TINTA),
        linea(x + 14, y + h - 34, x + w - 14, y + h - 34, TINTA, 7.0),
        ruta(f"M{_n(x + 62)} {_n(y + 24)}q26 -30 52 0", "none", TINTA, 7.0),
        ruta(f"M{_n(x + 152)} {_n(y + 14)}q26 -30 52 0", "none", TINTA, 7.0),
    ]


def _pieza(x, y, w, h, r=12.0, entrada=32.0, ancho=28.0, prof=13.0):
    """El contorno de un bloque de Scratch: muesca arriba, pestaña abajo.

    Es lo que convierte tres rectángulos apilados en algo que se reconoce sin
    que nadie lo explique. La pestaña de uno cae justo sobre la muesca del
    siguiente, que es lo que se ve en pantalla al arrastrarlos."""
    recto = w - entrada - ancho - r
    c = f"{_n(ancho * .18)} {_n(prof)} {_n(ancho * .82)} {_n(prof)}"
    return (f"M{_n(x + r)} {_n(y)}h{_n(entrada - r)}c{c} {_n(ancho)} 0h{_n(recto)}"
            f"a{_n(r)} {_n(r)} 0 0 1 {_n(r)} {_n(r)}v{_n(h - 2 * r)}"
            f"a{_n(r)} {_n(r)} 0 0 1 {_n(-r)} {_n(r)}h{_n(-recto)}"
            f"c{_n(-ancho * .18)} {_n(prof)} {_n(-ancho * .82)} {_n(prof)} {_n(-ancho)} 0"
            f"h{_n(-(entrada - r))}a{_n(r)} {_n(r)} 0 0 1 {_n(-r)} {_n(-r)}"
            f"v{_n(-(h - 2 * r))}a{_n(r)} {_n(r)} 0 0 1 {_n(r)} {_n(-r)}z")


def bloques(acento, rotulos=("1", "2", "3")):
    """Tres bloques apilados. Neutro: no dice si el orden importa."""
    piezas, w, h, sep = [], 430.0, 104.0, 12.0
    total = len(rotulos) * h + (len(rotulos) - 1) * sep
    y0 = CY - total / 2
    x = CX - w / 2
    for i, r in enumerate(rotulos):
        y = y0 + i * (h + sep)
        piezas.append(ruta(_pieza(x, y, w, h), BLANCO, TINTA))
        piezas.append(circulo(x + 56, y + h / 2, 28, acento, None))
        piezas.append(texto(x + 56, y + h / 2, r, 38, BLANCO))
        piezas.append(caja(x + 106, y + h / 2 - 11, 250, 22, GRIS, None, 11.0))
    return piezas


def pantalla_duda(acento):
    dentro = [texto(CX, CY - 30, "?", 190, acento)]
    return _monitor(CX, CY - 30, 520, 340, acento, dentro)


def cajas(acento, rotulos=("PUNTOS", "VIDAS")):
    """Variables: cajas rotuladas. La pregunta ya habla de cajas."""
    piezas, w, h, sep = [], 300.0, 230.0, 80.0
    total = len(rotulos) * w + (len(rotulos) - 1) * sep
    x0 = CX - total / 2
    for i, r in enumerate(rotulos):
        x = x0 + i * (w + sep)
        piezas += [
            caja(x, CY - h / 2, w, h, BLANCO, TINTA, 16.0),
            caja(x - 16, CY - h / 2 - 46, w + 32, 52, acento, TINTA, 12.0),
            texto(x + w / 2, CY - h / 2 - 20, r, 34, BLANCO),
            texto(x + w / 2, CY + 24, "?", 96, GRIS2),
        ]
    return piezas


def ciclo(acento, rotulo="∞"):
    """La flecha que vuelve sobre sí misma.

    El rótulo es un parámetro porque no todas las vueltas son iguales: un
    bucle infinito no lleva el mismo número que uno de diez pasadas."""
    r = 170.0
    return [
        ruta(f"M{_n(CX + r)} {_n(CY)}a{_n(r)} {_n(r)} 0 1 1 {_n(-r)} {_n(-r)}",
             "none", acento, 34.0),
        ruta(f"M{_n(CX)} {_n(CY - r - 44)}l0 88l-76 -44z", acento, acento, 20.0),
        texto(CX, CY, rotulo, 130, TINTA),
    ]


def repetido(acento, veces=6):
    """La misma instrucción escrita muchas veces: el problema, no la solución.

    Aquí no puede ir la flecha de `ciclo`: la pregunta es qué conviene hacer
    cuando algo se repite diez veces, y la respuesta correcta es «usar una
    repetición». Dibujar el bucle sería dar la respuesta en la imagen."""
    piezas, w, h, sep = [], 460.0, 42.0, 22.0
    total = veces * h + (veces - 1) * sep
    y = CY - total / 2
    for i in range(veces):
        piezas.append(caja(CX - w / 2, y + i * (h + sep), w, h, acento, None, 21.0))
    return piezas


def busqueda(acento):
    """Una caja de búsqueda con su lupa: el acto de buscar, sin los resultados.

    Los resultados son la respuesta correcta de la pregunta que usa esta
    escena, así que la pantalla se queda vacía a propósito."""
    dentro = [caja(CX - 190, CY - 76, 380, 76, "#F1F5F9", GRIS2, 38.0, 6.0),
              circulo(CX - 128, CY - 38, 26, "none", GRIS2, 9.0),
              linea(CX - 110, CY - 20, CX - 92, CY - 2, GRIS2, 11.0),
              caja(CX - 66, CY - 50, 220, 24, GRIS, None, 12.0)]
    return _monitor(CX, CY - 30, 520, 340, acento, dentro)


def lluvia_paraguas(acento):
    piezas = [
        ruta(f"M{_n(CX - 250)} {_n(CY + 30)}a250 250 0 0 1 500 0z", acento, TINTA),
        linea(CX, CY + 30, CX, CY + 200, TINTA),
        ruta(f"M{_n(CX)} {_n(CY + 200)}q0 46 -52 46t-52 -46", "none", TINTA),
    ]
    for i, (dx, dy) in enumerate(((-330, -120), (-250, 90), (300, -60), (350, 130), (-40, -230))):
        piezas.append(ruta(f"M{_n(CX + dx)} {_n(CY + dy)}l0 62", "none", GRIS2, 14.0))
    return piezas


def pantalla_codigo(acento):
    x, y, w = CX - 200, CY - 130, 400.0
    dentro = []
    for i, ancho in enumerate((0.72, 0.45, 0.88, 0.34)):
        dentro.append(caja(x, y + i * 62, w * ancho, 30,
                           acento if i % 2 == 0 else GRIS, None, 15.0))
    return _monitor(CX, CY - 30, 520, 340, acento, dentro)


def navegador(acento):
    """Una ventana con barra de dirección y una página con cabecera y tarjetas.

    Antes eran tres rayas grises: podía ser cualquier cosa. Lo que hace que se
    lea como un sitio web es la barra de arriba, no el contenido."""
    w, h = 660.0, 420.0
    x, y = CX - w / 2, CY - h / 2 - 10
    piezas = [caja(x, y, w, h, BLANCO, TINTA, 20.0),
              ruta(f"M{_n(x)} {_n(y + 76)}h{_n(w)}", "none", TINTA, 8.0)]
    for i in range(3):
        piezas.append(circulo(x + 44 + i * 44, y + 38, 14, GRIS, TINTA, 6.0))
    piezas.append(caja(x + 186, y + 22, w - 230, 32, GRIS, None, 16.0))
    piezas.append(caja(x + 40, y + 106, w - 80, 96, acento, None, 12.0))
    ancho = (w - 80 - 36) / 3
    for i in range(3):
        piezas.append(caja(x + 40 + i * (ancho + 18), y + 230, ancho, 128,
                           BLANCO, TINTA, 12.0, 7.0))
    return piezas


def naranja_vaso(acento):
    piezas = [
        circulo(CX - 230, CY + 20, 130, "#F59E0B", TINTA),
        ruta(f"M{_n(CX - 230)} {_n(CY - 110)}q40 -66 104 -58q-14 60 -78 76z", acento, TINTA, 8.0),
        ruta(f"M{_n(CX + 130)} {_n(CY - 130)}h230l-34 300h-162z", BLANCO, TINTA),
        ruta(f"M{_n(CX + 146)} {_n(CY - 20)}h198l-24 190h-150z", "#F59E0B", None),
    ]
    return piezas


def lupa_pantalla(acento):
    dentro = []
    for i, ancho in enumerate((0.8, 0.55, 0.7)):
        dentro.append(caja(CX - 190, CY - 130 + i * 60, 380 * ancho, 28, GRIS, None, 14.0))
    piezas = _monitor(CX - 40, CY - 40, 520, 340, acento, dentro)
    piezas += [
        circulo(CX + 190, CY + 80, 118, "none", acento, 22.0),
        linea(CX + 272, CY + 162, CX + 350, CY + 240, acento, 30.0),
    ]
    return piezas


def huellas(acento):
    """Cuatro pasos iguales en fila: la repetición, sin decir cómo acortarla."""
    piezas = []
    for i in range(4):
        x = CX - 420 + i * 240
        piezas.append(ruta(f"M{_n(x)} {_n(CY - 90)}l108 90l-108 90z", acento, TINTA))
    return piezas


def balanza(acento):
    piezas = [
        linea(CX, CY - 200, CX, CY + 180),
        linea(CX - 260, CY - 180, CX + 260, CY - 180),
        caja(CX - 110, CY + 180, 220, 34, TINTA, None, 17.0),
    ]
    for s in (-1, 1):
        x = CX + s * 260
        piezas += [linea(x, CY - 180, x, CY - 90, TINTA, 7.0),
                   ruta(f"M{_n(x - 110)} {_n(CY - 90)}h220l-52 118h-116z", acento, TINTA)]
    return piezas


def bicho(acento):
    piezas = [circulo(CX, CY + 30, 150, acento, TINTA),
              circulo(CX, CY - 130, 76, TINTA, TINTA),
              linea(CX, CY - 110, CX, CY + 180, TINTA, 8.0)]
    for s in (-1, 1):
        piezas += [linea(CX - 34 * s, CY - 186, CX - 92 * s, CY - 240, TINTA, 8.0)]
        for i, dy in enumerate((-40, 30, 100)):
            piezas.append(linea(CX + s * 140, CY + dy, CX + s * 226, CY + dy - 26, TINTA, 8.0))
    for dx, dy in ((-72, -10), (66, 20), (-40, 108), (58, 112)):
        piezas.append(circulo(CX + dx, CY + dy, 24, TINTA, None))
    return piezas


def dos_personas(acento):
    dentro = [caja(CX - 130, CY - 150, 260, 30, GRIS, None, 15.0),
              caja(CX - 130, CY - 96, 180, 30, acento, None, 15.0)]
    piezas = _monitor(CX, CY - 70, 420, 280, acento, dentro)
    for s, color in ((-1, acento), (1, GRIS2)):
        x = CX + s * 380
        piezas += [circulo(x, CY + 60, 62, color, TINTA),
                   ruta(f"M{_n(x - 96)} {_n(CY + 260)}q0 -110 96 -110t96 110z", color, TINTA)]
    return piezas


# -------------------------------------------------------------------- 2DO
def capas(acento):
    """Tres planos apilados, sin rótulo: la web por capas.

    Sin etiquetas a propósito. La pregunta es cuál de las tres hace la
    estructura, así que ponerles nombre sería contestarla."""
    piezas, w, h = [], 460.0, 92.0
    for i, tono in enumerate((GRIS, acento, TINTA)):
        y = CY - 150 + i * 130
        piezas.append(ruta(f"M{_n(CX - w / 2)} {_n(y)}l{_n(w / 2)} -{_n(h / 2)}"
                           f"l{_n(w / 2)} {_n(h / 2)}l-{_n(w / 2)} {_n(h / 2)}z",
                           tono, TINTA))
    return piezas


def paleta(acento):
    piezas = [ruta(f"M{_n(CX - 130)} {_n(CY + 170)}a210 190 0 1 1 240 -40"
                   f"a52 52 0 0 1 -52 52h-46a44 44 0 0 0 -20 82z", BLANCO, TINTA)]
    for i, (dx, dy, c) in enumerate((( -78, -66, acento), (6, -110, "#F59E0B"),
                                     (86, -40, "#EF4444"), (-40, 24, "#16A34A"))):
        piezas.append(circulo(CX + dx, CY + dy, 34, c, TINTA, 7.0))
    piezas.append(texto(CX + 330, CY - 10, "A", 250, acento))
    return piezas


def boton(acento):
    return [
        caja(CX - 230, CY - 90, 460, 150, acento, TINTA, 34.0),
        caja(CX - 150, CY - 24, 300, 22, BLANCO, None, 11.0),
        ruta(f"M{_n(CX + 60)} {_n(CY + 40)}l0 190l52 -54l38 78l44 -22l-40 -78l74 -6z",
             BLANCO, TINTA),
    ]


def etiqueta(acento):
    return [
        ruta(f"M{_n(CX - 250)} {_n(CY - 40)}l190 -140h270a34 34 0 0 1 34 34v212"
             f"a34 34 0 0 1 -34 34h-270z", acento, TINTA),
        circulo(CX - 68, CY - 92, 32, BLANCO, TINTA, 9.0),
        caja(CX + 10, CY - 30, 200, 24, BLANCO, None, 12.0),
        caja(CX + 10, CY + 30, 132, 24, BLANCO, None, 12.0),
    ]


def navegador_consola(acento):
    """Página arriba y consola abajo: se ven las dos, no señala ninguna."""
    w, h = 660.0, 440.0
    x, y = CX - w / 2, CY - h / 2
    piezas = [caja(x, y, w, h, BLANCO, TINTA, 20.0),
              ruta(f"M{_n(x)} {_n(y + 66)}h{_n(w)}", "none", TINTA, 8.0)]
    for i in range(3):
        piezas.append(circulo(x + 44 + i * 44, y + 33, 13, GRIS, TINTA, 6.0))
    piezas.append(caja(x + 50, y + 106, w - 100, 62, acento, None, 12.0))
    for i, an in enumerate((0.86, 0.6)):
        piezas.append(caja(x + 50, y + 196 + i * 42, (w - 100) * an, 22, GRIS, None, 11.0))
    piezas.append(ruta(f"M{_n(x)} {_n(y + 286)}h{_n(w)}v{_n(h - 306)}a20 20 0 0 1 -20 20"
                       f"h{_n(-w + 40)}a20 20 0 0 1 -20 -20z", TINTA, TINTA))
    for i, an in enumerate((0.5, 0.34)):
        piezas.append(caja(x + 50, y + 322 + i * 40, (w - 100) * an, 20, "#64748B", None, 10.0))
    return piezas


def teclado(acento):
    piezas = [caja(CX - 330, CY - 110, 660, 260, BLANCO, TINTA, 26.0)]
    for f in range(3):
        for c in range(8):
            piezas.append(caja(CX - 288 + c * 74, CY - 66 + f * 68, 56, 50,
                               acento if (f == 1 and c == 3) else GRIS, None, 10.0))
    piezas.append(caja(CX - 140, CY + 176, 280, 34, TINTA, None, 17.0))
    return piezas


def tarjeta(acento):
    x, y, w, h = CX - 250, CY - 200, 500.0, 400.0
    piezas = [caja(x, y, w, h, BLANCO, TINTA, 26.0),
              circulo(CX, y + 118, 66, acento, TINTA),
              caja(CX - 130, y + 216, 260, 26, TINTA, None, 13.0)]
    for i, an in enumerate((0.9, 0.7, 0.5)):
        piezas.append(caja(x + 60, y + 274 + i * 40, (w - 120) * an, 20, GRIS, None, 10.0))
    return piezas


def hoja_estilo(acento):
    x, y, w, h = CX - 210, CY - 230, 400.0, 460.0
    piezas = [caja(x, y, w, h, BLANCO, TINTA, 22.0)]
    for i, an in enumerate((0.8, 0.55, 0.9, 0.4)):
        piezas.append(caja(x + 46, y + 70 + i * 62, (w - 92) * an, 26,
                           acento if i % 2 == 0 else GRIS, None, 13.0))
    piezas += [
        ruta(f"M{_n(CX + 210)} {_n(CY + 190)}l150 -280a44 44 0 0 1 76 42l-150 280z",
             acento, TINTA),
        ruta(f"M{_n(CX + 210)} {_n(CY + 190)}l76 42l-96 34z", TINTA, TINTA),
    ]
    return piezas


def periodico(acento):
    """Titular, filete y una foto al lado del texto. Sin la foto y el filete
    eran rayas grises en una caja: no se leía como una portada."""
    x, y, w, h = CX - 310, CY - 225, 620.0, 450.0
    piezas = [caja(x, y, w, h, BLANCO, TINTA, 16.0),
              caja(x + 40, y + 36, w - 80, 40, TINTA, None, 8.0),
              ruta(f"M{_n(x + 40)} {_n(y + 94)}h{_n(w - 80)}", "none", TINTA, 6.0),
              caja(x + 40, y + 114, 248, 152, acento, None, 10.0)]
    for i, an in enumerate((1, .82, 1, .9)):
        piezas.append(caja(x + 308, y + 114 + i * 38, 268 * an, 20, GRIS, None, 10.0))
    for col in range(2):
        for i, an in enumerate((1, .88, .68)):
            piezas.append(caja(x + 40 + col * 290, y + 292 + i * 38,
                               248 * an, 20, GRIS, None, 10.0))
    return piezas


def marco_imagen(acento):
    x, y, w, h = CX - 280, CY - 200, 560.0, 400.0
    return [
        caja(x, y, w, h, BLANCO, TINTA, 22.0),
        circulo(x + 130, y + 110, 44, "#F59E0B", None),
        ruta(f"M{_n(x + 14)} {_n(y + h - 14)}l150 -180l110 120l90 -80l152 140z",
             acento, None),
        caja(x, y, w, h, "none", TINTA, 22.0),
    ]


def enlace(acento):
    piezas = []
    for s in (-1, 1):
        piezas.append(ruta(f"M{_n(CX + s * 40)} {_n(CY - 90)}h{_n(s * 130)}"
                           f"a90 90 0 0 1 0 180h{_n(-s * 130)}", "none", acento, 40.0))
    piezas.append(linea(CX - 70, CY, CX + 70, CY, acento, 40.0))
    return piezas


# -------------------------------------------------------------------- 3RO
def interruptor(acento):
    """Un conmutador: la idea de booleano, sin decidir entre true y "true"."""
    w, h = 520.0, 250.0
    return [
        caja(CX - w / 2, CY - h / 2, w, h, BLANCO, TINTA, h / 2),
        circulo(CX + w / 4 - 6, CY, h / 2 - 34, acento, TINTA),
    ]


def maquina(acento):
    """Entra algo, sale algo: la forma de una función, no lo que hace.

    Nada de piezas de puzle: «reutilizar» es la respuesta correcta de la
    pregunta que usa esta escena."""
    return [
        flecha(CX - 470, CY, CX - 230, CY, TINTA, 14.0, 34.0),
        caja(CX - 200, CY - 150, 400, 300, acento, TINTA, 30.0),
        caja(CX - 130, CY - 34, 260, 24, BLANCO, None, 12.0),
        caja(CX - 130, CY + 30, 170, 24, BLANCO, None, 12.0),
        flecha(CX + 230, CY, CX + 470, CY, TINTA, 14.0, 34.0),
    ]


def _tic(cx, cy, r, color):
    return ruta(f"M{_n(cx - r * .55)} {_n(cy)}l{_n(r * .42)} {_n(r * .5)}"
                f"l{_n(r * .75)} {_n(-r * .95)}", "none", color, 16.0)


def _cruz(cx, cy, r, color):
    return (linea(cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5, color, 16.0) +
            linea(cx + r * .5, cy - r * .5, cx - r * .5, cy + r * .5, color, 16.0))


def pruebas(acento):
    x, y, w = CX - 280, CY - 190, 560.0
    piezas = [caja(x, y, w, 380, BLANCO, TINTA, 22.0)]
    for i, ok in enumerate((True, False, True)):
        yy = y + 74 + i * 108
        piezas.append(circulo(x + 78, yy, 36, "none", TINTA, 8.0))
        piezas.append(_tic(x + 78, yy, 36, acento) if ok else _cruz(x + 78, yy, 36, "#EF4444"))
        piezas.append(caja(x + 140, yy - 13, 340, 26, GRIS, None, 13.0))
    return piezas


def pares(acento):
    """Ocho puntos en cuatro parejas: qué es par, no cómo se comprueba."""
    piezas = []
    for f in range(2):
        for p in range(2):
            for d in range(2):
                cx = CX - 320 + p * 420 + d * 130
                piezas.append(circulo(cx, CY - 100 + f * 200, 52, acento, TINTA))
    return piezas


def muchos(acento, filas=4, columnas=5):
    """Veinte fichas iguales: el problema de guardar muchos, sin la solución."""
    piezas, w, h, sep = [], 150.0, 92.0, 26.0
    x0 = CX - (columnas * w + (columnas - 1) * sep) / 2
    y0 = CY - (filas * h + (filas - 1) * sep) / 2
    for f in range(filas):
        for c in range(columnas):
            x, y = x0 + c * (w + sep), y0 + f * (h + sep)
            piezas.append(caja(x, y, w, h, BLANCO, TINTA, 12.0, 7.0))
            piezas.append(caja(x + 22, y + h / 2 - 9, w - 44, 18, acento, None, 9.0))
    return piezas


def caja_modelo(acento):
    """Rectángulos anidados sin rótulo: cuál de ellos es el padding es la
    pregunta, así que ponerles nombre sería contestarla."""
    piezas, tonos = [], (GRIS, BLANCO, acento)
    for i, tono in enumerate(tonos):
        w, h = 660.0 - i * 170, 440.0 - i * 120
        piezas.append(caja(CX - w / 2, CY - h / 2, w, h, tono, TINTA,
                           20.0 - i * 4, 10.0 - i))
    return piezas


# ------------------------------------------------------------------ BANDA 3
#  Las preguntas de código y de pasos. Antes eran una tarjeta oscura a sangre,
#  y en la fila de miniaturas cantaban: parecían de otro quiz. Ahora usan el
#  mismo marco blanco sobre el fondo del nivel que el resto, con la barra de
#  tres puntos que ya lleva `navegador`. El contenido manda —el fragmento tiene
#  que leerse— pero la ilustración pertenece a la misma familia.
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def _ventana(lineas, tam, salto, fuente, peso, sangria=56.0):
    ancho_car = tam * (0.605 if fuente == MONO else 0.52)
    largo = max((len(l) for l in lineas), default=0)
    w = max(560.0, min(ANCHO - 120, largo * ancho_car + sangria * 2))
    h = 74.0 + len(lineas) * salto + 48.0
    x, y = CX - w / 2, CY - h / 2

    piezas = [caja(x, y, w, h, BLANCO, TINTA, 22.0),
              ruta(f"M{_n(x)} {_n(y + 74)}h{_n(w)}", "none", TINTA, 8.0)]
    for i in range(3):
        piezas.append(circulo(x + 46 + i * 46, y + 37, 14, GRIS, TINTA, 6.0))
    for i, l in enumerate(lineas):
        piezas.append(texto(x + sangria, y + 74 + 30 + i * salto, l, tam,
                            TINTA, peso, "start", fuente))

    # La ventana se dimensiona por su contenido, así que una línea suelta
    # —`console.log("Hola);`— sale minúscula en un lienzo de 1200×675. Se
    # escala hasta llenar el recuadro: en Kahoot todas ocupan lo mismo.
    k = min(0.88 * ANCHO / w, 0.82 * ALTO / h)
    return [f'<g transform="translate({_n(CX)} {_n(CY)}) scale({_n(k)}) '
            f'translate({_n(-CX)} {_n(-CY)})">{"".join(piezas)}</g>']


def codigo(acento, lineas=()):
    return _ventana(list(lineas), 40.0, 56.0, MONO, 500)


def pasos(acento, lineas=()):
    return _ventana(list(lineas), 44.0, 64.0, FUENTE, 700)


ESCENAS = {
    "duda": duda, "robot_pan": robot_pan, "robot": robot, "bloques": bloques,
    "pantalla_duda": pantalla_duda, "cajas": cajas, "ciclo": ciclo,
    "lluvia_paraguas": lluvia_paraguas, "pantalla_codigo": pantalla_codigo,
    "navegador": navegador, "naranja_vaso": naranja_vaso,
    "repetido": repetido, "busqueda": busqueda,
    "capas": capas, "paleta": paleta, "boton": boton, "etiqueta": etiqueta,
    "navegador_consola": navegador_consola, "teclado": teclado,
    "tarjeta": tarjeta, "hoja_estilo": hoja_estilo, "periodico": periodico,
    "marco_imagen": marco_imagen, "enlace": enlace,
    "codigo": codigo, "pasos": pasos,
    "interruptor": interruptor, "maquina": maquina, "pruebas": pruebas,
    "pares": pares, "muchos": muchos, "caja_modelo": caja_modelo,
    "lupa_pantalla": lupa_pantalla, "huellas": huellas, "balanza": balanza,
    "bicho": bicho, "dos_personas": dos_personas,
}


def dibujar(nombre, acento, fondo, **kw):
    return lienzo(ESCENAS[nombre](acento, **kw), fondo)

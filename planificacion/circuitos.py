"""Esquemas eléctricos que se calculan, no se dibujan.

Igual que `plegado.py` con los aviones: un circuito se declara como lo que
tiene —la fuente, lo que va en serie y lo que va en paralelo— y de ahí sale el
SVG con los símbolos normalizados. Para corregir un esquema se cambia una
lista en `contenido.py` y se regenera; no hay SVG pegados a mano.

    esquema(fuente="5 V", serie=["resistencia:220 Ω", "led:on"])

Cada componente es una cadena `tipo:estado`. Si el tipo no existe, la
generación falla: más vale que rompa a que salga un hueco en la pantalla.
"""

TRAZO = "#1F2937"      # el cable y los cuerpos
ROJO = "#DC2626"
GRIS = "#94A3B8"
AZUL = "#2563EB"
AMBAR = "#F59E0B"
PAPEL = "#FFFFFF"

LARGO = 74             # lo que mide un componente, de punta a punta
HUECO = 34             # cable entre dos componentes
RIEL_ALTO = 168        # distancia entre el riel de arriba y el de abajo
MARGEN = 26

FUENTE = "font-family=\"system-ui,-apple-system,Segoe UI,sans-serif\""


def _t(x, y, txt, tam=13, ancla="middle", color=TRAZO, peso=600):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{ancla}" font-size="{tam}" '
            f'font-weight="{peso}" fill="{color}">{txt}</text>')


def _cable(*puntos, color=None):
    """Un cable. En la vista dibujada, rojo el que sale del + y negro el que
    vuelve al –, como los que van a tocar en la mesa."""
    d = " ".join(("M" if i == 0 else "L") + f"{x:.1f} {y:.1f}" for i, (x, y) in enumerate(puntos))
    return (f'<path d="{d}" fill="none" stroke="{color or TRAZO}" stroke-width="3" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _punto(x, y, r=4.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{TRAZO}"/>'


# ─── Los símbolos ────────────────────────────────────────────────────────
#
# Cada uno se dibuja a lo largo del eje +x, desde (0,0) hasta (LARGO,0), con
# el cable entrando y saliendo por la línea y=0. El rótulo lo coloca el
# montador, ya sin girar, para que se lea también en las ramas verticales.

def _resistencia(estado):
    z = "M18 0 l6 -11 l9 22 l9 -22 l9 22 l9 -22 l6 11"
    return {"svg": _cable((0, 0), (18, 0)) + _cable((56, 0), (LARGO, 0))
                   + f'<path d="{z}" fill="none" stroke="{TRAZO}" stroke-width="3" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>',
            "et": estado or ""}


def _led(estado):
    color = {"on": AMBAR, "quemado": GRIS}.get(estado, PAPEL)
    cuerpo = (f'<path d="M22 -13 L48 0 L22 13 Z" fill="{color}" stroke="{TRAZO}" stroke-width="3" '
              f'stroke-linejoin="round"/>'
              f'<path d="M48 -14 L48 14" stroke="{TRAZO}" stroke-width="3" stroke-linecap="round"/>')
    if estado == "on":
        cuerpo += (f'<path d="M30 -20 l7 -9M42 -20 l7 -9" stroke="{AMBAR}" stroke-width="3" '
                   f'stroke-linecap="round"/>'
                   f'<path d="M45 -30 l-4 2 4 2z" fill="{AMBAR}"/>'
                   f'<path d="M57 -30 l-4 2 4 2z" fill="{AMBAR}"/>')
    if estado == "quemado":
        cuerpo += (f'<path d="M24 -16 L46 16M46 -16 L24 16" stroke="{ROJO}" stroke-width="3.5" '
                   f'stroke-linecap="round"/>')
    et = {"on": "LED encendido", "quemado": "LED quemado"}.get(estado, "LED apagado")
    return {"svg": _cable((0, 0), (22, 0)) + _cable((48, 0), (LARGO, 0)) + cuerpo, "et": et}


def _pulsador(estado):
    alto = -14 if estado == "suelto" else -6
    return {"svg": _cable((0, 0), (20, 0)) + _cable((54, 0), (LARGO, 0))
                   + _punto(20, 0) + _punto(54, 0)
                   + _cable((16, alto), (58, alto))
                   + _cable((37, alto), (37, alto - 10))
                   + f'<rect x="27" y="{alto - 20}" width="20" height="10" rx="4" fill="{TRAZO}"/>'
                   + (_cable((20, 0), (20, alto)) + _cable((54, 0), (54, alto)) if estado != "suelto" else ""),
            "et": "sin presionar" if estado == "suelto" else "presionado"}


def _interruptor(estado):
    palanca = ((20, 0), (52, 0)) if estado == "cerrado" else ((20, 0), (50, -18))
    return {"svg": _cable((0, 0), (20, 0)) + _cable((54, 0), (LARGO, 0))
                   + _punto(20, 0) + _punto(54, 0) + _cable(*palanca),
            "et": "cerrado" if estado == "cerrado" else "abierto"}


def _potenciometro(estado):
    base = _resistencia(None)["svg"]
    flecha = (f'<path d="M37 -30 L37 -14" stroke="{AZUL}" stroke-width="3" stroke-linecap="round"/>'
              f'<path d="M37 -12 l-5 -8 10 0z" fill="{AZUL}"/>'
              f'<circle cx="37" cy="-34" r="6" fill="{PAPEL}" stroke="{AZUL}" stroke-width="3"/>')
    return {"svg": base + flecha, "et": estado or "potenciómetro"}


def _motor(estado):
    giro = {"invertido": "↺", "parado": "", }.get(estado, "↻")
    # La M no va dentro del dibujo: la escribe el montador al final, sin girar,
    # para que en una rama vertical siga leyéndose de frente.
    cuerpo = f'<circle cx="37" cy="0" r="19" fill="{PAPEL}" stroke="{TRAZO}" stroke-width="3"/>'
    if giro:
        cuerpo += _t(37, -26, giro, 20, color=AZUL)
    et = {"invertido": "gira al revés", "parado": "parado"}.get(estado, "gira")
    return {"svg": _cable((0, 0), (18, 0)) + _cable((56, 0), (LARGO, 0)) + cuerpo, "et": et,
            "centro": "M"}


def _zumbador(estado):
    """El zumbador: un círculo con la onda del sonido."""
    cuerpo = (f'<circle cx="37" cy="0" r="19" fill="{PAPEL}" stroke="{TRAZO}" stroke-width="3"/>'
              f'<path d="M30 -8 L30 8 L38 14 L38 -14 Z" fill="{TRAZO}"/>')
    if estado != "callado":
        cuerpo += (f'<path d="M44 -8 a10 10 0 0 1 0 16M50 -14 a17 17 0 0 1 0 28" fill="none" '
                   f'stroke="{AZUL}" stroke-width="2.5" stroke-linecap="round"/>')
    return {"svg": _cable((0, 0), (18, 0)) + _cable((56, 0), (LARGO, 0)) + cuerpo,
            "et": "callado" if estado == "callado" else "suena"}


def _ldr(estado):
    """La fotorresistencia: una resistencia con dos flechas de luz entrando."""
    base = _resistencia(None)["svg"]
    luz = (f'<path d="M20 -34 l10 12M32 -34 l10 12" stroke="{AMBAR}" stroke-width="3" '
           f'stroke-linecap="round"/>'
           f'<path d="M30 -22 l-2 -8 8 2z" fill="{AMBAR}"/>'
           f'<path d="M42 -22 l-2 -8 8 2z" fill="{AMBAR}"/>')
    return {"svg": base + luz, "et": estado or "fotorresistencia"}


def _limon(estado):
    """La pila de limón, en símbolos: una celda pequeña con su rótulo."""
    m = 37
    return {"svg": _cable((0, 0), (m - 10, 0)) + _cable((m + 10, 0), (LARGO, 0))
                   + f'<path d="M{m - 10} -14 L{m - 10} 14" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>'
                   + f'<path d="M{m + 10} -8 L{m + 10} 8" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>',
            "et": estado or "limón"}


def _cable_liso(estado):
    return {"svg": _cable((0, 0), (LARGO, 0)), "et": estado or ""}


SIMBOLOS = {
    "resistencia": _resistencia,
    "led": _led,
    "pulsador": _pulsador,
    "interruptor": _interruptor,
    "potenciometro": _potenciometro,
    "motor": _motor,
    "zumbador": _zumbador,
    "ldr": _ldr,
    "limon": _limon,
    "cable": _cable_liso,
}


# ─── Las mismas piezas, pero dibujadas ───────────────────────────────────
#
# El esquema con símbolos es lo que pide el libro para el cuaderno, pero a un
# niño de doce años la primera vez no le dice nada: no reconoce una pila en dos
# rayas. Así que la META se dibuja como se ve en Tinkercad —una pila con sus
# bornes, un LED con su bombillita, una resistencia con sus bandas— y el
# esquema queda para la guía y para el cuaderno.
#
# El interfaz es el mismo que el de los símbolos, así que el montador no sabe
# cuál de los dos está usando.

CUERPO = "#F8FAFC"
PILA = "#334155"
BEIGE = "#E7D3A9"
ROJO_CABLE = "#DC2626"
NEGRO_CABLE = "#1F2937"


def _caja(x, y, w, h, relleno, r=6, borde=TRAZO, ancho=2.5):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{r}" fill="{relleno}" '
            f'stroke="{borde}" stroke-width="{ancho}"/>')


def _d_resistencia(estado):
    bandas = "".join(f'<rect x="{25 + i * 7}" y="-9" width="4" height="18" fill="{c}"/>'
                     for i, c in enumerate(("#B45309", "#111827", "#B45309")))
    return {"svg": _cable((0, 0), (20, 0)) + _cable((54, 0), (LARGO, 0))
                   + _caja(20, -11, 34, 22, BEIGE, 8) + bandas,
            "et": estado or ""}


def _d_led(estado):
    color = {"on": "#FBBF24", "quemado": "#9CA3AF"}.get(estado, "#E5E7EB")
    cuerpo = (f'<path d="M22 8 v-8 a15 15 0 0 1 30 0 v8 z" fill="{color}" stroke="{TRAZO}" '
              f'stroke-width="2.5" stroke-linejoin="round"/>'
              f'<path d="M28 8 v12M46 8 v18" stroke="{TRAZO}" stroke-width="2.5" stroke-linecap="round"/>')
    if estado == "on":
        cuerpo += (f'<path d="M14 -16 l-7 -7M37 -22 l0 -9M60 -16 l7 -7" stroke="{AMBAR}" '
                   f'stroke-width="3" stroke-linecap="round"/>')
    if estado == "quemado":
        cuerpo += (f'<path d="M26 -10 L48 6M48 -10 L26 6" stroke="{ROJO}" stroke-width="3.5" '
                   f'stroke-linecap="round"/>')
    return {"svg": _cable((0, 0), (28, 0)) + _cable((46, 0), (LARGO, 0)) + cuerpo,
            "et": {"on": "encendido", "quemado": "quemado"}.get(estado, "apagado")}


def _d_pulsador(estado):
    tapa = "#94A3B8" if estado == "suelto" else "#475569"
    return {"svg": _cable((0, 0), (18, 0)) + _cable((56, 0), (LARGO, 0))
                   + _caja(18, -16, 38, 32, "#CBD5E1", 5)
                   + f'<circle cx="37" cy="0" r="9" fill="{tapa}" stroke="{TRAZO}" stroke-width="2.5"/>',
            "et": "sin presionar" if estado == "suelto" else "presionado"}


def _d_interruptor(estado):
    cerrado = estado == "cerrado"
    cx = 46 if cerrado else 28
    return {"svg": _cable((0, 0), (16, 0)) + _cable((58, 0), (LARGO, 0))
                   + _caja(16, -14, 42, 28, "#CBD5E1", 6)
                   + _caja(cx - 9, -10, 18, 20, PILA, 4),
            "et": "cerrado" if cerrado else "abierto"}


def _d_potenciometro(estado):
    return {"svg": _cable((0, 0), (16, 0)) + _cable((58, 0), (LARGO, 0))
                   + _caja(16, -16, 42, 32, "#CBD5E1", 6)
                   + f'<circle cx="37" cy="0" r="12" fill="{AZUL}" stroke="{TRAZO}" stroke-width="2.5"/>'
                   + f'<path d="M37 0 l0 -10" stroke="{PAPEL}" stroke-width="3" stroke-linecap="round"/>',
            "et": estado or "perilla"}


def _d_motor(estado):
    flecha = {"invertido": "↺", "parado": "", }.get(estado, "↻")
    cuerpo = (_caja(14, -17, 40, 34, "#FBBF24", 8)
              + f'<path d="M54 0 h12" stroke="{TRAZO}" stroke-width="5" stroke-linecap="round"/>')
    if flecha:
        cuerpo += _t(34, -24, flecha, 19, color=AZUL)
    return {"svg": _cable((0, 0), (14, 0)) + _cable((66, 0), (LARGO, 0)) + cuerpo,
            "et": {"invertido": "gira al revés", "parado": "parado"}.get(estado, "gira")}


def _d_zumbador(estado):
    cuerpo = (f'<circle cx="37" cy="0" r="17" fill="{PILA}" stroke="{TRAZO}" stroke-width="2.5"/>'
              f'<circle cx="37" cy="0" r="4" fill="{PAPEL}"/>')
    if estado != "callado":
        cuerpo += (f'<path d="M58 -9 a12 12 0 0 1 0 18M64 -15 a19 19 0 0 1 0 30" fill="none" '
                   f'stroke="{AZUL}" stroke-width="2.5" stroke-linecap="round"/>')
    return {"svg": _cable((0, 0), (20, 0)) + _cable((54, 0), (LARGO, 0)) + cuerpo,
            "et": "callado" if estado == "callado" else "suena"}


def _d_ldr(estado):
    cuerpo = (_caja(20, -12, 34, 24, "#FDE68A", 8)
              + f'<path d="M26 4 q5 -12 10 0 q5 12 10 0 q5 -12 6 -6" fill="none" stroke="{TRAZO}" '
                f'stroke-width="2.5" stroke-linecap="round"/>'
              + f'<path d="M24 -26 l6 8M37 -30 l0 9M50 -26 l-6 8" stroke="{AMBAR}" stroke-width="3" '
                f'stroke-linecap="round"/>')
    return {"svg": _cable((0, 0), (20, 0)) + _cable((54, 0), (LARGO, 0)) + cuerpo,
            "et": estado or "sensor de luz"}


def _d_limon(estado):
    """Un limón con su clavo y su moneda de cobre: la pila más barata que hay."""
    cuerpo = ('<ellipse cx="37" cy="4" rx="26" ry="19" fill="#FDE047" stroke="#CA8A04" stroke-width="2.5"/>'
              '<path d="M11 4 q-6 -2 -6 -5M63 4 q6 -2 6 -5" stroke="#CA8A04" stroke-width="2.5" '
              'fill="none" stroke-linecap="round"/>'
              # el clavo de zinc, a la izquierda; el cobre, a la derecha
              f'<path d="M24 -10 l-4 -12" stroke="#94A3B8" stroke-width="5" stroke-linecap="round"/>'
              f'<path d="M50 -10 l4 -12" stroke="#B45309" stroke-width="5" stroke-linecap="round"/>')
    return {"svg": _cable((0, 0), (20, -22)) + _cable((54, -22), (LARGO, 0)) + cuerpo,
            "et": estado or "limón"}


DIBUJOS = {
    "resistencia": _d_resistencia,
    "led": _d_led,
    "pulsador": _d_pulsador,
    "interruptor": _d_interruptor,
    "potenciometro": _d_potenciometro,
    "motor": _d_motor,
    "zumbador": _d_zumbador,
    "ldr": _d_ldr,
    "limon": _d_limon,
    "cable": _cable_liso,
}


def _d_fuente(etiqueta, x, y1, y2, invertida=False):
    """La pila, dibujada: una caja con sus dos bornes."""
    m = (y1 + y2) / 2
    alto = min(96, max(62, y2 - y1 - 44))
    arriba, abajo = ("–", "+") if invertida else ("+", "–")
    return "".join([
        _cable((x, y1), (x, m - alto / 2)), _cable((x, m + alto / 2), (x, y2)),
        _caja(x - 23, m - alto / 2, 46, alto, PILA, 8),
        _t(x, m + 5, etiqueta, 15, color=PAPEL),
        _t(x - 34, m - alto / 2 + 14, arriba, 19, color=ROJO if arriba == "+" else TRAZO),
        _t(x - 34, m + alto / 2 - 4, abajo, 19, color=ROJO if abajo == "+" else TRAZO),
    ])


def _pieza(spec, estilo="esquema"):
    """Una pieza, en símbolos (para el cuaderno) o dibujada (para la pantalla)."""
    juego = DIBUJOS if estilo == "real" else SIMBOLOS
    tipo, _, estado = spec.partition(":")
    if tipo not in juego:
        raise KeyError(f"componente desconocido en el circuito: {spec!r} "
                       f"(hay {', '.join(sorted(juego))})")
    return juego[tipo](estado or None)


def _fuente(etiqueta, x, y1, y2, invertida=False):
    """La pila, de pie en el lado izquierdo, entre los dos rieles.

    `invertida` cambia de sitio el + y el –: es lo único que hace falta para
    contar que el motor gira al revés."""
    m = (y1 + y2) / 2
    mas, menos = (m + 28, m - 18) if invertida else (m - 18, m + 28)
    return ("".join([
        _cable((x, y1), (x, m - 16)), _cable((x, m + 16), (x, y2)),
        f'<path d="M{x - 20} {m - 16} L{x + 20} {m - 16}" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>',
        f'<path d="M{x - 11} {m - 4} L{x + 11} {m - 4}" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>',
        f'<path d="M{x - 20} {m + 8} L{x + 20} {m + 8}" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>',
        f'<path d="M{x - 11} {m + 16} L{x + 11} {m + 16}" stroke="{TRAZO}" stroke-width="4" stroke-linecap="round"/>',
        _t(x - 32, mas, "+", 20, color=ROJO), _t(x - 32, menos, "–", 20),
        _t(x - 10, y1 - 12, etiqueta, 15, ancla="end"),
    ]))


def _tierra(x, y):
    return ("".join([
        _cable((x, y), (x, y + 16)),
        f'<path d="M{x - 17} {y + 16} L{x + 17} {y + 16}" stroke="{TRAZO}" stroke-width="3.5" stroke-linecap="round"/>',
        f'<path d="M{x - 11} {y + 23} L{x + 11} {y + 23}" stroke="{TRAZO}" stroke-width="3.5" stroke-linecap="round"/>',
        f'<path d="M{x - 5} {y + 30} L{x + 5} {y + 30}" stroke="{TRAZO}" stroke-width="3.5" stroke-linecap="round"/>',
        _t(x, y + 46, "GND", 12, peso=500, color=GRIS),
    ]))


def esquema(fuente="5 V", serie=(), ramas=(), gnd=True, nota=None, titulo=None,
            invertida=False, estilo="esquema"):
    """El SVG de un circuito.

    `serie` va en el riel de arriba, de izquierda a derecha. `ramas` son
    caminos en paralelo entre los dos rieles: cada rama es su propia lista de
    componentes, uno debajo del otro."""
    serie = [(_pieza(s, estilo), s) for s in serie]
    ramas = [[(_pieza(s, estilo), s) for s in rama] for rama in ramas]

    # Los rieles se separan lo que haga falta: una rama de tres componentes
    # no cabe en el alto de una de uno.
    alto_rama = max((len(r) * LARGO + (len(r) - 1) * HUECO for r in ramas), default=0)
    # Sin ramas el lazo no necesita tanto alto: así el dibujo llena mejor el
    # hueco de la diapositiva en vez de quedar como un marco vacío.
    riel = max(RIEL_ALTO if ramas else 116, alto_rama + 44)
    x0 = MARGEN + 34                                   # el eje de la pila
    y1, y2 = MARGEN + 42, MARGEN + 42 + riel           # riel de arriba y de abajo
    dibujar_fuente = _d_fuente if estilo == "real" else _fuente
    ida = ROJO_CABLE if estilo == "real" else None      # el cable que sale del +
    vuelta = NEGRO_CABLE if estilo == "real" else None  # el que vuelve al –
    # Sin `fuente` el lazo se cierra por la izquierda: la pila son las propias
    # piezas, como en la fila de limones.
    partes = [dibujar_fuente(fuente, x0, y1, y2, invertida) if fuente
              else _cable((x0, y1), (x0, y2), color=vuelta)]

    # Riel de arriba: los componentes en serie, con su cable entre uno y otro.
    x = x0 + HUECO
    partes.append(_cable((x0, y1), (x, y1), color=ida))
    for pieza, _ in serie:
        partes.append(f'<g transform="translate({x:.1f} {y1})">{pieza["svg"]}</g>')
        if pieza.get("centro"):
            partes.append(_t(x + 37, y1 + 6, pieza["centro"], 18))
        if pieza["et"]:
            partes.append(_t(x + LARGO / 2, y1 - 44, pieza["et"], 14, peso=500))
        x += LARGO
        partes.append(_cable((x, y1), (x + HUECO, y1), color=ida))
        x += HUECO

    if ramas:
        # El riel se abre en varias ramas y se vuelve a juntar abajo. Cada
        # rama se separa de la siguiente lo que mida su rótulo más largo, que
        # va a su derecha: si no, los textos se montan unos sobre otros.
        def _ancho_et(rama):
            return max((len(p["et"]) for p, _ in rama), default=0) * 7.2 + 12

        xs, xr = [], x
        for i, rama in enumerate(ramas):
            if i:
                xr += max(120, _ancho_et(ramas[i - 1]) + 54)
            xs.append(xr)
        ancho_ramas = xs[-1] - x
        for i, rama in enumerate(ramas):
            xr = xs[i]
            largo_rama = len(rama) * LARGO + (len(rama) - 1) * HUECO
            yr = y1 + (riel - largo_rama) / 2
            partes.append(_cable((xr, y1), (xr, yr), color=ida))
            for pieza, _ in rama:
                partes.append(f'<g transform="translate({xr:.1f} {yr:.1f}) rotate(90)">{pieza["svg"]}</g>')
                if pieza.get("centro"):
                    partes.append(_t(xr, yr + 43, pieza["centro"], 18))
                if pieza["et"]:
                    partes.append(_t(xr + 42, yr + LARGO / 2 + 5, pieza["et"], 13,
                                     ancla="start", peso=500))
                yr += LARGO
                partes.append(_cable((xr, yr), (xr, yr + HUECO)))
                yr += HUECO
            partes.append(_cable((xr, yr - HUECO), (xr, y2), color=vuelta))
            if i:
                partes.append(_cable((x, y1), (xr, y1), color=ida)
                              + _cable((x, y2), (xr, y2), color=vuelta))
                partes.append(_punto(xr, y1) + _punto(xr, y2))
        partes.append(_punto(x, y1) + _punto(x, y2))
        derecha = x + ancho_ramas
    else:
        # Sin ramas, el riel baja por la derecha y vuelve por abajo.
        derecha = x
        partes.append(_cable((derecha, y1), (derecha, y2), color=vuelta))

    partes.append(_cable((x0, y2), (derecha, y2), color=vuelta))
    # La tierra es un símbolo de esquema: en la vista dibujada no aparece,
    # porque en la mesa (y en Tinkercad) lo que hay es el cable de vuelta.
    if gnd and estilo != "real":
        partes.append(_tierra((x0 + derecha) / 2, y2))

    # A la derecha cabe el rótulo de la última rama, que va por fuera del riel.
    cola = max((len(p["et"]) for p, _ in (ramas[-1] if ramas else [])), default=0) * 7.2
    ancho = derecha + MARGEN + max(34, cola + 36)
    alto = y2 + (MARGEN + 52 if (gnd and estilo != "real") else MARGEN)
    if titulo:
        partes.append(_t(ancho / 2, MARGEN + 2, titulo, 17, peso=700))
    if nota:
        alto += 26
        partes.append(_t(ancho / 2, alto - 14, nota, 15, peso=600, color=AZUL))

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" '
            f'width="{ancho:.0f}" height="{alto:.0f}" {FUENTE} role="img" '
            f'aria-label="{titulo or "Esquema del circuito"}">'
            f'<rect width="{ancho:.0f}" height="{alto:.0f}" rx="14" fill="{PAPEL}"/>'
            + "".join(partes) + "</svg>")


if __name__ == "__main__":
    # Autocomprobación: todos los símbolos se dibujan y el SVG cierra bien.
    for nombre in SIMBOLOS:
        for estilo in ("esquema", "real"):
            s = esquema(serie=[nombre], nota="prueba", estilo=estilo)
            assert s.startswith("<svg") and s.endswith("</svg>"), (nombre, estilo)
    assert set(SIMBOLOS) == set(DIBUJOS), "un juego tiene piezas que el otro no"
    esquema(serie=["resistencia:220 Ω"], ramas=[["led:on"], ["led:on"]], estilo="real")
    print(f"  circuitos: {len(SIMBOLOS)} piezas, en símbolos y dibujadas")

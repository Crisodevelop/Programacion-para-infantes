# -*- coding: utf-8 -*-
"""
Diagramas de construcciones de palitos, calculados y no dibujados.

Un palito de helado es un rectángulo de esquinas redondeadas, siempre el mismo,
y una construcción es una lista de palitos colocados: `(x, y, ángulo)`, donde
(x, y) es el centro. Nada más. Por eso este archivo es una décima parte de
`plegado.py`: en el papel hay que calcular qué pasa al doblar; aquí solo hay
que poner una pieza donde va.

La razón de calcularlo en vez de dibujarlo es la misma de los aviones. Un paso
va a estar mal —eso se descubre con treinta niños delante, no antes— y hay que
poder arreglarlo moviendo un número, no reescribiendo un SVG que nadie se
atreve a tocar.

─── Lo que hace que un paso a paso se entienda ───
En cada diagrama, los palitos **nuevos** van en color y los de los pasos
anteriores en gris. Es lo que permite mirar la lámina y saber qué toca ahora
sin leer una palabra, que es como la va a usar un niño de siete años.
"""
import math

# Un palito de manualidad estándar: 114 × 10 mm. Todas las medidas del archivo
# están en milímetros para que la lista de materiales y el dibujo no puedan
# discrepar.
LARGO = 114.0
ANCHO = 10.0

TINTA = "#14213D"
GRIS = "#C2CBD8"
BLANCO = "#FFFFFF"


def _n(v):
    """Números cortos: un SVG con quince decimales pesa el triple y no se lee."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def palito(x, y, ang=0.0, largo=LARGO, ancho=ANCHO):
    """Un palito centrado en (x, y), girado `ang` grados."""
    return {"x": float(x), "y": float(y), "ang": float(ang),
            "largo": float(largo), "ancho": float(ancho)}


def lado(p0, p1):
    """Un palito puesto sobre el segmento p0→p1.

    Colocar los palitos por su centro «a ojo» deja las esquinas sin tocarse, y
    un cuadrado con las esquinas separadas no es un cuadrado: es basura. Con
    los dos extremos del lado, el ángulo y el centro salen solos."""
    return palito((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2,
                  math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0])))


def _caja(p):
    """Las cuatro esquinas, ya giradas. Sirve para encuadrar y para comprobar."""
    a = math.radians(p["ang"])
    dx, dy = p["largo"] / 2, p["ancho"] / 2
    co, si = math.cos(a), math.sin(a)
    return [(p["x"] + ex * dx * co - ey * dy * si,
             p["y"] + ex * dx * si + ey * dy * co)
            for ex, ey in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def _svg_palito(p, color, borde):
    r = p["ancho"] / 2                      # extremos redondeados, como el real
    return (f'<rect x="{_n(p["x"] - p["largo"] / 2)}" y="{_n(p["y"] - p["ancho"] / 2)}" '
            f'width="{_n(p["largo"])}" height="{_n(p["ancho"])}" rx="{_n(r)}" '
            f'fill="{color}" stroke="{borde}" stroke-width="1.6" '
            f'transform="rotate({_n(p["ang"])} {_n(p["x"])} {_n(p["y"])})"/>')


def _marco(piezas, margen=14.0):
    xs, ys = [], []
    for p in piezas:
        for x, y in _caja(p):
            xs.append(x); ys.append(y)
    if not xs:
        return (0.0, 0.0, 100.0, 100.0)
    return (min(xs) - margen, min(ys) - margen,
            max(xs) - min(xs) + 2 * margen, max(ys) - min(ys) + 2 * margen)


def diagramas(pasos, marco=None):
    """De una lista de pasos a una lista de {texto, detalle, svg}.

    Cada paso es `{"texto", "detalle", "nuevos": [palito, ...]}`. El encuadre
    es el mismo en todos los pasos —el de la construcción terminada— para que
    la pieza no baile de tamaño entre una lámina y la siguiente."""
    todos = [p for paso in pasos for p in paso["nuevos"]]
    vx, vy, vw, vh = marco or _marco(todos)

    salida, puestos = [], []
    for paso in pasos:
        cuerpo = "".join(_svg_palito(p, BLANCO, GRIS) for p in puestos)
        cuerpo += "".join(_svg_palito(p, "#FFF6E5", TINTA) for p in paso["nuevos"])
        salida.append({
            "texto": paso["texto"],
            "detalle": paso.get("detalle", ""),
            "svg": (f'<svg viewBox="{_n(vx)} {_n(vy)} {_n(vw)} {_n(vh)}" '
                    f'xmlns="http://www.w3.org/2000/svg" role="img">{cuerpo}</svg>'),
        })
        puestos = puestos + list(paso["nuevos"])
    return salida


def cuantos(pasos):
    return sum(len(p["nuevos"]) for p in pasos)


# ─── las construcciones ───────────────────────────────────────────────────
#  Todo va en ALZADO, mirando la pieza de frente. El primer intento las dibujó
#  en planta y no se entendía ninguna: la casa parecía una escalera y el puente
#  un peine. Una estructura se explica por su silueta, y la silueta solo
#  aparece de frente.
#
#  De la que sale en dos minutos a la que hay que pensar. El orden importa: el
#  triángulo es el descubrimiento y las otras dos lo usan.

def formas():
    """El cuadrado que se dobla y el triángulo que no. Sin pegamento."""
    L = LARGO

    def rombo(cx, grados):
        """Un cuadrado vencido `grados` grados. Con 0 es un cuadrado."""
        k = math.radians(grados)
        dx, dy = L * math.sin(k), -L * math.cos(k)
        a = (cx - L / 2, L / 2)                 # abajo izquierda
        b = (cx + L / 2, L / 2)                 # abajo derecha
        c = (b[0] + dx, b[1] + dy)              # arriba derecha
        d = (a[0] + dx, a[1] + dy)              # arriba izquierda
        return [lado(a, b), lado(b, c), lado(c, d), lado(d, a)]

    h = L * 0.866                               # altura del equilátero
    cx = 430.0
    t = [(cx - L / 2, h / 2), (cx + L / 2, h / 2), (cx, -h / 2)]

    return [
        {"texto": "Arma un cuadrado con cuatro palitos.",
         "detalle": "Las esquinas se atan con ligas, flojas: tienen que poder moverse.",
         "nuevos": rombo(0, 0)},
        {"texto": "Empuja una esquina con un dedo.",
         "detalle": "Se vence de lado y se queda así. Un cuadrado no aguanta nada.",
         "nuevos": rombo(215, 30)},
        {"texto": "Ahora tres palitos: un triángulo.",
         "detalle": "Mismas ligas, misma fuerza. Este no se mueve. De aquí sale todo lo demás.",
         "nuevos": [lado(t[0], t[1]), lado(t[1], t[2]), lado(t[2], t[0])]},
    ]


def casa():
    """De frente: una pared de palitos apilados y un techo en dos aguas.

    La pared mide once palitos de alto justamente para que los montantes de
    las esquinas sean palitos enteros y nadie tenga que cortar nada."""
    L, A = LARGO, ANCHO
    filas = 11
    alto = filas * A                                   # 110 mm ≈ un palito
    cy = -alto / 2 + A / 2

    pared = [palito(0, -i * A, 0) for i in range(filas)]
    montantes = [palito(-L / 2 + A / 2, cy, 90), palito(L / 2 - A / 2, cy, 90)]

    # El techo: dos aguas que se apoyan en la punta. Se calcula la pendiente
    # de verdad para que el ángulo del dibujo sea el que hay que copiar.
    cumbre = (0.0, -alto - 58.0)
    alero = (L / 2, -alto + A / 2)
    ang = math.degrees(math.atan2(cumbre[1] - alero[1], cumbre[0] - alero[0]))
    mx, my = (cumbre[0] + alero[0]) / 2, (cumbre[1] + alero[1]) / 2
    techo = []
    for k in (0, 1):
        d = k * (A + 1.0)
        nx, ny = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
        techo.append(palito(mx + nx * d, my + ny * d, ang))
        techo.append(palito(-(mx + nx * d), my + ny * d, -ang))

    return [
        {"texto": "La pared: palitos uno encima de otro.",
         "detalle": "Once alturas. Que queden bien alineados por los lados.",
         "nuevos": pared},
        {"texto": "Dos palitos de pie, uno en cada esquina.",
         "detalle": "Traban la pared entera. Sin ellos se abre como un acordeón.",
         "nuevos": montantes},
        {"texto": "El techo: dos aguas que se tocan arriba.",
         "detalle": "Eso es un triángulo. Por eso el techo no se hunde.",
         "nuevos": techo},
    ]


def puente():
    """De lado: la celosía de un puente de verdad.

    Los tramos miden 57 mm y la altura 100 mm porque así la diagonal sale de
    115 mm, que es un palito entero. La geometría está elegida para que no
    haya que cortar."""
    L, A = LARGO, ANCHO
    H, T = 100.0, 57.0                     # altura y ancho de cada tramo
    xs = [-2 * T, -T, 0.0, T, 2 * T]       # los cinco montantes

    abajo = [palito(-T, 0, 0), palito(T, 0, 0)]
    arriba = [palito(-T, -H, 0), palito(T, -H, 0)]
    montantes = [palito(x, -H / 2, 90) for x in xs]

    diagonales = []
    for i in range(4):
        x0, x1 = xs[i], xs[i + 1]
        sube = i % 2 == 0
        y0, y1 = (0.0, -H) if sube else (-H, 0.0)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        diagonales.append(palito((x0 + x1) / 2, (y0 + y1) / 2, ang))

    return [
        {"texto": "El tablero: dos palitos en línea, de punta a punta.",
         "detalle": "Por aquí pasa el carro. Es el suelo del puente.",
         "nuevos": abajo},
        {"texto": "Arriba, otros dos igual.",
         "detalle": "A la altura de un palito de pie. Todavía se tuerce todo.",
         "nuevos": arriba},
        {"texto": "Cinco palitos de pie, repartidos.",
         "detalle": "Unen el de abajo con el de arriba. Ya no se abre.",
         "nuevos": montantes},
        {"texto": "Y ahora las diagonales: cada hueco, un triángulo.",
         "detalle": "Esto es lo que hace que aguante. Sin ellas el puente se tuerce y cae.",
         "nuevos": diagonales},
        {"texto": "Haz otro lado igual y únelos con palitos cruzados.",
         "detalle": "Dos celosías paralelas. En medio, el tablero por donde se pone el peso.",
         "nuevos": []},
    ]


def icosaedro():
    """La tapa plana, que es por donde se empieza. El resto se explica."""
    L = LARGO
    R = L / (2 * math.sin(math.radians(36)))     # que el lado sea un palito

    borde, radios = [], []
    for k in range(5):
        a0 = math.radians(-90 + k * 72)
        a1 = math.radians(-90 + (k + 1) * 72)
        p0 = (R * math.cos(a0), R * math.sin(a0))
        p1 = (R * math.cos(a1), R * math.sin(a1))
        borde.append(palito((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2,
                            math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))))
        radios.append(palito(p0[0] / 2, p0[1] / 2, math.degrees(math.atan2(p0[1], p0[0]))))

    return [
        {"texto": "Cinco palitos en pentágono.",
         "detalle": "Plano sobre la mesa. Que las puntas se toquen.",
         "nuevos": borde},
        {"texto": "Cinco más, del centro a cada punta.",
         "detalle": "Ya tienes cinco triángulos juntos. Eso es una estrella.",
         "nuevos": radios},
        {"texto": "Levanta el centro y se hace una cúpula.",
         "detalle": "Dos cúpulas y un cinturón de diez palitos en zigzag: la bola. "
                    "Este es el reto extra, para quien termine antes.",
         "nuevos": []},
    ]


MODELOS = {"formas": formas, "casa": casa, "puente": puente, "icosaedro": icosaedro}


# ─── autocomprobación ─────────────────────────────────────────────────────
#  Lo que salvó los aviones. Una guía que pide 60 palitos y dibuja 54 se
#  descubre con treinta niños delante, y ahí ya no hay arreglo.

if __name__ == "__main__":
    fallos = []
    for nombre, hacer in MODELOS.items():
        pasos = hacer()
        ds = diagramas(pasos)
        n = cuantos(pasos)

        if len(ds) != len(pasos):
            fallos.append(f"{nombre}: {len(ds)} diagramas para {len(pasos)} pasos")
        # Un paso sin palitos es válido si es el último: son los cierres que
        # se explican con palabras («haz otro lado igual», «levanta el centro»).
        vacios = [i for i, p in enumerate(pasos, 1) if not p["nuevos"]]
        if [i for i in vacios if i != len(pasos)]:
            fallos.append(f"{nombre}: pasos vacíos que no son el último: {vacios}")

        # Nada fuera del lienzo.
        vx, vy, vw, vh = _marco([p for paso in pasos for p in paso["nuevos"]])
        for paso in pasos:
            for p in paso["nuevos"]:
                for x, y in _caja(p):
                    if not (vx - 0.5 <= x <= vx + vw + 0.5 and vy - 0.5 <= y <= vy + vh + 0.5):
                        fallos.append(f"{nombre}: un palito se sale del lienzo en ({x:.0f}, {y:.0f})")
                        break
        print(f"  {nombre:<10} {len(pasos)} pasos · {n:>3} palitos · "
              f"lienzo {vw:.0f}×{vh:.0f}")

    if fallos:
        print("\n✖ " + "\n✖ ".join(sorted(set(fallos))))
        raise SystemExit(1)
    print("\nTodo cuadra.")

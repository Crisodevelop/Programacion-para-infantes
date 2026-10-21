# -*- coding: utf-8 -*-
"""
Diagramas de plegado calculados, no dibujados.

Un avión se declara como la secuencia de pliegues que lo produce y de ahí sale
el SVG de cada paso. Escribir a mano las coordenadas de cuarenta diagramas
habría sido más rápido hoy y un callejón sin salida mañana: el día que un paso
esté mal —y algún paso va a estar mal, eso se descubre doblando papel delante
de treinta personas— hay que poder corregirlo moviendo un punto, no redibujando
un SVG que nadie se atreve a tocar.

El modelo es de capas planas. Cada pliegue parte todas las capas por una recta
y refleja la mitad que se mueve; las capas se dibujan superpuestas, que es
exactamente como se ve un diagrama de origami de verdad. No hay que unir
polígonos ni saber qué capa queda encima, y para estos aviones basta.

Dos cosas que el papel hace y el modelo no:

  · Doblar las alas es tridimensional. La convención de los diagramas de toda
    la vida lo resuelve mostrando el avión plano hasta el último pliegue y
    cerrando con una vista en perspectiva. `vista()` es ese cierre, y es el
    único SVG escrito a mano.

  · Algunos pliegues mueven una solapa suelta y no el avión entero: el candado
    del Nakamura levanta la puntita que asoma, nada más. Para eso está `solo`,
    que señala esa solapa con un punto encima de ella. No es un parche: es
    justo la diferencia entre doblar el papel y doblar la solapa.
"""
import math

EPS = 1e-7
A4 = (210.0, 297.0)          # milímetros; con papel carta todo escala igual


# ─── geometría ────────────────────────────────────────────────────────────

def _cruz(a, b, p):
    """>0 a un lado de la recta a→b, <0 al otro, 0 justo encima."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def reflejar(p, a, b):
    """El punto p visto al otro lado de la recta a→b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    px, py = a[0] + t * dx, a[1] + t * dy        # pie de la perpendicular
    return (2 * px - p[0], 2 * py - p[1])


def area(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def centroide(poly):
    """Centroide de área. El de vértices se va hacia donde hay más esquinas, y
    en un triángulo muy afilado eso deja la flecha fuera del papel que se
    mueve."""
    sx = sy = a2 = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        c = x1 * y2 - x2 * y1
        a2 += c
        sx += (x1 + x2) * c
        sy += (y1 + y2) * c
    if abs(a2) < 1e-9:
        return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))
    return (sx / (3 * a2), sy / (3 * a2))


def _limpiar(poly):
    """Quita vértices repetidos y descarta las briznas que deja el recorte."""
    sal = []
    for p in poly:
        if not sal or abs(p[0] - sal[-1][0]) > 1e-6 or abs(p[1] - sal[-1][1]) > 1e-6:
            sal.append(p)
    if len(sal) > 1 and abs(sal[0][0] - sal[-1][0]) < 1e-6 and abs(sal[0][1] - sal[-1][1]) < 1e-6:
        sal.pop()
    return sal if len(sal) >= 3 and area(sal) > 1e-4 else []


def recortar(poly, a, b, signo):
    """Sutherland–Hodgman: la parte de `poly` que cae del lado `signo` de a→b."""
    sal = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        cp, cq = signo * _cruz(a, b, p), signo * _cruz(a, b, q)
        if cp >= -EPS:
            sal.append(p)
        if (cp > EPS and cq < -EPS) or (cp < -EPS and cq > EPS):
            t = cp / (cp - cq)
            sal.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return _limpiar(sal)


def contiene(poly, p):
    """¿Cae el punto dentro del polígono? Lanzando un rayo y contando cruces."""
    dentro = False
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > p[1]) != (y2 > p[1]):
            x = x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1)
            if x > p[0]:
                dentro = not dentro
    return dentro


def entre(p, q, t):
    """El punto a la fracción t del camino de p a q."""
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def bis(v, p, q, largo=600.0):
    """Un segundo punto sobre la bisectriz del ángulo p–v–q.

    «Lleva este borde hasta aquel otro» es una bisectriz exacta. Declararlo así
    evita sembrar el temario de coordenadas calculadas a mano que nadie sabrá
    recalcular dentro de un año."""
    def u(w):
        d = math.hypot(w[0] - v[0], w[1] - v[1])
        return ((w[0] - v[0]) / d, (w[1] - v[1]) / d)
    ux, uy = u(p)
    wx, wy = u(q)
    bx, by = ux + wx, uy + wy
    d = math.hypot(bx, by)
    if d < EPS:                    # p y q opuestos: la bisectriz es la perpendicular
        return (v[0] - uy * largo, v[1] + ux * largo)
    return (v[0] + bx / d * largo, v[1] + by / d * largo)


def mediatriz(p, q, largo=600.0):
    """Los dos extremos de la recta sobre la que hay que doblar para que p
    caiga justo encima de q."""
    m = entre(p, q, 0.5)
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dy)
    px, py = -dy / d, dx / d
    return ((m[0] + px * largo, m[1] + py * largo),
            (m[0] - px * largo, m[1] - py * largo))


# ─── la hoja ──────────────────────────────────────────────────────────────

class Hoja:
    def __init__(self, ancho=A4[0], alto=A4[1]):
        self.capas = [([(0.0, 0.0), (ancho, 0.0), (ancho, alto), (0.0, alto)], 0)]
        self.marcas = []                    # pliegues ya hechos, se dibujan finos
        self.inicial = ancho * alto

    def doblar(self, a, b, mueve, solo=None):
        """`mueve` es un punto cualquiera del lado que se levanta. Decir «se
        mueve la esquina de arriba a la izquierda» se lee; decir «signo -1», no.

        `solo` es un punto encima de la solapa que hay que levantar: cuando se
        da, las demás capas ni se enteran. Sin eso el candado del Nakamura
        arrastraría medio avión.

        Una solapa se ha doblado al menos una vez, así que la hoja de debajo
        queda fuera aunque el punto caiga encima de ella: es lo que la
        distingue, y sin esa condición el candado se lleva el fuselaje."""
        signo = 1.0 if _cruz(a, b, mueve) > 0 else -1.0
        nuevas = []
        for poly, veces in self.capas:
            if solo is not None and not (veces and contiene(poly, solo)):
                nuevas.append((poly, veces))
                continue
            quieta = recortar(poly, a, b, -signo)
            movida = recortar(poly, a, b, signo)
            if quieta:
                nuevas.append((quieta, veces))
            if movida:
                nuevas.append(([reflejar(p, a, b) for p in movida], veces + 1))
        self.capas = nuevas
        return self

    def cortar(self, a, b, mantiene):
        """Recorta por la recta a→b y tira lo que queda del otro lado.

        Hasta ahora ningún avión perdía papel, pero el aro empieza por hacer un
        cuadrado de una hoja A4 y el recorte que sobra es justo el ala. El área
        de referencia baja con el corte: si no, la autocomprobación cantaría un
        fallo cada vez que se usan las tijeras."""
        signo = 1.0 if _cruz(a, b, mantiene) > 0 else -1.0
        self.capas = [(q, v) for q, v in
                      ((recortar(poly, a, b, signo), veces) for poly, veces in self.capas)
                      if q]
        self.inicial = self.area_total()
        return self

    def abrir(self, poly, marca=None):
        """Desdobla: el papel vuelve a ser una sola capa plana.

        El modelo de capas sabe doblar pero no deshacer —una capa no recuerda de
        dónde vino—, así que la forma resultante se declara. Es honesto: en el
        papel tú también sabes qué queda cuando abres."""
        self.capas = [([tuple(map(float, p)) for p in poly], 0)]
        if marca:
            self.marcas.append(marca)
        self.inicial = self.area_total()
        return self

    def marcar(self, a, b):
        """Dobla y abre: queda la raya y el papel como estaba.

        Solo estas dejan marca. Un pliegue de verdad se convierte en un borde
        del papel y ya se dibuja como tal; volver a pintarlo de puntos llena el
        diagrama de rayas que no hay que doblar."""
        self.marcas.append((a, b))
        return self

    def aplicar(self, paso):
        if paso["op"] == "doblar":
            for a, b, mueve in paso["pliegues"]:
                self.doblar(a, b, mueve, paso["solo"])
        elif paso["op"] == "marcar":
            for a, b, _ in paso["pliegues"]:
                self.marcar(a, b)
        elif paso["op"] == "cortar":
            a, b, mantiene = paso["pliegues"][0]
            self.cortar(a, b, mantiene)
        elif paso["op"] == "abrir":
            self.abrir(paso["forma"], paso["marca"])
        return self

    def puntos(self):
        return [p for poly, _ in self.capas for p in poly]

    def area_total(self):
        return sum(area(poly) for poly, _ in self.capas)


# ─── vocabulario de pasos ─────────────────────────────────────────────────
#
#  Un avión es una lista de estos. `texto` es lo que se lee al lado del dibujo.

def _paso(op, pliegues, texto, tipo, solo, detalle):
    return {"op": op, "pliegues": pliegues, "texto": texto, "tipo": tipo,
            "solo": solo, "detalle": detalle}


def doblar(a, b, mueve, texto, tipo="valle", solo=None, detalle=""):
    """`texto` es la orden y nada más: es lo que se proyecta, y desde el fondo
    del aula solo se lee una frase. El porqué, el truco y el aviso van en
    `detalle`, que sale en la guía impresa y no en la pantalla."""
    return _paso("doblar", [(a, b, mueve)], texto, tipo, solo, detalle)


def doblar_par(uno, otro, texto, tipo="valle", solo=None, detalle=""):
    """Los dos pliegues simétricos de un mismo paso. Se declaran juntos porque
    en la mesa se hacen juntos, y separarlos en dos diagramas sugiere un orden
    que no existe."""
    return _paso("doblar", [uno, otro], texto, tipo, solo, detalle)


def doblar_serie(pliegues, texto, tipo="valle", solo=None, detalle=""):
    """Varios pliegues seguidos en un mismo paso, para un borde que se enrolla
    sobre sí mismo. Se declaran juntos porque en la mesa es un solo gesto
    repetido, y separarlos en cuatro diagramas iguales no enseña nada."""
    return _paso("doblar", list(pliegues), texto, tipo, solo, detalle)


def cortar(a, b, mantiene, texto, detalle=""):
    return _paso("cortar", [(a, b, mantiene)], texto, "corte", None, detalle)


def abrir(forma, texto, marca=None, detalle=""):
    d = _paso("abrir", [], texto, "valle", None, detalle)
    d["forma"], d["marca"] = forma, marca
    return d


def marcar(a, b, mueve, texto, detalle=""):
    return _paso("marcar", [(a, b, mueve)], texto, "valle", None, detalle)


def llevar(desde_p, hasta_p, texto, tipo="valle", solo=None, detalle=""):
    """Dobla de forma que `desde_p` acabe justo encima de `hasta_p`.

    Es como se dan las instrucciones de verdad —«lleva la esquina hasta la
    raya del centro»— y la recta del pliegue sale sola."""
    a, b = mediatriz(desde_p, hasta_p)
    return _paso("doblar", [(a, b, desde_p)], texto, tipo, solo, detalle)


def llevar_par(uno, otro, texto, tipo="valle", solo=None, detalle=""):
    pliegues = []
    for desde_p, hasta_p in (uno, otro):
        a, b = mediatriz(desde_p, hasta_p)
        pliegues.append((a, b, desde_p))
    return _paso("doblar", pliegues, texto, tipo, solo, detalle)


def vista(svg_crudo, texto, detalle=""):
    """Un dibujo a mano intercalado en la secuencia: la vista en perspectiva
    del final, o un detalle que no es un pliegue plano (un corte, un tubo)."""
    return {"op": "vista", "svg": svg_crudo, "texto": texto, "detalle": detalle,
            "pliegues": [], "solo": None}


# ─── dibujo ───────────────────────────────────────────────────────────────

def _n(v):
    """Números cortos: cuarenta diagramas con seis decimales por punto pesan de
    más y no se leen mejor."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _d(poly, cerrar=True):
    partes = [f"M{_n(poly[0][0])} {_n(poly[0][1])}"]
    partes += [f"L{_n(p[0])} {_n(p[1])}" for p in poly[1:]]
    if cerrar:
        partes.append("Z")
    return "".join(partes)


def _t_de(a, b, p):
    """Dónde cae p a lo largo de la recta a→b, en unidades de |b-a|."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    return ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)


def _tramo_en(poly, a, b):
    """El tramo de la recta a→b que queda dentro del polígono, o None.

    Todas las capas son convexas —una hoja rectangular recortada por rectas y
    reflejada sigue siéndolo—, así que la recta entra una vez y sale una vez."""
    ts = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        cp, cq = _cruz(a, b, p), _cruz(a, b, q)
        if abs(cp) <= EPS:
            ts.append(_t_de(a, b, p))
        elif (cp > EPS and cq < -EPS) or (cp < -EPS and cq > EPS):
            u = cp / (cp - cq)
            ts.append(_t_de(a, b, (p[0] + u * (q[0] - p[0]), p[1] + u * (q[1] - p[1]))))
    return (min(ts), max(ts)) if len(ts) >= 2 and max(ts) - min(ts) > 1e-9 else None


def _rayas(a, b, capas, sobra=0.0):
    """Los trozos de la recta a→b que caen encima de papel.

    Sin esto las rayas de pliegue cruzan el dibujo de lado a lado y se juntan
    en equis en pleno aire, porque las rectas se declaran con puntos lejanos:
    `bis` devuelve uno a 600 mm. Un diagrama de origami solo dibuja el pliegue
    donde hay papel que doblar, más un dedo de más para que se vea dónde
    termina."""
    tramos = sorted(t for t in (_tramo_en(poly, a, b) for poly, _ in capas) if t)
    if not tramos:
        return []
    unidos = [list(tramos[0])]
    for t0, t1 in tramos[1:]:
        if t0 <= unidos[-1][1] + 1e-9:
            unidos[-1][1] = max(unidos[-1][1], t1)
        else:
            unidos.append([t0, t1])
    d = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    m = sobra / d
    return [(entre(a, b, t0 - m), entre(a, b, t1 + m)) for t0, t1 in unidos]


def _flecha(c0, c1, escala, vuelta=False):
    """Arco de c0 a c1 con la punta al final. Se comba en paralelo al pliegue:
    una flecha recta cae justo encima de la línea de pliegue y se confunde
    con ella."""
    dx, dy = c1[0] - c0[0], c1[1] - c0[1]
    largo = math.hypot(dx, dy)
    if largo < EPS:
        return ""
    mx, my = (c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2
    px, py = -dy / largo, dx / largo                  # perpendicular a la cuerda
    comba = largo * 0.30 * (-1 if vuelta else 1)
    ctrl = (mx + px * comba, my + py * comba)

    # Tangente al final de la Bézier cuadrática: el vector control→destino.
    tx, ty = c1[0] - ctrl[0], c1[1] - ctrl[1]
    tl = math.hypot(tx, ty) or 1.0
    tx, ty = tx / tl, ty / tl
    p = escala * (0.7 if vuelta else 1.0)
    base = (c1[0] - tx * p, c1[1] - ty * p)
    ala = (-ty * p * 0.42, tx * p * 0.42)
    punta = _d([c1, (base[0] + ala[0], base[1] + ala[1]),
                (base[0] - ala[0], base[1] - ala[1])])

    c = "dg-vuelta" if vuelta else "dg-flecha"
    return (f'<path class="{c}" d="M{_n(c0[0])} {_n(c0[1])}'
            f'Q{_n(ctrl[0])} {_n(ctrl[1])} {_n(c1[0])} {_n(c1[1])}"/>'
            f'<path class="{c}-p" d="{punta}"/>')


def dibujar(hoja, paso, caja):
    """El SVG de un paso: el papel como está ahora y el pliegue que viene.

    Se dibuja el estado ANTERIOR a la operación a propósito. Un diagrama que
    enseñara el resultado no diría qué hay que hacer para llegar a él."""
    x0, y0, w, h = caja
    escala = math.hypot(w, h) * 0.042
    piezas = [f'<path class="dg-capa" d="{_d(poly)}"/>'
              for poly, _ in sorted(hoja.capas, key=lambda c: c[1])]

    for a, b in hoja.marcas:
        for seg in _rayas(a, b, hoja.capas):
            piezas.append(f'<path class="dg-marca" d="{_d(seg, False)}"/>')

    if paso["op"] == "abrir" and paso["marca"]:
        # Se enseña el papel doblado y por dónde va a quedar la raya al abrirlo.
        for seg in _rayas(paso["marca"][0], paso["marca"][1], hoja.capas):
            piezas.append(f'<path class="dg-marca" d="{_d(seg, False)}"/>')
        # La flecha va de la solapa doblada a donde va a caer al abrirla.
        c = centroide(max((p for p, _ in hoja.capas), key=area))
        piezas.append(_flecha(c, reflejar(c, paso["marca"][0], paso["marca"][1]), escala))

    clase = {"corte": "dg-corte", "montana": "dg-mont"}.get(paso.get("tipo"), "dg-valle")
    for a, b, mueve in paso["pliegues"]:
        for seg in _rayas(a, b, hoja.capas, sobra=escala * 0.5):
            piezas.append(f'<path class="{clase}" d="{_d(seg, False)}"/>')

        if paso["op"] == "cortar":
            continue          # un corte no lleva flecha: no se mueve nada

        # La flecha nace en el trozo de papel que de verdad se levanta.
        signo = 1.0 if _cruz(a, b, mueve) > 0 else -1.0
        movidas = [recortar(poly, a, b, signo) for poly, veces in hoja.capas
                   if paso["solo"] is None or (veces and contiene(poly, paso["solo"]))]
        movidas = [m for m in movidas if m]
        if movidas:
            c0 = centroide(max(movidas, key=area))
            c1 = reflejar(c0, a, b)
            piezas.append(_flecha(c0, c1, escala))
            if paso["op"] == "marcar":
                piezas.append(_flecha(entre(c1, c0, 0.18), entre(c1, c0, 0.82),
                                      escala, vuelta=True))

    return (f'<svg class="dg" viewBox="{_n(x0)} {_n(y0)} {_n(w)} {_n(h)}" '
            f'role="img" aria-hidden="true">{"".join(piezas)}</svg>')


def diagramas(pasos, ancho=A4[0], alto=A4[1], margen=0.09):
    """De la lista de pliegues a la lista de pasos dibujados.

    Dos pasadas. La primera recorre todo para saber cuánto ocupa el avión en su
    momento más ancho; la segunda dibuja. Sin eso cada diagrama tendría su
    propia escala y el avión daría un salto de tamaño entre un paso y el
    siguiente, que es justo lo que vuelve ilegible una secuencia."""
    hoja = Hoja(ancho, alto)
    todos = list(hoja.puntos())
    for paso in pasos:
        hoja.aplicar(paso)
        todos += hoja.puntos()

    xs = [p[0] for p in todos]
    ys = [p[1] for p in todos]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    pad = max(w, h) * margen
    caja = (min(xs) - pad, min(ys) - pad, w + 2 * pad, h + 2 * pad)

    hoja = Hoja(ancho, alto)
    salida = []
    for paso in pasos:
        svg = paso["svg"] if paso["op"] == "vista" else dibujar(hoja, paso, caja)
        salida.append({"texto": paso["texto"], "detalle": paso["detalle"], "svg": svg})
        if paso["op"] != "vista":
            hoja.aplicar(paso)
    return salida


# ─── estilo ───────────────────────────────────────────────────────────────
#
#  Los colores son variables para que la misma marca sirva proyectada sobre
#  fondo oscuro y impresa en blanco. Ninguna regla cuelga de body/html/:root:
#  `comprobar_css` en exportar_nextjs.py aborta el build si alguna lo hiciera.

CSS = """
.dg{display:block;width:100%;height:auto;overflow:visible}
.dg-capa{fill:var(--dg-papel);stroke:var(--dg-borde);stroke-width:1.7;
  stroke-linejoin:round}
.dg-marca{fill:none;stroke:var(--dg-marca);stroke-width:1.1;stroke-dasharray:1.5 5;
  stroke-linecap:round}
.dg-valle{fill:none;stroke:var(--dg-pliegue);stroke-width:2;stroke-dasharray:9 6}
.dg-mont{fill:none;stroke:var(--dg-pliegue);stroke-width:2;stroke-dasharray:14 5 2.5 5}
.dg-flecha{fill:none;stroke:var(--dg-pliegue);stroke-width:2.2;stroke-linecap:round}
.dg-flecha-p{fill:var(--dg-pliegue);stroke:none}
.dg-vuelta{fill:none;stroke:var(--dg-pliegue);stroke-width:1.3;stroke-dasharray:5 4;opacity:.6}
.dg-vuelta-p{fill:var(--dg-pliegue);stroke:none;opacity:.6}
.dg-corte{fill:none;stroke:var(--dg-pliegue);stroke-width:2.2;stroke-linecap:round}
.dg-borde-grueso{fill:none;stroke:var(--dg-borde);stroke-width:4.5;stroke-linecap:round}
.dg-guia{fill:none;stroke:var(--dg-marca);stroke-width:1.2;stroke-dasharray:4 4}
"""


# ─── autocomprobación ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import contenido as C

    fallos = 0
    for avion in C.AVIONES:
        hoja = Hoja()
        for i, paso in enumerate(avion["pasos"], 1):
            if paso["op"] == "vista":
                continue
            hoja.aplicar(paso)
            # Un pliegue no crea ni destruye papel. Si el área cambia, el
            # recorte perdió un trozo y el diagrama estaría mintiendo.
            if abs(hoja.area_total() - hoja.inicial) > 0.5:
                print(f"  ✗ {avion['id']} paso {i}: el área cambió "
                      f"({hoja.area_total():.1f} vs {hoja.inicial:.1f})")
                fallos += 1
            if len(hoja.capas) > 80:
                print(f"  ✗ {avion['id']} paso {i}: {len(hoja.capas)} capas, algo se disparó")
                fallos += 1

        ds = diagramas(avion["pasos"])
        if len(ds) != len(avion["pasos"]):
            print(f"  ✗ {avion['id']}: {len(ds)} diagramas para {len(avion['pasos'])} pasos")
            fallos += 1
        vacios = [i for i, d in enumerate(ds, 1) if not d["svg"].strip()]
        if vacios:
            print(f"  ✗ {avion['id']}: diagramas vacíos en {vacios}")
            fallos += 1
        print(f"  · {avion['id']}: {len(ds)} pasos, {len(hoja.capas)} capas al final")

    print()
    raise SystemExit(f"  {fallos} fallo(s) de geometría\n" if fallos else 0)


# ─── los dibujos que no son pliegues ──────────────────────────────────────
#
#  Abrir las alas, cortar un alerón o enrollar un tubo no son pliegues planos,
#  así que el motor de capas no los alcanza. Son funciones con parámetros y no
#  SVG pegados a mano: `frente(22)` y `frente(6, winglet=14)` son dos aviones
#  distintos escritos igual, y eso es lo que hay que poder comparar.

def _svg(piezas, ancho=200.0, alto=120.0):
    return (f'<svg class="dg" viewBox="0 0 {_n(ancho)} {_n(alto)}" '
            f'role="img" aria-hidden="true">{"".join(piezas)}</svg>')


def frente(diedro=20.0, winglet=0.0, fuselaje=34.0):
    """El avión visto de frente, que es donde se comprueba la Y.

    El ángulo de las alas es lo único que separa un avión terminado de otro:
    plano vuela rápido y se cae de lado, muy abierto se frena. Por eso el
    diedro es el parámetro y no una decisión escondida en el dibujo."""
    cx, y0, media, t = 100.0, 62.0, 74.0, 5.0
    dy = media * math.tan(math.radians(diedro))
    piezas = [f'<path class="dg-guia" d="M16 {_n(y0)}L184 {_n(y0)}"/>']
    for s in (-1.0, 1.0):
        px, py = cx + s * media, y0 - dy
        piezas.append(f'<path class="dg-capa" d="'
                      f'{_d([(cx, y0), (px, py), (px, py + t), (cx, y0 + t)])}"/>')
        if winglet:
            piezas.append(f'<path class="dg-capa" d="'
                          f'{_d([(px, py), (px + s * 3.5, py - winglet), (px + s * 3.5, py - winglet + t), (px, py + t)])}"/>')
    piezas.append(f'<path class="dg-capa" d="'
                  f'{_d([(cx - 3.6, y0 + t), (cx + 3.6, y0 + t), (cx + 3.6, y0 + t + fuselaje), (cx - 3.6, y0 + t + fuselaje)])}"/>')
    return _svg(piezas)


def corte_alerones():
    """La cola vista desde arriba, con los dos cortes y una lengüeta ya
    levantada. Es el paso en que el avión deja de ser una manualidad."""
    izq = [(14.0, 30.0), (94.0, 46.0), (94.0, 96.0), (14.0, 96.0)]
    der = [(200.0 - p[0], p[1]) for p in izq]
    piezas = [
        f'<path class="dg-capa" d="{_d(izq)}"/>',
        f'<path class="dg-capa" d="{_d(der)}"/>',
        f'<path class="dg-capa" d="{_d([(94.0, 34.0), (106.0, 34.0), (106.0, 96.0), (94.0, 96.0)])}"/>',
    ]
    for x in (40.0, 68.0, 132.0, 160.0):
        piezas.append(f'<path class="dg-corte" d="M{_n(x)} 96L{_n(x)} 70"/>')
    # La lengüeta de la izquierda ya levantada: el paso se entiende de un vistazo.
    piezas.append(f'<path class="dg-guia" d="M40 70L68 70"/>')
    piezas.append(_flecha((54.0, 88.0), (54.0, 40.0), 11.0))
    return _svg(piezas)


def anillo(fase):
    """El aro pelado: una tira de papel cerrada en círculo y nada más.

    No tiene alas, ni punta, ni nada pegado. Vuela porque el aire entra por el
    agujero y sale por detrás, y eso solo basta para que no se tumbe. Se dibuja
    casi de frente, que es como se ve en la mano y como se entiende que por ahí
    se ve el otro lado."""
    CX, CY = 100.0, 60.0
    RX, RY = 42.0, 45.0
    HUECO = 8.0                      # el grosor del papel visto de canto

    def _elipse(cx, cy, rx, ry):
        return (f"M{_n(cx - rx)} {_n(cy)}"
                f"a{_n(rx)} {_n(ry)} 0 1 0 {_n(2 * rx)} 0"
                f"a{_n(rx)} {_n(ry)} 0 1 0 {_n(-2 * rx)} 0Z")

    def circulo():
        # Corona con el hueco recortado: el agujero del medio es el avión
        # entero, y una elipse rellena encima lo taparía. `evenodd` lo vacía.
        return [f'<path class="dg-capa" fill-rule="evenodd" d="'
                f'{_elipse(CX, CY, RX, RY)}{_elipse(CX + HUECO, CY, RX - HUECO, RY - HUECO)}"/>']

    if fase == 1:                                  # curvar la tira
        piezas = [
            f'<path class="dg-capa" fill="none" d="M30 98Q100 4 170 98"/>',
            f'<path class="dg-capa" fill="none" d="M30 112Q100 20 170 112"/>',
            f'<path class="dg-capa" d="M30 98L30 112"/>',
            f'<path class="dg-capa" d="M170 98L170 112"/>',
        ]
        piezas.append(_flecha((22.0, 106.0), (74.0, 106.0), 11.0))
        piezas.append(_flecha((178.0, 106.0), (126.0, 106.0), 11.0))
        return _svg(piezas)

    piezas = circulo()
    if fase == 2:                                  # el solape, pegado
        piezas.append(f'<path class="dg-marca" d="M{_n(CX)} {_n(CY - RY)}L{_n(CX + HUECO)} {_n(CY - RY + HUECO)}"/>')
        for dx in (-7.0, 0.0, 7.0):
            piezas.append(f'<path class="dg-corte" d="'
                          f'M{_n(CX + dx)} {_n(CY + RY - 3)}L{_n(CX + dx)} {_n(CY + RY + 5)}"/>')
    if fase == 3:                                  # cómo se lanza
        piezas.append(_flecha((46.0, 16.0), (10.0, 16.0), 11.0))
    return _svg(piezas)


def aro(fase):
    """El planeador de aro: un cilindro de papel con el borde de ataque
    enrollado y un ala cruzada por encima.

    Nada de esto son pliegues planos —el papel se curva, y una superficie
    curva no se puede reflejar sobre una recta—, así que va dibujado. El borde
    grueso se pinta doble a propósito: es donde está el peso, y es lo que
    distingue un aro que vuela de un tubo que se cae."""
    CX_F, CX_T, CY = 66.0, 140.0, 62.0     # centros del frente y del fondo
    RX, RY = 15.0, 40.0                    # el cilindro visto casi de canto

    def cilindro():
        piezas = [
            f'<path class="dg-capa" d="M{_n(CX_F)} {_n(CY - RY)}L{_n(CX_T)} {_n(CY - RY)}"/>',
            f'<path class="dg-capa" d="M{_n(CX_F)} {_n(CY + RY)}L{_n(CX_T)} {_n(CY + RY)}"/>',
            f'<ellipse class="dg-capa" cx="{_n(CX_T)}" cy="{_n(CY)}" rx="{_n(RX)}" ry="{_n(RY)}" fill="none"/>',
            f'<ellipse class="dg-capa" cx="{_n(CX_F)}" cy="{_n(CY)}" rx="{_n(RX)}" ry="{_n(RY)}" fill="none"/>',
            # El borde de ataque, enrollado: doble raya, que es lo que se ve.
            f'<ellipse class="dg-borde-grueso" cx="{_n(CX_F + 4)}" cy="{_n(CY)}" '
            f'rx="{_n(RX)}" ry="{_n(RY - 3)}" fill="none"/>',
        ]
        return piezas

    def ala():
        # La tira cruzada por encima, con las puntas levantadas.
        y = CY - RY
        cuerpo = [(22.0, y - 12), (98.0, y - 26), (178.0, y - 10),
                  (178.0, y - 2), (98.0, y - 18), (22.0, y - 4)]
        return [f'<path class="dg-capa" d="{_d(cuerpo)}"/>',
                f'<path class="dg-capa" d="{_d([(22.0, y - 12), (14.0, y - 20), (14.0, y - 12), (22.0, y - 4)])}"/>',
                f'<path class="dg-capa" d="{_d([(178.0, y - 10), (186.0, y - 19), (186.0, y - 11), (178.0, y - 2)])}"/>']

    if fase == 1:                                   # arquear la hoja
        # Vista de canto: la hoja combada, y los dos extremos yendo el uno
        # hacia el otro. Es lo único que hay que entender de este paso.
        piezas = [
            f'<path class="dg-capa" fill="none" d="M34 96Q100 8 166 96"/>',
            f'<path class="dg-capa" fill="none" d="M34 96Q100 20 166 96" opacity=".45"/>',
            f'<path class="dg-borde-grueso" d="M34 96L34 84"/>',
            f'<path class="dg-borde-grueso" d="M166 96L166 84"/>',
        ]
        piezas.append(_flecha((26.0, 108.0), (78.0, 108.0), 11.0))
        piezas.append(_flecha((174.0, 108.0), (122.0, 108.0), 11.0))
        return _svg(piezas)

    if fase == 2:                                   # unir los extremos y grapar
        piezas = cilindro()
        for dy in (-14.0, 0.0, 14.0):
            piezas.append(f'<path class="dg-corte" d="'
                          f'M{_n(CX_T - 6)} {_n(CY + dy)}L{_n(CX_T + 6)} {_n(CY + dy)}"/>')
        return _svg(piezas)

    if fase == 3:                                   # el ala, de la tira que sobró
        tira = [(30.0, 40.0), (170.0, 40.0), (170.0, 80.0), (30.0, 80.0)]
        piezas = [f'<path class="dg-capa" d="{_d(tira)}"/>',
                  f'<path class="dg-marca" d="M100 34L100 86"/>',
                  f'<path class="dg-corte" fill="none" d="M30 46Q100 30 170 52"/>']
        return _svg(piezas)

    piezas = cilindro() + ala()
    if fase == 5:                                   # cómo se lanza
        piezas.append(_flecha((44.0, 108.0), (12.0, 108.0), 11.0))
    return _svg(piezas)

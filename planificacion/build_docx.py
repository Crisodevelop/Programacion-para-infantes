# -*- coding: utf-8 -*-
"""
Genera Planificacion_Programacion_1ro_a_3ro_Secundaria.docx
clonando el .docx original como plantilla: conserva styles.xml, theme, numbering,
footer y margenes, y reescribe unicamente word/document.xml.
"""
import os, sys, shutil, zipfile, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C

# La plantilla vive en el repositorio: de ella solo se toman la cabecera de
# word/document.xml, el sectPr y el resto del paquete (estilos, pie de página).
# Antes se leía de Descargas, y el día que ese archivo desapareció el Word dejó
# de generarse.
PLANTILLA = os.path.join(HERE, "plantilla", "Planificacion_Programacion_1ro_a_3ro_Secundaria.docx")
SALIDA = os.path.join(HERE, "salida", "Planificacion_Programacion_1ro_a_3ro_Secundaria.docx")

P = C.PALETA
NAVY, GRIS_TX = P["navy"], "667085"
COL = {"n1": (P["n1"], P["n1_bg"]), "n2": (P["n2"], P["n2_bg"]),
       "n3": (P["n3"], P["n3_bg"]), "co": (P["co"], P["co_bg"])}

def x(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def r(t, b=False, color=None, sz=None, it=False, br=False, mono=False):
    rpr = ""
    # rFonts va el primero: el esquema de w:rPr exige ese orden.
    if mono: rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
    if b: rpr += "<w:b/>"
    if it: rpr += "<w:i/>"
    if color: rpr += f'<w:color w:val="{color}"/>'
    if sz: rpr += f'<w:sz w:val="{sz}"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    pre = "<w:br/>" if br else ""
    return f'<w:r>{rpr}{pre}<w:t xml:space="preserve">{x(t)}</w:t></w:r>'

def p(runs, before=0, after=0, jc=None, keep=False):
    pr = ""
    if keep: pr += "<w:keepNext/>"
    if before or after:
        pr += f'<w:spacing{f" w:before={chr(34)}{before}{chr(34)}" if before else ""}{f" w:after={chr(34)}{after}{chr(34)}" if after else ""}/>'
    if jc: pr += f'<w:jc w:val="{jc}"/>'
    pr = f"<w:pPr>{pr}</w:pPr>" if pr else ""
    body = runs if isinstance(runs, str) else "".join(runs)
    return f"<w:p>{pr}{body}</w:p>"

MAR = '<w:tcMar><w:top w:w="80" w:type="dxa"/><w:start w:w="70" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:end w:w="70" w:type="dxa"/></w:tcMar>'
NOBORDER = '<w:tcBorders><w:top w:val="nil"/><w:bottom w:val="nil"/><w:left w:val="nil"/><w:right w:val="nil"/></w:tcBorders>'

def tc(w, paras, shd=None, span=0, valign="top"):
    props = f'<w:tcW w:type="dxa" w:w="{w}"/>'
    if span: props += f'<w:gridSpan w:val="{span}"/>'
    props += NOBORDER
    if shd: props += f'<w:shd w:fill="{shd}"/>'
    props += MAR + f'<w:vAlign w:val="{valign}"/>'
    body = paras if isinstance(paras, str) else "".join(paras)
    return f"<w:tc><w:tcPr>{props}</w:tcPr>{body}</w:tc>"

def tr(cells, header=False):
    pr = "<w:trPr><w:tblHeader w:val=\"true\"/></w:trPr>" if header else ""
    return f"<w:tr>{pr}{''.join(cells)}</w:tr>"

ANCHO = 10368   # 12240 de pagina - 936 de margen izquierdo - 936 del derecho

def G(*partes):
    """Escala una rejilla de columnas para que sume exactamente el ancho util."""
    tot = sum(partes)
    ws = [round(w * ANCHO / tot) for w in partes]
    ws[-1] += ANCHO - sum(ws)
    return ws

def tbl(grid, rows):
    g = "".join(f'<w:gridCol w:w="{w}"/>' for w in grid)
    return (f'<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="{ANCHO}"/>'
            '<w:tblLayout w:type="fixed"/><w:tblLook w:firstColumn="1" w:firstRow="1"'
            ' w:lastColumn="0" w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0"/>'
            f'</w:tblPr><w:tblGrid>{g}</w:tblGrid>{"".join(rows)}</w:tbl>')

def head_row(grid, labels, color):
    return tr([tc(w, p(r(l, b=True, color="FFFFFF", sz=15), jc="center"), shd=color)
               for w, l in zip(grid, labels)], header=True)

PAGEBREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
def h1(t, color=NAVY, sz=38, before=0):
    return p(r(t, b=True, color=color, sz=sz), before=before, after=120, keep=True)
def h2(t, color=NAVY):
    return p(r(t, b=True, color=color, sz=24), before=340, after=120, keep=True)
def para(t, sz=None, color=None, before=0, after=140):
    return p(r(t, sz=sz, color=color), before=before, after=after)


G5 = G(605, 1800, 2232, 4248, 1656)      # SEM / TEMA / OBJETIVO / DESARROLLO / RECURSOS
G4 = G(2100, 2100, 3300, 3041)
G3 = G(2200, 2200, 6141)
G2 = G(4270, 6271)


def portada():
    gb = G(1, 1, 1)
    band = tbl(gb, [tr([
        tc(gb[k], p(r(t, b=True, color="FFFFFF", sz=28), jc="center"), shd=c)
        for k, (t, c) in enumerate((("1RO", P["n1"]), ("2DO", P["n2"]), ("3RO", P["n3"])))])])
    return "".join([
        p(r("PLANIFICACIÓN ACADÉMICA", b=True, color=P["n1"], sz=28), before=1100, jc="center"),
        p(r("PROGRAMACIÓN Y PENSAMIENTO", b=True, color=NAVY, sz=52), before=260, jc="center"),
        p(r("COMPUTACIONAL CON PYTHON", b=True, color=NAVY, sz=52), jc="center"),
        p(r("1ro a 3ro de Secundaria", b=True, color=NAVY, sz=26), before=300, jc="center"),
        p(r("12 semanas por curso  ·  1 sesión semanal de 45 – 50 minutos", color=GRIS_TX, sz=20),
          before=120, after=520, jc="center"),
        band,
        p(r("Aprender haciendo  ·  Retos prácticos  ·  Páginas web  ·  Juegos  ·  Proyectos",
            color=GRIS_TX, sz=20), before=520, jc="center"),
        p(r("Área de Tecnología / Informática", b=True, color=NAVY, sz=20), before=900, jc="center"),
        p([r(C.DOCENTE, b=True, color=NAVY, sz=22), r(f"   ·   {C.ESCUELA}   ·   Año escolar 2026 – 2027", color=GRIS_TX, sz=20)],
          before=200, jc="center"),
        PAGEBREAK])


def marco():
    o = [h1("MARCO GENERAL DE LA PLANIFICACIÓN")]
    o.append(para("Ruta progresiva: comprender la lógica → escribir código → desarrollar soluciones web. "
                  "Esta planificación trabaja con Python en los tres niveles, dentro del navegador, "
                  "con HTML y CSS para la página. "
                  "Los objetivos de aprendizaje, los componentes de evaluación y sus pesos no cambian.", after=240))
    gn = G(1400, 9141)
    filas = []
    for niv in C.NIVELES:
        c, bg = COL[niv["color"]]
        filas.append(tr([
            tc(gn[0], p(r(niv["titulo"].replace(" DE SECUNDARIA", ""), b=True, color="FFFFFF", sz=24), jc="center"), shd=c, valign="center"),
            tc(gn[1], p([r(niv["nombre"], b=True, color=c, sz=22),
                        r(niv["resumen"], sz=16, br=True)]), shd=bg)]))
    o.append(tbl(gn, filas))

    o.append(h2("El horario real"))
    o.append(para("Nueve secciones repartidas en tres días, más cuatro tardes de cocurricular. "
                  "Todo el desarrollo de las clases está calculado sobre estos bloques.", sz=18))
    filas = [head_row(G4, ["SECCIÓN", "DÍA", "HORA", "DURACIÓN"], NAVY)]
    for i, (sec, dia, hora, dur) in enumerate(C.HORARIO_CLASES):
        bg = "F8FAFC" if i % 2 else None
        filas.append(tr([
            tc(G4[0], p(r(sec, b=True, color=NAVY, sz=17)), shd=bg),
            tc(G4[1], p(r(dia, sz=16)), shd=bg),
            tc(G4[2], p(r(hora, sz=16)), shd=bg),
            tc(G4[3], p(r(dur, sz=16, color=GRIS_TX)), shd=bg)]))
    filas.append(tr([
        tc(G4[0], p(r("Cocurricular", b=True, color=P["co"], sz=17)), shd=P["co_bg"]),
        tc(G4[1], p(r("Lunes a jueves", sz=16)), shd=P["co_bg"]),
        tc(G4[2], p(r("14:15 – 15:45", sz=16)), shd=P["co_bg"]),
        tc(G4[3], p(r("90 min", sz=16, color=GRIS_TX)), shd=P["co_bg"])]))
    o.append(tbl(G4, filas))
    o.append(p([r("El jueves es el día crítico. ", b=True, color=NAVY, sz=17), r(C.HORARIO_NOTA, sz=17)], before=160, after=140))
    o.append(p([r("A confirmar con coordinación. ", b=True, color=NAVY, sz=17),
                r("El PDF del horario rotula los bloques de lunes y miércoles como cocurricular de primaria. "
                  "Esta planificación los trata como cocurricular de secundaria. Si finalmente corresponden a "
                  "primaria, esos dos bloques trabajan con Scratch y juegos visuales en lugar del arco de Python.", sz=17)], after=200))

    o.append(semana_dias())

    o.append(h2("Estructura de la clase · de 60 a 45 minutos"))
    o.append(para("Las clases reales duran 45 o 50 minutos. El reparto se recomprime y los minutos "
                  "adicionales de los bloques largos se destinan a un reto opcional, nunca a más explicación.", sz=18))
    ge = G(2100, 1500, 1500, 5441)
    filas = [head_row(ge, ["MOMENTO", "45 MIN", "50 MIN", "QUÉ PASA"], NAVY)]
    for i, (m, a, b, d) in enumerate(C.ESTRUCTURA_CLASE):
        bg = "F8FAFC" if i % 2 else None
        filas.append(tr([
            tc(ge[0], p(r(m, b=True, color=NAVY, sz=17)), shd=bg),
            tc(ge[1], p(r(a, sz=16, color=P["n1"]), jc="center"), shd=bg),
            tc(ge[2], p(r(b, sz=16, color=P["n1"]), jc="center"), shd=bg),
            tc(ge[3], p(r(d, sz=16)), shd=bg)]))
    o.append(tbl(ge, filas))
    o.append(p([r("Regla que lo sostiene. ", b=True, color=NAVY, sz=17), r(C.ESTRUCTURA_REGLA, sz=17)], before=160, after=200))

    o.append(h2("Herramientas · todo funciona desde el navegador"))
    filas = [head_row(G3, ["HERRAMIENTA", "DÓNDE", "CUÁNDO SE USA"], NAVY)]
    for i, (n, d, u) in enumerate(C.ENTORNO):
        bg = "F8FAFC" if i % 2 else None
        filas.append(tr([tc(G3[0], p(r(n, b=True, color=NAVY, sz=17)), shd=bg),
                         tc(G3[1], p(r(d, sz=16, color=GRIS_TX)), shd=bg),
                         tc(G3[2], p(r(u, sz=16)), shd=bg)]))
    o.append(tbl(G3, filas))

    o.append(h2("Python en la página"))
    o.append(para("Lo que se escribe para que el programa hable con la página. Todo el material usa "
                  "estas formas y no otras. Punto de partida: " + C.PLANTILLA + ".", sz=18))
    filas = [head_row(G2, ["QUIERO…", "ASÍ EN PYTHON"], NAVY)]
    for i, (a, b) in enumerate(C.PYTHON_EN_PAGINA):
        bg = "F8FAFC" if i % 2 else None
        filas.append(tr([tc(G2[0], p(r(a, b=True, sz=16, color=NAVY)), shd=bg),
                         tc(G2[1], p(r(b, sz=15, color=NAVY, mono=True)), shd=bg)]))
    o.append(tbl(G2, filas))
    o.append(PAGEBREAK)
    return "".join(o)



def semana_dias():
    LVL = {"1": "n1", "2": "n2", "3": "n3"}
    o = [h2("Tu semana, día por día")]
    o.append(para(C.SEMANA_DIAS_INTRO, sz=18))
    g = G(1300, 950, 4100, 4018)
    filas = [head_row(g, ["DÍA", "CLASES", "BLOQUES DEL DÍA", "QUÉ PREPARAR"], NAVY)]
    for i, d in enumerate(C.SEMANA_DIAS):
        sh = "F8FAFC" if i % 2 else None
        n = d["clases"]
        etq = "—" if n == 0 else (f"{n} clase" if n == 1 else f"{n} clases")
        bloques, first = [], True
        for hora, que, tipo in d["bloques"]:
            if tipo == "clase":
                col = P[LVL[que[0]]]
                runs = [r(hora + "   ", sz=15, color=GRIS_TX, br=not first),
                        r(que, b=True, sz=17, color=col)]
            elif tipo == "cocu":
                runs = [r(hora + "   ", sz=15, color=GRIS_TX, br=not first),
                        r(que, b=True, sz=15, color=P["co"])]
            else:
                runs = [r(hora + "   ", sz=15, color=GRIS_TX, br=not first),
                        r(que, sz=15, color=GRIS_TX)]
            bloques.append(p(runs, before=0 if first else 30))
            first = False
        filas.append(tr([
            tc(g[0], p(r(d["dia"], b=True, sz=20, color=NAVY)), shd=sh),
            tc(g[1], p(r(etq, b=True, sz=16, color=P["n1"] if n else GRIS_TX), jc="center"), shd=sh),
            tc(g[2], bloques, shd=sh),
            tc(g[3], p(r(d["nota"], sz=15)), shd=sh)]))
    o.append(tbl(g, filas))
    return "".join(o)


def semana1():
    o = [h1("LA PRIMERA SEMANA")]
    o.append(para(C.SEMANA1_INTRO, after=240))
    o.append(h2("Bloque fijo · los primeros 20 minutos, igual en los tres niveles"))
    g = G(1200, 2000, 7341)
    filas = [head_row(g, ["MINUTO", "MOMENTO", "QUÉ SE HACE"], NAVY)]
    for i, (a, b, c) in enumerate(C.SEMANA1_FIJO):
        bg = "F8FAFC" if i % 2 else None
        filas.append(tr([tc(g[0], p(r(a, b=True, sz=16, color=P["n1"]), jc="center"), shd=bg),
                         tc(g[1], p(r(b, b=True, sz=17, color=NAVY)), shd=bg),
                         tc(g[2], p(r(c, sz=16)), shd=bg)]))
    o.append(tbl(g, filas))

    o.append(h2("Dinámica preparada · se lleva el resto de la clase"))
    g = G(1100, 3000, 6441)
    filas = [head_row(g, ["NIVEL", "DINÁMICA", "DESARROLLO"], NAVY)]
    for d in C.SEMANA1_DINAMICAS:
        c, bg = COL[d["color"]]
        filas.append(tr([
            tc(g[0], p(r(d["nivel"], b=True, color="FFFFFF", sz=20), jc="center"), shd=c, valign="center"),
            tc(g[1], [p(r(d["nombre"], b=True, color=c, sz=20)),
                      p(r(d["duracion"], sz=15, color=GRIS_TX), before=60)], shd=bg),
            tc(g[2], [p(r(d["desc"], sz=16)),
                      p([r("Materiales. ", b=True, sz=15, color=c), r(d["materiales"], sz=15)], before=90),
                      p([r("Cierre. ", b=True, sz=15, color=c), r(d["cierre"], sz=15)], before=60),
                      p([r("Si sobra tiempo. ", b=True, sz=15, color=c), r(d["extra"], sz=15)], before=60)])]))
    o.append(tbl(g, filas))

    # Por nivel, el guion por minutos y los juegos de reserva. Son opcionales
    # en contenido.py: un nivel que aún no los tiene no deja tabla vacía.
    gg = G(1200, 2000, 7341)
    gj = G(2200, 1100, 4000, 3241)
    for d in C.SEMANA1_DINAMICAS:
        c, bg = COL[d["color"]]
        guion = d.get("guion") or []
        juegos = d.get("juegos") or []
        if guion:
            o.append(p(r(f'{d["nivel"]} · Guion minuto a minuto', b=True, color=c, sz=22),
                       before=340, after=120, keep=True))
            filas = [head_row(gg, ["MINUTO", "MOMENTO", "QUÉ SE HACE"], c)]
            for i, (a, b, t) in enumerate(guion):
                sh = bg if i % 2 == 0 else None
                filas.append(tr([tc(gg[0], p(r(a, b=True, sz=16, color=c), jc="center"), shd=sh),
                                 tc(gg[1], p(r(b, b=True, sz=17, color=NAVY)), shd=sh),
                                 tc(gg[2], p(r(t, sz=16)), shd=sh)]))
            o.append(tbl(gg, filas))
        if juegos:
            o.append(p(r(f'{d["nivel"]} · Juegos para elegir', b=True, color=c, sz=22),
                       before=340, after=120, keep=True))
            filas = [head_row(gj, ["JUEGO", "TIEMPO", "EN QUÉ CONSISTE", "CUÁNDO · MATERIALES"], c)]
            for i, (n, dur, desc, mat, cuando) in enumerate(juegos):
                sh = bg if i % 2 == 0 else None
                filas.append(tr([
                    tc(gj[0], p(r(n, b=True, sz=17, color=NAVY)), shd=sh),
                    tc(gj[1], p(r(dur, sz=15, color=c), jc="center"), shd=sh),
                    tc(gj[2], p(r(desc, sz=15)), shd=sh),
                    tc(gj[3], [p(r(cuando, sz=15)),
                               p([r("Materiales. ", b=True, sz=15, color=c),
                                  r(mat, sz=15, color=GRIS_TX)], before=60)], shd=sh)]))
            o.append(tbl(gj, filas))
    o.append(PAGEBREAK)
    return "".join(o)


def desarrollo_runs(s, c):
    """Celda DESARROLLO: marcadores de minuto en negrita + texto."""
    out, first = [], True
    for rango, etq, txt in s["bloques"]:
        runs = [r(f"{rango}  ", b=True, color=c, sz=15, br=not first),
                r(f"{etq}: ", b=True, sz=15), r(txt, sz=15)]
        out.append(p(runs, before=0 if first else 40))
        first = False
    out.append(p([r("+5  ", b=True, color=c, sz=15), r("Sube de nivel: ", b=True, sz=15),
                  r(s["extra"] + "  (solo en bloques de 50 minutos)", sz=15)], before=40))
    return out


def nivel(niv):
    c, bg = COL[niv["color"]]
    gb = G(2600, 7941)
    o = [tbl(gb, [tr([
        tc(gb[0], p(r(niv["titulo"], b=True, color="FFFFFF", sz=24), jc="center"), shd=c, valign="center"),
        tc(gb[1], [p(r(niv["nombre"], b=True, color=c, sz=22)),
                  p(r("12 semanas · sesiones de 45 – 50 minutos · "
                     + " · ".join(f["titulo"] for f in niv["fases"]), sz=15, color=GRIS_TX), before=60)], shd=bg)])])]
    o.append(p([r("PROPÓSITO: ", b=True, color=c), r(niv["proposito"])], before=140, after=200))

    for ini in (0, 4, 8):
        grupo = niv["semanas"][ini:ini + 4]
        if ini:
            o.append(p(r(f"{niv['titulo']} · {niv['nombre']} · Semanas {ini+1}-{ini+4}",
                         b=True, color=c, sz=18), before=300, after=120, keep=True))
        filas = [head_row(G5, ["SEM.", "TEMA", "OBJETIVO DE LA CLASE",
                               "DESARROLLO DE LA CLASE · 45 MIN (+5)", "RECURSOS / EVIDENCIA"], c)]
        for k, s in enumerate(grupo):
            sh = bg if k % 2 == 0 else None
            filas.append(tr([
                tc(G5[0], p(r(str(s["n"]), b=True, color=c, sz=24), jc="center"), shd=sh),
                tc(G5[1], p(r(s["tema"], b=True, sz=17, color=NAVY)), shd=sh),
                tc(G5[2], p(r(s["objetivo"], sz=15)), shd=sh),
                tc(G5[3], desarrollo_runs(s, c), shd=sh),
                tc(G5[4], [p(r(s["recursos"], sz=15, color=GRIS_TX)),
                           p([r("Evidencia: ", b=True, sz=15, color=c), r(s["evidencia"], sz=15)], before=70)], shd=sh)]))
        o.append(tbl(G5, filas))
        o.append(p(r("Orientación docente: priorizar la práctica y el razonamiento. Explicar solo lo necesario "
                     "para que el estudiante pueda intentar el reto, recibir retroalimentación y mejorar su solución.",
                     sz=15, color=GRIS_TX, it=True), before=120, after=140))
    o.append(PAGEBREAK)
    return "".join(o)


def cocurricular():
    """El Programa Maker en el documento de coordinación: dos carriles."""
    c, bg = COL["co"]
    o = [tbl(G(2600, 7941), [tr([
        tc(G(2600, 7941)[0], p(r("COCURRICULAR", b=True, color="FFFFFF", sz=22), jc="center"),
           shd=c, valign="center"),
        tc(G(2600, 7941)[1], [p(r("Programa Maker", b=True, color=c, sz=22)),
                  p(r("Primaria lunes · Secundaria martes a jueves · 90 min", sz=15, color=GRIS_TX),
                    before=60)], shd=bg)])])]
    o.append(p([r("PROPÓSITO: ", b=True, color=c), r(C.MAKER_INTRO)], before=140, after=200))

    g = [700, 2600, 4400, 2668]
    for pr in C.MAKER_PROGRAMAS:
        o.append(p([r(pr["nombre"], b=True, color=c, sz=22),
                    r("   ·   " + pr["publico"], sz=16, color=GRIS_TX)],
                   before=340, after=60, keep=True))
        o.append(p(r(pr["resumen"], sz=16), after=80))
        o.append(p(r(pr["nota"], sz=15, color=GRIS_TX, it=True), after=140))
        for t in pr["talleres"]:
            o.append(p([r(f'Taller {t["n"]} · {t["titulo"]}', b=True, color=NAVY, sz=19),
                        r("   " + t["horas"], sz=15, color=GRIS_TX)],
                       before=220, after=50, keep=True))
            o.append(p(r("Producto: " + t["producto"], sz=15, color=GRIS_TX), after=100))
            filas = [head_row(g, ["SES.", "SESIÓN", "EN LA MESA", "SE LLEVAN"], c)]
            for k, x in enumerate([y for y in pr["sesiones"] if y["n"] in t["sesiones"]]):
                sh = bg if k % 2 == 0 else None
                filas.append(tr([
                    tc(g[0], p(r(str(x["n"]), b=True, color=c, sz=22), jc="center"), shd=sh),
                    tc(g[1], [p(r(x["titulo"], b=True, sz=17, color=NAVY)),
                              p(r(x["proposito"], sz=15), before=50)], shd=sh),
                    tc(g[2], p(r(x["materiales"], sz=15, color=GRIS_TX)), shd=sh),
                    tc(g[3], p(r(x["evidencia"], sz=15)), shd=sh)]))
            o.append(tbl(g, filas))
    o.append(PAGEBREAK)
    return "".join(o)


def dinamicas():
    o = [h1("BANCO DE DINÁMICAS DE RESERVA")]
    o.append(para(C.DINAMICAS_INTRO, after=240))
    g = G(2400, 1000, 1000, 4400, 1741)
    for grupo in C.DINAMICAS:
        o.append(p(r(grupo["grupo"], b=True, color=NAVY, sz=20), before=280, after=100, keep=True))
        filas = [head_row(g, ["DINÁMICA", "TIEMPO", "NIVEL", "EN QUÉ CONSISTE", "QUÉ ENSEÑA"], NAVY)]
        for i, (n, dur, niv, desc, goal) in enumerate(grupo["items"]):
            sh = "F8FAFC" if i % 2 else None
            filas.append(tr([
                tc(g[0], p(r(n, b=True, sz=17, color=NAVY)), shd=sh),
                tc(g[1], p(r(dur, sz=15, color=P["n1"]), jc="center"), shd=sh),
                tc(g[2], p(r(niv, sz=15, color=GRIS_TX), jc="center"), shd=sh),
                tc(g[3], p(r(desc, sz=15)), shd=sh),
                tc(g[4], p(r(goal, sz=15, color=GRIS_TX)), shd=sh)]))
        o.append(tbl(g, filas))
    o.append(PAGEBREAK)
    return "".join(o)


def evaluacion():
    o = [h1("EVALUACIÓN Y CRITERIOS COMUNES")]
    o.append(para(C.EVALUACION_INTRO, after=240))
    g = G(3200, 1100, 6241)
    filas = [head_row(g, ["COMPONENTE", "VALOR", "QUÉ SE OBSERVA"], NAVY)]
    for i, (comp, pc, q) in enumerate(C.EVALUACION):
        sh = "F8FAFC" if i % 2 else None
        filas.append(tr([tc(g[0], p(r(comp, b=True, sz=17, color=NAVY)), shd=sh),
                         tc(g[1], p(r(pc, b=True, sz=20, color=P["n1"]), jc="center"), shd=sh),
                         tc(g[2], p(r(q, sz=16)), shd=sh)]))
    o.append(tbl(g, filas))

    o.append(h2("Rúbrica de proyecto"))
    o.append(para("Se aplica al proyecto final de cada nivel y a los proyectos del cocurricular.", sz=18))
    g = G(1900, 2160, 2160, 2160, 2161)
    filas = [head_row(g, ["CRITERIO"] + C.RUBRICA_NIVELES, NAVY)]
    for i, (crit, vals) in enumerate(C.RUBRICA):
        sh = "F8FAFC" if i % 2 else None
        cells = [tc(g[0], p(r(crit, b=True, sz=17, color=NAVY)), shd=sh)]
        cells += [tc(g[k + 1], p(r(v, sz=15)), shd=sh) for k, v in enumerate(vals)]
        filas.append(tr(cells))
    o.append(tbl(g, filas))

    o.append(p(r("PROGRESIÓN FINAL", b=True, color=NAVY, sz=24), before=400, after=120))
    o.append(p(r(C.PROGRESION, b=True, color=P["n1"], sz=20), after=200))
    o.append(p([r(C.DOCENTE, b=True, color=NAVY, sz=18),
                r(f"   ·   {C.AREA}   ·   {C.ESCUELA}   ·   2026 – 2027", sz=16, color=GRIS_TX)],
               before=300))
    return "".join(o)


HEAD = None
def build():
    global HEAD
    with zipfile.ZipFile(PLANTILLA) as z:
        orig = z.read("word/document.xml").decode("utf-8")
    m = re.match(r"(.*?<w:body>)", orig, re.S)
    head = m.group(1)
    sect = re.search(r"<w:sectPr.*?</w:sectPr>", orig, re.S).group(0)
    body = (portada() + marco() + semana1()
            + "".join(nivel(n) for n in C.NIVELES)
            + cocurricular() + dinamicas() + evaluacion())
    return head + body + sect + "</w:body></w:document>"


if __name__ == "__main__":
    doc = build()
    shutil.copyfile(PLANTILLA, SALIDA)
    # reescribir solo word/document.xml conservando el resto del paquete
    tmp = SALIDA + ".tmp"
    with zipfile.ZipFile(SALIDA) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = doc.encode("utf-8")
            if it.filename == "docProps/thumbnail.jpeg":
                continue
            if it.filename == "_rels/.rels":
                data = re.sub(rb'<Relationship[^>]*thumbnail[^>]*/>', b'', data)
            zout.writestr(it, data)
    os.replace(tmp, SALIDA)
    print("escrito:", SALIDA, os.path.getsize(SALIDA), "bytes")

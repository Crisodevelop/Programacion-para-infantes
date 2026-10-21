# -*- coding: utf-8 -*-
"""
El motor de las clases interactivas: convierte `contenido.ACTIVIDADES` en las
diapositivas que el estudiante toca.

`actividades.py` tiene el contrato y el validador; aquí va lo que se ve y lo que
responde. Cada semana con datos sale con nueve diapositivas (diez la primera):

  1 Portada + «Hoy vas a…»            6 Mini juego
  2 Calentamiento en grupo (votación)  7 Manos al código / a las tarjetas
  3 Mira cómo funciona (ejemplo)       8 Reto del día + Sube de nivel
  4 Retos: predice + completa          9 Ticket de salida
  5 Retos: ordena + encuentra el error

Las notas del docente salen de la proyección: van en el panel «Guion», que no
es una diapositiva y no cuenta en el contador.

Nada se guarda. Las respuestas solo las ve quien las toca: sin nombres, sin base
de datos y sin localStorage, que con menores es la única forma de no tener que
explicar a nadie qué se guarda y dónde.
"""
import html, json, random

import contenido as C
from build_deck import escena, CSS_MOV, juegos_de

E = lambda s: html.escape(str(s), quote=False)
A = lambda s: html.escape(str(s), quote=True)

PYSCRIPT_VERSION = "2026.7.3"
LETRAS = "ABCD"
NOMBRE_CARTA = {"AVANZA": "Avanza", "GIRA_IZQ": "Gira ↺", "GIRA_DER": "Gira ↻", "REPITE_2": "Repite 2×"}


def orden(n, semilla, distinto=True):
    """Un orden barajado y siempre el mismo para la misma semilla: los diffs de
    las 36 presentaciones no cambian cada vez que se regenera. Para «ordena»
    se exige que no salga ya ordenado, que sería regalar el reto."""
    idx = list(range(n))
    rnd = random.Random(semilla)
    for _ in range(50):
        rnd.shuffle(idx)
        if not distinto or idx != sorted(idx):
            break
    return idx


def codigo(lineas, leng):
    filas = []
    for l in lineas:
        t = E(l)
        if "___" in l:
            t = t.replace("___", '<span class="a-hueco">___</span>')
        # La línea va dentro de un <span>: el <li> es un grid de dos columnas
        # (número y código) y cualquier etiqueta suelta —el hueco de «completa»,
        # por ejemplo— se convertía en otra celda y partía la línea en dos.
        filas.append(f"<li><span>{t}</span></li>")
    return f'<ol class="a-cod" data-leng="{leng}">{"".join(filas)}</ol>'


def opcion(texto, leng):
    return f"<code>{E(texto)}</code>" if leng in ("python", "html", "css") else E(texto)


def slide(eyebrow, minutos, cuerpo, quien=None):
    q = f'<p class="a-quien">{E(quien)}</p>' if quien else ""
    return (f'\n  <section class="slide">\n   <div class="inner">\n'
            f'    <p class="eyebrow">{E(eyebrow)} · {E(minutos)}{" min" if any(c.isdigit() for c in minutos) else ""}</p>\n    {q}{cuerpo}\n'
            f'   </div>\n  </section>\n')


FB = '<p class="a-fb" role="status" aria-live="polite"></p>'


# ── Piezas ───────────────────────────────────────────────────────────────────

def vota(c):
    botones = "".join(
        f'<button type="button" class="a-op" aria-pressed="false"{" data-ok" if k == c["correcta"] else ""}>'
        f'<span class="a-letra">{LETRAS[k]}</span><span>{E(o)}</span></button>'
        for k, o in enumerate(c["opciones"]))
    return f"""<h2 class="a-titulo">{E(c["pregunta"])}</h2>
    <div class="a-vota" data-act="vota">
      <div class="a-ops">{botones}</div>
      <div class="a-acc"><button type="button" class="a-btn" data-revelar>Revelar la respuesta</button></div>
      <p class="a-fb" role="status"></p>
      <p class="a-porque" hidden>{E(c["por_que"])}</p>
    </div>"""


def ejemplo(e):
    etq = "Tarjeta" if e["lenguaje"] == "tarjetas" else "Línea"
    notas = "".join(
        # `data-marca`, no `data-nota`: ese es el de la nota de la clase, y la
        # hoja de puntos pintaba «vale undefined pts» sobre estos marcadores.
        f'<li><button type="button" class="a-nota" data-marca="{n}" aria-pressed="false">'
        f'<b>{etq} {n}</b><span>{E(t)}</span></button></li>' for n, t in e["notas"])
    return f"""<h2 class="a-titulo">{E(e["titulo"])}</h2>
    <div class="a-ejemplo" data-act="notas">
      {codigo(e["codigo"], e["lenguaje"])}
      <div><p class="a-etq">Toca una nota y mira su {etq.lower()}</p><ol class="a-notas">{notas}</ol></div>
    </div>"""


def reto_opciones(r, semilla, pregunta):
    ops = r["opciones"]
    botones = "".join(
        f'<button type="button" class="a-op" data-txt="{A(ops[i])}"{" data-ok" if i == r["correcta"] else ""}>'
        f'<span class="a-letra">{LETRAS[k]}</span><span>{opcion(ops[i], r["lenguaje"])}</span></button>'
        for k, i in enumerate(orden(len(ops), semilla, distinto=False)))
    return f"""<div class="a-panel" data-act="opciones">
      <p class="a-etq">{E(pregunta)}</p>
      {codigo(r["codigo"], r["lenguaje"])}
      <div class="a-ops">{botones}</div>
      {FB}
      <p class="a-explica" hidden>{E(r["explica"])}</p>
      <div class="a-acc"><button type="button" class="a-btn a-sec" data-reintentar hidden>Reintentar</button></div>
    </div>"""


def reto_ordena(r, semilla):
    lin = r["lineas"]
    filas = "".join(
        f'<li data-txt="{A(lin[i])}"><span>{E(lin[i])}</span>'
        f'<button type="button" class="a-mover" data-sube aria-label="Subir">↑</button>'
        f'<button type="button" class="a-mover" data-baja aria-label="Bajar">↓</button></li>'
        for i in orden(len(lin), semilla))
    return f"""<div class="a-panel" data-act="ordena" data-orden="{A(json.dumps(lin, ensure_ascii=False))}">
      <p class="a-etq">Ordena</p>
      <h3>{E(r["enunciado"])}</h3>
      <ol class="a-orden" data-leng="{r["lenguaje"]}">{filas}</ol>
      <div class="a-acc"><button type="button" class="a-btn" data-comprobar>Comprobar</button>
        <button type="button" class="a-btn a-sec" data-reintentar hidden>Reintentar</button></div>
      {FB}
    </div>"""


def reto_error(r):
    botones = "".join(
        f'<button type="button" class="a-linea"{" data-mala" if k == r["mala"] else ""}>'
        f'<i>{k + 1}</i><span>{E(l)}</span></button>' for k, l in enumerate(r["lineas"]))
    return f"""<div class="a-panel" data-act="error">
      <p class="a-etq">Encuentra el error</p>
      <h3>Toca la {"tarjeta" if r["lenguaje"] == "tarjetas" else "línea"} que está mal.</h3>
      <div class="a-lineas" data-leng="{r["lenguaje"]}">{botones}</div>
      {FB}
      <div class="a-explica" hidden><p class="a-etq">Así queda bien</p>
        <pre class="a-arreglo">{E(r["arreglo"])}</pre><p>{E(r["explica"])}</p></div>
      <div class="a-acc"><button type="button" class="a-btn a-sec" data-reintentar hidden>Reintentar</button></div>
    </div>"""


def juego_robot(j, ctx=None):
    tam, meta = j["tam"], list(j["meta"])
    muros = {tuple(m) for m in j.get("muros", [])}
    celdas = "".join(
        f'<div class="a-rb-celda{" muro" if (x, y) in muros else ""}">{"🏁" if [x, y] == meta else ""}</div>'
        for y in range(tam) for x in range(tam))
    cfg = {"tam": tam, "inicio": j["inicio"], "meta": meta, "muros": [list(m) for m in muros], "max": j["max"]}
    rot = {"N": 0, "E": 90, "S": 180, "O": 270}[j["inicio"][2]]
    cartas = "".join(f'<button type="button" class="a-carta" data-carta="{c}">{E(NOMBRE_CARTA[c])}</button>'
                     for c in j["cartas"])
    ayuda = ("«Repite 2×» hace dos veces la tarjeta que pongas justo después."
             if "REPITE_2" in j["cartas"] else "")
    return f"""<div class="a-robot" data-act="robot" data-cfg="{A(json.dumps(cfg))}">
      <div class="a-rb-tablero" style="--tam:{tam}">{celdas}<div class="a-rb-bot" aria-hidden="true"
        style="--x:{j["inicio"][0]};--y:{j["inicio"][1]};--rot:{rot}deg"><b>▲</b></div></div>
      <div class="a-rb-lado">
        <div><p class="a-etq">Tus tarjetas</p><div class="a-rb-cartas">{cartas}</div>
          <p class="a-explica">{E(ayuda)}</p></div>
        <div><p class="a-etq">Tu programa · <span data-cuenta>0 / {j["max"]}</span></p><ol class="a-rb-prog" data-prog></ol></div>
        <div class="a-acc"><button type="button" class="a-btn" data-ejecutar>▶ Ejecutar</button>
          <button type="button" class="a-btn a-sec" data-quitar>Quitar la última</button>
          <button type="button" class="a-btn a-sec" data-borrar>Borrar todo</button></div>
        {FB}
      </div>
    </div>"""


MOTORES_HTML = {"robot": juego_robot}


def practica(p, ses, nivel, n):
    lista = "".join(f"<li>{E(x)}</li>" for x in p["pasos"])
    if p["tipo"] == "editor":
        # La práctica se hace aquí mismo: pasos arriba y el editor debajo.
        return (f'<h2 class="a-titulo">{E(p["titulo"])}</h2>'
                f'<ol class="a-pasos a-pasos-fila">{lista}</ol>{editor_html(p)}')
    if p["tipo"] == "enlace":
        lado = f"""<div class="a-panel"><p class="a-etq">Herramienta</p>
        <a class="a-btn" href="{A(p["url"])}" target="_blank" rel="noopener">{E(p["boton"])} ↗</a></div>"""
    else:
        lado = f"""<div class="a-panel"><p class="a-etq">Sin computadora · necesitan</p>
        <p class="a-explica">{E(ses["recursos"])}</p></div>"""
    # Sin editor no hay nada que ejecutar: el punto lo da marcar que la terminó.
    return f"""<h2 class="a-titulo">{E(p["titulo"])}</h2>
    <div class="a-practica"><ol class="a-pasos">{lista}</ol>{lado}</div>
    <div class="a-acc" data-act="hecho">
      <button type="button" class="a-btn" data-hecho>La terminé</button></div>"""


def guion(ses):
    bloques = "".join(f'<div class="a-g-bloque"><b>{E(r)}</b> <em>{E(e)}</em><p>{E(t)}</p></div>'
                      for r, e, t in ses["bloques"])
    return f"""
<aside class="a-guion" hidden aria-label="Guion del docente">
  <div class="a-g-cab"><h2>Guion de la clase</h2>
    <button type="button" class="a-btn a-sec" data-cerrar aria-label="Cerrar el guion">✕</button></div>
  <p class="a-g-obj">{E(ses["objetivo"])}</p>
  {bloques}
  <div class="a-g-bloque"><em>Sube de nivel</em><p>{E(ses["extra"])}</p></div>
  <div class="a-g-bloque"><em>Recursos</em><p>{E(ses["recursos"])}</p></div>
  <div class="a-g-bloque"><em>Evidencia</em><p>{E(ses["evidencia"])}</p></div>
</aside>"""


# ── La presentación completa ─────────────────────────────────────────────────

# Lo que vale cada cosa que el estudiante hace por su cuenta. Se reparte en
# 100 puntos exactos por clase: con más ejercicios, cada uno vale un poco menos.
# ── La rúbrica: lo mismo vale lo mismo, en las 36 clases y en los tres grados ──
#
# Antes se repartían 100 puntos entre lo que tuviera esa semana, así que un
# reto valía 10 en una clase y 15 en otra, y en 2do y 3ro los retos extra
# diluían los de todos. Ahora cada pieza tiene su precio fijo:
#
#   calentamiento 5 · ¿lo entendí? 5 · cuatro retos 10 c/u · taller 10
#   mini juego 10 · otro juego 10 · práctica 15 · ticket de salida 5  = 100
#
# Dos reglas la sostienen:
#   · Los retos extra de 2do y 3ro valen 10 POR ENCIMA de 100: son colchón, no
#     dilución (el tope de 100 ya está en la base y en la presentación).
#   · Lo que una semana todavía no tiene —el taller, el segundo juego— le cede
#     sus puntos a la práctica, que existe en las 36. Así las preguntas valen
#     siempre lo mismo y la clase sigue sumando 100 exactos.
PUNTOS = {"calent": 5, "teoria": 5, "reto": 10, "extra": 10,
          "primera": 10, "juego": 10, "juego2": 10, "practica": 15, "salida": 5}


def rubrica(teoria, extra, pr, j2):
    """Los puntos de esta clase. Suman 100 sin contar los extras."""
    pts = {"calent": PUNTOS["calent"], "practica": PUNTOS["practica"],
           "juego": PUNTOS["juego"], "salida": PUNTOS["salida"]}
    for k in range(1, 5):
        pts[f"r{k}"] = PUNTOS["reto"]
    for k in range(1, len(extra) + 1):
        pts[f"x{k}"] = PUNTOS["extra"]
    # Lo que falte esta semana se le suma a la práctica.
    for clave, hay in (("teoria", bool(teoria)), ("primera", bool(pr)), ("juego2", bool(j2))):
        if hay:
            pts[clave] = PUNTOS[clave]
        else:
            pts["practica"] += PUNTOS[clave]
    base = sum(v for k, v in pts.items() if not k.startswith("x"))
    if base != 100:
        raise SystemExit(f"\n  ABORTADO: la rúbrica suma {base}, no 100: {pts}\n")
    return pts


# Actividades que no tienen respuesta correcta y por eso no puntúan: las notas
# al margen del ejemplo, la hoja de la nota y el botón de imprimir la chuleta.
# Cualquier OTRA cosa con la que el estudiante pueda acertar o fallar tiene que
# valer puntos, y el build lo comprueba.
SIN_PUNTOS = {"notas", "nota", "imprimir"}


def revisar_puntos(cuerpo, nid, n):
    """Aborta si alguna actividad con respuesta queda fuera de la nota."""
    from html.parser import HTMLParser

    class Mirar(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.pila = []          # ¿hay un data-nota por encima?
            self.sueltas = []

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            dentro = (self.pila[-1] if self.pila else False) or "data-nota" in d
            motor = d.get("data-act")
            if motor and not dentro and motor not in SIN_PUNTOS:
                self.sueltas.append(motor)
            if tag not in ("br", "hr", "img", "input", "meta", "link"):
                self.pila.append(dentro)

        def handle_endtag(self, tag):
            if self.pila:
                self.pila.pop()

    m = Mirar()
    m.feed(cuerpo)
    if m.sueltas:
        raise SystemExit(f"\n  ABORTADO en {nid} S{n}: hay actividades con respuesta y sin puntos: "
                         f"{', '.join(sorted(set(m.sueltas)))}.\n")


def marcar(html, id_, pts, tipo):
    """Pone la marca de la nota en la actividad: el primer data-act del trozo.
    Las demos no tienen uno propio, así que se envuelven."""
    attrs = f'data-nota="{id_}" data-pts="{pts}" data-nota-tipo="{tipo}" '
    k = -1 if tipo == "demo" else html.find('data-act="')
    if k < 0:
        return f'<div {attrs}class="a-nota-caja">{html}</div>'
    return html[:k] + attrs + html[k:]


def retos_extra_html(lista, nid, n, puntos=None):
    """Los retos de más para 2do y 3ro: la misma pinta que los otros cuatro."""
    piezas = []
    for k, r in enumerate(lista):
        semilla = f"{nid}:{n}:extra{k}"
        if r["tipo"] == "predice":
            piezas.append(reto_opciones(r, semilla, "¿Qué muestra?"))
        elif r["tipo"] == "completa":
            piezas.append(reto_opciones(r, semilla, "Completa la línea que falta"))
        elif r["tipo"] == "ordena":
            piezas.append(reto_ordena(r, semilla))
        else:
            piezas.append(reto_error(r))
        if puntos:
            piezas[-1] = marcar(piezas[-1], f"x{k + 1}", puntos[f"x{k + 1}"], "reto")
    return f'<div class="a-grid2">{"".join(piezas)}</div>'


def deck_actividad(nivel, ses, act):
    """Devuelve (diapositivas, panel del guion, capítulos, css, js)."""
    n, nid = ses["n"], nivel["id"]
    j = act["juego"]
    if j["tipo"] not in MOTORES_HTML:
        raise SystemExit(f"\n  ABORTADO en {nid} S{n}: el motor de juego «{j['tipo']}» todavía no existe.\n")
    retos = act["retos"]
    extra = act.get("retos_extra") or []
    esc = escena(act["escena"], nid) if act.get("escena") else ""
    pregunta_predice = "¿Qué pasa?" if retos[0]["lenguaje"] == "tarjetas" else "¿Qué muestra?"
    pregunta_completa = "Completa la tarjeta que falta" if retos[1]["lenguaje"] == "tarjetas" else "Completa la línea que falta"

    portada = f"""
  <section class="slide">
   <div class="inner">
    <div class="a-portada{" con-escena" if esc else ""}">
     <div>
      <p class="eyebrow">{E(nivel["titulo"])} · {E(nivel["nombre"])}</p>
      <div class="cinta"><span class="cinta-num">{n:02d}</span><span class="cinta-txt">Semana {n} de 12</span></div>
      <h1 class="mid">{E(ses["tema"])}</h1>
      <p class="a-hoy">{E(act["hoy"])}</p>
     </div>
     {f'<div class="a-escena">{esc}</div>' if esc else ""}
    </div>
   </div>
  </section>
"""
    reto_dia = act.get("reto_dia") or ses["bloques"][3][2]
    j2 = act.get("juego2")
    pr = act.get("primera")
    titulo_primera = (pr or {}).get("titulo") or "Tu primera variable"
    dp = bool(act.get("definir_primero"))

    # El reloj de la clase: cada diapositiva pide sus minutos en el orden real,
    # así los rótulos siempre salen seguidos y terminan en 45.
    reloj = [0]

    def tramo(mins):
        ini = reloj[0]
        reloj[0] = ini + mins
        return f"{ini} – {reloj[0]}"

    tramo(1)                                  # la portada no lleva rótulo
    if dp:
        # Definición, partes y comprobación seguidas; el voto, después.
        mins_teoria = [tramo(2), tramo(2), tramo(3)]
        min_calent = tramo(2)
    else:
        min_calent = tramo(3)
        mins_teoria = [tramo(2), tramo(2), tramo(3)]
    min_ejemplo, min_r12, min_r34 = tramo(3), tramo(3), tramo(3)
    min_extra = tramo(3) if extra else None
    min_primera = tramo(4) if pr else None
    min_juego = tramo(3)
    min_juego2 = tramo(3) if j2 else None
    arranque = reloj[0]
    min_practica, min_reto = f"{arranque} – 42", f"{arranque} – 44"
    reloj[0] = 44
    min_salida = tramo(1)

    teoria, esc_teoria = diapositivas_teoria(C.__dict__.get("TEORIA", {}).get(nid, {}).get(n), nid, n, mins_teoria)
    # La nota de esta clase, con la rúbrica de arriba.
    PTS = rubrica(teoria, extra, pr, j2)
    if teoria:
        teoria[2] = marcar(teoria[2], "teoria", PTS["teoria"], "reto")
    # El calentamiento es una pregunta con respuesta correcta: cuenta como tal.
    calentamiento = slide("Calentamiento", min_calent,
                          marcar(vota(act["calentamiento"]), "calent", PTS["calent"], "reto"),
                          "Todos · a mano alzada")
    tipo_j = "demo" if j["tipo"] in DEMOS else "juego"

    s = []                                    # (capítulo, diapositiva)

    def pon(capitulo, html):
        s.append((capitulo, html))

    pon("Empezar", portada)
    if dp and teoria:
        # La definición va pegada al tema y la teoría sigue de corrido.
        pon("Empezar", teoria[0])
        for hoja in teoria[1:]:
            pon("Aprender", hoja)
        pon("Aprender", calentamiento)
    else:
        pon("Empezar", calentamiento)
        for hoja in teoria:
            pon("Aprender", hoja)
    pon("Aprender", slide("Mira cómo funciona", min_ejemplo, ejemplo(act["ejemplo"])))
    pon("Aprender", slide("Retos 1 y 2", min_r12,
                          f'<div class="a-grid2">'
                          f'{marcar(reto_opciones(retos[0], f"{nid}:{n}:predice", pregunta_predice), "r1", PTS["r1"], "reto")}'
                          f'{marcar(reto_opciones(retos[1], f"{nid}:{n}:completa", pregunta_completa), "r2", PTS["r2"], "reto")}</div>',
                          "Tú solo · en tu compu"))
    pon("Aprender", slide("Retos 3 y 4", min_r34,
                          f'<div class="a-grid2">{marcar(reto_ordena(retos[2], f"{nid}:{n}:ordena"), "r3", PTS["r3"], "reto")}'
                          f'{marcar(reto_error(retos[3]), "r4", PTS["r4"], "reto")}</div>',
                          "Tú solo · en tu compu"))
    if extra:
        pon("Aprender", slide("Sube de nivel", min_extra, retos_extra_html(extra, nid, n, PTS),
                              "Para los que quieren más"))
    if pr:
        pon("Jugar", slide(titulo_primera, min_primera,
                           marcar(taller_primera(pr), "primera", PTS["primera"], "juego"),
                           "Primero en grupo · después en tu compu"))
    pon("Jugar", slide("Mini juego", min_juego,
                       f'<h2 class="a-titulo">{E(j["titulo"])}</h2><p class="pista a-pista">{E(j["pista"])}</p>'
                       f'{marcar(MOTORES_HTML[j["tipo"]](j, {"nid": nid, "n": n}), "juego", PTS["juego"], tipo_j)}',
                       "Tú solo o en parejas"))
    if j2:
        pon("Jugar", slide("Otro juego", min_juego2,
                           f'<h2 class="a-titulo">{E(j2["titulo"])}</h2><p class="pista a-pista">{E(j2["pista"])}</p>'
                           f'{marcar(MOTORES_HTML[j2["tipo"]](j2, {"nid": nid, "n": f"{n}b"}), "juego2", PTS["juego2"], "juego")}',
                           "Tú solo o en parejas"))
    pon("Construir", slide("Manos a la obra", min_practica,
                           marcar(practica(act["practica"], ses, nivel, n), "practica", PTS["practica"], "practica"),
                           "En parejas" if act["practica"]["tipo"] == "desenchufada" else "Tú solo · en tu compu"))
    pon("Construir", slide("El reto de hoy", min_reto,
                           f'<div class="bloque"><p>{E(reto_dia)}</p></div>'
                           f'<div class="bloque a-sube"><p class="a-etq">Sube de nivel · si terminas antes</p>'
                           f'<p>{E(ses["extra"])}</p></div>'))
    juegos = juegos_de(nid) if n == 1 else []
    if juegos:
        filas = "".join(f"<dt>{E(x[0])} · {E(x[1])}</dt><dd>{E(x[4])}</dd>" for x in juegos)
        pon("Cerrar", slide("Si sobra tiempo", "si sobra",
                            f'<h2 class="mid">Juegos para elegir.</h2><dl class="dato">{filas}</dl>'))
    if act.get("chuleta"):
        pon("Cerrar", slide("Chuleta de la semana", "para llevar", chuleta_html(act["chuleta"], nivel, n)))
    if act.get("recursos"):
        pon("Cerrar", slide("Sigue practicando", "en casa", recursos_html(act["recursos"]),
                            "Gratis · sin instalar nada"))
    sa = act["salida"]
    pon("Cerrar", slide("Ticket de salida", min_salida,
                        f'<h2 class="a-titulo">{E(sa["pregunta"])}</h2>'
                        f'<div data-nota="salida" data-pts="{PTS["salida"]}" data-nota-tipo="salida" data-act="salida">'
                        f'<textarea class="a-ticket" aria-label="Tu respuesta" '
                        f'placeholder="Escribe tu respuesta. No se guarda: es para ti."></textarea>'
                        f'<div class="a-acc"><button type="button" class="a-btn a-sec" data-ver>Ver una buena respuesta</button></div>'
                        f'<p class="a-resp" hidden>{E(sa["respuesta"])}</p></div>'
                        f'<dl class="dato"><dt>Qué entregas hoy</dt><dd>{E(ses["evidencia"])}</dd></dl>',
                        "Tú solo"))
    pon("Cerrar", slide("Tu nota", "al final", nota_html(nid), "Tú solo · al terminar"))

    cuerpo = "".join(html for _, html in s)

    revisar_puntos(cuerpo, nid, n)

    # `partir()` borra cualquier <script>, <style>, <link> o <title> del marcado
    # sin avisar. El código de las prácticas tiene que ir siempre escapado.
    for etiqueta in ("<script", "<style", "<link", "<title"):
        if etiqueta in cuerpo:
            raise SystemExit(f"\n  ABORTADO en {nid} S{n}: el marcado lleva un {etiqueta} sin escapar.\n")

    # Los capítulos salen de las diapositivas, no de contar a mano.
    caps = []
    for i, (capitulo, _) in enumerate(s):
        if caps and caps[-1]["t"] == capitulo:
            caps[-1]["b"] = i
        else:
            caps.append({"t": capitulo, "a": i, "b": i, "tecla": None})

    demo = j["tipo"] in DEMOS
    motores = ([j["tipo"]] + ([j2["tipo"]] if j2 and j2["tipo"] != j["tipo"] else [])
               + ((["montana"] if pr.get("montana") else
                   ["escalera"] if pr.get("escalera") else
                   ["taller"] if pr.get("taller2") else ["primeravar"]) if pr else [])
               + (["editor"] if act["practica"]["tipo"] == "editor" else []))
    css = (CSS_ACT + "".join(CSS_MOTOR.get(x, "") for x in motores) + (CSS_JUEGO if demo else "")
           + (CSS_TEORIA if teoria else "") + (CSS_MOV if esc or demo or esc_teoria else "")
           + (CSS_EXTRAS if act.get("chuleta") or act.get("recursos") else "") + CSS_ACT_FIN)
    # Lo que la hoja «Tu nota» enseña: qué puntúa hoy y cuánto vale, en el
    # orden en que aparece en la clase.
    nombres = ([("calent", "Calentamiento")]
               + ([("teoria", "¿Lo entendí?")] if teoria else [])
               + [(f"r{k}", f"Reto {k}") for k in range(1, 5)]
               + [(f"x{k}", f"Reto extra {k}") for k in range(1, len(extra) + 1)]
               + ([("primera", titulo_primera)] if pr else [])
               + [("juego", "Mini juego")]
               + ([("juego2", "Otro juego")] if j2 else [])
               + [("practica", "La práctica"), ("salida", "Ticket de salida")])
    assert {i for i, _ in nombres} == set(PTS), (nid, n, PTS)
    clase = {"nivel": nid, "semana": n, "items": [{"id": i, "nombre": t, "pts": PTS[i]} for i, t in nombres]}
    js = (f"var CLASE={json.dumps(clase, ensure_ascii=False)};\n" + JS_INICIO + JS_PY + JS_RETOS
          + "".join(JS_MOTOR.get(x, "") for x in motores) + JS_FIN)
    if demo:
        # Las demos de la primera clase, tal cual: su propio IIFE, y dentro de un
        # try para que un fallo suyo no se lleve lo demás.
        js += "\ntry{" + JS_INTER + "}catch(e){console.error('[demos]',e);}"
    return cuerpo, guion(ses), caps, css, js


# ── CSS ──────────────────────────────────────────────────────────────────────

CSS_ACT = """
/* ─── clases interactivas ─── */
.deck{--a-ok:#7BD8A8;--a-ko:#F4A4A4}
[data-tema="claro"] .deck,[data-tema="pared"] .deck{--a-ok:#0F7343;--a-ko:#B3261E}
.deck [hidden],.a-guion[hidden],.a-chip[hidden]{display:none!important}
.a-titulo{font-size:clamp(22px,3.3vw,40px);max-width:32ch}
.a-quien{display:inline-flex;font-family:var(--fm);font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--tx2);border:1px solid var(--line);border-radius:999px;
  padding:4px 11px;margin:-8px 0 14px}
.a-hoy{margin-top:18px;font-size:clamp(17px,2.2vw,26px);color:var(--tx2);max-width:44ch;line-height:1.4}
.a-portada{display:grid;gap:clamp(20px,4vw,56px);align-items:center}
@media(min-width:900px){.a-portada.con-escena{grid-template-columns:1.2fr .8fr}}
.a-escena svg{width:100%;height:auto;display:block}
.a-grid2 > :only-child{grid-column:1/-1;max-width:820px;justify-self:center}
.a-grid2{display:grid;gap:16px;margin-top:6px}
@media(min-width:980px){.a-grid2{grid-template-columns:1fr 1fr;align-items:start}}
.a-panel{background:var(--bg2);border:1px solid var(--line);border-top:3px solid var(--lvl);
  padding:clamp(14px,2vw,22px);border-radius:4px;display:flex;flex-direction:column;gap:12px}
.a-panel h3{font-size:clamp(16px,1.9vw,22px)}
.a-etq{font-family:var(--fm);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--lvl);margin:0}
.a-pista{margin:6px 0 0}
.a-cod{list-style:none;margin:0;padding:10px 0;background:#0B1020;border:1px solid var(--line);
  border-radius:4px;counter-reset:ln;font-family:var(--fm);font-size:clamp(13px,1.45vw,17px);
  line-height:1.65;color:#D7DEEC;overflow-x:auto}
.a-cod li{counter-increment:ln;display:grid;grid-template-columns:2.8em 1fr;padding-right:14px;
  white-space:pre;min-height:1.65em;transition:background .16s}
.a-cod li>span{min-width:0;white-space:pre}
.a-cod li::before{content:counter(ln);color:#5E6B85;text-align:right;padding-right:12px;user-select:none}
.a-cod li.a-foco{background:rgba(79,201,232,.18);box-shadow:inset 3px 0 0 var(--lvl)}
.a-cod[data-leng="tarjetas"]{background:transparent;border:0;padding:0;display:grid;gap:7px;
  font-family:var(--fb);color:var(--tx)}
.a-cod[data-leng="tarjetas"] li{white-space:normal;align-items:center;background:var(--panel);
  border:1px solid var(--line);border-left:4px solid var(--lvl);border-radius:4px;
  padding:9px 12px 9px 0;font-weight:700;letter-spacing:.02em}
.a-cod[data-leng="tarjetas"] li::before{color:var(--mut);font-family:var(--fm);font-size:.8em}
.a-cod[data-leng="tarjetas"] li.a-foco{box-shadow:inset 0 0 0 2px var(--lvl)}
.a-hueco{display:inline-block;min-width:5ch;border-bottom:2px dashed var(--lvl);color:var(--lvl)}
.a-hueco.a-lleno{border-bottom-style:solid;color:var(--a-ok)}
.a-ops{display:grid;gap:8px}
.a-op{display:flex;gap:11px;align-items:center;text-align:left;min-height:46px;padding:8px 13px;
  background:var(--panel);border:1px solid var(--line);border-radius:6px;color:var(--tx);
  font-family:var(--fb);font-size:clamp(14px,1.5vw,17px);cursor:pointer;touch-action:manipulation;
  transition:border-color .16s,background .16s,opacity .16s}
.a-op:hover:not(:disabled){border-color:var(--lvl)}
.a-op:focus-visible,.a-nota:focus-visible,.a-linea:focus-visible,.a-mover:focus-visible,
.a-carta:focus-visible,.a-btn:focus-visible,.a-guion-btn:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-op code{font-family:var(--fm)}
.a-op:disabled{cursor:default}
.a-op[data-estado="bien"]{border-color:var(--a-ok);box-shadow:inset 0 0 0 2px var(--a-ok)}
.a-op[data-estado="mal"]{border-color:var(--a-ko);opacity:.55}
.a-letra{flex:0 0 auto;display:grid;place-items:center;width:30px;height:30px;border-radius:6px;
  background:var(--lvl);color:var(--bg);font-family:var(--fd);font-weight:800}
.a-fb{min-height:1.4em;font-weight:700;font-size:clamp(14px,1.5vw,17px);margin:0}
.a-fb.a-bien{color:var(--a-ok)}
.a-fb.a-mal{color:var(--a-ko)}
.a-explica{color:var(--tx2);font-size:clamp(13px,1.4vw,16px);line-height:1.45;margin:0}
.a-explica p{margin:6px 0 0}
.a-acc{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0}
.a-btn{min-height:44px;padding:9px 16px;border-radius:6px;border:1px solid var(--lvl);
  background:var(--lvl);color:var(--bg);font-family:var(--fb);font-weight:700;
  font-size:clamp(13px,1.4vw,16px);cursor:pointer;touch-action:manipulation;text-decoration:none;
  display:inline-flex;align-items:center;gap:8px;transition:filter .16s}
.a-btn:hover:not(:disabled){filter:brightness(1.1)}
.a-btn:disabled{opacity:.4;cursor:default}
.a-btn.a-sec{background:transparent;color:var(--tx);border-color:var(--line)}
.a-btn.a-sec:hover:not(:disabled){border-color:var(--lvl)}

/* votación */
.a-vota{margin-top:22px;display:grid;gap:16px}
@media(min-width:800px){.a-vota .a-ops{grid-template-columns:1fr 1fr}}
.a-vota .a-op{min-height:76px;font-size:clamp(17px,2.1vw,25px);font-weight:600}
.a-vota .a-letra{width:46px;height:46px;font-size:23px}
.a-vota .a-op[aria-pressed="true"]{border-color:var(--tx2);background:var(--panel2)}
.a-vota[data-revelado="1"] .a-op:not([data-ok]){opacity:.38}
.a-vota[data-revelado="1"] .a-op[data-ok]{border-color:var(--a-ok);box-shadow:inset 0 0 0 3px var(--a-ok)}
.a-porque{font-size:clamp(15px,1.9vw,22px);color:var(--tx2);max-width:60ch;line-height:1.45}

/* ejemplo */
.a-ejemplo{display:grid;gap:18px;margin-top:20px}
@media(min-width:980px){.a-ejemplo{grid-template-columns:1.2fr .8fr;align-items:start}}
.a-notas{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:8px}
/* Las notas se leen desde el fondo del aula sin tocarlas: antes salían en el
   gris de segunda fila (--tx2) y solo llegaban a --tx al pulsarlas, así que lo
   que explica el ejemplo se perdía para quien mira de lejos. Tocarlas sigue
   sirviendo, pero ahora para SEÑALAR su línea, no para poder leerlas. */
.a-nota{width:100%;text-align:left;display:grid;gap:4px;padding:10px 13px;min-height:44px;
  background:var(--bg2);border:1px solid var(--line);border-radius:6px;color:var(--tx);
  font-family:var(--fb);font-size:clamp(13.5px,1.45vw,17px);line-height:1.4;cursor:pointer}
.a-nota b{font-family:var(--fm);color:var(--lvl);font-size:11px;letter-spacing:.1em;text-transform:uppercase}
.a-nota[aria-pressed="true"]{border-color:var(--lvl);background:var(--panel2)}

/* ordena */
.a-orden{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.a-orden li{display:grid;grid-template-columns:1fr auto auto;gap:6px;align-items:center;
  padding:5px 6px 5px 12px;background:var(--panel);border:1px solid var(--line);border-radius:6px}
.a-orden li span{font-family:var(--fm);font-size:clamp(12.5px,1.35vw,15.5px);white-space:pre;overflow-x:auto}
.a-orden[data-leng="tarjetas"] li span{font-family:var(--fb);white-space:normal;font-weight:600}
.a-mover{width:42px;height:42px;border-radius:6px;border:1px solid var(--line);background:transparent;
  color:var(--tx);cursor:pointer;font-size:17px;touch-action:manipulation}
.a-mover:disabled{opacity:.25;cursor:default}
.a-orden li[data-estado="bien"]{border-color:var(--a-ok);box-shadow:inset 3px 0 0 var(--a-ok)}
.a-orden li[data-estado="mal"]{border-color:var(--a-ko);box-shadow:inset 3px 0 0 var(--a-ko)}

/* encuentra el error */
.a-lineas{display:grid;gap:5px}
.a-linea{display:grid;grid-template-columns:2.4em 1fr;text-align:left;min-height:44px;align-items:center;
  padding:6px 12px 6px 0;background:#0B1020;color:#D7DEEC;border:1px solid var(--line);border-radius:5px;
  font-family:var(--fm);font-size:clamp(12.5px,1.35vw,15.5px);cursor:pointer;touch-action:manipulation}
.a-linea span{white-space:pre}
.a-linea i{font-style:normal;color:#5E6B85;text-align:right;padding-right:10px}
.a-lineas[data-leng="tarjetas"] .a-linea{background:var(--panel);color:var(--tx);font-family:var(--fb);font-weight:700}
.a-lineas[data-leng="tarjetas"] .a-linea span{white-space:normal}
.a-linea[data-estado="bien"]{border-color:var(--a-ok);box-shadow:inset 4px 0 0 var(--a-ok)}
.a-linea[data-estado="mal"]{border-color:var(--a-ko);opacity:.55}
.a-arreglo{font-family:var(--fm);background:#0B1020;color:#A7F3C4;padding:8px 12px;border-radius:5px;
  white-space:pre-wrap;margin:6px 0 0;font-size:14px}

/* manos a la obra */
.a-practica{display:grid;gap:22px;margin-top:20px}
@media(min-width:980px){.a-practica{grid-template-columns:1.1fr .9fr;align-items:start}}
.a-pasos{list-style:none;counter-reset:p;margin:0;padding:0;display:grid;gap:11px}
.a-pasos li{counter-increment:p;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:start;
  font-size:clamp(15px,1.7vw,20px);line-height:1.4;color:var(--tx)}
.a-pasos li::before{content:counter(p);display:grid;place-items:center;width:36px;height:36px;
  border-radius:99px;background:var(--lvl);color:var(--bg);font-family:var(--fd);font-weight:800;font-size:17px}
.a-codigo summary{cursor:pointer;font-family:var(--fm);font-size:12px;color:var(--mut);padding:6px 0}
.a-codigo pre{margin:6px 0 12px;max-height:34vh;overflow:auto;background:#0B1020;color:#D7DEEC;
  border:1px solid var(--line);border-radius:4px;padding:12px 14px;font-family:var(--fm);font-size:12.5px;
  line-height:1.55;white-space:pre}
.a-sube{border-left-color:var(--sand)}
.a-sube .a-etq{color:var(--sand);margin-bottom:8px}

/* ticket */
.a-ticket{display:block;width:100%;max-width:70ch;min-height:120px;margin:18px 0 10px;padding:12px 14px;
  border-radius:6px;border:1px solid var(--line);background:var(--bg2);color:var(--tx);
  font-family:var(--fb);font-size:clamp(15px,1.7vw,19px);line-height:1.45;resize:vertical}
.a-ticket:focus-visible{outline:2px solid var(--lvl);outline-offset:1px}
.a-resp{margin-top:12px;padding:12px 15px;max-width:70ch;border-left:3px solid var(--a-ok);
  background:var(--bg2);color:var(--tx2);font-size:clamp(14px,1.6vw,18px);line-height:1.45}

/* guion del docente */
.a-guion-btn{font-family:var(--fm);font-size:11px;letter-spacing:.06em;padding:5px 10px;background:transparent;
  color:var(--mut);border:1px dashed var(--line);border-radius:999px;cursor:pointer}
.a-guion-btn:hover{color:var(--tx)}
/* El guion es del docente: el botón solo aparece con su sesión, que marca <html data-docente>. */
.a-guion-btn,.a-guion-btn+.sep{display:none}
[data-docente] .a-guion-btn{display:inline-block}
[data-docente] .a-guion-btn+.sep{display:block}
.a-guion-btn[aria-expanded="true"]{color:var(--tx);border-style:solid;border-color:var(--lvl)}
.a-guion{position:fixed;top:0;right:0;bottom:0;z-index:70;width:min(460px,100vw);overflow-y:auto;
  background:var(--bg2);border-left:1px solid var(--line);padding:18px 22px 40px;
  box-shadow:-24px 0 60px -30px rgba(0,0,0,.7)}
.a-g-cab{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}
.a-g-cab h2{font-size:22px}
.a-g-obj{color:var(--tx);font-size:15px;line-height:1.5;margin-bottom:8px}
.a-g-bloque{padding:11px 0;border-top:1px solid var(--line)}
.a-g-bloque b{font-family:var(--fm);font-size:12px;color:var(--lvl)}
.a-g-bloque em{font-style:normal;font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--mut);font-weight:600}
.a-g-bloque p{font-size:14.5px;color:var(--tx2);line-height:1.5;margin-top:5px}

/* puntos e insignia */
.a-puntos{font-family:var(--fm);font-size:12px;padding:5px 11px;border-radius:999px;border:1px solid var(--line);
  color:var(--tx);background:var(--bg2);margin-left:10px}
.a-puntos.a-sube{animation:a-pop .45s}
@keyframes a-pop{40%{transform:scale(1.25);border-color:var(--sand)}}
.a-insignia{position:fixed;left:50%;top:84px;transform:translateX(-50%);z-index:80;display:flex;gap:12px;align-items:center;
  padding:14px 22px;border-radius:14px;background:var(--bg2);border:2px solid var(--sand);color:var(--tx);
  font-family:var(--fd);font-weight:700;font-size:clamp(15px,1.8vw,21px);box-shadow:0 20px 50px -20px rgba(0,0,0,.7);
  animation:a-baja .5s cubic-bezier(.3,1.4,.5,1)}
.a-insignia b{font-size:34px}
@keyframes a-baja{from{transform:translate(-50%,-30px);opacity:0}}

/* bloqueo del docente: mientras explica, nadie juega */
[data-bloqueo="juegos"] [data-act]{pointer-events:none;opacity:.38;filter:saturate(.3)}
"""

CSS_MOTOR = {
    "robot": """
/* robot */
.a-robot{display:grid;gap:22px;margin-top:16px}
@media(min-width:980px){.a-robot{grid-template-columns:auto 1fr;align-items:start}}
.a-rb-tablero{position:relative;display:grid;grid-template-columns:repeat(var(--tam),1fr);gap:4px;
  width:min(52vh,86vw,440px);aspect-ratio:1}
.a-rb-celda{background:var(--panel);border-radius:5px;display:grid;place-items:center;font-size:clamp(16px,3.4vh,30px)}
.a-rb-celda.muro{background:repeating-linear-gradient(45deg,var(--line) 0 6px,var(--panel2) 6px 12px)}
.a-rb-bot{position:absolute;z-index:2;display:grid;place-items:center;
  width:calc((100% - (var(--tam) - 1) * 4px) / var(--tam));aspect-ratio:1;
  left:calc((100% + 4px) / var(--tam) * var(--x));top:calc((100% + 4px) / var(--tam) * var(--y));
  transition:left .32s cubic-bezier(.3,1.2,.5,1),top .32s cubic-bezier(.3,1.2,.5,1)}
.a-rb-bot b{display:grid;place-items:center;width:74%;height:74%;border-radius:50%;background:var(--lvl);
  color:var(--bg);font-size:clamp(14px,2.6vh,24px);transform:rotate(var(--rot));transition:transform .25s}
.a-rb-lado{display:grid;gap:16px;align-content:start}
.a-rb-cartas{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}
.a-carta{min-height:50px;padding:8px 16px;border-radius:6px;border:2px solid var(--lvl);background:var(--panel);
  color:var(--tx);font-family:var(--fb);font-weight:800;font-size:clamp(14px,1.5vw,17px);cursor:pointer;
  touch-action:manipulation}
.a-carta:hover:not(:disabled){background:var(--panel2)}
.a-carta:disabled{opacity:.35;cursor:default}
.a-rb-prog{list-style:none;margin:8px 0 0;padding:8px;min-height:62px;display:flex;flex-wrap:wrap;gap:6px;
  align-content:flex-start;background:var(--bg2);border:1px dashed var(--line);border-radius:6px;counter-reset:c}
.a-rb-prog li{counter-increment:c;font-family:var(--fm);font-size:13px;padding:7px 10px;border-radius:5px;
  background:var(--panel2);color:var(--tx)}
.a-rb-prog li::before{content:counter(c) ". ";color:var(--mut)}
.a-rb-prog li.activa{background:var(--lvl);color:var(--bg)}
.a-rb-prog li.activa::before{color:var(--bg)}
.a-rb-prog li.falla{background:var(--a-ko);color:#1a0505}
.a-rb-prog:empty::after{content:"Toca las tarjetas para armar el programa";color:var(--mut);font-size:13px;padding:10px}
""",
}

CSS_ACT_FIN = """
@media (prefers-reduced-motion: reduce){
  .a-puntos.a-sube,.a-insignia{animation:none}
  .a-rb-bot,.a-rb-bot b{transition:none}
  .a-sacude{animation:none}
}
"""


# ── JS ───────────────────────────────────────────────────────────────────────
#  Un solo IIFE. Todo escuchador lleva la señal de aborto que PaginaGenerada
#  pasa como `senal`: al salir de la ruta se van todos y al volver no quedan
#  duplicados. Cada motor se arranca dentro de su propio try, para que un error
#  en un juego no se lleve la paginación ni los demás retos.

JS_INICIO = r"""
(function(){
var SEN={signal:typeof senal!=='undefined'?senal:undefined};
function todos(r,q){return [].slice.call(r.querySelectorAll(q));}
function ver(r,q){return r.querySelector(q);}
function on(el,ev,fn){if(el)el.addEventListener(ev,fn,SEN);}
var QUIETO=false;try{QUIETO=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
var pausas=[],cambios=[],M={};
// Puntos: 10 por cada actividad que se resuelve por primera vez. La insignia
// sale cuando están todos los retos. Nada se guarda: al recargar, a cero.
// ── La nota de la clase ───────────────────────────────────────────────────
// Sin nombre elegido, la clase va en modo repaso: se juega, pero no se anota.
// Cuando el estudiante elige su nombre en la ventana (la pone la página), cada
// primer intento se guarda en esta PC y en la base, y lo de la base manda.
var NOTA={clave:null,hechos:{},id:null,codigo:null},chipP=null,insignia=false;
function hoyISO(){var d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function totalNota(){var t=0;for(var k in NOTA.hechos)t+=NOTA.hechos[k];return Math.min(100,t);}
function corto(n){var p=String(n||'').trim().split(/\s+/);return p[0]+(p[1]?' '+p[1][0]+'.':'');}
function guardarNota(){
  if(!NOTA.clave)return;
  try{localStorage.setItem(NOTA.clave,JSON.stringify({hechos:NOTA.hechos,codigo:NOTA.codigo,t:Date.now()}));}catch(e){}
}
function subirNota(){
  if(!NOTA.id)return;
  document.dispatchEvent(new CustomEvent('nota:guardar',{detail:{detalle:NOTA.hechos,codigo:NOTA.codigo}}));
}
function identidad(d){
  NOTA.id=d;NOTA.clave='nota:'+CLASE.nivel+':'+CLASE.semana+':'+hoyISO()+':'+d.seccion;
  var local={};
  try{var g=JSON.parse(localStorage.getItem(NOTA.clave)||'null');if(g){local=g.hechos||{};NOTA.codigo=NOTA.codigo||g.codigo||null;}}catch(e){}
  // Lo que ya llevaba en esta PC pasa a su nombre; lo que ya estaba en la base, manda.
  NOTA.hechos=Object.assign({},NOTA.hechos,local,d.detalle||{});
  NOTA.codigo=NOTA.codigo||d.codigo||null;
  guardarNota();pintarNota();subirNota();
}
function etiquetaNota(n){
  if(n.dataset.notaTipo==='reto')return n;
  var sl=n.closest('.slide');return sl?sl.querySelector('.eyebrow'):null;
}
function pintarNota(){
  if(chipP)chipP.textContent=NOTA.id?'⭐ '+totalNota()+' / 100 · '+corto(NOTA.id.nombre):'Modo repaso';
  todos(document,'[data-nota]').forEach(function(n){
    var donde=etiquetaNota(n);if(!donde)return;
    var b=n.__vale;
    if(!b){b=document.createElement('span');b.className='a-vale';n.__vale=b;
      if(donde===n)n.insertBefore(b,n.firstChild);else donde.appendChild(b);}
    var id=n.dataset.nota,hecho=id in NOTA.hechos;
    b.textContent=hecho?NOTA.hechos[id]+' / '+n.dataset.pts+' pts'+(n.dataset.notaTipo==='reto'?' · ya contestado':''):'vale '+n.dataset.pts+' pts';
    b.classList.toggle('a-vale-hecho',hecho);
  });
  document.dispatchEvent(new CustomEvent('nota:pintar'));
}
function anotar(n,ok){
  if(!n||!n.dataset||!n.dataset.nota||!NOTA.id)return;   // en modo repaso no se anota
  var id=n.dataset.nota;if(id in NOTA.hechos)return;
  NOTA.hechos[id]=ok?+n.dataset.pts:0;guardarNota();pintarNota();subirNota();
  if(chipP&&ok){chipP.classList.remove('a-sube');void chipP.offsetWidth;chipP.classList.add('a-sube');}
  var retos=todos(document,'[data-nota-tipo=reto]');
  if(!insignia&&retos.length&&retos.every(function(x){return NOTA.hechos[x.dataset.nota]===+x.dataset.pts;})){
    insignia=true;
    var t=document.createElement('div');t.className='a-insignia';t.setAttribute('role','status');
    t.innerHTML='<b>🏅</b><span></span>';t.children[1].textContent='¡Insignia «Pythonista del día»! Todos los retos a la primera.';
    (document.querySelector('.deck')||document.body).appendChild(t);
    setTimeout(function(){t.remove();},5200);
  }
}
// Un juego da sus puntos cuando se resuelve de verdad: lo avisa cada motor.
function gana(r){anotar(r&&r.closest?r.closest('[data-nota]'):null,true);return true;}
function fb(caja,ok,texto){
  var n=caja&&caja.closest?caja.closest('[data-nota]'):null;
  if(n&&n.dataset.notaTipo==='reto'&&(ok===true||ok===false))anotar(n,ok);
  var p=ver(caja,'.a-fb');if(!p)return;
  p.textContent=ok===null?'':(ok?'✓ ':'✗ ')+texto;
  p.className='a-fb'+(ok===null?'':(ok?' a-bien':' a-mal'));
}
"""

JS_RETOS = r"""
M.vota=function(r){
  var ops=todos(r,'.a-op'),rev=ver(r,'[data-revelar]'),pq=ver(r,'.a-porque');
  /* El calentamiento tiene respuesta correcta, así que cuenta como un reto:
     vale la PRIMERA que toca, igual que en los demás. Seguir tocando cambia
     lo marcado para el conteo a mano alzada, pero ya no cambia la nota. */
  var contado=false;
  ops.forEach(function(b){on(b,'click',function(){
    ops.forEach(function(o){o.setAttribute('aria-pressed',String(o===b));});
    if(!contado){contado=true;fb(r,b.hasAttribute('data-ok'),
      b.hasAttribute('data-ok')?'¡Esa es!':'Esa no era. Mira la explicación.');}
  });});
  on(rev,'click',function(){
    var abierto=r.dataset.revelado==='1';
    r.dataset.revelado=abierto?'0':'1';
    rev.textContent=abierto?'Revelar la respuesta':'Ocultar la respuesta';
    pq.hidden=abierto;
  });
};

M.notas=function(r){
  var notas=todos(r,'[data-marca]'),filas=todos(r,'.a-cod li');
  notas.forEach(function(n){on(n,'click',function(){
    var activa=n.getAttribute('aria-pressed')==='true';
    notas.forEach(function(x){x.setAttribute('aria-pressed',String(!activa&&x===n));});
    filas.forEach(function(li,k){li.classList.toggle('a-foco',!activa&&String(k+1)===n.dataset.marca);});
  });});
};

M.opciones=function(r){
  var ops=todos(r,'.a-op'),ex=ver(r,'.a-explica'),re=ver(r,'[data-reintentar]'),hueco=ver(r,'.a-hueco');
  function reset(){
    ops.forEach(function(o){o.disabled=false;o.removeAttribute('data-estado');});
    fb(r,null,'');ex.hidden=true;re.hidden=true;
    if(hueco){hueco.textContent='___';hueco.classList.remove('a-lleno');}
  }
  ops.forEach(function(b){on(b,'click',function(){
    var ok=b.hasAttribute('data-ok');
    b.setAttribute('data-estado',ok?'bien':'mal');
    if(ok){
      ops.forEach(function(o){o.disabled=true;});
      if(hueco){hueco.textContent=b.dataset.txt;hueco.classList.add('a-lleno');}
      fb(r,true,'¡Correcto!');ex.hidden=false;
    }else{
      b.disabled=true;fb(r,false,'Todavía no. Mira otra vez y prueba otra opción.');
    }
    re.hidden=false;
  });});
  on(re,'click',reset);
};

M.ordena=function(r){
  var lista=ver(r,'.a-orden'),bien=JSON.parse(r.dataset.orden),inicial=todos(lista,'li');
  var comp=ver(r,'[data-comprobar]'),re=ver(r,'[data-reintentar]');
  function filas(){return todos(lista,'li');}
  function botones(bloq){
    var fs=filas();
    fs.forEach(function(li,k){
      ver(li,'[data-sube]').disabled=bloq||k===0;
      ver(li,'[data-baja]').disabled=bloq||k===fs.length-1;
    });
  }
  on(lista,'click',function(e){
    var b=e.target.closest('button');if(!b)return;
    var li=b.closest('li');
    if(b.hasAttribute('data-sube')&&li.previousElementSibling)lista.insertBefore(li,li.previousElementSibling);
    else if(b.hasAttribute('data-baja')&&li.nextElementSibling)lista.insertBefore(li.nextElementSibling,li);
    filas().forEach(function(x){x.removeAttribute('data-estado');});
    fb(r,null,'');botones(false);
    if(!b.disabled)b.focus();
  });
  on(comp,'click',function(){
    var fs=filas(),n=0;
    fs.forEach(function(li,k){var ok=li.dataset.txt===bien[k];if(ok)n++;li.setAttribute('data-estado',ok?'bien':'mal');});
    re.hidden=false;
    if(n===fs.length){fb(r,true,'¡Todo en su sitio! Así se ejecuta en orden.');botones(true);comp.disabled=true;}
    else fb(r,false,n+' de '+fs.length+' en su sitio. Mueve las rojas.');
  });
  on(re,'click',function(){
    inicial.forEach(function(li){li.removeAttribute('data-estado');lista.appendChild(li);});
    fb(r,null,'');comp.disabled=false;re.hidden=true;botones(false);
  });
  botones(false);
};

M.error=function(r){
  var lin=todos(r,'.a-linea'),ex=ver(r,'.a-explica'),re=ver(r,'[data-reintentar]');
  lin.forEach(function(b){on(b,'click',function(){
    if(b.hasAttribute('data-mala')){
      b.setAttribute('data-estado','bien');lin.forEach(function(x){x.disabled=true;});
      fb(r,true,'¡La encontraste!');ex.hidden=false;
    }else{
      b.setAttribute('data-estado','mal');b.disabled=true;
      fb(r,false,'Esa está bien. Sigue buscando.');
    }
    re.hidden=false;
  });});
  on(re,'click',function(){
    lin.forEach(function(x){x.disabled=false;x.removeAttribute('data-estado');});
    fb(r,null,'');ex.hidden=true;re.hidden=true;
  });
};

M.salida=function(r){
  var b=ver(r,'[data-ver]'),resp=ver(r,'.a-resp'),ta=ver(r,'textarea'),vista=false;
  // Cuenta si escribieron su respuesta antes de mirar la buena.
  if(ta)on(ta,'input',function(){if(!vista&&ta.value.trim().length>=15)gana(r);});
  on(b,'click',function(){vista=true;resp.hidden=!resp.hidden;b.textContent=resp.hidden?'Ver una buena respuesta':'Ocultar la respuesta';});
};

M.nota=function(r){
  var tot=ver(r,'[data-total]'),lista=ver(r,'[data-desglose]'),quien=ver(r,'[data-quien]');
  function pintar(){
    tot.textContent=totalNota();lista.innerHTML='';
    CLASE.items.forEach(function(it){
      var v=NOTA.hechos[it.id],li=document.createElement('li');
      li.innerHTML='<span></span><b></b>';li.children[0].textContent=it.nombre;
      li.children[1].textContent=(v===undefined?'—':v)+' / '+it.pts;
      if(v===undefined)li.className='a-pendiente';lista.appendChild(li);
    });
    quien.textContent=NOTA.id
      ?'Se guarda sola a nombre de '+NOTA.id.nombre+'.'
      :'Modo repaso: esta nota no se guarda. Cuando el docente abra la clase, te saldrá la ventana para elegir tu nombre.';
  }
  on(document,'nota:pintar',pintar);
  pintar();
};
"""

JS_MOTOR = {
    "robot": r"""
M.robot=function(r){
  var cfg=JSON.parse(r.dataset.cfg),tam=cfg.tam,max=cfg.max,muro={};
  (cfg.muros||[]).forEach(function(m){muro[m[0]+','+m[1]]=1;});
  var bot=ver(r,'.a-rb-bot'),prog=ver(r,'[data-prog]'),cuenta=ver(r,'[data-cuenta]'),cartas=todos(r,'[data-carta]');
  var bEj=ver(r,'[data-ejecutar]'),bQu=ver(r,'[data-quitar]'),bBo=ver(r,'[data-borrar]');
  var NOM={AVANZA:'Avanza',GIRA_IZQ:'Gira ↺',GIRA_DER:'Gira ↻',REPITE_2:'Repite 2×'};
  var ROT={N:0,E:90,S:180,O:270},IZQ={N:'O',O:'S',S:'E',E:'N'},DER={N:'E',E:'S',S:'O',O:'N'};
  var D={N:[0,-1],E:[1,0],S:[0,1],O:[-1,0]};
  var lista=[],reloj=null,est;
  function poner(){bot.style.setProperty('--x',est.x);bot.style.setProperty('--y',est.y);bot.style.setProperty('--rot',est.rot+'deg');}
  function inicio(){est={x:cfg.inicio[0],y:cfg.inicio[1],d:cfg.inicio[2],rot:ROT[cfg.inicio[2]]};poner();}
  function dibujar(){
    prog.innerHTML='';
    lista.forEach(function(c){var li=document.createElement('li');li.textContent=NOM[c];prog.appendChild(li);});
  }
  function botones(){
    var corre=!!reloj;
    cuenta.textContent=lista.length+' / '+max;
    cartas.forEach(function(b){b.disabled=corre||lista.length>=max;});
    bEj.disabled=corre||!lista.length;bQu.disabled=corre||!lista.length;bBo.disabled=corre||!lista.length;
  }
  function parar(){if(reloj){clearTimeout(reloj);reloj=null;}}
  function reiniciar(){parar();inicio();fb(r,null,'');dibujar();botones();}
  cartas.forEach(function(b){on(b,'click',function(){
    if(lista.length>=max||reloj)return;
    lista.push(b.dataset.carta);reiniciar();
  });});
  on(bQu,'click',function(){lista.pop();reiniciar();});
  on(bBo,'click',function(){lista=[];reiniciar();});
  on(bEj,'click',function(){
    reiniciar();
    var pasos=[];
    for(var k=0;k<lista.length;k++){
      var c=lista[k];
      if(c==='REPITE_2'){
        var sig=lista[k+1];
        if(sig&&sig!=='REPITE_2'){pasos.push({c:sig,k:k+1,rep:k});pasos.push({c:sig,k:k+1,rep:k});k++;}
      }else pasos.push({c:c,k:k});
    }
    var p=0,vel=QUIETO?90:430;
    function marca(q,clase){
      var lis=todos(prog,'li');
      lis.forEach(function(li){li.classList.remove('activa');});
      if(q.rep!==undefined&&lis[q.rep])lis[q.rep].classList.add(clase);
      if(lis[q.k])lis[q.k].classList.add(clase);
    }
    function fin(ok,msg){reloj=null;botones();if(ok)gana(r);fb(r,ok,msg);}
    function paso(){
      if(p>=pasos.length){marca({k:-1},'activa');return fin(false,'Se acabaron las tarjetas y el robot no llegó. Cambia el programa.');}
      var q=pasos[p++];marca(q,'activa');
      if(q.c==='GIRA_IZQ'){est.d=IZQ[est.d];est.rot-=90;}
      else if(q.c==='GIRA_DER'){est.d=DER[est.d];est.rot+=90;}
      else{
        var nx=est.x+D[est.d][0],ny=est.y+D[est.d][1];
        if(nx<0||ny<0||nx>=tam||ny>=tam||muro[nx+','+ny]){
          marca(q,'falla');
          return fin(false,'¡Choque en la tarjeta '+(q.k+1)+'! Ahí no se puede avanzar.');
        }
        est.x=nx;est.y=ny;
      }
      poner();
      if(est.x===cfg.meta[0]&&est.y===cfg.meta[1])return fin(true,'¡Llegó a la meta con '+lista.length+' tarjetas!');
      reloj=setTimeout(paso,vel);
    }
    reloj=setTimeout(paso,QUIETO?0:250);botones();
  });
  pausas.push(reiniciar);
  inicio();botones();
};
""",
}

JS_FIN = r"""
(function(){
  var bl=document.querySelector('.chrome.bl');if(!bl)return;
  chipP=document.createElement('span');chipP.className='a-puntos';chipP.setAttribute('aria-live','polite');
  bl.appendChild(chipP);
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){chipP.remove();});
})();
pintarNota();
// La página pone la ventana del nombre y habla con la base; aquí se escucha.
on(document,'clase:identidad',function(e){identidad(e.detail||{});});
on(document,'clase:guardado',function(e){
  var d=e.detail||{};
  if(d.detalle){NOTA.hechos=Object.assign({},NOTA.hechos,d.detalle);guardarNota();pintarNota();}
});
// Desmarcado por el docente: vuelve la ventana, y lo hecho sigue en esta PC.
on(document,'clase:desmarcado',function(){NOTA.id=null;pintarNota();});
document.dispatchEvent(new CustomEvent('clase:pregunta'));
// Las demos no tienen final: cuentan al usarlas.
todos(document,'[data-nota-tipo=demo]').forEach(function(n){on(n,'click',function(){gana(n);});});

M.hecho=function(r){
  /* La práctica sin editor (la desenchufada y la de enlace) no tiene nada que
     ejecutar: el punto se lo da el estudiante al marcar que la terminó. Es
     participación, no corrección, y por eso solo se puede marcar una vez. */
  var b=ver(r,'[data-hecho]');
  on(b,'click',function(){b.disabled=true;b.textContent='✓ Terminada';gana(r);});
};

M.imprimir=function(r){on(ver(r,'[data-imprimir]'),'click',function(){window.print();});};

todos(document,'[data-act]').forEach(function(r){
  var f=M[r.dataset.act];if(!f)return;
  try{f(r);}catch(e){console.error('[actividades]',r.dataset.act,e);}
});

// Al cambiar de diapositiva: los juegos se detienen y lo que mira la
// diapositiva en curso (el precalentado de Python) se vuelve a preguntar.
if(typeof show==='function'){
  var mostrarAct=show,relojYa=null;
  show=function(n){
    mostrarAct(n);
    pausas.forEach(function(f){try{f();}catch(e){}});
    cambios.forEach(function(f){try{f();}catch(e){}});
    // Si la entrada se queda a medias porque el navegador se trabó, al segundo
    // y pico se apaga la animación y la diapositiva se ve entera igual.
    clearTimeout(relojYa);
    todos(document,'.slide.a-ya').forEach(function(s){s.classList.remove('a-ya');});
    relojYa=setTimeout(function(){
      var s=document.querySelector('.slide.on');if(s)s.classList.add('a-ya');
    },1300);
  };
}

// El panel del guion: fuera de la proyección, cerrado hasta que se abre.
(function(){
  var btn=document.querySelector('.a-guion-btn'),panel=document.querySelector('.a-guion');
  if(!btn||!panel)return;
  var cerrar=ver(panel,'[data-cerrar]');
  function abrir(v){panel.hidden=!v;btn.setAttribute('aria-expanded',String(v));(v?cerrar:btn).focus();}
  on(btn,'click',function(){abrir(panel.hidden);});
  on(cerrar,'click',function(){abrir(false);});
  // Dentro del panel las teclas son del panel: ni flechas ni espacio pasan diapositivas.
  on(panel,'keydown',function(e){e.stopPropagation();if(e.key==='Escape')abrir(false);});
})();

// Con «Apagar los juegos» del docente, lo que esté corriendo se detiene.
try{
  var obs=new MutationObserver(function(){
    if(document.documentElement.getAttribute('data-bloqueo')==='juegos')
      pausas.forEach(function(f){try{f();}catch(e){}});
  });
  obs.observe(document.documentElement,{attributes:true,attributeFilter:['data-bloqueo']});
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){obs.disconnect();});
}catch(e){}
})();
"""


# ═════════════════════════════════════════════════════════════════════════════
#  El resto de los motores de juego
# ═════════════════════════════════════════════════════════════════════════════

from build_deck import CSS_JUEGO, JS_INTER, demo as demo_deck

DEMOS = {"dado", "ia", "datos", "formulario", "pagina"}


def _tipado(v):
    """El valor con su tipo de Python. En JSON 2.0 llega como 2 y «puntos»
    dejaría de ser float: el tipo viaja aparte."""
    if isinstance(v, bool):
        return ["bool", v]
    if isinstance(v, int):
        return ["int", v]
    if isinstance(v, float):
        return ["float", v]
    return ["str", str(v)]


def _cfg(d):
    return A(json.dumps(d, ensure_ascii=False))


def juego_demo(j, ctx):
    return f'<div class="tarj a-demo">{demo_deck(j["tipo"], ctx["nid"])}</div>'


def juego_clasifica(j, ctx):
    items = j["items"]
    fichas = "".join(f'<button type="button" class="a-ficha" aria-pressed="false" data-c="{items[i][1]}">{E(items[i][0])}</button>'
                     for i in orden(len(items), f'{ctx["nid"]}:{ctx["n"]}:clasifica', distinto=False))
    cubetas = "".join(f'<div class="a-cubeta"><button type="button" class="a-cub-btn" data-cub="{k}">{E(c)}</button>'
                      f'<div class="a-cub-dentro" data-dentro></div></div>' for k, c in enumerate(j["cubetas"]))
    return f"""<div class="a-clasifica" data-act="clasifica">
      <p class="a-explica">Toca una tarjeta y después la caja donde va.</p>
      <div class="a-fichas" data-fichas>{fichas}</div>
      <div class="a-cubetas">{cubetas}</div>
      <div class="a-acc"><span class="a-marca" data-marca>0 / {len(items)}</span>
        <button type="button" class="a-btn a-sec" data-reintentar>Reintentar</button></div>
      {FB}
    </div>"""


def juego_marcador(j, ctx):
    variables = {k: _tipado(v) for k, v in j.get("variables", {}).items()}
    cajas = j.get("cajas", [])
    for c in cajas:
        variables[c["var"]] = ["str", c["valor"]]
    botones = []
    for b in j["botones"]:
        c = {k: v for k, v in b.items() if k not in ("texto", "linea")}
        if "valor" in c:
            c["valor"] = _tipado(c["valor"])
        if "calc" in c:
            c["calc"] = dict(c["calc"])
            if not isinstance(c["calc"]["der"], str):
                c["calc"]["der"] = _tipado(c["calc"]["der"])
        botones.append(f'<button type="button" class="a-mb" data-b="{_cfg(c)}"><b>{E(b["texto"])}</b>'
                       f'<code>{E(b["linea"])}</code></button>')
    s_cajas = "".join(f'<label class="a-caja-e"><code>{E(c["var"])} = caja.value</code>'
                      f'<input class="campo" data-caja="{A(c["var"])}" value="{A(c["valor"])}"></label>' for c in cajas)
    meta = j.get("meta")
    s_meta = (f'<div class="a-meta"><span>Meta: <code>{E(meta["var"])}</code> llega a {meta["valor"]} en {meta["segundos"]} s</span>'
              f'<button type="button" class="a-btn" data-meta>▶ Empezar el reto</button><span data-crono></span></div>'
              if meta else "")
    s_ls = ('<div class="a-ls"><p class="a-etq">localStorage (lo que sobrevive a recargar)</p><pre data-ls>(vacío)</pre>'
            '<button type="button" class="a-btn a-sec" data-recargar>⟳ Recargar la página</button></div>'
            if j.get("recargar") else "")
    cfg = {"variables": variables, "meta": meta}
    return f"""<div class="a-marcador" data-act="marcador" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        {f'<div class="a-cajas">{s_cajas}</div>' if s_cajas else ''}
        <p class="a-etq">Toca un botón: cada uno ejecuta su línea</p>
        <div class="a-mbs">{"".join(botones)}</div>
        {s_meta}
      </div>
      <div class="a-col">
        <p class="a-etq">Variables</p><div class="a-vars" data-vars></div>
        <pre class="a-salida" data-salida>&gt;&gt;&gt; </pre>
        {s_ls}
        {FB}
      </div>
    </div>"""


def _num(v):
    return repr(v)


def juego_ramas(j, ctx):
    var, sec = j["variable"], j.get("secreto", False)
    filas = [f'<li data-var>{E(var)} = {E(_num(j["min"]))}</li>']
    if sec:
        filas.insert(0, f'<li>secreto = random.randint({_num(j["min"])}, {_num(j["max"])})</li>')
    for k, rm in enumerate(j["ramas"]):
        if rm["op"] == "else":
            cab = "else:"
        else:
            valor = "secreto" if rm["valor"] == "secreto" else _num(rm["valor"])
            cab = f'{"if" if k == 0 else "elif"} {var} {rm["op"]} {valor}:'
        filas.append(f'<li data-rama="{k}"><span>{E(cab)}</span></li>'
                     f'<li data-rama="{k}"><span>    display({E(json.dumps(rm["mensaje"], ensure_ascii=False))})</span></li>')
    if j["entrada"] == "slider":
        entrada = (f'<input type="range" data-entrada min="{j["min"]}" max="{j["max"]}" step="{j["paso"]}" value="{j["min"]}" '
                   f'aria-label="{A(var)}">')
    else:
        entrada = (f'<div class="a-acc"><input class="campo" type="number" data-entrada min="{j["min"]}" max="{j["max"]}" '
                   f'step="{j["paso"]}" aria-label="{A(var)}" placeholder="{j["min"]}–{j["max"]}">'
                   f'<button type="button" class="a-btn" data-probar>Probar</button></div>')
    extra = ('<div class="a-acc"><span class="a-marca">Intentos: <b data-intentos>0</b></span>'
             '<button type="button" class="a-btn a-sec" data-nuevo>Nuevo número secreto</button></div>' if sec else "")
    cfg = {k: j[k] for k in ("min", "max", "paso")}
    cfg.update({"secreto": sec, "ramas": j["ramas"], "variable": var})
    return f"""<div class="a-ramas" data-act="ramas" data-cfg="{_cfg(cfg)}">
      <ol class="a-cod" data-leng="python">{"".join(filas)}</ol>
      <div class="a-control">
        <p class="a-etq">Cambia <code>{E(var)}</code> y mira qué rama se ejecuta</p>
        {entrada}{extra}
        <p class="a-res" data-res aria-live="polite"></p>
        {FB}
      </div>
    </div>"""


def juego_ppt(j, ctx):
    codigo_ppt = [
        ("ops", 'opciones = ["piedra", "papel", "tijera"]'),
        ("yo", 'yo = "…"'),
        ("pc", "pc = random.choice(opciones)"),
        (0, "if yo == pc:"), (0, '    display("Empate")'),
        (1, 'elif yo == "piedra" and pc == "tijera":'), (1, '    display("¡Ganaste!")'),
        (2, 'elif yo == "papel" and pc == "piedra":'), (2, '    display("¡Ganaste!")'),
        (3, 'elif yo == "tijera" and pc == "papel":'), (3, '    display("¡Ganaste!")'),
        (4, "else:"), (4, '    display("Gana la computadora")'),
    ]
    def fila(m, t):
        if m == "ops":
            # Cada opción, marcable: mientras la compu sortea se va encendiendo
            # la que mira, y así se ve de dónde sale random.choice.
            dentro = 'opciones = [' + ", ".join(
                f'<span data-op="{o}">&quot;{o}&quot;</span>' for o in ("piedra", "papel", "tijera")) + "]"
            return f'<li><span>{dentro}</span></li>'
        abre = f'<li data-{m}>' if m in ("yo", "pc") else f'<li data-rama="{m}">' if m is not None else "<li>"
        return f"{abre}<span>{E(t)}</span></li>"

    filas = "".join(fila(m, t) for m, t in codigo_ppt)
    manos = "".join(
        f'<button type="button" data-jugada="{o}">{e}<span>{o}</span></button>'
        for o, e in (("piedra", "✊"), ("papel", "✋"), ("tijera", "✌")))
    return f"""<div class="a-ramas" data-act="ppt">
      <ol class="a-cod" data-leng="python">{filas}</ol>
      <div class="a-control">
        <p class="a-etq">Elige tu jugada</p>
        <div class="a-ppt-btns">{manos}</div>
        <div class="a-duelo">
          <div class="a-duelo-lado"><p class="a-etq">Tú</p>
            <span class="a-mano" data-mano="yo">·</span><b data-nom="yo">elige</b></div>
          <span class="a-vs">VS</span>
          <div class="a-duelo-lado" data-lado="pc"><p class="a-etq">La compu</p>
            <span class="a-mano" data-mano="pc">?</span><b data-nom="pc">esperando</b></div>
        </div>
        <p class="a-res" data-res aria-live="polite"></p>
        <div class="a-ppt-marcador"><span>Tú <b data-m="yo">0</b></span><span>Compu <b data-m="pc">0</b></span><span>Empates <b data-m="emp">0</b></span></div>
      </div>
    </div>"""


def _traza_bucle(j):
    ac = j.get("acumula")
    acc = ac["inicio"] if ac else None
    filas = []

    def paso(v):
        nonlocal acc
        if ac:
            x = v if ac["usa"] == "var" else ac["usa"]
            acc = acc + x if ac["op"] == "+=" else acc * x
        filas.append({"vuelta": len(filas) + 1, "var": repr(v), "acum": repr(acc) if ac else "—"})

    if j["modo"] == "for":
        it = j["iterable"]
        valores = list(range(*it["range"])) if "range" in it else list(it["lista"])
        for v in valores:
            paso(v)
        cab = (f'for {j["var"]} in range({", ".join(map(str, it["range"]))}):' if "range" in it
               else f'for {j["var"]} in {it["lista"]!r}:')
        antes = []
        final = (f'Terminó: {ac["var"]} = {acc!r}' if ac else f"Terminó después de {len(filas)} vueltas.")
        nombre_var = j["var"]
    else:
        m = j["mientras"]
        ops = {"<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b, ">=": lambda a, b: a >= b}
        v = m["inicio"]
        while ops[m["op"]](v, m["valor"]) and len(filas) < 12:
            paso(v)
            v = v + m["cambio"]
        cab = f'while {m["var"]} {m["op"]} {m["valor"]!r}:'
        antes = [f'{m["var"]} = {m["inicio"]!r}']
        final = f'{m["var"]} = {v!r} → {m["var"]} {m["op"]} {m["valor"]!r} es False: el bucle termina.'
        nombre_var = m["var"]
    if ac:
        antes.insert(0, f'{ac["var"]} = {ac["inicio"]!r}')
    return {"filas": filas, "final": final}, antes, cab, nombre_var


def juego_bucle(j, ctx):
    traza, antes, cab, nombre_var = _traza_bucle(j)
    ac = j.get("acumula")
    filas = ("".join(f"<li><span>{E(x)}</span></li>" for x in antes)
             + f'<li data-cab><span>{E(cab)}</span></li>'
             + "".join(f"<li><span>{E(x)}</span></li>" for x in j["cuerpo"]))
    # La apuesta: antes de ver la traza, dicen qué va a dar. Mirar una tabla
    # llenarse sola no enseña nada; arriesgar una respuesta, sí.
    ap = j.get("apuesta")
    apuesta = ""
    if ap:
        ops = "".join(
            f'<button type="button" class="a-op" data-ap="{k}"'
            f'{" data-ok" if k == ap["correcta"] else ""}>'
            f'<span class="a-letra">{chr(65 + k)}</span><code>{E(x)}</code></button>'
            for k, x in enumerate(ap["opciones"]))
        apuesta = (f'<div class="a-bu-apuesta" data-apuesta>'
                   f'<p class="a-etq">Antes de correrlo</p>'
                   f'<p class="a-bu-preg">{E(ap["pregunta"])}</p>'
                   f'<div class="a-ops">{ops}</div></div>')
    return f"""<div class="a-ramas" data-act="bucle" data-traza="{_cfg(traza)}">
      <ol class="a-cod" data-leng="python">{filas}</ol>
      <div class="a-control">
        {apuesta}
        <div class="a-acc"><button type="button" class="a-btn" data-sig>Siguiente vuelta</button>
          <button type="button" class="a-btn a-sec" data-todo>Todas de una</button>
          <button type="button" class="a-btn a-sec" data-reiniciar>Reiniciar</button></div>
        <div class="a-tabla-caja"><table class="a-traza"><thead><tr><th>Vuelta</th><th>{E(nombre_var)}</th>
          <th>{E(ac["var"]) if ac else "—"}</th></tr></thead><tbody></tbody></table></div>
        <p class="a-res" data-res aria-live="polite"></p>
        {FB}
      </div>
    </div>"""


def juego_lista(j, ctx):
    dic = j["modo"] == "dict"
    nombre, ops, valores = j["nombre"], j["ops"], j.get("valores", [])
    if dic:
        ini = [[_tipado(k), _tipado(v)] for k, v in j["inicial"].items()]
    else:
        ini = [_tipado(v) for v in j["inicial"]]
    cfg = {"modo": j["modo"], "nombre": nombre, "inicial": ini, "valores": [_tipado(v) for v in valores]}
    rotulos = ({"get": f"{nombre}[clave]", "set": f"{nombre}[clave] = valor", "del": f"del {nombre}[clave]",
                "len": f"len({nombre})", "in": f"clave in {nombre}"} if dic else
               {"append": f"{nombre}.append(valor)", "pop": f"{nombre}.pop()", "len": f"len({nombre})",
                "indice": f"{nombre}[i]", "in": f"valor in {nombre}"})
    necesita_valor = {"set"} if dic else {"append", "in"}
    controles = ""
    if dic:
        primera = next(iter(j["inicial"]), "")
        controles += f'<label class="a-caja-e"><code>clave =</code><input class="campo" data-key value="{A(primera)}"></label>'
    if "indice" in ops:
        controles += '<label class="a-caja-e"><code>i =</code><input class="campo" type="number" data-idx value="0"></label>'
    if necesita_valor & set(ops) and valores:
        opc = "".join(f'<option value="{k}">{E(repr(v))}</option>' for k, v in enumerate(valores))
        controles += f'<label class="a-caja-e"><code>valor =</code><select class="campo" data-val>{opc}</select></label>'
    botones = "".join(f'<button type="button" class="a-mb" data-op="{o}"><code>{E(rotulos[o])}</code></button>' for o in ops)
    return f"""<div class="a-marcador" data-act="lista" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        <div class="a-cajas">{controles}</div>
        <div class="a-mbs">{botones}</div>
        <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Reiniciar</button></div>
      </div>
      <div class="a-col">
        <p class="a-etq"><code>{E(nombre)}</code></p>
        <div class="a-cajas-l" data-cajas></div>
        <pre class="a-salida" data-salida>&gt;&gt;&gt; </pre>
      </div>
    </div>"""


def juego_caza(j, ctx):
    """Leer la lista, que es lo que de verdad cuesta: contar desde 0.

    La máquina de la lista daba sus puntos por tocar cuatro botones y no tenía
    respuesta correcta; además repetía lo que ya hace el taller, que es
    ESCRIBIR las líneas. Aquí solo se lee: cuál es `preguntas[2]`, en qué
    posición está una, cuánto da `len`. Las tarjetas salen SIN su número a
    propósito: el número se revela al contestar.
    """
    cfg = {"nombre": j["nombre"], "inicial": list(j["inicial"]),
           "extra": list(j.get("extra", [])), "rondas": j["rondas"], "gana": j["gana"]}
    return f"""<div class="a-caza" data-act="caza" data-cfg="{_cfg(cfg)}">
      <div class="a-caza-top"><span>Aciertos <b data-pts>0</b></span><span>Racha <b data-racha>0</b></span>
        <span>Ronda <b data-ronda>1</b> de {cfg["rondas"]}</span></div>
      <p class="a-caza-preg" data-preg></p>
      <p class="a-etq"><code>{E(j["nombre"])}</code></p>
      <div class="a-caza-fila" data-fila></div>
      <div class="a-caza-nums" data-nums hidden></div>
      <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar hidden>Otra vuelta</button></div>
      {FB}
    </div>"""


def juego_aventura(j, ctx):
    cfg = {"inicio": j["inicio"], "salas": j["salas"]}
    return f"""<div class="a-aventura" data-act="aventura" data-cfg="{_cfg(cfg)}">
      <div class="a-sala"><code data-cab></code><p data-txt></p><div class="a-ops" data-ops></div></div>
      <p class="a-rastro" data-rastro></p>
      <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Empezar otra vez</button></div>
      {FB}
    </div>"""


def juego_carrera(j, ctx):
    cfg = {"segundos": j["segundos"], "preguntas": j["preguntas"]}
    return f"""<div class="a-carrera" data-act="carrera" data-cfg="{_cfg(cfg)}">
      <div class="a-car-top"><span>Tiempo <b data-t>{j["segundos"]}</b></span><span>Aciertos <b data-pts>0</b></span>
        <span>Racha <b data-racha>0</b></span></div>
      <button type="button" class="a-btn" data-empezar>▶ Empezar la carrera</button>
      <div data-zona hidden><p class="a-car-preg" data-preg></p><div class="a-ops" data-ops></div></div>
      {FB}
    </div>"""


MOTORES_HTML.update({
    "clasifica": juego_clasifica, "marcador": juego_marcador, "ramas": juego_ramas, "ppt": juego_ppt,
    "bucle": juego_bucle, "lista": juego_lista, "caza": juego_caza,
    "aventura": juego_aventura, "carrera": juego_carrera,
    **{d: juego_demo for d in DEMOS},
})

# Lo que comparten los dos talleres de «tu primera vez»: la montaña de
# variables y la escalera de ciclos. Vive aparte porque cada motor carga solo
# su CSS, y la escalera salía desnuda cuando no había montaña en la clase.
_CSS_TALLER = """
.a-mt-din{font-size:13.5px;color:var(--tx2)}
.a-mt-din summary{cursor:pointer;font-family:var(--fm);font-size:12px;letter-spacing:.08em;color:var(--sand)}
.a-mt-din ol{margin:8px 0 0;padding-left:20px;display:grid;gap:4px}
.a-mt-mision{padding:10px 14px;background:var(--bg2);border:1px solid var(--line);border-left:4px solid var(--lvl);border-radius:6px}
.a-mt-pide{margin:4px 0 0;font-family:var(--fd);font-weight:700;font-size:clamp(16px,1.8vw,21px);line-height:1.3}
.a-mt-escribe{display:flex;gap:8px}
.a-mt-in{flex:1;min-height:48px;font-family:var(--fm);font-size:clamp(15px,1.6vw,19px)}
.a-mt-pista{margin:0;font-size:12.5px;color:var(--mut)}
.a-mt-pista code{font-family:var(--fm);color:var(--tx2)}
.a-mt-prog{margin:0;min-height:72px;padding:10px 14px;border-radius:8px;background:#0B1020;color:#D7DEEC;
  border:1px solid var(--line);font-family:var(--fm);font-size:clamp(13px,1.35vw,15.5px);line-height:1.6;white-space:pre-wrap}
"""

_CSS_COL = """
.a-marcador{display:grid;gap:16px;margin-top:14px}
@media(min-width:980px){.a-marcador{grid-template-columns:1fr 1fr;align-items:start}}
.a-col{display:grid;gap:12px;align-content:start}
.a-mbs{display:flex;flex-wrap:wrap;gap:8px}
.a-mb{display:grid;gap:3px;text-align:left;min-height:50px;padding:8px 13px;border-radius:6px;border:1px solid var(--lvl);
  background:var(--panel);color:var(--tx);cursor:pointer;touch-action:manipulation;font-family:var(--fb)}
.a-mb b{font-size:clamp(14px,1.5vw,17px)}
.a-mb code{font-family:var(--fm);font-size:clamp(12px,1.25vw,14px);color:var(--tx2)}
.a-mb:hover{background:var(--panel2)}
.a-mb:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-cajas{display:grid;gap:8px}
.a-caja-e{display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-family:var(--fm);font-size:14px;color:var(--tx2)}
.a-caja-e .campo{flex:0 1 220px;min-height:44px;font-size:16px}
.a-salida{margin:0;min-height:3.4em;padding:10px 14px;background:#0B1020;border:1px solid var(--line);border-radius:6px;
  color:#A7F3C4;font-family:var(--fm);font-size:clamp(12.5px,1.35vw,15px);white-space:pre-wrap;word-break:break-word}
.a-salida.a-err{color:#FCA5A5}
"""

_CSS_RAMAS = """
.a-ramas{display:grid;gap:16px;margin-top:14px}
@media(min-width:980px){.a-ramas{grid-template-columns:1.1fr .9fr;align-items:start}}
.a-control{display:grid;gap:12px;padding:16px;background:var(--bg2);border:1px solid var(--line);border-radius:6px}
.a-control input[type=range]{width:100%;accent-color:var(--lvl);min-height:40px}
.a-control .campo{flex:0 1 150px;min-height:46px;font-size:20px}
.a-res{font-family:var(--fd);font-weight:800;font-size:clamp(22px,3vw,38px);color:var(--lvl);min-height:1.2em;margin:0}
.a-cod li.a-toma{background:rgba(123,216,168,.16);box-shadow:inset 3px 0 0 var(--a-ok)}
.a-marca b{color:var(--lvl);font-size:18px}
"""

CSS_MOTOR.update({
    "clasifica": """
.a-clasifica{display:grid;gap:14px;margin-top:14px}
.a-fichas{display:flex;flex-wrap:wrap;gap:8px;min-height:50px}
.a-ficha{min-height:46px;padding:8px 15px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--tx);
  font-family:var(--fb);font-weight:600;font-size:clamp(13px,1.45vw,16px);cursor:pointer;touch-action:manipulation}
.a-ficha[aria-pressed="true"]{border-color:var(--lvl);box-shadow:0 0 0 2px var(--lvl);background:var(--panel2)}
.a-ficha:disabled{cursor:default;border-color:var(--a-ok)}
.a-ficha:focus-visible,.a-cub-btn:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-cubetas{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}
.a-cubeta{display:grid;gap:8px;align-content:start;padding:10px;border:2px dashed var(--line);border-radius:8px;min-height:120px}
.a-cub-btn{min-height:48px;border-radius:6px;border:0;background:var(--lvl);color:var(--bg);font-family:var(--fd);
  font-weight:800;font-size:clamp(14px,1.6vw,18px);cursor:pointer;touch-action:manipulation}
.a-cub-dentro{display:flex;flex-wrap:wrap;gap:6px}
.a-cub-dentro .a-ficha{min-height:34px;padding:4px 10px;font-size:13px}
.a-sacude{animation:a-sacude .35s}
@keyframes a-sacude{25%{transform:translateX(-7px)}75%{transform:translateX(7px)}}
.a-marca{font-family:var(--fm);font-size:13px;color:var(--mut)}
""",
    "marcador": _CSS_COL + """
.a-vars{display:grid;gap:6px;font-family:var(--fm)}
.a-var{display:grid;grid-template-columns:auto auto 1fr auto;gap:10px;align-items:baseline;padding:10px 14px;background:#0B1020;
  border:1px solid var(--line);border-radius:6px;color:#D7DEEC;font-size:clamp(15px,1.8vw,21px)}
.a-var b{color:#FDBA74;font-weight:600;word-break:break-all}
.a-var i{font-style:normal;font-size:11px;color:#7E8BA6;letter-spacing:.08em}
.a-meta{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:14px;color:var(--tx2)}
.a-meta [data-crono]{font-family:var(--fd);font-size:30px;font-weight:800;color:var(--lvl)}
.a-ls{padding:10px 12px;border:1px dashed var(--line);border-radius:6px;display:grid;gap:8px}
.a-ls pre{margin:0;font-family:var(--fm);font-size:13px;color:var(--tx2);white-space:pre-wrap;word-break:break-all}
""",
    "ramas": _CSS_RAMAS,
    "ppt": _CSS_RAMAS + """
/* La mesa: tu mano, el VS y la de la compu, que es lo que antes solo existía
   como un comentario diminuto dentro del código. */
.a-duelo{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center;
  padding:14px;border-radius:10px;background:var(--panel);border:1px solid var(--line)}
.a-duelo-lado{display:grid;gap:2px;justify-items:center;text-align:center}
.a-duelo-lado .a-etq{margin:0}
.a-mano{font-size:clamp(42px,6vh,68px);line-height:1.1}
.a-duelo-lado b{font-family:var(--fm);font-size:13.5px;color:var(--tx2)}
.a-vs{font-family:var(--fd);font-weight:800;font-size:clamp(16px,2vw,22px);color:var(--mut);letter-spacing:.06em}
.a-duelo-lado[data-lado=pc].a-sortea .a-mano{animation:tiembla .22s linear infinite}
@keyframes tiembla{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-5px) rotate(4deg)}}
.a-cod [data-op]{border-radius:4px;padding:0 1px}
.a-cod [data-op].a-mira{background:rgba(229,185,141,.22);box-shadow:0 0 0 2px rgba(229,185,141,.5)}
.a-res[data-r=gana]{color:var(--a-ok)}
.a-res[data-r=pierde]{color:var(--a-ko)}
.a-res[data-r=empate]{color:var(--sand)}
.a-ppt-btns{display:flex;gap:10px;flex-wrap:wrap}
.a-ppt-btns button{font-size:clamp(28px,5vh,44px);min-width:88px;min-height:88px;border-radius:12px;border:1px solid var(--line);
  background:var(--panel);cursor:pointer;display:grid;place-items:center;gap:2px;color:var(--tx);font-family:var(--fb);
  touch-action:manipulation}
.a-ppt-btns button:hover{border-color:var(--lvl)}
.a-ppt-btns button span{font-size:12px}
.a-ppt-marcador{display:flex;gap:18px;font-family:var(--fm);font-size:14px;color:var(--tx2)}
.a-ppt-marcador b{color:var(--lvl);font-size:22px}
""",
    "bucle": _CSS_RAMAS + """
.a-bu-apuesta{display:grid;gap:9px;padding:12px 14px;background:var(--bg2);border:1px solid var(--line);
  border-left:4px solid var(--lvl);border-radius:6px}
.a-bu-preg{margin:0;font-family:var(--fd);font-weight:700;font-size:clamp(15px,1.7vw,20px);line-height:1.3}
.a-bu-apuesta .a-ops{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}
.a-bu-apuesta code{font-family:var(--fm)}
.a-tabla-caja{max-height:40vh;overflow:auto;border:1px solid var(--line);border-radius:6px;background:var(--bg)}
.a-traza{width:100%;border-collapse:collapse;font-family:var(--fm);font-size:clamp(13px,1.4vw,16px)}
.a-traza th{position:sticky;top:0;background:var(--bg2);font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--mut);text-align:left;padding:7px 10px;border-bottom:1px solid var(--line)}
.a-traza td{padding:7px 10px;border-bottom:1px solid var(--line);color:var(--tx)}
.a-traza tr:last-child td{background:rgba(123,216,168,.12)}
.a-res{font-size:clamp(16px,2vw,22px)}
""",
    "lista": _CSS_COL + """
.a-cajas-l{display:flex;flex-wrap:wrap;gap:8px;min-height:78px;padding:10px;background:#0B1020;border:1px solid var(--line);
  border-radius:6px;align-items:flex-start}
.a-cl{display:grid;justify-items:center;gap:4px;min-width:66px;padding:8px 11px;border-radius:6px;background:#141B30;
  border:1px solid #2A3553;font-family:var(--fm)}
.a-cl i{font-style:normal;font-size:11px;color:#7E8BA6}
.a-cl b{color:#FDBA74;font-size:clamp(14px,1.6vw,18px);font-weight:600}
.a-cl.a-nuevo{border-color:#7BD8A8;box-shadow:0 0 0 1px #7BD8A8}
.a-lista-vacia{color:#7E8BA6;font-family:var(--fm);font-size:13px;padding:14px}
""",
    "aventura": """
.a-aventura{display:grid;gap:14px;margin-top:14px;max-width:780px}
.a-sala{padding:18px 20px;background:var(--bg2);border:1px solid var(--line);border-left:4px solid var(--lvl);border-radius:6px;
  display:grid;gap:12px}
.a-sala code{font-family:var(--fm);color:var(--lvl);font-size:15px}
.a-sala p{font-size:clamp(16px,1.9vw,22px);line-height:1.45}
.a-sala .a-op small{margin-left:auto;font-family:var(--fm);color:var(--mut);font-size:12px}
.a-rastro{font-family:var(--fm);font-size:13px;color:var(--mut);word-break:break-word;margin:0}
""",
    "caza": """
.a-caza{display:grid;gap:14px;margin-top:14px;max-width:900px;justify-items:start}
.a-caza-top{display:flex;gap:22px;align-items:baseline;flex-wrap:wrap;font-family:var(--fm);color:var(--tx2)}
.a-caza-top b{font-family:var(--fd);font-size:30px;color:var(--lvl)}
.a-caza .a-etq{margin:0}
.a-caza-fila{display:flex;flex-wrap:wrap;gap:10px}
/* La tarjeta sale SIN su número: contarlo es el ejercicio. El hueco se
   reserva desde el principio para que al revelarlo no salte la fila. */
.a-caza-c{display:grid;gap:4px;justify-items:center;min-width:104px;min-height:76px;padding:10px 14px;
  border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--tx);cursor:pointer;
  font-family:var(--fm);font-size:clamp(13px,1.5vw,17px);touch-action:manipulation}
.a-caza-c i{font-style:normal;font-family:var(--fd);font-weight:800;font-size:15px;color:var(--mut);
  min-height:1.2em;opacity:0;transition:opacity .25s}
.a-caza[data-ver="1"] .a-caza-c i{opacity:1}
.a-caza-c:disabled{cursor:default}
.a-caza-c:focus-visible,.a-caza-n:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-caza-c[data-estado=bien],.a-caza-n[data-estado=bien]{border-color:var(--a-ok);box-shadow:inset 0 0 0 1px var(--a-ok)}
.a-caza-c[data-estado=mal],.a-caza-n[data-estado=mal]{border-color:var(--a-ko);opacity:.6}
.a-caza-preg{margin:0;font-family:var(--fd);font-weight:700;line-height:1.25;
  font-size:clamp(18px,2.3vw,28px)}
.a-caza-preg code{font-family:var(--fm);font-weight:400;color:var(--lvl)}
.a-caza-nums{display:flex;flex-wrap:wrap;gap:8px}
.a-caza-n{min-width:58px;min-height:58px;border-radius:9px;border:1px solid var(--line);background:var(--panel);
  color:var(--tx);cursor:pointer;font-family:var(--fd);font-weight:800;font-size:22px;touch-action:manipulation}
""",
    "carrera": """
.a-carrera{display:grid;gap:14px;margin-top:14px;max-width:820px;justify-items:start}
.a-carrera [data-zona]{display:grid;gap:12px;width:100%}
.a-car-top{display:flex;gap:22px;align-items:baseline;flex-wrap:wrap;font-family:var(--fm);color:var(--tx2)}
.a-car-top b{font-family:var(--fd);font-size:34px;color:var(--lvl)}
.a-car-preg{font-size:clamp(18px,2.3vw,28px);font-family:var(--fd);font-weight:700;line-height:1.2;margin:0}
""",
    **{d: ".a-demo{max-width:520px;margin-top:14px}\n.a-demo .demo{margin-top:0;padding-top:0;border-top:0}\n" for d in DEMOS},
})

# Semántica de Python para los valores que se muestran: tipo aparte del
# valor, float siempre con decimal, errores con su nombre real. Una
# calculadora que dijera que "12" + "13" da 25 enseñaría justo lo contrario.
JS_PY = r"""
var P={
  err:function(tipo,msg){var e=new Error(msg);e.py=tipo+': '+msg;return e;},
  fstr:function(x){if(!isFinite(x))return isNaN(x)?'nan':(x>0?'inf':'-inf');return Number.isInteger(x)?x.toFixed(1):String(x);},
  repr:function(v){
    var t=v[0],x=v[1];
    if(t==='str')return "'"+String(x).replace(/\\/g,'\\\\').replace(/'/g,"\\'")+"'";
    if(t==='float')return P.fstr(x);
    if(t==='bool')return x?'True':'False';
    return String(x);
  },
  num:function(v){return v[0]==='int'||v[0]==='float'||v[0]==='bool';},
  conv:function(v,c){
    if(!c)return v;
    if(c==='int'){
      if(v[0]==='str'){var s=v[1].trim();if(!/^[+-]?\d+$/.test(s))throw P.err('ValueError',"invalid literal for int() with base 10: "+P.repr(v));return ['int',parseInt(s,10)];}
      return ['int',Math.trunc(Number(v[1]))];
    }
    if(v[0]==='str'){var f=v[1].trim();if(!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(f))throw P.err('ValueError',"could not convert string to float: "+P.repr(v));return ['float',parseFloat(f)];}
    return ['float',Number(v[1])];
  },
  op:function(a,o,b){
    if(a[0]==='str'||b[0]==='str'){
      if(o==='+'&&a[0]==='str'&&b[0]==='str')return ['str',a[1]+b[1]];
      if(o==='*'&&((a[0]==='str'&&b[0]==='int')||(a[0]==='int'&&b[0]==='str'))){
        var s=a[0]==='str'?a[1]:b[1],n=a[0]==='int'?a[1]:b[1];return ['str',n>0?s.repeat(n):''];
      }
      if(o==='+'&&a[0]==='str')throw P.err('TypeError','can only concatenate str (not "'+b[0]+'") to str');
      throw P.err('TypeError',"unsupported operand type(s) for "+o+": '"+a[0]+"' and '"+b[0]+"'");
    }
    var x=Number(a[1]),y=Number(b[1]),fl=a[0]==='float'||b[0]==='float',t=fl?'float':'int';
    if(y===0&&(o==='/'||o==='//'||o==='%'))
      throw P.err('ZeroDivisionError','division by zero');
    if(o==='+')return [t,x+y];
    if(o==='-')return [t,x-y];
    if(o==='*')return [t,x*y];
    if(o==='/')return ['float',x/y];
    if(o==='//')return [t,Math.floor(x/y)];
    if(o==='%')return [t,x-y*Math.floor(x/y)];
    throw P.err('SyntaxError','operador '+o);
  },
  eq:function(a,b){if(P.num(a)&&P.num(b))return Number(a[1])===Number(b[1]);return a[0]===b[0]&&a[1]===b[1];},
  json:function(v){
    if(v[0]==='str')return JSON.stringify(v[1]).replace(/[-￿]/g,function(c){return '\\u'+('000'+c.charCodeAt(0).toString(16)).slice(-4);});
    if(v[0]==='float')return P.fstr(v[1]);
    if(v[0]==='bool')return v[1]?'true':'false';
    return String(v[1]);
  },
  dumps:function(vars){return '{'+Object.keys(vars).map(function(k){return P.json(['str',k])+': '+P.json(vars[k]);}).join(', ')+'}';}
};
"""

JS_MOTOR.update({
    "clasifica": r"""
M.clasifica=function(r){
  var caja=ver(r,'[data-fichas]'),fichas=todos(r,'.a-ficha'),marca=ver(r,'[data-marca]'),sel=null,bien=0,fallos=0,total=fichas.length;
  function elegir(f){sel=f;fichas.forEach(function(x){x.setAttribute('aria-pressed',String(x===f));});}
  fichas.forEach(function(f){on(f,'click',function(){if(f.dataset.hecha)return;elegir(sel===f?null:f);});});
  todos(r,'[data-cub]').forEach(function(b){on(b,'click',function(){
    if(!sel){fb(r,false,'Primero toca una tarjeta.');return;}
    var cub=b.closest('.a-cubeta');
    if(sel.dataset.c===b.dataset.cub){
      sel.dataset.hecha='1';sel.setAttribute('aria-pressed','false');sel.disabled=true;
      ver(cub,'[data-dentro]').appendChild(sel);sel=null;bien++;marca.textContent=bien+' / '+total;
      if(bien===total)gana(r)&&fb(r,true,'¡Todo clasificado'+(fallos?' con '+fallos+(fallos===1?' error!':' errores!'):' sin un solo error!'));
      else fb(r,true,'¡Bien! Sigue.');
    }else{
      fallos++;cub.classList.remove('a-sacude');void cub.offsetWidth;cub.classList.add('a-sacude');
      fb(r,false,'Ahí no va. Piensa otra vez.');
    }
  });});
  on(ver(r,'[data-reintentar]'),'click',function(){
    fichas.forEach(function(f){delete f.dataset.hecha;f.disabled=false;f.setAttribute('aria-pressed','false');caja.appendChild(f);});
    sel=null;bien=0;fallos=0;marca.textContent='0 / '+total;fb(r,null,'');
  });
};
""",
    "marcador": r"""
M.marcador=function(r){
  var cfg=JSON.parse(r.dataset.cfg),ini=cfg.variables,vars,ls=null,lsVars=null;
  var panel=ver(r,'[data-vars]'),sal=ver(r,'[data-salida]'),lsBox=ver(r,'[data-ls]'),cajas=todos(r,'[data-caja]');
  function copia(o){return JSON.parse(JSON.stringify(o));}
  function empezar(){vars=copia(ini);cajas.forEach(function(inp){inp.value=ini[inp.dataset.caja][1];});}
  function pintar(){
    panel.innerHTML='';
    Object.keys(vars).forEach(function(k){
      var d=document.createElement('div');d.className='a-var';d.innerHTML='<code></code><span>=</span><b></b><i></i>';
      d.children[0].textContent=k;d.children[2].textContent=P.repr(vars[k]);d.children[3].textContent=vars[k][0];
      panel.appendChild(d);
    });
    if(lsBox)lsBox.textContent=ls===null?'(vacío)':ls;
  }
  function salida(linea,res,err){sal.textContent='>>> '+linea+(res!==undefined?'\n'+res:'');sal.classList.toggle('a-err',!!err);}
  cajas.forEach(function(inp){on(inp,'input',function(){vars[inp.dataset.caja]=['str',inp.value];pintar();});});
  var meta=cfg.meta,crono=ver(r,'[data-crono]'),bm=ver(r,'[data-meta]'),t=null,resta=0,enReto=false;
  function parar(){clearInterval(t);t=null;enReto=false;if(bm)bm.disabled=false;}
  function revisar(){
    if(!enReto)return;var v=vars[meta.var];
    if(v&&P.num(v)&&Number(v[1])>=meta.valor){parar();gana(r)&&fb(r,true,'¡Lo lograste con '+resta+' s de sobra!');}
  }
  todos(r,'[data-b]').forEach(function(b){on(b,'click',function(){
    var c=JSON.parse(b.dataset.b),linea=ver(b,'code').textContent;
    try{
      if(c.op==='guardar'){ls=P.dumps(vars);lsVars=copia(vars);salida(linea);}
      else if(c.op==='cargar'){
        if(ls===null)throw P.err('TypeError','the JSON object must be str, bytes or bytearray, not NoneType');
        vars=copia(lsVars);cajas.forEach(function(inp){if(vars[inp.dataset.caja])inp.value=vars[inp.dataset.caja][1];});salida(linea);
      }else if(c.calc){
        var k=c.calc,a=P.conv(vars[k.izq],k.convertir),d=Array.isArray(k.der)?k.der:vars[k.der];
        vars[k.destino]=P.op(a,k.op,P.conv(d,k.convertir));salida(linea,'# '+k.destino+' = '+P.repr(vars[k.destino]));
      }else{
        vars[c.var]=c.op==='='?c.valor:P.op(vars[c.var],c.op==='+='?'+':'-',c.valor);salida(linea);
      }
      pintar();revisar();
    }catch(e){if(e.py)salida(linea,e.py,true);else throw e;}
  });});
  if(bm)on(bm,'click',function(){
    empezar();pintar();salida('# ¡reto en marcha!');resta=meta.segundos;enReto=true;bm.disabled=true;
    crono.textContent=resta+' s';fb(r,null,'');
    t=setInterval(function(){resta--;crono.textContent=resta+' s';if(resta<=0){parar();fb(r,false,'Se acabó el tiempo. ¡Otra vez!');}},1000);
  });
  var brec=ver(r,'[data-recargar]');
  if(brec)on(brec,'click',function(){empezar();pintar();salida('# recargaste: las variables vuelven a empezar','# localStorage sigue ahí');});
  pausas.push(function(){if(t){parar();if(crono)crono.textContent='';}});
  empezar();pintar();
};
""",
    "ramas": r"""
M.ramas=function(r){
  var cfg=JSON.parse(r.dataset.cfg),inp=ver(r,'[data-entrada]'),filas=todos(r,'[data-rama]'),res=ver(r,'[data-res]');
  var lvar=ver(r,'[data-var]'),cont=ver(r,'[data-intentos]'),intentos=0,secreto=null,vistas={};
  function cumple(v,op,x){switch(op){case '<':return v<x;case '<=':return v<=x;case '>':return v>x;case '>=':return v>=x;
    case '==':return Math.abs(v-x)<1e-9;case '!=':return Math.abs(v-x)>=1e-9;}return true;}
  function nuevo(){
    var pasos=Math.floor((cfg.max-cfg.min)/cfg.paso+1e-9);
    secreto=cfg.min+Math.floor(Math.random()*(pasos+1))*cfg.paso;intentos=0;
    if(cont)cont.textContent='0';res.textContent='';filas.forEach(function(f){f.classList.remove('a-toma');});fb(r,null,'');
  }
  function probar(){
    if(inp.value===''){fb(r,false,'Escribe un número.');return;}
    var v=Number(inp.value);if(isNaN(v)){fb(r,false,'Escribe un número.');return;}
    lvar.textContent=cfg.variable+' = '+inp.value;
    var k=cfg.ramas.findIndex(function(rm){return rm.op==='else'||cumple(v,rm.op,rm.valor==='secreto'?secreto:rm.valor);});
    filas.forEach(function(f){f.classList.toggle('a-toma',Number(f.dataset.rama)===k);});
    res.textContent=cfg.ramas[k].mensaje;
    if(!cfg.secreto){vistas[k]=1;if(Object.keys(vistas).length>=filas.length)gana(r);}
    if(cfg.secreto){
      intentos++;cont.textContent=intentos;
      var gano=cfg.ramas[k].op==='=='&&cfg.ramas[k].valor==='secreto';
      if(gano&&gana(r))fb(r,true,'¡Adivinaste en '+intentos+(intentos===1?' intento!':' intentos!'));else fb(r,null,'');
    }
  }
  if(inp.type==='range')on(inp,'input',probar);
  on(ver(r,'[data-probar]'),'click',probar);
  on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();probar();}});
  on(ver(r,'[data-nuevo]'),'click',nuevo);
  if(cfg.secreto)nuevo();else probar();
};
""",
    "ppt": r"""
M.ppt=function(r){
  var OP=['piedra','papel','tijera'],MANO={piedra:'✊',papel:'✋',tijera:'✌'};
  var filas=todos(r,'[data-rama]'),res=ver(r,'[data-res]'),m={yo:0,pc:0,emp:0};
  var lyo=ver(r,'[data-yo]'),lpc=ver(r,'[data-pc]'),btns=todos(r,'[data-jugada]');
  var manoYo=ver(r,'[data-mano=yo]'),manoPc=ver(r,'[data-mano=pc]');
  var nomYo=ver(r,'[data-nom=yo]'),nomPc=ver(r,'[data-nom=pc]');
  var ladoPc=ver(r,'[data-lado=pc]'),ops=todos(r,'[data-op]'),reloj=null;

  function mira(cual){ops.forEach(function(o){o.classList.toggle('a-mira',o.dataset.op===cual);});}
  function parar(){clearTimeout(reloj);reloj=null;ladoPc.classList.remove('a-sortea');btns.forEach(function(b){b.disabled=false;});}

  /* La gracia del juego es ver que la máquina ELIGE: la mano de la compu pasa
     por las tres mientras se enciende, en la lista de arriba, la que está
     mirando. Eso es random.choice(opciones) en vivo. */
  function sortear(pc, fin){
    var i=0,vueltas=QUIETO?0:7;
    ladoPc.classList.add('a-sortea');
    (function paso(){
      if(i>=vueltas){
        manoPc.textContent=MANO[pc];nomPc.textContent=pc;mira(pc);
        ladoPc.classList.remove('a-sortea');
        reloj=setTimeout(function(){mira(null);fin();},180);
        return;
      }
      var cual=OP[i%3];
      manoPc.textContent=MANO[cual];nomPc.textContent=cual;mira(cual);
      i++;reloj=setTimeout(paso,i>vueltas-3?130:70);
    })();
  }

  btns.forEach(function(b){on(b,'click',function(){
    if(reloj)return;
    var yo=b.dataset.jugada,pc=OP[Math.floor(Math.random()*3)];
    btns.forEach(function(x){x.disabled=true;});
    manoYo.textContent=MANO[yo];nomYo.textContent=yo;
    lyo.textContent='yo = "'+yo+'"';
    lpc.textContent='pc = random.choice(opciones)';
    res.textContent='';res.removeAttribute('data-r');
    filas.forEach(function(f){f.classList.remove('a-toma');});
    sortear(pc,function(){
      lpc.textContent='pc = random.choice(opciones)   # "'+pc+'"';
      var k=yo===pc?0:(yo==='piedra'&&pc==='tijera')?1:(yo==='papel'&&pc==='piedra')?2:(yo==='tijera'&&pc==='papel')?3:4;
      filas.forEach(function(f){f.classList.toggle('a-toma',Number(f.dataset.rama)===k);});
      res.textContent=['Empate','¡Ganaste!','¡Ganaste!','¡Ganaste!','Gana la computadora'][k];
      res.dataset.r=k===0?'empate':(k===4?'pierde':'gana');
      if(k>0&&k<4)gana(r);
      if(k===0)m.emp++;else if(k===4)m.pc++;else m.yo++;
      todos(r,'[data-m]').forEach(function(x){x.textContent=m[x.dataset.m];});
      parar();
    });
  });});
  pausas.push(parar);
};
""",
    "bucle": r"""
M.bucle=function(r){
  var tr=JSON.parse(r.dataset.traza),cuerpo=ver(r,'tbody'),res=ver(r,'[data-res]'),bs=ver(r,'[data-sig]'),bt=ver(r,'[data-todo]');
  var cab=ver(r,'[data-cab]'),k=0,reloj=null,ap=ver(r,'[data-apuesta]');
  if(ap){
    // Hasta que no apuesten, la traza no se mueve: primero se piensa.
    bs.disabled=true;bt.disabled=true;
    todos(ap,'[data-ap]').forEach(function(b){on(b,'click',function(){
      var bien=b.hasAttribute('data-ok');
      todos(ap,'[data-ap]').forEach(function(x){
        x.disabled=true;x.dataset.estado=x.hasAttribute('data-ok')?'bien':(x===b?'mal':'');
      });
      bs.disabled=false;bt.disabled=false;
      fb(r,bien,bien?'¡Esa! Ahora míralo vuelta por vuelta.':'Todavía no. Córrelo y mira dónde se te fue.');
    });});
  }
  function fin(){bs.disabled=true;bt.disabled=true;res.textContent=tr.final;
    gana(r)&&fb(r,true,'El bucle dio '+tr.filas.length+(tr.filas.length===1?' vuelta.':' vueltas.'));}
  function sig(){
    if(k>=tr.filas.length){fin();return false;}
    var t=tr.filas[k++],fila=document.createElement('tr');
    [t.vuelta,t['var'],t.acum].forEach(function(x){var td=document.createElement('td');td.textContent=x;fila.appendChild(td);});
    cuerpo.appendChild(fila);
    cab.classList.add('a-toma');setTimeout(function(){cab.classList.remove('a-toma');},QUIETO?0:220);
    if(k>=tr.filas.length)fin();
    return true;
  }
  function reiniciar(){clearInterval(reloj);reloj=null;k=0;cuerpo.innerHTML='';bs.disabled=false;bt.disabled=false;res.textContent='';fb(r,null,'');}
  on(bs,'click',sig);
  on(bt,'click',function(){bt.disabled=true;bs.disabled=true;reloj=setInterval(function(){if(!sig()||k>=tr.filas.length){clearInterval(reloj);reloj=null;}},QUIETO?40:380);});
  on(ver(r,'[data-reiniciar]'),'click',reiniciar);
  pausas.push(function(){if(reloj){clearInterval(reloj);reloj=null;if(k<tr.filas.length){bs.disabled=false;bt.disabled=false;}}});
};
""",
    "lista": r"""
M.lista=function(r){
  var usadas={};
  var cfg=JSON.parse(r.dataset.cfg),n=cfg.nombre,dic=cfg.modo==='dict',datos,ultimo=-1;
  var caja=ver(r,'[data-cajas]'),sal=ver(r,'[data-salida]'),selV=ver(r,'[data-val]'),inI=ver(r,'[data-idx]'),inK=ver(r,'[data-key]');
  function empezar(){datos=JSON.parse(JSON.stringify(cfg.inicial));ultimo=-1;}
  function pintar(){
    caja.innerHTML='';
    if(!datos.length){var v=document.createElement('span');v.className='a-lista-vacia';v.textContent=dic?'{}  (vacío)':'[]  (vacía)';caja.appendChild(v);return;}
    datos.forEach(function(it,k){
      var d=document.createElement('div');d.className='a-cl'+(k===ultimo?' a-nuevo':'');d.innerHTML='<i></i><b></b>';
      d.children[0].textContent=dic?P.repr(it[0]):String(k);d.children[1].textContent=P.repr(dic?it[1]:it);caja.appendChild(d);
    });
  }
  function valor(){return cfg.valores[Number(selV?selV.value:0)];}
  function salida(l,res,err){sal.textContent='>>> '+l+(res!==undefined?'\n'+res:'');sal.classList.toggle('a-err',!!err);}
  todos(r,'[data-op]').forEach(function(b){on(b,'click',function(){
    var op=b.dataset.op,l='';ultimo=-1;
    usadas[op]=1;if(Object.keys(usadas).length>=Math.min(4,todos(r,'[data-op]').length))gana(r);
    try{
      if(!dic){
        if(op==='append'){var v=valor();l=n+'.append('+P.repr(v)+')';datos.push(v);ultimo=datos.length-1;salida(l);}
        else if(op==='pop'){l=n+'.pop()';if(!datos.length)throw P.err('IndexError','pop from empty list');salida(l,P.repr(datos.pop()));}
        else if(op==='len'){l='len('+n+')';salida(l,String(datos.length));}
        else if(op==='indice'){var i=parseInt(inI.value,10);if(isNaN(i))i=0;l=n+'['+i+']';var j=i<0?datos.length+i:i;
          if(j<0||j>=datos.length)throw P.err('IndexError','list index out of range');ultimo=j;salida(l,P.repr(datos[j]));}
        else if(op==='in'){var v2=valor();l=P.repr(v2)+' in '+n;salida(l,datos.some(function(x){return P.eq(x,v2);})?'True':'False');}
      }else{
        var k=['str',inK.value],pos=datos.findIndex(function(p){return P.eq(p[0],k);});
        if(op==='get'){l=n+'['+P.repr(k)+']';if(pos<0)throw P.err('KeyError',P.repr(k));ultimo=pos;salida(l,P.repr(datos[pos][1]));}
        else if(op==='set'){var v3=valor();l=n+'['+P.repr(k)+'] = '+P.repr(v3);if(pos<0){datos.push([k,v3]);ultimo=datos.length-1;}else{datos[pos][1]=v3;ultimo=pos;}salida(l);}
        else if(op==='del'){l='del '+n+'['+P.repr(k)+']';if(pos<0)throw P.err('KeyError',P.repr(k));datos.splice(pos,1);salida(l);}
        else if(op==='len'){l='len('+n+')';salida(l,String(datos.length));}
        else if(op==='in'){l=P.repr(k)+' in '+n;salida(l,pos>=0?'True':'False');}
      }
      pintar();
    }catch(e){if(e.py){salida(l,e.py,true);pintar();}else throw e;}
  });});
  on(ver(r,'[data-reiniciar]'),'click',function(){empezar();pintar();salida('');});
  empezar();pintar();
};
""",
    "aventura": r"""
M.aventura=function(r){
  var cfg=JSON.parse(r.dataset.cfg),cab=ver(r,'[data-cab]'),txt=ver(r,'[data-txt]'),ops=ver(r,'[data-ops]'),ras=ver(r,'[data-rastro]'),camino=[];
  function ir(nombre){
    camino.push(nombre+'()');var s=cfg.salas[nombre];
    cab.textContent='def '+nombre+'():';txt.textContent=s.texto;ops.innerHTML='';ras.textContent=camino.join(' → ');
    if(!s.opciones.length){gana(r)&&fb(r,true,'Fin de la aventura: llegaste a '+nombre+'() en '+camino.length+' pasos.');return;}
    fb(r,null,'');
    s.opciones.forEach(function(o,k){
      var b=document.createElement('button');b.type='button';b.className='a-op';
      b.innerHTML='<span class="a-letra"></span><span></span><small></small>';
      b.children[0].textContent=String.fromCharCode(65+k);b.children[1].textContent=o[0];b.children[2].textContent=o[1]+'()';
      b.addEventListener('click',function(){ir(o[1]);},SEN);ops.appendChild(b);
    });
  }
  on(ver(r,'[data-reiniciar]'),'click',function(){camino=[];ir(cfg.inicio);});
  ir(cfg.inicio);
};
""",
    "caza": r"""
M.caza=function(r){
  var cfg=JSON.parse(r.dataset.cfg),n=cfg.nombre;
  var fila=ver(r,'[data-fila]'),preg=ver(r,'[data-preg]'),nums=ver(r,'[data-nums]');
  var pEl=ver(r,'[data-pts]'),rEl=ver(r,'[data-racha]'),roEl=ver(r,'[data-ronda]'),bOtra=ver(r,'[data-reiniciar]');
  // El plan es siempre el mismo para que la clase sepa qué viene; lo que
  // cambia en cada partida es a cuál de la fila apunta.
  var PLAN=['cual','donde','len','cual','cual','ultimo','donde','len'];
  var lista,ronda,pts,racha,actual,espera=null;
  function cita(x){return "'"+String(x)+"'";}
  function azar(m){return Math.floor(Math.random()*m);}

  function tarjetas(){
    fila.innerHTML='';
    lista.forEach(function(x,i){
      var b=document.createElement('button');b.type='button';b.className='a-caza-c';
      b.innerHTML='<span></span><i></i>';
      b.children[0].textContent=cita(x);b.children[1].textContent=i;
      b.addEventListener('click',function(){responder(i,b);},SEN);
      fila.appendChild(b);
    });
  }
  function chips(hasta){
    nums.innerHTML='';nums.hidden=false;
    for(var i=0;i<=hasta;i++)(function(v){
      var b=document.createElement('button');b.type='button';b.className='a-caza-n';b.textContent=v;
      b.addEventListener('click',function(){responder(v,b);},SEN);nums.appendChild(b);
    })(i);
  }
  function bloquear(si){
    todos(r,'.a-caza-c,.a-caza-n').forEach(function(b){b.disabled=si;});
  }

  function plantear(){
    r.dataset.ver='0';nums.hidden=true;nums.innerHTML='';
    todos(r,'.a-caza-c,.a-caza-n').forEach(function(b){b.removeAttribute('data-estado');});
    roEl.textContent=ronda+1;
    var tipo=PLAN[ronda%PLAN.length],i;
    if(tipo==='cual'){
      i=azar(lista.length);
      actual={tipo:tipo,donde:'fila',ok:i};
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'['+i+']</code> \u00b7 toca la que sale.';
    }else if(tipo==='ultimo'){
      actual={tipo:tipo,donde:'fila',ok:lista.length-1};
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'[-1]</code> \u00b7 toca la que sale.';
    }else if(tipo==='donde'){
      i=azar(lista.length);
      actual={tipo:tipo,donde:'nums',ok:i};
      preg.innerHTML='\u00bfEn qu\u00e9 posici\u00f3n est\u00e1 <code>'+cita(lista[i])+'</code>?';
      chips(lista.length);
    }else{
      actual={tipo:tipo,donde:'nums',ok:lista.length};
      preg.innerHTML='<code>&gt;&gt;&gt; len('+n+')</code> \u00b7 toca el n\u00famero.';
      chips(lista.length);
    }
    bloquear(false);
  }

  function explica(){
    var i=actual.ok,u=lista.length-1;
    if(actual.tipo==='cual')
      return n+'['+i+'] es la '+(i+1)+'\u00aa: se cuenta '+lista.map(function(_,k){return k;}).slice(0,i+1).join(', ')+'.';
    if(actual.tipo==='ultimo')
      return 'La \u00faltima es '+n+'['+u+'], porque hay '+lista.length+' y se empieza en 0.';
    if(actual.tipo==='donde')
      return cita(lista[i])+' est\u00e1 en la posici\u00f3n '+i
        +(i===0?': es la primera, antes no hay ninguna.':': antes hay '+(i===1?'una':i)+'.');
    return 'Hay '+lista.length+', as\u00ed que len da '+lista.length+'. La \u00faltima es '+n+'['+u+'].';
  }

  function responder(v,b){
    if(espera)return;
    bloquear(true);r.dataset.ver='1';
    var ok=v===actual.ok;
    b.setAttribute('data-estado',ok?'bien':'mal');
    if(!ok){
      var caja=actual.donde==='fila'?fila:nums;
      var buena=todos(caja,'button')[actual.ok];
      if(buena)buena.setAttribute('data-estado','bien');
    }
    if(ok){pts++;racha++;}else{racha=0;}
    pEl.textContent=pts;rEl.textContent=racha;
    fb(r,ok,(ok?'\u00a1Bien! ':'')+explica());
    espera=setTimeout(function(){espera=null;ronda++;siguiente();},QUIETO?300:1500);
  }

  function siguiente(){
    if(ronda>=cfg.rondas){
      // La fila se queda a la vista con los n\u00fameros puestos: lo \u00faltimo que
      // ven es la lista entera numerada, que es lo que hay que recordar.
      nums.hidden=true;preg.textContent='';
      r.dataset.ver='1';bloquear(true);bOtra.hidden=false;
      if(pts>=cfg.gana){gana(r);fb(r,true,'\u00a1Cazadas! '+pts+' de '+cfg.rondas+'.');}
      else fb(r,false,pts+' de '+cfg.rondas+'. Con '+cfg.gana+' se gana: otra vuelta.');
      return;
    }
    // A mitad de partida entra una m\u00e1s: se ve que las posiciones corren.
    if(ronda===Math.floor(cfg.rondas/2)&&cfg.extra.length){
      lista.push(cfg.extra.shift());
      tarjetas();r.dataset.ver='1';
      preg.innerHTML='<code>&gt;&gt;&gt; '+n+'.append('+cita(lista[lista.length-1])+')</code>';
      nums.hidden=true;bloquear(true);
      espera=setTimeout(function(){espera=null;plantear();},QUIETO?300:1600);
      return;
    }
    plantear();
  }

  function empezar(){
    clearTimeout(espera);espera=null;
    cfg=JSON.parse(r.dataset.cfg);
    lista=cfg.inicial.slice();ronda=0;pts=0;racha=0;
    pEl.textContent='0';rEl.textContent='0';bOtra.hidden=true;fb(r,null,'');
    tarjetas();plantear();
  }
  on(bOtra,'click',empezar);
  pausas.push(function(){clearTimeout(espera);espera=null;});
  if(SEN.signal)SEN.signal.addEventListener('abort',function(){clearTimeout(espera);});
  empezar();
};
""",
    "carrera": r"""
M.carrera=function(r){
  var cfg=JSON.parse(r.dataset.cfg),Q=cfg.preguntas,bIni=ver(r,'[data-empezar]'),zona=ver(r,'[data-zona]'),pr=ver(r,'[data-preg]');
  var ops=ver(r,'[data-ops]'),tEl=ver(r,'[data-t]'),pEl=ver(r,'[data-pts]'),rEl=ver(r,'[data-racha]');
  var t=null,resta=0,pts=0,racha=0,mejor=0,cola=[],actual=null;
  function barajar(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),x=a[i];a[i]=a[j];a[j]=x;}return a;}
  function sig(){
    if(!cola.length)cola=barajar(Q.map(function(_,k){return k;}));
    actual=Q[cola.pop()];pr.textContent=actual.pregunta;ops.innerHTML='';
    barajar(actual.opciones.map(function(_,k){return k;})).forEach(function(k,pos){
      var b=document.createElement('button');b.type='button';b.className='a-op';b.innerHTML='<span class="a-letra"></span><span></span>';
      b.children[0].textContent='ABCD'[pos];b.children[1].textContent=actual.opciones[k];
      b.addEventListener('click',function(){responder(k===actual.correcta,b);},SEN);ops.appendChild(b);
    });
  }
  function responder(ok,b){
    if(!t)return;todos(ops,'button').forEach(function(x){x.disabled=true;});b.setAttribute('data-estado',ok?'bien':'mal');
    if(ok){pts++;racha++;mejor=Math.max(mejor,racha);fb(r,true,'¡Bien! Racha de '+racha+'.');}else{racha=0;fb(r,false,'Esa no era.');}
    pEl.textContent=pts;rEl.textContent=racha;setTimeout(function(){if(t)sig();},QUIETO?150:650);
  }
  function detener(texto){clearInterval(t);t=null;zona.hidden=true;bIni.hidden=false;bIni.textContent=texto;}
  on(bIni,'click',function(){
    pts=0;racha=0;mejor=0;pEl.textContent='0';rEl.textContent='0';resta=cfg.segundos;tEl.textContent=resta;cola=[];
    zona.hidden=false;bIni.hidden=true;fb(r,null,'');
    t=setInterval(function(){resta--;tEl.textContent=resta;if(resta<=0){detener('▶ Otra carrera');
      (pts>=Math.ceil(Q.length/2)&&gana(r)),fb(r,true,'¡Tiempo! '+pts+(pts===1?' acierto':' aciertos')+' · mejor racha: '+mejor+'.');}},1000);
    sig();
  });
  pausas.push(function(){if(t)detener('▶ Empezar la carrera');});
};
""",
})


# ── css: deslizadores que escriben CSS en vivo ───────────────────────────────

def juego_css(j, ctx):
    controles, reglas = [], []
    for c in j["controles"]:
        prop = c["prop"]
        if c["tipo"] == "slider":
            ini = round((c["min"] + c["max"]) / 2)
            valor = f'{ini}{c["unidad"]}'
            control = (f'<input type="range" data-prop="{A(prop)}" data-unidad="{A(c["unidad"])}" '
                       f'min="{c["min"]}" max="{c["max"]}" value="{ini}" aria-label="{A(prop)}">')
        else:
            valor = c["valores"][0]
            opc = "".join(f'<option>{E(v)}</option>' for v in c["valores"])
            control = f'<select class="campo" data-prop="{A(prop)}" aria-label="{A(prop)}">{opc}</select>'
        reglas.append((prop, valor))
        controles.append(f'<label class="a-css-ctl"><code>{E(prop)}</code>{control}<output data-out="{A(prop)}">{E(valor)}</output></label>')
    estilo = ";".join(f"{p}:{v}" for p, v in reglas)
    hijos = "".join(f'<div class="a-css-hijo">{k + 1}</div>' for k in range(j["hijos"]))
    return f"""<div class="a-css" data-act="css">
      <div class="a-col">{"".join(controles)}
        <pre class="a-salida a-css-codigo" data-codigo></pre>
      </div>
      <div class="a-css-vista" data-vista style="{A(estilo)}">{hijos}</div>
    </div>"""


MOTORES_HTML["css"] = juego_css

CSS_MOTOR["css"] = _CSS_COL + """
.a-css{display:grid;gap:18px;margin-top:14px}
@media(min-width:980px){.a-css{grid-template-columns:.9fr 1.1fr;align-items:start}}
.a-css-ctl{display:grid;grid-template-columns:150px 1fr 70px;gap:10px;align-items:center;font-size:14px}
.a-css-ctl code{font-family:var(--fm);color:var(--tx2)}
.a-css-ctl input[type=range]{width:100%;accent-color:var(--lvl);min-height:36px}
.a-css-ctl output{font-family:var(--fm);color:var(--lvl);text-align:right}
.a-css-ctl .campo{min-height:40px}
.a-css-codigo{color:#D7DEEC}
.a-css-vista{display:flex;min-height:260px;background:#fff;border:1px solid var(--line);border-radius:8px;
  color:#1e293b;overflow:auto;transition:all .2s}
.a-css-hijo{display:grid;place-items:center;min-width:56px;min-height:56px;border-radius:8px;background:#6366f1;
  color:#fff;font-family:var(--fd);font-weight:800;font-size:20px}
@media(max-width:640px){.a-css-ctl{grid-template-columns:1fr 70px}.a-css-ctl code{grid-column:1/-1}}
"""

JS_MOTOR["css"] = r"""
M.css=function(r){
  var vista=ver(r,'[data-vista]'),cod=ver(r,'[data-codigo]'),ctls=todos(r,'[data-prop]'),ini=vista.getAttribute('style');
  function valor(c){return c.tagName==='SELECT'?c.value:c.value+c.dataset.unidad;}
  function pintar(){
    var lineas=ctls.map(function(c){var v=valor(c);vista.style.setProperty(c.dataset.prop,v);
      var o=ver(r,'[data-out="'+c.dataset.prop+'"]');if(o)o.textContent=v;return '  '+c.dataset.prop+': '+v+';';});
    cod.textContent='.caja {\n  display: flex;\n'+lineas.join('\n')+'\n}';
  }
  var tocados={};
  ctls.forEach(function(c){
    function t(){tocados[c.dataset.prop]=1;pintar();if(Object.keys(tocados).length>=ctls.length)gana(r);}
    on(c,'input',t);on(c,'change',t);
  });
  pintar();
};
"""


# ── Teoría: tres diapositivas cortas antes del ejemplo y los retos ──────────

def diapositivas_teoria(te, nid, n, mins=("4 – 6", "6 – 8", "8 – 10")):
    """La idea, sus partes y una pregunta para comprobar. Devuelve
    (diapositivas, usa_escena). Sin teoría para esa semana, no añade nada."""
    if not te:
        return [], False
    idea, partes, comp = te["idea"], te["partes"], te["compruebo"]
    s1 = slide("Teoría · La idea", mins[0],
               f'<h2 class="a-teo-titulo">{E(idea["titulo"])}</h2>'
               f'<p class="a-teo-texto">{E(idea["texto"])}</p>'
               f'<div class="a-teo-ejemplo"><p class="a-etq">En la vida real</p><p>{E(idea["ejemplo"])}</p></div>',
               "Todos · escuchamos")
    ejemplos = partes.get("ejemplos")
    esc = escena(partes["escena"], nid) if partes.get("escena") and not ejemplos else ""
    lista = "".join(f"<li><b>{E(nom)}</b><span>{E(txt)}</span></li>" for nom, txt in partes["puntos"])
    if ejemplos:
        # Mejor que un dibujo: líneas bien escritas, para copiar el patrón.
        cod = "".join(f"<li><code>{E(x)}</code></li>" for x in ejemplos)
        lado = f'<div class="a-teo-ejemplos"><p class="a-etq">Así se escriben ✓</p><ol class="a-teo-cod">{cod}</ol></div>'
    else:
        lado = f'<div class="a-escena">{esc}</div>' if esc else ""
    clase = "a-teo-partes con-escena" if lado else "a-teo-partes"
    s2 = slide("Teoría · Las partes", mins[1],
               f'<h2 class="a-titulo">{E(partes["titulo"])}</h2>'
               f'<div class="{clase}"><ol class="a-teo-lista">{lista}</ol>{lado}</div>')
    ops = comp["opciones"]
    botones = "".join(
        f'<button type="button" class="a-op" data-txt="{A(ops[i])}"{" data-ok" if i == comp["correcta"] else ""}>'
        f'<span class="a-letra">{LETRAS[k]}</span><span>{E(ops[i])}</span></button>'
        for k, i in enumerate(orden(len(ops), f"{nid}:{n}:teoria", distinto=False)))
    s3 = slide("Teoría · ¿Lo entendí?", mins[2],
               f'<h2 class="a-titulo">{E(comp["pregunta"])}</h2>'
               f'<div class="a-panel a-teo-check" data-act="opciones"><div class="a-ops">{botones}</div>{FB}'
               f'<p class="a-explica" hidden>{E(comp["por_que"])}</p>'
               f'<div class="a-acc"><button type="button" class="a-btn a-sec" data-reintentar hidden>Reintentar</button></div></div>',
               "Tú solo · en tu compu")
    return [s1, s2, s3], bool(esc)


CSS_TEORIA = """
/* teoría */
.a-teo-titulo{font-size:clamp(34px,6vw,76px);max-width:18ch}
.a-teo-texto{margin-top:18px;font-size:clamp(20px,2.8vw,34px);line-height:1.3;max-width:34ch;color:var(--tx)}
.a-teo-ejemplo{margin-top:26px;max-width:62ch;padding:clamp(14px,2vw,22px);background:var(--bg2);
  border:1px solid var(--line);border-left:4px solid var(--sand);border-radius:6px}
.a-teo-ejemplo .a-etq{color:var(--sand);margin-bottom:8px}
.a-teo-ejemplo p:last-child{font-size:clamp(16px,2vw,23px);color:var(--tx2);line-height:1.45}
.a-teo-partes{display:grid;gap:24px;margin-top:20px;align-items:center}
@media(min-width:980px){.a-teo-partes.con-escena{grid-template-columns:1.25fr .75fr}}
.a-teo-lista{list-style:none;counter-reset:t;margin:0;padding:0;display:grid;gap:12px}
.a-teo-lista li{counter-increment:t;display:grid;grid-template-columns:48px 1fr;column-gap:14px;row-gap:3px;
  align-items:start;padding:14px 16px;background:var(--bg2);border:1px solid var(--line);border-radius:8px}
.a-teo-lista li::before{content:counter(t);grid-row:1/3;display:grid;place-items:center;width:44px;height:44px;
  border-radius:99px;background:var(--lvl);color:var(--bg);font-family:var(--fd);font-weight:800;font-size:22px}
.a-teo-lista b{font-family:var(--fd);font-size:clamp(18px,2.2vw,26px)}
.a-teo-lista span{color:var(--tx2);font-size:clamp(14px,1.6vw,19px);line-height:1.4}
.a-teo-check{max-width:760px;margin-top:14px}
.a-teo-check .a-op{min-height:56px;font-size:clamp(15px,1.8vw,20px)}
"""


# ── portada: las tres capas de la web, una tarjeta por capa ────────────────

CAPAS_PORTADA = [("html", "HTML", "la estructura: qué hay"),
                 ("css", "CSS", "el estilo: cómo se ve"),
                 ("py", "Python", "el comportamiento: qué hace")]


def juego_portada(j, ctx):
    grupos = []
    for capa, nombre, sub in CAPAS_PORTADA:
        cartas = j["cartas"][capa]
        botones = "".join(
            f'<button type="button" class="a-pt-carta" data-carta="{A(cartas[i]["id"])}" aria-pressed="false">'
            f'<code>{E(cartas[i]["codigo"])}</code></button>'
            for i in orden(len(cartas), f'{ctx["nid"]}:{ctx["n"]}:portada:{capa}', distinto=False))
        grupos.append(f'<div class="a-pt-capa" data-capa="{capa}"><p class="a-etq">{E(nombre)} · {E(sub)}</p>'
                      f'<div class="a-pt-cartas">{botones}</div></div>')
    cfg = {"cartas": j["cartas"], "misiones": j["misiones"]}
    return f"""<div class="a-portada-j" data-act="portada" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        <div class="a-pt-mision"><p class="a-etq" data-num></p><p class="a-pt-texto" data-texto></p></div>
        {"".join(grupos)}
        <div class="a-acc"><button type="button" class="a-btn" data-publicar>▶ Publicar</button>
          <button type="button" class="a-btn a-sec" data-limpiar>Quitar tarjetas</button></div>
      </div>
      <div class="a-col">
      <div class="a-pt-nav">
        <div class="a-pt-barra"><i></i><i></i><i></i><span>eldiariohdn.do</span></div>
        <div class="a-pt-pagina" data-pagina>
          <p class="a-pt-diario">EL DIARIO DEL CENTRO</p>
          <div class="a-pt-titular" data-titular>Titular aburrido</div>
          <p class="a-pt-bajada">Noticias de la escuela, hechas por 2do.</p>
          <button type="button" class="a-pt-boton" data-boton>Última hora</button>
          <p class="a-pt-nota" data-aviso hidden>Toca el botón de la portada.</p>
        </div>
      </div>
      <ul class="a-pt-res" data-res></ul>
      {FB}
      <div class="a-acc"><button type="button" class="a-btn" data-sig hidden>Siguiente misión →</button>
        <button type="button" class="a-btn a-sec" data-otra hidden>Empezar otra vez</button></div>
      </div>
    </div>"""


MOTORES_HTML["portada"] = juego_portada

CSS_MOTOR["portada"] = _CSS_COL + """
.a-portada-j{display:grid;gap:18px;margin-top:10px}
.a-portada-j .a-col{gap:9px}
@media(min-width:980px){.a-portada-j{grid-template-columns:1.3fr .7fr;align-items:start}}
.a-pt-mision{padding:9px 14px;background:var(--bg2);border:1px solid var(--line);border-left:4px solid var(--lvl);border-radius:6px}
.a-pt-texto{font-family:var(--fd);font-weight:700;font-size:clamp(15px,1.6vw,19px);line-height:1.3;margin-top:3px}
.a-pt-capa{display:grid;gap:4px;transition:opacity .2s}
.a-pt-capa.a-pt-opcional{opacity:.5}
.a-pt-cartas{display:flex;flex-wrap:wrap;gap:6px}
.a-pt-carta{min-height:40px;padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:#0B1020;
  color:#D7DEEC;cursor:pointer;text-align:left;touch-action:manipulation}
.a-pt-carta code{font-family:var(--fm);font-size:clamp(11px,1.05vw,12.5px)}
.a-pt-carta[aria-pressed="true"]{border-color:var(--lvl);box-shadow:0 0 0 2px var(--lvl)}
.a-pt-carta:focus-visible,.a-pt-boton:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-pt-res{list-style:none;margin:0;padding:0;display:grid;gap:3px;font-size:clamp(12.5px,1.25vw,15px);font-weight:600}
.a-pt-res .a-bien{color:var(--a-ok)}
.a-pt-res .a-mal{color:var(--a-ko)}
.a-pt-nav{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;box-shadow:0 20px 50px -30px rgba(0,0,0,.6)}
.a-pt-barra{display:flex;gap:5px;align-items:center;padding:8px 10px;background:#E7EAF0;font-family:var(--fm);font-size:11px;color:#5A6474}
.a-pt-barra i{width:9px;height:9px;border-radius:99px;background:#B8C0CE}
.a-pt-barra span{margin-left:8px}
.a-pt-pagina{min-height:230px;padding:16px 18px;background:#fff;color:#0f172a;display:grid;align-content:start;gap:12px;
  transition:background .45s,color .45s}
.a-pt-pagina[data-paso]{animation:a-pt-flash .6s}
@keyframes a-pt-flash{from{box-shadow:inset 0 0 0 4px var(--lvl)}to{box-shadow:inset 0 0 0 0 transparent}}
.a-pt-diario{font-family:Georgia,serif;font-weight:700;letter-spacing:.2em;font-size:12px;border-bottom:2px solid currentColor;
  padding-bottom:6px;margin:0}
.a-pt-titular{font-family:Georgia,serif;font-weight:800;font-size:clamp(22px,2.4vw,32px);line-height:1.1}
.a-pt-titular.a-pt-chico{font-size:15px;font-weight:400;font-family:inherit}
.a-pt-bajada{margin:0;opacity:.75;font-size:14px}
.a-pt-boton{justify-self:start;min-height:42px;padding:8px 18px;border-radius:999px;border:0;background:#dc2626;color:#fff;
  font-weight:700;cursor:pointer;touch-action:manipulation}
.a-pt-nota{margin:0;font-size:12.5px;opacity:.7}
@media (prefers-reduced-motion: reduce){.a-pt-pagina{transition:none}.a-pt-pagina[data-paso]{animation:none}}
"""

JS_MOTOR["portada"] = r"""
M.portada=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,corre=null,alTocar=null;
  var sel={html:null,css:null,py:null},NOM={html:'HTML',css:'CSS',py:'Python'};
  var pag=ver(r,'[data-pagina]'),tit=ver(r,'[data-titular]'),bot=ver(r,'[data-boton]'),res=ver(r,'[data-res]');
  var bPub=ver(r,'[data-publicar]'),bSig=ver(r,'[data-sig]'),bOtra=ver(r,'[data-otra]'),nota=ver(r,'[data-aviso]');
  function carta(c,id){return cfg.cartas[c].filter(function(x){return x.id===id;})[0]||null;}
  function pagina(){
    tit.textContent='Titular aburrido';tit.className='a-pt-titular';
    pag.style.background='';pag.style.color='';pag.removeAttribute('data-paso');alTocar=null;nota.hidden=true;
  }
  function mision(){
    var m=mis[k];
    ver(r,'[data-num]').textContent='Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-texto]').textContent=m.texto;
    todos(r,'[data-capa]').forEach(function(g){g.classList.toggle('a-pt-opcional',!m[g.dataset.capa]);});
  }
  function limpiar(){
    sel={html:null,css:null,py:null};
    todos(r,'.a-pt-carta').forEach(function(b){b.setAttribute('aria-pressed','false');});
  }
  function reiniciar(){
    if(corre){clearTimeout(corre);corre=null;}
    res.innerHTML='';fb(r,null,'');bSig.hidden=true;bOtra.hidden=true;bPub.disabled=false;pagina();
  }
  function fila(ok,texto){
    var li=document.createElement('li');li.className=ok?'a-bien':'a-mal';
    li.textContent=(ok?'✓ ':'✗ ')+texto;res.appendChild(li);
  }
  todos(r,'.a-pt-carta').forEach(function(b){on(b,'click',function(){
    if(corre)return;
    var g=b.closest('[data-capa]'),c=g.dataset.capa,ya=sel[c]===b.dataset.carta;
    sel[c]=ya?null:b.dataset.carta;
    todos(g,'.a-pt-carta').forEach(function(x){x.setAttribute('aria-pressed',String(!ya&&x===b));});
  });});
  on(bot,'click',function(){if(alTocar!==null)tit.textContent=alTocar;});
  on(bPub,'click',function(){
    reiniciar();bPub.disabled=true;
    var m=mis[k],capas=['html','css','py'],i=0,bien=true,vel=QUIETO?60:700;
    function paso(){
      if(i>=capas.length){
        corre=null;bPub.disabled=false;
        if(!bien)fb(r,false,'Cambia las tarjetas marcadas con ✗ y vuelve a publicar.');
        else if(k<mis.length-1){fb(r,true,'¡Misión cumplida!');bSig.hidden=false;}
        else{gana(r)&&fb(r,true,'¡Portada hackeada! Las tres capas funcionan juntas.');bOtra.hidden=false;}
        return;
      }
      var c=capas[i++],pide=m[c],x=sel[c]?carta(c,sel[c]):null;
      pag.removeAttribute('data-paso');void pag.offsetWidth;pag.setAttribute('data-paso',c);
      if(c==='html'&&x){tit.textContent=x.titular;tit.className='a-pt-titular'+(x.etiqueta==='p'?' a-pt-chico':'');}
      if(c==='css'&&x){pag.style.background=x.fondo||'';pag.style.color=x.letra||'';}
      if(c==='py'&&x){alTocar=x.al_tocar===undefined?null:x.al_tocar;nota.hidden=false;bot.click();}
      if(pide){
        var ok=sel[c]===pide;bien=bien&&ok;
        fila(ok,NOM[c]+': '+(x?(ok?'¡bien!':x.explica):'falta elegir una tarjeta'));
      }else if(x){
        fila(true,NOM[c]+': esta misión todavía no la pide');
      }
      corre=setTimeout(paso,vel);
    }
    corre=setTimeout(paso,QUIETO?0:250);
  });
  on(bSig,'click',function(){k++;limpiar();reiniciar();mision();});
  on(bOtra,'click',function(){k=0;limpiar();reiniciar();mision();});
  on(ver(r,'[data-limpiar]'),'click',function(){if(corre)return;limpiar();reiniciar();});
  pausas.push(function(){if(corre)reiniciar();});
  mision();pagina();
};
"""



# ── Chuleta para imprimir y sitios para seguir practicando ──────────────────

def chuleta_html(ch, nivel, n):
    filas = "".join(f'<li><code>{E(c)}</code><span>{E(t)}</span></li>' for c, t in ch["lineas"])
    return f"""<div class="a-chuleta" data-act="imprimir">
      <p class="a-ch-cab">{E(nivel["titulo"])} · Semana {n}</p>
      <h2 class="a-titulo">{E(ch["titulo"])}</h2>
      <ul class="a-ch-lista">{filas}</ul>
      <div class="a-acc a-ch-acc"><button type="button" class="a-btn" data-imprimir>🖨 Imprimir la chuleta</button></div>
    </div>"""


def recursos_html(rs):
    tarjetas = "".join(
        f'<a class="a-rec" href="{A(url)}" target="_blank" rel="noopener"><b>{E(nom)}</b>'
        f'<span>{E(txt)}</span><i>{E(url.split("//", 1)[-1].rstrip("/"))} ↗</i></a>'
        for nom, url, txt in rs)
    return f'<h2 class="a-titulo">Sigue practicando Python en casa</h2><div class="a-recs">{tarjetas}</div>'


CSS_EXTRAS = """
/* chuleta */
.a-chuleta{max-width:900px}
.a-ch-cab{font-family:var(--fm);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:0 0 6px}
.a-ch-lista{list-style:none;margin:16px 0;padding:0;display:grid;gap:8px}
.a-ch-lista li{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:16px;align-items:center;padding:10px 14px;
  background:var(--bg2);border:1px solid var(--line);border-radius:6px}
.a-ch-lista code{font-family:var(--fm);font-size:clamp(13px,1.45vw,17px);color:var(--lvl);white-space:pre-wrap}
.a-ch-lista span{color:var(--tx2);font-size:clamp(13px,1.4vw,16px);line-height:1.4}
@media(max-width:700px){.a-ch-lista li{grid-template-columns:1fr;gap:4px}}
@media print{
  .pg *{visibility:hidden}
  .a-chuleta,.a-chuleta *{visibility:visible}
  .a-chuleta{position:fixed;inset:0;max-width:none;padding:14mm;background:#fff;color:#000}
  .a-chuleta .a-titulo,.a-ch-cab{color:#000}
  .a-ch-lista li{background:#fff;border-color:#999}
  .a-ch-lista code{color:#000;font-weight:700}
  .a-ch-lista span{color:#222}
  .a-ch-acc{display:none!important}
}
/* recursos */
.a-recs{display:grid;gap:12px;margin-top:18px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.a-rec{display:grid;gap:6px;padding:16px 18px;border-radius:10px;background:var(--bg2);border:1px solid var(--line);
  border-top:3px solid var(--lvl);color:var(--tx);text-decoration:none;transition:border-color .16s,transform .16s}
.a-rec:hover{border-color:var(--lvl);transform:translateY(-2px)}
.a-rec:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-rec b{font-family:var(--fd);font-size:clamp(17px,2vw,22px)}
.a-rec span{color:var(--tx2);font-size:clamp(13px,1.4vw,16px);line-height:1.4}
.a-rec i{font-style:normal;font-family:var(--fm);font-size:12px;color:var(--lvl)}
"""



# ── Tu primera variable: dinámica en grupo y crearla en la pantalla ─────────



def juego_vueltas(j, ctx=None):
    """La fábrica de números: mueven los tres números de range hasta clavar
    la secuencia que les piden. Es la forma más corta de que range deje de
    ser magia: se ve al instante qué hace cada hueco."""
    cfg = {"rondas": j["rondas"]}
    return f"""<div class="a-vueltas" data-act="vueltas" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        <div class="a-mt-mision"><p class="a-etq" data-num></p>
          <p class="a-mt-pide">Haz que salga: <b data-meta></b></p>
          <p class="a-vu-pista" data-pista></p></div>
        <div class="a-vu-linea">
          <code>for n in range(</code>
          <label><span>desde</span><input class="campo" type="number" data-a value="0"></label>
          <code>,</code>
          <label><span>hasta</span><input class="campo" type="number" data-b value="5"></label>
          <code>,</code>
          <label><span>salto</span><input class="campo" type="number" data-p value="1"></label>
          <code>):</code>
        </div>
        <p class="a-vu-sale">Tu ciclo da: <b data-sale>—</b></p>
        <div class="a-acc"><button type="button" class="a-btn" data-probar>Probar</button>
          <button type="button" class="a-btn a-sec" data-reiniciar>Empezar de nuevo</button></div>
        {FB}
      </div>
      <div class="a-vu-marca"><p class="a-etq">Rondas</p><div class="a-vu-luces" data-luces></div></div>
    </div>"""


MOTORES_HTML["vueltas"] = juego_vueltas

CSS_MOTOR["vueltas"] = _CSS_COL + """
.a-vueltas{display:grid;gap:20px;margin-top:10px}
@media(min-width:980px){.a-vueltas{grid-template-columns:1.4fr .6fr;align-items:start}}
.a-vueltas .a-col{gap:10px}
.a-vu-pista{margin:6px 0 0;font-size:13.5px;color:var(--mut)}
.a-vu-linea{display:flex;flex-wrap:wrap;gap:8px;align-items:end;padding:12px 14px;background:#0B1020;
  border:1px solid var(--line);border-radius:8px;color:#D7DEEC;font-family:var(--fm);
  font-size:clamp(14px,1.6vw,19px)}
.a-vu-linea label{display:grid;gap:3px}
.a-vu-linea span{font-family:var(--fb);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.a-vu-linea input{width:5.5ch;min-height:44px;text-align:center;font-family:var(--fm);
  font-size:clamp(15px,1.7vw,20px)}
.a-vu-sale{margin:0;font-size:clamp(14px,1.5vw,18px);color:var(--tx2)}
.a-vu-sale b{font-family:var(--fm);color:var(--tx)}
.a-vu-luces{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.a-vu-luz{width:30px;height:30px;border-radius:50%;border:2px solid var(--line);display:grid;place-items:center;
  font-family:var(--fm);font-size:13px;color:var(--mut)}
.a-vu-luz.a-ok{border-color:var(--a-ok);color:var(--a-ok)}
.a-vu-luz.a-now{border-color:var(--lvl);color:var(--lvl);box-shadow:0 0 0 3px rgba(79,201,232,.18)}
"""

JS_MOTOR["vueltas"] = r"""
M.vueltas=function(r){
  var cfg=JSON.parse(r.dataset.cfg),rondas=cfg.rondas,k=0;
  var inA=ver(r,'[data-a]'),inB=ver(r,'[data-b]'),inP=ver(r,'[data-p]'),sale=ver(r,'[data-sale]');
  function lista(a){return a.length?a.join(', '):'nada';}
  function secuencia(){
    var a=parseInt(inA.value,10),b=parseInt(inB.value,10),p=parseInt(inP.value,10);
    if(isNaN(a)||isNaN(b)||isNaN(p)||p===0)return null;
    var out=[],x=a,tope=0;
    while((p>0?x<b:x>b)&&tope++<200){out.push(x);x+=p;}
    return out;
  }
  function verSalida(){
    var s=secuencia();
    sale.textContent=s===null?'— (el salto no puede ser 0)':lista(s);
  }
  function luces(){
    var caja=ver(r,'[data-luces]');caja.innerHTML='';
    rondas.forEach(function(_,i){
      var d=document.createElement('span');
      d.className='a-vu-luz'+(i<k?' a-ok':i===k?' a-now':'');
      d.textContent=i<k?'✓':String(i+1);caja.appendChild(d);
    });
  }
  function pintar(){
    var ro=rondas[Math.min(k,rondas.length-1)];
    ver(r,'[data-num]').textContent=k>=rondas.length?'¡Fábrica dominada!':'Ronda '+(k+1)+' de '+rondas.length;
    ver(r,'[data-meta]').textContent=k>=rondas.length?'ya está':lista(ro.objetivo);
    ver(r,'[data-pista]').textContent=k>=rondas.length?'':(ro.pista||'');
    ver(r,'[data-probar]').disabled=k>=rondas.length;
    [inA,inB,inP].forEach(function(x){x.disabled=k>=rondas.length;});
    luces();verSalida();
  }
  function probar(){
    if(k>=rondas.length)return;
    var s=secuencia(),meta=rondas[k].objetivo;
    if(s===null){fb(r,false,'El salto no puede ser 0: el ciclo no avanzaría nunca.');return;}
    if(!s.length){fb(r,false,'Así no da ninguna vuelta: con salto positivo, hasta tiene que ser mayor que desde.');return;}
    if(s.length===meta.length&&s.every(function(x,i){return x===meta[i];})){
      k++;
      if(k>=rondas.length){gana(r);fb(r,true,'¡Las cinco! range(desde, hasta, salto): el hasta nunca entra.');}
      else fb(r,true,'¡Clavado! Siguiente ronda.');
      pintar();return;
    }
    var p=[];
    if(s[0]!==meta[0])p.push('empieza en '+s[0]+' y debería empezar en '+meta[0]);
    if(s.length!==meta.length)p.push('da '+s.length+' números y hacen falta '+meta.length);
    else if(s.length>1&&(s[1]-s[0])!==(meta[1]-meta[0]))p.push('salta de '+(s[1]-s[0])+' en '+(s[1]-s[0]));
    fb(r,false,'Tu ciclo da '+lista(s)+(p.length?': '+p.join(' y ')+'.':'.'));
  }
  [inA,inB,inP].forEach(function(x){on(x,'input',verSalida);});
  on(ver(r,'[data-probar]'),'click',probar);
  on(ver(r,'[data-reiniciar]'),'click',function(){k=0;inA.value=0;inB.value=5;inP.value=1;fb(r,null,'');pintar();});
  pintar();
};
"""


# ─── La escalera de ciclos ───────────────────────────────────────────────
#
# Hermana de la montaña: allí se escribían variables, aquí se escribe la
# cabecera de un ciclo. La diferencia está en cómo se corrige: no se compara
# el texto, se **ejecuta el range** y se comparan los números que salen. Así
# vale cualquier forma correcta —range(1, 11) o range(1, 11, 1)— y el error
# se explica enseñando la secuencia que sí dio su línea.

def juego_escalera(pr):
    din, es = pr["dinamica"], pr["escalera"]
    n = len(es["misiones"])
    pasos = "".join(f"<li>{E(x)}</li>" for x in din["pasos"])
    escalones = "".join(f'<i class="a-es-escalon" style="--k:{k}"></i>' for k in range(1, n + 1))
    return f"""<div class="a-escalera" data-act="escalera" data-cfg="{_cfg({"misiones": es["misiones"]})}" style="--n:{n}">
      <div class="a-col">
        <details class="a-mt-din">
          <summary>Antes, en grupo · {E(din["titulo"])} · {din["minutos"]} min</summary>
          <ol>{pasos}</ol>
        </details>
        <div class="a-mt-mision"><p class="a-etq" data-num></p><p class="a-mt-pide" data-pide></p></div>
        <div class="a-mt-escribe">
          <input class="campo a-mt-in" data-linea autocomplete="off" spellcheck="false"
                 aria-label="Escribe la cabecera de tu ciclo" placeholder="for i in range(…):">
          <button type="button" class="a-btn" data-subir>Subir ▲</button>
        </div>
        <p class="a-mt-pista">Así se escribe: <code>for i in range(desde, hasta, salto):</code></p>
        <p class="a-es-sale" data-sale aria-live="polite"></p>
        {FB}
        <p class="a-etq">Tu programa</p>
        <pre class="a-mt-prog" data-prog></pre>
        <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Empezar de nuevo</button></div>
      </div>
      <div class="a-es-vista" aria-hidden="true">
        {escalones}
        <span class="a-es-meta">🏁</span>
        <span class="a-es-yo" data-yo>🤖</span>
      </div>
    </div>"""


CSS_MOTOR["escalera"] = _CSS_COL + _CSS_TALLER + """
.a-escalera{display:grid;gap:22px;margin-top:10px}
@media(min-width:980px){.a-escalera{grid-template-columns:1.1fr .9fr;align-items:start}}
.a-escalera .a-col{gap:9px}
.a-es-sale{margin:0;min-height:1.4em;font-family:var(--fm);font-size:clamp(13px,1.4vw,16px);color:var(--tx2)}
.a-es-sale b{color:var(--lvl);font-weight:600}
.a-es-vista{position:relative;height:clamp(300px,42vh,400px);border-radius:12px;overflow:hidden;
  background:linear-gradient(#101a33,#15284a 60%,#1b3560)}
.a-es-escalon{position:absolute;height:9px;border-radius:4px;background:rgba(255,255,255,.28);
  left:calc(8% + (var(--k) - 1) * 76% / var(--n));width:calc(60% / var(--n) + 22px);
  bottom:calc(8% + (var(--k) - 1) * 74% / var(--n))}
.a-es-meta{position:absolute;right:5%;top:7%;font-size:30px}
.a-es-yo{position:absolute;font-size:32px;left:calc(8% + var(--k,0) * 76% / var(--n));
  bottom:calc(8% + var(--k,0) * 74% / var(--n));transition:left .55s cubic-bezier(.3,1.3,.5,1),bottom .55s cubic-bezier(.3,1.3,.5,1)}
.a-es-yo.a-es-tropieza{animation:a-es-tropieza .45s}
@keyframes a-es-tropieza{30%{transform:translateY(6px) rotate(-10deg)}60%{transform:translateY(0) rotate(7deg)}}
.a-escalera.a-cima .a-es-yo{animation:a-es-salta .6s 2}
@keyframes a-es-salta{50%{transform:translateY(-14px)}}
@media (prefers-reduced-motion: reduce){.a-es-yo{transition:none}
  .a-es-yo.a-es-tropieza,.a-escalera.a-cima .a-es-yo{animation:none}}
"""

JS_MOTOR["escalera"] = r"""
M.escalera=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,lineas=[];
  var inp=ver(r,'[data-linea]'),prog=ver(r,'[data-prog]'),yo=ver(r,'[data-yo]'),sale=ver(r,'[data-sale]');
  function lista(a){return a.length>8?a.slice(0,6).join(', ')+' … '+a[a.length-1]:a.join(', ');}
  // Los números que de verdad produce su línea. null si no se puede leer.
  function corre(t){
    var m=t.match(/^for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+range\s*\(([^)]*)\)\s*:?\s*$/);
    if(!m)return null;
    var args=m[2].split(',').map(function(x){return x.trim();});
    if(args.length<1||args.length>3)return null;
    var nums=[];
    for(var i=0;i<args.length;i++){
      if(!/^-?\d+$/.test(args[i]))return null;
      nums.push(parseInt(args[i],10));
    }
    var a=nums.length===1?0:nums[0],b=nums.length===1?nums[0]:nums[1],p=nums.length===3?nums[2]:1;
    if(p===0)return 'salto0';
    var out=[],x=a,tope=0;
    while((p>0?x<b:x>b)&&tope++<500){out.push(x);x+=p;}
    return out;
  }
  // Qué le falta a la cabecera, dicho como lo diría el docente. null si está bien.
  function revisar(t,m){
    t=t.trim();
    if(!t)return ['Escribe la cabecera completa: for i in range(…):',null];
    if(!/^for\b/.test(t))return ['Un ciclo empieza con for.',null];
    if(!/\bin\b/.test(t))return ['Entre el nombre y range va in: for i in range(5):',null];
    if(!/range\s*\(/.test(t))return ['Dentro va range(...): es quien dice cuántas vueltas.',null];
    if(!/:\s*$/.test(t))return ['Falta los dos puntos al final de la cabecera.',null];
    var sec=corre(t);
    if(sec==='salto0')return ['El salto no puede ser 0: el ciclo no avanzaría nunca.',null];
    if(sec===null)return ['Dentro de range van números enteros separados por comas.',null];
    if(!sec.length)return ['Tu línea no da ninguna vuelta: revisa el desde y el hasta.',sec];
    if(sec.length!==m.secuencia.length||sec.some(function(x,i){return x!==m.secuencia[i];}))
      return ['El tuyo da '+lista(sec)+' y hacen falta '+lista(m.secuencia)+'.',sec];
    return [null,sec];
  }
  function pintar(){
    r.style.setProperty('--k',k);yo.style.setProperty('--k',k);
    var m=mis[Math.min(k,mis.length-1)];
    ver(r,'[data-num]').textContent=k>=mis.length?'¡Meta!':'Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-pide]').textContent=k>=mis.length?'Escribiste '+mis.length+' ciclos sin ayuda.':m.pide;
    prog.textContent=lineas.length?lineas.join('\n'):'# aquí van apareciendo tus ciclos';
    inp.disabled=k>=mis.length;ver(r,'[data-subir]').disabled=k>=mis.length;
    if(k<mis.length)sale.innerHTML='Tiene que dar: <b>'+lista(m.secuencia)+'</b>';
    else sale.textContent='';
    r.classList.toggle('a-cima',k>=mis.length);
  }
  function subir(){
    if(k>=mis.length)return;
    var res=revisar(inp.value,mis[k]),falla=res[0],sec=res[1];
    if(falla){
      fb(r,false,falla);
      yo.classList.remove('a-es-tropieza');void yo.offsetWidth;yo.classList.add('a-es-tropieza');
      return;
    }
    lineas.push(inp.value.trim()+'\n    display(i)');k++;inp.value='';
    if(k>=mis.length){gana(r);fb(r,true,'¡Meta! Ya sabes decirle a Python cuántas vueltas dar y en qué orden.');}
    else fb(r,true,'Da '+lista(sec)+'. Subes un escalón.');
    pintar();inp.focus();
  }
  on(ver(r,'[data-subir]'),'click',subir);
  on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();subir();}});
  on(ver(r,'[data-reiniciar]'),'click',function(){k=0;lineas=[];inp.value='';fb(r,null,'');pintar();});
  pintar();
};
"""


# ═════════════════════════════════════════════════════════════════════════════
#  «Tu primer…»: un solo taller para todas las semanas
#
#  La montaña (variables) y la escalera (ciclos) demostraron el patrón: misiones
#  cortas, el estudiante ESCRIBE la línea y la pantalla comprueba lo que la
#  línea HACE, no cómo está escrita. Repetir ese motor diez veces no tenía
#  sentido, así que este es el mismo esqueleto con un comprobador por tema:
#
#    condicion  if edad >= 18:        se prueba contra una tabla de valores
#    lista      frutas.append("x")    se corre sobre una lista de partida
#    funcion    def saluda(nombre):   se mira la cabecera y se llama
#    evento     @when("click", "#b")  se mira a qué botón se engancha
#    azar       random.randint(1,6)   se tiran 200 veces y se mira el rango
#    etiqueta   <h1>Hola</h1>         lo lee el navegador, no una expresión
#    exacto     una respuesta escrita que solo puede ser una
#    ordenar    no se escribe: se tocan los pasos en orden
#    clasificar no se escribe: se elige a qué grupo va cada ejemplo
#
#  Lo que todos comparten: fallar explica QUÉ pasó con lo suyo («el tuyo deja
#  pasar a 17»), nunca «incorrecto».
# ═════════════════════════════════════════════════════════════════════════════

# La chuleta del taller: lo que en papel estaría pegado en la pared. Está
# siempre a la vista para que elegir la pieza sea pensar, no adivinar: el que
# no ha visto nunca un != no puede inventárselo.
# El rótulo de la tira: sin nombre, una pista que diga «míralo abajo» no manda
# a ninguna parte.
TALLER_ROTULO = {
    "condicion": "Los comparadores",
    "lista": "Lo que puedes hacer con la lista",
    "funcion": "La forma de una función",
    "evento": "La forma de un evento",
    "azar": "Las dos formas del azar",
    "etiqueta": "Etiquetas que ya conoces",
    "exacto": "Cómo se contesta",
}

TALLER_AYUDA = {
    "condicion": [("==", "igual a"), ("!=", "distinto de"), ("&gt;", "mayor que"),
                  ("&lt;", "menor que"), ("&gt;=", "mayor o igual"), ("&lt;=", "menor o igual")],
    "lista": [("lista[0]", "el primero"), ("lista.append(x)", "añade al final"),
              ("lista.remove(x)", "saca ese"), ("len(lista)", "cuántos hay")],
    "funcion": [("def nombre():", "sin parámetros"), ("def nombre(a, b):", "con dos")],
    "evento": [('@when("click", "#id")', "engancha el botón")],
    "azar": [("random.randint(a, b)", "un número entre los dos"),
             ("random.choice(lista)", "uno de la lista")],
    "etiqueta": [("&lt;p&gt;texto&lt;/p&gt;", "se abre y se cierra"),
                 ("&lt;h1&gt; &lt;h2&gt;", "títulos"), ("&lt;button&gt;", "un botón")],
    "exacto": [("Escribe solo el resultado", "tal como saldría en pantalla")],
}


def juego_taller(pr):
    """El taller «Tu primer…» de la semana, sea del tema que sea."""
    din, t = pr["dinamica"], pr["taller2"]
    tipo, mis = t["tipo"], t["misiones"]
    pasos = "".join(f"<li>{E(x)}</li>" for x in din["pasos"])
    cfg = {"tipo": tipo, "misiones": mis, "unidad": t.get("unidad", "línea")}
    escribe = tipo not in ("ordenar", "clasificar")
    ayuda = "".join(f'<span class="a-tl-ay"><code>{c}</code><i>{E(q)}</i></span>'
                    for c, q in TALLER_AYUDA.get(tipo, []))
    if ayuda:
        rotulo = TALLER_ROTULO.get(tipo, "Lo que puedes usar")
        ayuda = f'<p class="a-etq">{rotulo}</p>{ayuda}'
    caja = (f'<div class="a-mt-escribe">'
            f'<input class="campo a-mt-in" data-linea autocomplete="off" spellcheck="false" '
            f'aria-label="Escribe tu {E(cfg["unidad"])}" placeholder="{E(t.get("ejemplo", ""))}">'
            f'<button type="button" class="a-btn" data-probar>Probar</button></div>'
            f'<p class="a-mt-pista" data-forma></p>'
            f'<div class="a-tl-ayuda">{ayuda}</div>'
            if escribe else
            '<div class="a-tl-ops" data-ops></div>')
    return f"""<div class="a-taller a-marcador" data-act="taller" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        <details class="a-mt-din">
          <summary>Antes, en grupo · {E(din["titulo"])} · {din["minutos"]} min</summary>
          <ol>{pasos}</ol>
        </details>
        <div class="a-mt-mision"><p class="a-etq" data-num></p><p class="a-mt-pide" data-pide></p>
          <button type="button" class="a-tl-pista" data-pista hidden>💡 Pista</button>
          <p class="a-tl-dice" data-dice hidden></p></div>
        {caja}
        <p class="a-tl-sale" data-sale aria-live="polite"></p>
        {FB}
      </div>
      <div class="a-col">
        <div class="a-tl-vista" data-vista hidden></div>
        <p class="a-etq">Lo que llevas</p>
        <pre class="a-mt-prog" data-prog></pre>
        <div class="a-tl-barra" aria-hidden="true"><i data-barra></i></div>
        <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Empezar de nuevo</button></div>
      </div>
    </div>"""


CSS_MOTOR["taller"] = _CSS_TALLER + _CSS_COL + """
.a-tl-sale{margin:0;font-size:14px;color:var(--tx2);min-height:20px}
.a-tl-sale b{color:var(--lvl);font-family:var(--fm)}
.a-tl-ops{display:flex;flex-wrap:wrap;gap:8px}
.a-tl-op{min-height:46px;padding:8px 14px;border-radius:8px;border:1px solid var(--lvl);background:var(--panel);
  color:var(--tx);font-family:inherit;font-size:clamp(14px,1.5vw,17px);cursor:pointer;touch-action:manipulation}
.a-tl-op[disabled]{opacity:.4;cursor:default}
.a-tl-op[data-estado=bien]{background:var(--a-ok);color:#06121f;border-color:var(--a-ok)}
.a-tl-op[data-estado=mal]{border-color:var(--a-ko);color:var(--a-ko)}
/* La vista: lo que hace su línea, dibujado. En el portero son las personas
   que llegan; en las listas, las fichas; en el azar, las tiradas. */
.a-tl-vista{display:grid;gap:10px}
.a-tl-fila{display:flex;flex-wrap:wrap;gap:8px}
.a-tl-caso{display:grid;gap:2px;justify-items:center;min-width:76px;padding:9px 12px;border-radius:10px;
  background:var(--panel);border:1px solid var(--line);text-align:center}
.a-tl-caso b{font-family:var(--fm);font-size:clamp(15px,1.7vw,19px);color:var(--tx)}
.a-tl-caso span{font-size:11.5px;letter-spacing:.04em;color:var(--mut)}
.a-tl-caso i{font-style:normal;font-size:19px;line-height:1}
.a-tl-caso[data-r=pasa]{border-color:var(--a-ok)}
.a-tl-caso[data-r=no]{border-color:var(--line);opacity:.55}
.a-tl-caso[data-r=mal]{border-color:var(--a-ko);background:rgba(244,164,164,.10)}
.a-tl-ficha{padding:8px 13px;border-radius:999px;background:var(--panel);border:1px solid var(--lvl);
  font-family:var(--fm);font-size:clamp(13px,1.4vw,16px);color:var(--tx)}
.a-tl-ficha[data-nueva]{background:var(--lvl);color:var(--fondo,#06121f);font-weight:700}
.a-tl-dado{display:grid;place-items:center;width:46px;height:46px;border-radius:10px;background:var(--panel);
  border:1px solid var(--line);font-family:var(--fm);font-size:19px;color:var(--tx)}
.a-tl-ayuda{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.a-tl-ayuda>.a-etq{flex:1 0 100%;margin:0}
.a-tl-ay{display:inline-flex;align-items:baseline;gap:6px;padding:4px 9px;border-radius:999px;
  background:var(--bg2);border:1px solid var(--line)}
.a-tl-ay code{font-family:var(--fm);font-size:12.5px;color:var(--lvl)}
.a-tl-ay i{font-style:normal;font-size:11.5px;color:var(--mut)}
.a-tl-pista{margin:8px 0 0;padding:4px 10px;border-radius:999px;border:1px dashed var(--sand);
  background:transparent;color:var(--sand);font-family:inherit;font-size:12.5px;cursor:pointer}
.a-tl-dice{margin:8px 0 0;font-size:14px;color:var(--sand);line-height:1.45}
.a-tl-barra{height:8px;border-radius:99px;background:var(--bg2);border:1px solid var(--line);overflow:hidden}
.a-tl-barra i{display:block;height:100%;width:var(--p,0%);background:var(--lvl);transition:width .3s}
"""

JS_MOTOR["taller"] = r"""
M.taller=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,hechas=[];
  var inp=ver(r,'[data-linea]'),prog=ver(r,'[data-prog]'),sale=ver(r,'[data-sale]'),ops=ver(r,'[data-ops]');

  /* ── Comprobadores: cada uno devuelve [queja, loQueHizo] ───────────────── */
  function num(x){return /^-?\d+$/.test(String(x).trim());}
  function val(x){ // "18" -> 18 ; "\"Ana\"" -> Ana (texto)
    x=String(x).trim();
    if(num(x))return parseInt(x,10);
    var m=x.match(/^["'](.*)["']$/);
    return m?m[1]:null;
  }
  // En el aula la tilde no es el tema: «Sofia» y «Sofía» valen lo mismo, y la
  // lista se queda con lo que el estudiante escribió.
  function pelado(x){return String(x).normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
  function mismo(a,b){return String(a)===String(b)||pelado(a)===pelado(b);}
  // Las listas se enseñan como las escribe Python, no como las escribe JSON:
  // el enunciado dice ['Ana', 'Luis'] y la queja tiene que decir lo mismo.
  function pyLista(l){
    return '['+l.map(function(x){return typeof x==='number'?String(x):"'"+x+"'";}).join(', ')+']';
  }
  function compara(a,op,b){
    if(a===null||b===null)return null;
    switch(op){case '==':return a===b;case '!=':return a!==b;
      case '>':return a>b;case '<':return a<b;case '>=':return a>=b;case '<=':return a<=b;}
    return null;
  }
  var CHK={
    // if <variable> <op> <valor>:   se prueba contra la tabla de la misión
    condicion:function(t,m){
      t=t.trim();
      if(!/^if\b/.test(t))return ['Una decisión empieza con if.',null];
      if(!/:\s*$/.test(t))return ['Falta los dos puntos al final.',null];
      var c=t.replace(/^if\s+/,'').replace(/:\s*$/,'').trim();
      if(/[^!<>=]=[^=]/.test(c))return ['Con un solo = se guarda. Para comparar van dos: ==.',null];
      var mm=c.match(/^([A-Za-z_][A-Za-z0-9_.]*)\s*(==|!=|>=|<=|>|<)\s*(.+)$/);
      if(!mm)return ['Escribe una sola comparación: variable, comparador y valor.',null];
      if(mm[1]!==m.variable)return ['La variable de esta misión es '+m.variable+'.',null];
      var b=val(mm[3]);
      if(b===null)return ['El valor va tal cual (18) o entre comillas ("Ana").',null];
      var pasa=[],fallo=null;
      for(var i=0;i<m.casos.length;i++){
        var a=val(String(m.casos[i])), res=compara(a,mm[2],b);
        if(res===null)return ['No puedo comparar '+m.casos[i]+' con eso.',null];
        if(res)pasa.push(m.casos[i]);
        if(res!==!!m.espera[i]&&fallo===null)
          fallo=m.casos[i]+(res?' pasa y no debía':' no pasa y debía');
      }
      if(fallo)return ['Con lo tuyo, '+fallo+'.',pasa];
      return [null,pasa];
    },
    // una operación sobre la lista de partida
    lista:function(t,m){
      t=t.trim();
      var l=(m.lista||[]).slice(),nom=m.variable;
      var ap=t.match(new RegExp('^'+nom+'\\.append\\(\\s*(.+?)\\s*\\)$'));
      var qu=t.match(new RegExp('^'+nom+'\\.remove\\(\\s*(.+?)\\s*\\)$'));
      var as=t.match(new RegExp('^'+nom+'\\s*\\[\\s*(-?\\d+)\\s*\\]\\s*=\\s*(.+)$'));
      var cr=t.match(new RegExp('^'+nom+'\\s*=\\s*\\[(.*)\\]$'));
      if(ap){var v=val(ap[1]);if(v===null)return ['El valor va entre comillas si es texto.',null];l.push(v);}
      else if(qu){var q=val(qu[1]),iq=l.findIndex(function(x){return mismo(x,q);});
        if(iq<0)return ['En la lista no hay ningún '+qu[1]+'.',l];l.splice(iq,1);}
      else if(as){var i=parseInt(as[1],10),v2=val(as[2]);
        if(i<0||i>=l.length)return ['La posición '+i+' no existe: la lista va de 0 a '+(l.length-1)+'.',l];
        if(v2===null)return ['El valor va entre comillas si es texto.',l];l[i]=v2;}
      else if(cr){l=cr[1].trim()?cr[1].split(',').map(function(x){return val(x);}):[];
        if(l.some(function(x){return x===null;}))return ['Dentro de los corchetes, los textos van entre comillas.',null];}
      else return ['Usa '+nom+' con [ ], .append( ) o .remove( ).',null];
      var bien=l.length===m.espera.length&&l.every(function(x,i){return mismo(x,m.espera[i]);});
      if(!bien)return ['Te queda '+pyLista(l)+' y hace falta '+pyLista(m.espera)+'.',l];
      return [null,l];
    },
    // def nombre(parámetros):
    funcion:function(t,m){
      t=t.trim();
      if(!/^def\b/.test(t))return ['Una función empieza con def.',null];
      if(!/:\s*$/.test(t))return ['Falta los dos puntos al final de la cabecera.',null];
      var mm=t.match(/^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*:$/);
      if(!mm)return ['Después del nombre van los paréntesis: def saluda(nombre):',null];
      if(mm[1]!==m.nombre)return ['Esta función se tiene que llamar '+m.nombre+'.',null];
      var ps=mm[2].trim()?mm[2].split(',').map(function(x){return x.trim();}):[];
      var esp=m.parametros||[];
      if(ps.length!==esp.length||ps.some(function(x,i){return x!==esp[i];}))
        return ['Entre paréntesis van '+(esp.length?esp.join(', '):'ninguno')+', y escribiste '+(ps.length?ps.join(', '):'ninguno')+'.',ps];
      return [null,ps];
    },
    // @when("click", "#boton")
    evento:function(t,m){
      t=t.trim();
      if(!/^@when\b/.test(t))return ['Empieza con @when, que es quien engancha el botón.',null];
      var mm=t.match(/^@when\s*\(\s*["'](\w+)["']\s*,\s*["']([^"']+)["']\s*\)$/);
      if(!mm)return ['Van dos cosas entre comillas: @when("click", "#boton").',null];
      if(mm[1]!==(m.evento||'click'))return ['El evento de esta misión es "'+(m.evento||'click')+'".',null];
      if(mm[2]!=='#'+m.id)return ['Ese es otro botón. El de esta misión es "#'+m.id+'".',mm[2]];
      return [null,'#'+m.id];
    },
    // random.randint(a, b) / random.choice(lista)
    azar:function(t,m){
      t=t.trim();
      if(!/^random\./.test(t))return ['Empieza con random., que es la caja del azar.',null];
      if(m.tipo==='choice'){
        var mc=t.match(/^random\.choice\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)$/);
        if(!mc)return ['Para elegir de una lista: random.choice(lista).',null];
        if(mc[1]!==m.variable)return ['La lista de esta misión se llama '+m.variable+'.',null];
        return [null,'uno de '+pyLista(m.lista)];
      }
      var mr=t.match(/^random\.randint\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)$/);
      if(!mr)return ['Para un número al azar: random.randint(desde, hasta).',null];
      var a=parseInt(mr[1],10),b=parseInt(mr[2],10);
      if(a>b)return ['El desde tiene que ser menor que el hasta.',null];
      if(a!==m.desde||b!==m.hasta){
        var tira=[];for(var i=0;i<6;i++)tira.push(a+Math.floor(Math.random()*(b-a+1)));
        return ['Lo tuyo saca de '+a+' a '+b+' ('+tira.join(', ')+'…) y hacen falta de '+m.desde+' a '+m.hasta+'.',tira];
      }
      var t2=[];for(var j=0;j<6;j++)t2.push(a+Math.floor(Math.random()*(b-a+1)));
      return [null,t2];
    },
    // una etiqueta de HTML: la lee el navegador
    etiqueta:function(t,m){
      t=t.trim();
      if(!/^</.test(t))return ['Una etiqueta empieza con <.',null];
      var d=document.createElement('div');d.innerHTML=t;
      var el=d.firstElementChild;
      if(!el)return ['El navegador no entiende eso como una etiqueta.',null];
      if(d.childNodes.length>1||el.outerHTML.replace(/\s+/g,'')!==t.replace(/\s+/g,''))
        return ['Escribe una sola etiqueta, abierta y cerrada: <'+m.etiqueta+'>…</'+m.etiqueta+'>',null];
      if(el.tagName.toLowerCase()!==m.etiqueta)
        return ['Esa es una etiqueta <'+el.tagName.toLowerCase()+'> y hace falta <'+m.etiqueta+'>.',el.tagName.toLowerCase()];
      if(m.texto&&!mismo(el.textContent.trim(),m.texto))
        return ['Dentro tiene que decir exactamente: '+m.texto,el.textContent.trim()];
      return [null,el.tagName.toLowerCase()+' · '+el.textContent.trim()];
    },
    // una respuesta que solo puede ser una
    exacto:function(t,m){
      var a=pelado(t.trim().replace(/\s+/g,' ').toLowerCase());
      var ok=(m.espera||[]).some(function(x){return pelado(String(x).trim().replace(/\s+/g,' ').toLowerCase())===a;});
      if(!a)return ['Escribe tu respuesta.',null];
      if(!ok)return ['Escribiste «'+t.trim()+'». '+(m.ayuda||'Mira otra vez el programa.'),t.trim()];
      return [null,t.trim()];
    }
  };

  /* ── El esqueleto, igual para todos ────────────────────────────────────── */
  function texto(m){return CHK[cfg.tipo]?CHK[cfg.tipo](inp.value,m):['Falta el comprobador.',null];}
  // Lo que hace su línea, dibujado: el que no se ve no se entiende.
  var vista=ver(r,'[data-vista]');
  function cajas(html){vista.hidden=!html;vista.innerHTML=html||'';}
  function esc(t){return String(t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
  function pintarVista(m,res){
    if(!m){cajas('');return;}
    if(cfg.tipo==='condicion'){
      var h='<p class="a-etq">Los valores de '+esc(m.variable)+' que llegan</p><div class="a-tl-fila">';
      for(var i=0;i<m.casos.length;i++){
        var debe=!!m.espera[i], hizo=res?res.indexOf(m.casos[i])>=0:null;
        var estado=hizo===null?(debe?'pasa':'no'):(hizo===debe?(hizo?'pasa':'no'):'mal');
        var marca=hizo===null?(debe?'✓':'✕'):(hizo?'✓':'✕');
        h+='<div class="a-tl-caso" data-r="'+estado+'"><i>'+marca+'</i><b>'+esc(m.casos[i])+'</b>'
          +'<span>'+(debe?'debe pasar':'no debe')+'</span></div>';
      }
      cajas(h+'</div>');return;
    }
    if(cfg.tipo==='lista'){
      var l=res||m.lista||[], h2='<p class="a-etq">'+esc(m.variable)+'</p><div class="a-tl-fila">';
      if(!l.length)h2+='<span class="a-tl-ficha">(vacía)</span>';
      for(var j2=0;j2<l.length;j2++)h2+='<span class="a-tl-ficha">'+esc(l[j2])+'</span>';
      cajas(h2+'</div>');return;
    }
    if(cfg.tipo==='azar'){
      if(!res){cajas('<p class="a-etq">Tiradas</p><div class="a-tl-fila">'
        +'<span class="a-tl-dado">?</span><span class="a-tl-dado">?</span><span class="a-tl-dado">?</span></div>');return;}
      var t=Array.isArray(res)?res:[res], h3='<p class="a-etq">Seis tiradas de tu línea</p><div class="a-tl-fila">';
      for(var i3=0;i3<t.length;i3++)h3+='<span class="a-tl-dado">'+esc(t[i3])+'</span>';
      cajas(h3+'</div>');return;
    }
    cajas('');
  }
  /* El esqueleto de ESTA misión: se ve la variable y la forma, pero no la
     respuesta. Antes el campo proponía siempre el mismo ejemplo y en la misión
     de la nota seguía diciendo «edad»: fallaban por eso, no por el tema. */
  function esqueleto(m){
    if(m.ejemplo)return m.ejemplo;
    if(cfg.tipo==='condicion')return 'if '+m.variable+' … :';
    if(cfg.tipo==='lista')return m.variable+' …';
    if(cfg.tipo==='funcion')return 'def '+m.nombre+'(…):';
    if(cfg.tipo==='evento')return '@when("click", "#…")';
    if(cfg.tipo==='azar')return m.tipo==='choice'?'random.choice(…)':'random.randint(…, …)';
    if(cfg.tipo==='etiqueta')return '<…>…</…>';
    return 'Escribe tu respuesta';
  }
  var fallos=0,dice=ver(r,'[data-dice]'),bPista=ver(r,'[data-pista]');
  function verPista(si){
    if(!bPista)return;
    dice.hidden=!si;bPista.hidden=si;
  }
  function pintar(){
    var fin=k>=mis.length,m=mis[Math.min(k,mis.length-1)];
    pintarVista(fin?null:m,null);
    if(bPista){
      dice.textContent=m&&m.pista?m.pista:'';
      bPista.hidden=fin||!m||!m.pista;dice.hidden=true;
    }
    ver(r,'[data-num]').textContent=fin?'¡Completo!':'Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-pide]').textContent=fin?'Hiciste las '+mis.length+' sin ayuda.':m.pide;
    prog.textContent=hechas.length?hechas.join('\n'):'# aquí va apareciendo lo tuyo';
    ver(r,'[data-barra]').style.setProperty('--p',Math.round(k*100/mis.length)+'%');
    if(inp){
      inp.disabled=fin;ver(r,'[data-probar]').disabled=fin;
      if(m&&!fin){
        inp.placeholder=esqueleto(m);
        ver(r,'[data-forma]').innerHTML='Tu línea va así: <code>'+esc(esqueleto(m))+'</code>';
      }
    }
    sale.innerHTML=fin?'':(m.sale?'Tiene que dar: <b>'+m.sale+'</b>':'');
    if(ops)pintarOps(fin?null:m);
  }
  function avanza(linea,hizo,texto_ok){
    hechas.push(linea);k++;fallos=0;
    if(inp)inp.value='';
    if(k>=mis.length){gana(r);fb(r,true,'¡Completo! '+(cfg.cierre||'Ya te sale sin ayuda.'));}
    // Con el número delante se sabe de qué misión habla; y en cuanto empiezan
    // a escribir la siguiente, se va.
    else fb(r,true,'Misión '+k+' lista. '+(texto_ok||('Bien: '+hizo)));
    pintar();verPista(false);
    if(inp&&k<mis.length)inp.focus();
  }
  // Lo que hizo su línea, dicho como se diría en voz alta.
  function muestra(v){
    if(v===null||v===undefined)return '';
    if(Array.isArray(v))return v.length?v.map(function(x){return String(x);}).join(', '):'(nada)';
    return String(v);
  }
  function probar(){
    if(k>=mis.length)return;
    var res=texto(mis[k]);
    if(res[0]){
      fb(r,false,res[0]);pintarVista(mis[k],res[1]);
      // Quien va bien no ve la pista; quien se traba de verdad —tres intentos—,
      // no se queda clavado.
      if(++fallos>=3&&mis[k].pista)verPista(true);
      return;
    }
    var hizo=muestra(res[1]);
    avanza(inp.value.trim(),hizo,hizo?'Bien: '+hizo+'.':'Bien.');
  }
  /* Las dos misiones que no se escriben: tocar en orden, o elegir el grupo. */
  function pintarOps(m){
    if(!m){ops.innerHTML='';return;}
    var lista=cfg.tipo==='ordenar'?m.pasos:m.grupos;
    ops.innerHTML='';
    lista.forEach(function(txt,i){
      var b=document.createElement('button');
      b.type='button';b.className='a-tl-op';b.textContent=txt;b.dataset.i=i;
      on(b,'click',function(){tocar(m,b,i);});
      ops.appendChild(b);
    });
    if(cfg.tipo==='ordenar')ops.dataset.van='0';
  }
  function tocar(m,b,i){
    if(cfg.tipo==='clasificar'){
      var bien=i===m.correcto;
      b.dataset.estado=bien?'bien':'mal';
      if(!bien){fb(r,false,m.porque||'Ese no es. Mira otra vez el ejemplo.');return;}
      todos(r,'.a-tl-op').forEach(function(x){x.disabled=true;});
      avanza(m.pide+' → '+m.grupos[i],m.grupos[i],'Bien: '+m.grupos[i]+'.');
      return;
    }
    var van=parseInt(ops.dataset.van||'0',10);
    if(i!==m.orden[van]){
      b.dataset.estado='mal';
      fb(r,false,'Ese no va '+(van===0?'primero':'ahora')+'. Piensa qué hace falta antes.');
      setTimeout(function(){b.removeAttribute('data-estado');},700);
      return;
    }
    b.dataset.estado='bien';b.disabled=true;b.textContent=(van+1)+'. '+b.textContent;
    ops.dataset.van=String(van+1);
    if(van+1>=m.orden.length)avanza(m.pide,'en orden','Ese es el orden.');
    else fb(r,true,'Va bien. ¿Y ahora?');
  }
  if(inp){
    on(ver(r,'[data-probar]'),'click',probar);
    on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();probar();}});
    on(inp,'input',function(){var p=ver(r,'.a-fb');if(p&&p.textContent)fb(r,null,'');});
  }
  if(bPista)on(bPista,'click',function(){verPista(true);});
  function reiniciar(){k=0;hechas=[];fallos=0;if(inp)inp.value='';fb(r,null,'');pintar();verPista(false);}
  on(ver(r,'[data-reiniciar]'),'click',reiniciar);
  pausas.push(function(){fb(r,null,'');});
  pintar();
};
"""

def taller_primera(pr, ctx=None):
    if pr.get("montana"):
        return juego_montana(pr)
    if pr.get("escalera"):
        return juego_escalera(pr)
    if pr.get("taller2"):
        return juego_taller(pr)
    din, t = pr["dinamica"], pr["taller"]
    pasos = "".join(f"<li>{E(x)}</li>" for x in din["pasos"])
    return f"""<div class="a-primera">
      <div class="a-pv-din">
        <p class="a-etq">Sin computadora · {din["minutos"]} min</p>
        <h3 class="a-pv-t">{E(din["titulo"])}</h3>
        <ol class="a-pv-pasos">{pasos}</ol>
      </div>
      <div class="a-pv-taller" data-act="primeravar" data-cfg="{_cfg({"cambia": t["cambia"], "como": t.get("cambia_como", "suma")})}">
        <p class="a-etq">En tu compu · ahora la escribes tú</p>
        <div class="a-pv-campos">
          <label>Nombre de la caja
            <input class="campo" data-nombre value="{A(t["nombre"])}" autocomplete="off" spellcheck="false"></label>
          <label>Valor que guarda
            <input class="campo" data-valor value="{A(t["valor"])}" autocomplete="off" spellcheck="false"></label>
        </div>
        <div class="a-acc"><button type="button" class="a-btn" data-crear>Crear la variable</button>
          <button type="button" class="a-btn a-sec" data-cambia hidden>Cámbiala</button></div>
        {FB}
        <div class="a-pv-res" data-res hidden>
          <div class="a-pv-caja"><span data-etq></span><b data-val></b><i data-tipo></i></div>
          <pre class="a-pv-code" data-codigo></pre>
          <pre class="a-pv-sal" data-sal></pre>
        </div>
      </div>
    </div>"""


CSS_MOTOR["primeravar"] = """
.a-primera{display:grid;gap:18px;margin-top:14px}
@media(min-width:980px){.a-primera{grid-template-columns:.85fr 1.15fr;align-items:start}}
.a-pv-din{padding:16px 18px;background:var(--bg2);border:1px solid var(--line);border-left:4px solid var(--sand);border-radius:8px}
.a-pv-din .a-etq{color:var(--sand)}
.a-pv-t{font-family:var(--fd);font-size:clamp(19px,2.2vw,26px);margin:6px 0 10px}
.a-pv-pasos{margin:0;padding-left:20px;display:grid;gap:7px;color:var(--tx2);
  font-size:clamp(13px,1.45vw,16.5px);line-height:1.4}
.a-pv-taller{padding:16px 18px;border:1px solid var(--line);border-top:3px solid var(--lvl);border-radius:8px;background:var(--bg2)}
.a-pv-campos{display:grid;gap:12px;margin:10px 0 14px}
@media(min-width:620px){.a-pv-campos{grid-template-columns:1fr 1fr}}
.a-pv-campos label{display:grid;gap:5px;font-size:13px;color:var(--mut);font-family:var(--fm)}
.a-pv-campos .campo{min-height:44px;font-size:clamp(15px,1.6vw,18px)}
.a-pv-res{display:grid;gap:10px;margin-top:12px}
.a-pv-caja{display:flex;gap:12px;align-items:center;padding:12px 16px;border:2px dashed var(--lvl);border-radius:10px}
.a-pv-caja span{font-family:var(--fm);font-size:13px;color:var(--mut);letter-spacing:.08em;text-transform:uppercase}
.a-pv-caja b{font-family:var(--fd);font-size:clamp(22px,2.6vw,32px);color:var(--lvl)}
.a-pv-caja i{margin-left:auto;font-style:normal;font-family:var(--fm);font-size:12px;color:var(--mut)}
.a-pv-code,.a-pv-sal{margin:0;padding:11px 14px;border-radius:6px;font-family:var(--fm);white-space:pre-wrap;
  font-size:clamp(13px,1.45vw,16px);line-height:1.5}
.a-pv-code{background:#0B1020;color:#D7DEEC;border:1px solid var(--line)}
.a-pv-sal{background:var(--bg);color:var(--tx2);border:1px dashed var(--line)}
"""

JS_MOTOR["primeravar"] = r"""
M.primeravar=function(r){
  var cfg=JSON.parse(r.dataset.cfg);
  var iN=ver(r,'[data-nombre]'),iV=ver(r,'[data-valor]'),caja=ver(r,'[data-res]');
  var bCrea=ver(r,'[data-crear]'),bCam=ver(r,'[data-cambia]');
  var RESERVADAS=['and','as','assert','break','class','continue','def','del','elif','else','except','False',
    'finally','for','from','global','if','import','in','is','lambda','None','nonlocal','not','or','pass',
    'raise','return','True','try','while','with','yield'];
  var nombre='',valor=null,lineas=[];
  function revisaNombre(n){
    if(!n)return 'Escribe un nombre para la caja, como puntos.';
    if(/\s/.test(n))return 'Sin espacios: júntalo con guion bajo, como mis_puntos.';
    if(/^[0-9]/.test(n))return 'Un nombre no puede empezar con un número.';
    if(RESERVADAS.indexOf(n)>-1)return '«'+n+'» es una palabra de Python: elige otro nombre.';
    if(!/^[A-Za-z_][A-Za-z0-9_]*$/.test(n))return 'Solo letras sin tilde, números y _ (nada de ñ, tildes ni signos).';
    return null;
  }
  function lee(v){
    if(v==='')return null;
    if(/^-?\d+$/.test(v))return ['int',v];
    if(/^-?(\d+\.\d*|\.\d+)$/.test(v))return ['float',String(Number(v))];
    if(v==='True'||v==='False')return ['bool',v];
    return ['str',v];
  }
  function lit(v){return v[0]==='str'?'"'+v[1].replace(/"/g,'\\"')+'"':P.repr(v);}
  function pinta(){
    ver(r,'[data-etq]').textContent=nombre;
    ver(r,'[data-val]').textContent=lit(valor);
    ver(r,'[data-tipo]').textContent='tipo: '+valor[0];
    ver(r,'[data-codigo]').textContent=lineas.join('\n');
    ver(r,'[data-sal]').textContent=P.num(valor)||valor[0]==='bool'?valor[1]:valor[1];
    caja.hidden=false;
  }
  on(bCrea,'click',function(){
    var n=iN.value.trim(),malo=revisaNombre(n),v=lee(iV.value.trim());
    if(malo){caja.hidden=true;bCam.hidden=true;fb(r,false,malo);return;}
    if(!v){caja.hidden=true;bCam.hidden=true;fb(r,false,'Escribe un valor: un número como 10 o un texto como Luna.');return;}
    nombre=n;valor=v;
    lineas=[nombre+' = '+lit(valor),'display('+nombre+')'];
    pinta();bCam.hidden=false;
    gana(r)&&fb(r,true,'¡Creaste tu primera variable! '+(valor[0]==='str'
      ? 'Es texto: por eso va entre comillas.'
      : 'Es un número: va sin comillas.'));
  });
  on(bCam,'click',function(){
    if(!valor)return;
    var linea;
    if(cfg.como==='asigna'){
      // En la primera clase todavía no existe +=: la caja se vuelve a llenar.
      valor=P.num(valor)?['int',String(cfg.cambia)]:['str','Ana'];
      linea=nombre+' = '+lit(valor);
    }else if(P.num(valor)){valor=P.op(valor,'+',['int',String(cfg.cambia)]);linea=nombre+' += '+cfg.cambia;}
    else{valor=['str',valor[1]+' Jr.'];linea=nombre+' = '+nombre+' + " Jr."';}
    lineas=[lineas[0],linea,'display('+nombre+')'];
    pinta();
    fb(r,true,'La caja sigue llamándose '+nombre+', pero ya guarda otra cosa.');
  });
  function reiniciar(){caja.hidden=true;bCam.hidden=true;fb(r,null,'');valor=null;lineas=[];}
  pausas.push(reiniciar);
  reiniciar();
};
"""



# ── La torre de variables ───────────────────────────────────────────────────

def juego_torre(j, ctx):
    fichas = "".join(
        f'<button type="button" class="a-tb" data-i="{i}"><code>{E(j["lineas"][i]["txt"])}</code></button>'
        for i in orden(len(j["lineas"]), f'{ctx["nid"]}:{ctx["n"]}:torre', distinto=False))
    meta = j.get("meta", 5)
    cfg = {"lineas": j["lineas"], "meta": meta}
    return f"""<div class="a-torre" data-act="torre" data-cfg="{_cfg(cfg)}">
      <div class="a-col">
        <p class="a-etq">Toca una línea: si está bien escrita, sube a la torre</p>
        <div class="a-tb-fichas">{fichas}</div>
        {FB}
        <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Empezar de nuevo</button></div>
      </div>
      <div class="a-tw">
        <div class="a-tw-pila" data-pila></div>
        <div class="a-tw-suelo"><span data-marca>0 / {meta}</span></div>
      </div>
    </div>"""


MOTORES_HTML["torre"] = juego_torre

CSS_MOTOR["torre"] = _CSS_COL + """
.a-torre{display:grid;gap:20px;margin-top:14px}
@media(min-width:980px){.a-torre{grid-template-columns:1.05fr .95fr;align-items:end}}
.a-tb-fichas{display:flex;flex-wrap:wrap;gap:8px}
.a-tb{min-height:46px;padding:8px 13px;border-radius:8px;border:1px solid var(--line);background:#0B1020;
  color:#D7DEEC;cursor:pointer;touch-action:manipulation}
.a-tb code{font-family:var(--fm);font-size:clamp(12.5px,1.25vw,15px)}
.a-tb:hover{border-color:var(--lvl)}
.a-tb:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-tb[disabled]{opacity:.35;cursor:default}
.a-tb.a-cae{animation:a-cae .5s ease-in forwards}
@keyframes a-cae{60%{transform:translateY(26px) rotate(8deg)}100%{transform:translateY(90px) rotate(22deg);opacity:0}}
.a-tw{display:flex;flex-direction:column;justify-content:flex-end;min-height:330px}
.a-tw-pila{display:flex;flex-direction:column-reverse;align-items:center;gap:6px}
.a-tw-bloque{padding:10px 16px;border-radius:8px;background:var(--lvl);color:#08111f;font-family:var(--fm);
  font-weight:700;font-size:clamp(12.5px,1.3vw,15.5px);box-shadow:0 8px 20px -12px rgba(0,0,0,.8);
  animation:a-sube-bloque .45s cubic-bezier(.2,1.4,.4,1)}
@keyframes a-sube-bloque{from{transform:translateY(60px) scale(.9);opacity:0}}
.a-tw-suelo{margin-top:10px;padding:10px 0;border-top:4px solid var(--line);text-align:center;
  font-family:var(--fm);font-size:13px;color:var(--mut);letter-spacing:.1em}
.a-tw.a-lista .a-tw-suelo{color:var(--a-ok);border-color:var(--a-ok)}
@media (prefers-reduced-motion: reduce){.a-tw-bloque,.a-tb.a-cae{animation:none}}
"""

JS_MOTOR["torre"] = r"""
M.torre=function(r){
  var cfg=JSON.parse(r.dataset.cfg),pila=ver(r,'[data-pila]'),marca=ver(r,'[data-marca]'),torre=ver(r,'.a-tw');
  var puestos=0;
  function pintar(){marca.textContent=puestos+' / '+cfg.meta;torre.classList.toggle('a-lista',puestos>=cfg.meta);}
  function reiniciar(){
    puestos=0;pila.innerHTML='';fb(r,null,'');
    todos(r,'.a-tb').forEach(function(b){b.disabled=false;b.classList.remove('a-cae');});
    pintar();
  }
  todos(r,'.a-tb').forEach(function(b){on(b,'click',function(){
    if(b.disabled)return;
    var linea=cfg.lineas[+b.dataset.i];
    if(!linea.ok){
      b.classList.add('a-cae');
      setTimeout(function(){b.classList.remove('a-cae');},520);
      fb(r,false,'Se cayó: '+linea.porque);
      return;
    }
    b.disabled=true;puestos++;
    var d=document.createElement('div');d.className='a-tw-bloque';d.textContent=linea.txt;
    pila.appendChild(d);pintar();
    if(puestos>=cfg.meta&&gana(r))fb(r,true,'¡Torre completa! Todas esas líneas guardan algo con su nombre.');
    else fb(r,true,'Bien escrita: sube a la torre.');
  });});
  on(ver(r,'[data-reiniciar]'),'click',reiniciar);
  pausas.push(reiniciar);
  pintar();
};
"""


# ── El editor dentro de la clase: la plantilla del pen, sin salir ──────────

def editor_html(p):
    # Empieza en Python si hay Python de partida; si no (la semana de HTML y
    # CSS), en HTML.
    inicio = "py" if p["py"].strip() else "html"
    cfg = {"v": PYSCRIPT_VERSION, "html": p["html"], "css": p["css"], "py": p["py"], "inicio": inicio}
    pestañas = "".join(
        f'<button type="button" role="tab" class="a-ed-tab" data-tab="{k}" aria-selected="{str(k == inicio).lower()}">{t}</button>'
        for k, t in (("py", "Python"), ("html", "HTML"), ("css", "CSS")))
    return f"""<div class="a-editor" data-act="editor" data-cfg="{_cfg(cfg)}">
      <div class="a-ed-col">
        <div class="a-ed-tabs" role="tablist" aria-label="Qué parte del código">{pestañas}</div>
        <textarea class="a-ed-code" data-codigo spellcheck="false" aria-label="Tu código"></textarea>
        <div class="a-acc"><button type="button" class="a-btn" data-correr>▶ Ejecutar</button>
          <button type="button" class="a-btn a-sec" data-completa>Pantalla completa ↗</button>
          <button type="button" class="a-btn a-sec" data-volver>Volver al código de partida</button></div>
        <p class="a-explica">Cada vez que pulsas Ejecutar, tu código se guarda con tu nota.</p>
      </div>
      <div class="a-ed-col">
        <p class="a-etq">Lo que se ve</p>
        <iframe class="a-ed-vista" data-marco title="Resultado de tu código" allow="camera; microphone"
                sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
      </div>
    </div>"""


CSS_MOTOR["editor"] = """
.a-editor{display:grid;gap:16px;margin-top:12px}
@media(min-width:980px){.a-editor{grid-template-columns:1fr 1fr;align-items:start}}
.a-ed-col{display:grid;gap:8px;min-width:0}
.a-ed-code{width:100%;min-height:300px;padding:12px 14px;border-radius:8px;border:1px solid var(--line);
  background:#0B1020;color:#D7DEEC;font-family:var(--fm);font-size:clamp(12.5px,1.3vw,15px);line-height:1.5;
  resize:vertical;tab-size:4}
.a-ed-code:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.a-ed-vista{width:100%;min-height:330px;border:1px solid var(--line);border-radius:8px;background:#fff}
.a-editor .a-explica{font-size:12.5px;color:var(--mut)}
.a-ed-tabs{display:flex;gap:4px}
.a-ed-tab{min-height:36px;padding:0 14px;border-radius:8px 8px 0 0;border:1px solid var(--line);border-bottom:0;
  background:transparent;color:var(--mut);font-family:var(--fm);font-size:13px;cursor:pointer}
.a-ed-tab[aria-selected="true"]{background:#0B1020;color:#D7DEEC}
.a-ed-tab:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
/* los pasos, en una franja compacta encima del editor */
.a-pasos.a-pasos-fila{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:6px 14px;margin:4px 0 10px}
.a-pasos.a-pasos-fila li{grid-template-columns:22px 1fr;gap:8px;font-size:clamp(12.5px,1.2vw,14.5px);line-height:1.35;
  color:var(--tx2)}
.a-pasos.a-pasos-fila li::before{width:22px;height:22px;font-size:11.5px}
.a-editor .a-ed-code{min-height:260px}
.a-editor .a-ed-vista{min-height:290px}
"""

JS_MOTOR["editor"] = r"""
M.editor=function(r){
  var cfg=JSON.parse(r.dataset.cfg),ta=ver(r,'[data-codigo]'),marco=ver(r,'[data-marco]');
  var valores={py:cfg.py,html:cfg.html,css:cfg.css},tab=cfg.inicio;
  /* Arrancar Python cuesta: la primera vez baja unos 6 MB (Pyodide) y en una
     máquina del aula son decenas de segundos. Así que el marco se abre VACÍO
     en cuanto se llega a la diapositiva —mientras el docente explica— y cada
     Ejecutar solo le manda el programa nuevo por postMessage, sin recargar:
     de ~2 s por tirada a ~0,1 s. Si la tirada anterior no contestó (un ciclo
     infinito deja Python colgado) la siguiente recarga la página entera. */
  var CALIENTE='/editor.html?v='+encodeURIComponent(cfg.v);
  var slide=r.closest('.slide'),corrio=false,vivo=false,pendiente=false;
  function mostrar(k){
    valores[tab]=ta.value;tab=k;ta.value=valores[k];
    todos(r,'[data-tab]').forEach(function(b){b.setAttribute('aria-selected',String(b.dataset.tab===k));});
  }
  todos(r,'[data-tab]').forEach(function(b){on(b,'click',function(){mostrar(b.dataset.tab);});});
  function paquete(){
    valores[tab]=ta.value;
    var d={v:cfg.v,css:valores.css,html:valores.html,py:valores.py};
    return btoa(unescape(encodeURIComponent(JSON.stringify(d))));
  }
  function calentar(){
    /* Arrancar Python mueve varios megas y los compila: en Safari eso traba el
       hilo principal, y como la diapositiva entra con una animación por hijo,
       lo que se veía era media diapositiva congelada. Así que el marco no se
       enciende en el mismo momento de llegar: se espera a que la entrada
       termine y a que el navegador esté libre. */
    if(marco.getAttribute('src'))return;
    var ir=function(){if(!marco.getAttribute('src')){vivo=false;pendiente=false;marco.src=CALIENTE;}};
    setTimeout(function(){
      if(window.requestIdleCallback)requestIdleCallback(ir,{timeout:4000});else ir();
    },900);
  }
  function decir(m){try{marco.contentWindow.postMessage(m,location.origin);return true;}catch(e){return false;}}
  function duro(b){
    vivo=false;pendiente=false;
    marco.src='/editor.html?n='+Date.now()+'#'+b;
    fb(r,true,'Ejecutando… la primera vez tarda unos segundos en cargar Python.');
  }
  function correr(){
    var b=paquete();
    NOTA.codigo=JSON.stringify({py:valores.py,html:valores.html,css:valores.css});
    guardarNota();subirNota();
    gana(r);            // la práctica puntúa por hacerla: con ejecutarla basta

    corrio=true;
    if(vivo&&!pendiente&&decir({editor:'corre',codigo:b})){
      pendiente=true;fb(r,true,'Ejecutando…');return;
    }
    duro(b);
  }
  on(window,'message',function(e){
    if(e.origin!==location.origin||!e.data||e.source!==marco.contentWindow)return;
    if(e.data.editor==='aqui'){vivo=true;pendiente=false;}
    else if(e.data.editor==='listo')pendiente=false;
  });
  function limpiar(){
    /* Al salir de la diapositiva el programa se va; Python se queda caliente.
       Si el programa traía <script> (la cámara de la IA) se recarga el marco:
       apagar la cámara de verdad importa más que ahorrar el arranque. */
    if(!corrio)return;
    corrio=false;
    if(/<script/i.test(valores.html||'')||!vivo||pendiente){vivo=false;pendiente=false;marco.src=CALIENTE;}
    else decir({editor:'limpia'});
  }
  on(ver(r,'[data-correr]'),'click',correr);
  // La cámara de Teachable Machine a veces no arranca dentro de un marco.
  on(ver(r,'[data-completa]'),'click',function(){window.open('/editor.html#'+paquete(),'_blank','noopener');});
  on(ver(r,'[data-volver]'),'click',function(){
    valores={py:cfg.py,html:cfg.html,css:cfg.css};ta.value=valores[tab];limpiar();fb(r,null,'');
  });
  ta.value=valores[tab];
  function cerca(){
    /* Se calienta en cuanto la clase pasa de la portada, no al acercarse al
       editor.

       Arrancar Python mueve varios megas y los compila, y eso tiene que caer
       mientras el docente explica la teoría, que no tiene nada que tocar.
       Antes empezaba dos diapositivas antes del editor, y cuando se escribió
       eso, dos antes era la teoría; después se añadieron el taller y el
       segundo juego y «dos antes» pasó a ser justo encima del mini juego: la
       clase se quedaba frisada ahí, con el juego ya en pantalla. */
    if(!slide)return true;
    var ss=[].slice.call(document.querySelectorAll('.slide'));
    var hay=ss.indexOf(slide),ahora=ss.findIndex(function(x){return x.classList.contains('on');});
    // El `hay-2` queda de red por si alguna semana trae el editor pegado al
    // principio y la teoría no llega a la segunda diapositiva.
    return ahora<0||ahora>=Math.min(2,Math.max(hay-2,0));
  }
  cambios.push(function(){if(cerca())calentar();});
  if(cerca())calentar();
  pausas.push(limpiar);
};
"""



# La página donde corre el código de la clase. Se escribe en public/ al generar:
# PyScript necesita una página servida, no un srcdoc ni un blob.
PAGINA_EDITOR = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prueba tu codigo</title>
<style>
  body{margin:0;font-family:system-ui,-apple-system,sans-serif}
  #aviso{margin:0;padding:14px 16px;font-size:14px;color:#475569}
</style>
</head>
<body>
<p id="aviso">Cargando Python...</p>
<script>
(function(){
  var aviso = document.getElementById('aviso');
  function leer(h){
    try{ return JSON.parse(decodeURIComponent(escape(atob(h)))); }catch(e){ return null; }
  }
  var h = location.hash.slice(1);
  var inicial = h ? leer(h) : null;
  if(h && !inicial){ aviso.textContent = 'No pude leer el codigo.'; return; }
  var q = location.search.match(/[?&]v=([^&]*)/);
  var v = (inicial && inicial.v) || (q && decodeURIComponent(q[1])) || '2026.7.3';

  // El sitio del programa del estudiante. Python se arranca UNA vez por
  // pagina: cada Ejecutar solo vacia esto y vuelve a llenarlo, asi la clase
  // no paga el arranque del interprete en cada tirada.
  var hoja = document.createElement('style');
  document.head.appendChild(hoja);
  var caja = document.createElement('div');
  document.body.appendChild(caja);
  var puestos = [];

  // Lo que definio el programa anterior se olvida, para que una linea borrada
  // deje de funcionar de verdad. Va en su propio script: asi los numeros de
  // linea de los errores siguen siendo los que el estudiante ve.
  var BASE = 'import builtins as _b\n'
    + '_b._base = set(globals()) | {"_b", "_n"}\n'
    + 'try:\n'
    + '    import js as _js\n'
    + '    _js.pyListo()\n'
    + 'except Exception:\n'
    + '    pass\n';
  var OLVIDA = 'import builtins as _b\n'
    + 'for _n in [k for k in list(globals()) if not k.startswith("_") and k not in _b._base]:\n'
    + '    del globals()[_n]\n';
  // Esto corre DESPUES del programa del estudiante: le dice a la clase que
  // Python acabo. Si su programa se queda en un ciclo infinito nunca llega,
  // y entonces la clase sabe que el siguiente Ejecutar tiene que recargar.
  var FIN = 'try:\n'
    + '    import js as _js\n'
    + '    _js.parent.postMessage(_js.JSON.parse(\'{"editor":"listo"}\'), _js.location.origin)\n'
    + 'except Exception:\n'
    + '    pass\n';

  function py(txt){
    var s = document.createElement('script');
    s.type = 'py';
    s.textContent = txt;
    document.body.appendChild(s);
    puestos.push(s);
  }
  function pintar(d){
    // Fuera el programa anterior: sus <script type="py"> y la salida que
    // PyScript dejo colgada del body (<script-py>), que si no se acumula.
    puestos.forEach(function(s){ s.remove(); });
    puestos = [];
    [].forEach.call(document.querySelectorAll('script-py'), function(n){ n.remove(); });
    hoja.textContent = d.css || '';
    caja.innerHTML = d.html || '';
    // innerHTML no ejecuta scripts: se rehacen, en orden (la camara de la IA).
    [].forEach.call(caja.querySelectorAll('script'), function(v){
      var nuevo = document.createElement('script');
      [].forEach.call(v.attributes, function(a){ nuevo.setAttribute(a.name, a.value); });
      nuevo.text = v.text;
      nuevo.async = false;
      v.replaceWith(nuevo);
    });
    py(OLVIDA);
    py(d.py || '');
    py(FIN);
  }

  // La clase manda el programa por aqui; el marco contesta para que sepa que
  // esta vivo (si no contesta, la clase recarga la pagina entera).
  window.addEventListener('message', function(e){
    if(e.origin !== location.origin || !e.data) return;
    if(e.data.editor === 'corre'){
      var d = leer(e.data.codigo);
      if(!d) return;
      if(aviso){ aviso.remove(); aviso = null; }
      pintar(d);
    }else if(e.data.editor === 'limpia'){
      pintar({ css: '', html: '', py: '' });
    }
  });

  py(BASE);
  if(inicial) pintar(inicial);
  // La clase necesita saber que este marco entiende mensajes: si no lo dice,
  // cada Ejecutar vuelve al camino viejo (recargar la pagina).
  try{ parent.postMessage({ editor: 'aqui' }, location.origin); }catch(e){}
  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = 'https://pyscript.net/releases/' + v + '/core.css';
  document.head.appendChild(css);
  var core = document.createElement('script');
  core.type = 'module';
  core.src = 'https://pyscript.net/releases/' + v + '/core.js';
  // Lo llama Python en cuanto arranca de verdad (core.js cargado no es lo
  // mismo que el interprete listo: entre uno y otro hay varios megas).
  window.pyListo = function(){
    if(!aviso) return;
    if(inicial){ aviso.remove(); aviso = null; }
    else aviso.textContent = 'Python listo. Escribe tu codigo en la clase y pulsa Ejecutar.';
  };
  core.onerror = function(){ if(aviso) aviso.textContent = 'No se pudo cargar Python: revisa la conexion.'; };
  document.head.appendChild(core);
})();
</script>
</body>
</html>
"""




# ── Tu nota: se guarda al final, con nombre y sección ──────────────────────

def nota_html(nid):
    return f"""<div class="a-nota" data-act="nota">
      <div class="a-nota-grande"><b data-total>0</b><span>/ 100</span></div>
      <ul class="a-nota-lista" data-desglose></ul>
      <p class="a-explica a-nota-quien" data-quien></p>
    </div>"""


CSS_ACT += """
/* la nota */
.a-vale{display:inline-block;margin-left:10px;padding:2px 9px;border-radius:999px;border:1px solid var(--line);
  font-family:var(--fm);font-size:11px;letter-spacing:.06em;color:var(--mut);text-transform:none;vertical-align:middle}
.a-panel > .a-vale{margin:0 0 8px}
.a-vale-hecho{color:var(--a-ok);border-color:var(--a-ok)}
.a-nota{display:grid;gap:16px;max-width:760px}
.a-nota-grande{display:flex;align-items:baseline;gap:10px;font-family:var(--fd)}
.a-nota-grande b{font-size:clamp(64px,9vw,120px);line-height:1;color:var(--lvl)}
.a-nota-grande span{font-size:clamp(20px,2.4vw,30px);color:var(--mut)}
.a-nota-lista{list-style:none;margin:0;padding:0;display:grid;gap:4px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.a-nota-lista li{display:flex;justify-content:space-between;gap:12px;padding:7px 12px;border-radius:6px;
  background:var(--bg2);border:1px solid var(--line);font-size:14px}
.a-nota-lista li b{font-family:var(--fm)}
.a-nota-lista li.a-pendiente{opacity:.55}
.a-nota-form{display:grid;gap:12px}
@media(min-width:720px){.a-nota-form{grid-template-columns:1.4fr 1fr auto;align-items:end}}
.a-nota-form label{display:grid;gap:5px;font-size:13px;color:var(--mut);font-family:var(--fm)}
.a-nota-form .campo{min-height:44px;font-size:16px}
/* ejemplos correctos en la teoría */
.a-teo-ejemplos{padding:16px 18px;border-radius:10px;background:#0B1020;border:1px solid var(--line);border-top:3px solid var(--a-ok)}
.a-teo-ejemplos .a-etq{color:var(--a-ok);margin-bottom:10px}
.a-teo-cod{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.a-teo-cod code{font-family:var(--fm);font-size:clamp(17px,2vw,24px);color:#D7DEEC}
"""



# ── La montaña de las variables: escribir una línea bien = subir un escalón ─

def juego_montana(pr):
    din, mt = pr["dinamica"], pr["montana"]
    n = len(mt["misiones"])
    pasos = "".join(f"<li>{E(x)}</li>" for x in din["pasos"])
    repisas = "".join(f'<i class="a-mt-repisa" style="--k:{k}"></i>' for k in range(1, n + 1))
    return f"""<div class="a-montana" data-act="montana" data-cfg="{_cfg({"misiones": mt["misiones"]})}" style="--n:{n}">
      <div class="a-col">
        <details class="a-mt-din">
          <summary>Antes, en grupo · {E(din["titulo"])} · {din["minutos"]} min</summary>
          <ol>{pasos}</ol>
        </details>
        <div class="a-mt-mision"><p class="a-etq" data-num></p><p class="a-mt-pide" data-pide></p></div>
        <div class="a-mt-escribe">
          <input class="campo a-mt-in" data-linea autocomplete="off" spellcheck="false"
                 aria-label="Escribe tu línea de Python" placeholder="escribe aquí tu línea">
          <button type="button" class="a-btn" data-subir>Subir ▲</button>
        </div>
        <p class="a-mt-pista">Así se escribe: <code>nombre_de_la_caja = valor</code></p>
        {FB}
        <p class="a-etq">Tu programa</p>
        <pre class="a-mt-prog" data-prog></pre>
        <div class="a-acc"><button type="button" class="a-btn a-sec" data-reiniciar>Empezar de nuevo</button></div>
      </div>
      <div class="a-mt-vista" aria-hidden="true">
        <div class="a-mt-monte"></div>
        {repisas}
        <span class="a-mt-bandera">🚩</span>
        <span class="a-mt-yo" data-yo>🧗</span>
      </div>
    </div>"""


CSS_MOTOR["montana"] = _CSS_COL + _CSS_TALLER + """
.a-montana{display:grid;gap:22px;margin-top:10px}
@media(min-width:980px){.a-montana{grid-template-columns:1.1fr .9fr;align-items:start}}
.a-montana .a-col{gap:9px}
.a-mt-vista{position:relative;height:clamp(300px,42vh,400px);border-radius:12px;overflow:hidden;
  background:linear-gradient(#0d2240,#123a5c 55%,#1c4a6e)}
.a-mt-monte{position:absolute;inset:14% 4% 0 4%;background:linear-gradient(160deg,#58708f,#34485f 60%,#263647);
  clip-path:polygon(0 100%,50% 0,100% 100%)}
.a-mt-monte::after{content:"";position:absolute;inset:0;background:#e8eef6;clip-path:polygon(40% 20%,50% 0,60% 20%,55% 17%,50% 22%,45% 17%)}
.a-mt-repisa{position:absolute;width:12%;height:6px;border-radius:3px;background:rgba(255,255,255,.35);
  left:calc(8% + (var(--k) * 38% / var(--n)));bottom:calc(6% + (var(--k) * 72% / var(--n)))}
.a-mt-bandera{position:absolute;left:47%;top:6%;font-size:30px}
.a-mt-yo{position:absolute;font-size:34px;left:calc(6% + (var(--k,0) * 38% / var(--n)));
  bottom:calc(6% + (var(--k,0) * 72% / var(--n)));transition:left .6s cubic-bezier(.3,1.3,.5,1),bottom .6s cubic-bezier(.3,1.3,.5,1)}
.a-mt-yo.a-mt-resbala{animation:a-mt-resbala .45s}
@keyframes a-mt-resbala{30%{transform:translateX(-8px) rotate(-12deg)}60%{transform:translateX(6px) rotate(8deg)}}
.a-montana.a-cima .a-mt-yo{animation:a-mt-salta .6s 2}
@keyframes a-mt-salta{50%{transform:translateY(-14px)}}
@media (prefers-reduced-motion: reduce){.a-mt-yo{transition:none}.a-mt-yo.a-mt-resbala,.a-montana.a-cima .a-mt-yo{animation:none}}
"""

JS_MOTOR["montana"] = r"""
M.montana=function(r){
  var cfg=JSON.parse(r.dataset.cfg),mis=cfg.misiones,k=0,lineas=[];
  var inp=ver(r,'[data-linea]'),prog=ver(r,'[data-prog]'),yo=ver(r,'[data-yo]');
  // Qué le falta a la línea, dicho como lo diría el docente. null si está bien.
  function revisar(t,m){
    t=t.trim();
    if(!t)return 'Escribe una línea: el nombre de la caja, = y el valor.';
    if(t.indexOf('==')>-1)return 'Con == se compara. Para guardar es un solo =.';
    var i=t.indexOf('=');
    if(i<0)return 'Falta el signo = entre el nombre y el valor.';
    var izq=t.slice(0,i).trim(),der=t.slice(i+1).trim();
    if(!izq)return 'Falta el nombre de la caja antes del =.';
    if(/^\d+$/.test(izq)||/^["']/.test(izq))return 'El nombre va a la izquierda del = y el valor a la derecha.';
    if(/^\d/.test(izq))return 'Un nombre no puede empezar con un número.';
    if(/\s/.test(izq))return 'Un nombre no lleva espacios: júntalo con _ (como mis_puntos).';
    if(!/^[A-Za-z_][A-Za-z0-9_]*$/.test(izq))return 'En el nombre van letras sin tilde, números y _, nada más.';
    if(izq!==m.var)return 'La caja se tiene que llamar '+m.var+'.';
    if(!der)return 'Falta el valor después del =.';
    if(m.tipo==='str'){
      var q=der.match(/^(["'])(.*)\1$/);
      if(!q)return /["']/.test(der)?'Las comillas tienen que abrir y cerrar.':m.valor+' es texto: va entre comillas, así: "'+m.valor+'".';
      if(q[2]!==m.valor)return 'El texto tiene que ser "'+m.valor+'".';
      return null;
    }
    if(/["']/.test(der))return 'Es un número: va sin comillas.';
    if(!/^[\d\s+\-*()]+$/.test(der))return 'Aquí va un número, o una cuenta con números.';
    if(m.exige&&der.indexOf(m.exige)<0)return 'Escribe la cuenta con '+m.exige+': Python la hace por ti.';
    var v;try{v=Function('"use strict";return ('+der+');')();}catch(e){return 'Esa cuenta no está bien escrita.';}
    if(String(v)!==m.valor)return 'El valor tiene que dar '+m.valor+'.';
    return null;
  }
  function pintar(){
    r.style.setProperty('--k',k);yo.style.setProperty('--k',k);
    var m=mis[Math.min(k,mis.length-1)];
    ver(r,'[data-num]').textContent=k>=mis.length?'¡Cima!':'Misión '+(k+1)+' de '+mis.length;
    ver(r,'[data-pide]').textContent=k>=mis.length?'Escribiste '+mis.length+' variables sin ayuda.':m.pide;
    prog.textContent=lineas.length?lineas.join('\n'):'# aquí van apareciendo tus líneas';
    inp.disabled=k>=mis.length;ver(r,'[data-subir]').disabled=k>=mis.length;
    r.classList.toggle('a-cima',k>=mis.length);
  }
  function subir(){
    if(k>=mis.length)return;
    var t=inp.value,falla=revisar(t,mis[k]);
    if(falla){
      fb(r,false,falla);
      yo.classList.remove('a-mt-resbala');void yo.offsetWidth;yo.classList.add('a-mt-resbala');
      return;
    }
    lineas.push(t.trim().replace(/\s*=\s*/,' = '));k++;inp.value='';
    if(k>=mis.length){gana(r);fb(r,true,'¡Llegaste a la cima! Cada línea guarda un valor en una caja con nombre.');}
    else fb(r,true,'¡Bien escrita! Subes un escalón.');
    pintar();inp.focus();
  }
  on(ver(r,'[data-subir]'),'click',subir);
  on(inp,'keydown',function(e){if(e.key==='Enter'){e.preventDefault();subir();}});
  on(ver(r,'[data-reiniciar]'),'click',function(){k=0;lineas=[];inp.value='';fb(r,null,'');pintar();});
  pintar();
};
"""

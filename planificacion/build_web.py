# -*- coding: utf-8 -*-
"""Genera plan-programacion.html a partir de contenido.py"""
import sys, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contenido as C

E = lambda s: html.escape(str(s), quote=False)

# Dónde vive la presentación. Cambia según dónde se sirva esta página: como
# artifact suelto apunta al enlace publicado; dentro de la app, a su ruta
# local, que abre sin internet y sin pedir sesión.
ENLACE_PRESENTACION = "https://claude.ai/code/artifact/b274057a-a83c-4bce-87ff-2bbc6cc386ff"

# El botón «Proyectar» lleva a una ruta de la app. En la página suelta —la que
# se publica como enlace y se imprime— esa ruta no existe, así que serían 36
# enlaces muertos. Solo se pinta en las páginas que sirve la app.
MOSTRAR_PROYECTAR = False

# ---------------------------------------------------------------- HORARIO GRID
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
# (etiqueta_hora, rango, [celdas por dia])  celda = (texto, tipo, rowspan|0)
# tipo: clase | cocu | admin | pausa | vacio
GRID = [
    ("1ra", "8:00 – 8:50", [
        ("Diseño de soluciones tecnológicas", "admin", 2),
        ("Planificación", "admin", 1),
        ("1ro A", "clase", 1), ("2do A", "clase", 1), ("2do B", "clase", 1)]),
    ("2da", "8:50 – 9:40", [
        (None, None, 0),
        ("Desarrollo de proyectos", "admin", 2),
        ("Atención a padres", "admin", 1), ("2do C", "clase", 1), ("3ro A", "clase", 1)]),
    ("3ra", "9:40 – 10:25", [
        ("", "vacio", 1), (None, None, 0),
        ("Planificación", "admin", 1), ("Planificación", "admin", 1), ("1ro C", "clase", 1)]),
    ("—", "10:25 – 10:55", [("RECESO", "pausa", 1)]),
    ("4ta", "10:55 – 11:45", [
        ("Planificación", "admin", 1),
        ("Diseño de soluciones tecnológicas", "admin", 2),
        ("Desarrollo de proyectos", "admin", 2),
        ("3ro B", "clase", 1), ("", "vacio", 1)]),
    ("5ta", "11:45 – 12:30", [
        ("", "vacio", 1), (None, None, 0), (None, None, 0),
        ("1ro B", "clase", 1), ("Diseño de soluciones tecnológicas", "admin", 1)]),
    ("6ta", "12:30 – 13:15", [
        ("Desarrollo de proyectos", "admin", 1), ("", "vacio", 1),
        ("Planificación", "admin", 1), ("3ro C", "clase", 1), ("", "vacio", 1)]),
    ("—", "13:15 – 14:15", [("ALMUERZO", "pausa", 1)]),
    ("7ma · 8va", "14:15 – 15:45", [
        ("Cocurricular", "cocu", 1), ("Cocurricular", "cocu", 1), ("Cocurricular", "cocu", 1),
        ("Cocurricular", "cocu", 1), ("Desarrollo de proyectos", "admin", 1)]),
    ("—", "15:45 – 16:00", [("Organización y salida", "pausa", 1)]),
]

def grid_html():
    out = ['<div class="scrollx"><table class="timetable"><thead><tr><th class="th-h">Hora</th>']
    for d in DIAS:
        out.append(f'<th>{E(d)}</th>')
    out.append('</tr></thead><tbody>')
    for etq, rango, celdas in GRID:
        out.append('<tr>')
        out.append(f'<th class="th-h"><span class="hh">{E(etq)}</span><span class="hr">{E(rango)}</span></th>')
        if len(celdas) == 1 and celdas[0][1] == "pausa":
            out.append(f'<td class="c-pausa" colspan="5">{E(celdas[0][0])}</td>')
        else:
            for txt, tipo, rs in celdas:
                if txt is None:
                    continue
                span = f' rowspan="{rs}"' if rs > 1 else ''
                if tipo == "vacio":
                    out.append(f'<td class="c-vacio"{span}></td>')
                else:
                    out.append(f'<td class="c-{tipo}"{span}><span>{E(txt)}</span></td>')
        out.append('</tr>')
    out.append('</tbody></table></div>')
    return "".join(out)

# ------------------------------------------------------------------- SECCIONES
def semanas_html(nivel):
    """Las 12 semanas, agrupadas bajo la fase a la que pertenecen.

    Antes eran doce filas seguidas y había que leer los doce títulos para
    darse cuenta de que 1ro pasa de bloques a código en la semana 8. Con las
    fases visibles, eso se ve de un vistazo."""
    nid = nivel["id"]
    out = [f'<div class="weeks" id="weeks-{nid}">']
    porfase = {}
    for f in nivel["fases"]:
        a, b = f["semanas"]
        for n in range(a, b + 1):
            porfase[n] = f
    fase_actual = None
    for s in nivel["semanas"]:
        fase = porfase.get(s["n"])
        if fase is not None and fase is not fase_actual:
            fase_actual = fase
            a, b = fase["semanas"]
            rango = f"Semana {a}" if a == b else f"Semanas {a}–{b}"
            out.append(f'''<div class="fase">
      <span class="fase-rango">{E(rango)}</span>
      <h4 class="fase-titulo">{E(fase["titulo"])}</h4>
      <p class="fase-nota">{E(fase["nota"])}</p>
    </div>''')
        wid = f"{nid}-{s['n']}"
        out.append(f'''<article class="week" data-lvl="{nid}">
  <button class="week-head" aria-expanded="false" aria-controls="body-{wid}" id="head-{wid}">
    <span class="wnum">{s['n']:02d}</span>
    <span class="wtxt"><span class="wtema">{E(s['tema'])}</span>
      <span class="wobj">{E(s['objetivo'])}</span></span>
    <span class="wchev" aria-hidden="true"></span>
  </button>
  <div class="week-body" id="body-{wid}" role="region" aria-labelledby="head-{wid}" hidden>
    <ol class="rail">''')
        for rango, etq, txt in s["bloques"]:
            out.append(f'''<li class="rail-row">
        <span class="rmin">{E(rango)}</span>
        <span class="rlab">{E(etq)}</span>
        <span class="rtxt">{E(txt)}</span></li>''')
        out.append(f'''<li class="rail-row is-extra">
        <span class="rmin">+5</span>
        <span class="rlab">Sube de nivel</span>
        <span class="rtxt">{E(s['extra'])} <em>Solo en bloques de 50 minutos.</em></span></li>''')
        out.append(f'''</ol>
    <div class="wmeta">
      <div><h4>Recursos</h4><p>{E(s['recursos'])}</p></div>
      <div><h4>Evidencia que se recoge</h4><p>{E(s['evidencia'])}</p></div>
    </div>
    {f'<a class="proyectar" href="/curso/{nid}/semana/{s["n"]}">Proyectar esta clase &#8594;</a>' if MOSTRAR_PROYECTAR else ''}
  </div>
</article>''')
    out.append('</div>')
    return "".join(out)

def nivel_html(nivel):
    nid, col = nivel["id"], nivel["color"]
    ruta = "".join(
        f'<li>{E(f["titulo"])}</li>' for f in nivel["fases"]
    )
    return f'''<section class="level lvl-{col}" id="{nid}">
  <header class="level-head">
    <p class="eyebrow">{E(nivel['titulo'])}</p>
    <h2>{E(nivel['nombre'])}</h2>
    <p class="lead">{E(nivel['resumen'])}</p>
    <ol class="ruta">{ruta}</ol>
  </header>
  <div class="proposito"><h3>Propósito del curso</h3><p>{E(nivel['proposito'])}</p></div>
  <div class="weeks-bar">
    <span>12 semanas</span>
    <button class="mini" data-toggle-all="{nid}">Abrir todas</button>
  </div>
  {semanas_html(nivel)}
</section>'''



def dias_html():
    LVL = {"1": "n1", "2": "n2", "3": "n3"}
    cards = []
    for d in C.SEMANA_DIAS:
        n = d["clases"]
        etq = "sin clases" if n == 0 else ("1 clase" if n == 1 else f"{n} clases")
        heavy = " is-heavy" if n >= 5 else (" is-free" if n == 0 else "")
        filas = []
        for hora, que, tipo in d["bloques"]:
            if tipo == "clase":
                cl = f"lvl-{LVL[que[0]]}"
                filas.append(f'''<li class="db is-clase {cl}">
          <span class="dbh">{E(hora)}</span>
          <span class="dbq">{E(que)}</span>
          <span class="dbt">{E(que[:3])} de secundaria</span></li>''')
            else:
                filas.append(f'''<li class="db is-{tipo}">
          <span class="dbh">{E(hora)}</span>
          <span class="dbq">{E(que)}</span></li>''')
        cards.append(f'''<article class="day{heavy}">
      <header><h4>{E(d["dia"])}</h4><span class="daycount">{E(etq)}</span></header>
      <ol class="dblocks">{"".join(filas)}</ol>
      <p class="daynote">{E(d["nota"])}</p>
    </article>''')
    return f'''<h3 class="sub" id="dias">Tu semana, día por día</h3>
  <p class="lead">{E(C.SEMANA_DIAS_INTRO)}</p>
  <div class="days">{"".join(cards)}</div>'''


def semana1_html(solo_nivel: str | None = None):
    fijo = "".join(f'''<li class="rail-row"><span class="rmin">{E(a)}</span>
      <span class="rlab">{E(b)}</span><span class="rtxt">{E(c)}</span></li>''' for a, b, c in C.SEMANA1_FIJO)
    dins, extras = [], []
    for d in C.SEMANA1_DINAMICAS:
        # En la página de un nivel solo interesa SU dinámica: las otras dos
        # son para grupos que ese día no están en el aula.
        if solo_nivel and d["nivel"].lower() != solo_nivel.lower():
            continue
        # El guion por minutos y los juegos de reserva son opcionales: solo se
        # pintan si el nivel ya los tiene en contenido.py. En la página general
        # llevan el nivel en el título, porque salen los tres seguidos.
        cola = "" if solo_nivel else f" · {E(d['nivel'])}"
        guion = d.get("guion") or []
        juegos = d.get("juegos") or []
        if guion:
            filas = "".join(f'''<li class="rail-row"><span class="rmin">{E(a)}</span>
      <span class="rlab">{E(b)}</span><span class="rtxt">{E(c)}</span></li>''' for a, b, c in guion)
            extras.append(f'''<div class="lvl-{d['color']}">
  <h3 class="sub">Guion minuto a minuto{cola}</h3>
  <ol class="rail rail-solo">{filas}</ol></div>''')
        if juegos:
            cartas = "".join(f'''<article class="bd">
        <h4>{E(n)}</h4>
        <p class="bd-tags"><span class="tag-t">{E(dur)}</span></p>
        <p>{E(desc)}</p>
        <p class="bd-goal"><span>Cuándo</span> {E(cuando)}<br><span>Materiales</span> {E(mat)}</p>
      </article>''' for n, dur, desc, mat, cuando in juegos)
            extras.append(f'''<div class="lvl-{d['color']}">
  <h3 class="sub">Juegos para elegir{cola}</h3>
  <div class="bd-grid">{cartas}</div></div>''')
        dins.append(f'''<article class="din lvl-{d['color']}">
      <header><span class="din-lvl">{E(d['nivel'])}</span><span class="din-dur">{E(d['duracion'])}</span></header>
      <h4>{E(d['nombre'])}</h4>
      <p>{E(d['desc'])}</p>
      <dl>
        <dt>Materiales</dt><dd>{E(d['materiales'])}</dd>
        <dt>Cierre</dt><dd>{E(d['cierre'])}</dd>
        <dt>Si sobra tiempo</dt><dd>{E(d['extra'])}</dd>
      </dl>
    </article>''')
    return f'''<section id="semana1">
  <header class="sec-head">
    <p class="eyebrow">Arranque</p>
    <h2>La primera semana</h2>
    <p class="lead">{E(C.SEMANA1_INTRO)}</p>
  </header>
  <a class="tarjeta-enlace" href="{ENLACE_PRESENTACION}">
    <span class="te-eyebrow">Material listo</span>
    <span class="te-titulo">Presentación de la primera clase</span>
    <span class="te-texto">Nueve diapositivas para proyectar. Trae un selector de nivel: pulsas
      1ro, 2do o 3ro y cambian la lista de la clase, lo que van a construir y el reto del día.
      Se avanza con las flechas.</span>
    <span class="te-flecha" aria-hidden="true">Abrir &#8594;</span>
  </a>

  <h3 class="sub">Bloque fijo · los primeros 20 minutos, igual en los tres niveles</h3>
  <ol class="rail rail-solo">{fijo}</ol>
  <h3 class="sub">Dinámica preparada · se lleva el resto de la clase</h3>
  <div class="din-grid">{"".join(dins)}</div>
  {"".join(extras)}
</section>'''


def cocu_html():
    """El cocurricular, que ya no es un taller de pantalla sino el Programa Maker.

    Son dos carriles con públicos distintos —primaria el lunes, secundaria de
    martes a jueves— y se muestran como tales: mezclarlos en una sola tabla
    escondía que son dos programas."""
    # Sin programas no hay sección: una cabecera «Cocurricular» con nada
    # debajo se lee como un error, no como una ausencia a propósito.
    if not C.MAKER_PROGRAMAS:
        return ""
    bloques = []
    for pr in C.MAKER_PROGRAMAS:
        mods = []
        for t in pr["talleres"]:
            ses = [x for x in pr["sesiones"] if x["n"] in t["sesiones"]]
            filas = "".join(f'''<article class="cs">
        <span class="cs-n">{x["n"]:02d}</span>
        <div><h5>{E(x["titulo"])}</h5><p>{E(x["proposito"])}</p>
        <p class="cs-mat"><span>En la mesa</span> {E(x["materiales"])}</p>
        <p class="cs-ev"><span>Se llevan</span> {E(x["evidencia"])}</p></div>
      </article>''' for x in ses)
            mods.append(f'''<div class="cmod">
      <header><h4>Taller {t["n"]} · {E(t["titulo"])}</h4>
        <span class="cmod-w">{E(t["horas"])}</span></header>
      <p class="cmod-meta">Producto: {E(t["producto"])}</p>
      <div class="cs-list">{filas}</div>
    </div>''')
        bloques.append(f'''<div class="via">
  <header class="via-cab">
    <h3>{E(pr["nombre"])}</h3>
    <span class="via-pub">{E(pr["publico"])}</span>
  </header>
  <p class="lead">{E(pr["resumen"])}</p>
  <p class="nota">{E(pr["nota"])}</p>
  <div class="cmods">{"".join(mods)}</div>
</div>''')

    return f'''<section id="cocurricular" class="lvl-co">
  <header class="sec-head">
    <p class="eyebrow">Cocurricular</p>
    <h2>Programa Maker</h2>
    <p class="lead">{E(C.MAKER_INTRO)}</p>
  </header>
  {"".join(bloques)}
</section>'''


def dinamicas_html(solo_nivel: str | None = None):
    grupos = []
    for g in C.DINAMICAS:
        # «1ro · 2do» o «Todos»: se queda lo que aplica a este nivel.
        vistos = [it for it in g["items"]
                  if not solo_nivel or "todos" in it[2].lower() or solo_nivel.lower() in it[2].lower()]
        if not vistos:
            continue
        items = "".join(f'''<article class="bd">
        <h4>{E(n)}</h4>
        <p class="bd-tags"><span class="tag-t">{E(dur)}</span><span class="tag-n">{E(niv)}</span></p>
        <p>{E(desc)}</p>
        <p class="bd-goal"><span>Enseña</span> {E(goal)}</p>
      </article>''' for n, dur, niv, desc, goal in vistos)
        grupos.append(f'''<div class="bdgroup"><h3 class="sub">{E(g['grupo'])}</h3>
      <div class="bd-grid">{items}</div></div>''')
    return f'''<section id="dinamicas">
  <header class="sec-head">
    <p class="eyebrow">Plan B</p>
    <h2>Banco de dinámicas</h2>
    <p class="lead">{E(C.DINAMICAS_INTRO)}</p>
  </header>
  {"".join(grupos)}
</section>'''


def evaluacion_nivel():
    """Evaluación y rúbrica, sin las tablas de herramientas y equivalencias:
    esas son del marco general y no cambian de un curso a otro."""
    filas = "".join(f'''<tr><td class="ev-c">{E(c)}</td>
      <td class="ev-p">{E(p)}</td><td>{E(q)}</td></tr>''' for c, p, q in C.EVALUACION)
    rub_h = "".join(f'<th>{E(n)}</th>' for n in C.RUBRICA_NIVELES)
    rub_r = "".join(
        '<tr><th class="rub-c">' + E(crit) + '</th>' + "".join(f'<td>{E(x)}</td>' for x in vals) + '</tr>'
        for crit, vals in C.RUBRICA)
    return f'''<section id="evaluacion">
  <header class="sec-head">
    <p class="eyebrow">Metodología</p>
    <h2>Cómo se evalúa</h2>
    <p class="lead">{E(C.EVALUACION_INTRO)}</p>
  </header>
  <div class="scrollx"><table class="tbl"><thead><tr><th>Componente</th><th>Valor</th><th>Qué se observa</th></tr></thead>
    <tbody>{filas}</tbody></table></div>
  <h3 class="sub">Rúbrica de proyecto</h3>
  <div class="scrollx"><table class="tbl tbl-rub"><thead><tr><th>Criterio</th>{rub_h}</tr></thead>
    <tbody>{rub_r}</tbody></table></div>'''


def evaluacion_html():
    filas = "".join(f'''<tr><td class="ev-c">{E(c)}</td>
      <td class="ev-p">{E(p)}</td><td>{E(q)}</td></tr>''' for c, p, q in C.EVALUACION)
    rub_h = "".join(f'<th>{E(n)}</th>' for n in C.RUBRICA_NIVELES)
    rub_r = "".join(
        '<tr><th class="rub-c">' + E(crit) + '</th>' + "".join(f'<td>{E(x)}</td>' for x in vals) + '</tr>'
        for crit, vals in C.RUBRICA)
    chuleta = "".join(f'<tr><td class="tr-quiero">{E(a)}</td><td class="tr-codigo">{E(b)}</td></tr>'
                      for a, b in C.PYTHON_EN_PAGINA)
    ent = "".join(f'''<tr><th>{E(n)}</th><td class="ent-d">{E(d)}</td><td>{E(u)}</td></tr>''' for n, d, u in C.ENTORNO)
    return f'''<section id="evaluacion">
  <header class="sec-head">
    <p class="eyebrow">Marco común</p>
    <h2>Evaluación, entorno y Python en la página</h2>
  </header>
  <h3 class="sub">Componentes y pesos</h3>
  <p class="lead">{E(C.EVALUACION_INTRO)}</p>
  <div class="scrollx"><table class="tbl"><thead><tr><th>Componente</th><th>Valor</th><th>Qué se observa</th></tr></thead>
    <tbody>{filas}</tbody></table></div>
  <h3 class="sub">Rúbrica de proyecto</h3>
  <div class="scrollx"><table class="tbl tbl-rub"><thead><tr><th>Criterio</th>{rub_h}</tr></thead>
    <tbody>{rub_r}</tbody></table></div>
  <h3 class="sub">Herramientas · todo funciona desde el navegador</h3>
  <div class="scrollx"><table class="tbl"><thead><tr><th>Herramienta</th><th>Dónde</th><th>Cuándo se usa</th></tr></thead>
    <tbody>{ent}</tbody></table></div>
  <h3 class="sub">Python en la página</h3>
  <p class="lead">Lo que se escribe para que el programa hable con la página. Todo el material usa estas formas y no otras. Punto de partida: {E(C.PLANTILLA)}.</p>
  <div class="scrollx"><table class="tbl tbl-trad"><thead><tr><th>Quiero…</th><th>Así en Python</th></tr></thead>
    <tbody>{chuleta}</tbody></table></div>
</section>'''


CSS = r"""
:root{
  --paper:#EFF3F8; --surface:#FFFFFF; --surface-2:#F7F9FC;
  --ink:#14213D; --ink-2:#33415C; --muted:#6B7A99;
  --rule:#DBE3ED; --rule-2:#C2CDDD;
  --l1:#1D4ED8; --l1-bg:#E7EEFD; --l2:#15803D; --l2-bg:#E4F4EA;
  --l3:#6D28D9; --l3-bg:#EFE9FC; --lco:#B45309; --lco-bg:#FBF0E1;
  --accent:var(--l1); --accent-bg:var(--l1-bg);
  --shadow:0 1px 2px rgba(20,33,61,.06), 0 8px 24px -18px rgba(20,33,61,.35);
  --f-disp:"Fraunces",Georgia,"Times New Roman",serif;
  --f-body:"Public Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --f-mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --wrap:1120px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0D1320; --surface:#141C2B; --surface-2:#1A2434;
  --ink:#E7EDF8; --ink-2:#BDC8DC; --muted:#8494B2;
  --rule:#26314A; --rule-2:#374561;
  --l1:#83A9FF; --l1-bg:#152647; --l2:#5FD08D; --l2-bg:#102D1E;
  --l3:#B79BFF; --l3-bg:#241B43; --lco:#F0A55A; --lco-bg:#3A2410;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -18px rgba(0,0,0,.9);
}}
:root[data-theme="dark"]{
  --paper:#0D1320; --surface:#141C2B; --surface-2:#1A2434;
  --ink:#E7EDF8; --ink-2:#BDC8DC; --muted:#8494B2;
  --rule:#26314A; --rule-2:#374561;
  --l1:#83A9FF; --l1-bg:#152647; --l2:#5FD08D; --l2-bg:#102D1E;
  --l3:#B79BFF; --l3-bg:#241B43; --lco:#F0A55A; --lco-bg:#3A2410;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -18px rgba(0,0,0,.9);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--f-body);font-size:16px;line-height:1.6;
  -webkit-font-smoothing:antialiased}
h1,h2,h3,h4,h5{font-family:var(--f-disp);font-weight:600;line-height:1.18;
  text-wrap:balance;margin:0;letter-spacing:-.012em}
p{margin:0}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 24px}
.scrollx{overflow-x:auto;-webkit-overflow-scrolling:touch}

/* ---------- masthead ---------- */
.mast{background:var(--surface);border-bottom:1px solid var(--rule)}
.mast-in{max-width:var(--wrap);margin:0 auto;padding:44px 24px 34px}
.kicker{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.mast h1{font-size:clamp(30px,4.6vw,46px);max-width:20ch;font-weight:600}
.mast .sub{margin-top:12px;color:var(--ink-2);font-size:17px;max-width:62ch}
.byline{margin-top:22px;padding-top:18px;border-top:1px solid var(--rule);
  display:flex;flex-wrap:wrap;gap:8px 28px;align-items:baseline}
.byline b{font-weight:600;font-size:15px}
.byline span{color:var(--muted);font-size:14px}
.stats{margin-top:26px;display:grid;gap:1px;background:var(--rule);
  border:1px solid var(--rule);grid-template-columns:repeat(2,1fr)}
@media(min-width:660px){.stats{grid-template-columns:repeat(4,1fr)}}
.stat{background:var(--surface);padding:14px 16px}
.stat b{display:block;font-family:var(--f-mono);font-size:22px;font-weight:600;
  color:var(--ink);font-variant-numeric:tabular-nums}
.stat span{font-size:12.5px;color:var(--muted);letter-spacing:.01em}

/* ---------- barra lateral ---------- */
.principal{min-width:0}
@media(min-width:1000px){
  body{display:grid;grid-template-columns:246px 1fr;align-items:start}
  .lateral{position:sticky;top:0;height:100dvh;overflow-y:auto}
}
.lateral{background:var(--surface);border-right:1px solid var(--rule);
  padding:26px 18px 40px;z-index:60}
.lat-marca{font-family:var(--f-disp);font-size:15px;line-height:1.35;color:var(--muted);
  margin-bottom:24px;padding-bottom:18px;border-bottom:1px solid var(--rule)}
.lat-marca b{color:var(--ink);font-weight:600}
.lat-bloque{margin-bottom:22px}
.lat-grupo{font-family:var(--f-mono);font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--muted);margin:0 0 8px;padding-left:11px}
.lateral a{display:block;padding:7px 11px;font-size:14.5px;color:var(--ink-2);
  text-decoration:none;border-radius:6px;border-left:2px solid transparent}
.lateral a:hover{background:var(--surface-2);color:var(--ink)}
.lateral a.on{color:var(--accent);border-left-color:var(--accent);
  background:var(--accent-bg);font-weight:600}
.lateral a:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.lat-fuera{color:var(--accent)!important;font-weight:600}
.lat-abrir{display:none;position:fixed;left:14px;bottom:14px;z-index:70;
  align-items:center;gap:9px;font:inherit;font-size:14px;font-weight:600;
  padding:11px 16px;border-radius:999px;cursor:pointer;
  background:var(--ink);color:var(--paper);border:0;
  box-shadow:0 6px 20px -6px rgba(0,0,0,.45)}
.lat-abrir span{display:block;width:15px;height:1.5px;background:currentColor;
  margin-bottom:3px}
.lat-abrir span:last-of-type{margin-bottom:0}
.lat-velo{display:none}
@media(max-width:999px){
  .lat-abrir{display:flex}
  .lateral{position:fixed;inset:0 auto 0 0;width:250px;transform:translateX(-102%);
    transition:transform .22s ease;box-shadow:0 0 40px rgba(0,0,0,.3)}
  .lateral.abierta{transform:none}
  .lat-velo:not([hidden]){display:block;position:fixed;inset:0;z-index:55;
    background:rgba(0,0,0,.45)}
}

/* ---------- secciones ---------- */
section{padding:56px 0 8px;scroll-margin-top:56px}
[id]{scroll-margin-top:64px}
.sec-head,.level-head{max-width:66ch}
.eyebrow{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent);margin-bottom:10px}
h2{font-size:clamp(24px,3.2vw,33px)}
.lead{margin-top:12px;color:var(--ink-2);font-size:16.5px}
.tagline{margin-top:8px;font-family:var(--f-mono);font-size:12.5px;color:var(--muted)}
h3.sub{margin:38px 0 14px;font-size:17px;font-weight:600;
  padding-bottom:8px;border-bottom:1px solid var(--rule)}
.nota{margin-top:22px;padding:16px 18px;background:var(--surface-2);
  border-left:2px solid var(--accent);font-size:14.5px;color:var(--ink-2)}
.nota strong{color:var(--ink)}

/* ---------- horario ---------- */
.timetable{width:100%;border-collapse:collapse;font-size:13px;min-width:760px}
.timetable th,.timetable td{border:1px solid var(--rule);padding:9px 10px;
  text-align:left;vertical-align:top}
.timetable thead th{background:var(--ink);color:var(--paper);font-family:var(--f-body);
  font-weight:600;font-size:12px;letter-spacing:.04em;text-transform:uppercase}
:root[data-theme="dark"] .timetable thead th{background:var(--surface-2);color:var(--ink)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .timetable thead th{
  background:var(--surface-2);color:var(--ink)}}
.th-h{background:var(--surface-2);width:104px;white-space:nowrap}
.hh{display:block;font-weight:600;font-size:12px}
.hr{display:block;font-family:var(--f-mono);font-size:11px;color:var(--muted);
  font-variant-numeric:tabular-nums}
.timetable td{background:var(--surface)}
.c-clase{background:var(--l1-bg)!important;font-weight:700;font-size:14px}
.c-clase span{color:var(--l1)}
.c-cocu{background:var(--lco-bg)!important;font-weight:600}
.c-cocu span{color:var(--lco)}
.c-admin span{color:var(--muted);font-size:12.5px}
.c-pausa{background:var(--surface-2)!important;text-align:center!important;
  font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--muted)}
.c-vacio{background:var(--surface-2)!important}
.legend{display:flex;flex-wrap:wrap;gap:6px 20px;margin-top:14px;font-size:13px;color:var(--muted)}
.legend i{display:inline-block;width:11px;height:11px;margin-right:7px;
  vertical-align:-1px;border:1px solid var(--rule-2)}
.lg1{background:var(--l1-bg)}.lg2{background:var(--lco-bg)}.lg3{background:var(--surface)}

/* ---------- listado de horas ---------- */
.hgrid{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  grid-template-columns:1fr;margin-top:20px}
@media(min-width:620px){.hgrid{grid-template-columns:repeat(3,1fr)}}
.hcell{background:var(--surface);padding:12px 14px;display:flex;
  justify-content:space-between;align-items:baseline;gap:10px}
.hcell b{font-size:15px;font-weight:700}
.hcell span{font-family:var(--f-mono);font-size:12px;color:var(--muted);
  font-variant-numeric:tabular-nums;text-align:right}
.hcell em{display:block;font-style:normal;font-size:11px;color:var(--muted)}

/* ---------- riel de minutos ---------- */
.rail{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.rail-solo{border:1px solid var(--rule);background:var(--surface)}
.rail-row{display:grid;grid-template-columns:66px 106px 1fr;gap:0 14px;
  padding:11px 14px;border-bottom:1px solid var(--rule);align-items:start}
.rail-row:last-child{border-bottom:0}
@media(max-width:620px){.rail-row{grid-template-columns:66px 1fr;gap:2px 12px}
  .rlab{grid-column:2}.rtxt{grid-column:1/-1;margin-top:4px}}
.rmin{font-family:var(--f-mono);font-size:12px;color:var(--accent);
  font-variant-numeric:tabular-nums;padding-top:2px;font-weight:600;white-space:nowrap}
.rlab{font-size:11px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);padding-top:3px;font-weight:600}
.rtxt{font-size:14.6px;color:var(--ink-2);line-height:1.58}
.rail-row.is-extra{background:var(--surface-2)}
.rail-row.is-extra .rtxt em{color:var(--muted);font-size:12.5px;font-style:normal;
  display:block;margin-top:3px}

/* ---------- niveles ---------- */
.lvl-n1{--accent:var(--l1);--accent-bg:var(--l1-bg)}
.lvl-n2{--accent:var(--l2);--accent-bg:var(--l2-bg)}
.lvl-n3{--accent:var(--l3);--accent-bg:var(--l3-bg)}
.lvl-co{--accent:var(--lco);--accent-bg:var(--lco-bg)}
.level{border-top:3px solid var(--accent);padding-top:34px;margin-top:34px}
.ruta{list-style:none;margin:22px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.ruta li{font-family:var(--f-mono);font-size:11.5px;padding:5px 10px;
  background:var(--accent-bg);color:var(--accent);border:1px solid var(--rule)}
.proposito{margin-top:26px;padding:18px 20px;background:var(--surface);
  border:1px solid var(--rule)}
.proposito h3{font-size:13px;letter-spacing:.08em;text-transform:uppercase;
  font-family:var(--f-body);color:var(--muted);margin-bottom:8px}
.proposito p{font-size:15px;color:var(--ink-2);max-width:74ch}
.weeks-bar{display:flex;justify-content:space-between;align-items:center;
  margin:30px 0 0;padding-bottom:9px;border-bottom:1px solid var(--rule)}
.weeks-bar>span{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted)}
.mini{font:inherit;font-size:12.5px;background:none;border:1px solid var(--rule-2);
  color:var(--ink-2);padding:4px 11px;cursor:pointer}
.mini:hover{border-color:var(--accent);color:var(--accent)}
.mini:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.weeks{border:1px solid var(--rule);border-top:0;background:var(--surface)}
.week+.week{border-top:1px solid var(--rule)}
.week-head{display:grid;grid-template-columns:52px 1fr 22px;gap:14px;width:100%;
  text-align:left;background:none;border:0;font:inherit;color:inherit;
  padding:15px 16px;cursor:pointer;align-items:start}
.week-head:hover{background:var(--surface-2)}
.week-head:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.wnum{font-family:var(--f-mono);font-size:19px;font-weight:600;color:var(--accent);
  font-variant-numeric:tabular-nums;line-height:1.3}
.wtema{display:block;font-family:var(--f-disp);font-size:17px;font-weight:600;
  line-height:1.28;text-wrap:balance}
.wobj{display:block;margin-top:5px;font-size:14px;color:var(--muted);line-height:1.5}
.wchev{width:11px;height:11px;margin-top:7px;border-right:1.5px solid var(--muted);
  border-bottom:1.5px solid var(--muted);transform:rotate(45deg);
  transition:transform .18s ease;justify-self:end}
.week-head[aria-expanded="true"] .wchev{transform:rotate(-135deg)}
.week-head[aria-expanded="true"]{background:var(--accent-bg)}
.week-body{padding:0 16px 18px}
.wmeta{display:grid;gap:1px;background:var(--rule);border:1px solid var(--rule);
  margin-top:16px;grid-template-columns:1fr}
@media(min-width:700px){.wmeta{grid-template-columns:1fr 1fr}}
.wmeta>div{background:var(--surface-2);padding:13px 15px}
.wmeta h4{font-family:var(--f-body);font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);margin-bottom:6px;font-weight:700}
.wmeta p{font-size:14px;color:var(--ink-2)}

/* ---------- fases dentro de un curso ---------- */
.fase{padding:16px 16px 14px;background:var(--accent-bg);
  border-bottom:1px solid var(--rule)}
.week+.fase,.fase+.week{border-top:0}
.fase-rango{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);font-weight:600}
.fase-titulo{margin:4px 0 3px;font-size:18px;font-weight:600}
.fase-nota{font-size:13.8px;color:var(--ink-2);max-width:66ch;line-height:1.5}

/* ---------- semana 1 ---------- */
.din-grid{display:grid;gap:16px;grid-template-columns:1fr}
@media(min-width:820px){.din-grid{grid-template-columns:repeat(3,1fr)}}
.din{background:var(--surface);border:1px solid var(--rule);
  border-top:3px solid var(--accent);padding:18px}
.din header{display:flex;justify-content:space-between;align-items:baseline;
  gap:10px;margin-bottom:10px}
.din-lvl{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--accent);font-weight:600}
.din-dur{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.din h4{font-size:19px;margin-bottom:9px}
.din>p{font-size:14.5px;color:var(--ink-2)}
.din dl{margin:14px 0 0;padding-top:12px;border-top:1px solid var(--rule);
  display:grid;grid-template-columns:1fr;gap:9px}
.din dt{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:700}
.din dd{margin:2px 0 0;font-size:13.8px;color:var(--ink-2)}

/* ---------- cocurricular ---------- */
.cmods{display:grid;gap:22px;margin-top:30px}
.cmod{border:1px solid var(--rule);background:var(--surface)}
.cmod header{display:flex;justify-content:space-between;align-items:baseline;
  gap:12px;flex-wrap:wrap;padding:15px 18px;background:var(--accent-bg);
  border-bottom:1px solid var(--rule)}
.cmod h4{font-size:19px}
.cmod-w{font-family:var(--f-mono);font-size:11.5px;color:var(--accent);font-weight:600}
.cmod-meta{padding:14px 18px;font-size:14.5px;color:var(--ink-2);
  border-bottom:1px solid var(--rule)}
.cs{display:grid;grid-template-columns:46px 1fr;gap:14px;padding:15px 18px}
.cs+.cs{border-top:1px solid var(--rule)}
.cs-n{font-family:var(--f-mono);font-size:16px;font-weight:600;color:var(--accent);
  font-variant-numeric:tabular-nums}
.cs h5{font-size:15.5px;font-family:var(--f-body);font-weight:700;margin-bottom:5px}
.cs p{font-size:14.2px;color:var(--ink-2)}
.cs-ev{margin-top:8px!important;font-size:13.2px!important}
.cs-ev span{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent);font-weight:700;margin-right:7px}

/* ---------- inicio: los tres cursos ---------- */
.mast-inicio{max-width:64ch;margin-bottom:8px}
.mast-inicio h1{font-size:clamp(30px,4.4vw,46px);margin-top:10px;max-width:20ch}
.mast-inicio .lead{margin-top:14px;font-size:17px}
.sub-primero{margin-top:34px}
.niveles-rejilla{display:grid;gap:16px;grid-template-columns:1fr;margin-top:4px}
@media(min-width:840px){.niveles-rejilla{grid-template-columns:repeat(3,1fr)}}
.nivel-tarjeta{display:grid;gap:7px;align-content:start;padding:22px 22px 20px;
  background:var(--surface);border:1px solid var(--rule);border-top:3px solid var(--accent);
  text-decoration:none;color:inherit;transition:border-color .16s ease,transform .16s ease}
.nivel-tarjeta:hover{border-color:var(--accent);transform:translateY(-2px)}
/* El número del curso, en grande y detrás del texto: es lo que se busca al
   entrar, y de lejos las tres tarjetas eran casi idénticas. Va marcado como
   decorativo porque el nombre del curso ya está escrito debajo; leerlo dos
   veces no ayuda a nadie con lector de pantalla. */
.nivel-tarjeta{position:relative;overflow:hidden}
.nt-curso{position:absolute;top:-14px;right:8px;font-family:var(--f-disp);
  font-weight:700;font-size:92px;line-height:1;color:var(--accent);opacity:.13;
  letter-spacing:-.05em;pointer-events:none;transition:opacity .18s,transform .18s}
.nivel-tarjeta:hover .nt-curso{opacity:.2;transform:translateY(2px)}
.nivel-tarjeta>*:not(.nt-curso){position:relative}
@media(prefers-reduced-motion:reduce){.nivel-tarjeta,.nt-curso{transition:none}}
.nivel-tarjeta:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.nt-eyebrow{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent)}
.nt-titulo{font-family:var(--f-disp);font-size:21px;font-weight:600;line-height:1.2;
  text-wrap:balance}
.nt-texto{font-size:14.2px;color:var(--ink-2);line-height:1.55;margin-top:2px}
.nt-fases{margin-top:8px;font-family:var(--f-mono);font-size:11px;color:var(--muted);
  line-height:1.6}
.nt-flecha{margin-top:12px;font-family:var(--f-mono);font-size:12px;color:var(--accent);
  font-weight:600}

/* ---------- botón de proyectar en cada semana ---------- */
.proyectar{display:inline-flex;align-items:center;gap:7px;margin-top:14px;
  padding:8px 14px;font-family:var(--f-mono);font-size:12px;font-weight:600;
  letter-spacing:.04em;text-decoration:none;color:var(--accent);
  background:var(--accent-bg);border:1px solid var(--rule)}
.proyectar:hover{border-color:var(--accent)}
.proyectar:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* ---------- tarjeta de enlace ---------- */
.tarjeta-enlace{display:grid;gap:6px;margin:24px 0 8px;padding:20px 22px;
  background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--accent);
  text-decoration:none;color:inherit;max-width:70ch;
  transition:border-color .16s ease, transform .16s ease}
.tarjeta-enlace:hover{border-color:var(--accent);transform:translateX(2px)}
.tarjeta-enlace:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.te-eyebrow{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent)}
.te-titulo{font-family:var(--f-disp);font-size:21px;font-weight:600;line-height:1.2}
.te-texto{font-size:14.5px;color:var(--ink-2);line-height:1.55;margin-top:2px}
.te-flecha{font-family:var(--f-mono);font-size:12.5px;color:var(--accent);
  font-weight:600;margin-top:6px}

.via{margin-top:34px;padding-top:26px;border-top:1px solid var(--rule)}
.via:first-of-type{border-top:0;padding-top:8px}
.via-cab{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.via-cab h3{font-family:var(--f-disp);font-size:23px;font-weight:600}
.via-pub{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--accent);font-weight:600}
.cs-mat{margin-top:8px!important;font-size:13.2px!important;color:var(--muted)}
.cs-mat span{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent);font-weight:700;margin-right:7px}

/* ---------- banco de dinamicas ---------- */
.bdgroup{margin-top:6px}
.bd-grid{display:grid;gap:14px;grid-template-columns:1fr}
@media(min-width:700px){.bd-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1000px){.bd-grid{grid-template-columns:repeat(3,1fr)}}
.bd{background:var(--surface);border:1px solid var(--rule);padding:16px 17px;
  display:flex;flex-direction:column}
.bd h4{font-size:16.5px;margin-bottom:8px}
.bd-tags{display:flex;gap:7px;margin-bottom:9px!important;flex-wrap:wrap}
.tag-t,.tag-n{font-family:var(--f-mono);font-size:10.5px;padding:2px 7px;
  border:1px solid var(--rule-2);color:var(--muted)}
.tag-t{background:var(--accent-bg);border-color:transparent;color:var(--accent);font-weight:600}
.bd>p{font-size:14px;color:var(--ink-2)}
.bd-goal{margin-top:auto;padding-top:11px;font-size:13px;
  border-top:1px solid var(--rule)}
.bd-goal span{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-weight:700;margin-right:6px}

/* ---------- tablas ---------- */
.tbl{width:100%;border-collapse:collapse;font-size:14.2px;background:var(--surface);
  min-width:540px}
.tbl th,.tbl td{border:1px solid var(--rule);padding:10px 13px;text-align:left;
  vertical-align:top}
.tbl thead th{background:var(--surface-2);font-family:var(--f-body);font-weight:700;
  font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.tbl td{color:var(--ink-2)}
.ev-c{font-weight:600;color:var(--ink)!important;width:27%}
.ev-p{font-family:var(--f-mono);font-weight:600;color:var(--accent)!important;
  width:9%;font-variant-numeric:tabular-nums}
.tbl-rub td{font-size:13.4px}
.rub-c{background:var(--surface-2);font-weight:700;color:var(--ink);width:20%;font-size:13.5px}
.tbl-trad{min-width:460px}
.tr-quiero{color:var(--ink)!important;font-weight:600;width:36%}
.tr-codigo{font-family:var(--f-mono);font-size:13px;color:var(--ink)!important;font-weight:500}
.ent-d{font-family:var(--f-mono);font-size:12.5px;width:22%}

/* ---------- aviso de scroll ---------- */
.swipe{display:none;margin-top:8px;font-family:var(--f-mono);font-size:11.5px;
  color:var(--accent);letter-spacing:.04em}
@media(max-width:860px){.swipe{display:block}}

/* ---------- la semana dia por dia ---------- */
.days{display:grid;gap:14px;grid-template-columns:1fr;margin-top:18px}
@media(min-width:760px){.days{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1060px){.days{grid-template-columns:repeat(3,1fr)}}
.day{background:var(--surface);border:1px solid var(--rule);
  border-top:3px solid var(--rule-2);padding:16px 17px;display:flex;flex-direction:column}
.day.is-heavy{border-top-color:var(--l1)}
.day.is-free{border-top-color:var(--rule-2)}
.day>header{display:flex;justify-content:space-between;align-items:baseline;
  gap:10px;margin-bottom:12px}
.day h4{font-size:19px}
.daycount{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;
  color:var(--muted);white-space:nowrap}
.day.is-heavy .daycount{color:var(--l1);font-weight:600}
.dblocks{list-style:none;margin:0;padding:0;border-top:1px solid var(--rule)}
.db{display:grid;grid-template-columns:92px 1fr;gap:0 12px;padding:7px 0;
  border-bottom:1px solid var(--rule);align-items:baseline}
.dbh{font-family:var(--f-mono);font-size:11.5px;color:var(--muted);
  font-variant-numeric:tabular-nums;white-space:nowrap}
.dbq{font-size:14px;color:var(--ink-2)}
.db.is-admin .dbq{color:var(--muted)}
.db.is-cocu .dbq{color:var(--lco);font-weight:600}
.db.is-clase .dbq{font-family:var(--f-mono);font-weight:600;font-size:15px;color:var(--accent)}
.dbt{grid-column:2;font-size:11px;color:var(--muted);letter-spacing:.02em}
.daynote{margin-top:13px;font-size:13.2px;color:var(--muted);line-height:1.5}
.day.is-heavy .daynote{color:var(--ink-2)}

/* ---------- footer ---------- */
footer{margin-top:64px;border-top:1px solid var(--rule);background:var(--surface)}
.foot-in{max-width:var(--wrap);margin:0 auto;padding:30px 24px 44px;
  display:flex;flex-wrap:wrap;gap:14px 30px;justify-content:space-between;align-items:baseline}
.prog{font-family:var(--f-disp);font-size:15.5px;color:var(--ink-2);max-width:62ch}
.foot-in small{color:var(--muted);font-size:12.5px;font-family:var(--f-mono)}

@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
@media print{
  nav.bar{display:none}
  body{background:#fff}
  .week-body[hidden]{display:block!important}
  .wchev,.mini{display:none}
  section{page-break-inside:auto;padding-top:24px}
  .week,.din,.bd,.cmod{page-break-inside:avoid}
}
"""

JS = r"""
var OPC={signal:typeof senal!=='undefined'?senal:undefined};
document.querySelectorAll('.week-head').forEach(function(b){
  b.addEventListener('click',function(){
    var open=b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded',String(!open));
    document.getElementById(b.getAttribute('aria-controls')).hidden=open;
  },OPC);
});
document.querySelectorAll('[data-toggle-all]').forEach(function(btn){
  btn.addEventListener('click',function(){
    var box=document.getElementById('weeks-'+btn.dataset.toggleAll);
    var open=btn.dataset.state==='open';
    box.querySelectorAll('.week-head').forEach(function(h){
      h.setAttribute('aria-expanded',String(!open));
      document.getElementById(h.getAttribute('aria-controls')).hidden=open;
    });
    btn.dataset.state=open?'closed':'open';
    btn.textContent=open?'Abrir todas':'Cerrar todas';
  },OPC);
});
var links=[].slice.call(document.querySelectorAll('.lateral a[href^="#"]'));
// getElementById y no querySelector: los identificadores de los cursos son
// «1ro», «2do» y «3ro», y un selector CSS no puede empezar por dígito.
// querySelector('#1ro') lanza SyntaxError y se llevaba por delante todo lo
// que venía detrás — el resaltado de sección y el cajón de móvil.
var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(!e.isIntersecting)return;
    var i=secs.indexOf(e.target);
    if(i<0)return;
    links.forEach(function(l){l.classList.remove('on');});
    links[i].classList.add('on');
  });
},{rootMargin:'-56px 0px -72% 0px'});
secs.forEach(function(s){if(s)io.observe(s);});
if(OPC.signal)OPC.signal.addEventListener('abort',function(){io.disconnect();});

// En móvil la lateral es un cajón. Se cierra al elegir una sección: dejarla
// abierta taparía justo lo que se acaba de pedir ver.
var lateral=document.getElementById('lateral');
var abrir=document.getElementById('latAbrir');
var velo=document.getElementById('latVelo');
function cajon(abierta){
  if(!lateral)return;
  lateral.classList.toggle('abierta',abierta);
  if(velo)velo.hidden=!abierta;
  if(abrir)abrir.setAttribute('aria-expanded',String(abierta));
}
if(abrir)abrir.addEventListener('click',function(){
  cajon(!lateral.classList.contains('abierta'));
},OPC);
if(velo)velo.addEventListener('click',function(){cajon(false);},OPC);
links.forEach(function(a){a.addEventListener('click',function(){cajon(false);},OPC);});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape')cajon(false);
},OPC);
"""


# ─────────────────────────────────────────────────────────────────────────
#  Una página por área
#
#  Todo esto era un único documento de 150 KB: para llegar a la semana 7 de
#  2do había que pasar por delante de 1ro entero. Se reparte en un área por
#  nivel, y cada una se basta sola —contenido y metodología juntos— para no
#  tener que cambiar de página con el grupo delante.
#
#  Las funciones de sección no cambian de sitio: solo se reparten.
# ─────────────────────────────────────────────────────────────────────────

AREAS = [
    ("/", "Inicio"),
    ("/curso/1ro", "1ro"),
    ("/curso/2do", "2do"),
    ("/curso/3ro", "3ro"),
    ("/presentaciones", "Presentaciones"),
]


def lateral_html(activa, secciones):
    """Arriba, en qué área estoy. Abajo, qué hay dentro de esta página."""
    areas = "".join(
        ('<a class="on" href="%s">%s</a>' % (h, E(t))) if h == activa
        else ('<a href="%s">%s</a>' % (h, E(t)))
        for h, t in AREAS
    )
    dentro = ""
    if secciones:
        enlaces = "".join('<a href="%s">%s</a>' % (h, E(t)) for h, t in secciones)
        dentro = '<div class="lat-bloque"><p class="lat-grupo">En esta página</p>%s</div>' % enlaces
    return '<div class="lat-bloque">%s</div>%s' % (areas, dentro)


def envoltura(titulo, descripcion, lateral, contenido):
    """El esqueleto común de todas las páginas."""
    return f"""<title>{E(titulo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Public+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>

<button class="lat-abrir" id="latAbrir" aria-expanded="false" aria-controls="lateral">
  <span></span><span></span><span></span> Secciones
</button>
<div class="lat-velo" id="latVelo" hidden></div>

<aside class="lateral" id="lateral">
  <p class="lat-marca">Programación<br><b>1ro a 3ro</b></p>
  <nav>{lateral}</nav>
</aside>

<div class="principal">
<main class="wrap">
{contenido}
</main>

<footer><div class="foot-in">
  <p class="prog">{E(descripcion)}</p>
  <small>{E(C.DOCENTE)} · {E(C.ESCUELA)}</small>
</div></footer>
</div>

<script>{JS}</script>"""


def _con_proyectar(fn, *args):
    """Enciende el botón de proyectar solo mientras se genera para la app."""
    global MOSTRAR_PROYECTAR
    antes = MOSTRAR_PROYECTAR
    MOSTRAR_PROYECTAR = True
    try:
        return fn(*args)
    finally:
        MOSTRAR_PROYECTAR = antes


def pagina_inicio():
    """La planificación: lo primero que ve un estudiante al entrar."""
    # Es por donde entra todo el mundo, así que la tarjeta dice de un vistazo
    # de qué curso es: el número grande primero y el nombre después. Antes
    # empezaba por «1RO · De la lógica…» en letra pequeña y las tres se
    # parecían demasiado como para distinguirlas de lejos.
    tarjetas = []
    for niv in C.NIVELES:
        fases = " · ".join(f["titulo"] for f in niv["fases"])
        tarjetas.append(f"""<a class="nivel-tarjeta lvl-{niv['color']}" href="/curso/{niv['id']}">
      <span class="nt-curso" aria-hidden="true">{E(niv['titulo'][:3])}</span>
      <span class="nt-eyebrow">{E(niv['titulo'])}</span>
      <span class="nt-titulo">{E(niv['nombre'])}</span>
      <span class="nt-texto">{E(niv['resumen'])}</span>
      <span class="nt-fases">{E(fases)}</span>
      <span class="nt-flecha">12 semanas &#8594;</span>
    </a>""")

    return envoltura(
        "Programación con Python · Secundaria",
        C.PROGRESION,
        # La barra ya sabía listar las secciones de la página; el inicio era la
        # única que no las usaba. «Enlaces útiles» se oculta solo cuando no hay
        # ninguno, igual que la sección.
        lateral_html("/", [("#niveles", "Los tres cursos"),
                           ("#enlaces", "Enlaces útiles"),
                           ("#mas", "Y además")]),
        f"""<header class="mast-inicio">
  <p class="eyebrow">{E(C.AREA)} · {E(C.ESCUELA)} · Año escolar 2026 – 2027</p>
  <h1>{E(C.TITULO)}</h1>
  <p class="lead">{E(C.SUBTITULO)}. Todo lo que damos en clase, en abierto: qué se ve cada
    semana, con qué se trabaja y cómo se evalúa.</p>
</header>

<section id="niveles">
  <h2 class="sub">Los tres cursos</h2>
  <div class="niveles-rejilla">{''.join(tarjetas)}</div>
</section>

<!-- El hueco de los enlaces. Nace oculto y lo rellena el navegador con lo que
     haya en la base: esta página se publica estática, así que si los enlaces
     se hornearan aquí, cambiar uno sería editar Python y volver a generar.
     Un título sobre un hueco vacío es peor que no tener la sección, por eso
     empieza con `hidden` y solo se muestra si hay algo que enseñar. -->
<section id="enlaces" hidden>
  <h3 class="sub">Enlaces útiles</h3>
  <div class="niveles-rejilla" data-enlaces></div>
</section>

<section id="mas">
  <h3 class="sub">Y además</h3>
  <div class="niveles-rejilla">
    <a class="nivel-tarjeta" href="/presentaciones">
      <span class="nt-eyebrow">Para proyectar</span>
      <span class="nt-titulo">Presentaciones</span>
      <span class="nt-texto">Las 36 clases curriculares y la de la primera clase,
        cada una lista para pantalla completa.</span>
      <span class="nt-flecha">Ver todas &#8594;</span>
    </a>
  </div>
</section>""")


def pagina_nivel(niv):
    """Un nivel entero: su contenido y su metodología, sin salir de aquí."""
    secciones = [("#" + niv["id"], "Las 12 semanas"), ("#clase", "Cómo es una clase"),
                 ("#semana1", "La primera semana"), ("#dinamicas", "Banco de dinámicas"),
                 ("#evaluacion", "Cómo se evalúa")]
    estruct = "".join(f"""<tr><td class="ev-c">{E(m)}</td>
      <td class="ev-p">{E(a)}</td><td class="ev-p">{E(b)}</td><td>{E(d)}</td></tr>"""
      for m, a, b, d in C.ESTRUCTURA_CLASE)

    return envoltura(
        f"{niv['titulo'][:3]} · {niv['nombre']}",
        niv["resumen"],
        lateral_html("/curso/" + niv["id"], secciones),
        f"""{_con_proyectar(nivel_html, niv)}

<section id="clase" class="lvl-{niv['color']}">
  <header class="sec-head">
    <p class="eyebrow">Metodología</p>
    <h2>Cómo es una clase</h2>
    <p class="lead">Las clases duran 45 o 50 minutos. Los minutos de más van a un reto
      opcional, nunca a más explicación.</p>
  </header>
  <div class="scrollx"><table class="tbl"><thead><tr>
    <th>Momento</th><th>45 min</th><th>50 min</th><th>Qué pasa</th></tr></thead>
    <tbody>{estruct}</tbody></table></div>
  <p class="nota"><strong>La regla que lo sostiene.</strong> {E(C.ESTRUCTURA_REGLA)}</p>
</section>

{semana1_html(niv['id'])}

{dinamicas_html(niv['id'])}

{evaluacion_nivel()}""")


def pagina_horario():
    """Solo para el docente: dice a qué hora está dónde y qué prepara cada día."""
    hcells = "".join(f"""<div class="hcell"><b>{E(sec)}</b>
      <span>{E(dia)}<em>{E(hora)} · {E(dur)}</em></span></div>"""
      for sec, dia, hora, dur in C.HORARIO_CLASES)
    return envoltura(
        "Horario",
        C.PROGRESION,
        "",
        f"""<section id="horario">
  <header class="sec-head">
    <p class="eyebrow">Punto de partida</p>
    <h2>El horario real</h2>
    <p class="lead">Nueve secciones repartidas en tres días, más cuatro tardes de cocurricular.
      Todo el desarrollo de las clases está calculado sobre estos bloques.</p>
  </header>
  {grid_html()}
  <p class="swipe">Desliza la tabla para ver jueves y viernes →</p>
  <p class="legend">
    <span><i class="lg1"></i>Clase de programación</span>
    <span><i class="lg2"></i>Cocurricular</span>
    <span><i class="lg3"></i>Planificación y otras funciones</span>
  </p>
  <h3 class="sub">Las nueve secciones</h3>
  <div class="hgrid">{hcells}</div>
  <p class="nota"><strong>El jueves es el día crítico.</strong> {E(C.HORARIO_NOTA)}</p>
</section>
{dias_html()}""")


# El menú, agrupado por para qué sirve cada cosa.
#
# Antes era una fila de once enlaces donde «3ro» y «Dinámicas» pesaban igual,
# y había que acordarse de cuál era cuál. Agrupados se lee en tres bloques:
# dónde estoy, qué curso, y qué necesito mientras doy clase.
MENU = [
    (None, [("#horario", "Horario"), ("#dias", "Mi semana")]),
    ("Cursos", [("#1ro", "1ro"), ("#2do", "2do"), ("#3ro", "3ro")]),
    ("En el aula", [("#clase", "Cómo es una clase"), ("#semana1", "Primera semana"),
                    ("#dinamicas", "Dinámicas")]),
    (None, [("#evaluacion", "Evaluación")]),
]

def menu_html():
    bloques = []
    for titulo, enlaces in MENU:
        cabecera = f'<p class="lat-grupo">{E(titulo)}</p>' if titulo else ""
        items = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in enlaces)
        bloques.append(f'<div class="lat-bloque">{cabecera}{items}</div>')
    bloques.append(
        f'<div class="lat-bloque"><a class="lat-fuera" href="{ENLACE_PRESENTACION}">'
        'Presentación &#8594;</a></div>'
    )
    return "".join(bloques)


def build(enlace_presentacion: str | None = None):
    global ENLACE_PRESENTACION
    if enlace_presentacion:
        ENLACE_PRESENTACION = enlace_presentacion
    nav = menu_html()

    hcells = "".join(f'''<div class="hcell"><b>{E(sec)}</b>
      <span>{E(dia)}<em>{E(hora)} · {E(dur)}</em></span></div>''' for sec, dia, hora, dur in C.HORARIO_CLASES)

    estruct = "".join(f'''<tr><td class="ev-c">{E(m)}</td>
      <td class="ev-p">{E(a)}</td><td class="ev-p">{E(b)}</td><td>{E(d)}</td></tr>'''
      for m, a, b, d in C.ESTRUCTURA_CLASE)

    niveles = "".join(nivel_html(n) for n in C.NIVELES)

    return f'''<title>Programación con Python · Secundaria</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Public+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>

<button class="lat-abrir" id="latAbrir" aria-expanded="false" aria-controls="lateral">
  <span></span><span></span><span></span> Secciones
</button>
<div class="lat-velo" id="latVelo" hidden></div>

<aside class="lateral" id="lateral">
  <p class="lat-marca">Programación<br><b>1ro a 3ro</b></p>
  <nav>{nav}</nav>
</aside>

<div class="principal">
<header class="mast">
  <div class="mast-in">
    <p class="kicker">{E(C.AREA)} · {E(C.ESCUELA)} · Año escolar 2026 – 2027</p>
    <h1>{E(C.TITULO)}</h1>
    <p class="sub">{E(C.SUBTITULO)}. Adaptación de la planificación del área: mismos objetivos y misma evaluación, con Python como lenguaje y HTML/CSS para la página.</p>
    <div class="byline"><b>{E(C.DOCENTE)}</b><span>Docente de Programación · 1ro a 3ro de Secundaria</span></div>
    <div class="stats">
      <div class="stat"><b>9</b><span>secciones a cargo</span></div>
      <div class="stat"><b>36</b><span>sesiones planificadas</span></div>
      <div class="stat"><b>12</b><span>semanas por nivel</span></div>
      <div class="stat"><b>4</b><span>tardes de cocurricular</span></div>
    </div>
  </div>
</header>

<main class="wrap">

<section id="horario">
  <header class="sec-head">
    <p class="eyebrow">Punto de partida</p>
    <h2>El horario real</h2>
    <p class="lead">Nueve secciones repartidas en tres días, más cuatro tardes de cocurricular. Todo lo que sigue está calculado sobre estos bloques, no sobre la sesión de 60 minutos de la planificación original.</p>
  </header>
  {grid_html()}
  <p class="swipe">Desliza la tabla para ver jueves y viernes →</p>
  <p class="legend">
    <span><i class="lg1"></i>Clase de programación</span>
    <span><i class="lg2"></i>Cocurricular</span>
    <span><i class="lg3"></i>Planificación y otras funciones</span>
  </p>
  <h3 class="sub">Las nueve secciones</h3>
  <div class="hgrid">{hcells}</div>
  {dias_html()}
  <p class="nota"><strong>El jueves es el día crítico.</strong> {E(C.HORARIO_NOTA)}</p>
  <p class="nota"><strong>Un punto a confirmar con coordinación.</strong> El PDF del horario rotula los bloques de lunes y miércoles como cocurricular de primaria. Esta planificación los trata como cocurricular de secundaria, según lo indicado. Si finalmente son de primaria, esos dos bloques usan Scratch y juegos visuales en lugar del arco de Python.</p>
</section>

<section id="clase">
  <header class="sec-head">
    <p class="eyebrow">Método</p>
    <h2>Cómo es una clase</h2>
    <p class="lead">La planificación original reparte 60 minutos. Las clases reales duran 45 o 50, así que el reparto se recomprime y el minuto sobrante de los bloques largos se destina a un reto opcional, no a más explicación.</p>
  </header>
  <div class="scrollx"><table class="tbl"><thead><tr>
    <th>Momento</th><th>45 min</th><th>50 min</th><th>Qué pasa</th></tr></thead>
    <tbody>{estruct}</tbody></table></div>
  <p class="nota"><strong>La regla que lo sostiene.</strong> {E(C.ESTRUCTURA_REGLA)}</p>
</section>

{semana1_html()}

{niveles}

{cocu_html()}

{dinamicas_html()}

{evaluacion_html()}

</main>

<footer><div class="foot-in">
  <p class="prog">{E(C.PROGRESION)}</p>
  <small>{E(C.DOCENTE)} · {E(C.ESCUELA)}</small>
</div></footer>
</div>

<script>{JS}</script>'''


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida", "plan-programacion.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print("escrito:", out, os.path.getsize(out), "bytes")

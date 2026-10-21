# -*- coding: utf-8 -*-
"""
Una presentación por sesión del Programa Maker: 16 de secundaria y 12 de primaria.

Estas no son clases de pantalla. Llevan una diapositiva que las curriculares no
tienen —los materiales— porque en un taller de 90 minutos con treinta personas,
saber qué tiene que estar en la mesa antes de empezar es la diferencia entre
construir y pasarse media hora buscando tijeras.

Y cuando la sesión tiene riesgo, la seguridad va en su propia diapositiva. El
manual de la escuela lo dice así: la seguridad no es una charla aparte, es una
condición para actuar.
"""
import os, sys, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C
import plegado as P
import palitos as PAL
from build_deck import CSS as CSS_BASE, JS as JS_BASE, CSS_PAG, JS_PAG, chrome_pag, botones_tema

E = lambda s: html.escape(str(s), quote=False)
SALIDA = os.path.join(HERE, "..", "asistente-aula", "src", "contenido", "taller")

# Naranja para secundaria, verde cálido para primaria, azul para Makers Space:
# en el pasillo se sabe de qué taller es la pantalla sin leer nada.
ACENTO = {"secundaria": "#E9A44C", "primaria": "#6FD08C", "space": "#5FA8F5",
          "chicas": "#E86AA8"}

CSS_EXTRA = """
.cinta{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:14px}
.cinta-num{font-family:var(--fd);font-weight:800;font-size:clamp(46px,10vw,128px);
  line-height:.85;color:var(--lvl);letter-spacing:-.04em}
.cinta-txt{font-family:var(--fm);font-size:clamp(10px,1.1vw,12px);letter-spacing:.15em;
  text-transform:uppercase;color:var(--mut);max-width:26ch;line-height:1.6}
.pasos{list-style:none;margin:32px 0 0;padding:0;display:grid;gap:15px;max-width:66ch;
  counter-reset:paso}
.pasos li{display:grid;grid-template-columns:38px 1fr;gap:16px;align-items:baseline;
  font-size:clamp(14.5px,1.85vw,21px);color:var(--tx2);line-height:1.42}
.pasos li::before{counter-increment:paso;content:counter(paso);font-family:var(--fm);
  font-size:clamp(13px,1.5vw,17px);color:var(--lvl);font-weight:600}
.mesa{margin-top:30px;padding:clamp(20px,2.6vw,30px);background:var(--bg2);
  border:1px solid var(--line);border-left:3px solid var(--lvl);max-width:64ch}
.mesa p{font-size:clamp(15px,1.9vw,22px);line-height:1.5}
.alerta{margin-top:30px;padding:clamp(20px,2.6vw,30px);max-width:64ch;
  background:rgba(233,120,120,.10);border:1px solid #E97878;border-left:3px solid #E97878}
.alerta p{font-size:clamp(14.5px,1.8vw,20px);line-height:1.5}
.alerta p+p{margin-top:12px;color:var(--tx2);font-size:clamp(13px,1.5vw,17px)}
.falta{color:#F0A55A;font-weight:600}
"""

# El paso a paso de un avión: un pliegue por diapositiva, dibujo a la izquierda
# e instrucción a la derecha. Se avanza con la flecha al ritmo al que la clase
# dobla, que es lo único que funciona con treinta personas siguiendo desde el
# fondo del aula.
CSS_AVIONES = """
/* ─── por qué vuela un avión ─── */
.fz-intro{margin-top:14px;font-size:clamp(16px,2vw,23px);color:var(--tx2);max-width:44ch;line-height:1.4}
.fz-lista{list-style:none;margin:20px 0 0;padding:0;display:grid;gap:10px;max-width:58ch}
.fz-lista li{display:grid;grid-template-columns:40px 1fr;column-gap:12px;align-items:start;padding:10px 14px;
  background:var(--bg2);border:1px solid var(--line);border-left:4px solid var(--fz);border-radius:6px}
.fz-lista i{grid-row:1/3;font-style:normal;font-size:26px;line-height:1.1;color:var(--fz);text-align:center}
.fz-lista b{font-family:var(--fd);font-size:clamp(17px,2vw,23px)}
.fz-lista span{color:var(--tx2);font-size:clamp(13.5px,1.5vw,17px);line-height:1.4}
.fz-fuente{margin-top:12px;font-size:12px;color:var(--mut)}
.fz-fuente a{color:inherit}
.fz-dibujo svg{width:100%;max-width:460px;height:auto;display:block;margin:0 auto;color:var(--tx)}
.fz-arriba{--fz:#3B82F6}.fz-abajo{--fz:#EF4444}.fz-adelante{--fz:#22C55E}.fz-atras{--fz:#F59E0B}
.pg{--dg-papel:rgba(150,200,235,.13);--dg-borde:#C6DCEE;
  --dg-marca:#6C8CA8;--dg-pliegue:var(--lvl)}
/* El papel se dibuja claro sobre oscuro; al invertir el fondo hay que invertir
   también el trazo, o el avión desaparece. */
[data-tema="claro"],[data-tema="pared"]{--dg-papel:rgba(20,45,75,.06);
  --dg-borde:#33475C;--dg-marca:#93A5B8;--dg-pliegue:var(--lvl)}
.pv{display:grid;gap:clamp(22px,4vw,56px);align-items:center;grid-template-columns:1fr}
@media(min-width:900px){.pv{grid-template-columns:1fr 1fr}}
/* Altura fija en el hueco y el SVG que la llena: los diagramas van de una hoja
   A4 de pie a una vista de frente apaisada, y con width:100% los altos se salen
   de una diapositiva 16:9 por abajo. El preserveAspectRatio por defecto centra
   el dibujo dentro sin deformarlo, sea alto o ancho. */
.pv-dib{height:min(62vh,540px);justify-self:center;width:100%}
.pv-dib .dg{width:100%;height:100%}
.pv-txt{font-family:var(--fd);font-weight:700;letter-spacing:-.02em;
  font-size:clamp(26px,4vw,52px);line-height:1.1;color:var(--tx);max-width:15ch}
.pv-de{font-family:var(--fm);font-size:clamp(11px,1.2vw,14px);letter-spacing:.14em;
  text-transform:uppercase;color:var(--mut);margin-top:26px}
.av-cinta{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;margin-bottom:16px}
.av-num{font-family:var(--fd);font-weight:800;font-size:clamp(52px,11vw,140px);
  line-height:.82;color:var(--lvl);letter-spacing:-.04em}
.av-que{font-family:var(--fm);font-size:clamp(10px,1.1vw,13px);letter-spacing:.15em;
  text-transform:uppercase;color:var(--mut)}
.av-mote{margin-top:10px;font-size:clamp(15px,2vw,24px);color:var(--tx2)}
.av-ficha{margin-top:26px;padding:14px 18px;background:var(--bg2);
  border-left:3px solid var(--lvl);font-size:clamp(14px,1.8vw,21px);
  line-height:1.4;color:var(--tx2);max-width:30ch}
.av-ficha b{color:var(--tx)}

/* El guion: la hora y el titular, nada más. El párrafo de cada bloque es nota
   para el docente y ya está en la sesión; proyectado no se lee y además no
   cabía: el último bloque se salía por debajo de la diapositiva. */
.agenda{list-style:none;margin:26px 0 0;padding:0;display:grid;gap:clamp(7px,1.1vh,13px)}
.agenda li{display:grid;grid-template-columns:clamp(72px,8vw,104px) 1fr;gap:16px;
  align-items:baseline;font-size:clamp(15px,2.1vw,27px);color:var(--tx);line-height:1.2}
.ag-min{font-family:var(--fm);font-size:clamp(11px,1.3vw,16px);color:var(--lvl);
  letter-spacing:.04em;font-variant-numeric:tabular-nums}
/* La escalera de un vistazo. Con el dibujo solo no basta: a este tamaño las
   vistas de frente del Dardo, el Planeador y el Delta son la misma Y. El
   nombre al lado es lo que las separa. */
.escalera{display:grid;gap:clamp(4px,1.2vh,14px);align-content:center}
.esc-t{font-family:var(--fm);font-size:clamp(10px,1.1vw,13px);letter-spacing:.18em;
  text-transform:uppercase;color:var(--mut);margin-bottom:6px}
.esc{display:grid;grid-template-columns:auto clamp(66px,8vw,104px) 1fr;gap:clamp(10px,1.4vw,18px);
  align-items:center}
.esc-n{font-family:var(--fm);font-size:clamp(11px,1.2vw,15px);color:var(--lvl)}
.esc-d{height:clamp(32px,5.6vh,52px)}
.esc-d .dg{width:100%;height:100%}
.esc-nom{font-size:clamp(14px,1.8vw,22px);color:var(--tx2);line-height:1.15}
"""




def _dibujos(pieza):
    """Los aviones traen la lista de pliegues; los palitos, el nombre del
    modelo. Es la única diferencia entre las dos guías, y se resuelve aquí para
    que el resto del archivo no tenga que saber cuál es cuál."""
    pasos = pieza["pasos"]
    if isinstance(pasos, str):
        return PAL.diagramas(PAL.MODELOS[pasos]())
    return P.diagramas(pasos)


def diapositivas_aviones(aviones, desplazamiento, rotulo="Avión"):
    """Portadilla y un paso por diapositiva, para cada pieza de la guía.

    Devuelve también dónde empieza y acaba cada avión. De ahí sale la
    paginación de dos niveles: con cincuenta y ocho diapositivas, llegar al
    Delta a golpe de flecha no es navegar, es rezar."""
    trozos, capitulos = [], []
    n = desplazamiento
    for av in aviones:
        inicio = n
        n += 1
        # El dibujo del último paso es el avión terminado: es la mejor
        # portada que puede tener, y ya está calculada.
        pasos = _dibujos(av)
        trozos.append(f"""
  <section class="slide">
   <div class="inner">
    <div class="pv">
     <div>
      <p class="eyebrow">Paso a paso · {rotulo} {av["n"]} de {len(aviones)}</p>
      <div class="av-cinta">
        <span class="av-num">{av["n"]}</span>
        <span class="av-que">Enseña<br>{E(av["ensena"])}</span>
      </div>
      <h1 class="mid">{E(av["nombre"])}</h1>
      <p class="av-mote">{E(av["apodo"])}</p>
      <p class="av-ficha"><b>Necesitas.</b> {E(av["materiales"])}</p>
     </div>
     <div class="pv-dib">{pasos[-1]["svg"]}</div>
    </div>
   </div>
  </section>""")
        for i, paso in enumerate(pasos, 1):
            n += 1
            # Solo la orden. El porqué y el truco están en `detalle`, que sale
            # en la guía de mano y no en la pared: desde el fondo del aula no
            # se lee un párrafo.
            trozos.append(f"""
  <section class="slide">
   <div class="inner">
    <div class="pv">
      <div>
        <p class="eyebrow">{E(av["nombre"])}</p>
        <p class="pv-txt">{E(paso["texto"])}</p>
        <p class="pv-de">Paso {i} de {len(pasos)}</p>
      </div>
      <div class="pv-dib">{paso["svg"]}</div>
    </div>
   </div>
  </section>""")
        capitulos.append({"t": av["nombre"].split(" ", 1)[-1], "a": inicio, "b": n - 1,
                          "tecla": str(av["n"])})
    return "".join(trozos), capitulos


# ═══ Un deck para programar ═════════════════════════════════════════════════
#
# La sesión del botón de Makers Space la escriben ellos. La misma página sirve
# a dos personas:
#   · el estudiante ve la META de cada paso (un dibujo de cómo debe quedar, que
#     puede descargar), las piezas que va a usar y su propio editor;
#   · el docente, con su sesión abierta, ve además la demo y decide cuándo
#     abrir el código de cada paso a la clase.
# El código NO viaja en esta página: el generador lo escribe aparte en
# `<n>.codigo.json`, y la app solo lo entrega por /api/taller/... al docente o,
# a los estudiantes, el de los pasos que él abrió hoy.

import difflib
import circuitos as CIR
from motor_actividades import PYSCRIPT_VERSION

# En el orden en que se construye una página: qué hay, cómo se ve, qué hace.
ARCHIVOS = (("html", "HTML"), ("css", "CSS"), ("py", "Python"))


def _nuevas(antes, ahora):
    """Los índices de las líneas de `ahora` que no estaban en `antes`."""
    a, b = antes.splitlines(), ahora.splitlines()
    nuevas = set()
    for op, _, _, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op in ("insert", "replace"):
            nuevas.update(range(j1, j2))
    return nuevas


def _pre(texto, nuevas):
    """El código con las líneas nuevas marcadas. El bloque nuevo más largo
    lleva además el ancla: es lo que el deck pone a la vista al llegar, que en
    el paso largo está abajo y no en el import de arriba."""
    lineas = texto.splitlines() or [""]
    ancla, mejor, i = None, 0, 0
    while i < len(lineas):
        if i in nuevas:
            j = i
            while j in nuevas:
                j += 1
            if j - i > mejor:
                ancla, mejor = i, j - i
            i = j
        else:
            i += 1
    return "".join(f'<span class="ln{" nuevo" if i in nuevas else ""}{" ancla" if i == ancla else ""}">{E(l) or " "}</span>'
                   for i, l in enumerate(lineas))


def _pasos(ses):
    """(id, botón, número de botón, número de paso, paso, id del anterior) en orden."""
    anterior = None
    for bn, boton in enumerate(ses["progresion"], 1):
        for pn, paso in enumerate(boton["pasos"], 1):
            pid = f"{bn}-{pn}"
            yield pid, boton, bn, pn, paso, anterior
            anterior = pid


def codigo_json(ses):
    """Lo que solo el servidor guarda: el código de cada paso, con el resaltado
    ya hecho, y el punto de partida de los botones que empiezan de cero."""
    pasos, previo = {}, {}
    for pid, boton, bn, pn, paso, _ in _pasos(ses):
        # Un botón que empieza de cero se compara con su punto de partida: el
        # CSS que ya les llega hecho no cuenta como línea nueva.
        antes = boton["base"] if pn == 1 and boton.get("base") else previo
        cambios = {k: _nuevas(antes.get(k, ""), paso[k]) for k, _ in ARCHIVOS}
        presentes = [k for k, _ in ARCHIVOS if paso[k].strip()]
        inicio = next((k for k in presentes if cambios[k]), presentes[0])
        pasos[pid] = {"html": paso["html"], "css": paso["css"], "py": paso["py"], "inicio": inicio,
                      "pre": {k: _pre(paso[k], cambios[k]) for k in presentes},
                      "cambios": [k for k in presentes if cambios[k]]}
        previo = paso
    return {"pasos": pasos}


# ─── La meta: cómo tiene que verse la página, dibujada ───────────────────────

_MW, _MH, _MG = 240, 158, 64           # ancho y alto de cada ventanita, hueco de la flecha


def _svg_boton(x, y, texto, h=26):
    w = round(len(texto) * 6.8 + 22)
    return w, (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="#efefef"/>'
               f'<text x="{x + w / 2}" y="{y + h / 2 + 4.5}" text-anchor="middle" font-size="12" fill="#111">{E(texto)}</text>')


def _svg_interruptor(x, y, spec):
    _, estado, *resto = spec.split(":")
    emoji = resto[0] if resto else "🌙"
    claro = estado == "claro"
    acento, fondo = ("#f59e0b", "#e2e8f0") if claro else ("#38bdf8", "#1e293b")
    cx = x + (41 if claro else 15)
    return 56, (f'<rect x="{x}" y="{y}" width="56" height="30" rx="15" fill="{fondo}" stroke="{acento}" stroke-width="2"/>'
                f'<circle cx="{cx}" cy="{y + 15}" r="11" fill="{acento}"/>'
                f'<text x="{cx}" y="{y + 19.5}" text-anchor="middle" font-size="12">{emoji}</text>')


def _svg_cuadro(x, c):
    """Una ventanita de navegador con la página tal como se ve en ese momento."""
    t = [f'<g><rect x="{x}" y="0" width="{_MW}" height="{_MH}" rx="10" fill="{c["fondo"]}" stroke="#94a3b8"/>'
         f'<path d="M{x} 10a10 10 0 0 1 10-10h{_MW - 20}a10 10 0 0 1 10 10v8h-{_MW}z" fill="#e2e8f0"/>']
    t += [f'<circle cx="{x + 12 + i * 10}" cy="9" r="3" fill="{col}"/>'
          for i, col in enumerate(("#f87171", "#fbbf24", "#34d399"))]
    # Filas: el título, los botones (se reparten en renglones) y el texto.
    filas = []
    if c["h1"]:
        filas.append(("h1", 22))
    renglones, actual, ancho = [], [], 0
    for b in c["botones"]:
        w = 56 if b.startswith("interruptor:") else round(len(b) * 6.8 + 22)
        if actual and ancho + 6 + w > _MW - 24:
            renglones.append(actual)
            actual, ancho = [], 0
        actual.append((b, w))
        ancho += (6 if ancho else 0) + w
    if actual:
        renglones.append(actual)
    for r in renglones:
        filas.append(("b", 32 if any(b.startswith("interruptor:") for b, _ in r) else 28, r))
    if c["p"]:
        filas.append(("p", 18))
    alto = sum(f[1] for f in filas) + 6 * max(0, len(filas) - 1)
    y = 18 + (_MH - 18 - alto) / 2
    for f in filas:
        if f[0] == "h1":
            t.append(f'<text x="{x + _MW / 2}" y="{y + 16}" text-anchor="middle" font-size="16" font-weight="700" fill="{c["tinta"]}">{E(c["h1"])}</text>')
        elif f[0] == "p":
            t.append(f'<text x="{x + _MW / 2}" y="{y + 13}" text-anchor="middle" font-size="12" fill="{c["tinta"]}">{E(c["p"])}</text>')
        else:
            total = sum(w for _, w in f[2]) + 6 * (len(f[2]) - 1)
            bx = x + (_MW - total) / 2
            for b, w in f[2]:
                if b.startswith("interruptor:"):
                    t.append(_svg_interruptor(bx, y, b)[1])
                else:
                    by = y + 1
                    if c["salto"]:
                        # El salto: el botón más grande y dos rayitas de movimiento.
                        cxb, cyb = bx + w / 2, by + 13
                        t.append(f'<g transform="translate({cxb} {cyb}) scale(1.3) translate({-cxb} {-cyb})">{_svg_boton(bx, by, b)[1]}</g>'
                                 f'<path d="M{bx - 12} {by + 4}l-6 -4M{bx - 12} {by + 22}l-6 4M{bx + w + 12} {by + 4}l6 -4M{bx + w + 12} {by + 22}l6 4" '
                                 f'stroke="{c["tinta"]}" stroke-width="2" stroke-linecap="round"/>')
                    else:
                        t.append(_svg_boton(bx, by, b)[1])
                bx += w + 6
        y += f[1] + 6
    t.append("</g>")
    if c["nota"]:
        t.append(f'<text x="{x + _MW / 2}" y="{_MH + 22}" text-anchor="middle" font-size="13" fill="#334155">{E(c["nota"])}</text>')
    return "".join(t)


def svg_meta(meta, pid):
    cuadros = meta["cuadros"]
    ancho = len(cuadros) * _MW + (len(cuadros) - 1) * _MG
    partes = []
    for i, c in enumerate(cuadros):
        x = i * (_MW + _MG)
        partes.append(_svg_cuadro(x, c))
        if i:
            ax = x - _MG + 8
            partes.append(f'<path d="M{ax} {_MH / 2}h{_MG - 22}" stroke="#2563eb" stroke-width="3"/>'
                          f'<path d="M{ax + _MG - 22} {_MH / 2 - 7}l10 7-10 7z" fill="#2563eb"/>'
                          f'<text x="{x - _MG / 2}" y="{_MH / 2 - 12}" text-anchor="middle" font-size="11.5" font-weight="700" fill="#2563eb">{E(meta["flecha"])}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -12 {ancho + 24} {_MH + 44}" '
            f'width="{ancho + 24}" height="{_MH + 44}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
            f'role="img" aria-label="La meta del paso {pid}">'
            f'<rect x="-12" y="-12" width="{ancho + 24}" height="{_MH + 44}" rx="14" fill="#ffffff"/>'
            + "".join(partes) + "</svg>")


NOMBRE = dict(ARCHIVOS)


def _escribe_en(paso, antes):
    """En qué archivos se escribe en este paso: los que cambian respecto a lo
    que ya tenían. Solo dice dónde, no qué: no delata el código."""
    return [k for k, _ in ARCHIVOS if _nuevas(antes.get(k, ""), paso[k])] or ["py"]


def diapositiva_codigo(pid, boton, bn, pn, paso, anterior, antes):
    escribe = _escribe_en(paso, antes)
    nombres = [NOMBRE[k] for k in escribe]
    donde = nombres[0] if len(nombres) == 1 else ", ".join(nombres[:-1]) + " y " + nombres[-1]
    piezas = "".join(f"<li><code>{E(x)}</code></li>" for x in paso["piezas"])
    tabs = "".join(
        f'<button type="button" role="tab" class="cd-tab{" obj" if k in escribe else ""}" data-tab="{k}">'
        f'{t}{"<span class=\"lapiz\" aria-label=\"aquí escribes\"> ✎</span>" if k in escribe else ""}</button>'
        for k, t in ARCHIVOS)
    base = boton.get("base") if pn == 1 else None
    extra = (f' data-base="{html.escape(json.dumps(base, ensure_ascii=False), quote=True)}"' if base else "")
    return f"""
  <section class="slide">
   <div class="inner cd" data-cd="{pid}" data-prev="{anterior or ""}" data-escribe="{",".join(escribe)}"{extra}>
    <p class="eyebrow">Botón {bn} · {E(boton["titulo"])} · paso {pn} de {len(boton["pasos"])}</p>
    <h2 class="cd-t">{E(paso["titulo"])}</h2>
    <p class="cd-frase">{E(paso["frase"])}</p>
    <div class="cd-cols">
     <div class="cd-izq">
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">1</span>La meta
        <button type="button" class="cd-mini" data-bajar>⬇ Descargar</button></h3>
       <figure class="cd-meta" data-meta>{svg_meta(paso["meta"], pid)}</figure>
      </div>
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">3</span><span data-h3>Tu resultado</span>
        <span class="cd-sub" data-sub>¿se ve como la meta?</span>
        <button type="button" class="cd-mini" data-completa title="Pantalla completa">↗</button></h3>
       <iframe class="cd-vista" data-marco title="Resultado" allow="camera"
         sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
      </div>
     </div>
     <div class="cd-der">
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">2</span><span data-h2>Escribe en {E(donde)}</span></h3>
       <div class="cd-candado" data-candado hidden>
        <span data-estado>🔒 Cerrado para la clase</span>
        <button type="button" class="cd-btn" data-dar>Dar el código</button>
       </div>
       <ul class="cd-piezas" aria-label="Piezas que vas a usar">{piezas}</ul>
       <div class="cd-barra">
        <div class="cd-tabs" role="tablist" aria-label="Qué parte del código">{tabs}</div>
        <button type="button" class="cd-mini" data-ojo hidden>👁 Ver</button>
        <button type="button" class="cd-mini" data-copiar hidden>⧉ Copiar</button>
       </div>
       <div class="cd-caja">
        <textarea class="cd-ta" data-ta spellcheck="false" wrap="off" aria-label="Tu código"
          placeholder="Escribe aquí tu código"></textarea>
        <div class="cd-pre" data-pre hidden></div>
        <p class="cd-cerrado" data-cerrado hidden>🔒 El código está cerrado.<br>Primero lo escriben ellos.</p>
       </div>
       <div class="cd-acc"><button type="button" class="cd-btn" data-correr>▶ Ejecutar</button></div>
       <div class="cd-ayuda" data-ayuda>
        <span data-ayuda-txt>🔒 El profe abre su código cuando todos lo intenten.</span>
        <button type="button" class="cd-mini" data-ver hidden>Ver código del profe</button>
        <button type="button" class="cd-mini" data-usar hidden>Usar código del profe</button>
       </div>
      </div>
     </div>
    </div>
   </div>
  </section>
"""


# ─── Los peldaños de circuito ────────────────────────────────────────────────
#
# Aquí no hay editor: el taller es Tinkercad. La diapositiva mantiene el mismo
# orden numerado —la meta, lo que hay que hacer, lo que responde el profe— y el
# esquema resuelto viaja aparte, como el código, para que solo lo vean cuando
# el docente lo abra.

def circuito_svg(spec, estilo="real"):
    """En la pantalla, las piezas dibujadas como se ven en Tinkercad. El
    esquema con símbolos es para el cuaderno y para la guía del docente."""
    return CIR.esquema(**spec, estilo=estilo)


def circuitos_json(ses):
    """El secreto de cada peldaño: el esquema resuelto y el porqué."""
    pasos = {}
    for i, paso in enumerate(ses["circuitos"], 1):
        r = paso["respuesta"]
        pasos[f"{i}-1"] = {"svg": circuito_svg(r["esquema"]), "porque": r["porque"]}
    return {"pasos": pasos}


def diapositiva_circuito(ses, i, paso, tinkercad):
    piezas = "".join(f"<li>{E(x)}</li>" for x in paso["piezas"])
    arma = "".join(f"<li>{E(x)}</li>" for x in paso["arma"])
    # El último peldaño de cada sesión es un proyecto: algo que sirve fuera del
    # aula. Se nota en la chapa, en el «para qué» y en el reto de después.
    chapa = '<span class="ci-chapa">Proyecto real</span>' if paso.get("proyecto") else ""
    para = f'<p class="ci-para">{E(paso["para"])}</p>' if paso.get("para") else ""
    sube = (f'<p class="ci-sube"><b>Sube de nivel</b>{E(paso["sube"])}</p>'
            if paso.get("sube") else "")
    comprueba = "".join(
        f'<li><label><input type="checkbox" data-chk="{j}"><span>{E(x)}</span></label></li>'
        for j, x in enumerate(paso["comprueba"]))
    return f"""
  <section class="slide">
   <div class="inner cd ci" data-ci="{i}-1">
    <p class="eyebrow">{E(ses["titulo"])} · paso {i} de {len(ses["circuitos"])}{chapa}</p>
    <h2 class="cd-t">{E(paso["titulo"])}</h2>
    <p class="cd-frase">{E(paso["frase"])}</p>
    {para}
    <div class="cd-cols">
     <div class="cd-izq">
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">1</span>La meta
        <button type="button" class="cd-mini" data-bajar>⬇ Descargar</button></h3>
       <figure class="cd-meta" data-meta>{circuito_svg(paso["meta"])}</figure>
      </div>
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">3</span><span data-h3>El circuito del profe</span>
        <button type="button" class="cd-mini" data-ojo hidden>👁 Ver</button>
        <button type="button" class="cd-mini" data-copiar hidden>⧉ Copiar</button></h3>
       <div class="cd-candado" data-candado hidden>
        <span data-estado>🔒 Cerrado para la clase</span>
        <button type="button" class="cd-btn" data-dar>Dar el circuito</button>
       </div>
       <div class="ci-resp" data-resp hidden></div>
       <p class="ci-cerrado" data-cerrado>🔒 Primero inténtalo tú. El profe abre su circuito
        cuando todos lo hayan probado.</p>
      </div>
     </div>
     <div class="cd-der">
      <div class="cd-bloque">
       <h3 class="cd-h"><span class="cd-num">2</span>Ármalo en Tinkercad
        <a class="cd-mini" href="{tinkercad}" target="_blank" rel="noopener">Abrir Tinkercad ↗</a></h3>
       <p class="cd-rotulo">Piezas</p>
       <ul class="ci-piezas">{piezas}</ul>
       <ol class="ci-arma">{arma}</ol>
       <p class="cd-rotulo">Comprueba</p>
       <ul class="ci-chk" data-chks>{comprueba}</ul>
       {sube}
      </div>
     </div>
    </div>
   </div>
  </section>
"""



# ─── La ventana de Tinkercad, dibujada ───────────────────────────────────
#
# Antes de armar nada hay que saber dónde está cada cosa. En vez de una
# captura de pantalla —que envejece con cada rediseño de Autodesk— se dibuja
# la ventana con sus zonas numeradas, y los números coinciden con la lista.

def svg_tinkercad(puntos):
    W, H = 640, 360
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#F1F5F9" stroke="#94A3B8" stroke-width="2"/>',
         f'<rect x="0" y="0" width="{W}" height="42" rx="14" fill="#FFFFFF"/>',
         f'<rect x="0" y="28" width="{W}" height="14" fill="#FFFFFF"/>',
         # el nombre del diseño
         f'<rect x="14" y="10" width="150" height="22" rx="11" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.5"/>',
         f'<text x="26" y="26" font-size="12" fill="#64748B">Tu nombre</text>',
         # el botón de simular
         f'<rect x="{W - 250}" y="9" width="120" height="24" rx="6" fill="#2563EB"/>',
         f'<text x="{W - 190}" y="26" font-size="12.5" fill="#fff" text-anchor="middle" font-weight="700">▶ Simular</text>',
         f'<rect x="{W - 120}" y="9" width="72" height="24" rx="6" fill="#E2E8F0"/>',
         f'<text x="{W - 84}" y="26" font-size="12" fill="#475569" text-anchor="middle">Código</text>',
         # el lienzo y el panel de piezas
         f'<rect x="12" y="54" width="{W - 214}" height="{H - 68}" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>',
         f'<rect x="{W - 192}" y="54" width="180" height="{H - 68}" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>',
         f'<rect x="{W - 180}" y="66" width="156" height="22" rx="11" fill="#F1F5F9" stroke="#CBD5E1"/>',
         f'<text x="{W - 170}" y="82" font-size="11.5" fill="#94A3B8">Buscar pieza…</text>']
    for i in range(6):
        x = W - 180 + (i % 2) * 80
        y = 100 + (i // 2) * 62
        p.append(f'<rect x="{x}" y="{y}" width="68" height="50" rx="8" fill="#F8FAFC" stroke="#CBD5E1"/>')
    # dentro del lienzo, un circuito de muestra
    # Dentro del lienzo, un circuito de muestra: se pega el interior del SVG
    # que dibuja circuitos.py, sin su etiqueta ni su papel de fondo.
    muestra = CIR.esquema(fuente="5 V", serie=["resistencia:220 Ω", "led:on"], gnd=False,
                          estilo="real")
    muestra = muestra.split(">", 1)[1].split("/>", 1)[1].rsplit("</svg>", 1)[0]
    p.append(f'<g transform="translate(40 96) scale(0.72)">{muestra}</g>')
    # los números, encima de lo que nombran
    sitios = [(178, 21), (W - 102, 168), (W - 214, 200), (206, 250), (168, 136), (W - 264, 21)]
    for n, (x, y) in enumerate(sitios[:len(puntos)], 1):
        p.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#2563EB" stroke="#fff" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 6}" font-size="15" font-weight="700" fill="#fff" '
                 f'text-anchor="middle">{n}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 -8 {W + 16} {H + 16}" '
            f'width="{W + 16}" height="{H + 16}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" '
            f'role="img" aria-label="La ventana de Tinkercad, con sus zonas numeradas">'
            f'<rect x="-8" y="-8" width="{W + 16}" height="{H + 16}" rx="16" fill="#FFFFFF"/>'
            + "".join(p) + "</svg>")


def diapositiva_tour(tour):
    lista = "".join(f'<li><span class="tp-n">{i}</span><span><b>{E(t)}</b> {E(d)}</span></li>'
                    for i, (t, d) in enumerate(tour["puntos"], 1))
    return f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de armar nada</p>
    <h2 class="cd-t">{E(tour["titulo"])}</h2>
    <div class="ci-tour">
     <figure class="cd-meta" data-meta>{svg_tinkercad(tour["puntos"])}</figure>
     <ol class="ci-guia">{lista}</ol>
    </div>
   </div>
  </section>
"""


def diapositivas_circuitos(ses, antes):
    """El deck de una sesión de circuitos, con sus capítulos. `antes` es cuántas
    diapositivas van delante, para que los capítulos apunten bien."""
    total_s = len(ses["circuitos"])
    trozos, n = [], antes
    entrada = ses.get("entrada")
    if entrada:
        pasos = "".join(f'<li><span class="tp-n">{j}</span><span>{E(p)}</span></li>'
                        for j, p in enumerate(entrada["pasos"], 1))
        trozos.append(f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de armar nada</p>
    <h2 class="mid">{E(entrada["titulo"])}</h2>
    <ol class="ci-entrada">{pasos}</ol>
    <p class="cd-url">La dirección: <b>{E(entrada["url"].replace("https://", ""))}</b></p>
   </div>
  </section>
""")
        n += 1
    if ses.get("tour"):
        trozos.append(diapositiva_tour(ses["tour"]))
        n += 1
    capitulos = [{"t": "Inicio", "a": 0, "b": n - 1, "tecla": None}]
    for i, paso in enumerate(ses["circuitos"], 1):
        trozos.append(diapositiva_circuito(ses, i, paso, ses["tinkercad"]))
        rotulo = "Proyecto" if paso.get("proyecto") else f"Paso {i}"
        capitulos.append({"t": rotulo, "a": n, "b": n, "tecla": str(i)})
        n += 1
    return "".join(trozos), capitulos, total_s


CSS_CIRCUITO = """
/* ─── los peldaños de circuito ─── */
.cd-rotulo{margin:12px 0 6px;font-family:var(--fm);font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--mut)}
.ci-piezas{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.ci-piezas li{padding:6px 12px;border:1px solid var(--line);border-left:3px solid var(--lvl);
  border-radius:8px;background:var(--bg2);font-size:clamp(13px,1.3vw,16px)}
.ci-arma{margin:10px 0 0;padding-left:22px;display:grid;gap:5px;color:var(--tx);
  font-size:clamp(14px,1.5vw,18px);line-height:1.35}
.ci-arma li::marker{color:var(--lvl);font-family:var(--fm);font-size:.85em}
.ci-chk{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.ci-chk label{display:flex;gap:10px;align-items:flex-start;cursor:pointer;
  font-size:clamp(13.5px,1.4vw,17px);color:var(--tx2);line-height:1.3}
.ci-chk input{margin:2px 0 0;width:18px;height:18px;accent-color:var(--lvl);flex:none}
.ci-chk input:checked+span{color:var(--tx);text-decoration:line-through;text-decoration-color:var(--lvl)}
.ci-cerrado{margin:0;padding:16px;border:1px dashed var(--line);border-radius:12px;background:var(--bg2);
  color:var(--mut);font-size:clamp(13.5px,1.4vw,17px);line-height:1.35}
.ci-cerrado[hidden]{display:none}
/* La respuesta: el esquema y el porqué, uno al lado del otro, para que el
   bloque no empuje la diapositiva hacia abajo. */
.ci-resp{display:grid;gap:12px;align-items:start}
@media(min-width:900px){.ci-resp{grid-template-columns:1.3fr 1fr}}
.ci-resp[hidden]{display:none}
.ci-resp figure{margin:0;display:flex;justify-content:center;border:1px solid var(--line);
  border-radius:12px;overflow:hidden;background:#fff}
.ci-resp svg{display:block;width:100%;height:auto;max-height:26vh}
.ci-resp p{margin:0;color:var(--tx2);font-size:clamp(13px,1.3vw,16px);line-height:1.4}
/* Un circuito con ramas queda pequeño en media columna: al tocarlo se abre
   a pantalla completa, que es como se mira desde el fondo del aula. */
.ci-lupa{cursor:zoom-in}
.ci-grande{position:fixed;inset:16px;z-index:60;display:flex;align-items:center;justify-content:center;
  padding:18px;border-radius:16px;background:#fff;box-shadow:0 30px 80px rgba(0,0,0,.55);cursor:zoom-out}
.ci-grande svg{width:100%;max-width:none;height:auto;max-height:86vh}
.ci-chapa{margin-left:14px;padding:3px 10px;border-radius:999px;background:var(--lvl);color:#0B1020;
  font-family:var(--fm);font-size:10.5px;font-weight:700;letter-spacing:.12em}
.ci-para{margin:2px 0 6px;max-width:70ch;color:var(--tx);font-size:clamp(14px,1.5vw,19px);line-height:1.35}
.ci-sube{margin:12px 0 0;padding:10px 14px;border-left:3px solid var(--lvl);background:var(--bg2);
  color:var(--tx2);font-size:clamp(13px,1.3vw,16px);line-height:1.4}
.ci-sube b{display:block;font-family:var(--fm);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--lvl);margin-bottom:3px}
/* La vuelta por la ventana de Tinkercad: el dibujo a la izquierda y la lista
   numerada a la derecha, con los números encima de lo que nombran. */
.ci-tour{display:grid;gap:clamp(14px,2.4vw,30px);grid-template-columns:1fr;margin-top:10px}
@media(min-width:900px){.ci-tour{grid-template-columns:1.25fr 1fr;align-items:center}}
.ci-tour .cd-meta svg{max-height:52vh}
.ci-guia{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.ci-guia li{display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:baseline;
  font-size:clamp(14px,1.5vw,19px);color:var(--tx2);line-height:1.35}
.ci-guia b{color:var(--tx)}
.ci-entrada{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:12px;max-width:60ch}
.ci-entrada li{display:grid;grid-template-columns:36px 1fr;align-items:baseline;gap:12px;
  font-size:clamp(16px,2vw,24px);color:var(--tx);line-height:1.3}
.ci-entrada .tp-n{font-size:clamp(15px,1.7vw,20px);font-weight:700}
"""

JS_CIRCUITO = r"""
(function(){
  var SESION='__SESION__';
  var SEN={signal:typeof senal!=='undefined'?senal:undefined};
  function on(el,ev,fn){if(el)el.addEventListener(ev,fn,SEN);}
  var DOC=false,COD={},ABIERTOS=[],PASOS=[];
  [].forEach.call(document.querySelectorAll('[data-ci]'),function(r){
    var id=r.getAttribute('data-ci'),resp=r.querySelector('[data-resp]'),cerrado=r.querySelector('[data-cerrado]');
    var cand=r.querySelector('[data-candado]'),estado=r.querySelector('[data-estado]'),bDar=r.querySelector('[data-dar]');
    var bOjo=r.querySelector('[data-ojo]'),bCopiar=r.querySelector('[data-copiar]');
    var st={ojo:false};
    function profe(){return COD[id];}
    function abierto(){return ABIERTOS.indexOf(id)>=0;}
    function pintar(){
      var c=profe(),ver=!!c&&(DOC?(abierto()||st.ojo):true);
      if(ver&&resp.getAttribute('data-puesto')!==id){
        resp.innerHTML='<figure>'+c.svg+'</figure><p>'+c.porque+'</p>';
        resp.setAttribute('data-puesto',id);
      }
      resp.hidden=!ver;cerrado.hidden=ver;
      cand.hidden=!DOC;bOjo.hidden=!DOC||!c||abierto();bCopiar.hidden=!DOC||!c;
      bOjo.textContent=st.ojo?'🙈 Ocultar':'👁 Ver';
      if(DOC){var a=abierto();cand.classList.toggle('abierto',a);
        estado.textContent=a?'🔓 Abierto: ya lo ven en sus computadoras':'🔒 Cerrado para la clase';
        bDar.textContent=a?'Cerrar':'Dar el circuito';}
    }
    on(bDar,'click',function(){document.dispatchEvent(new CustomEvent('taller:dar',{detail:{sesion:SESION,paso:id,abrir:!abierto()}}));
      bDar.disabled=true;setTimeout(function(){bDar.disabled=false;},1500);});
    on(bOjo,'click',function(){st.ojo=!st.ojo;pintar();});
    on(bCopiar,'click',function(){var c=profe();if(!c)return;var t=c.porque;
      function listo(){bCopiar.textContent='✓ Copiado';setTimeout(function(){bCopiar.textContent='⧉ Copiar';},1500);}
      function aMano(){var x=document.createElement('textarea');x.value=t;x.style.position='fixed';x.style.opacity='0';
        document.body.appendChild(x);x.select();try{document.execCommand('copy');listo();}catch(e){}x.remove();}
      if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(listo,aMano);else aMano();});
    // Lo que ya comprobaron se queda marcado aunque recarguen.
    var llave='taller:'+SESION+':'+id+':chk';
    var marcas={};try{marcas=JSON.parse(localStorage.getItem(llave)||'{}');}catch(e){}
    [].forEach.call(r.querySelectorAll('[data-chk]'),function(c){
      c.checked=!!marcas[c.getAttribute('data-chk')];
      on(c,'change',function(){marcas[c.getAttribute('data-chk')]=c.checked;
        try{localStorage.setItem(llave,JSON.stringify(marcas));}catch(e){}});
    });
    // La meta se descarga como PNG: el SVG pasa por un canvas al doble de tamaño.
    on(r.querySelector('[data-bajar]'),'click',function(){
      var svg=r.querySelector('[data-meta] svg'),w=+svg.getAttribute('width'),h=+svg.getAttribute('height');
      var url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml'}));
      var img=new Image();img.onload=function(){var c=document.createElement('canvas');c.width=w*2;c.height=h*2;
        var x=c.getContext('2d');x.scale(2,2);x.drawImage(img,0,0,w,h);URL.revokeObjectURL(url);
        c.toBlob(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='meta-circuito-'+id+'.png';
          document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href);},2000);},'image/png');};
      img.src=url;});
    // Tocar un esquema lo abre grande; volver a tocarlo lo devuelve a su sitio.
    [].forEach.call(r.querySelectorAll('[data-meta]'),function(f){f.classList.add('ci-lupa');});
    on(r,'click',function(e){
      var f=e.target.closest('[data-meta],[data-resp] figure');if(!f||!r.contains(f))return;
      f.classList.toggle('ci-grande');f.classList.toggle('ci-lupa');
    });
    // Al volver a la diapositiva, el ojo empieza cerrado.
    var slide=r.closest('.slide'),visible=false;
    function mirar(){var ahora=slide.classList.contains('on');
      if(ahora&&!visible){st.ojo=false;
        [].forEach.call(r.querySelectorAll('.ci-grande'),function(f){f.classList.remove('ci-grande');f.classList.add('ci-lupa');});
        pintar();}visible=ahora;}
    var mo=new MutationObserver(mirar);mo.observe(slide,{attributes:true,attributeFilter:['class']});
    if(SEN.signal)SEN.signal.addEventListener('abort',function(){mo.disconnect();});
    PASOS.push(pintar);pintar();
  });
  on(document,'taller:codigo',function(e){var d=e.detail||{};if(d.sesion&&d.sesion!==SESION)return;
    DOC=!!d.docente;COD=d.pasos||{};ABIERTOS=d.abiertos||[];PASOS.forEach(function(f){f();});});
  document.dispatchEvent(new CustomEvent('taller:listo',{detail:{sesion:SESION}}));
})();
"""


def reloj_sesion(programa):
    """«las dos horas», «los noventa minutos»… lo que dure el bloque. Estaba
    escrito a mano y los programas de hora y media mentían."""
    horas = programa.get("horas_sesion", 2)
    return {1: "la hora", 1.5: "los noventa minutos", 2: "las dos horas"}.get(
        horas, f"las {horas} horas".replace(".", ","))


def cierre(ses):
    return f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de cerrar</p>
    <p class="go">{E(ses["pregunta"])}</p>
   </div>
  </section>
"""


def diapositivas_programa(programa, taller, ses):
    total = len(programa["sesiones"])
    ruta = f"/taller/{programa['via']}/{ses['n']}"
    intro = ""
    if ses.get("dinamica"):
        dinamica = "".join(f'<li><span class="tp-n">{i}</span><b>{E(a)}</b><span>{E(b)}</span></li>'
                           for i, (a, b) in enumerate(ses["dinamica"], 1))
        intro += f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Cómo trabajamos · en parejas: piloto y copiloto</p>
    <ol class="tp-pasos">{dinamica}</ol>
   </div>
  </section>
"""
    if ses.get("idea"):
        idea = '<span class="id-fl">→</span>'.join(f'<span class="id-p">{E(w)}</span>' for w in ses["idea"])
        intro += f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">La idea</p>
    <p class="id-linea">{idea}</p>
   </div>
  </section>
"""
    trozos = [f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">{E(programa["nombre"])} · Sesión {ses["n"]} de {total}</p>
    <div class="cinta">
      <span class="cinta-num">{ses["n"]:02d}</span>
      <span class="cinta-txt">Programado por ustedes<br>desde una página en blanco</span>
    </div>
    <h1 class="mid">{E(ses["titulo"])}</h1>
    <p class="cd-url">Ábrela en tu computadora: <b>{E(C.SITIO.split("://")[-1])}{E(ruta)}</b></p>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="go cd-lema">{E(ses["frase"])}</p>
   </div>
  </section>

{intro}"""]
    antes = "".join(trozos).count('<section class="slide"')
    if ses.get("circuitos"):
        cuerpo, capitulos, _ = diapositivas_circuitos(ses, antes)
        trozos.append(cuerpo)
        n = capitulos[-1]["b"] + 1
        trozos.append(cierre(ses))
        capitulos.append({"t": "Cierre", "a": n, "b": n, "tecla": None})
        return "".join(trozos), capitulos

    n = antes
    capitulos = [{"t": "Inicio", "a": 0, "b": n - 1, "tecla": None}]
    # Con qué llega el estudiante a cada paso: lo del paso anterior, o el
    # punto de partida si el botón empieza de cero.
    previo = {}
    for bn, boton in enumerate(ses["progresion"], 1):
        a = n
        for pid, b, bn_, pn, paso, anterior in _pasos(ses):
            if bn_ == bn:
                antes = b["base"] if pn == 1 and b.get("base") else previo
                trozos.append(diapositiva_codigo(pid, b, bn_, pn, paso, anterior, antes))
                previo = paso
                n += 1
        capitulos.append({"t": f"Botón {bn}", "a": a, "b": n - 1, "tecla": str(bn)})
    trozos.append(cierre(ses))
    capitulos.append({"t": "Cierre", "a": n, "b": n, "tecla": None})
    return "".join(trozos), capitulos


CSS_CODIGO = """
/* ─── el deck para programar ─── */
.id-linea{display:flex;flex-wrap:wrap;align-items:center;gap:clamp(12px,2vw,28px);margin-top:30px;
  font-family:var(--fd);font-weight:800;font-size:clamp(38px,8vw,110px);letter-spacing:-.03em;line-height:1}
.id-fl{color:var(--lvl)}
/* Cómo trabajamos: cuatro tarjetas en fila. */
.tp-pasos{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:14px;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.tp-pasos li{display:grid;gap:6px;align-content:start;padding:20px;border:1px solid var(--line);
  border-top:4px solid var(--lvl);border-radius:12px;background:var(--bg2)}
.tp-n{font-family:var(--fm);font-size:13px;color:var(--lvl)}
.tp-pasos b{font-family:var(--fd);font-size:clamp(24px,3vw,38px)}
.tp-pasos span:last-child{color:var(--tx2);font-size:clamp(15px,1.7vw,20px);line-height:1.4}
.cd-lema{font-size:clamp(40px,7vw,96px);line-height:1.02;max-width:14ch;margin-top:0}
.cd-url{margin-top:26px;font-family:var(--fm);font-size:clamp(13px,1.5vw,18px);color:var(--tx2)}
.cd-url b{color:var(--lvl);font-weight:600}
.cd{display:grid;gap:6px}
.cd-t{font-size:clamp(24px,3.2vw,40px);margin:0}
.cd-frase{margin:0 0 6px;font-size:clamp(15px,1.7vw,21px);color:var(--tx2);max-width:64ch;line-height:1.35}
.cd-cols{display:grid;gap:clamp(12px,2vw,26px);grid-template-columns:1fr}
@media(min-width:900px){.cd-cols{grid-template-columns:1fr 1.1fr}}
.cd-izq,.cd-der{min-width:0}
/* Tres bloques numerados, en el orden en que se hacen: 1 la meta, 2 escribir,
   3 comparar el resultado con la meta (debajo de ella, para verlos juntos). */
.cd-bloque+.cd-bloque{margin-top:12px}
.cd-h{display:flex;align-items:center;gap:10px;margin:0 0 8px;font-family:var(--fd);font-weight:700;
  font-size:clamp(16px,1.6vw,21px);color:var(--tx)}
.cd-num{display:grid;place-items:center;flex:none;width:26px;height:26px;border-radius:50%;background:var(--lvl);
  color:#0B1020;font-family:var(--fm);font-size:14px;font-weight:700}
.cd-sub{font-family:var(--fb,inherit);font-weight:400;font-size:clamp(13px,1.2vw,15px);color:var(--mut)}
.cd-mini{margin-left:auto;display:inline-flex;align-items:center;gap:6px;min-height:30px;padding:0 11px;
  border-radius:8px;border:1px solid var(--line);background:transparent;white-space:nowrap;text-decoration:none;
  color:var(--tx2);font-family:inherit;font-size:13px;cursor:pointer}
.cd-mini+.cd-mini{margin-left:0}
.cd-mini[hidden]{display:none}
/* El dibujo manda su propio tamaño: se centra sobre el papel blanco en vez
   de dejar dos franjas oscuras a los lados. */
.cd-meta{margin:0;display:flex;justify-content:center;border-radius:12px;overflow:hidden;
  border:1px solid var(--line);background:#fff}
.cd-meta svg{display:block;width:100%;height:auto;max-height:32vh}
.cd-piezas{list-style:none;margin:0 0 10px;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.cd-piezas code{display:block;padding:7px 12px;border-radius:8px;background:#0B1020;color:#D7DEEC;
  font-family:var(--fm);font-size:clamp(12px,1.2vw,15px);border-left:3px solid var(--lvl)}
.cd-candado{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px;
  padding:6px 8px 6px 14px;border:1px solid var(--line);border-radius:10px;background:var(--bg2);font-size:15px}
.cd-candado[hidden]{display:none}
.cd-candado.abierto{border-color:var(--lvl)}
.cd-barra{display:flex;align-items:flex-end;gap:6px}
.cd-barra .cd-mini{margin-bottom:4px}
.cd-barra .cd-mini:first-of-type{margin-left:auto}
.cd-tabs{display:flex;gap:4px}
/* La pestaña donde toca escribir lleva el lápiz y el color; las otras se
   pueden abrir, pero quedan apagadas. */
.cd-tab{position:relative;min-height:34px;padding:0 14px;border-radius:8px 8px 0 0;border:1px solid var(--line);border-bottom:0;
  background:transparent;color:var(--mut);font-family:var(--fm);font-size:13px;cursor:pointer;opacity:.7}
.cd-tab.obj{opacity:1;color:var(--tx);border-color:var(--lvl)}
.cd-tab .lapiz{color:var(--lvl);font-weight:700}
.cd-tab[aria-selected="true"]{background:#0B1020;color:#D7DEEC;border-color:#0B1020;opacity:1}
.cd-tab.obj[aria-selected="true"]{box-shadow:inset 0 3px 0 var(--lvl)}
.cd-caja{border-radius:0 10px 10px 10px;background:#0B1020;overflow:hidden}
.cd-pre,.cd-ta,.cd-cerrado{display:block;width:100%;box-sizing:border-box;margin:0;height:min(32vh,300px);overflow:auto;
  background:#0B1020;color:#D7DEEC;font-family:var(--fm);font-size:clamp(12px,1.15vw,15px);line-height:1.5;tab-size:4}
.cd-pre[hidden],.cd-ta[hidden],.cd-cerrado[hidden]{display:none}
.cd-ta{padding:12px 16px;border:0;resize:none;outline:none}
.cd-ta::placeholder{color:#64748B}
.cd-pre{padding:12px 0}
.cd-pre .ln{display:block;padding:0 16px;white-space:pre}
.cd-pre .nuevo{background:color-mix(in srgb,var(--lvl) 30%,transparent);box-shadow:inset 4px 0 0 var(--lvl);color:#fff}
.cd-cerrado{display:grid;place-items:center;text-align:center;color:#94A3B8;font-family:var(--fb,inherit);font-size:clamp(15px,1.6vw,20px)}
.cd-acc{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.cd-btn{min-height:36px;padding:0 13px;border-radius:9px;border:0;background:var(--lvl);color:#0B1020;font-family:inherit;
  font-size:14.5px;font-weight:700;cursor:pointer}
.cd-btn[hidden]{display:none}
.cd-acc .cd-btn{min-height:40px;padding:0 20px;font-size:15.5px}
/* La ayuda del profe va aparte, debajo de una línea: primero se intenta. */
.cd-ayuda{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:12px;padding-top:10px;
  border-top:1px dashed var(--line);font-size:clamp(13px,1.2vw,15px);color:var(--mut)}
.cd-ayuda[hidden]{display:none}
.cd-ayuda .cd-mini:first-of-type{margin-left:auto}
.cd-vista{display:block;width:100%;height:min(26vh,250px);border:1px solid var(--line);border-radius:12px;background:#fff}
"""

JS_CODIGO = r"""
(function(){
  var SESION='__SESION__';
  var SEN={signal:typeof senal!=='undefined'?senal:undefined};
  function on(el,ev,fn){if(el)el.addEventListener(ev,fn,SEN);}
  function b64(d){return btoa(unescape(encodeURIComponent(JSON.stringify(d))));}
  var V='__PYV__',DOC=false,COD={},ABIERTOS=[];
  var VACIO={html:'',css:'',py:''};
  function leer(id){try{var s=localStorage.getItem('taller:'+SESION+':'+id);return s?JSON.parse(s):null;}catch(e){return null;}}
  function escribir(id,v){try{localStorage.setItem('taller:'+SESION+':'+id,JSON.stringify(v));}catch(e){}}
  var RAIZ={};
  [].forEach.call(document.querySelectorAll('[data-cd]'),function(r){RAIZ[r.getAttribute('data-cd')]=r;});
  // Con qué arranca el editor de un paso: lo suyo de este paso; si no, lo
  // suyo del anterior (su botón crece con lo que escribieron); y un botón que
  // empieza de cero, con su punto de partida.
  function inicial(id){
    var r=RAIZ[id],g=leer(id);if(g)return g;
    if(r.getAttribute('data-base'))return JSON.parse(r.getAttribute('data-base'));
    var p=r.getAttribute('data-prev');return p?inicial(p):VACIO;
  }
  var PASOS=[];
  Object.keys(RAIZ).forEach(function(id){
    var r=RAIZ[id],ta=r.querySelector('[data-ta]'),pre=r.querySelector('[data-pre]'),cerrado=r.querySelector('[data-cerrado]');
    var marco=r.querySelector('[data-marco]'),bVer=r.querySelector('[data-ver]'),bUsar=r.querySelector('[data-usar]');
    var cand=r.querySelector('[data-candado]'),estado=r.querySelector('[data-estado]'),bDar=r.querySelector('[data-dar]');
    var escribe=(r.getAttribute('data-escribe')||'py').split(',');
    var ayuda=r.querySelector('[data-ayuda]'),ayudaTxt=r.querySelector('[data-ayuda-txt]');
    // El editor abre en la pestaña donde toca escribir en este paso.
    var bOjo=r.querySelector('[data-ojo]'),bCopiar=r.querySelector('[data-copiar]');
    var st={tab:escribe[0],val:null,viendo:false,corrio:false,confirmar:false,ojo:false};
    // Mientras no escriba en este paso, se lee al vuelo: así hereda lo que
    // acaba de escribir en el anterior, aunque la página cargara antes.
    function mio(){return st.val||inicial(id);}
    function propio(){if(!st.val)st.val=JSON.parse(JSON.stringify(inicial(id)));return st.val;}
    function profe(){return COD[id];}
    function abierto(){return ABIERTOS.indexOf(id)>=0;}
    function pintar(){
      // El docente puede mirar el código sin abrirlo a la clase (el ojo).
      var c=profe(),verPre=DOC?(c&&(abierto()||st.ojo)):st.viendo&&c;
      [].forEach.call(r.querySelectorAll('[data-tab]'),function(b){var k=b.getAttribute('data-tab');
        b.setAttribute('aria-selected',String(k===st.tab));});
      ta.hidden=DOC||verPre;
      pre.hidden=!verPre;
      cerrado.hidden=!(DOC&&!verPre);
      bOjo.hidden=!DOC||!c||abierto();bOjo.textContent=st.ojo?'🙈 Ocultar':'👁 Ver';
      bCopiar.hidden=!DOC||!c;
      if(verPre){pre.innerHTML=c.pre[st.tab]||'<span class="ln"> </span>';}
      else if(!DOC){var x=mio()[st.tab];if(ta.value!==x)ta.value=x;}
      bVer.hidden=DOC||!c;bVer.textContent=st.viendo?'Volver a mi código':'Ver código del profe';
      bUsar.hidden=DOC||!c;bUsar.textContent=st.confirmar?'¿Seguro? Borra lo tuyo · toca otra vez':'Usar código del profe';
      ayuda.hidden=DOC;
      ayudaTxt.textContent=c?'¿Te perdiste?':'🔒 El profe abre su código cuando todos lo intenten.';
      r.querySelector('[data-h3]').textContent=DOC?'La demo':'Tu resultado';
      r.querySelector('[data-sub]').hidden=DOC;
      if(DOC)r.querySelector('[data-h2]').textContent='El código del paso';
      cand.hidden=!DOC;
      if(DOC){var a=abierto();cand.classList.toggle('abierto',a);
        estado.textContent=a?'🔓 Abierto: ya lo ven en sus computadoras':'🔒 Cerrado para la clase';
        bDar.textContent=a?'Cerrar':'Dar el código';}
    }
    function aLoNuevo(){var n=pre.querySelector('.ancla');if(n)pre.scrollTop=Math.max(0,n.offsetTop-pre.clientHeight/3);}
    function paquete(){var c=profe();if(DOC)return c?{v:V,html:c.html,css:c.css,py:c.py}:null;
      var m=mio();return {v:V,html:m.html,css:m.css,py:m.py};}
    function correr(){var p=paquete();if(!p)return;st.corrio=true;marco.src='/editor.html?n='+Date.now()+'#'+b64(p);}
    [].forEach.call(r.querySelectorAll('[data-tab]'),function(b){on(b,'click',function(){
      st.tab=b.getAttribute('data-tab');pintar();aLoNuevo();});});
    on(ta,'input',function(){propio()[st.tab]=ta.value;escribir(id,st.val);});
    // El tabulador escribe cuatro espacios en vez de saltar al siguiente botón.
    on(ta,'keydown',function(e){if(e.key==='Tab'){e.preventDefault();var s=ta.selectionStart;
      ta.value=ta.value.slice(0,s)+'    '+ta.value.slice(ta.selectionEnd);ta.selectionStart=ta.selectionEnd=s+4;
      propio()[st.tab]=ta.value;escribir(id,st.val);}});
    on(r.querySelector('[data-correr]'),'click',correr);
    on(r.querySelector('[data-completa]'),'click',function(){var p=paquete();if(p)window.open('/editor.html#'+b64(p),'_blank','noopener');});
    on(bOjo,'click',function(){st.ojo=!st.ojo;pintar();aLoNuevo();});
    // Copiar la pestaña que está a la vista, tal cual, sin el resaltado.
    on(bCopiar,'click',function(){var c=profe();if(!c)return;var t=c[st.tab]||'';
      function listo(){bCopiar.textContent='✓ Copiado';setTimeout(function(){bCopiar.textContent='⧉ Copiar';},1500);}
      function aMano(){var x=document.createElement('textarea');x.value=t;x.style.position='fixed';x.style.opacity='0';
        document.body.appendChild(x);x.select();try{document.execCommand('copy');listo();}catch(e){}x.remove();}
      if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(listo,aMano);else aMano();});
    on(bVer,'click',function(){st.viendo=!st.viendo;st.confirmar=false;pintar();aLoNuevo();});
    on(bUsar,'click',function(){if(!st.confirmar){st.confirmar=true;pintar();return;}
      var c=profe();st.confirmar=false;st.viendo=false;st.val={html:c.html,css:c.css,py:c.py};escribir(id,st.val);pintar();correr();});
    on(bDar,'click',function(){document.dispatchEvent(new CustomEvent('taller:dar',{detail:{sesion:SESION,paso:id,abrir:!abierto()}}));
      bDar.disabled=true;setTimeout(function(){bDar.disabled=false;},1500);});
    // La meta se descarga como PNG: el SVG pasa por un canvas al doble de tamaño.
    on(r.querySelector('[data-bajar]'),'click',function(){
      var svg=r.querySelector('[data-meta] svg'),w=+svg.getAttribute('width'),h=+svg.getAttribute('height');
      var url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml'}));
      var img=new Image();img.onload=function(){var c=document.createElement('canvas');c.width=w*2;c.height=h*2;
        var x=c.getContext('2d');x.scale(2,2);x.drawImage(img,0,0,w,h);URL.revokeObjectURL(url);
        c.toBlob(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='meta-boton-'+id+'.png';
          document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(a.href);},2000);},'image/png');};
      img.src=url;});
    // Al salir en pantalla: el docente ve su demo corriendo sola.
    var slide=r.closest('.slide'),visible=false;
    function mirar(){var ahora=slide.classList.contains('on');
      if(ahora&&!visible){st.ojo=false;pintar();if(DOC&&!st.corrio)correr();aLoNuevo();}visible=ahora;}
    var mo=new MutationObserver(mirar);mo.observe(slide,{attributes:true,attributeFilter:['class']});
    if(SEN.signal)SEN.signal.addEventListener('abort',function(){mo.disconnect();});
    PASOS.push({pintar:pintar,mirar:mirar,refrescar:function(){if(DOC&&!st.corrio&&slide.classList.contains('on'))correr();}});
    pintar();
  });
  // El componente de la app trae quién mira y el código que le toca ver.
  on(document,'taller:codigo',function(e){var d=e.detail||{};if(d.sesion&&d.sesion!==SESION)return;
    DOC=!!d.docente;COD=d.pasos||{};ABIERTOS=d.abiertos||[];
    PASOS.forEach(function(p){p.pintar();p.refrescar();});});
  document.dispatchEvent(new CustomEvent('taller:listo',{detail:{sesion:SESION}}));
})();
"""


def diapositivas(programa, taller, ses):
    if ses.get("progresion") or ses.get("circuitos"):
        return diapositivas_programa(programa, taller, ses)
    pasos = "".join(f"<li>{E(p)}</li>" for p in ses["pasos"])
    total = len(programa["sesiones"])

    # La seguridad solo aparece cuando la sesión la tiene. Una diapositiva de
    # seguridad vacía enseña a saltársela.
    seguridad = ""
    if ses["seguridad"]:
        partes = [t.strip() for t in ses["seguridad"].split("||")]
        cuerpo = "".join(
            f'<p{" class=\"falta\"" if t.startswith("FALTA") else ""}>{E(t)}</p>'
            for t in partes
        )
        seguridad = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de tocar nada</p>
    <h2 class="mid">Seguridad.</h2>
    <div class="alerta">{cuerpo}</div>
   </div>
  </section>
"""

    # Cuando el programa trae aviones, el paso a paso de verdad son ellos: la
    # lista de texto es el guion de las dos horas y se llama por su nombre.
    # La guía dibujada puede venir de la sesión —las construcciones de palitos,
    # que solo son de la 13— o del programa entero, como los aviones.
    # Una sesión puede decir que no lleva los aviones del programa y traer su
    # propia agenda.
    con_aviones = ses.get("aviones", True)
    aviones = ses.get("guia") or (programa.get("aviones") if con_aviones else None)
    rotulo = "Construcción" if ses.get("guia") else "Avión"
    agenda = ses.get("agenda") or (programa.get("agenda") if con_aviones else None)
    if agenda:
        reloj = "".join(f'<li><span class="ag-min">{E(r)}</span>{E(t)}</li>'
                        for r, t, _ in agenda)
        escalera = "".join(
            f'<div class="esc"><span class="esc-n">{av["n"]}</span>'
            f'<div class="esc-d">{_dibujos(av)[-1]["svg"]}</div>'
            f'<span class="esc-nom">{E(av["nombre"])}</span></div>'
            for av in (aviones or []))
        if aviones:
            lado = f'<div class="escalera"><p class="esc-t">La escalera</p>{escalera}</div>'
        else:
            lado = ""
        guion = f"""<div class="pv">
     <div>
      <p class="eyebrow">El guion de {E(reloj_sesion(programa))}</p>
      <h2 class="mid">Cómo va la sesión.</h2>
      <ol class="agenda">{reloj}</ol>
     </div>
     {lado}
    </div>"""
    else:
        guion = f"""<p class="eyebrow">Cómo va la sesión</p>
    <h2 class="mid">Paso a paso.</h2>
    <ol class="pasos">{pasos}</ol>"""

    # Antes del primer avión, por qué vuela. Solo en los programas con aviones:
    # las construcciones de palitos traen su propia guía y no tienen alas.
    fisica = ""
    if programa.get("aviones") and con_aviones and not ses.get("guia") and hasattr(C, "MAKERS_FISICA"):
        from fuerzas import svg_fuerzas, FLECHAS
        F = C.MAKERS_FISICA
        filas = "".join(f'<li class="fz-{d}"><i aria-hidden="true">{FLECHAS[d]}</i><b>{E(n)}</b><span>{E(t)}</span></li>'
                        for n, t, d in F["fuerzas"])
        rotulo, url = F["fuente"]
        fisica = f"""
  <section class="slide">
   <div class="inner">
    <div class="pv">
     <div>
      <p class="eyebrow">Antes de doblar</p>
      <h2 class="mid">{E(F["titulo"])}</h2>
      <p class="fz-intro">{E(F["intro"])}</p>
      <ul class="fz-lista">{filas}</ul>
      <p class="fz-fuente">Fuente: <a href="{url}" target="_blank" rel="noopener">{E(rotulo)}</a></p>
     </div>
     <div class="fz-dibujo">{svg_fuerzas(F["fuerzas"], "fz-deck")}</div>
    </div>
   </div>
  </section>
"""

    # Los enlaces del día. En el área de cómputo la dirección tiene que leerse
    # desde el fondo del aula, porque la van a teclear ellos.
    enlaces = ""
    if ses.get("enlaces"):
        tarjetas = "".join(
            f'<li><b>{E(nombre)}</b>'
            f'<span class="en-dir">{E(url.replace("https://", "").rstrip("/"))}</span>'
            f'<span class="en-para">{E(para)}</span></li>'
            for nombre, url, para in ses["enlaces"])
        enlaces = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">En la computadora</p>
    <h2 class="mid">Dónde se juega hoy.</h2>
    <ul class="en-lista">{tarjetas}</ul>
   </div>
  </section>
"""

    # El propósito y el material no se proyectan siempre: una sesión «escueta»
    # va de la portada al guion. El dato sigue en la sesión, que es de donde
    # salen el índice y el documento de coordinación.
    proposito = material = ""
    if not ses.get("escueta"):
        proposito = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Para qué es esta sesión</p>
    <h2 class="mid">{E(ses["proposito"])}</h2>
   </div>
  </section>
"""
        material = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">En la mesa, antes de empezar</p>
    <h2 class="mid">Material.</h2>
    <div class="mesa"><p>{E(ses["materiales"])}</p></div>
   </div>
  </section>
"""

    # Las metas del día: lo que convierte «jugar» en «aprender». Una ficha por
    # juego, con casilla, porque se marcan en el pasaporte.
    metas = ""
    if ses.get("metas"):
        fichas = "".join(f'<li><b>{E(juego)}</b><span>{E(meta)}</span></li>'
                         for juego, meta in ses["metas"])
        metas = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Para marcar en el pasaporte</p>
    <h2 class="mid">Tus metas de hoy.</h2>
    <ul class="me-lista">{fichas}</ul>
   </div>
  </section>
"""

    cabecera = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">{E(programa["nombre"])} · Taller {taller["n"]}</p>
    <div class="cinta">
      <span class="cinta-num">{ses["n"]:02d}</span>
      <span class="cinta-txt">Sesión {ses["n"]} de {total}<br>{E(taller["titulo"])}</span>
    </div>
    <h1 class="mid">{E(ses["titulo"])}</h1>
   </div>
  </section>

{proposito}{material}{seguridad}
  <section class="slide">
   <div class="inner">{guion}</div>
  </section>
{fisica}{enlaces}{metas}"""

    # Los aviones van justo después del guion, y saber cuántas diapositivas
    # llevamos hasta aquí es lo que hace que las teclas 1 a 5 apunten bien.
    # Se cuentan, no se suman a mano: así añadir una diapositiva arriba no
    # descoloca los atajos en silencio.
    medio, capitulos = ("", [])
    if aviones:
        antes = cabecera.count('<section class="slide"')
        medio, capitulos = diapositivas_aviones(aviones, antes, rotulo)
        # Los capítulos cubren el deck entero, no solo los aviones: si el
        # primero empezara en la sexta diapositiva, las cinco anteriores no
        # tendrían dónde caerse.
        capitulos = ([{"t": "Inicio", "a": 0, "b": antes - 1, "tecla": None}] + capitulos
                     + [{"t": "El reto", "a": capitulos[-1]["b"] + 1,
                         "b": capitulos[-1]["b"] + 2, "tecla": None}])

    return cabecera + medio + f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">El reto de hoy</p>
    <p class="go">{E(ses["reto"])}</p>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de recoger</p>
    <h2 class="mid">Qué se llevan.</h2>
    <div class="mesa"><p>{E(ses["evidencia"])}</p></div>
   </div>
  </section>
""", capitulos


CSS_ENLACES = """
/* Los enlaces del día: nombre grande, dirección más grande todavía. */
.en-lista{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:14px;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.en-lista li{display:grid;gap:6px;padding:20px 22px;border:1px solid var(--line);
  border-left:5px solid var(--lvl);border-radius:12px;background:var(--bg2)}
.en-lista b{font-family:var(--fd);font-size:clamp(20px,2.6vw,30px)}
.en-dir{font-family:var(--fm);font-size:clamp(14px,1.8vw,22px);color:var(--lvl);word-break:break-all}
.en-para{color:var(--tx2);font-size:clamp(13px,1.5vw,17px);line-height:1.35}
/* Las metas: la casilla delante, para marcarlas de una en una. */
.me-lista{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:12px;max-width:70ch}
.me-lista li{display:grid;grid-template-columns:auto 1fr;align-items:baseline;gap:16px;
  padding:16px 20px;border:1px solid var(--line);border-radius:12px;background:var(--bg2)}
.me-lista li::before{content:"☐";color:var(--lvl);font-size:clamp(20px,2.4vw,28px);line-height:1}
.me-lista b{font-family:var(--fd);font-size:clamp(18px,2.2vw,26px)}
.me-lista span{grid-column:2;color:var(--tx2);font-size:clamp(14px,1.6vw,19px);line-height:1.35}
"""


JS_SESION = JS_BASE.split("function setLvl")[0] + "\nshow(0);\n"


def build(programa, taller, ses):
    acento = ACENTO[programa["via"]]
    cuerpo, capitulos = diapositivas(programa, taller, ses)

    # El CSS de los diagramas y el salto por teclas solo viajan en el deck que
    # los usa: los otros veintiocho no cargan reglas de un dibujo que no tienen.
    # El CSS de los diagramas solo viaja en el deck que los usa; la paginación
    # la llevan los veintinueve, con capítulos o sin ellos.
    tembtns = botones_tema()
    volver, pag, js_pag = chrome_pag(capitulos, "/presentaciones")
    # La agenda por minutos y la guía comparten estas reglas con los aviones.
    css_av = (P.CSS + CSS_AVIONES) if (capitulos or ses.get("agenda")) else ""
    if ses.get("enlaces") or ses.get("metas"):
        css_av += CSS_ENLACES
    # El deck de código lleva sus reglas y el JS de los editores; los demás no.
    sesion_id = f'{programa["via"]}-{ses["n"]}'
    js_cd = ""
    if ses.get("progresion"):
        js_cd = JS_CODIGO.replace("__SESION__", sesion_id).replace("__PYV__", PYSCRIPT_VERSION)
        css_av += CSS_CODIGO
    elif ses.get("circuitos"):
        js_cd = JS_CIRCUITO.replace("__SESION__", sesion_id)
        css_av += CSS_CODIGO + CSS_CIRCUITO

    return f"""<title>{E(programa['nombre'])} {ses['n']:02d} · {E(ses['titulo'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS_BASE}{CSS_PAG}{CSS_EXTRA}{css_av}
.pg{{--lvl:{acento}}}
</style>

<div class="prog" id="prog"></div>
{volver}
<div class="chrome tr" role="group" aria-label="Color de la pantalla">{tembtns}</div>

<main class="deck">{cuerpo}</main>

<div class="chrome bl"><span class="count" id="cnt">01 / 06</span></div>
<div class="chrome br">
  <button class="navb" id="prev" aria-label="Diapositiva anterior">&#8592;</button>
  <button class="navb" id="next" aria-label="Diapositiva siguiente">&#8594;</button>
</div>
{pag}
<script>{JS_SESION}{js_pag}{js_cd}</script>"""


def taller_de(programa, n):
    """El taller al que pertenece la sesión n."""
    for t in programa["talleres"]:
        if n in t["sesiones"]:
            return t
    raise KeyError(f"la sesión {n} no pertenece a ningún taller")


if __name__ == "__main__":
    from exportar_nextjs import partir, reescribir_css, comprobar_css

    indice = []
    for programa in C.MAKER_PROGRAMAS:
        carpeta = os.path.join(SALIDA, programa["via"])
        os.makedirs(carpeta, exist_ok=True)
        for ses in programa["sesiones"]:
            taller = taller_de(programa, ses["n"])
            piezas = partir(build(programa, taller, ses))
            piezas["css"] = reescribir_css(piezas["css"])
            comprobar_css(f"taller/{programa['via']}/{ses['n']}", piezas["css"])
            for ext in ("html", "css", "js"):
                with open(os.path.join(carpeta, f"{ses['n']}.{ext}"), "w", encoding="utf-8") as f:
                    f.write(piezas[ext])
            # El código de una sesión para programar va aparte: la app solo lo
            # entrega por su API, nunca dentro de la página pública.
            ruta_cod = os.path.join(carpeta, f"{ses['n']}.codigo.json")
            secreto = (codigo_json(ses) if ses.get("progresion")
                       else circuitos_json(ses) if ses.get("circuitos") else None)
            if secreto:
                with open(ruta_cod, "w", encoding="utf-8") as f:
                    json.dump(secreto, f, ensure_ascii=False)
            elif os.path.exists(ruta_cod):
                os.remove(ruta_cod)
            with open(os.path.join(carpeta, f"{ses['n']}.meta.json"), "w", encoding="utf-8") as f:
                json.dump({"titulo": piezas["titulo"], "fuente": piezas["fuente"]}, f,
                          ensure_ascii=False, indent=2)
            indice.append({
                "via": programa["via"], "programa": programa["nombre"],
                "horasSesion": programa["horas_sesion"],
                "publico": programa["publico"], "n": ses["n"], "titulo": ses["titulo"],
                "taller": taller["n"], "tallerTitulo": taller["titulo"],
                "reto": ses["reto"], "materiales": ses["materiales"],
                "seguridad": bool(ses["seguridad"]),
            })

    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)
    porvia = " + ".join(f"{sum(1 for x in indice if x['via'] == p['via'])} {p['via']}"
                        for p in C.MAKER_PROGRAMAS)
    print(f"  taller: {len(indice)} sesiones ({porvia})")

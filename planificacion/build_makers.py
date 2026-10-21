# -*- coding: utf-8 -*-
"""
Las dos páginas de Makers Space que la sesión necesita fuera de la pantalla.

  · La guía de aviones. Cinco modelos, un diagrama por paso, calculados desde
    los pliegues (ver plegado.py). Sirve proyectada y sirve impresa, porque a
    los diez minutos de empezar hay treinta personas doblando a ritmos
    distintos y una sola pantalla no alcanza para todos.

  · La hoja de jurado. Un reto que se mide en el patio con cinta métrica y
    cronómetro se anota en papel o no se anota: nadie va a estar tecleando
    entre lanzamiento y lanzamiento.

El deck de la sesión no se genera aquí. Makers Space está en MAKER_PROGRAMAS,
así que build_taller.py ya lo produce con el mismo formato que el resto del
programa, y la ruta /taller/space/1 lo sirve sin tocar nada.
"""
import os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C
import plegado as P
import palitos as PAL
import circuitos as CIR
from build_web import envoltura, lateral_html

E = lambda s: html.escape(str(s), quote=False)

# Los colores del papel y de las rayas, en los tres sitios donde se va a leer
# esto: pantalla clara, pantalla oscura y hoja impresa. Nada cuelga de :root ni
# de body — `comprobar_css` en exportar_nextjs.py aborta el build si lo hiciera.
_OSCURO = """--dg-papel:rgba(150,200,235,.13);--dg-borde:#A8CBE6;
  --dg-marca:#63839F;--dg-pliegue:#83A9FF"""

CSS_EXTRA = """
/* ─── por qué vuela un avión ─── */
.mk-fisica .fz-dibujo{max-width:460px;margin:18px auto 6px}
.mk-fisica .fz-dibujo svg{width:100%%;height:auto;display:block}
.mk-fisica .fz-rejilla{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));margin-top:14px}
.mk-fisica .fz{padding:14px 16px;border:1px solid rgba(127,127,127,.28);border-top:4px solid var(--fz);border-radius:8px}
.mk-fisica .fz i{font-style:normal;font-size:1.6rem;line-height:1;color:var(--fz)}
.mk-fisica .fz b{display:block;font-size:1.1rem;margin:6px 0 4px}
.mk-fisica .fz p{margin:0;opacity:.85;line-height:1.45}
.mk-fisica .fz-fuente{margin-top:12px;font-size:.85rem;opacity:.7}
.mk-fisica .fz-fuente a{color:inherit}
.fz-arriba{--fz:#3B82F6}.fz-abajo{--fz:#EF4444}.fz-adelante{--fz:#22C55E}.fz-atras{--fz:#F59E0B}
.mk{--dg-papel:#FFFFFF;--dg-borde:#5B6E8C;--dg-marca:#A9B6C9;--dg-pliegue:#1D4ED8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .mk{%(osc)s}}
:root[data-theme="dark"] .mk{%(osc)s}

.av{margin-top:56px;padding-top:30px;border-top:1px solid var(--rule)}
.av-apodo{display:block;font-family:var(--f-body);font-weight:400;font-size:.52em;
  color:var(--muted);margin-top:8px;letter-spacing:0}
.av-meta{margin-top:20px;display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.av-meta p{padding:14px 16px;background:var(--surface-2);border-left:3px solid var(--lco);
  font-size:14.6px;color:var(--ink-2)}
.av-meta b{color:var(--ink)}

.av-pasos{list-style:none;margin:26px 0 0;padding:0;counter-reset:paso;
  display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(196px,1fr))}
.av-pasos li{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:14px;position:relative;box-shadow:var(--shadow)}
.av-pasos li::before{counter-increment:paso;content:counter(paso);position:absolute;
  top:10px;left:12px;font-family:var(--f-mono);font-size:12px;font-weight:600;
  color:var(--lco)}
.av-dib{padding:6px 4px 2px}
.av-pasos p{margin-top:10px;font-size:13.8px;line-height:1.45;color:var(--ink);font-weight:500}
.av-pasos .av-det{margin-top:7px;font-size:12.6px;font-weight:400;color:var(--muted)}

.mk-reglas{list-style:none;margin:22px 0 0;padding:0;display:grid;gap:10px}
.mk-reglas li{padding:14px 16px 14px 46px;background:var(--surface);position:relative;
  border:1px solid var(--rule);font-size:15px;color:var(--ink-2)}
.mk-reglas li::before{content:counter(r);counter-increment:r;position:absolute;left:18px;
  font-family:var(--f-mono);font-weight:600;color:var(--lco)}
.mk-reglas{counter-reset:r}

.mk-firma{margin-top:26px;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.mk-firma p{border-top:1px solid var(--rule-2);padding-top:8px;font-size:13px;color:var(--muted)}

.jur td.vacio{height:30px}
.jur .num{width:34px;text-align:center;color:var(--muted);font-family:var(--f-mono);font-size:12px}
.jur th{font-size:12.5px;line-height:1.25}

/* Impreso el objetivo es otro: que un avión entero quepa en una hoja, para que
   nadie tenga que pasar página con las manos llenas de papel a medio doblar.
   El índice de tarjetas sobra —en papel se pasa la hoja, no se navega— y los
   dibujos se limitan en ancho para que las seis viñetas entren en dos filas. */
@media print{
  .mk{--dg-papel:#FFFFFF;--dg-borde:#000000;--dg-marca:#9AA3AF;--dg-pliegue:#000000}
  .lateral,.lat-abrir,.lat-velo,footer,.mk-nota-pantalla,.mk-indice{display:none!important}
  .principal{margin:0!important}
  .wrap{max-width:none;padding:0}
  .av{border-top:2px solid #000;break-before:page;page-break-before:always;
    break-inside:avoid;page-break-inside:avoid;margin-top:0;padding-top:16px}
  .av-meta p{padding:8px 12px;font-size:12px}
  .av-pasos{grid-template-columns:repeat(3,1fr);gap:8px;margin-top:14px}
  .av-pasos li{padding:10px}
  .av-pasos li,.jur tr,.mk-firma{break-inside:avoid;page-break-inside:avoid;box-shadow:none}
  .av-dib{max-width:132px;margin:0 auto;padding:2px}
  .av-pasos p{font-size:11.5px;line-height:1.38;margin-top:8px}
  .av-pasos .av-det{font-size:10.5px;margin-top:5px}
  .jur{font-size:11px}
}
""" % {"osc": _OSCURO}


def _paso_html(paso):
    """En papel sí cabe el porqué: es la guía que se sigue a solas, sin nadie
    delante explicando. El deck se queda con la orden y nada más."""
    detalle = f'<p class="av-det">{E(paso["detalle"])}</p>' if paso["detalle"] else ""
    return (f'<li><div class="av-dib">{paso["svg"]}</div>'
            f'<p>{E(paso["texto"])}</p>{detalle}</li>')


def avion_html(av):
    pasos = "".join(_paso_html(p) for p in P.diagramas(av["pasos"]))
    return f"""
<section class="av" id="{av['id']}">
  <header>
    <p class="eyebrow">Nivel {av['n']} · Enseña: {E(av['ensena'])}</p>
    <h2>{E(av['nombre'])}<span class="av-apodo">{E(av['apodo'])}</span></h2>
    <p class="lead">{E(av['idea'])}</p>
    <div class="av-meta">
      <p><b>Cómo vuela.</b> {E(av['vuela'])}</p>
      <p><b>Necesitas.</b> {E(av['materiales'])}</p>
    </div>
  </header>
  <ol class="av-pasos">{pasos}</ol>
</section>"""


from fuerzas import svg_fuerzas, FLECHAS


def fisica_html():
    """La sección «¿Por qué vuela un avión?», antes de las reglas y los peldaños."""
    F = C.MAKERS_FISICA
    tarjetas = "".join(
        f'<div class="fz fz-{d}"><i aria-hidden="true">{FLECHAS[d]}</i><b>{E(n)}</b><p>{E(t)}</p></div>'
        for n, t, d in F["fuerzas"])
    rotulo, url = F["fuente"]
    return f"""
<section class="mk-fisica">
  <h2 class="sub">{E(F["titulo"])}</h2>
  <p class="lead">{E(F["intro"])}</p>
  <div class="fz-dibujo">{svg_fuerzas(F["fuerzas"], "fz-guia")}</div>
  <div class="fz-rejilla">{tarjetas}</div>
  <p class="fz-fuente">Fuente: <a href="{url}" target="_blank" rel="noopener">{E(rotulo)}</a></p>
</section>"""


def pagina_aviones():
    reglas = "".join(f"<li>{E(r)}</li>" for r in C.MAKERS_REGLAS)
    aviones = "".join(avion_html(a) for a in C.AVIONES)
    indice = "".join(
        f'<a class="nivel-tarjeta lvl-co" href="#{a["id"]}">'
        f'<span class="nt-eyebrow">Nivel {a["n"]} · {E(a["ensena"])}</span>'
        f'<span class="nt-titulo">{E(a["nombre"])}</span>'
        f'<span class="nt-texto">{E(a["vuela"])}</span>'
        f'<span class="nt-flecha">Ver los pasos &#8594;</span></a>'
        for a in C.AVIONES)

    return envoltura(
        "Makers Space · La escalera de aviones",
        C.MAKERS_INTRO,
        lateral_html("/makers/aviones",
                     [("#" + a["id"], f"{a['n']}. {a['nombre']}") for a in C.AVIONES]
                     + [("/makers/jurado", "Hoja de jurado")]),
        f"""<style>{P.CSS}{CSS_EXTRA}</style>
<div class="mk">
<header class="sec-head">
  <p class="eyebrow">Makers Space · Sesión 1</p>
  <h1>La escalera de aviones</h1>
  <p class="lead">{E(C.MAKERS_INTRO)}</p>
</header>
{fisica_html()}

<section>
  <h2 class="sub">Las tres reglas</h2>
  <ol class="mk-reglas">{reglas}</ol>
</section>

<section class="mk-indice">
  <h2 class="sub">Los peldaños</h2>
  <p class="lead">Cada avión añade una idea nueva y una sola. Se sube en orden: el alerón
    del cuarto no significa nada hasta haber visto que el primero se tuerce cuando las alas
    no son iguales.</p>
  <div class="niveles-rejilla">{indice}</div>
</section>
{aviones}

<p class="nota mk-nota-pantalla"><strong>Cómo se leen los dibujos.</strong> La raya
  discontinua es por donde se dobla; la de raya y punto, un pliegue hacia atrás. La flecha
  dice hacia dónde va el papel. La raya de puntos finos es una marca que ya hiciste y que
  solo sirve de referencia. Esta página está pensada también para imprimirse: cada avión
  empieza en una hoja nueva.</p>
</div>""")


# Once columnas no caben en vertical, y en pantalla la tabla se desliza dentro
# de .scrollx —que al imprimir recorta justo la última columna, que es la que
# más se mira—. Impresa va apaisada, sin scroll y con anchos fijos.
CSS_JURADO = """
@page{size:landscape;margin:11mm}
@media print{
  .scrollx{overflow:visible}
  .jur{table-layout:fixed;width:100%;font-size:10.5px}
  .jur th,.jur td{padding:4px 6px}
  .jur td.vacio{height:22px}
  .jur-hoja{break-before:page;page-break-before:always}
}
.jur col.c-n{width:4%}
.jur col.c-txt{width:15%}
.jur col.c-dato{width:8.2%}
"""


def palito_html(pal):
    """Una construcción con sus pasos dibujados. Misma forma que `avion_html`:
    lo que cambia es el objeto, no la manera de explicarlo."""
    pasos = "".join(_paso_html(p) for p in PAL.diagramas(PAL.MODELOS[pal["pasos"]]()))
    return f"""
<section class="av" id="{pal['id']}">
  <header>
    <p class="eyebrow">Nivel {pal['n']} &#183; Ense&#241;a: {E(pal['ensena'])}</p>
    <h2>{E(pal['nombre'])}<span class="av-apodo">{E(pal['apodo'])}</span></h2>
    <p class="lead">{E(pal['idea'])}</p>
    <div class="av-meta">
      <p><b>Para qu&#233;.</b> {E(pal['sirve'])}</p>
      <p><b>Necesitas.</b> {E(pal['materiales'])}</p>
    </div>
  </header>
  <ol class="av-pasos">{pasos}</ol>
</section>"""


def pagina_palitos():
    piezas = "".join(palito_html(x) for x in C.PALITOS)
    indice = "".join(
        f'<a class="nivel-tarjeta lvl-co" href="#{x["id"]}">'
        f'<span class="nt-eyebrow">Nivel {x["n"]} &#183; {E(x["ensena"])}</span>'
        f'<span class="nt-titulo">{E(x["nombre"])}</span>'
        f'<span class="nt-texto">{E(x["sirve"])}</span>'
        f'<span class="nt-flecha">Ver los pasos &#8594;</span></a>'
        for x in C.PALITOS)

    return envoltura(
        "Taller Maker de Primaria · Palitos que aguantan",
        C.PALITOS_INTRO,
        lateral_html("/makers/palitos",
                     [("#" + x["id"], f'{x["n"]}. {x["nombre"]}') for x in C.PALITOS]
                     + [("/makers/aviones", "La escalera de aviones")]),
        f"""<style>{CSS_EXTRA}</style>
<div class="mk">
<header class="sec-head">
  <p class="eyebrow">Taller Maker de Primaria &#183; Sesi&#243;n 13</p>
  <h1>Palitos que aguantan</h1>
  <p class="lead">{E(C.PALITOS_INTRO)}</p>
</header>

<section>
  <h2 class="sub">La silicona la maneja el docente</h2>
  <p class="lead">Una sola pistola, en la mesa del docente. El ni&#241;o trae su pieza,
    se&#241;ala d&#243;nde va y el docente pega. Ning&#250;n ni&#241;o sostiene la pistola:
    pasa de los 150 grados y quema de verdad. Los equipos arman en seco y solo van a la
    mesa cuando la pieza est&#225; lista, que adem&#225;s evita la cola de veinte esperando.</p>
</section>

<section class="mk-indice">
  <h2 class="sub">Los peldaños</h2>
  <p class="lead">Cada construcci&#243;n a&#241;ade una idea y una sola. Se sube en orden:
    las diagonales del puente no significan nada hasta haber visto el cuadrado vencerse
    de un dedazo.</p>
  <div class="niveles-rejilla">{indice}</div>
</section>
{piezas}

<p class="nota mk-nota-pantalla"><strong>C&#243;mo se leen los dibujos.</strong> Los palitos
  en color son los que se ponen en ese paso; los blancos ya estaban. Todo se ve de frente,
  como queda la pieza puesta de pie sobre la mesa.</p>
</div>""")


def pagina_jurado():
    cats = "".join(
        f'<tr><td><b>{E(n)}</b></td><td class="ev-p">{E(c)}</td><td>{E(d)}</td></tr>'
        for n, c, d in C.MAKERS_JURADO)
    reglas = "".join(f"<li>{E(r)}</li>" for r in C.MAKERS_REGLAS_RETO)

    cols = ('<colgroup><col class="c-n"><col class="c-txt"><col class="c-txt">'
            + '<col class="c-dato">' * 8 + '</colgroup>')
    cab = ("<th></th><th>Nombre</th><th>Avión</th>"
           "<th>Dist. 1</th><th>Dist. 2</th><th>Tiempo 1</th><th>Tiempo 2</th>"
           "<th>Punt. 1</th><th>Punt. 2</th><th>Diseño</th><th>Ing.</th>")
    filas = "".join(
        f'<tr><td class="num">{i}</td>' + '<td class="vacio"></td>' * 10 + '</tr>'
        # Dieciocho y no más: las que caben en una hoja apaisada dejando sitio
        # a las firmas. Una fila que se derrama obliga a llevar dos hojas al patio.
        for i in range(1, 19))

    return envoltura(
        "Makers Space · Hoja de jurado",
        C.MAKERS_JURADO_INTRO,
        lateral_html("/makers/jurado", [("/makers/aviones", "La escalera de aviones")]),
        f"""<style>{P.CSS}{CSS_EXTRA}{CSS_JURADO}</style>
<div class="mk">
<header class="sec-head">
  <p class="eyebrow">Makers Space · Sesión 1</p>
  <h1>Hoja de jurado</h1>
  <p class="lead">{E(C.MAKERS_JURADO_INTRO)}</p>
</header>

<section>
  <h2 class="sub">Las cinco categorías</h2>
  <div class="scrollx"><table class="tbl"><thead><tr>
    <th>Categoría</th><th>Con qué</th><th>Cómo se mide</th></tr></thead>
    <tbody>{cats}</tbody></table></div>
</section>

<section>
  <h2 class="sub">Reglas del reto</h2>
  <ol class="mk-reglas">{reglas}</ol>
</section>

<section class="jur-hoja">
  <h2 class="sub">Resultados</h2>
  <p class="lead">Se anota mientras se lanza, no después. Distancia y puntería en metros con
    un decimal; tiempo en segundos; diseño e ingeniería del 1 al 5.</p>
  <div class="scrollx"><table class="tbl jur">{cols}<thead><tr>{cab}</tr></thead>
    <tbody>{filas}</tbody></table></div>
  <div class="mk-firma">
    <p>Juez de distancia y puntería</p>
    <p>Juez de tiempo</p>
    <p>Juez de diseño e ingeniería</p>
  </div>
</section>

<p class="nota mk-nota-pantalla"><strong>Se imprime apaisada sola.</strong> Son once columnas
  y en vertical no cabrían. La tabla sale en su propia hoja, con dieciocho filas: si el
  grupo es más grande, se imprimen dos.</p>
</div>""")


# ═══ Sesión 2 · El botón que cambia de color ══════════════════════════════
#
# La guía de la sesión se abre en cada computadora: trae su propio editor
# (pestañas HTML, CSS y Python, que corren en /editor.html como en las
# clases) y, para primaria, un armador de tarjetas que escribe el programa por
# ellos. El JS es de esta página y no depende del motor de las clases.

import json as _json
from motor_actividades import PYSCRIPT_VERSION

CSS_BOTON = """
.mb-saltos{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px}
.mb-saltos a{padding:7px 14px;border-radius:999px;border:1px solid var(--rule);color:var(--ink);text-decoration:none;font-size:14px}
.mb-saltos a:hover{border-color:var(--accent);color:var(--accent)}
.mb-idea{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin:16px 0 6px}
.mb-idea li{list-style:none;padding:16px 18px;border:1px solid var(--rule);border-top:4px solid var(--accent);border-radius:10px;
  background:var(--surface)}
.mb-idea b{display:block;font-family:var(--f-disp);font-size:20px;margin:4px 0}
.mb-idea .n{font-family:var(--f-mono);font-size:12px;color:var(--accent)}
.mb-idea{padding:0}
.mb-nivel{margin-top:44px;padding-top:10px;border-top:2px solid var(--rule)}
.mb-paso{margin:26px 0 0}
.mb-boton{margin-top:38px}
.mb-paso h3{margin:0 0 6px;font-family:var(--f-disp);font-size:22px}
.mb-paso .n{font-family:var(--f-mono);font-size:12px;color:var(--accent);letter-spacing:.12em;text-transform:uppercase}
.mb-paso p{max-width:70ch;color:var(--ink-2)}
.mb-ed{display:grid;gap:12px;margin-top:10px}
@media(min-width:900px){.mb-ed{grid-template-columns:1fr 1fr;align-items:start}}
.mb-tabs{display:flex;gap:4px}
.mb-tab{min-height:36px;padding:0 14px;border-radius:8px 8px 0 0;border:1px solid var(--rule);border-bottom:0;background:transparent;
  color:var(--muted);font-family:var(--f-mono);font-size:13px;cursor:pointer}
.mb-tab[aria-selected="true"]{background:#0B1020;color:#D7DEEC;border-color:#0B1020}
.mb-code{width:100%;min-height:250px;box-sizing:border-box;padding:12px 14px;border-radius:0 8px 8px 8px;border:1px solid #0B1020;
  background:#0B1020;color:#D7DEEC;font-family:var(--f-mono);font-size:14px;line-height:1.55;resize:vertical;tab-size:4}
.mb-acc{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.mb-btn{min-height:42px;padding:0 16px;border-radius:9px;border:0;background:var(--accent);color:#fff;font-family:inherit;
  font-size:15px;font-weight:700;cursor:pointer}
.mb-btn.sec{background:transparent;color:var(--ink);border:1px solid var(--rule);font-weight:500}
.mb-vista{width:100%;min-height:290px;border:1px solid var(--rule);border-radius:10px;background:#fff}
.mb-arma{display:grid;gap:14px;margin-top:14px}
.mb-carta{display:grid;gap:10px;padding:16px 18px;border:1px solid var(--rule);border-left:5px solid var(--accent);
  border-radius:10px;background:var(--surface)}
.mb-carta h4{margin:0;font-family:var(--f-disp);font-size:18px}
.mb-fila{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.mb-fila .et{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);min-width:170px}
.mb-chip{min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--rule);background:transparent;color:var(--ink);
  font-family:inherit;font-size:15px;cursor:pointer}
.mb-chip[aria-pressed="true"]{background:var(--ink);color:var(--paper,#fff);border-color:var(--ink)}
.mb-color{width:40px;height:40px;border-radius:50%;border:3px solid transparent;cursor:pointer}
.mb-color[aria-pressed="true"]{border-color:var(--ink);box-shadow:0 0 0 2px var(--paper,#fff) inset}
.mb-py{margin:0;padding:12px 14px;border-radius:8px;background:#0B1020;color:#D7DEEC;font-family:var(--f-mono);font-size:13.5px;
  line-height:1.55;white-space:pre-wrap}
.mb-proy{margin-top:30px;padding:18px 20px;border:1px solid var(--rule);border-radius:12px;background:var(--surface)}
.mb-proy h3{margin:0;font-family:var(--f-disp);font-size:24px}
.mb-proy .para{margin:4px 0 10px;color:var(--muted)}
.mb-proy dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0 0 6px}
.mb-proy dt{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.mb-proy dd{margin:0;color:var(--ink-2)}
.mb-jur{width:100%;border-collapse:collapse;font-size:14px;margin-top:12px}
.mb-jur th,.mb-jur td{border:1px solid var(--rule);padding:8px 10px;text-align:left}
.mb-jur td.v{height:26px}
.mb-cat{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));padding:0;margin:12px 0}
.mb-cat li{list-style:none;padding:12px 14px;border:1px solid var(--rule);border-radius:10px}
.mb-cat b{display:block}
@media print{
  .mb-ed,.mb-arma,.mb-saltos,.mb-vista{display:none!important}
  .mb-jurado{break-before:page}
}
"""

JS_BOTON = r"""
(function(){
  var SEN={signal:typeof senal!=='undefined'?senal:undefined};
  function on(el,ev,fn){if(el)el.addEventListener(ev,fn,SEN);}
  function b64(d){return btoa(unescape(encodeURIComponent(JSON.stringify(d))));}
  function correr(marco,d){marco.src='/editor.html?n='+Date.now()+'#'+b64(d);}

  // El editor de cada paso y de cada proyecto.
  [].forEach.call(document.querySelectorAll('[data-ed]'),function(r){
    var cfg=JSON.parse(r.getAttribute('data-cfg')),ta=r.querySelector('[data-codigo]'),marco=r.querySelector('[data-marco]');
    var val={py:cfg.py,html:cfg.html,css:cfg.css},tab=cfg.inicio;
    function mostrar(k){val[tab]=ta.value;tab=k;ta.value=val[k];
      [].forEach.call(r.querySelectorAll('[data-tab]'),function(b){b.setAttribute('aria-selected',String(b.getAttribute('data-tab')===k));});}
    [].forEach.call(r.querySelectorAll('[data-tab]'),function(b){on(b,'click',function(){mostrar(b.getAttribute('data-tab'));});});
    function paquete(){val[tab]=ta.value;return {v:cfg.v,html:val.html,css:val.css,py:val.py};}
    on(r.querySelector('[data-correr]'),'click',function(){correr(marco,paquete());});
    on(r.querySelector('[data-completa]'),'click',function(){window.open('/editor.html#'+b64(paquete()),'_blank','noopener');});
    on(r.querySelector('[data-reset]'),'click',function(){val={py:cfg.py,html:cfg.html,css:cfg.css};ta.value=val[tab];marco.removeAttribute('src');});
    ta.value=val[tab];
  });

  // Primaria: el programa se arma con tarjetas y se ve escrito en Python.
  [].forEach.call(document.querySelectorAll('[data-arma]'),function(r){
    var cfg=JSON.parse(r.getAttribute('data-cfg')),caja=r.querySelector('[data-botones]'),py=r.querySelector('[data-py]');
    var marco=r.querySelector('[data-marco]'),mas=r.querySelector('[data-mas]');
    var botones=[{texto:cfg.textos[0],color:cfg.colores[2][0],mensaje:cfg.mensajes[0]}];
    function chip(clase,txt,on_,accion,estilo){
      var b=document.createElement('button');b.type='button';b.className=clase;b.setAttribute('aria-pressed',String(on_));
      if(txt!==null)b.textContent=txt;if(estilo)b.style.background=estilo;on(b,'click',accion);return b;
    }
    function fila(et,hijos){var f=document.createElement('div');f.className='mb-fila';
      var e=document.createElement('span');e.className='et';e.textContent=et;f.appendChild(e);hijos.forEach(function(h){f.appendChild(h);});return f;}
    function codigo(){
      var html=botones.map(function(b,i){return '<button id="b'+(i+1)+'">'+b.texto+'</button>';}).join('\n')+'\n<h1 id="mensaje"></h1>';
      var p='from pyscript import when, document\n';
      botones.forEach(function(b,i){
        p+='\n@when("click", "#b'+(i+1)+'")\ndef boton'+(i+1)+'(evento):\n'
          +'    document.body.style.background = "'+b.color+'"\n'
          +'    document.querySelector("#mensaje").innerText = "'+b.mensaje.replace(/"/g,'\\"')+'"\n';
      });
      return {html:html,py:p};
    }
    function pintar(){
      caja.innerHTML='';
      botones.forEach(function(b,i){
        var c=document.createElement('div');c.className='mb-carta';
        var h=document.createElement('h4');h.textContent='Botón '+(i+1);c.appendChild(h);
        c.appendChild(fila('Cuando toquen el botón que dice',cfg.textos.map(function(t){
          return chip('mb-chip',t,b.texto===t,function(){b.texto=t;pintar();});})));
        c.appendChild(fila('pon el fondo en',cfg.colores.map(function(par){
          var x=chip('mb-color',null,b.color===par[0],function(){b.color=par[0];pintar();},par[0]);
          x.setAttribute('aria-label',par[1]);x.title=par[1];return x;})));
        c.appendChild(fila('y escribe',cfg.mensajes.map(function(m){
          return chip('mb-chip',m,b.mensaje===m,function(){b.mensaje=m;pintar();});})));
        if(botones.length>1){c.appendChild(chip('mb-btn sec','Quitar este botón',false,function(){botones.splice(i,1);pintar();}));}
        caja.appendChild(c);
      });
      py.textContent=codigo().py;
      mas.disabled=botones.length>=cfg.maximo;
    }
    on(mas,'click',function(){if(botones.length<cfg.maximo){botones.push({texto:cfg.textos[botones.length%cfg.textos.length],
      color:cfg.colores[(botones.length*2)%cfg.colores.length][0],mensaje:cfg.mensajes[botones.length%cfg.mensajes.length]});pintar();}});
    on(r.querySelector('[data-probar]'),'click',function(){var c=codigo();correr(marco,{v:cfg.v,html:c.html,css:cfg.css,py:c.py});});
    pintar();
  });
})();
"""


def _editor(html_, css, py):
    inicio = "py" if py.strip() else "html"
    cfg = {"v": PYSCRIPT_VERSION, "html": html_, "css": css, "py": py, "inicio": inicio}
    tabs = "".join(
        f'<button type="button" role="tab" class="mb-tab" data-tab="{k}" aria-selected="{str(k == inicio).lower()}">{t}</button>'
        for k, t in (("py", "Python"), ("html", "HTML"), ("css", "CSS")))
    return f"""<div class="mb-ed" data-ed data-cfg="{html.escape(_json.dumps(cfg, ensure_ascii=False), quote=True)}">
      <div>
        <div class="mb-tabs" role="tablist" aria-label="Qué parte del código">{tabs}</div>
        <textarea class="mb-code" data-codigo spellcheck="false" aria-label="Tu código"></textarea>
        <div class="mb-acc">
          <button type="button" class="mb-btn" data-correr>▶ Ejecutar</button>
          <button type="button" class="mb-btn sec" data-completa>Pantalla completa ↗</button>
          <button type="button" class="mb-btn sec" data-reset>Volver al inicio</button>
        </div>
      </div>
      <iframe class="mb-vista" data-marco title="Resultado" allow="camera" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
    </div>"""


def pagina_boton():
    B = C.MAKERS_BOTON
    idea = "".join(f'<li><span class="n">{i}</span><b>{E(a)}</b>{E(t)}</li>'
                   for i, (a, t) in enumerate(B["teoria"]["pasos"], 1))
    reglas = "".join(f"<li>{E(r)}</li>" for r in B["reglas"])
    # La misma progresión que se proyecta en /taller/space/2: lo que ven en su
    # computadora es lo que está en la pantalla grande.
    pasos = "".join(
        f'<h3 class="sub mb-boton">Botón {bn} · {E(b["titulo"])}</h3>' + "".join(
            f'<article class="mb-paso"><p class="n">Paso {pn} de {len(b["pasos"])}</p>'
            f'<h3>{E(p["titulo"])}</h3><p>{E(p["frase"])}</p>'
            f'{_editor(p["html"], p["css"], p["py"])}</article>'
            for pn, p in enumerate(b["pasos"], 1))
        for bn, b in enumerate(B["progresion"], 1))
    pr = B["primaria"]
    arma_cfg = {"v": PYSCRIPT_VERSION, "colores": pr["colores"], "mensajes": pr["mensajes"],
                "textos": pr["textos"], "maximo": pr["maximo"],
                "css": C._BOTON_CSS + "\nh1{font-size:2.6rem}\nbutton{margin:.3rem}"}
    proyectos = "".join(
        f'<article class="mb-proy" id="{p["id"]}"><h3>{p["emoji"]} {E(p["titulo"])}</h3>'
        f'<p class="para">{E(p["para"])}</p>'
        f'<dl><dt>Qué hace</dt><dd>{E(p["pide"])}</dd><dt>Sube de nivel</dt><dd>{E(p["sube"])}</dd></dl>'
        f'{_editor(p["html"], p["css"], p["py"])}</article>'
        for p in B["proyectos"])
    cats = "".join(f"<li><b>{E(n)}</b>{E(d)}</li>" for n, d in B["jurado"])
    cabeza = "".join(f"<th>{E(n)}</th>" for n, _ in B["jurado"])
    filas = "".join(f'<tr><td class="v"></td><td class="v"></td>{"<td class=\"v\"></td>" * len(B["jurado"])}</tr>'
                    for _ in range(14))
    return envoltura(
        "Makers Space · El botón que cambia de color",
        B["intro"],
        lateral_html("/makers/boton",
                     [("#idea", "La idea"), ("#secundaria", "Secundaria · desde cero"),
                      ("#primaria", "Primaria · con tarjetas"), ("#proyectos", "El proyecto real"),
                      ("#jurado", "Hoja de jurado"), ("/makers/circuitos", "Circuitos en Tinkercad")]),
        f"""<style>{CSS_BOTON}</style>
<div class="mk">
<header class="sec-head">
  <p class="eyebrow">Makers Space · Sesión 2</p>
  <h1>El botón que cambia de color</h1>
  <p class="lead">{E(B["intro"])}</p>
  <nav class="mb-saltos" aria-label="Saltar a">
    <a href="#idea">La idea</a><a href="#secundaria">Secundaria</a><a href="#primaria">Primaria</a>
    <a href="#proyectos">El proyecto real</a><a href="#jurado">Jurado</a>
  </nav>
</header>

<section id="idea">
  <h2 class="sub">{E(B["teoria"]["titulo"])}</h2>
  <ol class="mb-idea">{idea}</ol>
  <p class="lead">{E(B["teoria"]["enlace"])}</p>
  <h2 class="sub">Las tres reglas de hoy</h2>
  <ol class="mk-reglas">{reglas}</ol>
</section>

<section id="secundaria" class="mb-nivel">
  <h2 class="sub">Secundaria · Tres botones, desde cero</h2>
  <p class="lead">El botón que cambia el fondo, el mismo con colores y animado, y la máquina de colores. Cada paso tiene su editor: cambia el código, pulsa Ejecutar y mira el resultado al lado.</p>
  {pasos}
</section>

<section id="primaria" class="mb-nivel">
  <h2 class="sub">Primaria · Programa tu botón con tarjetas</h2>
  <p class="lead">Elige las tarjetas y pulsa Probar. Abajo aparece tu programa escrito en Python: eso lo hiciste tú.</p>
  <div class="mb-arma" data-arma data-cfg="{html.escape(_json.dumps(arma_cfg, ensure_ascii=False), quote=True)}">
    <div data-botones></div>
    <div class="mb-acc"><button type="button" class="mb-btn sec" data-mas>+ Otro botón</button>
      <button type="button" class="mb-btn" data-probar>▶ Probar mi programa</button></div>
    <p class="eyebrow">Tu programa en Python</p>
    <pre class="mb-py" data-py></pre>
    <iframe class="mb-vista" data-marco title="Tu programa" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
  </div>
</section>

<section id="proyectos" class="mb-nivel">
  <h2 class="sub">El proyecto real</h2>
  <p class="lead">Elige uno con tu pareja y termínalo. Cada proyecto trae su código de partida: la línea «Tu turno» dice qué te toca. Primaria hace el suyo con tarjetas y hasta tres botones.</p>
  {proyectos}
</section>

<section id="jurado" class="mb-nivel mb-jurado">
  <h2 class="sub">Hoja de jurado</h2>
  <p class="lead">Cada pareja prueba el proyecto de otra y marca una categoría. Esta sección se imprime sola.</p>
  <ul class="mb-cat">{cats}</ul>
  <table class="mb-jur"><thead><tr><th>Pareja</th><th>Proyecto</th>{cabeza}</tr></thead><tbody>{filas}</tbody></table>
</section>
</div>
<script>{JS_BOTON}</script>""")


# ═══ La guía del docente para las sesiones de circuitos ══════════════════
#
# Todo junto y con las respuestas: las cuatro escaleras, los esquemas
# resueltos, la ley de Ohm y la hoja que se imprime. Lo que se proyecta es el
# deck; esto es para preparar la clase y para tenerlo al lado durante ella.

CSS_CIRCUITOS = """
.mc-sesion{margin-top:40px;padding-top:12px;border-top:2px solid var(--rule)}
.mc-idea{display:inline-flex;gap:10px;align-items:center;margin:4px 0 10px;font-family:var(--f-mono);
  font-size:13px;color:var(--accent)}
.mc-paso{margin:24px 0 0;padding:18px 20px;border:1px solid var(--rule);border-radius:12px;background:var(--surface)}
.mc-paso h4{margin:0 0 2px;font-family:var(--f-disp);font-size:20px}
.mc-paso .n{font-family:var(--f-mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.mc-rej{display:grid;gap:16px;margin-top:12px}
@media(min-width:900px){.mc-rej{grid-template-columns:1fr 1fr}}
.mc-fig{margin:0;border:1px solid var(--rule);border-radius:10px;overflow:hidden;background:#fff}
.mc-fig svg{display:block;width:100%;height:auto}
.mc-fig figcaption{padding:6px 10px;font-size:12.5px;color:var(--muted);border-top:1px solid var(--rule)}
.mc-piezas{list-style:none;margin:0 0 10px;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.mc-piezas li{padding:5px 10px;border:1px solid var(--rule);border-left:3px solid var(--accent);
  border-radius:7px;font-size:13.5px}
.mc-arma{margin:0 0 10px;padding-left:20px;color:var(--ink-2);font-size:14.5px;line-height:1.45}
.mc-chk{list-style:none;margin:0;padding:0;font-size:14px;color:var(--ink-2)}
.mc-chk li::before{content:"☐ ";color:var(--accent)}
.mc-resp{margin-top:12px;padding:12px 14px;border-left:4px solid var(--accent);background:var(--surface);
  font-size:14.5px;line-height:1.5}
.mc-para{color:var(--ink);font-weight:500}
.mc-resp b{display:block;font-family:var(--f-mono);font-size:11.5px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--accent);margin-bottom:4px}
.mc-hoja{margin-top:16px;border:1px solid var(--rule);border-radius:12px;padding:18px 20px}
.mc-hoja h4{margin:14px 0 4px;font-family:var(--f-disp);font-size:18px}
.mc-hoja ol{padding-left:20px;color:var(--ink-2)}
.mc-lineas{display:grid;gap:14px;margin:8px 0 0}
.mc-lineas span{display:block;border-bottom:1px solid var(--rule);height:20px}
@media print{
  .mc-fig svg{max-height:120mm}
  .mc-hoja{break-before:page}
}
"""


def pagina_circuitos():
    secciones = [("#tinkercad", "Entrar a Tinkercad")]
    cuerpo = []
    for ses in C.MAKERS_CIRCUITOS:
        secciones.append((f"#s{ses['n']}", f"Sesión {ses['n']} · {ses['titulo']}"))
        pasos = []
        for i, paso in enumerate(ses["pasos"], 1):
            piezas = "".join(f"<li>{E(x)}</li>" for x in paso["piezas"])
            arma = "".join(f"<li>{E(x)}</li>" for x in paso["arma"])
            chk = "".join(f"<li>{E(x)}</li>" for x in paso["comprueba"])
            # En la guía van los dos: el dibujo que ven ellos y el esquema
            # con símbolos, que es el que copian al cuaderno.
            meta = CIR.esquema(**paso["meta"], estilo="real")
            resuelto = CIR.esquema(**paso["respuesta"]["esquema"], estilo="real")
            simbolos = CIR.esquema(**paso["meta"])
            para = f'<p class="mc-para">{E(paso["para"])}</p>' if paso.get("para") else ""
            sube = (f'<p class="mc-resp"><b>Sube de nivel</b>{E(paso["sube"])}</p>'
                    if paso.get("sube") else "")
            pasos.append(f"""
  <article class="mc-paso">
    <p class="n">{"Proyecto real" if paso.get("proyecto") else f"Paso {i}"}</p>
    <h4>{E(paso["titulo"])}</h4>
    <p>{E(paso["frase"])}</p>
    {para}
    <div class="mc-rej">
      <figure class="mc-fig">{meta}<figcaption>La meta, lo que ven ellos</figcaption></figure>
      <figure class="mc-fig">{resuelto}<figcaption>El circuito del profe, lo que abres tú</figcaption></figure>
    </div>
    <div class="mc-rej">
      <figure class="mc-fig">{simbolos}<figcaption>El mismo circuito en símbolos, para el cuaderno</figcaption></figure>
    </div>
    <div class="mc-rej">
      <div>
        <p class="eyebrow">Piezas y pasos</p>
        <ul class="mc-piezas">{piezas}</ul>
        <ol class="mc-arma">{arma}</ol>
      </div>
      <div>
        <p class="eyebrow">Comprueba</p>
        <ul class="mc-chk">{chk}</ul>
      </div>
    </div>
    <p class="mc-resp"><b>Por qué</b>{E(paso["respuesta"]["porque"])}</p>
    {sube}
  </article>""")
        cuerpo.append(f"""
<section id="s{ses['n']}" class="mc-sesion">
  <h2 class="sub">Sesión {ses['n']} · {E(ses['titulo'])}</h2>
  <p class="mc-idea">{" → ".join(E(w) for w in ses["idea"])}</p>
  <p class="lead">{E(ses["proposito"])}</p>
  <p><b>Reto:</b> {E(ses["reto"])}</p>
  {"".join(pasos)}
</section>""")

    secciones.append(("#hoja", "Hoja para imprimir"))
    secciones.append(("/makers/boton", "El botón que cambia de color"))
    entrada = C.MAKERS_CIRCUITOS[0]["entrada"]
    entrar = "".join(f"<li>{E(p)}</li>" for p in entrada["pasos"])
    tour = "".join(f"<li><b>{E(t)}</b> {E(d)}</li>"
                   for t, d in C.MAKERS_CIRCUITOS[0]["tour"]["puntos"])
    return envoltura(
        "Makers Space · Electricidad y circuitos en Tinkercad",
        "Las cuatro sesiones de electricidad y circuitos, con los esquemas resueltos, "
        "la ley de Ohm y la hoja que se imprime.",
        lateral_html("/makers/circuitos", secciones),
        f"""<style>{CSS_CIRCUITOS}</style>
<div class="mk">
<header class="sec-head">
  <p class="eyebrow">Makers Space · Sesiones 2 a 5</p>
  <h1>Electricidad y circuitos en Tinkercad</h1>
  <p class="lead">Cuatro bloques de dos horas: encender un LED, encenderlo y apagarlo, medir
  cuánta corriente pasa y mover un motor. Todo en el simulador; los kits físicos vienen después.</p>
</header>

<section id="tinkercad">
  <h2 class="sub">Entrar a Tinkercad</h2>
  <p class="lead">Crea la clase una sola vez, en tinkercad.com → «Classes» → nueva clase. Los
  estudiantes entran con el código y un apodo: no hace falta correo, que es justo lo que Autodesk
  pide para menores. Apunta el código en la pizarra antes de que lleguen.</p>
  <ol class="mk-reglas">{entrar}</ol>
  <p class="lead">Dentro, cada pareja crea un circuito nuevo en «Circuits» y lo guarda con su
  nombre. Desde tu panel de la clase ves sus diseños sin pedirles nada.</p>
  <h2 class="sub">La vuelta por la ventana</h2>
  <p class="lead">Es la primera diapositiva de la sesión 2, y conviene darla despacio: quince
  minutos aquí ahorran una hora de «no me aparece».</p>
  <ol class="mk-reglas">{tour}</ol>
  <h2 class="sub">Las tres reglas de estas sesiones</h2>
  <ol class="mk-reglas">
    <li>Primero lo intentan ellos; el circuito del profe se abre después.</li>
    <li>Un LED nunca va sin su resistencia, ni en el simulador ni en la mesa.</li>
    <li>Si no funciona, se lee el circuito con el dedo: del + hasta el –, sin saltarse nada.</li>
  </ol>
  <p class="lead"><b>La ley de Ohm, en una línea:</b> V = I × R. Con 5 V y 220 Ω pasan unos 20 mA,
  que es justo lo que un LED aguanta contento.</p>
</section>
{"".join(cuerpo)}

<section id="hoja" class="mc-sesion">
  <h2 class="sub">Hoja para imprimir</h2>
  <p class="lead">Una por pareja y por sesión. Sale de las actividades del Módulo 1 de Actuana:
  explicar, dibujar, diagnosticar, mejorar y reflexionar.</p>
  <div class="mc-hoja">
    <h4>1 · Explica con tus palabras</h4>
    <ol>
      <li>¿Qué hace cada componente de tu circuito?</li>
      <li>¿Por qué el LED necesita una resistencia? ¿Qué pasa sin ella?</li>
      <li>¿Qué es GND y por qué hace falta?</li>
      <li>Si el LED no enciende, escribe tres causas probables.</li>
    </ol>
    <div class="mc-lineas"><span></span><span></span><span></span></div>
    <h4>2 · Dibuja el esquema</h4>
    <p>Dibuja tu circuito con símbolos, no el dibujo de la protoboard. Marca con flechas por dónde
    va la corriente, del + al –, y escribe el nombre de cada componente.</p>
    <div class="mc-lineas"><span></span><span></span><span></span><span></span><span></span></div>
    <h4>3 · Diagnóstico</h4>
    <p>Tu profe cambia una cosa. Antes de simular, escribe qué crees que va a pasar; después,
    qué pasó de verdad.</p>
    <div class="mc-lineas"><span></span><span></span><span></span></div>
    <h4>4 · Mejora el diseño</h4>
    <p>Añade algo tuyo —otro LED, otro botón, un orden de cables más limpio— y explica por qué
    mejora el circuito.</p>
    <div class="mc-lineas"><span></span><span></span><span></span></div>
    <h4>5 · Reflexión</h4>
    <p>¿Qué fue lo más difícil? ¿Qué error casi cometes? Escribe una regla de oro para el próximo
    circuito.</p>
    <div class="mc-lineas"><span></span><span></span><span></span></div>
  </div>
  <p class="lead">Basado en el <b>Módulo 1 · Fundamentos de Robótica y Electrónica</b> de Actuana
  Education (Laury Emmanuel Jaquez, 2025). Los esquemas y los textos de esta guía son propios.</p>
</section>
</div>""")


if __name__ == "__main__":
    from exportar_nextjs import exportar

    exportar("makers-aviones", pagina_aviones())
    exportar("makers-jurado", pagina_jurado())
    exportar("makers-palitos", pagina_palitos())
    exportar("makers-boton", pagina_boton())
    exportar("makers-circuitos", pagina_circuitos())
    print(f"  aviones: {sum(len(a['pasos']) for a in C.AVIONES)} diagramas "
          f"en {len(C.AVIONES)} modelos")

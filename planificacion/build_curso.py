# -*- coding: utf-8 -*-
"""
Una presentación por cada clase curricular: 3 niveles × 12 semanas = 36.

Todo sale de `contenido.py`, que ya tiene los cinco bloques de cada sesión, el
reto extra, los recursos y la evidencia. Aquí no se inventa contenido: se saca
de la tabla del plan, donde no se puede proyectar, y se pone en pantalla.

Mismo andamiaje que `build_taller.py` y `build_deck.py` para que las tres
cosas se sientan del mismo curso; lo único que cambia es el color de acento,
que es el del nivel.
"""
import os, sys, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C
from build_deck import CSS as CSS_BASE, JS as JS_BASE, CSS_PAG, chrome_pag, botones_tema, juegos_de
from actividades import validar_actividades, validar_teoria
from motor_actividades import PAGINA_EDITOR, deck_actividad

# Las semanas con actividades salen interactivas; las demás conservan la
# presentación de texto hasta que tengan sus datos.
ACTIVIDADES = getattr(C, "ACTIVIDADES", {})

E = lambda s: html.escape(str(s), quote=False)
SALIDA = os.path.join(HERE, "..", "asistente-aula", "src", "contenido", "curso")

# El acento de cada nivel, el mismo que ya lo identifica en el plan.
ACENTO = {"1ro": "#7BA4FF", "2do": "#63D392", "3ro": "#B79BFF"}

CSS_EXTRA = """
.cinta{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:16px}
.cinta-num{font-family:var(--fd);font-weight:800;font-size:clamp(48px,10vw,132px);
  line-height:.85;color:var(--lvl);letter-spacing:-.04em}
.cinta-txt{font-family:var(--fm);font-size:clamp(10px,1.1vw,12px);letter-spacing:.16em;
  text-transform:uppercase;color:var(--mut)}
.reparto{list-style:none;margin:32px 0 0;padding:0;display:grid;gap:9px;max-width:74ch}
.reparto li{display:grid;grid-template-columns:96px 132px 1fr;gap:16px;align-items:baseline;
  padding:12px 15px;background:var(--bg2);border:1px solid var(--line);border-radius:3px}
@media(max-width:760px){.reparto li{grid-template-columns:88px 1fr}
  .reparto li>span:nth-child(3){grid-column:1/-1;margin-top:4px}}
.reparto b{font-family:var(--fm);font-size:clamp(11px,1.3vw,15px);color:var(--lvl);
  font-variant-numeric:tabular-nums}
.reparto em{font-style:normal;font-size:clamp(10px,1.1vw,12px);letter-spacing:.11em;
  text-transform:uppercase;color:var(--mut);font-weight:600}
.reparto span{font-size:clamp(12.5px,1.35vw,16px);color:var(--tx2);line-height:1.45}
.bloque{margin-top:32px;padding:clamp(20px,2.6vw,30px);background:var(--bg2);
  border:1px solid var(--line);border-left:3px solid var(--lvl);max-width:66ch}
.bloque p{font-size:clamp(15px,1.9vw,22px);line-height:1.45}
.bloque p+p{margin-top:14px;color:var(--tx2);font-size:clamp(13.5px,1.5vw,17px)}
.dato{margin-top:26px;display:grid;gap:5px;max-width:66ch}
.dato dt{font-family:var(--fm);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--lvl);font-weight:600}
.a-cursos{display:flex;gap:6px}
.a-curso{font-family:var(--fm);font-size:12px;letter-spacing:.06em;padding:6px 12px;color:var(--mut);
  border:1px solid var(--line);border-radius:999px;text-decoration:none;transition:color .16s,border-color .16s}
.a-curso:hover{color:var(--tx);border-color:var(--lvl)}
.a-curso[aria-current="page"]{color:var(--bg);background:var(--lvl);border-color:var(--lvl);font-weight:600}
.a-curso:focus-visible{outline:2px solid var(--lvl);outline-offset:2px}
.dato dd{margin:0 0 16px;font-size:clamp(14px,1.7vw,19px);color:var(--tx2);line-height:1.5}
"""


def diapositivas(nivel, ses):
    enganche, concepto, practica, reto, cierre = ses["bloques"]
    reparto = "".join(
        f"<li><b>{E(rango)}</b><em>{E(etq)}</em><span>{E(txt)}</span></li>"
        for rango, etq, txt in (enganche, concepto, practica, cierre)
    )
    # Solo en la primera clase: los juegos de reserva de SEMANA1_DINAMICAS, si
    # el nivel ya los tiene. Nombre y tiempo arriba, cuándo usarlo debajo.
    juegos = juegos_de(nivel["id"]) if ses["n"] == 1 else []
    s_juegos = ""
    if juegos:
        filas = "".join(f"<dt>{E(j[0])} · {E(j[1])}</dt><dd>{E(j[4])}</dd>" for j in juegos)
        s_juegos = f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Si sobra tiempo</p>
    <h2 class="mid">Juegos para elegir.</h2>
    <dl class="dato">{filas}</dl>
   </div>
  </section>
"""
    return f"""
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">{E(nivel["titulo"])} · {E(nivel["nombre"])}</p>
    <div class="cinta">
      <span class="cinta-num">{ses["n"]:02d}</span>
      <span class="cinta-txt">Semana {ses["n"]} de 12</span>
    </div>
    <h1 class="mid">{E(ses["tema"])}</h1>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Al terminar hoy</p>
    <h2 class="mid">{E(ses["objetivo"])}</h2>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Los 45 minutos</p>
    <h2 class="mid">Cómo se reparte la clase.</h2>
    <ul class="reparto">{reparto}</ul>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">El reto de hoy</p>
    <div class="bloque">
      <p>{E(reto[2])}</p>
    </div>
   </div>
  </section>

  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Si terminas antes</p>
    <h2 class="mid">Sube de nivel.</h2>
    <div class="bloque">
      <p>{E(ses["extra"])}</p>
      <p>Solo en los bloques de 50 minutos.</p>
    </div>
   </div>
  </section>
{s_juegos}
  <section class="slide">
   <div class="inner">
    <p class="eyebrow">Antes de irte</p>
    <h2 class="mid">Qué se recoge.</h2>
    <dl class="dato">
      <dt>Evidencia</dt><dd>{E(ses["evidencia"])}</dd>
      <dt>Con qué se trabaja</dt><dd>{E(ses["recursos"])}</dd>
    </dl>
   </div>
  </section>
"""


JS_SESION = JS_BASE.split("function setLvl")[0] + "\nshow(desdeHash());\n"


def build(nivel, ses):
    acento = ACENTO[nivel["id"]]
    tembtns = botones_tema()
    act = ACTIVIDADES.get(nivel["id"], {}).get(ses["n"])
    if act:
        cuerpo, panel_guion, caps, css_act, js_act = deck_actividad(nivel, ses, act)
        # El mismo número de semana en los otros cursos: cada uno con su propio
        # tema. La ruta nueva monta el panel del docente con su nivel, así que
        # «Pasar lista» pasa sola a las secciones de ese curso.
        enlaces = []
        for c in ("1ro", "2do", "3ro"):
            actual = ' aria-current="page"' if c == nivel["id"] else ""
            enlaces.append(f'<a class="a-curso" href="/curso/{c}/semana/{ses["n"]}"{actual}>{c}</a>')
        cursos = '<nav class="a-cursos" aria-label="Curso">' + "".join(enlaces) + '</nav><span class="sep"></span>'

        # El hueco vacío es para el botón «Pasar lista» del panel del docente,
        # que lo pinta con un portal solo si hay sesión de docente.
        boton_guion = ('<span data-hueco-docente style="display:flex"></span>'
                       '<button type="button" class="a-guion-btn" aria-expanded="false" '
                       'title="Notas del docente">Guion</button><span class="sep"></span>')
    else:
        cuerpo, panel_guion, caps, css_act, js_act, boton_guion = diapositivas(nivel, ses), "", None, "", "", ""
        cursos = ""
    volver, pag, js_pag = chrome_pag(caps, "/presentaciones")
    # La primera semana puede llevar una diapositiva más: el contador se cuenta.
    total = cuerpo.count('<section class="slide">')
    return f"""<title>{E(nivel["titulo"][:3])} · Semana {ses["n"]} · {E(ses["tema"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS_BASE}{CSS_PAG}{CSS_EXTRA}{css_act}
.pg{{--lvl:{acento}}}
</style>

<div class="prog" id="prog"></div>
{volver}
<div class="chrome tr" role="group" aria-label="Controles">{cursos}{boton_guion}{tembtns}</div>

<main class="deck">{cuerpo}</main>
{panel_guion}

<div class="chrome bl"><span class="count" id="cnt">01 / {total:02d}</span></div>
<div class="chrome br">
  <button class="navb" id="prev" aria-label="Diapositiva anterior">&#8592;</button>
  <button class="navb" id="next" aria-label="Diapositiva siguiente">&#8594;</button>
</div>
{pag}

<script>{JS_SESION}{js_pag}{js_act}</script>"""


if __name__ == "__main__":
    from exportar_nextjs import partir, reescribir_css, comprobar_css

    for nid, act in ACTIVIDADES.items():
        validar_actividades(nid, act)
    for nid, te in getattr(C, "TEORIA", {}).items():
        validar_teoria(nid, te)

    indice = []
    for nivel in C.NIVELES:
        carpeta = os.path.join(SALIDA, nivel["id"])
        os.makedirs(carpeta, exist_ok=True)
        for ses in nivel["semanas"]:
            piezas = partir(build(nivel, ses))
            piezas["css"] = reescribir_css(piezas["css"])
            comprobar_css(f"curso/{nivel['id']}/{ses['n']}", piezas["css"])
            for ext in ("html", "css", "js"):
                with open(os.path.join(carpeta, f"{ses['n']}.{ext}"), "w", encoding="utf-8") as f:
                    f.write(piezas[ext])
            with open(os.path.join(carpeta, f"{ses['n']}.meta.json"), "w", encoding="utf-8") as f:
                json.dump({"titulo": piezas["titulo"], "fuente": piezas["fuente"]}, f,
                          ensure_ascii=False, indent=2)
            indice.append({
                "nivel": nivel["id"], "nivelNombre": nivel["nombre"], "n": ses["n"],
                "tema": ses["tema"], "objetivo": ses["objetivo"],
            })

    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, "indice.json"), "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)
    # La página donde corre el código de la clase: PyScript necesita una página
    # servida, así que vive en public/ y el marco de la diapositiva apunta ahí.
    publico = os.path.join(HERE, "..", "asistente-aula", "public")
    os.makedirs(publico, exist_ok=True)
    with open(os.path.join(publico, "editor.html"), "w", encoding="utf-8") as f:
        f.write(PAGINA_EDITOR)

    print(f"  curso: {len(indice)} presentaciones generadas + editor.html")

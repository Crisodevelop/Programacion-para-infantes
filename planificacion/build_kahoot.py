# -*- coding: utf-8 -*-
"""
Genera los documentos de los quiz de diagnóstico: uno por nivel y su versión
corta para las secciones de 45 minutos.

Cada documento trae la pregunta numerada, las cuatro opciones con letra y una
línea al pie con la respuesta correcta, el tiempo y la banda. Con eso se
escriben en Kahoot como preguntas de tipo Quiz, y esa misma línea sirve después
para contar aciertos por banda, que es lo que convierte el porcentaje en un
diagnóstico: no importa que sacaran 62 %, importa que la banda 1 vaya al 80 %
y la 3 al 20 %.

Las opciones se barajan. En contenido.py la correcta es siempre la primera,
que es como se escribe y se revisa cómodo; si salieran así al proyector, a la
tercera pregunta toda la clase estaría pulsando el primer botón. El barajado va
con semilla fija: el mismo temario da siempre el mismo orden, así que el
documento impreso sigue coincidiendo con la pantalla la semana que viene.
"""
import os, sys, html, random, zipfile, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contenido as C
import ilustra as IL

E = lambda s: html.escape(str(s), quote=False)
SALIDA = os.path.join(HERE, "salida", "kahoot")
PLANTILLA = os.path.join(HERE, "plantillas", "kahoot.xlsx")
NIVELES = [("1ro", C.PRIMERO), ("2do", C.SEGUNDO), ("3ro", C.TERCERO)]
LETRAS = "ABCD"
P = C.PALETA

# Fila donde la plantilla de Kahoot espera la primera pregunta. Si algún día se
# guarda la plantilla oficial en plantillas/kahoot.xlsx, el script la clona y
# conserva su cabecera verbatim; mientras tanto escribe la suya en la fila 8.
FILA_DATOS = 9
CABECERA = ["", "Question - max 120 characters",
            "Answer 1 - max 75 characters", "Answer 2 - max 75 characters",
            "Answer 3 - max 75 characters", "Answer 4 - max 75 characters",
            "Time limit (sec)", "Correct answer(s)"]


# ---------------------------------------------------------------- VALIDAR
def validar():
    """Falla ruidosamente antes de escribir nada.

    Una pregunta de 130 caracteres se copia a Kahoot sin protestar y aparece
    cortada en el proyector, delante de treinta personas. Es exactamente el
    error que no se puede descubrir en el aula.
    """
    fallos = []
    for niv, preguntas in C.KAHOOT.items():
        for q in preguntas:
            ref = f"{niv} · pregunta {q['n']}"
            if len(q["pregunta"]) > C.KAHOOT_MAX_PREGUNTA:
                fallos.append(f"{ref}: la pregunta tiene {len(q['pregunta'])} caracteres, "
                              f"el máximo es {C.KAHOOT_MAX_PREGUNTA}")
            if len(q["opciones"]) != 4:
                fallos.append(f"{ref}: tiene {len(q['opciones'])} opciones, deben ser 4")
            for i, o in enumerate(q["opciones"], 1):
                if len(o) > C.KAHOOT_MAX_RESPUESTA:
                    fallos.append(f"{ref}, respuesta {i}: tiene {len(o)} caracteres, "
                                  f"el máximo es {C.KAHOOT_MAX_RESPUESTA}")
            if not 1 <= q["correcta"] <= 4:
                fallos.append(f"{ref}: la correcta es {q['correcta']}, debe estar entre 1 y 4")
            if q["segundos"] not in C.KAHOOT_TIEMPOS:
                fallos.append(f"{ref}: {q['segundos']} s no es un tiempo que Kahoot acepte "
                              f"({', '.join(str(t) for t in C.KAHOOT_TIEMPOS)})")
            if q["banda"] not in (1, 2, 3):
                fallos.append(f"{ref}: banda {q['banda']}, debe ser 1, 2 o 3")
            # Kahoot rechaza < y > al importar: «unsupported character in that
            # line», y no dice cuál. Costó una tarde encontrarlo, así que la
            # comprobación se queda aquí. Las etiquetas se escriben sin
            # corchetes angulares: «img», no «<img>».
            for campo, valor in [("la pregunta", q["pregunta"])] + \
                    [(f"la respuesta {i}", o) for i, o in enumerate(q["opciones"], 1)]:
                if "<" in valor or ">" in valor:
                    fallos.append(f"{ref}: {campo} lleva < o >, y Kahoot no los "
                                  f"importa: {valor}")
    if fallos:
        print("\n  Los quiz no se pueden generar:\n", file=sys.stderr)
        for f in fallos:
            print(f"    · {f}", file=sys.stderr)
        print(file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------- BARAJAR
def barajadas(niv, preguntas):
    """Devuelve las preguntas con las opciones en desorden y la correcta reubicada.

    No basta con barajar cada pregunta por su cuenta: barajando sin más, en un
    banco de veinte, una posición acaba llevándose la mitad de las correctas y
    la clase lo huele. Se reparten las cuatro posiciones a partes iguales —cinco
    cada una— y después se coloca la correcta en la que le tocó.
    """
    rnd = random.Random(f"kahoot-{niv}")   # semilla fija: mismo orden en cada corrida
    objetivo = ([1, 2, 3, 4] * (len(preguntas) // 4 + 1))[:len(preguntas)]
    rnd.shuffle(objetivo)

    salida = []
    for q, pos in zip(preguntas, objetivo):
        i = q["correcta"] - 1
        correcta = q["opciones"][i]
        resto = q["opciones"][:i] + q["opciones"][i + 1:]
        rnd.shuffle(resto)
        salida.append({**q, "opciones": resto[:pos - 1] + [correcta] + resto[pos - 1:],
                       "correcta": pos})
    return salida


def filas(preguntas):
    return [[q["pregunta"], *q["opciones"], q["segundos"], q["correcta"]] for q in preguntas]


# ------------------------------------------------------------------ XLSX
#  Se arma a mano con zipfile, igual que build_docx.py arma el .docx: openpyxl
#  no está instalado y no vale una dependencia para ocho celdas por fila.
def _celda(ref, valor):
    if isinstance(valor, int):
        return f'<c r="{ref}"><v>{valor}</v></c>'
    txt = (str(valor).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{txt}</t></is></c>'


def _fila_xml(n, valores):
    celdas = "".join(_celda(f"{chr(65 + i)}{n}", v) for i, v in enumerate(valores))
    return f'<row r="{n}">{celdas}</row>'


_PARTES = {
 "[Content_Types].xml":
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
   '<Default Extension="xml" ContentType="application/xml"/>'
   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.'
   'spreadsheetml.sheet.main+xml"/>'
   '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-'
   'officedocument.spreadsheetml.worksheet+xml"/></Types>',
 "_rels/.rels":
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
   'officeDocument" Target="xl/workbook.xml"/></Relationships>',
 "xl/workbook.xml":
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
   '<sheets><sheet name="Kahoot" sheetId="1" r:id="rId1"/></sheets></workbook>',
 "xl/_rels/workbook.xml.rels":
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
   'worksheet" Target="worksheets/sheet1.xml"/></Relationships>',
}


def xlsx(filas_datos, destino):
    """Desde cero: cabecera propia en la fila 8, datos desde la 9."""
    cuerpo = [_fila_xml(FILA_DATOS - 1, CABECERA)]
    cuerpo += [_fila_xml(FILA_DATOS + i, ["", *f]) for i, f in enumerate(filas_datos)]
    ult = FILA_DATOS + len(filas_datos) - 1
    hoja = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            f'<dimension ref="A1:H{ult}"/>'
            '<cols><col min="2" max="2" width="70" customWidth="1"/>'
            '<col min="3" max="6" width="34" customWidth="1"/>'
            '<col min="7" max="8" width="16" customWidth="1"/></cols>'
            f'<sheetData>{"".join(cuerpo)}</sheetData></worksheet>')
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, parte in _PARTES.items():
            z.writestr(nombre, parte)
        z.writestr("xl/worksheets/sheet1.xml", hoja)


def xlsx_desde_plantilla(filas_datos, destino):
    """Clona la plantilla oficial y le añade las filas de datos.

    Conserva las filas de cabecera de Kahoot tal como vienen —con sus estilos y
    sus referencias a sharedStrings— y solo añade las nuestras debajo, con texto
    en línea. Las dos formas conviven sin problema en la misma hoja.
    """
    with zipfile.ZipFile(PLANTILLA) as z:
        nombres = z.namelist()
        contenidos = {n: z.read(n) for n in nombres}
    hoja = contenidos["xl/worksheets/sheet1.xml"].decode("utf-8")

    conservadas = [m.group(0) for m in re.finditer(r'<row r="(\d+)"[\s\S]*?(?:</row>|/>)', hoja)
                   if int(m.group(1)) < FILA_DATOS]
    nuevas = "".join(_fila_xml(FILA_DATOS + i, ["", *f]) for i, f in enumerate(filas_datos))
    ult = FILA_DATOS + len(filas_datos) - 1
    hoja = re.sub(r"<sheetData>[\s\S]*?</sheetData>",
                  f"<sheetData>{''.join(conservadas)}{nuevas}</sheetData>", hoja, count=1)
    hoja = re.sub(r'<dimension ref="[^"]*"/>', f'<dimension ref="A1:H{ult}"/>', hoja, count=1)

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for n in nombres:
            z.writestr(n, hoja.encode("utf-8") if n == "xl/worksheets/sheet1.xml" else contenidos[n])


def tsv(filas_datos, destino):
    """Para pegar en la plantilla oficial si Kahoot rechazara el .xlsx."""
    lineas = ["\t".join(CABECERA[1:])]
    lineas += ["\t".join(str(v).replace("\t", " ") for v in f) for f in filas_datos]
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lineas) + "\n")


# ------------------------------------------------------------- IMÁGENES
#  Chrome hace la captura: es el único rasterizador que hay en la máquina y no
#  añade dependencias. Sin --user-data-dir a propósito; con un perfil temporal
#  se queda colgado en el primer arranque.
#
#  Una imagen por pregunta, numerada como la pregunta y en la carpeta de su
#  nivel: img/1ro/p01.png … p20.png. Las de banda 3 son la tarjeta de código o
#  de pasos; el resto, la ilustración que dibuja ilustra.py.
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IMG = os.path.join(SALIDA, "img")
FONDO = {"1ro": "#" + P["n1_bg"], "2do": "#" + P["n2_bg"], "3ro": "#" + P["n3_bg"]}

CSS_ESCENA = "html,body{margin:0}svg{display:block}"
ACENTO = {"1ro": "#" + P["n1"], "2do": "#" + P["n2"], "3ro": "#" + P["n3"]}


def _pagina(niv, n):
    """El HTML de una imagen, o None si esa pregunta no lleva ninguna."""
    escena = C.ESCENAS[niv].get(n)
    if not escena:
        return None
    nombre, kw = escena
    return CSS_ESCENA + "|" + IL.dibujar(nombre, ACENTO[niv], FONDO[niv], **kw)


def imagenes():
    if not os.path.exists(CHROME):
        print("    (sin Chrome: no se generaron las imágenes)")
        return
    fuente_mtime = max(os.path.getmtime(os.path.join(HERE, f))
                       for f in ("contenido.py", "ilustra.py"))
    hechas = total = 0

    for niv, _ in NIVELES:
        carpeta = os.path.join(IMG, niv)
        os.makedirs(carpeta, exist_ok=True)
        for q in C.KAHOOT[niv]:
            pagina = _pagina(niv, q["n"])
            if not pagina:
                continue
            total += 1
            png = os.path.join(carpeta, f"p{q['n']:02d}.png")
            if os.path.exists(png) and os.path.getmtime(png) > fuente_mtime:
                continue                  # ya está y el temario no ha cambiado

            css, cuerpo = pagina.split("|", 1)
            tmp = os.path.join(carpeta, f".p{q['n']:02d}.html")
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write('<!doctype html><html><head><meta charset="utf-8">'
                         f"<style>{css}</style></head><body>{cuerpo}</body></html>")
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--window-size=1200,675",
                            f"--screenshot={png}", "file://" + tmp], capture_output=True)
            os.remove(tmp)
            hechas += 1

    print(f"    imágenes: {total} en img/" + (f" ({hechas} regeneradas)" if hechas else " (al día)"))


def hoja_contacto(bancos):
    """Todas las ilustraciones junto a sus cuatro opciones, en una sola página.

    Es la única forma de hacer el repaso que de verdad importa y que ninguna
    prueba automática puede hacer: mirar cada dibujo al lado de las respuestas y
    comprobar que no señala la correcta.
    """
    filas_html = []
    for niv, nivel in NIVELES:
        filas_html.append(f'<h2 style="color:#{ACENTO[niv][1:]}">{E(nivel["titulo"])}</h2>')
        for q in bancos[niv]:
            png = f"img/{niv}/p{q['n']:02d}.png"
            hay = os.path.exists(os.path.join(SALIDA, png))
            marco = (f'<img src="{png}" alt="">' if hay
                     else '<div class="sin">sin ilustración</div>')
            ops = "".join(
                f'<li class="{"ok" if i == q["correcta"] else ""}">{E(o)}</li>'
                for i, o in enumerate(q["opciones"], 1))
            filas_html.append(
                f'<section><div class="im">{marco}</div><div class="tx">'
                f'<p class="pr"><b>{q["n"]}.</b> {E(q["pregunta"])}</p>'
                f'<ol>{ops}</ol></div></section>')

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilustraciones del quiz · repaso</title><style>
body{{margin:0;padding:30px;max-width:1080px;margin-inline:auto;background:#fff;
 font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#{P['texto']}}}
h1{{font-size:26px;margin:0 0 4px;color:#{P['navy']}}}
p.sub{{color:#{P['suave']};margin:0 0 30px;max-width:76ch}}
h2{{font-size:18px;margin:38px 0 10px;padding-bottom:6px;border-bottom:2px solid currentColor}}
section{{display:grid;grid-template-columns:300px 1fr;gap:22px;align-items:start;
 padding:16px 0;border-bottom:1px solid #{P['borde']}}}
.im img{{width:100%;display:block;border:1px solid #{P['borde']};border-radius:8px}}
.sin{{padding:44px 0;text-align:center;color:#{P['suave']};background:#{P['gris']};
 border:1px dashed #{P['borde']};border-radius:8px;font-size:13px}}
.pr{{margin:0 0 8px;font-size:15.5px}}
ol{{margin:0;padding-left:22px;color:#{P['suave']};font-size:14px}}
li.ok{{color:#{P['texto']};font-weight:700}}
li.ok::after{{content:" ✓";color:#16A34A}}
</style></head><body>
<h1>Ilustraciones del quiz · repaso</h1>
<p class="sub">Cada dibujo al lado de sus cuatro opciones, con la correcta en negrita.
Lo que hay que comprobar en cada fila es que la ilustración no señale esa opción:
una imagen que regala la respuesta convierte el diagnóstico en ruido, y no se nota
hasta ver los resultados altos y no entender por qué.</p>
{"".join(filas_html)}
</body></html>"""


# ------------------------------------------------------------- DOCUMENTO
CSS = """
body{margin:0;padding:34px 40px;font:13pt/1.5 Georgia,"Times New Roman",serif;color:#000;
  background:#fff;max-width:820px;margin-inline:auto}
h1{font-size:19pt;margin:0 0 4px}
p.meta{font-size:10pt;color:#444;margin:0 0 26px}
.q{margin:0 0 20px;page-break-inside:avoid;break-inside:avoid}
.q p{margin:0 0 3px}
.enunciado{font-weight:bold}
.op{margin-left:22px}
.pie{margin-top:5px;font-size:10.5pt;font-style:italic;color:#333}
@page{margin:16mm}
"""


def documento(titulo, nivel, preguntas):
    bloques = []
    for i, q in enumerate(preguntas, 1):
        opciones = "".join(
            f'<p class="op">{LETRAS[j]}) {E(o)}</p>' for j, o in enumerate(q["opciones"]))
        imagen = (f' &nbsp;·&nbsp; imagen: img/{nivel}/p{q["n"]:02d}.png'
                  if q["n"] in C.ESCENAS[nivel] else "")
        bloques.append(
            f'<div class="q"><p class="enunciado">{i}. {E(q["pregunta"])}</p>{opciones}'
            f'<p class="pie">Correcta: {LETRAS[q["correcta"] - 1]} &nbsp;·&nbsp; '
            f'{q["segundos"]} s &nbsp;·&nbsp; banda {q["banda"]}{imagen}</p></div>')

    conteo = {b: sum(1 for q in preguntas if q["banda"] == b) for b in (1, 2, 3)}
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(titulo)}</title><style>{CSS}</style></head><body>
<h1>{E(titulo)}</h1>
<p class="meta">{len(preguntas)} preguntas de opción múltiple, una sola correcta.
Banda 1: {conteo[1]} · banda 2: {conteo[2]} · banda 3: {conteo[3]}.
No puntúa para nota: mide de dónde parte el grupo.</p>
{"".join(bloques)}
</body></html>"""


# ------------------------------------------------------------------ BUILD
def build():
    validar()
    os.makedirs(SALIDA, exist_ok=True)

    imagenes()
    bancos = {}
    escribir_xlsx = xlsx_desde_plantilla if os.path.exists(PLANTILLA) else xlsx

    for niv, _ in NIVELES:
        preguntas = barajadas(niv, C.KAHOOT[niv])
        bancos[niv] = preguntas
        nucleo = [q for q in preguntas if q["nucleo"]]

        for sufijo, cuales, etiqueta in (("", preguntas, ""), ("_corto", nucleo, " · corto")):
            base = os.path.join(SALIDA, f"Quiz_Diagnostico_{niv}{sufijo}")
            with open(base + ".html", "w", encoding="utf-8") as fh:
                fh.write(documento(f"Diagnóstico {niv}{etiqueta}", niv, cuales))
            escribir_xlsx(filas(cuales), base + ".xlsx")
            tsv(filas(cuales), base + ".tsv")

        print(f"    {niv}: {len(preguntas)} preguntas · corto de {len(nucleo)}")

    with open(os.path.join(SALIDA, "contacto.html"), "w", encoding="utf-8") as fh:
        fh.write(hoja_contacto(bancos))


if __name__ == "__main__":
    build()

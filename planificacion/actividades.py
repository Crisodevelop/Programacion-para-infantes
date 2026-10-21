# -*- coding: utf-8 -*-
"""
Las actividades de cada clase: lo que convierte las 36 presentaciones del curso
en clases que el alumno toca, no solo mira.

Los datos viven en `contenido.ACTIVIDADES = {"1ro": ACT, "2do": ACT, "3ro": ACT}`.
Este módulo tiene tres cosas: el contrato (este texto), el validador que lo hace
cumplir antes de escribir nada, y el motor (CSS, JS y diapositivas) que
`build_curso.py` usa para las semanas que ya tienen datos.

ESQUEMA (contrato fijo; el mismo texto que tienen los agentes de contenido)
--------------------------------------------------------------------------

ACT = {1: semana, …, 12: semana}
semana = {
 "hoy": str (≤90 chars, student voice «Vas a…»),
 "escena": str key of ilustra.ESCENAS | None,
 "calentamiento": {"pregunta": str≤110, "opciones": [4 unique str≤48], "correcta": 0-3, "por_que": str},
 "ejemplo": {"titulo": str, "lenguaje": L, "codigo": [2–14 str, each ≤52 cols], "notas": [(linea_1based:int, str)] 1–4 items, pointing at non-blank lines},
 "retos": [  # exactly these 4, in this order
   {"tipo":"predice","lenguaje":L,"codigo":[1–10 str ≤52],"opciones":[3–4 unique str≤48],"correcta":int,"explica":str},
   {"tipo":"completa","lenguaje":L,"codigo":[1–10 str ≤52] containing exactly one "___" in total,"opciones":[3–4 unique str≤48],"correcta":int,"explica":str},
   {"tipo":"ordena","lenguaje":L,"enunciado":str,"lineas":[3–7 str ≤52] in CORRECT order, not all identical},
   {"tipo":"error","lenguaje":L,"lineas":[3–8 str ≤52],"mala":int 0-based,"arreglo":str (≠ bad line),"explica":str},
 ],
 "juego": {"tipo": MOTOR, "titulo": str≤60, "pista": str≤40, …config per MOTOR below},
 "practica": {"tipo": "editor"|"enlace"|"desenchufada", "titulo": str, "pasos": [3–7 str],
              editor  → "html": str, "css": str, "py": str (may be "" in HTML/CSS-only weeks),
              enlace  → "url": str (https), "boton": str},
 "reto_dia": str | None (None = use the session's Reto block text),
 "salida": {"pregunta": str, "respuesta": str},
}
L = "python" | "html" | "css" | "tarjetas"   # tarjetas = unplugged steps in plain Spanish (1ro S1–2)

- For editor weeks the practice runs in the class editor (tabs Python, HTML and
  CSS); what the student writes is saved with their grade when they press Ejecutar.

Predice execution rule (lenguaje python):
- If the code does not contain `document`, `window`, `when`, `random`, `input`
  or `time`, execute it with injected `display` and `print` that append
  `" ".join(str(a) for a in args)` to a list.
- Output = items joined with `" · "`.
- If it raises, the acceptable outputs are the exception class name
  (e.g. `TypeError`) or `"Error"`.
- `opciones[correcta]` must equal the output (or one of the acceptable names),
  and no other option may equal it.
- If not executable, just `compile()` it.

Other Python checks:
- completa: with `opciones[correcta]` substituted for `___`, compile.
- ordena: lines joined in order compile.
- error: lines with `lineas[mala]` replaced by `arreglo` compile.
- ejemplo compiles. practica.py compiles when non-empty.
- Fragments: indented snippets are dedented; function-body or loop-body
  fragments are wrapped (`def _f():`, `while True:`) before compiling; top-level
  `await` is allowed.

House API (python):
- Forbid `input(`, `alert(`, `import js`, `from js`, `pyodide`.
- If `ejemplo` or `practica.py` use `when`/`display`/`document`/`window`, they
  must import them `from pyscript import …`.
- `print(` is allowed only in 1ro week 3.

Practica:
- Every `#id` used in `@when("…", "#id")` or `querySelector("#id")` inside `py`
  must exist as `id="id"` in `html`.
- Week 1 must be `desenchufada` (the same route for the three grades).
- Week 10 must be `enlace` (Teachable Machine).
- All other weeks must be `editor`.

Limits: `escena` is in `IL.ESCENAS` or None.

MOTORES and their config:
- robot: {"tam":5–7, "inicio":[x,y,"N"|"E"|"S"|"O"], "meta":[x,y], "muros":[[x,y],…],
          "max":≤10, "cartas": subset of ["AVANZA","GIRA_IZQ","GIRA_DER","REPITE_2"]}
  0-based coords; x = column, y = row from the top; N = up. REPITE_2 repeats the
  NEXT card twice. The meta must be reachable with ≤ max cards.
- clasifica: {"cubetas":[2–4 str], "items":[[texto, idx_cubeta] ×6–12]}. Every bucket gets ≥1 item.
- marcador: {"variables":{nombre: int|float|str}, "cajas":[{"var":str,"valor":str}] (optional),
             "botones":[B…], "meta":{"var","valor","segundos"} (optional), "recargar": bool (optional)}
  B is one of:
    {"texto","linea","var","op": "+="|"-="|"=","valor"}
    {"texto","linea","calc":{"izq":var,"op":"+"|"-"|"*"|"/"|"//"|"%","der":var|number,
                             "convertir":None|"int"|"float","destino":var}}
    {"texto","linea","op":"guardar"|"cargar"}   (only if recargar)
  With recargar there is also an automatic «Recargar la página» button that
  resets variables to their initial values but keeps the saved box.
- ramas: {"variable":str, "entrada":"slider"|"numero", "min":num, "max":num, "paso":num,
          "secreto":bool, "ramas":[{"op":"<"|"<="|">"|">="|"=="|"!="|"else",
          "valor":number|"secreto", "mensaje":str}]}
  Last branch is `else`; every branch reachable by some value in [min,max] step paso.
- ppt: {}
- bucle: {"modo":"for", "var":str, "iterable":{"range":[a,b,paso]} | {"lista":[…]},
          "acumula":{"var":str,"op":"+="|"*=","inicio":num,"usa":"var"|number} | None, "cuerpo":[str]}
      or {"modo":"while", "mientras":{"var":str,"op":"<"|"<="|">"|">=","valor":num,"inicio":num,"cambio":num},
          "acumula":…|None, "cuerpo":[str]}
  ≤12 iterations.
- caza: {"nombre":str (variable), "inicial":[4-8 str], "extra":[0-3 str más que
         entran a media partida], "rondas":4-12, "gana":1..rondas}
  Solo se LEE la lista: índice, índice negativo, posición de un valor y len.
- lista: {"modo":"lista"|"dict", "nombre":str, "inicial":list|dict,
          "ops":subset (lista: ["append","pop","len","indice","in"]; dict: ["get","set","del","len","in"]),
          "valores":[str|num offered for append/set/in]}
- css: {"controles":[{"prop":P, "tipo":"slider","min":n,"max":n,"unidad":"px"|"rem"|"%"}
                     | {"prop":P,"tipo":"opciones","valores":[str]}], "hijos":3–6}
  P ∈ {background-color, color, padding, margin, border-radius, font-size, gap,
  justify-content, align-items, flex-direction, flex-wrap, width}.
- aventura: {"inicio":nombre_funcion, "salas":{nombre_funcion:{"texto":str,"opciones":[[texto,destino],…]}}}
  Empty opciones = ending. All destinations exist; an ending is reachable from inicio.
- carrera: {"segundos":30–90, "preguntas":[{"pregunta":str≤110,"opciones":[3–4 str≤48],"correcta":int}] ≥8}
- dado, ia, datos, formulario, pagina: {} (reuse build_deck.demo)

Week → engine mapping:
1ro: 1 robot, 2 clasifica, 3 clasifica, 4 marcador, 5 marcador, 6 dado, 7 ramas, 8 ppt, 9 bucle, 10 lista, 11 aventura, 12 carrera
2do: 1 pagina, 2 clasifica, 3 css, 4 ia, 5 clasifica, 6 marcador, 7 ramas, 8 bucle, 9 lista, 10 aventura, 11 ia, 12 carrera
3ro: 1 clasifica, 2 marcador, 3 clasifica, 4 datos, 5 lista, 6 carrera, 7 bucle, 8 formulario, 9 marcador, 10 ramas, 11 clasifica, 12 carrera

ACLARACIONES (todas permisivas; ninguna agrega una regla)
----------------------------------------------------------
- Las semanas que faltan en ACT no fallan: se avisa y esas semanas conservan la
  presentación anterior. Las `notas` pueden ser tuplas o listas de dos.
- Predice: si el código importa de `pyscript` (por ejemplo `display`), se usa
  un módulo `pyscript` simulado, así que igual se ejecuta.
- `import json` y `from json` no cuentan como `import js` / `from js`.
- marcador · calc: `convertir` se aplica a cada operando que sea una variable
  con texto (lo típico: `int(caja) + 1`); si ningún operando es texto, se
  aplica al resultado (`int(a / b)`). `destino` puede ser una variable nueva:
  aparece en el marcador la primera vez que se calcula.
- marcador · meta: con número se cumple cuando la variable llega (≥) al valor;
  con texto, cuando es igual. El reloj de `segundos` arranca con el primer toque.
- robot: se gana al pisar la meta en cualquier paso del programa; una
  REPITE_2 al final (sin carta siguiente) no hace nada.
- lista · dict: `set` ofrece como clave las claves existentes y los textos de
  `valores`, y como valor los `valores`.
- `ppt` y los motores reutilizados aceptan claves extra sin quejarse.
"""
import ast, builtins, html, json, os, random, re, signal, sys, textwrap, types

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import ilustra as IL

E = lambda s: html.escape(str(s), quote=False)
A = lambda s: html.escape(str(s), quote=True)

# ── El contrato en datos ──────────────────────────────────────────────────────

LENGUAJES = ("python", "html", "css", "tarjetas")

MAPA_MOTORES = {
    # La 4 es de if: el juego es piedra, papel o tijera, que ES un if/elif/else
    # y se entiende sin leer código. El visor de ramas quedó como segundo juego
    # de la 11, donde lo que se lee es lo que decide la IA.
    "1ro": "robot clasifica bucle ppt caza aventura marcador dado portada ia ia carrera",
    "2do": "robot clasifica bucle ppt caza aventura marcador dado portada ia ia carrera",
    "3ro": "robot clasifica bucle ppt caza aventura marcador dado portada ia ia carrera",
}
MAPA_MOTORES = {k: dict(enumerate(v.split(), 1)) for k, v in MAPA_MOTORES.items()}

# Los que ya existen en build_deck.demo(): se reutilizan tal cual.
MOTORES_DEMO = {"dado": "dado", "ia": "ia", "datos": "datos", "formulario": "formulario", "pagina": "pagina"}


CSS_PROPS = {"background-color", "color", "padding", "margin", "border-radius", "font-size",
             "gap", "justify-content", "align-items", "flex-direction", "flex-wrap", "width"}

CARTAS = ("AVANZA", "GIRA_IZQ", "GIRA_DER", "REPITE_2")
DIRS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "O": (-1, 0)}
IZQ = {"N": "O", "O": "S", "S": "E", "E": "N"}
DER = {v: k for k, v in IZQ.items()}

NO_EJECUTAR = ("document", "window", "when", "random", "input", "time")
PROHIBIDO = [(re.compile(r"\binput\s*\("), "input("), (re.compile(r"\balert\s*\("), "alert("),
             (re.compile(r"\bimport\s+js\b"), "import js"), (re.compile(r"\bfrom\s+js\b"), "from js"),
             (re.compile(r"pyodide", re.I), "pyodide")]
RE_PRINT = re.compile(r"\bprint\s*\(")
NOMBRES_PYSCRIPT = {"when", "display", "document", "window"}


# ── Utilidades del validador ─────────────────────────────────────────────────

def _es_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _es_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _texto(v, maximo=None, vacio=False):
    return isinstance(v, str) and (vacio or v.strip() != "") and (maximo is None or len(v) <= maximo)


def _cols(linea):
    return len(linea.expandtabs(4))


def _intentos(src):
    """Versiones del fragmento que se prueban hasta que una compile."""
    ded = textwrap.dedent(src)
    ind = textwrap.indent(ded, "    ")
    yield ded
    yield "if True:\n" + src            # cuerpo de bloque con cierre sin sangría
    yield "def _f():\n" + ind           # return / yield sueltos
    yield "async def _f():\n" + ind     # await suelto
    yield "while True:\n" + ind         # break / continue sueltos
    yield "async def _f():\n while True:\n" + textwrap.indent(ded, "  ")


def compilar(src):
    """Devuelve (arbol_ast, None) si compila con alguna envoltura, o (None, error)."""
    primero = None
    for i, cand in enumerate(_intentos(src)):
        try:
            flags = ast.PyCF_ALLOW_TOP_LEVEL_AWAIT if i == 0 else 0
            compile(cand, "<reto>", "exec", flags=flags)
            return ast.parse(cand), None
        except SyntaxError as e:
            if primero is None:
                primero = f"SyntaxError línea {e.lineno}: {e.msg}"
        except Exception as e:  # ValueError por bytes nulos, etc.
            if primero is None:
                primero = f"{type(e).__name__}: {e}"
    return None, primero


class _Tiempo(Exception):
    pass


def ejecutar(src):
    """Ejecuta un predice. Devuelve (salida, None) o (None, NombreExcepcion)."""
    salida = []

    def mostrar(*args, **kw):
        salida.append(" ".join(str(a) for a in args))

    falso = types.ModuleType("pyscript")
    falso.display = mostrar
    previo = sys.modules.get("pyscript")
    sys.modules["pyscript"] = falso
    alarma = hasattr(signal, "SIGALRM")
    if alarma:
        def _corta(*_):
            raise _Tiempo()
        viejo = signal.signal(signal.SIGALRM, _corta)
        signal.alarm(2)
    try:
        exec(compile(textwrap.dedent(src), "<predice>", "exec"),
             {"__builtins__": builtins, "display": mostrar, "print": mostrar, "__name__": "__main__"})
        return " · ".join(salida), None
    except _Tiempo:
        return None, "_Tiempo"
    except BaseException as e:
        return None, type(e).__name__
    finally:
        if alarma:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, viejo)
        if previo is None:
            sys.modules.pop("pyscript", None)
        else:
            sys.modules["pyscript"] = previo


def _importa_pyscript(arbol):
    """Nombres importados de pyscript y nombres definidos en el propio código."""
    importados, definidos, usados = set(), set(), set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.ImportFrom) and nodo.module == "pyscript":
            for a in nodo.names:
                importados.add(a.asname or a.name)
        elif isinstance(nodo, (ast.Import, ast.ImportFrom)):
            for a in nodo.names:
                definidos.add((a.asname or a.name).split(".")[0])
        elif isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definidos.add(nodo.name)
            for arg in nodo.args.args if hasattr(nodo, "args") else ():
                definidos.add(arg.arg)
        elif isinstance(nodo, ast.Name):
            if isinstance(nodo.ctx, ast.Load):
                usados.add(nodo.id)
            else:
                definidos.add(nodo.id)
    return importados, definidos, usados


# ── El validador ─────────────────────────────────────────────────────────────

def validar_actividades(nivel, act):
    """Revisa todas las semanas de un nivel; junta los fallos y sale con 1 si hay alguno."""
    fallos = []
    if nivel not in MAPA_MOTORES:
        print(f"✗ nivel desconocido: {nivel!r}")
        raise SystemExit(1)
    if not isinstance(act, dict):
        print(f"✗ {nivel}: ACT debe ser un dict {{1..12: semana}}")
        raise SystemExit(1)
    for k in act:
        if not (_es_int(k) and 1 <= k <= 12):
            fallos.append(f"{nivel}: clave de semana inválida {k!r} (deben ser int 1–12)")
    faltan = [n for n in range(1, 13) if n not in act]
    for n in range(1, 13):
        if n in act:
            fallos += [f"{nivel} S{n} · {f}" for f in _validar_semana(nivel, n, act[n])]
    if faltan:
        print(f"  aviso {nivel}: sin actividades en semanas {faltan} (conservan la presentación anterior)")
    if fallos:
        print(f"✗ actividades {nivel}: {len(fallos)} fallo(s)")
        for f in fallos:
            print("   ✗", f)
        raise SystemExit(1)
    return None


def _validar_semana(nivel, n, s):
    F = []
    ok = F.append
    if not isinstance(s, dict):
        return ["la semana debe ser un dict"]
    codigos_py = []   # (etiqueta, código) para las reglas de la casa

    if not _texto(s.get("hoy"), 90):
        ok("hoy: str no vacío de ≤90 caracteres")
    esc = s.get("escena")
    if esc is not None and esc not in IL.ESCENAS:
        ok(f"escena {esc!r} no está en ilustra.ESCENAS")

    # Calentamiento
    c = s.get("calentamiento")
    if not isinstance(c, dict):
        ok("calentamiento: falta")
    else:
        if not _texto(c.get("pregunta"), 110):
            ok("calentamiento.pregunta: str ≤110")
        _opciones(F, "calentamiento", c.get("opciones"), 4, 4)
        if not (_es_int(c.get("correcta")) and 0 <= c["correcta"] <= 3):
            ok("calentamiento.correcta: int 0–3")
        if not _texto(c.get("por_que")):
            ok("calentamiento.por_que: str")

    # Ejemplo
    e = s.get("ejemplo")
    if not isinstance(e, dict):
        ok("ejemplo: falta")
    else:
        if not _texto(e.get("titulo")):
            ok("ejemplo.titulo: str")
        leng = e.get("lenguaje")
        if leng not in LENGUAJES:
            ok(f"ejemplo.lenguaje {leng!r} no es uno de {LENGUAJES}")
        cod = e.get("codigo")
        if _lineas(F, "ejemplo.codigo", cod, 2, 14):
            notas = e.get("notas")
            if not isinstance(notas, (list, tuple)) or not 1 <= len(notas) <= 4:
                ok("ejemplo.notas: 1–4 pares (linea, texto)")
            else:
                for i, nota in enumerate(notas):
                    if (not isinstance(nota, (list, tuple)) or len(nota) != 2 or not _es_int(nota[0])
                            or not _texto(nota[1])):
                        ok(f"ejemplo.notas[{i}]: debe ser (linea_int, texto)")
                    elif not 1 <= nota[0] <= len(cod) or not cod[nota[0] - 1].strip():
                        ok(f"ejemplo.notas[{i}]: la línea {nota[0]} no existe o está en blanco")
            if leng == "python":
                src = "\n".join(cod)
                codigos_py.append(("ejemplo", src))
                arbol, err = compilar(src)
                if err:
                    ok(f"ejemplo no compila: {err}")
                else:
                    _pyscript(F, "ejemplo", arbol)

    # Retos
    retos = s.get("retos")
    tipos = ["predice", "completa", "ordena", "error"]
    if not isinstance(retos, list) or [r.get("tipo") if isinstance(r, dict) else None for r in retos] != tipos:
        ok(f"retos: deben ser exactamente 4 dicts con tipo {tipos} en ese orden")
    else:
        for r in retos:
            _reto(F, r, codigos_py)

    # Retos extra (2do y 3ro): mismas reglas, 1 o 2, de cualquiera de los cuatro tipos.
    ex = s.get("retos_extra")
    if ex is not None:
        if not (isinstance(ex, list) and 1 <= len(ex) <= 2
                and all(isinstance(r, dict) and r.get("tipo") in ("predice", "completa", "ordena", "error") for r in ex)):
            ok("retos_extra: 1 o 2 retos de tipo predice, completa, ordena o error")
        else:
            for r in ex:
                _reto(F, r, codigos_py)

    # Juego
    j = s.get("juego")
    esperado = MAPA_MOTORES[nivel][n]
    if not isinstance(j, dict):
        ok("juego: falta")
    else:
        if j.get("tipo") != esperado:
            ok(f"juego.tipo es {j.get('tipo')!r}; esta semana toca {esperado!r}")
        if not _texto(j.get("titulo"), 60):
            ok("juego.titulo: str ≤60")
        if not _texto(j.get("pista"), 40):
            ok("juego.pista: str ≤40")
        if j.get("tipo") == esperado:
            try:
                for f in VALIDA_MOTOR.get(esperado, lambda j: [])(j):
                    ok(f"juego ({esperado}): {f}")
            except Exception as ex:
                ok(f"juego ({esperado}): configuración ilegible ({type(ex).__name__}: {ex})")

    # Práctica
    p = s.get("practica")
    # La ruta es la misma en los tres grados: la S1 va sin computadora y la S10
    # se hace en Teachable Machine, fuera del editor de la clase.
    if n == 1:
        tipo_p = "desenchufada"
    elif n == 10:
        tipo_p = "enlace"
    else:
        tipo_p = "editor"
    if not isinstance(p, dict):
        ok("practica: falta")
    else:
        if p.get("tipo") != tipo_p:
            ok(f"practica.tipo es {p.get('tipo')!r}; esta semana toca {tipo_p!r}")
        if not _texto(p.get("titulo")):
            ok("practica.titulo: str")
        pasos = p.get("pasos")
        if not isinstance(pasos, list) or not 3 <= len(pasos) <= 7 or not all(_texto(x) for x in pasos):
            ok("practica.pasos: 3–7 str")
        if p.get("tipo") == "editor":
            for k in ("html", "css", "py"):
                if not isinstance(p.get(k), str):
                    ok(f"practica.{k}: str (puede ser \"\")")
            py = p.get("py") if isinstance(p.get("py"), str) else ""
            htm = p.get("html") if isinstance(p.get("html"), str) else ""
            if py.strip():
                codigos_py.append(("practica.py", py))
                arbol, err = compilar(py)
                if err:
                    ok(f"practica.py no compila: {err}")
                else:
                    _pyscript(F, "practica.py", arbol)
                ids = set(re.findall(r"""\bid\s*=\s*["']([^"']+)["']""", htm))
                usados = re.findall(r"""@when\(\s*["'][^"']*["']\s*,\s*["']#([\w-]+)""", py)
                usados += re.findall(r"""querySelector(?:All)?\(\s*["']#([\w-]+)""", py)
                for u in sorted(set(usados)):
                    if u not in ids:
                        ok(f"practica: el Python usa #{u} pero el html no tiene id=\"{u}\"")
        elif p.get("tipo") == "enlace":
            if not (isinstance(p.get("url"), str) and p["url"].startswith("https://")):
                ok("practica.url: debe empezar por https://")
            if not _texto(p.get("boton")):
                ok("practica.boton: str")

    # Segundo juego, chuleta y recursos: opcionales.
    j2 = s.get("juego2")
    if j2 is not None:
        if not isinstance(j2, dict) or j2.get("tipo") not in VALIDA_MOTOR and j2.get("tipo") != "ppt":
            ok("juego2.tipo: un motor con configuración (no una demo)")
        else:
            if not _texto(j2.get("titulo"), 60):
                ok("juego2.titulo: str ≤60")
            if not _texto(j2.get("pista"), 40):
                ok("juego2.pista: str ≤40")
            try:
                for f in VALIDA_MOTOR.get(j2["tipo"], lambda j: [])(j2):
                    ok(f"juego2 ({j2['tipo']}): {f}")
            except Exception as ex:
                ok(f"juego2: configuración ilegible ({type(ex).__name__}: {ex})")
    ch = s.get("chuleta")
    if ch is not None:
        lin = ch.get("lineas") if isinstance(ch, dict) else None
        if not (isinstance(ch, dict) and _texto(ch.get("titulo"), 60) and isinstance(lin, list) and 4 <= len(lin) <= 6
                and all(isinstance(x, (list, tuple)) and len(x) == 2 and _texto(x[0]) and _cols(x[0]) <= 52
                        and _texto(x[1], 90) for x in lin)):
            ok("chuleta: {titulo ≤60, lineas: 4–6 (código ≤52, texto ≤90)}")
    rec = s.get("recursos")
    if rec is not None:
        if not (isinstance(rec, list) and 2 <= len(rec) <= 4 and all(
                isinstance(x, (list, tuple)) and len(x) == 3 and _texto(x[0], 40)
                and isinstance(x[1], str) and x[1].startswith("https://") and _texto(x[2], 110) for x in rec)):
            ok("recursos: 2–4 (nombre ≤40, url https, texto ≤110)")

    # «Tu primera variable»: dinámica en grupo + taller en pantalla.
    pri = s.get("primera")
    if pri is not None:
        d = pri.get("dinamica") if isinstance(pri, dict) else None
        tl = pri.get("taller") if isinstance(pri, dict) else None
        mt = pri.get("montana") if isinstance(pri, dict) else None
        esc = pri.get("escalera") if isinstance(pri, dict) else None
        if pri.get("titulo") is not None and not _texto(pri["titulo"], 40):
            ok("primera.titulo: str ≤40")
        t2 = pri.get("taller2") if isinstance(pri, dict) else None
        if isinstance(t2, dict):
            # El taller de todas las demás semanas: misiones + un comprobador.
            if not (isinstance(d, dict) and _texto(d.get("titulo"), 40) and isinstance(d.get("minutos"), int)
                    and 2 <= d["minutos"] <= 8 and isinstance(d.get("pasos"), list) and 2 <= len(d["pasos"]) <= 5
                    and all(_texto(x, 120) for x in d["pasos"])):
                ok("primera.dinamica: {titulo ≤40, minutos 2–8, pasos 2–5 ≤120}")
            ms = t2.get("misiones")
            tipo = t2.get("tipo")
            PIDE = {"condicion": ("variable", "casos", "espera"), "lista": ("variable", "lista", "espera"),
                    "funcion": ("nombre", "parametros"), "evento": ("id",), "azar": (),
                    "etiqueta": ("etiqueta",), "exacto": ("espera",),
                    "ordenar": ("pasos", "orden"), "clasificar": ("grupos", "correcto")}
            if tipo not in PIDE:
                ok(f"primera.taller2.tipo: uno de {', '.join(sorted(PIDE))}")
            elif not (isinstance(ms, list) and 3 <= len(ms) <= 6):
                ok("primera.taller2.misiones: 3–6")
            else:
                for i, x in enumerate(ms):
                    # La pista es obligatoria: una misión sin guía es una
                    # adivinanza, y eso se ve en clase como «no lo entiendo».
                    bien = isinstance(x, dict) and _texto(x.get("pide"), 110) and _texto(x.get("pista"), 110)
                    bien = bien and all(x.get(c) is not None for c in PIDE[tipo])
                    if bien and tipo == "condicion":
                        bien = (isinstance(x["casos"], list) and isinstance(x["espera"], list)
                                and len(x["casos"]) == len(x["espera"]) and 2 <= len(x["casos"]) <= 6
                                and all(isinstance(v, bool) for v in x["espera"]))
                    if bien and tipo == "lista":
                        bien = isinstance(x["lista"], list) and isinstance(x["espera"], list)
                    if bien and tipo == "funcion":
                        bien = isinstance(x["parametros"], list) and all(isinstance(v, str) for v in x["parametros"])
                    if bien and tipo == "azar":
                        bien = (x.get("tipo") == "choice" and isinstance(x.get("lista"), list) and x.get("variable")) or \
                               (_es_int(x.get("desde")) and _es_int(x.get("hasta")) and x["desde"] < x["hasta"])
                    if bien and tipo == "exacto":
                        bien = isinstance(x["espera"], list) and x["espera"] and all(isinstance(v, str) for v in x["espera"])
                    if bien and tipo == "ordenar":
                        bien = (isinstance(x["pasos"], list) and isinstance(x["orden"], list)
                                and 3 <= len(x["pasos"]) <= 6 and sorted(x["orden"]) == list(range(len(x["pasos"]))))
                    if bien and tipo == "clasificar":
                        bien = (isinstance(x["grupos"], list) and 2 <= len(x["grupos"]) <= 4
                                and isinstance(x["correcto"], int) and 0 <= x["correcto"] < len(x["grupos"]))
                    if not bien:
                        ok(f"primera.taller2.misiones[{i}]: le falta algo para el tipo {tipo!r}")
        elif isinstance(esc, dict):
            # La escalera: se escribe la cabecera del ciclo y se compara la
            # secuencia que produce, no el texto.
            ms = esc.get("misiones")
            if not (isinstance(d, dict) and _texto(d.get("titulo"), 40) and isinstance(d.get("minutos"), int)
                    and 2 <= d["minutos"] <= 8 and isinstance(d.get("pasos"), list) and 2 <= len(d["pasos"]) <= 5
                    and all(_texto(x, 120) for x in d["pasos"])):
                ok("primera.dinamica: {titulo ≤40, minutos 2–8, pasos 2–5 ≤120}")
            if not (isinstance(ms, list) and 3 <= len(ms) <= 6):
                ok("primera.escalera.misiones: 3–6")
            else:
                for i, x in enumerate(ms):
                    sec = x.get("secuencia") if isinstance(x, dict) else None
                    bien = (isinstance(x, dict) and _texto(x.get("pide"), 110)
                            and isinstance(sec, list) and 2 <= len(sec) <= 12 and all(_es_int(v) for v in sec))
                    if bien:
                        paso = sec[1] - sec[0]
                        bien = paso != 0 and all(b - a == paso for a, b in zip(sec, sec[1:]))
                    if not bien:
                        ok(f"primera.escalera.misiones[{i}]: {{pide ≤110, secuencia 2–12 enteros con salto constante}}")
        elif isinstance(mt, dict):
            # La montaña reemplaza al taller: misiones que se escriben a mano.
            ms = mt.get("misiones")
            if not (isinstance(d, dict) and _texto(d.get("titulo"), 40) and isinstance(d.get("minutos"), int)
                    and 2 <= d["minutos"] <= 8 and isinstance(d.get("pasos"), list) and 2 <= len(d["pasos"]) <= 5
                    and all(_texto(x, 120) for x in d["pasos"])):
                ok("primera.dinamica: {titulo ≤40, minutos 2–8, pasos 2–5 ≤120}")
            if not (isinstance(ms, list) and 3 <= len(ms) <= 6):
                ok("primera.montana.misiones: 3–6")
            else:
                for i, x in enumerate(ms):
                    bien = (isinstance(x, dict) and _texto(x.get("pide"), 110)
                            and isinstance(x.get("var"), str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", x["var"])
                            and x.get("tipo") in ("str", "int") and isinstance(x.get("valor"), str) and x["valor"]
                            and (x["tipo"] == "str" or re.fullmatch(r"-?\d+", x["valor"])))
                    if not bien:
                        ok(f"primera.montana.misiones[{i}]: {{pide ≤110, var nombre válido, tipo str|int, valor}}")
        elif not (isinstance(pri, dict) and isinstance(d, dict) and isinstance(tl, dict)
                and _texto(d.get("titulo"), 40) and isinstance(d.get("minutos"), int) and 3 <= d["minutos"] <= 8
                and isinstance(d.get("pasos"), list) and 3 <= len(d["pasos"]) <= 5
                and all(_texto(x, 120) for x in d["pasos"])
                and _texto(tl.get("nombre"), 20) and _texto(tl.get("valor"), 20)
                and isinstance(tl.get("cambia"), int) and tl["cambia"] > 0
                and tl.get("cambia_como", "suma") in ("suma", "asigna")):
            ok("primera: {dinamica{titulo, minutos 3–8, pasos 3–5 ≤120}, taller{nombre, valor, cambia, cambia_como}}")
        elif not mt and not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", tl["nombre"]):
            ok(f"primera.taller.nombre: {tl['nombre']!r} no es un nombre válido en Python")
    if not isinstance(s.get("definir_primero", False), bool):
        ok("definir_primero: True o False")

    rd = s.get("reto_dia")
    if rd is not None and not _texto(rd):
        ok("reto_dia: str o None")
    sa = s.get("salida")
    if not isinstance(sa, dict) or not _texto(sa.get("pregunta")) or not _texto(sa.get("respuesta")):
        ok("salida: {pregunta: str, respuesta: str}")

    # Reglas de la casa sobre todo el Python de la semana
    for etq, src in codigos_py:
        for rx, nombre in PROHIBIDO:
            if rx.search(src):
                ok(f"{etq}: no se usa `{nombre}` en este curso")
        if RE_PRINT.search(src) and not (nivel == "1ro" and n == 3):
            ok(f"{etq}: `print(` solo se permite en 1ro semana 3; usa display()")
    return F


def _opciones(F, etq, ops, mn, mx):
    if (not isinstance(ops, list) or not mn <= len(ops) <= mx
            or not all(_texto(o, 48) for o in ops)):
        F.append(f"{etq}.opciones: {mn}–{mx} str de ≤48" if mn != mx else f"{etq}.opciones: {mn} str de ≤48")
        return False
    if len(set(ops)) != len(ops):
        F.append(f"{etq}.opciones: repetidas")
        return False
    return True


def _lineas(F, etq, lineas, mn, mx):
    if not isinstance(lineas, list) or not mn <= len(lineas) <= mx or not all(isinstance(x, str) for x in lineas):
        F.append(f"{etq}: lista de {mn}–{mx} str")
        return False
    largas = [i + 1 for i, x in enumerate(lineas) if _cols(x) > 52]
    if largas:
        F.append(f"{etq}: líneas de más de 52 columnas: {largas}")
    return True


def _pyscript(F, etq, arbol):
    importados, definidos, usados = _importa_pyscript(arbol)
    faltan = sorted((usados & NOMBRES_PYSCRIPT) - importados - definidos)
    if faltan:
        F.append(f"{etq}: usa {', '.join(faltan)} sin `from pyscript import {', '.join(faltan)}`")


def _reto(F, r, codigos_py):
    t = r["tipo"]
    etq = f"retos.{t}"
    leng = r.get("lenguaje")
    if leng not in LENGUAJES:
        F.append(f"{etq}.lenguaje {leng!r} no es uno de {LENGUAJES}")
    py = leng == "python"

    if t in ("predice", "completa"):
        okc = _lineas(F, f"{etq}.codigo", r.get("codigo"), 1, 10)
        okop = _opciones(F, etq, r.get("opciones"), 3, 4)
        cor = r.get("correcta")
        if not (okop and _es_int(cor) and 0 <= cor < len(r["opciones"])):
            F.append(f"{etq}.correcta: índice dentro de opciones")
            okop = False
        if not _texto(r.get("explica")):
            F.append(f"{etq}.explica: str")
        if not okc:
            return
        src = "\n".join(r["codigo"])
        if t == "completa" and src.count("___") != 1:
            F.append(f"{etq}.codigo: debe tener exactamente un ___ (tiene {src.count('___')})")
            return
        if not py:
            return
        if t == "predice":
            codigos_py.append((etq, src))
            if any(w in src for w in NO_EJECUTAR):
                _, err = compilar(src)
                if err:
                    F.append(f"{etq} no compila: {err}")
                return
            _, err = compilar(src)
            if err:
                F.append(f"{etq} no compila: {err}")
                return
            salida, exc = ejecutar(src)
            if exc == "_Tiempo":
                F.append(f"{etq}: tardó más de 2 s (¿bucle infinito?)")
                return
            if not okop:
                return
            ops = r["opciones"]
            validas = {salida} if exc is None else {exc, "Error"}
            if ops[cor] not in validas:
                real = salida if exc is None else f"{exc} (o Error)"
                F.append(f"{etq}: la salida real es {real!r} pero la opción correcta es {ops[cor]!r}")
            otras = [o for i, o in enumerate(ops) if i != cor and o in validas]
            if otras:
                F.append(f"{etq}: otra opción también es correcta: {otras}")
        else:
            if not okop:
                return
            lleno = src.replace("___", r["opciones"][cor])
            codigos_py.append((etq, lleno))
            _, err = compilar(lleno)
            if err:
                F.append(f"{etq}: con la opción correcta no compila: {err}")

    elif t == "ordena":
        if not _texto(r.get("enunciado")):
            F.append(f"{etq}.enunciado: str")
        lin = r.get("lineas")
        if not _lineas(F, f"{etq}.lineas", lin, 3, 7):
            return
        if len(set(lin)) < 2:
            F.append(f"{etq}.lineas: no pueden ser todas iguales")
            return
        if py:
            src = "\n".join(lin)
            codigos_py.append((etq, src))
            _, err = compilar(src)
            if err:
                F.append(f"{etq}: las líneas en orden no compilan: {err}")

    elif t == "error":
        lin = r.get("lineas")
        if not _lineas(F, f"{etq}.lineas", lin, 3, 8):
            return
        mala = r.get("mala")
        if not (_es_int(mala) and 0 <= mala < len(lin)):
            F.append(f"{etq}.mala: índice 0-based dentro de lineas")
            return
        arr = r.get("arreglo")
        if not isinstance(arr, str) or not arr.strip() or arr == lin[mala]:
            F.append(f"{etq}.arreglo: str distinto de la línea mala")
            return
        if _cols(arr) > 52:
            F.append(f"{etq}.arreglo: más de 52 columnas")
        if not _texto(r.get("explica")):
            F.append(f"{etq}.explica: str")
        if py:
            arreglado = list(lin)
            arreglado[mala] = arr
            src = "\n".join(arreglado)
            codigos_py.append((etq, "\n".join(lin) + "\n" + arr))
            _, err = compilar(src)
            if err:
                F.append(f"{etq}: con el arreglo no compila: {err}")


# ── Validadores de cada motor ────────────────────────────────────────────────

def _v_robot(j):
    F = []
    tam = j.get("tam")
    if not (_es_int(tam) and 5 <= tam <= 7):
        return ["tam: int 5–7"]
    dentro = lambda x, y: 0 <= x < tam and 0 <= y < tam
    ini, meta, muros = j.get("inicio"), j.get("meta"), j.get("muros", [])
    if not (isinstance(ini, list) and len(ini) == 3 and _es_int(ini[0]) and _es_int(ini[1])
            and ini[2] in DIRS and dentro(ini[0], ini[1])):
        F.append("inicio: [x, y, 'N'|'E'|'S'|'O'] dentro de la cuadrícula")
    if not (isinstance(meta, (list, tuple)) and len(meta) == 2 and all(_es_int(v) for v in meta)
            and dentro(*meta)):
        F.append("meta: [x, y] dentro de la cuadrícula")
    if not isinstance(muros, list) or not all(isinstance(m, (list, tuple)) and len(m) == 2
                                              and all(_es_int(v) for v in m) and dentro(*m) for m in muros):
        F.append("muros: lista de [x, y] dentro de la cuadrícula")
    mx = j.get("max")
    if not (_es_int(mx) and 1 <= mx <= 10):
        F.append("max: int 1–10")
    cartas = j.get("cartas")
    if not (isinstance(cartas, list) and cartas and all(c in CARTAS for c in cartas)):
        F.append(f"cartas: subconjunto no vacío de {list(CARTAS)}")
    if F:
        return F
    muro = {tuple(m) for m in muros}
    if tuple(ini[:2]) in muro or tuple(meta) in muro:
        return ["inicio o meta encima de un muro"]
    if tuple(ini[:2]) == tuple(meta):
        return ["la meta no puede ser la casilla de inicio"]
    if robot_camino(j) is None:
        F.append(f"la meta no se alcanza con ≤{mx} cartas usando {cartas}")
    return F


def robot_camino(j):
    """BFS sobre (x, y, dir). Devuelve la lista de cartas más corta o None."""
    tam, muro, meta = j["tam"], {tuple(m) for m in j.get("muros", [])}, tuple(j["meta"])
    cartas = set(j["cartas"])
    basicas = [c for c in ("AVANZA", "GIRA_IZQ", "GIRA_DER") if c in cartas]

    def paso(estado, c):
        x, y, d = estado
        if c == "GIRA_IZQ":
            return (x, y, IZQ[d])
        if c == "GIRA_DER":
            return (x, y, DER[d])
        dx, dy = DIRS[d]
        nx, ny = x + dx, y + dy
        if not (0 <= nx < tam and 0 <= ny < tam) or (nx, ny) in muro:
            return None
        return (nx, ny, d)

    inicio = (j["inicio"][0], j["inicio"][1], j["inicio"][2])
    frente = [(inicio, [])]
    visto = {inicio: 0}
    while frente:
        nuevo = []
        for estado, prog in frente:
            movs = [([c], [c]) for c in basicas]
            if "REPITE_2" in cartas:
                movs += [(["REPITE_2", c], [c, c]) for c in basicas]
            for cartas_usadas, efectos in movs:
                costo = len(prog) + len(cartas_usadas)
                if costo > j["max"]:
                    continue
                e = estado
                gano = False
                for c in efectos:
                    e = paso(e, c)
                    if e is None:
                        break
                    if (e[0], e[1]) == meta:
                        gano = True
                        break
                if e is None:
                    continue
                if gano:
                    return prog + cartas_usadas
                if visto.get(e, 99) > costo:
                    visto[e] = costo
                    nuevo.append((e, prog + cartas_usadas))
        frente = nuevo
    return None


def _v_clasifica(j):
    F = []
    cub, items = j.get("cubetas"), j.get("items")
    if not (isinstance(cub, list) and 2 <= len(cub) <= 4 and all(_texto(c) for c in cub)):
        return ["cubetas: 2–4 str"]
    if not (isinstance(items, list) and 6 <= len(items) <= 12):
        return ["items: 6–12 pares [texto, idx_cubeta]"]
    usadas = set()
    for i, it in enumerate(items):
        if not (isinstance(it, (list, tuple)) and len(it) == 2 and _texto(it[0])
                and _es_int(it[1]) and 0 <= it[1] < len(cub)):
            F.append(f"items[{i}]: [texto, idx_cubeta válido]")
        else:
            usadas.add(it[1])
    vacias = [cub[k] for k in range(len(cub)) if k not in usadas]
    if vacias and not F:
        F.append(f"cubetas sin ningún item: {vacias}")
    return F


def _v_marcador(j):
    F = []
    vars_ = j.get("variables")
    if not isinstance(vars_, dict) or not all(isinstance(k, str) and k.isidentifier() for k in vars_):
        return ["variables: dict {nombre: valor}"]
    for k, v in vars_.items():
        if not (_es_num(v) or isinstance(v, str)):
            F.append(f"variables.{k}: int, float o str")
    nombres = set(vars_)
    cajas = j.get("cajas", [])
    if not isinstance(cajas, list):
        F.append("cajas: lista")
        cajas = []
    for i, c in enumerate(cajas):
        if not (isinstance(c, dict) and isinstance(c.get("var"), str) and c["var"].isidentifier()
                and isinstance(c.get("valor"), str)):
            F.append(f"cajas[{i}]: {{var: str, valor: str}}")
        else:
            nombres.add(c["var"])
    recargar = bool(j.get("recargar", False))
    bot = j.get("botones")
    if not isinstance(bot, list) or not bot:
        return F + ["botones: lista no vacía"]
    for i, b in enumerate(bot):
        etq = f"botones[{i}]"
        if not isinstance(b, dict) or not _texto(b.get("texto")) or not isinstance(b.get("linea"), str):
            F.append(f"{etq}: necesita texto y linea")
            continue
        if "calc" in b:
            c = b["calc"]
            if not isinstance(c, dict):
                F.append(f"{etq}.calc: dict")
                continue
            if c.get("izq") not in nombres:
                F.append(f"{etq}.calc.izq {c.get('izq')!r} no es una variable")
            if c.get("op") not in ("+", "-", "*", "/", "//", "%"):
                F.append(f"{etq}.calc.op inválido")
            der = c.get("der")
            if not (_es_num(der) or der in nombres):
                F.append(f"{etq}.calc.der: variable o número")
            if c.get("convertir") not in (None, "int", "float"):
                F.append(f"{etq}.calc.convertir: None, 'int' o 'float'")
            if not (isinstance(c.get("destino"), str) and c["destino"].isidentifier()):
                F.append(f"{etq}.calc.destino: nombre de variable")
            else:
                nombres.add(c["destino"])
        elif b.get("op") in ("guardar", "cargar"):
            if not recargar:
                F.append(f"{etq}: guardar/cargar solo con recargar: True")
        elif b.get("op") in ("+=", "-=", "="):
            if b.get("var") not in nombres:
                F.append(f"{etq}.var {b.get('var')!r} no es una variable")
            if "valor" not in b or not (_es_num(b["valor"]) or isinstance(b["valor"], str)):
                F.append(f"{etq}.valor: número o str")
        else:
            F.append(f"{etq}: op debe ser +=, -=, =, guardar, cargar, o usar calc")
    meta = j.get("meta")
    if meta is not None:
        if not (isinstance(meta, dict) and meta.get("var") in nombres and "valor" in meta
                and _es_num(meta.get("segundos")) and meta["segundos"] > 0):
            F.append("meta: {var existente, valor, segundos > 0}")
    return F


def _cumple(v, op, x):
    return {"<": v < x, "<=": v <= x, ">": v > x, ">=": v >= x, "==": v == x, "!=": v != x}[op]


def ramas_rama(ramas, v, secreto=None):
    """Índice de la primera rama que se cumple con el valor v."""
    for i, r in enumerate(ramas):
        if r["op"] == "else":
            return i
        x = secreto if r["valor"] == "secreto" else r["valor"]
        if _cumple(v, r["op"], x):
            return i
    return None


def _v_ramas(j):
    F = []
    if not (isinstance(j.get("variable"), str) and j["variable"].isidentifier()):
        F.append("variable: nombre de variable")
    if j.get("entrada") not in ("slider", "numero"):
        F.append("entrada: 'slider' o 'numero'")
    mn, mx, paso = j.get("min"), j.get("max"), j.get("paso")
    if not (_es_num(mn) and _es_num(mx) and _es_num(paso) and mn < mx and paso > 0):
        return F + ["min < max y paso > 0 (números)"]
    secreto = bool(j.get("secreto", False))
    ramas = j.get("ramas")
    if not isinstance(ramas, list) or len(ramas) < 2:
        return F + ["ramas: al menos 2 (la última con op 'else')"]
    for i, r in enumerate(ramas):
        if not isinstance(r, dict) or not _texto(r.get("mensaje")):
            F.append(f"ramas[{i}]: necesita mensaje")
            continue
        ultima = i == len(ramas) - 1
        if ultima != (r.get("op") == "else"):
            F.append(f"ramas[{i}]: solo la última rama es 'else' (y la última debe serlo)")
        if r.get("op") != "else":
            if r.get("op") not in ("<", "<=", ">", ">=", "==", "!="):
                F.append(f"ramas[{i}].op inválido")
            if not (_es_num(r.get("valor")) or (r.get("valor") == "secreto" and secreto)):
                F.append(f"ramas[{i}].valor: número (o 'secreto' si secreto: True)")
    if F:
        return F
    pasos = int(round((mx - mn) / paso))
    if pasos > 5000:
        return ["demasiados valores entre min y max con ese paso (máx. 5000)"]
    valores = [round(mn + k * paso, 10) for k in range(pasos + 1) if mn + k * paso <= mx + 1e-9]
    secretos = [None]
    if secreto:
        import math
        secretos = list(range(math.ceil(mn), math.floor(mx) + 1))[:400] or [None]
    vistas = set()
    for s in secretos:
        for v in valores:
            k = ramas_rama(ramas, v, s)
            if k is not None:
                vistas.add(k)
    nunca = [i for i in range(len(ramas)) if i not in vistas]
    if nunca:
        F.append(f"ramas que ningún valor alcanza: {nunca}")
    return F


def bucle_traza(j):
    """Simula el bucle. Devuelve lista de (valor_var, acumulado_o_None) o None si pasa de 12."""
    acu = j.get("acumula")
    total = acu["inicio"] if acu else None

    def acumular(v):
        nonlocal total
        if not acu:
            return None
        x = v if acu["usa"] == "var" else acu["usa"]
        total = total + x if acu["op"] == "+=" else total * x
        return total

    traza = []
    if j["modo"] == "for":
        it = j["iterable"]
        if "range" in it:
            seq = range(*it["range"])
        else:
            seq = it["lista"]
        for v in seq:
            if len(traza) >= 12:
                return None
            traza.append((v, acumular(v)))
    else:
        m = j["mientras"]
        v = m["inicio"]
        while _cumple(v, m["op"], m["valor"]):
            if len(traza) >= 12:
                return None
            traza.append((v, acumular(v)))
            v = v + m["cambio"]
    return traza


def _v_bucle(j):
    F = []
    modo = j.get("modo")
    if modo == "for":
        if not (isinstance(j.get("var"), str) and j["var"].isidentifier()):
            F.append("var: nombre de variable")
        it = j.get("iterable")
        if isinstance(it, dict) and "range" in it:
            r = it["range"]
            if not (isinstance(r, list) and 1 <= len(r) <= 3 and all(_es_int(x) for x in r)
                    and (len(r) < 3 or r[2] != 0)):
                F.append("iterable.range: [a, b, paso] enteros, paso ≠ 0")
        elif isinstance(it, dict) and "lista" in it:
            if not isinstance(it["lista"], list):
                F.append("iterable.lista: lista")
        else:
            F.append("iterable: {'range': [a,b,paso]} o {'lista': [...]}")
    elif modo == "while":
        m = j.get("mientras")
        if not (isinstance(m, dict) and isinstance(m.get("var"), str) and m["var"].isidentifier()
                and m.get("op") in ("<", "<=", ">", ">=")
                and all(_es_num(m.get(k)) for k in ("valor", "inicio", "cambio"))):
            F.append("mientras: {var, op <|<=|>|>=, valor, inicio, cambio}")
    else:
        return ["modo: 'for' o 'while'"]
    ap = j.get("apuesta")
    if ap is not None:
        ops = ap.get("opciones") if isinstance(ap, dict) else None
        if not (isinstance(ap, dict) and _texto(ap.get("pregunta"), 90) and isinstance(ops, list)
                and 2 <= len(ops) <= 4 and all(_texto(o, 24) for o in ops)
                and isinstance(ap.get("correcta"), int) and 0 <= ap["correcta"] < len(ops)):
            F.append("apuesta: {pregunta ≤90, opciones 2–4 ≤24, correcta}")
    acu = j.get("acumula")
    if acu is not None:
        if not (isinstance(acu, dict) and isinstance(acu.get("var"), str) and acu["var"].isidentifier()
                and acu.get("op") in ("+=", "*=") and _es_num(acu.get("inicio"))
                and (acu.get("usa") == "var" or _es_num(acu.get("usa")))):
            F.append("acumula: {var, op +=|*=, inicio num, usa 'var'|num} o None")
    cuerpo = j.get("cuerpo")
    if not (isinstance(cuerpo, list) and all(isinstance(x, str) for x in cuerpo)):
        F.append("cuerpo: lista de str")
    if F:
        return F
    try:
        traza = bucle_traza(j)
    except Exception as ex:
        return [f"no se puede simular ({type(ex).__name__}: {ex})"]
    if traza is None:
        F.append("más de 12 vueltas")
    elif not traza:
        F.append("el bucle no da ninguna vuelta")
    return F


def _v_caza(j):
    F = []
    if not (isinstance(j.get("nombre"), str) and j["nombre"].isidentifier()):
        F.append("nombre: nombre de variable")
    ini = j.get("inicial")
    if not (isinstance(ini, list) and 4 <= len(ini) <= 8 and all(_texto(x) for x in ini)):
        F.append("inicial: 4-8 textos")
    ex = j.get("extra", [])
    if not (isinstance(ex, list) and len(ex) <= 3 and all(_texto(x) for x in ex)):
        F.append("extra: hasta 3 textos")
    if isinstance(ini, list) and isinstance(ex, list) and len(set(map(str, ini + ex))) != len(ini + ex):
        # Con dos iguales, «¿en qué posición está X?» tiene dos respuestas.
        F.append("inicial + extra: sin repetidos")
    ro = j.get("rondas")
    if not (_es_int(ro) and 4 <= ro <= 12):
        F.append("rondas: int 4-12")
    g = j.get("gana")
    if not (_es_int(g) and _es_int(ro) and 1 <= g <= ro):
        F.append("gana: int de 1 a rondas")
    return F


OPS_LISTA = {"lista": {"append", "pop", "len", "indice", "in"}, "dict": {"get", "set", "del", "len", "in"}}


def _v_lista(j):
    F = []
    modo = j.get("modo")
    if modo not in OPS_LISTA:
        return ["modo: 'lista' o 'dict'"]
    if not (isinstance(j.get("nombre"), str) and j["nombre"].isidentifier()):
        F.append("nombre: nombre de variable")
    ini = j.get("inicial")
    if modo == "lista" and not isinstance(ini, list):
        F.append("inicial: lista")
    if modo == "dict" and not isinstance(ini, dict):
        F.append("inicial: dict")
    ops = j.get("ops")
    if not (isinstance(ops, list) and ops and set(ops) <= OPS_LISTA[modo]):
        F.append(f"ops: subconjunto no vacío de {sorted(OPS_LISTA[modo])}")
        ops = []
    val = j.get("valores", [])
    if not (isinstance(val, list) and all(_es_num(v) or isinstance(v, str) for v in val)):
        F.append("valores: lista de str o números")
    elif not val and set(ops) & {"append", "set", "in"}:
        F.append("valores: hace falta al menos uno para append/set/in")
    return F


def _v_css(j):
    F = []
    ctr = j.get("controles")
    if not (isinstance(ctr, list) and ctr):
        F.append("controles: lista no vacía")
        ctr = []
    for i, c in enumerate(ctr):
        if not isinstance(c, dict) or c.get("prop") not in CSS_PROPS:
            F.append(f"controles[{i}].prop debe ser una de {sorted(CSS_PROPS)}")
            continue
        if c.get("tipo") == "slider":
            if not (_es_num(c.get("min")) and _es_num(c.get("max")) and c["min"] < c["max"]
                    and c.get("unidad") in ("px", "rem", "%")):
                F.append(f"controles[{i}]: slider con min < max y unidad px|rem|%")
        elif c.get("tipo") == "opciones":
            if not (isinstance(c.get("valores"), list) and len(c["valores"]) >= 2
                    and all(_texto(v) for v in c["valores"])):
                F.append(f"controles[{i}]: opciones con ≥2 valores str")
        else:
            F.append(f"controles[{i}].tipo: 'slider' u 'opciones'")
    if not (_es_int(j.get("hijos")) and 3 <= j["hijos"] <= 6):
        F.append("hijos: int 3–6")
    return F


def _v_aventura(j):
    F = []
    salas, ini = j.get("salas"), j.get("inicio")
    if not isinstance(salas, dict) or not salas:
        return ["salas: dict no vacío"]
    if ini not in salas:
        F.append(f"inicio {ini!r} no es una sala")
    for nom, sala in salas.items():
        if not (isinstance(nom, str) and nom.isidentifier()):
            F.append(f"sala {nom!r}: el nombre debe servir de nombre de función")
        if not (isinstance(sala, dict) and _texto(sala.get("texto")) and isinstance(sala.get("opciones"), list)):
            F.append(f"sala {nom!r}: {{texto: str, opciones: [[texto, destino], …]}}")
            continue
        for k, o in enumerate(sala["opciones"]):
            if not (isinstance(o, (list, tuple)) and len(o) == 2 and _texto(o[0])):
                F.append(f"sala {nom!r} opciones[{k}]: [texto, destino]")
            elif o[1] not in salas:
                F.append(f"sala {nom!r} opciones[{k}]: destino {o[1]!r} no existe")
    if F:
        return F
    pila, visto, final = [ini], {ini}, False
    while pila:
        s = pila.pop()
        if not salas[s]["opciones"]:
            final = True
        for _, d in salas[s]["opciones"]:
            if d not in visto:
                visto.add(d)
                pila.append(d)
    if not final:
        F.append("desde inicio no se llega a ningún final (sala sin opciones)")
    return F


def _v_carrera(j):
    F = []
    if not (_es_int(j.get("segundos")) and 30 <= j["segundos"] <= 90):
        F.append("segundos: int 30–90")
    pr = j.get("preguntas")
    if not (isinstance(pr, list) and len(pr) >= 8):
        return F + ["preguntas: al menos 8"]
    for i, q in enumerate(pr):
        if not isinstance(q, dict) or not _texto(q.get("pregunta"), 110):
            F.append(f"preguntas[{i}].pregunta: str ≤110")
            continue
        if _opciones(F, f"preguntas[{i}]", q.get("opciones"), 3, 4):
            if not (_es_int(q.get("correcta")) and 0 <= q["correcta"] < len(q["opciones"])):
                F.append(f"preguntas[{i}].correcta: índice dentro de opciones")
    return F


def _v_portada(j):
    F = []
    cartas, misiones = j.get("cartas"), j.get("misiones")
    if not isinstance(cartas, dict) or set(cartas) != {"html", "css", "py"}:
        return ["cartas: {html, css, py}"]
    ids = {}
    for capa, lista in cartas.items():
        if not (isinstance(lista, list) and 2 <= len(lista) <= 4):
            F.append(f"cartas.{capa}: 2–4 tarjetas")
            continue
        vistos = set()
        for i, x in enumerate(lista):
            etq = f"cartas.{capa}[{i}]"
            if not (isinstance(x, dict) and _texto(x.get("id")) and _texto(x.get("codigo")) and _texto(x.get("explica"))):
                F.append(f"{etq}: necesita id, codigo y explica")
                continue
            if _cols(x["codigo"]) > 52:
                F.append(f"{etq}.codigo: más de 52 columnas")
            if x["id"] in vistos:
                F.append(f"{etq}: id repetido {x['id']!r}")
            vistos.add(x["id"])
            if capa == "html" and not (_texto(x.get("titular")) and x.get("etiqueta") in ("h1", "p")):
                F.append(f"{etq}: titular str y etiqueta 'h1' o 'p'")
            if capa == "css" and not (x.get("fondo") or x.get("letra")):
                F.append(f"{etq}: fondo o letra")
            if capa == "py" and not (x.get("al_tocar") is None or _texto(x.get("al_tocar"))):
                F.append(f"{etq}.al_tocar: str o None")
        ids[capa] = vistos
    if not (isinstance(misiones, list) and 2 <= len(misiones) <= 4):
        return F + ["misiones: 2–4"]
    for i, m in enumerate(misiones):
        if not (isinstance(m, dict) and _texto(m.get("texto"), 110)):
            F.append(f"misiones[{i}].texto: str ≤110")
            continue
        for capa in ("html", "css", "py"):
            v = m.get(capa)
            if v is not None and v not in ids.get(capa, set()):
                F.append(f"misiones[{i}].{capa}: {v!r} no es una tarjeta de {capa}")
    ultima = misiones[-1]
    if isinstance(ultima, dict) and not all(ultima.get(c) for c in ("html", "css", "py")):
        F.append("la última misión tiene que pedir las tres capas")
    return F


def _v_torre(j):
    F = []
    lineas, meta = j.get("lineas"), j.get("meta", 5)
    if not (isinstance(lineas, list) and 6 <= len(lineas) <= 12):
        return ["lineas: 6–12"]
    if not (_es_int(meta) and 3 <= meta <= 8):
        F.append("meta: 3–8 bloques")
    buenas = malas = 0
    vistos = set()
    for i, x in enumerate(lineas):
        if not (isinstance(x, dict) and _texto(x.get("txt"), 40) and isinstance(x.get("ok"), bool)):
            F.append(f"lineas[{i}]: {{txt ≤40, ok}}")
            continue
        if x["txt"] in vistos:
            F.append(f"lineas[{i}]: línea repetida")
        vistos.add(x["txt"])
        if x["ok"]:
            buenas += 1
        else:
            malas += 1
            if not _texto(x.get("porque"), 90):
                F.append(f"lineas[{i}].porque: hace falta decir por qué se cae (≤90)")
    if buenas < meta:
        F.append(f"hacen falta al menos {meta} líneas bien escritas y hay {buenas}")
    if malas < 2:
        F.append("al menos 2 líneas mal escritas")
    return F


def _v_vueltas(j):
    """La fábrica de números: rondas con la secuencia que hay que clavar."""
    F = []
    ro = j.get("rondas")
    if not (isinstance(ro, list) and 3 <= len(ro) <= 6):
        return ["rondas: 3–6"]
    for i, x in enumerate(ro):
        obj = x.get("objetivo") if isinstance(x, dict) else None
        if not (isinstance(x, dict) and isinstance(obj, list) and 2 <= len(obj) <= 12
                and all(_es_int(v) for v in obj)):
            F.append(f"rondas[{i}].objetivo: 2–12 enteros")
            continue
        # Lo que se pide tiene que poder salir de un range: salto constante.
        paso = obj[1] - obj[0]
        if paso == 0 or any(b - a != paso for a, b in zip(obj, obj[1:])):
            F.append(f"rondas[{i}].objetivo: el salto tiene que ser constante y ≠ 0")
        if x.get("pista") is not None and not _texto(x["pista"], 90):
            F.append(f"rondas[{i}].pista: str ≤90")
    return F


VALIDA_MOTOR = {
    "torre": _v_torre, "vueltas": _v_vueltas,
    "portada": _v_portada,
    "robot": _v_robot, "clasifica": _v_clasifica, "marcador": _v_marcador, "ramas": _v_ramas,
    "bucle": _v_bucle, "lista": _v_lista, "caza": _v_caza, "css": _v_css, "aventura": _v_aventura,
    "carrera": _v_carrera,
}


# ── Teoría de cada semana ────────────────────────────────────────────────────

def validar_teoria(nivel, teoria):
    """TEORIA[nivel] = {1..12: {idea, partes, compruebo}}. Junta los fallos y sale con 1."""
    F = []
    if not isinstance(teoria, dict):
        print(f"✗ teoría {nivel}: debe ser un dict {{1..12: semana}}")
        raise SystemExit(1)
    for k in teoria:
        if not (_es_int(k) and 1 <= k <= 12):
            F.append(f"clave de semana inválida {k!r}")
    for n in range(1, 13):
        t = teoria.get(n)
        if not isinstance(t, dict):
            F.append(f"S{n}: falta la teoría")
            continue
        i, p, c = t.get("idea"), t.get("partes"), t.get("compruebo")
        if not (isinstance(i, dict) and _texto(i.get("titulo"), 60) and _texto(i.get("texto"), 160)
                and _texto(i.get("ejemplo"), 160)):
            F.append(f"S{n} · idea: {{titulo ≤60, texto ≤160, ejemplo ≤160}}")
        if not (isinstance(p, dict) and _texto(p.get("titulo"), 60)):
            F.append(f"S{n} · partes.titulo: str ≤60")
        else:
            pts = p.get("puntos")
            if not (isinstance(pts, (list, tuple)) and 3 <= len(pts) <= 4
                    and all(isinstance(x, (list, tuple)) and len(x) == 2 and _texto(x[0], 30) and _texto(x[1], 110)
                            for x in pts)):
                F.append(f"S{n} · partes.puntos: 3–4 pares (nombre ≤30, texto ≤110)")
            esc = p.get("escena")
            if esc is not None and esc not in IL.ESCENAS:
                F.append(f"S{n} · partes.escena {esc!r} no está en ilustra.ESCENAS")
            ej = p.get("ejemplos")
            if ej is not None:
                if not (isinstance(ej, list) and 3 <= len(ej) <= 6 and all(_texto(x) and _cols(x) <= 40 for x in ej)):
                    F.append(f"S{n} · partes.ejemplos: 3–6 líneas de código de ≤40 columnas")
                else:
                    err = compilar("\n".join(ej))[1] if callable(globals().get("compilar")) else None
                    if err:
                        F.append(f"S{n} · partes.ejemplos no compila: {err}")
        if not (isinstance(c, dict) and _texto(c.get("pregunta"), 110) and _texto(c.get("por_que"))):
            F.append(f"S{n} · compruebo: {{pregunta ≤110, opciones, correcta, por_que}}")
        else:
            ops = c.get("opciones")
            if not (isinstance(ops, list) and len(ops) == 3 and all(_texto(o, 60) for o in ops) and len(set(ops)) == 3):
                F.append(f"S{n} · compruebo.opciones: 3 str únicos ≤60")
            if not (_es_int(c.get("correcta")) and 0 <= c["correcta"] <= 2):
                F.append(f"S{n} · compruebo.correcta: 0–2")
    if F:
        print(f"✗ teoría {nivel}: {len(F)} fallo(s)")
        for f in F:
            print("   ✗", f)
        raise SystemExit(1)

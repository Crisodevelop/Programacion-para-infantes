# -*- coding: utf-8 -*-
"""
Parte las páginas generadas en tres trozos (marcado, estilos, comportamiento)
para que Next.js pueda servirlas como rutas.

`contenido.py` sigue siendo la única fuente: de ahí salen el .docx, la página
suelta y ahora también lo que consume la app. Duplicar el temario en un TSX
significaría que al corregir una semana habría que acordarse de dos sitios.
"""
import os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
DESTINO = os.path.join(AQUI, "..", "asistente-aula", "src", "contenido")


# ─────────────────────────────────────────────────────────────────────────
#  Reescritura para Next.js: que nada toque `body`
#
#  Las páginas se escriben como documentos sueltos, así que estilan `body`,
#  `html` y `:root` con toda naturalidad. Dentro de la app eso es hostil:
#  `body` no es suyo. Next.js le cuelga los datos serializados de React, una
#  decena de scripts y, en desarrollo, el panel de errores. Cuando la barra
#  lateral puso una rejilla sobre `body`, uno de esos elementos ocupó una
#  celda y el contenido acabó aplastado en la columna de 246px.
#
#  Aquí se reescriben esos selectores para que apunten al contenedor propio
#  de la página. Solo en la versión de la app: el archivo suelto y el artifact
#  se quedan como están, porque ahí `body` sí es de la página.
# ─────────────────────────────────────────────────────────────────────────

ENVOLTORIO = "pg"

REESCRITURAS = [
    # Los temas guardados dependen de un atributo en el elemento raíz, que
    # sigue estando en <html>: el contenedor cuelga de él, no lo sustituye.
    (r':root:not\(\[data-theme="light"\]\)\s*\{', f':root:not([data-theme="light"]) .{ENVOLTORIO}{{'),
    (r':root\[data-theme="dark"\]\s*\{',            f':root[data-theme="dark"] .{ENVOLTORIO}{{'),
    (r':root\[data-theme="light"\]\s*\{',           f':root[data-theme="light"] .{ENVOLTORIO}{{'),
    (r'(?<![\w.#\[-]):root\s*\{',                    f'.{ENVOLTORIO}{{'),
    (r'(?<![\w.#\[-])html\s*,\s*body\s*\{',        f'.{ENVOLTORIO}{{'),
    (r'(?<![\w.#\[-])body\s*,\s*html\s*\{',        f'.{ENVOLTORIO}{{'),
    (r'(?<![\w.#\[-])html\s*\{',                     f'.{ENVOLTORIO}{{'),
    (r'(?<![\w.#\[-])body\s*\{',                     f'.{ENVOLTORIO}{{'),
]


def reescribir_css(css: str) -> str:
    for patron, reemplazo in REESCRITURAS:
        css = re.sub(patron, reemplazo, css)
    # El contenedor tiene que cubrir la ventana: si no, el fondo oscuro de la
    # app asoma por debajo de una página corta.
    return f".{ENVOLTORIO}{{min-height:100dvh}}\n" + css


def comprobar_css(nombre: str, css: str) -> None:
    """Un selector suelto que se escape no rompe hoy: rompe el día que Next.js
    cuelgue un elemento más de body, y para entonces nadie recuerda por qué."""
    sueltos = re.findall(r'(?:^|[},])\s*(html\s*,\s*body|body|html|:root)\s*\{', css)
    if sueltos:
        raise SystemExit(
            f"\n  ABORTADO en {nombre}: quedaron selectores globales sin reescribir: "
            f"{sorted(set(s.strip() for s in sueltos))}\n"
            f"  Dentro de la app no pueden tocar body/html/:root.\n"
        )


def partir(html: str) -> dict[str, str]:
    titulo = re.search(r"<title>(.*?)</title>", html, re.S)
    fuentes = re.findall(r'<link rel="stylesheet" href="(https://fonts\.googleapis[^"]+)">', html)
    estilos = re.findall(r"<style>(.*?)</style>", html, re.S)
    guiones = re.findall(r"<script>(.*?)</script>", html, re.S)

    cuerpo = html
    for patron in (r"<title>.*?</title>", r"<link[^>]*>", r"<style>.*?</style>", r"<script>.*?</script>"):
        cuerpo = re.sub(patron, "", cuerpo, flags=re.S)

    return {
        "titulo": titulo.group(1).strip() if titulo else "",
        "fuente": fuentes[0] if fuentes else "",
        "css": "\n".join(e.strip() for e in estilos),
        "js": "\n".join(g.strip() for g in guiones),
        "html": cuerpo.strip(),
    }


def exportar(nombre: str, html: str) -> None:
    piezas = partir(html)
    piezas["css"] = reescribir_css(piezas["css"])
    comprobar_css(nombre, piezas["css"])
    os.makedirs(DESTINO, exist_ok=True)
    for extension, clave in (("html", "html"), ("css", "css"), ("js", "js")):
        ruta = os.path.join(DESTINO, f"{nombre}.{extension}")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(piezas[clave])
    meta = os.path.join(DESTINO, f"{nombre}.meta.json")
    with open(meta, "w", encoding="utf-8") as f:
        import json
        json.dump({"titulo": piezas["titulo"], "fuente": piezas["fuente"]}, f,
                  ensure_ascii=False, indent=2)
    tam = {k: len(piezas[k]) for k in ("html", "css", "js")}
    print(f"  {nombre}: {piezas['titulo']!r}  html={tam['html']} css={tam['css']} js={tam['js']}")


if __name__ == "__main__":
    import build_web, build_deck
    print("exportando a asistente-aula/src/contenido/")
    # Dentro de la app la presentación es una ruta, no un enlace externo.
    exportar("plan", build_web.build(enlace_presentacion="/presentacion"))
    exportar("presentacion", build_deck.build(enlace_indice="/presentaciones",
                                              url_muestra="/muestra/tienda.mp4"))

    # Y las páginas separadas, que es lo que la app sirve de verdad.
    import contenido as C
    exportar("inicio", build_web.pagina_inicio())
    exportar("horario", build_web.pagina_horario())
    for niv in C.NIVELES:
        exportar(f"nivel-{niv['id']}", build_web.pagina_nivel(niv))

    # El diagnóstico no es una página generada sino datos: lo pinta un
    # componente de React porque hay que escribir en él, y eso el HTML suelto
    # que produce el resto de este archivo no sabe hacerlo. Pero las preguntas
    # salen igual de contenido.py, que es la regla de la casa.
    import json
    destino = os.path.join(DESTINO, "diagnostico.json")
    os.makedirs(DESTINO, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        json.dump({
            "intro": C.DIAGNOSTICO_INTRO,
            "cierre": C.DIAGNOSTICO_CIERRE,
            "secciones": [s for s, _, _, _ in C.HORARIO_CLASES],
            "preguntas": [{"id": i, "texto": t, "tipo": tp, "opciones": o}
                          for i, t, tp, o in C.DIAGNOSTICO],
        }, f, ensure_ascii=False, indent=2)
    print(f"  diagnostico.json: {len(C.DIAGNOSTICO)} preguntas, "
          f"{len(C.HORARIO_CLASES)} secciones")

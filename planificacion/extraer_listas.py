"""Saca las listas de clase de los .docx que manda la escuela.

    python3 extraer_listas.py ~/Downloads/Listas            # ver el resumen
    python3 extraer_listas.py ~/Downloads/Listas --json out.json

No escribe nada dentro del repositorio a propósito. Son 256 nombres de menores
y este proyecto publica lo que hay en `src/contenido/`; un CSV olvidado ahí
acabaría en internet. Quien los sube a la base es
`asistente-aula/scripts/cargar-listas.ts`, y de ahí solo salen con sesión de
docente.

─── Cómo vienen los documentos ───
Una tabla de cuatro columnas: número (vacío), nombre, Femenino, Masculino, y una
fila final «TOTAL» con las dos sumas. El nombre viene «Apellidos, Nombres», que
es como se archiva y no como se llama a nadie: se guardan las dos formas.

La fila TOTAL no es decorativa: es la única forma de comprobar que este archivo
leyó a todo el mundo. Si no cuadra, aborta.
"""
import json
import os
import re
import sys
import unicodedata
import zipfile

# «1ero. A Secundaria», «2do B de Secundaria», «3ro C» → «1ro A»
NIVELES = {"1": "1ro", "2": "2do", "3": "3ro"}


def celdas(fila: str) -> list[str]:
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", " ", tc))).strip()
            for tc in re.findall(r"<w:tc[ >].*?</w:tc>", fila, re.S)]


def seccion_de(grado: str) -> str | None:
    """«1ero A de Secundaria» → «1ro A». None si no se reconoce."""
    m = re.search(r"([123])\s*(?:ro|do|ero|er|º|°)?\.?\s*([ABC])\b", grado, re.I)
    return f"{NIVELES[m.group(1)]} {m.group(2).upper()}" if m else None


def partir_nombre(bruto: str) -> tuple[str, str, bool, bool]:
    """(apellidos, nombres, nuevo, dudoso).

    `dudoso` marca los que no traen coma: ahí no se sabe dónde acaba el
    apellido, y adivinarlo en silencio es peor que avisar."""
    nuevo = bool(re.search(r"\(?\s*nuevo(\s+ingreso)?\s*\)?\s*$", bruto, re.I))
    limpio = re.sub(r"\(?\s*nuevo(\s+ingreso)?\s*\)?\s*$", "", bruto, flags=re.I).strip(" ,")
    if "," in limpio:
        ape, nom = limpio.split(",", 1)
        return titular(ape), titular(nom), nuevo, False
    # Sin coma: se parte por la mitad. Y un apellido no termina en «de» ni en
    # «del», así que si el corte cae ahí se mueve una palabra más allá.
    partes = limpio.split()
    corte = max(1, len(partes) // 2)
    while corte < len(partes) - 1 and partes[corte - 1].lower() in MINUS:
        corte += 1
    return titular(" ".join(partes[:corte])), titular(" ".join(partes[corte:])), nuevo, True


MINUS = {"de", "del", "la", "las", "los", "y", "san", "santa"}


def titular(s: str) -> str:
    """«severino juan» → «Severino Juan», dejando en minúscula las partículas.

    Los documentos mezclan mayúsculas («Elizabeth maria»), y esto se proyecta."""
    out = []
    for i, p in enumerate(s.split()):
        b = p.lower()
        out.append(b if (i and b in MINUS) else (b[:1].upper() + b[1:]))
    return " ".join(out)


def sin_tildes(s: str) -> str:
    n = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"\s+", " ", "".join(c for c in n if unicodedata.category(c) != "Mn")).strip()


def leer(ruta: str) -> dict:
    xml = zipfile.ZipFile(ruta).read("word/document.xml").decode("utf8")
    filas = [celdas(t) for t in re.findall(r"<w:tr[ >].*?</w:tr>", xml, re.S)]
    grado = titular_doc = ""
    alumnos, total = [], None
    for c in filas:
        if len(c) == 2 and c[0].startswith("Grado"):
            grado = c[1].lstrip(": ").strip()
        elif len(c) == 2 and c[0].startswith("Docente Titular"):
            titular_doc = c[1].lstrip(": ").strip()
        elif len(c) >= 4 and c[1]:
            if c[1].strip().upper() == "TOTAL":
                try:
                    total = int(c[2] or 0) + int(c[3] or 0)
                except ValueError:
                    pass
            elif c[2] == "F" or c[3] == "M":
                ape, nom, nuevo, dudoso = partir_nombre(c[1])
                alumnos.append({"apellidos": ape, "nombres": nom,
                                "nombre": f"{nom} {ape}".strip(),
                                "sexo": "F" if c[2] == "F" else "M",
                                "nuevo": nuevo, "dudoso": dudoso, "bruto": c[1]})
    return {"archivo": os.path.basename(ruta), "grado": grado, "titular": titular_doc,
            "seccion": seccion_de(grado), "alumnos": alumnos, "total": total}


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("uso: extraer_listas.py <carpeta> [--json salida.json]")
    carpeta = os.path.expanduser(sys.argv[1])
    archivos = sorted(f for f in os.listdir(carpeta) if f.endswith(".docx")
                      and not f.startswith("~$"))
    if not archivos:
        raise SystemExit(f"No hay .docx en {carpeta}")

    secciones, problemas, dudosos = {}, [], []
    print(f"{'sección':<9} {'titular de aula':<24} {'alumnos':>7}  {'TOTAL':>6}  archivo")
    for a in archivos:
        d = leer(os.path.join(carpeta, a))
        n = len(d["alumnos"])
        if not d["seccion"]:
            problemas.append(f"{a}: no se reconoce la sección en «{d['grado']}»")
            continue
        if d["seccion"] in secciones:
            problemas.append(f"{a}: la sección {d['seccion']} ya venía de otro archivo")
            continue
        # La comprobación que vale: contra lo que dice el propio documento.
        if d["total"] is None:
            problemas.append(f"{a}: no trae fila TOTAL, no se puede comprobar")
        elif d["total"] != n:
            problemas.append(f"{a}: leí {n} y el documento dice {d['total']}")
        secciones[d["seccion"]] = d
        dudosos += [(d["seccion"], x["bruto"]) for x in d["alumnos"] if x["dudoso"]]
        print(f"{d['seccion']:<9} {d['titular'][:23]:<24} {n:>7}  "
              f"{(d['total'] if d['total'] is not None else '—'):>6}  {a[:38]}")

    # Nadie repetido, ni dentro de su sección ni entre dos.
    visto = {}
    for sec, d in secciones.items():
        for x in d["alumnos"]:
            visto.setdefault(sin_tildes(x["nombre"]), []).append(sec)
    repes = {k: v for k, v in visto.items() if len(v) > 1}

    total = sum(len(d["alumnos"]) for d in secciones.values())
    print(f"\n{len(secciones)} secciones · {total} estudiantes")
    if dudosos:
        print(f"\n⚠ {len(dudosos)} sin coma: hay que confirmar dónde acaba el apellido")
        for sec, b in dudosos:
            print(f"    {sec}: «{b}»")
    if repes:
        print(f"\n⚠ repetidos: {len(repes)}")
        for k, v in list(repes.items())[:10]:
            print(f"    {k} → {', '.join(v)}")
    if problemas:
        print("\n✖ " + "\n✖ ".join(problemas))
        raise SystemExit(1)

    if "--json" in sys.argv:
        destino = os.path.expanduser(sys.argv[sys.argv.index("--json") + 1])
        with open(destino, "w", encoding="utf-8") as f:
            json.dump([{"seccion": s, "titular": d["titular"], "alumnos": d["alumnos"]}
                       for s, d in sorted(secciones.items())], f, ensure_ascii=False, indent=2)
        print(f"\nescrito: {destino}")


if __name__ == "__main__":
    main()

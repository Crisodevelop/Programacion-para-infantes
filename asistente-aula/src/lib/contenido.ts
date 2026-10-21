import "server-only";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

/**
 * Las páginas de clase (el plan y la presentación) se generan desde
 * `contenido.py`, en la carpeta de arriba: es la misma fuente de la que sale
 * el .docx que va a coordinación. Aquí solo se leen los trozos ya generados.
 *
 * No se convirtieron a componentes de React a propósito. Habría que mantener
 * el temario en dos sitios, y la primera vez que se corrigiera una semana en
 * uno solo, el proyector y el documento de coordinación dirían cosas distintas.
 */

export type Generada = {
  titulo: string;
  fuente: string;
  html: string;
  css: string;
  js: string;
};

const CARPETA = join(process.cwd(), "src", "contenido");

export type Pagina =
  | "plan" | "presentacion" | "inicio" | "horario"
  | "nivel-1ro" | "nivel-2do" | "nivel-3ro";

export async function leerGenerada(nombre: Pagina): Promise<Generada> {
  const [html, css, js, meta] = await Promise.all([
    readFile(join(CARPETA, `${nombre}.html`), "utf8"),
    readFile(join(CARPETA, `${nombre}.css`), "utf8"),
    readFile(join(CARPETA, `${nombre}.js`), "utf8"),
    readFile(join(CARPETA, `${nombre}.meta.json`), "utf8"),
  ]);
  const { titulo, fuente } = JSON.parse(meta) as { titulo: string; fuente: string };
  return { titulo, fuente, html, css, js };
}


export type Pregunta = {
  id: string;
  texto: string;
  tipo: "una" | "varias" | "texto";
  opciones: string[];
};

export type Diagnostico = {
  intro: string;
  cierre: string;
  secciones: string[];
  preguntas: Pregunta[];
};

/**
 * Las preguntas del diagnóstico de entrada.
 *
 * Salen de `contenido.py` como el resto del temario y llegan aquí en JSON. No
 * están escritas en el componente a propósito: corregir una pregunta tiene que
 * ser editar la fuente y regenerar, no tocar React.
 */
export async function leerDiagnostico(): Promise<Diagnostico> {
  const crudo = await readFile(join(CARPETA, "diagnostico.json"), "utf8");
  return JSON.parse(crudo) as Diagnostico;
}

export type ClaseCurso = {
  nivel: string;
  nivelNombre: string;
  n: number;
  tema: string;
  objetivo: string;
};

export const NIVELES = ["1ro", "2do", "3ro"] as const;
export type Nivel = (typeof NIVELES)[number];

export function esNivel(v: string): v is Nivel {
  return (NIVELES as readonly string[]).includes(v);
}

/** Las 36 clases curriculares, con su nivel y su semana. */
export async function indiceCurso(): Promise<ClaseCurso[]> {
  const crudo = await readFile(join(CARPETA, "curso", "indice.json"), "utf8");
  return JSON.parse(crudo) as ClaseCurso[];
}

/** La presentación de una clase. `null` si esa semana no existe. */
export async function leerClase(nivel: string, n: number): Promise<Generada | null> {
  if (!esNivel(nivel) || !Number.isInteger(n) || n < 1 || n > 12) return null;
  const carpeta = join(CARPETA, "curso", nivel);
  try {
    const [html, css, js, meta] = await Promise.all([
      readFile(join(carpeta, `${n}.html`), "utf8"),
      readFile(join(carpeta, `${n}.css`), "utf8"),
      readFile(join(carpeta, `${n}.js`), "utf8"),
      readFile(join(carpeta, `${n}.meta.json`), "utf8"),
    ]);
    const { titulo, fuente } = JSON.parse(meta) as { titulo: string; fuente: string };
    return { titulo, fuente, html, css, js };
  } catch {
    return null;
  }
}

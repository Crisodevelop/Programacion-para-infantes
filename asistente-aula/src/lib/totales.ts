/*
 * La nota acumulada de cada estudiante, a partir de las notas por clase.
 *
 * No hay una tabla de «nota final» ni una columna de «semana en curso»: la
 * semana sale de la URL cuando abres la clase y se guarda en cada nota. Así
 * que lo que se ha dado se deduce de los datos — las semanas que esa sección
 * tiene registradas — y no de un calendario que habría que mantener a mano y
 * que se desincronizaría el primer día que se cae una clase.
 */

export type NotaBase = {
  nombre: string;
  seccion: string;
  semana: number;
  puntos: number;
  /** Quién es, de verdad. El nombre agrupa; esto cruza con la disciplina. */
  estudiante_id?: string | null;
};

/**
 * Cuánto pesa la conducta en la nota final.
 *
 * 15 %: mueve a quien está en el borde sin decidir por él. Un 78 académico con
 * la conducta intacta llega a 81; un 60 se queda en 66, que sigue siendo 60.
 * No rescata ni hunde a nadie — la nota la sigue poniendo el trabajo.
 */
export const PESO_DISCIPLINA = 0.15;

/** Sin fila en `disciplina` se entiende que no hubo nada que anotar. */
export const DISCIPLINA_POR_DEFECTO = 100;

/** Faltar vale 0, o la nota es solo de lo que entregó. */
export type Criterio = "falta-cero" | "solo-entregado";

export type Total = {
  clave: string;
  nombre: string;
  seccion: string;
  /** La mejor nota de cada semana: quien repitió la clase no se castiga. */
  porSemana: Map<number, number>;
  /** Semanas que esa sección tiene registradas, hasta el tope. */
  dadas: number[];
  entregadas: number;
  puntos: number;
  /** El máximo al que podía aspirar con el criterio elegido. */
  sobre: number;
  /** Sobre 100. `null` si no hay nada que promediar. */
  nota: number | null;
  /** Los uuid de `lista` con los que aparece: casi siempre uno. */
  ids: string[];
  /** Conducta, sobre 100. 100 mientras no se le haya anotado nada. */
  disciplina: number;
  /** La académica y la conducta, con su peso. `null` si no hay académica. */
  final: number | null;
};

/** El mismo nombre escrito con otro espaciado o en mayúsculas es la misma persona. */
export function normaliza(nombre: string) {
  return nombre.trim().toLowerCase().replace(/\s+/g, " ");
}

/**
 * Las semanas que cada sección ha dado, hasta `tope` inclusive.
 *
 * Se usan las semanas que REALMENTE tienen nota en esa sección, no el rango
 * 1..tope: si una semana se cayó por un feriado y nadie la guardó, no puede
 * contar como cero para toda la clase.
 */
export function semanasDadas(filas: NotaBase[], tope: number): Map<string, number[]> {
  const porSeccion = new Map<string, Set<number>>();
  for (const f of filas) {
    if (f.semana > tope) continue;
    if (!porSeccion.has(f.seccion)) porSeccion.set(f.seccion, new Set());
    porSeccion.get(f.seccion)!.add(f.semana);
  }
  return new Map([...porSeccion].map(([s, w]) => [s, [...w].sort((a, b) => a - b)]));
}

export function totales(
  filas: NotaBase[], tope: number, criterio: Criterio,
  /** estudiante_id → puntos. Quien no esté, va con 100. */
  disciplina: Map<string, number> = new Map(),
): Total[] {
  const dadas = semanasDadas(filas, tope);
  const por = new Map<string, Total>();

  for (const f of filas) {
    if (f.semana > tope) continue;
    const clave = `${f.seccion}|${normaliza(f.nombre)}`;
    let t = por.get(clave);
    if (!t) {
      t = {
        clave, nombre: f.nombre.trim(), seccion: f.seccion,
        porSemana: new Map(), dadas: dadas.get(f.seccion) ?? [],
        entregadas: 0, puntos: 0, sobre: 0, nota: null,
        ids: [], disciplina: DISCIPLINA_POR_DEFECTO, final: null,
      };
      por.set(clave, t);
    }
    if (f.estudiante_id && !t.ids.includes(f.estudiante_id)) t.ids.push(f.estudiante_id);
    const antes = t.porSemana.get(f.semana);
    if (antes === undefined || f.puntos > antes) t.porSemana.set(f.semana, f.puntos);
  }

  for (const t of por.values()) {
    const entregado = t.dadas.map((w) => t.porSemana.get(w)).filter((p): p is number => p !== undefined);
    t.entregadas = entregado.length;
    t.puntos = entregado.reduce((s, p) => s + p, 0);
    const divisor = criterio === "falta-cero" ? t.dadas.length : t.entregadas;
    t.sobre = divisor * 100;
    t.nota = divisor ? Math.round(t.puntos / divisor) : null;

    // Si el mismo nombre llegó con dos uuid —pasa cuando una nota vieja no
    // trae estudiante_id— vale la conducta más baja: la anotación existe y no
    // se puede borrar por accidente de agrupación.
    const suyas = t.ids.map((id) => disciplina.get(id)).filter((p): p is number => p !== undefined);
    t.disciplina = suyas.length ? Math.min(...suyas) : DISCIPLINA_POR_DEFECTO;
    t.final = t.nota === null ? null
      : Math.round(t.nota * (1 - PESO_DISCIPLINA) + t.disciplina * PESO_DISCIPLINA);
  }

  return [...por.values()].sort((a, b) =>
    a.seccion.localeCompare(b.seccion, "es") || (b.nota ?? -1) - (a.nota ?? -1) ||
    a.nombre.localeCompare(b.nombre, "es"));
}

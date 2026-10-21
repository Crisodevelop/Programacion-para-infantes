/*
 * Sin `import "server-only"`, a propósito. Esto es el horario de clases: qué
 * sección toca a qué hora, lo mismo que está colgado en la puerta del aula. No
 * hay nada secreto, y la presentación —que es estática y se sirve igual a
 * todo el mundo— lo necesita en el navegador para saber qué sección enseñar
 * al cambiar de nivel.
 */

/**
 * El horario real, para que el panel sepa qué toca hoy.
 *
 * Duplica lo que ya está en la planificación, pero en un formato que el código
 * puede consultar. La alternativa —leer el HTML generado— sería frágil y lento
 * para responder a «¿qué clase tengo ahora?».
 */
export type Bloque = { seccion: string; desde: string; hasta: string };

/** Las nueve secciones, en el orden en que se enseñan en las pestañas. */
export const SECCIONES = ["1ro A", "1ro B", "1ro C", "2do A", "2do B", "2do C", "3ro A", "3ro B", "3ro C"];

export const HORARIO: Record<number, Bloque[]> = {
  // getDay(): 0 domingo … 6 sábado
  3: [{ seccion: "1ro A", desde: "08:00", hasta: "08:50" }],
  4: [
    { seccion: "2do A", desde: "08:00", hasta: "08:50" },
    { seccion: "2do C", desde: "08:50", hasta: "09:40" },
    { seccion: "3ro B", desde: "10:55", hasta: "11:45" },
    { seccion: "1ro B", desde: "11:45", hasta: "12:30" },
    { seccion: "3ro C", desde: "12:30", hasta: "13:15" },
  ],
  5: [
    { seccion: "2do B", desde: "08:00", hasta: "08:50" },
    { seccion: "3ro A", desde: "08:50", hasta: "09:40" },
    { seccion: "1ro C", desde: "09:40", hasta: "10:25" },
  ],
};

export const DIAS = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];

export function bloquesDeHoy(ahora = new Date()): Bloque[] {
  return HORARIO[ahora.getDay()] ?? [];
}

/** El bloque en curso, si estamos dentro de uno. */
export function bloqueActual(ahora = new Date()): Bloque | null {
  const hhmm = horaMinuto(ahora);
  return bloquesDeHoy(ahora).find((b) => hhmm >= b.desde && hhmm < b.hasta) ?? null;
}

/**
 * La sección de un nivel que toca hoy.
 *
 * Al pulsar «2do» en la presentación lo normal es querer la de 2do que está
 * en clase ahora; si no hay ninguna en curso, la siguiente que va a entrar; y
 * si ya pasaron todas, la primera del día, que es la que más probablemente se
 * quiera repasar. `null` si ese nivel no tiene clase hoy.
 *
 * Hora local, igual que `bloqueActual`: es la hora del reloj del aula.
 */
export function seccionDeHoy(nivel: string, ahora = new Date()): Bloque | null {
  const hhmm = horaMinuto(ahora);
  const delNivel = bloquesDeHoy(ahora).filter((b) => b.seccion.startsWith(nivel + " "));
  return delNivel.find((b) => hhmm >= b.desde && hhmm < b.hasta)
    ?? delNivel.find((b) => b.desde > hhmm)
    ?? delNivel[0]
    ?? null;
}

function horaMinuto(d: Date): string {
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

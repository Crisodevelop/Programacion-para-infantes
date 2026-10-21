"use client";
import { useEffect, useState } from "react";
import type { Bloque } from "@/lib/horario";
import { PasarLista } from "@/components/PasarLista";

/**
 * Las clases de hoy, y pasar lista desde la misma fila.
 *
 * Antes el panel decía «2do C · pendiente» y había que ir a Asistencia y
 * volver a elegir 2do C entre nueve pestañas. Ahora cada fila tiene su botón,
 * que deja la sección elegida abajo y baja hasta ella: en el celular la lista
 * queda fuera de la pantalla y sin el desplazamiento parecería que no pasó
 * nada.
 *
 * ─── Por qué la clase pendiente se calcula aquí ───
 * El servidor puede ir en UTC y el aula no. La que está en curso llega ya
 * calculada; la siguiente se decide en el navegador, con su reloj, y después
 * de montar: calcularla durante el primer render daría una fila marcada
 * distinta en el servidor y en el navegador.
 */
type Props = { bloques: Bloque[]; pasadas: string[]; enCurso: string | null };

export function ClasesDeHoy({ bloques, pasadas, enCurso }: Props) {
  const [sel, setSel] = useState<string | undefined>(enCurso ?? undefined);
  const [hechas, setHechas] = useState(() => new Set(pasadas));

  // Solo al montar: después manda lo que toque el docente.
  useEffect(() => {
    if (enCurso || bloques.length === 0) return;
    const ahora = new Date();
    const hhmm = `${String(ahora.getHours()).padStart(2, "0")}:${String(ahora.getMinutes()).padStart(2, "0")}`;
    setSel((bloques.find((b) => b.desde > hhmm) ?? bloques[0]).seccion);
  }, []);

  function irA(s: string) {
    setSel(s);
    document.getElementById("pasar-lista")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return (
    <>
      {bloques.length > 0 && (
        <section style={S.seccion}>
          <ul style={S.lista}>
            {bloques.map((b) => {
              const pasada = hechas.has(b.seccion);
              const activa = enCurso === b.seccion;
              const elegida = sel === b.seccion;
              return (
                <li key={b.seccion} style={{ ...S.fila, borderColor: elegida ? "var(--aqua)" : "var(--linea)" }}>
                  <span style={S.hora}>{b.desde} – {b.hasta}</span>
                  <span style={S.seccionNombre}>{b.seccion}</span>
                  <span style={{ ...S.marca, color: pasada ? "var(--verde)" : "var(--mut)" }}>
                    {pasada ? "lista pasada" : activa ? "en curso" : "pendiente"}
                  </span>
                  <button type="button" style={S.boton(elegida)} aria-pressed={elegida}
                          onClick={() => irA(b.seccion)}>
                    Pasar lista
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      <section id="pasar-lista" style={S.seccion}>
        <h2 style={S.h2}>Pasar lista</h2>
        <PasarLista seccion={sel} onSeccion={setSel}
                    onGuardada={(s) => setHechas((h) => new Set(h).add(s))} />
      </section>
    </>
  );
}

const S = {
  seccion: { marginBottom: 34, scrollMarginTop: 16 } as React.CSSProperties,
  h2: { fontSize: 14, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--mut)",
        margin: "0 0 12px", fontWeight: 600 } as React.CSSProperties,
  lista: { listStyle: "none", margin: 0, padding: 0, display: "grid", gap: 8 } as React.CSSProperties,
  // La hora cede algo de ancho en un teléfono; con 132px fijos y el botón
  // nuevo, el nombre de la sección se quedaba sin sitio.
  fila: {
    display: "grid", gridTemplateColumns: "minmax(96px,132px) 1fr auto auto", gap: 14, alignItems: "center",
    padding: "13px 16px", background: "var(--panel)", border: "1px solid var(--linea)", borderRadius: 9,
  } as React.CSSProperties,
  hora: { fontSize: 13.5, color: "var(--mut)", fontVariantNumeric: "tabular-nums" } as React.CSSProperties,
  seccionNombre: { fontSize: 17, fontWeight: 600 } as React.CSSProperties,
  marca: { fontSize: 12.5, letterSpacing: ".04em" } as React.CSSProperties,
  boton: (act: boolean): React.CSSProperties => ({
    padding: "6px 11px", borderRadius: 8, cursor: "pointer", whiteSpace: "nowrap",
    fontFamily: "inherit", fontSize: 12.5, fontWeight: act ? 600 : 400,
    border: "1px solid var(--aqua)",
    background: act ? "var(--aqua)" : "transparent",
    color: act ? "var(--fondo)" : "var(--aqua)",
  }),
};

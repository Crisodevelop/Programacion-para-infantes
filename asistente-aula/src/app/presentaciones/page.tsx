import Link from "next/link";
import { indiceCurso, type ClaseCurso } from "@/lib/contenido";

export const dynamic = "force-static";
export const metadata = {
  title: "Presentaciones",
  description: "Las presentaciones del curso, listas para proyectar.",
};

/**
 * Todas las presentaciones en un sitio.
 *
 * Cada semana ya tiene su botón de proyectar dentro de su curso, pero para
 * encontrar una hay que recordar en qué semana estaba. Aquí están todas
 * juntas, agrupadas por nivel.
 */
export default async function Pagina() {
  const clases = await indiceCurso();

  const porNivel = new Map<string, ClaseCurso[]>();
  for (const c of clases) {
    if (!porNivel.has(c.nivel)) porNivel.set(c.nivel, []);
    porNivel.get(c.nivel)!.push(c);
  }

  const total = clases.length + 1;

  return (
    <main style={S.pantalla}>
      <header style={S.cabecera}>
        <Link href="/" style={S.volverArriba}>&#8592; La planificaci&#243;n</Link>
        <p style={S.eyebrow}>Para proyectar</p>
        <h1 style={S.titulo}>Presentaciones</h1>
        <p style={S.lead}>
          {total} en total. Se abren a pantalla completa y se avanza con las flechas.
        </p>
      </header>

      <section style={S.grupo}>
        <h2 style={S.h2}>Primera clase</h2>
        <ul style={S.rejilla}>
          <li>
            <Link href="/presentacion" style={S.tarjeta}>
              <span style={S.num}>—</span>
              <span style={S.tTitulo}>Hola, soy Criso</span>
              <span style={S.tSub}>Cómo arranca el curso. Cambia según el nivel.</span>
            </Link>
          </li>
        </ul>
      </section>

      {[...porNivel.entries()].map(([nivel, lista]) => (
        <section key={nivel} style={S.grupo}>
          <div style={S.grupoCabecera}>
            <h2 style={S.h2}>{nivel.toUpperCase()} · {lista[0].nivelNombre}</h2>
            <Link href={`/curso/${nivel}`} style={S.verCurso}>Ver el curso →</Link>
          </div>
          <ul style={S.rejilla}>
            {lista.sort((a, b) => a.n - b.n).map((c) => (
              <li key={c.n}>
                <Link href={`/curso/${nivel}/semana/${c.n}`} style={S.tarjeta}>
                  <span style={{ ...S.num, color: COLOR[nivel] }}>
                    Semana {String(c.n).padStart(2, "0")}
                  </span>
                  <span style={S.tTitulo}>{c.tema}</span>
                  <span style={S.tSub}>{c.objetivo}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}

      <footer style={S.pie}>
        <Link href="/" style={S.volver}>← La planificación</Link>
      </footer>
    </main>
  );
}

const COLOR: Record<string, string> = {
  "1ro": "var(--aqua)",
  "2do": "var(--verde)",
  "3ro": "var(--lila)",
};

const S: Record<string, React.CSSProperties> = {
  volverArriba: { display: "inline-block", marginBottom: 18, fontSize: 13,
                  color: "var(--mut)", textDecoration: "none" },
  pantalla: {
    minHeight: "100dvh", maxWidth: 1080, margin: "0 auto",
    padding: "52px 24px 72px", display: "flex", flexDirection: "column", gap: 36,
  },
  cabecera: { display: "grid", gap: 11, maxWidth: "58ch" },
  eyebrow: { margin: 0, fontSize: 12, letterSpacing: ".16em", textTransform: "uppercase", color: "var(--aqua)" },
  titulo: { margin: 0, fontSize: "clamp(28px,4.4vw,42px)", letterSpacing: "-.025em" },
  lead: { margin: 0, fontSize: 16.5, color: "var(--tx-2)", lineHeight: 1.6 },
  grupo: { display: "grid", gap: 13 },
  grupoCabecera: {
    display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 14,
    flexWrap: "wrap", paddingBottom: 9, borderBottom: "1px solid var(--linea)",
  },
  h2: { margin: 0, fontSize: 17, fontWeight: 600 },
  verCurso: { fontSize: 13.5, color: "var(--mut)", textDecoration: "none" },
  rejilla: {
    listStyle: "none", margin: 0, padding: 0, display: "grid", gap: 11,
    gridTemplateColumns: "repeat(auto-fill, minmax(258px, 1fr))",
  },
  tarjeta: {
    display: "grid", gap: 6, alignContent: "start", height: "100%", padding: "16px 17px",
    background: "var(--panel)", border: "1px solid var(--linea)", borderRadius: 10,
    textDecoration: "none", color: "inherit",
  },
  num: { fontSize: 11.5, fontWeight: 700, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--mut)" },
  tTitulo: { fontSize: 15.5, fontWeight: 600, lineHeight: 1.32 },
  tSub: { fontSize: 13, color: "var(--mut)", lineHeight: 1.5 },
  pie: { paddingTop: 14, borderTop: "1px solid var(--linea)" },
  volver: { fontSize: 14, color: "var(--tx-2)", textDecoration: "none" },
};

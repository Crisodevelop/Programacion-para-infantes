import Link from "next/link";
import { supabaseServidor } from "@/lib/supabase/sesion";
import { bloquesDeHoy, bloqueActual, DIAS } from "@/lib/horario";
import { ClasesDeHoy } from "@/components/ClasesDeHoy";

export const dynamic = "force-dynamic";
export const metadata = { title: "Panel" };

export default async function Panel() {
  const ahora = new Date();
  const hoy = bloquesDeHoy(ahora);
  const enCurso = bloqueActual(ahora);
  const sb = await supabaseServidor();

  // Se lee con la sesión del docente, no con la clave de servicio: si la RLS
  // estuviera mal, esto devolvería vacío y se notaría aquí.
  const { data: listas } = await sb
    .from("asistencia")
    .select("id, grupo, fecha, cerrada_en")
    .order("fecha", { ascending: false })
    .limit(8);

  // En hora local, como la guarda `PasarLista`. Con `toISOString` a secas, a
  // partir de las ocho de la tarde el servidor en UTC ya estaba en mañana y
  // ninguna lista de hoy salía como pasada.
  const fechaHoy = new Date(ahora.getTime() - ahora.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  const yaPasadas = new Set((listas ?? []).filter((l) => l.fecha === fechaHoy).map((l) => l.grupo));

  return (
    <>
      <header style={S.cabecera}>
        <p style={S.eyebrow}>{DIAS[ahora.getDay()]} {ahora.getDate()}</p>
        <h1 style={S.titulo}>{hoy.length ? `${hoy.length} ${hoy.length === 1 ? "clase" : "clases"} hoy` : "Hoy no hay clases"}</h1>
      </header>

      <ClasesDeHoy bloques={hoy} pasadas={[...yaPasadas]} enCurso={enCurso?.seccion ?? null} />

      <section style={S.seccion}>
        <h2 style={S.h2}>Últimas listas</h2>
        {listas?.length ? (
          <ul style={S.lista}>
            {listas.map((l) => (
              <li key={l.id} style={S.fila}>
                <span style={S.hora}>{l.fecha}</span>
                <span style={S.seccionNombre}>{l.grupo}</span>
                <span style={{ ...S.marca, color: l.cerrada_en ? "var(--verde)" : "var(--ambar)" }}>
                  {l.cerrada_en ? "cerrada" : "abierta"}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p style={S.vacio}>Todavía no has pasado ninguna lista.</p>
        )}
        <Link href="/admin/asistencia" style={S.masEnlace}>Ver todas →</Link>
      </section>

      <section style={S.seccion}>
        <h2 style={S.h2}>Antes de clase</h2>
        <ol style={S.pasos}>
          <li>Cuando empiece la hora, abre la <Link href="/admin/clase" style={S.enlaceTx}>clase en vivo</Link> de la sección que toca.</li>
          <li>Repasa <Link href="/admin/horario" style={S.enlaceTx}>tu horario</Link> si no recuerdas qué sección toca.</li>
          <li>La primera semana, mira <Link href="/admin/diagnostico" style={S.enlaceTx}>el diagnóstico</Link> antes de preparar la clase.</li>
        </ol>
      </section>
    </>
  );
}

const S: Record<string, React.CSSProperties> = {
  cabecera: { marginBottom: 28 },
  eyebrow: { margin: 0, fontSize: 12, letterSpacing: ".16em", textTransform: "uppercase", color: "var(--aqua)" },
  titulo: { margin: "8px 0 0", fontSize: 32, letterSpacing: "-.025em" },
  seccion: { marginBottom: 34 },
  h2: { fontSize: 14, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--mut)", margin: "0 0 12px", fontWeight: 600 },
  lista: { listStyle: "none", margin: 0, padding: 0, display: "grid", gap: 8 },
  fila: {
    display: "grid", gridTemplateColumns: "132px 1fr auto", gap: 14, alignItems: "center",
    padding: "13px 16px", background: "var(--panel)", border: "1px solid var(--linea)", borderRadius: 9,
  },
  hora: { fontSize: 13.5, color: "var(--mut)", fontVariantNumeric: "tabular-nums" },
  seccionNombre: { fontSize: 17, fontWeight: 600 },
  marca: { fontSize: 12.5, letterSpacing: ".04em" },
  vacio: { margin: 0, fontSize: 14.5, color: "var(--mut)" },
  masEnlace: { display: "inline-block", marginTop: 12, fontSize: 14, color: "var(--aqua)", textDecoration: "none" },
  pasos: { margin: 0, paddingLeft: 22, fontSize: 15, color: "var(--tx-2)", lineHeight: 2 },
  enlaceTx: { color: "var(--aqua)", textDecoration: "none" },
};

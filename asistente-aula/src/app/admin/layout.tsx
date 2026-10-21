import Link from "next/link";
import { redirect } from "next/navigation";
import { docenteActual } from "@/lib/supabase/sesion";
import { SalirBoton } from "@/components/SalirBoton";

export const dynamic = "force-dynamic";

/**
 * Marco del área de administración.
 *
 * El middleware ya rebotó a quien no tiene sesión. Aquí se comprueba el ROL,
 * que es lo que el middleware no puede saber sin consultar la base. Un
 * estudiante con sesión anónima —hay seis en el sistema— llega hasta aquí y
 * sale de vuelta a la portada.
 */
export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const docente = await docenteActual();
  if (!docente) redirect("/");

  return (
    <div style={S.marco}>
      <nav style={S.barra}>
        <div style={S.marca}>
          <Link href="/admin" style={S.logo}>Asistente de aula</Link>
          <span style={S.quien}>{docente.nombre}</span>
        </div>
        <div style={S.enlaces}>
          <Link href="/admin" style={S.enlace}>Panel</Link>
          <Link href="/admin/horario" style={S.enlace}>Horario</Link>
          <Link href="/admin/asistencia" style={S.enlace}>Asistencia</Link>
          <Link href="/admin/clase" style={S.enlace}>Clase en vivo</Link>
          <Link href="/admin/diagnostico" style={S.enlace}>Diagnóstico</Link>
          <Link href="/admin/notas" style={S.enlace}>Notas</Link>
          <Link href="/admin/enlaces" style={S.enlace}>Enlaces</Link>
          <SalirBoton />
        </div>
      </nav>
      <main style={S.contenido}>{children}</main>
    </div>
  );
}

const S: Record<string, React.CSSProperties> = {
  marco: { minHeight: "100dvh", background: "var(--fondo)" },
  barra: {
    position: "sticky", top: 0, zIndex: 20, display: "flex", flexWrap: "wrap", gap: "10px 20px",
    alignItems: "center", justifyContent: "space-between", padding: "12px 24px",
    background: "var(--fondo-2)", borderBottom: "1px solid var(--linea)",
  },
  marca: { display: "flex", alignItems: "baseline", gap: 12 },
  logo: { color: "var(--tx)", textDecoration: "none", fontWeight: 600, fontSize: 15.5 },
  quien: { fontSize: 13, color: "var(--mut)" },
  enlaces: { display: "flex", gap: 4, alignItems: "center", flexWrap: "wrap", rowGap: 6 },
  enlace: {
    color: "var(--tx-2)", textDecoration: "none", fontSize: 14,
    padding: "7px 11px", borderRadius: 7,
  },
  contenido: { maxWidth: 1100, margin: "0 auto", padding: "30px 24px 64px" },
};

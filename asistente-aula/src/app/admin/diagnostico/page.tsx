import { supabaseServidor } from "@/lib/supabase/sesion";
import { leerDiagnostico } from "@/lib/contenido";
import { SalaDiagnostico } from "@/components/SalaDiagnostico";
import { ResultadosDiagnostico } from "@/components/ResultadosDiagnostico";

export const dynamic = "force-dynamic";
export const metadata = { title: "Diagnóstico de entrada" };

type Fila = {
  id: string;
  creado_en: string;
  nombre: string;
  seccion: string;
  respuestas: Record<string, string | string[]>;
};

/**
 * La sala y las respuestas, en una sola página.
 *
 * Arriba la sala, porque es lo que se mira con la clase delante; debajo los
 * resultados, que se leen después y sin prisa.
 *
 * Se lee con la sesión del docente y la clave anónima, igual que la asistencia:
 * es la RLS la que decide, no esta página. Sin sesión no llega ni una fila, así
 * que no hay que comprobar nada aquí.
 */
export default async function Pagina() {
  const sb = await supabaseServidor();
  const { data, error } = await sb
    .from("diagnostico")
    .select("id,creado_en,nombre,seccion,respuestas")
    .order("creado_en", { ascending: false });

  const filas = (data ?? []) as Fila[];
  const { preguntas, secciones } = await leerDiagnostico();

  return (
    <main style={S.pantalla}>
      <header style={S.cabecera}>
        <p style={S.eyebrow}>Primera clase</p>
        <h1 style={S.titulo}>Diagnóstico de entrada</h1>
      </header>

      <SalaDiagnostico secciones={secciones} />

      {error && <p style={S.error}>No se pudieron leer las respuestas: {error.message}</p>}

      <ResultadosDiagnostico filas={filas} preguntas={preguntas} secciones={secciones} />
    </main>
  );
}

const S: Record<string, React.CSSProperties> = {
  pantalla: { padding: "34px 22px 80px", maxWidth: 900, margin: "0 auto" },
  cabecera: { marginBottom: 24 },
  eyebrow: { margin: 0, fontSize: 12, letterSpacing: ".16em", textTransform: "uppercase", color: "var(--aqua)" },
  titulo: { margin: "8px 0 0", fontSize: 30, fontWeight: 700, letterSpacing: "-.02em" },
  error: { marginTop: 20, color: "var(--rojo)", fontSize: 14 },
};

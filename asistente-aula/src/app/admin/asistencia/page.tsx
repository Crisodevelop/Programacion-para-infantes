import { AreaAsistencia } from "@/components/AreaAsistencia";

export const dynamic = "force-dynamic";
export const metadata = { title: "Asistencia" };

/**
 * Pasar lista, corregirla y borrarla. Todo se lee y se escribe desde el
 * navegador con la sesión del docente: es la RLS la que decide, y así editar o
 * borrar se ve al momento sin recargar la página.
 */
export default function Pagina() {
  return (
    <>
      <header style={{ marginBottom: 18 }}>
        <h1 style={{ fontSize: 30, margin: 0, letterSpacing: "-.025em" }}>Asistencia</h1>
        <p style={{ margin: "10px 0 0", fontSize: 15.5, color: "var(--tx-2)" }}>
          Pasa lista, corrige una que ya guardaste o bórrala. Lo que marcaron los estudiantes en la clase en vivo aparece aquí.
        </p>
      </header>
      <AreaAsistencia />
    </>
  );
}

import { ClaseEnVivo } from "@/components/ClaseEnVivo";

export const dynamic = "force-dynamic";
export const metadata = { title: "Clase en vivo" };

/**
 * Donde empieza la clase: el docente la abre, los estudiantes eligen su nombre
 * (y así queda pasada la lista) y aquí se ve quién entró y cuánto lleva.
 */
export default function Pagina() {
  return (
    <main style={S.pantalla}>
      <header style={S.cabecera}>
        <p style={S.eyebrow}>Tú decides cuándo empieza</p>
        <h1 style={S.titulo}>Clase en vivo</h1>
      </header>
      <ClaseEnVivo />
    </main>
  );
}

const S: Record<string, React.CSSProperties> = {
  pantalla: { padding: "34px 22px 80px", maxWidth: 900, margin: "0 auto" },
  cabecera: { marginBottom: 24 },
  eyebrow: { margin: 0, fontSize: 12, letterSpacing: ".16em", textTransform: "uppercase", color: "var(--aqua)" },
  titulo: { margin: "8px 0 0", fontSize: 30, fontWeight: 700, letterSpacing: "-.02em" },
};

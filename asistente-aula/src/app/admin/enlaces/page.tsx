import { PanelEnlaces } from "@/components/PanelEnlaces";

export const dynamic = "force-dynamic";
export const metadata = { title: "Enlaces del inicio" };

export default function Pagina() {
  return (
    <main style={{ padding: "34px 22px 80px", maxWidth: 820, margin: "0 auto" }}>
      <header style={{ marginBottom: 22 }}>
        <p style={{ margin: 0, fontSize: 12, letterSpacing: ".16em",
                    textTransform: "uppercase", color: "var(--aqua)" }}>Página de inicio</p>
        <h1 style={{ margin: "8px 0 0", fontSize: 30, fontWeight: 700,
                     letterSpacing: "-.02em" }}>Enlaces</h1>
        <p style={{ margin: "10px 0 0", fontSize: 15, color: "var(--tx-2)", maxWidth: "60ch" }}>
          Salen en el inicio, debajo de las tarjetas de los tres cursos. Los ve cualquiera
          que entre, sin necesidad de cuenta.
        </p>
      </header>
      <PanelEnlaces />
    </main>
  );
}

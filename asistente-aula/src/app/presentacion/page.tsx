import type { Metadata } from "next";
import { leerGenerada } from "@/lib/contenido";
import { PaginaGenerada } from "@/components/PaginaGenerada";
import { PanelDocente } from "@/components/PanelDocente";

export const dynamic = "force-static";

export async function generateMetadata(): Promise<Metadata> {
  const { titulo } = await leerGenerada("presentacion");
  return { title: titulo, description: "Presentación de la primera clase." };
}

export default async function Pagina() {
  const { fuente, html, css, js } = await leerGenerada("presentacion");
  return (
    <>
      {fuente && <link rel="stylesheet" href={fuente} />}
      <style dangerouslySetInnerHTML={{ __html: css }} />
      <PaginaGenerada html={html} js={js} />
      {/* Se monta para todo el mundo: el bloqueo es para los estudiantes. Solo
          enseña controles a quien tiene sesión de docente. */}
      <PanelDocente />
    </>
  );
}

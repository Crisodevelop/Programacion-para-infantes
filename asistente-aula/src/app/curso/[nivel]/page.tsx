import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { leerGenerada, esNivel, NIVELES } from "@/lib/contenido";
import { PaginaGenerada } from "@/components/PaginaGenerada";

export const dynamic = "force-static";

export function generateStaticParams() {
  return NIVELES.map((nivel) => ({ nivel }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ nivel: string }> },
): Promise<Metadata> {
  const { nivel } = await params;
  if (!esNivel(nivel)) return { title: "No encontrado" };
  const { titulo } = await leerGenerada(`nivel-${nivel}`);
  return { title: titulo };
}

/**
 * Un curso entero: su contenido y su metodología.
 *
 * Se basta solo a propósito. Antes había que buscar la metodología en otra
 * parte del documento largo; con el grupo delante, cambiar de página para
 * recordar cómo se reparten los 45 minutos no es una opción.
 */
export default async function Pagina({ params }: { params: Promise<{ nivel: string }> }) {
  const { nivel } = await params;
  if (!esNivel(nivel)) notFound();
  const { fuente, html, css, js } = await leerGenerada(`nivel-${nivel}`);
  return (
    <>
      {fuente && <link rel="stylesheet" href={fuente} />}
      <style dangerouslySetInnerHTML={{ __html: css }} />
      <PaginaGenerada html={html} js={js} />
    </>
  );
}

import { leerGenerada } from "@/lib/contenido";
import { PaginaGenerada } from "@/components/PaginaGenerada";
import { Enlaces } from "@/components/Enlaces";

export const dynamic = "force-static";

export async function generateMetadata() {
  const { titulo } = await leerGenerada("inicio");
  return {
    title: titulo,
    description: "La planificación completa del curso de Programación, de 1ro a 3ro.",
  };
}

/**
 * Lo primero que ve un estudiante.
 *
 * Antes había una portada con dos tarjetas que solo servía para llevar a otro
 * sitio: un clic de peaje antes de lo único que le interesa. Ahora entra
 * directo en la planificación.
 */
export default async function Pagina() {
  const { fuente, html, css, js } = await leerGenerada("inicio");
  return (
    <>
      {fuente && <link rel="stylesheet" href={fuente} />}
      <style dangerouslySetInnerHTML={{ __html: css }} />
      <PaginaGenerada html={html} js={js} />
      {/* Rellena el hueco que deja el generador. Sin enlaces no pinta nada. */}
      <Enlaces />
    </>
  );
}

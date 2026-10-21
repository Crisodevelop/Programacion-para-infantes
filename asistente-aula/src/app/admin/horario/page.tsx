import { leerGenerada } from "@/lib/contenido";
import { PaginaGenerada } from "@/components/PaginaGenerada";

export const dynamic = "force-dynamic";
export const metadata = { title: "Horario" };

/**
 * El horario y «Mi semana», que antes estaban en el plan público.
 *
 * Decían a qué hora está con cada sección y qué prepara cada día: eso es
 * información del docente, no del estudiante. El layout de /admin ya
 * comprueba que quien mira es docente.
 */
export default async function Pagina() {
  const { fuente, html, css, js } = await leerGenerada("horario");
  return (
    <>
      {fuente && <link rel="stylesheet" href={fuente} />}
      <style dangerouslySetInnerHTML={{ __html: css }} />
      <PaginaGenerada html={html} js={js} />
    </>
  );
}

import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { leerClase, indiceCurso } from "@/lib/contenido";
import { PaginaGenerada } from "@/components/PaginaGenerada";
import { PanelDocente } from "@/components/PanelDocente";
import { EntradaClase } from "@/components/EntradaClase";

export const dynamic = "force-static";

export async function generateStaticParams() {
  const clases = await indiceCurso();
  return clases.map((c) => ({ nivel: c.nivel, n: String(c.n) }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ nivel: string; n: string }> },
): Promise<Metadata> {
  const { nivel, n } = await params;
  const mazo = await leerClase(nivel, Number(n));
  return { title: mazo?.titulo ?? "Clase" };
}

export default async function Pagina(
  { params }: { params: Promise<{ nivel: string; n: string }> },
) {
  const { nivel, n } = await params;
  const mazo = await leerClase(nivel, Number(n));
  if (!mazo) notFound();
  return (
    <>
      {mazo.fuente && <link rel="stylesheet" href={mazo.fuente} />}
      <style dangerouslySetInnerHTML={{ __html: mazo.css }} />
      <PaginaGenerada html={mazo.html} js={mazo.js} />
      {/* El docente: bloqueo de juegos, pasar lista y el guion. «Cerrar la
          presentación» no aplica: las de cada semana sirven para repasar. */}
      <PanelDocente nivel={nivel} respetarCierre={false} />
      {/* La ventana del principio: el estudiante elige su nombre (queda presente)
          y desde ahí su nota se guarda sola. En el proyector del docente no sale. */}
      <EntradaClase nivel={nivel} semana={Number(n)} />
    </>
  );
}

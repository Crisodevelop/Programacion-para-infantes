import type { Metadata } from "next";
import { leerDiagnostico } from "@/lib/contenido";
import { Diagnostico } from "@/components/Diagnostico";

/**
 * El diagnóstico, como lo abre el estudiante desde el QR proyectado.
 *
 * `noindex` no es una formalidad: son menores respondiendo en un sitio
 * público. Que la página exista no significa que tenga que aparecer en una
 * búsqueda.
 */
export const metadata: Metadata = {
  title: "Antes de empezar",
  description: "Diez preguntas para saber de dónde parte el grupo.",
  robots: { index: false, follow: false },
};

export default async function Pagina({
  searchParams,
}: {
  searchParams: Promise<{ curso?: string }>;
}) {
  const { curso } = await searchParams;
  const datos = await leerDiagnostico();
  const valido = curso && ["1ro", "2do", "3ro"].includes(curso) ? curso : undefined;
  return <Diagnostico datos={datos} curso={valido} />;
}

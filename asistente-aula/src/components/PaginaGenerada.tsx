"use client";

import { useEffect, useRef } from "react";

/**
 * Monta una página generada fuera de React.
 *
 * El marcado se inyecta tal cual y el comportamiento se ejecuta al montar,
 * pasándole una señal de cancelación: al salir de la ruta se aborta y todos
 * los escuchadores se van con ella. Sin eso, ir del plan a la presentación y
 * volver dejaría el atajo de flecha derecha respondiendo dos veces.
 */
export function PaginaGenerada({ html, js }: { html: string; js: string }) {
  const caja = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!caja.current || !js) return;
    const controlador = new AbortController();
    try {
      // El código viene de nuestros propios generadores, no de la red ni del
      // usuario: no hay entrada externa que pueda acabar aquí dentro.
      new Function("senal", js)(controlador.signal);
    } catch (e) {
      console.error("[asistente] falló el comportamiento de la página:", e);
    }
    return () => controlador.abort();
  }, [js]);

  // La clase `pg` es la que el exportador puso en lugar de `body` al reescribir
  // el CSS. Este div es, para la página generada, lo que <body> era en el
  // archivo suelto: su lienzo.
  //
  // Antes llevaba `display: contents`, que lo sacaba del árbol de cajas y
  // dejaba a los hijos de la página compitiendo por celdas con lo que Next.js
  // cuelga de <body> —datos de React, scripts, el panel de errores—. Con la
  // rejilla de la barra lateral eso aplastó el plan en una columna de 246px.
  return <div ref={caja} className="pg" dangerouslySetInnerHTML={{ __html: html }} />;
}

"use client";
import { useEffect } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";

/**
 * Los enlaces del inicio.
 *
 * La página de inicio se genera desde `contenido.py` y se publica estática, así
 * que los enlaces no pueden ir horneados: cambiar uno sería editar Python y
 * regenerar, y una lista de recursos se toca en mitad de una semana.
 *
 * El generador deja el hueco —`<section id="enlaces" hidden>`— y esto lo
 * rellena en el navegador. Es el mismo patrón que usa `PanelDocente` con la
 * lista de clase: la página no es React, se le llena el hueco desde fuera.
 *
 * ─── Por qué esto sí lo lee cualquiera ───
 * La RLS de `enlace` deja leer sin sesión, al revés que la de `lista`. Son
 * enlaces publicados a propósito: si hiciera falta sesión para verlos, no
 * servirían para nada. Escribirlos sigue siendo cosa del docente.
 */
type Enlace = { id: string; titulo: string; url: string; descripcion: string };

export function Enlaces() {
  useEffect(() => {
    let vivo = true;
    (async () => {
      const { data } = await supabaseNavegador()
        .from("enlace")
        .select("id,titulo,url,descripcion")
        .eq("activo", true)
        .order("orden")
        .order("creado_en");

      const lista = (data ?? []) as Enlace[];
      if (!vivo) return;

      const seccion = document.getElementById("enlaces");
      const caja = seccion?.querySelector<HTMLElement>("[data-enlaces]");
      // El mismo interruptor apaga la entrada de la barra lateral: un enlace
      // del menú que lleva a una sección oculta es un callejón.
      const enMenu = document.querySelector<HTMLElement>('.lateral a[href="#enlaces"]');
      if (!seccion || !caja) return;

      // Sin enlaces la sección no aparece: un encabezado sobre un hueco vacío
      // es peor que no tener la sección.
      if (lista.length === 0) {
        seccion.hidden = true;
        if (enMenu) enMenu.hidden = true;
        return;
      }

      caja.replaceChildren(...lista.map(tarjeta));
      seccion.hidden = false;
      if (enMenu) enMenu.hidden = false;
    })();
    return () => { vivo = false; };
  }, []);

  return null;
}

/**
 * Se construye con el DOM y no con `innerHTML`.
 *
 * El título y la descripción los escribe el docente, pero esto acaba en una
 * página pública: creando los nodos, el texto es texto y no hay forma de que
 * un `<script>` se cuele por ahí. La dirección, además, tiene que empezar por
 * http — la base ya lo exige, y aquí se vuelve a mirar porque el coste es una
 * línea y lo que evita es código ajeno ejecutándose en el navegador de un
 * estudiante.
 */
function tarjeta(e: Enlace): HTMLElement {
  const a = document.createElement("a");
  a.className = "nivel-tarjeta lvl-co";
  a.href = /^https?:\/\//i.test(e.url) ? e.url : "#";
  a.target = "_blank";
  a.rel = "noopener noreferrer";

  const donde = document.createElement("span");
  donde.className = "nt-eyebrow";
  donde.textContent = dominio(e.url);

  const titulo = document.createElement("span");
  titulo.className = "nt-titulo";
  titulo.textContent = e.titulo;

  a.append(donde, titulo);

  if (e.descripcion) {
    const t = document.createElement("span");
    t.className = "nt-texto";
    t.textContent = e.descripcion;
    a.append(t);
  }

  const flecha = document.createElement("span");
  flecha.className = "nt-flecha";
  flecha.textContent = "Abrir →";
  a.append(flecha);
  return a;
}

/** «https://scratch.mit.edu/projects» → «scratch.mit.edu». */
function dominio(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "enlace";
  }
}

"use client";

import { useEffect, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";

/**
 * ¿Quién está mirando esta página?
 *
 * `null` mientras no se sabe, y solo entonces `true` o `false`. Esa tercera
 * respuesta es la importante: la ventana de «elige tu nombre» se dibujaba en
 * el proyector del docente porque el componente daba por hecho que no lo era
 * mientras llegaba la respuesta de Supabase.
 *
 * La comprobación es la de siempre —`getUser()` y el rol del perfil— y la RLS
 * sigue mandando sobre los datos: esto solo decide qué se enseña.
 */
export function useDocente(): boolean | null {
  const [docente, setDocente] = useState<boolean | null>(null);

  useEffect(() => {
    let vivo = true;
    (async () => {
      const sb = supabaseNavegador();
      try {
        const { data: { user } } = await sb.auth.getUser();
        if (!user) { if (vivo) setDocente(false); return; }
        const { data } = await sb.from("profiles").select("role").eq("id", user.id).maybeSingle();
        if (vivo) setDocente(data?.role === "docente");
      } catch {
        // Sin red no se puede saber: se trata como estudiante, que es el caso
        // seguro —no se abre nada del docente— y el siguiente render reintenta.
        if (vivo) setDocente(false);
      }
    })();
    return () => { vivo = false; };
  }, []);

  return docente;
}

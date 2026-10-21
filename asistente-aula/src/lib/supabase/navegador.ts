"use client";
import { createBrowserClient } from "@supabase/ssr";

/**
 * Cliente del navegador, con la clave anónima.
 *
 * Esta clave es pública a propósito: viaja al navegador de cualquiera. Lo que
 * decide qué puede leer cada quien no es la clave, es la RLS junto con la
 * sesión. Sin sesión de docente, `asistencia` devuelve cero filas aunque se
 * consulte directamente desde la consola del navegador.
 */
export function supabaseNavegador() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}

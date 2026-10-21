import "server-only";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { config } from "@/lib/config";

/**
 * Cliente de Supabase con la clave de servicio.
 *
 * Salta la RLS, así que solo puede existir en el servidor. Es legítimo aquí
 * porque este proceso corre en el Mac del docente y no lo alcanza nadie más:
 * el mando exige ASISTENTE_CLAVE y el sitio de los estudiantes es otra app.
 */
let cliente: SupabaseClient | null = null;

export function supabase(): SupabaseClient {
  if (cliente) return cliente;
  if (!config.supabase.url || !config.supabase.servicio) {
    throw new Error("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local.");
  }
  cliente = createClient(config.supabase.url, config.supabase.servicio, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  return cliente;
}

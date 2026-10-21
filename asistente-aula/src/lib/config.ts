import "server-only";

/**
 * Configuración del servidor.
 *
 * Todo lo secreto vive en `.env.local`, que está en `.gitignore`. Nada de esto
 * lleva prefijo `NEXT_PUBLIC_`: si una de estas variables cruzara al navegador,
 * cualquiera podría leerla desde el inspector.
 */

export const config = {
  supabase: {
    url: process.env.SUPABASE_URL ?? "",
    servicio: process.env.SUPABASE_SERVICE_ROLE_KEY ?? "",
  },
} as const;

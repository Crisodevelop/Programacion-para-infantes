import "server-only";
import { cookies } from "next/headers";
import { createServerClient } from "@supabase/ssr";

/** Cliente de servidor atado a las cookies de la petición. */
export async function supabaseServidor() {
  const almacen = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => almacen.getAll(),
        setAll: (nuevas) => {
          try {
            for (const { name, value, options } of nuevas) almacen.set(name, value, options);
          } catch {
            // En un Server Component no se pueden escribir cookies. No pasa
            // nada: el middleware ya refrescó la sesión antes de llegar aquí.
          }
        },
      },
    },
  );
}

export type Docente = { id: string; nombre: string; correo: string };

/**
 * Quién está pidiendo esto, si es docente.
 *
 * Se usa `getUser()` y no `getSession()`: getSession lee la cookie sin
 * verificarla contra el servidor de auth, y una cookie se puede falsificar.
 * Para decidir si alguien entra al área de administración eso no vale.
 */
export async function docenteActual(): Promise<Docente | null> {
  const sb = await supabaseServidor();
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return null;

  const { data: perfil } = await sb
    .from("profiles")
    .select("id, display_name, role")
    .eq("id", user.id)
    .maybeSingle();

  if (!perfil || perfil.role !== "docente") return null;
  return {
    id: perfil.id as string,
    nombre: (perfil.display_name as string) ?? "Docente",
    correo: user.email ?? "",
  };
}

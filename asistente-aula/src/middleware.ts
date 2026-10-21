import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";

/**
 * Refresca la sesión y guarda el área de administración.
 *
 * El middleware solo comprueba que HAYA sesión; que además sea docente lo
 * decide cada página con `docenteActual()`, que consulta el perfil. Se separa
 * a propósito: el middleware corre en el runtime de borde, donde una consulta
 * a la base en cada navegación se paga en latencia, y la comprobación de rol
 * de verdad la hace la RLS cuando la página pide datos.
 */
export async function middleware(peticion: NextRequest) {
  let respuesta = NextResponse.next({ request: peticion });

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  // Sin credenciales no hay sesión que refrescar, y el cliente de Supabase
  // lanzaría. Como el middleware corre en casi todas las rutas, eso convertía
  // un despliegue al que le falta una variable en un 500 en TODO el sitio,
  // incluidas las páginas de clase, que no tocan la base. Se cierra el área de
  // administración —sin auth no se puede comprobar quién eres— y el material
  // se sigue sirviendo.
  if (!url || !anon) {
    return peticion.nextUrl.pathname.startsWith("/admin")
      ? NextResponse.redirect(new URL("/entrar", peticion.nextUrl))
      : respuesta;
  }

  const sb = createServerClient(
    url,
    anon,
    {
      cookies: {
        getAll: () => peticion.cookies.getAll(),
        setAll: (nuevas) => {
          for (const { name, value } of nuevas) peticion.cookies.set(name, value);
          respuesta = NextResponse.next({ request: peticion });
          for (const { name, value, options } of nuevas) respuesta.cookies.set(name, value, options);
        },
      },
    },
  );

  const { data: { user } } = await sb.auth.getUser();

  if (!user && peticion.nextUrl.pathname.startsWith("/admin")) {
    const destino = peticion.nextUrl.clone();
    destino.pathname = "/entrar";
    // Para volver a donde iba después de entrar.
    destino.searchParams.set("volver", peticion.nextUrl.pathname);
    return NextResponse.redirect(destino);
  }

  return respuesta;
}

export const config = {
  // Se excluyen los estáticos y las rutas del asistente: esas las guarda
  // `guardia.ts` con la clave de emparejamiento, no con la sesión, porque el
  // celular se empareja como dispositivo y no inicia sesión.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};

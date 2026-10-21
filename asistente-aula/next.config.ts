import type { NextConfig } from "next";

const config: NextConfig = {
  // Compilar no puede tumbar lo que hay abierto.
  //
  // `next build` y `next dev` escriben los dos en `.next`. Si se lanza un
  // build mientras el servidor de desarrollo está en marcha, el build se lleva
  // por delante el CSS de desarrollo: las páginas siguen respondiendo 200 pero
  // piden una hoja que ya no existe, y el navegador las pinta sobre blanco.
  // Pasó, y con las presentaciones abiertas. Con esto, una comprobación de
  // compilación puede escribir en otra carpeta:
  //   NEXT_DIST_DIR=.next-verificar next build   →  npm run verificar
  distDir: process.env.NEXT_DIST_DIR ?? ".next",

  // Esta app se ejecuta SOLO en la máquina del docente: sus rutas abren
  // aplicaciones y mueven el navegador. Desplegarla en un servidor no tendría
  // sentido (no hay Mac que controlar) y expondría el ejecutor de comandos.
  // El aviso queda aquí para que se lea antes que en ningún otro sitio.
  reactStrictMode: true,

  // El aula entra por la IP de la red, no por localhost: el proyector y los
  // equipos de los estudiantes abren http://172.20.1.64:3002. Next avisa de
  // cada petición a /_next/* que no venga del host del servidor y en una
  // versión mayor próxima pasará a bloquearlas. Solo afecta a `next dev`.
  allowedDevOrigins: ["172.20.1.64", "*.local"],

  // El código de los talleres para programar no va en la página: lo entrega
  // la API, que lo lee del disco. Sin esto Vercel no mete esos archivos en la
  // función y la API respondería vacío.
  outputFileTracingIncludes: {
    "/api/taller/[via]/[n]/codigo": ["./src/contenido/taller/**/*.codigo.json"],
  },
};

export default config;

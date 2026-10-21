/**
 * Aplica las migraciones de `migraciones/` al proyecto de Supabase.
 *
 * Usa el token de administración, que es lo único que puede crear tablas.
 * Ese token NO lo necesita la app en marcha: se lee aquí, en un script que se
 * ejecuta a mano, y por eso vive aparte de la clave de servicio.
 *
 *   npm run db:migrar
 */
import { readFile, readdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const aqui = dirname(fileURLToPath(import.meta.url));
const carpeta = join(aqui, "..", "migraciones");

await cargarEnv(join(aqui, "..", ".env.local"));

const token = process.env.SUPABASE_ACCESS_TOKEN;
const ref = process.env.SUPABASE_PROJECT_REF;
if (!token || !ref) {
  console.error("Faltan SUPABASE_ACCESS_TOKEN o SUPABASE_PROJECT_REF en .env.local");
  process.exit(1);
}

const archivos = (await readdir(carpeta)).filter((f) => f.endsWith(".sql")).sort();
if (!archivos.length) {
  console.log("No hay migraciones que aplicar.");
  process.exit(0);
}

for (const archivo of archivos) {
  const sql = await readFile(join(carpeta, archivo), "utf8");
  process.stdout.write(`  ${archivo} … `);

  const respuesta = await fetch(`https://api.supabase.com/v1/projects/${ref}/database/query`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ query: sql }),
  });

  if (!respuesta.ok) {
    const detalle = await respuesta.text();
    console.log("falló");
    console.error(detalle);
    process.exit(1);
  }
  console.log("aplicada");
}

console.log("\nListo.");

/** dotenv en miniatura: no merece una dependencia para esto. */
async function cargarEnv(ruta: string): Promise<void> {
  let texto: string;
  try {
    texto = await readFile(ruta, "utf8");
  } catch {
    return;
  }
  for (const linea of texto.split("\n")) {
    const limpia = linea.trim();
    if (!limpia || limpia.startsWith("#")) continue;
    const i = limpia.indexOf("=");
    if (i < 1) continue;
    const nombre = limpia.slice(0, i).trim();
    const valor = limpia.slice(i + 1).trim().replace(/^["']|["']$/g, "");
    if (!(nombre in process.env)) process.env[nombre] = valor;
  }
}

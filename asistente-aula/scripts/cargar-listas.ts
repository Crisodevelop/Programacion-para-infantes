/**
 * Sube las listas de clase a Supabase.
 *
 *   python3 ../planificacion/extraer_listas.py ~/Downloads/Listas --json /tmp/listas.json
 *   npm run listas:cargar -- /tmp/listas.json
 *
 * Dos pasos y no uno porque un .docx es un ZIP con XML dentro, y eso en Python
 * son tres líneas de biblioteca estándar. El paso de Python además imprime lo
 * que va a subir y aborta si algún archivo no cuadra con su propia fila TOTAL:
 * conviene mirarlo antes de escribir en la base.
 *
 * Es idempotente. Volver a correrlo con el mismo archivo no duplica a nadie:
 * un estudiante repetido en la lista de clase es peor que uno que falta,
 * porque aparece dos veces al pasar lista y nadie sabe cuál marcar.
 *
 * A quien agregaste tú desde la presentación no lo toca: si la escuela manda
 * una lista corregida, el que metiste a mano sigue ahí.
 */
import { readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";

type Alumno = {
  apellidos: string; nombres: string; nombre: string;
  sexo: "F" | "M"; nuevo: boolean; dudoso: boolean; bruto: string;
};
type Seccion = { seccion: string; titular: string; alumnos: Alumno[] };

const aqui = dirname(fileURLToPath(import.meta.url));
await cargarEnv(join(aqui, "..", ".env.local"));

const ruta = process.argv[2];
if (!ruta) {
  console.error("Uso: npm run listas:cargar -- ruta/al/listas.json");
  process.exit(1);
}

const url = process.env.SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL;
const clave = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !clave) {
  console.error("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local");
  process.exit(1);
}
const sb = createClient(url, clave, { auth: { persistSession: false } });

const secciones = JSON.parse(await readFile(ruta, "utf8")) as Seccion[];
const dudosos = secciones.flatMap((s) =>
  s.alumnos.filter((a) => a.dudoso).map((a) => `${s.seccion}: «${a.bruto}» → ${a.nombre}`));

let nuevos = 0, ya = 0;
for (const s of secciones) {
  const { data: existentes } = await sb
    .from("lista").select("nombre").eq("seccion", s.seccion);
  const tengo = new Set((existentes ?? []).map((r) => normalizar(r.nombre as string)));

  const faltan = s.alumnos.filter((a) => !tengo.has(normalizar(a.nombre)));
  ya += s.alumnos.length - faltan.length;

  if (faltan.length) {
    const { error } = await sb.from("lista").insert(faltan.map((a) => ({
      seccion: s.seccion, apellidos: a.apellidos, nombres: a.nombres,
      nombre: a.nombre, sexo: a.sexo, nuevo: a.nuevo,
    })));
    if (error) {
      console.error(`  ${s.seccion}: ${error.message}`);
      process.exit(1);
    }
    nuevos += faltan.length;
  }
  const { count } = await sb.from("lista")
    .select("*", { count: "exact", head: true }).eq("seccion", s.seccion);
  console.log(`  ${s.seccion}  ${String(faltan.length).padStart(3)} nuevos · ` +
              `${count} en total · ${s.titular}`);
}

console.log(`\n${nuevos} altas, ${ya} que ya estaban.`);
if (dudosos.length) {
  console.log("\n⚠ Sin coma en el documento: confirma dónde acaba el apellido.");
  for (const d of dudosos) console.log("   " + d);
  console.log("   Se corrige en el panel de la presentación o directamente en la tabla.");
}

/** Compara sin tildes ni mayúsculas, como el índice único de la base. */
function normalizar(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, " ").trim();
}

/** dotenv en miniatura: no merece una dependencia para esto. */
async function cargarEnv(ruta: string): Promise<void> {
  let texto: string;
  try { texto = await readFile(ruta, "utf8"); } catch { return; }
  for (const linea of texto.split("\n")) {
    const l = linea.trim();
    if (!l || l.startsWith("#")) continue;
    const i = l.indexOf("=");
    if (i < 1) continue;
    const nombre = l.slice(0, i).trim();
    if (!(nombre in process.env)) process.env[nombre] = l.slice(i + 1).trim().replace(/^["']|["']$/g, "");
  }
}

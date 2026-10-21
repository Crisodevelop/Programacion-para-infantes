/**
 * Pone a mano la nota de una semana que no se guardó sola.
 *
 *   npm run notas:semana -- 1              # enseña lo que haría, no escribe
 *   npm run notas:semana -- 1 --escribir   # lo escribe
 *
 * La semana 1 es la única clase desenchufada de las doce: nadie tocó una
 * computadora, así que nadie guardó nota y la semana no existe en `notas`.
 * Pero la clase se dio y se evalúa por participación.
 *
 * A diferencia de los otros scripts del repo, este NO escribe si no se lo
 * pides. Los demás suben el padrón que manda la escuela; este pone
 * calificaciones a cientos de menores, y conviene leer el ensayo antes.
 *
 * Es idempotente: a quien ya tenga nota de esa semana no se le toca, venga de
 * donde venga. Correrlo dos veces no duplica ni pisa una nota ganada en clase.
 *
 * Recibe nota quien esté activo en `lista` Y tenga al menos una fila en
 * `asistencia_registros` —presente, tarde, ausente o excusa, da igual—. Quien
 * no sale en ninguna lista se queda fuera: entró al padrón después de que se
 * pasara lista, o su sección nunca la tuvo, y no hay forma de saber si estaba.
 */
import { readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";

type Alumno = { id: string; nombre: string };
type Reparto = { dar: { id: string; nombre: string; puntos: number }[]; sinLista: number; yaTenian: number };

/**
 * 80–100 estable, sacado del uuid del estudiante.
 *
 * Con Math.random() el ensayo enseñaría unos números y se escribirían otros,
 * que es justo lo que el ensayo tiene que evitar.
 */
export function nota(id: string, min = 80, max = 100): number {
  let h = 0;
  for (const c of id) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return min + (h % (max - min + 1));
}

/** Quién recibe nota en una sección, y cuánta. Sin tocar la red. */
export function reparto(
  alumnos: Alumno[], conAsistencia: Set<string>, yaConNota: Set<string>,
  min = 80, max = 100,
): Reparto {
  const dar: Reparto["dar"] = [];
  let sinLista = 0, yaTenian = 0;
  for (const a of alumnos) {
    if (yaConNota.has(a.id)) { yaTenian++; continue; }
    if (!conAsistencia.has(a.id)) { sinLista++; continue; }
    dar.push({ id: a.id, nombre: a.nombre.slice(0, 60), puntos: nota(a.id, min, max) });
  }
  return { dar, sinLista, yaTenian };
}

/** Lee una tabla entera: PostgREST corta en 1000 filas y aquí se pasa. */
async function todas<T>(
  sb: SupabaseClient, tabla: string, columnas: string,
  filtrar: (q: any) => any,
): Promise<T[]> {
  const salida: T[] = [];
  for (let desde = 0; ; desde += 1000) {
    const { data, error } = await filtrar(sb.from(tabla).select(columnas)).range(desde, desde + 999);
    if (error) throw new Error(`${tabla}: ${error.message}`);
    salida.push(...((data ?? []) as T[]));
    if ((data ?? []).length < 1000) return salida;
  }
}

async function main(): Promise<void> {
  const aqui = dirname(fileURLToPath(import.meta.url));
  await cargarEnv(join(aqui, "..", ".env.local"));

  const args = process.argv.slice(2);
  const semana = Number(args.find((a) => /^\d+$/.test(a)));
  const escribir = args.includes("--escribir");
  const min = Number(valor(args, "--min") ?? 80);
  const max = Number(valor(args, "--max") ?? 100);

  if (!Number.isInteger(semana) || semana < 1 || semana > 12) {
    console.error("Uso: npm run notas:semana -- <1-12> [--escribir] [--min 80] [--max 100]");
    process.exit(1);
  }
  if (!(min >= 0 && max <= 100 && min <= max)) {
    console.error("El rango tiene que ir de 0 a 100, y --min no puede pasar de --max.");
    process.exit(1);
  }

  const url = process.env.SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL;
  const clave = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !clave) {
    console.error("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local");
    process.exit(1);
  }
  const sb = createClient(url, clave, { auth: { persistSession: false } });

  const padron = await todas<{ id: string; seccion: string; nombre: string }>(
    sb, "lista", "id,seccion,nombre", (q) => q.eq("activo", true).order("seccion"));
  const secciones = [...new Set(padron.map((a) => a.seccion))].sort();
  if (!secciones.length) {
    console.error("No hay nadie activo en `lista`.");
    process.exit(1);
  }

  console.log(`\n  Nota de la semana ${semana} · ${min}–${max} puntos` +
              `${escribir ? "" : "  ·  ENSAYO, no se escribe nada"}\n`);

  let total = 0, sinLista = 0, yaTenian = 0;
  const saltadas: string[] = [];

  for (const seccion of secciones) {
    const alumnos = padron.filter((a) => a.seccion === seccion);

    // Las listas de esa sección, la más vieja primero: esa fecha es el día en
    // que se dio la semana 1. Con la de hoy, la clase saldría como dada hoy y
    // aparecería en Clase en vivo, que filtra por fecha = hoy_aula().
    const listas = await todas<{ id: string; fecha: string }>(
      sb, "asistencia", "id,fecha", (q) => q.eq("grupo", seccion).order("fecha"));
    if (!listas.length) {
      saltadas.push(seccion);
      console.log(`  ${seccion}  —  sin ninguna lista de asistencia: se salta`);
      continue;
    }
    const fecha = listas[0].fecha;

    const registros = await todas<{ estudiante_id: string }>(
      sb, "asistencia_registros", "estudiante_id",
      (q) => q.in("asistencia_id", listas.map((l) => l.id)));
    const conAsistencia = new Set(registros.map((r) => r.estudiante_id));

    const previas = await todas<{ estudiante_id: string | null }>(
      sb, "notas", "estudiante_id", (q) => q.eq("seccion", seccion).eq("semana", semana));
    const yaConNota = new Set(previas.map((n) => n.estudiante_id).filter((x): x is string => !!x));

    const { dar, sinLista: sl, yaTenian: yt } = reparto(alumnos, conAsistencia, yaConNota, min, max);
    total += dar.length; sinLista += sl; yaTenian += yt;

    if (escribir && dar.length) {
      const { error } = await sb.from("notas").insert(dar.map((d) => ({
        nombre: d.nombre,
        seccion,
        nivel: seccion.slice(0, 3),
        semana,
        puntos: d.puntos,
        detalle: { participacion: d.puntos },
        estudiante_id: d.id,
        fecha,
      })));
      if (error) {
        console.error(`  ${seccion}: ${error.message}`);
        process.exit(1);
      }
    }

    console.log(
      `  ${seccion}  ${String(dar.length).padStart(3)} ${escribir ? "escritas" : "pendientes"} · ` +
      `${String(sl).padStart(2)} sin asistencia · ${String(yt).padStart(2)} ya tenían · ` +
      `lista del ${fecha}`);
  }

  console.log(`\n  ${total} ${escribir ? "notas escritas" : "notas por escribir"} ` +
              `de la semana ${semana}.`);
  if (yaTenian) console.log(`  ${yaTenian} ya tenían nota de esa semana: no se tocaron.`);
  if (sinLista) {
    console.log(`\n  ⚠ ${sinLista} sin una sola fila de asistencia, así que se quedan sin nota.`);
    console.log("    Al escribir la semana, esa clase pasa a contar para su sección: a estos");
    console.log("    les saldrá como 0 en la nota acumulada. Mételos a mano si procede.");
  }
  if (saltadas.length) {
    console.log(`\n  ⚠ Sin ninguna lista de asistencia: ${saltadas.join(", ")}.`);
    console.log("    Pasa lista de un día de esas secciones y vuelve a correrlo.");
  }
  if (!escribir && total) console.log("\n  Repite con --escribir para guardarlas.\n");
}

function valor(args: string[], bandera: string): string | undefined {
  const i = args.indexOf(bandera);
  return i >= 0 ? args[i + 1] : undefined;
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

// Solo corre si lo invocas; importarlo —la prueba lo hace— no toca la base.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) await main();

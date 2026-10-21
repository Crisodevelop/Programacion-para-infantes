/**
 * Carga las listas reales de estudiantes desde un CSV.
 *
 *   npm run lista:importar -- listas/2do-a.csv
 *
 * El CSV lleva cabecera y dos columnas:
 *
 *   nombre_completo,grupo
 *   María Rodríguez,2do A
 *
 * Es idempotente: volver a correrlo con el mismo archivo no duplica a nadie,
 * porque un estudiante repetido en la lista de clase es peor que uno que falta
 * (aparece dos veces al pasar lista y nadie sabe cuál marcar).
 *
 * ─── Sobre las cuentas ───────────────────────────────────────────────────
 * `profiles.id` es clave foránea de `auth.users`, así que no se puede crear un
 * perfil suelto: hace falta una cuenta detrás. Se crea con un correo sintético
 * y NO enrutable (`nombre.grupo@lista.invalid`) y `email_confirm` activado,
 * de modo que no se envía ningún mensaje a ninguna parte.
 *
 * Es una decisión con peso: son cuentas de menores. Sirven solo para que la
 * asistencia tenga a quién apuntar; no dan acceso a nada mientras nadie les
 * fije una contraseña. Si prefieres que los estudiantes se registren ellos
 * mismos desde el sitio de Clases, no uses este script.
 */
import { readFile } from "node:fs/promises";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";

const aqui = dirname(fileURLToPath(import.meta.url));
await cargarEnv(join(aqui, "..", ".env.local"));

const ruta = process.argv[2];
if (!ruta) {
  console.error("Uso: npm run lista:importar -- ruta/al/archivo.csv");
  process.exit(1);
}

const url = process.env.SUPABASE_URL;
const clave = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !clave) {
  console.error("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local");
  process.exit(1);
}

const texto = await readFile(resolve(ruta), "utf8");
const lineas = texto.split("\n").map((l) => l.trim()).filter(Boolean);
if (lineas.length < 2) {
  console.error("El CSV no tiene filas de datos.");
  process.exit(1);
}

const filas = lineas.slice(1).map((linea) => {
  const [nombre, grupo] = linea.split(",").map((c) => c.trim().replace(/^"|"$/g, ""));
  return { nombre, grupo };
});

const invalidas = filas.filter((f) => !f.nombre || !f.grupo);
if (invalidas.length) {
  console.error(`${invalidas.length} fila(s) sin nombre o sin grupo. Revisa el CSV.`);
  process.exit(1);
}

const supabase = createClient(url, clave, { auth: { persistSession: false } });

/** «María Rodríguez» + «2do A» → «maria-rodriguez.2do-a@lista.invalid».
 *  `.invalid` está reservado por la RFC 2606 justo para esto: garantiza que
 *  el dominio no existe y que ningún correo puede salir hacia él. */
function correoSintetico(nombre: string, grupo: string): string {
  const trozo = (t: string) =>
    t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
      .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return `${trozo(nombre)}.${trozo(grupo)}@lista.invalid`;
}

let creados = 0;
let existentes = 0;
let fallidos = 0;

for (const fila of filas) {
  const { data: yaEsta } = await supabase
    .from("profiles")
    .select("id")
    .eq("display_name", fila.nombre)
    .eq("grupo", fila.grupo)
    .maybeSingle();

  if (yaEsta) {
    existentes++;
    continue;
  }

  // Primero la cuenta: sin ella el perfil viola profiles_id_fkey.
  const { data: cuenta, error: errorCuenta } = await supabase.auth.admin.createUser({
    email: correoSintetico(fila.nombre, fila.grupo),
    email_confirm: true,
    user_metadata: { display_name: fila.nombre, grupo: fila.grupo },
  });

  if (errorCuenta || !cuenta.user) {
    console.error(`  ${fila.nombre}: ${errorCuenta?.message ?? "no se creó la cuenta"}`);
    fallidos++;
    continue;
  }

  const { error } = await supabase.from("profiles").upsert({
    id: cuenta.user.id,
    display_name: fila.nombre,
    grupo: fila.grupo,
    role: "estudiante",
    is_guest: true,
  });

  if (error) {
    console.error(`  ${fila.nombre}: ${error.message}`);
    // Sin perfil, la cuenta queda huérfana y estorba: se deshace.
    await supabase.auth.admin.deleteUser(cuenta.user.id);
    fallidos++;
    continue;
  }
  creados++;
}

console.log(
  `Creados ${creados}, ya estaban ${existentes}` +
    (fallidos ? `, fallaron ${fallidos}` : "") +
    `, de ${filas.length} filas.`,
);
if (fallidos) process.exit(1);

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

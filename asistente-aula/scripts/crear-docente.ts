/**
 * Crea la cuenta de docente y siembra la clave de emparejamiento del mando.
 *
 *   npm run docente:crear -- correo@ejemplo.com
 *
 * Hace falta un script y no basta con el panel de Supabase porque son dos
 * cosas que tienen que ocurrir juntas: la cuenta en `auth.users` y su fila en
 * `profiles` con role='docente'. Una cuenta sin perfil entra pero `is_teacher()`
 * le dice que no, y el área de administración la rebota sin explicar por qué.
 *
 * Es idempotente: si la cuenta ya existe, solo se asegura de que el perfil
 * tenga el rol correcto y no toca la contraseña.
 */
import { readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { randomBytes } from "node:crypto";
import { createClient } from "@supabase/supabase-js";

const aqui = dirname(fileURLToPath(import.meta.url));
await cargarEnv(join(aqui, "..", ".env.local"));

const correo = (process.argv[2] ?? "").trim().toLowerCase();
if (!correo || !correo.includes("@")) {
  console.error("Uso: npm run docente:crear -- correo@ejemplo.com");
  process.exit(1);
}

const url = process.env.SUPABASE_URL;
const servicio = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!url || !servicio) {
  console.error("Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en .env.local");
  process.exit(1);
}

const sb = createClient(url, servicio, { auth: { persistSession: false } });

// ─── La cuenta ────────────────────────────────────────────────────────────
const { data: existentes } = await sb.auth.admin.listUsers({ page: 1, perPage: 200 });
let usuario = existentes?.users.find((u) => u.email?.toLowerCase() === correo);
let contrasena: string | null = null;

if (usuario) {
  console.log(`  La cuenta ${correo} ya existía. No se toca la contraseña.`);
} else {
  // Legible al dictarla en voz alta pero con entropía de sobra: 12 bytes.
  contrasena = randomBytes(12).toString("base64url");
  const { data, error } = await sb.auth.admin.createUser({
    email: correo,
    password: contrasena,
    email_confirm: true, // no se envía correo: no hay SMTP configurado
  });
  if (error || !data.user) {
    console.error(`  No se pudo crear la cuenta: ${error?.message}`);
    process.exit(1);
  }
  usuario = data.user;
  console.log(`  Cuenta creada: ${correo}`);
}

// ─── El perfil, con su rol ────────────────────────────────────────────────
const { error: errorPerfil } = await sb.from("profiles").upsert({
  id: usuario.id,
  display_name: process.env.ASISTENTE_DOCENTE_NOMBRE ?? "Docente",
  role: "docente",
  is_guest: false,
});
if (errorPerfil) {
  console.error(`  La cuenta existe pero el perfil falló: ${errorPerfil.message}`);
  process.exit(1);
}
console.log("  Perfil con role='docente' listo.");

// ─── La clave del mando ───────────────────────────────────────────────────
const { data: ajuste } = await sb
  .from("asistente_ajustes")
  .select("clave_mando")
  .eq("id", 1)
  .maybeSingle();

if (!ajuste) {
  // Se reaprovecha la de .env.local si ya había teléfonos emparejados con ella.
  const clave = process.env.ASISTENTE_CLAVE || randomBytes(24).toString("hex");
  const { error } = await sb.from("asistente_ajustes").insert({ id: 1, clave_mando: clave });
  if (error) console.error(`  No se pudo sembrar la clave del mando: ${error.message}`);
  else console.log("  Clave de emparejamiento guardada en la base.");
} else {
  console.log("  La clave de emparejamiento ya estaba en la base.");
}

if (contrasena) {
  console.log("\n  ┌──────────────────────────────────────────────────────");
  console.log(`  │  Correo:     ${correo}`);
  console.log(`  │  Contraseña: ${contrasena}`);
  console.log("  │");
  console.log("  │  Cámbiala al entrar. Esta línea queda en el historial");
  console.log("  │  de tu terminal, así que no la dejes ahí para siempre.");
  console.log("  └──────────────────────────────────────────────────────\n");
}

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
    if (!(nombre in process.env)) {
      process.env[nombre] = limpia.slice(i + 1).trim().replace(/^["']|["']$/g, "");
    }
  }
}

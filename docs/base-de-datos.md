# La base de datos, desde cero

Esta copia **no lleva base de datos**: ni los datos ni las credenciales de la
del aula, que tiene nombres y notas de menores de edad. Quien la abra tiene que
crearse la suya, y esta es la guía para hacerlo en unos diez minutos.

---

## Antes: casi todo se ve sin base de datos

Lo primero que pregunta cualquiera es qué queda si no hay base. Casi todo:

| Ruta | ¿Necesita base? |
|---|---|
| `/` la portada, `/plan`, `/presentacion` | **No.** Salen de `src/contenido/` |
| `/curso/1ro…3ro` y sus 36 semanas | **No.** `force-static`: las diapositivas son archivos |
| `/presentaciones` el índice para proyectar | **No** |
| `/diagnostico` | La prueba se ve; enviarla sí necesita base |
| El editor de Python de cada clase | **No.** Pyodide corre en el navegador |
| «Entrar a clase» y guardar la nota | **Sí** |
| `/entrar` y todo `/admin` | **Sí** |

Y esto ya está resuelto en el código, no hay que tocar nada:
`src/middleware.ts:19-29` detecta que faltan las credenciales, cierra el área
de admin —rebota a `/entrar`— y **sigue sirviendo todo el material**. Una copia
sin `.env.local` arranca y se puede recorrer entera; lo único que no funciona
es entrar como docente, y el formulario de `/entrar` falla al pulsar el botón
porque el cliente de Supabase lanza sin URL.

Así que la respuesta a «¿y cómo verán el contenido?» es: **lo ven, sin hacer
nada**. La base solo hace falta para la parte de gestión del aula —asistencia,
clase en vivo, notas—, que es justo la que no se puede enseñar con datos
reales. Para esa parte hay dos caminos:

1. **Capturas en el README.** Cuatro pantallazos del área de admin cuestan un
   minuto y es lo que va a ver el 90 % de quien pase por el repositorio.
2. **Esta guía**, para quien quiera levantarlo de verdad.

---

## Lo que al repositorio le falta

Aquí hay una trampa que hay que arreglar antes de escribir ninguna guía, y que
solo se nota al montar una base nueva: **las migraciones no bastan**. Dan por
hecho que ya existen cosas que nunca creó ninguna de ellas, porque se hicieron
a mano en el panel de Supabase antes de que el proyecto tuviera migraciones:

- la tabla **`public.profiles`** y el tipo **`user_role`**, que usan como clave
  foránea `asistencia`, `asistencia_registros` y `disciplina`;
- la función **`public.is_teacher()`**, que aparece **34 veces** en 9 de las 12
  migraciones: es la que decide, en cada política de RLS, quién es docente;
- los disparadores de `auth.users` que crean el perfil al registrarse alguien,
  incluidas las sesiones anónimas de los estudiantes.

Sobre una base nueva, `npm run db:migrar` revienta en `0001` con
`function public.is_teacher() does not exist`.

**Hay que crear `asistente-aula/migraciones/0000_base.sql` con esto.** El `0000`
no es decorativo: `migrar.ts` ordena los archivos por nombre y los aplica en
ese orden, así que es lo primero que corre. Está sacado de la base real, tal
como está hoy, y es idempotente como exigen las demás:

```sql
-- ═══════════════════════════════════════════════════════════════════════
--  El suelo: lo que las demás migraciones dan por hecho
--
--  `profiles`, el tipo de su rol, `is_teacher()` y los disparadores que
--  crean el perfil al registrarse alguien existían antes de que esto
--  tuviera migraciones, hechos a mano en el panel. Sobre una base nueva
--  nada de lo que viene después se puede aplicar sin ellos.
-- ═══════════════════════════════════════════════════════════════════════

do $$ begin
  create type public.user_role as enum ('estudiante', 'docente');
exception when duplicate_object then null; end $$;

create table if not exists public.profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  display_name  text        not null default 'Invitado',
  avatar_emoji  text        not null default '🙂',
  role          public.user_role not null default 'estudiante',
  grupo         text,
  is_guest      boolean     not null default false,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

alter table public.profiles enable row level security;

-- Quién es docente. La respuesta a esta pregunta es toda la seguridad del
-- proyecto: nueve migraciones la hacen 34 veces.
create or replace function public.is_teacher()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.profiles where id = auth.uid() and role = 'docente');
$$;

drop policy if exists "perfil propio: leer" on public.profiles;
create policy "perfil propio: leer" on public.profiles
  for select using (auth.uid() = id or public.is_teacher());

drop policy if exists "perfil propio: actualizar" on public.profiles;
create policy "perfil propio: actualizar" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);

-- El perfil nace con la cuenta. Las sesiones anónimas —cómo entra un
-- estudiante a la sala— pasan por aquí igual que las de correo.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, display_name, avatar_emoji, is_guest)
  values (
    new.id,
    coalesce(
      nullif(new.raw_user_meta_data->>'display_name', ''),
      case when coalesce(new.is_anonymous, false)
           then 'Invitado ' || upper(substr(replace(new.id::text, '-', ''), 1, 4))
           else split_part(coalesce(new.email, 'estudiante'), '@', 1)
      end
    ),
    coalesce(nullif(new.raw_user_meta_data->>'avatar_emoji', ''), '🙂'),
    coalesce(new.is_anonymous, false)
  )
  on conflict (id) do nothing;
  return new;
end $$;

create or replace function public.handle_user_updated()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  update public.profiles
     set is_guest = coalesce(new.is_anonymous, false), updated_at = now()
   where id = new.id;
  return new;
end $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

drop trigger if exists on_auth_user_updated on auth.users;
create trigger on_auth_user_updated after update of is_anonymous, email on auth.users
  for each row execute function public.handle_user_updated();
```

Compruébalo contra una base nueva antes de darlo por bueno. Es la única parte
de esta guía que no está rodada: todo lo demás lleva un curso entero funcionando.

---

## Los pasos

### 1 · Un proyecto de Supabase

[supabase.com](https://supabase.com) → **New project**. El plan gratuito sobra.
Elige la región más cercana y guarda la contraseña de la base, aunque esta app
no la use.

### 2 · `.env.local`

`cp .env.example .env.local` y se rellena. De dónde sale cada valor:

| Variable | Dónde está | Para qué |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project Settings → API → *Project URL* | La app, en el navegador y en el servidor |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Project Settings → API → *anon public* | Lo mismo. Es pública a propósito: lo que protege es la RLS, no la clave |
| `SUPABASE_URL` | La misma de arriba | Solo los scripts de `scripts/` |
| `SUPABASE_SERVICE_ROLE_KEY` | Project Settings → API → *service_role* | **Se salta toda la RLS.** Solo scripts, en tu máquina |
| `SUPABASE_ACCESS_TOKEN` | [Account → Access Tokens](https://supabase.com/dashboard/account/tokens) | Solo `npm run db:migrar`. Caduca: si dice `Invalid access token`, se regenera |
| `SUPABASE_PROJECT_REF` | El trozo del medio de la URL: `https://XXXX.supabase.co` | Lo mismo |
| `ASISTENTE_DOCENTE_NOMBRE` | Lo que quieras | El nombre que sale en la barra del admin |
| `ASISTENTE_CLAVE` | Lo que quieras, o vacío | La contraseña del docente. Vacía, se genera una al azar y se imprime |

**En Vercel van dos, y solo dos:** `NEXT_PUBLIC_SUPABASE_URL` y
`NEXT_PUBLIC_SUPABASE_ANON_KEY`. La `service_role` y el token de
administración saltan la RLS entera: en un despliegue no pintan nada.

> `.env.example` va sin valores: solo los nombres de las variables. Rellénalos
> en tu `.env.local` con los datos de **tu** proyecto de Supabase.

### 3 · El esquema

```sh
cd asistente-aula
npm install
npm run db:migrar
```

Aplica los trece archivos de `migraciones/` en orden, `0000` primero. **Los
reaplica todos en cada pasada**, así que cada uno es idempotente —`if not
exists`, `create or replace`, `drop policy if exists`— y correrlo dos veces no
rompe nada. Si uno falla, para ahí y dice cuál.

Qué queda montado: asistencia y sus registros, el área de admin y la clave del
mando, el diagnóstico, la sala, `lista` (el padrón), los enlaces, `notas`, la
clase en vivo con sus funciones, el taller, la disciplina y la nota a mano.

### 4 · El docente

```sh
npm run docente:crear -- tu@correo.com
```

Crea la cuenta en `auth.users`, le pone perfil con `role='docente'` —sin eso,
`is_teacher()` dice que no y el área de admin te rebota— y deja escrita la
clave del mando. Si no pusiste `ASISTENTE_CLAVE`, imprime una al azar: cópiala,
no se vuelve a enseñar.

### 5 · Datos para que se vea algo

Con la base vacía, `/admin` funciona pero está todo a cero. Hay dos scripts
hechos:

- `npm run listas:cargar -- lista.json` sube el padrón (el formato lo produce
  `planificacion/extraer_listas.py` desde los `.docx` de la escuela).
- `npm run notas:semana -- 1` pone la nota de una semana a quien tenga
  asistencia. Es un ensayo si no le pasas `--escribir`.

Para una copia que se enseña, lo que falta es un tercer script —`scripts/
sembrar-ejemplo.ts`— que llene `lista` con **nombres inventados** y les ponga
asistencia y notas de unas pocas semanas. Con 25 nombres falsos en dos
secciones, el área de admin se ve exactamente como se ve en el aula. Ninguno
de los dos scripts de arriba sirve para eso: uno quiere los documentos de la
escuela y el otro necesita asistencia previa.

### 6 · Arrancar

```sh
npm run dev          # http://localhost:3000
```

`/entrar` con el correo y la clave del paso 4.

---

## Si algo falla

| Lo que dice | Qué pasa |
|---|---|
| `function public.is_teacher() does not exist` | Falta `0000_base.sql`. Arriba está |
| `Invalid access token` en `db:migrar` | El token caducó. Se regenera en la página de tokens |
| Entras pero `/admin` te devuelve a la portada | La cuenta no tiene perfil con `role='docente'`: `npm run docente:crear` |
| `/admin` sale vacío y sin errores | Es la RLS haciendo su trabajo con una sesión que no es docente. No subas la `service_role` para «arreglarlo» |
| `supabaseUrl is required` | Falta `.env.local`, o lo creaste con el servidor ya levantado: reinícialo |

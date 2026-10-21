-- ═══════════════════════════════════════════════════════════════════════
--  Diagnóstico de entrada
--
--  Lo que responden los estudiantes en la primera clase: qué aparato tienen,
--  para qué lo usan, si en casa alguien mira, si distinguen un video real de
--  uno fabricado. No mide programación; mide con qué llegan.
--
--  ─── La asimetría es el diseño ───
--  El estudiante escribe sin haber iniciado sesión: escanea un QR proyectado y
--  responde. Así que la política de alta es para `anon`. La de lectura no: solo
--  un docente autenticado ve una sola fila, la suya incluida. Un estudiante no
--  puede leer lo que puso su compañero ni lo que puso él mismo, y eso lo
--  garantiza la base, no el formulario.
--
--  El precio de que no haya sesión es que cualquiera con la dirección puede
--  enviar una respuesta. La RLS no arregla eso y no pretende hacerlo; se acota
--  con lo barato —la sección tiene que ser una de las nueve, los textos van
--  limitados— y la página no se indexa. Si algún día aparece basura, el paso
--  siguiente es un código de sala que se proyecta en la diapositiva.
--
--  ─── Por qué jsonb y no veinte columnas ───
--  Las preguntas van a cambiar en cuanto se dé la primera clase. Una columna
--  por opción convierte cada retoque del temario en una migración, y el
--  temario vive en contenido.py, que se edita sin pedir permiso a nadie.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.diagnostico (
  id         uuid primary key default gen_random_uuid(),
  creado_en  timestamptz not null default now(),
  nombre     text not null check (length(btrim(nombre)) between 2 and 60),
  seccion    text not null check (seccion in (
               '1ro A','1ro B','1ro C',
               '2do A','2do B','2do C',
               '3ro A','3ro B','3ro C')),
  respuestas jsonb not null default '{}'::jsonb
);

-- Se consulta siempre por sección y por fecha: es como se mira un grupo.
create index if not exists diagnostico_seccion_idx
  on public.diagnostico (seccion, creado_en desc);

alter table public.diagnostico enable row level security;

-- Alta: el estudiante no tiene sesión. `with check (true)` porque lo que se
-- puede escribir ya lo limitan las restricciones de la tabla, y repetirlo aquí
-- sería tener la misma regla en dos sitios que se pueden desincronizar.
drop policy if exists diagnostico_alta on public.diagnostico;
create policy diagnostico_alta on public.diagnostico
  for insert to anon, authenticated
  with check (true);

-- Lectura y todo lo demás: solo docente. `is_teacher()` viene de 0001 y es la
-- misma que decide quién ve la asistencia; si algún día cambia, cambia para
-- todo a la vez, que es justo lo que se buscaba al dejar una sola función.
drop policy if exists diagnostico_docente on public.diagnostico;
create policy diagnostico_docente on public.diagnostico
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

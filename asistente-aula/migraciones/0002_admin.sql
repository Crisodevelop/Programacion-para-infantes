-- ═══════════════════════════════════════════════════════════════════════
--  Área de administración: identidad real y clave de emparejamiento
--
--  ─── Un duplicado que hay que deshacer ───
--  La migración 0001 creó `es_docente()` sin mirar lo que ya había. Pero
--  `is_teacher()` existía desde antes, es idéntica palabra por palabra, y es
--  la que usa la política de `profiles`. Dos funciones con la misma lógica
--  aguantan hasta que alguien corrige una sola: a partir de ahí, quién puede
--  leer la asistencia y quién puede leer los perfiles dejan de coincidir sin
--  que nadie lo note. Se deja una.
--
--  ─── Por qué la clave del mando baja a la base ───
--  Vivía en `.env.local`, así que rotarla exigía editar un archivo y
--  reiniciar el servidor en mitad de la jornada. Si un teléfono se pierde,
--  eso no sirve: hay que poder invalidarlo desde el área de administración
--  en el momento. En la base se rota con un update.
-- ═══════════════════════════════════════════════════════════════════════


-- ─── Una sola función de rol ────────────────────────────────────────────

drop policy if exists asistencia_docente           on public.asistencia;
drop policy if exists asistencia_registros_docente on public.asistencia_registros;
drop function if exists public.es_docente();

create policy asistencia_docente on public.asistencia
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

create policy asistencia_registros_docente on public.asistencia_registros
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());


-- ─── Ajustes del asistente ──────────────────────────────────────────────
--  Una sola fila, siempre. El `check (id = 1)` lo garantiza: sin él, una
--  segunda fila crearía dos claves válidas y nadie sabría cuál manda.

create table if not exists public.asistente_ajustes (
  id          int primary key default 1 check (id = 1),
  clave_mando text not null,
  rotada_en   timestamptz not null default now()
);

alter table public.asistente_ajustes enable row level security;

drop policy if exists ajustes_docente on public.asistente_ajustes;
create policy ajustes_docente on public.asistente_ajustes
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

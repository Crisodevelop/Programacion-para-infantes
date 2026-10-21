-- ═══════════════════════════════════════════════════════════════════════
--  Notas de clase
--
--  Cada presentación de semana suma una nota sobre 100: el primer intento de
--  cada reto y los juegos resueltos. Al final el estudiante escribe su nombre,
--  elige su sección y la guarda. Se lee en /admin/notas.
--
--  ─── La misma asimetría que el diagnóstico ───
--  El estudiante no inicia sesión, así que el alta es para `anon`. Leer, no:
--  solo el docente. Un estudiante no puede ver la nota de otro ni la suya una
--  vez enviada, y eso lo garantiza la base, no la diapositiva.
--
--  Sin sesión, cualquiera con la dirección puede enviar una fila. Se acota con
--  lo barato —la sección tiene que ser una de las nueve, la nota entre 0 y 100,
--  la semana entre 1 y 12— y el panel marca a quien envió dos veces.
--
--  ─── Por qué el desglose va en jsonb ───
--  Qué puntúa cambia de una semana a otra (hay semanas con retos extra, otras
--  con dos juegos). Una columna por actividad sería una migración por cada
--  retoque del temario, que vive en contenido.py.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.notas (
  id         uuid primary key default gen_random_uuid(),
  creado_en  timestamptz not null default now(),
  nombre     text not null check (length(btrim(nombre)) between 2 and 60),
  seccion    text not null check (seccion in (
               '1ro A','1ro B','1ro C',
               '2do A','2do B','2do C',
               '3ro A','3ro B','3ro C')),
  nivel      text not null check (nivel in ('1ro','2do','3ro')),
  semana     int  not null check (semana between 1 and 12),
  puntos     int  not null check (puntos between 0 and 100),
  detalle    jsonb not null default '{}'::jsonb,
  -- La sección tiene que ser del grado de la clase: 1ro no entrega en 3ro B.
  constraint notas_seccion_del_nivel check (left(seccion, 3) = nivel)
);

-- Se mira siempre por sección y semana, lo último primero.
create index if not exists notas_seccion_idx
  on public.notas (seccion, semana, creado_en desc);

alter table public.notas enable row level security;

-- Alta: sin sesión. Lo que se puede escribir ya lo limitan las restricciones.
drop policy if exists notas_alta on public.notas;
create policy notas_alta on public.notas
  for insert to anon, authenticated
  with check (true);

-- Lectura y todo lo demás: solo docente, con la misma función que la asistencia.
drop policy if exists notas_docente on public.notas;
create policy notas_docente on public.notas
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

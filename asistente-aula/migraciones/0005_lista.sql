-- ═══════════════════════════════════════════════════════════════════════
--  La lista de clase, y el mando del docente sobre la presentación
--
--  ─── Por qué la asistencia deja de apuntar a `profiles` ───
--  `asistencia_registros.estudiante_id` referenciaba `profiles`, que referencia
--  `auth.users`. Es decir: para pasar lista había que abrirle una cuenta a cada
--  estudiante. Son 256 menores, y el propio script de importación advertía del
--  peso de esa decisión.
--
--  Las dos tablas de asistencia están vacías, así que se corrige ahora y sale
--  gratis: la asistencia apunta a la lista de clase, que es lo que de verdad
--  es —un papel con nombres— y no requiere identidad de nadie. `profiles`
--  se queda para lo que sí necesita cuenta: el docente.
--
--  ─── Por qué los nombres no viajan en la página ───
--  La presentación es pública. Hasta ahora la diapositiva «Quiénes son»
--  incrustaba la lista en el HTML, y con nombres de ejemplo daba igual; con
--  256 menores, no. Aquí no hay ninguna política para `anon`: los nombres solo
--  salen con sesión de docente.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.lista (
  id        uuid primary key default gen_random_uuid(),
  seccion   text not null check (seccion in (
              '1ro A','1ro B','1ro C',
              '2do A','2do B','2do C',
              '3ro A','3ro B','3ro C')),
  apellidos text not null,
  nombres   text not null,
  -- «Nombres Apellidos»: los documentos vienen al revés, que es como se
  -- archiva y no como se llama a nadie en un aula.
  nombre    text not null check (length(btrim(nombre)) between 2 and 90),
  sexo      text check (sexo in ('F','M')),
  nuevo     boolean not null default false,   -- viene marcado como nuevo ingreso
  agregado  boolean not null default false,   -- lo metió el docente en clase
  activo    boolean not null default true,
  creado_en timestamptz not null default now()
);

-- Un estudiante repetido en la lista es peor que uno que falta: aparece dos
-- veces al pasar lista y nadie sabe cuál marcar.
create unique index if not exists lista_unico
  on public.lista (seccion, lower(nombre));
create index if not exists lista_seccion_idx
  on public.lista (seccion, nombre);

alter table public.lista enable row level security;

drop policy if exists lista_docente on public.lista;
create policy lista_docente on public.lista
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());


-- ─── La asistencia pasa a apuntar a la lista ────────────────────────────
--  El migrador reaplica todos los archivos en cada pasada, así que esto tiene
--  que poder correr mil veces. Y la guarda sigue haciendo falta: en una base
--  con listas ya pasadas, cambiar la clave foránea a ciegas dejaría registros
--  apuntando a un sitio que no existe.
--
--  Se comprueba primero si el cambio ya está hecho —entonces no hay nada que
--  hacer— y solo si no lo está se exige que no haya datos que perder.
do $$
declare v_apunta text;
begin
  select confrelid::regclass::text into v_apunta
    from pg_constraint
   where conname = 'asistencia_registros_estudiante_id_fkey';

  if v_apunta = 'lista' then
    return;                       -- ya apunta donde debe
  end if;

  if exists (select 1 from public.asistencia_registros) then
    raise exception 'asistencia_registros tiene filas: migrar a mano antes de cambiar la clave foránea';
  end if;

  alter table public.asistencia_registros
    drop constraint if exists asistencia_registros_estudiante_id_fkey;
  alter table public.asistencia_registros
    add constraint asistencia_registros_estudiante_id_fkey
    foreign key (estudiante_id) references public.lista(id) on delete cascade;
end $$;


-- ═══════════════════════════════════════════════════════════════════════
--  El estado de la presentación: dos interruptores del docente
--
--  Sirven para parar a treinta personas a la vez mientras se explica algo.
--  Una sola fila, como `asistente_ajustes`: sin el `check (id = 1)`, una
--  segunda fila daría dos estados válidos y nadie sabría cuál manda.
--
--  Aquí sí hay lectura para `anon`, y es deliberado: son dos booleanos sin
--  nada que proteger, y el estudiante tiene que poder enterarse de que la
--  presentación está cerrada sin haber iniciado sesión.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.presentacion_estado (
  id             int primary key default 1 check (id = 1),
  juegos         boolean not null default true,   -- se puede jugar
  abierta        boolean not null default true,   -- se puede ver
  actualizado_en timestamptz not null default now()
);

insert into public.presentacion_estado (id) values (1)
on conflict (id) do nothing;

alter table public.presentacion_estado enable row level security;

drop policy if exists estado_lectura on public.presentacion_estado;
create policy estado_lectura on public.presentacion_estado
  for select to anon, authenticated
  using (true);

drop policy if exists estado_docente on public.presentacion_estado;
create policy estado_docente on public.presentacion_estado
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

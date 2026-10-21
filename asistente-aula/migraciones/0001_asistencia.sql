-- ═══════════════════════════════════════════════════════════════════════
--  Asistencia dictada por voz
--
--  En «Clases» los estudiantes son filas de `profiles` con role='estudiante'
--  y un campo `grupo` de texto. No hay tabla de grupos, así que la asistencia
--  se ancla al mismo texto que ya usa el resto de la aplicación.
--
--  Dos tablas y no una: la cabecera dice que ESE grupo pasó lista ESE día
--  —que es un hecho por sí mismo, y distinto de «nadie faltó»— y los
--  registros dicen qué pasó con cada estudiante. Con una sola tabla no se
--  puede distinguir un día sin ausencias de un día en que no se pasó lista.
--
--  `unique (grupo, fecha)` es deliberado: si se pasa lista dos veces el mismo
--  día porque la primera salió mal, la segunda CORRIGE. Un historial con dos
--  listas contradictorias del mismo día no le sirve a nadie.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.asistencia (
  id          uuid primary key default gen_random_uuid(),
  grupo       text not null,
  fecha       date not null,
  docente_id  uuid references public.profiles(id) on delete set null,
  cerrada_en  timestamptz,
  nota        text,
  created_at  timestamptz not null default now(),
  unique (grupo, fecha)
);

create table if not exists public.asistencia_registros (
  asistencia_id uuid not null references public.asistencia(id) on delete cascade,
  estudiante_id uuid not null references public.profiles(id) on delete cascade,
  estado        text not null default 'presente'
                check (estado in ('presente','ausente','tarde','excusa')),
  nota          text,
  primary key (asistencia_id, estudiante_id)
);

create index if not exists asistencia_grupo_fecha_idx
  on public.asistencia (grupo, fecha desc);
create index if not exists asistencia_registros_estudiante_idx
  on public.asistencia_registros (estudiante_id);


-- ─── Quién puede ver esto ───────────────────────────────────────────────
--  Solo docentes. Un estudiante autenticado en el sitio de Clases no tiene
--  por qué poder consultar quién faltó hoy: es información de sus compañeros.
--  El asistente entra con la clave de servicio y no pasa por estas políticas.

alter table public.asistencia            enable row level security;
alter table public.asistencia_registros  enable row level security;

create or replace function public.es_docente()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'docente'
  );
$$;

drop policy if exists asistencia_docente on public.asistencia;
create policy asistencia_docente on public.asistencia
  for all to authenticated
  using (public.es_docente()) with check (public.es_docente());

drop policy if exists asistencia_registros_docente on public.asistencia_registros;
create policy asistencia_registros_docente on public.asistencia_registros
  for all to authenticated
  using (public.es_docente()) with check (public.es_docente());

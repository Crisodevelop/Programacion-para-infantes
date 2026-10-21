-- ═══════════════════════════════════════════════════════════════════════
--  El código de un taller, paso a paso
--
--  En la sesión del botón de Makers Space los estudiantes escriben el código
--  ellos: ven la meta, no la solución. El docente, desde su presentación,
--  abre el código de un paso cuando ya lo intentaron. Cada fila es un paso
--  abierto un día; al día siguiente todo vuelve a empezar cerrado.
--
--  La tabla es solo del docente. El estudiante pregunta por
--  `taller_abiertos`, que dice qué pasos están abiertos hoy y nada más; el
--  código en sí lo entrega la app (/api/taller/...), que lo lee de su propio
--  disco y filtra con esta lista.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.taller_acceso (
  sesion     text not null check (sesion ~ '^[a-z]+-[0-9]{1,2}$'),
  paso       text not null check (paso ~ '^[0-9]{1,2}-[0-9]{1,2}$'),
  fecha      date not null default public.hoy_aula(),
  abierto_en timestamptz not null default now(),
  primary key (sesion, paso, fecha)
);

alter table public.taller_acceso enable row level security;

drop policy if exists taller_acceso_docente on public.taller_acceso;
create policy taller_acceso_docente on public.taller_acceso
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

-- Qué pasos de una sesión están abiertos hoy.
create or replace function public.taller_abiertos(p_sesion text)
returns text[]
language sql
stable
security definer
set search_path = public
as $$
  select coalesce(array_agg(paso order by paso), '{}')
    from public.taller_acceso
   where sesion = p_sesion and fecha = public.hoy_aula();
$$;

-- Abrir o cerrar un paso. Solo el docente.
create or replace function public.taller_dar(p_sesion text, p_paso text, p_abrir boolean)
returns text[]
language plpgsql
security definer
set search_path = public
as $$
begin
  if not public.is_teacher() then
    raise exception 'solo_docente' using errcode = 'P0001';
  end if;
  if p_abrir then
    insert into public.taller_acceso (sesion, paso) values (p_sesion, p_paso)
    on conflict do nothing;
  else
    delete from public.taller_acceso
     where sesion = p_sesion and paso = p_paso and fecha = public.hoy_aula();
  end if;
  return public.taller_abiertos(p_sesion);
end;
$$;

revoke all on function public.taller_abiertos(text) from public;
revoke all on function public.taller_dar(text, text, boolean) from public, anon;
grant execute on function public.taller_abiertos(text) to anon, authenticated;
grant execute on function public.taller_dar(text, text, boolean) to authenticated;

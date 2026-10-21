-- ═══════════════════════════════════════════════════════════════════════
--  Bloquear a un estudiante durante la clase
--
--  Desde «Clase en vivo» el docente pone en pausa la pantalla de quien está
--  haciendo algo que no debe. La presentación del estudiante lo ve al volver a
--  preguntar por su entrada (cada pocos segundos) y se tapa entera. Mientras
--  dura, la base no le guarda nota: aunque alguien quitara la pantalla desde
--  el inspector, no sumaría nada.
-- ═══════════════════════════════════════════════════════════════════════

alter table public.clase_entrada
  add column if not exists bloqueado boolean not null default false;

-- La ficha que recibe el navegador del estudiante ahora dice si está en pausa.
create or replace function public.clase_ficha(p_entrada uuid, p_semana int)
returns json
language sql
stable
security definer
set search_path = public
as $$
  select json_build_object(
    'token', e.token, 'entrada', e.id, 'seccion', e.seccion, 'nombre', l.nombre,
    'bloqueado', e.bloqueado,
    'detalle', coalesce(n.detalle, '{}'::jsonb), 'codigo', n.codigo)
    from public.clase_entrada e
    join public.lista l on l.id = e.estudiante_id
    left join public.notas n
      on n.estudiante_id = e.estudiante_id and n.fecha = e.fecha and n.semana = p_semana
   where e.id = p_entrada;
$$;

-- Guardar la nota, igual que antes, salvo que esté en pausa.
create or replace function public.clase_nota(p_token uuid, p_semana int, p_detalle jsonb, p_codigo text)
returns json
language plpgsql
security definer
set search_path = public
as $$
declare
  e public.clase_entrada;
  v_nombre text;
  v_antes jsonb;
  v_detalle jsonb;
  v_puntos int;
begin
  select * into e from public.clase_entrada where token = p_token and fecha = public.hoy_aula();
  if e.id is null then
    raise exception 'desmarcado' using errcode = 'P0001';
  end if;
  if e.bloqueado then
    raise exception 'bloqueado' using errcode = 'P0001';
  end if;
  if p_semana is null or p_semana < 1 or p_semana > 12 then
    raise exception 'semana_invalida' using errcode = 'P0001';
  end if;
  if jsonb_typeof(coalesce(p_detalle, '{}'::jsonb)) <> 'object' then
    raise exception 'detalle_invalido' using errcode = 'P0001';
  end if;

  select detalle into v_antes from public.notas
   where estudiante_id = e.estudiante_id and fecha = e.fecha and semana = p_semana;

  select coalesce(jsonb_object_agg(k, v), '{}'::jsonb) into v_detalle
    from jsonb_each(coalesce(p_detalle, '{}'::jsonb)) as t(k, v)
   where jsonb_typeof(v) = 'number' and (v::text)::numeric between 0 and 100
     and length(k) <= 20;
  v_detalle := v_detalle || coalesce(v_antes, '{}'::jsonb);

  select least(100, coalesce(sum((v::text)::numeric), 0))::int into v_puntos
    from jsonb_each(v_detalle) as t(k, v);

  select left(nombre, 60) into v_nombre from public.lista where id = e.estudiante_id;

  insert into public.notas (nombre, seccion, nivel, semana, puntos, detalle, estudiante_id, fecha, codigo)
  values (v_nombre, e.seccion, left(e.seccion, 3), p_semana, v_puntos, v_detalle,
          e.estudiante_id, e.fecha, left(p_codigo, 20000))
  on conflict (estudiante_id, fecha, semana) do update
     set puntos = excluded.puntos,
         detalle = excluded.detalle,
         codigo = coalesce(excluded.codigo, public.notas.codigo),
         actualizado_en = now();

  return json_build_object('puntos', v_puntos, 'detalle', v_detalle);
end;
$$;

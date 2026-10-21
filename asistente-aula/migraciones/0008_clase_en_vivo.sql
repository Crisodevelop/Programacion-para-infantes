-- ═══════════════════════════════════════════════════════════════════════
--  Clase en vivo
--
--  El docente abre la clase de una sección. A los estudiantes de ese grado les
--  aparece una ventana con la lista de su sección: tocan su nombre y quedan
--  presentes. Desde ahí, su nota se guarda sola mientras avanzan.
--
--  ─── La misma asimetría que la sala del diagnóstico ───
--  Las tablas solo las lee y escribe el docente. El estudiante no tiene sesión:
--  entra por funciones `security definer`, que son la única puerta y deciden
--  qué puede hacer. Cada entrada lleva un token secreto que se queda en su
--  navegador; con él, y solo con él, puede guardar su nota.
--
--  ─── Lo que ya está en la base manda ───
--  El primer intento de cada reto se guarda. Si el navegador vuelve a mandar
--  ese reto con otro valor —porque borró su historial o cambió de PC—, gana el
--  que ya estaba. Así un reto fallado no vuelve a sumar por ningún camino.
-- ═══════════════════════════════════════════════════════════════════════

-- La fecha del aula, no la del servidor (UTC).
create or replace function public.hoy_aula()
returns date
language sql
stable
as $$ select (now() at time zone 'America/Santo_Domingo')::date $$;

-- ─── La sala: el docente decide cuándo empieza ───────────────────────────
create table if not exists public.clase_sala (
  seccion        text primary key check (seccion in (
                   '1ro A','1ro B','1ro C',
                   '2do A','2do B','2do C',
                   '3ro A','3ro B','3ro C')),
  abierta        boolean not null default false,
  fecha          date,
  actualizado_en timestamptz not null default now()
);

insert into public.clase_sala (seccion) values
  ('1ro A'),('1ro B'),('1ro C'),
  ('2do A'),('2do B'),('2do C'),
  ('3ro A'),('3ro B'),('3ro C')
on conflict (seccion) do nothing;

-- ─── Quién eligió qué nombre hoy ─────────────────────────────────────────
create table if not exists public.clase_entrada (
  id            uuid primary key default gen_random_uuid(),
  token         uuid not null unique default gen_random_uuid(),
  seccion       text not null references public.clase_sala(seccion) on delete cascade,
  fecha         date not null default public.hoy_aula(),
  estudiante_id uuid not null references public.lista(id) on delete cascade,
  entro_en      timestamptz not null default now(),
  unique (fecha, estudiante_id)
);

create index if not exists clase_entrada_sala_idx
  on public.clase_entrada (seccion, fecha);

-- ─── Las notas pasan a ser de alguien de la lista ────────────────────────
-- La tabla está vacía: se amplía en su sitio.
alter table public.notas add column if not exists estudiante_id uuid
  references public.lista(id) on delete cascade;
alter table public.notas add column if not exists fecha date not null default public.hoy_aula();
alter table public.notas add column if not exists codigo text
  check (codigo is null or length(codigo) <= 20000);
alter table public.notas add column if not exists actualizado_en timestamptz not null default now();

create unique index if not exists notas_una_por_clase
  on public.notas (estudiante_id, fecha, semana);

-- Se acaba el alta anónima directa: ahora solo se escribe por clase_nota().
drop policy if exists notas_alta on public.notas;

alter table public.clase_sala    enable row level security;
alter table public.clase_entrada enable row level security;

drop policy if exists clase_sala_docente on public.clase_sala;
create policy clase_sala_docente on public.clase_sala
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

drop policy if exists clase_entrada_docente on public.clase_entrada;
create policy clase_entrada_docente on public.clase_entrada
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());


-- ═══ Las puertas del estudiante ══════════════════════════════════════════

-- Qué secciones de un grado están abiertas hoy.
create or replace function public.clase_abiertas(p_nivel text)
returns table (seccion text)
language sql
stable
security definer
set search_path = public
as $$
  select s.seccion from public.clase_sala s
   where s.abierta and s.fecha = public.hoy_aula() and left(s.seccion, 3) = p_nivel
   order by s.seccion;
$$;

-- La lista de una sección, solo mientras su clase está abierta.
create or replace function public.clase_lista(p_seccion text)
returns table (id uuid, nombre text, tomado boolean)
language sql
stable
security definer
set search_path = public
as $$
  select l.id, l.nombre,
         exists (select 1 from public.clase_entrada e
                  where e.estudiante_id = l.id and e.fecha = public.hoy_aula())
    from public.lista l
   where l.seccion = p_seccion and l.activo
     and exists (select 1 from public.clase_sala s
                  where s.seccion = p_seccion and s.abierta and s.fecha = public.hoy_aula())
   order by l.apellidos, l.nombres;
$$;

-- Lo que se devuelve al entrar o al volver: quién es y lo que ya llevaba.
create or replace function public.clase_ficha(p_entrada uuid, p_semana int)
returns json
language sql
stable
security definer
set search_path = public
as $$
  select json_build_object(
    'token', e.token, 'entrada', e.id, 'seccion', e.seccion, 'nombre', l.nombre,
    'detalle', coalesce(n.detalle, '{}'::jsonb), 'codigo', n.codigo)
    from public.clase_entrada e
    join public.lista l on l.id = e.estudiante_id
    left join public.notas n
      on n.estudiante_id = e.estudiante_id and n.fecha = e.fecha and n.semana = p_semana
   where e.id = p_entrada;
$$;

-- Tocar su nombre: queda dentro y presente.
create or replace function public.clase_entrar(p_seccion text, p_estudiante uuid, p_semana int)
returns json
language plpgsql
security definer
set search_path = public
as $$
declare
  v_hoy date := public.hoy_aula();
  v_entrada uuid;
  v_asistencia uuid;
begin
  if not exists (select 1 from public.clase_sala
                  where seccion = p_seccion and abierta and fecha = v_hoy) then
    raise exception 'sala_cerrada' using errcode = 'P0001';
  end if;
  if not exists (select 1 from public.lista
                  where id = p_estudiante and seccion = p_seccion and activo) then
    raise exception 'estudiante_desconocido' using errcode = 'P0001';
  end if;

  begin
    insert into public.clase_entrada (seccion, fecha, estudiante_id)
    values (p_seccion, v_hoy, p_estudiante)
    returning id into v_entrada;
  exception when unique_violation then
    -- Otro ya eligió ese nombre hoy. Si era suyo, el docente lo desmarca.
    raise exception 'nombre_tomado' using errcode = 'P0001';
  end;

  -- La asistencia de hoy, la misma que usa «Pasar lista». No pisa lo que el
  -- docente ya haya marcado (tarde, excusa).
  insert into public.asistencia (grupo, fecha)
  values (p_seccion, v_hoy)
  on conflict (grupo, fecha) do nothing;
  select id into v_asistencia from public.asistencia where grupo = p_seccion and fecha = v_hoy;
  insert into public.asistencia_registros (asistencia_id, estudiante_id, estado, nota)
  values (v_asistencia, p_estudiante, 'presente', 'entró solo')
  on conflict (asistencia_id, estudiante_id) do nothing;

  return public.clase_ficha(v_entrada, p_semana);
end;
$$;

-- Recargar: con el token de su navegador vuelve a ser quien era, sin elegir.
create or replace function public.clase_volver(p_token uuid, p_semana int)
returns json
language sql
stable
security definer
set search_path = public
as $$
  select public.clase_ficha(e.id, p_semana)
    from public.clase_entrada e
   where e.token = p_token and e.fecha = public.hoy_aula();
$$;

-- Guardar la nota. Lo que ya estaba manda; la nota se recalcula y no pasa de 100.
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
  if p_semana is null or p_semana < 1 or p_semana > 12 then
    raise exception 'semana_invalida' using errcode = 'P0001';
  end if;
  if jsonb_typeof(coalesce(p_detalle, '{}'::jsonb)) <> 'object' then
    raise exception 'detalle_invalido' using errcode = 'P0001';
  end if;

  select detalle into v_antes from public.notas
   where estudiante_id = e.estudiante_id and fecha = e.fecha and semana = p_semana;

  -- Solo valores enteros de 0 a 100; lo que ya estaba gana a lo que llega.
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


-- ═══ La puerta del docente ═══════════════════════════════════════════════

-- Desmarcar a quien eligió el nombre equivocado: el nombre queda libre y se
-- borra lo que se había puesto solo (la entrada, su nota de hoy y el presente
-- que marcó al entrar). Lo que el docente marcó a mano no se toca.
create or replace function public.clase_desmarcar(p_entrada uuid)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  e public.clase_entrada;
begin
  if not public.is_teacher() then
    raise exception 'solo_docente' using errcode = '42501';
  end if;
  select * into e from public.clase_entrada where id = p_entrada;
  if e.id is null then
    return;
  end if;
  delete from public.notas where estudiante_id = e.estudiante_id and fecha = e.fecha;
  delete from public.asistencia_registros r
   using public.asistencia a
   where r.asistencia_id = a.id and a.grupo = e.seccion and a.fecha = e.fecha
     and r.estudiante_id = e.estudiante_id and r.nota = 'entró solo';
  delete from public.clase_entrada where id = e.id;
end;
$$;

revoke all on function public.clase_desmarcar(uuid) from anon;

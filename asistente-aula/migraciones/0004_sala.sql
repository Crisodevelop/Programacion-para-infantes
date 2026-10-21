-- ═══════════════════════════════════════════════════════════════════════
--  La sala de espera del diagnóstico
--
--  Antes, el diagnóstico era un formulario suelto: quien escaneaba el QR
--  empezaba a responder. En un aula eso significa que unos van por la pregunta
--  seis mientras otros todavía buscan el enlace, y el docente no sabe si están
--  todos hasta que empiezan a llegar respuestas.
--
--  Ahora hay una sala por sección. El estudiante entra y espera; el docente ve
--  los nombres llegar y decide cuándo se empieza. Solo el arranque: pasado ese
--  momento cada uno responde a su ritmo. Sincronizar las diez preguntas entre
--  treinta teléfonos sería una cosa más que se puede quedar colgada delante de
--  la clase, y no compra nada: el diagnóstico no lleva nota.
--
--  ─── Por qué `anon` no toca estas tablas ───
--  La clave anónima es pública: viaja a todos los teléfonos. Si `anon` tuviera
--  `select` sobre `diagnostico_presente`, cualquiera podría sacar desde la
--  consola la lista de nombres de las nueve secciones del curso entero. Así que
--  las tablas son solo del docente y el estudiante entra por dos funciones
--  `security definer`, que enseñan una sala, y solo mientras está abierta.
--
--  ─── Por qué los nombres salen abreviados ───
--  En la pantalla del estudiante los nombres se ven, como en Kahoot: es lo que
--  hace que valga la pena esperar. Pero son menores en una página pública, así
--  que sale «Ana M.» y no el apellido entero. El docente, que lee la tabla con
--  su sesión, sí ve el nombre completo: lo necesita para hablar con cada uno.
-- ═══════════════════════════════════════════════════════════════════════


-- ─── Las salas ──────────────────────────────────────────────────────────
--  Tres estados y no dos. `espera` y `abierta` parecen lo mismo desde el
--  servidor, pero son justo la distinción que pidió el docente: entrar y
--  empezar son dos momentos distintos, y él manda en el segundo.

create table if not exists public.diagnostico_sala (
  seccion        text primary key check (seccion in (
                   '1ro A','1ro B','1ro C',
                   '2do A','2do B','2do C',
                   '3ro A','3ro B','3ro C')),
  estado         text not null default 'cerrada'
                 check (estado in ('cerrada','espera','abierta')),
  actualizado_en timestamptz not null default now()
);

-- Las nueve filas se siembran aquí. Crearlas en caliente obligaría a que la
-- función de entrada supiera insertar salas, y entonces un nombre de sección
-- mal escrito crearía una sala fantasma en vez de fallar.
insert into public.diagnostico_sala (seccion) values
  ('1ro A'),('1ro B'),('1ro C'),
  ('2do A'),('2do B'),('2do C'),
  ('3ro A'),('3ro B'),('3ro C')
on conflict (seccion) do nothing;


-- ─── Quién está dentro ──────────────────────────────────────────────────

create table if not exists public.diagnostico_presente (
  id       uuid primary key default gen_random_uuid(),
  seccion  text not null references public.diagnostico_sala(seccion) on delete cascade,
  nombre   text not null check (length(btrim(nombre)) between 2 and 60),
  entro_en timestamptz not null default now()
);

create index if not exists diagnostico_presente_sala_idx
  on public.diagnostico_presente (seccion, entro_en);

-- Recargar la página no puede duplicarte en la lista. Se garantiza aquí y no
-- en la función: una comprobación en código tiene una ventana entre el select
-- y el insert, y treinta personas entrando a la vez es exactamente el momento
-- en que esa ventana se abre.
--
-- Se compara en minúsculas porque medio grupo escribe sin mayúsculas. Los
-- espacios sobrantes ya los quita `sala_entrar` antes de insertar, que es
-- donde tiene arreglo: aquí solo se compara lo que se guardó.
drop index if exists public.diagnostico_presente_unico_idx;
create unique index diagnostico_presente_unico_idx
  on public.diagnostico_presente (seccion, lower(nombre));


-- ─── Quién puede ver esto ───────────────────────────────────────────────
--  Solo docente, con `is_teacher()`, igual que la asistencia y los ajustes.
--  Para `anon` no hay ninguna política: ni lectura ni escritura directas.

alter table public.diagnostico_sala      enable row level security;
alter table public.diagnostico_presente  enable row level security;

drop policy if exists sala_docente on public.diagnostico_sala;
create policy sala_docente on public.diagnostico_sala
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

drop policy if exists presente_docente on public.diagnostico_presente;
create policy presente_docente on public.diagnostico_presente
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());


-- ─── El nombre, acortado ────────────────────────────────────────────────
--  «Ana María Pérez» → «Ana M.». Con una sola palabra se deja tal cual.

create or replace function public.nombre_corto(p_nombre text)
returns text
language sql
immutable
as $$
  select case
    when coalesce(array_length(regexp_split_to_array(btrim(p_nombre), '\s+'), 1), 0) > 1
      then initcap((regexp_split_to_array(btrim(p_nombre), '\s+'))[1])
           || ' '
           || upper(left((regexp_split_to_array(btrim(p_nombre), '\s+'))[2], 1))
           || '.'
    else initcap(btrim(p_nombre))
  end;
$$;


-- ─── Entrar en la sala ──────────────────────────────────────────────────
--  `security definer`: se ejecuta con los permisos del dueño, así que salta la
--  RLS. Es toda la superficie que tiene `anon` sobre estas tablas, y por eso
--  comprueba el estado antes de escribir nada.

create or replace function public.sala_entrar(p_seccion text, p_nombre text)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_estado text;
  -- Se normaliza antes de comparar y antes de guardar. Sin esto, «Juan Test»
  -- y «juan   test» son dos personas para el índice único: los espacios de
  -- dentro no los toca `btrim`, y quien escribe en un teléfono mete dobles.
  v_nombre text := regexp_replace(btrim(p_nombre), '\s+', ' ', 'g');
  v_id     uuid;
begin
  select estado into v_estado
    from public.diagnostico_sala where seccion = p_seccion;

  if v_estado is null then
    raise exception 'seccion_desconocida' using errcode = 'P0001';
  end if;
  if v_estado = 'cerrada' then
    raise exception 'sala_cerrada' using errcode = 'P0001';
  end if;
  if length(v_nombre) < 2 or length(v_nombre) > 60 then
    raise exception 'nombre_invalido' using errcode = 'P0001';
  end if;

  -- Un aula no pasa de cuarenta. El tope no protege de un ataque serio; corta
  -- el caso real, que es alguien metiendo nombres inventados por diversión.
  if (select count(*) from public.diagnostico_presente
       where seccion = p_seccion) >= 60 then
    raise exception 'sala_llena' using errcode = 'P0001';
  end if;

  insert into public.diagnostico_presente (seccion, nombre)
  values (p_seccion, v_nombre)
  returning id into v_id;
  return v_id;

exception when unique_violation then
  -- Ya estaba dentro: recargó, o el móvil reintentó. Se devuelve el mismo.
  select id into v_id from public.diagnostico_presente
   where seccion = p_seccion and lower(nombre) = lower(v_nombre);
  return v_id;
end;
$$;


-- ─── Mirar la sala ──────────────────────────────────────────────────────
--  Lo que sondea el teléfono cada tres segundos. Una sola llamada devuelve el
--  estado, el total y los nombres: tres consultas por estudiante y por tick
--  serían tres veces el ruido para la misma información.

create or replace function public.sala_estado(p_seccion text)
returns json
language sql
security definer
stable
set search_path = public
as $$
  with s as (
    select coalesce(
      (select estado from public.diagnostico_sala where seccion = p_seccion),
      'cerrada') as estado
  )
  select json_build_object(
    'estado', s.estado,
    'total',  case when s.estado = 'cerrada' then 0 else
              (select count(*) from public.diagnostico_presente p
                where p.seccion = p_seccion) end,
    -- Con la sala cerrada no se devuelve ni un nombre. Es lo que impide que
    -- alguien recorra las nueve secciones fuera de clase y se lleve la lista.
    'nombres', case when s.estado = 'cerrada' then '[]'::json else
               coalesce((select json_agg(public.nombre_corto(p.nombre)
                                         order by p.entro_en)
                           from public.diagnostico_presente p
                          where p.seccion = p_seccion), '[]'::json) end
  ) from s;
$$;

revoke all on function public.sala_entrar(text, text) from public;
revoke all on function public.sala_estado(text)       from public;
grant execute on function public.sala_entrar(text, text) to anon, authenticated;
grant execute on function public.sala_estado(text)       to anon, authenticated;

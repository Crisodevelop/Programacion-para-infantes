-- ═══════════════════════════════════════════════════════════════════════
--  La disciplina, y poder corregir una nota a mano
--
--  Dos huecos del registro que se arreglan juntos porque tocan lo mismo.
--
--  ─── Por qué la disciplina va en su propia tabla ───
--  Es UNA por estudiante para todo el curso, no una por clase. Meterla en
--  `notas` chocaría con el único `notas_una_por_clase (estudiante_id, fecha,
--  semana)`, obligaría a cambiar el `on conflict` de `clase_nota()` en el
--  mismo movimiento, y `clase_desmarcar()` la borraría al liberar un nombre.
--
--  Y no hay dónde colgarla en el tiempo: no existe periodo ni trimestre, solo
--  semana 1..12 y la fecha del día. Inventar un eje para un número por curso
--  sería inventar trabajo.
--
--  Sin fila = 100. Solo se escribe a quien haya que bajar, que es un puñado
--  de 253: para la mayoría no hay nada que mantener, y nadie hereda un cero
--  por un descuido.
--
--  ─── Por qué `puntos` no bastaba ───
--  El docente ya podía hacer `update` sobre `notas`: la política es `for all`.
--  Lo que no podía era que durase. `puntos` no es un dato, es una suma
--  derivada: `clase_nota()` lo recalcula desde `detalle` en cada escritura del
--  estudiante. Corregías un 70 a 85, el estudiante resolvía una actividad más
--  y el 85 se convertía en 25 sin dejar rastro.
--
--  `puntos_docente` es la marca de autoría que a esta tabla le faltaba —la
--  asistencia ya tiene la suya, `nota = 'entró solo'`— y además guarda el
--  valor. `puntos` sigue siendo la nota que vale, así que todo lo que ya lee
--  esa columna sigue leyendo el número correcto sin enterarse de nada.
-- ═══════════════════════════════════════════════════════════════════════

-- ─── La conducta: una por estudiante, para las 12 semanas ───────────────

create table if not exists public.disciplina (
  estudiante_id  uuid primary key references public.lista(id) on delete cascade,
  puntos         int not null check (puntos between 0 and 100),
  -- El porqué, en una línea. Igual que `asistencia_registros.nota`: dentro de
  -- un mes nadie se acuerda de por qué ese 70.
  nota           text check (nota is null or length(btrim(nota)) <= 200),
  docente_id     uuid references public.profiles(id) on delete set null,
  actualizado_en timestamptz not null default now()
);

alter table public.disciplina enable row level security;

drop policy if exists disciplina_docente on public.disciplina;
create policy disciplina_docente on public.disciplina
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

-- ─── La marca de «esto lo puse yo» ──────────────────────────────────────

alter table public.notas add column if not exists puntos_docente int
  check (puntos_docente is null or puntos_docente between 0 and 100);

-- ─── `clase_nota()`: el desglose sigue, la nota se queda ────────────────
--
--  Cambia una sola línea del `on conflict`, la de `puntos`. El resto del
--  cuerpo es el de 0010 palabra por palabra.
--
--  `detalle` se sigue acumulando a propósito: el estudiante puede seguir
--  trabajando y queda constancia de lo que hizo. Lo que no se mueve es la
--  nota. Es el mismo gesto que la línea de `codigo` justo debajo.

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
     set puntos = coalesce(public.notas.puntos_docente, excluded.puntos),
         detalle = excluded.detalle,
         codigo = coalesce(excluded.codigo, public.notas.codigo),
         actualizado_en = now();

  return json_build_object('puntos', v_puntos, 'detalle', v_detalle);
end;
$$;

-- ─── `clase_desmarcar()`: cumple lo que promete el aviso ────────────────
--
--  Borraba las notas del día sin mirar de dónde venían, pero el aviso que lee
--  el docente antes de pulsar dice «se borra la nota de hoy QUE SE PUSO
--  SOLA». Ahora es verdad: la que pusiste a mano sobrevive a liberar un
--  nombre mal elegido. El resto del cuerpo, igual que en 0008.

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
  delete from public.notas
   where estudiante_id = e.estudiante_id and fecha = e.fecha
     and puntos_docente is null;
  delete from public.asistencia_registros r
   using public.asistencia a
   where r.asistencia_id = a.id and a.grupo = e.seccion and a.fecha = e.fecha
     and r.estudiante_id = e.estudiante_id and r.nota = 'entró solo';
  delete from public.clase_entrada where id = e.id;
end;
$$;

revoke all on function public.clase_desmarcar(uuid) from anon;

-- ═══════════════════════════════════════════════════════════════════════
--  Entrar después de que se pasó la lista
--
--  Al cerrar la clase, el docente puede guardar la lista: los que no eligieron
--  su nombre quedan «ausente». Si después vuelve a abrir y ese estudiante
--  entra, tiene que pasar a presente. Antes, `on conflict do nothing` lo
--  dejaba ausente para siempre.
--
--  Solo se corrige un «ausente». Lo que el docente marcó a mano (tarde,
--  excusa) no se toca.
-- ═══════════════════════════════════════════════════════════════════════

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
    raise exception 'nombre_tomado' using errcode = 'P0001';
  end;

  insert into public.asistencia (grupo, fecha)
  values (p_seccion, v_hoy)
  on conflict (grupo, fecha) do nothing;
  select id into v_asistencia from public.asistencia where grupo = p_seccion and fecha = v_hoy;

  insert into public.asistencia_registros (asistencia_id, estudiante_id, estado, nota)
  values (v_asistencia, p_estudiante, 'presente', 'entró solo')
  on conflict (asistencia_id, estudiante_id) do update
     set estado = 'presente', nota = 'entró solo'
   where public.asistencia_registros.estado = 'ausente';

  return public.clase_ficha(v_entrada, p_semana);
end;
$$;

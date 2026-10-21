"use client";

import { useCallback, useEffect, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { SECCIONES, bloqueActual } from "@/lib/horario";

/**
 * La clase en vivo: abrirla, ver quién entró y desmarcar a quien se equivocó.
 *
 * Todo se lee y se escribe con la sesión del docente; es la RLS la que manda.
 * Abrir una sección cierra las demás: se da una clase a la vez, y así nunca
 * queda abierta la de la hora anterior por olvido.
 */

type Persona = { id: string; nombre: string };
type Entrada = { id: string; estudiante_id: string; entro_en: string; bloqueado: boolean };
type Lista = { cerrada_en: string | null } | null;
type Nota = { estudiante_id: string; puntos: number; semana: number };

const SONDEO = 5_000;

function hoy() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export function ClaseEnVivo() {
  const [seccion, setSeccion] = useState(() => bloqueActual()?.seccion ?? SECCIONES[0]);
  const [abierta, setAbierta] = useState(false);
  const [gente, setGente] = useState<Persona[]>([]);
  const [entradas, setEntradas] = useState<Map<string, Entrada>>(new Map());
  const [notas, setNotas] = useState<Map<string, Nota>>(new Map());
  const [ocupado, setOcupado] = useState(false);
  const [error, setError] = useState("");
  const [cerrando, setCerrando] = useState(false);     // paso de confirmar el cierre
  const [listaHoy, setListaHoy] = useState<Lista>(null);
  const [aviso, setAviso] = useState("");

  const cargar = useCallback(async (sec: string) => {
    const sb = supabaseNavegador();
    const dia = hoy();
    const [sala, lista, ent, nts, asis] = await Promise.all([
      sb.from("clase_sala").select("abierta,fecha").eq("seccion", sec).maybeSingle(),
      sb.from("lista").select("id,nombre").eq("seccion", sec).eq("activo", true).order("apellidos").order("nombres"),
      sb.from("clase_entrada").select("id,estudiante_id,entro_en,bloqueado").eq("seccion", sec).eq("fecha", dia),
      sb.from("notas").select("estudiante_id,puntos,semana").eq("seccion", sec).eq("fecha", dia),
      sb.from("asistencia").select("cerrada_en").eq("grupo", sec).eq("fecha", dia).maybeSingle(),
    ]);
    const e = sala.error ?? lista.error ?? ent.error ?? nts.error;
    setError(e ? `No se pudo leer la clase: ${e.message}` : "");
    setAbierta(!!sala.data?.abierta && sala.data?.fecha === dia);
    setGente((lista.data ?? []) as Persona[]);
    setEntradas(new Map(((ent.data ?? []) as Entrada[]).map((x) => [x.estudiante_id, x])));
    setNotas(new Map(((nts.data ?? []) as Nota[]).map((x) => [x.estudiante_id, x])));
    setListaHoy((asis.data ?? null) as Lista);
  }, []);

  useEffect(() => {
    void cargar(seccion);
    const reloj = setInterval(() => { void cargar(seccion); }, SONDEO);
    return () => clearInterval(reloj);
  }, [cargar, seccion]);

  async function abrir(si: boolean) {
    setOcupado(true);
    const sb = supabaseNavegador();
    const ahora = new Date().toISOString();
    if (si) {
      await sb.from("clase_sala").update({ abierta: false, actualizado_en: ahora }).neq("seccion", seccion);
    }
    const { error: e } = await sb.from("clase_sala")
      .update({ abierta: si, fecha: hoy(), actualizado_en: ahora }).eq("seccion", seccion);
    setOcupado(false);
    if (e) setError(`No se pudo ${si ? "abrir" : "cerrar"} la clase: ${e.message}`);
    await cargar(seccion);
  }

  /**
   * Cerrar y pasar lista: igual que «Pasar lista», la cabecera del día queda a
   * tu nombre y quien no eligió su nombre queda ausente. No pisa lo que ya
   * esté marcado (presente al entrar, o tarde y excusa que pusiste a mano).
   */
  async function cerrarYPasarLista() { await pasarLista(true); }

  async function pasarLista(cerrar: boolean) {
    setOcupado(true);
    setError("");
    const sb = supabaseNavegador();
    const { data: { user } } = await sb.auth.getUser();
    const { data: cab, error: e1 } = await sb.from("asistencia").upsert(
      { grupo: seccion, fecha: hoy(), docente_id: user?.id ?? null, cerrada_en: new Date().toISOString() },
      { onConflict: "grupo,fecha" },
    ).select("id").single();
    if (e1 || !cab) { setOcupado(false); setError(`No se pudo guardar la lista: ${e1?.message}`); return; }

    const faltan = gente.filter((p) => !entradas.has(p.id)).map((p) => ({
      asistencia_id: cab.id as string, estudiante_id: p.id, estado: "ausente",
    }));
    if (faltan.length) {
      const { error: e2 } = await sb.from("asistencia_registros")
        .upsert(faltan, { onConflict: "asistencia_id,estudiante_id", ignoreDuplicates: true });
      if (e2) { setOcupado(false); setError(`No se pudieron guardar los ausentes: ${e2.message}`); return; }
    }
    setCerrando(false);
    if (cerrar) await abrir(false);
    else { setOcupado(false); await cargar(seccion); }
    setAviso(`Lista de ${seccion} guardada: entraron ${gente.length - faltan.length}; los otros ${faltan.length} ` +
             "quedan ausentes, salvo a quien ya hubieras marcado a mano. Para corregir (tarde, excusa), usa Asistencia.");
  }

  async function bloquear(entrada: Entrada, si: boolean) {
    const { error: e } = await supabaseNavegador().from("clase_entrada").update({ bloqueado: si }).eq("id", entrada.id);
    if (e) setError(`No se pudo ${si ? "bloquear" : "desbloquear"}: ${e.message}`);
    await cargar(seccion);
  }

  /**
   * Bloquear o desbloquear a toda la sección de un golpe, que es lo que hace
   * falta cuando hay que parar la clase entera y no a una persona. Solo toca
   * las filas que cambian, y afecta a quien ya entró: si alguien entra después
   * de pausar, entra sin pausa.
   */
  async function bloquearTodos(si: boolean) {
    const cambian = [...entradas.values()].filter((e) => e.bloqueado !== si).length;
    if (!cambian) return;
    setOcupado(true);
    setError("");
    setAviso("");
    const { error: e } = await supabaseNavegador().from("clase_entrada")
      .update({ bloqueado: si }).eq("seccion", seccion).eq("fecha", hoy()).eq("bloqueado", !si);
    setOcupado(false);
    if (e) setError(`No se pudo ${si ? "bloquear" : "desbloquear"} a todos: ${e.message}`);
    else setAviso(si
      ? `${cambian} en pausa: se les tapa la pantalla y no se les guarda nota mientras dure. ` +
        "Tardan unos segundos en verlo, y quien entre después entra sin pausa."
      : `${cambian} de vuelta: pueden seguir con la clase.`);
    await cargar(seccion);
  }

  async function desmarcar(entrada: Entrada, nombre: string) {
    if (!window.confirm(`¿Desmarcar a ${nombre}? Se libera el nombre y se borra la nota de hoy que se puso sola.`)) return;
    const { error: e } = await supabaseNavegador().rpc("clase_desmarcar", { p_entrada: entrada.id });
    if (e) setError(`No se pudo desmarcar: ${e.message}`);
    await cargar(seccion);
  }

  const dentro = gente.filter((p) => entradas.has(p.id)).length;
  const enPausa = [...entradas.values()].filter((e) => e.bloqueado).length;
  const conNota = [...notas.values()];
  const promedio = conNota.length ? Math.round(conNota.reduce((t, n) => t + n.puntos, 0) / conNota.length) : null;

  return (
    <>
      <div style={S.mandos}>
        <label style={S.campo}>
          Sección
          <select value={seccion} onChange={(e) => setSeccion(e.target.value)} style={S.select}>
            {SECCIONES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        <span style={abierta ? S.abierta : S.cerrada}>{abierta ? "● Abierta" : "Cerrada"}</span>
        <button type="button" disabled={ocupado}
                onClick={() => { setAviso(""); if (abierta) setCerrando(true); else void abrir(true); }}
                style={abierta ? S.botonSec : S.boton}>
          {abierta ? "Cerrar clase" : "Abrir clase"}
        </button>
      </div>

      {cerrando && (
        <div style={S.confirmar} role="group" aria-label="Cerrar la clase">
          <p style={S.confTitulo}>
            ¿Cerrar la clase de {seccion}? Entraron {dentro} de {gente.length}.
          </p>
          {gente.length - dentro > 0 ? (
            <p style={S.confTexto}>
              Si pasas la lista, estos {gente.length - dentro} quedan <b>ausentes</b>:{" "}
              {gente.filter((p) => !entradas.has(p.id)).map((p) => p.nombre).join(", ")}.
            </p>
          ) : (
            <p style={S.confTexto}>Entraron todos: la lista queda completa.</p>
          )}
          <div style={S.confAcc}>
            <button type="button" style={S.boton0} disabled={ocupado} onClick={() => void cerrarYPasarLista()}>
              Cerrar y pasar lista
            </button>
            <button type="button" style={S.botonSec0} disabled={ocupado}
                    onClick={() => { setCerrando(false); void abrir(false); }}>
              Solo cerrar
            </button>
            <button type="button" style={S.botonSec0} disabled={ocupado} onClick={() => setCerrando(false)}>
              Cancelar
            </button>
          </div>
        </div>
      )}
      {aviso && <p style={S.aviso}>{aviso}</p>}

      <div style={S.listaHoy}>
        <span>
          <b>Lista de hoy:</b>{" "}
          {listaHoy?.cerrada_en
            ? `guardada a las ${new Date(listaHoy.cerrada_en).toLocaleTimeString("es-DO", { hour: "numeric", minute: "2-digit" })}`
            : "todavía sin pasar"}
        </span>
        <button type="button" style={S.botonSec0} disabled={ocupado || !gente.length}
                onClick={() => { setAviso(""); void pasarLista(false); }}>
          {listaHoy?.cerrada_en ? "Volver a pasar lista" : "Pasar lista"}
        </button>
      </div>
      <p style={S.nota}>
        {abierta
          ? "A los estudiantes de esta sección les sale la ventana para elegir su nombre (tarda hasta 10 segundos)."
          : "Cerrada: la presentación va en modo repaso y no se guarda nota. Al abrir esta, se cierra cualquier otra que siga abierta."}
      </p>

      {error && <p style={S.error}>{error}</p>}

      <div style={S.todos}>
        <span style={S.resumen}>
          {dentro} de {gente.length} entraron{promedio !== null && <> · promedio {promedio} / 100</>}
          {enPausa > 0 && <> · {enPausa} en pausa</>}
        </span>
        <span style={S.acciones}>
          <button type="button" style={S.bloquear} disabled={ocupado || dentro === 0 || enPausa === dentro}
                  onClick={() => void bloquearTodos(true)}>
            ⏸ Bloquear a todos
          </button>
          <button type="button" style={enPausa ? S.desbloquear : S.botonSec0} disabled={ocupado || enPausa === 0}
                  onClick={() => void bloquearTodos(false)}>
            ▶ Desbloquear a todos
          </button>
        </span>
      </div>

      <ul style={S.lista}>
        {gente.map((p) => {
          const e = entradas.get(p.id);
          const n = notas.get(p.id);
          return (
            <li key={p.id} style={e ? S.fila : { ...S.fila, ...S.fuera }}>
              <span style={S.nombre}>{e ? (e.bloqueado ? "⏸ " : "✓ ") : ""}{p.nombre}</span>
              <span style={S.hora}>
                {e ? new Date(e.entro_en).toLocaleTimeString("es-DO", { hour: "numeric", minute: "2-digit" }) : "—"}
              </span>
              <span style={S.puntos}>{n ? `${n.puntos} / 100` : ""}</span>
              {e ? (
                <span style={S.acciones}>
                  <button type="button" style={e.bloqueado ? S.desbloquear : S.bloquear}
                          onClick={() => bloquear(e, !e.bloqueado)}>
                    {e.bloqueado ? "Desbloquear" : "Bloquear"}
                  </button>
                  <button type="button" style={S.desmarcar} onClick={() => desmarcar(e, p.nombre)}>Desmarcar</button>
                </span>
              ) : <span />}
            </li>
          );
        })}
        {!gente.length && <li style={S.vacio}>Esta sección no tiene lista cargada.</li>}
      </ul>
    </>
  );
}

const S: Record<string, React.CSSProperties> = {
  mandos: { display: "flex", flexWrap: "wrap", gap: 14, alignItems: "end" },
  campo: { display: "grid", gap: 6, fontSize: 12, color: "var(--mut)", letterSpacing: ".04em" },
  select: { minHeight: 42, padding: "0 12px", borderRadius: 8, border: "1px solid var(--linea)",
            background: "var(--panel)", color: "var(--tx)", fontFamily: "inherit", fontSize: 15 },
  abierta: { alignSelf: "center", fontSize: 14, fontWeight: 700, color: "var(--verde)" },
  cerrada: { alignSelf: "center", fontSize: 14, color: "var(--mut)" },
  boton: { minHeight: 42, padding: "0 20px", borderRadius: 8, border: 0, background: "var(--aqua)",
           color: "var(--fondo)", fontFamily: "inherit", fontSize: 15, fontWeight: 700, cursor: "pointer", marginLeft: "auto" },
  botonSec: { minHeight: 42, padding: "0 20px", borderRadius: 8, border: "1px solid var(--linea)", background: "transparent",
              color: "var(--tx)", fontFamily: "inherit", fontSize: 15, cursor: "pointer", marginLeft: "auto" },
  nota: { margin: "12px 0 0", fontSize: 13.5, color: "var(--tx-2)", lineHeight: 1.5 },
  error: { marginTop: 12, color: "var(--rojo)", fontSize: 14 },
  resumen: { fontSize: 13, color: "var(--mut)", fontFamily: "ui-monospace,Menlo,monospace" },
  lista: { listStyle: "none", margin: "10px 0 0", padding: 0, display: "grid", gap: 4 },
  fila: { display: "grid", gridTemplateColumns: "1fr 80px 90px 210px", gap: 10, alignItems: "center",
          padding: "9px 12px", borderRadius: 8, background: "var(--panel)", fontSize: 14.5 },
  fuera: { opacity: 0.5 },
  nombre: { overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" },
  hora: { fontSize: 13, color: "var(--mut)", fontFamily: "ui-monospace,Menlo,monospace" },
  puntos: { fontSize: 13.5, fontWeight: 700, fontFamily: "ui-monospace,Menlo,monospace", textAlign: "right" },
  desmarcar: { minHeight: 32, padding: "0 10px", borderRadius: 7, border: "1px solid var(--linea)", background: "transparent",
               color: "var(--ambar)", fontFamily: "inherit", fontSize: 13, cursor: "pointer" },
  vacio: { padding: 14, color: "var(--tx-2)", fontSize: 14 },
  confirmar: { marginTop: 16, padding: "16px 18px", borderRadius: 10, border: "1px solid var(--ambar)",
               background: "var(--panel)", display: "grid", gap: 10 },
  confTitulo: { margin: 0, fontSize: 16, fontWeight: 700 },
  confTexto: { margin: 0, fontSize: 14, color: "var(--tx-2)", lineHeight: 1.5 },
  confAcc: { display: "flex", flexWrap: "wrap", gap: 10 },
  boton0: { minHeight: 42, padding: "0 18px", borderRadius: 8, border: 0, background: "var(--aqua)",
            color: "var(--fondo)", fontFamily: "inherit", fontSize: 15, fontWeight: 700, cursor: "pointer" },
  botonSec0: { minHeight: 42, padding: "0 16px", borderRadius: 8, border: "1px solid var(--linea)", background: "transparent",
               color: "var(--tx)", fontFamily: "inherit", fontSize: 15, cursor: "pointer" },
  aviso: { marginTop: 12, fontSize: 14, color: "var(--verde)" },
  listaHoy: { marginTop: 14, padding: "10px 14px", borderRadius: 8, border: "1px solid var(--linea)",
              display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center", justifyContent: "space-between",
              fontSize: 14, color: "var(--tx-2)" },
  acciones: { display: "flex", gap: 6, justifyContent: "flex-end" },
  todos: { margin: "20px 0 0", display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center",
           justifyContent: "space-between" },
  bloquear: { minHeight: 32, padding: "0 10px", borderRadius: 7, border: "1px solid var(--linea)", background: "transparent",
              color: "var(--rojo)", fontFamily: "inherit", fontSize: 13, cursor: "pointer" },
  desbloquear: { minHeight: 32, padding: "0 10px", borderRadius: 7, border: 0, background: "var(--rojo)",
                 color: "var(--fondo)", fontFamily: "inherit", fontSize: 13, fontWeight: 700, cursor: "pointer" },
};

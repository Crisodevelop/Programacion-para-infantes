"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { SECCIONES, bloqueActual } from "@/lib/horario";

/**
 * Asistencia: pasar lista, corregirla y borrarla, en una sola pantalla.
 *
 * Arriba, el editor de la lista de una sección y un día. Dice siempre qué se
 * está haciendo —una lista nueva o corregir una guardada— y cada estudiante
 * tiene sus cuatro estados a la vista, sin tener que adivinar qué hace un toque.
 * Abajo, las listas guardadas, con Editar (la sube al editor) y Borrar.
 *
 * Todo va con la sesión del docente; la RLS decide. La clase en vivo escribe
 * en las mismas tablas, así que lo que marcaron los estudiantes aparece aquí.
 */

type Estado = "presente" | "tarde" | "ausente" | "excusa";
type Marca = { estado: Estado; nota?: string };
type Alumno = { id: string; nombre: string };
type Cabecera = { id: string; grupo: string; fecha: string; cerrada_en: string | null };
type Registro = { asistencia_id: string; estudiante_id: string; estado: Estado; nota: string | null; nombre: string };

const ESTADOS: { k: Estado; t: string; color: string }[] = [
  { k: "presente", t: "Presente", color: "var(--verde)" },
  { k: "tarde", t: "Tarde", color: "var(--ambar)" },
  { k: "ausente", t: "Ausente", color: "var(--rojo)" },
  { k: "excusa", t: "Excusa", color: "var(--lila)" },
];
const COLOR = Object.fromEntries(ESTADOS.map((e) => [e.k, e.color])) as Record<Estado, string>;

function hoy(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
/** «vie 18 sep»: la fecha se lee a mediodía para que la zona horaria no la mueva de día. */
function fechaCorta(f: string) {
  return new Date(`${f}T12:00:00`).toLocaleDateString("es-DO", { weekday: "short", day: "numeric", month: "short" });
}
function fechaLarga(f: string) {
  return new Date(`${f}T12:00:00`).toLocaleDateString("es-DO", { weekday: "long", day: "numeric", month: "long" });
}
const borradorDe = (sec: string, dia: string) => `asistencia-borrador:${sec}:${dia}`;

export function AreaAsistencia() {
  // ─── El editor ──────────────────────────────────────────────────────────
  const [seccion, setSeccion] = useState(() => bloqueActual()?.seccion ?? SECCIONES[0]);
  const [fecha, setFecha] = useState(hoy);
  const [alumnos, setAlumnos] = useState<Alumno[]>([]);
  const [marcas, setMarcas] = useState<Record<string, Marca>>({});
  const [guardadas, setGuardadas] = useState<Record<string, Marca>>({});
  const [cabecera, setCabecera] = useState<Cabecera | null>(null);
  const [borrador, setBorrador] = useState(false);
  const [buscar, setBuscar] = useState("");
  const [cargando, setCargando] = useState(true);
  const [ocupado, setOcupado] = useState(false);
  const [aviso, setAviso] = useState<{ ok: boolean; t: string } | null>(null);
  const [confirmarBorrar, setConfirmarBorrar] = useState<string | null>(null);
  const editorRef = useRef<HTMLElement>(null);
  const turno = useRef(0);

  // ─── Las listas guardadas ───────────────────────────────────────────────
  const [listas, setListas] = useState<Cabecera[]>([]);
  const [registros, setRegistros] = useState<Registro[]>([]);
  const [filtro, setFiltro] = useState("");
  const [abierta, setAbierta] = useState<string | null>(null);

  const cargarListas = useCallback(async () => {
    const sb = supabaseNavegador();
    const { data: cabs, error } = await sb.from("asistencia")
      .select("id,grupo,fecha,cerrada_en").order("fecha", { ascending: false }).order("grupo").limit(150);
    if (error) { setAviso({ ok: false, t: `No pude leer las listas: ${error.message}` }); return; }
    const ids = (cabs ?? []).map((c) => c.id as string);
    const { data: regs } = ids.length
      ? await sb.from("asistencia_registros").select("asistencia_id,estudiante_id,estado,nota,lista(nombre)").in("asistencia_id", ids)
      : { data: [] };
    setListas((cabs ?? []) as Cabecera[]);
    setRegistros(((regs ?? []) as Array<Record<string, unknown>>).map((r) => ({
      asistencia_id: r.asistencia_id as string,
      estudiante_id: r.estudiante_id as string,
      estado: r.estado as Estado,
      nota: (r.nota as string | null) ?? null,
      nombre: (r.lista as { nombre?: string } | null)?.nombre ?? "Sin nombre",
    })));
  }, []);

  /** La sección y el día en el editor: la lista si ya existe, y el borrador si lo hay. */
  const cargarEditor = useCallback(async (sec: string, dia: string) => {
    const mio = ++turno.current;
    setCargando(true);
    setConfirmarBorrar(null);
    const sb = supabaseNavegador();
    const [{ data: gente }, { data: cab }] = await Promise.all([
      sb.from("lista").select("id,nombre").eq("seccion", sec).eq("activo", true).order("apellidos").order("nombres"),
      sb.from("asistencia").select("id,grupo,fecha,cerrada_en").eq("grupo", sec).eq("fecha", dia).maybeSingle(),
    ]);
    let previas: Record<string, Marca> = {};
    if (cab?.id) {
      const { data: regs } = await sb.from("asistencia_registros")
        .select("estudiante_id,estado,nota").eq("asistencia_id", cab.id as string);
      for (const r of regs ?? []) {
        previas[r.estudiante_id as string] = { estado: r.estado as Estado, nota: (r.nota as string | null) ?? undefined };
      }
    }
    if (mio !== turno.current) return;
    let local: Record<string, Marca> | null = null;
    try { local = JSON.parse(localStorage.getItem(borradorDe(sec, dia)) ?? "null"); } catch { local = null; }
    setAlumnos((gente ?? []) as Alumno[]);
    setCabecera((cab ?? null) as Cabecera | null);
    setGuardadas(previas);
    setMarcas(local ?? previas);
    setBorrador(!!local);
    setCargando(false);
  }, []);

  useEffect(() => { void cargarListas(); }, [cargarListas]);
  useEffect(() => { void cargarEditor(seccion, fecha); }, [cargarEditor, seccion, fecha]);

  function cambiar(nuevas: Record<string, Marca>) {
    setMarcas(nuevas);
    setBorrador(true);
    setAviso(null);
    try { localStorage.setItem(borradorDe(seccion, fecha), JSON.stringify(nuevas)); } catch { /* sin almacenamiento */ }
  }
  function marcar(id: string, estado: Estado) {
    const antes = marcas[id];
    const siguiente = { ...marcas };
    if (antes?.estado === estado) delete siguiente[id];          // tocar el mismo lo desmarca
    else siguiente[id] = { estado, nota: estado === "excusa" ? antes?.nota : (antes?.nota === "entró solo" ? antes.nota : undefined) };
    cambiar(siguiente);
  }
  function motivo(id: string, texto: string) {
    cambiar({ ...marcas, [id]: { estado: "excusa", nota: texto.slice(0, 120) } });
  }
  function todosPresentes() {
    const s = { ...marcas };
    for (const a of alumnos) if (!s[a.id]) s[a.id] = { estado: "presente" };
    cambiar(s);
  }
  function descartar() {
    try { localStorage.removeItem(borradorDe(seccion, fecha)); } catch { /* sin almacenamiento */ }
    setMarcas(guardadas);
    setBorrador(false);
  }

  const cuenta = useMemo(() => {
    const c = { presente: 0, tarde: 0, ausente: 0, excusa: 0, sinMarcar: 0 };
    for (const a of alumnos) {
      const e = marcas[a.id]?.estado;
      if (e) c[e]++; else c.sinMarcar++;
    }
    return c;
  }, [marcas, alumnos]);

  async function guardar() {
    if (!cabecera && cuenta.presente + cuenta.tarde + cuenta.excusa === 0) {
      setAviso({ ok: false, t: "No hay nadie marcado. Marca a quien vino antes de guardar." });
      return;
    }
    setOcupado(true);
    setAviso(null);
    const sb = supabaseNavegador();
    const { data: { user } } = await sb.auth.getUser();
    const { data: cab, error: e1 } = await sb.from("asistencia").upsert(
      { grupo: seccion, fecha, docente_id: user?.id ?? null, cerrada_en: new Date().toISOString() },
      { onConflict: "grupo,fecha" },
    ).select("id").single();
    if (e1 || !cab) { setOcupado(false); setAviso({ ok: false, t: `No se pudo guardar: ${e1?.message}` }); return; }
    // Se escriben todos: el que quedó sin marcar es un ausente y tiene que constar.
    const filas = alumnos.map((a) => ({
      asistencia_id: cab.id as string,
      estudiante_id: a.id,
      estado: marcas[a.id]?.estado ?? "ausente",
      nota: marcas[a.id]?.nota ?? null,
    }));
    const { error: e2 } = await sb.from("asistencia_registros").upsert(filas, { onConflict: "asistencia_id,estudiante_id" });
    setOcupado(false);
    if (e2) { setAviso({ ok: false, t: `No se pudieron guardar los registros: ${e2.message}` }); return; }
    try { localStorage.removeItem(borradorDe(seccion, fecha)); } catch { /* sin almacenamiento */ }
    setAviso({ ok: true, t: `Lista de ${seccion} del ${fechaCorta(fecha)} guardada: ${cuenta.presente} presentes, ` +
      `${cuenta.tarde} tarde, ${cuenta.ausente + cuenta.sinMarcar} ausentes y ${cuenta.excusa} con excusa.` });
    await Promise.all([cargarEditor(seccion, fecha), cargarListas()]);
  }

  async function borrar(id: string, sec: string, dia: string) {
    setOcupado(true);
    const { error } = await supabaseNavegador().from("asistencia").delete().eq("id", id);
    setOcupado(false);
    setConfirmarBorrar(null);
    if (error) { setAviso({ ok: false, t: `No se pudo borrar: ${error.message}` }); return; }
    try { localStorage.removeItem(borradorDe(sec, dia)); } catch { /* sin almacenamiento */ }
    setAviso({ ok: true, t: `Borrada la lista de ${sec} del ${fechaCorta(dia)}.` });
    await Promise.all([cargarEditor(seccion, fecha), cargarListas()]);
  }

  function editar(c: Cabecera) {
    setSeccion(c.grupo);
    setFecha(c.fecha);
    setAviso(null);
    editorRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  const vistos = useMemo(() => {
    const q = buscar.trim().toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
    if (!q) return alumnos;
    return alumnos.filter((a) => a.nombre.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "").includes(q));
  }, [alumnos, buscar]);

  const porLista = useMemo(() => {
    const m = new Map<string, Registro[]>();
    for (const r of registros) {
      if (!m.has(r.asistencia_id)) m.set(r.asistencia_id, []);
      m.get(r.asistencia_id)!.push(r);
    }
    return m;
  }, [registros]);
  const gruposConLista = [...new Set(listas.map((l) => l.grupo))].sort();
  const listasVistas = filtro ? listas.filter((l) => l.grupo === filtro) : listas;

  return (
    <>
      {/* ═══ El editor ═══ */}
      <section ref={editorRef} style={S.editor} aria-label="Pasar lista">
        <div style={S.pestanas} role="tablist" aria-label="Sección">
          {SECCIONES.map((s) => (
            <button key={s} type="button" role="tab" aria-selected={s === seccion}
                    style={s === seccion ? { ...S.pestana, ...S.pestanaOn } : S.pestana}
                    onClick={() => { setSeccion(s); setAviso(null); }}>
              {s}
            </button>
          ))}
        </div>

        <div style={S.estadoFila}>
          <div>
            <p style={S.estadoEtq}>{cabecera ? "Editando" : "Lista nueva"}</p>
            <h2 style={S.estadoTitulo}>
              {seccion} · <span style={{ textTransform: "capitalize" }}>{fechaLarga(fecha)}</span>
            </h2>
            <p style={S.estadoSub}>
              {cabecera
                ? cabecera.cerrada_en
                  ? `Guardada a las ${new Date(cabecera.cerrada_en).toLocaleTimeString("es-DO", { hour: "numeric", minute: "2-digit" })}. Lo que cambies reemplaza lo guardado.`
                  : "Empezada por la clase en vivo: todavía no la has guardado tú."
                : "Todavía no hay lista de este día. Marca a cada uno y guárdala."}
            </p>
          </div>
          <div style={S.estadoAcc}>
            <label style={S.campoFecha}>
              Día
              <input type="date" value={fecha} max={hoy()} onChange={(e) => setFecha(e.target.value || hoy())} style={S.fecha} />
            </label>
            {cabecera && (
              confirmarBorrar === cabecera.id ? (
                <span style={S.confirmar}>
                  ¿Borrar esta lista?
                  <button type="button" style={S.botonPeligro} disabled={ocupado}
                          onClick={() => void borrar(cabecera.id, seccion, fecha)}>Sí, borrar</button>
                  <button type="button" style={S.botonSec} onClick={() => setConfirmarBorrar(null)}>No</button>
                </span>
              ) : (
                <button type="button" style={S.botonBorrar} onClick={() => setConfirmarBorrar(cabecera.id)}>
                  Borrar esta lista
                </button>
              )
            )}
          </div>
        </div>

        {borrador && (
          <p style={S.borrador}>
            Borrador sin guardar: lo que ves todavía no está en la lista.
            <button type="button" style={S.enlace} onClick={descartar}>Descartar</button>
          </p>
        )}

        <div style={S.herramientas}>
          <input type="search" value={buscar} onChange={(e) => setBuscar(e.target.value)}
                 placeholder="Buscar estudiante" aria-label="Buscar estudiante" style={S.buscar} />
          <button type="button" style={S.botonSec} onClick={todosPresentes} disabled={cargando}>
            Todos presentes
          </button>
          <button type="button" style={S.botonSec} onClick={() => cambiar({})} disabled={cargando}>Limpiar</button>
        </div>

        {cargando ? (
          <p style={S.vacio}>Cargando la lista…</p>
        ) : !alumnos.length ? (
          <p style={S.vacio}>Esta sección no tiene lista cargada.</p>
        ) : (
          <ul style={S.alumnos}>
            {vistos.map((a) => {
              const m = marcas[a.id];
              return (
                <li key={a.id} style={S.alumno}>
                  <span style={S.num}>{alumnos.indexOf(a) + 1}</span>
                  <span style={S.nombre}>
                    {a.nombre}
                    {m?.nota === "entró solo" && <span style={S.solo}>entró solo</span>}
                  </span>
                  <span style={S.segmento} role="radiogroup" aria-label={`Asistencia de ${a.nombre}`}>
                    {ESTADOS.map((e) => {
                      const on = m?.estado === e.k;
                      return (
                        <button key={e.k} type="button" role="radio" aria-checked={on}
                                style={on ? { ...S.opcion, background: e.color, color: "var(--fondo)", borderColor: e.color } : S.opcion}
                                onClick={() => marcar(a.id, e.k)}>
                          {e.t}
                        </button>
                      );
                    })}
                  </span>
                  {m?.estado === "excusa" && (
                    <input value={m.nota ?? ""} onChange={(ev) => motivo(a.id, ev.target.value)}
                           placeholder="Motivo de la excusa (opcional)" aria-label={`Motivo de ${a.nombre}`}
                           style={S.motivo} />
                  )}
                </li>
              );
            })}
            {!vistos.length && <li style={S.vacio}>Nadie con ese nombre.</li>}
          </ul>
        )}

        {aviso && <p style={aviso.ok ? S.avisoOk : S.avisoMal}>{aviso.t}</p>}

        <div style={S.barra}>
          <span style={S.cuenta}>
            <b style={{ color: COLOR.presente }}>{cuenta.presente}</b> presentes ·{" "}
            <b style={{ color: COLOR.tarde }}>{cuenta.tarde}</b> tarde ·{" "}
            <b style={{ color: COLOR.ausente }}>{cuenta.ausente}</b> ausentes ·{" "}
            <b style={{ color: COLOR.excusa }}>{cuenta.excusa}</b> excusa
            {cuenta.sinMarcar > 0 && <span style={S.sinMarcar}> · {cuenta.sinMarcar} sin marcar quedan ausentes</span>}
          </span>
          <button type="button" style={S.boton} disabled={ocupado || cargando || !alumnos.length} onClick={() => void guardar()}>
            {ocupado ? "Guardando…" : cabecera ? "Guardar cambios" : "Guardar lista"}
          </button>
        </div>
      </section>

      {/* ═══ Las listas guardadas ═══ */}
      <section style={{ marginTop: 40 }} aria-label="Listas guardadas">
        <h2 style={S.h2}>Listas guardadas</h2>
        <p style={S.sub}>{listas.length} {listas.length === 1 ? "lista" : "listas"}. Editar la sube al editor de arriba.</p>

        {gruposConLista.length > 1 && (
          <div style={S.filtros}>
            <button type="button" style={filtro === "" ? { ...S.chip, ...S.chipOn } : S.chip} onClick={() => setFiltro("")}>Todas</button>
            {gruposConLista.map((g) => (
              <button key={g} type="button" style={filtro === g ? { ...S.chip, ...S.chipOn } : S.chip} onClick={() => setFiltro(g)}>{g}</button>
            ))}
          </div>
        )}

        <ul style={S.historial}>
          {listasVistas.map((l) => {
            const regs = (porLista.get(l.id) ?? []).slice().sort((a, b) => a.nombre.localeCompare(b.nombre, "es"));
            const c = { presente: 0, tarde: 0, ausente: 0, excusa: 0 };
            for (const r of regs) c[r.estado]++;
            const base = regs.length - c.excusa;
            const pct = base > 0 ? Math.round(((c.presente + c.tarde) / base) * 100) : 0;
            const abiertaEsta = abierta === l.id;
            const faltan = regs.filter((r) => r.estado !== "presente");
            return (
              <li key={l.id} style={S.tarjeta}>
                <div style={S.tarjetaFila}>
                  <button type="button" style={S.tarjetaBoton} onClick={() => setAbierta(abiertaEsta ? null : l.id)}
                          aria-expanded={abiertaEsta}>
                    <span style={S.tarjetaFecha}>{fechaCorta(l.fecha)}</span>
                    <span style={S.tarjetaGrupo}>{l.grupo}</span>
                    <span style={S.tarjetaCuenta}>
                      {c.presente} P{c.tarde ? ` · ${c.tarde} T` : ""}{c.ausente ? ` · ${c.ausente} A` : ""}{c.excusa ? ` · ${c.excusa} E` : ""}
                    </span>
                    <span style={S.pct} aria-label={`${pct} % de asistencia`}>
                      <span style={{ ...S.pctBarra, width: `${pct}%`, background: pct >= 90 ? "var(--verde)" : pct >= 75 ? "var(--ambar)" : "var(--rojo)" }} />
                    </span>
                    <span style={S.pctNum}>{pct} %</span>
                  </button>
                  <span style={S.tarjetaAcc}>
                    <button type="button" style={S.accion} onClick={() => editar(l)}>Editar</button>
                    {confirmarBorrar === l.id ? (
                      <>
                        <button type="button" style={S.accionPeligro} disabled={ocupado} onClick={() => void borrar(l.id, l.grupo, l.fecha)}>Sí, borrar</button>
                        <button type="button" style={S.accion} onClick={() => setConfirmarBorrar(null)}>No</button>
                      </>
                    ) : (
                      <button type="button" style={{ ...S.accion, color: "var(--rojo)" }} onClick={() => setConfirmarBorrar(l.id)}>Borrar</button>
                    )}
                  </span>
                </div>
                {abiertaEsta && (
                  <div style={S.detalle}>
                    {faltan.length > 0 && (
                      <>
                        <p style={S.detalleEtq}>No estuvieron a tiempo</p>
                        <ul style={S.detalleLista}>
                          {faltan.map((r) => (
                            <li key={r.estudiante_id} style={S.persona}>
                              <span>{r.nombre}{r.nota && r.nota !== "entró solo" ? <span style={S.notaTx}> · {r.nota}</span> : null}</span>
                              <b style={{ color: COLOR[r.estado], fontSize: 12.5 }}>{r.estado}</b>
                            </li>
                          ))}
                        </ul>
                      </>
                    )}
                    <p style={S.detalleEtq}>Presentes ({c.presente})</p>
                    <p style={S.presentes}>{regs.filter((r) => r.estado === "presente").map((r) => r.nombre).join(" · ") || "Nadie"}</p>
                  </div>
                )}
              </li>
            );
          })}
          {!listasVistas.length && <li style={S.vacio}>Todavía no hay listas guardadas.</li>}
        </ul>
      </section>
    </>
  );
}

const S: Record<string, React.CSSProperties> = {
  editor: { padding: "18px 18px 0", borderRadius: 14, border: "1px solid var(--linea)", background: "var(--panel)",
            scrollMarginTop: 90 },
  pestanas: { display: "flex", flexWrap: "wrap", gap: 6 },
  pestana: { minHeight: 36, padding: "0 13px", borderRadius: 999, border: "1px solid var(--linea)", background: "transparent",
             color: "var(--tx-2)", fontFamily: "inherit", fontSize: 14, cursor: "pointer" },
  pestanaOn: { background: "var(--aqua)", borderColor: "var(--aqua)", color: "var(--fondo)", fontWeight: 700 },
  estadoFila: { display: "flex", flexWrap: "wrap", gap: 16, justifyContent: "space-between", alignItems: "flex-end",
                marginTop: 18, paddingBottom: 14, borderBottom: "1px solid var(--linea)" },
  estadoEtq: { margin: 0, fontSize: 12, letterSpacing: ".14em", textTransform: "uppercase", color: "var(--aqua)" },
  estadoTitulo: { margin: "6px 0 0", fontSize: 24, fontWeight: 700, letterSpacing: "-.02em" },
  estadoSub: { margin: "6px 0 0", fontSize: 14, color: "var(--tx-2)" },
  estadoAcc: { display: "flex", flexWrap: "wrap", gap: 10, alignItems: "flex-end" },
  campoFecha: { display: "grid", gap: 5, fontSize: 12, color: "var(--mut)" },
  fecha: { minHeight: 40, padding: "0 10px", borderRadius: 8, border: "1px solid var(--linea)", background: "var(--fondo-2)",
           color: "var(--tx)", fontFamily: "inherit", fontSize: 14, colorScheme: "dark" },
  confirmar: { display: "flex", alignItems: "center", gap: 8, fontSize: 14 },
  borrador: { margin: "12px 0 0", padding: "8px 12px", borderRadius: 8, background: "rgba(245,158,11,.1)",
              border: "1px solid var(--ambar)", fontSize: 13.5, color: "var(--tx)", display: "flex", gap: 10, alignItems: "center" },
  enlace: { background: "none", border: 0, color: "var(--aqua)", fontFamily: "inherit", fontSize: 13.5, cursor: "pointer",
            padding: 0, textDecoration: "underline" },
  herramientas: { display: "flex", flexWrap: "wrap", gap: 8, marginTop: 14 },
  buscar: { flex: "1 1 220px", minHeight: 40, padding: "0 12px", borderRadius: 8, border: "1px solid var(--linea)",
            background: "var(--fondo-2)", color: "var(--tx)", fontFamily: "inherit", fontSize: 14 },
  alumnos: { listStyle: "none", margin: "12px 0 0", padding: 0, display: "grid", gap: 4 },
  alumno: { display: "flex", flexWrap: "wrap", alignItems: "center", gap: "6px 12px", padding: "8px 10px", borderRadius: 8,
            background: "var(--fondo-2)" },
  num: { width: 22, fontSize: 12, color: "var(--mut)", fontFamily: "ui-monospace,Menlo,monospace", textAlign: "right" },
  nombre: { flex: "1 1 220px", fontSize: 14.5, display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" },
  solo: { fontSize: 11, padding: "1px 7px", borderRadius: 99, border: "1px solid var(--aqua)", color: "var(--aqua)" },
  segmento: { display: "inline-flex", gap: 4, flexWrap: "wrap" },
  opcion: { minHeight: 34, minWidth: 74, padding: "0 10px", borderRadius: 7, border: "1px solid var(--linea)",
            background: "transparent", color: "var(--tx-2)", fontFamily: "inherit", fontSize: 13, cursor: "pointer" },
  motivo: { flex: "1 1 100%", minHeight: 34, padding: "0 10px", borderRadius: 7, border: "1px solid var(--lila)",
            background: "transparent", color: "var(--tx)", fontFamily: "inherit", fontSize: 13 },
  vacio: { padding: 14, color: "var(--tx-2)", fontSize: 14, listStyle: "none" },
  avisoOk: { margin: "12px 0 0", fontSize: 14, color: "var(--verde)" },
  avisoMal: { margin: "12px 0 0", fontSize: 14, color: "var(--rojo)" },
  barra: { position: "sticky", bottom: 0, zIndex: 5, display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center",
           justifyContent: "space-between", margin: "14px -18px 0", padding: "12px 18px", borderTop: "1px solid var(--linea)",
           background: "var(--panel)", borderRadius: "0 0 14px 14px" },
  cuenta: { fontSize: 14, color: "var(--tx-2)" },
  sinMarcar: { color: "var(--mut)" },
  boton: { minHeight: 44, padding: "0 22px", borderRadius: 9, border: 0, background: "var(--aqua)", color: "var(--fondo)",
           fontFamily: "inherit", fontSize: 15, fontWeight: 700, cursor: "pointer" },
  botonSec: { minHeight: 40, padding: "0 14px", borderRadius: 8, border: "1px solid var(--linea)", background: "transparent",
              color: "var(--tx)", fontFamily: "inherit", fontSize: 14, cursor: "pointer" },
  botonBorrar: { minHeight: 40, padding: "0 14px", borderRadius: 8, border: "1px solid var(--linea)", background: "transparent",
                 color: "var(--rojo)", fontFamily: "inherit", fontSize: 14, cursor: "pointer" },
  botonPeligro: { minHeight: 36, padding: "0 12px", borderRadius: 8, border: 0, background: "var(--rojo)", color: "var(--fondo)",
                  fontFamily: "inherit", fontSize: 13.5, fontWeight: 700, cursor: "pointer" },
  h2: { fontSize: 19, margin: 0, fontWeight: 600 },
  sub: { margin: "6px 0 14px", fontSize: 14, color: "var(--tx-2)" },
  filtros: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 12 },
  chip: { minHeight: 32, padding: "0 12px", borderRadius: 99, border: "1px solid var(--linea)", background: "transparent",
          color: "var(--tx-2)", fontFamily: "inherit", fontSize: 13, cursor: "pointer" },
  chipOn: { background: "var(--tx)", color: "var(--fondo)", borderColor: "var(--tx)" },
  historial: { listStyle: "none", margin: 0, padding: 0, display: "grid", gap: 6 },
  tarjeta: { borderRadius: 10, border: "1px solid var(--linea)", background: "var(--panel)", overflow: "hidden" },
  tarjetaFila: { display: "flex", flexWrap: "wrap", alignItems: "center", gap: 8, paddingRight: 10 },
  tarjetaBoton: { flex: "1 1 420px", display: "grid", gridTemplateColumns: "92px 60px 1fr 90px 44px", gap: 10, alignItems: "center",
                  padding: "12px 14px", background: "none", border: 0, color: "var(--tx)", fontFamily: "inherit",
                  fontSize: 14, textAlign: "left", cursor: "pointer" },
  tarjetaFecha: { textTransform: "capitalize", color: "var(--tx-2)" },
  tarjetaGrupo: { fontWeight: 700 },
  tarjetaCuenta: { color: "var(--tx-2)", fontFamily: "ui-monospace,Menlo,monospace", fontSize: 13 },
  pct: { height: 6, borderRadius: 99, background: "var(--fondo-2)", overflow: "hidden" },
  pctBarra: { display: "block", height: "100%", borderRadius: 99 },
  pctNum: { fontSize: 13, fontFamily: "ui-monospace,Menlo,monospace", textAlign: "right" },
  tarjetaAcc: { display: "flex", gap: 6 },
  accion: { minHeight: 32, padding: "0 11px", borderRadius: 7, border: "1px solid var(--linea)", background: "transparent",
            color: "var(--tx)", fontFamily: "inherit", fontSize: 13, cursor: "pointer" },
  accionPeligro: { minHeight: 32, padding: "0 11px", borderRadius: 7, border: 0, background: "var(--rojo)", color: "var(--fondo)",
                   fontFamily: "inherit", fontSize: 13, fontWeight: 700, cursor: "pointer" },
  detalle: { padding: "4px 16px 14px", borderTop: "1px solid var(--linea)" },
  detalleEtq: { margin: "12px 0 6px", fontSize: 11.5, letterSpacing: ".12em", textTransform: "uppercase", color: "var(--mut)" },
  detalleLista: { listStyle: "none", margin: 0, padding: 0, display: "grid", gap: 3 },
  persona: { display: "flex", justifyContent: "space-between", gap: 10, fontSize: 14 },
  notaTx: { color: "var(--mut)", fontSize: 13 },
  presentes: { margin: 0, fontSize: 13.5, color: "var(--tx-2)", lineHeight: 1.6 },
};

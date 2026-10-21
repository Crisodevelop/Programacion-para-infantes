"use client";

import { Fragment, useMemo, useState } from "react";
import { SECCIONES } from "@/lib/horario";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { PESO_DISCIPLINA, totales, type Criterio, type Total } from "@/lib/totales";

export type FilaNota = {
  id: string;
  creado_en: string;
  nombre: string;
  seccion: string;
  nivel: string;
  semana: number;
  puntos: number;
  /** Puesta a mano por el docente: entonces manda sobre lo que calcule sola. */
  puntos_docente?: number | null;
  detalle: Record<string, number>;
  codigo?: string | null;
  estudiante_id?: string | null;
};

export type Conducta = { estudiante_id: string; puntos: number; nota: string | null };

/**
 * La tabla de notas, filtrable por sección y semana, y descargable para Excel.
 *
 * De cliente porque filtrar tiene que ser instantáneo con filas que ya están
 * en la página. Quien tiene dos notas de la misma semana (la clase se repitió
 * otro día) queda marcado, y es el docente quien decide cuál vale.
 *
 * Dos vistas sobre los mismos datos: «por clase», una fila por nota, y
 * «acumulada», una fila por estudiante con lo que lleva hasta la semana que
 * se elija. La acumulada se calcula aquí, no en la base: no hay tabla de nota
 * final y las filas ya están todas en la página.
 */
export function TablaNotas({ filas, conducta = [] }: { filas: FilaNota[]; conducta?: Conducta[] }) {
  const [vista, setVista] = useState<"clase" | "total">("clase");
  const [criterio, setCriterio] = useState<Criterio>("falta-cero");
  const [seccion, setSeccion] = useState("todas");
  const [semana, setSemana] = useState("todas");
  const [abierto, setAbierto] = useState<string | null>(null);

  // Lo que se edita a mano vive aquí hasta que la base lo confirma. El patrón
  // es el de PanelEnlaces: un solo campo abierto a la vez —con dos nunca se
  // sabe cuál se está guardando—, se escribe, y se recarga de la base.
  const [editando, setEditando] = useState<string | null>(null);
  const [valor, setValor] = useState("");
  const [motivo, setMotivo] = useState("");
  const [ocupado, setOcupado] = useState(false);
  const [aviso, setAviso] = useState<{ ok: boolean; t: string } | null>(null);

  const [notas, setNotas] = useState(filas);
  const [conductas, setConductas] = useState(conducta);
  const porEstudiante = useMemo(
    () => new Map(conductas.map((c) => [c.estudiante_id, c.puntos])), [conductas]);
  const motivoDe = useMemo(
    () => new Map(conductas.map((c) => [c.estudiante_id, c.nota])), [conductas]);

  // La semana que vamos, sacada del NIVEL, no de la sección ni de todo junto.
  //
  // Las tres secciones de un nivel ven la misma clase esa semana, así que la
  // última semana de 2do B dice por dónde va 2do A aunque a 2do A no se le
  // haya guardado. Con el máximo de todo, 1ro —que va una semana por delante—
  // abría la tabla de 2do en una semana que 2do no ha dado; con el máximo de
  // la propia sección, una semana que no se registró desaparecía sin más y no
  // había forma de notar que faltaba.
  const ultima = useMemo(() => notas.reduce(
    (m, f) => (seccion === "todas" || nivelDe(f.seccion) === nivelDe(seccion)) ? Math.max(m, f.semana) : m, 1),
    [notas, seccion]);
  // `tope` solo manda mientras no se cambie de sección: al cambiar vuelve a
  // mandar la última de la nueva, que es lo que uno espera ver.
  const [tope, setTope] = useState<{ seccion: string; n: number } | null>(null);
  const hasta = tope && tope.seccion === seccion ? tope.n : ultima;

  const acumuladas = useMemo(() => {
    const base = totales(notas, hasta, criterio, porEstudiante);
    return seccion === "todas" ? base : base.filter((t) => t.seccion === seccion);
  }, [notas, hasta, criterio, seccion, porEstudiante]);

  const repetidos = useMemo(() => {
    const cuenta = new Map<string, number>();
    for (const f of notas) {
      const k = clave(f);
      cuenta.set(k, (cuenta.get(k) ?? 0) + 1);
    }
    return cuenta;
  }, [notas]);

  const vistas = useMemo(
    () => notas.filter((f) =>
      (seccion === "todas" || f.seccion === seccion) && (semana === "todas" || String(f.semana) === semana)),
    [notas, seccion, semana],
  );

  const promedio = vistas.length
    ? Math.round(vistas.reduce((t, f) => t + f.puntos, 0) / vistas.length)
    : null;

  const promedioTotal = acumuladas.length
    ? Math.round(acumuladas.reduce((t, a) => t + (a.nota ?? 0), 0) / acumuladas.length)
    : null;

  // Con una sola sección a la vista se pueden nombrar: así se ve de un golpe
  // que falta la semana 4 porque nadie de ese grupo la tiene guardada.
  // Con «Todas» a la vista conviven niveles que no van por la misma semana, y
  // la tira llegaba hasta la última de TODOS: a 1ro le salían como huecos las
  // semanas que solo ha dado 3ro. Cada fila se corta en la última de su nivel.
  const ultimaDelNivel = useMemo(() => {
    const m = new Map<string, number>();
    for (const f of notas) {
      const n = nivelDe(f.seccion);
      m.set(n, Math.max(m.get(n) ?? 1, f.semana));
    }
    return m;
  }, [notas]);

  const semanasContadas = seccion === "todas" || !acumuladas.length ? null : acumuladas[0].dadas;
  const faltantes = semanasContadas
    ? Array.from({ length: hasta }, (_, i) => i + 1).filter((w) => !semanasContadas.includes(w))
    : [];

  function descargarTotal() {
    const semanas = [...new Set(acumuladas.flatMap((a) => a.dadas))].sort((x, y) => x - y);
    const cabeza = ["Sección", "Nombre", "Clases dadas", "Entregadas", "Puntos",
                    `Académico (${criterio === "falta-cero" ? "faltar vale 0" : "solo lo entregado"})`,
                    "Disciplina", "Por qué", `Final (${Math.round(PESO_DISCIPLINA * 100)} % disciplina)`,
                    ...semanas.map((w) => `S${w}`)];
    const lineas = acumuladas.map((a) => [
      a.seccion, a.nombre, String(a.dadas.length), String(a.entregadas), String(a.puntos),
      a.nota === null ? "" : String(a.nota),
      String(a.disciplina), motivoDe.get(a.ids[0] ?? "") ?? "",
      a.final === null ? "" : String(a.final),
      ...semanas.map((w) => a.dadas.includes(w) ? String(a.porSemana.get(w) ?? 0) : ""),
    ]);
    bajar(`notas-acumuladas-${seccion === "todas" ? "todas" : seccion.replace(" ", "")}-hasta${hasta}.csv`,
          [cabeza, ...lineas]);
  }

  // ── Escribir a mano ───────────────────────────────────────────────────────

  /** Lo que la base va a exigir de todas formas, dicho antes y en cristiano. */
  function queFalta(v: string): string {
    const n = Number(v.trim());
    if (!v.trim()) return "Escribe un número.";
    if (!Number.isInteger(n)) return "Tiene que ser un número entero.";
    if (n < 0 || n > 100) return "La nota va de 0 a 100.";
    return "";
  }

  async function recargar() {
    const sb = supabaseNavegador();
    const [{ data: n }, { data: c }] = await Promise.all([
      sb.from("notas")
        .select("id,creado_en,nombre,seccion,nivel,semana,puntos,puntos_docente,detalle,codigo,estudiante_id")
        .order("creado_en", { ascending: false }),
      sb.from("disciplina").select("estudiante_id,puntos,nota"),
    ]);
    if (n) setNotas(n as FilaNota[]);
    if (c) setConductas(c as Conducta[]);
  }

  function cerrar() {
    setEditando(null);
    setValor("");
    setMotivo("");
  }

  /**
   * La fecha de esa clase, sacada de las notas de sus compañeros.
   *
   * Hace falta para dar de alta una nota a quien no la tiene: `notas` exige
   * fecha y el único es (estudiante_id, fecha, semana). Con la de hoy, la
   * clase aparecería como dada hoy y saldría en Clase en vivo.
   */
  function fechaDe(sec: string, sem: number): string | null {
    const f = notas.find((x) => x.seccion === sec && x.semana === sem && x.creado_en);
    return f ? f.creado_en.slice(0, 10) : null;
  }

  /** Cambia la nota de una clase, o la crea si esa persona no tenía. */
  async function guardarNota(t: Total, sem: number, existente: FilaNota | undefined) {
    const falta = queFalta(valor);
    if (falta) { setAviso({ ok: false, t: falta }); return; }
    const puntos = Number(valor.trim());
    setOcupado(true);
    setAviso(null);
    const sb = supabaseNavegador();

    let error = null;
    if (existente) {
      ({ error } = await sb.from("notas")
        .update({ puntos, puntos_docente: puntos, actualizado_en: new Date().toISOString() })
        .eq("id", existente.id));
    } else {
      const fecha = fechaDe(t.seccion, sem);
      const id = t.ids[0];
      if (!fecha || !id) {
        setOcupado(false);
        setAviso({ ok: false, t: "No puedo crearla: falta saber de qué día fue esa clase." });
        return;
      }
      ({ error } = await sb.from("notas").insert({
        nombre: t.nombre.slice(0, 60), seccion: t.seccion, nivel: t.seccion.slice(0, 3),
        semana: sem, puntos, puntos_docente: puntos, detalle: {}, estudiante_id: id, fecha,
      }));
    }
    setOcupado(false);
    if (error) { setAviso({ ok: false, t: `No se pudo guardar: ${error.message}` }); return; }
    cerrar();
    setAviso({ ok: true, t: `${t.nombre}, semana ${sem}: ${puntos}. Esa clase ya no se recalcula sola.` });
    await recargar();
  }

  /** La conducta del curso. Sin fila es 100, así que un 100 borra la fila. */
  async function guardarConducta(t: Total) {
    const falta = queFalta(valor);
    if (falta) { setAviso({ ok: false, t: falta }); return; }
    const puntos = Number(valor.trim());
    const id = t.ids[0];
    if (!id) { setAviso({ ok: false, t: "Esa persona no tiene ninguna nota con su ficha: no sé a quién anotárselo." }); return; }
    setOcupado(true);
    setAviso(null);
    const sb = supabaseNavegador();

    const { error } = puntos === 100 && !motivo.trim()
      ? await sb.from("disciplina").delete().eq("estudiante_id", id)
      : await sb.from("disciplina").upsert({
          estudiante_id: id, puntos, nota: motivo.trim() || null,
          actualizado_en: new Date().toISOString(),
        }, { onConflict: "estudiante_id" });
    setOcupado(false);
    if (error) { setAviso({ ok: false, t: `No se pudo guardar: ${error.message}` }); return; }
    cerrar();
    setAviso({ ok: true, t: `Disciplina de ${t.nombre}: ${puntos}${puntos === 100 ? " (vuelve al valor de partida)" : ""}.` });
    await recargar();
  }

  function bajar(nombre: string, filas: string[][]) {
    // Con BOM para que Excel lea bien los acentos.
    const csv = "\ufeff" + filas.map((l) => l.map(celda).join(",")).join("\r\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = nombre;
    a.click();
    URL.revokeObjectURL(url);
  }

  function descargar() {
    const cabeza = ["Fecha", "Sección", "Semana", "Nombre", "Nota", "Enviada más de una vez", "Desglose"];
    const lineas = vistas.map((f) => [
      fechaHora(f.creado_en),
      f.seccion,
      String(f.semana),
      f.nombre,
      String(f.puntos),
      (repetidos.get(clave(f)) ?? 0) > 1 ? "sí" : "",
      Object.entries(f.detalle ?? {}).map(([k, v]) => `${k} ${v}`).join(" · "),
    ]);
    bajar(`notas-${seccion === "todas" ? "todas" : seccion.replace(" ", "")}` +
          `${semana === "todas" ? "" : `-semana${semana}`}.csv`, [cabeza, ...lineas]);
  }

  if (!notas.length) {
    return <p style={S.vacio}>Todavía no hay notas. Aparecen aquí en cuanto un estudiante elige su nombre en una clase abierta.</p>;
  }

  return (
    <>
      <div style={S.pestanas} role="tablist" aria-label="Cómo ver las notas">
        {([["clase", "Por clase"], ["total", "Acumulada"]] as const).map(([v, etq]) => (
          <button key={v} type="button" role="tab" aria-selected={vista === v}
                  onClick={() => setVista(v)}
                  style={{ ...S.pestana, ...(vista === v ? S.pestanaViva : null) }}>
            {etq}
          </button>
        ))}
      </div>

      <div style={S.mandos}>
        <label style={S.campo}>
          Sección
          <select value={seccion} onChange={(e) => setSeccion(e.target.value)} style={S.select}>
            <option value="todas">Todas</option>
            {SECCIONES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </label>
        {vista === "clase" ? (
          <label style={S.campo}>
            Semana
            <select value={semana} onChange={(e) => setSemana(e.target.value)} style={S.select}>
              <option value="todas">Todas</option>
              {Array.from({ length: 12 }, (_, i) => String(i + 1)).map((n) =>
                <option key={n} value={n}>Semana {n}</option>)}
            </select>
          </label>
        ) : (
          <>
            <label style={S.campo}>
              Hasta la semana
              <select value={String(hasta)} onChange={(e) => setTope({ seccion, n: Number(e.target.value) })}
                      style={S.select}>
                {Array.from({ length: 12 }, (_, i) => i + 1).map((n) =>
                  <option key={n} value={n}>Semana {n}{n === ultima ? " · la que vamos" : ""}</option>)}
              </select>
            </label>
            <label style={S.campo}>
              Quien falta
              <select value={criterio} onChange={(e) => setCriterio(e.target.value as Criterio)} style={S.select}>
                <option value="falta-cero">Esa clase le vale 0</option>
                <option value="solo-entregado">Solo cuenta lo que entregó</option>
              </select>
            </label>
          </>
        )}
        <button type="button" onClick={vista === "clase" ? descargar : descargarTotal} style={S.boton}
                disabled={vista === "clase" ? !vistas.length : !acumuladas.length}>
          Descargar para Excel
        </button>
      </div>

      <p style={S.resumen}>
        {vista === "clase" ? (
          <>
            {vistas.length} {vistas.length === 1 ? "nota" : "notas"}
            {promedio !== null && <> · promedio {promedio} / 100</>}
          </>
        ) : (
          <>
            {acumuladas.length} {acumuladas.length === 1 ? "estudiante" : "estudiantes"}
            {semanasContadas
              ? <> · cuentan {semanasContadas.length === 1 ? "la semana" : "las semanas"} {lista(semanasContadas)}</>
              : <> · hasta la semana {hasta}</>}
            {promedioTotal !== null && <> · promedio del grupo {promedioTotal} / 100</>}
            {faltantes.length > 0 && (
              <span style={S.sinRegistrar}>
                sin registrar: {lista(faltantes)}
              </span>
            )}
          </>
        )}
      </p>

      {aviso && <p style={aviso.ok ? S.avisoOk : S.avisoMal} role="status">{aviso.t}</p>}

      {vista === "total" ? (
        <div style={S.marco}>
          <table style={S.tabla}>
            <thead>
              <tr>
                <th style={{ ...S.th, ...S.fijo }}>Nombre</th>
                <th style={S.th}>Sección</th>
                <th style={S.th}>Clases</th>
                <th style={{ ...S.th, textAlign: "right" }}>Puntos</th>
                <th style={{ ...S.th, textAlign: "right" }}>Académico</th>
                <th style={{ ...S.th, textAlign: "right" }}>Disciplina</th>
                <th style={{ ...S.th, textAlign: "right" }}>Final</th>
                <th style={S.th}>Por semana</th>
              </tr>
            </thead>
            <tbody>
              {acumuladas.map((a) => (
                <tr key={a.clave}>
                  <td style={{ ...S.td, ...S.fijo }}>{a.nombre}</td>
                  <td style={S.td}>{a.seccion}</td>
                  <td style={{ ...S.td, color: a.entregadas < a.dadas.length ? "var(--ambar)" : "var(--mut)" }}>
                    {a.entregadas} de {a.dadas.length}
                  </td>
                  <td style={{ ...S.td, ...S.num, color: "var(--mut)" }}>
                    {a.puntos}<span style={S.sobre}> / {a.sobre}</span>
                  </td>
                  <td style={{ ...S.td, ...S.num, color: a.nota === null ? "var(--mut)" : color(a.nota) }}>
                    {a.nota ?? "—"}
                  </td>
                  <td style={{ ...S.td, ...S.num }}>
                    {editando === `d:${a.clave}` ? (
                      <span style={S.editor}>
                        <input autoFocus type="number" min={0} max={100} value={valor} style={S.campoNum}
                               onChange={(e) => setValor(e.target.value)}
                               onKeyDown={(e) => { if (e.key === "Escape") cerrar(); }} />
                        <input placeholder="por qué" value={motivo} style={S.campoTexto} maxLength={200}
                               onChange={(e) => setMotivo(e.target.value)}
                               onKeyDown={(e) => { if (e.key === "Escape") cerrar(); }} />
                        <button type="button" style={S.ok} disabled={ocupado}
                                onClick={() => void guardarConducta(a)}>{ocupado ? "…" : "✓"}</button>
                        <button type="button" style={S.no} onClick={cerrar}>✕</button>
                      </span>
                    ) : (
                      <button type="button" style={{ ...S.tocable, color: color(a.disciplina) }}
                              title={motivoDe.get(a.ids[0] ?? "") || (a.disciplina === 100
                                ? "Sin nada anotado. Toca para bajarla." : "Toca para cambiarla.")}
                              onClick={() => {
                                setEditando(`d:${a.clave}`);
                                setValor(String(a.disciplina));
                                setMotivo(motivoDe.get(a.ids[0] ?? "") ?? "");
                                setAviso(null);
                              }}>
                        {a.disciplina}{a.disciplina !== 100 ? " ✎" : ""}
                      </button>
                    )}
                  </td>
                  <td style={{ ...S.td, ...S.num, ...S.final,
                               color: a.final === null ? "var(--mut)" : color(a.final) }}>
                    {a.final ?? "—"}
                  </td>
                  {/* La tira va dentro de un div, no en el propio `td`: un
                      `display:flex` sobre una celda la saca del reparto de
                      columnas de la tabla, y era eso lo que aplastaba las
                      casillas en dos filas y estiraba cada estudiante a tres
                      renglones de alto. */}
                  <td style={{ ...S.td, ...S.tdTira }}>
                   <div style={S.tira}>
                    {/* Todas las semanas hasta la de arriba, no solo las que
                        cuentan: la que no registró nadie desaparecía de la
                        fila y no había manera de notar que faltaba. */}
                    {Array.from({ length: Math.min(hasta, ultimaDelNivel.get(nivelDe(a.seccion)) ?? hasta) },
                                (_, i) => i + 1).map((w) => {
                      const seDio = a.dadas.includes(w);
                      const p = a.porSemana.get(w);
                      const hueco = !seDio ? S.casillaHueco : p === undefined ? S.casillaFalta : null;
                      const suya = notas.find((f) => f.semana === w && f.seccion === a.seccion
                        && normalizaNombre(f.nombre) === normalizaNombre(a.nombre));
                      const aMano = suya?.puntos_docente != null;
                      const sola = suya ? Object.values(suya.detalle ?? {}).reduce((x, y) => x + y, 0) : null;

                      if (editando === `n:${a.clave}:${w}`) {
                        return (
                          <span key={w} style={S.editor}>
                            <i style={S.casillaSem}>S{w}</i>
                            <input autoFocus type="number" min={0} max={100} value={valor} style={S.campoNum}
                                   onChange={(e) => setValor(e.target.value)}
                                   onKeyDown={(e) => { if (e.key === "Escape") cerrar(); }} />
                            <button type="button" style={S.ok} disabled={ocupado}
                                    onClick={() => void guardarNota(a, w, suya)}>{ocupado ? "…" : "✓"}</button>
                            <button type="button" style={S.no} onClick={cerrar}>✕</button>
                          </span>
                        );
                      }
                      // La gris no se toca: esa clase no la tiene nadie de la
                      // sección, así que no hay fecha de la que colgarla.
                      const Etiqueta = seDio ? "button" : "span";
                      return (
                        <Etiqueta key={w} type={seDio ? "button" : undefined}
                              style={{ ...S.casilla, ...hueco, ...(seDio ? S.casillaTocable : null) }}
                              onClick={seDio ? () => {
                                setEditando(`n:${a.clave}:${w}`);
                                setValor(p === undefined ? "" : String(p));
                                setAviso(null);
                              } : undefined}
                              title={!seDio ? `Semana ${w}: nadie de ${a.seccion} la tiene guardada, no cuenta`
                                     : p === undefined ? `Semana ${w}: sin nota. Toca para ponerle una.`
                                     : aMano ? `Semana ${w}: ${p} / 100, puesta a mano` +
                                               (sola !== null ? ` (sola sacó ${Math.min(100, sola)})` : "")
                                     : `Semana ${w}: ${p} / 100. Toca para cambiarla.`}>
                          <i style={S.casillaSem}>S{w}{aMano ? " ✎" : ""}</i>
                          <b style={{ color: !seDio ? "var(--mut)" : p === undefined ? "var(--rojo)" : color(p) }}>
                            {p ?? "·"}
                          </b>
                        </Etiqueta>
                      );
                    })}
                   </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
      <div style={S.marco}>
        <table style={S.tabla}>
          <thead>
            <tr>
              <th style={S.th}>Nombre</th>
              <th style={S.th}>Sección</th>
              <th style={S.th}>Semana</th>
              <th style={{ ...S.th, textAlign: "right" }}>Nota</th>
              <th style={S.th}>Fecha</th>
              <th style={S.th} />
            </tr>
          </thead>
          <tbody>
            {vistas.map((f) => {
              const dos = (repetidos.get(clave(f)) ?? 0) > 1;
              const partes = codigoDe(f.codigo);
              return (
                <Fragment key={f.id}>
                <tr>
                  <td style={S.td}>
                    {f.nombre}
                    {dos && <span style={S.aviso} title="Tiene más de una nota de esta semana">dos veces</span>}
                  </td>
                  <td style={S.td}>{f.seccion}</td>
                  <td style={S.td}>{f.semana}</td>
                  <td style={{ ...S.td, ...S.num, color: color(f.puntos) }}>{f.puntos}</td>
                  <td style={{ ...S.td, color: "var(--mut)" }}>
                    {fechaHora(f.creado_en, true)}
                  </td>
                  <td style={S.td}>
                    {partes.length > 0 && (
                      <button type="button" style={S.ver} onClick={() => setAbierto(abierto === f.id ? null : f.id)}
                              aria-expanded={abierto === f.id}>
                        {abierto === f.id ? "Ocultar código" : "Ver código"}
                      </button>
                    )}
                  </td>
                </tr>
                {abierto === f.id && (
                  <tr>
                    <td colSpan={6} style={S.codigoCelda}>
                      {partes.map(([k, v]) => (
                        <div key={k}>
                          <p style={S.codigoEtq}>{k}</p>
                          <pre style={S.codigo}>{v}</pre>
                        </div>
                      ))}
                    </td>
                  </tr>
                )}
                </Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      )}
    </>
  );
}

/** El editor guarda {py, html, css}; se enseña solo lo que tiene algo escrito. */
function codigoDe(codigo?: string | null): [string, string][] {
  if (!codigo) return [];
  try {
    const d = JSON.parse(codigo) as Record<string, string>;
    const nombres: Record<string, string> = { py: "Python", html: "HTML", css: "CSS" };
    return Object.entries(nombres).filter(([k]) => d[k]?.trim()).map(([k, n]) => [n, d[k]]);
  } catch {
    return [["Código", codigo]];
  }
}

function clave(f: FilaNota) {
  return `${f.seccion}|${f.semana}|${f.nombre.trim().toLowerCase().replace(/\s+/g, " ")}`;
}

/**
 * La fecha, armada a mano a partir de los números.
 *
 * Dos trampas, las dos vistas en vivo en /admin/notas:
 *
 * 1. `toLocaleString` sin `timeZone` usa el huso de quien la ejecuta. Este
 *    componente es de cliente, pero Next lo renderiza también en el servidor,
 *    y en Vercel ese servidor corre en UTC: la misma nota salía «12:09 p. m.»
 *    desde el servidor y «8:09 a. m.» en el navegador.
 *
 * 2. Fijar el huso tampoco basta. Node y Chrome traen versiones distintas de
 *    ICU: Node escribe «a.\u00a0m.» con espacio duro y Chrome «a. m.» con uno
 *    normal. Las dos cadenas se ven idénticas y React las da por distintas —
 *    eso era el «Hydration failed» del panel de avisos.
 *
 * Los NÚMEROS sí son iguales en todas partes, así que se piden solo ellos
 * —en el huso del aula, el mismo que usa `hoy_aula()` en la base— y los
 * separadores los ponemos nosotros.
 */
const HUSO_AULA = "America/Santo_Domingo";

function fechaHora(iso: string, corta = false) {
  const partes = new Intl.DateTimeFormat("en-CA", {
    timeZone: HUSO_AULA, hour12: false,
    year: "2-digit", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  }).formatToParts(new Date(iso));
  const v = (t: Intl.DateTimeFormatPartTypes) => partes.find((x) => x.type === t)?.value ?? "00";
  // Medianoche sale como 24 en algunas versiones de ICU.
  const h24 = Number(v("hour")) % 24;
  const h12 = h24 % 12 === 0 ? 12 : h24 % 12;
  return `${v("day")}/${v("month")}/${v("year")}, ` +
         `${h12}:${v("minute")}${corta ? "" : `:${v("second")}`} ${h24 >= 12 ? "p. m." : "a. m."}`;
}

/** El mismo criterio con el que `totales()` junta a una persona. */
function normalizaNombre(n: string) {
  return n.trim().toLowerCase().replace(/\s+/g, " ");
}

/** «2do A» → «2do»: las tres secciones de un nivel van por la misma semana. */
function nivelDe(seccion: string) {
  return seccion.split(" ")[0];
}

/** 1, 2 y 4 — como se dice en voz alta, no como lo escribe un array. */
function lista(ns: number[]) {
  if (ns.length <= 1) return ns.join("");
  return `${ns.slice(0, -1).join(", ")} y ${ns[ns.length - 1]}`;
}

function celda(v: string) {
  return /[",\r\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
}

function color(p: number) {
  return p >= 80 ? "var(--verde)" : p >= 60 ? "var(--ambar)" : "var(--rojo)";
}

const S: Record<string, React.CSSProperties> = {
  vacio: { marginTop: 30, color: "var(--tx-2)", fontSize: 15 },
  pestanas: { display: "flex", gap: 4, marginBottom: 18 },
  pestana: { minHeight: 36, padding: "0 14px", borderRadius: 8, border: "1px solid var(--linea)",
             background: "transparent", color: "var(--tx-2)", fontFamily: "inherit", fontSize: 14,
             cursor: "pointer" },
  // La abreviada entera, no solo `borderColor`: al cambiar de pestaña React
  // quitaba la propiedad suelta y dejaba la abreviada puesta, y avisa de ello
  // porque el resultado depende del orden en que el navegador las aplique.
  pestanaViva: { border: "1px solid var(--aqua)", color: "var(--aqua)" },
  sobre: { color: "var(--mut)", fontWeight: 400, fontSize: 12.5 },
  // En una sola línea. Al envolverse, un estudiante ocupaba tres renglones y
  // las doce semanas salían en dos columnas pegadas; si no caben, el marco de
  // la tabla ya se desplaza de lado y el nombre se queda fijo a la izquierda.
  tira: { display: "flex", gap: 4, flexWrap: "nowrap", alignItems: "center" },
  casilla: { display: "grid", gap: 0, minWidth: 34, padding: "2px 5px 3px", borderRadius: 5,
             textAlign: "center", lineHeight: 1.2, fontSize: 13.5,
             fontFamily: "ui-monospace,Menlo,monospace", background: "var(--fondo-2)" },
  casillaSem: { fontStyle: "normal", fontSize: 9, letterSpacing: ".06em", color: "var(--mut)" },
  // Dos huecos distintos: rojo, la clase se dio y esta persona no tiene nota
  // —cuenta como 0—; gris, no la tiene nadie de la sección y no cuenta.
  casillaFalta: { border: "1px dashed var(--rojo)", background: "transparent" },
  casillaHueco: { border: "1px dashed var(--linea)", background: "transparent", opacity: .65 },
  sinRegistrar: { marginLeft: 10, padding: "1px 8px", borderRadius: 99, fontSize: 12,
                  color: "var(--ambar)", border: "1px solid var(--ambar)" },
  final: { fontSize: 16 },
  casillaTocable: { cursor: "pointer", font: "inherit", textAlign: "center" },
  tocable: { background: "transparent", border: 0, font: "inherit", fontWeight: 700,
             fontFamily: "ui-monospace,Menlo,monospace", cursor: "pointer", padding: "2px 4px",
             borderRadius: 5 },
  editor: { display: "inline-flex", gap: 4, alignItems: "center" },
  campoNum: { width: 58, minHeight: 32, padding: "0 6px", borderRadius: 6,
              border: "1px solid var(--aqua)", background: "var(--fondo-2)", color: "var(--tx)",
              fontFamily: "ui-monospace,Menlo,monospace", fontSize: 14, textAlign: "right" },
  campoTexto: { width: 130, minHeight: 32, padding: "0 8px", borderRadius: 6,
                border: "1px solid var(--linea)", background: "var(--fondo-2)", color: "var(--tx)",
                fontFamily: "inherit", fontSize: 13 },
  ok: { minWidth: 32, minHeight: 32, borderRadius: 6, border: 0, background: "var(--aqua)",
        color: "var(--fondo)", fontSize: 14, cursor: "pointer" },
  no: { minWidth: 32, minHeight: 32, borderRadius: 6, border: "1px solid var(--linea)",
        background: "transparent", color: "var(--tx-2)", fontSize: 13, cursor: "pointer" },
  avisoOk: { margin: "14px 0 0", fontSize: 14, color: "var(--verde)" },
  avisoMal: { margin: "14px 0 0", fontSize: 14, color: "var(--rojo)" },
  mandos: { display: "flex", flexWrap: "wrap", gap: 14, alignItems: "end" },
  campo: { display: "grid", gap: 6, fontSize: 12, color: "var(--mut)", letterSpacing: ".04em" },
  select: { minHeight: 40, padding: "0 12px", borderRadius: 8, border: "1px solid var(--linea)",
            background: "var(--panel)", color: "var(--tx)", fontFamily: "inherit", fontSize: 14 },
  boton: { minHeight: 40, padding: "0 16px", borderRadius: 8, border: 0, background: "var(--aqua)",
           color: "var(--fondo)", fontFamily: "inherit", fontSize: 14, fontWeight: 700, cursor: "pointer",
           marginLeft: "auto" },
  resumen: { margin: "16px 0 0", fontSize: 13, color: "var(--mut)", fontFamily: "ui-monospace,Menlo,monospace" },
  marco: { marginTop: 14, overflowX: "auto", border: "1px solid var(--linea)", borderRadius: 10 },
  tabla: { width: "100%", borderCollapse: "collapse", fontSize: 14 },
  th: { textAlign: "left", padding: "10px 11px", fontSize: 11, letterSpacing: ".1em", textTransform: "uppercase",
        color: "var(--mut)", borderBottom: "1px solid var(--linea)", whiteSpace: "nowrap" },
  td: { padding: "7px 11px", borderBottom: "1px solid var(--linea)", whiteSpace: "nowrap",
        verticalAlign: "middle" },
  tdTira: { padding: "6px 12px 6px 8px" },
  // El nombre, quieto mientras la tabla se desplaza de lado: con doce semanas
  // en la tira, leer un 47 sin saber de quién es no sirve de nada.
  fijo: { position: "sticky", left: 0, zIndex: 1, background: "var(--fondo)" },
  num: { textAlign: "right", fontWeight: 700, fontFamily: "ui-monospace,Menlo,monospace" },
  ver: { minHeight: 30, padding: "0 10px", borderRadius: 7, border: "1px solid var(--linea)", background: "transparent",
         color: "var(--aqua)", fontFamily: "inherit", fontSize: 12.5, cursor: "pointer" },
  codigoCelda: { padding: "4px 14px 16px", borderBottom: "1px solid var(--linea)", display: "grid", gap: 10 },
  codigoEtq: { margin: "8px 0 4px", fontSize: 11, letterSpacing: ".1em", textTransform: "uppercase", color: "var(--mut)" },
  codigo: { margin: 0, padding: 12, borderRadius: 8, background: "var(--fondo-2)", fontSize: 13, lineHeight: 1.5,
            fontFamily: "ui-monospace,Menlo,monospace", whiteSpace: "pre-wrap", maxHeight: 320, overflow: "auto" },
  aviso: { marginLeft: 8, fontSize: 11, padding: "1px 7px", borderRadius: 99, color: "var(--ambar)",
           border: "1px solid var(--ambar)" },
};

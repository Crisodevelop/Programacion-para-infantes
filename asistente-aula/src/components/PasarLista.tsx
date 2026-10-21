"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { SECCIONES } from "@/lib/horario";

/**
 * Pasar lista tocando nombres.
 *
 * Hasta ahora la única forma era dictársela al asistente por voz, que exige el
 * Mac en modo local y el mando emparejado. Con la clase entrando por la puerta
 * eso no sirve: hace falta el celular y un dedo.
 *
 * ─── Cómo se marca ───
 * Todos empiezan en blanco y cada toque avanza: blanco → P → T → blanco. Al
 * guardar, **lo que quedó en blanco se registra como ausente**.
 *
 * Eso es rápido y es también el riesgo del método: abrir y guardar sin tocar
 * nada marcaría ausente a treinta y cuatro personas. Por eso el botón lleva la
 * cuenta de ausentes escrita antes de pulsarlo, y sin nadie marcado no guarda.
 *
 * ─── Por qué se escribe una sola vez ───
 * Los toques van a `localStorage` según se dan, así que una recarga en mitad
 * de la clase no pierde nada; a la base se va al pulsar Guardar. En el aula el
 * wifi va como va, y treinta escrituras sueltas es treinta oportunidades de
 * fallar a medias.
 *
 * ─── Quién elige la sección ───
 * Sola, sin props, se acuerda de la última sección tocada y enseña las nueve.
 * Dentro de otra pantalla que ya sabe qué clase toca —la presentación, el
 * panel de hoy— se le pasa `seccion` y la sigue; `nivel` deja solo las
 * pestañas de ese curso. Tocar una pestaña se avisa con `onSeccion` para que
 * quien la contiene también cambie, y `onGuardada` dice qué lista quedó
 * guardada.
 */
type Marca = "presente" | "tarde";
type Alumno = { id: string; nombre: string };

const RECUERDA = "lista-seccion";

function hoyLocal(): string {
  const d = new Date();
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

type Props = {
  compacto?: boolean;
  seccion?: string;
  nivel?: string;
  onSeccion?: (s: string) => void;
  onGuardada?: (s: string) => void;
};

export function PasarLista({ compacto = false, seccion: impuesta, nivel, onSeccion, onGuardada }: Props) {
  const [seccion, setSeccion] = useState(
    impuesta && SECCIONES.includes(impuesta) ? impuesta : SECCIONES[0]);
  const [fecha, setFecha] = useState(hoyLocal);
  const [alumnos, setAlumnos] = useState<Alumno[]>([]);
  const [marcas, setMarcas] = useState<Record<string, Marca>>({});
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [aviso, setAviso] = useState("");

  const llave = `pasar-lista:${seccion}:${fecha}`;
  const pestanas = nivel ? SECCIONES.filter((s) => s.startsWith(nivel + " ")) : SECCIONES;

  // La recordada solo cuenta cuando nadie de fuera ha dicho cuál toca.
  useEffect(() => {
    if (impuesta) return;
    try {
      const s = localStorage.getItem(RECUERDA);
      if (s && SECCIONES.includes(s) && (!nivel || s.startsWith(nivel + " "))) setSeccion(s);
    } catch {}
  }, []);

  useEffect(() => {
    if (impuesta && SECCIONES.includes(impuesta)) setSeccion(impuesta);
  }, [impuesta]);

  /**
   * Cada carga lleva su turno y solo pinta la última. Al cambiar de sección
   * deprisa —o de nivel en la presentación— una respuesta lenta de la sección
   * anterior podía llegar después y dejar sus nombres bajo la nueva: al
   * guardar, esos serían los ausentes registrados en el grupo equivocado.
   */
  const turno = useRef(0);

  /**
   * Trae la sección y, si ese día ya se pasó lista, las marcas guardadas.
   * Lo escrito en `localStorage` manda sobre lo guardado: es lo que se estaba
   * tocando ahora mismo.
   */
  const cargar = useCallback(async (sec: string, dia: string) => {
    const mio = ++turno.current;
    setCargando(true); setAviso("");
    const sb = supabaseNavegador();
    const { data: gente } = await sb.from("lista")
      .select("id,nombre").eq("seccion", sec).eq("activo", true).order("nombre");
    if (mio !== turno.current) return;

    let previas: Record<string, Marca> = {};
    const { data: cab } = await sb.from("asistencia")
      .select("id").eq("grupo", sec).eq("fecha", dia).maybeSingle();
    if (mio !== turno.current) return;
    if (cab?.id) {
      const { data: regs } = await sb.from("asistencia_registros")
        .select("estudiante_id,estado").eq("asistencia_id", cab.id as string);
      if (mio !== turno.current) return;
      for (const r of regs ?? []) {
        const e = r.estado as string;
        if (e === "presente" || e === "tarde") previas[r.estudiante_id as string] = e;
      }
    }
    try {
      const local = JSON.parse(localStorage.getItem(`pasar-lista:${sec}:${dia}`) ?? "null");
      if (local && typeof local === "object") previas = local as Record<string, Marca>;
    } catch {}
    setAlumnos((gente ?? []) as Alumno[]);
    setMarcas(previas);
    setCargando(false);
  }, []);

  useEffect(() => { void cargar(seccion, fecha); }, [cargar, seccion, fecha]);

  function guardarLocal(m: Record<string, Marca>) {
    try { localStorage.setItem(llave, JSON.stringify(m)); } catch {}
  }

  function tocar(id: string) {
    setMarcas((m) => {
      const s = { ...m };
      if (!s[id]) s[id] = "presente";
      else if (s[id] === "presente") s[id] = "tarde";
      else delete s[id];
      guardarLocal(s);
      return s;
    });
    setAviso("");
  }

  const cuenta = useMemo(() => {
    const v = Object.values(marcas);
    const p = v.filter((x) => x === "presente").length;
    const t = v.filter((x) => x === "tarde").length;
    return { p, t, a: alumnos.length - p - t };
  }, [marcas, alumnos.length]);

  async function guardar() {
    if (cuenta.p + cuenta.t === 0) {
      setAviso("No has marcado a nadie. Toca al menos a uno.");
      return;
    }
    setGuardando(true); setAviso("");
    const sb = supabaseNavegador();
    const { data: { user } } = await sb.auth.getUser();

    // La clave única (grupo, fecha) hace que pasar lista dos veces el mismo
    // día corrija en vez de duplicar.
    const { data: cab, error: e1 } = await sb.from("asistencia").upsert(
      { grupo: seccion, fecha, docente_id: user?.id ?? null, cerrada_en: new Date().toISOString() },
      { onConflict: "grupo,fecha" },
    ).select("id").single();

    if (e1 || !cab) { setGuardando(false); setAviso(`No se pudo guardar: ${e1?.message}`); return; }

    // Se escriben TODOS, no solo los tocados: el que quedó en blanco es un
    // ausente y tiene que quedar registrado como tal.
    const filas = alumnos.map((a) => ({
      asistencia_id: cab.id as string,
      estudiante_id: a.id,
      estado: marcas[a.id] ?? "ausente",
    }));
    const { error: e2 } = await sb.from("asistencia_registros")
      .upsert(filas, { onConflict: "asistencia_id,estudiante_id" });

    setGuardando(false);
    if (e2) { setAviso(`No se pudieron guardar los registros: ${e2.message}`); return; }
    try { localStorage.removeItem(llave); } catch {}
    setAviso(`Guardada la lista de ${seccion}: ${cuenta.p} presentes, ${cuenta.t} tarde, ${cuenta.a} ausentes.`);
    onGuardada?.(seccion);
  }

  function elegir(s: string) {
    setSeccion(s);
    try { localStorage.setItem(RECUERDA, s); } catch {}
    onSeccion?.(s);
  }

  return (
    <section style={compacto ? S.marcoCompacto : S.marco}>
      <div style={S.mandos}>
        <div style={S.grupo} role="group" aria-label="Sección">
          {pestanas.map((s) => (
            <button key={s} type="button" style={pest(s === seccion)} onClick={() => elegir(s)}>
              {s}
            </button>
          ))}
        </div>
        <input type="date" value={fecha} style={S.fecha} aria-label="Fecha"
               onChange={(e) => setFecha(e.target.value || hoyLocal())} />
      </div>

      <p style={S.cuenta} role="status">
        <b style={{ color: "var(--verde, #7CD9A6)" }}>{cuenta.p}</b> presentes ·{" "}
        <b style={{ color: "#E8B45A" }}>{cuenta.t}</b> tarde ·{" "}
        <b style={{ color: "var(--mut)" }}>{cuenta.a}</b> sin marcar
      </p>

      <div style={S.atajos}>
        <button type="button" style={S.suave}
                onClick={() => { const m = Object.fromEntries(alumnos.map((a) => [a.id, "presente" as Marca]));
                                 setMarcas(m); guardarLocal(m); setAviso(""); }}>
          Todos presentes
        </button>
        <button type="button" style={S.suave}
                onClick={() => { setMarcas({}); guardarLocal({}); setAviso(""); }}>
          Limpiar
        </button>
      </div>

      {cargando ? (
        <p style={S.vacio}>Cargando la lista…</p>
      ) : alumnos.length === 0 ? (
        <p style={S.vacio}>No hay nadie cargado en {seccion}.</p>
      ) : (
        <ul style={S.lista}>
          {alumnos.map((a, i) => {
            const m = marcas[a.id];
            return (
              <li key={a.id}>
                <button type="button" style={S.fila(m)} onClick={() => tocar(a.id)}
                        aria-pressed={!!m}
                        aria-label={`${a.nombre}: ${m === "presente" ? "presente" : m === "tarde" ? "tarde" : "sin marcar"}`}>
                  <span style={S.num}>{String(i + 1).padStart(2, "0")}</span>
                  <span style={S.nombre}>{a.nombre}</span>
                  <span style={S.marca(m)}>{m === "presente" ? "P" : m === "tarde" ? "T" : "—"}</span>
                </button>
              </li>
            );
          })}
        </ul>
      )}

      {aviso && <p style={S.aviso} role="status">{aviso}</p>}

      <button type="button" style={S.guardar} disabled={guardando || cargando} onClick={guardar}>
        {guardando ? "Guardando…" : `Guardar · ${cuenta.p} P · ${cuenta.t} T · ${cuenta.a} A`}
      </button>
    </section>
  );
}

function pest(activa: boolean): React.CSSProperties {
  return {
    padding: "5px 10px", borderRadius: 99, cursor: "pointer",
    fontFamily: "inherit", fontSize: 12.5, fontWeight: activa ? 600 : 400,
    border: `1px solid ${activa ? "var(--aqua)" : "var(--linea)"}`,
    background: activa ? "color-mix(in srgb, var(--aqua) 18%, transparent)" : "transparent",
    color: activa ? "var(--tx)" : "var(--tx-2)",
  };
}

const S = {
  marco: { border: "1px solid var(--linea)", borderRadius: 14, padding: 16,
           background: "var(--panel)" } as React.CSSProperties,
  marcoCompacto: { marginTop: 10 } as React.CSSProperties,
  mandos: { display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center",
            justifyContent: "space-between" } as React.CSSProperties,
  grupo: { display: "flex", flexWrap: "wrap", gap: 4 } as React.CSSProperties,
  fecha: { padding: "5px 8px", borderRadius: 8, border: "1px solid var(--linea)",
           background: "var(--fondo)", color: "var(--tx)", fontFamily: "inherit",
           fontSize: 12.5 } as React.CSSProperties,
  cuenta: { margin: "12px 0 0", fontFamily: "ui-monospace,Menlo,monospace",
            fontSize: 13 } as React.CSSProperties,
  atajos: { display: "flex", gap: 8, margin: "10px 0 0" } as React.CSSProperties,
  suave: { padding: "6px 11px", borderRadius: 8, cursor: "pointer", fontFamily: "inherit",
           fontSize: 12.5, border: "1px solid var(--linea)", background: "transparent",
           color: "var(--tx-2)" } as React.CSSProperties,
  lista: { listStyle: "none", margin: "12px 0 0", padding: 0,
           display: "grid", gap: 4 } as React.CSSProperties,
  // Botones altos: esto se usa de pie, con una mano y con la clase entrando.
  fila: (m?: Marca): React.CSSProperties => ({
    display: "flex", alignItems: "center", gap: 10, width: "100%", textAlign: "left",
    padding: "12px 12px", borderRadius: 9, cursor: "pointer", fontFamily: "inherit", fontSize: 15,
    border: `1px solid ${m === "presente" ? "#7CD9A6" : m === "tarde" ? "#E8B45A" : "var(--linea)"}`,
    background: m === "presente" ? "rgba(124,217,166,.13)"
              : m === "tarde" ? "rgba(232,180,90,.13)" : "var(--fondo)",
    color: "var(--tx)",
  }),
  num: { fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11,
         color: "var(--mut)", minWidth: 20 } as React.CSSProperties,
  nombre: { flex: 1, lineHeight: 1.3 } as React.CSSProperties,
  // La letra, no solo el color: en un proyector y con daltonismo el color solo
  // no distingue nada.
  marca: (m?: Marca): React.CSSProperties => ({
    fontFamily: "ui-monospace,Menlo,monospace", fontSize: 15, fontWeight: 700,
    minWidth: 18, textAlign: "center",
    color: m === "presente" ? "#7CD9A6" : m === "tarde" ? "#E8B45A" : "var(--mut)",
  }),
  vacio: { margin: "14px 0 0", fontSize: 14, color: "var(--tx-2)" } as React.CSSProperties,
  aviso: { margin: "12px 0 0", fontSize: 13.5, color: "var(--aqua)" } as React.CSSProperties,
  guardar: { marginTop: 14, width: "100%", padding: "13px 16px", borderRadius: 10, border: 0,
             background: "var(--aqua)", color: "var(--fondo)", cursor: "pointer",
             fontFamily: "inherit", fontSize: 15, fontWeight: 600 } as React.CSSProperties,
};

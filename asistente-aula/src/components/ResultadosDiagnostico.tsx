"use client";
import { useMemo, useState } from "react";
import type { Pregunta } from "@/lib/contenido";

/**
 * Las respuestas del diagnóstico, en dos vistas.
 *
 * **Global** responde «¿cómo está el grupo?»: cuántos tienen laptop, cuántos
 * ya vieron Scratch. Es con lo que se decide qué se da la semana que viene.
 *
 * **Por nombre** responde «¿y este?»: las dieciséis respuestas de una persona,
 * juntas. Es con lo que se decide a quién sentar al lado de quién y a quién
 * hay que dar una salida distinta porque en su casa no hay internet.
 *
 * Las dos hacen falta y ninguna sustituye a la otra: un promedio esconde
 * justo al que se estaba buscando, y una lista de fichas sueltas no deja ver
 * si el problema es de uno o de veinte.
 *
 * Es un componente de cliente aunque no escriba nada: filtrar por sección y
 * buscar un nombre son cosas que tienen que pasar al instante, y volver al
 * servidor por cada tecla para leer filas que ya están en la página sería
 * pagar una vuelta de red por nada.
 */
type Fila = {
  id: string;
  creado_en: string;
  nombre: string;
  seccion: string;
  respuestas: Record<string, string | string[]>;
};

const TODAS = "Todas";

/** Lo que marcó alguien en una pregunta, siempre como lista. */
function marcado(f: Fila, id: string): string[] {
  const v = f.respuestas?.[id];
  if (Array.isArray(v)) return v.filter(Boolean);
  return v ? [String(v)] : [];
}

export function ResultadosDiagnostico({
  filas, preguntas, secciones,
}: { filas: Fila[]; preguntas: Pregunta[]; secciones: string[] }) {
  const [vista, setVista] = useState<"global" | "nombres">("global");
  const [seccion, setSeccion] = useState(TODAS);
  const [busca, setBusca] = useState("");

  const visibles = useMemo(
    () => (seccion === TODAS ? filas : filas.filter((f) => f.seccion === seccion)),
    [filas, seccion],
  );

  const porSeccion = useMemo(() => {
    const m = new Map<string, number>();
    for (const f of filas) m.set(f.seccion, (m.get(f.seccion) ?? 0) + 1);
    return m;
  }, [filas]);

  if (filas.length === 0) {
    return <p style={S.vacio}>Todavía no ha respondido nadie.</p>;
  }

  return (
    <section>
      <div style={S.mandos}>
        <div style={S.grupo} role="group" aria-label="Vista">
          {(["global", "nombres"] as const).map((v) => (
            <button key={v} type="button" style={pest(vista === v)}
                    onClick={() => setVista(v)}>
              {v === "global" ? "Global" : "Por nombre"}
            </button>
          ))}
        </div>
        <div style={S.grupo} role="group" aria-label="Sección">
          {[TODAS, ...secciones.filter((s) => porSeccion.has(s))].map((s) => (
            <button key={s} type="button" style={pest(seccion === s)}
                    onClick={() => setSeccion(s)}>
              {s}
              <span style={S.badge}>{s === TODAS ? filas.length : porSeccion.get(s)}</span>
            </button>
          ))}
        </div>
      </div>

      <p style={S.resumen}>
        {visibles.length} {visibles.length === 1 ? "respuesta" : "respuestas"}
        {seccion === TODAS && ` · ${porSeccion.size} ${porSeccion.size === 1 ? "sección" : "secciones"}`}
      </p>

      {vista === "global"
        ? <Global filas={visibles} preguntas={preguntas} />
        : <PorNombre filas={visibles} preguntas={preguntas}
                     busca={busca} setBusca={setBusca} />}
    </section>
  );
}

// ─── Global ────────────────────────────────────────────────────────────

function Global({ filas, preguntas }: { filas: Fila[]; preguntas: Pregunta[] }) {
  return (
    <>
      {preguntas.map((p, i) => {
        if (p.tipo === "texto") {
          const dichos = filas
            .map((f) => ({ txt: marcado(f, p.id)[0]?.trim(), quien: f.nombre }))
            .filter((x) => x.txt);
          return (
            <div key={p.id} style={S.bloque}>
              <p style={S.pregunta}><span style={S.num}>{i + 1}</span>{p.texto}</p>
              {dichos.length === 0
                ? <p style={S.nadie}>Sin respuestas.</p>
                : <ul style={S.textos}>
                    {dichos.map((d, k) => (
                      <li key={k} style={S.dicho}>
                        <span>{d.txt}</span>
                        <span style={S.quien}>{d.quien}</span>
                      </li>
                    ))}
                  </ul>}
            </div>
          );
        }

        const conteo = new Map<string, number>();
        // Se cuentan también las opciones que nadie marcó: un cero es un dato.
        // «Ninguno todavía: 0» y «esa opción no aparece» no significan lo mismo.
        for (const op of p.opciones) conteo.set(op, 0);
        for (const f of filas) {
          for (const x of marcado(f, p.id)) conteo.set(x, (conteo.get(x) ?? 0) + 1);
        }
        const sinResponder = filas.filter((f) => marcado(f, p.id).length === 0).length;
        const orden = [...conteo.entries()].sort((a, b) => b[1] - a[1]);
        const base = Math.max(1, filas.length);

        return (
          <div key={p.id} style={S.bloque}>
            <p style={S.pregunta}>
              <span style={S.num}>{i + 1}</span>{p.texto}
              {p.tipo === "varias" && <span style={S.multi}>varias</span>}
            </p>
            <ul style={S.lista}>
              {orden.map(([op, n]) => (
                <li key={op} style={{ ...S.item, opacity: n === 0 ? 0.45 : 1 }}>
                  <span style={{ ...S.barra, width: `${(n / base) * 100}%` }} />
                  <span style={S.op}>{op}</span>
                  <b style={S.n}>{n}</b>
                  <span style={S.pc}>{Math.round((n / base) * 100)}%</span>
                </li>
              ))}
            </ul>
            {sinResponder > 0 && (
              <p style={S.nadie}>{sinResponder} sin responder</p>
            )}
          </div>
        );
      })}
    </>
  );
}

// ─── Por nombre ────────────────────────────────────────────────────────

function PorNombre({
  filas, preguntas, busca, setBusca,
}: { filas: Fila[]; preguntas: Pregunta[]; busca: string; setBusca: (v: string) => void }) {
  const q = busca.trim().toLowerCase();
  const lista = useMemo(
    () => filas
      .filter((f) => !q || f.nombre.toLowerCase().includes(q))
      .sort((a, b) => a.seccion.localeCompare(b.seccion) || a.nombre.localeCompare(b.nombre)),
    [filas, q],
  );

  return (
    <>
      <input
        style={S.buscar}
        value={busca}
        onChange={(e) => setBusca(e.target.value)}
        placeholder="Buscar un nombre"
        aria-label="Buscar un nombre"
      />
      {lista.length === 0 && <p style={S.nadie}>Nadie con ese nombre.</p>}
      {lista.map((f) => (
        <details key={f.id} style={S.ficha}>
          <summary style={S.cabezaFicha}>
            <span style={S.nombreFicha}>{f.nombre}</span>
            <span style={S.secFicha}>{f.seccion}</span>
            <span style={S.horaFicha}>
              {new Date(f.creado_en).toLocaleString("es-DO",
                { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" })}
            </span>
          </summary>
          <dl style={S.dl}>
            {preguntas.map((p, i) => {
              const v = marcado(f, p.id);
              return (
                <div key={p.id} style={S.par}>
                  <dt style={S.dt}><span style={S.num}>{i + 1}</span>{p.texto}</dt>
                  <dd style={S.dd}>
                    {v.length === 0
                      ? <span style={S.sin}>sin responder</span>
                      : v.map((x) => <span key={x} style={S.valor}>{x}</span>)}
                  </dd>
                </div>
              );
            })}
          </dl>
        </details>
      ))}
    </>
  );
}

/** La pestaña activa, en el mismo tono que las de la sala. */
function pest(activa: boolean): React.CSSProperties {
  return {
    display: "flex", alignItems: "center", gap: 7, padding: "7px 12px", fontSize: 13.5,
    borderRadius: 99, cursor: "pointer", fontFamily: "inherit", fontWeight: activa ? 600 : 400,
    border: `1px solid ${activa ? "var(--aqua)" : "var(--linea)"}`,
    background: activa ? "color-mix(in srgb, var(--aqua) 18%, transparent)" : "transparent",
    color: activa ? "var(--tx)" : "var(--tx-2)",
  };
}

const S: Record<string, React.CSSProperties> = {
  vacio: { marginTop: 30, color: "var(--tx-2)", fontSize: 15 },
  mandos: { marginTop: 30, display: "flex", flexWrap: "wrap", gap: 14,
            justifyContent: "space-between", alignItems: "center" },
  grupo: { display: "flex", flexWrap: "wrap", gap: 6 },
  badge: { fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11, color: "var(--mut)" },
  resumen: { margin: "16px 0 0", fontSize: 13, color: "var(--mut)",
             fontFamily: "ui-monospace,Menlo,monospace" },

  bloque: { marginTop: 26, paddingTop: 18, borderTop: "1px solid var(--linea)" },
  pregunta: { margin: 0, fontSize: 14.5, fontWeight: 600, display: "flex",
              alignItems: "baseline", gap: 8, lineHeight: 1.35 },
  num: { fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5,
         color: "var(--mut)", flexShrink: 0 },
  multi: { fontSize: 11, color: "var(--mut)", fontWeight: 400,
           border: "1px solid var(--linea)", borderRadius: 99, padding: "1px 7px" },
  lista: { listStyle: "none", margin: "10px 0 0", padding: 0, display: "grid", gap: 4 },
  item: { position: "relative", display: "flex", alignItems: "center", gap: 10,
          padding: "8px 11px", borderRadius: 7, background: "var(--panel)", overflow: "hidden" },
  barra: { position: "absolute", inset: "0 auto 0 0", background: "var(--aqua)", opacity: 0.22 },
  op: { position: "relative", fontSize: 13.5, flex: 1 },
  n: { position: "relative", fontFamily: "ui-monospace,Menlo,monospace", fontSize: 12.5 },
  pc: { position: "relative", fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5,
        color: "var(--mut)", minWidth: 34, textAlign: "right" },
  nadie: { margin: "8px 0 0", fontSize: 12.5, color: "var(--mut)" },
  textos: { listStyle: "none", margin: "10px 0 0", padding: 0, display: "grid", gap: 4 },
  dicho: { display: "flex", gap: 10, alignItems: "baseline", justifyContent: "space-between",
           padding: "8px 11px", borderRadius: 7, background: "var(--panel)", fontSize: 13.5 },
  quien: { fontSize: 11.5, color: "var(--mut)", flexShrink: 0 },

  buscar: { marginTop: 16, width: "100%", padding: "11px 14px", fontSize: 15,
            borderRadius: 10, border: "1px solid var(--linea)", background: "var(--panel)",
            color: "var(--tx)", fontFamily: "inherit" },
  ficha: { marginTop: 8, border: "1px solid var(--linea)", borderRadius: 10,
           background: "var(--panel)" },
  cabezaFicha: { cursor: "pointer", display: "flex", alignItems: "baseline", gap: 10,
                 padding: "12px 14px", fontSize: 14.5 },
  nombreFicha: { fontWeight: 600 },
  secFicha: { fontSize: 12, color: "var(--aqua)",
              fontFamily: "ui-monospace,Menlo,monospace" },
  horaFicha: { marginLeft: "auto", fontSize: 11.5, color: "var(--mut)",
               fontFamily: "ui-monospace,Menlo,monospace" },
  dl: { margin: 0, padding: "0 14px 14px", display: "grid", gap: 12 },
  par: { display: "grid", gap: 5 },
  dt: { fontSize: 12.5, color: "var(--tx-2)", display: "flex", gap: 8,
        alignItems: "baseline", lineHeight: 1.35 },
  dd: { margin: 0, display: "flex", flexWrap: "wrap", gap: 5 },
  valor: { fontSize: 13.5, padding: "4px 10px", borderRadius: 99,
           background: "color-mix(in srgb, var(--aqua) 14%, transparent)",
           border: "1px solid var(--linea)" },
  sin: { fontSize: 12.5, color: "var(--mut)", fontStyle: "italic" },
};

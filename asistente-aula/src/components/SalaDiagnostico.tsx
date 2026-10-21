"use client";
import { useCallback, useEffect, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";

/**
 * La sala de espera, desde el lado del docente.
 *
 * Abre la sala de una sección, ve llegar los nombres y decide cuándo se
 * empieza. Es lo único que el docente controla: pasado el arranque, cada
 * estudiante responde a su ritmo.
 *
 * Escribe con la clave anónima y la sesión de docente, igual que lee la
 * asistencia: la cookie viaja con la petición y la RLS deja pasar a quien
 * cumple `is_teacher()`. Por eso no hace falta ningún endpoint nuevo ni la
 * clave de servicio en el navegador.
 *
 * Aquí los nombres salen enteros. Los estudiantes se ven entre ellos
 * abreviados —«Ana M.»— porque esa lista la sirve una función accesible sin
 * sesión; esta consulta va contra la tabla, y para hablar con cada uno después
 * hace falta el apellido.
 */
type Estado = "cerrada" | "espera" | "abierta";
type Presente = { id: string; nombre: string; entro_en: string };

const SONDEO = 2000;
const RECUERDA = "sala-seccion";

export function SalaDiagnostico({ secciones }: { secciones: string[] }) {
  const [seccion, setSeccion] = useState(secciones[0] ?? "");
  const [salas, setSalas] = useState<Record<string, Estado>>({});
  const [gente, setGente] = useState<Presente[]>([]);
  const [error, setError] = useState("");
  const estado: Estado = salas[seccion] ?? "cerrada";

  // La misma sección casi siempre durante una hora entera; y si se recarga la
  // página en mitad de la clase, no se vuelve a 1ro A por sorpresa.
  useEffect(() => {
    try {
      const s = localStorage.getItem(RECUERDA);
      if (s && secciones.includes(s)) setSeccion(s);
    } catch {}
  }, [secciones]);

  const mirar = useCallback(async () => {
    if (!seccion || document.visibilityState === "hidden") return;
    const sb = supabaseNavegador();
    const [s, g] = await Promise.all([
      sb.from("diagnostico_sala").select("seccion,estado"),
      sb.from("diagnostico_presente").select("id,nombre,entro_en")
        .eq("seccion", seccion).order("entro_en"),
    ]);
    if (s.data) {
      setSalas(Object.fromEntries(
        (s.data as { seccion: string; estado: Estado }[]).map((r) => [r.seccion, r.estado])));
    }
    if (g.data) setGente(g.data as Presente[]);
    setError(s.error?.message ?? g.error?.message ?? "");
  }, [seccion]);

  useEffect(() => {
    void mirar();
    const reloj = setInterval(mirar, SONDEO);
    document.addEventListener("visibilitychange", mirar);
    return () => {
      clearInterval(reloj);
      document.removeEventListener("visibilitychange", mirar);
    };
  }, [mirar]);

  async function poner(nuevo: Estado, vaciar = false) {
    const sb = supabaseNavegador();
    if (vaciar) await sb.from("diagnostico_presente").delete().eq("seccion", seccion);
    const { error: e } = await sb.from("diagnostico_sala")
      .update({ estado: nuevo, actualizado_en: new Date().toISOString() })
      .eq("seccion", seccion);
    if (e) setError(e.message);
    else { setSalas((v) => ({ ...v, [seccion]: nuevo })); void mirar(); }
  }

  async function sacar(id: string) {
    await supabaseNavegador().from("diagnostico_presente").delete().eq("id", id);
    setGente((g) => g.filter((x) => x.id !== id));
  }

  const abiertas = secciones.filter((s) => (salas[s] ?? "cerrada") !== "cerrada" && s !== seccion);

  return (
    <section style={S.marco}>
      <div style={S.fila}>
        {secciones.map((s) => {
          const activa = s === seccion;
          const viva = (salas[s] ?? "cerrada") !== "cerrada";
          return (
            <button key={s} type="button" style={S.pestana(activa, viva)}
                    onClick={() => {
                      setSeccion(s); setGente([]);
                      try { localStorage.setItem(RECUERDA, s); } catch {}
                    }}>
              {viva && <span style={S.vivo} aria-hidden="true" />}
              {s}
            </button>
          );
        })}
      </div>

      <div style={S.tablero}>
        <div>
          <p style={S.rotulo}>{ROTULO[estado]}</p>
          <p style={S.cifra}>{gente.length}</p>
          <p style={S.pieCifra}>
            {estado === "cerrada"
              ? "la sala está cerrada"
              : gente.length === 1 ? "persona dentro" : "personas dentro"}
          </p>
        </div>

        <div style={S.botones}>
          {estado === "cerrada" && (
            <button type="button" style={S.principal} onClick={() => poner("espera", true)}>
              Abrir sala
            </button>
          )}
          {estado === "espera" && (
            <>
              <button type="button" style={S.principal} onClick={() => poner("abierta")}>
                Empezar
              </button>
              <button type="button" style={S.suave} onClick={() => poner("cerrada")}>
                Cerrar
              </button>
            </>
          )}
          {estado === "abierta" && (
            <>
              <p style={S.nota}>Ya están respondiendo.</p>
              <button type="button" style={S.suave} onClick={() => poner("cerrada")}>
                Cerrar la entrada
              </button>
            </>
          )}
          {estado === "cerrada" && gente.length > 0 && (
            <p style={S.nota}>Al abrir se vacía la lista anterior.</p>
          )}
        </div>
      </div>

      {abiertas.length > 0 && (
        <p style={S.aviso}>
          Sigue abierta la sala de {abiertas.join(", ")}. Ciérrala cuando termine esa clase.
        </p>
      )}
      {error && <p style={S.error}>{error}</p>}

      {gente.length > 0 && (
        <ul style={S.lista}>
          {gente.map((g) => (
            <li key={g.id} style={S.persona}>
              <span>{g.nombre}</span>
              <span style={S.hora}>
                {new Date(g.entro_en).toLocaleTimeString("es-DO",
                  { hour: "2-digit", minute: "2-digit" })}
              </span>
              <button type="button" style={S.sacar} onClick={() => sacar(g.id)}
                      title={`Sacar a ${g.nombre} de la sala`} aria-label={`Sacar a ${g.nombre}`}>
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

const ROTULO: Record<Estado, string> = {
  cerrada: "CERRADA",
  espera: "ENTRANDO",
  abierta: "EN MARCHA",
};

const S = {
  marco: { border: "1px solid var(--linea)", borderRadius: 14, padding: "18px 18px 20px",
           background: "var(--panel)" } as React.CSSProperties,
  fila: { display: "flex", flexWrap: "wrap", gap: 6 } as React.CSSProperties,
  pestana: (activa: boolean, viva: boolean): React.CSSProperties => ({
    display: "flex", alignItems: "center", gap: 6, padding: "7px 12px", fontSize: 13.5,
    borderRadius: 99, cursor: "pointer", fontFamily: "inherit", fontWeight: activa ? 600 : 400,
    border: `1px solid ${activa ? "var(--aqua)" : "var(--linea)"}`,
    background: activa ? "color-mix(in srgb, var(--aqua) 18%, transparent)" : "transparent",
    color: viva && !activa ? "var(--tx)" : "var(--tx-2)",
  }),
  vivo: { width: 6, height: 6, borderRadius: 99, background: "var(--aqua)" } as React.CSSProperties,
  tablero: { marginTop: 18, display: "flex", flexWrap: "wrap", gap: 18,
             alignItems: "flex-end", justifyContent: "space-between" } as React.CSSProperties,
  rotulo: { margin: 0, fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5,
            letterSpacing: ".14em", color: "var(--aqua)" } as React.CSSProperties,
  cifra: { margin: "4px 0 0", fontSize: 52, lineHeight: 1, fontWeight: 800,
           letterSpacing: "-.04em", fontVariantNumeric: "tabular-nums" } as React.CSSProperties,
  pieCifra: { margin: "4px 0 0", fontSize: 13, color: "var(--tx-2)" } as React.CSSProperties,
  botones: { display: "flex", flexWrap: "wrap", gap: 8, alignItems: "center" } as React.CSSProperties,
  principal: { padding: "12px 22px", fontSize: 15, fontWeight: 600, borderRadius: 10, border: 0,
               background: "var(--aqua)", color: "var(--fondo)", cursor: "pointer",
               fontFamily: "inherit" } as React.CSSProperties,
  suave: { padding: "12px 16px", fontSize: 14, borderRadius: 10, cursor: "pointer",
           border: "1px solid var(--linea)", background: "transparent",
           color: "var(--tx-2)", fontFamily: "inherit" } as React.CSSProperties,
  nota: { margin: 0, fontSize: 12.5, color: "var(--mut)" } as React.CSSProperties,
  aviso: { marginTop: 14, fontSize: 13, color: "var(--tx-2)" } as React.CSSProperties,
  error: { marginTop: 12, fontSize: 13, color: "var(--rojo)" } as React.CSSProperties,
  lista: { listStyle: "none", margin: "18px 0 0", padding: 0,
           display: "grid", gap: 4 } as React.CSSProperties,
  persona: { display: "flex", alignItems: "center", gap: 10, fontSize: 14,
             padding: "7px 0", borderBottom: "1px solid var(--linea)" } as React.CSSProperties,
  hora: { marginLeft: "auto", fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5,
          color: "var(--mut)" } as React.CSSProperties,
  sacar: { border: 0, background: "transparent", color: "var(--mut)", cursor: "pointer",
           fontSize: 17, lineHeight: 1, padding: "0 2px" } as React.CSSProperties,
};

"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import type { Diagnostico as Datos } from "@/lib/contenido";

/**
 * El diagnóstico de entrada, tal como lo ve el estudiante.
 *
 * Tres fases. En `quien` dice quién es y entra en la sala de su sección; en
 * `sala` espera, viendo llegar a los demás; en `preguntas` responde.
 *
 * Una pregunta por pantalla y no un formulario largo. Con diez preguntas en una
 * sola página, en un teléfono, la mitad abandona a la cuarta; de una en una se
 * ve el final desde el principio y cada paso cuesta un toque.
 *
 * ─── Por qué hay sala ───
 * Sin ella, quien encuentra el QR primero va por la sexta pregunta mientras
 * otro sigue buscando el enlace, y el docente no sabe si están todos hasta que
 * empiezan a llegar respuestas. Con ella, se empieza a la vez.
 *
 * ─── Qué toca de la base y qué no ───
 * La sala va por dos funciones (`sala_entrar`, `sala_estado`): la clave anónima
 * no tiene permiso sobre las tablas, así que desde aquí no se puede sacar la
 * lista de ninguna sección que no esté abierta ahora mismo. Las respuestas sí
 * se insertan directas en `diagnostico`, que admite altas anónimas y no admite
 * lecturas: ni este componente ni la consola del navegador pueden leer una fila.
 */
type Respuestas = Record<string, string | string[]>;
type EstadoSala = { estado: "cerrada" | "espera" | "abierta"; total: number; nombres: string[] };

const GUARDADO = "diagnostico-sala";   // para que recargar no cueste reescribir el nombre
const SONDEO = 3000;                   // en la sala, mirando si ya empezamos
const REINTENTO = 4000;                // esperando a que el docente abra

const A = {
  velo: { position: "fixed", inset: 0, overflowY: "auto",
          background: "var(--fondo)" } as React.CSSProperties,
  caja: { maxWidth: 640, margin: "0 auto", padding: "28px 20px 64px",
          minHeight: "100dvh", display: "flex", flexDirection: "column" } as React.CSSProperties,
  barra: { height: 4, background: "var(--linea)", borderRadius: 99, overflow: "hidden" },
  avance: { height: "100%", background: "var(--aqua)", transition: "width .32s cubic-bezier(.4,0,.2,1)" },
  paso: { marginTop: 10, fontFamily: "ui-monospace,Menlo,monospace", fontSize: 12,
          letterSpacing: ".1em", color: "var(--mut)" },
  titulo: { margin: "26px 0 0", fontSize: "clamp(23px,5.4vw,34px)", lineHeight: 1.18,
            fontWeight: 700, letterSpacing: "-.02em" } as React.CSSProperties,
  ayuda: { marginTop: 10, fontSize: 14.5, color: "var(--tx-2)", lineHeight: 1.5 },
  ops: { marginTop: 22, display: "grid", gap: 9 } as React.CSSProperties,
  campo: { width: "100%", padding: "15px 16px", fontSize: 16, borderRadius: 12,
           border: "1px solid var(--linea)", background: "var(--panel)",
           color: "var(--tx)", fontFamily: "inherit" } as React.CSSProperties,
  pie: { marginTop: "auto", paddingTop: 26, display: "flex", gap: 10, alignItems: "center" },
  seguir: { flex: 1, padding: "15px 18px", fontSize: 16, fontWeight: 600, borderRadius: 12,
            border: 0, background: "var(--aqua)", color: "var(--fondo)", cursor: "pointer" },
  atras: { padding: "15px 16px", fontSize: 15, borderRadius: 12, cursor: "pointer",
           border: "1px solid var(--linea)", background: "transparent", color: "var(--tx-2)" },
  error: { marginTop: 14, fontSize: 14, color: "var(--rojo)" },

  // La sala
  cuenta: { fontSize: "clamp(56px,17vw,92px)", lineHeight: 1, fontWeight: 800,
            letterSpacing: "-.04em", color: "var(--aqua)", margin: "26px 0 0",
            fontVariantNumeric: "tabular-nums" } as React.CSSProperties,
  cuentaPie: { margin: "6px 0 0", fontSize: 14, color: "var(--tx-2)" },
  fichas: { marginTop: 24, display: "flex", flexWrap: "wrap", gap: 8 } as React.CSSProperties,
  ficha: { padding: "8px 13px", borderRadius: 99, fontSize: 14.5, background: "var(--panel)",
           border: "1px solid var(--linea)" } as React.CSSProperties,
  yo: { borderColor: "var(--aqua)", background: "color-mix(in srgb, var(--aqua) 16%, transparent)",
        fontWeight: 600 } as React.CSSProperties,
  // Pegado a las fichas y no al fondo de la pantalla: con cinco personas
  // dentro, empujarlo abajo deja tres cuartos de móvil en blanco y la sala
  // parece rota justo cuando más gente está mirando si funciona.
  espera: { marginTop: 30, display: "flex", alignItems: "center", gap: 10,
            fontSize: 14.5, color: "var(--tx-2)" } as React.CSSProperties,
  punto: { width: 7, height: 7, borderRadius: 99, background: "var(--aqua)",
           animation: "late 1.4s ease-in-out infinite" } as React.CSSProperties,
};

function opcion(activa: boolean): React.CSSProperties {
  return {
    display: "flex", alignItems: "center", gap: 12, width: "100%", textAlign: "left",
    padding: "14px 16px", fontSize: 16, lineHeight: 1.35, borderRadius: 12, cursor: "pointer",
    border: `1px solid ${activa ? "var(--aqua)" : "var(--linea)"}`,
    background: activa ? "color-mix(in srgb, var(--aqua) 16%, transparent)" : "var(--panel)",
    color: "var(--tx)", transition: "border-color .14s, background .14s",
  };
}

/** «Ana María Pérez» → «Ana M.», igual que lo abrevia la base. */
function corto(n: string): string {
  const p = n.trim().split(/\s+/);
  if (p.length < 2) return p[0] ?? "";
  return `${p[0][0].toUpperCase()}${p[0].slice(1)} ${p[1][0].toUpperCase()}.`;
}

export function Diagnostico({ datos, curso }: { datos: Datos; curso?: string }) {
  // El curso llega por la URL del QR proyectado, así que solo se ofrecen sus
  // tres secciones: en un aula de 1ro nadie tiene que ver las de 3ro.
  //
  // Memorizado, y no es un adorno: `filter` devuelve un array nuevo en cada
  // render, y un array nuevo hace que los efectos que dependen de él se
  // vuelvan a ejecutar en bucle.
  const secciones = useMemo(
    () => (curso ? datos.secciones.filter((s) => s.startsWith(curso)) : datos.secciones),
    [curso, datos.secciones],
  );

  const [fase, setFase] = useState<"quien" | "sala" | "preguntas">("quien");
  const [i, setI] = useState(0);                 // 0 = quién eres
  const [nombre, setNombre] = useState("");
  const [seccion, setSeccion] = useState(secciones.length === 1 ? secciones[0] : "");
  const [sala, setSala] = useState<EstadoSala>({ estado: "cerrada", total: 0, nombres: [] });
  const [resp, setResp] = useState<Respuestas>({});
  const [entrando, setEntrando] = useState(false);
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState("");
  const [listo, setListo] = useState(false);

  const total = datos.preguntas.length + 1;
  const p = i > 0 ? datos.preguntas[i - 1] : null;
  const yo = corto(nombre);

  function marcar(op: string) {
    if (!p) return;
    setResp((r) => {
      if (p.tipo === "una") return { ...r, [p.id]: op };
      const ya = Array.isArray(r[p.id]) ? (r[p.id] as string[]) : [];
      return { ...r, [p.id]: ya.includes(op) ? ya.filter((x) => x !== op) : [...ya, op] };
    });
  }

  function elegida(op: string) {
    if (!p) return false;
    const v = resp[p.id];
    return Array.isArray(v) ? v.includes(op) : v === op;
  }

  // Se puede seguir sin responder: obligar a contestar «¿en casa te revisan?»
  // es la forma más rápida de que alguien marque cualquier cosa por salir.
  //
  // El nombre y la sección sí hacen falta, pero el botón no se desactiva por
  // eso: un botón apagado sin explicación es un callejón, se pulsa, no pasa
  // nada y no hay forma de saber qué se espera. Se deja pulsable y se dice qué
  // falta, que es lo único que el que está atascado necesita saber.
  function queFalta() {
    if (nombre.trim().length < 2) return "Escribe tu nombre para empezar.";
    if (!seccion) return "Elige tu sección.";
    return "";
  }

  /**
   * Entrar en la sala.
   *
   * `callado` es para los reintentos automáticos: mientras el docente no abre,
   * esto se llama solo cada cuatro segundos y no tendría sentido que la
   * pantalla parpadeara en cada intento fallido.
   */
  const entrar = useCallback(
    async (nom: string, sec: string, callado = false) => {
      if (!callado) setEntrando(true);
      const sb = supabaseNavegador();
      const { error: e } = await sb.rpc("sala_entrar", { p_seccion: sec, p_nombre: nom });
      if (!callado) setEntrando(false);

      if (e) {
        if (e.message.includes("sala_cerrada")) {
          setError(`Tu profe todavía no ha abierto la sala de ${sec}. Espera un momento, esto lo intenta solo.`);
        } else if (e.message.includes("sala_llena")) {
          setError("La sala está llena. Avisa al profe.");
        } else if (!callado) {
          setError("No se pudo entrar. Revisa la conexión y vuelve a intentarlo.");
        }
        return false;
      }

      setError("");
      try { sessionStorage.setItem(GUARDADO, JSON.stringify({ nombre: nom, seccion: sec })); } catch {}

      // Quien llega tarde, con la sala ya abierta, no se queda esperando solo:
      // pasa directo a la primera pregunta.
      const { data } = await sb.rpc("sala_estado", { p_seccion: sec });
      const est = (data as EstadoSala | null) ?? { estado: "espera", total: 1, nombres: [] };
      setSala(est);
      if (est.estado === "abierta") { setFase("preguntas"); setI(1); }
      else setFase("sala");
      return true;
    },
    [],
  );

  // Recargar no puede costar volver a escribirlo todo: en un teléfono de
  // catorce años la página se recarga sola más de una vez por clase. Volver a
  // entrar con el mismo nombre devuelve la misma persona, no una copia.
  //
  // Una sola vez por carga, y el candado es una referencia y no una
  // dependencia: si esto se repitiera, cada repetición devolvería al
  // estudiante a la pregunta 1 en mitad del cuestionario.
  const restaurado = useRef(false);
  useEffect(() => {
    if (restaurado.current) return;
    restaurado.current = true;
    let guardado: { nombre?: string; seccion?: string } | null = null;
    try { guardado = JSON.parse(sessionStorage.getItem(GUARDADO) ?? "null"); } catch {}
    if (!guardado?.nombre || !guardado?.seccion) return;
    if (!secciones.includes(guardado.seccion)) return;
    setNombre(guardado.nombre);
    setSeccion(guardado.seccion);
    void entrar(guardado.nombre, guardado.seccion, true);
  }, [entrar, secciones]);

  // Mientras espera, mira la sala cada tres segundos. Se para con la pestaña
  // oculta, que en un móvil es la mitad del tiempo, y se mira una vez al
  // volver para no arrastrar los tres segundos de retraso al reaparecer.
  useEffect(() => {
    if (fase !== "sala" || !seccion) return;
    let vivo = true;

    async function mirar() {
      if (document.visibilityState === "hidden") return;
      const { data } = await supabaseNavegador().rpc("sala_estado", { p_seccion: seccion });
      if (!vivo || !data) return;
      const est = data as EstadoSala;
      setSala(est);
      if (est.estado === "abierta") { setFase("preguntas"); setI(1); }
    }

    const reloj = setInterval(mirar, SONDEO);
    document.addEventListener("visibilitychange", mirar);
    return () => {
      vivo = false;
      clearInterval(reloj);
      document.removeEventListener("visibilitychange", mirar);
    };
  }, [fase, seccion]);

  // Con la sala cerrada, reintentar solo. Que nadie se quede pulsando un botón
  // que aún no puede funcionar.
  const cerrada = fase === "quien" && error.includes("todavía no ha abierto");
  useEffect(() => {
    if (!cerrada || !seccion) return;
    const reloj = setInterval(() => { void entrar(nombre, seccion, true); }, REINTENTO);
    return () => clearInterval(reloj);
  }, [cerrada, entrar, nombre, seccion]);

  async function enviar() {
    setEnviando(true);
    setError("");
    const { error: e } = await supabaseNavegador()
      .from("diagnostico")
      .insert({ nombre: nombre.trim().slice(0, 60), seccion, respuestas: resp });
    setEnviando(false);
    if (e) setError("No se pudo enviar. Revisa la conexión y vuelve a intentarlo.");
    else {
      try { sessionStorage.removeItem(GUARDADO); } catch {}
      setListo(true);
    }
  }

  if (listo) {
    return (
      <div style={A.velo}>
        <div style={{ ...A.caja, justifyContent: "center", textAlign: "center" }}>
          <p style={{ fontSize: 52, margin: 0 }} aria-hidden="true">✓</p>
          <h1 style={{ ...A.titulo, marginTop: 16 }}>Listo, {nombre.trim().split(" ")[0]}.</h1>
          <p style={{ ...A.ayuda, maxWidth: 46 + "ch", margin: "14px auto 0" }}>{datos.cierre}</p>
        </div>
      </div>
    );
  }

  // ─── La sala de espera ───────────────────────────────────────────────
  if (fase === "sala") {
    return (
      <div style={A.velo}>
        <div style={A.caja}>
          <p style={{ ...A.paso, marginTop: 0 }}>SALA DE {seccion.toUpperCase()}</p>
          <h1 style={{ ...A.titulo, marginTop: 12 }}>
            Ya estás dentro, {nombre.trim().split(" ")[0]}.
          </h1>
          <p style={A.ayuda}>Empezamos todos a la vez, cuando el profe lo diga.</p>

          <p style={A.cuenta}>{sala.total}</p>
          <p style={A.cuentaPie}>
            {sala.total === 1 ? "eres el primero en llegar" : "en la sala"}
          </p>

          <div style={A.fichas}>
            {sala.nombres.map((n, k) => (
              <span key={`${n}-${k}`}
                    style={{ ...A.ficha, ...(n === yo ? A.yo : null),
                             animation: "entra .3s cubic-bezier(.2,.7,.3,1) both" }}>
                {n}
              </span>
            ))}
          </div>

          <p style={A.espera}>
            <span style={A.punto} aria-hidden="true" />
            Esperando a que empiece…
          </p>
        </div>
        <Animaciones />
      </div>
    );
  }

  // ─── Identificarse y responder ───────────────────────────────────────
  return (
    <div style={A.velo}>
      <div style={A.caja}>
        <div style={A.barra}>
          <div style={{ ...A.avance, width: `${((i + 1) / total) * 100}%` }} />
        </div>
        <p style={A.paso}>{i === 0 ? "ANTES DE EMPEZAR" : `${i} DE ${datos.preguntas.length}`}</p>

        {/* La animación se ata a la pregunta con `key`: al cambiar de índice
            React monta un elemento nuevo y la entrada se reproduce sola. */}
        <div key={i} style={{ animation: "entra .34s cubic-bezier(.2,.7,.3,1) both" }}>
          {i === 0 ? (
            <>
              <h1 style={A.titulo}>¿Quién eres?</h1>
              <p style={A.ayuda}>{datos.intro}</p>
              <div style={A.ops}>
                <input
                  style={A.campo}
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  placeholder="Tu nombre y apellido"
                  maxLength={60}
                  autoComplete="name"
                />
                {secciones.map((s) => (
                  <button key={s} type="button" style={opcion(seccion === s)}
                          onClick={() => setSeccion(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </>
          ) : p ? (
            <>
              <h1 style={A.titulo}>{p.texto}</h1>
              {p.tipo === "varias" && <p style={A.ayuda}>Puedes marcar varias.</p>}
              <div style={A.ops}>
                {p.tipo === "texto" ? (
                  <input
                    style={A.campo}
                    value={(resp[p.id] as string) ?? ""}
                    onChange={(e) => setResp((r) => ({ ...r, [p.id]: e.target.value }))}
                    placeholder="Escribe los que quieras"
                    maxLength={120}
                  />
                ) : (
                  p.opciones.map((op) => (
                    <button key={op} type="button" style={opcion(elegida(op))}
                            aria-pressed={elegida(op)} onClick={() => marcar(op)}>
                      {op}
                    </button>
                  ))
                )}
              </div>
            </>
          ) : null}
        </div>

        {error && (
          <p style={A.error} role="status">
            {error}
          </p>
        )}

        <div style={A.pie}>
          {/* Desde la pregunta 1 no se vuelve a la pantalla del nombre: ya se
              entró en la sala con ese nombre y cambiarlo ahí no cambiaría nada. */}
          {i > 1 && (
            <button type="button" style={A.atras} onClick={() => setI(i - 1)}>
              Atrás
            </button>
          )}
          <button
            type="button"
            style={{ ...A.seguir, opacity: enviando || entrando ? 0.45 : 1 }}
            disabled={enviando || entrando}
            onClick={() => {
              if (i === 0) {
                const falta = queFalta();
                if (falta) return setError(falta);
                setError("");
                void entrar(nombre.trim(), seccion);
                return;
              }
              setError("");
              if (i === datos.preguntas.length) enviar();
              else setI(i + 1);
            }}
          >
            {i === 0
              ? entrando ? "Entrando…" : "Entrar a la sala"
              : enviando ? "Enviando…" : i === datos.preguntas.length ? "Enviar" : "Siguiente"}
          </button>
        </div>
      </div>
      <Animaciones />
    </div>
  );
}

function Animaciones() {
  return (
    <style>{`
      @keyframes entra{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
      @keyframes late{0%,100%{opacity:.25;transform:scale(.8)}50%{opacity:1;transform:scale(1)}}
      @media(prefers-reduced-motion:reduce){
        [style*="entra"],[style*="late"]{animation:none!important}
      }
    `}</style>
  );
}

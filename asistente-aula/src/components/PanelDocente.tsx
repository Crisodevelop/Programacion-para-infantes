"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { useDocente } from "@/lib/supabase/docente";
import { PasarLista } from "@/components/PasarLista";
import { SECCIONES, seccionDeHoy } from "@/lib/horario";

/**
 * El mando del docente sobre la presentación.
 *
 * Se monta siempre —también para los estudiantes— porque el bloqueo es para
 * ellos: es lo que permite parar a treinta personas a la vez mientras se
 * explica algo. Pero solo enseña controles a quien tiene sesión de docente;
 * para el resto no se ve nada y la página queda exactamente como antes.
 *
 * ─── Por qué la lista se pide aquí y no viene en el HTML ───
 * La presentación es pública. Antes la diapositiva «Quiénes son» traía los
 * nombres incrustados, y con 256 menores eso es publicarlos. Ahora el hueco
 * está vacío en la página y solo lo llena esta sesión: la RLS de `lista` no
 * tiene ninguna política para `anon`, así que sin ser docente no llega ni un
 * nombre aunque se pida a mano desde la consola.
 *
 * ─── Una sola sección para todo ───
 * El nivel lo manda la presentación: los botones 1ro/2do/3ro de arriba. Al
 * cambiarlo se elige la sección de ese nivel que toca hoy según el horario, y
 * esa misma sección llena la diapositiva, marca la pestaña del mando y es la
 * que se pasa en el cajón de asistencia. Antes cada sitio recordaba la suya y
 * se podía estar viendo 2do B mientras se pasaba lista a 1ro A.
 */
type Estado = { juegos: boolean; abierta: boolean };
type Alumno = { id: string; nombre: string; seccion: string; agregado: boolean };

const NIVELES = ["1ro", "2do", "3ro"];
const SONDEO = 3000;
const RECUERDA = "panel-seccion";

/**
 * La que toca ahora en ese nivel; si hoy no tiene clase, la última que se usó
 * con él; y si nunca se usó, la A.
 */
function seccionPara(nivel: string): string {
  const hoy = seccionDeHoy(nivel)?.seccion;
  if (hoy) return hoy;
  try {
    const s = localStorage.getItem(`${RECUERDA}:${nivel}`);
    if (s && SECCIONES.includes(s) && s.startsWith(nivel + " ")) return s;
  } catch {}
  return `${nivel} A`;
}

export function PanelDocente(
  { nivel: nivelFijo, respetarCierre = true }: { nivel?: string; respetarCierre?: boolean } = {},
) {
  const docente = useDocente();
  const [estado, setEstado] = useState<Estado>({ juegos: true, abierta: true });
  const [abierto, setAbierto] = useState(false);
  const [nivel, setNivel] = useState("1ro");
  const [seccion, setSeccion] = useState(SECCIONES[0]);
  const [lista, setLista] = useState<Alumno[]>([]);
  const [nuevo, setNuevo] = useState("");
  const [aviso, setAviso] = useState("");
  const [cajon, setCajon] = useState(false);
  const [hueco, setHueco] = useState<HTMLElement | null>(null);
  const [sinHueco, setSinHueco] = useState(false);
  const cajonRef = useRef<HTMLDivElement>(null);

  // ── el bloqueo, que mira todo el mundo ─────────────────────────────
  const mirar = useCallback(async () => {
    if (document.visibilityState === "hidden") return;
    const { data } = await supabaseNavegador()
      .from("presentacion_estado").select("juegos,abierta").eq("id", 1).maybeSingle();
    if (data) setEstado(data as Estado);
  }, []);

  useEffect(() => {
    void mirar();
    const reloj = setInterval(mirar, SONDEO);
    document.addEventListener("visibilitychange", mirar);
    return () => { clearInterval(reloj); document.removeEventListener("visibilitychange", mirar); };
  }, [mirar]);

  // El CSS de la presentación apaga las demos con este atributo, y su JS
  // aprovecha para detener una partida ya empezada.
  useEffect(() => {
    const raiz = document.documentElement;
    const apagar = !estado.juegos && !docente;
    if (apagar) raiz.setAttribute("data-bloqueo", "juegos");
    else raiz.removeAttribute("data-bloqueo");
    return () => raiz.removeAttribute("data-bloqueo");
  }, [estado.juegos, docente]);

  // Marca de docente en <html>: las presentaciones de cada semana la usan para
  // enseñar el botón «Guion», que la clase no necesita ver proyectado.
  useEffect(() => {
    if (!docente) return;
    const raiz = document.documentElement;
    raiz.dataset.docente = "";
    return () => { delete raiz.dataset.docente; };
  }, [docente]);

  // ── el nivel, que lo dicta la presentación ─────────────────────────
  // Nivel y sección cambian en el mismo golpe: si la sección llegara un
  // render después, durante ese render el cajón pediría la lista de la
  // sección vieja con las pestañas del nivel nuevo.
  const aplicarNivel = useCallback((l: string) => {
    if (!NIVELES.includes(l)) return;
    setNivel(l);
    setSeccion(seccionPara(l));
    setAviso("");
  }, []);

  /**
   * El JS de la presentación ya llamó a `setLvl` con lo guardado antes de que
   * corra este efecto, así que el nivel se lee de donde lo dejó: el atributo
   * de <html>, y si no, lo guardado. Desde ahí, cada cambio llega como evento.
   */
  useEffect(() => {
    // En las presentaciones de cada semana el nivel lo fija la ruta: no hay
    // botones 1ro/2do/3ro que escuchar.
    if (nivelFijo) { aplicarNivel(nivelFijo); return; }
    let inicial = document.documentElement.dataset.lvl;
    if (!inicial) {
      try { inicial = localStorage.getItem("deck-lvl") ?? undefined; } catch {}
    }
    aplicarNivel(inicial && NIVELES.includes(inicial) ? inicial : "1ro");

    const oir = (e: Event) => aplicarNivel(String((e as CustomEvent).detail));
    window.addEventListener("deck:nivel", oir);
    return () => window.removeEventListener("deck:nivel", oir);
  }, [aplicarNivel, nivelFijo]);

  function elegir(s: string) {
    setSeccion(s); setAviso("");
    try { localStorage.setItem(`${RECUERDA}:${s.split(" ")[0]}`, s); } catch {}
  }

  // ── la lista, dentro de la diapositiva ─────────────────────────────
  const traer = useCallback(async (sec: string) => {
    const { data } = await supabaseNavegador()
      .from("lista").select("id,nombre,seccion,agregado")
      .eq("seccion", sec).eq("activo", true).order("nombre");
    setLista((data ?? []) as Alumno[]);
  }, []);

  useEffect(() => { if (docente) void traer(seccion); }, [docente, seccion, traer]);

  // Se pinta en el hueco que dejó el generador. Se toca el DOM a mano porque
  // la diapositiva no es React: es HTML generado desde contenido.py.
  useEffect(() => {
    if (!docente) return;
    const nivelSec = seccion.split(" ")[0];
    const caja = document.querySelector<HTMLElement>(`[data-roster="${nivelSec}"]`);
    if (!caja) return;
    if (lista.length === 0) {
      caja.innerHTML = '<p class="conteo">Sin nadie en esta sección todavía.</p>';
      return;
    }
    const filas = lista.map((a, i) =>
      `<li><b>${String(i + 1).padStart(2, "0")}</b><span>${escapar(a.nombre)}</span></li>`).join("");
    caja.innerHTML = `<ul class="roster">${filas}</ul>` +
      `<p class="conteo">${lista.length} en ${escapar(seccion)}</p>`;
    return () => { caja.innerHTML = '<p class="conteo">La lista aparece al entrar con tu cuenta.</p>'; };
  }, [docente, lista, seccion]);

  // ── el botón «Pasar lista», junto a 1ro/2do/3ro ────────────────────
  /**
   * Va en la barra de arriba de la presentación, que no es React: se le cuelga
   * un hueco propio justo después del grupo de niveles y se pinta ahí con un
   * portal. Solo con sesión de docente, así que un estudiante no recibe ni el
   * nodo.
   *
   * `PaginaGenerada` inyecta el HTML en su propio efecto; por si este corre
   * antes, se vuelve a buscar en el siguiente fotograma. Si ni así aparece —
   * otra presentación, otro marcado— el botón queda fijo arriba a la derecha.
   */
  useEffect(() => {
    if (!docente) return;
    let host: HTMLElement | null = null;
    let fotograma = 0;

    const colgar = () => {
      // Las presentaciones de cada semana dejan su propio hueco en la barra.
      const propio = document.querySelector<HTMLElement>("[data-hueco-docente]");
      if (propio) { setHueco(propio); return true; }
      const grupo = document.querySelector<HTMLElement>(".lvlbtn")?.parentElement;
      if (!grupo) return false;
      host = document.createElement("span");
      host.style.display = "flex";
      grupo.after(host);
      setHueco(host);
      return true;
    };

    if (!colgar()) {
      fotograma = requestAnimationFrame(() => { if (!colgar()) setSinHueco(true); });
    }
    return () => {
      cancelAnimationFrame(fotograma);
      host?.remove();
      setHueco(null);
    };
  }, [docente]);

  // ── el cajón: Escape cierra, y las teclas no pasan de diapositiva ──
  /**
   * La presentación escucha el teclado en `document`. Su primer escuchador
   * ignora los campos de texto, pero no los botones —y el cajón es casi todo
   * botones—, y el de los capítulos y el del Snake no ignoran nada: una flecha
   * con el foco en un nombre movía la diapositiva de detrás. Así que en la raíz
   * del cajón se corta la propagación de `keydown`.
   *
   * Es un escuchador nativo y no `onKeyDown` a propósito: React escucha en la
   * raíz del documento, igual que la presentación, y para entonces ya sería
   * tarde. La contrapartida es que un `onKeyDown` de React dentro del cajón no
   * se enteraría; hoy no hay ninguno.
   */
  useEffect(() => {
    if (!cajon) return;
    const raiz = cajonRef.current;
    const conEscape = (e: KeyboardEvent) => { if (e.key === "Escape") setCajon(false); };
    const aislar = (e: KeyboardEvent) => { conEscape(e); e.stopPropagation(); };
    document.addEventListener("keydown", conEscape);
    raiz?.addEventListener("keydown", aislar);
    // Con el foco dentro, las teclas van al cajón y no a la presentación. En
    // Safari tocar un botón no le da el foco, así que se le da a la raíz.
    raiz?.focus();
    return () => {
      document.removeEventListener("keydown", conEscape);
      raiz?.removeEventListener("keydown", aislar);
    };
  }, [cajon]);

  async function agregar() {
    const n = nuevo.trim().replace(/\s+/g, " ");
    if (n.split(" ").length < 2) { setAviso("Escribe nombre y apellido."); return; }
    const partes = n.split(" ");
    const corte = Math.max(1, Math.ceil(partes.length / 2));
    const { error } = await supabaseNavegador().from("lista").insert({
      seccion, nombres: partes.slice(0, corte).join(" "),
      apellidos: partes.slice(corte).join(" "), nombre: n, agregado: true,
    });
    if (error) {
      setAviso(error.code === "23505" ? "Ese nombre ya está en la lista." : "No se pudo guardar.");
      return;
    }
    setNuevo(""); setAviso(`${n} queda en ${seccion}.`);
    void traer(seccion);
  }

  async function poner(cambio: Partial<Estado>) {
    const sb = supabaseNavegador();
    const { error } = await sb.from("presentacion_estado")
      .update({ ...cambio, actualizado_en: new Date().toISOString() }).eq("id", 1);
    if (!error) setEstado((e) => ({ ...e, ...cambio }));
  }

  // ── lo que ve un estudiante con la presentación cerrada ────────────
  if (respetarCierre && !estado.abierta && docente === false) {
    return (
      <div style={S.velo}>
        <p style={S.veloTitulo}>La presentación está cerrada.</p>
        <p style={S.veloTexto}>Se abre en clase. Nos vemos ahí.</p>
      </div>
    );
  }
  if (!docente) return null;

  const boton = (
    <button type="button" style={S.pasar(cajon, !hueco)} aria-expanded={cajon}
            onClick={() => setCajon((v) => !v)}>
      Pasar lista
    </button>
  );

  return (
    <>
      {hueco ? createPortal(boton, hueco) : sinHueco && boton}

      {cajon && (
        <div ref={cajonRef} style={S.cajon} role="dialog" aria-label={`Pasar lista · ${seccion}`}
             tabIndex={-1}>
          <div style={S.fila}>
            <b style={S.cajonTitulo}>Pasar lista · {seccion}</b>
            <button type="button" style={S.cerrar} onClick={() => setCajon(false)}
                    aria-label="Cerrar pasar lista">×</button>
          </div>
          {/* Es el mismo componente que la pantalla de administración: dos
              pantallas que hacen lo mismo acaban siempre con una desactualizada. */}
          <PasarLista compacto nivel={nivel} seccion={seccion} onSeccion={elegir} />
        </div>
      )}

      {abierto && (
        <div style={S.panel}>
          <div style={S.fila}>
            <b style={S.titulo}>Mando</b>
            <button type="button" style={S.cerrar} onClick={() => setAbierto(false)}
                    aria-label="Cerrar el mando">×</button>
          </div>

          <div style={S.grupo} role="group" aria-label="Sección">
            {SECCIONES.filter((s) => s.startsWith(nivel + " ")).map((s) => (
              <button key={s} type="button" style={S.pest(s === seccion)} onClick={() => elegir(s)}>
                {s}
              </button>
            ))}
          </div>

          <p style={S.cuenta}>{lista.length} en la lista</p>
          <div style={S.fila}>
            <input style={S.campo} value={nuevo} maxLength={80}
                   placeholder="Agregar a quien falte" aria-label="Nombre y apellido"
                   onChange={(e) => setNuevo(e.target.value)}
                   onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); void agregar(); } }} />
            <button type="button" style={S.btn} onClick={agregar}>Guardar</button>
          </div>
          {aviso && <p style={S.aviso} role="status">{aviso}</p>}

          <div style={S.linea} />
          {/* Abre el mismo cajón que el botón de arriba: una sola puerta. */}
          <button type="button" style={S.suave} onClick={() => setCajon((v) => !v)}>
            {cajon ? "Cerrar pasar lista" : "Pasar lista"}
          </button>

          <div style={S.linea} />
          <label style={S.check}>
            <input type="checkbox" checked={!estado.juegos}
                   onChange={(e) => poner({ juegos: !e.target.checked })} />
            Apagar los juegos
          </label>
          {respetarCierre && (
            <label style={S.check}>
            <input type="checkbox" checked={!estado.abierta}
                   onChange={(e) => poner({ abierta: !e.target.checked })} />
            Cerrar la presentación
          </label>
          )}
          <p style={S.pie}>Se aplica a todos menos a ti.</p>
        </div>
      )}

      <button type="button" style={S.tirador(!estado.juegos || !estado.abierta)}
              onClick={() => setAbierto((v) => !v)}
              aria-label="Mando del docente">
        {!estado.juegos || !estado.abierta ? "● Bloqueado" : "Mando"}
      </button>
    </>
  );
}

function escapar(s: string): string {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
}

const S = {
  velo: { position: "fixed", inset: 0, zIndex: 2000, display: "grid", alignContent: "center",
          justifyItems: "center", gap: 10, textAlign: "center", padding: 24,
          background: "#070d18", color: "#E7ECF5" } as React.CSSProperties,
  veloTitulo: { margin: 0, fontSize: "clamp(22px,5vw,34px)", fontWeight: 700 } as React.CSSProperties,
  veloTexto: { margin: 0, fontSize: 15, opacity: .66 } as React.CSSProperties,
  tirador: (bloq: boolean): React.CSSProperties => ({
    position: "fixed", left: 22, bottom: 62, zIndex: 1000, padding: "7px 14px",
    fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5, letterSpacing: ".08em",
    borderRadius: 99, cursor: "pointer",
    border: `1px solid ${bloq ? "#F4A4A4" : "rgba(255,255,255,.28)"}`,
    background: bloq ? "rgba(244,164,164,.14)" : "rgba(10,18,32,.72)",
    color: bloq ? "#F4A4A4" : "rgba(255,255,255,.72)", backdropFilter: "blur(6px)",
  }),
  // Mismas medidas que las pastillas de nivel, para que se lea como parte de
  // la fila; con el color del mando, para que se lea como cosa del docente y
  // no como un cuarto nivel. Sin la clase `lvlbtn`: el JS de la presentación
  // recorre esa clase para marcar el nivel activo.
  pasar: (activo: boolean, fijo: boolean): React.CSSProperties => ({
    ...(fijo ? { position: "fixed", top: 20, right: 24, zIndex: 1000 } : {}),
    padding: "6px 12px", borderRadius: 999, cursor: "pointer", whiteSpace: "nowrap",
    fontFamily: "var(--fm, ui-monospace,Menlo,monospace)", fontSize: 12, letterSpacing: ".06em",
    fontWeight: activo ? 600 : 400,
    border: "1px solid #6EC7E0",
    background: activo ? "#6EC7E0" : "rgba(110,199,224,.12)",
    color: activo ? "#070d18" : "#6EC7E0",
  }),
  panel: { position: "fixed", left: 22, bottom: 104, zIndex: 1001, width: 292,
           padding: 14, borderRadius: 12, background: "#0d1830",
           border: "1px solid rgba(255,255,255,.14)", color: "#E7ECF5",
           boxShadow: "0 24px 60px -28px rgba(0,0,0,.9)",
           fontFamily: "system-ui,sans-serif", fontSize: 14, lineHeight: 1.45 } as React.CSSProperties,
  // Por encima de la barra de la presentación (50) y del mando (1001); por
  // debajo del velo de «cerrada», que de todos modos el docente nunca ve.
  cajon: { position: "fixed", top: 0, right: 0, bottom: 0, zIndex: 1002,
           width: "min(420px, 100vw)", overflowY: "auto", overscrollBehavior: "contain",
           padding: "14px 16px 22px", background: "#0d1830", color: "#E7ECF5",
           borderLeft: "1px solid rgba(255,255,255,.14)",
           boxShadow: "-24px 0 60px -28px rgba(0,0,0,.9)", outline: "none",
           fontFamily: "system-ui,sans-serif", fontSize: 14, lineHeight: 1.45 } as React.CSSProperties,
  cajonTitulo: { flex: 1, fontFamily: "ui-monospace,Menlo,monospace", fontSize: 12.5,
                 letterSpacing: ".08em", color: "#6EC7E0" } as React.CSSProperties,
  fila: { display: "flex", gap: 8, alignItems: "center" } as React.CSSProperties,
  titulo: { flex: 1, fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5,
            letterSpacing: ".14em", color: "#6EC7E0" } as React.CSSProperties,
  cerrar: { border: 0, background: "transparent", color: "rgba(255,255,255,.5)",
            fontSize: 18, lineHeight: 1, cursor: "pointer", padding: 0 } as React.CSSProperties,
  grupo: { display: "flex", flexWrap: "wrap", gap: 4, margin: "10px 0 0" } as React.CSSProperties,
  pest: (act: boolean): React.CSSProperties => ({
    padding: "4px 9px", borderRadius: 99, cursor: "pointer",
    fontFamily: "inherit", fontSize: 12, fontWeight: act ? 600 : 400,
    border: `1px solid ${act ? "#6EC7E0" : "rgba(255,255,255,.16)"}`,
    background: act ? "rgba(110,199,224,.18)" : "transparent",
    color: act ? "#E7ECF5" : "rgba(255,255,255,.6)",
  }),
  cuenta: { margin: "10px 0 8px", fontFamily: "ui-monospace,Menlo,monospace",
            fontSize: 11.5, color: "rgba(255,255,255,.5)" } as React.CSSProperties,
  campo: { flex: 1, minWidth: 0, padding: "7px 9px", borderRadius: 7,
           border: "1px solid rgba(255,255,255,.16)", background: "#070d18",
           color: "#E7ECF5", fontFamily: "inherit", fontSize: 13 } as React.CSSProperties,
  btn: { padding: "7px 12px", borderRadius: 7, border: 0,
         background: "#6EC7E0", color: "#070d18", cursor: "pointer",
         fontFamily: "inherit", fontSize: 12.5, fontWeight: 600 } as React.CSSProperties,
  aviso: { margin: "8px 0 0", fontSize: 12, color: "#7CD9A6" } as React.CSSProperties,
  linea: { height: 1, background: "rgba(255,255,255,.12)", margin: "13px 0" } as React.CSSProperties,
  suave: { width: "100%", padding: "8px 12px", borderRadius: 8, cursor: "pointer",
           fontFamily: "inherit", fontSize: 13, border: "1px solid rgba(255,255,255,.18)",
           background: "transparent", color: "#E7ECF5" } as React.CSSProperties,
  check: { display: "flex", gap: 8, alignItems: "center", fontSize: 13.5,
           cursor: "pointer", padding: "3px 0" } as React.CSSProperties,
  pie: { margin: "8px 0 0", fontSize: 11.5, color: "rgba(255,255,255,.42)" } as React.CSSProperties,
};

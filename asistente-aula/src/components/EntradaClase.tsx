"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";
import { useDocente } from "@/lib/supabase/docente";

/**
 * La ventana del principio de la clase: el estudiante elige su nombre.
 *
 * Mientras el docente no abra la clase de su sección, la presentación va en
 * modo repaso y aquí no se enseña nada. Cuando la abre, aparece la lista de
 * esa sección; al tocar su nombre el estudiante queda presente (la misma
 * asistencia de «Pasar lista») y desde ahí su nota se guarda sola.
 *
 * La presentación es HTML generado sin cliente de Supabase. Se hablan por
 * eventos: ella pide `nota:guardar` y este componente contesta con
 * `clase:guardado`, `clase:identidad` o `clase:desmarcado`.
 *
 * En el proyector del docente no sale nunca, y tampoco mientras se averigua
 * quién mira: `useDocente` devuelve `null` hasta saberlo. Antes se leía una
 * marca que ponía otro componente, y en ese hueco la ventana se abría encima
 * de la clase proyectada.
 */

type Ficha = {
  token: string;
  entrada: string;
  seccion: string;
  nombre: string;
  detalle: Record<string, number>;
  codigo: string | null;
  bloqueado?: boolean;
};
type Persona = { id: string; nombre: string; tomado: boolean };

const SONDEO = 10_000;
const SONDEO_DENTRO = 5_000;   // con nombre elegido: la pausa del docente llega rápido

function hoy() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
const llave = (seccion: string) => `clase:${seccion}:${hoy()}`;
const leer = (k: string) => { try { return localStorage.getItem(k); } catch { return null; } };
const escribir = (k: string, v: string | null) => {
  try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch { /* sin almacenamiento */ }
};

function mensaje(e: { message?: string } | null): string {
  const m = e?.message ?? "";
  if (m.includes("nombre_tomado")) return "Ese nombre ya entró. Si es el tuyo, avísale al docente.";
  if (m.includes("sala_cerrada")) return "La clase se acaba de cerrar.";
  return "No se pudo entrar. Revisa la conexión y vuelve a intentarlo.";
}

export function EntradaClase({ nivel, semana }: { nivel: string; semana: number }) {
  const [abiertas, setAbiertas] = useState<string[]>([]);
  const [ficha, setFicha] = useState<Ficha | null>(null);
  const [seccion, setSeccion] = useState("");
  const [lista, setLista] = useState<Persona[] | null>(null);
  const [elegido, setElegido] = useState<Persona | null>(null);
  const [filtro, setFiltro] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);
  const docente = useDocente();

  const fichaRef = useRef<Ficha | null>(null);
  fichaRef.current = ficha;

  const avisar = useCallback((f: Ficha) => {
    document.dispatchEvent(new CustomEvent("clase:identidad", {
      detail: { nombre: f.nombre, seccion: f.seccion, detalle: f.detalle ?? {}, codigo: f.codigo },
    }));
  }, []);

  const olvidar = useCallback((f: Ficha) => {
    escribir(llave(f.seccion), null);
    setFicha(null);
    setSeccion("");
    setLista(null);
    setElegido(null);
    setFiltro("");
    document.dispatchEvent(new CustomEvent("clase:desmarcado"));
  }, []);

  // Cada diez segundos: qué está abierto y si quien está sigue siendo válido.
  const sondear = useCallback(async () => {
    if (docente !== false) return;        // el docente no entra, y sin saberlo tampoco se pregunta
    const sb = supabaseNavegador();
    const { data } = await sb.rpc("clase_abiertas", { p_nivel: nivel });
    const secs = ((data ?? []) as { seccion: string }[]).map((r) => r.seccion);
    setAbiertas(secs);

    const actual = fichaRef.current;
    if (actual) {
      // Cerró su sección y abrió otra del grado: en esta PC ahora hay otro grupo.
      if (secs.length && !secs.includes(actual.seccion)) { olvidar(actual); return; }
      const { data: v } = await sb.rpc("clase_volver", { p_token: actual.token, p_semana: semana });
      if (!v) { olvidar(actual); return; }          // el docente lo desmarcó
      const bloqueado = !!(v as Ficha).bloqueado;
      if (bloqueado !== !!actual.bloqueado) setFicha({ ...actual, bloqueado });
      return;
    }

    // Sin nombre todavía: ¿esta PC ya había entrado hoy en una sección abierta?
    for (const s of secs) {
      const t = leer(llave(s));
      if (!t) continue;
      const { data: v } = await sb.rpc("clase_volver", { p_token: t, p_semana: semana });
      if (v) { setFicha(v as Ficha); avisar(v as Ficha); return; }
      escribir(llave(s), null);
    }
    if (secs.length === 1) setSeccion(secs[0]);
    else if (!secs.length) { setSeccion(""); setLista(null); setElegido(null); }
  }, [docente, nivel, semana, avisar, olvidar]);

  const dentro = !!ficha;
  useEffect(() => {
    void sondear();
    const reloj = setInterval(() => { void sondear(); }, dentro ? SONDEO_DENTRO : SONDEO);
    document.addEventListener("visibilitychange", sondear);
    return () => {
      clearInterval(reloj);
      document.removeEventListener("visibilitychange", sondear);
    };
  }, [sondear, dentro]);

  // La lista de la sección elegida, al día con quién ya entró.
  useEffect(() => {
    if (!seccion || ficha || docente !== false) return;
    setFiltro("");            // la búsqueda del anterior no se hereda
    let vivo = true;
    async function cargar() {
      const { data } = await supabaseNavegador().rpc("clase_lista", { p_seccion: seccion });
      if (vivo) setLista((data ?? []) as Persona[]);
    }
    void cargar();
    const reloj = setInterval(() => { void cargar(); }, SONDEO);
    return () => { vivo = false; clearInterval(reloj); };
  }, [seccion, ficha, docente]);

  // La presentación pide guardar; se agrupan los avisos seguidos en uno.
  useEffect(() => {
    let espera: ReturnType<typeof setTimeout> | null = null;
    let ultimo: { detalle: Record<string, number>; codigo: string | null } | null = null;

    async function guardar() {
      const f = fichaRef.current;
      if (!f || !ultimo) return;
      const { detalle, codigo } = ultimo;
      ultimo = null;
      const { data, error: e } = await supabaseNavegador().rpc("clase_nota", {
        p_token: f.token, p_semana: semana, p_detalle: detalle, p_codigo: codigo,
      });
      if (e) {
        if (e.message.includes("desmarcado")) olvidar(f);
        return;                     // «bloqueado»: en pausa no se guarda nada
      }
      document.dispatchEvent(new CustomEvent("clase:guardado", { detail: data }));
    }
    function pedir(ev: Event) {
      const d = ((ev as CustomEvent).detail ?? {}) as { detalle?: Record<string, number>; codigo?: string | null };
      ultimo = { detalle: d.detalle ?? {}, codigo: d.codigo ?? null };
      if (espera) clearTimeout(espera);
      espera = setTimeout(() => { void guardar(); }, 700);
    }
    function pregunta() { if (fichaRef.current) avisar(fichaRef.current); }

    document.addEventListener("nota:guardar", pedir);
    document.addEventListener("clase:pregunta", pregunta);
    return () => {
      if (espera) clearTimeout(espera);
      document.removeEventListener("nota:guardar", pedir);
      document.removeEventListener("clase:pregunta", pregunta);
    };
  }, [semana, avisar, olvidar]);

  async function entrar() {
    if (!elegido || !seccion) return;
    setEnviando(true);
    setError("");
    const { data, error: e } = await supabaseNavegador().rpc("clase_entrar", {
      p_seccion: seccion, p_estudiante: elegido.id, p_semana: semana,
    });
    setEnviando(false);
    if (e || !data) {
      setError(mensaje(e));
      setElegido(null);
      return;
    }
    const f = data as Ficha;
    escribir(llave(f.seccion), f.token);
    setFicha(f);
    avisar(f);
  }

  const vistos = useMemo(() => {
    const q = filtro.trim().toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
    if (!lista) return [];
    if (!q) return lista;
    return lista.filter((p) => p.nombre.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "").includes(q));
  }, [lista, filtro]);

  if (docente === false && ficha?.bloqueado) {
    return (
      <div style={S.pausa} role="alertdialog" aria-modal="true" aria-labelledby="pausa-titulo">
        <div style={S.pausaCaja}>
          <p style={S.pausaIcono} aria-hidden="true">⏸</p>
          <h2 id="pausa-titulo" style={S.titulo}>Tu pantalla está en pausa</h2>
          <p style={S.ayuda}>Mira al frente. El docente te la devuelve cuando esté listo.</p>
        </div>
      </div>
    );
  }

  if (docente !== false || ficha || !abiertas.length) return null;

  return (
    <div style={S.velo} role="dialog" aria-modal="true" aria-labelledby="entrada-titulo">
      <div style={S.caja}>
        {!seccion ? (
          <>
            <p style={S.paso}>EMPIEZA LA CLASE</p>
            <h2 id="entrada-titulo" style={S.titulo}>¿En qué sección estás?</h2>
            <div style={S.secciones}>
              {abiertas.map((s) => (
                <button key={s} type="button" style={S.seccion} onClick={() => setSeccion(s)}>{s}</button>
              ))}
            </div>
          </>
        ) : elegido ? (
          <>
            <p style={S.paso}>{seccion.toUpperCase()}</p>
            <h2 id="entrada-titulo" style={S.titulo}>¿Eres {elegido.nombre}?</h2>
            <p style={S.ayuda}>Al confirmar quedas presente en la lista de hoy y tu nota se guarda a tu nombre.</p>
            <div style={S.acciones}>
              <button type="button" style={S.boton} onClick={entrar} disabled={enviando} autoFocus>
                {enviando ? "Entrando…" : "Sí, soy yo"}
              </button>
              <button type="button" style={S.botonSec} onClick={() => setElegido(null)} disabled={enviando}>
                No, volver a la lista
              </button>
            </div>
          </>
        ) : (
          <>
            <p style={S.paso}>{seccion.toUpperCase()} · EMPIEZA LA CLASE</p>
            <h2 id="entrada-titulo" style={S.titulo}>Toca tu nombre</h2>
            <input
              type="search" value={filtro} onChange={(e) => setFiltro(e.target.value)}
              placeholder="Busca tu nombre" aria-label="Busca tu nombre" style={S.buscar}
            />
            {error && <p style={S.error}>{error}</p>}
            {lista === null ? (
              <p style={S.ayuda}>Cargando la lista…</p>
            ) : (
              <div style={S.lista}>
                {vistos.map((p) => (
                  <button
                    key={p.id} type="button" disabled={p.tomado}
                    style={p.tomado ? { ...S.nombre, ...S.tomado } : S.nombre}
                    onClick={() => { setError(""); setElegido(p); }}
                  >
                    {p.nombre}
                    {p.tomado && <span style={S.yaEntro}>ya entró</span>}
                  </button>
                ))}
                {!vistos.length && <p style={S.ayuda}>No aparece nadie con ese nombre.</p>}
              </div>
            )}
            {abiertas.length > 1 && (
              <button type="button" style={S.cambiar} onClick={() => { setSeccion(""); setLista(null); }}>
                ← No es mi sección
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}

const S: Record<string, React.CSSProperties> = {
  pausa: { position: "fixed", inset: 0, zIndex: 1001, display: "grid", placeItems: "center", padding: 16,
           background: "rgba(4,8,18,.96)" },
  pausaCaja: { maxWidth: 560, textAlign: "center", color: "#e8eefb", display: "grid", gap: 12, fontFamily: "inherit" },
  pausaIcono: { margin: 0, fontSize: 64, lineHeight: 1 },
  velo: { position: "fixed", inset: 0, zIndex: 1000, display: "grid", placeItems: "center", padding: 16,
          background: "rgba(4,8,18,.88)", backdropFilter: "blur(3px)" },
  caja: { width: "min(760px, 100%)", maxHeight: "88vh", display: "flex", flexDirection: "column", gap: 14,
          padding: "26px 26px 22px", borderRadius: 16, background: "#0f1a2e", color: "#e8eefb",
          border: "1px solid #24324d", boxShadow: "0 30px 80px -30px rgba(0,0,0,.8)", fontFamily: "inherit" },
  paso: { margin: 0, fontSize: 12, letterSpacing: ".16em", color: "#7dd3fc" },
  titulo: { margin: 0, fontSize: "clamp(24px, 3.4vw, 34px)", lineHeight: 1.15, fontWeight: 800, letterSpacing: "-.01em" },
  ayuda: { margin: 0, fontSize: 15, color: "#a9b6cf", lineHeight: 1.5 },
  error: { margin: 0, fontSize: 14, color: "#fca5a5" },
  buscar: { minHeight: 46, padding: "0 14px", borderRadius: 10, border: "1px solid #2b3b5a", background: "#0b1322",
            color: "#e8eefb", fontFamily: "inherit", fontSize: 16 },
  lista: { overflowY: "auto", display: "grid", gap: 8, gridTemplateColumns: "repeat(auto-fill, minmax(210px, 1fr))",
           paddingRight: 4 },
  nombre: { minHeight: 48, padding: "10px 14px", borderRadius: 10, border: "1px solid #2b3b5a", background: "#15223a",
            color: "#e8eefb", fontFamily: "inherit", fontSize: 15, textAlign: "left", cursor: "pointer",
            display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 },
  tomado: { opacity: 0.45, cursor: "not-allowed" },
  yaEntro: { fontSize: 11, color: "#94a3b8", whiteSpace: "nowrap" },
  secciones: { display: "flex", flexWrap: "wrap", gap: 10 },
  seccion: { minHeight: 56, minWidth: 120, padding: "0 20px", borderRadius: 12, border: 0, background: "#7dd3fc",
             color: "#06121f", fontFamily: "inherit", fontSize: 20, fontWeight: 800, cursor: "pointer" },
  acciones: { display: "flex", flexWrap: "wrap", gap: 10, marginTop: 4 },
  boton: { minHeight: 48, padding: "0 22px", borderRadius: 10, border: 0, background: "#7dd3fc", color: "#06121f",
           fontFamily: "inherit", fontSize: 16, fontWeight: 800, cursor: "pointer" },
  botonSec: { minHeight: 48, padding: "0 18px", borderRadius: 10, border: "1px solid #2b3b5a", background: "transparent",
              color: "#e8eefb", fontFamily: "inherit", fontSize: 15, cursor: "pointer" },
  cambiar: { alignSelf: "flex-start", background: "none", border: 0, color: "#7dd3fc", fontFamily: "inherit",
             fontSize: 14, cursor: "pointer", padding: 0 },
};

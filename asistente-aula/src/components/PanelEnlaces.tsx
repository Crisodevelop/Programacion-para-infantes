"use client";
import { useCallback, useEffect, useState } from "react";
import { supabaseNavegador } from "@/lib/supabase/navegador";

/**
 * Los enlaces del inicio, desde el admin.
 *
 * Se escribe con la sesión del docente y la clave anónima, como el resto del
 * área: la RLS de `enlace` deja leer a cualquiera y escribir solo a quien
 * cumple `is_teacher()`.
 *
 * El orden se decide a mano con las flechas y no por la fecha en que se añadió:
 * el enlace que más se usa tiene que poder ir primero, y eso no lo sabe la base.
 */
type Enlace = {
  id: string; titulo: string; url: string; descripcion: string;
  orden: number; activo: boolean;
};

export function PanelEnlaces() {
  const [lista, setLista] = useState<Enlace[]>([]);
  const [titulo, setTitulo] = useState("");
  const [url, setUrl] = useState("");
  const [desc, setDesc] = useState("");
  const [aviso, setAviso] = useState("");
  const [cargando, setCargando] = useState(true);
  // Cuál se está editando y con qué valores. Un solo enlace a la vez: con dos
  // formularios abiertos nunca se sabe cuál se está guardando.
  const [editando, setEditando] = useState<string | null>(null);
  const [borrador, setBorrador] = useState({ titulo: "", url: "", descripcion: "" });

  const traer = useCallback(async () => {
    const { data, error } = await supabaseNavegador()
      .from("enlace").select("id,titulo,url,descripcion,orden,activo")
      .order("orden").order("creado_en");
    if (error) setAviso(error.message);
    setLista((data ?? []) as Enlace[]);
    setCargando(false);
  }, []);

  useEffect(() => { void traer(); }, [traer]);

  /** Lo que la base va a exigir de todas formas, dicho antes y en cristiano. */
  function queFalta(t: string, u: string): string {
    if (t.trim().length < 2) return "Ponle un título.";
    if (!/^https?:\/\/./i.test(u.trim()))
      return "La dirección tiene que empezar por http:// o https://";
    return "";
  }

  async function agregar() {
    const t = titulo.trim(), u = url.trim();
    const falta = queFalta(t, u);
    if (falta) { setAviso(falta); return; }
    const { error } = await supabaseNavegador().from("enlace").insert({
      titulo: t, url: u, descripcion: desc.trim().slice(0, 140),
      orden: (lista.at(-1)?.orden ?? 0) + 1,
    });
    if (error) { setAviso(error.message); return; }
    setTitulo(""); setUrl(""); setDesc(""); setAviso(`«${t}» ya está en el inicio.`);
    void traer();
  }

  /** Intercambia el orden con el vecino. Dos filas, una escritura cada una. */
  async function mover(i: number, d: -1 | 1) {
    const j = i + d;
    if (j < 0 || j >= lista.length) return;
    const a = lista[i], b = lista[j];
    const sb = supabaseNavegador();
    await Promise.all([
      sb.from("enlace").update({ orden: b.orden }).eq("id", a.id),
      sb.from("enlace").update({ orden: a.orden }).eq("id", b.id),
    ]);
    // Si los dos tenían el mismo número, intercambiarlos no cambia nada:
    // se renumera la lista entera y se acabó el problema.
    if (a.orden === b.orden) {
      const nueva = [...lista];
      nueva[i] = b; nueva[j] = a;
      await Promise.all(nueva.map((e, k) =>
        sb.from("enlace").update({ orden: k }).eq("id", e.id)));
    }
    void traer();
  }

  function editar(e: Enlace) {
    setEditando(e.id);
    setBorrador({ titulo: e.titulo, url: e.url, descripcion: e.descripcion });
    setAviso("");
  }

  async function guardar(e: Enlace) {
    const falta = queFalta(borrador.titulo, borrador.url);
    if (falta) { setAviso(falta); return; }
    const { error } = await supabaseNavegador().from("enlace").update({
      titulo: borrador.titulo.trim(),
      url: borrador.url.trim(),
      descripcion: borrador.descripcion.trim().slice(0, 140),
    }).eq("id", e.id);
    if (error) { setAviso(error.message); return; }
    setEditando(null);
    setAviso(`«${borrador.titulo.trim()}» actualizado.`);
    void traer();
  }

  async function alternar(e: Enlace) {
    await supabaseNavegador().from("enlace").update({ activo: !e.activo }).eq("id", e.id);
    void traer();
  }

  async function borrar(e: Enlace) {
    await supabaseNavegador().from("enlace").delete().eq("id", e.id);
    setAviso(`«${e.titulo}» borrado.`);
    void traer();
  }

  return (
    <section>
      <div style={S.alta}>
        <input style={S.campo} value={titulo} maxLength={60} placeholder="Título"
               aria-label="Título" onChange={(e) => setTitulo(e.target.value)} />
        <input style={S.campo} value={url} placeholder="https://…" aria-label="Dirección"
               inputMode="url" onChange={(e) => setUrl(e.target.value)} />
        <input style={{ ...S.campo, gridColumn: "1 / -1" }} value={desc} maxLength={140}
               placeholder="Una línea: para qué sirve" aria-label="Descripción"
               onChange={(e) => setDesc(e.target.value)}
               onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); void agregar(); } }} />
        <button type="button" style={S.btn} onClick={agregar}>Añadir al inicio</button>
      </div>
      {aviso && <p style={S.aviso} role="status">{aviso}</p>}

      {cargando ? (
        <p style={S.vacio}>Cargando…</p>
      ) : lista.length === 0 ? (
        <p style={S.vacio}>Todavía no hay enlaces. Mientras no haya ninguno, en el
          inicio no aparece la sección.</p>
      ) : (
        <ul style={S.lista}>
          {lista.map((e, i) => (
            <li key={e.id} style={{ ...S.fila, opacity: e.activo ? 1 : 0.5 }}>
              <div style={S.orden}>
                <button type="button" style={S.flecha} disabled={i === 0}
                        onClick={() => mover(i, -1)} aria-label={`Subir ${e.titulo}`}>↑</button>
                <button type="button" style={S.flecha} disabled={i === lista.length - 1}
                        onClick={() => mover(i, 1)} aria-label={`Bajar ${e.titulo}`}>↓</button>
              </div>
              {editando === e.id ? (
                <>
                  <div style={S.editar}>
                    <input style={S.campo} value={borrador.titulo} maxLength={60}
                           aria-label="Título" autoFocus
                           onChange={(v) => setBorrador({ ...borrador, titulo: v.target.value })} />
                    <input style={S.campo} value={borrador.url} inputMode="url"
                           aria-label="Dirección"
                           onChange={(v) => setBorrador({ ...borrador, url: v.target.value })} />
                    <input style={{ ...S.campo, gridColumn: "1 / -1" }} value={borrador.descripcion}
                           maxLength={140} aria-label="Descripción"
                           placeholder="Una línea: para qué sirve"
                           onChange={(v) => setBorrador({ ...borrador, descripcion: v.target.value })}
                           onKeyDown={(v) => { if (v.key === "Enter") { v.preventDefault(); void guardar(e); } }} />
                  </div>
                  <button type="button" style={S.btnFila} onClick={() => guardar(e)}>Guardar</button>
                  <button type="button" style={S.suave} onClick={() => setEditando(null)}>Cancelar</button>
                </>
              ) : (
                <>
                  <div style={S.datos}>
                    <b style={S.tit}>{e.titulo}</b>
                    <a style={S.url} href={e.url} target="_blank" rel="noopener noreferrer">{e.url}</a>
                    {e.descripcion && <span style={S.desc}>{e.descripcion}</span>}
                  </div>
                  <button type="button" style={S.suave} onClick={() => editar(e)}>Editar</button>
                  <button type="button" style={S.suave} onClick={() => alternar(e)}>
                    {e.activo ? "Ocultar" : "Mostrar"}
                  </button>
                  <button type="button" style={S.borrar} onClick={() => borrar(e)}
                          aria-label={`Borrar ${e.titulo}`}>×</button>
                </>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

const S: Record<string, React.CSSProperties> = {
  alta: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, alignItems: "start" },
  campo: { padding: "10px 12px", borderRadius: 9, border: "1px solid var(--linea)",
           background: "var(--panel)", color: "var(--tx)", fontFamily: "inherit", fontSize: 14.5 },
  btn: { gridColumn: "1 / -1", justifySelf: "start", padding: "10px 18px", borderRadius: 9,
         border: 0, background: "var(--aqua)", color: "var(--fondo)", cursor: "pointer",
         fontFamily: "inherit", fontSize: 14.5, fontWeight: 600 },
  aviso: { margin: "12px 0 0", fontSize: 13.5, color: "var(--aqua)" },
  vacio: { margin: "22px 0 0", fontSize: 14.5, color: "var(--tx-2)", maxWidth: "56ch" },
  lista: { listStyle: "none", margin: "24px 0 0", padding: 0, display: "grid", gap: 6 },
  fila: { display: "flex", gap: 12, alignItems: "center", padding: "11px 13px",
          borderRadius: 10, background: "var(--panel)", border: "1px solid var(--linea)" },
  orden: { display: "grid", gap: 2 },
  flecha: { width: 26, height: 20, borderRadius: 5, cursor: "pointer", fontFamily: "inherit",
            fontSize: 11, border: "1px solid var(--linea)", background: "transparent",
            color: "var(--tx-2)", padding: 0 },
  datos: { flex: 1, display: "grid", gap: 2, minWidth: 0 },
  editar: { flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6, minWidth: 0 },
  btnFila: { padding: "6px 13px", borderRadius: 8, border: 0, background: "var(--aqua)",
             color: "var(--fondo)", cursor: "pointer", fontFamily: "inherit", fontSize: 12.5,
             fontWeight: 600 },
  tit: { fontSize: 15 },
  url: { fontFamily: "ui-monospace,Menlo,monospace", fontSize: 11.5, color: "var(--mut)",
         overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" },
  desc: { fontSize: 13, color: "var(--tx-2)" },
  suave: { padding: "6px 11px", borderRadius: 8, cursor: "pointer", fontFamily: "inherit",
           fontSize: 12.5, border: "1px solid var(--linea)", background: "transparent",
           color: "var(--tx-2)" },
  borrar: { border: 0, background: "transparent", color: "var(--mut)", cursor: "pointer",
            fontSize: 18, lineHeight: 1, padding: "0 2px" },
};

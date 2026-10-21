"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { supabaseNavegador } from "@/lib/supabase/navegador";

/**
 * Entrada del docente.
 *
 * No hay registro. Las cuentas se crean con `npm run docente:crear`, así que
 * nadie que llegue al enlace puede darse de alta: el plan y las presentaciones
 * son públicos porque tienen que serlo, pero el área de administración no es
 * un sitio al que uno se apunta.
 */
export default function Entrar() {
  return (
    <Suspense fallback={null}>
      <Formulario />
    </Suspense>
  );
}

function Formulario() {
  const router = useRouter();
  const params = useSearchParams();
  const [correo, setCorreo] = useState("");
  const [clave, setClave] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function enviar(e: React.FormEvent) {
    e.preventDefault();
    setEnviando(true);
    setError("");

    const sb = supabaseNavegador();
    const { error: fallo } = await sb.auth.signInWithPassword({
      email: correo.trim(),
      password: clave,
    });

    if (fallo) {
      // Mensaje único a propósito: distinguir «ese correo no existe» de «la
      // contraseña está mal» le dice a un desconocido cuáles son las cuentas
      // reales del sistema.
      setError("Correo o contraseña incorrectos.");
      setEnviando(false);
      return;
    }

    const volver = params.get("volver");
    router.push(volver?.startsWith("/admin") ? volver : "/admin");
    router.refresh();
  }

  return (
    <main style={S.pantalla}>
      <form style={S.caja} onSubmit={enviar}>
        <p style={S.eyebrow}>Asistente de aula</p>
        <h1 style={S.titulo}>Entrar</h1>

        <label style={S.campo}>
          <span style={S.etiqueta}>Correo</span>
          <input
            style={S.entrada}
            type="email"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            autoComplete="username"
            required
            autoFocus
          />
        </label>

        <label style={S.campo}>
          <span style={S.etiqueta}>Contraseña</span>
          <input
            style={S.entrada}
            type="password"
            value={clave}
            onChange={(e) => setClave(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        {error && <p style={S.error} role="alert">{error}</p>}

        <button style={S.boton} type="submit" disabled={enviando}>
          {enviando ? "Entrando…" : "Entrar"}
        </button>

        <a style={S.volver} href="/">← Volver al inicio</a>
      </form>
    </main>
  );
}

const S: Record<string, React.CSSProperties> = {
  pantalla: {
    minHeight: "100dvh", display: "grid", placeItems: "center", padding: 24,
    background: "radial-gradient(120% 80% at 50% 0%, var(--fondo-2) 0%, var(--fondo) 62%)",
  },
  caja: {
    width: "min(94vw, 380px)", display: "grid", gap: 16,
    background: "var(--panel)", border: "1px solid var(--linea)", borderRadius: 14, padding: 28,
  },
  eyebrow: { margin: 0, fontSize: 11, letterSpacing: ".18em", textTransform: "uppercase", color: "var(--mut)" },
  titulo: { margin: "0 0 6px", fontSize: 28, letterSpacing: "-.02em" },
  campo: { display: "grid", gap: 6 },
  etiqueta: { fontSize: 13, color: "var(--tx-2)" },
  entrada: {
    padding: "12px 14px", fontSize: 16, borderRadius: 9,
    border: "1px solid var(--linea)", background: "var(--fondo-2)", color: "var(--tx)",
  },
  error: { margin: 0, fontSize: 14, color: "var(--rojo)" },
  boton: {
    padding: "13px 16px", fontSize: 16, fontWeight: 600, borderRadius: 9, cursor: "pointer",
    border: "1px solid var(--aqua)", background: "var(--aqua)", color: "#06121f",
  },
  volver: { fontSize: 13.5, color: "var(--mut)", textDecoration: "none", textAlign: "center" },
};

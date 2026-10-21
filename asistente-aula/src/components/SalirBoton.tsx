"use client";
import { useRouter } from "next/navigation";
import { supabaseNavegador } from "@/lib/supabase/navegador";

export function SalirBoton() {
  const router = useRouter();
  return (
    <button
      style={{
        background: "none", border: "1px solid var(--linea)", color: "var(--mut)",
        fontSize: 13.5, padding: "6px 12px", borderRadius: 7, cursor: "pointer",
      }}
      onClick={async () => {
        await supabaseNavegador().auth.signOut();
        router.push("/");
        router.refresh();
      }}
    >
      Salir
    </button>
  );
}

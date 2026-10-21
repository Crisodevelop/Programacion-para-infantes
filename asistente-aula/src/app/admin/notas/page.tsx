import { supabaseServidor } from "@/lib/supabase/sesion";
import { TablaNotas, type Conducta, type FilaNota } from "@/components/TablaNotas";

export const dynamic = "force-dynamic";
export const metadata = { title: "Notas de clase" };

/**
 * Las notas que los estudiantes guardan al final de cada clase.
 *
 * Se leen con la sesión del docente y la clave anónima, como el diagnóstico:
 * es la RLS la que decide. Sin sesión no llega ni una fila.
 */
export default async function Pagina() {
  const sb = await supabaseServidor();
  const [{ data, error }, { data: conducta }] = await Promise.all([
    sb.from("notas")
      .select("id,creado_en,nombre,seccion,nivel,semana,puntos,puntos_docente,detalle,codigo,estudiante_id")
      .order("creado_en", { ascending: false }),
    // Solo están los que se apartan del 100: a los demás no hay nada que
    // anotarles, así que no ocupan fila.
    sb.from("disciplina").select("estudiante_id,puntos,nota"),
  ]);

  return (
    <main style={S.pantalla}>
      <header style={S.cabecera}>
        <p style={S.eyebrow}>Cada clase suma 100</p>
        <h1 style={S.titulo}>Notas de clase</h1>
        <p style={S.nota}>
          Cuenta el primer intento de cada reto y los juegos resueltos. Se guarda sola desde que el
          estudiante elige su nombre al abrir la clase, junto con el código de su práctica.
        </p>
        <p style={S.nota}>
          En <b>Acumulada</b> está lo que lleva cada quien. La semana de arriba es la última que ese
          nivel tiene guardada —las tres secciones de un nivel van por la misma— y las clases que
          cuentan son solo las que esa sección tiene registradas: una semana que no se guardó no le
          resta a nadie, pero sale avisada como <b>sin registrar</b> y su casilla queda gris en la tira
          de la derecha. La casilla en rojo es otra cosa: esa clase sí se dio y esa persona no tiene
          nota. De dos notas de la misma semana vale la mejor.
        </p>
        <p style={S.nota}>
          La <b>disciplina</b> arranca en 100 para todo el mundo y solo se toca a quien haya que bajar;
          pesa un 15 % de la final, lo justo para mover a quien está en el borde sin decidir por él.
          Una nota que cambies a mano queda marcada y <b>deja de recalcularse</b>: aunque esa persona
          vuelva a la clase y resuelva algo más, la nota sigue siendo la tuya.
        </p>
      </header>

      {error && <p style={S.error}>No se pudieron leer las notas: {error.message}</p>}

      <TablaNotas filas={(data ?? []) as FilaNota[]} conducta={(conducta ?? []) as Conducta[]} />
    </main>
  );
}

const S: Record<string, React.CSSProperties> = {
  // Ocho columnas y una tira de doce semanas no caben en 1000: la tira se
  // envolvía y cada estudiante ocupaba tres renglones. Con 1320 entran las
  // doce de un vistazo. Los párrafos siguen cortados a 62ch, que leer una
  // línea de 1300 px es otro problema.
  pantalla: { padding: "34px 22px 80px", maxWidth: 1320, margin: "0 auto" },
  cabecera: { marginBottom: 24 },
  eyebrow: { margin: 0, fontSize: 12, letterSpacing: ".16em", textTransform: "uppercase", color: "var(--aqua)" },
  titulo: { margin: "8px 0 0", fontSize: 30, fontWeight: 700, letterSpacing: "-.02em" },
  nota: { margin: "10px 0 0", fontSize: 14, color: "var(--tx-2)", maxWidth: "62ch", lineHeight: 1.5 },
  error: { marginTop: 20, color: "var(--rojo)", fontSize: 14 },
};

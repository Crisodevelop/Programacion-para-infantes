import { redirect } from "next/navigation";

/** `/plan` fue la dirección de la planificación durante un tiempo: está en el
 *  atajo de voz, en el .docx y en cualquier sitio donde él la haya pegado.
 *  Romperla no aporta nada. */
export default function Pagina() {
  redirect("/");
}

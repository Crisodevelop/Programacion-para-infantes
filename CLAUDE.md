# Esta copia

Copia de trabajo del proyecto *Secundaria*, puesta en el escritorio el 21 de
octubre de 2026. **Hoy no tiene `.git`**: ni rama ni `origin`, y nada de lo
que se haga aquí llega a GitHub ni a Vercel. El original sigue en
`~/Desktop/Secundaria` y es el que se despliega.

Eso cambia en cuanto se haga lo de `docs/subir-a-github.md`: la copia tendrá
su propio repositorio, **distinto** del del aula. Lo que nunca va a pasar es
que esto escriba en el repositorio del aula.

Lo que se decida aquí no vuelve solo al original. Si algo de esto tiene que
acabar en producción, se copia a mano y se comenta antes.

## Lo que hay que hacer

**Lee `docs/encargo.md` antes de tocar nada.** Son cuatro encargos del docente
—quitar el cocurricular, borrar el nombre de la escuela, escribir una guía del
área de admin y dejar el repositorio montable sin la base del aula—, cada uno
con sus archivos concretos. **El primero ya está hecho**, y lo que se tocó está
escrito ahí: no lo repitas ni lo deshagas. Las decisiones que hacían falta ya
las tomó él y están anotadas en su sitio, así que no hay nada que preguntar
para empezar.

`docs/base-de-datos.md` es el material del cuarto: cómo crear la base desde
cero, las variables de entorno y el SQL que al repositorio le falta.

`docs/subir-a-github.md` es el último paso: esta copia se publica en
`github.com/Crisodevelop/Programacion-para-infantes`, que es **público y está
vacío**. Ahí está lo que hay que limpiar antes del primer `push` y cómo usar
el token sin dejarlo escrito. **No subas nada hasta que el encargo 0 esté
hecho.**

Y antes de los cuatro, el encargo 0: **esta copia es para enseñarla**, así que
primero hay que limpiarla de credenciales y de datos de estudiantes.

## Cómo se trabaja aquí

- El contenido de las clases **no se edita a mano**: sale de
  `planificacion/contenido.py` y se regenera con `./planificacion/generar.sh`.
  Editar los HTML de `asistente-aula/src/contenido/` funciona hasta la
  siguiente regeneración, que los pisa sin avisar.
- Para comprobar que la app compila, `npm run verificar`, **nunca
  `npm run build`**: los dos escriben en `.next` y el `build` tumba el servidor
  de desarrollo si lo tienes abierto.
- `npm run dev -- -p 3002`: el 3000 lo ocupa el original y el 3001, otro
  proyecto suyo.
- El código y los comentarios van en castellano, como el resto del repositorio.
- `.env.local` apunta todavía a la **base de datos real**, con los nombres de
  los estudiantes dentro. Es lo primero que hay que resolver: encargo 0.

# Secundaria

Dos piezas que comparten una sola fuente de contenido.

    planificacion/     el temario: de aquí salen el Word, la web y la presentación
    asistente-aula/    la app Next.js: clases, clase en vivo, notas y asistencia

## planificacion/

`contenido.py` es la única fuente: las 36 sesiones, el banco de dinámicas y
la evaluación. Todo lo demás se genera desde ahí.

> En esta copia el cocurricular (el Programa Maker: Makers Space, secundaria,
> primaria y el club de chicas) **no se publica**. El material sigue escrito en
> `contenido.py`, pero `MAKER_PROGRAMAS` está vacío y la app no tiene rutas que
> lo sirvan. Para devolverlo: los cuatro programas a esa lista y sus pasos a
> `generar.sh`.

    ./planificacion/generar.sh

Escribe en `planificacion/salida/`:

| Archivo | Para qué |
|---|---|
| `Planificacion_..._Secundaria.docx` | Coordinación. Mismo formato que el original |
| `Planificacion_..._Secundaria.pdf` | Imprimir |
| `plan-programacion.html` | Página suelta, la que se publica como artifact |
| `presentacion-criso.html` | Presentación suelta |
| `kahoot/` | Los quiz de diagnóstico: uno por nivel y su versión corta |

Y además los fragmentos que la app sirve en `/plan` y `/presentacion`.

**Para corregir una semana se edita `contenido.py` y se vuelve a generar.**
Editar los HTML a mano funciona hasta la siguiente regeneración, que los
sobrescribe sin avisar.

El PDF es el único paso manual: se exporta abriendo el `.docx` en Pages o Word.

## asistente-aula/

Las clases de cada semana, la clase en vivo, las notas y la asistencia.
Ver `asistente-aula/README.md`.

    cd asistente-aula && npm run dev

- `/curso/…` las presentaciones de cada semana
- `/admin/clase` abrir la clase y ver quién entró
- `/plan` y `/presentacion` el material de clase

## Desplegar en Vercel

Este repositorio tiene dos carpetas y la app está en una de ellas, así que hay
que decírselo a Vercel o el despliegue sale vacío con un 404:

**Settings → Build and Deployment → Root Directory:** `asistente-aula`

Y dos variables de entorno, ambas de tipo **Config** y no *Secret*. Vercel
rechaza marcar como secreto cualquier cosa con prefijo `NEXT_PUBLIC_`, y con
razón: ese prefijo significa que el valor se compila dentro del JavaScript que
llega al navegador, donde cualquiera lo lee.

    NEXT_PUBLIC_SUPABASE_URL
    NEXT_PUBLIC_SUPABASE_ANON_KEY

La `anon key` es pública por diseño: identifica el proyecto, no da acceso. Lo
que protege los datos es la RLS de Supabase (ver `migraciones/`).

**Lo demás no sube.** `SUPABASE_SERVICE_ROLE_KEY` se salta la RLS: solo la usan
los scripts que corres en tu Mac.

Cambiar una variable no redespliega solo. Hay que ir a Deployments → Redeploy,
sin el caché del build anterior si el anterior falló.

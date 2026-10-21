# Programación para infantes

Un curso de programación con Python para 1ro, 2do y 3ro de secundaria —36
clases, 12 semanas por grado— y la app con la que se da en el aula: las
presentaciones de cada semana con un editor de Python dentro, la clase en vivo,
la asistencia y las notas.

Lo escribe y lo da **Criso**, docente de programación.

## Qué se ve sin configurar nada

Casi todo. El material son archivos, no consultas: se clona, se instala y se
recorre entero sin base de datos ni claves.

```sh
git clone https://github.com/Crisodevelop/Programacion-para-infantes.git
cd Programacion-para-infantes/asistente-aula
npm install
npm run dev          # http://localhost:3000
```

| Ruta | Qué hay | ¿Necesita base? |
|---|---|---|
| `/` | La portada y los tres niveles | No |
| `/curso/1ro` · `/curso/2do` · `/curso/3ro` | Las 36 clases, cada una con sus diapositivas | No |
| El editor de cada clase | Python, HTML y CSS en el navegador, con [PyScript](https://pyscript.net) | No |
| `/plan` | La planificación completa: objetivos, sesiones, evaluación | No |
| `/presentacion` · `/presentaciones` | La clase de presentación y el índice para proyectar | No |
| `/diagnostico` | La prueba de entrada | Para verla no; para enviarla, sí |
| `/entrar` y `/admin/…` | La gestión del aula | **Sí** |

Sin credenciales la app no se rompe: el área de admin rebota a `/entrar` y todo
lo demás se sigue sirviendo (`asistente-aula/src/middleware.ts`). El formulario
de `/entrar`, eso sí, falla al pulsar el botón, porque no hay base a la que
llamar.

## El área de admin

Es la parte que solo se ve con una base de datos, y la que más trabajo tiene
detrás:

- **Clase en vivo** (`/admin/clase`). El docente abre la clase de una sección;
  a cada estudiante le aparece la lista de su grupo, toca su nombre y queda
  presente. Lo que escribe en el editor se guarda con su nota al pulsar
  Ejecutar.
- **Asistencia** y **notas**, por sección y por semana, con nota a mano cuando
  hace falta corregir.
- **Diagnóstico**: los resultados de la prueba de entrada por grupo.
- **Horario** y **enlaces** de la semana.

Los datos los protege la RLS de Supabase, no la interfaz: con la clave pública
y sin sesión, asistencia, listas y notas devuelven cero filas. El estudiante,
que no tiene cuenta, solo entra por funciones `security definer` que deciden
qué puede hacer.

## Levantarlo con tu propia base

La guía paso a paso está en [`docs/base-de-datos.md`](docs/base-de-datos.md):
un proyecto de Supabase gratuito, `.env.local` a partir de `.env.example`, las
migraciones y la cuenta del docente.

> **Aún no funciona sobre una base vacía.** Las migraciones dan por hecho una
> tabla `profiles`, el tipo `user_role` y la función `is_teacher()` que en la
> base original se crearon a mano. Hasta que exista
> `asistente-aula/migraciones/0000_base.sql`, `npm run db:migrar` falla en el
> primer archivo. La guía explica qué tiene que llevar.

## Cómo está hecho

```
planificacion/     el temario: de aquí sale todo el material
asistente-aula/    la app: Next.js + Supabase
docs/              la guía de la base de datos
```

### planificacion/

`contenido.py` es la **única fuente**: las 36 sesiones, el banco de dinámicas y
la evaluación. Todo lo demás se genera desde ahí:

```sh
./planificacion/generar.sh
```

Necesita Python 3 (solo la biblioteca estándar) y el `npm install` de
`asistente-aula/`, porque los códigos QR se generan con Node desde allí. Las
imágenes de los quiz se capturan con Google Chrome en modo headless, desde la
ruta de macOS (`build_kahoot.py`); solo se rehacen si cambia el temario.

Escribe en `planificacion/salida/`:

| Archivo | Para qué |
|---|---|
| `Planificacion_..._Secundaria.docx` | La planificación para coordinación |
| `plan-programacion.html` | La misma planificación como página suelta |
| `presentacion-criso.html` | La clase de presentación, suelta |
| `kahoot/` | Los quiz de diagnóstico: uno por nivel y su versión corta |

Y además los fragmentos que sirve la app, en `asistente-aula/src/contenido/`.

**Para cambiar una clase se edita `contenido.py` y se vuelve a generar.** Los
HTML generados se sobrescriben en cada pasada sin avisar.

El PDF es el único paso manual: se exporta abriendo el `.docx` en Pages o Word.

El temario incluye un programa cocurricular (el Programa Maker) que en este
repositorio **no se publica**: sigue escrito en `contenido.py`, pero
`MAKER_PROGRAMAS` está vacío y la app no tiene rutas que lo sirvan.

### asistente-aula/

Next.js con App Router. Las clases son estáticas; solo el área de admin, la
clase en vivo y el envío del diagnóstico hablan con Supabase. Más detalle en
[`asistente-aula/README.md`](asistente-aula/README.md).

## Desplegar en Vercel

La app está en una subcarpeta, así que hay que decírselo a Vercel o el
despliegue sale vacío con un 404:

**Settings → Build and Deployment → Root Directory:** `asistente-aula`

Sin variables de entorno se publica el material entero y el área de admin
queda cerrada. Para abrirla, dos variables y solo dos:

    NEXT_PUBLIC_SUPABASE_URL
    NEXT_PUBLIC_SUPABASE_ANON_KEY

Las dos son públicas por diseño —el prefijo `NEXT_PUBLIC_` las compila dentro
del JavaScript que llega al navegador—, así que van como **Config**, no como
*Secret*. `SUPABASE_SERVICE_ROLE_KEY` se salta la RLS: **nunca** va en un
despliegue, solo en los scripts que se corren en local.

Cambiar una variable no redespliega solo: Deployments → Redeploy.

# Asistente de aula

La app de las clases: las presentaciones de cada semana, la clase en vivo
(el estudiante elige su nombre y su nota se guarda sola), las notas, la
asistencia y el diagnóstico de entrada. Se publica en Vercel.

## Quién ve qué

| Ruta | Quién |
|---|---|
| `/` · `/plan` · `/presentacion` · `/curso/…` | **Cualquiera.** Es lo que ven los estudiantes |
| `/entrar` | Público, pero sin registro: las cuentas se crean por script |
| `/admin` y todo lo que cuelga de ahí | Solo `role = 'docente'` |

Lo que protege los datos es la RLS, no la interfaz. Asistencia, listas, notas y
entradas de clase: con la clave anónima y sin sesión devuelven cero filas. El
estudiante sin cuenta solo entra por funciones `security definer` (la de la
clase en vivo y la del diagnóstico), que deciden qué puede hacer.

## Poner en marcha

1. Copia `.env.example` a `.env.local` y rellena lo que falte.
2. `npm run db:migrar` — aplica las migraciones de `migraciones/`.
3. `npm run dev`

## Dar una clase

1. En `/admin/clase` elige la sección y pulsa **Abrir clase**.
2. A los estudiantes de ese grado les sale una ventana con la lista de su
   sección: tocan su nombre y quedan presentes.
3. Su nota se guarda sola mientras avanzan. Si alguien eligió mal, lo
   desmarcas desde la misma página.
4. Al terminar, **Cerrar clase**. Las notas quedan en `/admin/notas`.

## Cargar las listas reales

    npm run listas:cargar

Las listas viven en la tabla `lista` (una fila por estudiante y sección).
`npm run lista:importar` sigue disponible para un CSV suelto con cabecera
`nombre_completo,grupo`.

Las instrucciones de despliegue están en el README de la raíz.

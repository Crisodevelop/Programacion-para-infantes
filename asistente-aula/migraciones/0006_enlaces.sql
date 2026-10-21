-- ═══════════════════════════════════════════════════════════════════════
--  Enlaces del inicio
--
--  La página de inicio se genera desde contenido.py y se publica estática, así
--  que hasta ahora cambiar un enlace era editar Python y regenerar. Una lista
--  de recursos no funciona así: se añade uno en mitad de una semana y se quita
--  al mes siguiente, sin tocar el repositorio.
--
--  ─── La comprobación de la dirección no es cosmética ───
--  Esto se pinta como `href` en una página pública. Una dirección que empiece
--  por `javascript:` sería código ejecutándose en el navegador de cualquiera
--  que entre. Se corta aquí, en la base, que es el único sitio por el que pasa
--  todo y del que no se puede salir por otra puerta.
--
--  ─── Y la RLS va al revés que la de la lista de clase ───
--  Ahí `anon` no podía leer nada porque eran nombres de menores. Aquí sí lee:
--  son enlaces publicados a propósito, y si no se pudieran leer sin sesión no
--  servirían para nada. Lo que `anon` no puede es escribir.
-- ═══════════════════════════════════════════════════════════════════════

create table if not exists public.enlace (
  id          uuid primary key default gen_random_uuid(),
  titulo      text not null check (length(btrim(titulo)) between 2 and 60),
  url         text not null check (url ~* '^https?://.'),
  descripcion text not null default '' check (length(descripcion) <= 140),
  -- El orden lo decide el docente, no la fecha en que lo añadió: el enlace
  -- que más se usa tiene que poder ir primero.
  orden       int not null default 0,
  activo      boolean not null default true,
  creado_en   timestamptz not null default now()
);

create index if not exists enlace_orden_idx
  on public.enlace (activo, orden, creado_en);

alter table public.enlace enable row level security;

drop policy if exists enlace_lectura on public.enlace;
create policy enlace_lectura on public.enlace
  for select to anon, authenticated
  using (true);

drop policy if exists enlace_docente on public.enlace;
create policy enlace_docente on public.enlace
  for all to authenticated
  using (public.is_teacher()) with check (public.is_teacher());

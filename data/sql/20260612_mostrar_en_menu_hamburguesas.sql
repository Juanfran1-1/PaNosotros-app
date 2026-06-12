alter table public.hamburguesas
add column if not exists mostrar_en_menu boolean not null default true;

update public.hamburguesas
set mostrar_en_menu = true
where mostrar_en_menu is null;

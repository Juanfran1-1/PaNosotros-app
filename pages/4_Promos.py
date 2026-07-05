import streamlit as st
from utils.diseno import aplicar_estilos, page_header, section_note
from data.modificador_db import (
    cargar_hamburguesas,
    cargar_extras,
    cargar_promos,
    cargar_promo_items,
    cargar_promo_extras,
    agregar_promo,
    actualizar_promo_completa,
    actualizar_disponibilidad_promo,
    eliminar_promo,
    guardar_items_promo,
    guardar_extras_promo
)
from utils.storage import mostrar_control_encuadre, resolver_foto_menu

st.set_page_config(page_title="PA' NOSOTROS - PROMOS", page_icon="logo.png", layout="wide")
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py")
    st.stop()

page_header(
    "Promos",
    "Creá promos configurables: precio, foto, variedades permitidas, extras y disponibilidad."
)

df_promos = cargar_promos()
df_hamburguesas = cargar_hamburguesas()
df_extras = cargar_extras()
df_promo_items = cargar_promo_items()
df_promo_extras = cargar_promo_extras()

def obtener_variedades_promo(promo_id):
    if df_promo_items.empty or df_hamburguesas.empty:
        return "Sin variedades configuradas"

    items = df_promo_items[df_promo_items["promo_id"] == promo_id]
    if items.empty:
        return "Sin variedades configuradas"

    nombres = []
    for _, item in items.iterrows():
        hamburguesa = df_hamburguesas[df_hamburguesas["id"] == item["hamburguesa_id"]]
        if hamburguesa.empty:
            continue
        nombre = hamburguesa.iloc[0]["nombre"]
        cantidad = int(item.get("cantidad", 1))
        nombres.append(f"{nombre} ({cantidad})")

    return ", ".join(nombres) if nombres else "Sin variedades configuradas"

def obtener_extras_promo(promo_id):
    if df_promo_extras.empty or df_extras.empty:
        return "Sin extras configurados"

    items = df_promo_extras[df_promo_extras["promo_id"] == promo_id]
    if items.empty:
        return "Sin extras configurados"

    nombres = []
    for _, item in items.iterrows():
        extra = df_extras[df_extras["id"] == item["extra_id"]]
        if extra.empty:
            continue
        nombres.append(extra.iloc[0]["nombre"])

    return ", ".join(nombres) if nombres else "Sin extras configurados"

def opciones_hamburguesas():
    if df_hamburguesas.empty:
        return {}
    return {
        row["nombre"]: int(row["id"])
        for _, row in df_hamburguesas.iterrows()
    }

def cantidad_tipos_hamburguesas():
    if df_hamburguesas.empty:
        return 1
    return max(1, len(df_hamburguesas))

def opciones_extras():
    if df_extras.empty:
        return {}
    return {
        row["nombre"]: int(row["id"])
        for _, row in df_extras.iterrows()
    }

def guardar_relaciones_promo(promo_id, variedades, mapa_hamburguesas, cantidad, extras, mapa_extras):
    items_payload = [
        {
            "promo_id": promo_id,
            "hamburguesa_id": mapa_hamburguesas[nombre],
            "cantidad": int(cantidad)
        }
        for nombre in variedades
    ]
    extras_payload = [
        {
            "promo_id": promo_id,
            "extra_id": mapa_extras[nombre]
        }
        for nombre in extras
    ]

    return (
        guardar_items_promo(promo_id, items_payload)
        and guardar_extras_promo(promo_id, extras_payload)
    )

if df_promos.empty:
    st.info("No hay promos cargadas.")
else:
    df_promos_vista = df_promos.copy()
    df_promos_vista["variedades"] = df_promos_vista["id"].apply(obtener_variedades_promo)
    df_promos_vista["extras_permitidos"] = df_promos_vista["id"].apply(obtener_extras_promo)
    st.dataframe(
        df_promos_vista.rename(columns={
            "id": "ID",
            "nombre": "Nombre",
            "descripcion": "Descripción",
            "precio": "Precio",
            "foto": "Imagen",
            "disponible": "Disponible",
            "variedades": "Variedades",
            "extras_permitidos": "Extras permitidos"
        }),
        use_container_width=True
    )

    st.markdown("### Resumen de promos")
    cols_resumen = st.columns(2)
    for i, (_, promo) in enumerate(df_promos.iterrows()):
        with cols_resumen[i % 2]:
            st.info(
                f"**{promo['nombre']}**\n\n"
                f"Variedades: {obtener_variedades_promo(int(promo['id']))}\n\n"
                f"Extras: {obtener_extras_promo(int(promo['id']))}"
            )

st.markdown("### Disponibilidad")
section_note("Desactivar una promo la oculta del menú. Las variedades agotadas se muestran como agotadas dentro de la promo.")
if not df_promos.empty:
    cols = st.columns(3)
    for i, (_, fila) in enumerate(df_promos.iterrows()):
        with cols[i % 3]:
            disponible = fila.get("disponible", True)
            estado_clase = "pa-state-on" if disponible else "pa-state-off"
            estado_texto = "Habilitada" if disponible else "Deshabilitada"
            label = f"{estado_texto} · {fila['nombre']}"
            st.markdown(f'<span class="{estado_clase}"></span>', unsafe_allow_html=True)
            if st.button(label, key=f"promo_stock_{fila['id']}", use_container_width=True):
                actualizar_disponibilidad_promo(int(fila["id"]), not disponible)
                st.rerun()

st.divider()

with st.expander("Agregar promo"):
    nueva_foto_archivo = st.file_uploader(
        "Foto de la promo",
        type=["jpg", "jpeg", "png", "webp"],
        key="foto_nueva_promo"
    )
    encuadre_nueva_foto = mostrar_control_encuadre(nueva_foto_archivo, "promos", "encuadre_nueva_promo")

    with st.form("form_agregar_promo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_nombre = st.text_input("Nombre de la promo", placeholder="PROMO GORDITXS")
            nuevo_precio = st.number_input("Precio ($)", min_value=0.0, step=100.0)
        with col2:
            nueva_desc = st.text_area("Descripción", placeholder="3 mini burgers + papas noisette")
        max_variedades_disponibles = cantidad_tipos_hamburguesas()
        max_variedades_nueva = st.number_input(
            "Máximo de tipos combinables",
            min_value=1,
            max_value=max_variedades_disponibles,
            step=1,
            value=1,
            key="max_variedades_nueva"
        )
        st.caption("1 = todas del mismo tipo. 2 o más = permite combinar variedades.")

        mapa_hamburguesas = opciones_hamburguesas()
        variedades_nueva_promo = []
        cantidad_nueva_promo = 3
        if mapa_hamburguesas:
            variedades_nueva_promo = st.multiselect(
                "Variedades incluidas en la promo",
                list(mapa_hamburguesas.keys()),
                key="variedades_nueva_promo"
            )
            cantidad_nueva_promo = st.number_input(
                "Cantidad total de minis de la promo",
                min_value=1,
                step=1,
                value=3,
                key="cantidad_nueva_promo"
            )
        else:
            st.caption("Primero tenés que cargar hamburguesas para asociarlas a una promo.")

        mapa_extras = opciones_extras()
        extras_nueva_promo = []
        if mapa_extras:
            extras_nueva_promo = st.multiselect(
                "Extras que se le pueden agregar",
                list(mapa_extras.keys()),
                key="extras_nueva_promo"
            )
        else:
            st.caption("Si querés agregar extras a una promo, primero cargalos desde Productos.")

        if st.form_submit_button("Agregar promo", type="primary"):
            if not nuevo_nombre or nuevo_precio <= 0:
                st.error("Nombre y precio son obligatorios.")
            else:
                foto_url = resolver_foto_menu(nueva_foto_archivo, nuevo_nombre, "promos", posicion_recorte=encuadre_nueva_foto)
                if nueva_foto_archivo and not foto_url:
                    st.stop()
                promo_creada = agregar_promo(
                    nuevo_nombre,
                    nueva_desc,
                    nuevo_precio,
                    foto_url,
                    max_variedades_nueva > 1,
                    max_variedades_nueva
                )
                if promo_creada:
                    if type(promo_creada) is int:
                        guardar_relaciones_promo(
                            promo_creada,
                            variedades_nueva_promo,
                            mapa_hamburguesas,
                            cantidad_nueva_promo,
                            extras_nueva_promo,
                            mapa_extras
                        )
                    st.success("Promo agregada correctamente.")
                    st.rerun()

if not df_promos.empty:
    st.divider()

    with st.expander("Editar promo"):
        promo_editar = st.selectbox(
            "Seleccionar promo",
            df_promos["nombre"].tolist(),
            key="editar_promo"
        )
        fila = df_promos[df_promos["nombre"] == promo_editar].iloc[0]
        promo_id = int(fila["id"])

        edit_foto_archivo = st.file_uploader(
            "Nueva foto de la promo (opcional)",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"foto_edit_promo_{promo_id}"
        )
        encuadre_edit_foto = mostrar_control_encuadre(edit_foto_archivo, "promos", f"encuadre_edit_promo_{promo_id}")

        with st.form("form_editar_promo"):
            col1, col2 = st.columns(2)
            with col1:
                edit_nombre = st.text_input("Nombre", value=fila.get("nombre", ""))
                edit_precio = st.number_input("Precio ($)", min_value=0.0, step=100.0, value=float(fila.get("precio", 0)))
            with col2:
                edit_desc = st.text_area("Descripción", value=fila.get("descripcion", "") or "")
            max_variedades_disponibles = cantidad_tipos_hamburguesas()
            max_variedades_actual = int(fila.get("max_variedades", 1) or 1)
            max_variedades_actual = min(max(1, max_variedades_actual), max_variedades_disponibles)
            max_variedades_edit = st.number_input(
                "Máximo de tipos combinables",
                min_value=1,
                max_value=max_variedades_disponibles,
                step=1,
                value=max_variedades_actual,
                key=f"max_variedades_edit_{promo_id}"
            )
            st.caption("1 = todas del mismo tipo. 2 o más = permite combinar variedades.")

            extras_actuales = df_promo_extras[df_promo_extras["promo_id"] == promo_id] if not df_promo_extras.empty else df_promo_extras
            ids_extras_actuales = set(extras_actuales["extra_id"].astype(int).tolist()) if not extras_actuales.empty else set()
            opciones_extras = {
                row["nombre"]: int(row["id"])
                for _, row in df_extras.iterrows()
            } if not df_extras.empty else {}
            extras_seleccionados = [
                nombre for nombre, extra_id in opciones_extras.items()
                if extra_id in ids_extras_actuales
            ]
            edit_extras = st.multiselect(
                "Extras que se le pueden agregar",
                list(opciones_extras.keys()),
                default=extras_seleccionados,
                disabled=df_extras.empty
            )
            if df_extras.empty:
                st.caption("Primero tenés que cargar extras desde Productos.")

            items_actuales = df_promo_items[df_promo_items["promo_id"] == promo_id] if not df_promo_items.empty else df_promo_items
            ids_actuales = set(items_actuales["hamburguesa_id"].astype(int).tolist()) if not items_actuales.empty else set()
            mapa_hamburguesas = opciones_hamburguesas()
            variedades_seleccionadas = [
                nombre for nombre, hamburguesa_id in mapa_hamburguesas.items()
                if hamburguesa_id in ids_actuales
            ]
            edit_variedades = st.multiselect(
                "Variedades incluidas en la promo",
                list(mapa_hamburguesas.keys()),
                default=variedades_seleccionadas,
                disabled=df_hamburguesas.empty
            )
            cantidad_actual = int(items_actuales.iloc[0]["cantidad"]) if not items_actuales.empty else (5 if "LIGHT" in str(fila.get("nombre", "")).upper() else 3)
            edit_cantidad = st.number_input(
                "Cantidad total de minis de la promo",
                min_value=1,
                step=1,
                value=cantidad_actual
            )
            if df_hamburguesas.empty:
                st.caption("Primero tenés que cargar hamburguesas para asociarlas a una promo.")

            if st.form_submit_button("Guardar promo", type="primary"):
                foto_url = resolver_foto_menu(edit_foto_archivo, edit_nombre, "promos", fila.get("foto", ""), encuadre_edit_foto)
                if edit_foto_archivo and not foto_url:
                    st.stop()
                if actualizar_promo_completa(
                    promo_id,
                    edit_nombre,
                    edit_desc,
                    edit_precio,
                    foto_url,
                    max_variedades_edit > 1,
                    max_variedades_edit
                ):
                    guardar_relaciones_promo(
                        promo_id,
                        edit_variedades,
                        mapa_hamburguesas,
                        edit_cantidad,
                        edit_extras,
                        opciones_extras
                    )
                    st.success("Promo actualizada correctamente.")
                    st.rerun()

    with st.expander("Eliminar promo"):
        promo_eliminar = st.selectbox(
            "Promo a eliminar",
            df_promos["nombre"].tolist(),
            key="eliminar_promo"
        )
        fila_eliminar = df_promos[df_promos["nombre"] == promo_eliminar].iloc[0]

        st.markdown('<span class="pa-danger-button"></span>', unsafe_allow_html=True)
        if st.button("Eliminar promo", type="secondary"):
            if eliminar_promo(int(fila_eliminar["id"])):
                st.success("Promo eliminada correctamente.")
                st.rerun()

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()

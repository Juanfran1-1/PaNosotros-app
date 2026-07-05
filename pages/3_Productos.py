import streamlit as st
import pandas as pd
from utils.diseno import aplicar_estilos, page_header, section_note
from data.modificador_db import (
    cargar_hamburguesas,
    cargar_extras,
    agregar_hamburguesa,
    agregar_extra,
    actualizar_hamburguesa_completa,
    actualizar_extra_completo,
    eliminar_hamburguesa,
    eliminar_extra,
    actualizar_disponibilidad,
    actualizar_disponibilidad_extra,
    actualizar_visibilidad_menu
)
from utils.storage import mostrar_control_encuadre, resolver_foto_menu

st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")

aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

page_header(
    "Productos",
    "Administrá las mini burgers, extras y disponibilidad que ve el menú del cliente."
)

try:
    df_hamburguesas = cargar_hamburguesas()
    df_extras = cargar_extras()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

st.markdown("### Hamburguesas")
section_note("Usá disponibilidad para marcar agotadas y mostrar en el menú para ocultar productos sorpresa o fuera de carta.")

if df_hamburguesas.empty:
    st.info("No hay hamburguesas cargadas.")
else:
    st.dataframe(
        df_hamburguesas.rename(columns={
            "id": "ID",
            "nombre": "Nombre",
            "precio": "Precio",
            "foto": "Imagen",
            "desc": "Descripción",
            "ingredientes": "Ingredientes",
            "disponible": "Disponible",
            "mostrar_en_menu": "Mostrar en menú"
        }),
        use_container_width=True
    )

st.markdown("### Disponibilidad de hamburguesas")
section_note("Si está apagada, la hamburguesa se ve como agotada pero sigue apareciendo en el menú.")
if not df_hamburguesas.empty:
    cols = st.columns(3)
    for i, (_, fila) in enumerate(df_hamburguesas.iterrows()):
        with cols[i % 3]:
            disponible = fila.get("disponible", True)
            label = f"✅ {fila['nombre']}" if disponible else f"❌ {fila['nombre']}"
            if st.button(label, key=f"stock_{fila['id']}", use_container_width=True):
                actualizar_disponibilidad(int(fila["id"]), not disponible)
                st.rerun()

st.markdown("### Mostrar en el menú")
section_note("Si está apagada, la hamburguesa no aparece para clientes. Ideal para productos sorpresa o lanzamientos.")
if not df_hamburguesas.empty:
    cols_menu = st.columns(3)
    for i, (_, fila) in enumerate(df_hamburguesas.iterrows()):
        with cols_menu[i % 3]:
            mostrar_en_menu = fila.get("mostrar_en_menu", True)
            if pd.isna(mostrar_en_menu):
                mostrar_en_menu = True
            label = f"👁️ {fila['nombre']}" if mostrar_en_menu else f"🙈 {fila['nombre']}"
            if st.button(label, key=f"menu_visible_{fila['id']}", use_container_width=True):
                actualizar_visibilidad_menu(int(fila["id"]), not bool(mostrar_en_menu))
                st.rerun()

st.divider()

st.subheader("Extras")
section_note("Los extras se cargan acá y después se asignan a cada promo desde la pantalla Promos.")

if df_extras.empty:
    st.info("No hay extras cargados.")
else:
    st.dataframe(
        df_extras.rename(columns={
            "id": "ID",
            "nombre": "Nombre",
            "precio": "Precio",
            "disponible": "Disponible"
        }),
        use_container_width=True
    )

    st.markdown("### Disponibilidad de extras")
    cols_extras = st.columns(3)
    for i, (_, fila) in enumerate(df_extras.iterrows()):
        with cols_extras[i % 3]:
            disponible = fila.get("disponible", True)
            label = f"✅ {fila['nombre']}" if disponible else f"❌ {fila['nombre']}"
            if st.button(label, key=f"extra_stock_{fila['id']}", use_container_width=True):
                actualizar_disponibilidad_extra(int(fila["id"]), not disponible)
                st.rerun()

with st.expander("Agregar extra"):
    foto_extra = st.file_uploader(
        "Foto del extra (opcional)",
        type=["jpg", "jpeg", "png", "webp"],
        key="foto_nuevo_extra"
    )
    encuadre_extra = mostrar_control_encuadre(foto_extra, "extras", "encuadre_nuevo_extra")

    with st.form("form_agregar_extra", clear_on_submit=True):
        col_extra_1, col_extra_2 = st.columns(2)
        with col_extra_1:
            nuevo_extra = st.text_input("Nombre del extra", placeholder="Papas noisette")
        with col_extra_2:
            precio_extra = st.number_input("Precio extra ($)", min_value=0.0, step=100.0)

        if st.form_submit_button("Agregar extra", type="primary"):
            if not nuevo_extra or precio_extra <= 0:
                st.error("Nombre y precio son obligatorios.")
            else:
                foto_extra_url = resolver_foto_menu(foto_extra, nuevo_extra, "extras", posicion_recorte=encuadre_extra)
                if foto_extra and not foto_extra_url:
                    st.stop()
                if agregar_extra(nuevo_extra, precio_extra, foto_extra_url):
                    st.success("Extra agregado correctamente.")
                    st.rerun()

if not df_extras.empty:
    with st.expander("Editar extra"):
        extra_editar = st.selectbox(
            "Seleccionar extra",
            df_extras["nombre"].tolist(),
            key="editar_extra"
        )
        fila_extra = df_extras[df_extras["nombre"] == extra_editar].iloc[0]

        edit_extra_foto = st.file_uploader(
            "Nueva foto del extra (opcional)",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"foto_edit_extra_{fila_extra['id']}"
        )
        encuadre_edit_extra = mostrar_control_encuadre(edit_extra_foto, "extras", f"encuadre_edit_extra_{fila_extra['id']}")

        with st.form("form_editar_extra"):
            col_edit_extra_1, col_edit_extra_2 = st.columns(2)
            with col_edit_extra_1:
                edit_extra_nombre = st.text_input("Nombre", value=fila_extra.get("nombre", ""))
            with col_edit_extra_2:
                edit_extra_precio = st.number_input("Precio ($)", min_value=0.0, step=100.0, value=float(fila_extra.get("precio", 0)))

            if st.form_submit_button("Guardar extra", type="primary"):
                foto_extra_url = resolver_foto_menu(edit_extra_foto, edit_extra_nombre, "extras", fila_extra.get("foto", ""), encuadre_edit_extra)
                if edit_extra_foto and not foto_extra_url:
                    st.stop()
                if actualizar_extra_completo(int(fila_extra["id"]), edit_extra_nombre, edit_extra_precio, foto_extra_url):
                    st.success("Extra actualizado correctamente.")
                    st.rerun()

    with st.expander("Eliminar extra"):
        extra_eliminar = st.selectbox(
            "Extra a eliminar",
            df_extras["nombre"].tolist(),
            key="eliminar_extra"
        )
        fila_extra_eliminar = df_extras[df_extras["nombre"] == extra_eliminar].iloc[0]

        st.markdown('<span class="pa-danger-button"></span>', unsafe_allow_html=True)
        if st.button("Eliminar extra", type="secondary"):
            if eliminar_extra(int(fila_extra_eliminar["id"])):
                st.success("Extra eliminado correctamente.")
                st.rerun()

st.divider()

# --- SECCIÓN: AGREGAR ---
with st.expander("Agregar hamburguesa"):
    nueva_foto_archivo = st.file_uploader(
        "Foto de la hamburguesa",
        type=["jpg", "jpeg", "png", "webp"],
        key="foto_nueva_hamburguesa"
    )
    encuadre_nueva_foto = mostrar_control_encuadre(nueva_foto_archivo, "productos", "encuadre_nueva_hamburguesa")

    with st.form("form_agregar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_nombre = st.text_input("Nombre de la hamburguesa")
            nuevo_precio = st.number_input("Precio", min_value=0.0, step=100.0)
        
        with col2:
            nuevos_ingredientes = st.text_area("Ingredientes (separados por coma)", placeholder="Cheddar, Panceta, Cebolla")

        nueva_desc = st.text_input("Descripción corta", placeholder="Combo de 5 mini burgers + papas")

        if st.form_submit_button("Agregar", type="primary"):
            if not nuevo_nombre or nuevo_precio <= 0:
                st.error("Nombre y Precio son obligatorios.")
            else:
                try:
                    foto_url = resolver_foto_menu(nueva_foto_archivo, nuevo_nombre, "productos", posicion_recorte=encuadre_nueva_foto)
                    if nueva_foto_archivo and not foto_url:
                        st.stop()
                    agregar_hamburguesa(nuevo_nombre, nuevo_precio, foto_url, nueva_desc, nuevos_ingredientes)
                    st.success(f"¡{nuevo_nombre} agregada con éxito!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")

# --- SECCIÓN: EDITAR ---
if not df_hamburguesas.empty:
    with st.expander("Editar hamburguesa"):
        hamburguesa_editar = st.selectbox(
            "Seleccionar hamburguesa para modificar",
            df_hamburguesas["nombre"].tolist(),
            key="editar_hamburguesa"
        )

        fila = df_hamburguesas[df_hamburguesas["nombre"] == hamburguesa_editar].iloc[0]
        hamburguesa_id = int(fila["id"])

        edit_foto_archivo = st.file_uploader(
            "Nueva foto de la hamburguesa (opcional)",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"foto_edit_hamburguesa_{hamburguesa_id}"
        )
        encuadre_edit_foto = mostrar_control_encuadre(edit_foto_archivo, "productos", f"encuadre_edit_hamburguesa_{hamburguesa_id}")

        with st.form("form_edicion_total"):
            col1, col2 = st.columns(2)
            with col1:
                edit_precio = st.number_input("Precio ($)", min_value=0.0, step=100.0, value=float(fila["precio"]))
            with col2:
                edit_desc = st.text_input("Descripción corta", value=fila.get("desc", ""))
                edit_ing = st.text_area("Ingredientes (separados por coma)", value=fila.get("ingredientes", ""))

            st.info("💡 Tip: Para los ingredientes usa el formato: Cheddar, Panceta, Cebolla")

            if st.form_submit_button("Guardar todos los cambios", type="primary"):
                if edit_precio <= 0:
                    st.error("El precio es obligatorio y debe ser mayor a 0.")
                else:
                    try:
                        foto_url = resolver_foto_menu(edit_foto_archivo, hamburguesa_editar, "productos", fila.get("foto", ""), encuadre_edit_foto)
                        if edit_foto_archivo and not foto_url:
                            st.stop()
                        actualizar_hamburguesa_completa(hamburguesa_id, edit_precio, edit_desc, edit_ing, foto_url)
                        st.success("¡Hamburguesa actualizada correctamente!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

    # --- SECCIÓN: ELIMINAR ---
    with st.expander("Eliminar hamburguesa"):
        hamburguesa_eliminar = st.selectbox(
            "Hamburguesa a eliminar",
            df_hamburguesas["nombre"].tolist(),
            key="eliminar_hamburguesa"
        )

        fila_eliminar = df_hamburguesas[df_hamburguesas["nombre"] == hamburguesa_eliminar].iloc[0]
        hamburguesa_id_eliminar = int(fila_eliminar["id"])

        st.markdown('<span class="pa-danger-button"></span>', unsafe_allow_html=True)
        if st.button("Eliminar hamburguesa", type="secondary"):
            try:
                eliminar_hamburguesa(hamburguesa_id_eliminar)
                st.success("Hamburguesa eliminada correctamente.")
                st.rerun()
            except Exception as e:
                st.error(f"No se pudo eliminar: {e}")
            
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()

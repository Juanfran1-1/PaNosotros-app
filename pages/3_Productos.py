import streamlit as st
import pandas as pd
from utils.diseno import aplicar_estilos
from data.modificador_db import (
    cargar_hamburguesas,
    agregar_hamburguesa,
    actualizar_hamburguesa_completa,
    eliminar_hamburguesa,
    actualizar_disponibilidad  # <--- Agregada
)

st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")

aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

st.subheader("🍔 Productos")

try:
    df_hamburguesas = cargar_hamburguesas()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

st.markdown("### Hamburguesas actuales")

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
            "ingredientes": "Ingredientes"
        }),
        use_container_width=True
    )

st.markdown("### ⚡ Control de Stock")
if not df_hamburguesas.empty:
    cols = st.columns(3)
    for i, (_, fila) in enumerate(df_hamburguesas.iterrows()):
        with cols[i % 3]:
            disponible = fila.get("disponible", True)
            label = f"✅ {fila['nombre']}" if disponible else f"❌ {fila['nombre']}"
            if st.button(label, key=f"stock_{fila['id']}", use_container_width=True):
                actualizar_disponibilidad(int(fila["id"]), not disponible)
                st.rerun()

st.divider()

# --- SECCIÓN: AGREGAR ---
with st.expander("Agregar nueva hamburguesa"):
    with st.form("form_agregar", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_nombre = st.text_input("Nombre de la hamburguesa")
            nuevo_precio = st.number_input("Precio", min_value=0.0, step=100.0)
        
        with col2:
            nueva_foto = st.text_input("Nombre del archivo de imagen", placeholder="ejemplo: Hamburguesa.jpg")
            nuevos_ingredientes = st.text_area("Ingredientes (separados por coma)", placeholder="Cheddar, Panceta, Cebolla")

        nueva_desc = st.text_input("Descripción corta", placeholder="Combo de 5 mini burgers + papas")

        if st.form_submit_button("Agregar", type="primary"):
            if not nuevo_nombre or nuevo_precio <= 0:
                st.error("Nombre y Precio son obligatorios.")
            else:
                try:
                    agregar_hamburguesa(nuevo_nombre, nuevo_precio, nueva_foto, nueva_desc, nuevos_ingredientes)
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
                        actualizar_hamburguesa_completa(hamburguesa_id, edit_precio, edit_desc, edit_ing)
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
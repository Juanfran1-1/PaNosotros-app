import streamlit as st

from data.modificador_db import (
    cargar_hamburguesas,
    agregar_hamburguesa,
    actualizar_precio_hamburguesa,
    eliminar_hamburguesa,
)



st.subheader("🍔 Productos")

df_hamburguesas = cargar_hamburguesas()

st.markdown("### Hamburguesas actuales")

if df_hamburguesas.empty:
    st.info("No hay hamburguesas cargadas.")
else:
    st.dataframe(
        df_hamburguesas.rename(columns={
            "id": "ID",
            "nombre": "Nombre",
            "precio": "Precio"
        }),
        use_container_width=True
    )

st.divider()

st.markdown("### Agregar nueva hamburguesa")

with st.form("form_agregar_hamburguesa"):
    nombre_nuevo = st.text_input("Nombre")
    precio_nuevo = st.number_input("Precio", min_value=0.0, step=100.0)
    submit_agregar = st.form_submit_button("Agregar hamburguesa")

    if submit_agregar:
        if nombre_nuevo.strip() == "":
            st.error("El nombre no puede estar vacío.")
        elif precio_nuevo <= 0:
            st.error("El precio debe ser mayor a 0.")
        else:
            nombres_existentes = df_hamburguesas["nombre"].str.lower().tolist()

            if nombre_nuevo.strip().lower() in nombres_existentes:
                st.warning("Esa hamburguesa ya existe.")
            else:
                agregar_hamburguesa(nombre_nuevo.strip(), precio_nuevo)
                st.success("Hamburguesa agregada correctamente.")
                st.rerun()

st.divider()

if not df_hamburguesas.empty:
    st.markdown("### Editar precio")

    hamburguesa_editar = st.selectbox(
        "Seleccionar hamburguesa",
        df_hamburguesas["nombre"].tolist(),
        key="editar_hamburguesa"
    )

    fila = df_hamburguesas[df_hamburguesas["nombre"] == hamburguesa_editar].iloc[0]
    hamburguesa_id = int(fila["id"])
    precio_actual = float(fila["precio"])

    nuevo_precio = st.number_input(
        "Nuevo precio",
        min_value=0.0,
        step=100.0,
        value=precio_actual,
        key="nuevo_precio"
    )

    if st.button("Actualizar precio"):
        if nuevo_precio <= 0:
            st.error("El precio debe ser mayor a 0.")
        else:
            actualizar_precio_hamburguesa(hamburguesa_id, nuevo_precio)
            st.success("Precio actualizado correctamente.")
            st.rerun()

    st.divider()

    st.markdown("### Eliminar hamburguesa")

    hamburguesa_eliminar = st.selectbox(
        "Hamburguesa a eliminar",
        df_hamburguesas["nombre"].tolist(),
        key="eliminar_hamburguesa"
    )

    fila_eliminar = df_hamburguesas[df_hamburguesas["nombre"] == hamburguesa_eliminar].iloc[0]
    hamburguesa_id_eliminar = int(fila_eliminar["id"])

    if st.button("Eliminar hamburguesa"):
        eliminar_hamburguesa(hamburguesa_id_eliminar)
        st.success("Hamburguesa eliminada correctamente.")
        st.rerun()
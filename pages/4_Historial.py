import pandas as pd
import streamlit as st
from data.modificador_db import cargar_datos
from utils.diseno import aplicar_estilos
import time
import datetime

st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")

aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()

st.subheader("Historial de pedidos")

# Colocamos el logo y el filtro de fecha fuera del fragmento para que no parpadeen
col1, col2, col3 = st.columns([2, 2, 1])
with col2:
    try:
        st.image("logo.png", width=250)
    except:
        pass

filtro_fecha = st.date_input("Filtrar por fecha", value=None)

# --- FRAGMENTO QUE SE ACTUALIZA SOLO ---
@st.fragment(run_every=30)
def mostrar_tabla_viva(fecha_seleccionada):
    try:
        # Cargamos datos frescos de la DB
        df = cargar_datos()
        
        if df.empty:
            st.info("No hay pedidos cargados todavía.")
            return

        df_mostrar = df.copy()
        
        # Procesar fechas
        df_mostrar["fecha"] = pd.to_datetime(df_mostrar["fecha"], errors="coerce")

        if fecha_seleccionada:
            fecha_dt = pd.to_datetime(fecha_seleccionada)
            df_mostrar = df_mostrar[df_mostrar["fecha"].dt.date == fecha_dt.date()]

        df_mostrar = df_mostrar.sort_values(by="fecha", ascending=False)
        df_mostrar["Fecha y Hora"] = df_mostrar["fecha"].dt.strftime('%d/%m/%Y %H:%M')

        # Mostrar tabla
        hora_argentina = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3)
        st.caption(f"Última actualización: {hora_argentina.strftime('%H:%M:%S')}")
        st.dataframe(
            df_mostrar.rename(columns={
                "Fecha y Hora": "Fecha y Hora",
                "detalle": "Detalle",
                "cliente": "Cliente",
                "monto": "Monto",
                "metodo_pago": "Método de Pago",
                "entrega": "Tipo de Entrega",
                "direccion": "Dirección",
                "estado": "Estado"
            })[["Fecha y Hora", "Detalle", "Cliente", "Monto", "Método de Pago", "Tipo de Entrega", "Dirección", "Estado"]],
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error al actualizar la tabla: {e}")

# Llamamos a la función del fragmento
mostrar_tabla_viva(filtro_fecha)
import pandas as pd
import streamlit as st
from data.modificador_db import cargar_datos
from utils.diseno import aplicar_estilos


st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")


aplicar_estilos()



if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    
    # botón que lo lleva a la página principal
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    
    st.stop()


if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

st.subheader("Historial de pedidos")

# --- TRY PARA CARGAR DATOS ---
try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

col1, col2, col3 = st.columns([2, 2, 1])

with col2:
    try:
        st.image("logo.png", width=250)
    except:
        pass

# Si está vacío, mostramos el mensaje y DETENEMOS la ejecución
if df.empty:
    st.info("No hay pedidos cargados todavía.")
    st.stop() 

# Filtro de fecha
filtro_fecha = st.date_input("Filtrar por fecha", value=None)

df_mostrar = df.copy()

# --- TRY PARA PROCESAR FECHAS Y HORAS ---
try:
    # Convertir columna a datetime
    df_mostrar["fecha"] = pd.to_datetime(df_mostrar["fecha"], errors="coerce")

    # Aplicar filtro si se eligió fecha (comparamos solo el día)
    if filtro_fecha:
        filtro_fecha = pd.to_datetime(filtro_fecha)
        df_mostrar = df_mostrar[df_mostrar["fecha"].dt.date == filtro_fecha.date()]

    # Ordenar pedidos por fecha (más nuevos arriba)
    df_mostrar = df_mostrar.sort_values(by="fecha", ascending=False)

    # Formatear la fecha para que incluya la hora (Día/Mes/Año Hora:Minutos)
    df_mostrar["Fecha y Hora"] = df_mostrar["fecha"].dt.strftime('%d/%m/%Y %H:%M')

except Exception as e:
    st.error(f"Error al procesar el formato de fechas: {e}")

# --- MOSTRAR TABLA ACTUALIZADA ---
try:
    # Mostramos "Fecha y Hora" en lugar de la columna "fecha" original
    st.dataframe(
        df_mostrar.rename(columns={
            "Fecha y Hora": "Fecha y Hora",
            "detalle": "Detalle",
            "cliente": "Cliente",
            "monto": "Monto",
            "metodo_pago": "Método de Pago",
            "entrega": "Tipo de Entrega",
            "direccion": "Dirección"
        })[["Fecha y Hora", "Detalle", "Cliente", "Monto", "Método de Pago", "Tipo de Entrega", "Dirección"]],
        use_container_width=True
    )
except Exception as e:
    st.error(f"Error al mostrar la tabla: {e}")
    
    


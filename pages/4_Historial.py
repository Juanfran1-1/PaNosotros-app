import pandas as pd
import streamlit as st
from data.modificador_db import cargar_datos

# BLOQUEO DE SEGURIDAD
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión en la página principal para continuar.")
    st.stop()

st.subheader("Historial de pedidos")

df = cargar_datos()

col1, col2, col3 = st.columns([2, 2, 1])

with col2:
    st.image("logo.png", width=250)


#Si está vacío, mostramos el mensaje y DETENEMOS la ejecución ahí mismo
if df.empty:
    st.info("No hay pedidos cargados todavía.")
    st.stop() # Esto evita que el código de abajo siga corriendo y tire error

# Si hay datos, el código llega hasta acá
filtro_fecha = st.date_input("Filtrar por fecha", value=None)

df_mostrar = df.copy()

# convertir columna a datetime (ahora es seguro porque sabemos que hay datos)
df_mostrar["fecha"] = pd.to_datetime(df_mostrar["fecha"], errors="coerce")

# aplicar filtro si se eligió fecha
if filtro_fecha:
    filtro_fecha = pd.to_datetime(filtro_fecha)
    # Filtramos comparando solo la fecha (sin hora)
    df_mostrar = df_mostrar[df_mostrar["fecha"].dt.date == filtro_fecha.date()]

# ordenar pedidos
df_mostrar = df_mostrar.sort_values(by="fecha", ascending=False)

# Mostrar tabla
st.dataframe(
    df_mostrar.rename(columns={
        "fecha": "Fecha",
        "detalle": "Detalle",
        "cliente": "Cliente",
        "monto": "Monto",
        "metodo_pago": "Método de Pago"
    }),
    use_container_width=True
)
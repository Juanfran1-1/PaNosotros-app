import pandas as pd
import streamlit as st

from data.modificador_db import cargar_datos



st.subheader("Historial de pedidos")

df = cargar_datos()

if df.empty:
    st.info("No hay pedidos cargados todavía.")

filtro_fecha = st.date_input("Filtrar por fecha", value=None)

df_mostrar = df.copy()

# convertir columna a datetime
df_mostrar["fecha"] = pd.to_datetime(df_mostrar["fecha"], errors="coerce")

# aplicar filtro si se eligió fecha
if filtro_fecha:
    filtro_fecha = pd.to_datetime(filtro_fecha)
    df_mostrar = df_mostrar[df_mostrar["fecha"] == filtro_fecha]

# ordenar pedidos
df_mostrar = df_mostrar.sort_values(by="fecha", ascending=False)

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
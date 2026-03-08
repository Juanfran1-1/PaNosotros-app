import pandas as pd
import streamlit as st
import streamlit as st

from data.modificador_db import cargar_datos, cargar_hamburguesas
from services.metricas import calcular_metricas, calcular_hamburguesas_mes


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión en la página principal para continuar.")
    st.stop()

st.subheader("Resumen general")

df = cargar_datos()
df_hamburguesas = cargar_hamburguesas()
TIPOS_HAMBURGUESA = df_hamburguesas["nombre"].tolist()

col1, col2, col3 = st.columns([2, 2, 1])

with col2:
    st.image("logo.png", width=250)

if df.empty:
    st.info("Todavía no hay pedidos cargados.")
else :

    ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital = calcular_metricas(df)

    col1, col2 = st.columns(2)
    col1.metric("Ventas de hoy", f"${ventas_hoy:,.0f}")
    col2.metric("Pedidos de hoy", pedidos_hoy)

    col3, col4 = st.columns(2)
    col3.metric("Ventas del mes", f"${ventas_mes:,.0f}")
    col4.metric("Pedidos del mes", pedidos_mes)

    col5, col6 = st.columns(2)
    col5.metric("Efectivo", f"${efectivo:,.0f}")
    col6.metric("Virtual", f"${digital:,.0f}")

    st.divider()
    st.subheader("Hamburguesas vendidas en el mes")

    conteo_hamburguesas = calcular_hamburguesas_mes(df, TIPOS_HAMBURGUESA)

    df_conteo = pd.DataFrame(
        {
            "Hamburguesa": list(conteo_hamburguesas.keys()),
            "Cantidad vendida": list(conteo_hamburguesas.values())
        }
    )
    cols = st.columns(len(TIPOS_HAMBURGUESA))

    for i, tipo in enumerate(TIPOS_HAMBURGUESA):
        cols[i].metric(tipo, conteo_hamburguesas[tipo])
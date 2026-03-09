import pandas as pd
import streamlit as st
import plotly.express as px 

from datetime import datetime
from utils.diseno import aplicar_estilos
from data.modificador_db import cargar_datos, cargar_hamburguesas
from services.metricas import calcular_metricas, calcular_hamburguesas_mes

# 1. Configuración de página (Debe ser lo primero)
st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")

# 2. Aplicar el CSS centralizado
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    
    # Creamos un botón que lo lleva a la página principal
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") # <--- Asegurate de que el nombre coincida con tu archivo principal
    
    st.stop()

# Configuración de encabezado
st.title("Dashboard de Ventas")
st.divider()

# --- TRY PARA CARGAR DATOS ---
try:
    df = cargar_datos()
    df_hamburguesas = cargar_hamburguesas()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

if df.empty:
    st.info("Todavía no hay pedidos cargados. ¡A empezar a vender!")
else:
    # --- TRY PARA CÁLCULOS DE MÉTRICAS ---
    try:
        ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital = calcular_metricas(df)
        TIPOS_HAMBURGUESA = df_hamburguesas["nombre"].tolist()
        conteo = calcular_hamburguesas_mes(df, TIPOS_HAMBURGUESA)
    except Exception as e:
        st.error(f"Error al procesar las métricas: {e}")
        st.stop()

    st.subheader("Hoy")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Ventas Hoy", f"${ventas_hoy:,.0f}")
    c2.metric("📦 Pedidos Hoy", pedidos_hoy)
    c3.metric("💵 Efectivo", f"${efectivo:,.0f}")
    c4.metric("💳 Virtual", f"${digital:,.0f}")

    st.subheader("Mes actual")
    m1, m2 = st.columns(2)
    m1.metric("📈 Total Ventas Mes", f"${ventas_mes:,.0f}")
    m2.metric("🍔 Total Pedidos Mes", pedidos_mes)

    st.divider()

    # 2. GRÁFICOS DE GESTIÓN
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Hamburguesas más vendidas")
        # --- TRY PARA EL GRÁFICO DE BARRAS ---
        try:
            df_conteo = pd.DataFrame({
                "Hamburguesa": list(conteo.keys()),
                "Cantidad": list(conteo.values())
            }).sort_values(by="Cantidad", ascending=True)

            fig_bar = px.bar(df_conteo, x="Cantidad", y="Hamburguesa", orientation='h',
                            color="Cantidad", color_continuous_scale="Reds")
            fig_bar.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
        except Exception as e:
            st.error(f"Error al generar gráfico de barras: {e}")

    with col_der:
        st.subheader("💳 Métodos de Pago")
        # --- TRY PARA EL GRÁFICO DE TORTA ---
        try:
            df_pagos = pd.DataFrame({
                "Método": ["Efectivo", "Virtual"],
                "Monto": [efectivo, digital]
            })
            fig_pie = px.pie(df_pagos, values="Monto", names="Método", 
                            color_discrete_sequence=["#2ecc71", "#3498db"])
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        except Exception as e:
            st.error(f"Error al generar gráfico de torta: {e}")

    # 3. DETALLE POR TIPO (Métricas individuales)
    st.subheader("Detalle por producto (Unidades)")
    if TIPOS_HAMBURGUESA:
        cols = st.columns(len(TIPOS_HAMBURGUESA))
        for i, tipo in enumerate(TIPOS_HAMBURGUESA):
            cols[i].metric(tipo, conteo.get(tipo, 0))

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
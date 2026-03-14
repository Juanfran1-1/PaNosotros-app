import pandas as pd
import streamlit as st
import plotly.express as px 
import time

from datetime import datetime
from utils.diseno import aplicar_estilos
from data.modificador_db import cargar_datos, cargar_hamburguesas
from services.metricas import calcular_metricas, calcular_hamburguesas_mes

# 1. Configuración de página
st.set_page_config(page_title="PA' NOSOTROS - DASHBOARD", page_icon="logo.png", layout="wide")

# 2. Aplicar el CSS centralizado
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

# Configuración de encabezado
st.title("📊 Dashboard de Ventas")
st.caption(f"Última actualización: {time.strftime('%H:%M:%S')}")
st.divider()

# --- CARGA DE DATOS ---
try:
    df = cargar_datos()
    df_hamburguesas = cargar_hamburguesas()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

if df.empty:
    st.info("Todavía no hay pedidos cargados. ¡A empezar a vender!")
else:
    # --- LIMPIEZA Y FILTRADO ESTRICTO ---
    df['estado'] = df['estado'].astype(str).str.strip()
    df['metodo_pago'] = df['metodo_pago'].astype(str).str.strip()
    
    # 🟢 IMPORTANTE: Consideramos "cobrado" aquello que está Pagado o Terminado
    df_cobrado = df[df["estado"].isin(["Pagado", "Terminado"])].copy()

    # --- CÁLCULO DE MÉTRICAS ---
    try:
        ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital = calcular_metricas(df_cobrado)
        
        # 🟢 UNIFICACIÓN: Sumamos Mercado Pago y Transferencia en una sola bolsa si calcular_metricas no lo hizo
        monto_digital_total = df_cobrado[df_cobrado["metodo_pago"].isin(["Transferencia", "Mercado Pago"])]["monto"].sum()
        monto_efectivo = df_cobrado[df_cobrado["metodo_pago"] == "Efectivo"]["monto"].sum()

        TIPOS_HAMBURGUESA = df_hamburguesas["nombre"].tolist()
        conteo = calcular_hamburguesas_mes(df_cobrado, TIPOS_HAMBURGUESA)
    except Exception as e:
        st.error(f"Error al procesar las métricas: {e}")
        st.stop()

    # --- BLOQUE DE MÉTRICAS VISUALES ---
    st.subheader("💰 Ventas Confirmadas (Hoy)")
    c1, c2 = st.columns(2)
    c1.metric("Total Cobrado", f"${ventas_hoy:,.0f}")
    c2.metric("Pedidos Finalizados", pedidos_hoy)

    st.subheader("📅 Resumen del Mes")
    m1, m2 , m3 , m4= st.columns(4)
    m1.metric("Ingresos Totales Mes", f"${ventas_mes:,.0f}")
    m2.metric("Hamburguesas Vendidas", pedidos_mes)
    m3.metric("Efectivo", f"${monto_efectivo:,.0f}")
    m4.metric("Digital (MP/Transf)", f"${monto_digital_total:,.0f}") # <--- Unificado

    st.divider()

    # --- GRÁFICOS ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("🍔 Top Hamburguesas (Mes)")
        try:
            df_conteo = pd.DataFrame({
                "Hamburguesa": list(conteo.keys()),
                "Cantidad": list(conteo.values())
            }).sort_values(by="Cantidad", ascending=True)

            if df_conteo["Cantidad"].sum() > 0:
                fig_bar = px.bar(df_conteo, x="Cantidad", y="Hamburguesa", orientation='h',
                                color="Cantidad", color_continuous_scale="Reds")
                fig_bar.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No hay ventas registradas este mes para el gráfico.")
        except Exception as e:
            st.error(f"Error gráfico de barras: {e}")

    with col_der:
        st.subheader("💳 Distribución de Pagos")
        try:
            # 🟢 Gráfico unificado: Efectivo vs Digital
            df_pagos = pd.DataFrame({
                "Método": ["Efectivo", "Digital"],
                "Monto": [monto_efectivo, monto_digital_total]
            })
            
            if df_pagos["Monto"].sum() > 0:
                fig_pie = px.pie(df_pagos, values="Monto", names="Método", 
                                color_discrete_sequence=["#3473e9", "#42db34"],
                                hole=0.4) 
                fig_pie.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Sin datos de pago para mostrar.")
        except Exception as e:
            st.error(f"Error gráfico de torta: {e}")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
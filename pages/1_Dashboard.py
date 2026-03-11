import pandas as pd
import streamlit as st
import plotly.express as px 

from datetime import datetime
from utils.diseno import aplicar_estilos
from data.modificador_db import cargar_datos, cargar_hamburguesas
from services.metricas import calcular_metricas, calcular_hamburguesas_mes

# 1. Configuración de página
st.set_page_config(page_title="PA' NOSOTROS", page_icon="logo.png", layout="wide")

# 2. Aplicar el CSS centralizado
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

# Configuración de encabezado
st.title("Dashboard de Ventas")
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
    # --- FILTRO ESTRICTO (SOLO COBRADO) ---
    # Limpiamos el texto para evitar errores de espacios
    df['estado'] = df['estado'].astype(str).str.strip()
    
    # SOLO sumamos lo que ya pasó por caja
    df_cobrado = df[df["estado"].isin(["Pagado", "Terminado"])].copy()

    # --- CÁLCULO DE MÉTRICAS ---
    # Nota: Pasamos df_cobrado para el dinero, pero podrías pasar df completo si quieres 
    # que 'pedidos_hoy' cuente también los pendientes. Aquí usamos df_cobrado para todo.
    try:
        ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital = calcular_metricas(df_cobrado)
        
        TIPOS_HAMBURGUESA = df_hamburguesas["nombre"].tolist()
        conteo = calcular_hamburguesas_mes(df_cobrado, TIPOS_HAMBURGUESA)
    except Exception as e:
        st.error(f"Error al procesar las métricas: {e}")
        st.stop()

    # --- BLOQUE DE MÉTRICAS VISUALES ---
    st.subheader("Ventas Confirmadas (Hoy)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Cobrado Hoy", f"${ventas_hoy:,.0f}")
    c2.metric("📦 Entregas Pagas", pedidos_hoy)
    c3.metric("💵 En Efectivo", f"${efectivo:,.0f}")
    c4.metric("💳 En Virtual", f"${digital:,.0f}")

    st.subheader("Resumen Mes Confirmado")
    m1, m2 = st.columns(2)
    m1.metric("📈 Ventas Totales Mes", f"${ventas_mes:,.0f}")
    m2.metric("🍔 Hamburguesas Pagas", pedidos_mes)

    st.divider()

    # --- GRÁFICOS ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Hamburguesas más vendidas (Pagadas)")
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
        st.subheader("💳 Métodos de Pago Confirmados")
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

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
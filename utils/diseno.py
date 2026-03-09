import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
        /* 1. FONDO GENERAL */
        .stApp { 
            background-color: #FDFCF0; 
        }
        
        /* 2. TEXTOS CUERPO PRINCIPAL */
        /* Forzamos color café para que no queden letras blancas invisibles */
        [data-testid="stMain"] p, 
        [data-testid="stMain"] li, 
        [data-testid="stMain"] label,
        [data-testid="stMain"] span {
            color: #4A2C2A !important;
        }

        /* 3. BARRA LATERAL (Sidebar) */
        [data-testid="stSidebar"] { 
            background-color: #4A2C2A !important; 
        }
        
        /* Textos de la sidebar en crema para contraste */
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebarNav"] span { 
            color: #FDFCF0 !important; 
        }
        
        /* Iconos de la sidebar */
        [data-testid="stSidebarNav"] svg {
            fill: #FDFCF0 !important;
        }

        /* 4. TÍTULOS */
        h1, h2, h3 { 
            color: #4A2C2A !important; 
        }

        /* 5. BOTONES (CORREGIDOS) */
        /* Estilo base para todos los botones */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: bold !important;
            border: none !important;
            color: white !important; /* Texto siempre blanco */
        }

        /* Aseguramos que el texto dentro del botón sea blanco (evita letras negras) */
        .stButton > button p, .stButton > button span {
            color: white !important;
        }

        /* Botón Verde (tipo 'primary') */
        div.stButton > button[kind="primary"] {
            background-color: #28a745 !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #218838 !important;
        }

        /* Botón Rojo (tipo 'secondary') */
        div.stButton > button[kind="secondary"] {
            background-color: #D32F2F !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #B71C1C !important;
        }

        /* 6. INPUTS Y SELECTORES (Adiós a las cajas negras) */
        /* Cajas de selección, texto y números */
        div[data-baseweb="select"] > div, 
        .stTextInput input, 
        .stNumberInput input {
            background-color: white !important;
            color: #4A2C2A !important;
            border: 1px solid #4A2C2A !important;
        }

        /* Color del texto sugerido (placeholder) */
        input::placeholder {
            color: #A0A0A0 !important;
        }

        /* 7. MÉTRICAS (Dashboard) */
        [data-testid="stMetricValue"] {
            color: #D32F2F !important;
        }
        [data-testid="stMetricLabel"] p {
            color: #4A2C2A !important;
        }
        
        /* Estilo para las tarjetas de métricas */
        [data-testid="stMetric"] {
            background-color: white !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border: 1px solid #4A2C2A !important;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1) !important;
        }
        
        /* Forzar color de los números de métricas */
        [data-testid="stMetricValue"] div {
            color: #D32F2F !important; /* Rojo para los números importantes */
        }
    </style>
    """, unsafe_allow_html=True)
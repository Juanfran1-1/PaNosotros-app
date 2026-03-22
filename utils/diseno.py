import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
        /* 1. FONDO GENERAL */
        .stApp { 
            background-color: #FDFCF0; 
        }
        
        /* 2. TEXTOS CUERPO PRINCIPAL */
        /*color café para que no queden letras blancas invisibles */
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

        /* Aseguramos que el texto dentro del botón sea blanco  */
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

        /* 6. INPUTS Y SELECTORES */
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
        
        /* ARREGLO FINAL DEL HEADER Y TODOS SUS ÍCONOS (Estrella, Lápiz, GitHub, Menú) */
        header[data-testid="stHeader"] {
            background-color: #FDFCF0 !important;
            border-bottom: none !important;
        }

        
        header[data-testid="stHeader"] svg, 
        header[data-testid="stHeader"] a, 
        header[data-testid="stHeader"] button {
            fill: #4A2C2A !important;
            color: #4A2C2A !important;
            opacity: 0.6 !important; /* Suavizados para que no pesen */
            transition: opacity 0.3s !important;
        }

        /* Efecto hover para todos los elementos del header */
        header[data-testid="stHeader"] svg:hover, 
        header[data-testid="stHeader"] a:hover, 
        header[data-testid="stHeader"] button:hover {
            opacity: 1 !important;
            background-color: rgba(74, 44, 42, 0.05) !important; /* Un sutil brillo café al pasar el mouse */
            border-radius: 50%;
        }
        header[data-testid="stHeader"] span {
            color: #4A2C2A !important;
        }
        
        /* Contenedor principal del toggle */
        .stElementContainer div[data-testid="stCheckbox"] {
            background-color: #808080;
            padding: 15px 25px;
            border-radius: 15px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        /* Color cuando está ACTIVO (Abierto) */
        div[data-testid="stWidgetLabel"] + div [data-baseweb="checkbox"] [role="switch"][aria-checked="false"] {
            background-color: #2ecc71 !important; /* Verde éxito */
        }

        /* Color cuando está INACTIVO (Cerrado) */
        div[data-testid="stWidgetLabel"] + div [data-baseweb="checkbox"] [role="switch"][aria-checked="true"] {
            background-color: #e74c3c !important; /* Rojo error */
        }
        
    
    </style>
    """, unsafe_allow_html=True)
import streamlit as st
from data.database import inicializar_db

st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

# --- FUNCIÓN DE LOGIN ---
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.image("logo.png", width=250)

            st.title("Iniciar Sesión")
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            
            if st.button("Ingresar"):
                # Validamos contra los Secrets de Streamlit Cloud
                if usuario == st.secrets["credentials"]["user"] and clave == st.secrets["credentials"]["password"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
        return False
    return True

# --- EJECUCIÓN PRINCIPAL ---
if login():
    inicializar_db()

    col1, col2, col3 = st.columns([2, 2, 1])

    with col2:
        st.image("logo.png", width=250)

    st.title("¡Bienvenido a PA' NOSOTROS!")
    st.markdown(
        """
        ### 🍔 UNA HAMBURGUESERÍA DEDICADA SOLO PARA NOSOTROS
        *Los verdaderos amantes de las minihamburguesas.*

        ---
        **¿Qué querés hacer hoy?**
        * Usa el **Dashboard** para ver cómo vienen las ventas.
        * Entra a **Registrar Pedido** para anotar un nuevo pedido.
        """
    )
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()
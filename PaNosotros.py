import streamlit as st

from data.database import inicializar_db


st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

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

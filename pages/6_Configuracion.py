import streamlit as st
from utils.diseno import aplicar_estilos
from data.database import get_connection
from data.modificador_db import cargar_configuracion

st.set_page_config(page_title="PA' NOSOTROS - CONFIGURACIÓN", page_icon="logo.png", layout="wide")
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión.")
    st.stop()

# Función auxiliar para actualizar solo un campo a la vez
def actualizar_campo(columna, valor):
    try:
        client = get_connection()
        client.table("configuracion").update({columna: valor}).eq("id", config.get("id")).execute()
        st.toast(f"✅ {columna.replace('_', ' ').capitalize()} actualizado", icon="🚀")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Carga inicial
config = cargar_configuracion()

st.title("⚙️ Panel de Control")

# --- SECCIÓN 1: ESTADO DEL LOCAL (INSTANTÁNEO) ---
st.subheader("🚀 Estado del Local")
estado_actual = config.get("abierto", True)

# Al tocar el toggle, se ejecuta la actualización inmediatamente
nuevo_estado = st.toggle("Abrir Local / Recibir Pedidos", value=estado_actual, key="toggle_abierto")

if nuevo_estado != estado_actual:
    actualizar_campo("abierto", nuevo_estado)
    st.rerun()

if nuevo_estado:
    st.success("El local está recibiendo pedidos ✅")
else:
    st.error("El local está CERRADO ❌")

st.divider()

# --- SECCIÓN 2: ALIAS MERCADO PAGO ---
st.subheader("💳 Finanzas")
col_alias, col_btn_alias = st.columns([3, 1])

with col_alias:
    alias_input = st.text_input("Alias de Mercado Pago", value=config.get("alias_mp", ""))
with col_btn_alias:
    st.write(" ") # Espaciado
    if st.button("Guardar Alias", use_container_width=True,type="primary"):
        actualizar_campo("alias_mp", alias_input)

st.divider()

# --- SECCIÓN 3: LOGÍSTICA (COSTO ENVÍO) ---
st.subheader("🚚 Logística")
col_envio, col_btn_envio = st.columns([3, 1])

with col_envio:
    envio_input = st.number_input("Costo de Envío ($)", value=int(config.get("COSTO_ENVIO", 0)), step=50)
with col_btn_envio:
    st.write(" ")
    if st.button("Guardar Envío", use_container_width=True,type="primary"):
        actualizar_campo("COSTO_ENVIO", envio_input)

st.divider()

# --- SECCIÓN 4: CONTACTO (WHATSAPP) ---
st.subheader("📱 WhatsApp de Pedidos")
col_ws, col_btn_ws = st.columns([3, 1])

with col_ws:
    ws_input = st.text_input("Número (ej: 5491122334455)", value=config.get("whatsapp", ""))
with col_btn_ws:
    st.write(" ")
    if st.button("Guardar WhatsApp", use_container_width=True,type="primary"):
        actualizar_campo("whatsapp", ws_input)
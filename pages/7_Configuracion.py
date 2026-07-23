import streamlit as st
import re
from utils.diseno import aplicar_estilos, page_header, section_note
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
        data = {"id": config.get("id", 1), columna: valor}
        client.table("configuracion").upsert(data).execute()
        st.toast(f"✅ {columna.replace('_', ' ').capitalize()} actualizado", icon="🚀")
    except Exception as e:
        st.error(f"❌ Error: {e}")

def normalizar_whatsapp(numero):
    return re.sub(r"\D", "", str(numero or ""))

# Carga inicial
config = cargar_configuracion()

page_header(
    "Configuración",
    "Ajustes generales del local, pagos, envíos y textos visibles en el menú."
)

# --- SECCIÓN 1: ESTADO DEL LOCAL (INSTANTÁNEO) ---
st.subheader("🚀 Estado del Local")
section_note("Este cambio se refleja en el menú del cliente. Si cerrás el local, pueden ver la carta pero no pedir.")
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

# --- SECCIÓN 2: MODO MANTENIMIENTO ---
st.subheader("🛠️ Aplicación de clientes")
section_note("Al activarlo, se bloquean el menú y los pedidos. Los clientes solo ven la pantalla informativa y el acceso a Instagram.")
mantenimiento_actual = config.get("mantenimiento", False)

nuevo_mantenimiento = st.toggle(
    "Activar modo mantenimiento",
    value=mantenimiento_actual,
    key="toggle_mantenimiento"
)

if nuevo_mantenimiento != mantenimiento_actual:
    actualizar_campo("mantenimiento", nuevo_mantenimiento)
    st.rerun()

if nuevo_mantenimiento:
    st.warning("La aplicación de clientes está en MODO MANTENIMIENTO 🛠️")
else:
    st.success("La aplicación de clientes está habilitada ✅")

st.divider()

# --- SECCIÓN 3: ALIAS MERCADO PAGO ---
st.subheader("💳 Finanzas")
col_alias, col_btn_alias = st.columns([3, 1])

with col_alias:
    alias_input = st.text_input("Alias de Mercado Pago", value=config.get("alias_mp", ""))
with col_btn_alias:
    st.write(" ") # Espaciado
    if st.button("Guardar Alias", use_container_width=True,type="primary"):
        actualizar_campo("alias_mp", alias_input)

st.divider()

# --- SECCIÓN 4: LOGÍSTICA (COSTO ENVÍO) ---
st.subheader("🚚 Logística")
col_envio, col_btn_envio = st.columns([3, 1])

with col_envio:
    envio_input = st.number_input("Costo de Envío ($)", value=int(config.get("COSTO_ENVIO", 0)), step=50)
with col_btn_envio:
    st.write(" ")
    if st.button("Guardar Envío", use_container_width=True,type="primary"):
        actualizar_campo("COSTO_ENVIO", envio_input)

st.divider()

# --- SECCIÓN 5: RETIRO EN LOCAL ---
st.subheader("📍 Retiro en local")
col_dir_local, col_btn_dir_local = st.columns([3, 1])

with col_dir_local:
    dir_local_input = st.text_input("Dirección del local", value=config.get("direccion_local", ""))
with col_btn_dir_local:
    st.write(" ")
    if st.button("Guardar Dirección", use_container_width=True,type="primary"):
        actualizar_campo("direccion_local", dir_local_input)

st.divider()

# --- SECCIÓN 6: PROMOS ---
st.subheader("🎁 Promos")
col_promo_titulo, col_btn_promo_titulo = st.columns([3, 1])

with col_promo_titulo:
    promo_titulo_input = st.text_input(
        "Título del carrusel de promos",
        value=config.get("promo_titulo", ""),
        placeholder="Día de la Mini Burger"
    )
with col_btn_promo_titulo:
    st.write(" ")
    if st.button("Guardar Título", use_container_width=True,type="primary"):
        actualizar_campo("promo_titulo", promo_titulo_input)

st.caption("Este texto aparece en el carrusel de promos del inicio.")

st.divider()

# --- SECCIÓN 7: CONTACTO (WHATSAPP) ---
st.subheader("📱 WhatsApp de Pedidos")
col_ws, col_btn_ws = st.columns([3, 1])

with col_ws:
    ws_input = st.text_input("Número (ej: 5491122334455)", value=config.get("whatsapp", ""))
with col_btn_ws:
    st.write(" ")
    if st.button("Guardar WhatsApp", use_container_width=True,type="primary"):
        ws_normalizado = normalizar_whatsapp(ws_input)
        if not ws_normalizado:
            st.error("Ingresá un número de WhatsApp válido.")
        else:
            actualizar_campo("whatsapp", ws_normalizado)

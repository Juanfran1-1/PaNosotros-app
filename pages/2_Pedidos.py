import streamlit as st
import time
from utils.diseno import aplicar_estilos
from data.modificador_db import cargar_datos, actualizar_estado_pedido

# Configuración básica
st.set_page_config(page_title="PA' NOSOTROS - GESTIÓN", page_icon="logo.png", layout="wide")
aplicar_estilos()

# Verificación de sesión
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    st.stop()

st.title("👨‍🍳 Gestión de Pedidos en Vivo")
st.markdown("---")

# El multiselect lo dejamos FUERA del fragmento para que el usuario pueda interactuar 
# sin que se le cierre el menú desplegable cada vez que la página busca datos nuevos.
estados_visibles = st.multiselect(
    "Ver pedidos con estado:",
    ["Pendiente de Pago", "Pagado", "Terminado", "Rechazado"],
    default=["Pendiente de Pago", "Pagado"]
)

# --- FRAGMENTO DE ACTUALIZACIÓN AUTOMÁTICA ---
@st.fragment(run_every=30)
def mostrar_gestion_pedidos(filtros):
    # Carga de datos fresca
    df = cargar_datos()
    
    st.caption(f"Última actualización de cocina: {time.strftime('%H:%M:%S')}")

    if df.empty:
        st.info("No hay pedidos registrados por el momento.")
        return

    # Filtrar el DataFrame según la selección del multiselect
    df_filtrado = df[df['estado'].isin(filtros)]

    if df_filtrado.empty:
        st.write("No hay pedidos con esos estados.")
    else:
        # Dibujamos cada pedido como una tarjeta
        for _, p in df_filtrado.iterrows():
            # Definir color según estado
            color_estado = "#D32F2F" if p['estado'] == "Pendiente de Pago" else "#2E7D32"
            
            with st.container(border=True):
                col_info, col_btns = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"### 👤 {p['cliente']}")
                    st.markdown(f"**Estado:** :{color_estado}[{p['estado']}]")
                    st.write(f"**🍔 Detalle:** {p['detalle']}")
                    st.write(f"**💰 Monto:** ${p['monto']} | **Método:** {p['metodo_pago']}")
                    
                    if p['entrega'] == "Delivery":
                        st.write(f"📍 **Dirección:** {p['direccion']}")
                    else:
                        st.write("🏬 **Retira en local**")

                with col_btns:
                    st.write("¿Acciones?")
                    
                    # 1. Botón para PAGADO
                    if p['estado'] == "Pendiente de Pago":
                        if st.button("💰 Marcar Pagado", key=f"pag_{p['id']}", use_container_width=True):
                            if actualizar_estado_pedido(p['id'], "Pagado"):
                                st.rerun()

                        # 2. Botón para RECHAZAR
                        if st.button("❌ Rechazar", key=f"rech_{p['id']}", use_container_width=True):
                            if actualizar_estado_pedido(p['id'], "Rechazado"):
                                st.rerun()

                    # 3. Botón para TERMINADO
                    if p['estado'] == "Pagado":
                        if st.button("✅ Terminado", key=f"term_{p['id']}", use_container_width=True):
                            if actualizar_estado_pedido(p['id'], "Terminado"):
                                st.rerun()

# Llamada a la función del fragmento pasando los filtros elegidos
mostrar_gestion_pedidos(estados_visibles)

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
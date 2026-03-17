import streamlit as st
import time
import datetime
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
st.subheader("Si el pedido es Transferencia, los estados son 'Pendiente de Pago' → 'Cocinando' → 'Terminado'.")
st.subheader("Si el pedido es Efectivo, los estados son 'Confirmar Pedido' → 'Cocinando' → 'Pendiente de Pago' → 'Terminado'.")
st.markdown("---")

# 1. Agregamos "Cocinando" a la lista de estados visibles por defecto
estados_visibles = st.multiselect(
    "Ver pedidos con estado:",
    ["Pendiente de Pago", "Cocinando", "Terminado", "Rechazado"],
    default=["Pendiente de Pago", "Cocinando"]
)

# --- FRAGMENTO DE ACTUALIZACIÓN AUTOMÁTICA ---
@st.fragment(run_every=30)
def mostrar_gestion_pedidos(filtros):
    df = cargar_datos()
    
    if df.empty:
        st.info("No hay pedidos registrados.")
        return

    # Filtramos por los estados seleccionados en el multiselect
    df_activos = df[df['estado'].isin(filtros)]

    if df_activos.empty:
        st.write("No hay pedidos con esos estados ahora mismo.")
        return

    hora_argentina = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3)

    # Lo mostramos formateado
    st.caption(f"Última actualización: {hora_argentina.strftime('%H:%M:%S')}")

    for _, p in df_activos.iterrows():
        with st.container():
            col_info, col_accion = st.columns([3, 1])
            
            with col_info:
                st.subheader(f"{p['cliente']} - {p['metodo_pago']}")
                st.subheader(f"Telefono: {p['numero']}")
                st.subheader(f"{p['estado']}")
                st.write(f"🍔 {p['detalle']}")
                st.caption(f"💰 ${p['monto']} | {p['entrega']} | {p['fecha']}")

            with col_accion:
                # --- LÓGICA PARA TRANSFERENCIA (Basado en lo que manda tu JS) ---
                if p['metodo_pago'] == "Transferencia":
                    if p['estado'] == "Pendiente de Pago":
                        if st.button("💳 Cobrar", key=f"pay_{p['id']}", use_container_width=True):
                            actualizar_estado_pedido(p['id'], "Cocinando")
                            st.rerun()
                    elif p['estado'] == "Cocinando":
                        if st.button("✅ Cerrar pedido", key=f"done_{p['id']}", use_container_width=True, type="primary"):
                            actualizar_estado_pedido(p['id'], "Terminado")
                            st.rerun()

                # --- LÓGICA PARA EFECTIVO ---
                else:
                    if p['estado'] == "Esperando Confirmacion":
                        if st.button("✅ Confirmar pedido", key=f"confirm_{p['id']}", use_container_width=True, type="primary"):
                            actualizar_estado_pedido(p['id'], "Cocinando")
                            st.rerun()
                    elif p['estado'] == "Cocinando":
                        if st.button("✅ Cerrar pedido", key=f"done_ef_{p['id']}", use_container_width=True , type="primary"):
                            actualizar_estado_pedido(p['id'], "Pendiente de Pago")
                            st.rerun()
                    elif p['estado'] == "Pendiente de Pago":
                        if st.button("💵 Cobrado", key=f"pay_ef_{p['id']}", use_container_width=True, type="primary"):
                            actualizar_estado_pedido(p['id'], "Terminado")
                            st.rerun()
                
                # Botón cancelar siempre disponible
                if (p['estado'] != "Terminado" and p['estado'] != "Rechazado") and st.button("🚫 Cancelar", key=f"can_{p['id']}", use_container_width=True, type="secondary"):
                    actualizar_estado_pedido(p['id'], "Rechazado")
                    st.rerun()
        st.divider()

# Llamada a la función
mostrar_gestion_pedidos(estados_visibles)

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
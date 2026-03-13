import streamlit as st
from datetime import datetime
import time
from data.modificador_db import guardar_pedido, cargar_hamburguesas
from utils.diseno import aplicar_estilos

# Configuración de página
st.set_page_config(page_title="PA' NOSOTROS - REGISTRAR", page_icon="logo.png", layout="wide")
aplicar_estilos()

# Verificación de sesión
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py") 
    st.stop()

st.title("📝 Registrar Nuevo Pedido")

# Cargar productos desde DB
df_hamburguesas = cargar_hamburguesas()
tipos_hamburguesa = df_hamburguesas["nombre"].tolist()

if "pedido_actual" not in st.session_state:
    st.session_state.pedido_actual = []

# --- SECCIÓN: SELECCIÓN DE PRODUCTOS ---
col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Elegí la hamburguesa", tipos_hamburguesa)

with col2:
    cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)

# Botón Agregar
if st.button("➕ Agregar al pedido", type="primary", use_container_width=True):
    encontrada = False
    for item in st.session_state.pedido_actual:
        if item["tipo"] == tipo:
            item["cantidad"] += int(cantidad)
            encontrada = True
            break
    if not encontrada:
        st.session_state.pedido_actual.append({"tipo": tipo, "cantidad": int(cantidad)})
    st.rerun()

st.divider()

# --- SECCIÓN: RESUMEN DEL PEDIDO ACTUAL ---
st.markdown("### 🛒 Resumen del Pedido")

if not st.session_state.pedido_actual:
    st.info("El carrito está vacío.")
else:
    total_hamburguesas = 0
    total_pedido = 0

    # Cabecera de la tabla
    h1, h2, h3, h4 = st.columns([3, 1, 2, 1])
    h1.markdown("**Producto**")
    h2.markdown("**Cant.**")
    h3.markdown("**Subtotal**")
    h4.markdown("**Acción**")

    # Lista de productos en el carrito
    for i, item in enumerate(st.session_state.pedido_actual):
        precio = df_hamburguesas.loc[df_hamburguesas["nombre"] == item["tipo"], "precio"].values[0]
        subtotal = item["cantidad"] * precio
        total_hamburguesas += item["cantidad"]
        total_pedido += subtotal

        c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
        c1.write(item['tipo'])
        c2.write(f"{item['cantidad']}x")
        c3.write(f"${subtotal:,.0f}")
        
        # Botón para quitar el item por completo
        if c4.button("🗑️", key=f"del_{i}"):
            st.session_state.pedido_actual.pop(i)
            st.rerun()

    st.divider()

    t1, t2 = st.columns(2)
    t1.metric("Total unidades", total_hamburguesas)
    t2.metric("Total a cobrar", f"${total_pedido:,.0f}")

    st.markdown("### 👤 Datos de Cliente y Pago")
    cliente = st.text_input("Nombre del cliente")
    numero_tel = st.text_input("Número de WhatsApp (ej: 2215556677)") # <--- NUEVO CAMPO
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        tipo_entrega = st.radio("¿Cómo se entrega?", ["Retiro", "Delivery"], horizontal=True)
    
    direccion = "Retira en local"
    if tipo_entrega == "Delivery":
        with col_e2:
            direccion = st.text_input("📍 Dirección de envío")

    # 🟢 CAMBIO: Usamos "Transferencia" para que coincida con la Web y el Dashboard
    metodo_pago = st.selectbox("Método de pago", ["Efectivo", "Transferencia"])

    st.write("") 

    # --- BOTONES DE ACCIÓN ---
    g1, g2 = st.columns(2)

    with g1:
        if st.button("✅ GUARDAR PEDIDO", use_container_width=True, type="primary"):
            if cliente.strip() == "" or numero_tel.strip() == "":
                st.error("Faltan datos del cliente (nombre o teléfono).")
            elif tipo_entrega == "Delivery" and (not direccion or direccion == "Retira en local"):
                st.error("Si es Delivery, tenés que poner una dirección.")
            elif not st.session_state.pedido_actual:
                st.error("El carrito está vacío.")
            else:
                detalle_productos = " | ".join(f"{item['cantidad']}x {item['tipo']}" for item in st.session_state.pedido_actual)
                fecha_y_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 🟢 LÓGICA DE ESTADO DINÁMICO:
                # Si es Transferencia -> Pendiente de Pago (Hay que chequear el celu)
                # Si es Efectivo -> Cocinando (Se cobra al entregar)
                # 1. Definís el estado según el pago
                estado_inicial = "Pendiente de Pago" if metodo_pago == "Transferencia" else "Cocinando"

                # 2. Se lo pasás a la función (asegurándote que guardar_pedido acepte ese argumento)
                exito = guardar_pedido(
                    fecha_y_hora, 
                    detalle_productos, 
                    cliente.strip(), 
                    numero_tel.strip(), # <--- Enviamos el número
                    total_pedido, 
                    metodo_pago, 
                    tipo_entrega, 
                    direccion.strip(),
                    estado_inicial 
                )

                if exito:
                    st.session_state.pedido_actual = []
                    st.success(f"¡Pedido guardado! Estado: {estado_inicial}")
                    time.sleep(1.5)
                    st.rerun()
    with g2:
        if st.button("🗑️ VACIAR CARRITO", use_container_width=True, type="secondary"):
            st.session_state.pedido_actual = []
            st.rerun()

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
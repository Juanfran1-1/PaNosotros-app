import streamlit as st
from datetime import date
import time

from data.modificador_db import guardar_pedido, cargar_hamburguesas

# BLOQUEO DE SEGURIDAD
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión en la página principal para continuar.")
    st.stop()

st.subheader("Registrar nuevo pedido")

df_hamburguesas = cargar_hamburguesas()
tipos_hamburguesa = df_hamburguesas["nombre"].tolist()

if "pedido_actual" not in st.session_state:
    st.session_state.pedido_actual = []

col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Tipo de hamburguesa", tipos_hamburguesa)

with col2:
    cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)

if st.button("Agregar hamburguesa"):
    encontrada = False

    for item in st.session_state.pedido_actual:
        if item["tipo"] == tipo:
            item["cantidad"] += int(cantidad)
            encontrada = True
            break

    if not encontrada:
        st.session_state.pedido_actual.append({
            "tipo": tipo,
            "cantidad": int(cantidad)
        })

    st.rerun()

st.markdown("### Pedido actual")

if not st.session_state.pedido_actual:
    st.info("Todavía no agregaste hamburguesas al pedido.")


total_hamburguesas = 0
total_pedido = 0

h1, h2, h3, h4 = st.columns([4, 1, 2, 1])
h1.markdown("**Hamburguesa**")
h2.markdown("**Cant.**")
h3.markdown("**Subtotal**")
h4.markdown("**Quitar**")
st.divider()

for i, item in enumerate(st.session_state.pedido_actual):
    precio = df_hamburguesas.loc[
        df_hamburguesas["nombre"] == item["tipo"], "precio"
    ].values[0]

    subtotal = item["cantidad"] * precio
    total_hamburguesas += item["cantidad"]
    total_pedido += subtotal

    c1, c2, c3, c4 = st.columns([4, 1, 2, 1])
    c1.write(f"**{item['tipo']}**")
    c2.write(f"**{item['cantidad']}x**")
    c3.write(f"**${subtotal:,.0f}**")

    if c4.button("❌", key=f"eliminar_{i}"):
        st.session_state.pedido_actual.pop(i)
        st.rerun()

st.divider()

t1, t2 = st.columns(2)
t1.metric("Total hamburguesas", total_hamburguesas)
t2.metric("Total a cobrar", f"${total_pedido:,.0f}")

cliente = st.text_input("Nombre o número del cliente")
metodo_pago = st.selectbox("Método de pago", ["Efectivo", "Virtual"])

g1, g2 = st.columns(2)

with g1:
    if st.button("Guardar pedido"):
        if cliente.strip() == "":
            st.error("Tenés que ingresar el nombre o número del cliente.")
        else:
            detalle = " | ".join(
                f"{item['cantidad']}x {item['tipo']}"
                for item in st.session_state.pedido_actual
            )

            guardar_pedido(
                date.today(),
                detalle,
                cliente.strip(),
                total_pedido,
                metodo_pago
            )

            st.session_state.pedido_actual = []
            st.success("Pedido guardado correctamente.")
            time.sleep(1.5)
            st.rerun()

with g2:
    if st.button("Vaciar pedido"):
        st.session_state.pedido_actual = []
        st.warning("Se vació el pedido actual.")
        st.rerun()
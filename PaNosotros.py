import base64
from pathlib import Path

import streamlit as st
from utils.diseno import aplicar_estilos

st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

aplicar_estilos()


def cargar_logo_data_uri():
    try:
        data = Path("logo.png").read_bytes()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode('ascii')}"
    except Exception:
        return ""


# ---------------- LOGIN ----------------
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            c1, c2, c3 = st.columns([1, 2, 1])

            with c2:
                try:
                    st.image("logo.png", width=250)
                    st.title("Iniciar Sesión")
                except:
                    pass

            st.text_input(
                "Usuario",
                key="login_user",
                autocomplete="username"
            )

            st.text_input(
                "Contraseña",
                type="password",
                key="login_pass",
                autocomplete="current-password"
            )

            if st.button("Ingresar", type="primary", use_container_width=True):
                try:
                    user_real = st.secrets["credentials"]["user"]
                    pass_real = st.secrets["credentials"]["password"]

                    usuario = st.session_state.get("login_user", "").strip()
                    clave = st.session_state.get("login_pass", "").strip()

                    if usuario != user_real:
                        st.error("Usuario incorrecto")

                    elif clave != pass_real:
                        st.error("Contraseña incorrecta")

                    else:
                        st.session_state.authenticated = True
                        st.rerun()

                except KeyError:
                    st.error("❌ No se encontraron las credenciales en Secrets.")

                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")

        return False

    return True


# ---------------- HOME ----------------
if login():
    logo_src = cargar_logo_data_uri()
    logo_html = f'<img class="pa-home-logo" src="{logo_src}" alt="Logo Pa Nosotros">' if logo_src else ""

    st.markdown(
        f"""
        <div class="pa-home-hero">
            {logo_html}
            <div>
                <p class="pa-home-kicker">Panel interno</p>
                <h1>PA' <span>NOSOTROS</span></h1>
                <p>Gestioná ventas, pedidos, productos, promos, reseñas y configuración desde un solo lugar.</p>
            </div>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )

    st.markdown('<h2 class="pa-home-section-title">Accesos rápidos</h2>', unsafe_allow_html=True)

    # FILA 1
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>📊 Dashboard</h3><p>Ventas, ingresos, pagos y productos más vendidos.</p></div>', unsafe_allow_html=True)
            if st.button("Abrir Dashboard", key="home_dashboard", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Dashboard.py")

    with col2:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>⭐ Reseñas</h3><p>Opiniones del menú con filtros por puntaje.</p></div>', unsafe_allow_html=True)
            if st.button("Ver Reseñas", key="home_resenas", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Resenas.py")

    with col3:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>🧾 Pedidos</h3><p>Seguimiento operativo de pedidos en vivo.</p></div>', unsafe_allow_html=True)
            if st.button("Gestionar Pedidos", key="home_pedidos", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Pedidos.py")

    # FILA 2
    col4, col5, col6 = st.columns(3)

    with col4:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>🍔 Productos</h3><p>Alta, edición y disponibilidad de mini burgers.</p></div>', unsafe_allow_html=True)
            if st.button("Administrar Productos", key="home_productos", use_container_width=True, type="primary"):
                st.switch_page("pages/3_Productos.py")

    with col5:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>🔥 Promos</h3><p>Combos, precios y configuraciones de promociones.</p></div>', unsafe_allow_html=True)
            if st.button("Administrar Promos", key="home_promos", use_container_width=True, type="primary"):
                st.switch_page("pages/4_Promos.py")

    with col6:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>📜 Historial</h3><p>Consulta de pedidos anteriores y ventas cerradas.</p></div>', unsafe_allow_html=True)
            if st.button("Ver Historial", key="home_historial", use_container_width=True, type="primary"):
                st.switch_page("pages/5_Historial.py")

    # FILA 3
    col7, col8, col9 = st.columns(3)

    with col7:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>➕ Registrar</h3><p>Carga manual de pedidos cuando haga falta.</p></div>', unsafe_allow_html=True)
            if st.button("Registrar Pedido", key="home_registrar", use_container_width=True, type="primary"):
                st.switch_page("pages/6_Registrar.py")

    with col8:
        with st.container(border=False):
            st.markdown('<div class="pa-home-card"><h3>⚙️ Configuración</h3><p>Horarios, envío y ajustes generales del sistema.</p></div>', unsafe_allow_html=True)
            if st.button("Abrir Configuración", key="home_configuracion", use_container_width=True, type="primary"):
                st.switch_page("pages/7_Configuracion.py")

    st.divider()

    if st.sidebar.button(
        "Cerrar Sesión",
        type="secondary",
        use_container_width=True
    ):
        st.session_state.authenticated = False
        st.rerun()

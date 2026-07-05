import streamlit as st
from utils.diseno import aplicar_estilos, page_header

st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

aplicar_estilos()


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

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        try:
            st.image("logo.png", width=220)
        except:
            pass

    page_header(
        "PA' NOSOTROS",
        "Panel interno para gestionar pedidos, productos, promos y configuración."
    )

    st.markdown(
        """
        ### 🍔 Panel interno
        
        Accedé rápidamente a cualquier sección del sistema.
        """
    )

    st.divider()

    # FILA 1
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "📊 Dashboard",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/1_Dashboard.py")

    with col2:
        if st.button(
            "⭐ Reseñas",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/1_Resenas.py")

    with col3:
        if st.button(
            "🧾 Pedidos",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/2_Pedidos.py")

    # FILA 2
    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button(
            "🍔 Productos",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/3_Productos.py")

    with col5:
        if st.button(
            "🔥 Promos",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/4_Promos.py")

    with col6:
        if st.button(
            "📜 Historial",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/5_Historial.py")

    # FILA 3
    col7, col8, col9 = st.columns(3)

    with col7:
        if st.button(
            "➕ Registrar",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/6_Registrar.py")

    with col8:
        if st.button(
            "⚙️ Configuración",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page("pages/7_Configuracion.py")

    st.divider()

    if st.sidebar.button(
        "Cerrar Sesión",
        type="secondary",
        use_container_width=True
    ):
        st.session_state.authenticated = False
        st.rerun()

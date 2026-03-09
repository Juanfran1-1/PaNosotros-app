import streamlit as st
from utils.diseno import aplicar_estilos

st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

aplicar_estilos()

# --- FUNCIÓN DE LOGIN ---
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Sub-columnas para centrar la imagen
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                try:
                    st.image("logo.png", width=250)
                    st.title("Iniciar Sesión")
                except:
                    pass

            
            usuario_ingresado = st.text_input("Usuario")
            clave_ingresada = st.text_input("Contraseña", type="password")
            
            if st.button("Ingresar"):
                try:
                    user_real = st.secrets["credentials"]["user"]
                    pass_real = st.secrets["credentials"]["password"]
                    
                    if usuario_ingresado.strip() != user_real:
                        st.error("Usuario incorrecto")
                    elif clave_ingresada.strip() != pass_real:
                        st.error("Contraseña incorrecta")
                    else:
                        st.session_state.authenticated = True
                        st.rerun()
                        
                except KeyError:
                    st.error("❌ Error: No se encontraron las credenciales en 'Secrets'.")
                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")
        return False
    return True

if login():

    col1, col2, col3 = st.columns([1, 1, 1]) 

    with col2:
        try:
            st.image("logo.png", width=250)
        except:
            pass

    st.title("¡Bienvenido a PA' NOSOTROS!")
    st.markdown(
        """
        ### 🍔 UNA HAMBURGUESERÍA DEDICADA SOLO PARA NOSOTROS
        *Los verdaderos amantes de las minihamburguesas.*

        ---
        **¿Qué querés hacer hoy?**
        * Usa el **Dashboard** para ver cómo vienen las ventas.
        * Entra a **Registrar Pedido** para anotar un nuevo pedido.
        * En **Productos** podés ver y editar las hamburguesas actuales y agregar nuevas.
        * En el **Historial** tenés un registro de todos los pedidos anteriores, con filtro por fecha incluido.
        """
    )
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()
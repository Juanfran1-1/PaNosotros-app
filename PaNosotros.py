import streamlit as st


st.set_page_config(
    page_title="PA' NOSOTROS",
    page_icon="logo.png",
    layout="wide"
)

# --- FUNCIÓN DE LOGIN ---
def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("logo.png", width=250)
            except:
                pass

            st.title("Iniciar Sesión")
            usuario_ingresado = st.text_input("Usuario")
            clave_ingresada = st.text_input("Contraseña", type="password")
            
            if st.button("Ingresar"):
                try:
                    
                    user_real = st.secrets["credentials"]["user"]
                    pass_real = st.secrets["credentials"]["password"]
                    
                    # 1. PASO: Validar Usuario 
                    if usuario_ingresado.strip() != user_real:
                        st.error("Usuario incorrecto")
                    
                    # 2. PASO: Si el usuario es correcto, validar contraseña
                    elif clave_ingresada.strip() != pass_real:
                        st.error("Contraseña incorrecta")
                    
                    # 3. PASO: Si ambos están bien
                    else:
                        st.session_state.authenticated = True
                        st.rerun()
                        
                except KeyError:
                    st.error("❌ Error: No se encontraron las credenciales en 'Secrets'.")
                except Exception as e:
                    st.error(f"❌ Error inesperado: {e}")
        return False
    return True

# --- EJECUCIÓN PRINCIPAL ---
if login():

    col1, col2, col3 = st.columns([2, 2, 1])

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
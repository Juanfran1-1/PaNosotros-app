import streamlit as st
from st_supabase_connection import SupabaseConnection

def get_connection():
    try:
        return st.connection(
            "supabase",
            type=SupabaseConnection,
            url=st.secrets["connections"]["supabase"]["url"],
            key=st.secrets["connections"]["supabase"]["key"]
        )
    except KeyError as e:
        st.error(f"Falta una clave de configuración en secrets: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error inesperado al conectar con la base de datos: {e}")
        st.stop()

import streamlit as st
from st_supabase_connection import SupabaseConnection
import toml

def get_connection():
    try:
        # Intentamos leer el archivo secrets.toml
        with open(".streamlit/secrets.toml", "r") as f:
            secrets = toml.load(f)
        
        return st.connection(
            "supabase",
            type=SupabaseConnection,
            url=secrets["connections"]["supabase"]["url"],
            key=secrets["connections"]["supabase"]["key"]
        )
    except FileNotFoundError:
        st.error("No se encontró el archivo de configuración (.streamlit/secrets.toml)")
        st.stop()
    except KeyError as e:
        st.error(f"Falta una clave de configuración en secrets: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error inesperado al conectar con la base de datos: {e}")
        st.stop()
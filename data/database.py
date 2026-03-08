import streamlit as st
from st_supabase_connection import SupabaseConnection
import toml

def get_connection():
    # Leemos el archivo secrets.toml a la fuerza
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = toml.load(f)
    
    # Le pasamos los datos directamente
    return st.connection(
        "supabase",
        type=SupabaseConnection,
        url=secrets["connections"]["supabase"]["url"],
        key=secrets["connections"]["supabase"]["key"]
    )

def inicializar_db():
    pass
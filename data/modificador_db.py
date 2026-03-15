import pandas as pd
import streamlit as st
from .database import get_connection

def cargar_hamburguesas():
    try:
        client = get_connection()
        res = client.table("hamburguesas").select("*").order("nombre").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar hamburguesas: {e}")
        return pd.DataFrame()

def cargar_datos():
    try:
        client = get_connection()
        res = client.table("pedidos").select("*").order("id", desc=True).execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar el historial: {e}")
        return pd.DataFrame()

def guardar_pedido(fecha, detalle, cliente, numero, monto, metodo_pago, entrega, direccion, estado):
    try:
        client = get_connection()
        data = {
            "fecha": str(fecha),
            "detalle": str(detalle),
            "cliente": str(cliente),
            "numero": str(numero), # <--- Agregamos la columna 'numero'
            "monto": int(monto), 
            "metodo_pago": str(metodo_pago),
            "entrega": str(entrega),      
            "direccion": str(direccion),
            "estado": str(estado), 
        }
        client.table("pedidos").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
        return False

def actualizar_disponibilidad(hamburguesa_id, estado):
    try:
        client = get_connection()
        client.table("hamburguesas").update({"disponible": bool(estado)}).eq("id", hamburguesa_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar disponibilidad: {e}")
        return False

def agregar_hamburguesa(nombre, precio, foto, desc, ingredientes):
    try:
        client = get_connection()
        data = {
            "nombre": str(nombre), 
            "precio": float(precio),
            "foto": str(foto),
            "desc": str(desc),
            "ingredientes": str(ingredientes),
            "disponible": True  # <--- Agregamos esto para que nazca con stock
        }
        client.table("hamburguesas").insert(data).execute()
    except Exception as e:
        st.error(f"❌ Error al agregar producto: {e}")
        
def actualizar_hamburguesa_completa(hamburguesa_id,precio, desc, ingredientes):
    try:
        client = get_connection()
        data = {
            "precio": float(precio),
            "desc": str(desc),
            "ingredientes": str(ingredientes)
        }
        # Actualizamos la fila que coincide con el ID
        client.table("hamburguesas").update(data).eq("id", hamburguesa_id).execute()
    except Exception as e:
        st.error(f"❌ Error al actualizar producto: {e}")
def eliminar_hamburguesa(hamburguesa_id):
    try:
        client = get_connection()
        client.table("hamburguesas").delete().eq("id", hamburguesa_id).execute()
    except Exception as e:
        st.error(f"❌ Error al eliminar producto: {e}")
        
def actualizar_disponibilidad(hamburguesa_id, estado):
    try:
        client = get_connection()
        client.table("hamburguesas").update({"disponible": bool(estado)}).eq("id", hamburguesa_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar disponibilidad: {e}")
        return False
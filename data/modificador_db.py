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

def cargar_promos():
    try:
        client = get_connection()
        res = client.table("promos").select("*").order("id", desc=True).execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar promos: {e}")
        return pd.DataFrame()

def cargar_promo_items():
    try:
        client = get_connection()
        res = client.table("promo_items").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar items de promo: {e}")
        return pd.DataFrame()

def cargar_promo_extras():
    try:
        client = get_connection()
        res = client.table("promo_extras").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar extras de promo: {e}")
        return pd.DataFrame()

def cargar_extras():
    try:
        client = get_connection()
        res = client.table("extras").select("*").order("nombre").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"⚠️ Error al cargar extras: {e}")
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

def actualizar_visibilidad_menu(hamburguesa_id, estado):
    try:
        client = get_connection()
        client.table("hamburguesas").update({"mostrar_en_menu": bool(estado)}).eq("id", hamburguesa_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar visibilidad en el menú: {e}")
        return False

def actualizar_disponibilidad_promo(promo_id, estado):
    try:
        client = get_connection()
        client.table("promos").update({"disponible": bool(estado)}).eq("id", promo_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar disponibilidad de promo: {e}")
        return False

def actualizar_disponibilidad_extra(extra_id, estado):
    try:
        client = get_connection()
        client.table("extras").update({"disponible": bool(estado)}).eq("id", extra_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar disponibilidad de extra: {e}")
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
            "disponible": True
        }
        client.table("hamburguesas").insert(data).execute()
    except Exception as e:
        st.error(f"❌ Error al agregar producto: {e}")

def agregar_promo(nombre, descripcion, precio, foto, permite_variedades=False, max_variedades=1):
    try:
        client = get_connection()
        data = {
            "nombre": str(nombre),
            "descripcion": str(descripcion),
            "precio": float(precio),
            "foto": str(foto),
            "permite_variedades": bool(permite_variedades),
            "max_variedades": int(max_variedades),
            "disponible": True
        }
        res = client.table("promos").insert(data).execute()
        if res.data:
            return res.data[0].get("id", True)
        return True
    except Exception as e:
        st.error(f"❌ Error al agregar promo: {e}")
        return False

def agregar_extra(nombre, precio, foto=""):
    try:
        client = get_connection()
        data = {
            "nombre": str(nombre),
            "precio": float(precio),
            "disponible": True
        }
        if foto:
            data["foto"] = str(foto)
        client.table("extras").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al agregar extra: {e}")
        return False
        
def actualizar_hamburguesa_completa(hamburguesa_id, precio, desc, ingredientes, foto=None):
    try:
        client = get_connection()
        data = {
            "precio": float(precio),
            "desc": str(desc),
            "ingredientes": str(ingredientes)
        }
        if foto is not None:
            data["foto"] = str(foto)
        # Actualizamos la fila que coincide con el ID
        client.table("hamburguesas").update(data).eq("id", hamburguesa_id).execute()
    except Exception as e:
        st.error(f"❌ Error al actualizar producto: {e}")

def actualizar_promo_completa(promo_id, nombre, descripcion, precio, foto, permite_variedades=False, max_variedades=1):
    try:
        client = get_connection()
        data = {
            "nombre": str(nombre),
            "descripcion": str(descripcion),
            "precio": float(precio),
            "foto": str(foto),
            "permite_variedades": bool(permite_variedades),
            "max_variedades": int(max_variedades)
        }
        client.table("promos").update(data).eq("id", promo_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al actualizar promo: {e}")
        return False

def actualizar_extra_completo(extra_id, nombre, precio, foto=None):
    try:
        client = get_connection()
        data = {
            "nombre": str(nombre),
            "precio": float(precio)
        }
        if foto is not None:
            data["foto"] = str(foto)
        client.table("extras").update(data).eq("id", extra_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al actualizar extra: {e}")
        return False

def eliminar_hamburguesa(hamburguesa_id):
    try:
        client = get_connection()
        client.table("hamburguesas").delete().eq("id", hamburguesa_id).execute()
    except Exception as e:
        st.error(f"❌ Error al eliminar producto: {e}")

def eliminar_promo(promo_id):
    try:
        client = get_connection()
        client.table("promos").delete().eq("id", promo_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al eliminar promo: {e}")
        return False

def eliminar_extra(extra_id):
    try:
        client = get_connection()
        client.table("extras").delete().eq("id", extra_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al eliminar extra: {e}")
        return False

def guardar_items_promo(promo_id, items):
    try:
        client = get_connection()
        client.table("promo_items").delete().eq("promo_id", promo_id).execute()
        if items:
            client.table("promo_items").insert(items).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar variedades de promo: {e}")
        return False

def guardar_extras_promo(promo_id, extras):
    try:
        client = get_connection()
        client.table("promo_extras").delete().eq("promo_id", promo_id).execute()
        if extras:
            client.table("promo_extras").insert(extras).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar extras de promo: {e}")
        return False
        
def actualizar_estado_pedido(pedido_id, estado):
    try:
        client = get_connection()
        client.table("pedidos").update({"estado": str(estado)}).eq("id", pedido_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar estado del pedido: {e}")
        return False
    
def cargar_configuracion():
    try:
        client = get_connection()
        res = client.table("configuracion").select("*").execute()
        if res.data:
            return res.data[0]  # Asumimos que solo hay una fila de configuración
        else:
            return {}  # Retornamos un diccionario vacío si no hay configuración
    except Exception as e:
        st.error(f"⚠️ Error al cargar configuración: {e}")
        return {}

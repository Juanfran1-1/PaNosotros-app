import pandas as pd
from data.database import get_connection

def cargar_hamburguesas():
    client = get_connection()
    # Traemos todas las burguers ordenadas por nombre
    res = client.table("hamburguesas").select("*").order("nombre").execute()
    return pd.DataFrame(res.data)

def cargar_datos():
    client = get_connection()
    # Traemos los pedidos, el más nuevo primero
    res = client.table("pedidos").select("*").order("id", desc=True).execute()
    return pd.DataFrame(res.data)

def guardar_pedido(fecha, detalle, cliente, monto, metodo_pago):
    client = get_connection()
    data = {
        "fecha": str(fecha),
        "detalle": detalle,
        "cliente": cliente,
        "monto": float(monto),
        "metodo_pago": metodo_pago
    }
    client.table("pedidos").insert(data).execute()

# ---------------------------
# FUNCIONES DE PRODUCTOS
# ---------------------------

def agregar_hamburguesa(nombre, precio):
    client = get_connection()
    data = {"nombre": nombre, "precio": float(precio)}
    client.table("hamburguesas").insert(data).execute()

def actualizar_precio_hamburguesa(hamburguesa_id, nuevo_precio):
    client = get_connection()
    client.table("hamburguesas").update({"precio": float(nuevo_precio)}).eq("id", hamburguesa_id).execute()

def eliminar_hamburguesa(hamburguesa_id):
    client = get_connection()
    client.table("hamburguesas").delete().eq("id", hamburguesa_id).execute()
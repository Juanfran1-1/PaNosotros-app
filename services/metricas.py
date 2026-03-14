import pandas as pd
from datetime import datetime

def calcular_metricas(df):
    try:
        if df.empty:
            return 0, 0, 0, 0, 0, 0

        # 1. Aseguramos que el monto sea numérico
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)

        # 2. Manejo de Fechas
        df["fecha_dt"] = pd.to_datetime(df["fecha"], errors='coerce')
        
        # Obtenemos la fecha de hoy
        hoy_texto = datetime.now().strftime('%Y-%m-%d')
        df["solo_fecha"] = df["fecha_dt"].dt.strftime('%Y-%m-%d')

        # --- VENTAS HOY ---
        df_hoy = df[df["solo_fecha"] == hoy_texto]
        ventas_hoy = df_hoy["monto"].sum()
        pedidos_hoy = len(df_hoy)

        # --- VENTAS MES ---
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        
        df_mes = df[(df["fecha_dt"].dt.month == mes_actual) & (df["fecha_dt"].dt.year == anio_actual)]
        
        ventas_mes = df_mes["monto"].sum()
        pedidos_mes = len(df_mes)

        # --- MÉTODOS DE PAGO ---
        # Efectivo es solo Efectivo
        efectivo = df_mes[df_mes["metodo_pago"] == "Efectivo"]["monto"].sum()
        
        # 🟢 UNIFICACIÓN: Todo lo que no es Efectivo va a la bolsa de 'digital'
        # Esto incluye 'Transferencia', 'Mercado Pago', 'Digital', etc.
        metodos_digitales = ["Transferencia", "Mercado Pago", "Digital", "Virtual"]
        digital = df_mes[df_mes["metodo_pago"].isin(metodos_digitales)]["monto"].sum()

        return ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital
    except Exception as e:
        print(f"Error en métricas: {e}")
        return 0, 0, 0, 0, 0, 0

def calcular_hamburguesas_mes(df, tipos_hamburguesa):
    conteo = {tipo: 0 for tipo in tipos_hamburguesa}
    try:
        if df.empty: return conteo
        
        df["fecha_dt"] = pd.to_datetime(df["fecha"], errors='coerce')
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        
        df_mes = df[(df["fecha_dt"].dt.month == mes_actual) & (df["fecha_dt"].dt.year == anio_actual)]

        for detalle in df_mes["detalle"].fillna(""):
            for parte in str(detalle).split("|"):
                texto = parte.strip()
                for tipo in tipos_hamburguesa:
                    if tipo in texto:
                        try:
                            if "x" in texto:
                                # Manejamos el formato "2x Americana"
                                cantidad = int(texto.split("x")[0].strip())
                                conteo[tipo] += cantidad
                            else:
                                conteo[tipo] += 1
                        except:
                            continue
        return conteo
    except:
        return conteo
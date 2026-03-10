import pandas as pd
from datetime import date, datetime

import pandas as pd
from datetime import datetime

def calcular_metricas(df):
    try:
        if df.empty:
            return 0, 0, 0, 0, 0, 0

        # 1. Convertimos la columna a datetime 
        df["fecha_dt"] = pd.to_datetime(df["fecha"], utc=True).dt.tz_convert('America/Argentina/Buenos_Aires')
        
        # 2. CREAMOS UNA COLUMNA DE TEXTO YYYY-MM-DD
        df["fecha_texto"] = df["fecha_dt"].dt.strftime('%Y-%m-%d')
        
        # 3. Obtenemos el texto de HOY
        hoy_texto = datetime.now().strftime('%Y-%m-%d')
        
        # 4. Aseguramos que el monto sea número
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)

        # --- FILTRAR HOY ---
        df_hoy = df[df["fecha_texto"] == hoy_texto]
        ventas_hoy = df_hoy["monto"].sum()
        pedidos_hoy = len(df_hoy)

        # --- FILTRAR MES ---
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        df_mes = df[(df["fecha_dt"].dt.month == mes_actual) & (df["fecha_dt"].dt.year == anio_actual)]

        ventas_mes = df_mes["monto"].sum()
        pedidos_mes = len(df_mes)

        # 5. Métodos de pago (Suma todo el mes)
        efectivo = df_mes[df_mes["metodo_pago"] == "Efectivo"]["monto"].sum()
        # Usamos .isin para que agarre tanto "Digital" como "Virtual" según uses
        digital = df_mes[df_mes["metodo_pago"].isin(["Digital", "Virtual"])]["monto"].sum()

        return ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital
    except Exception as e:
        print(f"Error en métricas: {e}")
        return 0, 0, 0, 0, 0, 0
    

def calcular_hamburguesas_mes(df, tipos_hamburguesa):
    conteo = {tipo: 0 for tipo in tipos_hamburguesa}
    try:
        if df.empty: return conteo
        
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        hoy = pd.to_datetime(date.today())
        df_mes = df[(df["fecha"].dt.month == hoy.month) & (df["fecha"].dt.year == hoy.year)]

        for detalle in df_mes["detalle"].fillna(""):
            for parte in str(detalle).split("|"):
                texto = parte.strip()
                for tipo in tipos_hamburguesa:
                    if tipo in texto:
                        try:
                            # Extraemos cantidad de formatos como "2x Clásica"
                            cantidad = int(texto.split("x")[0].strip())
                            conteo[tipo] += cantidad
                        except:
                            continue
        return conteo
    except:
        return conteo
import pandas as pd
from datetime import date

def calcular_metricas(df):
    try:
        if df.empty:
            return 0, 0, 0, 0, 0, 0

        # Forzamos conversión segura
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)

        hoy = pd.to_datetime(date.today())
        ventas_hoy = df[df["fecha"] == hoy]["monto"].sum()
        pedidos_hoy = len(df[df["fecha"] == hoy])

        mes_actual, anio_actual = hoy.month, hoy.year
        df_mes = df[(df["fecha"].dt.month == mes_actual) & (df["fecha"].dt.year == anio_actual)]

        ventas_mes = df_mes["monto"].sum()
        pedidos_mes = len(df_mes)

        # Filtro seguro por método de pago
        efectivo = df_mes[df_mes["metodo_pago"] == "Efectivo"]["monto"].sum()
        digital = df_mes[df_mes["metodo_pago"] == "Digital"]["monto"].sum()

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
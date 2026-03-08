import pandas as pd
from datetime import date


def calcular_metricas(df):
    if df.empty:
        return 0, 0, 0, 0, 0, 0

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["monto"] = pd.to_numeric(df["monto"], errors="coerce").fillna(0)

    hoy = pd.to_datetime(date.today())

    ventas_hoy = df[df["fecha"] == hoy]["monto"].sum()
    pedidos_hoy = len(df[df["fecha"] == hoy])

    mes_actual = hoy.month
    anio_actual = hoy.year

    df_mes = df[
        (df["fecha"].dt.month == mes_actual) &
        (df["fecha"].dt.year == anio_actual)
    ]

    ventas_mes = df_mes["monto"].sum()
    pedidos_mes = len(df_mes)

    efectivo = df_mes[df_mes["metodo_pago"] == "Efectivo"]["monto"].sum()
    digital = df_mes[df_mes["metodo_pago"] == "Virtual"]["monto"].sum()

    return ventas_hoy, pedidos_hoy, ventas_mes, pedidos_mes, efectivo, digital


def calcular_hamburguesas_mes(df, tipos_hamburguesa):
    conteo = {tipo: 0 for tipo in tipos_hamburguesa}

    if df.empty:
        return conteo

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    hoy = pd.to_datetime(date.today())
    mes_actual = hoy.month
    anio_actual = hoy.year

    df_mes = df[
        (df["fecha"].dt.month == mes_actual) &
        (df["fecha"].dt.year == anio_actual)
    ]

    for detalle in df_mes["detalle"].fillna(""):
        partes = str(detalle).split("|")

        for parte in partes:
            texto = parte.strip()

            for tipo in tipos_hamburguesa:
                if tipo in texto:
                    try:
                        cantidad = int(texto.split("x")[0].strip())
                        conteo[tipo] += cantidad
                    except:
                        pass

    return conteo
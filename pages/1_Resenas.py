import pandas as pd
import streamlit as st

from data.modificador_db import cargar_resenas
from utils.diseno import aplicar_estilos, page_header


st.set_page_config(page_title="PA' NOSOTROS - RESEÑAS", page_icon="logo.png", layout="wide")
aplicar_estilos()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("⚠️ Por favor, inicia sesión para continuar.")
    if st.button("Ir al Inicio", type="secondary"):
        st.switch_page("PaNosotros.py")
    st.stop()

page_header(
    "Reseñas",
    "Opiniones que dejan los clientes desde el menú."
)

df = cargar_resenas()

if df.empty:
    st.info("Todavía no hay reseñas cargadas.")
else:
    df = df.copy()
    df["puntaje"] = pd.to_numeric(df.get("puntaje"), errors="coerce")

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        df = df.sort_values("created_at", ascending=False)

    filtro = st.radio(
        "Filtrar por mini burgers",
        ["Todas", "5", "4", "3", "2", "1"],
        horizontal=True,
    )

    df_filtrado = df
    if filtro != "Todas":
        puntaje = int(filtro)
        if puntaje == 5:
            df_filtrado = df[df["puntaje"] == 5]
        else:
            df_filtrado = df[(df["puntaje"] >= puntaje) & (df["puntaje"] < puntaje + 1)]

    promedio = df_filtrado["puntaje"].mean() if not df_filtrado.empty else 0
    visibles = int(df_filtrado.get("visible", pd.Series(dtype=bool)).fillna(True).sum()) if "visible" in df_filtrado.columns else len(df_filtrado)

    c1, c2, c3 = st.columns(3)
    c1.metric("Reseñas", len(df_filtrado))
    c2.metric("Promedio", f"{promedio:.1f}" if len(df_filtrado) else "-")
    c3.metric("Visibles", visibles)

    st.divider()

    if df_filtrado.empty:
        st.info("No hay reseñas con ese filtro.")
    else:
        for _, resena in df_filtrado.iterrows():
            nombre = str(resena.get("nombre", "Sin nombre")).strip() or "Sin nombre"
            puntaje = resena.get("puntaje", 0)
            texto = str(resena.get("texto", "")).strip()
            tags = str(resena.get("tags", "") or "").strip()
            visible = bool(resena.get("visible", True))
            fecha = resena.get("created_at")

            estrellas = "🍔" * int(puntaje) if pd.notna(puntaje) else ""
            puntaje_texto = f"{puntaje:.1f}" if pd.notna(puntaje) else "-"

            with st.container():
                col_info, col_meta = st.columns([4, 1])

                with col_info:
                    st.subheader(f"{nombre}")
                    st.write(texto if texto else "Sin comentario.")
                    if tags:
                        st.caption(f"Destacó: {tags.replace(',', ' · ')}")

                with col_meta:
                    st.metric("Puntaje", puntaje_texto)
                    st.write(estrellas)
                    st.caption("Visible" if visible else "Oculta")
                    if pd.notna(fecha):
                        st.caption(fecha.strftime("%d/%m/%Y %H:%M"))

            st.divider()

        columnas_tabla = [col for col in ["created_at", "nombre", "puntaje", "texto", "tags", "visible"] if col in df_filtrado.columns]
        if columnas_tabla:
            st.subheader("Vista rápida")
            st.dataframe(
                df_filtrado[columnas_tabla].rename(columns={
                    "created_at": "fecha",
                    "nombre": "nombre",
                    "puntaje": "puntaje",
                    "texto": "reseña",
                    "tags": "destacó",
                    "visible": "visible",
                }),
                use_container_width=True,
                hide_index=True,
            )

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()

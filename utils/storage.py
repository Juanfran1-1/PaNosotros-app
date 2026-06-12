from io import BytesIO
import re
import unicodedata

import streamlit as st
from PIL import Image, ImageOps
from supabase import create_client

FOTO_DEFAULT = "Logo.jpg"
CALIDAD_WEBP_MENU = 92
TAMANO_PRODUCTO_MENU = (1080, 1620)
TAMANO_EXTRA_MENU = (900, 900)


def obtener_bucket_imagenes():
    try:
        return st.secrets["storage"]["bucket"]
    except Exception:
        return "menu-imagenes"


def get_storage_client():
    return create_client(
        st.secrets["connections"]["supabase"]["url"],
        st.secrets["connections"]["supabase"]["key"],
    )


def normalizar_nombre_archivo(nombre):
    texto = unicodedata.normalize("NFKD", nombre or "imagen")
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto).strip("-").lower()
    return texto or "imagen"


def obtener_resampling_lanczos():
    try:
        return Image.Resampling.LANCZOS
    except AttributeError:
        return Image.LANCZOS


def obtener_tamano_final(carpeta):
    return TAMANO_EXTRA_MENU if carpeta == "extras" else TAMANO_PRODUCTO_MENU


def normalizar_posicion_recorte(posicion_recorte=None):
    if not posicion_recorte:
        return (0.5, 0.5)

    posicion_x, posicion_y = posicion_recorte
    posicion_x = min(max(float(posicion_x), 0.0), 1.0)
    posicion_y = min(max(float(posicion_y), 0.0), 1.0)
    return (posicion_x, posicion_y)


def preparar_imagen_menu(archivo, carpeta, posicion_recorte=None):
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)

    if imagen.mode not in ("RGB", "RGBA"):
        imagen = imagen.convert("RGBA")

    return ImageOps.fit(
        imagen,
        obtener_tamano_final(carpeta),
        method=obtener_resampling_lanczos(),
        centering=normalizar_posicion_recorte(posicion_recorte),
    )


def convertir_a_webp(archivo, carpeta, posicion_recorte=None):
    imagen = preparar_imagen_menu(archivo, carpeta, posicion_recorte)

    salida = BytesIO()
    imagen.save(salida, format="WEBP", quality=CALIDAD_WEBP_MENU, method=6)
    salida.seek(0)
    return salida.getvalue()


def mostrar_control_encuadre(archivo, carpeta, key):
    if archivo is None:
        return (0.5, 0.5)

    col_x, col_y = st.columns(2)
    with col_x:
        posicion_x = st.slider(
            "Mover izquierda / derecha",
            min_value=0,
            max_value=100,
            value=50,
            key=f"{key}_pos_x",
        )
    with col_y:
        posicion_y = st.slider(
            "Mover arriba / abajo",
            min_value=0,
            max_value=100,
            value=50,
            key=f"{key}_pos_y",
        )

    posicion_recorte = (posicion_x / 100, posicion_y / 100)
    archivo.seek(0)
    vista_previa = preparar_imagen_menu(archivo, carpeta, posicion_recorte)
    archivo.seek(0)
    st.image(vista_previa, caption="Vista previa final del menú", width=260)
    return posicion_recorte


def subir_imagen_menu(archivo, nombre_base, carpeta, posicion_recorte=None):
    if archivo is None:
        return None

    try:
        bucket = obtener_bucket_imagenes()
        nombre_limpio = normalizar_nombre_archivo(nombre_base)
        ruta = f"{carpeta}/{nombre_limpio}.webp"
        contenido = convertir_a_webp(archivo, carpeta, posicion_recorte)
        if contenido is None:
            return None

        client = get_storage_client()
        client.storage.from_(bucket).upload(
            ruta,
            contenido,
            file_options={
                "content-type": "image/webp",
                "upsert": "true",
            },
        )

        return client.storage.from_(bucket).get_public_url(ruta)
    except Exception as e:
        st.error(f"No se pudo subir la imagen: {e}")
        return None


def resolver_foto_menu(archivo, nombre_base, carpeta, foto_manual="", posicion_recorte=None):
    if archivo is not None:
        return subir_imagen_menu(archivo, nombre_base, carpeta, posicion_recorte)

    foto = str(foto_manual or "").strip()
    return foto if foto else FOTO_DEFAULT

from io import BytesIO
import re
import unicodedata

import streamlit as st
from PIL import Image, ImageOps
from supabase import create_client

FOTO_DEFAULT = "Logo.jpg"


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


def convertir_a_webp(archivo):
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)

    if imagen.mode not in ("RGB", "RGBA"):
        imagen = imagen.convert("RGBA")

    salida = BytesIO()
    imagen.save(salida, format="WEBP", quality=82, method=6)
    salida.seek(0)
    return salida.getvalue()


def subir_imagen_menu(archivo, nombre_base, carpeta):
    if archivo is None:
        return None

    try:
        bucket = obtener_bucket_imagenes()
        nombre_limpio = normalizar_nombre_archivo(nombre_base)
        ruta = f"{carpeta}/{nombre_limpio}.webp"
        contenido = convertir_a_webp(archivo)

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


def resolver_foto_menu(archivo, nombre_base, carpeta, foto_manual=""):
    if archivo is not None:
        return subir_imagen_menu(archivo, nombre_base, carpeta)

    foto = str(foto_manual or "").strip()
    return foto if foto else FOTO_DEFAULT

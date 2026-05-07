"""
config.py — Constantes globales y configuración de la aplicación.

Este módulo centraliza todo lo que puede necesitar cambiarse sin tocar
la lógica del programa: sitios destino, rutas de archivos y funciones
para leer/guardar el archivo config.json.
Separarlo evita que los demás módulos dependan unos de otros solo para
leer un valor de configuración.
"""

import json

# ── Apariencia de la interfaz ─────────────────────────────────────────
# Se definen aquí para aplicarlos antes de importar CustomTkinter en main.
TEMA_APARIENCIA = "dark"
TEMA_COLOR = "blue"

# ── Archivos del proyecto ─────────────────────────────────────────────
# Ruta del archivo donde se persiste el estado entre ejecuciones
# (región de captura, atajo de teclado, etc.).
ARCHIVO_CONFIG = "config.json"

# Nombre clave usado en el llavero del sistema operativo para guardar
# credenciales de forma segura (no en texto plano).
KEYRING_APP = "AutoCapturaApp"

# ── Sitios destino ────────────────────────────────────────────────────
# Lista de sitios a los que se sube la captura.
# Cada dict describe un sitio: si requiere login, sus URLs y los
# selectores CSS de los elementos con los que interactúa Selenium.
#
# Para agregar un sitio nuevo, copia uno de estos bloques y ajusta
# los valores sin modificar el resto del código.
SITIOS = [
    {
        # Sitio público: no necesita iniciar sesión.
        "nombre": "Sitio 1 (sin login)",
        "necesita_login": False,
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",  # campo <input type="file">
        "selector_submit": "#file-submit",  # botón de envío
    },
    {
        # Sitio privado: requiere usuario y contraseña antes de subir.
        "nombre": "Sitio 2 (con login)",
        "necesita_login": True,
        "url_login": "https://the-internet.herokuapp.com/login",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "button[type='submit']",
        # url_base_upload se usa cuando la URL de subida varía por número
        # (p. ej. /upload/1, /upload/2…). Si es fija, usa url_upload.
        "url_base_upload": "https://miejemplo.com/upload",
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
    },
]


# ── Funciones de configuración ────────────────────────────────────────


def cargar_config() -> dict:
    """
    Lee config.json y devuelve su contenido como diccionario.

    Si el archivo no existe o está corrupto, devuelve un dict vacío
    para que la app arranque con valores por defecto sin fallar.
    """
    try:
        with open(ARCHIVO_CONFIG, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def guardar_config(datos: dict) -> None:
    """
    Escribe el diccionario 'datos' en config.json con indentación legible.

    Se llama cada vez que el usuario cambia el atajo de teclado o la
    región, para que esos valores persistan en la próxima ejecución.
    """
    try:
        with open(ARCHIVO_CONFIG, "w") as f:
            json.dump(datos, f, indent=2)
    except Exception as e:
        print(f"[✗] Error guardando config: {e}")


# # Coordenadas de la región a capturar (x, y, ancho, alto)
# REGION = {"top": 100, "left": 200, "width": 800, "height": 600}

# URL = [
#     {
#         "url": "HUBSPOT",
#         "usuario": "tu_usuario",
#         "clave": "tu_clave",
#         "url_upload": "HUBSPOT-SUBIR",
#         "selector_user": "#username",
#         "selector_pass": "#password",
#         "selector_submit": "#btn-login",
#         "selector_input_file": "input[type='file']",
#     },
#     {
#         "url": "SUNRUN",
#         "usuario": "tu_usuario2",
#         "clave": "tu_clave2",
#         "url_upload": "SUNRUN-SUBIR",
#         "selector_user": "#email",
#         "selector_pass": "#pwd",
#         "selector_submit": ".login-btn",
#         "selector_input_file": "#file-upload",
#     },
# ]

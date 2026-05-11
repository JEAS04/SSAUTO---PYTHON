"""
configuracion.py — Constantes globales y configuración de la aplicación.

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
        "nombre": "HUBSPOT",
        "necesita_login": True,
        "url_login": "https://app.hubspot.com/login/",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "#loginBtn",
        # URL base del ticket: se reemplazará dinámicamente con el número
        # del ticket actual cuando se integre con la API de HubSpot.
        # Por ahora apunta a una URL de prueba.
        "url_upload": "https://app.hubspot.com/contacts/TICKET_ID",
        # ── Selectores específicos para subir captura a nota ──────────
        # Flujo: Notas → Crear nota → botón imagen → input file → Guardar
        "selector_tab_notas": '[data-test-id="timeline-tab-filter-notes"]',
        "selector_btn_crear_nota": 'button[data-selenium-test="create-engagement-note-button"]',
        "selector_btn_imagen": '[data-test-id="image-upload-toggle"]',
        "selector_input_file": 'input[type="file"]',
        "selector_btn_guardar": '[data-test-id="activity-creator-window-footer-save-button"]',
        "selector_confirmacion": "h3, h1",
        "palabras_confirmacion": [
            "uploaded",
            "success",
            "exitoso",
            "subido",
            "note",
            "nota",
            "guardado",
        ],
    },
    {
        "nombre": "SUNRUN",
        "necesita_login": True,
        "url_login": "https://sunrun.my.site.com/partner/login?locale=us",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "#Login",
        # url_base_upload se usa cuando la URL de subida varía por número
        # (p. ej. /upload/1, /upload/2…). Si es fija, usa url_upload.
        "url_base_upload": "https://miejemplo.com/upload",
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
        "selector_confirmacion": "h3, h1",
        "palabras_confirmacion": ["uploaded", "success", "exitoso", "subido"],
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


# ── Perfiles de región ────────────────────────────────────────────────
# Los perfiles se guardan dentro de config.json bajo la clave "perfiles_region".
# Estructura: {"Monitor principal": {"top": 0, "left": 0, "width": 1920, "height": 1080}, ...}
# Se usan funciones independientes para dejar clara la separación de datos.

CLAVE_PERFILES = "perfiles_region"

# Perfil por defecto que se carga la primera vez que se abre la app,
# antes de que el usuario haya creado ninguno propio.
PERFIL_POR_DEFECTO = {"top": 392, "left": 524, "width": 934, "height": 404}


def cargar_perfiles() -> dict:
    """
    Devuelve todos los perfiles de región guardados en config.json.

    Si no existe ninguno todavía, devuelve un dict vacío para que la app
    arranque sin perfiles predefinidos y el usuario cree los suyos.
    """
    config = cargar_config()
    return config.get(CLAVE_PERFILES, {})


def guardar_perfiles(perfiles: dict) -> None:
    """
    Persiste el dict completo de perfiles en config.json.

    Lee la config actual para no sobreescribir otros valores (keybind,
    etc.) y solo actualiza la clave de perfiles.

    Parámetros
    ----------
    perfiles : dict con el formato {nombre_perfil: {top, left, width, height}}
    """
    config = cargar_config()
    config[CLAVE_PERFILES] = perfiles
    guardar_config(config)

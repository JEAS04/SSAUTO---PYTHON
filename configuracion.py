"""
configuracion.py — Constantes globales y configuración de la aplicación.

Este módulo centraliza todo lo que puede necesitar cambiarse sin tocar
la lógica del programa: sitios destino, rutas de archivos y funciones
para leer/guardar el archivo config.json.
Separarlo evita que los demás módulos dependan unos de otros solo para
leer un valor de configuración.
"""

import os
import json

# ── Apariencia de la interfaz ─────────────────────────────────────────
# Se definen aquí para aplicarlos antes de importar CustomTkinter en main.
TEMA_APARIENCIA = "dark"
TEMA_COLOR = "blue"

# ── Archivos del proyecto ─────────────────────────────────────────────
# Ruta del archivo donde se persiste el estado entre ejecuciones
# (región de captura, atajo de teclado, etc.).
ARCHIVO_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Nombre clave usado en el llavero del sistema operativo para guardar
# credenciales de forma segura (no en texto plano).
KEYRING_APP = "AutoCapturaApp"

# ── Control de subida de nota ─────────────────────────────────────────
# Clave en config.json para el toggle de auto-submit de nota en HubSpot.
CLAVE_AUTO_SUBMIT = "auto_submit_nota"
AUTO_SUBMIT_DEFAULT = True


def cargar_auto_submit() -> bool:
    """Lee de config.json si el auto-submit de nota está activado.

    Returns
    -------
    bool : True si la nota debe enviarse automáticamente, False en caso contrario.
           Por defecto devuelve True.
    """
    config = cargar_config()
    return config.get(CLAVE_AUTO_SUBMIT, AUTO_SUBMIT_DEFAULT)


def guardar_auto_submit(valor: bool) -> None:
    """Persiste el valor del toggle auto-submit en config.json.

    Parámetros
    ----------
    valor : bool - nuevo estado del toggle.
    """
    config = cargar_config()
    config[CLAVE_AUTO_SUBMIT] = valor
    guardar_config(config)


# ── Constantes de temporización y reintentos ──────────────────────────
#
# Valores globales que usan los módulos de automatización y scraping.
# Ajusta estos valores si los sitios destino son particularmente lentos
# o si experimentas timeouts frecuentes.

# Timeout general para esperar elementos individuales (segundos).
TIMEOUT_ELEMENTO = 15
# Timeout para páginas completas o listas que tardan en cargar.
TIMEOUT_PAGINA = 30
# Timeout máximo para confirmación de subida.
TIMEOUT_CONFIRMACION = 30
# Número de reintentos para elementos obsoletos (stale elements).
REINTENTOS_STALE = 3
# Pausa entre reintentos de stale elements (segundos).
PAUSA_REINTENTO_STALE = 0.3
# Pausa breve estándar para animaciones SPA/React/Vue (segundos).
PAUSA_ANIMACION_SPA = 0.5


# ── Sitios destino ────────────────────────────────────────────────────
#
# Cada dict describe un sitio: si requiere login, sus URLs y los
# selectores CSS/XPath de los elementos con los que interactúa Selenium.
#
# Validación de selectores:
#   ✓ #username / #password → selectores por ID estándar.
#   ✓ #loginBtn             → ID de botón en HubSpot.
#   ✓ [data-test-id="..."]  → selectores data-test-id (estables frente a
#                              cambios de clase, típicos en React).
#   ✓ input[type="file"]    → selector genérico para input file.
#   ✓ #file-upload / #file-submit → selectores de the-internet.herokuapp.com.
#   ✓ h3, h1                → selectores de confirmación de subida.
#
# Para agregar un sitio nuevo, copia uno de estos bloques y ajusta
# los valores sin modificar el resto del código.
SITIOS = [
    {
        "nombre": "HUBSPOT",
        "necesita_login": True,
        "usar_pagina_actual": True,
        "url_login": "https://app.hubspot.com/login/",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "#loginBtn",
        # URL base del ticket: se usaba anteriormente para navegar a una URL
        # fija. Ahora con 'usar_pagina_actual: True' se omite la navegación
        # y se trabaja directamente con la página de HubSpot que el usuario
        # tenga abierta en su Chrome de depuración.
        "url_upload": "https://app.hubspot.com/contacts/TICKET_ID",
        # ── Selectores específicos para subir captura a nota ──────────
        # Flujo: Notas → Crear nota → botón adjuntar → Subir → input file → Guardar
        # Selector para la pestaña "Actividades" (se hace clic primero)
        "selector_tab_actividades": 'a[data-tab-id="1"]',
        "selector_tab_actividades_fallback": 'a[data-tab-link="true"]',
        "selector_tab_notas": '[data-test-id="timeline-tab-filter-notes"]',
        "selector_btn_crear_nota": 'button[data-selenium-test="create-engagement-note-button"]',
        "selector_btn_adjuntar": '[data-test-id="select-file-dropdown"]',
        "selector_btn_subir": '[data-test-id="select-file-dropdown"]',
        "selector_btn_subir_opcion": 'i18n-string[data-key="customerDataRte.attachmentOptions.upload"]',
        "selector_input_file": 'input[type="file"]',
        "selector_nota_editor": '[data-test-id="rte-content"]',
        "selector_nota_editor_alt": 'div.ProseMirror[contenteditable="true"]',
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
    except Exception as e:
        print(f"[✗] Error cargando config: {e}")
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
        print(f"[✗] Error cargando config: {e}")
    return {}


# ── Perfiles de región ────────────────────────────────────────────────
# Los perfiles se guardan dentro de config.json bajo la clave "perfiles_region".
# Estructura: {"Nombre perfil": {"top": 0, "left": 0, "width": 1920, "height": 1080, "monitor_index": 1}, ...}
# El campo "monitor_index" es opcional (compatibilidad hacia atrás).
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
    perfiles : dict con el formato {nombre_perfil: {top, left, width, height, ...}}
    """
    config = cargar_config()
    config[CLAVE_PERFILES] = perfiles
    guardar_config(config)


# ── Funciones de detección de monitores ───────────────────────────────


def obtener_monitores() -> list:
    """
    Devuelve la lista de monitores detectados por mss.

    El índice 0 es el monitor virtual (todos los monitores combinados).
    Los índices 1, 2, ... son monitores físicos individuales.
    Cada monitor es un dict con: left, top, width, height, (is_primary, name, unique_id).

    Returns
    -------
    list : lista de dicts de monitores, o lista vacía si no se pudo detectar.
    """
    try:
        import mss

        with mss.MSS() as sct:
            return sct.monitors
    except Exception as e:
        print(f"[✗] Error detectando monitores: {e}")
        return []


def obtener_nombres_monitores() -> list[str]:
    """
    Devuelve una lista de nombres legibles para mostrar en la UI.

    Formato: "Monitor 1 (principal)", "Monitor 2", "Todos los monitores".

    Returns
    -------
    list[str] : nombres legibles para cada monitor detectado.
    """
    monitores = obtener_monitores()
    nombres = []
    for i, mon in enumerate(monitores):
        if i == 0:
            nombres.append("Todos los monitores")
        elif mon.get("is_primary"):
            nombre_extra = mon.get("name", "").strip()
            if nombre_extra:
                nombres.append(f"Monitor {i} — {nombre_extra} (principal)")
            else:
                nombres.append(f"Monitor {i} (principal)")
        else:
            nombre_extra = mon.get("name", "").strip()
            if nombre_extra:
                nombres.append(f"Monitor {i} — {nombre_extra}")
            else:
                nombres.append(f"Monitor {i}")
    return nombres


def obtener_monitor_por_indice(indice: int) -> dict:
    """
    Devuelve el dict del monitor en la posición 'indice' de la lista.

    Parámetros
    ----------
    indice : int - índice del monitor (0 = virtual, 1 = primer físico, ...)

    Returns
    -------
    dict | None : el monitor o None si no existe.
    """
    monitores = obtener_monitores()
    indice = int(indice)
    if 0 <= indice < len(monitores):
        return monitores[indice]
    return None

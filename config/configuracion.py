"""
configuracion.py — Constantes globales y configuracion de la aplicacion.

Centraliza config.json I/O, perfiles, toggles, y re-exporta utilidades
de sistema para mantener compatibilidad con codigo existente.
"""

import json
import os
import threading
from dataclasses import dataclass
from typing import Any

from utils.paths import resource_path, get_writable_path
from core.monitors import (            # re-exportado para compatibilidad
    obtener_monitores,
    obtener_nombres_monitores,
    obtener_monitor_por_indice,
)
from core.browser import (             # re-exportado para compatibilidad
    PUERTO_DEBUG,
    CHROME_USER_DATA,
    CHROME_PATHS,
    obtener_chrome_exe,
)

# ── Apariencia de la interfaz ─────────────────────────────────────────
TEMA_APARIENCIA = "dark"
TEMA_COLOR = "blue"

# ── Archivos del proyecto ─────────────────────────────────────────────
ARCHIVO_CONFIG = get_writable_path(os.path.join("config", "config.json"))
KEYRING_APP = "AutoCapturaApp"


# ── ToggleConfig: reemplaza las 8 funciones cargar_X/guardar_X ────────

@dataclass
class ToggleConfig:
    """Toggle de configuracion persistente con clave, default, cargar y guardar."""
    clave: str
    default: Any

    def cargar(self):
        config = cargar_config()
        return config.get(self.clave, self.default)

    def guardar(self, valor) -> None:
        config = cargar_config()
        config[self.clave] = valor
        guardar_config(config)

    def __call__(self):
        """Permite usar toggle() como shortcut para toggle.cargar()."""
        return self.cargar()


# ── Instancias de toggles (reemplazan las 8 funciones repetitivas) ────

toggle_auto_submit = ToggleConfig("auto_submit_nota", True)
toggle_headless = ToggleConfig("headless", False)
toggle_chrome_existente = ToggleConfig("chrome_existente", True)
toggle_destino_subida = ToggleConfig("destino_subida", "AMBOS")
toggle_capture_delay = ToggleConfig("capture_delay", 0.5)


# ── Backward-compatible wrappers (las funciones antiguas siguen funcionando) ──

def cargar_auto_submit() -> bool:
    return toggle_auto_submit.cargar()

def guardar_auto_submit(valor: bool) -> None:
    toggle_auto_submit.guardar(valor)

def cargar_headless() -> bool:
    return toggle_headless.cargar()

def guardar_headless(valor: bool) -> None:
    toggle_headless.guardar(valor)

def cargar_chrome_existente() -> bool:
    return toggle_chrome_existente.cargar()

def guardar_chrome_existente(valor: bool) -> None:
    toggle_chrome_existente.guardar(valor)

def cargar_destino_subida() -> str:
    return toggle_destino_subida.cargar()

def guardar_destino_subida(valor: str) -> None:
    toggle_destino_subida.guardar(valor)

def cargar_capture_delay() -> float:
    return toggle_capture_delay.cargar()

def guardar_capture_delay(valor: float) -> None:
    toggle_capture_delay.guardar(valor)


# ── Backward-compat constants (replaced by ToggleConfig instances) ────
CLAVE_AUTO_SUBMIT = toggle_auto_submit.clave
AUTO_SUBMIT_DEFAULT = toggle_auto_submit.default
CLAVE_HEADLESS = toggle_headless.clave
HEADLESS_DEFAULT = toggle_headless.default
CLAVE_CHROME_EXISTENTE = toggle_chrome_existente.clave
CHROME_EXISTENTE_DEFAULT = toggle_chrome_existente.default
CLAVE_DESTINO_SUBIDA = toggle_destino_subida.clave
DESTINO_SUBIDA_DEFAULT = toggle_destino_subida.default


# ── Cache de configuracion (evita lecturas repetitivas de disco) ──────
_config_cache: dict | None = None
_config_lock = threading.Lock()
_ultimo_error_config: str | None = None


# ── Funciones de configuracion ────────────────────────────────────────


def cargar_config() -> dict:
    """
    Lee config.json y devuelve su contenido como diccionario.

    Si el archivo no existe, devuelve un dict vacío para que la app
    arranque con valores por defecto sin fallar.

    Si el JSON está corrupto, intenta restaurar desde una copia de
    respaldo (.bak) antes de devolver un dict vacío, para no perder
    todos los ajustes del usuario.

    Usa un caché en memoria con thread-lock para evitar lecturas
    repetitivas de disco.
    """
    global _config_cache
    with _config_lock:
        if _config_cache is not None:
            return dict(_config_cache)
    resultado: dict = {}
    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            resultado = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        ruta_backup = ARCHIVO_CONFIG + ".bak"
        try:
            with open(ruta_backup, "r", encoding="utf-8") as fb:
                resultado = json.load(fb)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    except Exception:
        pass
    with _config_lock:
        _config_cache = resultado
    return dict(resultado)


def _invalidar_cache_config() -> None:
    """Fuerza la próxima llamada a cargar_config() a leer de disco."""
    global _config_cache
    with _config_lock:
        _config_cache = None


_ultimo_error_config: str | None = None


def _obtener_ultimo_error_config() -> str | None:
    """Devuelve el último error ocurrido al guardar/cargar config, o None."""
    return _ultimo_error_config


def guardar_config(datos: dict) -> None:
    """
    Escribe el diccionario 'datos' en config.json con indentación legible.

    Estrategia de escritura segura:
      1. Escribe el JSON en un archivo temporal (.tmp).
      2. Si existe un config.json previo válido, lo renombra como .bak.
      3. Renombra el temporal a config.json (atómico en el mismo volumen).

    Usa thread-lock para evitar escrituras concurrentes desde hilos
    distintos que podrían corromper el archivo.
    """
    global _ultimo_error_config, _config_cache
    _ultimo_error_config = None
    with _config_lock:
        try:
            os.makedirs(os.path.dirname(ARCHIVO_CONFIG), exist_ok=True)
            tmp_path = ARCHIVO_CONFIG + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            if os.path.isfile(ARCHIVO_CONFIG):
                respaldo = ARCHIVO_CONFIG + ".bak"
                try:
                    with open(respaldo, "w", encoding="utf-8") as fb:
                        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as fo:
                            fb.write(fo.read())
                except Exception:
                    pass
            os.replace(tmp_path, ARCHIVO_CONFIG)
            _config_cache = dict(datos)
        except Exception as e:
            _ultimo_error_config = str(e)
            try:
                if os.path.isfile(ARCHIVO_CONFIG + ".tmp"):
                    os.unlink(ARCHIVO_CONFIG + ".tmp")
            except Exception:
                pass


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

"""
utils/paths.py — Utilidades de rutas del sistema de archivos.
"""

import os
import sys
from pathlib import Path


def resource_path(relative_path):
    """Devuelve la ruta absoluta a un recurso, compatible con PyInstaller.

    Cuando la app se ejecuta como ejecutable empaquetado por PyInstaller,
    los recursos residen en sys._MEIPASS. En modo desarrollo, se usa el
    directorio de trabajo actual.

    Args:
        relative_path: ruta relativa al recurso (ej. "config/config.json").

    Returns:
        Ruta absoluta al recurso como string.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_project_root() -> Path:
    """
    Devuelve el directorio raíz del proyecto de forma determinista,
    independiente del working directory.

    Se basa en la ubicación de este mismo archivo (utils/paths.py).
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


def get_writable_path(relative_path: str) -> str:
    """Devuelve una ruta absoluta escribible para un archivo de datos.

    En modo desarrollo usa el directorio de trabajo actual (igual que
    resource_path sin _MEIPASS). En modo PyInstaller (sys.frozen) usa
    %APPDATA%/SSAuto/ para que los archivos de configuracion y estado
    se puedan leer y escribir (sys._MEIPASS es solo lectura).

    Args:
        relative_path: ruta relativa al archivo (ej. "config/config.json").

    Returns:
        Ruta absoluta escribible como string.
    """
    if getattr(sys, "frozen", False):
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "SSAuto")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, relative_path)
    return os.path.abspath(relative_path)

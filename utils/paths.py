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
    return Path(__file__).resolve().parent.parent

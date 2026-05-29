"""
utils/paths.py — Utilidades de rutas del sistema de archivos.
"""

import os
import sys
from pathlib import Path


def resource_path(relative_path):
    """Devuelve la ruta absoluta a un recurso, compatible con PyInstaller."""
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

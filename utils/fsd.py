"""
utils/fsd.py — Utilidades de normalización de números FSD.

Unifica las funciones que estaban repartidas entre core/browser.py y
scraping_sunrun.py en un solo módulo.
"""

import re


def solo_digitos(fsd: str) -> str:
    """
    Extrae solo los dígitos del FSD, en cualquier formato de entrada.

    "FSD-1172172"  → "1172172"
    "FSD1172172"   → "1172172"
    "fsd 1172172"  → "1172172"
    "1172172"      → "1172172"
    """
    return re.sub(r"[^0-9]", "", fsd)


def fsd_display(numero: str) -> str:
    """Formato de display estándar: "FSD-1172172"."""
    return f"FSD-{numero}"


def normalizar_fsd(fsd: str | None) -> str | None:
    """
    Normaliza el FSD para búsqueda inteligente en pestañas.

    - Si es None, vacío o solo espacios: devuelve None
    - Si es "980124": convierte a "FSD-980124"
    - Si es "FSD-980124": lo mantiene igual
    - Case-insensitive: siempre devuelve mayúsculas
    """
    if not fsd or not isinstance(fsd, str):
        return None

    fsd = fsd.strip().upper()

    if not fsd:
        return None

    if fsd.startswith("FSD-"):
        return fsd

    if fsd.replace("-", "").isdigit():
        return f"FSD-{fsd}"

    return fsd

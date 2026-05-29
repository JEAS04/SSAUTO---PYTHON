"""
services/driver_provider.py — Factory de drivers Chrome para Selenium.

Responsabilidad única: crear o conectar un driver según las opciones.
No conoce de sesiones, plugins, ni UI.
"""

from __future__ import annotations

from typing import Callable

from core.browser import BrowserFactory, ErrorBrowser, puerto_activo


class DriverProvider:
    """Crea o conecta un driver Chrome y rastrea su propiedad."""

    def obtener(
        self,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
    ) -> tuple:
        """
        Devuelve (driver, es_propio).
        - es_propio=True  → Chrome nuevo (debe cerrarse al terminar)
        - es_propio=False → Chrome existente (no tocar)
        """
        if usar_chrome_existente:
            if not puerto_activo():
                raise RuntimeError(
                    "No hay Chrome con depuracion en puerto 9222. "
                    "Abrelo desde el boton 'Abrir Chrome con depuracion'."
                )
            log("  -> Conectando al Chrome existente (puerto 9222)...")
            driver = BrowserFactory.conectar_existente()
            log("  v Conectado.")
            return driver, False
        else:
            log("  -> Abriendo Chrome nuevo...")
            driver = BrowserFactory.nuevo(headless=headless)
            log("  v Chrome abierto.")
            return driver, True

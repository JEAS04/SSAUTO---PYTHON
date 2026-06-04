"""
services/driver_provider.py — Factory de drivers Chrome para Selenium.

Responsabilidad única: crear o conectar un driver según las opciones.
No conoce de sesiones, plugins, ni UI.
"""

from __future__ import annotations

from typing import Callable

from core.browser import BrowserFactory, ErrorBrowser, puerto_activo


class DriverProvider:
    """Crea o conecta un driver Chrome y rastrea su propiedad.

    Responsabilidad unica: devolver una tupla (driver, es_propio) donde
    es_propio indica si el driver debe cerrarse al terminar (True para
    Chrome nuevo, False para Chrome existente del usuario).
    """

    def obtener(
        self,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
    ) -> tuple:
        """
        Devuelve un driver Chrome listo para usar.

        Args:
            log: callback para registrar mensajes de estado.
            headless: si True, abre Chrome en modo sin interfaz grafica.
            usar_chrome_existente: si True, intenta conectar al Chrome del
                usuario en puerto 9222. Si False, abre un Chrome nuevo.

        Returns:
            Tupla (driver, es_propio) donde:
                - driver: instancia de webdriver.Chrome
                - es_propio: True si es Chrome nuevo (debe cerrarse con quit()),
                  False si es el Chrome del usuario (no tocar).

        Raises:
            RuntimeError: si se solicita Chrome existente pero el puerto 9222
                no esta activo.
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

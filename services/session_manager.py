"""
services/session_manager.py — Gestion de sesion del plugin.

Responsabilidad unica: posicionar la pestana correcta y asegurar que
la sesion este activa (cookies + login). No conoce de driver creation
ni de subida de archivos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from core.base_plugin import SitioPlugin
from core.browser import esperar_carga
from config.credenciales import cargar_cookies, cargar_credenciales


class SessionManager:
    """Asegura la sesion del plugin en el navegador.

    Responsabilidad unica: posicionar la pestana correcta y garantizar que
    la sesion este activa (intentando cookies primero, luego login automatico).
    No crea drivers ni sube archivos.
    """

    def __init__(self, driver):
        """Inicializa el gestor de sesion con un driver ya conectado.

        Args:
            driver: instancia activa de Selenium WebDriver.
        """
        self.driver = driver

    def asegurar(
        self,
        plugin: SitioPlugin,
        log: Callable[[str], None],
        credenciales_sesion: dict,
    ) -> None:
        """
        Verifica/establece la sesion del plugin.
        Lanza RuntimeError si no se puede establecer.
        """
        self._posicionar_pestana(plugin, log)

        if plugin.usar_pagina_actual:
            plugin.verificar_sesion(self.driver, log)
            return

        # Chrome propio: intentar cookies primero, luego login
        ruta_cookies = Path(f"cookies/{plugin.nombre}.pkl")
        if ruta_cookies.exists():
            log(f"  -> Restaurando sesion con cookies para {plugin.nombre}...")
            url_base = getattr(plugin, "URL_LOGIN", "")
            if url_base:
                try:
                    cargar_cookies(
                        self.driver, {"nombre": plugin.nombre}, url_base
                    )
                    esperar_carga(self.driver, timeout=5)
                    if plugin.verificar_sesion(self.driver, log):
                        return
                    log("  . Cookies invalidas, iniciando login...")
                except Exception as e:
                    log(f"  . Error restaurando cookies: {e}")

        # Login automatico
        credenciales = self._obtener_credenciales(
            plugin.nombre, credenciales_sesion
        )
        if credenciales:
            if plugin.hacer_login(self.driver, credenciales, log):
                return

        raise RuntimeError(
            f"No se pudo establecer sesion para {plugin.nombre}. "
            f"Verifica las credenciales en el menu 'Credenciales'."
        )

    def _posicionar_pestana(
        self, plugin: SitioPlugin, log: Callable[[str], None]
    ) -> None:
        """Valida la pestana del plugin y recorre tabs si hace falta."""
        if plugin.usar_pagina_actual and plugin.dominio:
            log(f"  -> Validando pestana activa de {plugin.nombre}...")
            try:
                url = self.driver.current_url.lower()
                if plugin.dominio.lower() not in url:
                    log(
                        f"  . Pestana activa no es {plugin.nombre}. "
                        f"El plugin buscara la pestana correcta."
                    )
                else:
                    log("  v Pestana activa validada.")
            except Exception:
                log(
                    f"  . Pestaña sin contexto — {plugin.nombre} "
                    f"buscara la correcta por su cuenta."
                )
        elif not plugin.usar_pagina_actual and plugin.dominio:
            log(
                f"  . [{plugin.nombre}] No se cambia de pestana "
                f"automaticamente."
            )

    @staticmethod
    def _es_tab_valida(driver, handle) -> bool:
        """Verifica si un handle de pestana tiene un contexto JavaScript vivo.

        Cambia temporalmente a la pestana, ejecuta un script minimo y
        retorna True si el contexto responde.

        Args:
            driver: instancia de WebDriver.
            handle: identificador de la pestana (window handle).

        Returns:
            True si la pestana responde a ejecucion de JavaScript.
        """
        try:
            driver.switch_to.window(handle)
            driver.execute_script("return 1")
            return True
        except Exception:
            return False

    @staticmethod
    def _obtener_credenciales(nombre_plugin: str, sesion: dict) -> dict:
        """Credenciales de la sesion actual o del llavero del SO."""
        if nombre_plugin in sesion:
            return sesion[nombre_plugin]
        usuario, clave = cargar_credenciales(nombre_plugin)
        if usuario:
            return {"usuario": usuario, "clave": clave}
        return {}

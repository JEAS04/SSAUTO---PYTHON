"""
services/sesion_service.py — Orquestación de sesiones y subidas.

Este servicio es el puente entre la UI y los plugins:
  - Crea el driver según las opciones del usuario.
  - Localiza la pestaña correcta.
  - Verifica/establece la sesión.
  - Llama al plugin para subir el archivo.
  - Devuelve el resultado a la UI.

La UI no sabe nada de Selenium. Los plugins no saben nada de la UI.
Este servicio habla con ambos.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import BrowserFactory, esperar_carga, puerto_activo
from core.plugin_registry import PluginRegistry
from config.credenciales import cargar_cookies, cargar_credenciales


class SesionService:
    """
    Orquesta el ciclo completo de una subida para un plugin dado.

    Uso desde la UI (hilo secundario):
        resultado = SesionService.ejecutar_subida(
            nombre_plugin="HUBSPOT",
            ruta_imagen="screenshots/captura_xxx.png",
            log=self._log,
            headless=False,
            usar_chrome_existente=True,
            credenciales_sesion=self._credenciales_sesion,
            opciones={"auto_submit_nota": True},
        )
    """

    @classmethod
    def ejecutar_subida(
        cls,
        nombre_plugin: str,
        ruta_imagen: str,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
        credenciales_sesion: dict | None = None,
        opciones: dict | None = None,
    ) -> ResultadoSubida:
        """
        Ciclo completo: driver → sesión → plugin.subir() → resultado.

        Nunca cierra el driver del usuario (Chrome existente).
        Siempre cierra el driver propio (Chrome nuevo) al terminar.
        """
        plugin = PluginRegistry.obtener(nombre_plugin)
        driver = None
        driver_propio = False

        try:
            # ── 1. Obtener driver ──────────────────────────────────────
            driver, driver_propio = cls._obtener_driver(
                log, headless, usar_chrome_existente
            )

            # ── 2. Validar pestaña actual ─────────────────────────────
            cls._posicionar_pestana(driver, plugin, log)

            # ── 3. Verificar / establecer sesión ──────────────────────
            cls._asegurar_sesion(driver, plugin, log, credenciales_sesion or {})

            # ── 4. Llamar al plugin ───────────────────────────────────
            credenciales = cls._obtener_credenciales(
                plugin.nombre, credenciales_sesion or {}
            )
            ctx = ContextoSubida(
                ruta_imagen=ruta_imagen,
                log=log,
                driver=driver,
                credenciales=credenciales,
                opciones=opciones or {},
            )
            log(f"  → [{plugin.nombre}] Iniciando subida…")
            resultado = plugin.subir(ctx)

            if resultado.exitoso:
                log(f"  ✓ [{plugin.nombre}] {resultado.mensaje}")
            else:
                log(f"  ✗ [{plugin.nombre}] {resultado.mensaje}")

            return resultado

        except Exception as e:
            log(f"  ✗ [{nombre_plugin}] Error inesperado: {e}")
            return ResultadoSubida(exitoso=False, mensaje=str(e))

        finally:
            if driver_propio and driver:
                try:
                    driver.quit()
                    log(f"  · [{nombre_plugin}] Chrome cerrado.")
                except Exception:
                    pass

    # ── Pasos internos ────────────────────────────────────────────────

    @staticmethod
    def _obtener_driver(log: Callable, headless: bool, usar_existente: bool):
        """Crea o conecta el driver. Devuelve (driver, es_propio)."""
        from core.browser import ErrorBrowser

        if usar_existente:
            if not puerto_activo():
                raise RuntimeError(
                    "No hay Chrome con depuración en puerto 9222. "
                    "Ábrelo desde el botón 'Abrir Chrome con depuración'."
                )
            log("  → Conectando al Chrome existente (puerto 9222)…")
            driver = BrowserFactory.conectar_existente()
            log("  ✓ Conectado.")
            return driver, False
        else:
            log("  → Abriendo Chrome nuevo…")
            driver = BrowserFactory.nuevo(headless=headless)
            log("  ✓ Chrome abierto.")
            return driver, True

    @staticmethod
    def _posicionar_pestana(driver, plugin: SitioPlugin, log: Callable) -> None:
        """Valida SOLO la pestaña actual; nunca recorre ni cambia tabs del usuario."""
        if plugin.usar_pagina_actual and plugin.dominio:
            log(f"  → Validando pestaña activa de {plugin.nombre}…")
            handle = driver.current_window_handle
            url = driver.current_url.lower()
            if plugin.dominio.lower() not in url:
                raise RuntimeError(
                    f"La pestaña activa no es {plugin.nombre}. "
                    f"Ubicate en la pestaña visible/enfocada de {plugin.nombre} y reintentá."
                )
            try:
                mismo_handle = driver.current_window_handle == handle
                visible = driver.execute_script(
                    "return document.visibilityState === 'visible'"
                )
                focused = driver.execute_script("return document.hasFocus()")
            except Exception:
                mismo_handle = visible = focused = False
            if not mismo_handle or not visible or not focused:
                raise RuntimeError(
                    "Subida cancelada: la pestaña/ventana activa perdió foco. "
                    "No se subió información."
                )
            log(f"  ✓ Pestaña activa validada.")
        elif not plugin.usar_pagina_actual and plugin.dominio:
            log(f"  · [{plugin.nombre}] No se cambia de pestaña automáticamente.")

    @staticmethod
    def _asegurar_sesion(
        driver, plugin: SitioPlugin, log: Callable, credenciales_sesion: dict
    ) -> None:
        """
        Verifica la sesión. Si no está activa y es Chrome existente, advierte.
        Si es Chrome nuevo, intenta restaurar cookies o hacer login automático.
        """
        if plugin.usar_pagina_actual:
            # Modo página actual: el usuario ya tiene la sesión. Solo verificamos.
            plugin.verificar_sesion(driver, log)
            return

        # Chrome propio: intentar cookies primero, luego login
        ruta_cookies = Path(f"cookies/{plugin.nombre}.pkl")
        if ruta_cookies.exists():
            log(f"  → Restaurando sesión con cookies para {plugin.nombre}…")
            url_base = getattr(plugin, "URL_LOGIN", "")
            if url_base:
                try:
                    cargar_cookies(driver, {"nombre": plugin.nombre}, url_base)
                    esperar_carga(driver, timeout=5)
                    if plugin.verificar_sesion(driver, log):
                        return
                    log("  · Cookies inválidas, iniciando login…")
                except Exception as e:
                    log(f"  · Error restaurando cookies: {e}")

        # Login automático
        credenciales = SesionService._obtener_credenciales(
            plugin.nombre, credenciales_sesion
        )
        if credenciales:
            if plugin.hacer_login(driver, credenciales, log):
                return
        raise RuntimeError(
            f"No se pudo establecer sesión para {plugin.nombre}. "
            f"Verifica las credenciales en el menú 'Credenciales'."
        )

    @staticmethod
    def _obtener_credenciales(nombre_plugin: str, sesion: dict) -> dict:
        """Credenciales de la sesión actual o del llavero del SO."""
        if nombre_plugin in sesion:
            return sesion[nombre_plugin]
        usuario, clave = cargar_credenciales(nombre_plugin)
        if usuario:
            return {"usuario": usuario, "clave": clave}
        return {}

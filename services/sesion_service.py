"""
services/sesion_service.py — Orquestacion de subidas.

Este servicio es el puente entre la UI y los plugins:
  - Delega la creacion del driver a DriverProvider.
  - Delega la gestion de sesion a SessionManager.
  - Llama al plugin para subir el archivo.
  - Devuelve el resultado a la UI.

La UI no sabe nada de Selenium. Los plugins no saben nada de la UI.
"""

from __future__ import annotations

from typing import Callable

from core.base_plugin import ContextoSubida, ResultadoSubida
from core.plugin_registry import PluginRegistry
from utils.fsd import normalizar_fsd
from services.driver_provider import DriverProvider
from services.session_manager import SessionManager


class SesionService:
    """
    Orquesta el ciclo completo de una subida para un plugin dado.

    Uso desde la UI (hilo secundario):
        servicio = SesionService()
        resultado = servicio.ejecutar_subida(
            nombre_plugin="HUBSPOT",
            ruta_imagen="screenshots/captura_xxx.png",
            log=self._log,
            headless=False,
            usar_chrome_existente=True,
            credenciales_sesion=self._credenciales_sesion,
            opciones={"auto_submit_nota": True},
            rutas_imagenes=["screenshots/extra1.png", "screenshots/extra2.png"],
        )
    """

    def __init__(self, driver_provider=None):
        """
        Args:
            driver_provider: DriverProvider opcional para DI en tests.
        """
        self._driver_provider = driver_provider or DriverProvider()

    def ejecutar_subida(
        self,
        nombre_plugin: str,
        ruta_imagen: str,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
        credenciales_sesion: dict | None = None,
        opciones: dict | None = None,
        fsd: str | None = None,
        cancel_event: object | None = None,
        rutas_imagenes: list[str] | None = None,
    ) -> ResultadoSubida:
        """
        Ciclo completo: driver -> sesion -> plugin.subir() -> resultado.

        Args:
            nombre_plugin: Identificador del plugin (ej. "HUBSPOT").
            ruta_imagen: Ruta de la imagen principal a subir.
            log: Callback para mensajes de progreso.
            headless: Si True, lanza Chrome en modo headless.
            usar_chrome_existente: Si True, se conecta a una instancia de Chrome
                ya abierta por el usuario en el puerto 9222.
            credenciales_sesion: Credenciales de sesión ya cargadas.
            opciones: Diccionario de flags extra (auto_submit_nota, etc.).
            fsd: FSD para búsqueda inteligente de pestaña.
            cancel_event: threading.Event para abortar el proceso.
            rutas_imagenes: Lista opcional de rutas de imágenes adicionales
                para adjuntar múltiples capturas en una sola nota.

        Returns:
            ResultadoSubida con el estado final de la operación.

        Nunca cierra el driver del usuario (Chrome existente).
        Siempre cierra el driver propio (Chrome nuevo) al terminar.
        """
        plugin = PluginRegistry.obtener(nombre_plugin)
        driver = None
        driver_propio = False

        try:
            # 1. Obtener driver
            driver, driver_propio = self._driver_provider.obtener(
                log, headless, usar_chrome_existente
            )

            if cancel_event and hasattr(cancel_event, 'is_set') and cancel_event.is_set():
                log(f"  ⚠ [{nombre_plugin}] Cancelado antes de iniciar sesión.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # 2. Asegurar sesion
            session = SessionManager(driver)
            session.asegurar(plugin, log, credenciales_sesion or {})

            if cancel_event and hasattr(cancel_event, 'is_set') and cancel_event.is_set():
                log(f"  ⚠ [{nombre_plugin}] Cancelado antes de subir.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # 3. Llamar al plugin
            credenciales = SessionManager._obtener_credenciales(
                plugin.nombre, credenciales_sesion or {}
            )
            fsd_normalizado = normalizar_fsd(fsd)
            ctx = ContextoSubida(
                ruta_imagen=ruta_imagen,
                log=log,
                driver=driver,
                credenciales=credenciales,
                opciones=opciones or {},
                fsd=fsd_normalizado,
                cancelado=cancel_event,
                rutas_imagenes=rutas_imagenes,
            )
            log(f"  -> [{plugin.nombre}] Iniciando subida...")
            resultado = plugin.subir(ctx)

            if resultado.exitoso:
                log(f"  v [{plugin.nombre}] {resultado.mensaje}")
            else:
                log(f"  x [{plugin.nombre}] {resultado.mensaje}")

            return resultado

        except Exception as e:
            log(f"  x [{nombre_plugin}] Error inesperado: {e}")
            return ResultadoSubida(exitoso=False, mensaje=str(e))

        finally:
            if driver_propio and driver:
                try:
                    driver.quit()
                    log(f"  . [{nombre_plugin}] Chrome cerrado.")
                except Exception:
                    pass

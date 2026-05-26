"""
core/browser.py — Creación y gestión de instancias de ChromeDriver.

Extrae la lógica de crear_driver() de automatizacion.py a un módulo propio
sin dependencias de UI. Los plugins y servicios lo usan para obtener
un driver ya configurado.

Uso:
    from core.browser import BrowserFactory, encontrar_pestana
    driver = BrowserFactory.conectar_existente()   # puerto 9222
    driver = BrowserFactory.nuevo(headless=True)   # Chrome nuevo
"""

from __future__ import annotations

import logging
import time
from typing import Callable

from selenium import webdriver
from subprocess import Popen
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import socket
import time

logger = logging.getLogger("ssauto.browser")

# Puerto estándar de Chrome remote debugging
PUERTO_DEBUG = 9222
CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"


class ErrorBrowser(Exception):
    """Error al crear o conectar el driver de Chrome."""

    pass


class BrowserFactory:
    """
    Métodos de clase para obtener instancias de ChromeDriver configuradas.

    Dos modos:
      - conectar_existente(): se engancha al Chrome abierto por el usuario.
      - nuevo(): abre un Chrome nuevo (headless o visible).
    """

    @classmethod
    def conectar_existente(cls, puerto: int = PUERTO_DEBUG) -> webdriver.Chrome:
        """
        Conecta al Chrome ya abierto por el usuario en el puerto dado.

        No cierra este driver al terminar — es el Chrome del usuario.

        Lanza ErrorBrowser si no hay Chrome con debugging en ese puerto.
        """

        def puerto_activo_local():
            try:
                with socket.create_connection(("127.0.0.1", puerto), timeout=1):
                    return True
            except:
                return False

        if not puerto_activo_local():
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
            ]

            chrome_path = next((p for p in chrome_paths if Path(p).exists()), None)
            if not chrome_path:
                raise ErrorBrowser(f"Chrome no encontrado en el puerto: {puerto}.")

            Popen(
                [
                    chrome_path,
                    f"--remote-debugging-port={puerto}",
                    f"--user-data-dir={CHROME_USER_DATA}",
                    "--disable-popup-blocking",
                    "--disable-default-apps",
                ]
            )

            for _ in range(20):
                if puerto_activo_local():
                    break
                time.sleep(0.5)

        opciones = webdriver.ChromeOptions()
        opciones.add_experimental_option("debuggerAddress", f"127.0.0.1:{puerto}")

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opciones,
            )
            cls._inyectar_antideteccion(driver)
            logger.debug(f"Conectado al Chrome en puerto {puerto}.")
            return driver
        except Exception as e:
            raise ErrorBrowser(
                f"No se pudo conectar al Chrome en puerto {puerto}. "
                f"¿Está abierto con --remote-debugging-port={puerto}? Error: {e}"
            ) from e

    @classmethod
    def nuevo(cls, headless: bool = False) -> webdriver.Chrome:
        """
        Abre un Chrome nuevo gestionado por la aplicación.

        Este driver SÍ debe cerrarse con driver.quit() al terminar.
        """
        opciones = webdriver.ChromeOptions()
        opciones.add_argument("--disable-blink-features=AutomationControlled")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")

        if headless:
            opciones.add_argument("--headless=new")
            opciones.add_argument("--disable-gpu")

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opciones,
            )
            cls._inyectar_antideteccion(driver)
            return driver
        except Exception as e:
            raise ErrorBrowser(f"No se pudo abrir Chrome nuevo: {e}") from e

    @classmethod
    def crear(
        cls, headless: bool, usar_existente: bool, puerto: int = PUERTO_DEBUG
    ) -> webdriver.Chrome:
        """
        Punto de entrada unificado — elige el modo según los flags.

        Úsalo cuando la decisión depende de opciones del usuario (como en la UI).
        """
        if usar_existente:
            return cls.conectar_existente(puerto)
        return cls.nuevo(headless)

    # ── Antidetección ─────────────────────────────────────────────────

    @staticmethod
    def _inyectar_antideteccion(driver: webdriver.Chrome) -> None:
        """
        Intenta ocultar navigator.webdriver.

        En Chrome 147+ esto falla en sesiones de debugging — se captura
        silenciosamente porque no es un error crítico.
        """
        try:
            driver.execute_script("""
            try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            } catch(e) {
                // Chrome 147+ en sesiones reales no permite redefinir webdriver. Normal.
            }
            """)
        except Exception as e:
            logger.debug(
                f"Script antidetección no aplicado (esperado en Chrome moderno): {e}"
            )


# ── Helpers de pestañas ───────────────────────────────────────────────


def encontrar_pestana(driver, subcadena_url: str, log: Callable | None = None) -> bool:
    """
    Cambia al driver a la primera pestaña cuya URL contenga subcadena_url.

    Devuelve True si la encontró y cambió, False si no.
    """
    _log = log or (lambda m: None)
    try:
        handles = driver.window_handles
        for handle in handles:
            try:
                driver.switch_to.window(handle)
                time.sleep(0.3)
                if subcadena_url.lower() in driver.current_url.lower():
                    _log(f"  ✓ Pestaña encontrada: {driver.title}")
                    return True
            except Exception:
                continue
        _log(f"  ⚠ No se encontró pestaña con '{subcadena_url}'")
        if handles:
            driver.switch_to.window(handles[0])
        return False
    except Exception as e:
        _log(f"  ⚠ Error al buscar pestaña: {e}")
        return False


def esperar_carga(driver, timeout: float = 10.0) -> bool:
    """Espera a que document.readyState sea 'complete'."""
    import time as _time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, WebDriverException

    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        _time.sleep(0.5)
        return True
    except (TimeoutException, WebDriverException):
        return False


def puerto_activo(host: str = "127.0.0.1", puerto: int = PUERTO_DEBUG) -> bool:
    """Devuelve True si hay algo escuchando en host:puerto."""
    import socket

    try:
        with socket.create_connection((host, puerto), timeout=1):
            return True
    except OSError:
        return False

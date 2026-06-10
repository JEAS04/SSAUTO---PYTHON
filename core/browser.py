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

import concurrent.futures
import logging
import os
import sys
import time
from pathlib import Path
from typing import Callable

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from subprocess import Popen
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("ssauto.browser")

# ── Constantes de Chrome ───────────────────────────────────────────────
PUERTO_DEBUG = 9222
CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
]

_chrome_exe_cache: str | None = None

# ── Cache de chromedriver (evita descargarlo dos veces) ────────────────
_chromedriver_path: str | None = None
_frozen_fallback: bool = False


def _obtener_chromedriver_bundled() -> str | None:
    """Busca chromedriver.exe empaquetado con el .exe (PyInstaller)."""
    for base in (Path(sys.executable).parent, Path(sys._MEIPASS)):
        candidato = base / "chromedriver.exe"
        if candidato.exists():
            return str(candidato)
    return None


def _obtener_chromedriver_path() -> str:
    """Devuelve la ruta al chromedriver.

    Prioridad:
      1. Cache en memoria (si ya se obtuvo con exito).
      2. Descargar version correcta via webdriver_manager (30s timeout).
         Con internet, esto siempre da la version que coincide con Chrome.
      3. Si no hay internet → fallback: chromedriver.exe empaquetado.
         Sin internet, usa el que viene en el build.
    """
    global _chromedriver_path, _frozen_fallback
    if _chromedriver_path is not None and Path(_chromedriver_path).exists():
        return _chromedriver_path

    # Intentar descargar la version correcta (con internet)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            futuro = ex.submit(ChromeDriverManager().install)
            _chromedriver_path = futuro.result(timeout=30)
        _frozen_fallback = False
        return _chromedriver_path
    except concurrent.futures.TimeoutError:
        pass  # sin internet, probar fallback
    except Exception:
        pass  # error de red, probar fallback

    # Fallback: chromedriver empaquetado (sin internet)
    if getattr(sys, "frozen", False):
        bundled = _obtener_chromedriver_bundled()
        if bundled:
            _chromedriver_path = bundled
            _frozen_fallback = True
            logger.warning("Usando chromedriver empaquetado (sin internet).")
            return _chromedriver_path

    raise ErrorBrowser(
        "No se pudo obtener chromedriver — sin internet y no hay "
        "chromedriver.exe junto al ejecutable."
    )


def _obtener_chromedriver_forzado() -> str:
    """Fuerza la descarga de chromedriver, ignorando el cache.

    Se usa cuando el chromedriver empaquetado no coincide con la
    version de Chrome instalada (SessionNotCreatedException).
    """
    global _chromedriver_path, _frozen_fallback
    _chromedriver_path = None
    _frozen_fallback = False
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            futuro = ex.submit(ChromeDriverManager().install)
            _chromedriver_path = futuro.result(timeout=30)
        return _chromedriver_path
    except concurrent.futures.TimeoutError:
        raise ErrorBrowser(
            "Timeout al descargar chromedriver — sin internet.\n"
            "El chromedriver empaquetado no coincide con tu version de Chrome.\n"
            "Conectate a internet o instala la version correcta de Chrome."
        )
    except Exception as e:
        raise ErrorBrowser(
            f"No se pudo descargar chromedriver: {e}\n"
            "Verifica tu conexion a internet."
        ) from e


def obtener_chrome_exe() -> str | None:
    """Devuelve la primera ruta de Chrome que exista en el sistema (cacheada)."""
    global _chrome_exe_cache
    if _chrome_exe_cache is not None:
        return _chrome_exe_cache if os.path.isfile(_chrome_exe_cache) else None
    for p in CHROME_PATHS:
        if os.path.isfile(p):
            _chrome_exe_cache = p
            return p
    return None


# ── Referencia global al proceso de Chrome lanzado por la app ──────────
_ultimo_chrome_proc: Popen | None = None


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
            return puerto_activo("127.0.0.1", puerto)

        if not puerto_activo_local():
            chrome_path = obtener_chrome_exe()
            if not chrome_path:
                raise ErrorBrowser(f"Chrome no encontrado en el puerto: {puerto}.")

            global _ultimo_chrome_proc
            _ultimo_chrome_proc = Popen(
                [
                    chrome_path,
                    f"--remote-debugging-port={puerto}",
                    f"--user-data-dir={CHROME_USER_DATA}",
                    "--disable-popup-blocking",
                    "--disable-default-apps",
                ]
            )

            for intento in range(20):
                if puerto_activo_local():
                    break
                time.sleep(0.1 + intento * 0.05)  # backoff progresivo

        opciones = webdriver.ChromeOptions()
        opciones.add_experimental_option("debuggerAddress", f"127.0.0.1:{puerto}")

        try:
            driver = cls._crear_driver(opciones)
            _inyectar_antideteccion(driver)
            logger.debug(f"Conectado al Chrome en puerto {puerto}.")
            return driver
        except SessionNotCreatedException as e:
            if not _frozen_fallback:
                raise ErrorBrowser(
                    f"No se pudo conectar al Chrome en puerto {puerto}. "
                    f"¿Está abierto con --remote-debugging-port={puerto}? Error: {e}"
                ) from e
            logger.warning(
                "chromedriver empaquetado incompatible, descargando version correcta..."
            )
            driver = cls._crear_driver(opciones, forzar_descarga=True)
            _inyectar_antideteccion(driver)
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
            driver = cls._crear_driver(opciones)
            _inyectar_antideteccion(driver)
            return driver
        except SessionNotCreatedException as e:
            if not _frozen_fallback:
                raise ErrorBrowser(
                    f"No se pudo abrir Chrome nuevo: {e}"
                ) from e
            # chromedriver empaquetado no coincide con Chrome → forzar descarga
            logger.warning(
                "chromedriver empaquetado incompatible, descargando version correcta..."
            )
            driver = cls._crear_driver(opciones, forzar_descarga=True)
            _inyectar_antideteccion(driver)
            return driver
        except Exception as e:
            raise ErrorBrowser(f"No se pudo abrir Chrome nuevo: {e}") from e

    @classmethod
    def _crear_driver(
        cls, opciones: webdriver.ChromeOptions, forzar_descarga: bool = False
    ) -> webdriver.Chrome:
        path = (
            _obtener_chromedriver_forzado() if forzar_descarga
            else _obtener_chromedriver_path()
        )
        return webdriver.Chrome(service=Service(path), options=opciones)

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
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, WebDriverException

    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
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

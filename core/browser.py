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
_CHROME_DATA_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "chrome_sesion_ssauto",
)
CHROME_USER_DATA = _CHROME_DATA_DIR
_PROG_FILES = os.environ.get("ProgramFiles", r"C:\Program Files")
_PROG_FILES_X86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
_LOCAL_APP_DATA = os.environ.get(
    "LOCALAPPDATA", str(Path.home() / "AppData/Local")
)
CHROME_PATHS = [
    os.path.join(_PROG_FILES, r"Google\Chrome\Application\chrome.exe"),
    os.path.join(_PROG_FILES_X86, r"Google\Chrome\Application\chrome.exe"),
    os.path.join(_LOCAL_APP_DATA, r"Google\Chrome\Application\chrome.exe"),
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
                    "--disable-background-mode",
                    "--disable-popup-blocking",
                    "--disable-default-apps",
                    "--no-first-run",
                    "--no-default-browser-check",
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


def obtener_chrome_user_data_dir() -> str | None:
    """Detecta el --user-data-dir del proceso Chrome actual via psutil.
    Si no lo encuentra, devuelve el perfil por defecto de Chrome."""
    try:
        import psutil
    except ImportError:
        return None
    for proc in psutil.process_iter(["name", "cmdline"]):
        try:
            info = proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if info and info.get("name", "").lower() in ("chrome.exe", "chromium.exe"):
            cmdline = info.get("cmdline") or []
            for i, arg in enumerate(cmdline):
                if arg == "--user-data-dir" and i + 1 < len(cmdline):
                    return cmdline[i + 1]
            break
    return str(
        Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")))
        / "Google" / "Chrome" / "User Data"
    )


def detectar_perfil_activo(user_data_dir: str) -> str:
    """Lee Local State del user-data-dir para obtener el perfil activo.

    Busca 'profile.last_used' en Local State. Si no existe,
    devuelve 'Default'.
    """
    import json
    local_state = Path(user_data_dir) / "Local State"
    try:
        with open(local_state, "r", encoding="utf-8") as f:
            data = json.load(f)
        nombre = (
            data.get("profile", {})
            .get("last_used", "Default")
        )
        return nombre or "Default"
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return "Default"


def obtener_chrome_exe_desde_proceso() -> str | None:
    """Obtiene la ruta del ejecutable de Chrome desde el proceso corriendo via psutil.
    Mas confiable que CHROME_PATHS porque usa el proceso real."""
    try:
        import psutil
    except ImportError:
        return None
    for proc in psutil.process_iter(["name", "exe"]):
        try:
            info = proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if info and info.get("name", "").lower() in ("chrome.exe", "chromium.exe"):
            exe = info.get("exe")
            if exe and os.path.isfile(exe):
                return exe
            break
    return None


def cerrar_chrome(log: Callable[[str], None] | None = None) -> bool:
    """Cierra todos los procesos Chrome y espera a que mueran.
    Devuelve True si no queda ningun proceso Chrome corriendo."""
    _log = log or (lambda _: None)
    try:
        import psutil
    except ImportError:
        return False

    procesos: list = []
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if proc.info.get("name", "").lower() in ("chrome.exe", "chromium.exe"):
                procesos.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if not procesos:
        _log("  Ningun proceso Chrome encontrado.")
        return True

    _log(f"  {len(procesos)} procesos Chrome encontrados. Cerrando...")

    # Ronda 1: terminate (WM_CLOSE)
    for proc in procesos:
        try:
            proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    time.sleep(2)

    # Ronda 2: kill forzoso
    for proc in procesos:
        try:
            if proc.is_running():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Esperar que todos mueran
    for i in range(20):
        vivos = 0
        for proc in procesos:
            try:
                if proc.is_running():
                    vivos += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if vivos == 0:
            _log("  ✓ Chrome cerrado completamente.")
            time.sleep(0.5)
            return True
        time.sleep(0.3)

    _log(f"  ⚠ {vivos} procesos no se pudieron cerrar.")
    return False


def _limpiar_locks(user_data_dir: str, _log: Callable[[str], None]) -> None:
    """Borra archivos de bloqueo de Chrome que impiden el puerto de debug."""
    locks = ["SingletonLock", "SingletonSocket", "SingletonCookie", "lockfile"]
    base = Path(user_data_dir)
    for lock in locks:
        p = base / lock
        if p.exists():
            try:
                p.unlink()
                _log(f"  → Lock eliminado: {lock}")
            except OSError:
                pass


def abrir_chrome_debug_con_perfil(
    user_data_dir: str,
    puerto: int = PUERTO_DEBUG,
    profile_dir: str = "Default",
    chrome_exe: str | None = None,
    log: Callable[[str], None] | None = None,
) -> bool:
    """Lanza Chrome con --remote-debugging-port, --user-data-dir y --profile-directory.
    Devuelve True si se pudo lanzar y el puerto quedó activo.

    Args:
        chrome_exe: ruta al ejecutable. Si es None, se busca con obtener_chrome_exe().
        log: callback opcional para diagnosticos.
    """
    _log = log or (lambda _: None)
    exe = chrome_exe or obtener_chrome_exe()
    if not exe:
        _log("  ✗ No se encontró chrome.exe.")
        return False

    perfil_path = Path(user_data_dir) / profile_dir
    if not perfil_path.exists():
        _log(f"  ⚠ Directorio de perfil no encontrado: {perfil_path}")
        _log("  → Lanzando sin --profile-directory.")
        profile_dir = None

    # Limpiar archivos de bloqueo que impiden el puerto de debug
    _limpiar_locks(user_data_dir, _log)

    from subprocess import Popen
    args = [
        exe,
        f"--remote-debugging-port={puerto}",
        f"--user-data-dir={user_data_dir}",
        "--restore-last-session",
        "--disable-background-mode",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    if profile_dir:
        args.insert(3, f"--profile-directory={profile_dir}")

    Popen(args)
    import time
    _log("  → Esperando puerto 9222…")
    for i in range(50):  # hasta ~15 segundos
        if puerto_activo("127.0.0.1", puerto):
            _log(f"  ✓ Puerto 9222 activo tras {i * 0.3:.1f}s.")
            return True
        time.sleep(0.3)
    _log("  ✗ Timeout esperando puerto 9222 (15s).")
    return False


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

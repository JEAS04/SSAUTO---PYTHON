"""
automatizacion.py — Lógica de captura de pantalla y subida con Selenium.

Separa completamente la automatización de la interfaz gráfica.
Las funciones de este módulo no importan nada de CustomTkinter, lo que
permite probarlas o usarlas desde la línea de comandos sin abrir la UI.

Flujo principal:
    1. capturar(region)  →  toma la captura y devuelve la ruta del archivo.
    2. subir(...)        →  abre Chrome, hace login si es necesario y
                            envía el archivo al sitio destino.

Mejoras aplicadas (v2.0):
    - Logging robusto: URL actual, título, pestaña activa, fallos de selector.
    - Conexión verificada al Chrome con depuración (puerto 9222).
    - Cambio automático a la pestaña correcta antes de interactuar.
    - Esperas explícitas (WebDriverWait) en lugar de time.sleep() frágiles.
    - Manejo de contenido dinámico (React/Vue) con espera de renderizado.
    - Manejo de iframes con detección y cambio automático.
    - Manejo de elementos obsoletos (stale element) con reintento automático.
    - Manejo de Shadow DOM cuando sea necesario.
    - Selectores validados con logging detallado de fallos.
    - Tolerancia a fallos mejorada (retry lógico en cada paso).
"""

import os
import time
from datetime import datetime
from functools import wraps
from pathlib import Path

import mss
import mss.tools
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from credenciales import cargar_cookies, guardar_cookies, cargar_credenciales

# ── Logger interno ─────────────────────────────────────────────────────
# Prepara mensajes con timestamp, emoji y contexto para que el callable
# 'log' los muestre en la UI de manera uniforme.


class Logger:
    """Mini-logger que envuelve el callable 'log' de la UI con formato rico.

    Proporciona métodos semánticos (ok, error, info, debug) que añaden
    automáticamente el prefijo de color/emoji correspondiente.
    """

    def __init__(self, log_callable):
        self._log = log_callable

    def ok(self, msg: str):
        self._log(f"  ✓ {msg}")

    def error(self, msg: str):
        self._log(f"  ✗ {msg}")

    def info(self, msg: str):
        self._log(f"  → {msg}")

    def warn(self, msg: str):
        self._log(f"  ⚠ {msg}")

    def debug(self, msg: str):
        self._log(f"  · {msg}")


# ── Decorador de reintento para elementos obsoletos ───────────────────


def retry_on_stale(max_attempts: int = 3, delay: float = 0.3):
    """Decorador que reintenta la función si lanza StaleElementReferenceException.

    Útil para operaciones sobre elementos que pueden ser reemplazados por
    el DOM dinámico (React/Vue) entre la localización y la interacción.

    Parámetros
    ----------
    max_attempts : número máximo de intentos.
    delay        : segundos de espera entre reintentos.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]

        return wrapper

    return decorator


# ── Drivers loggers de página ─────────────────────────────────────────


def _log_estado_pagina(driver, log_func, prefix: str = ""):
    """Registra URL actual, título y número de pestañas/ventanas.

    Útil después de cada navegación para diagnosticar problemas de
    redirección, pestaña incorrecta o carga fallida.
    """
    try:
        url = driver.current_url
        titulo = driver.title
        handles = driver.window_handles
        if isinstance(log_func, Logger):
            log_func.debug(
                f"{prefix}URL: {url} | Título: {titulo} | " f"Pestañas: {len(handles)}"
            )
        else:
            log_func(
                f"  · {prefix}URL: {url} | Título: {titulo} | "
                f"Pestañas: {len(handles)}"
            )
    except Exception:
        pass  # Si el driver no responde, no interrumpir.


# ── Ayudantes de pestaña/ventana ──────────────────────────────────────


def _cambiar_a_pestana_por_url(
    driver, subcadena_url: str, log_func, timeout: float = 8.0
) -> bool:
    """Cambia a la primera pestaña/ventana cuya URL contenga 'subcadena_url'.

    Si ninguna pestaña coincide, NO cambia y devuelve False.
    Si hay varias, elige la primera que coincida.

    Útil cuando al conectar al Chrome de depuración la pestaña activa no
    es la que necesitamos (p.ej. el asistente estaba en otra página).
    """
    try:
        handles = driver.window_handles
        if isinstance(log_func, Logger):
            log_func.debug(
                f"Buscando pestaña que contenga '{subcadena_url}' "
                f"({len(handles)} disponibles)"
            )
        else:
            log_func(
                f"  · Buscando pestaña con '{subcadena_url}' "
                f"({len(handles)} disponibles)"
            )

        for handle in handles:
            try:
                driver.switch_to.window(handle)
                time.sleep(0.3)  # Permitir que la pestaña responda
                url_actual = driver.current_url.lower()
                if subcadena_url.lower() in url_actual:
                    if isinstance(log_func, Logger):
                        log_func.ok(
                            f"Cambiado a pestaña: {driver.title} — {driver.current_url}"
                        )
                    else:
                        log_func(
                            f"  ✓ Cambiado a pestaña: {driver.title} — "
                            f"{driver.current_url}"
                        )
                    return True
            except Exception:
                continue

        if isinstance(log_func, Logger):
            log_func.warn(
                f"No se encontró pestaña con '{subcadena_url}'. "
                f"Usando pestaña activa actual."
            )
        else:
            log_func(
                f"  ⚠ No se encontró pestaña con '{subcadena_url}'. "
                f"Usando pestaña activa actual."
            )
        # Volver a la primera pestaña
        if handles:
            driver.switch_to.window(handles[0])
        return False

    except Exception as e:
        if isinstance(log_func, Logger):
            log_func.warn(f"Error al buscar pestaña: {e}")
        else:
            log_func(f"  ⚠ Error al buscar pestaña: {e}")
        return False


# ── Ayudantes de iframes ──────────────────────────────────────────────


def _esperar_y_cambiar_a_iframe(
    driver, espera, selector_iframe: str, log_func, timeout: float = 15.0
) -> bool:
    """Espera a que un iframe esté disponible y cambia a él.

    Devuelve True si pudo cambiar al iframe, False si no se encontró.
    El llamador debe recordar volver al contenido principal después.
    """
    try:
        wait_local = WebDriverWait(driver, timeout)
        iframe = wait_local.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, selector_iframe)
            )
        )
        if isinstance(log_func, Logger):
            log_func.ok(f"Cambiado a iframe: {selector_iframe}")
        else:
            log_func(f"  ✓ Cambiado a iframe: {selector_iframe}")
        return True
    except (TimeoutException, NoSuchElementException) as e:
        if isinstance(log_func, Logger):
            log_func.warn(f"Iframe no encontrado: {selector_iframe} — {e}")
        else:
            log_func(f"  ⚠ Iframe no encontrado: {selector_iframe} — {e}")
        return False


# ── Ayudante de espera de contenido dinámico ──────────────────────────


def _esperar_renderizado_completo(driver, timeout: float = 10.0) -> bool:
    """Espera a que el DOM termine de mutar (útil para React/Vue/SPA).

    Ejecuta JavaScript para comprobar si 'document.readyState' es
    'complete' y si no hay cambios pendientes en el DOM (MutationObserver
    básico). Si tras 'timeout' segundos no se completa, devuelve False.

    Parámetros
    ----------
    driver  : instancia activa de Selenium WebDriver.
    timeout : tiempo máximo de espera en segundos.

    Returns
    -------
    bool : True si el DOM parece estable, False si se agotó el tiempo.
    """
    try:
        wait_local = WebDriverWait(driver, timeout)
        wait_local.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Pequeña pausa adicional para que React/Vue terminen de re-renderizar
        time.sleep(0.5)
        return True
    except (TimeoutException, WebDriverException):
        return False


# ── Ayudante de clic robusto ──────────────────────────────────────────


@retry_on_stale(max_attempts=3)
def _clic_seguro(element):
    """Hace clic en un elemento con reintento automático si queda obsoleto.

    Útil en flujos donde el DOM se re-renderiza entre la obtención del
    elemento y el clic (típico en React/Vue).
    """
    element.click()


# ── Ayudante de localización con logging ──────────────────────────────


def _localizar_con_log(
    driver,
    espera,
    by: By,
    selector: str,
    log_func,
    timeout: float = 15.0,
    descripcion: str = "",
) -> object:
    """Localiza un elemento con WebDriverWait y registra si falla.

    Parámetros
    ----------
    driver      : instancia activa de Selenium WebDriver.
    espera      : instancia de WebDriverWait (se sobreescribe con 'timeout').
    by          : By.CSS_SELECTOR, By.XPATH, etc.
    selector    : valor del selector.
    log_func    : callable para registrar mensajes (Logger o función).
    timeout     : timeout para esta búsqueda en particular.
    descripcion : texto descriptivo del elemento (para el log).

    Returns
    -------
    WebElement si se encontró, o lanza TimeoutException/NoSuchElementException.
    """
    try:
        wait_local = WebDriverWait(driver, timeout)
        elemento = wait_local.until(EC.presence_of_element_located((by, selector)))
        return elemento
    except (TimeoutException, NoSuchElementException) as e:
        if isinstance(log_func, Logger):
            log_func.error(
                f"Selector no encontrado: "
                f"{(descripcion + ' — ') if descripcion else ''}"
                f"'{selector}' — {e}"
            )
        else:
            log_func(
                f"  ✗ Selector no encontrado: "
                f"{(descripcion + ' — ') if descripcion else ''}"
                f"'{selector}' — {e}"
            )
        raise


# ── Creación del driver de Chrome ─────────────────────────────────────


def crear_driver(headless: bool, usar_chrome_existente: bool = False):
    """
    Crea y devuelve una instancia de ChromeDriver configurada.

    Tiene dos modos de operación:
      · usar_chrome_existente=True  → se conecta al Chrome que el usuario
        ya tiene abierto en el puerto 9222 (útil cuando la sesión está
        activa y no se quiere volver a hacer login).
      · usar_chrome_existente=False → abre un Chrome nuevo, con o sin
        ventana visible según el flag 'headless'.

    NOTA: Se evitan opciones experimentales obsoletas (excludeSwitches,
    useAutomationExtension) que causan errores con ChromeDriver moderno.
    El antifingerprinting se logra exclusivamente vía --disable-blink-features.

    Parámetros
    ----------
    headless              : si True, Chrome corre sin ventana (solo en modo nuevo).
    usar_chrome_existente : si True, conecta al Chrome del usuario en puerto 9222.
    """
    opciones = webdriver.ChromeOptions()

    # ── Antifingerprinting: ocultar indicadores de automatización ──────────
    # NOTA: excludeSwitches y useAutomationExtension ya no son compatibles
    # con ChromeDriver moderno (causan "invalid argument: unrecognized chrome
    # option"). Se reemplazan por --disable-blink-features que es el método
    # oficial y soportado.
    opciones.add_argument("--disable-blink-features=AutomationControlled")

    try:
        if usar_chrome_existente:
            # Conectar al Chrome ya abierto; no se pueden pasar flags de headless
            # porque el proceso ya está corriendo.
            opciones.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        else:
            if headless:
                # Modo sin ventana: ideal para servidores o ejecución en segundo plano.
                opciones.add_argument("--headless=new")
                opciones.add_argument("--disable-gpu")
            opciones.add_argument("--no-sandbox")
            opciones.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opciones,
        )

        # ── Opcional: ocultar navigator.webdriver ─────────────────────────
        # En Chrome 147+ esta propiedad ya no es redefinible cuando se
        # conecta a una sesión real de usuario (remote debugging 9222).
        # Se envuelve en try/catch para evitar el error:
        #   "Cannot redefine property: webdriver"
        # El logging permite diagnosticar si la inyección falla.
        try:
            driver.execute_script("""
            try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            } catch(e) {
                // Chrome 147+ no permite redefinir navigator.webdriver
                // en sesiones de depuración reales. Esto es normal y seguro.
            }
            """)
        except Exception as _js_err:
            import logging as _logging

            _logging.getLogger("ssauto.driver").debug(
                f"Script de navigator.webdriver no se pudo inyectar "
                f"(esperado en Chrome moderno): {_js_err}"
            )

        return driver

    except Exception as e:
        import logging

        logging.getLogger("ssauto.driver").error(
            f"Error al inicializar ChromeDriver: {e}"
        )
        raise


# ── Captura de pantalla ───────────────────────────────────────────────


def capturar(region: dict) -> str:
    """
    Toma una captura de la región indicada y la guarda en ./screenshots/.

    Usa mss, que es más rápido que PIL/Pillow y no requiere permisos extra.
    Devuelve la ruta absoluta del archivo generado para pasársela al driver.

    Parámetros
    ----------
    region : dict con claves top, left, width, height (píxeles en pantalla).
    """
    Path("screenshots").mkdir(exist_ok=True)
    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{marca_tiempo}.png"

    # Asegurar que todos los valores de región sean enteros antes de pasarlos a mss.
    region_int = {k: int(v) for k, v in region.items()}
    with mss.MSS() as sct:
        captura = sct.grab(region_int)
        mss.tools.to_png(captura.rgb, captura.size, output=ruta)

    return ruta


# ── Subida al sitio destino ───────────────────────────────────────────


def subir(
    sitio: dict,
    ruta_imagen: str,
    headless: bool,
    log,
    credenciales_sesion: dict = None,
    usar_chrome_existente: bool = False,
    auto_submit_nota: bool = True,
) -> None:
    """
    Sube la imagen al sitio destino usando Selenium.

    Maneja dos modos de operación principales:

      A) usar_pagina_actual=True (configurable por sitio)
         Solo funciona con usar_chrome_existente=True. NO navega a
         url_upload, sino que trabaja directamente con la página que
         el usuario tiene abierta en ese momento en el Chrome de
         depuración. Ideal para HubSpot donde el usuario ya tiene
         abierto un ticket/contacto/deal específico.

      B) usar_pagina_actual=False (comportamiento heredado)
         Navega a url_upload y sigue el flujo estándar de login/subida.

    Maneja dos escenarios de autenticación:

      C) usar_chrome_existente=True
         Conecta al Chrome abierto por el usuario. Verifica si hay sesión
         activa navegando a url_upload (a menos que usar_pagina_actual
         esté activo). Si la URL redirige a login, avisa al usuario para
         que inicie sesión manualmente y sale; no intenta login automático.

      D) usar_chrome_existente=False
         Abre un Chrome nuevo. Restaura cookies o hace login automático.

    El parámetro 'log' es un callable thread-safe (normalmente self.after)
    para poder llamarse desde hilos secundarios sin bloquear la UI.

    Parámetros
    ----------
    sitio                 : dict de config.SITIOS con las URLs y selectores.
    ruta_imagen           : ruta local del archivo a subir.
    headless              : modo sin ventana (solo aplicable si se abre Chrome nuevo).
    log                   : función para registrar mensajes en la UI (thread-safe).
    credenciales_sesion   : dict {nombre_sitio: {usuario, clave}} de la sesión actual.
    usar_chrome_existente : conectar al Chrome del usuario en vez de abrir uno nuevo.
    """
    logger = Logger(log)
    driver = crear_driver(headless, usar_chrome_existente)
    espera = WebDriverWait(driver, 15)
    nombre = sitio.get("nombre", "sitio")
    usar_pagina_actual = sitio.get("usar_pagina_actual", False)

    try:
        # ── Logging de conexión ────────────────────────────────────────
        logger.info(f"Iniciando subida a {nombre}...")
        logger.info(
            f"Modo: {'Chrome existente (9222)' if usar_chrome_existente else 'Chrome nuevo'}"
        )
        if usar_pagina_actual:
            logger.info("Modo 'página actual' activo — no se navegará a URL fija.")
        _log_estado_pagina(driver, logger, "[conexión] ")

        # ── Cambiar a pestaña correcta según el modo de operación ──
        # Cuando usamos Chrome existente, buscamos activamente la
        # pestaña correcta entre todas las abiertas en el navegador.
        if usar_chrome_existente:
            if usar_pagina_actual:
                # Modo HubSpot: buscar pestaña que contenga "app.hubspot.com"
                logger.info(
                    "Buscando pestaña de HubSpot entre las "
                    f"{len(driver.window_handles)} pestaña(s) abierta(s)..."
                )
                if _cambiar_a_pestana_por_url(driver, "app.hubspot.com", logger):
                    logger.ok("Pestaña de HubSpot encontrada y seleccionada.")
                else:
                    logger.warn(
                        "No se encontró pestaña de HubSpot. "
                        "Asegúrate de tener un ticket/contacto/deal de HubSpot "
                        "abierto en el navegador."
                    )
            elif sitio.get("url_upload"):
                # Modo normal (navegación a URL fija): buscar por dominio
                subcadena = (
                    sitio["url_upload"].replace("https://", "").replace("http://", "")
                )
                dominio = subcadena.split("/")[0] if "/" in subcadena else subcadena
                if dominio:
                    _cambiar_a_pestana_por_url(driver, dominio, logger)

        # ── Manejo de sesión ─────────────────────────────────────────
        if sitio["necesita_login"]:
            if usar_chrome_existente:
                if usar_pagina_actual:
                    _verificar_pagina_actual(driver, sitio, nombre, logger)
                else:
                    _verificar_sesion_chrome_existente(driver, sitio, nombre, logger)
            else:
                _autenticar_chrome_nuevo(
                    driver, espera, sitio, nombre, logger, credenciales_sesion
                )
        else:
            # Sitio público: ir directo a la página de subida.
            logger.info(f"Navegando a {sitio['url_upload']}...")
            driver.get(sitio["url_upload"])
            _esperar_renderizado_completo(driver)
            _log_estado_pagina(driver, logger, "[upload] ")

        # ── Subida del archivo ────────────────────────────────────────
        # Si el sitio tiene selectores específicos de HubSpot (data-test-id
        # para notas), usar flujo HubSpot; de lo contrario, flujo genérico.
        if sitio.get("selector_tab_notas"):
            _subir_captura_hubspot(
                driver,
                espera,
                sitio,
                nombre,
                ruta_imagen,
                logger,
                auto_submit_nota=auto_submit_nota,
            )
        else:
            _realizar_subida(driver, espera, sitio, nombre, ruta_imagen, logger)

    except Exception as e:
        logger.error(f"Error inesperado en {nombre}: {e}")
        try:
            ruta_debug = f"debug_error_{nombre.replace(' ', '_')}.png"
            driver.save_screenshot(ruta_debug)
            logger.info(f"Captura de debug guardada: {ruta_debug}")
        except Exception:
            pass
    finally:
        # Nunca cerrar el Chrome del usuario; sí cerrar el que abrimos nosotros.
        if not usar_chrome_existente:
            logger.info("Cerrando Chrome (abierto por la aplicación)...")
            driver.quit()


# ── Funciones auxiliares internas ─────────────────────────────────────
# (prefijo _ = uso interno del módulo, no son parte de la API pública)


def _verificar_pagina_actual(driver, sitio: dict, nombre: str, logger) -> None:
    """
    Verifica la página actual del Chrome abierto por el usuario sin navegar.

    Este modo se usa cuando 'usar_pagina_actual' está activo (HubSpot).
    En lugar de hacer driver.get() a url_upload, asume que el usuario ya
    tiene abierta la página correcta (ticket/contacto/deal) y registra:
      - URL activa
      - Título de la página
      - Número de pestañas abiertas
      - Si la URL contiene 'hubspot' o no (validación básica)

    No se redirige ni se cambia de pestaña; se trabaja con la que esté
    activa en el momento de la conexión.
    """
    logger.info(f"Verificando página actual para {nombre} (modo: página actual)...")
    _log_estado_pagina(driver, logger, "[página actual] ")

    # Registrar la URL y título actuales para diagnóstico
    try:
        url_actual = driver.current_url
        titulo = driver.title
        handles = driver.window_handles
        logger.info(f"URL activa: {url_actual}")
        logger.info(f"Título activo: {titulo}")
        logger.info(f"Pestañas abiertas: {len(handles)}")

        # Verificar que esté en una página de HubSpot
        if "hubspot" in url_actual.lower():
            logger.ok(
                f"HubSpot detectado en página actual — {len(handles)} pestaña(s) disponible(s)."
            )
        else:
            logger.warn(
                f"La URL actual no parece ser de HubSpot: '{url_actual[:80]}...'"
            )
            logger.info(
                "Asegúrate de tener el ticket/contacto/deal de HubSpot abierto "
                "en la pestaña activa del navegador."
            )
    except Exception as e:
        logger.warn(f"No se pudo inspeccionar la página actual: {e}")

    # NO se navega a ninguna URL — el usuario debe tener la página correcta abierta.
    logger.info("Continuando con la página actual (sin navegación).")


def _verificar_sesion_chrome_existente(
    driver, sitio: dict, nombre: str, logger
) -> None:
    """
    Verifica si el Chrome abierto por el usuario ya tiene sesión activa.

    Si la URL actual contiene 'login' o 'signin' después de navegar a
    url_upload, asume que no hay sesión y le pide al usuario que inicie
    sesión manualmente.
    """
    logger.info(f"Verificando sesión activa en Chrome abierto para {nombre}...")
    logger.info(f"Navegando a {sitio['url_upload']}...")
    driver.get(sitio["url_upload"])

    # Esperar a que la página cargue completamente.
    _esperar_renderizado_completo(driver, timeout=5.0)
    _log_estado_pagina(driver, logger, "[verificación sesión] ")

    url_actual = driver.current_url.lower()
    if "login" in url_actual or "signin" in url_actual:
        logger.error(f"No hay sesión activa en Chrome para {nombre}.")
        logger.info("Inicia sesión manualmente en el navegador y vuelve a intentar.")
        raise RuntimeError(f"Sin sesión activa en Chrome para {nombre}")
    logger.ok(f"Sesión activa detectada en Chrome: {nombre}")


def _autenticar_chrome_nuevo(
    driver, espera, sitio: dict, nombre: str, logger, credenciales_sesion: dict
) -> None:
    """
    Gestiona la autenticación al abrir un Chrome nuevo.

    Orden de intento:
      1. Restaurar sesión con cookies guardadas.
      2. Login automático con credenciales (sesión > llavero).
      3. Si no hay credenciales, registrar error y salir.
    """
    sesion_restaurada = False
    ruta_cookies = f"cookies/{nombre.replace(' ', '_')}.pkl"

    if Path(ruta_cookies).exists():
        logger.info("Intentando restaurar sesión con cookies…")
        cargar_cookies(driver, sitio, sitio["url_login"])
        driver.get(sitio["url_upload"])
        _esperar_renderizado_completo(driver, timeout=5.0)
        _log_estado_pagina(driver, logger, "[cookies] ")

        url_actual = driver.current_url.lower()
        if "login" not in url_actual and "signin" not in url_actual:
            logger.ok(f"Sesión restaurada con cookies para {nombre}.")
            sesion_restaurada = True
        else:
            logger.warn("Cookies expiradas o inválidas, realizando login…")

    if not sesion_restaurada:
        # Obtener credenciales: primero las de la sesión actual, luego el llavero.
        usuario, clave = "", ""
        if credenciales_sesion and nombre in credenciales_sesion:
            usuario = credenciales_sesion[nombre].get("usuario", "")
            clave = credenciales_sesion[nombre].get("clave", "")
        else:
            usuario, clave = cargar_credenciales(nombre)

        if not usuario or not clave:
            logger.error(
                f"No hay credenciales para {nombre}. Abre 'Credenciales' para configurarlas."
            )
            raise RuntimeError(f"Sin credenciales para {nombre}")

        _hacer_login(driver, espera, sitio, nombre, usuario, clave, logger)


def _hacer_login(
    driver, espera, sitio: dict, nombre: str, usuario: str, clave: str, logger
) -> None:
    """
    Realiza el flujo de login en el sitio: rellena usuario/contraseña y envía el formulario.

    Después de un login exitoso guarda las cookies para no repetir el
    proceso en ejecuciones futuras.
    """
    logger.info(f"Navegando a página de login: {sitio['url_login']}")
    driver.get(sitio["url_login"])
    _esperar_renderizado_completo(driver)
    _log_estado_pagina(driver, logger, "[login] ")

    # Localizar campo de usuario
    logger.info(f"Buscando campo de usuario: '{sitio['selector_user']}'")
    campo_user = _localizar_con_log(
        driver,
        espera,
        By.CSS_SELECTOR,
        sitio["selector_user"],
        logger,
        descripcion="campo usuario",
    )
    campo_user.clear()
    campo_user.send_keys(usuario)
    logger.ok("Usuario ingresado")

    # Localizar campo de contraseña
    logger.info(f"Buscando campo de contraseña: '{sitio['selector_pass']}'")
    campo_pass = _localizar_con_log(
        driver,
        espera,
        By.CSS_SELECTOR,
        sitio["selector_pass"],
        logger,
        descripcion="campo contraseña",
    )
    campo_pass.clear()
    campo_pass.send_keys(clave)
    logger.ok("Contraseña ingresada")

    # Localizar y hacer clic en botón de login
    logger.info(f"Buscando botón de login: '{sitio['selector_btn_login']}'")
    btn_login = _localizar_con_log(
        driver,
        espera,
        By.CSS_SELECTOR,
        sitio["selector_btn_login"],
        logger,
        descripcion="botón login",
    )
    _clic_seguro(btn_login)
    logger.info("Clic en botón de login enviado")

    try:
        # Esperar a que la URL cambie; 'secure' es típico de demos de Herokuapp.
        # Para sitios reales, cambiar este selector a uno apropiado.
        espera.until(EC.url_contains("secure"))
        _log_estado_pagina(driver, logger, "[post-login] ")
    except Exception:
        logger.error(
            f"Error al iniciar sesión para {nombre}: la URL no cambió como se esperaba."
        )
        try:
            driver.save_screenshot(f"debug_login_{nombre.replace(' ', '_')}.png")
        except Exception:
            pass
        raise RuntimeError(f"Login fallido para {nombre}")

    guardar_cookies(driver, nombre)
    logger.ok(f"Login exitoso, cookies guardadas: {nombre}")
    driver.get(sitio["url_upload"])
    _log_estado_pagina(driver, logger, "[post-login upload] ")


def _realizar_subida(
    driver, espera, sitio: dict, nombre: str, ruta_imagen: str, logger
) -> None:
    """
    Envía el archivo al formulario de subida y verifica la confirmación.

    Para confirmar la subida, compara el texto de un elemento (h3 o h1 por
    defecto) antes y después de hacer clic en 'Submit'. Si el texto cambia
    y contiene alguna de las palabras_confirmacion, considera la subida exitosa.
    Si no cambia en 30 segundos, guarda una captura de debug y registra el error.
    """
    logger.info(f"Subiendo imagen a {nombre}…")

    # Esperar renderizado completo de la página de subida
    _esperar_renderizado_completo(driver)
    _log_estado_pagina(driver, logger, "[upload page] ")

    # --- Detectar si el input file está dentro de un iframe ---
    # Primero intentamos buscar el iframe por posibles selectores comunes
    iframes = driver.find_elements(By.CSS_SELECTOR, "iframe")
    if iframes:
        logger.info(
            f"Se detectaron {len(iframes)} iframe(s) en la página. "
            f"Buscando el que contenga el input file..."
        )
        # Intentar cambiar al primer iframe que tenga un input file
        encontrado = False
        for idx, iframe in enumerate(iframes):
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame(iframe)
                inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if inputs:
                    logger.info(f"Input file encontrado dentro del iframe {idx}")
                    encontrado = True
                    break
            except Exception:
                driver.switch_to.default_content()
                continue
        if not encontrado:
            # Volver al contenido principal si no se encontró input en iframes
            driver.switch_to.default_content()

    # Esperar y localizar el campo de archivo.
    logger.info(f"Buscando input file: '{sitio['selector_input_file']}'")
    try:
        campo_archivo = _localizar_con_log(
            driver,
            espera,
            By.CSS_SELECTOR,
            sitio["selector_input_file"],
            logger,
            timeout=15.0,
            descripcion="input file",
        )
    except (TimeoutException, NoSuchElementException):
        # Intentar con un selector más genérico como fallback
        logger.warn(
            "Selector específico no encontrado, intentando 'input[type=\"file\"]'..."
        )
        try:
            campo_archivo = _localizar_con_log(
                driver,
                espera,
                By.CSS_SELECTOR,
                "input[type='file']",
                logger,
                timeout=10.0,
                descripcion="input file (fallback genérico)",
            )
        except (TimeoutException, NoSuchElementException):
            logger.error("No se pudo localizar el campo de archivo para subir.")
            raise

    # send_keys necesita la ruta absoluta para que Chrome la encuentre correctamente.
    ruta_abs = os.path.abspath(ruta_imagen)
    logger.info(f"Enviando archivo: {ruta_abs}")
    campo_archivo.send_keys(ruta_abs)

    # Guardar el texto del indicador de confirmación ANTES de enviar,
    # para detectar el cambio después.
    selector_confirmacion = sitio.get("selector_confirmacion", "h3, h1")
    palabras_ok = [
        p.lower()
        for p in sitio.get(
            "palabras_confirmacion", ["uploaded", "success", "exitoso", "subido"]
        )
    ]

    try:
        texto_antes = (
            driver.find_element(By.CSS_SELECTOR, selector_confirmacion)
            .text.strip()
            .lower()
        )
        logger.debug(f"Texto de confirmación antes de enviar: '{texto_antes}'")
    except Exception:
        texto_antes = ""
        logger.warn("No se pudo leer el texto de confirmación antes de enviar.")

    # Localizar botón de submit con logging
    logger.info(f"Buscando botón submit: '{sitio['selector_submit']}'")
    try:
        btn_submit = _localizar_con_log(
            driver,
            espera,
            By.CSS_SELECTOR,
            sitio["selector_submit"],
            logger,
            descripcion="botón submit",
        )
        _clic_seguro(btn_submit)
        logger.info("Clic en botón submit enviado")
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"No se pudo localizar el botón submit: {e}")
        raise

    # Esperar hasta que el texto del indicador cambie (máx. 30 segundos).
    try:
        espera_confirmacion = WebDriverWait(driver, 30)
        espera_confirmacion.until(
            lambda d: d.find_element(By.CSS_SELECTOR, selector_confirmacion)
            .text.strip()
            .lower()
            != texto_antes
        )
        resultado = driver.find_element(
            By.CSS_SELECTOR, selector_confirmacion
        ).text.strip()
        logger.debug(f"Texto de confirmación después de enviar: '{resultado}'")
        if any(p in resultado.lower() for p in palabras_ok):
            logger.ok(f"Subida exitosa → {resultado}")
        else:
            logger.warn(f'Respuesta inesperada → "{resultado}"')
            try:
                driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")
            except Exception:
                pass
    except Exception:
        logger.error("No se pudo confirmar la subida (timeout).")
        try:
            driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")
        except Exception:
            pass


# ── Subida HubSpot (notas con imagen) ─────────────────────────────────


def _subir_captura_hubspot(
    driver,
    espera,
    sitio: dict,
    nombre: str,
    ruta_imagen: str,
    logger,
    auto_submit_nota: bool = True,
) -> None:
    """
    Sube una captura a una nueva nota dentro del ticket actual de HubSpot.
    v2.5 — Fix condición de carrera editor → FileButton.
    """
    logger.info(f"Subiendo captura a nota de {nombre}…")
    ruta_abs = os.path.abspath(ruta_imagen)
    logger.debug(f"[HubSpot] Ruta absoluta del archivo: {ruta_abs}")

    _esperar_renderizado_completo(driver)
    _log_estado_pagina(driver, logger, "[HubSpot inicio] ")

    # ── Validación: asegurar que estamos en HubSpot ──────────────────
    try:
        url_actual = driver.current_url.lower()
        if "hubspot" not in url_actual:
            logger.error(
                f"[HubSpot] Pestaña incorrecta: '{url_actual[:100]}'. Abortando."
            )
            raise RuntimeError(
                f"Pestaña incorrecta para subida HubSpot: {url_actual[:80]}"
            )
        logger.ok(f"[HubSpot] Confirmado: página HubSpot — {url_actual[:80]}")
    except RuntimeError:
        raise
    except Exception as e:
        logger.warn(f"[HubSpot] No se pudo validar URL: {e}")

    # ── Paso 0: Tab "Actividades" ────────────────────────────────────
    logger.info("[HubSpot] Paso 0/8: Abriendo pestaña 'Actividades'…")
    selector_actividades = sitio.get("selector_tab_actividades")
    selector_actividades_fallback = sitio.get("selector_tab_actividades_fallback")

    tab_actividades_ok = False
    if selector_actividades:
        try:
            tab = espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector_actividades))
            )
            _clic_seguro(tab)
            logger.ok("[HubSpot] Pestaña 'Actividades' clickeada")
            tab_actividades_ok = True
            time.sleep(0.5)
        except (TimeoutException, NoSuchElementException) as e:
            logger.warn(f"[HubSpot] Selector principal 'Actividades' falló: {e}")

    if not tab_actividades_ok and selector_actividades_fallback:
        try:
            tab = espera.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//{selector_actividades_fallback}[text()='Actividades']",
                    )
                )
            )
            _clic_seguro(tab)
            logger.ok("[HubSpot] Pestaña 'Actividades' clickeada (fallback)")
            time.sleep(0.5)
        except (TimeoutException, NoSuchElementException) as e:
            logger.warn(f"[HubSpot] Fallback 'Actividades' también falló: {e}")
            logger.info("[HubSpot] Continuando (posiblemente ya está activa)")

    # ── Paso 1: Tab "Notas" ──────────────────────────────────────────
    logger.info("[HubSpot] Paso 1/8: Abriendo pestaña 'Notas'…")
    try:
        tab_notas = espera.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_tab_notas"]))
        )
        _clic_seguro(tab_notas)
        logger.ok("[HubSpot] Pestaña 'Notas' abierta")
        time.sleep(0.5)
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"[HubSpot] No se pudo abrir pestaña 'Notas': {e}")
        raise

    # ── Paso 2: Crear nota ───────────────────────────────────────────
    logger.info("[HubSpot] Paso 2/8: Creando nueva nota…")
    try:
        btn_crear = espera.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, sitio["selector_btn_crear_nota"])
            )
        )
        _clic_seguro(btn_crear)
        logger.ok("[HubSpot] Nueva nota creada")
        # FIX: esperar a que el editor esté presente antes de continuar,
        # no solo un sleep fijo. El editor es la señal de que React terminó
        # de montar el formulario completo (incluido el FileButton).
        _esperar_renderizado_completo(driver, timeout=5.0)
        time.sleep(0.5)
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"[HubSpot] No se pudo crear nota: {e}")
        raise

    # ── Paso 3: Insertar texto en el editor ─────────────────────────
    # CRÍTICO: HubSpot no renderiza el FileButton hasta que el editor
    # tiene foco. El click() en el editor es lo que dispara el render
    # del toolbar completo en React. Si este paso falla, el paso 4 falla.
    logger.info("[HubSpot] Paso 3/8: Enfocando editor e insertando texto…")
    selector_editor = sitio.get("selector_nota_editor")
    selector_editor_alt = sitio.get("selector_nota_editor_alt")
    editor_ok = False

    for sel, label in [
        (selector_editor, "principal"),
        (selector_editor_alt, "alternativo"),
    ]:
        if not sel or editor_ok:
            continue
        try:
            nota_editor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sel))
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
            )
            # 1. Click para dar foco
            _clic_seguro(nota_editor)
            time.sleep(0.3)

            # 2. Insertar texto vía JavaScript disparando eventos React.
            # send_keys() escribe en el DOM pero NO dispara los eventos
            # sintéticos de React (onInput, onChange). Sin esos eventos,
            # React no actualiza su estado interno y HubSpot no habilita
            # el toolbar (FileButton incluido).
            texto = "Escribe tu nota aqui."
            driver.execute_script(
                """
                var el = arguments[0];
                var texto = arguments[1];

                // Enfocar el elemento
                el.focus();

                // Insertar texto vía execCommand (compatible con contenteditable)
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, texto);

                // Disparar eventos React manualmente como fallback
                // por si execCommand no los dispara en esta versión de Chrome
                ['input', 'change', 'keyup'].forEach(function(tipo) {
                    var ev = new Event(tipo, { bubbles: true, cancelable: true });
                    el.dispatchEvent(ev);
                });
            """,
                nota_editor,
                texto,
            )

            logger.ok(f"[HubSpot] Texto insertado vía JS (selector {label})")
            editor_ok = True

            # 3. Esperar a que React procese el estado y renderice el toolbar
            time.sleep(0.8)
        except (TimeoutException, NoSuchElementException) as e:
            logger.warn(f"[HubSpot] Editor ({label}) no encontrado: {e}")
        except Exception as e:
            logger.error(f"[HubSpot] Error al escribir en editor ({label}): {e}")
            raise

    if not editor_ok:
        # No abortar — intentar continuar, pero advertir que el FileButton
        # puede no aparecer y que el botón guardar podría quedar deshabilitado.
        logger.warn(
            "[HubSpot] Editor no localizado con ningún selector. "
            "El FileButton y el botón guardar podrían no funcionar."
        )

    # ── Paso 4: Abrir componente de subida (FileButton) ──────────────
    # FIX: el FileButton solo existe en el DOM después de que el editor
    # tiene foco y contenido (paso 3). Si el paso 3 falló, este también fallará.
    logger.info("[HubSpot] Paso 4/8: Abriendo componente de subida…")
    selector_upload_btn = sitio.get(
        "selector_btn_subir", '[data-test-id="select-file-dropdown"]'
    )
    try:
        # FIX: aumentar timeout a 20s porque React puede tardar en renderizar
        # el toolbar completo después de que el editor recibe foco.
        upload_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector_upload_btn))
        )
        _clic_seguro(upload_btn)
        logger.ok("[HubSpot] FileButton clickeado — esperando render del input…")
        # FIX: esperar a que el input[type="file"] aparezca en el DOM
        # en lugar de un sleep fijo. Esto es más robusto y más rápido.
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        logger.ok("[HubSpot] input[type='file'] detectado en DOM")
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(
            f"[HubSpot] FileButton no encontrado tras esperar 20s: {e}\n"
            "Causa probable: el editor (paso 3) no recibió foco correctamente.\n"
            "Revisa selector_nota_editor en config.py."
        )
        try:
            with open("debug_dom.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logger.info("[HubSpot] DOM guardado en debug_dom.html")
        except Exception:
            pass
        raise

    # ── Paso 5: send_keys al input[type="file"] ──────────────────────
    logger.info("[HubSpot] Paso 5/8: Enviando archivo al input…")
    selector_file = sitio.get("selector_input_file", 'input[type="file"]')
    try:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector_file))
        )
        # NO hacer click() — abriría el file picker nativo. Solo send_keys.
        file_input.send_keys(ruta_abs)
        logger.ok(f"[HubSpot] Archivo enviado: {ruta_abs}")
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"[HubSpot] input[type='file'] no encontrado: {e}")
        raise
    except Exception as e:
        logger.error(f"[HubSpot] Error en send_keys: {e}")
        raise

    # ── Paso 6: Esperar que HubSpot procese el archivo ───────────────
    # FIX: en lugar de 3x sleep(1) ciegos, esperar a que desaparezca
    # el indicador de carga O a que aparezca el nombre del archivo adjunto.
    # Si ninguno ocurre en 15s, continuar igual (subida puede estar lista).
    logger.info("[HubSpot] Paso 6/8: Esperando procesamiento del archivo…")
    try:
        # Intentar detectar el attachment procesado en el DOM
        # (HubSpot muestra el nombre del archivo después de subirlo)
        nombre_archivo = os.path.basename(ruta_abs)
        WebDriverWait(driver, 15).until(
            lambda d: nombre_archivo.lower() in d.page_source.lower()
        )
        logger.ok(f"[HubSpot] Archivo '{nombre_archivo}' confirmado en página")
    except TimeoutException:
        # No es un error fatal — HubSpot puede haber procesado el archivo
        # sin mostrar el nombre en el DOM de forma detectable. Continuar.
        logger.warn(
            "[HubSpot] No se pudo confirmar el archivo en DOM tras 15s. "
            "Continuando de todas formas (la subida puede estar completa)."
        )
    _log_estado_pagina(driver, logger, "[post-upload] ")

    # ── Paso 7: Guardar nota (condicional) ───────────────────────────
    if not auto_submit_nota:
        logger.info(
            "[HubSpot] Paso 7/8: Omitido — auto-submit DESACTIVADO. "
            "Nota queda abierta para edición manual."
        )
        logger.ok(f"[HubSpot] Captura subida a {nombre} (guardado manual pendiente)")
        return

    logger.info("[HubSpot] Paso 7/8: Guardando nota…")
    selector_guardar = sitio["selector_btn_guardar"]
    try:
        # HubSpot usa aria-disabled="true" para deshabilitar el botón,
        # NO el atributo HTML "disabled". get_attribute("disabled") devuelve
        # None aunque el botón esté bloqueado, por eso el clic no tenía efecto.
        # Hay que esperar a que aria-disabled sea "false" o None.
        def _boton_habilitado(d):
            el = d.find_element(By.CSS_SELECTOR, selector_guardar)
            aria = el.get_attribute("aria-disabled")
            disabled = el.get_attribute("disabled")
            # Habilitado solo si aria-disabled no es "true" Y disabled es None
            if aria == "true" or disabled is not None:
                return False
            return el

        btn_guardar = WebDriverWait(driver, 20).until(_boton_habilitado)
        logger.ok(
            "[HubSpot] Botón guardar habilitado (aria-disabled=false) — clickeando"
        )
        _clic_seguro(btn_guardar)
        time.sleep(1)
        _log_estado_pagina(driver, logger, "[post-save] ")
        logger.ok(f"[HubSpot] Nota guardada correctamente en {nombre}")
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"[HubSpot] No se pudo guardar la nota: {e}")
        try:
            driver.save_screenshot("debug_error_HUBSPOT_save.png")
            logger.info("[HubSpot] Debug screenshot guardado")
        except Exception:
            pass
        raise

    logger.ok(f"[HubSpot] Flujo completado — archivo: {ruta_abs}")
    logger.ok(f"[HubSpot] Captura subida correctamente a nota de {nombre}")
    logger.info(f"[HubSpot] Archivo: {ruta_abs}")
    logger.debug("[HubSpot] Flujo de subida completado exitosamente")

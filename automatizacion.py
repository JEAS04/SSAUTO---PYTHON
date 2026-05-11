"""
automatizacion.py — Lógica de captura de pantalla y subida con Selenium.

Separa completamente la automatización de la interfaz gráfica.
Las funciones de este módulo no importan nada de CustomTkinter, lo que
permite probarlas o usarlas desde la línea de comandos sin abrir la UI.

Flujo principal:
    1. capturar(region)  →  toma la captura y devuelve la ruta del archivo.
    2. subir(...)        →  abre Chrome, hace login si es necesario y
                            envía el archivo al sitio destino.
"""

import os
import time
from datetime import datetime
from pathlib import Path

import mss
import mss.tools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from credenciales import cargar_cookies, guardar_cookies, cargar_credenciales

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

    En ambos casos se disfrazan las huellas de automatización para reducir
    la probabilidad de que el sitio detecte que es un bot.

    Parámetros
    ----------
    headless              : si True, Chrome corre sin ventana (solo en modo nuevo).
    usar_chrome_existente : si True, conecta al Chrome del usuario en puerto 9222.
    """
    opciones = webdriver.ChromeOptions()

    # Ocultar indicadores de automatización que algunos sitios detectan.
    opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
    opciones.add_experimental_option("useAutomationExtension", False)
    opciones.add_argument("--disable-blink-features=AutomationControlled")

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

    # Eliminar la propiedad navigator.webdriver que delata la automatización.
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
    )

    return driver


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

    with mss.MSS() as sct:
        captura = sct.grab(region)
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
) -> None:
    """
    Sube la imagen al sitio destino usando Selenium.

    Maneja dos escenarios de autenticación:

      A) usar_chrome_existente=True
         Conecta al Chrome abierto por el usuario. Verifica si hay sesión
         activa navegando a url_upload. Si la URL redirige a login, avisa
         al usuario para que inicie sesión manualmente y sale; no intenta
         login automático para no interferir con la sesión del usuario.

      B) usar_chrome_existente=False
         Abre un Chrome nuevo. Primero intenta restaurar la sesión con las
         cookies guardadas. Si las cookies expiaron o no existen, hace login
         automático con las credenciales del llavero (o las de la sesión
         actual) y guarda las cookies nuevas para la próxima vez.

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
    driver = crear_driver(headless, usar_chrome_existente)
    espera = WebDriverWait(driver, 15)
    nombre = sitio.get("nombre", "sitio")

    try:
        # ── Manejo de sesión ─────────────────────────────────────────
        if sitio["necesita_login"]:
            if usar_chrome_existente:
                _verificar_sesion_chrome_existente(driver, sitio, nombre, log)
            else:
                _autenticar_chrome_nuevo(
                    driver, espera, sitio, nombre, log, credenciales_sesion
                )
        else:
            # Sitio público: ir directo a la página de subida.
            driver.get(sitio["url_upload"])

        # ── Subida del archivo ────────────────────────────────────────
        # Si el sitio tiene selectores específicos de HubSpot (data-test-id
        # para notas), usar flujo HubSpot; de lo contrario, flujo genérico.
        if sitio.get("selector_tab_notas"):
            _subir_captura_hubspot(driver, espera, sitio, nombre, ruta_imagen, log)
        else:
            _realizar_subida(driver, espera, sitio, nombre, ruta_imagen, log)

    except Exception as e:
        log(f"  ✗ Error inesperado en {nombre}: {e}")
        try:
            driver.save_screenshot(f"debug_error_{nombre.replace(' ', '_')}.png")
        except Exception:
            pass
    finally:
        # Nunca cerrar el Chrome del usuario; sí cerrar el que abrimos nosotros.
        if not usar_chrome_existente:
            driver.quit()


# ── Funciones auxiliares internas ─────────────────────────────────────
# (prefijo _ = uso interno del módulo, no son parte de la API pública)


def _verificar_sesion_chrome_existente(driver, sitio: dict, nombre: str, log) -> None:
    """
    Verifica si el Chrome abierto por el usuario ya tiene sesión activa.

    Si la URL actual contiene 'login' o 'signin' después de navegar a
    url_upload, asume que no hay sesión y le pide al usuario que inicie
    sesión manualmente.
    """
    log(f"  → Verificando sesión activa en Chrome abierto para {nombre}...")
    driver.get(sitio["url_upload"])
    time.sleep(1.5)  # Pausa para que el sitio redirija si no hay sesión.
    url_actual = driver.current_url.lower()
    if "login" in url_actual or "signin" in url_actual:
        log(f"  ✗ No hay sesión activa en Chrome para {nombre}.")
        log(f"  → Inicia sesión manualmente en el navegador y vuelve a intentar.")
        raise RuntimeError(f"Sin sesión activa en Chrome para {nombre}")
    log(f"  ✓ Sesión activa detectada en Chrome: {nombre}")


def _autenticar_chrome_nuevo(
    driver, espera, sitio: dict, nombre: str, log, credenciales_sesion: dict
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
        log(f"  → Intentando restaurar sesión con cookies…")
        cargar_cookies(driver, sitio, sitio["url_login"])
        driver.get(sitio["url_upload"])
        time.sleep(1.5)
        url_actual = driver.current_url.lower()
        if "login" not in url_actual and "signin" not in url_actual:
            log(f"  ✓ Sesión restaurada con cookies para {nombre}.")
            sesion_restaurada = True
        else:
            log(f"  ✗ Cookies expiradas o inválidas, realizando login…")

    if not sesion_restaurada:
        # Obtener credenciales: primero las de la sesión actual, luego el llavero.
        usuario, clave = "", ""
        if credenciales_sesion and nombre in credenciales_sesion:
            usuario = credenciales_sesion[nombre].get("usuario", "")
            clave = credenciales_sesion[nombre].get("clave", "")
        else:
            usuario, clave = cargar_credenciales(nombre)

        if not usuario or not clave:
            log(
                f"  ✗ No hay credenciales para {nombre}. Abre 'Credenciales' para configurarlas."
            )
            raise RuntimeError(f"Sin credenciales para {nombre}")

        _hacer_login(driver, espera, sitio, nombre, usuario, clave, log)


def _hacer_login(
    driver, espera, sitio: dict, nombre: str, usuario: str, clave: str, log
) -> None:
    """
    Realiza el flujo de login en el sitio: rellena usuario/contraseña y envía el formulario.

    Después de un login exitoso guarda las cookies para no repetir el
    proceso en ejecuciones futuras.
    """
    driver.get(sitio["url_login"])
    espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, sitio["selector_user"]))
    )

    driver.find_element(By.CSS_SELECTOR, sitio["selector_user"]).send_keys(usuario)
    driver.find_element(By.CSS_SELECTOR, sitio["selector_pass"]).send_keys(clave)
    driver.find_element(By.CSS_SELECTOR, sitio["selector_btn_login"]).click()

    try:
        # Esperar a que la URL cambie; 'secure' es típico de demos de Herokuapp.
        # Para sitios reales, cambiar este selector a uno apropiado.
        espera.until(EC.url_contains("secure"))
    except Exception:
        log(
            f"  ✗ Error al iniciar sesión para {nombre}: la URL no cambió como se esperaba."
        )
        raise RuntimeError(f"Login fallido para {nombre}")

    guardar_cookies(driver, nombre)
    log(f"  ✓ Login exitoso, cookies guardadas: {nombre}")
    driver.get(sitio["url_upload"])


def _realizar_subida(
    driver, espera, sitio: dict, nombre: str, ruta_imagen: str, log
) -> None:
    """
    Envía el archivo al formulario de subida y verifica la confirmación.

    Para confirmar la subida, compara el texto de un elemento (h3 o h1 por
    defecto) antes y después de hacer clic en 'Submit'. Si el texto cambia
    y contiene alguna de las palabras_confirmacion, considera la subida exitosa.
    Si no cambia en 30 segundos, guarda una captura de debug y registra el error.
    """
    log(f"  → Subiendo imagen a {nombre}…")

    # Esperar y localizar el campo de archivo.
    campo_archivo = espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, sitio["selector_input_file"]))
    )
    # send_keys necesita la ruta absoluta para que Chrome la encuentre correctamente.
    campo_archivo.send_keys(os.path.abspath(ruta_imagen))

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
    except Exception:
        texto_antes = ""

    driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

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
        if any(p in resultado.lower() for p in palabras_ok):
            log(f"  ✓ {nombre}: subida exitosa → {resultado}")
        else:
            log(f'  ✗ {nombre}: respuesta inesperada → "{resultado}"')
            driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")
    except Exception:
        log(f"  ✗ {nombre}: no se pudo confirmar la subida (timeout).")
        driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")


# ── Subida HubSpot (notas con imagen) ─────────────────────────────────


def _subir_captura_hubspot(
    driver, espera, sitio: dict, nombre: str, ruta_imagen: str, log
) -> None:
    """
    Sube una captura a una nueva nota dentro del ticket actual de HubSpot.

    Flujo específico de HubSpot:
      1. Click en la pestaña "Notas" de la timeline
      2. Click en "Crear nota"
      3. Click en botón de imagen
      4. Localiza el input file real
      5. Sube la imagen
      6. Guarda la nota

    Requiere que el sitio tenga las claves:
      selector_tab_notas, selector_btn_crear_nota, selector_btn_imagen,
      selector_input_file, selector_btn_guardar
    """
    log(f"  → Subiendo captura a nota de {nombre}…")

    # ── 1. ABRIR TAB "NOTAS" ──────────────────────────────────────────
    log("  → Abriendo pestaña 'Notas'…")
    espera.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_tab_notas"]))
    ).click()
    time.sleep(1)

    # ── 2. CREAR NOTA ─────────────────────────────────────────────────
    log("  → Creando nueva nota…")
    espera.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_btn_crear_nota"]))
    ).click()
    time.sleep(1)

    # ── 3. CLICK BOTÓN IMAGEN ─────────────────────────────────────────
    log("  → Haciendo clic en botón de imagen…")
    espera.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_btn_imagen"]))
    ).click()
    time.sleep(0.5)

    # ── 4. INPUT FILE REAL ────────────────────────────────────────────
    log("  → Localizando input file…")
    file_input = espera.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, sitio["selector_input_file"]))
    )

    # ── 5. SUBIR IMAGEN ───────────────────────────────────────────────
    log(f"  → Enviando archivo: {ruta_imagen}")
    file_input.send_keys(os.path.abspath(ruta_imagen))
    # Esperar a que la imagen se procese (subida asíncrona en HubSpot)
    time.sleep(2)

    # ── 6. GUARDAR NOTA ───────────────────────────────────────────────
    log("  → Guardando nota…")
    espera.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, sitio["selector_btn_guardar"]))
    ).click()
    time.sleep(1.5)

    log(f"  ✓ Captura subida correctamente a nota de {nombre}")

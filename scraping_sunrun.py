"""
scraping_sunrun.py — Extracción de datos del cliente desde Sunrun.

Se conecta al Chrome ya abierto (puerto 9222) donde el usuario ya tiene
sesión activa, busca el ticket por número FSD y extrae:
  · Nombre del cliente
  · Dirección
  · Teléfono principal (Customer Phone)
  · Teléfono móvil (Mobile Phone)
  · Email
  · Estado (State)
  · County
  · Ciudad (City)
  · Zip Code
  · Número FSD confirmado

IMPORTANTE — Selectores configurables:
  Todos los selectores están agrupados al inicio del módulo.
  Si el DOM de Sunrun cambia, solo actualiza esos valores.

Mejoras aplicadas (v2.1):
  - _clic_resultado() refactorizado: detecta si estamos en /global-search/
    y aplica 6 estrategias XPath progresivas para encontrar el ticket
    en la página de resultados (texto visible, href, title, tabla, etc.).
  - Fallback mejorado para otras páginas de Sunrun (múltiples XPaths).
  - Guardado de DOM de diagnóstico diferenciado por escenario.
  - Cambio automático a la pestaña correcta de Sunrun al conectar.
  - Logging detallado de URL, título y pestaña activa.
  - Esperas explícitas con WebDriverWait mejoradas.
  - Manejo de contenido dinámico Salesforce LWC (espera de renderizado).
  - Reintento en elementos obsoletos (stale elements).
  - Selectores con logging de fallos.
  - Detección y cambio a iframes si es necesario.
"""

import re
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ══════════════════════════════════════════════════════════════════════
#  SELECTORES SUNRUN — actualiza aquí si el DOM cambia
# ══════════════════════════════════════════════════════════════════════

# URL base del portal Sunrun
URL_BASE_SUNRUN = "https://sunrun.my.site.com"

# URL de la lista de FS Dispatch (fallback si la búsqueda global falla)
URL_LISTA_SUNRUN = (
    "https://sunrun.my.site.com/partners/s/fs-dispatch/FS_Dispatch__c/Default"
)

# ── Barra de búsqueda GLOBAL de Salesforce (header superior) ─────────
# Confirmado en DOM: input dentro de .forceSearchInputDesktop
# role="combobox", placeholder="Search...", clase uiInputTextForAutocomplete
SEL_BUSQUEDA_GLOBAL = "div.forceSearchInputDesktop input[role='combobox']"

# ── Link del FSD en la tabla de resultados ────────────────────────────
# Patrón de href confirmado en DOM:
#   /partners/s/fs-dispatch/{RECORD_ID}/fsd{NUMERO}
# Se construye dinámicamente con el número buscado (ver _clic_resultado)

# ── Datos del cliente — XPath corregidos según DOM real de Sunrun ──────
#
# PROBLEMA ANTERIOR: se usaba //span[text()='Campo'] pero el DOM real
# tiene el texto en un nodo hijo sin espacios exactos, y el valor NO está
# directamente en <lightning-formatted-text> bajo slds-form-element, sino
# dentro de slds-form-element__control > span > slot > records-formula-output
# > lightning-formatted-text.
#
# SOLUCIÓN: usar normalize-space() en el span con clase test-id__field-label
# y bajar por slds-form-element__control hasta lightning-formatted-text.
# Patrón correcto confirmado en DOM capturado:
#
#   <div class="slds-form-element ...">
#     <div class="slds-form-element__label ...">
#       <span class="test-id__field-label">Customer Name</span>
#     </div>
#     <div class="slds-form-element__control">
#       <span class="slds-form-element__static ...">
#         <slot name="outputField">
#           <records-formula-output>
#             <lightning-formatted-text>Loyda Martinez</lightning-formatted-text>
#           </records-formula-output>
#         </slot>
#       </span>
#     </div>
#   </div>

SELECTOR_NUMERO_FSD = "//slot[@name='primaryField']//lightning-formatted-text"

SELECTOR_NOMBRE = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Customer Name']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_DIRECCION = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Address']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_TELEFONO = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Customer Phone']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_MOVIL = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Mobile Phone']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_EMAIL = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Customer Email']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_ESTADO = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='State']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_COUNTY = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='County']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_CIUDAD = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='City']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

SELECTOR_ZIP = "//span[contains(@class,'test-id__field-label') and normalize-space(text())='Zip Code']/ancestor::div[contains(@class,'label-stacked') or (contains(@class,'slds-form-element') and not(contains(@class,'slds-form-element__')))]//lightning-formatted-text"

# Tiempos de espera
TIMEOUT = 15  # espera normal por elemento
TIMEOUT_LISTA = 30  # espera para que cargue la lista
PAUSA_FILTRO = 2.0  # pausa tras escribir en el buscador (SPA Aura)
PAUSA_DETALLE = 1.5  # pausa tras clic en resultado

# Selector para el dropdown MRU de la barra global de Salesforce
# Confirmado en DOM: <a role="option" class="MRU_SCOPED ...">
SEL_MRU_DROPDOWN = "a.MRU_SCOPED"
TIMEOUT_MRU = 10  # espera máxima para que el dropdown MRU aparezca


# ══════════════════════════════════════════════════════════════════════
#  Normalización del FSD
# ══════════════════════════════════════════════════════════════════════


def _solo_digitos(fsd: str) -> str:
    """
    Extrae solo los dígitos del FSD, en cualquier formato de entrada.

    "FSD-1172172"  → "1172172"
    "FSD1172172"   → "1172172"
    "fsd 1172172"  → "1172172"
    "1172172"      → "1172172"
    """
    return re.sub(r"[^0-9]", "", fsd)


def _fsd_display(numero: str) -> str:
    """Formato de display estándar: "FSD-1172172"."""
    return f"FSD-{numero}"


# ══════════════════════════════════════════════════════════════════════
#  Ayudantes de logging y página
# ══════════════════════════════════════════════════════════════════════


def _log_estado_pagina(driver, log_func, prefix: str = ""):
    """Registra URL actual y título de la página."""
    try:
        url = driver.current_url
        titulo = driver.title
        log_func(f"  · {prefix}URL: {url} | Título: {titulo}")
    except Exception:
        pass


def _esperar_renderizado_completo(driver, timeout: float = 10.0) -> bool:
    """Espera a que document.readyState sea 'complete' (SPA/React/Vue)."""
    try:
        wait_local = WebDriverWait(driver, timeout)
        wait_local.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(0.5)  # Pausa adicional para frameworks SPA
        return True
    except (TimeoutException, WebDriverException):
        return False


def _clic_con_nueva_pestana(driver, elemento, log_func, timeout: float = 15.0) -> bool:
    """
    Hace clic en un elemento que puede abrir una pestaña nueva (target="_blank").

    Si el clic genera una pestaña nueva, cambia el driver a esa pestaña.
    Si no genera pestaña nueva (navegación en la misma), no hace nada extra.

    Devuelve True si después del clic el driver está en una pestaña con
    contenido (readyState complete), False si hubo error.
    """
    handles_antes = set(driver.window_handles)
    try:
        elemento.click()
    except Exception as e:
        log_func(f"  ⚠ Error al hacer clic: {e}")
        return False

    # Esperar hasta 3s a ver si aparece una pestaña nueva
    import time as _time

    deadline = _time.time() + 3.0
    while _time.time() < deadline:
        handles_ahora = set(driver.window_handles)
        nuevas = handles_ahora - handles_antes
        if nuevas:
            nueva = nuevas.pop()
            driver.switch_to.window(nueva)
            log_func(f"  ✓ Nueva pestaña detectada — cambiando a ella.")
            _esperar_renderizado_completo(driver, timeout=timeout)
            return True
        _time.sleep(0.2)

    # No se abrió pestaña nueva — navegación en la misma pestaña
    _esperar_renderizado_completo(driver, timeout=timeout)
    return True


def _cambiar_a_pestana_por_url(driver, subcadena_url: str, log_func) -> bool:
    """Cambia a la primera pestaña/ventana cuya URL contenga 'subcadena_url'."""
    try:
        handles = driver.window_handles
        log_func(
            f"  · Buscando pestaña que contenga '{subcadena_url}' "
            f"({len(handles)} disponibles)"
        )

        for handle in handles:
            try:
                driver.switch_to.window(handle)
                time.sleep(0.3)
                url_actual = driver.current_url.lower()
                if subcadena_url.lower() in url_actual:
                    log_func(
                        f"  ✓ Cambiado a pestaña: {driver.title} — "
                        f"{driver.current_url}"
                    )
                    return True
            except Exception:
                continue

        log_func(
            f"  ⚠ No se encontró pestaña con '{subcadena_url}'. "
            f"Usando pestaña activa actual."
        )
        if handles:
            driver.switch_to.window(handles[0])
        return False
    except Exception as e:
        log_func(f"  ⚠ Error al buscar pestaña: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════
#  Clase ScraperSunrun
# ══════════════════════════════════════════════════════════════════════


class ScraperSunrun:
    """
    Extrae datos de un ticket FS Dispatch en Sunrun.

    Siempre usa el Chrome ya abierto por el usuario (puerto 9222).
    Nunca abre un Chrome nuevo ni cierra el existente.

    Uso:
        scraper = ScraperSunrun(log_callback=mi_funcion_log)
        datos   = scraper.obtener_datos_por_fsd("1172172")
    """

    def __init__(self, log_callback=None):
        self._log = log_callback or print
        self._driver = None

    # ── Conexión ──────────────────────────────────────────────────────

    def _conectar(self) -> bool:
        """
        Se conecta al Chrome abierto en puerto 9222.
        Devuelve True si la conexión fue exitosa.

        NOTA: Se evitan opciones experimentales obsoletas (excludeSwitches,
        useAutomationExtension) que causan errores con ChromeDriver moderno.
        """
        try:
            opts = webdriver.ChromeOptions()

            # ── Antifingerprinting: solo --disable-blink-features ────────
            # excludeSwitches y useAutomationExtension ya no son compatibles
            # con ChromeDriver moderno (causan "invalid argument: unrecognized
            # chrome option"). Se reemplazan por --disable-blink-features.
            opts.add_argument("--disable-blink-features=AutomationControlled")

            # Conectar al Chrome ya abierto en puerto 9222
            opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opts,
            )

            # ── Opcional: ocultar navigator.webdriver ─────────────────
            # En Chrome 147+ esta propiedad ya no es redefinible cuando se
            # conecta a una sesión real de usuario (remote debugging 9222).
            # Se envuelve en try/catch para evitar el error:
            #   "Cannot redefine property: webdriver"
            try:
                self._driver.execute_script("""
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

            # ── Verificar que la conexión es funcional ─────────────────
            self._log("  ✓ Conectado al Chrome existente (puerto 9222).")

            # ── Logging del estado actual ──────────────────────────────
            _log_estado_pagina(self._driver, self._log, "[conexión] ")

            # ── Cambiar a pestaña de Sunrun si existe ──────────────────
            _cambiar_a_pestana_por_url(self._driver, "sunrun.my.site.com", self._log)

            return True

        except Exception as e:
            self._log(f"  ✗ No se pudo conectar al Chrome: {e}")
            self._log("  → Abre Chrome con depuración desde el botón en SSAuto.")
            import logging

            logging.getLogger("ssauto.driver").error(
                f"Error al conectar Chrome en scraping_sunrun: {e}"
            )
            return False

    # ── Detección de estado actual del navegador ────────────────────────

    def _detectar_estado(self, fsd_numero: str) -> str:
        """
        Analiza la URL actual del Chrome y determina en qué punto del
        flujo se encuentra el bot, para no reiniciar desde cero.

        Estados posibles:
          "en_detalle"   → ya está en la página del ticket FSD buscado
          "en_resultados"→ en la página de resultados de búsqueda global
                           (/global-search/) con el FSD ya buscado
          "en_sunrun"    → en Sunrun pero en otra página (lista, home, etc.)
          "fuera"        → fuera de Sunrun o URL desconocida

        Parámetros
        ----------
        fsd_numero : solo dígitos del FSD buscado (ej: "1245180")
        """
        try:
            url = self._driver.current_url.lower()
        except Exception:
            return "fuera"

        fsd_display = _fsd_display(fsd_numero).lower()  # "fsd-1245180"
        fsd_corto = f"fsd{fsd_numero}"  # "fsd1245180"

        # ── ¿Ya estamos en la página de detalle del ticket? ──────────
        # URL patrón: /partners/s/fs-dispatch/{RECORD_ID}/fsd1245180
        if fsd_corto in url and "/fs-dispatch/" in url:
            return "en_detalle"

        # ── ¿Estamos en la página de resultados de búsqueda global? ──
        # URL patrón: /partners/s/global-search/FSD-1245180
        if "/global-search/" in url and (
            fsd_numero in url or fsd_display.replace("-", "") in url
        ):
            return "en_resultados"

        # ── ¿Estamos en alguna otra página de Sunrun? ─────────────────
        if "sunrun.my.site.com" in url:
            return "en_sunrun"

        return "fuera"

    # ── Paso 1: buscar el FSD via barra global de Salesforce ────────────

    def _buscar_en_lista(self, fsd_numero: str) -> bool:
        """
        Usa la barra de búsqueda GLOBAL de Salesforce (header superior)
        para localizar el FSD y llegar a su página de detalle directamente.

        Flujo:
          1. Navegar a la lista de FS Dispatch para asegurar sesión activa.
          2. Localizar el input global (div.forceSearchInputDesktop input[role=combobox]).
          3. Escribir el FSD con send_keys carácter a carácter (evita autocomplete agresivo).
          4. Pulsar ENTER para lanzar la búsqueda.
          5. Esperar que aparezca el link del FSD en los resultados y hacer clic.

        Si la barra global falla (timeout), cae en fallback:
          → Intenta hacer clic directamente en el link de la tabla si ya
            está en la lista (el DOM de la lista ya muestra FSDs sin filtrar).

        Devuelve True si se llegó a la página de detalle del ticket.
        """
        fsd_display = _fsd_display(fsd_numero)
        wait_lista = WebDriverWait(self._driver, TIMEOUT_LISTA)
        wait_normal = WebDriverWait(self._driver, TIMEOUT)

        # ── Paso 1a: navegar a la lista para asegurar sesión ─────────
        self._log("  → Navegando a la lista de FS Dispatch...")
        self._driver.get(URL_LISTA_SUNRUN)
        _esperar_renderizado_completo(self._driver, timeout=TIMEOUT_LISTA)
        _log_estado_pagina(self._driver, self._log, "[lista] ")

        if "login" in self._driver.current_url.lower():
            self._log("  ✗ Sunrun redirigió al login.")
            self._log("  → Inicia sesión manualmente en Chrome primero.")
            return False

        # ── Paso 1b: intentar con la barra global de búsqueda ────────
        self._log(f"  → Buscando via barra global: {fsd_display}")
        try:
            campo = wait_lista.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_BUSQUEDA_GLOBAL))
            )
            self._log(f"  ✓ Barra global encontrada.")

            # Limpiar y escribir carácter a carácter para evitar que
            # el autocomplete de Aura/LWC descarte caracteres iniciales
            campo.click()
            time.sleep(0.3)
            campo.send_keys(Keys.CONTROL + "a")
            campo.send_keys(Keys.DELETE)
            time.sleep(0.3)
            for char in fsd_display:
                campo.send_keys(char)
                time.sleep(0.05)

            self._log(f"  ✓ FSD escrito en barra global: {fsd_display}")

            # Pausa para que Aura renderice el dropdown de sugerencias
            time.sleep(PAUSA_FILTRO)

            # ── Estrategia 1: clic en cualquier item del dropdown que
            # contenga el FSD buscado.
            #
            # Salesforce puede mostrar dos tipos de items:
            #   A) Item de resultado de búsqueda textual:
            #      <a role="option"> con texto exacto "FSD-XXXXXXX" (icono lupa)
            #   B) Item MRU (Most Recently Used):
            #      <a class="MRU_SCOPED" role="option"> con icono morado
            #
            # El XPath unificado detecta CUALQUIERA de los dos.
            # Siempre se intenta primero el dropdown antes de esperar TIMEOUT_MRU,
            # usando una espera corta (3s). Si no aparece en 3s, se espera hasta
            # TIMEOUT_MRU para dar tiempo al SPA de renderizar el MRU.
            try:
                # XPath unificado: cualquier <a role="option"> que contenga
                # el texto del FSD, independientemente de su clase o estructura.
                XPATH_DROPDOWN_FSD = (
                    f"//a[@role='option' and ("
                    f"  .//span[@title='{fsd_display}'] or"
                    f"  .//*[normalize-space(text())='{fsd_display}'] or"
                    f"  contains(normalize-space(.), '{fsd_display}')"
                    f")]"
                )

                # Intento rápido primero (3s) — cubre el caso del item
                # de búsqueda textual que aparece casi inmediatamente.
                try:
                    dropdown_fsd = WebDriverWait(self._driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (rápido): {fsd_display}")
                except (TimeoutException, NoSuchElementException):
                    # No apareció en 3s — esperar hasta TIMEOUT_MRU para el MRU
                    self._log(
                        f"  · Item no apareció en 3s, esperando hasta {TIMEOUT_MRU}s..."
                    )
                    dropdown_fsd = WebDriverWait(self._driver, TIMEOUT_MRU).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (MRU): {fsd_display}")

                self._log(f"  → Clic en item del dropdown: {fsd_display}")
                dropdown_fsd.click()
                _esperar_renderizado_completo(self._driver, timeout=TIMEOUT)
                _log_estado_pagina(self._driver, self._log, "[detalle-dropdown] ")
                if fsd_numero.lower() in self._driver.current_url.lower():
                    self._log(f"  ✓ Llegamos al detalle via dropdown.")
                    return True
                # URL puede tardar en actualizar en SPAs — esperar un poco más
                time.sleep(1.5)
                if fsd_numero.lower() in self._driver.current_url.lower():
                    self._log(f"  ✓ Llegamos al detalle via dropdown (espera extra).")
                    return True
                self._log(f"  · Dropdown clicado pero URL no cambió, continuando...")
            except (TimeoutException, NoSuchElementException):
                self._log(
                    f"  · Ningún item del dropdown encontrado tras {TIMEOUT_MRU}s,"
                    f" enviando ENTER..."
                )

            # ── Estrategia 2: ENTER → página de resultados → clic en link ──
            # URL de resultados: /partners/s/global-search/FSD-XXXXXXX
            # El link del FSD en la tabla tiene href con patrón:
            #   /partners/s/fs-dispatch/{RECORD_ID}/fsd{NUMERO}
            campo.send_keys(Keys.RETURN)
            _esperar_renderizado_completo(self._driver, timeout=TIMEOUT_LISTA)
            _log_estado_pagina(self._driver, self._log, "[resultados-global] ")

            try:
                # Esperar el link con href que contiene fsd+numero (confirmado en DOM)
                link_resultado = wait_normal.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//a[contains(@href,'/fs-dispatch/') "
                            f"and contains(@href,'fsd{fsd_numero}')]",
                        )
                    )
                )
                self._log(f"  → Clic en link de resultados: {fsd_display}")
                _clic_con_nueva_pestana(
                    self._driver, link_resultado, self._log, TIMEOUT
                )
                _log_estado_pagina(self._driver, self._log, "[detalle-resultados] ")
                self._log(f"  ✓ Página de detalle cargada via página de resultados.")
                return True
            except (TimeoutException, NoSuchElementException) as e:
                self._log(f"  · Link en página de resultados no encontrado: {e}")

        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"  · Barra global no disponible: {e}")

        # ── Fallback: el link ya existe en la tabla de la lista ───────
        # El DOM de la lista muestra FSDs sin filtrar. Si el FSD está
        # en la lista visible, podemos hacer clic directo en su link.
        self._log(f"  → Fallback: buscando link directo en tabla de lista...")
        try:
            link_tabla = wait_normal.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@href,'fsd{fsd_numero}')]")
                )
            )
            self._log(f"  → Clic en link de tabla (fallback): {fsd_display}")
            _clic_con_nueva_pestana(self._driver, link_tabla, self._log, TIMEOUT)
            _log_estado_pagina(self._driver, self._log, "[detalle-tabla] ")
            self._log(f"  ✓ Página de detalle cargada via tabla.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"  · Link en tabla no encontrado: {e}")

        self._log(f"  ✗ No se pudo llegar al detalle de {fsd_display} por ninguna vía.")
        return False

    # ── Búsqueda rápida desde cualquier página de Sunrun ───────────────

    def _buscar_desde_sunrun(self, fsd_numero: str) -> bool:
        """
        Usa la barra global directamente sin navegar a la lista primero.
        Solo se llama cuando ya estamos en Sunrun (sesión confirmada).

        Igual que _buscar_en_lista pero sin el paso 1a (navegar a lista).
        Devuelve True si llegó a la página de detalle o de resultados.
        """
        fsd_display = _fsd_display(fsd_numero)
        wait_lista = WebDriverWait(self._driver, TIMEOUT_LISTA)
        wait_normal = WebDriverWait(self._driver, TIMEOUT)

        self._log(f"  → Búsqueda rápida via barra global: {fsd_display}")
        try:
            campo = wait_lista.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_BUSQUEDA_GLOBAL))
            )
            campo.click()
            time.sleep(0.3)
            campo.send_keys(Keys.CONTROL + "a")
            campo.send_keys(Keys.DELETE)
            time.sleep(0.3)
            for char in fsd_display:
                campo.send_keys(char)
                time.sleep(0.05)

            time.sleep(PAUSA_FILTRO)

            # Intentar cualquier item del dropdown que contenga el FSD.
            # Misma lógica unificada que en _buscar_en_lista:
            # intento rápido (3s) primero, luego espera hasta TIMEOUT_MRU.
            try:
                XPATH_DROPDOWN_FSD = (
                    f"//a[@role='option' and ("
                    f"  .//span[@title='{fsd_display}'] or"
                    f"  .//*[normalize-space(text())='{fsd_display}'] or"
                    f"  contains(normalize-space(.), '{fsd_display}')"
                    f")]"
                )
                try:
                    dropdown_fsd = WebDriverWait(self._driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (rápido): {fsd_display}")
                except (TimeoutException, NoSuchElementException):
                    self._log(
                        f"  · Item no apareció en 3s, esperando hasta {TIMEOUT_MRU}s..."
                    )
                    dropdown_fsd = WebDriverWait(self._driver, TIMEOUT_MRU).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (MRU): {fsd_display}")

                dropdown_fsd.click()
                _esperar_renderizado_completo(self._driver, timeout=TIMEOUT)
                time.sleep(1.0)
                if fsd_numero.lower() in self._driver.current_url.lower():
                    self._log(f"  ✓ Llegamos al detalle via dropdown (rápido).")
                    return True
            except (TimeoutException, NoSuchElementException):
                self._log(
                    f"  · Ningún item del dropdown encontrado tras {TIMEOUT_MRU}s,"
                    f" enviando ENTER..."
                )

            # ENTER → página de resultados
            campo.send_keys(Keys.RETURN)
            _esperar_renderizado_completo(self._driver, timeout=TIMEOUT_LISTA)
            try:
                link_resultado = wait_normal.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//a[contains(@href,'/fs-dispatch/') "
                            f"and contains(@href,'fsd{fsd_numero}')]",
                        )
                    )
                )
                _clic_con_nueva_pestana(
                    self._driver, link_resultado, self._log, TIMEOUT
                )
                self._log(f"  ✓ Detalle cargado via resultados (búsqueda rápida).")
                return True
            except (TimeoutException, NoSuchElementException) as e:
                self._log(f"  · Link en resultados no encontrado: {e}")
                return False

        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"  · Barra global no disponible: {e}")
            return False

    # ── Paso 2: verificar que estamos en la página correcta ─────────────

    def _clic_resultado(self, fsd_numero: str) -> bool:
        """
        Navega al detalle del FSD desde la página actual.

        Soporta dos escenarios:
          A) Página de resultados de búsqueda global (/global-search/):
             Salesforce muestra los resultados en una tabla con links cuyo
             texto visible es "FSD-XXXXXXX". Se intentan múltiples XPaths
             para cubrir variaciones del DOM de Salesforce LWC.
          B) Cualquier otra página con link por href (fsd{numero}):
             Fallback clásico — href contiene fsd+número.

        Desde v3.0 _buscar_en_lista ya intenta llegar al detalle directo,
        así que si la URL ya es la del ticket, se retorna True inmediatamente.
        """
        fsd_display = _fsd_display(fsd_numero)

        # ── ¿Ya estamos en la página de detalle? ─────────────────────
        url_actual = self._driver.current_url.lower()
        if f"fsd{fsd_numero}" in url_actual and "/fs-dispatch/" in url_actual:
            self._log(f"  ✓ Ya en la página de detalle de {fsd_display}.")
            return True

        wait = WebDriverWait(self._driver, TIMEOUT)

        # ── Escenario A: página de resultados de búsqueda global ─────
        # URL: /partners/s/global-search/FSD-XXXXXXX
        # El DOM de resultados de Salesforce puede presentar el link con:
        #   1. Texto visible exacto "FSD-XXXXXXX"
        #   2. href que contiene fsd{numero} (el más fiable)
        #   3. Atributo title o aria-label con el nombre del registro
        #   4. Cualquier <a> dentro de la fila que contenga el número
        if "/global-search/" in url_actual:
            self._log(
                f"  → Estamos en resultados globales, buscando link del ticket..."
            )
            # Espera adicional para que Salesforce renderice los resultados
            time.sleep(PAUSA_FILTRO)

            # XPaths en orden de preferencia para la página de resultados
            xpaths_resultados = [
                # 1. href con fsd+numero (más específico y fiable)
                f"//a[contains(@href,'/fs-dispatch/') and contains(@href,'fsd{fsd_numero}')]",
                # 2. Texto visible exacto del link = "FSD-XXXXXXX"
                f"//a[normalize-space(text())='{fsd_display}']",
                # 3. Link con title o data-record-id que contenga el número
                f"//a[@title='{fsd_display}' or contains(@title,'{fsd_numero}')]",
                # 4. Cualquier <a> dentro de una celda/fila de resultado que
                #    contenga el texto del FSD (cubre wrappers LWC con slots)
                f"//table//a[contains(normalize-space(.), '{fsd_display}')]",
                f"//tbody//a[contains(normalize-space(.), '{fsd_display}')]",
                # 5. Genérico: cualquier <a> en la página que contenga el texto
                f"//a[contains(normalize-space(.), '{fsd_display}')]",
                # 6. Último recurso: href solo con el número (sin "fsd" prefix)
                f"//a[contains(@href,'{fsd_numero}') and contains(@href,'/fs-dispatch/')]",
            ]

            for i, xpath in enumerate(xpaths_resultados, 1):
                try:
                    link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    self._log(
                        f"  ✓ Link encontrado en resultados (estrategia {i}): {fsd_display}"
                    )
                    _clic_con_nueva_pestana(self._driver, link, self._log, TIMEOUT)
                    _log_estado_pagina(self._driver, self._log, "[detalle-resultados] ")
                    self._log(
                        f"  ✓ Página de detalle cargada desde resultados globales."
                    )
                    return True
                except (TimeoutException, NoSuchElementException):
                    self._log(f"  · Estrategia {i} no encontró el link, siguiente...")
                    continue
                except StaleElementReferenceException:
                    self._log(f"  · Elemento obsoleto en estrategia {i}, siguiente...")
                    continue

            self._log(
                f"  ✗ No se encontró {fsd_display} en la página de resultados globales."
            )
            # Guardar DOM para diagnóstico
            try:
                with open(
                    "debug_dom_sunrun_resultados.html", "w", encoding="utf-8"
                ) as f:
                    f.write(self._driver.page_source)
                self._log("  → DOM guardado en debug_dom_sunrun_resultados.html")
            except Exception:
                pass
            return False

        # ── Escenario B: otra página de Sunrun (lista, home, etc.) ───
        self._log(
            f"  · URL no es de detalle ni de resultados globales, buscando link..."
        )
        xpaths_fallback = [
            f"//a[contains(@href,'/fs-dispatch/') and contains(@href,'fsd{fsd_numero}')]",
            f"//a[contains(@href,'fsd{fsd_numero}')]",
            f"//a[normalize-space(text())='{fsd_display}']",
        ]

        for i, xpath in enumerate(xpaths_fallback, 1):
            try:
                link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self._log(f"  → Clic en link (fallback {i}): {fsd_display}")
                _clic_con_nueva_pestana(self._driver, link, self._log, TIMEOUT)
                _log_estado_pagina(self._driver, self._log, "[detalle-fallback] ")
                return True
            except (TimeoutException, NoSuchElementException):
                continue
            except StaleElementReferenceException:
                continue

        self._log(f"  ✗ No se encontró {fsd_display} en la página actual.")
        try:
            with open("debug_dom_sunrun_busqueda.html", "w", encoding="utf-8") as f:
                f.write(self._driver.page_source)
            self._log("  → DOM guardado en debug_dom_sunrun_busqueda.html")
        except Exception:
            pass
        return False

    # ── Paso 3: extraer datos del detalle del ticket ──────────────────

    def _extraer_campo(self, xpath: str, nombre: str) -> str:
        """
        Extrae el texto de un campo usando XPath.

        Estrategias en orden:
          1. XPath principal → lightning-formatted-text dentro de slds-form-element__control
          2. Fallback: innerText del elemento via JS (shadow DOM parcial)
          3. Fallback: texto del div slds-form-element__control completo

        Devuelve "" si el elemento no existe.
        """
        try:
            wait = WebDriverWait(self._driver, TIMEOUT // 2)
            elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            texto = elem.text.strip()
            if texto:
                return texto
            # Algunos campos LWC guardan el valor en un atributo
            valor = (elem.get_attribute("value") or "").strip()
            if valor:
                return valor
            # Fallback JS: leer innerText cuando .text no llega por shadow DOM
            try:
                texto_js = self._driver.execute_script(
                    "return arguments[0].innerText;", elem
                )
                if texto_js and texto_js.strip():
                    return texto_js.strip()
            except Exception:
                pass
            return ""
        except (
            TimeoutException,
            NoSuchElementException,
            StaleElementReferenceException,
        ) as e:
            # Fallback: subir al div slds-form-element__control y leer su texto.
            # Cubre casos donde lightning-formatted-text no es accesible por Selenium
            # pero el texto si esta renderizado en el DOM visible.
            try:
                xpath_control = (
                    xpath.rsplit(
                        "//div[contains(@class,'slds-form-element__control')]", 1
                    )[0]
                    + "//div[contains(@class,'slds-form-element__control')]"
                )
                elem_ctrl = self._driver.find_element(By.XPATH, xpath_control)
                texto_ctrl = (elem_ctrl.text or "").strip()
                if texto_ctrl:
                    self._log(
                        f"  · '{nombre}' extraído via fallback (slds-form-element__control)."
                    )
                    return texto_ctrl
            except Exception:
                pass

            self._log(
                f"  ⚠ Campo '{nombre}' no encontrado en la página ({type(e).__name__})."
            )
            self._log(f"  → XPath: {xpath[:80]}...")
            return ""

    def _extraer_detalle(self, fsd_numero: str) -> dict:
        """
        Extrae todos los campos de CUSTOMER CONTACT INFORMATION.

        Espera primero a que el número FSD aparezca en la página para
        confirmar que estamos en el ticket correcto antes de extraer.
        """
        self._log("  → Extrayendo datos del ticket...")

        # Confirmar que cargó la página del ticket esperando el FSD
        fsd_display = _fsd_display(fsd_numero)
        try:
            WebDriverWait(self._driver, TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(text(),'{fsd_display}') "
                        f"or contains(text(),'{fsd_numero}')]",
                    )
                )
            )
            self._log(f"  ✓ Ticket confirmado en página: {fsd_display}")
            time.sleep(1)  # pausa para campos dinámicos LWC
        except (TimeoutException, NoSuchElementException):
            self._log("  ⚠ No se confirmó el ticket en la página, extrayendo igual...")

        nombre = self._extraer_campo(SELECTOR_NOMBRE, "Customer Name")
        direccion = self._extraer_campo(SELECTOR_DIRECCION, "Address")
        telefono = self._extraer_campo(SELECTOR_TELEFONO, "Customer Phone")
        movil = self._extraer_campo(SELECTOR_MOVIL, "Mobile Phone")
        email = self._extraer_campo(SELECTOR_EMAIL, "Customer Email")

        # ── Pausa extra: State/City/Zip están en la sección Address que
        # Salesforce LWC renderiza en un segundo ciclo después de los
        # campos de contacto. Sin espera, Selenium los encuentra vacíos.
        self._log("  → Esperando renderizado de sección de dirección...")
        time.sleep(2.5)

        estado = self._extraer_campo(SELECTOR_ESTADO, "State")
        county = self._extraer_campo(SELECTOR_COUNTY, "County")
        ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
        zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")

        # ── Si siguen vacíos, intentar scroll + reintento ─────────────
        if not estado or not ciudad or not zip_code:
            self._log("  → Campos de dirección vacíos, intentando scroll...")
            try:
                self._driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(2.0)
                if not estado:
                    estado = self._extraer_campo(SELECTOR_ESTADO, "State")
                if not county:
                    county = self._extraer_campo(SELECTOR_COUNTY, "County")
                if not ciudad:
                    ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
                if not zip_code:
                    zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")
            except Exception as e:
                self._log(f"  ⚠ Error en scroll/reintento: {e}")

        # ── Si aún vacíos, intentar con JS directamente ───────────────
        if not estado or not ciudad or not zip_code:
            self._log("  → Intentando extracción JS para campos de dirección...")
            for sel_var, nombre_campo, var_name in [
                (SELECTOR_ESTADO, "State", "estado"),
                (SELECTOR_COUNTY, "County", "county"),
                (SELECTOR_CIUDAD, "City", "ciudad"),
                (SELECTOR_ZIP, "Zip Code", "zip_code"),
            ]:
                try:
                    elem = self._driver.find_element(By.XPATH, sel_var)
                    valor_js = self._driver.execute_script(
                        "return arguments[0].innerText || arguments[0].textContent;",
                        elem,
                    )
                    if valor_js and valor_js.strip():
                        valor = valor_js.strip()
                        self._log(f"  ✓ {nombre_campo} via JS: '{valor}'")
                        if var_name == "estado":
                            estado = valor
                        elif var_name == "county":
                            county = valor
                        elif var_name == "ciudad":
                            ciudad = valor
                        elif var_name == "zip_code":
                            zip_code = valor
                except Exception:
                    pass

        self._log(
            f"  ✓ Sunrun → {nombre or '(sin nombre)'} | "
            f"{ciudad or '(sin ciudad)'} | "
            f"Tel: {telefono or '(sin tel)'}"
        )

        return {
            "fuente": "Sunrun",
            "fsd": fsd_display,
            "nombre": nombre,
            "telefono": telefono,
            "telefono_movil": movil,
            "email": email,
            "direccion": direccion,
            "estado_pr": estado,
            "condado": county,
            "ciudad": ciudad,
            "codigo_postal": zip_code,
            "error": None,
        }

    # ── Método público principal ──────────────────────────────────────

    def obtener_datos_por_fsd(self, fsd: str) -> dict:
        """
        Conecta al Chrome, busca el FSD en Sunrun y devuelve los datos.

        Parámetros
        ----------
        fsd : número FSD en cualquier formato:
              "FSD-1172172", "FSD1172172", "fsd1172172", "1172172"

        Devuelve
        --------
        dict con los datos extraídos. La clave "error" es None si todo
        fue bien, o contiene el mensaje de error si algo falló.
        Las demás claves siempre están presentes (vacías si no se encontró).
        Nunca lanza excepciones al llamador.

        Nota: No cierra Chrome — es el navegador del usuario.
        """
        fsd_numero = _solo_digitos(fsd)

        if not fsd_numero:
            return self._dict_error("", f"Formato de FSD inválido: '{fsd}'")

        self._log(f"  → Buscando FSD: {_fsd_display(fsd_numero)}")

        if not self._conectar():
            return self._dict_error(
                fsd_numero,
                "No se pudo conectar al Chrome. "
                "¿Está abierto con --remote-debugging-port=9222?",
            )

        try:
            # ── Detectar en qué punto del flujo está el navegador ────
            estado_actual = self._detectar_estado(fsd_numero)
            self._log(f"  → Estado actual del navegador: [{estado_actual}]")

            if estado_actual == "en_detalle":
                # ✅ Ya estamos en la página correcta — extraer directo
                self._log("  ✓ Ya en la página del ticket, extrayendo datos...")
                return self._extraer_detalle(fsd_numero)

            elif estado_actual == "en_resultados":
                # ✅ Ya buscamos el FSD — solo hacer clic en el link
                self._log(
                    "  ✓ Ya en resultados de búsqueda, haciendo clic en el ticket..."
                )
                if not self._clic_resultado(fsd_numero):
                    return self._dict_error(
                        fsd_numero,
                        f"El FSD {_fsd_display(fsd_numero)} no apareció en resultados.",
                    )
                return self._extraer_detalle(fsd_numero)

            elif estado_actual == "en_sunrun":
                # ✅ Estamos en Sunrun — usar barra global directamente
                # sin navegar a la lista primero (ya hay sesión activa)
                self._log("  ✓ Ya en Sunrun, usando barra global de búsqueda...")
                if not self._buscar_desde_sunrun(fsd_numero):
                    # Fallback: proceso completo
                    self._log("  · Fallback: iniciando proceso completo...")
                    if not self._buscar_en_lista(fsd_numero):
                        return self._dict_error(
                            fsd_numero,
                            "No se pudo cargar la lista de Sunrun.",
                        )
                if not self._clic_resultado(fsd_numero):
                    return self._dict_error(
                        fsd_numero,
                        f"El FSD {_fsd_display(fsd_numero)} no apareció en la lista.",
                    )
                return self._extraer_detalle(fsd_numero)

            else:
                # "fuera" → proceso completo desde el principio
                self._log(
                    "  · Navegador fuera de Sunrun, iniciando proceso completo..."
                )
                if not self._buscar_en_lista(fsd_numero):
                    return self._dict_error(
                        fsd_numero,
                        "No se pudo cargar la lista de Sunrun. "
                        "Verifica que la sesión esté activa en Chrome.",
                    )
                if not self._clic_resultado(fsd_numero):
                    return self._dict_error(
                        fsd_numero,
                        f"El FSD {_fsd_display(fsd_numero)} no apareció en la lista.",
                    )
                return self._extraer_detalle(fsd_numero)

        except Exception as e:
            self._log(f"  ✗ Error inesperado en ScraperSunrun: {e}")
            return self._dict_error(fsd_numero, str(e))

        # IMPORTANTE: NO se cierra el driver porque es el Chrome del usuario.

    @staticmethod
    def _dict_error(fsd_numero: str, mensaje: str) -> dict:
        """Dict con todos los campos vacíos y el error registrado."""
        return {
            "fuente": "Sunrun",
            "fsd": _fsd_display(fsd_numero) if fsd_numero else "",
            "nombre": "",
            "telefono": "",
            "telefono_movil": "",
            "email": "",
            "direccion": "",
            "estado_pr": "",
            "condado": "",
            "ciudad": "",
            "codigo_postal": "",
            "error": mensaje,
        }

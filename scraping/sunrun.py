"""
scraping.sunrun — Extracción de datos del cliente desde Sunrun.

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

import time
import re

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

from core.browser import BrowserFactory, encontrar_pestana, esperar_carga, ErrorBrowser
from utils.fsd import solo_digitos, fsd_display
from .sunrun_selectors import (
    URL_BASE_SUNRUN,
    URL_LISTA_SUNRUN,
    SEL_BUSQUEDA_GLOBAL,
    SEL_MRU_DROPDOWN,
    SELECTOR_NOMBRE,
    SELECTOR_DIRECCION,
    SELECTOR_TELEFONO,
    SELECTOR_MOVIL,
    SELECTOR_EMAIL,
    SELECTOR_ESTADO,
    SELECTOR_COUNTY,
    SELECTOR_CIUDAD,
    SELECTOR_ZIP,
    SELECTOR_DISPATCH_STATE,
    SELECTOR_APPOINTMENT_DATE,
    SELECTOR_CASE_REASON,
    TIMEOUT,
    TIMEOUT_LISTA,
    TIMEOUT_MRU,
    PAUSA_FILTRO,
    PAUSA_DETALLE,
)


# ══════════════════════════════════════════════════════════════════════
#  Ayudantes de logging y página
# ══════════════════════════════════════════════════════════════════════


def _log_estado_pagina(driver, log_func, prefix: str = ""):
    """Registra URL actual y titulo de la pagina para diagnostico.

    Args:
        driver: instancia de Selenium WebDriver.
        log_func: callback de logging (ej. print o self._log).
        prefix: texto opcional a anteponer en el mensaje de log.
    """
    try:
        url = driver.current_url
        titulo = driver.title
        log_func(f"  · {prefix}URL: {url} | Título: {titulo}")
    except Exception:
        pass


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
            if not esperar_carga(driver, timeout):
                return False
            return True
        _time.sleep(0.2)

    # No se abrió pestaña nueva — navegación en la misma pestaña
    if not esperar_carga(driver, timeout):
        return False
    return True


# ══════════════════════════════════════════════════════════════════════
#  Clase ScraperSunrun
# ══════════════════════════════════════════════════════════════════════


class ScraperSunrun:
    """
    Extrae datos de un ticket FS Dispatch en Sunrun.

    Siempre usa el Chrome ya abierto por el usuario (puerto 9222).
    Nunca abre un Chrome nuevo ni cierra el existente.

    Attributes:
        _driver: instancia de Selenium WebDriver conectada al Chrome del usuario.
        _log: callback de logging.

    Uso:
        scraper = ScraperSunrun(log_callback=mi_funcion_log)
        datos   = scraper.obtener_datos_por_fsd("1172172")
    """

    def __init__(self, log_callback=None):
        """Inicializa el scraper con un callback de logging opcional.

        Args:
            log_callback: funcion que recibe un string para registrar
                          mensajes. Por defecto usa print.
        """
        self._log = log_callback or print
        self._driver = None

    # ── Conexión ──────────────────────────────────────────────────────

    def _conectar(self) -> bool:
        """
        Se conecta al Chrome abierto en puerto 9222 via BrowserFactory.
        Devuelve True si la conexión fue exitosa.
        """
        try:
            self._driver = BrowserFactory.conectar_existente()
            self._log("  ✓ Conectado al Chrome existente (puerto 9222).")
            _log_estado_pagina(self._driver, self._log, "[conexión] ")
            encontrar_pestana(self._driver, "sunrun.my.site.com", self._log)
            return True
        except ErrorBrowser as e:
            self._log(f"  ✗ No se pudo conectar al Chrome: {e}")
            self._log("  → Abre Chrome con depuración desde el botón en SSAuto.")
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

        fsd_corto = f"fsd{fsd_numero}"  # "fsd1245180"

        # ── ¿Ya estamos en la página de detalle del ticket? ──────────
        # URL patrón: /partners/s/fs-dispatch/{RECORD_ID}/fsd1245180
        if re.search(r'/fsd' + re.escape(fsd_numero) + r'(?![0-9])', url) and "/fs-dispatch/" in url:
            return "en_detalle"

        # ── ¿Estamos en la página de resultados de búsqueda global? ──
        # URL patrón: /partners/s/global-search/FSD-1245180
        if "/global-search/" in url and re.search(
            r'(?<![0-9])' + re.escape(fsd_numero) + r'(?![0-9])', url
        ):
            return "en_resultados"

        # ── ¿Estamos en alguna otra página de Sunrun? ─────────────────
        if "sunrun.my.site.com" in url:
            return "en_sunrun"

        return "fuera"

    # ── Paso 1: buscar el FSD via barra global de Salesforce ────────────

    def _buscar_en_lista(self, fsd_numero: str) -> bool:
        self._log("  → Navegando a la lista de FS Dispatch...")
        self._driver.get(URL_LISTA_SUNRUN)
        esperar_carga(self._driver, TIMEOUT_LISTA)
        _log_estado_pagina(self._driver, self._log, "[lista] ")

        if "login" in self._driver.current_url.lower():
            self._log("  ✗ Sunrun redirigió al login.")
            self._log("  → Inicia sesión manualmente en Chrome primero.")
            return False

        if self._buscar_con_barra_global(fsd_numero):
            return True

        # ── Fallback: el link ya existe en la tabla de la lista ───────
        self._log("  → Fallback: buscando link directo en tabla de lista...")
        fsd_display_val = fsd_display(fsd_numero)
        wait_normal = WebDriverWait(self._driver, TIMEOUT)
        try:
            link_tabla = wait_normal.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[contains(@href,'fsd{fsd_numero}')]")
                )
            )
            self._log(f"  → Clic en link de tabla (fallback): {fsd_display_val}")
            _clic_con_nueva_pestana(self._driver, link_tabla, self._log, TIMEOUT)
            _log_estado_pagina(self._driver, self._log, "[detalle-tabla] ")
            self._log("  ✓ Página de detalle cargada via tabla.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"  · Link en tabla no encontrado: {e}")

        self._log(f"  ✗ No se pudo llegar al detalle de {fsd_display_val} por ninguna vía.")
        return False

    def _buscar_desde_sunrun(self, fsd_numero: str) -> bool:
        """Busca el FSD desde cualquier pagina de Sunrun usando la barra global.

        Args:
            fsd_numero: solo digitos del FSD (ej. "1172172").

        Returns:
            True si se navego exitosamente al detalle del ticket.
        """
        self._log(f"  -> Busqueda rapida via barra global: {fsd_display(fsd_numero)}")
        return self._buscar_con_barra_global(fsd_numero)

    def _buscar_con_barra_global(self, fsd_numero: str) -> bool:
        """
        Lógica compartida de búsqueda con la barra global de Salesforce.

        Estrategias en orden:
          1. Dropdown MRU (rápido 3s → TIMEOUT_MRU si es necesario)
          2. ENTER → página de resultados globales → clic en link del ticket

        Asume que el driver ya está en una página de Sunrun con sesión activa.
        """
        fsd_display_val = fsd_display(fsd_numero)
        wait_lista = WebDriverWait(self._driver, TIMEOUT_LISTA)
        wait_normal = WebDriverWait(self._driver, TIMEOUT)

        try:
            campo = wait_lista.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_BUSQUEDA_GLOBAL))
            )
            self._log("  ✓ Barra global encontrada.")

            campo.click()
            campo.send_keys(Keys.CONTROL + "a")
            campo.send_keys(Keys.DELETE)
            campo.send_keys(fsd_display_val)

            self._log(f"  ✓ FSD escrito en barra global: {fsd_display_val}")

            # Esperar a que aparezca el dropdown o la página de resultados
            try:
                WebDriverWait(self._driver, PAUSA_FILTRO + 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//*[contains(text(),'{fsd_display_val}')]")
                    )
                )
            except TimeoutException:
                pass  # Seguimos adelante — puede que no haya dropdown

            # ── Estrategia 1: dropdown ─────────────────────────────────
            try:
                XPATH_DROPDOWN_FSD = (
                    f"//a[@role='option' and ("
                    f"  .//span[@title='{fsd_display_val}'] or"
                    f"  .//*[normalize-space(text())='{fsd_display_val}'] or"
                    f"  contains(normalize-space(.), '{fsd_display_val}')"
                    f")]"
                )
                try:
                    dropdown_fsd = WebDriverWait(self._driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (rápido): {fsd_display_val}")
                except (TimeoutException, NoSuchElementException):
                    self._log(
                        f"  · Item no apareció en 3s, esperando hasta {TIMEOUT_MRU}s..."
                    )
                    dropdown_fsd = WebDriverWait(self._driver, TIMEOUT_MRU).until(
                        EC.element_to_be_clickable((By.XPATH, XPATH_DROPDOWN_FSD))
                    )
                    self._log(f"  ✓ Item en dropdown (MRU): {fsd_display_val}")

                dropdown_fsd.click()
                esperar_carga(self._driver, TIMEOUT)
                _log_estado_pagina(self._driver, self._log, "[detalle-dropdown] ")
                try:
                    WebDriverWait(self._driver, 3).until(
                        lambda d: fsd_numero.lower() in d.current_url.lower()
                    )
                except TimeoutException:
                    pass
                if fsd_numero.lower() in self._driver.current_url.lower():
                    self._log("  ✓ Llegamos al detalle via dropdown.")
                    return True
                self._log("  · Dropdown clicado pero URL no cambió, continuando...")
            except (TimeoutException, NoSuchElementException):
                self._log(
                    f"  · Ningún item del dropdown encontrado tras {TIMEOUT_MRU}s,"
                    f" enviando ENTER..."
                )

            # ── Estrategia 2: ENTER → resultados globales → link ──────
            campo.send_keys(Keys.RETURN)
            esperar_carga(self._driver, TIMEOUT_LISTA)
            _log_estado_pagina(self._driver, self._log, "[resultados-global] ")

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
                self._log(f"  → Clic en link de resultados: {fsd_display_val}")
                if not _clic_con_nueva_pestana(
                    self._driver, link_resultado, self._log, TIMEOUT
                ):
                    self._log("  · Clic no navegó correctamente.")
                elif self._detectar_estado(fsd_numero) != "en_detalle":
                    self._log("  · No se llegó al detalle del ticket esperado.")
                else:
                    _log_estado_pagina(self._driver, self._log, "[detalle-resultados] ")
                    self._log("  ✓ Página de detalle cargada via resultados globales.")
                    return True
            except (TimeoutException, NoSuchElementException) as e:
                self._log(f"  · Link en resultados no encontrado: {e}")

        except (TimeoutException, NoSuchElementException) as e:
            self._log(f"  · Barra global no disponible: {e}")

        return False

    # ── Paso 2: verificar que estamos en la pagina correcta ─────────────

    def _clic_resultado(self, fsd_numero: str) -> bool:
        """
        Navega al detalle del FSD desde la pagina actual.
        Despacha a _clic_desde_resultados_globales o _clic_desde_otra_pagina
        segun la URL actual.
        """
        fsd_display_val = fsd_display(fsd_numero)

        url_actual = self._driver.current_url.lower()
        if re.search(r'/fsd' + re.escape(fsd_numero) + r'(?![0-9])', url_actual) and "/fs-dispatch/" in url_actual:
            self._log(f"  v Ya en la pagina de detalle de {fsd_display_val}.")
            return True

        if "/global-search/" in url_actual:
            return self._clic_desde_resultados_globales(fsd_numero, fsd_display_val)
        return self._clic_desde_otra_pagina(fsd_numero, fsd_display_val)

    def _clic_desde_resultados_globales(self, fsd_numero: str, fsd_display_val: str) -> bool:
        """Escenario A: pagina de resultados de busqueda global (/global-search/)."""
        self._log("  -> Estamos en resultados globales, buscando link del ticket...")

        try:
            WebDriverWait(self._driver, PAUSA_FILTRO + 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@href,'/fs-dispatch/')]")
                )
            )
        except TimeoutException:
            pass

        wait = WebDriverWait(self._driver, TIMEOUT)
        xpaths_resultados = [
            f"//a[contains(@href,'/fs-dispatch/') and contains(@href,'fsd{fsd_numero}')]",
            f"//a[normalize-space(text())='{fsd_display_val}']",
            f"//a[@title='{fsd_display_val}' or contains(@title,'{fsd_numero}')]",
            f"//table//a[contains(normalize-space(.), '{fsd_display_val}')]",
            f"//tbody//a[contains(normalize-space(.), '{fsd_display_val}')]",
            f"//a[contains(normalize-space(.), '{fsd_display_val}')]",
            f"//a[contains(@href,'{fsd_numero}') and contains(@href,'/fs-dispatch/')]",
        ]

        for i, xpath in enumerate(xpaths_resultados, 1):
            try:
                link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self._log(f"  v Link encontrado en resultados (estrategia {i}): {fsd_display_val}")
                if _clic_con_nueva_pestana(
                    self._driver, link, self._log, TIMEOUT
                ) and self._detectar_estado(fsd_numero) == "en_detalle":
                    _log_estado_pagina(self._driver, self._log, "[detalle-resultados] ")
                    self._log("  v Pagina de detalle cargada desde resultados globales.")
                    return True
                self._log(f"  . Estrategia {i}: navegación fallida, probando siguiente...")
            except (TimeoutException, NoSuchElementException):
                self._log(f"  . Estrategia {i} no encontro el link, siguiente...")
                continue
            except StaleElementReferenceException:
                self._log(f"  . Elemento obsoleto en estrategia {i}, siguiente...")
                continue

        self._log(f"  x No se encontro {fsd_display_val} en la pagina de resultados globales.")
        try:
            with open("debug_dom_sunrun_resultados.html", "w", encoding="utf-8") as f:
                f.write(self._driver.page_source)
            self._log("  -> DOM guardado en debug_dom_sunrun_resultados.html")
        except Exception:
            pass
        return False

    def _clic_desde_otra_pagina(self, fsd_numero: str, fsd_display_val: str) -> bool:
        """Escenario B: cualquier otra pagina de Sunrun (lista, home, etc.)."""
        self._log("  . URL no es de detalle ni de resultados globales, buscando link...")
        wait = WebDriverWait(self._driver, TIMEOUT)
        xpaths_fallback = [
            f"//a[contains(@href,'/fs-dispatch/') and contains(@href,'fsd{fsd_numero}')]",
            f"//a[contains(@href,'fsd{fsd_numero}')]",
            f"//a[normalize-space(text())='{fsd_display_val}']",
        ]

        for i, xpath in enumerate(xpaths_fallback, 1):
            try:
                link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self._log(f"  -> Clic en link (fallback {i}): {fsd_display_val}")
                if _clic_con_nueva_pestana(
                    self._driver, link, self._log, TIMEOUT
                ) and self._detectar_estado(fsd_numero) == "en_detalle":
                    _log_estado_pagina(self._driver, self._log, "[detalle-fallback] ")
                    return True
                self._log(f"  . Fallback {i}: navegación fallida.")
            except (TimeoutException, NoSuchElementException):
                continue
            except StaleElementReferenceException:
                continue

        self._log(f"  x No se encontro {fsd_display_val} en la pagina actual.")
        try:
            with open("debug_dom_sunrun_busqueda.html", "w", encoding="utf-8") as f:
                f.write(self._driver.page_source)
            self._log("  -> DOM guardado en debug_dom_sunrun_busqueda.html")
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

    def _extraer_seccion_direccion(self) -> tuple:
        """
        Extrae estado, county, ciudad y codigo postal con reintentos y fallback JS.

        Salesforce LWC renderiza State/City/Zip en un segundo ciclo asincrono.
        Estrategia: esperar render, scroll, reintento, JS directo.
        """
        self._log("  -> Esperando renderizado de seccion de direccion...")
        try:
            WebDriverWait(self._driver, 5).until(
                lambda d: (
                    d.find_element(By.XPATH, SELECTOR_ESTADO).text.strip()
                    or d.find_element(By.XPATH, SELECTOR_CIUDAD).text.strip()
                    or d.find_element(By.XPATH, SELECTOR_ZIP).text.strip()
                )
            )
        except (TimeoutException, NoSuchElementException):
            pass

        estado = self._extraer_campo(SELECTOR_ESTADO, "State")
        county = self._extraer_campo(SELECTOR_COUNTY, "County")
        ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
        zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")

        # Scroll + reintento
        if not estado or not ciudad or not zip_code:
            self._log("  -> Campos de direccion vacios, intentando scroll...")
            try:
                self._driver.execute_script("window.scrollBy(0, 400);")
                WebDriverWait(self._driver, 4).until(
                    lambda d: (
                        d.find_element(By.XPATH, SELECTOR_ESTADO).text.strip()
                        or d.find_element(By.XPATH, SELECTOR_CIUDAD).text.strip()
                        or d.find_element(By.XPATH, SELECTOR_ZIP).text.strip()
                    )
                )
            except (TimeoutException, NoSuchElementException):
                pass
            except Exception as e:
                self._log(f"  . Error en scroll/reintento: {e}")
            if not estado:
                estado = self._extraer_campo(SELECTOR_ESTADO, "State")
            if not county:
                county = self._extraer_campo(SELECTOR_COUNTY, "County")
            if not ciudad:
                ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
            if not zip_code:
                zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")

        # Fallback JS directo
        if not estado or not ciudad or not zip_code:
            self._log("  -> Intentando extraccion JS para campos de direccion...")
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
                        self._log(f"  v {nombre_campo} via JS: '{valor}'")
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

        return estado, county, ciudad, zip_code

    def _extraer_detalle(self, fsd_numero: str) -> dict:
        """Extrae todos los campos de CUSTOMER CONTACT INFORMATION."""
        self._log("  -> Extrayendo datos del ticket...")

        fsd_display_val = fsd_display(fsd_numero)
        try:
            WebDriverWait(self._driver, TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(),'{fsd_display_val}') "
                               f"or contains(text(),'{fsd_numero}')]")
                )
            )
            self._log(f"  v Ticket confirmado en pagina: {fsd_display_val}")
            try:
                WebDriverWait(self._driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, SELECTOR_NOMBRE))
                )
            except TimeoutException:
                pass
        except (TimeoutException, NoSuchElementException):
            self._log("  . No se confirmo el ticket en la pagina, extrayendo igual...")

        nombre = self._extraer_campo(SELECTOR_NOMBRE, "Customer Name")
        direccion = self._extraer_campo(SELECTOR_DIRECCION, "Address")
        telefono = self._extraer_campo(SELECTOR_TELEFONO, "Customer Phone")
        movil = self._extraer_campo(SELECTOR_MOVIL, "Mobile Phone")
        email = self._extraer_campo(SELECTOR_EMAIL, "Customer Email")
        dispatch_state = self._extraer_campo(SELECTOR_DISPATCH_STATE, "Dispatch State")
        appointment_date = self._extraer_campo(
            SELECTOR_APPOINTMENT_DATE, "Appointment Date"
        )
        case_reason = self._extraer_campo(SELECTOR_CASE_REASON, "Case Reason")

        estado, county, ciudad, zip_code = self._extraer_seccion_direccion()

        self._log(
            f"  v Sunrun -> {nombre or '(sin nombre)'} | "
            f"{ciudad or '(sin ciudad)'} | "
            f"Tel: {telefono or '(sin tel)'}"
        )

        return {
            "fuente": "Sunrun",
            "fsd": fsd_display_val,
            "nombre": nombre,
            "telefono": telefono,
            "telefono_movil": movil,
            "email": email,
            "direccion": direccion,
            "estado_pr": estado,
            "condado": county,
            "ciudad": ciudad,
            "codigo_postal": zip_code,
            "dispatch_state": dispatch_state,
            "appointment_date": appointment_date,
            "case_reason": case_reason,
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
        fsd_numero = solo_digitos(fsd)

        if not fsd_numero:
            return self._dict_error("", f"Formato de FSD inválido: '{fsd}'")

        self._log(f"  → Buscando FSD: {fsd_display(fsd_numero)}")

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
                        f"El FSD {fsd_display(fsd_numero)} no apareció en resultados.",
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
                        f"El FSD {fsd_display(fsd_numero)} no apareció en la lista.",
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
                        f"El FSD {fsd_display(fsd_numero)} no apareció en la lista.",
                    )
                return self._extraer_detalle(fsd_numero)

        except Exception as e:
            self._log(f"  ✗ Error inesperado en ScraperSunrun: {e}")
            return self._dict_error(fsd_numero, str(e))

        # IMPORTANTE: NO se cierra el driver porque es el Chrome del usuario.

    def navegar_a_fsd(self, fsd: str) -> dict:
        """
        Busca un FSD en Sunrun y navega hasta la página de detalle del ticket,
        SIN extraer datos.

        Usa exactamente la misma lógica de búsqueda que obtener_datos_por_fsd():
          - Conexión al Chrome existente (puerto 9222)
          - Detección de estado actual del navegador
          - Búsqueda via barra global de Salesforce
          - Navegación al detalle del ticket

        La diferencia es que se detiene en la página de detalle (no llama a
        _extraer_detalle). El navegador queda posicionado en el ticket.

        Parámetros
        ----------
        fsd : número FSD en cualquier formato ("FSD-1172172", "1172172", etc.)

        Devuelve
        --------
        dict con:
          - "ok"         : bool   — True si se llegó al detalle del ticket
          - "fsd"        : str    — FSD en formato display ("FSD-980124")
          - "mensaje"    : str    — descripción del resultado o error
          - "url"        : str    — URL final del navegador
        """
        fsd_numero = solo_digitos(fsd)

        if not fsd_numero:
            return {
                "ok": False,
                "fsd": "",
                "mensaje": f"Formato de FSD inválido: '{fsd}'",
                "url": "",
            }

        fsd_display_val = fsd_display(fsd_numero)
        self._log(f"  → Buscando FSD (solo navegación): {fsd_display_val}")

        if not self._conectar():
            return {
                "ok": False,
                "fsd": fsd_display_val,
                "mensaje": "No se pudo conectar al Chrome. ¿Está abierto con --remote-debugging-port=9222?",
                "url": "",
            }

        try:
            estado_actual = self._detectar_estado(fsd_numero)
            self._log(f"  → Estado actual del navegador: [{estado_actual}]")

            if estado_actual == "en_detalle":
                self._log(f"  ✓ Ya en la página del ticket: {fsd_display_val}")
                return {
                    "ok": True,
                    "fsd": fsd_display_val,
                    "mensaje": f"El navegador ya estaba en el detalle de {fsd_display_val}.",
                    "url": self._driver.current_url,
                }

            if estado_actual == "en_resultados":
                self._log("  ✓ Ya en resultados de búsqueda, haciendo clic en el ticket...")
                ok = self._clic_resultado(fsd_numero)
                return self._resultado_navegacion(fsd_display_val, ok)

            if estado_actual == "en_sunrun":
                self._log("  ✓ Ya en Sunrun, usando barra global de búsqueda...")
                if not self._buscar_desde_sunrun(fsd_numero):
                    self._log("  · Fallback: iniciando proceso completo...")
                    if not self._buscar_en_lista(fsd_numero):
                        return {
                            "ok": False,
                            "fsd": fsd_display_val,
                            "mensaje": "No se pudo cargar la lista de Sunrun.",
                            "url": self._driver.current_url,
                        }
                ok = self._clic_resultado(fsd_numero)
                return self._resultado_navegacion(fsd_display_val, ok)

            # "fuera" → proceso completo desde el principio
            self._log("  · Navegador fuera de Sunrun, iniciando proceso completo...")
            if not self._buscar_en_lista(fsd_numero):
                return {
                    "ok": False,
                    "fsd": fsd_display_val,
                    "mensaje": "No se pudo cargar la lista de Sunrun. Verifica que la sesión esté activa en Chrome.",
                    "url": self._driver.current_url,
                }
            ok = self._clic_resultado(fsd_numero)
            return self._resultado_navegacion(fsd_display_val, ok)

        except Exception as e:
            self._log(f"  ✗ Error inesperado en navegar_a_fsd: {e}")
            return {
                "ok": False,
                "fsd": fsd_display_val,
                "mensaje": str(e),
                "url": self._driver.current_url if self._driver else "",
            }

    def _resultado_navegacion(self, fsd_display_val: str, ok: bool) -> dict:
        """Construye el dict de resultado para el metodo navegar_a_fsd.

        Args:
            fsd_display_val: FSD en formato display ("FSD-980124").
            ok: True si se llego al detalle del ticket.

        Returns:
            Dict con ok, fsd, mensaje y url (esta ultima vacia si no hay driver).
        """
        url = self._driver.current_url if self._driver else ""
        if ok:
            self._log(f"  ✓ Ticket {fsd_display_val} abierto en el navegador.")
            return {
                "ok": True,
                "fsd": fsd_display_val,
                "mensaje": f"Ticket {fsd_display_val} encontrado y abierto en Sunrun.",
                "url": url,
            }
        self._log(f"  ✗ No se encontró el ticket {fsd_display_val}.")
        return {
            "ok": False,
            "fsd": fsd_display_val,
            "mensaje": f"No se encontró el ticket {fsd_display_val} en Sunrun.",
            "url": url,
        }

    @staticmethod
    def _dict_error(fsd_numero: str, mensaje: str) -> dict:
        """Dict con todos los campos vacíos y el error registrado."""
        return {
            "fuente": "Sunrun",
            "fsd": fsd_display(fsd_numero) if fsd_numero else "",
            "nombre": "",
            "telefono": "",
            "telefono_movil": "",
            "email": "",
            "direccion": "",
            "estado_pr": "",
            "condado": "",
            "ciudad": "",
            "codigo_postal": "",
            "dispatch_state": "",
            "appointment_date": "",
            "case_reason": "",
            "error": mensaje,
        }

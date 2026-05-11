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
"""

import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ══════════════════════════════════════════════════════════════════════
#  SELECTORES SUNRUN — actualiza aquí si el DOM cambia
# ══════════════════════════════════════════════════════════════════════

# URL de la lista de FS Dispatch
URL_LISTA_SUNRUN = (
    "https://sunrun.my.site.com/partners/s/fs-dispatch/FS_Dispatch__c/Default"
)

# ── Campo de búsqueda de la LISTA (filtra la tabla directamente) ──────
# Confirmado en DevTools: input[name='FS_Dispatch__c-search-input']
SEL_BUSQUEDA_LISTA = "input[name='FS_Dispatch__c-search-input']"

# ── Link del FSD en la tabla de resultados ────────────────────────────
# Los FSDs aparecen como <a> con texto "FSD-XXXXXXX"
# Se construye dinámicamente con el número buscado (ver _clic_resultado)

# ── Datos del cliente — XPath basados en estructura LWC de Salesforce ─
# Patrón: etiqueta span → ancestor slds-form-element → lightning-formatted-text

SELECTOR_NUMERO_FSD = "//slot[@name='primaryField']//lightning-formatted-text"

SELECTOR_NOMBRE = (
    "//span[text()='Customer Name']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_DIRECCION = (
    "//span[text()='Address']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_TELEFONO = (
    "//span[text()='Customer Phone']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_MOVIL = (
    "//span[text()='Mobile Phone']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_EMAIL = (
    "//span[text()='Customer Email']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_ESTADO = (
    "//span[text()='State']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_COUNTY = (
    "//span[text()='County']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_CIUDAD = (
    "//span[text()='City']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

SELECTOR_ZIP = (
    "//span[text()='Zip Code']"
    "/ancestor::div[contains(@class,'slds-form-element')]"
    "//lightning-formatted-text"
)

# Tiempos de espera
TIMEOUT = 15  # espera normal por elemento
TIMEOUT_LISTA = 30  # espera para que cargue la lista
PAUSA_FILTRO = 2.0  # pausa tras escribir en el buscador (SPA Aura)
PAUSA_DETALLE = 1.5  # pausa tras clic en resultado


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
        """
        try:
            opts = webdriver.ChromeOptions()
            opts.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            opts.add_experimental_option("useAutomationExtension", False)
            opts.add_argument("--disable-blink-features=AutomationControlled")

            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opts,
            )
            self._driver.execute_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
            )
            self._log("  ✓ Conectado al Chrome existente.")
            return True

        except Exception as e:
            self._log(f"  ✗ No se pudo conectar al Chrome: {e}")
            self._log("  → Abre Chrome con depuración desde el botón en SSAuto.")
            return False

    # ── Paso 1: navegar a la lista y filtrar por FSD ─────────────────

    def _buscar_en_lista(self, fsd_numero: str) -> bool:
        """
        Navega a la página de lista de FS Dispatch y filtra por el FSD.

        Usa el campo 'FS_Dispatch__c-search-input' (buscador de la lista,
        no la barra global de Salesforce) para filtrar la tabla directamente.

        Devuelve True si el campo de búsqueda cargó correctamente.
        """
        wait = WebDriverWait(self._driver, TIMEOUT_LISTA)
        fsd_display = _fsd_display(fsd_numero)

        self._log("  → Navegando a la lista de FS Dispatch...")
        self._driver.get(URL_LISTA_SUNRUN)

        # Verificar que no redirigió al login
        time.sleep(1)
        if "login" in self._driver.current_url.lower():
            self._log("  ✗ Sunrun redirigió al login.")
            self._log("  → Inicia sesión manualmente en Chrome primero.")
            return False

        # Esperar el campo de búsqueda de la lista
        try:
            campo = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_BUSQUEDA_LISTA))
            )
        except Exception:
            self._log("  ✗ El campo de búsqueda de la lista no cargó.")
            self._log(f"  → Selector: {SEL_BUSQUEDA_LISTA}")
            return False

        # Escribir el FSD y esperar que la SPA filtre la tabla
        self._log(f"  → Filtrando lista por: {fsd_display}")
        campo.clear()
        campo.send_keys(fsd_display)
        time.sleep(PAUSA_FILTRO)
        return True

    # ── Paso 2: hacer clic en el link del FSD en la tabla ────────────

    def _clic_resultado(self, fsd_numero: str) -> bool:
        """
        Hace clic en el link del FSD que aparece en la tabla filtrada.

        Estrategias en orden:
          1. <a> con texto exacto "FSD-XXXXXXX"
          2. <a> cuyo href contiene el número (ej: /fsd1172172)
          3. Cualquier elemento que contenga el texto del FSD
        """
        wait = WebDriverWait(self._driver, TIMEOUT)
        fsd_display = _fsd_display(fsd_numero)

        # Estrategia 1: texto exacto del link
        try:
            link = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//a[normalize-space(text())='{fsd_display}']")
                )
            )
            self._log(f"  → Abriendo: {fsd_display}")
            link.click()
            time.sleep(PAUSA_DETALLE)
            return True
        except Exception:
            pass

        # Estrategia 2: href parcial con el número
        try:
            link = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//a[contains(@href,'fsd{fsd_numero}') "
                        f"or contains(@href,'{fsd_numero}')]",
                    )
                )
            )
            self._log(f"  → Abriendo por href: {fsd_display}")
            link.click()
            time.sleep(PAUSA_DETALLE)
            return True
        except Exception:
            pass

        # Estrategia 3: cualquier elemento con el texto
        try:
            elem = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//*[contains(text(),'{fsd_display}') "
                        f"or contains(text(),'{fsd_numero}')]",
                    )
                )
            )
            self._log(f"  → Abriendo (texto): {fsd_display}")
            elem.click()
            time.sleep(PAUSA_DETALLE)
            return True
        except Exception:
            pass

        self._log(f"  ✗ No se encontró el FSD {fsd_display} en la lista.")
        self._log("  → Verifica que el número sea correcto y esté en tu lista activa.")
        return False

    # ── Paso 3: extraer datos del detalle del ticket ──────────────────

    def _extraer_campo(self, xpath: str, nombre: str) -> str:
        """
        Extrae el texto de un campo usando XPath.
        Devuelve "" si el elemento no existe (en vez de "No encontrado"
        para que el comparador distinga vacío de error).
        """
        try:
            wait = WebDriverWait(self._driver, TIMEOUT // 2)
            elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            texto = elem.text.strip()
            if texto:
                return texto
            # Algunos campos LWC guardan el valor en el atributo
            valor = (elem.get_attribute("value") or "").strip()
            return valor
        except Exception:
            self._log(f"  ⚠ Campo '{nombre}' no encontrado en la página.")
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
            time.sleep(1)  # pausa para campos dinámicos LWC
        except Exception:
            self._log("  ⚠ No se confirmó el ticket en la página, extrayendo igual...")

        nombre = self._extraer_campo(SELECTOR_NOMBRE, "Customer Name")
        direccion = self._extraer_campo(SELECTOR_DIRECCION, "Address")
        telefono = self._extraer_campo(SELECTOR_TELEFONO, "Customer Phone")
        movil = self._extraer_campo(SELECTOR_MOVIL, "Mobile Phone")
        email = self._extraer_campo(SELECTOR_EMAIL, "Customer Email")
        estado = self._extraer_campo(SELECTOR_ESTADO, "State")
        county = self._extraer_campo(SELECTOR_COUNTY, "County")
        ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
        zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")

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

        if not self._conectar():
            return self._dict_error(
                fsd_numero,
                "No se pudo conectar al Chrome. "
                "¿Está abierto con --remote-debugging-port=9222?",
            )

        try:
            if not self._buscar_en_lista(fsd_numero):
                return self._dict_error(
                    fsd_numero,
                    "No se pudo cargar la lista de Sunrun. "
                    "Verifica que la sesión esté activa en Chrome.",
                )

            if not self._clic_resultado(fsd_numero):
                return self._dict_error(
                    fsd_numero,
                    f"El FSD {_fsd_display(fsd_numero)} no apareció en la lista. "
                    "Verifica que el número sea correcto.",
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

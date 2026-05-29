"""
plugins/sunrun.py — Plugin de Sunrun para SSAuto.

Flujo real (portal Salesforce de Sunrun):
  1. Detectar la pestaña abierta del FSD (URL contiene 'FSD-').
  2. Hacer clic en la pestaña RELATED y esperar que cargue.
  3. Hacer clic en el botón visual "Upload Files".
  4. Enviar la ruta del archivo al input[name='fileInput'] (oculto).
  5. Esperar que el archivo aparezca listado (subida completada).
  5. Hacer clic en el botón DONE para cerrar el modal y finalizar el flujo.

Para cambiar algo de Sunrun, solo editar este archivo.
"""

from __future__ import annotations

import os
import re
import time
from typing import Callable

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import esperar_carga


class SunrunPlugin(SitioPlugin):
    """
    Plugin para subir archivos al portal de Sunrun (Salesforce Experience Cloud).

    El usuario debe tener abierta en Chrome la página del FSD correcto.
    El plugin detecta la pestaña buscando 'sunrun.my.site.com' + 'FSD-' en la URL.
    """

    # ── Metadatos ─────────────────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return "SUNRUN"

    @property
    def necesita_login(self) -> bool:
        return True

    @property
    def usar_pagina_actual(self) -> bool:
        # El SesionService NO navegará a ninguna URL fija;
        # este plugin se encarga de encontrar la pestaña correcta.
        return True

    @property
    def dominio(self) -> str:
        return "sunrun.my.site.com"

    # ── URLs y selectores ─────────────────────────────────────────────

    URL_LOGIN = "https://sunrun.my.site.com/partner/login?locale=us"
    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#Login"

    # Patrón de URL para identificar la pestaña del FSD activo
    PATRON_FSD = re.compile(r"FSD\d+", re.IGNORECASE)

    # XPath reales del portal Salesforce (de SELECTORES.HTML)
    SEL_RELATED = "//a[@role='tab' and @data-tab-name='related']"
    SEL_UPLOAD_BTN = "//span[contains(text(),'Upload Files')]"
    SEL_INPUT_FILE = "//input[@type='file' and @name='fileInput']"
    SEL_DROP_ZONE = "//*[contains(@class,'slds-file-selector__dropzone')]"

    # Confirmación: el archivo aparece listado tras la subida
    # Salesforce muestra el nombre del archivo en un <a> o <span> dentro del modal
    SEL_ARCHIVO_SUBIDO = "//span[contains(@class,'file-selector-file-name')] | //a[contains(@class,'slds-file-card')]"

    # Botón DONE — cierra el modal al finalizar la subida
    SEL_DONE = (
        "//button[not(@disabled)]"
        "[contains(@class,'uiButton--brand')]"
        "[.//span[normalize-space()='Done']]"
    )

    TIMEOUT = 15
    TIMEOUT_SUBIDA = 30

    # ── Legacy: búsqueda sin FSD específico ────────────────────────────

    def _encontrar_pestana_legacy(self, driver, log) -> bool:
        """
        Busca cualquier pestaña de Sunrun con un FSD en la URL.
        """
        handles = driver.window_handles
        log(
            f"  -> [Sunrun] Buscando pestaña FSD entre {len(handles)} "
            f"pestaña(s) abierta(s)..."
        )
        for handle in handles:
            driver.switch_to.window(handle)
            url = driver.current_url
            if self.dominio in url and self.PATRON_FSD.search(url):
                fsd_encontrado = self.PATRON_FSD.search(url).group(0).upper()
                log(
                    f"  v [Sunrun] Pestaña encontrada: {fsd_encontrado} "
                    f"- {url}"
                )
                return True

        log(
            "  x [Sunrun] No se encontro ninguna pestaña con un FSD de "
            "Sunrun abierto."
        )
        log(
            "             Asegurate de tener el FSD abierto en Chrome "
            "antes de ejecutar."
        )
        return False

    # ── Verificación de sesión ────────────────────────────────────────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """
        Busca la pestaña del FSD. Si la encuentra y no está en login, hay sesión.
        """
        if not self._encontrar_pestana_fsd(driver, log):
            return False

        url = driver.current_url.lower()
        if "login" in url or "signin" in url:
            log("  ✗ [Sunrun] La pestaña encontrada apunta a login — sesión expirada.")
            return False

        log("  ✓ [Sunrun] Sesión activa detectada.")
        return True

    # ── Login ─────────────────────────────────────────────────────────

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        """Login automático con usuario y contraseña."""
        usuario = credenciales.get("usuario", "")
        clave = credenciales.get("clave", "")
        if not usuario or not clave:
            log("  ✗ [Sunrun] Sin credenciales configuradas.")
            return False

        try:
            log("  → [Sunrun] Navegando a login…")
            driver.get(self.URL_LOGIN)
            esperar_carga(driver)
            espera = WebDriverWait(driver, self.TIMEOUT)

            espera.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_USER))
            ).send_keys(usuario)
            espera.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_PASS))
            ).send_keys(clave)
            espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_LOGIN))
            ).click()

            esperar_carga(driver, timeout=20)
            url = driver.current_url.lower()
            if "login" not in url and "signin" not in url:
                log("  ✓ [Sunrun] Login exitoso.")
                return True
            log("  ✗ [Sunrun] Login falló — sigue en la página de login.")
            return False
        except Exception as e:
            log(f"  ✗ [Sunrun] Error durante login: {e}")
            return False

    # ── Subida principal ──────────────────────────────────────────────

    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """
        Flujo completo de subida para Sunrun:
          1. Localizar pestaña del FSD (con búsqueda inteligente si se proporciona FSD).
          2. Clic en RELATED → esperar carga.
          3. Enviar ruta directamente al input file oculto (sin clic en botón visual).
             Evitamos abrir el file picker del OS — Salesforce lo cancela si el driver pierde foco.
          4. Confirmar que el archivo quedó listado.
          5. Clic en DONE para cerrar el modal y finalizar el flujo.
        """
        log = ctx.log
        driver = ctx.driver
        ruta_abs = os.path.abspath(ctx.ruta_imagen)
        fsd_objetivo = ctx.fsd  # Búsqueda inteligente por FSD

        if not os.path.isfile(ruta_abs):
            return ResultadoSubida(
                exitoso=False, mensaje=f"Archivo no encontrado: {ruta_abs}"
            )

        log(f"  → [Sunrun] Iniciando subida: {ruta_abs}")

        # Paso 1 — Localizar pestaña (con FSD inteligente si está disponible)
        if not self._encontrar_pestana_fsd(driver, log, fsd_objetivo=fsd_objetivo):
            return ResultadoSubida(
                exitoso=False,
                mensaje="No se encontró pestaña del FSD",
                detalle="Abre el FSD en Chrome antes de ejecutar la automatización.",
            )

        try:
            # Paso 2 — Clic en RELATED
            self._clic_related(driver, log)

            # Paso 3 — Enviar archivo directo al input oculto (sin abrir file picker)
            self._enviar_archivo(driver, log, ruta_abs)

            # Paso 4 — Confirmar
            ok = self._confirmar_subida(driver, log, ruta_abs)
            if ok:
                # Paso 5 — Clic en DONE para cerrar el modal
                self._clic_done(driver, log)
                return ResultadoSubida(
                    exitoso=True, mensaje="Archivo subido correctamente a Sunrun"
                )
            return ResultadoSubida(
                exitoso=False,
                mensaje="No se pudo confirmar la subida",
                detalle="Timeout esperando confirmación. Verifica manualmente en el portal.",
            )

        except Exception as e:
            log(f"  ✗ [Sunrun] Error inesperado: {e}")
            try:
                driver.save_screenshot("debug_sunrun_error.png")
                log("  · [Sunrun] Screenshot guardado: debug_sunrun_error.png")
            except Exception:
                pass
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}")

    # ── Pasos internos ────────────────────────────────────────────────

    def _clic_related(self, driver, log: Callable) -> None:
        """Hace clic en la pestaña RELATED y espera que el contenido cargue."""
        log("  → [Sunrun] Buscando pestaña RELATED…")
        espera = WebDriverWait(driver, self.TIMEOUT)
        try:
            btn_related = espera.until(
                EC.presence_of_element_located((By.XPATH, self.SEL_RELATED))
            )

            # Scroll el elemento a la vista
            driver.execute_script("arguments[0].scrollIntoView(true);", btn_related)

            # Esperar a que esté realmente clickeable
            espera.until(EC.element_to_be_clickable((By.XPATH, self.SEL_RELATED)))

            # Intentar click normal
            try:
                btn_related.click()
                log("  ✓ [Sunrun] Clic en RELATED (click normal).")
            except Exception as e:
                # Si falla por elemento interceptado, usar JavaScript click
                log(
                    f"  · [Sunrun] Click normal falló ({str(e)[:50]}...), intentando JavaScript click…"
                )
                driver.execute_script("arguments[0].click();", btn_related)
                log("  ✓ [Sunrun] Clic en RELATED (JavaScript click).")

        except TimeoutException:
            raise RuntimeError(
                "No se encontró el botón RELATED. "
                "¿Está el FSD completamente cargado en la pestaña?"
            )

        # Esperar a que aparezca la zona de Upload Files como señal de carga
        try:
            espera.until(
                EC.presence_of_element_located((By.XPATH, self.SEL_UPLOAD_BTN))
            )
            log("  ✓ [Sunrun] Sección Related cargada.")
        except TimeoutException:
            # No es fatal — la sección puede haber cargado sin ese elemento visible aún.
            # Damos una espera condicional más larga como fallback.
            log("  · [Sunrun] Upload Files no visible aún, esperando renderizado…")
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.SEL_INPUT_FILE)
                    )
                )
                log("  ✓ [Sunrun] Input file detectado tras espera.")
            except TimeoutException:
                log("  . [Sunrun] Seccion Related puede no haber cargado completamente.")

    @staticmethod
    def _mostrar_input_oculto(driver, elemento) -> None:
        """Hace visible un input file oculto para poder usar send_keys sin file picker."""
        driver.execute_script(
            "arguments[0].style.display='block';"
            "arguments[0].style.visibility='visible';"
            "arguments[0].style.opacity='1';"
            "arguments[0].style.position='fixed';"
            "arguments[0].style.top='0';"
            "arguments[0].style.left='0';",
            elemento,
        )

    @staticmethod
    def _restaurar_input_oculto(driver, elemento) -> None:
        """Restaura los estilos originales de un input file tras enviar el archivo."""
        driver.execute_script(
            "arguments[0].style.display='';"
            "arguments[0].style.visibility='';"
            "arguments[0].style.opacity='';"
            "arguments[0].style.position='';"
            "arguments[0].style.top='';"
            "arguments[0].style.left='';",
            elemento,
        )

    def _enviar_archivo(self, driver, log: Callable, ruta_abs: str) -> None:
        """
        Envía la ruta directamente al input[name='fileInput'] oculto de Salesforce,
        SIN hacer clic en el botón visual 'Upload Files'.

        Por qué: el botón visual abre el file picker nativo del OS. Cuando eso ocurre,
        Chrome pierde el foco de Selenium y Salesforce cancela la subida con el error
        "Subida cancelada: la pestaña/ventana activa perdió foco."

        Solución: hacer el input visible vía JS (solo por el tiempo del send_keys),
        enviar la ruta, y restaurar el estilo original. Salesforce procesa el archivo
        exactamente igual que si el usuario lo hubiera seleccionado desde el diálogo.
        """
        log("  → [Sunrun] Localizando input file oculto (sin abrir file picker)…")
        espera = WebDriverWait(driver, self.TIMEOUT)

        try:
            input_file = espera.until(
                EC.presence_of_element_located((By.XPATH, self.SEL_INPUT_FILE))
            )
        except TimeoutException:
            raise RuntimeError(
                "No se encontró el input file (name='fileInput'). "
                "¿La sección RELATED cargó correctamente y tiene la sección de archivos?"
            )

        # Hacer visible el input temporalmente — evita que Selenium abra
        # el file picker nativo del OS (que causaría la pérdida de foco)
        # Hacer visible el input oculto para poder enviar el archivo
        self._mostrar_input_oculto(driver, input_file)
        input_file.send_keys(ruta_abs)
        log(f"  ✓ [Sunrun] Archivo enviado: {os.path.basename(ruta_abs)}")
        self._restaurar_input_oculto(driver, input_file)

    def _clic_done(self, driver, log: Callable) -> bool:
        """
        Espera que la subida termine y hace clic en DONE.
        Retorna True si se hizo clic en el botón, False si no se encontró.
        """

        log("  → [Sunrun] Esperando que la subida finalice…")

        espera = WebDriverWait(driver, self.TIMEOUT_SUBIDA)

        try:
            # Esperar texto "1 of 1 file uploaded"
            espera.until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, "//*[contains(text(),'file uploaded')]"),
                    "1 of 1 file uploaded",
                )
            )

            log("  ✓ [Sunrun] Subida completada.")

        except TimeoutException:
            log("  ⚠ [Sunrun] No se pudo confirmar el fin de la subida.")

        log("  → [Sunrun] Buscando botón DONE habilitado…")

        try:
            btn_done = espera.until(
                EC.element_to_be_clickable((By.XPATH, self.SEL_DONE))
            )

            # Scroll por seguridad
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", btn_done
            )

            # Click JS evita overlays/intercepts de Salesforce
            driver.execute_script("arguments[0].click();", btn_done)

            log("  ✓ [Sunrun] Clic en DONE. Modal cerrado.")
            return True

        except TimeoutException:
            log("  · [Sunrun] Botón DONE no disponible — el modal puede seguir abierto.")
            return False

    def _confirmar_subida(self, driver, log: Callable, ruta_abs: str) -> bool:
        """
        Salesforce procesa el archivo tras el send_keys.
        Esperamos a que el nombre del archivo aparezca listado en el modal
        como señal de que la subida se completó.

        Si el selector específico no aparece, hace fallback a timeout fijo
        asumiendo que Salesforce procesó silenciosamente.
        """
        nombre_archivo = os.path.basename(ruta_abs)
        log(f"  → [Sunrun] Esperando confirmación de '{nombre_archivo}'…")

        # Intentar detección por nombre de archivo en el DOM
        selector_nombre = f"//span[contains(text(),'{nombre_archivo}')] | //a[contains(text(),'{nombre_archivo}')]"
        try:
            WebDriverWait(driver, self.TIMEOUT_SUBIDA).until(
                EC.presence_of_element_located((By.XPATH, selector_nombre))
            )
            log(f"  ✓ [Sunrun] Archivo '{nombre_archivo}' confirmado en el portal.")
            return True
        except TimeoutException:
            pass

        # Fallback: verificar por el selector genérico de archivo subido
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.SEL_ARCHIVO_SUBIDO))
            )
            log("  ✓ [Sunrun] Archivo subido (confirmación genérica).")
            return True
        except TimeoutException:
            log(
                "  ⚠ [Sunrun] No se detectó confirmación visual. El archivo puede haberse subido igual."
            )
            log("             Verifica manualmente en el portal si es necesario.")
            return False

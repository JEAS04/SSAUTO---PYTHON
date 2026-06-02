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
    SEL_DONE_PRINCIPAL = (
        "//button[not(@disabled)]"
        "[contains(@class,'uiButton--brand')]"
        "[.//span[normalize-space()='Done']]"
    )
    SEL_DONE_FALLBACKS = [
        "//button[not(@disabled)][contains(@class,'slds-button')][.//span[normalize-space()='Done']]",
        "//button[not(@disabled)][.//span[normalize-space()='Done']]",
        "//button[not(@disabled)][contains(text(),'Done')]",
        "//button[not(@disabled)][@title='Done']",
        "//*[@role='button'][@title='Done']",
    ]

    TIMEOUT = 15
    TIMEOUT_SUBIDA = 30

    # ── Legacy: búsqueda sin FSD específico ────────────────────────────

    def _encontrar_pestana_legacy(self, driver, log) -> bool:
        """
        Busca pestañas Sunrun con FSD en la URL usando CDP Target.getTargets,
        SIN hacer switch_to.window (que activaría tabs y falsearía el foco).

        Solo se activa una pestaña al final, con Target.activateTarget.
        """
        try:
            targets_resp = driver.execute_cdp_cmd("Target.getTargets", {})
            target_infos = targets_resp.get("targetInfos", [])
        except Exception:
            return self._encontrar_pestana_legacy_fallback(driver, log)

        candidatos = []
        for t in target_infos:
            if t.get("type") != "page":
                continue
            url = t.get("url", "")
            if self.dominio in url and self.PATRON_FSD.search(url):
                fsd = self.PATRON_FSD.search(url).group(0).upper()
                candidatos.append({"targetId": t["targetId"], "url": url, "fsd": fsd})

        if not candidatos:
            log("  x [Sunrun] No se encontro ninguna pestaña FSD de Sunrun abierta.")
            log("             Asegurate de tener el FSD abierto en Chrome antes de ejecutar.")
            return False

        try:
            handle_inicial = driver.current_window_handle
            url_inicial = driver.current_url
        except Exception:
            handle_inicial = None
            url_inicial = ""

        tiene_foco = False
        try:
            tiene_foco = driver.execute_script("return document.hasFocus()")
        except Exception:
            pass

        if tiene_foco and url_inicial and self.dominio in url_inicial and self.PATRON_FSD.search(url_inicial):
            fsd = self.PATRON_FSD.search(url_inicial).group(0).upper()
            log(f"  v [Sunrun] Pestaña con foco: {fsd}")
            return True

        if len(candidatos) == 1:
            driver.execute_cdp_cmd("Target.activateTarget", {"targetId": candidatos[0]["targetId"]})
            log(f"  v [Sunrun] Única pestaña FSD: {candidatos[0]['fsd']}")
            return True

        log(
            f"  ⚠ [Sunrun] Hay {len(candidatos)} pestañas Sunrun abiertas."
        )
        log("           Usa el campo FSD para elegir, o navega a la pestaña deseada.")
        driver.execute_cdp_cmd("Target.activateTarget", {"targetId": candidatos[0]["targetId"]})
        log(f"  v [Sunrun] Usando la primera: {candidatos[0]['fsd']}")
        return True

    def _encontrar_pestana_legacy_fallback(self, driver, log) -> bool:
        """Fallback si CDP Target.getTargets no funciona."""
        handles = driver.window_handles
        for handle in handles:
            try:
                driver.switch_to.window(handle)
                url = driver.current_url
            except Exception:
                continue
            if self.dominio in url and self.PATRON_FSD.search(url):
                fsd = self.PATRON_FSD.search(url).group(0).upper()
                log(f"  v [Sunrun] Pestaña (fallback): {fsd} - {url}")
                return True
        log("  x [Sunrun] No se encontro pestaña FSD (fallback).")
        return False

    # ── Verificación de sesión ────────────────────────────────────────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """
        Busca la pestaña del FSD. Si la encuentra y no está en login, hay sesión.
        Solo busca entre pestañas si la actual no es Sunrun.
        """
        try:
            url = driver.current_url.lower()
        except Exception:
            url = ""

        if self.dominio in url:
            if "login" in url or "signin" in url:
                log("  ✗ [Sunrun] La pestaña actual apunta a login — sesión expirada.")
                return False
            log("  ✓ [Sunrun] Sesión activa detectada.")
            return True

        if not self._encontrar_pestana_fsd(driver, log):
            return False

        try:
            url = driver.current_url.lower()
        except Exception:
            url = ""

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
        cancel = ctx.cancelado

        def _check():
            return cancel and hasattr(cancel, 'is_set') and cancel.is_set()

        if not os.path.isfile(ruta_abs):
            return ResultadoSubida(
                exitoso=False, mensaje=f"Archivo no encontrado: {ruta_abs}"
            )

        log(f"  → [Sunrun] Iniciando subida: {ruta_abs}")

        if _check():
            log("  ⚠ [Sunrun] Cancelado por el usuario.")
            return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

        # Paso 1 — Localizar pestaña (solo si se proporciona FSD explícito)
        if fsd_objetivo:
            if not self._encontrar_pestana_fsd(driver, log, fsd_objetivo=fsd_objetivo):
                return ResultadoSubida(
                    exitoso=False,
                    mensaje="No se encontró pestaña del FSD",
                    detalle="Abre el FSD en Chrome antes de ejecutar la automatización.",
                )
            if _check():
                log("  ⚠ [Sunrun] Cancelado por el usuario.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

        try:
            # Refrescar la página para limpiar cualquier modal o archivo residual
            log("  → [Sunrun] Refrescando página para limpiar estado…")
            driver.refresh()
            esperar_carga(driver, timeout=15)

            # Esperar a que Salesforce termine de inicializar sus componentes lazys
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.SEL_RELATED))
                )
                log("  ✓ [Sunrun] Componentes de Salesforce cargados.")
            except TimeoutException:
                log("  ⚠ [Sunrun] RELATED no detectado tras refresh — continuando igual.")

            # Paso 2 — Clic en RELATED
            self._clic_related(driver, log)

            if _check():
                log("  ⚠ [Sunrun] Cancelado antes de enviar archivo.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # Paso 3 — Enviar archivo directo al input oculto (sin abrir file picker)
            self._enviar_archivo(driver, log, ruta_abs)

            if _check():
                log("  ⚠ [Sunrun] Cancelado antes de confirmar subida.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # Paso 4 — Confirmar
            ok = self._confirmar_subida(driver, log, ruta_abs)
            if ok:
                if _check():
                    log("  ⚠ [Sunrun] Cancelado antes de cerrar modal.")
                    return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

                # Paso 5 — Clic en DONE para cerrar el modal
                done_ok = self._clic_done(driver, log)
                if done_ok:
                    return ResultadoSubida(
                        exitoso=True, mensaje="Archivo subido correctamente a Sunrun"
                    )
                return ResultadoSubida(
                    exitoso=False,
                    mensaje="No se pudo cerrar el modal (DONE no disponible).",
                    detalle="El archivo puede haberse subido. Verifica manualmente.",
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

    def _cerrar_modal_residual(self, driver, log: Callable) -> None:
        """Cierra cualquier modal de subida que haya quedado abierto de intentos previos."""
        cerrar_selectors = [
            "//button[contains(@class,'uiButton')][.//span[contains(text(),'Cancel')]]",
            "//button[not(@disabled)][.//span[normalize-space()='Cancel']]",
            "//button[contains(@class,'uiButton--default')][.//span[normalize-space()='Close']]",
            "//button[contains(@title,'Cancel')]",
            "//button[contains(@title,'Close')]",
            "//button[contains(@class,'close')]",
            "//*[@aria-label='Close']",
        ]
        for sel in cerrar_selectors:
            try:
                btn = driver.find_element(By.XPATH, sel)
                driver.execute_script("arguments[0].click();", btn)
                log("  · [Sunrun] Modal residual cerrado.")
                time.sleep(0.5)
                return
            except Exception:
                continue

        try:
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception:
            pass

    def _clic_related(self, driver, log: Callable) -> None:
        """Hace clic en la pestaña RELATED y espera que el contenido cargue.
        Primero cierra cualquier modal abierto de subidas anteriores."""
        log("  → [Sunrun] Buscando pestaña RELATED…")

        # Limpiar modal residual de subidas previas fallidas
        self._cerrar_modal_residual(driver, log)

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

        # Esperar a que el dropzone esté visible = componente de upload completamente inicializado
        # En primera carga, Salesforce puede mostrar el input pero no tener los handlers listos
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.SEL_DROP_ZONE))
            )
            log("  ✓ [Sunrun] Dropzone visible — componente listo.")
        except TimeoutException:
            log("  · [Sunrun] Dropzone no visible, continuando de todos modos…")

        self._mostrar_input_oculto(driver, input_file)
        input_file.send_keys(ruta_abs)
        log(f"  ✓ [Sunrun] Archivo enviado: {os.path.basename(ruta_abs)}")
        self._restaurar_input_oculto(driver, input_file)

    def _clic_done(self, driver, log: Callable) -> bool:
        """
        Espera que la subida termine y hace clic en DONE.
        Retorna True si se hizo clic, False si no se pudo cerrar el modal.
        """
        log("  → [Sunrun] Esperando que la subida finalice…")

        # 1. Esperar cualquier indicio de subida completada (texto flexible)
        try:
            WebDriverWait(driver, self.TIMEOUT_SUBIDA).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(),'file uploaded') or contains(text(),'uploaded')]")
                )
            )
            log("  ✓ [Sunrun] Subida completada (texto detectado).")
            time.sleep(3)
            self._esperar_fin_carga_upload(driver, log)
        except TimeoutException:
            log("  ⚠ [Sunrun] No se detectó texto de subida completada.")
            log("     Intentando cerrar modal de todos modos…")

        # 2. Buscar botón DONE con múltiples estrategias
        log("  → [Sunrun] Buscando botón DONE…")

        todos_selectores = [self.SEL_DONE_PRINCIPAL] + self.SEL_DONE_FALLBACKS

        for i, sel in enumerate(todos_selectores):
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                log(f"  ✓ [Sunrun] Clic en DONE ({'principal' if i == 0 else f'fallback #{i}'}).")
                return True
            except TimeoutException:
                continue
            except Exception:
                continue

        # 3. Fallback final: intentar cerrar modal con Escape o click en X
        log("  ⚠ [Sunrun] Botón DONE no encontrado con ningún selector.")
        try:
            from selenium.webdriver.common.keys import Keys
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            log("  · [Sunrun] Intentando cerrar modal con Escape.")
            time.sleep(1)
            return True
        except Exception:
            pass

        # 4. Intentar click en botón Cancel o X genérico
        cancel_selectors = [
            "//button[contains(@class,'uiButton')][.//span[contains(text(),'Cancel')]]",
            "//button[contains(@title,'Cancel')]",
            "//button[contains(@title,'Close')]",
            "//button[contains(@class,'close')]",
            "//*[@aria-label='Close']",
        ]
        for sel in cancel_selectors:
            try:
                btn = driver.find_element(By.XPATH, sel)
                driver.execute_script("arguments[0].click();", btn)
                log(f"  · [Sunrun] Modal cerrado con botón cancel/close.")
                time.sleep(1)
                return True
            except Exception:
                continue

        log("  · [Sunrun] No se pudo cerrar el modal automáticamente.")
        return False

    def _esperar_fin_carga_upload(self, driver, log: Callable) -> None:
        """
        Espera a que cualquier spinner o barra de progreso de subida desaparezca.
        Salesforce procesa el archivo en background incluso después de mostrar
        '1 of 1 file uploaded'; si se cierra el modal antes de que termine,
        el archivo no queda asociado al registro.
        """
        spinners = [
            "//div[contains(@class,'spinner') and contains(@class,'slds-is-relative')]",
            "//div[contains(@class,'slds-progress-bar')]",
            "//div[@role='progressbar']",
            "//div[contains(@class,'slds-spinner')]",
        ]
        for xpath in spinners:
            try:
                WebDriverWait(driver, 10).until_not(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                log("  ✓ [Sunrun] Carga finalizada (spinner desapareció).")
                return
            except TimeoutException:
                continue
        log("  · [Sunrun] No se detectó spinner de carga — continuando.")

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

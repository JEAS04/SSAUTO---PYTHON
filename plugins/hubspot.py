"""
plugins/hubspot.py — Plugin de HubSpot para SSAuto.

Encapsula TODO lo específico de HubSpot:
  - URLs y selectores CSS.
  - Lógica de subida de captura a nota.
  - Verificación de sesión.

Para cambiar algo de HubSpot, solo editar este archivo.
Para agregar un sitio nuevo, copiar este archivo y adaptarlo.

No importa nada de la UI (sin CustomTkinter, sin tkinter).
"""

from __future__ import annotations

import os
import time
from functools import wraps
from typing import Callable

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import esperar_carga


def _retry_stale(max_intentos: int = 3, pausa: float = 0.3):
    """Decorador: reintenta si el elemento queda obsoleto (DOM dinámico)."""

    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            ultimo = None
            for _ in range(max_intentos):
                try:
                    return fn(*args, **kwargs)
                except StaleElementReferenceException as e:
                    ultimo = e
                    time.sleep(pausa)
            raise ultimo

        return wrapper

    return deco


class HubSpotPlugin(SitioPlugin):
    """
    Plugin para subir capturas como nota adjunta en HubSpot.

    Flujo:
      Actividades → Notas → Crear nota → Adjuntar → input file → Guardar
    """

    # ── Metadatos ─────────────────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return "HUBSPOT"

    @property
    def necesita_login(self) -> bool:
        return True

    @property
    def usar_pagina_actual(self) -> bool:
        return True

    @property
    def dominio(self) -> str:
        return "app.hubspot.com"

    # ── Selectores (todo en un solo lugar) ────────────────────────────

    URL_LOGIN = "https://app.hubspot.com/login/"
    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#loginBtn"

    SEL_TAB_ACTIVIDADES = 'a[data-tab-id="1"]'
    SEL_TAB_ACTIVIDADES_FB = 'a[data-tab-link="true"]'
    SEL_TAB_NOTAS = '[data-test-id="timeline-tab-filter-notes"]'
    SEL_BTN_CREAR_NOTA = 'button[data-selenium-test="create-engagement-note-button"]'
    SEL_BTN_ADJUNTAR = '[data-test-id="select-file-dropdown"]'
    SEL_INPUT_FILE = 'input[type="file"]'
    SEL_EDITOR = '[data-test-id="rte-content"]'
    SEL_EDITOR_ALT = 'div.ProseMirror[contenteditable="true"]'
    SEL_BTN_GUARDAR = '[data-test-id="activity-creator-window-footer-save-button"]'

    # XPaths de fallback para la pestaña Actividades (orden de intento)
    XPATH_ACTIVIDADES = [
        "//a[contains(@data-tab-id,'activity') or contains(@data-tab-id,'1')]",
        "//a[contains(@href,'activity') and contains(@class,'tab')]",
        "//a[contains(text(),'Actividades') or contains(text(),'Activities')]",
        "//button[contains(text(),'Actividades') or contains(text(),'Activities')]",
        "//*[@role='tab' and (contains(text(),'Actividades') or contains(text(),'Activities'))]",
        "//a[contains(@aria-label,'Activities') or contains(@aria-label,'Actividades')]",
    ]

    # XPaths de fallback para el filtro Notas
    XPATH_NOTAS = [
        "//button[contains(text(),'Notas') or contains(text(),'Notes')]",
        "//a[contains(text(),'Notas') or contains(text(),'Notes')]",
        "//*[contains(@data-test-id,'note') or contains(@data-test-id,'Note')]",
        "//*[contains(@aria-label,'Note') or contains(@aria-label,'Nota')]",
        "//span[contains(text(),'Notas') or contains(text(),'Notes')]/..",
    ]

    TIMEOUT = 15
    TIMEOUT_LARGO = 20

    # ── Interfaz pública ──────────────────────────────────────────────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        try:
            url = driver.current_url.lower()
            if "hubspot" in url:
                log("  ✓ [HubSpot] Sesión activa detectada.")
                return True
            log("  ⚠ [HubSpot] No estamos en HubSpot.")
            return False
        except Exception:
            return False

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        usuario = credenciales.get("usuario", "")
        clave = credenciales.get("clave", "")
        if not usuario or not clave:
            log("  ✗ [HubSpot] Sin credenciales para login automático.")
            return False
        try:
            log(f"  → [HubSpot] Navegando a login...")
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
            if (
                "hubspot" in driver.current_url.lower()
                and "login" not in driver.current_url.lower()
            ):
                log("  ✓ [HubSpot] Login exitoso.")
                return True
            log("  ✗ [HubSpot] Login falló — URL no cambió como se esperaba.")
            return False
        except Exception as e:
            log(f"  ✗ [HubSpot] Error en login: {e}")
            return False

    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """Sube la captura como archivo adjunto en una nueva nota de HubSpot."""
        log = ctx.log
        driver = ctx.driver
        ruta_abs = os.path.abspath(ctx.ruta_imagen)
        auto_submit = ctx.opciones.get("auto_submit_nota", True)
        fsd_objetivo = ctx.fsd  # Búsqueda inteligente por FSD

        # Búsqueda inteligente: si hay FSD, buscar pestaña correcta
        if fsd_objetivo and not self._encontrar_pestana_fsd(driver, log, fsd_objetivo):
            log(f"  ✗ [HubSpot] No se pudo encontrar pestaña para FSD: {fsd_objetivo}")
            return ResultadoSubida(
                exitoso=False,
                mensaje="No se encontró pestaña del FSD",
                detalle="Abre el ticket de HubSpot en Chrome antes de ejecutar.",
            )

        contexto_activo = self._capturar_contexto_activo(driver, fsd_objetivo)

        log(f"  → [HubSpot] Iniciando subida: {ruta_abs}")
        esperar_carga(driver)

        try:
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_actividades(driver, log, contexto_activo)
            self._paso_notas(driver, log, contexto_activo)
            self._paso_crear_nota(driver, log, contexto_activo)
            self._paso_editor(driver, log, contexto_activo)
            self._paso_adjuntar(driver, log, ruta_abs, contexto_activo)
            self._paso_esperar_archivo(driver, log, ruta_abs, contexto_activo)

            if not auto_submit:
                log("  ✓ [HubSpot] Archivo adjunto. Guardado manual pendiente.")
                return ResultadoSubida(
                    exitoso=True, mensaje="Archivo adjunto (guardado manual)"
                )

            self._paso_guardar(driver, log, contexto_activo)
            return ResultadoSubida(exitoso=True, mensaje="Nota guardada correctamente")

        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}", detalle=str(e))

    # ── Pasos internos ────────────────────────────────────────────────

    def _espera(self, driver) -> WebDriverWait:
        return WebDriverWait(driver, self.TIMEOUT)

    def _es_pagina_registro(self, url: str) -> bool:
        url = url.lower()
        return ("/ticket/" in url or "/contact/" in url
                or "/company/" in url or "/deal/" in url
                or "/record/" in url or "contacts/" in url)

    def _capturar_contexto_activo(self, driver, fsd_objetivo: str | None = None) -> dict:
        url = driver.current_url.lower()
        if self.dominio not in url:
            raise RuntimeError("La pestaña activa no es HubSpot. Subida cancelada.")

        if self._es_pagina_registro(url):
            ctx = {
                "handle": driver.current_window_handle,
                "url": url,
                "title": driver.title,
            }
            self._validar_contexto_activo(driver, ctx)
            return ctx

        handle_actual = driver.current_window_handle
        for handle in driver.window_handles:
            if handle == handle_actual:
                continue
            try:
                driver.switch_to.window(handle)
                if self._es_pagina_registro(driver.current_url):
                    ctx = {
                        "handle": driver.current_window_handle,
                        "url": driver.current_url.lower(),
                        "title": driver.title,
                    }
                    self._validar_contexto_activo(driver, ctx)
                    return ctx
            except Exception:
                continue

        driver.switch_to.window(handle_actual)
        raise RuntimeError(
            "No se encontró ninguna pestaña de un registro (ticket/contacto). "
            "Abre el ticket de HubSpot en Chrome antes de ejecutar."
        )

    def _validar_contexto_activo(self, driver, ctx: dict) -> None:
        try:
            misma_tab = driver.current_window_handle == ctx["handle"]
            url_ok = self.dominio in driver.current_url.lower()
        except Exception as e:
            raise RuntimeError(f"No se pudo validar pestaña activa: {e}") from e

        if not misma_tab or not url_ok:
            raise RuntimeError(
                "Subida cancelada: cambiaste de pestaña/ventana de HubSpot. "
                "No se subió información."
            )

    def _safe_click(self, driver, elemento, ctx: dict) -> None:
        self._validar_contexto_activo(driver, ctx)
        elemento.click()
        self._validar_contexto_activo(driver, ctx)

    def _safe_send_file(self, driver, elemento, ruta_abs: str, ctx: dict) -> None:
        self._validar_contexto_activo(driver, ctx)
        elemento.send_keys(ruta_abs)
        self._validar_contexto_activo(driver, ctx)

    @staticmethod
    def _guardar_dom(driver, nombre: str) -> None:
        try:
            ruta = f"debug_dom_hubspot_{nombre}.html"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass

    def _paso_actividades(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 1/7: Pestaña Actividades…")

        selectores = [
            (By.CSS_SELECTOR, self.SEL_TAB_ACTIVIDADES, "CSS primary"),
            (By.CSS_SELECTOR, self.SEL_TAB_ACTIVIDADES_FB, "CSS fallback"),
        ] + [(By.XPATH, xp, f"XPath {i+1}") for i, xp in enumerate(self.XPATH_ACTIVIDADES)]

        for by, sel, label in selectores:
            try:
                tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((by, sel))
                )
                self._safe_click(driver, tab, ctx)
                log(f"  ✓ [HubSpot] Pestaña Actividades abierta ({label}).")
                return
            except (TimeoutException, NoSuchElementException):
                continue
            except Exception:
                continue

        # Fallback JS: buscar por texto visible
        try:
            encontrado = driver.execute_script("""
                var textos = ['Actividades', 'Activities'];
                var todos = document.querySelectorAll('a, button, [role="tab"]');
                for (var i = 0; i < todos.length; i++) {
                    var t = todos[i].textContent.trim();
                    for (var j = 0; j < textos.length; j++) {
                        if (t === textos[j] || t.startsWith(textos[j])) {
                            if (todos[i].offsetParent !== null) {
                                todos[i].click();
                                return true;
                            }
                        }
                    }
                }
                return false;
            """)
            if encontrado:
                log("  ✓ [HubSpot] Pestaña Actividades abierta (JS fallback).")
                return
        except Exception:
            pass

        self._guardar_dom(driver, "actividades")
        log("  · [HubSpot] Actividades no encontrado, continuando igual.")

    def _paso_notas(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 2/7: Pestaña Notas…")

        selectores = [
            (By.CSS_SELECTOR, self.SEL_TAB_NOTAS, "CSS primary"),
        ] + [(By.XPATH, xp, f"XPath {i+1}") for i, xp in enumerate(self.XPATH_NOTAS)]

        for by, sel, label in selectores:
            try:
                tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((by, sel))
                )
                self._safe_click(driver, tab, ctx)
                log(f"  ✓ [HubSpot] Pestaña Notas abierta ({label}).")
                return
            except (TimeoutException, NoSuchElementException):
                continue
            except Exception:
                continue

        # Fallback JS: buscar por texto visible
        try:
            encontrado = driver.execute_script("""
                var textos = ['Notas', 'Notes', 'Note', 'Nota'];
                var todos = document.querySelectorAll('a, button, span, [role="tab"]');
                for (var i = 0; i < todos.length; i++) {
                    var t = todos[i].textContent.trim();
                    for (var j = 0; j < textos.length; j++) {
                        if (t === textos[j] || t.startsWith(textos[j])) {
                            if (todos[i].offsetParent !== null) {
                                todos[i].click();
                                return true;
                            }
                        }
                    }
                }
                return false;
            """)
            if encontrado:
                log("  ✓ [HubSpot] Pestaña Notas abierta (JS fallback).")
                return
        except Exception:
            pass

        self._guardar_dom(driver, "notas")
        raise RuntimeError(
            "No se pudo abrir pestaña Notas. DOM guardado en debug_dom_hubspot_notas.html"
        )

    def _paso_crear_nota(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 3/7: Crear nota…")
        try:
            btn = self._espera(driver).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_CREAR_NOTA))
            )
            self._safe_click(driver, btn, ctx)
            esperar_carga(driver, timeout=5)
            log("  ✓ [HubSpot] Nueva nota creada.")
        except Exception as e:
            raise RuntimeError(f"No se pudo crear nota: {e}") from e

    def _paso_editor(self, driver, log: Callable, ctx: dict) -> None:
        """
        Da foco al editor e inserta texto vía JS para que React habilite el toolbar.
        Sin este paso el FileButton no aparece en el DOM.
        """
        log("  → [HubSpot] Paso 4/7: Enfocando editor…")
        editor_ok = False
        for sel, label in [
            (self.SEL_EDITOR, "principal"),
            (self.SEL_EDITOR_ALT, "alternativo"),
        ]:
            if editor_ok:
                break
            try:
                editor = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                )
                self._safe_click(driver, editor, ctx)
                self._validar_contexto_activo(driver, ctx)
                driver.execute_script(
                    """
                    var el = arguments[0];
                    el.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, 'Nota de captura.');
                    ['input', 'change', 'keyup'].forEach(function(t) {
                        el.dispatchEvent(new Event(t, { bubbles: true }));
                    });
                """,
                    editor,
                )
                self._validar_contexto_activo(driver, ctx)
                log(f"  ✓ [HubSpot] Editor enfocado ({label}).")
                editor_ok = True
            except Exception as e:
                log(f"  · [HubSpot] Editor {label} no encontrado: {e}")

        if not editor_ok:
            log("  ⚠ [HubSpot] Editor no localizado. El FileButton puede no aparecer.")

    def _paso_adjuntar(self, driver, log: Callable, ruta_abs: str, ctx: dict) -> None:
        log("  → [HubSpot] Paso 5/7: Adjuntando archivo…")
        try:
            btn = WebDriverWait(driver, self.TIMEOUT_LARGO).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_ADJUNTAR))
            )
            self._safe_click(driver, btn, ctx)
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_INPUT_FILE))
            )
            self._safe_send_file(driver, file_input, ruta_abs, ctx)
            log(f"  ✓ [HubSpot] Archivo enviado al input.")
        except Exception as e:
            # Guardar DOM para diagnóstico antes de propagar el error
            try:
                with open("debug_dom_hubspot.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                log("  · [HubSpot] DOM guardado en debug_dom_hubspot.html")
            except Exception:
                pass
            raise RuntimeError(f"No se pudo adjuntar el archivo: {e}") from e

    def _paso_esperar_archivo(
        self, driver, log: Callable, ruta_abs: str, ctx: dict
    ) -> None:
        log("  → [HubSpot] Paso 6/7: Esperando confirmación de archivo…")
        nombre = os.path.basename(ruta_abs)
        try:
            WebDriverWait(driver, 15).until(
                lambda d: (self._validar_contexto_activo(d, ctx) is None)
                and (
                    d.find_elements(
                        By.XPATH, f"//*[contains(text(),'{nombre}')]"
                    )
                    or d.find_elements(
                        By.XPATH, f"//*[contains(@title,'{nombre}')]"
                    )
                )
            )
            log(f"  ✓ [HubSpot] Archivo '{nombre}' confirmado en página.")
        except TimeoutException:
            log(
                "  · [HubSpot] No se confirmó el archivo en DOM (puede estar listo igual)."
            )

    def _paso_guardar(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 7/7: Guardando nota…")

        def _boton_habilitado(d):
            self._validar_contexto_activo(d, ctx)
            try:
                el = d.find_element(By.CSS_SELECTOR, self.SEL_BTN_GUARDAR)
                if el.get_attribute("aria-disabled") == "true":
                    return False
                if el.get_attribute("disabled") is not None:
                    return False
                return el
            except NoSuchElementException:
                return False

        try:
            btn = WebDriverWait(driver, self.TIMEOUT_LARGO).until(_boton_habilitado)
            log("  ✓ [HubSpot] Botón guardar habilitado.")
            self._safe_click(driver, btn, ctx)
            log("  ✓ [HubSpot] Nota guardada.")
        except Exception as e:
            try:
                driver.save_screenshot("debug_error_hubspot_save.png")
            except Exception:
                pass
            raise RuntimeError(f"No se pudo guardar la nota: {e}") from e

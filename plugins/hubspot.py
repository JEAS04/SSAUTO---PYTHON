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
    Plugin para subir capturas como imagen(es) incrustada(s) en una nota de HubSpot.

    Soporta hasta 2 imagenes (ctx.rutas_imagenes) en una sola nota, con <br>
    entre cada una para evitar reemplazos. Si hay una sola imagen, usa
    ctx.ruta_imagen (comportamiento clasico).

    Flujo de subida:
      1. Intentar crear nota desde el sidebar (funciona en ticket y contacto).
      2. Si falla: navegar Actividades → Notas → Crear nota.
      3. Enfocar el editor de texto para que React renderice la toolbar.
      4. Insertar cada imagen via el input file oculto (sin abrir file picker).
      5. Esperar confirmacion visual de cada imagen via selector <img>.
      6. Guardar la nota o dejarla abierta segun ctx.opciones["auto_submit_nota"].

    Soporta busqueda inteligente de pestanas por FSD usando CDP para evitar
    activar pestanas innecesarias y mantener el contexto correcto.
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
    SEL_BTN_INSERTAR_IMAGEN = '[data-test-id="image-upload-toggle"]'
    SEL_INPUT_FILE = 'input[type="file"]'
    SEL_BTN_NOTA_SIDEBAR = 'button[data-selenium-test="create-engagement-note-button"]'
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
        """Verifica si la pestaña actual del driver esta en HubSpot.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.

        Returns:
            True si la URL actual contiene 'hubspot'.
        """
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
        """Navega a la pagina de login de HubSpot y autentica con credenciales.

        Args:
            driver: instancia de Selenium WebDriver.
            credenciales: dict con claves "usuario" y "clave".
            log: funcion callback para registrar mensajes.

        Returns:
            True si tras el login la URL contiene 'hubspot' sin 'login'.
        """
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
        """Sube la(s) captura(s) como imagen(es) incrustada(s) en una nota de HubSpot.

        Si ctx.rutas_imagenes tiene múltiples rutas, todas se insertan en la
        misma nota. Si no, usa ctx.ruta_imagen (comportamiento clásico).

        Flujo:
          1. Intentar crear nota desde el sidebar.
          2. Si falla, navegar Actividades → Notas → Crear nota.
          3. Enfocar editor.
          4. Insertar cada imagen con confirmación.
          5. Guardar o dejar abierta según auto_submit.
        """
        log = ctx.log
        driver = ctx.driver
        rutas = ctx.rutas_imagenes if ctx.rutas_imagenes else [ctx.ruta_imagen]
        total = len(rutas)
        auto_submit = ctx.opciones.get("auto_submit_nota", True)
        mensaje_nota = ctx.opciones.get("mensaje_nota", "") or "Nota de captura."
        fsd_objetivo = ctx.fsd
        cancel = ctx.cancelado

        def _check():
            return cancel and hasattr(cancel, "is_set") and cancel.is_set()

        if _check():
            log("  ⚠ [HubSpot] Cancelado por el usuario.")
            return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

        if fsd_objetivo and not self._encontrar_pestana_fsd(driver, log, fsd_objetivo):
            log(f"  ✗ [HubSpot] No se pudo encontrar pestaña para FSD: {fsd_objetivo}")
            return ResultadoSubida(
                exitoso=False,
                mensaje="No se encontró pestaña del FSD",
                detalle="Abre el ticket de HubSpot en Chrome antes de ejecutar.",
            )

        contexto_activo = self._capturar_contexto_activo(driver, log, fsd_objetivo)

        if total > 1:
            log(f"  → [HubSpot] Iniciando subida de {total} imágenes…")
        else:
            log(f"  → [HubSpot] Iniciando subida: {os.path.abspath(rutas[0])}")
        esperar_carga(driver)

        try:
            if _check():
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._validar_contexto_activo(driver, contexto_activo)

            # Paso 1: intentar crear nota via sidebar (funciona en ticket y contacto)
            nota_creada = self._paso_crear_nota_directa(driver, log, contexto_activo)

            # Si el sidebar no funciono, navegar por pestañas
            if not nota_creada:
                if _check():
                    return ResultadoSubida(
                        exitoso=False, mensaje="Cancelado por el usuario."
                    )
                self._paso_actividades(driver, log, contexto_activo)

                if _check():
                    return ResultadoSubida(
                        exitoso=False, mensaje="Cancelado por el usuario."
                    )
                self._paso_notas(driver, log, contexto_activo)

                if _check():
                    return ResultadoSubida(
                        exitoso=False, mensaje="Cancelado por el usuario."
                    )
                self._paso_crear_nota(driver, log, contexto_activo)

            if _check():
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_editor(driver, log, contexto_activo, mensaje_nota)

            if _check():
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            # Insertar todas las imágenes en la misma nota
            for i, ruta in enumerate(rutas):
                ruta_abs = os.path.abspath(ruta)
                if total > 1:
                    log(f"  → [HubSpot] Insertando imagen {i+1}/{total}…")
                self._paso_insertar_imagen(driver, log, ruta_abs, contexto_activo)

                if _check():
                    return ResultadoSubida(
                        exitoso=False, mensaje="Cancelado por el usuario."
                    )

                self._paso_esperar_imagen(driver, log, ruta_abs, contexto_activo)

                # Separar imágenes con salto de línea (evita que la siguiente reemplace)
                if i < total - 1:
                    try:
                        driver.execute_script(
                            """
                            var sel = window.getSelection();
                            if (sel.rangeCount) {
                                var range = sel.getRangeAt(0);
                                range.collapse(false);
                            }
                            document.execCommand('insertHTML', false, '<br>');
                            """
                        )
                        time.sleep(0.3)
                    except Exception:
                        pass

            if not auto_submit:
                if total > 1:
                    log(f"  ✓ [HubSpot] {total} imágenes insertadas. Guardado manual pendiente.")
                    return ResultadoSubida(
                        exitoso=True, mensaje=f"{total} imágenes insertadas (guardado manual)"
                    )
                else:
                    log("  ✓ [HubSpot] Imagen insertada. Guardado manual pendiente.")
                    return ResultadoSubida(
                        exitoso=True, mensaje="Imagen insertada (guardado manual)"
                    )

            if _check():
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_guardar(driver, log, contexto_activo)
            return ResultadoSubida(exitoso=True, mensaje="Nota guardada correctamente")

        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}", detalle=str(e))

    # ── Pasos internos ────────────────────────────────────────────────

    def _espera(self, driver) -> WebDriverWait:
        """Crea un WebDriverWait con el timeout estandar del plugin.

        Args:
            driver: instancia de Selenium WebDriver.

        Returns:
            WebDriverWait configurado con self.TIMEOUT.
        """
        return WebDriverWait(driver, self.TIMEOUT)

    def _es_pagina_registro(self, url: str) -> bool:
        """Determina si una URL de HubSpot apunta a un registro (ticket/contacto/company/deal).

        Args:
            url: URL completa de HubSpot en minusculas.

        Returns:
            True si la URL contiene /ticket/, /contact/, /company/, /deal/ o /record/.
        """
        url = url.lower()
        return (
            "/ticket/" in url
            or "/contact/" in url
            or "/company/" in url
            or "/deal/" in url
            or "/record/" in url
            or "contacts/" in url
        )

    def _despertar_pestana_cdp(self, driver, target_id: str, log: Callable) -> bool:
        """
        Fuerza la inicialización del Runtime context de una pestaña via CDP.
        Retorna True si la pestaña respondió correctamente.
        """
        try:
            # 1. Traer la pestaña al frente
            driver.execute_cdp_cmd("Target.activateTarget", {"targetId": target_id})
            time.sleep(0.4)

            # 2. Adjuntar una sesión CDP con flatten=True — esto es lo que crea el Runtime
            session = driver.execute_cdp_cmd(
                "Target.attachToTarget", {"targetId": target_id, "flatten": True}
            )
            session_id = session.get("sessionId")
            if not session_id:
                log("  · [HubSpot] CDP: no se obtuvo sessionId.")
                return False

            # 3. Activar el Runtime en esa sesión
            driver.execute_cdp_cmd("Runtime.enable", {})
            time.sleep(0.3)

            # 4. Validar que el contexto responde
            result = driver.execute_cdp_cmd(
                "Runtime.evaluate", {"expression": "document.readyState"}
            )
            estado = result.get("result", {}).get("value", "")
            log(f"  · [HubSpot] CDP Runtime activo. readyState: {estado}")
            return True

        except Exception as e:
            log(f"  · [HubSpot] _despertar_pestana_cdp falló: {str(e)[:100]}")
            return False

    def _capturar_contexto_activo(
        self, driver, log: Callable, fsd_objetivo: str | None = None
    ) -> dict:
        """Busca y activa una pestana de HubSpot que contenga un registro.

        Usa CDP Target.getTargets para encontrar la pestana correcta, la
        despierta via CDP Runtime.evaluate, y retorna un dict con handle,
        url y title del contexto activo.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            fsd_objetivo: FSD a buscar en el titulo de la pestana (opcional).

        Returns:
            dict con claves "handle", "url", "title" del contexto activo.

        Raises:
            RuntimeError: si no se encuentra ninguna pestana de registro.
        """
        # Estrategia 1: CDP Target.getTargets — buscar y activar pestaña HubSpot
        try:
            targets_resp = driver.execute_cdp_cmd("Target.getTargets", {})
            for t in targets_resp.get("targetInfos", []):
                if t.get("type") != "page":
                    continue
                url = t.get("url", "").lower()
                title = t.get("title", "")
                if url:
                    log(f"  · [HubSpot] CDP: {title[:60]} ({url[:80]})")
                if self.dominio in url and self._es_pagina_registro(url):
                    log(f"  · [HubSpot] ✓ encontrada en CDP: {title[:60]}")

                    self._despertar_pestana_cdp(driver, t["targetId"], log)
                    time.sleep(0.5)

                    for handle in driver.window_handles:
                        try:
                            driver.switch_to.window(handle)
                            time.sleep(0.2)
                            url_actual = driver.current_url.lower()
                            if self.dominio in url_actual:
                                ctx = {
                                    "handle": handle,
                                    "url": driver.current_url,
                                    "title": driver.title,
                                }
                                log(f"  ✓ [HubSpot] Contexto activo: {handle}")
                                return ctx
                        except Exception as e:
                            if "no such execution context" in str(e).lower():
                                try:
                                    driver.execute_cdp_cmd("Runtime.enable", {})
                                    time.sleep(0.3)
                                    driver.switch_to.window(handle)
                                    time.sleep(0.2)
                                    url_actual = driver.current_url.lower()
                                    if self.dominio in url_actual:
                                        ctx = {
                                            "handle": handle,
                                            "url": driver.current_url,
                                            "title": driver.title,
                                        }
                                        log(f"  ✓ [HubSpot] Contexto activo (wake): {handle}")
                                        return ctx
                                except Exception:
                                    pass
                            continue

                    log(f"  · [HubSpot] No se pudo hacer switch a la pestaña CDP.")

        except Exception as e:
            log(f"  · [HubSpot] CDP falló: {str(e)[:80]}")

        raise RuntimeError(
            "No se encontró ninguna pestaña de un registro (ticket/contacto). "
            "Abre el ticket de HubSpot en Chrome antes de ejecutar."
        )

    def _validar_contexto_activo(self, driver, ctx: dict) -> None:
        """Verifica que el driver siga apuntando a una pestaña de HubSpot.

        Si la pestaña actual no coincide, intenta volver a la pestaña
        guardada en ctx['handle']. Lanza RuntimeError si no es posible.

        Args:
            driver: instancia de Selenium WebDriver.
            ctx: dict con al menos la clave "handle" (window handle) y
                opcionalmente "url".

        Raises:
            RuntimeError: si la pestaña actual no es de HubSpot tras reintentos.
        """
        url_conocida = ctx.get("url", "")
        if url_conocida and self.dominio in url_conocida:
            try:
                if self.dominio in driver.current_url.lower():
                    return
                driver.switch_to.window(ctx["handle"])
                if self.dominio in driver.current_url.lower():
                    return
            except Exception:
                pass

        for intento in range(3):
            try:
                url = driver.current_url.lower()
                if url and self.dominio not in url:
                    raise RuntimeError(
                        "Subida cancelada: cambiaste de pestaña/ventana de HubSpot."
                    )
                return
            except RuntimeError:
                raise
            except Exception:
                if intento < 2:
                    time.sleep(0.5)
                    try:
                        driver.switch_to.window(ctx["handle"])
                    except Exception:
                        pass

    def _safe_click(self, driver, elemento, ctx: dict) -> None:
        """Hace click en un elemento WebElement validando contexto antes y despues.

        Args:
            driver: instancia de Selenium WebDriver.
            elemento: WebElement sobre el que hacer click.
            ctx: dict con el contexto activo para validar.
        """
        self._validar_contexto_activo(driver, ctx)
        elemento.click()
        self._validar_contexto_activo(driver, ctx)

    def _safe_send_file(self, driver, elemento, ruta_abs: str, ctx: dict) -> None:
        """Envia una ruta de archivo a un input file validando contexto antes y despues.

        Args:
            driver: instancia de Selenium WebDriver.
            elemento: WebElement <input type="file">.
            ruta_abs: ruta absoluta del archivo a subir.
            ctx: dict con el contexto activo para validar.
        """
        self._validar_contexto_activo(driver, ctx)
        elemento.send_keys(ruta_abs)
        self._validar_contexto_activo(driver, ctx)

    @staticmethod
    def _guardar_dom(driver, nombre: str) -> None:
        """Guarda el DOM actual de la pagina en un archivo HTML para depuracion.

        Args:
            driver: instancia de Selenium WebDriver.
            nombre: sufijo para el nombre del archivo
                (ej: 'actividades' → debug_dom_hubspot_actividades.html).
        """
        try:
            ruta = f"debug_dom_hubspot_{nombre}.html"
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass

    def _paso_actividades(self, driver, log: Callable, ctx: dict) -> None:
        """Navega a la pestana Actividades en el registro de HubSpot.

        Prueba selectores CSS, XPath y un fallback JS por texto visible.
        No lanza excepcion si falla; continua sin abrir Actividades.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ctx: dict con el contexto activo para validar.
        """
        log("  → [HubSpot] Paso 1/7: Pestaña Actividades…")

        selectores = [
            (By.CSS_SELECTOR, self.SEL_TAB_ACTIVIDADES, "CSS primary"),
            (By.CSS_SELECTOR, self.SEL_TAB_ACTIVIDADES_FB, "CSS fallback"),
        ] + [
            (By.XPATH, xp, f"XPath {i+1}")
            for i, xp in enumerate(self.XPATH_ACTIVIDADES)
        ]

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
        """Abre el filtro Notas dentro de la pestana Actividades.

        Prueba selectores CSS, XPath y un fallback JS por texto visible.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ctx: dict con el contexto activo para validar.

        Raises:
            RuntimeError: si no se pudo abrir la pestana Notas.
        """
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
        """Hace click en el boton 'Crear nota' dentro de la pestana Notas.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ctx: dict con el contexto activo para validar.

        Raises:
            RuntimeError: si no se pudo encontrar o clickear el boton.
        """
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

    @_retry_stale(max_intentos=3)
    def _paso_crear_nota_directa(self, driver, log: Callable, ctx: dict) -> bool:
        """Intenta crear una nota desde el sidebar, sin navegar pestañas.

        El sidebar con el boton "Nota" existe tanto en tickets como en
        contactos, independientemente de la pestaña activa. Si funciona,
        nos ahorramos los pasos de Actividades y Notas.

        Returns:
            True si se pudo crear la nota desde el sidebar.
        """
        log("  → [HubSpot] Intentando crear nota desde sidebar…")
        try:
            btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, self.SEL_BTN_NOTA_SIDEBAR)
                )
            )
            self._safe_click(driver, btn, ctx)
            esperar_carga(driver, timeout=5)
            log("  ✓ [HubSpot] Nota creada desde sidebar.")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            log(f"  · [HubSpot] Sidebar no disponible: {e}")
        except Exception as e:
            log(f"  · [HubSpot] Error en sidebar: {e}")
        return False

    def _paso_editor(self, driver, log: Callable, ctx: dict, mensaje: str = "Nota de captura.") -> None:
        """
        Da foco al editor e inserta texto vía JS para que React habilite el toolbar.
        Sin este paso el ImageButton no aparece en el DOM.
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
                    var msg = arguments[1];
                    el.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, msg);
                    ['input', 'change', 'keyup'].forEach(function(t) {
                        el.dispatchEvent(new Event(t, { bubbles: true }));
                    });
                """,
                    editor,
                    mensaje,
                )
                self._validar_contexto_activo(driver, ctx)
                log(f"  ✓ [HubSpot] Editor enfocado ({label}).")
                editor_ok = True
            except Exception as e:
                log(f"  · [HubSpot] Editor {label} no encontrado: {e}")

        if not editor_ok:
            log("  ⚠ [HubSpot] Editor no localizado. El ImageButton puede no aparecer.")

    def _paso_insertar_imagen(self, driver, log: Callable, ruta_abs: str, ctx: dict) -> None:
        """Inserta una imagen en el editor haciendo click en el boton de imagen
        y enviando la ruta al input[type=file] oculto.

        Ambos pasos (click y send_keys) tienen reintentos independientes
        con @_retry_stale para manejar re-renders de React.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ruta_abs: ruta absoluta del archivo de imagen a insertar.
            ctx: dict con el contexto activo para validar.

        Raises:
            RuntimeError: si no se pudo hacer click en el boton o enviar
                la imagen tras los reintentos.
        """
        try:

            @_retry_stale(max_intentos=3)
            def _click_btn():
                btn = WebDriverWait(driver, self.TIMEOUT_LARGO).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, self.SEL_BTN_INSERTAR_IMAGEN)
                    )
                )
                self._safe_click(driver, btn, ctx)
                time.sleep(0.5)

            _click_btn()

            @_retry_stale(max_intentos=5, pausa=0.5)
            def _send_file():
                file_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.SEL_INPUT_FILE)
                    )
                )
                self._safe_send_file(driver, file_input, ruta_abs, ctx)

            _send_file()
            log(f"  ✓ [HubSpot] Imagen enviada al input.")
        except Exception as e:
            try:
                with open("debug_dom_hubspot.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                log("  · [HubSpot] DOM guardado en debug_dom_hubspot.html")
            except Exception:
                pass
            raise RuntimeError(f"No se pudo insertar la imagen: {e}") from e

    def _paso_esperar_imagen(
        self, driver, log: Callable, ruta_abs: str, ctx: dict
    ) -> None:
        """Espera a que la imagen insertada aparezca en el DOM del editor.

        Usa un selector CSS <img> dentro del editor (data-test-id='rte-content'
        o div.ProseMirror) con un timeout de 5 segundos. No lanza excepcion
        si el timeout expira; continua tras una pausa de 1.5s.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ruta_abs: ruta absoluta de la imagen insertada (no usada en el
                selector, conservada por compatibilidad).
            ctx: dict con el contexto activo para validar.
        """
        try:
            WebDriverWait(driver, 5).until(
                lambda d: (
                    self._validar_contexto_activo(d, ctx) is None
                    and d.find_elements(
                        By.CSS_SELECTOR,
                        '[data-test-id="rte-content"] img, div.ProseMirror img',
                    )
                )
            )
        except TimeoutException:
            time.sleep(1.5)

    def _paso_guardar(self, driver, log: Callable, ctx: dict) -> None:
        """Espera a que el boton Guardar este habilitado y hace click.

        Usa un expected condition personalizado que verifica que el boton
        no tenga aria-disabled='true' ni el atributo disabled.

        Args:
            driver: instancia de Selenium WebDriver.
            log: funcion callback para registrar mensajes.
            ctx: dict con el contexto activo para validar.

        Raises:
            RuntimeError: si el boton no se habilita dentro del timeout.
        """
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

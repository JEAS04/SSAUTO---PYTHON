"""
plugins/sunrun.py — Plugin de Sunrun para SSAuto.

Encapsula TODO lo específico de Sunrun:
  - URLs y selectores CSS.
  - Lógica de subida de archivo (flujo genérico de input file + submit).
  - Verificación de sesión.

Para cambiar algo de Sunrun, solo editar este archivo.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Callable

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import esperar_carga
from config.credenciales import cargar_cookies, guardar_cookies


class SunrunPlugin(SitioPlugin):
    """
    Plugin para subir archivos al portal de Sunrun.

    Flujo estándar: login (si es necesario) → navegar a URL de subida
    → input file → submit → confirmar.
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
        return False

    @property
    def dominio(self) -> str:
        return "sunrun.my.site.com"

    # ── URLs y selectores ─────────────────────────────────────────────

    URL_LOGIN = "https://sunrun.my.site.com/partner/login?locale=us"
    URL_UPLOAD = "https://the-internet.herokuapp.com/upload"  # Actualizar al URL real

    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#Login"
    SEL_INPUT_FILE = "#file-upload"
    SEL_SUBMIT = "#file-submit"
    SEL_CONFIRMACION = "h3, h1"
    PALABRAS_CONFIRMACION = ["uploaded", "success", "exitoso", "subido"]

    TIMEOUT = 15
    TIMEOUT_CONFIRMACION = 30

    # ── Interfaz pública ──────────────────────────────────────────────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """Navega a la URL de upload y verifica que no redirija a login."""
        try:
            log(f"  → [Sunrun] Verificando sesión en {self.URL_UPLOAD}…")
            driver.get(self.URL_UPLOAD)
            esperar_carga(driver, timeout=8)
            url_actual = driver.current_url.lower()
            if "login" in url_actual or "signin" in url_actual:
                log("  ✗ [Sunrun] Sin sesión activa — redirigido a login.")
                return False
            log("  ✓ [Sunrun] Sesión activa.")
            return True
        except Exception as e:
            log(f"  ⚠ [Sunrun] No se pudo verificar sesión: {e}")
            return False

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        """Login automático con usuario y contraseña."""
        usuario = credenciales.get("usuario", "")
        clave = credenciales.get("clave", "")
        if not usuario or not clave:
            log("  ✗ [Sunrun] Sin credenciales.")
            return False

        try:
            log(f"  → [Sunrun] Navegando a login…")
            driver.get(self.URL_LOGIN)
            esperar_carga(driver)
            espera = WebDriverWait(driver, self.TIMEOUT)

            espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_USER))).send_keys(usuario)
            driver.find_element(By.CSS_SELECTOR, self.SEL_PASS).send_keys(clave)
            espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_LOGIN))).click()

            esperar_carga(driver, timeout=20)
            url = driver.current_url.lower()
            if "login" not in url and "signin" not in url:
                guardar_cookies(driver, self.nombre)
                log("  ✓ [Sunrun] Login exitoso, cookies guardadas.")
                return True
            log("  ✗ [Sunrun] Login falló.")
            return False
        except Exception as e:
            log(f"  ✗ [Sunrun] Error en login: {e}")
            return False

    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """Sube el archivo al formulario de subida de Sunrun."""
        log = ctx.log
        driver = ctx.driver
        ruta_abs = os.path.abspath(ctx.ruta_imagen)

        log(f"  → [Sunrun] Iniciando subida: {ruta_abs}")
        esperar_carga(driver)

        try:
            self._localizar_y_enviar_archivo(driver, log, ruta_abs)
            ok = self._confirmar_subida(driver, log)
            if ok:
                return ResultadoSubida(exitoso=True, mensaje="Subida confirmada")
            return ResultadoSubida(exitoso=False, mensaje="No se pudo confirmar la subida")
        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}")

    # ── Pasos internos ────────────────────────────────────────────────

    def _localizar_y_enviar_archivo(self, driver, log: Callable, ruta_abs: str) -> None:
        espera = WebDriverWait(driver, self.TIMEOUT)

        # Buscar input file (selector específico primero, genérico como fallback)
        input_file = None
        for sel, label in [(self.SEL_INPUT_FILE, "específico"), ("input[type='file']", "genérico")]:
            try:
                input_file = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                log(f"  ✓ [Sunrun] Input file encontrado ({label}).")
                break
            except (TimeoutException, NoSuchElementException):
                log(f"  · [Sunrun] Selector {label} no encontrado, siguiente…")

        if not input_file:
            raise RuntimeError("No se encontró el campo de archivo en la página de Sunrun.")

        input_file.send_keys(ruta_abs)
        log(f"  ✓ [Sunrun] Archivo enviado.")

        # Submit
        try:
            btn = espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_SUBMIT)))
            btn.click()
            log("  ✓ [Sunrun] Submit enviado.")
        except Exception as e:
            raise RuntimeError(f"No se pudo hacer clic en Submit: {e}") from e

    def _confirmar_subida(self, driver, log: Callable) -> bool:
        """Espera y verifica el texto de confirmación."""
        try:
            texto_antes = driver.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text.strip().lower()
        except Exception:
            texto_antes = ""

        try:
            WebDriverWait(driver, self.TIMEOUT_CONFIRMACION).until(
                lambda d: d.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text.strip().lower() != texto_antes
            )
            resultado = driver.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text.strip()
            if any(p in resultado.lower() for p in self.PALABRAS_CONFIRMACION):
                log(f"  ✓ [Sunrun] Confirmado: {resultado}")
                return True
            log(f"  ⚠ [Sunrun] Respuesta inesperada: {resultado}")
            return False
        except Exception:
            log("  ✗ [Sunrun] Timeout esperando confirmación.")
            try:
                driver.save_screenshot(f"debug_upload_sunrun.png")
            except Exception:
                pass
            return False
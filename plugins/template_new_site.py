"""
plugins/template_nuevo_sitio.py — Plantilla para agregar un sitio nuevo.

INSTRUCCIONES:
  1. Copiar este archivo: cp template_nuevo_sitio.py mi_sitio.py
  2. Renombrar la clase y rellenar los campos marcados con TODO.
  3. En main.py agregar:
       from plugins.mi_sitio import MiSitioPlugin
       PluginRegistry.registrar(MiSitioPlugin())
  4. Listo. Sin tocar ningún otro archivo.
"""

from __future__ import annotations

import os
from typing import Callable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import esperar_carga


class NuevoSitioPlugin(SitioPlugin):
    """Plugin para [NOMBRE DEL SITIO]."""

    # ── Metadatos ─────────────────────────────────────────────────────

    @property
    def nombre(self) -> str:
        return "NUEVO_SITIO"  # TODO: cambiar. Debe ser único y en MAYÚSCULAS.

    @property
    def necesita_login(self) -> bool:
        return True  # TODO: False si el sitio es público.

    @property
    def usar_pagina_actual(self) -> bool:
        return False  # TODO: True solo si el usuario debe tener la página ya abierta.

    @property
    def dominio(self) -> str:
        return "ejemplo.com"  # TODO: subdominio para buscar la pestaña correcta.

    # ── URLs y selectores ─────────────────────────────────────────────
    # TODO: rellenar con los valores reales del sitio.

    URL_LOGIN = "https://ejemplo.com/login"
    URL_UPLOAD = "https://ejemplo.com/upload"

    SEL_USER = "#username"  # TODO: selector del campo usuario
    SEL_PASS = "#password"  # TODO: selector del campo contraseña
    SEL_BTN_LOGIN = "#login-btn"  # TODO: selector del botón de login
    SEL_INPUT_FILE = "input[type='file']"  # TODO: selector del input file
    SEL_SUBMIT = "#submit-btn"  # TODO: selector del botón submit (si aplica)
    SEL_CONFIRMACION = "h1, h2"  # TODO: selector del elemento de confirmación
    PALABRAS_CONFIRMACION = ["success", "uploaded", "exitoso"]

    TIMEOUT = 15

    # ── Implementación ────────────────────────────────────────────────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """
        Navega a la URL de upload y verifica que no haya redirección a login.
        Override si la lógica de detección de sesión es diferente.
        """
        try:
            driver.get(self.URL_UPLOAD)
            esperar_carga(driver, timeout=8)
            url = driver.current_url.lower()
            if "login" in url or "signin" in url:
                log(f"  ✗ [{self.nombre}] Sin sesión activa.")
                return False
            log(f"  ✓ [{self.nombre}] Sesión activa.")
            return True
        except Exception as e:
            log(f"  ⚠ [{self.nombre}] No se pudo verificar sesión: {e}")
            return False

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        """Login automático. Adaptar si el flujo de login tiene más pasos."""
        usuario = credenciales.get("usuario", "")
        clave = credenciales.get("clave", "")
        if not usuario or not clave:
            log(f"  ✗ [{self.nombre}] Sin credenciales.")
            return False
        try:
            driver.get(self.URL_LOGIN)
            esperar_carga(driver)
            espera = WebDriverWait(driver, self.TIMEOUT)
            espera.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_USER))
            ).send_keys(usuario)
            driver.find_element(By.CSS_SELECTOR, self.SEL_PASS).send_keys(clave)
            espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_LOGIN))
            ).click()
            esperar_carga(driver, timeout=20)
            url = driver.current_url.lower()
            if "login" not in url and "signin" not in url:
                log(f"  ✓ [{self.nombre}] Login exitoso.")
                return True
            log(f"  ✗ [{self.nombre}] Login falló.")
            return False
        except Exception as e:
            log(f"  ✗ [{self.nombre}] Error en login: {e}")
            return False

    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """Lógica principal de subida. Adaptar según el formulario del sitio."""
        log = ctx.log
        driver = ctx.driver
        ruta_abs = os.path.abspath(ctx.ruta_imagen)

        log(f"  → [{self.nombre}] Subiendo: {ruta_abs}")
        esperar_carga(driver)

        try:
            espera = WebDriverWait(driver, self.TIMEOUT)

            # 1. Enviar el archivo al input
            input_file = espera.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_INPUT_FILE))
            )
            input_file.send_keys(ruta_abs)
            log(f"  ✓ [{self.nombre}] Archivo enviado.")

            # 2. Submit (si aplica)
            # Si el formulario se envía automáticamente al elegir el archivo,
            # comentar o eliminar este bloque.
            btn = espera.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_SUBMIT))
            )
            btn.click()

            # 3. Confirmar
            texto_antes = ""
            try:
                texto_antes = driver.find_element(
                    By.CSS_SELECTOR, self.SEL_CONFIRMACION
                ).text.lower()
            except Exception:
                pass

            from selenium.webdriver.support.ui import WebDriverWait as WDW

            WDW(driver, 30).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR, self.SEL_CONFIRMACION
                ).text.lower()
                != texto_antes
            )
            resultado = driver.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text
            if any(p in resultado.lower() for p in self.PALABRAS_CONFIRMACION):
                log(f"  ✓ [{self.nombre}] Confirmado: {resultado}")
                return ResultadoSubida(exitoso=True, mensaje=resultado)
            return ResultadoSubida(
                exitoso=False, mensaje=f"Respuesta inesperada: {resultado}"
            )

        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}")

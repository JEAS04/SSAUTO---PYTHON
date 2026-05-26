This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where comments have been removed.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: node_modules/**, dist/**, .next/**, doms/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.clinerules
.gitignore
config/apps_captura.py
config/config.json
config/configuracion.py
config/credenciales.py
config/plantillas.json
core/base_plugin.py
core/browser.py
core/captura.py
core/comparador.py
core/plugin_registry.py
data/api.py
doku.md
GENERADOR_MENSAJES.md
iniciar_chrome_sesion.py
LICENSE
main.py
medidor.py
plugins/hubspot.py
plugins/sunrun.py
plugins/template_new_site.py
readme.md
recuperar_puerto.py
repomix.config.json
requirements.txt
scraping_sunrun.py
SELECTORES.HTML
services/sesion_service.py
template_filler.py
ui/custom_ctkframe.py
ui/posicion_ventanas.py
ui/ventana_comparacion.py
ui/ventana_credenciales.py
ui/ventana_generador_mensajes.py
ui/ventana_plantillas.py
ui/ventana_principal.py
version.py
```

# Files

## File: iniciar_chrome_sesion.py
````python
import subprocess
import time
import sys
from pathlib import Path

CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
PORT = 9222


def iniciar_chrome_con_sesion():








    rutas_chrome = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        Path.home()
        / "AppData"
        / "Local"
        / "Google"
        / "Chrome"
        / "Application"
        / "chrome.exe",
    ]

    chrome_path = None
    for ruta in rutas_chrome:
        if Path(ruta).exists():
            chrome_path = str(ruta)
            break

    if not chrome_path:
        print("[✗] Chrome no encontrado en rutas estándar")
        sys.exit(1)

    print(f"[*] Chrome encontrado: {chrome_path}")
    print(f"[*] Sesión: {CHROME_USER_DATA}")
    print(f"[*] Puerto: {PORT}")

    # Construir comando
    cmd = [
        chrome_path,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={CHROME_USER_DATA}",
        "--disable-popup-blocking",
        "--disable-default-apps",
    ]

    print(f"\n[*] Iniciando Chrome...")
    print(f"[*] Comando: {' '.join(cmd)}\n")

    try:

        subprocess.Popen(cmd)

        print("[✓] Chrome iniciado con sesión guardada")
        print(f"[*] Esperando que Chrome esté listo en puerto {PORT}...")

        # Esperar a que Chrome esté realmente listo
        for intento in range(20):
            time.sleep(0.5)
            if _puerto_activo(PORT):
                print(f"[✓] Chrome listo en puerto {PORT}")
                print("\n[ℹ] Ahora puedes ejecutar tu script de automatización:")
                print("    from core.browser import BrowserFactory")
                print("    driver = BrowserFactory.conectar_existente()")
                return True

        print("[!] Chrome se inició pero tardó mucho en estar listo")
        return False

    except Exception as e:
        print(f"[✗] Error al iniciar Chrome: {e}")
        return False


def _puerto_activo(puerto: int, host: str = "127.0.0.1") -> bool:

    import socket

    try:
        with socket.create_connection((host, puerto), timeout=1):
            return True
    except OSError:
        return False


if __name__ == "__main__":
    iniciar_chrome_con_sesion()
````

## File: recuperar_puerto.py
````python
import subprocess
import time
import os
from pathlib import Path


CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
CHROME_BACKUP = r"C:\chrome_sesion_ssauto_backup"
PORT = 9222

print("[*] Iniciando recuperación del puerto 9222...")


print("[*] Matando procesos Chrome/Chromedriver...")
os.system("taskkill /IM chrome.exe /F 2>nul")
os.system("taskkill /IM chromedriver.exe /F 2>nul")
time.sleep(2)


print(f"[*] Verificando carpeta: {CHROME_USER_DATA}")
if Path(CHROME_USER_DATA).exists():
    print("[✓] Carpeta encontrada")

    archivos = list(Path(CHROME_USER_DATA).rglob("*"))
    print(f"[*] Archivos encontrados: {len(archivos)}")
else:
    print("[!] Carpeta no existe, se creará nueva")


print(f"[*] Verificando puerto {PORT}...")
resultado = subprocess.run(
    f"netstat -ano | findstr :{PORT}", shell=True, capture_output=True, text=True
)
if resultado.stdout:
    print(f"[!] ALERTA: Algo está usando el puerto {PORT}")
    print(resultado.stdout)
else:
    print(f"[✓] Puerto {PORT} disponible")


print("[*] Iniciando Chrome con debugging remoto...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument(f"--remote-debugging-port={PORT}")
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")

    driver = webdriver.Chrome(options=options)
    print("[✓] Chrome iniciado exitosamente")
    time.sleep(2)


    print("[*] Verificando sesión...")
    driver.get("chrome://version")
    print("[✓] Sesión activa y funcionando")

    driver.quit()
    print("[✓] Chrome cerrado correctamente")

except Exception as e:
    print(f"[✗] Error: {e}")
    print("[!] Puede que necesitemos borrar la carpeta de sesión y empezar de nuevo")
````

## File: repomix.config.json
````json
{
  "output": {
    "style": "markdown",
    "removeComments": true
  },
  "ignore": {
    "customPatterns": [
      "node_modules/**",
      "dist/**",
      ".next/**",
      "doms/**"
    ]
  }
}
````

## File: SELECTORES.HTML
````html
# Dispatch State
SELECTOR_DISPATCH_STATE = (
    "//*[@data-target-selection-name="
    "'sfdc:RecordField.FS_Dispatch__c.FS_Dispatch_State__c']"
    "//lightning-formatted-text"
)

# Appointment Date
SELECTOR_APPOINTMENT_DATE = (
    "//*[contains(@data-target-selection-name,'Appointment_Date')]"
    "//lightning-formatted-text"
)

# Case Reason
SELECTOR_CASE_REASON = (
    "//*[@data-target-selection-name="
    "'sfdc:RecordField.FS_Dispatch__c.Case_Reason__c']"
    "//lightning-formatted-text"
)

# Related tab/button
SELECTOR_RELATED = (
    "//a[@role='tab' and @data-tab-name='related']"
)

# Upload Files (REAL input principal)
SELECTOR_UPLOAD_FILES_MAIN = (
    "//input[@type='file' and @name='fileInput']"
)

# Upload Files (botón visual secundario)
SELECTOR_UPLOAD_FILES_SECONDARY = (
    "//span[contains(text(),'Upload Files')]"
)

# Drop Files zone
SELECTOR_DROP_FILES = (
    "//*[contains(@class,'slds-file-selector__dropzone')]"
)
````

## File: .clinerules
````
# Cline Rules

## Objetivo principal
Minimizar uso de tokens y mensajes.
Responder de forma corta, técnica y accionable.

Asume conocimiento técnico avanzado.

---

# Reglas de respuesta

- NO expliques cosas obvias.
- NO repitas el requerimiento.
- NO des resúmenes largos.
- Usa respuestas máximas de 5 líneas salvo que se pida detalle.
- Prioriza código sobre explicación.
- Si algo ya fue analizado antes, no re-analizar.
- No describas archivos completos si no es necesario.
- Evitar markdown excesivo.
- Evitar ejemplos innecesarios.
- Preferir listas cortas.
- Sin introducciones largas.
- Ir directo al problema y solución.

Formato ideal:

1. problema
2. solución
3. código

---

# Manejo de contexto

- Mantener contexto corto.
- Antes de responder, evaluar si la información ya existe en contexto.
- Si la información ya existe, NO volver a leer archivos.
- Evitar releer archivos ya vistos.
- No mantener contexto innecesario.

---

# Lectura de archivos

- Leer SOLO archivos relevantes.
- Nunca escanear recursivamente todo el proyecto.
- Leer primero entrypoints y dependencias directas.
- Antes de abrir múltiples archivos, evaluar si realmente hace falta.
- No abrir archivos irrelevantes para la tarea.

Ignorar:

- node_modules
- dist
- build
- .next
- coverage
- .turbo
- .cache
- tmp
- logs
- package-lock.json
- yarn.lock
- pnpm-lock.yaml

Priorizar:

- src/
- app/
- components/
- services/
- lib/
- api/
- features/

---

# Generación de código

- Hacer cambios mínimos.
- Preferir patches pequeños y localizados.
- Mantener estilo existente.
- No refactorizar sin pedirlo.
- No mejorar código fuera del scope solicitado.
- No cambiar nombres innecesariamente.
- No mover archivos sin pedirlo.
- No reestructurar arquitectura.
- Entregar únicamente bloques modificados cuando sea posible.
- Cuando sea posible, responder usando diff minimalista.

Ejemplo preferido:

```diff
- const x = 1
+ const x = 2
````

## File: config/apps_captura.py
````python
_AZUL = ("#1f6aa5", "#1a5496")
_VERDE = ("#2d7a3a", "#256630")
_NARANJA = ("#a05a00", "#8a4e00")
_VIOLETA = ("#6b3fa0", "#5a3488")
_TEAL = ("#1a7a6e", "#146058")

APPS_CAPTURA = [
    {
        "nombre": "Wolkbox",
        "icono": "📞",
        "region": {"top": 100, "left": 0, "width": 800, "height": 600},
        "monitor": 1,
        "color": _AZUL,
    },
    {
        "nombre": "B2Chat",
        "icono": "💬",
        "region": {"top": 200, "left": 100, "width": 900, "height": 500},
        "monitor": 1,
        "color": _VERDE,
    },
    {
        "nombre": "Correo",
        "icono": "📧",
        "region": {"top": 150, "left": 50, "width": 1000, "height": 700},
        "monitor": 1,
        "color": _NARANJA,
    },
    {
        "nombre": "Calendar",
        "icono": "📅",
        "region": {"top": 300, "left": 200, "width": 850, "height": 550},
        "monitor": 1,
        "color": _VIOLETA,
    },
    {
        "nombre": "App 5",
        "icono": "📊",
        "region": {"top": 80, "left": 0, "width": 1920, "height": 980},
        "monitor": 1,
        "color": _TEAL,
    },
]
````

## File: config/credenciales.py
````python
import pickle
import keyring
from pathlib import Path

from config.configuracion import KEYRING_APP




def guardar_cookies(driver, sitio_nombre: str) -> None:











    Path("cookies").mkdir(exist_ok=True)
    ruta = f"cookies/{sitio_nombre.replace(' ', '_')}.pkl"
    with open(ruta, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"[cookies] Guardadas en: {ruta}")


def cargar_cookies(driver, sitio: dict, url_base: str) -> bool:
    """
    Intenta restaurar la sesión inyectando cookies guardadas en el driver.

    Navega primero a url_base para que el dominio coincida (requisito de
    los navegadores para aceptar cookies), luego inyecta las cookies y
    recarga la página. Devuelve True si el archivo existía, False si no.

    Parámetros
    ----------
    driver   : instancia activa de Selenium WebDriver.
    sitio    : dict del sitio (necesita la clave 'nombre').
    url_base : URL del dominio donde se van a inyectar las cookies.
    """
    ruta = f"cookies/{sitio['nombre'].replace(' ', '_')}.pkl"
    if not Path(ruta).exists():
        print(f"[cookies] No existe archivo: {ruta}")
        return False

    driver.get(url_base)
    with open(ruta, "rb") as f:
        cookies = pickle.load(f)
        print(f"[cookies] Cargando {len(cookies)} cookies para {sitio['nombre']}")
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                # Algunas cookies tienen atributos que el driver rechaza;
                # se omiten sin detener el proceso.
                print(f"[cookies] Omitida: {cookie.get('name')} — {e}")

    driver.refresh()
    return True


# ── Credenciales en el llavero del SO ────────────────────────────────


def guardar_credenciales(sitio_nombre: str, usuario: str, clave: str) -> None:
    """
    Persiste usuario y contraseña en el llavero del sistema operativo.

    El llavero cifra los valores; nunca se escriben en texto plano en
    ningún archivo del proyecto.
    """
    keyring.set_password(KEYRING_APP, f"{sitio_nombre}_usuario", usuario)
    keyring.set_password(KEYRING_APP, f"{sitio_nombre}_clave", clave)


def cargar_credenciales(sitio_nombre: str) -> tuple[str, str]:






    usuario = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_usuario") or ""
    clave = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_clave") or ""
    return usuario, clave


def borrar_credenciales(sitio_nombre: str) -> None:
    """
    Elimina usuario y contraseña del llavero del SO.

    Si no existen, la excepción se captura silenciosamente para no
    interrumpir el flujo cuando el usuario desmarca 'Recordar'.
    """
    for sufijo in ("_usuario", "_clave"):
        try:
            keyring.delete_password(KEYRING_APP, f"{sitio_nombre}{sufijo}")
        except Exception:
            pass
````

## File: config/plantillas.json
````json
[
  {
    "titulo": "Saludo inicial",
    "categoria": "HubSpot",
    "texto": "Hola [Nombre], espero que estés muy bien. Me comunico para hacerte seguimiento sobre tu solicitud. ¿Tienes alguna duda o necesitas información adicional?"
  },
  {
    "titulo": "Nota de seguimiento",
    "categoria": "HubSpot",
    "texto": "Se realizó llamada al cliente [Nombre] el [Fecha]. Se discutió [Tema]. Próximo paso: [Acción]. Fecha estimada: [Fecha siguiente]."
  },
  {
    "titulo": "Confirmación de cita",
    "categoria": "HubSpot",
    "texto": "Hola [Nombre], confirmamos tu cita para el día [Fecha] a las [Hora]. Por favor avísanos con anticipación si necesitas reagendar."
  },
  {
    "titulo": "Actualización de estado",
    "categoria": "Sunrun",
    "texto": "Actualización de estado para el caso [ID]: El sistema se encuentra en etapa [Estado]. Tiempo estimado de resolución: [Tiempo]."
  },
  {
    "titulo": "Cierre de caso",
    "categoria": "Sunrun",
    "texto": "El caso [ID] ha sido cerrado exitosamente el [Fecha]. Motivo de cierre: [Motivo]. Si tiene alguna consulta adicional no dude en contactarnos."
  },
  {
    "titulo": "Sin respuesta",
    "categoria": "General",
    "texto": "Hola [Nombre], intentamos comunicarnos contigo sin éxito. Por favor contáctanos al [Teléfono] o responde este mensaje para continuar con tu proceso."
  },
  {
    "titulo": "Respuesta",
    "categoria": "General",
    "texto": "El cliente [cliente] a aceptado su visita."
  }
]
````

## File: core/base_plugin.py
````python
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable





@dataclass
class RegionCaptura:
    top: int
    left: int
    width: int
    height: int

    def as_dict(self) -> dict:
        return {"top": self.top, "left": self.left, "width": self.width, "height": self.height}


@dataclass
class ResultadoSubida:

    exitoso: bool
    mensaje: str = ""
    detalle: str = ""


@dataclass
class ContextoSubida:
    """
    Todo lo que un plugin necesita para ejecutar la subida.

    Se construye en el servicio y se pasa al plugin — el plugin no toca
    la UI ni la configuración global.
    """
    ruta_imagen: str
    log: Callable[[str], None]
    driver: object                          # WebDriver (tipado débil para no forzar selenium aquí)
    credenciales: dict = field(default_factory=dict)   # {"usuario": ..., "clave": ...}
    opciones: dict = field(default_factory=dict)





class SitioPlugin(ABC):
















    @property
    @abstractmethod
    def nombre(self) -> str:

        ...

    @property
    def necesita_login(self) -> bool:

        return True

    @property
    def usar_pagina_actual(self) -> bool:





        return False

    @property
    def dominio(self) -> str:




        return ""

    # ── Métodos abstractos ────────────────────────────────────────────

    @abstractmethod
    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """
        Lógica completa de subida del archivo.

        Recibe el contexto con todo lo necesario (driver, ruta, log, etc.)
        y devuelve un ResultadoSubida con el estado final.

        El driver YA está conectado y posicionado en la pestaña correcta
        cuando este método se llama — el SesionService se encargó de eso.
        """
        ...

    # ── Métodos con implementación por defecto (override opcional) ─────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """
        Verifica si hay sesión activa en el driver para este sitio.

        Devuelve True si la sesión está activa, False si hay que hacer login.
        La implementación por defecto siempre devuelve True (útil para sitios
        donde el usuario maneja la sesión manualmente en Chrome).

        Override en plugins que puedan detectar redirección a login.
        """
        return True

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        """
        Realiza el login automático en el sitio.

        Devuelve True si el login fue exitoso.
        La implementación por defecto no hace nada (retorna False).

        Override en plugins que soporten login automático.
        """
        log(f"  ⚠ El plugin '{self.nombre}' no implementa login automático.")
        return False

    def describir(self) -> str:
        """Descripción legible del plugin para mostrar en la UI."""
        login = "con login" if self.necesita_login else "sin login"
        pagina = " · usa página actual" if self.usar_pagina_actual else ""
        return f"{self.nombre} ({login}{pagina})"
````

## File: core/browser.py
````python
from __future__ import annotations

import logging
import time
from typing import Callable

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("ssauto.browser")


PUERTO_DEBUG = 9222


class ErrorBrowser(Exception):

    pass


class BrowserFactory:








    @classmethod
    def conectar_existente(cls, puerto: int = PUERTO_DEBUG) -> webdriver.Chrome:







        opciones = webdriver.ChromeOptions()
        opciones.add_argument("--disable-blink-features=AutomationControlled")
        opciones.add_experimental_option("debuggerAddress", f"127.0.0.1:{puerto}")

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opciones,
            )
            cls._inyectar_antideteccion(driver)
            logger.debug(f"Conectado al Chrome en puerto {puerto}.")
            return driver
        except Exception as e:
            raise ErrorBrowser(
                f"No se pudo conectar al Chrome en puerto {puerto}. "
                f"¿Está abierto con --remote-debugging-port={puerto}? Error: {e}"
            ) from e

    @classmethod
    def nuevo(cls, headless: bool = False) -> webdriver.Chrome:
        """
        Abre un Chrome nuevo gestionado por la aplicación.

        Este driver SÍ debe cerrarse con driver.quit() al terminar.
        """
        opciones = webdriver.ChromeOptions()
        opciones.add_argument("--disable-blink-features=AutomationControlled")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")

        if headless:
            opciones.add_argument("--headless=new")
            opciones.add_argument("--disable-gpu")

        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=opciones,
            )
            cls._inyectar_antideteccion(driver)
            return driver
        except Exception as e:
            raise ErrorBrowser(f"No se pudo abrir Chrome nuevo: {e}") from e

    @classmethod
    def crear(cls, headless: bool, usar_existente: bool, puerto: int = PUERTO_DEBUG) -> webdriver.Chrome:
        """
        Punto de entrada unificado — elige el modo según los flags.

        Úsalo cuando la decisión depende de opciones del usuario (como en la UI).
        """
        if usar_existente:
            return cls.conectar_existente(puerto)
        return cls.nuevo(headless)

    # ── Antidetección ─────────────────────────────────────────────────

    @staticmethod
    def _inyectar_antideteccion(driver: webdriver.Chrome) -> None:
        """
        Intenta ocultar navigator.webdriver.

        En Chrome 147+ esto falla en sesiones de debugging — se captura
        silenciosamente porque no es un error crítico.
        """
        try:
            driver.execute_script("""
            try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            } catch(e) {
                // Chrome 147+ en sesiones reales no permite redefinir webdriver. Normal.
            }
            """)
        except Exception as e:
            logger.debug(f"Script antidetección no aplicado (esperado en Chrome moderno): {e}")


# ── Helpers de pestañas ───────────────────────────────────────────────


def encontrar_pestana(driver, subcadena_url: str, log: Callable | None = None) -> bool:
    """
    Cambia al driver a la primera pestaña cuya URL contenga subcadena_url.

    Devuelve True si la encontró y cambió, False si no.
    """
    _log = log or (lambda m: None)
    try:
        handles = driver.window_handles
        for handle in handles:
            try:
                driver.switch_to.window(handle)
                time.sleep(0.3)
                if subcadena_url.lower() in driver.current_url.lower():
                    _log(f"  ✓ Pestaña encontrada: {driver.title}")
                    return True
            except Exception:
                continue
        _log(f"  ⚠ No se encontró pestaña con '{subcadena_url}'")
        if handles:
            driver.switch_to.window(handles[0])
        return False
    except Exception as e:
        _log(f"  ⚠ Error al buscar pestaña: {e}")
        return False


def esperar_carga(driver, timeout: float = 10.0) -> bool:
    """Espera a que document.readyState sea 'complete'."""
    import time as _time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, WebDriverException
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        _time.sleep(0.5)
        return True
    except (TimeoutException, WebDriverException):
        return False


def puerto_activo(host: str = "127.0.0.1", puerto: int = PUERTO_DEBUG) -> bool:

    import socket
    try:
        with socket.create_connection((host, puerto), timeout=1):
            return True
    except OSError:
        return False
````

## File: core/captura.py
````python
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Union

import mss
import mss.tools


class ErrorCaptura(Exception):

    pass


class CapturaService:






    CARPETA_CAPTURAS = Path("screenshots")



    @classmethod
    def capturar(
        cls,
        region: Union[dict, "RegionCaptura"],
        carpeta: Path | None = None,
    ) -> str:
















        region_dict = cls._normalizar_region(region)
        cls._validar_region(region_dict)

        destino = carpeta or cls.CARPETA_CAPTURAS
        destino.mkdir(parents=True, exist_ok=True)

        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = destino / f"captura_{marca}.png"

        try:
            with mss.MSS() as sct:
                captura = sct.grab(region_dict)
                mss.tools.to_png(captura.rgb, captura.size, output=str(ruta))
        except Exception as e:
            raise ErrorCaptura(f"Error al capturar región {region_dict}: {e}") from e

        return str(ruta.resolve())

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _normalizar_region(region) -> dict:
        """Acepta dict o RegionCaptura y devuelve siempre un dict con ints."""
        if hasattr(region, "as_dict"):
            region = region.as_dict()
        return {k: int(v) for k, v in region.items() if k in ("top", "left", "width", "height")}

    @staticmethod
    def _validar_region(region: dict) -> None:

        claves = ("top", "left", "width", "height")
        faltantes = [c for c in claves if c not in region]
        if faltantes:
            raise ErrorCaptura(f"Faltan campos en la región: {faltantes}")
        if region["width"] <= 0:
            raise ErrorCaptura(f"width debe ser > 0, recibido: {region['width']}")
        if region["height"] <= 0:
            raise ErrorCaptura(f"height debe ser > 0, recibido: {region['height']}")

    @classmethod
    def listar_capturas(cls, carpeta: Path | None = None) -> list[Path]:
        """Lista todas las capturas guardadas, de más nueva a más vieja."""
        destino = carpeta or cls.CARPETA_CAPTURAS
        if not destino.exists():
            return []
        return sorted(destino.glob("captura_*.png"), reverse=True)

    @classmethod
    def limpiar_antiguas(cls, mantener: int = 50, carpeta: Path | None = None) -> int:




        archivos = cls.listar_capturas(carpeta)
        a_borrar = archivos[mantener:]
        for archivo in a_borrar:
            try:
                archivo.unlink()
            except Exception:
                pass
        return len(a_borrar)
````

## File: core/comparador.py
````python
import re
from rapidfuzz import fuzz






def _norm(texto: str) -> str:









    if not texto or texto.strip() in ("No encontrado", "No detectado", ""):
        return ""

    reemplazos = str.maketrans("áéíóúüñàèìòùÁÉÍÓÚÜÑ", "AEIOUUNAEIOUAEIOUUN")
    texto = texto.translate(reemplazos)
    texto = texto.upper().strip()
    texto = re.sub(r"\s{2,}", " ", texto)
    texto = re.sub(r"[.,;:'\"]", "", texto)
    return texto


def _comparar_nombres(valor_hs: str, valor_sr: str, umbral: float = 0.70) -> dict:
    """
    Compara nombres usando lógica token-based con rapidfuzz.
    Maneja nombres hispanos con segundos apellidos opcionales.

    Devuelve:
      similitud : float 0.0-1.0
      estado    : "igual" | "similar" | "diferente"
      nota      : string descriptivo

    Estrategia:
      1. Normalizar (MAYÚSCULAS, sin tildes, tokenizar).
      2. Token containment: si todos los tokens del nombre más corto
         aparecen en el más largo, es MATCH (caso hispano típico).
      3. Si falla lo anterior, usar token_set_ratio / token_sort_ratio
         / partial_ratio / WRatio de rapidfuzz y elegir el mejor.
    """
    na = _norm(valor_hs)
    nb = _norm(valor_sr)

    # Coincidencia exacta post-normalización
    if na == nb:
        return {"similitud": 1.0, "estado": "igual", "nota": "Coinciden exactamente."}

    tokens_a = set(na.split())
    tokens_b = set(nb.split())

    # Token containment: todos los tokens del nombre más corto
    # están presentes en el nombre más largo
    shorter_tokens = tokens_a if len(tokens_a) <= len(tokens_b) else tokens_b
    longer_tokens = tokens_b if len(tokens_a) <= len(tokens_b) else tokens_a

    if shorter_tokens and shorter_tokens.issubset(longer_tokens):
        # Puntaje basado en qué proporción de tokens únicos coinciden
        overlap_ratio = len(shorter_tokens) / max(len(tokens_a | tokens_b), 1)
        sim = max(overlap_ratio, 0.85)
        return {
            "similitud": sim,
            "estado": "similar",
            "nota": (
                "Posible coincidencia: todos los tokens del nombre más corto "
                "están contenidos en el nombre más largo."
            ),
        }

    # Usar rapidfuzz con múltiples métricas token-based
    token_set = fuzz.token_set_ratio(na, nb) / 100.0
    token_sort = fuzz.token_sort_ratio(na, nb) / 100.0
    partial = fuzz.partial_ratio(na, nb) / 100.0
    wratio = fuzz.WRatio(na, nb) / 100.0

    best = max(token_set, token_sort, partial, wratio)

    if best >= 0.85:
        return {
            "similitud": best,
            "estado": "similar",
            "nota": f"Alta similitud en nombres ({best:.0%}).",
        }
    else:
        return {
            "similitud": best,
            "estado": "diferente",
            "nota": f"Nombres distintos ({best:.0%}).",
        }


def _similitud(a: str, b: str) -> float:
    """
    Devuelve un valor entre 0.0 y 1.0 indicando qué tan similares son
    dos strings (1.0 = idénticos, 0.0 = completamente distintos).

    Útil para detectar errores tipográficos leves (ej: "Cruz" vs "Gruz").
    """
    return fuzz.ratio(_norm(a), _norm(b)) / 100.0


def _vacio(valor: str) -> bool:
    """Devuelve True si el valor es vacío, None o un placeholder de error."""
    return not valor or _norm(valor) == ""


def _normalizar_telefono(telefono: str) -> str:
    """
    Normaliza un número de teléfono removiendo todo carácter no numérico
    y el código de país '1' inicial si está presente.

    Ejemplos:
        "+17872979317"      → "7872979317"
        "(787)297-9317"     → "7872979317"
        "787-297-9317"      → "7872979317"
        "1-787-297-9317"    → "7872979317"


























    Compara el valor de un campo entre HubSpot y Sunrun.

    Parámetros
    ----------
    campo       : nombre del campo (ej: "nombre", "id_cliente", "municipio")
    valor_hs    : valor obtenido desde HubSpot
    valor_sunrun: valor obtenido desde Sunrun

    Devuelve
    --------
    dict con:
      campo      : nombre del campo
      valor_hs   : valor de HubSpot (original, sin normalizar)
      valor_sr   : valor de Sunrun (original)
      estado     : "igual" | "similar" | "diferente" | "solo_hs" | "solo_sunrun" | "ambos_vacios"
      similitud  : float entre 0.0 y 1.0
      nota       : string descriptivo para mostrar en la UI






















































































    Compara todos los campos disponibles entre HubSpot y Sunrun.

    Los campos se dividen en dos grupos:
      · Campos compartidos: existen en ambas fuentes y se comparan.
      · Campos exclusivos: solo existen en una fuente, se muestran como
        "solo_hs" o "solo_sunrun" directamente sin comparación.

    Parámetros
    ----------
    datos_hubspot : dict con datos de HubSpot ( api.py)
    datos_sunrun  : dict con datos de Sunrun  (scraping_sunrun.py)

    Devuelve
    --------
    dict con:
      fsd         : número FSD analizado
      campos      : lista de dicts (uno por campo), resultado de comparar_campo()
      resumen     : dict con conteos por estado
      tiene_error : bool — True si alguna fuente reportó error
      errores     : lista de mensajes de error de cada fuente



























































































    Adapta el dict devuelto por  api.extraer_datos_hubspot() al formato
    interno que usa comparar(). Todas las claves se pasan directamente;
    se garantiza que existan con valor vacío si faltaran.
````

## File: core/plugin_registry.py
````python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.base_plugin import SitioPlugin


class PluginRegistry:








    _plugins: dict[str, "SitioPlugin"] = {}



    @classmethod
    def registrar(cls, plugin: "SitioPlugin") -> None:





        cls._plugins[plugin.nombre] = plugin

    @classmethod
    def desregistrar(cls, nombre: str) -> None:

        cls._plugins.pop(nombre, None)

    @classmethod
    def limpiar(cls) -> None:

        cls._plugins.clear()



    @classmethod
    def obtener(cls, nombre: str) -> "SitioPlugin":





        if nombre not in cls._plugins:
            disponibles = list(cls._plugins.keys())
            raise KeyError(
                f"Plugin '{nombre}' no registrado. "
                f"Disponibles: {disponibles}"
            )
        return cls._plugins[nombre]

    @classmethod
    def obtener_o_none(cls, nombre: str) -> "SitioPlugin | None":

        return cls._plugins.get(nombre)

    @classmethod
    def todos(cls) -> list["SitioPlugin"]:

        return list(cls._plugins.values())

    @classmethod
    def nombres(cls) -> list[str]:

        return list(cls._plugins.keys())

    @classmethod
    def existe(cls, nombre: str) -> bool:
        return nombre in cls._plugins



    @classmethod
    def con_login(cls) -> list["SitioPlugin"]:

        return [p for p in cls.todos() if p.necesita_login]

    @classmethod
    def filtrar(cls, nombres: list[str]) -> list["SitioPlugin"]:




        if not nombres or nombres == ["AMBOS"]:
            return cls.todos()
        return [cls._plugins[n] for n in nombres if n in cls._plugins]



    @classmethod
    def __repr__(cls) -> str:
        plugins = [p.describir() for p in cls.todos()]
        return f"PluginRegistry({plugins})"
````

## File: data/api.py
````python
import os
import re
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest as TicketSearchRequest
from hubspot.crm.tickets import ApiException as TicketApiException
from hubspot.crm.contacts import PublicObjectSearchRequest as ContactSearchRequest
from hubspot.crm.contacts import ApiException as ContactApiException




load_dotenv()
_token = os.getenv("ACCESS_TOKEN")
_client = HubSpot(access_token=_token)






_T_FSD = "fsd__"
_T_FIRSTNAME = "firstname"
_T_LASTNAME = "lastname"
_T_ID_GOFORMZ = "id_goformz__servicios_tecnicos_"
_T_ADDRESS = "physical_address"
_T_PHONE = "phone"
_T_EMAIL = "e_mail"
_T_COUNTY = "pueblo_para_servicio_tecnico"
_T_SUBJECT = "subject"
_T_NOTA = "nota_ticket__sac_"
_T_PHONE_ALT = "telefono_alterno"
_T_STATE = "state"
_T_ZIP = "zip"
_T_CITY = "city"

_TICKET_PROPS = [
    _T_SUBJECT,
    _T_FSD,
    _T_ID_GOFORMZ,
    _T_FIRSTNAME,
    _T_LASTNAME,
    _T_ADDRESS,
    _T_PHONE,
    _T_PHONE_ALT,
    _T_EMAIL,
    _T_COUNTY,
    _T_STATE,
    _T_ZIP,
    _T_CITY,
    _T_NOTA,
]


_C_FIRSTNAME = "firstname"
_C_LASTNAME = "lastname"
_C_ID_GOFORMZ = "id_de_goformz__contacto_"
_C_ADDRESS = "direccion__fisica_"
_C_PHONE = "phone"
_C_PHONE_ALT = "telefono_alterno_del_cliente"
_C_EMAIL = "email"
_C_STATE = "country"
_C_MUNICIPIO = "municipio_de_residencia"
_C_MUNICIPIO_CO = "municipios_co__contacto_"
_C_STATE2 = "state"
_C_ZIP = "zip"

_CONTACT_PROPS = [
    _C_FIRSTNAME,
    _C_LASTNAME,
    _C_ID_GOFORMZ,
    _C_ADDRESS,
    _C_PHONE,
    _C_PHONE_ALT,
    _C_EMAIL,
    _C_STATE,
    _C_MUNICIPIO,
    _C_MUNICIPIO_CO,
    _C_STATE2,
    _C_ZIP,
]




_MUNICIPIOS_PR = [
    "Adjuntas",
    "Aguada",
    "Aguadilla",
    "Aguas Buenas",
    "Aibonito",
    "Añasco",
    "Arecibo",
    "Arroyo",
    "Barceloneta",
    "Barranquitas",
    "Bayamón",
    "Cabo Rojo",
    "Caguas",
    "Camuy",
    "Canóvanas",
    "Carolina",
    "Cataño",
    "Cayey",
    "Ceiba",
    "Ciales",
    "Cidra",
    "Coamo",
    "Comerío",
    "Corozal",
    "Culebra",
    "Dorado",
    "Fajardo",
    "Florida",
    "Guánica",
    "Guayama",
    "Guayanilla",
    "Guaynabo",
    "Gurabo",
    "Hatillo",
    "Hormigueros",
    "Humacao",
    "Isabela",
    "Jayuya",
    "Juana Díaz",
    "Juncos",
    "Lajas",
    "Lares",
    "Las Marías",
    "Las Piedras",
    "Loíza",
    "Luquillo",
    "Manatí",
    "Maricao",
    "Maunabo",
    "Mayagüez",
    "Moca",
    "Morovis",
    "Naguabo",
    "Naranjito",
    "Orocovis",
    "Patillas",
    "Peñuelas",
    "Ponce",
    "Quebradillas",
    "Rincón",
    "Río Grande",
    "Sabana Grande",
    "Salinas",
    "San Germán",
    "San Juan",
    "San Lorenzo",
    "San Sebastián",
    "Santa Isabel",
    "Toa Alta",
    "Toa Baja",
    "Trujillo Alto",
    "Utuado",
    "Vega Alta",
    "Vega Baja",
    "Vieques",
    "Villalba",
    "Yabucoa",
    "Yauco",
]

_MUNICIPIOS_SORTED = sorted(_MUNICIPIOS_PR, key=len, reverse=True)


def _norm(texto: str) -> str:

    for src, dst in zip("áéíóúüñàèìòùÁÉÍÓÚÜÑ", "aeiouunaeiouAEIOUUN"):
        texto = texto.replace(src, dst)
    return texto.lower()


_MUNICIPIOS_NORM = {_norm(m): m for m in _MUNICIPIOS_SORTED}


def _detectar_municipio(asunto: str) -> str:

    asunto_norm = _norm(asunto)
    for norm, original in _MUNICIPIOS_NORM.items():
        patron = r"(?<![a-z])" + re.escape(norm) + r"(?![a-z])"
        if re.search(patron, asunto_norm):
            return original
    return ""


def _parsear_asunto(asunto: str) -> dict:
    """
    Extrae del subject:
      - fsd        : número FSD (sin prefijo)
      - nombre     : nombre del cliente
      - id_cliente : ID GoFormz
      - municipio  : municipio detectado

    Regla: estos valores solo se usan como FALLBACK si el atributo
    directo de HubSpot está vacío.
    """
    texto = asunto

    # 1. Extraer FSD ("FSD983316" → "983316")
    fsd_parsed = ""
    m_fsd = re.search(r"\bFSD[-\s]*(\d+)\b", texto, re.IGNORECASE)
    if m_fsd:
        fsd_parsed = m_fsd.group(1)
        texto = texto[: m_fsd.start()] + texto[m_fsd.end() :]


    id_cliente = ""
    m_id = re.search(r"\bID\s*(\d{4,})\b", texto, re.IGNORECASE)
    if m_id:
        id_cliente = m_id.group(1)
        texto = texto[: m_id.start()] + texto[m_id.end() :]
    else:
        m_num = re.search(r"\b(\d{4,})\b", texto)
        if m_num:
            id_cliente = m_num.group(1)
            texto = texto[: m_num.start()] + texto[m_num.end() :]


    municipio = _detectar_municipio(texto)
    if municipio:
        texto = re.sub(re.escape(_norm(municipio)), "", _norm(texto))
    else:
        texto = _norm(texto)

    # 4. Limpiar separadores y dígitos residuales
    texto = re.sub(r"[-|/\\]+", " ", texto)
    texto = re.sub(r"\b\d+\b", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto).strip()

    nombre = texto.title() if texto else ""

    return {
        "fsd_parsed": fsd_parsed,
        "nombre": nombre,
        "id_cliente": id_cliente,
        "municipio": municipio,
    }







def _val(props: dict, key: str) -> str:

    v = props.get(key) or ""
    return v.strip()


def _buscar_ticket_por_fsd(fsd: str) -> dict | None:
    """
    Busca el ticket en HubSpot cuyo campo fsd__ coincide exactamente.
    Devuelve el dict de propiedades raw + ticket_id, o None si no existe.

    Acepta cualquier formato de FSD (FSD-1236711, FSD1236711, 1236711, etc.)
    y prueba múltiples variaciones hasta encontrar el ticket.
    """
    fsd_clean = fsd.strip()

    # ── 1. Generar variaciones candidatas ──────────────────────────────────
    candidates = []

    # (a) Entrada original
    candidates.append(fsd_clean)

    # (b) En mayúsculas
    candidates.append(fsd_clean.upper())

    # (c) Sin espacios
    candidates.append(fsd_clean.replace(" ", ""))

    # (d) Sin guion (en mayúsculas)
    candidates.append(fsd_clean.upper().replace("-", ""))

    # (e) Solo números
    numeric_only = re.sub(r"\D", "", fsd_clean)
    if numeric_only:
        candidates.append(numeric_only)

    # (f) Formateado como FSD-<número>
    if numeric_only:
        candidates.append(f"FSD-{numeric_only}")

    # Eliminar duplicados preservando orden
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    # ── 2. Probar cada variación secuencialmente ───────────────────────────
    for candidate in unique_candidates:
        print(f"[HubSpot] Buscando ticket con FSD='{candidate}'")

        search_request = TicketSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": _T_FSD,
                            "operator": "EQ",
                            "value": candidate,
                        }
                    ]
                }
            ],
            properties=_TICKET_PROPS,
            limit=1,
        )

        try:
            page = _client.crm.tickets.search_api.do_search(
                public_object_search_request=search_request
            )
            if page.results:
                ticket = page.results[0]
                print(
                    f"[HubSpot] ✓ Ticket encontrado con FSD='{candidate}' "
                    f"(id={ticket.id})"
                )
                return {"ticket_id": ticket.id, "props": ticket.properties}
        except TicketApiException as e:
            print(f"[HubSpot] Error buscando FSD='{candidate}': {e}")

    # ── 3. Ninguna variación dio resultado ─────────────────────────────────
    print(
        f"[HubSpot] ✗ No se encontró ningún ticket para FSD='{fsd_clean}' "
        f"(variaciones probadas: {unique_candidates})"
    )
    return None


def _buscar_contacto_por_id_goformz(id_goformz: str) -> dict | None:
    """
    Busca el contacto cuyo id_de_goformz__contacto_ coincide con id_goformz.
    Devuelve el dict de propiedades raw + contact_id, o None si no existe.
    """
    if not id_goformz:
        return None

    search_request = ContactSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "propertyName": _C_ID_GOFORMZ,
                        "operator": "EQ",
                        "value": id_goformz,
                    }
                ]
            }
        ],
        properties=_CONTACT_PROPS,
        limit=1,
    )

    try:
        page = _client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )
        if not page.results:
            return None
        contact = page.results[0]
        return {"contact_id": contact.id, "props": contact.properties}

    except ContactApiException as e:
        print(f"[HubSpot] Error buscando contacto id_goformz={id_goformz}: {e}")
        return None


# ──────────────────────────────────────────────
# Función pública principal
# ──────────────────────────────────────────────


def extraer_datos_hubspot(fsd: str) -> dict:
    """
    Extrae y unifica los datos de un ticket y su contacto relacionado.

    Regla de prioridad (campo por campo):
        1. Atributo directo del CONTACTO  (más completo y confiable)
        2. Atributo directo del TICKET
        3. Valor parseado del subject      (fallback)

    Parámetros
    ----------
    fsd : str
        Número FSD con o sin prefijo ("FSD983316" o "983316").

    Devuelve
    --------
    dict con las siguientes claves estandarizadas:
        fsd, ticket_id, contact_id,
        nombre, id_cliente,
        direccion, telefono, telefono_alterno,
        email, estado, municipio, zip,
        nota,
        fuente_nombre, fuente_id,      ← indica de dónde vino cada dato clave
        error                          ← None si todo OK, mensaje si hubo problema










































        Recibe pares (valor, etiqueta_fuente).
        Devuelve el primer par cuyo valor no esté vacío.





























































































    Alias de compatibilidad para ventana_comparacion.py.
````

## File: GENERADOR_MENSAJES.md
````markdown
# Generador de Mensajes de Contacto - Documentación

## 📋 Descripción General

Se ha implementado un **generador de mensajes de contacto** moderno y funcional utilizando `customtkinter`, que permite crear mensajes estandarizados para tres situaciones comunes de contacto con clientes.

## 🎯 Características Principales

### 1. **Tipos de Mensaje Disponibles**
- **Fuera de Servicio**: Para cuando el número registrado está fuera de servicio
- **Buzón de Voz**: Para cuando la llamada es dirigida al buzón de voz
- **No Contesta**: Para cuando el cliente no responde la llamada

### 2. **Soporte Bilingüe**
- Español (por defecto)
- Inglés
- Cada tipo de mensaje tiene su propia traducción profesional

### 3. **Manejo Inteligente de Números Telefónicos**
- Permite ingresar **1 o 2 números telefónicos**
- **Detección automática de singular/plural**:
  - 1 número: "al número", "el número", "fue enviado"
  - 2 números: "a los números", "los números", "fueron enviados"
- Los números se muestran automáticamente en el mensaje generado

### 4. **Fecha Automática**
- Formato: `MM/DD/YYYY` (ej: 05/25/2026)
- Se genera automáticamente al crear el mensaje
- Solo se incluye en las plantillas en inglés (como requiere el formato "LS:")

### 5. **Interfaz Moderna y Responsive**
- Diseño limpio y profesional con `customtkinter`
- Previsualización en tiempo real del mensaje
- Botones claramente identificados con emojis
- Confirmación visual al copiar el mensaje

## 🏗️ Arquitectura de la Solución

### **Decisión de Diseño: Mantener Separación**

Después de analizar `ventana_plantillas.py` y `template_filler.py`, se decidió:

1. **NO combinar** los archivos existentes
2. **Crear un nuevo módulo** (`ui/ventana_generador_mensajes.py`) específico para estos mensajes
3. **Mantener compatibilidad** con la funcionalidad existente

### **Razones de esta decisión:**

- `ventana_plantillas.py`: Gestiona plantillas genéricas editables con CRUD completo
- `template_filler.py`: Es un script standalone para plantillas con placeholders variables
- **Nuevo generador**: Casos específicos de contacto con lógica especializada (singular/plural, fecha automática)

### **Reutilización de Patrones:**
- Se mantuvo el patrón de `CTkToplevel` de `ventana_plantillas.py`
- Se reutilizó la función de copiar al portapapeles
- Se mantuvo el estilo visual consistente con la aplicación principal

## 📁 Estructura de Archivos

```
ssauto/
├── ui/
│   ├── ventana_generador_mensajes.py  ← NUEVO ARCHIVO
│   ├── ventana_plantillas.py          ← SIN CAMBIOS
│   └── ...
├── template_filler.py                 ← SIN CAMBIOS
├── main.py                            ← MODIFICADO (se agregó botón)
└── ...
```

## 🚀 Cómo Usar

### **1. Abrir el Generador**
- Ejecutar `main.py`
- Hacer clic en el botón **"Mensajes"** en la barra superior

### **2. Configurar el Mensaje**
1. **Seleccionar tipo de mensaje** (Fuera de Servicio, Buzón de Voz, No Contesta)
2. **Elegir idioma** (Español o English)
3. **Ingresar números telefónicos**:
   - Número 1 (obligatorio)
   - Número 2 (opcional, máximo 2 números)

### **3. Previsualizar y Copiar**
- El mensaje se genera **automáticamente** mientras escribes
- Revisar la previsualización
- Hacer clic en **"📋 Copiar Mensaje"**

## 💡 Ejemplos de Uso

### **Ejemplo 1: Un número - Fuera de Servicio (Español)**
```
Número 1: 555-1234
Resultado:
"Se llamó al número 555-1234, pero está fuera de servicio. Se envió un correo electrónico como método de contacto alternativo."
```

### **Ejemplo 2: Dos números - No Contesta (Español)**
```
Número 1: 555-1234
Número 2: 555-5678
Resultado:
"Se llamó a los clientes a los números 555-1234 y 555-5678, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico."
```

### **Ejemplo 3: Un número - Buzón de Voz (Inglés)**
```
Número 1: 555-1234
Resultado:
"LS: 05/25/2026 The customer was called at the registered number, but the call went to voicemail. A text message and an email were sent."
```

## 🔧 Detalles Técnicos

### **Manejo de Singular/Plural**

El sistema usa una expresión regular para detectar patrones `{singular|plural}`:

```python
def _procesar_texto(plantilla, cantidad_numeros, telefonos_str, idioma):
    # Reemplaza {al número|a los números} según cantidad
    # Si cantidad == 1 → usa "al número"
    # Si cantidad == 2 → usa "a los números"
```

### **Validaciones**
- ✅ Mínimo 1 número telefónico
- ✅ Máximo 2 números telefónicos
- ✅ Mensaje de error si no hay números
- ✅ Mensaje de error si excede el límite

### **Plantillas**

Las plantillas están definidas en el diccionario `PLANTILLAS_MENSAJES`:

```python
PLANTILLAS_MENSAJES = {
    "fuera_servicio": {
        "titulo": "Fuera de Servicio",
        "es": "Se llamó {al número|a los números} {telefonos}, ...",
        "en": "LS: {fecha} A call was placed to the registered phone {number|numbers}, ..."
    },
    # ... más plantillas
}
```

## ✅ Compatibilidad y Mantenimiento

### **Lo que NO se rompió:**
- ✅ `ventana_plantillas.py` sigue funcionando igual
- ✅ `template_filler.py` sigue funcionando igual
- ✅ Todos los imports existentes se mantienen
- ✅ El estilo visual es consistente
- ✅ La aplicación principal (`main.py`) funciona correctamente

### **Buenas Prácticas Aplicadas:**
- ✅ Código modular y fácil de mantener
- ✅ Comentarios claros en español
- ✅ Nombres de variables descriptivos
- ✅ Separación de responsabilidades
- ✅ Manejo de errores básico
- ✅ Sin código redundante

## 🔄 Flujo de Trabajo Recomendado

1. **Para mensajes de contacto estandarizados** → Usar **Generador de Mensajes**
2. **Para plantillas personalizables** → Usar **Plantillas** (ventana_plantillas.py)
3. **Para mensajes con placeholders variables** → Usar **Template Filler** (template_filler.py)

## 📝 Notas Importantes

- El generador está diseñado específicamente para los 3 tipos de mensajes de contacto
- Los mensajes se copian al portapapeles listos para pegar
- La fecha se genera automáticamente en el momento de crear el mensaje
- El formato de fecha (MM/DD/YYYY) es el estándar americano

## 🎨 Características de UI/UX

- **Diseño moderno** con customtkinter
- **Responsive** dentro de las limitaciones de customtkinter
- **Iconos emoji** para mejor identificación visual
- **Feedback visual** al copiar (mensaje de confirmación)
- **Previsualización en tiempo real** mientras se escriben los números
- **Organización clara** por secciones (configuración, teléfonos, preview)

## 🔮 Posibles Mejoras Futuras

- Agregar más tipos de mensajes si se requieren
- Permitir personalizar las plantillas (guardar en JSON)
- Agregar historial de mensajes generados
- Exportar a diferentes formatos
- Integrar con APIs de envío de mensajes

---

**Implementado el**: 2026-05-25  
**Versión**: 1.0.0  
**Autor**: SSAuto Development Team
````

## File: LICENSE
````
MIT License

Copyright (c) 2026 JEAS04

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

## File: plugins/sunrun.py
````python
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



    URL_LOGIN = "https://sunrun.my.site.com/partner/login?locale=us"
    URL_UPLOAD = "https://the-internet.herokuapp.com/upload"

    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#Login"
    SEL_INPUT_FILE = "#file-upload"
    SEL_SUBMIT = "#file-submit"
    SEL_CONFIRMACION = "h3, h1"
    PALABRAS_CONFIRMACION = ["uploaded", "success", "exitoso", "subido"]

    TIMEOUT = 15
    TIMEOUT_CONFIRMACION = 30



    def verificar_sesion(self, driver, log: Callable) -> bool:

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
````

## File: plugins/template_new_site.py
````python
from __future__ import annotations

import os
from typing import Callable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import esperar_carga


class NuevoSitioPlugin(SitioPlugin):




    @property
    def nombre(self) -> str:
        return "NUEVO_SITIO"

    @property
    def necesita_login(self) -> bool:
        return True

    @property
    def usar_pagina_actual(self) -> bool:
        return False

    @property
    def dominio(self) -> str:
        return "ejemplo.com"




    URL_LOGIN = "https://ejemplo.com/login"
    URL_UPLOAD = "https://ejemplo.com/upload"

    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#login-btn"
    SEL_INPUT_FILE = "input[type='file']"
    SEL_SUBMIT = "#submit-btn"
    SEL_CONFIRMACION = "h1, h2"
    PALABRAS_CONFIRMACION = ["success", "uploaded", "exitoso"]

    TIMEOUT = 15



    def verificar_sesion(self, driver, log: Callable) -> bool:




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
            espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_USER))).send_keys(usuario)
            driver.find_element(By.CSS_SELECTOR, self.SEL_PASS).send_keys(clave)
            espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_LOGIN))).click()
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
            btn = espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_SUBMIT)))
            btn.click()

            # 3. Confirmar
            texto_antes = ""
            try:
                texto_antes = driver.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text.lower()
            except Exception:
                pass

            from selenium.webdriver.support.ui import WebDriverWait as WDW
            WDW(driver, 30).until(
                lambda d: d.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text.lower() != texto_antes
            )
            resultado = driver.find_element(By.CSS_SELECTOR, self.SEL_CONFIRMACION).text
            if any(p in resultado.lower() for p in self.PALABRAS_CONFIRMACION):
                log(f"  ✓ [{self.nombre}] Confirmado: {resultado}")
                return ResultadoSubida(exitoso=True, mensaje=resultado)
            return ResultadoSubida(exitoso=False, mensaje=f"Respuesta inesperada: {resultado}")

        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}")
````

## File: template_filler.py
````python
import re
import customtkinter as ctk
from ui.ventana_plantillas import PLANTILLAS_DEFAULT

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x600")
app.title("Generador de Mensajes")





def plural(cantidad: int, singular: str, plural_form: str = "") -> str:
    """Retorna la forma singular o plural según la cantidad."""
    if not plural_form:
        plural_form = singular + "s"
    return singular if cantidad == 1 else plural_form


def s(
    cantidad: int,
    singular: str,
    plural_form: str = "",
) -> str:
    """Alias corto de plural()."""
    return plural(cantidad, singular, plural_form)


def _reemplazar_plurales(texto: str) -> str:
    """
    Reemplaza tokens con sintaxis `{palabra|palabras}` dentro del texto
    según la cantidad definida en el contexto global *__ctx_cantidad__*.

    Ejemplo:
        "Tengo {1} {cliente|clientes}" → "Tengo 1 cliente"  si cantidad==1
        "Tengo {3} {cliente|clientes}" → "Tengo 3 clientes" si cantidad==3





































































Mi nombre es {nombre} y le escribo en calidad de {cargo} en {empresa}.

Este mensaje va dirigido a {texto_clientes}.
````

## File: ui/custom_ctkframe.py
````python
import customtkinter as ctk


class CustomCTkFrame(ctk.CTkFrame):











    def get_root(self):






        return self.winfo_toplevel()

    def iconify_window(self):






        root = self.get_root()
        try:
            root.iconify()
        except Exception as e:
            print(f"Error al minimizar ventana: {e}")

    def deiconify_window(self):
        """
        Restaura la ventana raíz si está minimizada.

        Este método obtiene la ventana raíz y la restaura (state='normal').
        También trae la ventana al frente.
        """
        root = self.get_root()
        try:
            root.deiconify()
            root.lift()
            root.focus_force()
        except Exception as e:
            print(f"Error al restaurar ventana: {e}")

    def set_window_geometry(self, geometry: str):
        """
        Configura la geometría (tamaño y posición) de la ventana raíz.

        Parameters:
        -----------
        geometry : str
            Geometría en formato "WIDTHxHEIGHT+X+Y"
            Ejemplo: "800x600+100+50"
````

## File: ui/posicion_ventanas.py
````python
from __future__ import annotations

from config.configuracion import obtener_monitores


def _parse_geometry(widget) -> tuple[int, int, int, int]:

    widget.update_idletasks()
    return (
        int(widget.winfo_rootx()),
        int(widget.winfo_rooty()),
        int(widget.winfo_width()),
        int(widget.winfo_height()),
    )


def _monitor_for_rect(x: int, y: int, width: int, height: int) -> dict | None:

    monitors = obtener_monitores()
    if not monitors:
        return None

    center_x = x + width // 2
    center_y = y + height // 2
    physical_monitors = monitors[1:] if len(monitors) > 1 else monitors

    for monitor in physical_monitors:
        left = int(monitor.get("left", 0))
        top = int(monitor.get("top", 0))
        right = left + int(monitor.get("width", 0))
        bottom = top + int(monitor.get("height", 0))
        if left <= center_x < right and top <= center_y < bottom:
            return monitor

    return physical_monitors[0] if physical_monitors else monitors[0]


def _clamp(value: int, minimum: int, maximum: int) -> int:
    if maximum < minimum:
        return minimum
    return max(minimum, min(value, maximum))


def _tk_offset(value: int) -> str:

    return f"{value:+d}"


def ubicar_junto_a_padre(ventana, padre, margen: int = 12) -> None:
    """
    Place a child window next to its parent on the parent's current monitor.

    It prefers the right side, falls back to the left side, and finally clamps
    the window inside the monitor if there is not enough horizontal space.
    """
    try:
        parent_top = padre.winfo_toplevel()
        parent_x, parent_y, parent_w, parent_h = _parse_geometry(parent_top)
        ventana.update_idletasks()

        # A newly-created Tk window can briefly report 1x1. Use requested size
        # as a lower bound to avoid shrinking modal windows.
        win_w = max(int(ventana.winfo_width()), int(ventana.winfo_reqwidth()))
        win_h = max(int(ventana.winfo_height()), int(ventana.winfo_reqheight()))

        monitor = _monitor_for_rect(parent_x, parent_y, parent_w, parent_h)
        if monitor:
            mon_left = int(monitor.get("left", 0))
            mon_top = int(monitor.get("top", 0))
            mon_right = mon_left + int(
                monitor.get("width", ventana.winfo_screenwidth())
            )
            mon_bottom = mon_top + int(
                monitor.get("height", ventana.winfo_screenheight())
            )
        else:
            mon_left, mon_top = 0, 0
            mon_right = ventana.winfo_screenwidth()
            mon_bottom = ventana.winfo_screenheight()

        right_x = parent_x + parent_w + margen
        left_x = parent_x - win_w - margen

        if right_x + win_w <= mon_right:
            x = right_x
        elif left_x >= mon_left:
            x = left_x
        else:
            x = _clamp(right_x, mon_left + margen, mon_right - win_w - margen)

        ideal_y = parent_y + max(0, (parent_h - win_h) // 2)
        y = _clamp(ideal_y, mon_top + margen, mon_bottom - win_h - margen)

        ventana.geometry(f"{win_w}x{win_h}{_tk_offset(x)}{_tk_offset(y)}")
    except Exception:

        pass
````

## File: ui/ventana_generador_mensajes.py
````python
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date as date_type
import re
from ui.posicion_ventanas import ubicar_junto_a_padre



PLANTILLAS_MENSAJES = {
    "fuera_servicio": {
        "titulo": "Fuera de Servicio",
        "es": "LS: {fecha}. Se llamó {al número|a los números} {telefonos}, pero {está|están} fuera de servicio. Se envió un correo electrónico como método de contacto alternativo.",
        "en": "LS: {fecha}. A call was placed to the registered phone {number|numbers}, but {it is|they are} out of service. An email was sent as an alternative method of contact.",
    },
    "buzon_voz": {
        "titulo": "Buzón de Voz",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero la llamada fue enviada al buzón de voz. Se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers}, but the call went to voicemail. A text message and an email were sent.",
    },
    "no_contesta": {
        "titulo": "No Contesta",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers}, but did not answer. A text message and an email were sent as alternative methods of contact.",
    },
    "confirma_visita_tecnica": {
        "titulo": "Cliente confirma visita técnica",
        "requiere_telefonos": False,
        "es": "Cliente confirma visita técnica en chat para el {fecha_habil_siguiente}.",
        "en": "Customer confirms technical visit in chat for {fecha_habil_siguiente}.",
    },
}


def _obtener_fecha() -> str:

    return datetime.now().strftime("%m/%d/%Y")


def _obtener_fecha_habil_siguiente() -> str:






    try:
        import pandas as pd

        fecha_actual = pd.Timestamp(datetime.now().date())
        fecha_habil_siguiente = fecha_actual + pd.offsets.BusinessDay(1)
        return fecha_habil_siguiente.strftime("%m/%d/%Y")
    except ImportError:

        dia = datetime.now().date()
        dia_siguiente = date_type.fromordinal(dia.toordinal() + 1)
        while dia_siguiente.weekday() >= 5:
            dia_siguiente = date_type.fromordinal(dia_siguiente.toordinal() + 1)
        return dia_siguiente.strftime("%m/%d/%Y")


CODIGOS_AREA_PR = {"787", "939"}


def _normalizar_telefono_nanp(telefono: str) -> tuple[str, str | None]:











    original = telefono.strip()
    digitos = re.sub(r"\D", "", original)

    if len(digitos) < 7:
        return "", f"'{original}' debe tener al menos 7 dígitos."

    if len(digitos) == 7:
        return f"{digitos[:3]}-{digitos[3:]}", None

    if len(digitos) == 10:
        codigo_area = digitos[:3]
        if codigo_area not in CODIGOS_AREA_PR:
            return (
                "",
                f"'{original}' debe usar un código de área de Puerto Rico: 787 o 939.",
            )
        return f"({codigo_area}) {digitos[3:6]}-{digitos[6:]}", None

    if len(digitos) == 11:
        codigo_pais = digitos[0]
        codigo_area = digitos[1:4]
        if codigo_pais != "1":
            return "", f"'{original}' debe usar el código de país NANP +1."
        if codigo_area not in CODIGOS_AREA_PR:
            return (
                "",
                f"'{original}' debe usar un código de área de Puerto Rico: 787 o 939.",
            )
        return f"+1 ({codigo_area}) {digitos[4:7]}-{digitos[7:]}", None

    return "", f"'{original}' debe tener 7, 10 u 11 dígitos."


def _procesar_texto(
    plantilla: str, cantidad_numeros: int, telefonos_str: str, idioma: str
) -> str:
    """
    Procesa una plantilla reemplazando:
    - {singular|plural} según la cantidad de números
    - {telefonos} con la lista de números
    - {fecha} con la fecha actual
    - {fecha_habil_siguiente} con el próximo día hábil
    """
    texto = plantilla

    texto = texto.replace("{fecha}", _obtener_fecha())
    texto = texto.replace("{fecha_habil_siguiente}", _obtener_fecha_habil_siguiente())
    texto = texto.replace("{telefonos}", telefonos_str)

    def reemplazar_plural(match: re.Match) -> str:
        singular = match.group(1)
        plural = match.group(2)
        return singular if cantidad_numeros == 1 else plural

    texto = re.sub(r"\{([^|}]+)\|([^}]+)\}", reemplazar_plural, texto)

    return texto


class VentanaGeneradorMensajes(ctk.CTkToplevel):
    """
    Ventana para generar mensajes de contacto estandarizados.

    Permite seleccionar tipo de mensaje, idioma, ingresar hasta 2 números
    telefónicos, previsualizar el mensaje y copiarlo al portapapeles.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generador de Mensajes de Contacto")
        self.geometry("700x650")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._tipo_mensaje_var = ctk.StringVar(value="fuera_servicio")
        self._idioma_var = ctk.StringVar(value="es")

        self._construir_ui()
        ubicar_junto_a_padre(self, parent)
        self._actualizar_preview()



    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        margen_x = 20
        margen_y = 10


        lbl_titulo = ctk.CTkLabel(
            self,
            text="📝 Generador de Mensajes de Contacto",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_titulo.grid(row=0, column=0, sticky="w", padx=margen_x, pady=(margen_y, 0))

        lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Selecciona un tipo de mensaje, ingresa los números y genera el texto",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        lbl_subtitulo.grid(
            row=1, column=0, sticky="w", padx=margen_x, pady=(0, margen_y)
        )


        panel_config = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_config.grid(
            row=2, column=0, sticky="ew", padx=margen_x, pady=(0, margen_y)
        )
        panel_config.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_config,
            text="Tipo de mensaje:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        opciones_tipo = [
            (clave, plantilla["titulo"])
            for clave, plantilla in PLANTILLAS_MENSAJES.items()
        ]
        self._combo_tipo = ctk.CTkOptionMenu(
            panel_config,
            variable=self._tipo_mensaje_var,
            values=[clave for clave, _ in opciones_tipo],
            command=self._al_cambiar_tipo_mensaje,
            font=ctk.CTkFont(size=11),
        )
        self._combo_tipo.grid(row=0, column=1, sticky="w", padx=12, pady=(12, 4))

        ctk.CTkLabel(
            panel_config,
            text="Idioma:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=4)

        frame_idioma = ctk.CTkFrame(panel_config, fg_color="transparent")
        frame_idioma.grid(row=1, column=1, sticky="w", padx=12, pady=4)

        self._radio_es = ctk.CTkRadioButton(
            frame_idioma,
            text="Español",
            variable=self._idioma_var,
            value="es",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=11),
        )
        self._radio_es.pack(side="left", padx=(0, 16))

        self._radio_en = ctk.CTkRadioButton(
            frame_idioma,
            text="Ingles",
            variable=self._idioma_var,
            value="en",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=11),
        )
        self._radio_en.pack(side="left")


        panel_telefonos = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_telefonos.grid(
            row=3, column=0, sticky="ew", padx=margen_x, pady=(0, margen_y)
        )
        panel_telefonos.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_telefonos,
            text="📞 Números telefónicos:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        lbl_info = ctk.CTkLabel(
            panel_telefonos,
            text="NANP PR: 555-1234, (787) 555-1234 o +1 (939) 555-1234",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        lbl_info.grid(row=0, column=1, sticky="w", padx=4, pady=(12, 4))

        ctk.CTkLabel(
            panel_telefonos,
            text="Número 1:",
            font=ctk.CTkFont(size=11),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=4)

        self._entry_tel1 = ctk.CTkEntry(
            panel_telefonos,
            placeholder_text="Ej: (787) 555-1234",
            font=ctk.CTkFont(size=12),
        )
        self._entry_tel1.grid(row=1, column=1, sticky="ew", padx=12, pady=4)
        self._entry_tel1.bind("<KeyRelease>", lambda e: self._actualizar_preview())

        ctk.CTkLabel(
            panel_telefonos,
            text="Número 2:",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, sticky="w", padx=12, pady=(4, 12))

        self._entry_tel2 = ctk.CTkEntry(
            panel_telefonos,
            placeholder_text="Opcional: +1 (939) 555-1234",
            font=ctk.CTkFont(size=12),
        )
        self._entry_tel2.grid(row=2, column=1, sticky="ew", padx=12, pady=(4, 12))
        self._entry_tel2.bind("<KeyRelease>", lambda e: self._actualizar_preview())


        panel_preview = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_preview.grid(
            row=4, column=0, sticky="nsew", padx=margen_x, pady=(0, margen_y)
        )
        panel_preview.grid_rowconfigure(1, weight=1)
        panel_preview.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_preview,
            text="📄 Previsualización:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        self._textbox_preview = ctk.CTkTextbox(
            panel_preview,
            font=ctk.CTkFont(size=12),
            wrap="word",
            state="disabled",
        )
        self._textbox_preview.grid(
            row=1, column=0, sticky="nsew", padx=12, pady=(0, 12)
        )


        panel_botones = ctk.CTkFrame(self, fg_color="transparent")
        panel_botones.grid(
            row=5, column=0, sticky="e", padx=margen_x, pady=(0, margen_y)
        )

        self._btn_copiar = ctk.CTkButton(
            panel_botones,
            text="📋 Copiar Mensaje",
            command=self._copiar_mensaje,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            width=160,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self._btn_copiar.pack(side="right", padx=(8, 0))

        self._btn_generar = ctk.CTkButton(
            panel_botones,
            text="🔄 Generar",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=12),
            height=36,
            width=120,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        )
        self._btn_generar.pack(side="right")

        self._label_estado = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("
        )
        self._label_estado.grid(row=6, column=0, sticky="e", padx=margen_x, pady=(0, 4))



    def _obtener_telefonos(self) -> tuple[list[str], list[str]]:
        telefonos = []
        errores = []

        tel1 = self._entry_tel1.get().strip()
        if tel1:
            telefono_formateado, error = _normalizar_telefono_nanp(tel1)
            if error:
                errores.append(f"Número 1: {error}")
            else:
                telefonos.append(telefono_formateado)

        tel2 = self._entry_tel2.get().strip()
        if tel2:
            telefono_formateado, error = _normalizar_telefono_nanp(tel2)
            if error:
                errores.append(f"Número 2: {error}")
            else:
                telefonos.append(telefono_formateado)

        return telefonos, errores

    def _formatear_telefonos(self, telefonos: list[str]) -> str:
        if len(telefonos) == 1:
            return telefonos[0]
        elif len(telefonos) == 2:
            return f"{telefonos[0]} y {telefonos[1]}"
        return ", ".join(telefonos)

    def _requiere_telefonos(self) -> bool:
        tipo = self._tipo_mensaje_var.get()
        return PLANTILLAS_MENSAJES[tipo].get("requiere_telefonos", True)

    def _al_cambiar_tipo_mensaje(self, *_):
        self._actualizar_estado_telefonos()
        self._actualizar_preview()

    def _actualizar_estado_telefonos(self):
        requiere_telefonos = self._requiere_telefonos()
        estado = "normal" if requiere_telefonos else "disabled"
        self._entry_tel1.configure(state=estado)
        self._entry_tel2.configure(state=estado)

    def _actualizar_preview(self, *_):
        tipo = self._tipo_mensaje_var.get()
        idioma = self._idioma_var.get()
        telefonos, errores = self._obtener_telefonos()
        plantilla = PLANTILLAS_MENSAJES[tipo]
        requiere_telefonos = self._requiere_telefonos()
        self._preview_valido = False

        if requiere_telefonos and errores:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0",
                "Corrige los números telefónicos:\n"
                + "\n".join(f"• {error}" for error in errores)
                + "\n\nFormatos aceptados: 555-1234, (787) 555-1234, +1 (939) 555-1234.",
            )
            self._textbox_preview.configure(state="disabled")
            return

        if requiere_telefonos and not telefonos:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0", "Ingresa al menos un número telefónico para generar el mensaje."
            )
            self._textbox_preview.configure(state="disabled")
            return

        if requiere_telefonos and len(telefonos) > 2:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0", "Máximo 2 números telefónicos permitidos."
            )
            self._textbox_preview.configure(state="disabled")
            return

        texto_plantilla = plantilla[idioma]
        telefonos_str = (
            self._formatear_telefonos(telefonos) if requiere_telefonos else ""
        )
        mensaje = _procesar_texto(
            texto_plantilla, len(telefonos), telefonos_str, idioma
        )

        self._textbox_preview.configure(state="normal")
        self._textbox_preview.delete("0.0", "end")
        self._textbox_preview.insert("0.0", mensaje)
        self._textbox_preview.configure(state="disabled")
        self._preview_valido = True

    def _copiar_mensaje(self):
        mensaje = self._textbox_preview.get("0.0", "end").strip()

        if not mensaje or not getattr(self, "_preview_valido", False):
            messagebox.showwarning(
                "Sin mensaje", "Genera un mensaje válido antes de copiar.", parent=self
            )
            return

        self.clipboard_clear()
        self.clipboard_append(mensaje)

        self._label_estado.configure(text="✓ Mensaje copiado al portapapeles")
        self.after(2500, lambda: self._label_estado.configure(text=""))
````

## File: version.py
````python
__version__ = "0.1.0"
````

## File: config/config.json
````json
{
  "tema": "dark",
  "ultimo_monitor": 1,
  "regiones_apps": {
    "Wolkbox": {
      "top": 52,
      "left": 18,
      "width": 1901,
      "height": 966
    },
    "App 2": {
      "top": 448,
      "left": 826,
      "width": 97,
      "height": 76
    },
    "App 3": {
      "top": 249,
      "left": 546,
      "width": 752,
      "height": 459
    },
    "App 4": {
      "top": 232,
      "left": 292,
      "width": 1509,
      "height": 674
    },
    "App 5": {
      "top": 288,
      "left": 186,
      "width": 1415,
      "height": 529
    }
  },
  "keybind": "<Control-p>",
  "perfiles_region": {
    "monitor 1": {
      "top": 267,
      "left": 91,
      "width": 410,
      "height": 220,
      "monitor_index": 1
    },
    "monitor 2": {
      "top": 81,
      "left": -1885,
      "width": 1416,
      "height": 806,
      "monitor_index": 2
    }
  },
  "auto_submit_nota": false
}
````

## File: config/configuracion.py
````python
import os
import sys
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




TEMA_APARIENCIA = "dark"
TEMA_COLOR = "blue"





ARCHIVO_CONFIG = resource_path(os.path.join("config", "config.json"))



KEYRING_APP = "AutoCapturaApp"



CLAVE_AUTO_SUBMIT = "auto_submit_nota"
AUTO_SUBMIT_DEFAULT = True


def cargar_auto_submit() -> bool:







    config = cargar_config()
    return config.get(CLAVE_AUTO_SUBMIT, AUTO_SUBMIT_DEFAULT)


def guardar_auto_submit(valor: bool) -> None:






    config = cargar_config()
    config[CLAVE_AUTO_SUBMIT] = valor
    guardar_config(config)









TIMEOUT_ELEMENTO = 15

TIMEOUT_PAGINA = 30

TIMEOUT_CONFIRMACION = 30

REINTENTOS_STALE = 3

PAUSA_REINTENTO_STALE = 0.3

PAUSA_ANIMACION_SPA = 0.5


















SITIOS = [
    {
        "nombre": "HUBSPOT",
        "necesita_login": True,
        "usar_pagina_actual": True,
        "url_login": "https://app.hubspot.com/login/",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "#loginBtn",




        "url_upload": "https://app.hubspot.com/contacts/TICKET_ID",



        "selector_tab_actividades": 'a[data-tab-id="1"]',
        "selector_tab_actividades_fallback": 'a[data-tab-link="true"]',
        "selector_tab_notas": '[data-test-id="timeline-tab-filter-notes"]',
        "selector_btn_crear_nota": 'button[data-selenium-test="create-engagement-note-button"]',
        "selector_btn_adjuntar": '[data-test-id="select-file-dropdown"]',
        "selector_btn_subir": '[data-test-id="select-file-dropdown"]',
        "selector_btn_subir_opcion": 'i18n-string[data-key="customerDataRte.attachmentOptions.upload"]',
        "selector_input_file": 'input[type="file"]',
        "selector_nota_editor": '[data-test-id="rte-content"]',
        "selector_nota_editor_alt": 'div.ProseMirror[contenteditable="true"]',
        "selector_btn_guardar": '[data-test-id="activity-creator-window-footer-save-button"]',
        "selector_confirmacion": "h3, h1",
        "palabras_confirmacion": [
            "uploaded",
            "success",
            "exitoso",
            "subido",
            "note",
            "nota",
            "guardado",
        ],
    },
    {
        "nombre": "SUNRUN",
        "necesita_login": True,
        "url_login": "https://sunrun.my.site.com/partner/login?locale=us",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "#Login",


        "url_base_upload": "https://miejemplo.com/upload",
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
        "selector_confirmacion": "h3, h1",
        "palabras_confirmacion": ["uploaded", "success", "exitoso", "subido"],
    },
]





def cargar_config() -> dict:






    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"[✗] Error cargando config desde {ARCHIVO_CONFIG}: {e}")
    return {}


def guardar_config(datos: dict) -> None:
    """
    Escribe el diccionario 'datos' en config.json con indentación legible.

    Se llama cada vez que el usuario cambia el atajo de teclado o la
    región, para que esos valores persistan en la próxima ejecución.
    En caso de error de escritura, lo reporta por consola sin lanzar excepción.
    """
    try:
        os.makedirs(os.path.dirname(ARCHIVO_CONFIG), exist_ok=True)
        with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[✗] Error guardando config: {e}")


# ── Perfiles de región ────────────────────────────────────────────────
# Los perfiles se guardan dentro de config.json bajo la clave "perfiles_region".




CLAVE_PERFILES = "perfiles_region"



PERFIL_POR_DEFECTO = {"top": 392, "left": 524, "width": 934, "height": 404}


def cargar_perfiles() -> dict:






    config = cargar_config()
    return config.get(CLAVE_PERFILES, {})


def guardar_perfiles(perfiles: dict) -> None:










    config = cargar_config()
    config[CLAVE_PERFILES] = perfiles
    guardar_config(config)





def obtener_monitores() -> list:











    try:
        import mss

        with mss.MSS() as sct:
            return sct.monitors
    except Exception as e:
        print(f"[✗] Error detectando monitores: {e}")
        return []


from typing import List


def obtener_nombres_monitores() -> List[str]:
    """
    Devuelve una lista de nombres legibles para mostrar en la UI.

    Formato: "Monitor 1 (principal)", "Monitor 2", "Todos los monitores".

    Returns
    -------
    List[str] : nombres legibles para cada monitor detectado.























    Devuelve el dict del monitor en la posición 'indice' de la lista.

    Parámetros
    ----------
    indice : int - índice del monitor (0 = virtual, 1 = primer físico, ...)

    Returns
    -------
    dict | None : el monitor o None si no existe.
````

## File: medidor.py
````python
MEDIDOR_CODE = """
import tkinter as tk
import ctypes
import sys

# Necesario en Windows para que las coordenadas sean correctas en
# pantallas con escala (ej. 150 % DPI); sin esto, las coords estarían
# desplazadas en monitores de alta resolución.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass  # En macOS/Linux no hay windll, se ignora sin error.


# ── Detectar monitor desde argumentos ────────────────────────────────
# Busca "--monitor X" en sys.argv. Si no se encuentra, usa monitor 0
# (virtual / todos los monitores) para mantener compatibilidad.
try:
    idx = sys.argv.index("--monitor")
    MONITOR_IDX = int(sys.argv[idx + 1])
except (ValueError, IndexError):
    MONITOR_IDX = 0


def _obtener_monitores():
    \"\"\"Usa mss para obtener la lista de monitores.\"\"\"
    try:
        import mss
        with mss.MSS() as sct:
            return sct.monitors
    except Exception:
        return []


MONITORES = _obtener_monitores()


def _bounds_monitor(indice):
    \"\"\"
    Devuelve (x, y, ancho, alto) del monitor en la posición `indice`.
    Si el índice está fuera de rango, devuelve el escritorio virtual (índice 0).
    \"\"\"
    if 0 <= indice < len(MONITORES):
        m = MONITORES[indice]
    else:
        m = MONITORES[0]
    return m["left"], m["top"], m["width"], m["height"]

# Desplazamiento del monitor donde se mostrará la ventana.
MON_X, MON_Y, MON_W, MON_H = _bounds_monitor(MONITOR_IDX)


class MedidorDeRegion:
    \"\"\"
    Ventana transparente que permite al usuario dibujar un rectángulo
    y obtener sus coordenadas (top, left, width, height).

    Si se especificó un monitor distinto de 0, la ventana se posiciona
    únicamente sobre ese monitor. Con monitor 0 (virtual) cubre toda el
    área del escritorio.
    \"\"\"

    def __init__(self):
        self.root = tk.Tk()
        # Sin bordes ni barra de título: ocupa toda la pantalla o el monitor elegido.
        self.root.overrideredirect(True)
        self.root.geometry(f"{MON_W}x{MON_H}+{MON_X}+{MON_Y}")
        # Semitransparente para que el usuario vea lo que va a capturar.
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>",   self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>",        self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>",  self.al_soltar_clic)

        # Estado interno del dibujo
        self.inicio_x  = None
        self.inicio_y  = None
        self.rectangulo = None
        self.texto      = None

    def al_hacer_clic(self, event):
        \"\"\"Registra el punto de inicio y crea el rectángulo vacío.\"\"\"
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x, self.inicio_y,
            self.inicio_x, self.inicio_y,
            outline="red", width=2,
        )
        # Texto que muestra las dimensiones mientras se arrastra.
        self.texto = self.canvas.create_text(
            self.inicio_x + 10, self.inicio_y - 10,
            text="0 x 0", fill="white",
            font=("Arial", 12, "bold"), anchor="nw",
        )

    def al_arrastrar(self, event):
        \"\"\"Actualiza el rectángulo y el texto de dimensiones en tiempo real.\"\"\"
        self.canvas.coords(
            self.rectangulo,
            self.inicio_x, self.inicio_y,
            event.x, event.y,
        )
        ancho = abs(event.x - self.inicio_x)
        alto  = abs(event.y - self.inicio_y)
        self.canvas.itemconfig(self.texto, text=f"{ancho} x {alto} px")
        # El texto sigue al cursor para no tapar el rectángulo.
        self.canvas.coords(self.texto, event.x + 10, event.y + 10)

    def al_soltar_clic(self, event):
        \"\"\"
        Calcula la región final y la imprime en stdout.

        La app principal lee esta línea del subproceso para obtener las
        coordenadas sin necesitar archivos temporales.

        Nota: las coordenadas devueltas son absolutas (pantalla virtual),
        no relativas al monitor. Esto es necesario porque mss.grab()
        espera coordenadas absolutas.
        \"\"\"
        top    = MON_Y + min(self.inicio_y, event.y)
        left   = MON_X + min(self.inicio_x, event.x)
        width  = abs(event.x - self.inicio_x)
        height = abs(event.y - self.inicio_y)
        region = {"top": top, "left": left, "width": width, "height": height}
        # flush=True garantiza que el pipe lo reciba aunque no haya salto de línea.
        print(f"REGION = {region}", flush=True)
        self.root.destroy()

    def iniciar(self):
        \"\"\"Lanza el loop de eventos de Tkinter.\"\"\"
        self.root.mainloop()


app = MedidorDeRegion()
app.iniciar()
"""
````

## File: plugins/hubspot.py
````python
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

    TIMEOUT = 15
    TIMEOUT_LARGO = 20



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
        contexto_activo = self._capturar_contexto_activo(driver)

        log(f"  → [HubSpot] Iniciando subida: {ruta_abs}")
        esperar_carga(driver)

        try:
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_actividades(driver, log, contexto_activo)
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_notas(driver, log, contexto_activo)
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_crear_nota(driver, log, contexto_activo)
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_editor(driver, log, contexto_activo)
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_adjuntar(driver, log, ruta_abs, contexto_activo)
            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_esperar_archivo(driver, log, ruta_abs, contexto_activo)

            if not auto_submit:
                log("  ✓ [HubSpot] Archivo adjunto. Guardado manual pendiente.")
                return ResultadoSubida(
                    exitoso=True, mensaje="Archivo adjunto (guardado manual)"
                )

            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_guardar(driver, log, contexto_activo)
            return ResultadoSubida(exitoso=True, mensaje="Nota guardada correctamente")

        except Exception as e:
            return ResultadoSubida(exitoso=False, mensaje=f"Error: {e}", detalle=str(e))

    # ── Pasos internos ────────────────────────────────────────────────

    def _espera(self, driver) -> WebDriverWait:
        return WebDriverWait(driver, self.TIMEOUT)

    def _capturar_contexto_activo(self, driver) -> dict:
        url = driver.current_url.lower()
        if self.dominio not in url:
            raise RuntimeError("La pestaña activa no es HubSpot. Subida cancelada.")
        ctx = {
            "handle": driver.current_window_handle,
            "url": url,
            "title": driver.title,
        }
        self._validar_contexto_activo(driver, ctx)
        return ctx

    def _validar_contexto_activo(self, driver, ctx: dict) -> None:
        try:
            misma_tab = driver.current_window_handle == ctx["handle"]
            url_ok = self.dominio in driver.current_url.lower()
            visible = driver.execute_script(
                "return document.visibilityState === 'visible'"
            )
            focused = driver.execute_script("return document.hasFocus()")
        except Exception as e:
            raise RuntimeError(f"No se pudo validar pestaña activa: {e}") from e

        if not misma_tab or not url_ok or not visible or not focused:
            raise RuntimeError(
                "Subida cancelada: cambiaste de pestaña/ventana o HubSpot perdió foco. "
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

    def _paso_actividades(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 1/7: Pestaña Actividades…")
        try:
            tab = self._espera(driver).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_TAB_ACTIVIDADES))
            )
            self._safe_click(driver, tab, ctx)
            time.sleep(0.5)
            log("  ✓ [HubSpot] Pestaña Actividades abierta.")
        except (TimeoutException, NoSuchElementException):
            log("  · [HubSpot] Selector principal falló, intentando fallback…")
            try:
                xpath_fb = f"//{self.SEL_TAB_ACTIVIDADES_FB}[text()='Actividades']"
                tab = self._espera(driver).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_fb))
                )
                self._safe_click(driver, tab, ctx)
                time.sleep(0.5)
            except Exception:
                log("  · [HubSpot] Actividades no encontrado, continuando igual.")

    def _paso_notas(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 2/7: Pestaña Notas…")
        try:
            tab = self._espera(driver).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_TAB_NOTAS))
            )
            self._safe_click(driver, tab, ctx)
            time.sleep(0.5)
            log("  ✓ [HubSpot] Pestaña Notas abierta.")
        except Exception as e:
            raise RuntimeError(f"No se pudo abrir pestaña Notas: {e}") from e

    def _paso_crear_nota(self, driver, log: Callable, ctx: dict) -> None:
        log("  → [HubSpot] Paso 3/7: Crear nota…")
        try:
            btn = self._espera(driver).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.SEL_BTN_CREAR_NOTA))
            )
            self._safe_click(driver, btn, ctx)
            esperar_carga(driver, timeout=5)
            time.sleep(0.5)
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
                time.sleep(0.3)
                self._validar_contexto_activo(driver, ctx)
                driver.execute_script(








,
                    editor,
                )
                self._validar_contexto_activo(driver, ctx)
                time.sleep(0.8)
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
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEL_INPUT_FILE))
            )
            file_input = driver.find_element(By.CSS_SELECTOR, self.SEL_INPUT_FILE)
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
                and nombre.lower() in d.page_source.lower()
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
            time.sleep(1)
            log("  ✓ [HubSpot] Nota guardada.")
        except Exception as e:
            try:
                driver.save_screenshot("debug_error_hubspot_save.png")
            except Exception:
                pass
            raise RuntimeError(f"No se pudo guardar la nota: {e}") from e
````

## File: services/sesion_service.py
````python
from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.browser import BrowserFactory, esperar_carga, puerto_activo
from core.plugin_registry import PluginRegistry
from config.credenciales import cargar_cookies, cargar_credenciales


class SesionService:















    @classmethod
    def ejecutar_subida(
        cls,
        nombre_plugin: str,
        ruta_imagen: str,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
        credenciales_sesion: dict | None = None,
        opciones: dict | None = None,
    ) -> ResultadoSubida:






        plugin = PluginRegistry.obtener(nombre_plugin)
        driver = None
        driver_propio = False

        try:

            driver, driver_propio = cls._obtener_driver(
                log, headless, usar_chrome_existente
            )


            cls._posicionar_pestana(driver, plugin, log)


            cls._asegurar_sesion(driver, plugin, log, credenciales_sesion or {})


            credenciales = cls._obtener_credenciales(
                plugin.nombre, credenciales_sesion or {}
            )
            ctx = ContextoSubida(
                ruta_imagen=ruta_imagen,
                log=log,
                driver=driver,
                credenciales=credenciales,
                opciones=opciones or {},
            )
            log(f"  → [{plugin.nombre}] Iniciando subida…")
            resultado = plugin.subir(ctx)

            if resultado.exitoso:
                log(f"  ✓ [{plugin.nombre}] {resultado.mensaje}")
            else:
                log(f"  ✗ [{plugin.nombre}] {resultado.mensaje}")

            return resultado

        except Exception as e:
            log(f"  ✗ [{nombre_plugin}] Error inesperado: {e}")
            return ResultadoSubida(exitoso=False, mensaje=str(e))

        finally:
            if driver_propio and driver:
                try:
                    driver.quit()
                    log(f"  · [{nombre_plugin}] Chrome cerrado.")
                except Exception:
                    pass

    # ── Pasos internos ────────────────────────────────────────────────

    @staticmethod
    def _obtener_driver(log: Callable, headless: bool, usar_existente: bool):
        """Crea o conecta el driver. Devuelve (driver, es_propio)."""
        from core.browser import ErrorBrowser

        if usar_existente:
            if not puerto_activo():
                raise RuntimeError(
                    "No hay Chrome con depuración en puerto 9222. "
                    "Ábrelo desde el botón 'Abrir Chrome con depuración'."
                )
            log("  → Conectando al Chrome existente (puerto 9222)…")
            driver = BrowserFactory.conectar_existente()
            log("  ✓ Conectado.")
            return driver, False
        else:
            log("  → Abriendo Chrome nuevo…")
            driver = BrowserFactory.nuevo(headless=headless)
            log("  ✓ Chrome abierto.")
            return driver, True

    @staticmethod
    def _posicionar_pestana(driver, plugin: SitioPlugin, log: Callable) -> None:
        """Valida SOLO la pestaña actual; nunca recorre ni cambia tabs del usuario."""
        if plugin.usar_pagina_actual and plugin.dominio:
            log(f"  → Validando pestaña activa de {plugin.nombre}…")
            handle = driver.current_window_handle
            url = driver.current_url.lower()
            if plugin.dominio.lower() not in url:
                raise RuntimeError(
                    f"La pestaña activa no es {plugin.nombre}. "
                    f"Ubicate en la pestaña visible/enfocada de {plugin.nombre} y reintentá."
                )
            try:
                mismo_handle = driver.current_window_handle == handle
                visible = driver.execute_script(
                    "return document.visibilityState === 'visible'"
                )
                focused = driver.execute_script("return document.hasFocus()")
            except Exception:
                mismo_handle = visible = focused = False
            if not mismo_handle or not visible or not focused:
                raise RuntimeError(
                    "Subida cancelada: la pestaña/ventana activa perdió foco. "
                    "No se subió información."
                )
            log(f"  ✓ Pestaña activa validada.")
        elif not plugin.usar_pagina_actual and plugin.dominio:
            log(f"  · [{plugin.nombre}] No se cambia de pestaña automáticamente.")

    @staticmethod
    def _asegurar_sesion(
        driver, plugin: SitioPlugin, log: Callable, credenciales_sesion: dict
    ) -> None:
        """
        Verifica la sesión. Si no está activa y es Chrome existente, advierte.
        Si es Chrome nuevo, intenta restaurar cookies o hacer login automático.
        """
        if plugin.usar_pagina_actual:
            # Modo página actual: el usuario ya tiene la sesión. Solo verificamos.
            plugin.verificar_sesion(driver, log)
            return

        # Chrome propio: intentar cookies primero, luego login
        ruta_cookies = Path(f"cookies/{plugin.nombre}.pkl")
        if ruta_cookies.exists():
            log(f"  → Restaurando sesión con cookies para {plugin.nombre}…")
            url_base = getattr(plugin, "URL_LOGIN", "")
            if url_base:
                try:
                    cargar_cookies(driver, {"nombre": plugin.nombre}, url_base)
                    esperar_carga(driver, timeout=5)
                    if plugin.verificar_sesion(driver, log):
                        return
                    log("  · Cookies inválidas, iniciando login…")
                except Exception as e:
                    log(f"  · Error restaurando cookies: {e}")

        # Login automático
        credenciales = SesionService._obtener_credenciales(
            plugin.nombre, credenciales_sesion
        )
        if credenciales:
            if plugin.hacer_login(driver, credenciales, log):
                return
        raise RuntimeError(
            f"No se pudo establecer sesión para {plugin.nombre}. "
            f"Verifica las credenciales en el menú 'Credenciales'."
        )

    @staticmethod
    def _obtener_credenciales(nombre_plugin: str, sesion: dict) -> dict:
        """Credenciales de la sesión actual o del llavero del SO."""
        if nombre_plugin in sesion:
            return sesion[nombre_plugin]
        usuario, clave = cargar_credenciales(nombre_plugin)
        if usuario:
            return {"usuario": usuario, "clave": clave}
        return {}
````

## File: ui/ventana_credenciales.py
````python
import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import cargar_config
from config.credenciales import (
    cargar_credenciales,
    guardar_credenciales,
    borrar_credenciales,
)
from ui.posicion_ventanas import ubicar_junto_a_padre


class VentanaCredenciales(ctk.CTkToplevel):














    def __init__(self, parent, sitios: list):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")
        self.resizable(False, False)


        self.grab_set()
        self.confirmado = False
        self._construir_ui()
        ubicar_junto_a_padre(self, parent)

        self.transient(parent)

        self.wait_window()
        self._config = cargar_config()
        config = cargar_config()
        ctk.set_appearance_mode(config.get("tema", "dark"))

    def _construir_ui(self):

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Configurar credenciales",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, pady=(16, 12), padx=20, sticky="w")

        self.campos = {}
        indice_fila = 1

        for sitio in self.sitios:
            if not sitio.get("necesita_login"):
                continue

            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)


            frame = ctk.CTkFrame(self, fg_color=("gray95", "gray20"), border_width=1)
            frame.grid(row=indice_fila, column=0, sticky="ew", padx=20, pady=(0, 10))
            frame.grid_columnconfigure(1, weight=1)
            indice_fila += 1

            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("royalblue", "#4a9eff"),
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(10, 6))

            var_usuario = ctk.StringVar(value=usuario_guardado)
            var_clave = ctk.StringVar(value=clave_guardada)


            ctk.CTkLabel(
                frame,
                text="Usuario",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=1, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_usuario,
                width=220,
                font=ctk.CTkFont(size=11),
            ).grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=4)


            ctk.CTkLabel(
                frame,
                text="Contraseña",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=2, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_clave,
                width=220,
                show="*",
                font=ctk.CTkFont(size=11),
            ).grid(row=2, column=1, sticky="ew", padx=(0, 14), pady=4)


            var_recordar = ctk.BooleanVar(value=tiene_guardado)
            ctk.CTkSwitch(
                frame,
                text="  Recordar credenciales",
                variable=var_recordar,
                font=ctk.CTkFont(size=11),
            ).grid(row=3, column=0, columnspan=2, sticky="w", padx=14, pady=(6, 12))

            self.campos[nombre] = {
                "usuario": var_usuario,
                "clave": var_clave,
                "recordar": var_recordar,
            }


        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(
            row=indice_fila + 1, column=0, sticky="e", padx=20, pady=(4, 16)
        )
        frame_botones.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self._cancelar,
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            width=100,
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            frame_botones,
            text="Continuar",
            command=self._confirmar,
            font=ctk.CTkFont(size=11, weight="bold"),
            width=100,
        ).pack(side="right")

    def _confirmar(self):





        for nombre, vars_ in self.campos.items():
            if not vars_["usuario"].get().strip() or not vars_["clave"].get().strip():
                messagebox.showerror(
                    "Campos vacíos",
                    f"Completa usuario y contraseña para:\n{nombre}",
                    parent=self,
                )
                return

        # Guardar o eliminar según el switch 'Recordar'.
        for nombre, vars_ in self.campos.items():
            if vars_["recordar"].get():
                guardar_credenciales(
                    nombre, vars_["usuario"].get(), vars_["clave"].get()
                )
            else:
                borrar_credenciales(nombre)


        self.credenciales_sesion = {
            nombre: {
                "usuario": vars_["usuario"].get(),
                "clave": vars_["clave"].get(),
            }
            for nombre, vars_ in self.campos.items()
        }

        self.confirmado = True
        self.destroy()

    def _cancelar(self):

        self.confirmado = False
        self.destroy()
````

## File: ui/ventana_plantillas.py
````python
import json
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from ui.posicion_ventanas import ubicar_junto_a_padre

PLANTILLAS_PATH = Path("config/plantillas.json")

PLANTILLAS_DEFAULT = [
    {
        "titulo": "Saludo inicial",
        "categoria": "HubSpot",
        "texto": "Hola [Nombre], espero que estés muy bien. Me comunico para hacerte seguimiento sobre tu solicitud. ¿Tienes alguna duda o necesitas información adicional?",
    },
    {
        "titulo": "Nota de seguimiento",
        "categoria": "HubSpot",
        "texto": "Se realizó llamada al cliente [Nombre] el [Fecha]. Se discutió [Tema]. Próximo paso: [Acción]. Fecha estimada: [Fecha siguiente].",
    },
    {
        "titulo": "Confirmación de cita",
        "categoria": "HubSpot",
        "texto": "Hola [Nombre], confirmamos tu cita para el día [Fecha] a las [Hora]. Por favor avísanos con anticipación si necesitas reagendar.",
    },
    {
        "titulo": "Actualización de estado",
        "categoria": "Sunrun",
        "texto": "Actualización de estado para el caso [ID]: El sistema se encuentra en etapa [Estado]. Tiempo estimado de resolución: [Tiempo].",
    },
    {
        "titulo": "Cierre de caso",
        "categoria": "Sunrun",
        "texto": "El caso [ID] ha sido cerrado exitosamente el [Fecha]. Motivo de cierre: [Motivo]. Si tiene alguna consulta adicional no dude en contactarnos.",
    },
    {
        "titulo": "Sin respuesta",
        "categoria": "General",
        "texto": "Hola [Nombre], intentamos comunicarnos contigo sin éxito. Por favor contáctanos al [Teléfono] o responde este mensaje para continuar con tu proceso.",
    },
]


def _cargar_plantillas() -> list:
    if PLANTILLAS_PATH.exists():
        try:
            return json.loads(PLANTILLAS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return PLANTILLAS_DEFAULT.copy()


def _guardar_plantillas(plantillas: list):
    PLANTILLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLANTILLAS_PATH.write_text(
        json.dumps(plantillas, ensure_ascii=False, indent=2), encoding="utf-8"
    )


class VentanaPlantillas(ctk.CTkToplevel):







    def __init__(self, parent):
        super().__init__(parent)
        self.title("Plantillas de mensajes")
        self.geometry("780x520")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._plantillas = _cargar_plantillas()
        self._indice_actual: int | None = None

        self._construir_ui()
        ubicar_junto_a_padre(self, parent)
        self._poblar_lista()



    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        panel_izq = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color=("gray92", "gray17")
        )
        panel_izq.grid(row=0, column=0, sticky="nsew")
        panel_izq.grid_propagate(False)
        panel_izq.grid_rowconfigure(1, weight=1)
        panel_izq.grid_columnconfigure(0, weight=1)


        ctk.CTkLabel(
            panel_izq,
            text="PLANTILLAS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))


        self._frame_lista = ctk.CTkScrollableFrame(
            panel_izq,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._frame_lista.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        self._frame_lista.grid_columnconfigure(0, weight=1)


        ctk.CTkButton(
            panel_izq,
            text="+ Nueva plantilla",
            command=self._nueva_plantilla,
            font=ctk.CTkFont(size=11),
            height=32,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).grid(row=2, column=0, sticky="ew", padx=8, pady=8)


        panel_der = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        panel_der.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        panel_der.grid_rowconfigure(2, weight=1)
        panel_der.grid_columnconfigure(0, weight=1)


        ctk.CTkLabel(
            panel_der,
            text="Título",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 2))

        fila_titulo = ctk.CTkFrame(panel_der, fg_color="transparent")
        fila_titulo.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        fila_titulo.grid_columnconfigure(0, weight=1)

        self._titulo_var = ctk.StringVar()
        ctk.CTkEntry(
            fila_titulo,
            textvariable=self._titulo_var,
            font=ctk.CTkFont(size=13, weight="bold"),
            placeholder_text="Nombre de la plantilla",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))


        self._cat_var = ctk.StringVar(value="General")
        ctk.CTkOptionMenu(
            fila_titulo,
            variable=self._cat_var,
            values=["General", "HubSpot", "Sunrun"],
            font=ctk.CTkFont(size=11),
            width=110,
        ).grid(row=0, column=1)


        ctk.CTkLabel(
            panel_der,
            text="Mensaje",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).grid(row=2, column=0, sticky="nw", padx=16, pady=(0, 2))

        self._texto_box = ctk.CTkTextbox(
            panel_der,
            font=ctk.CTkFont(size=12),
            wrap="word",
        )
        self._texto_box.grid(row=2, column=0, sticky="nsew", padx=16, pady=(18, 8))


        barra_inf = ctk.CTkFrame(panel_der, fg_color="transparent")
        barra_inf.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 14))

        ctk.CTkButton(
            barra_inf,
            text="📋  Copiar al portapapeles",
            command=self._copiar,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        ).pack(side="left")

        ctk.CTkButton(
            barra_inf,
            text="Guardar cambios",
            command=self._guardar_actual,
            font=ctk.CTkFont(size=11),
            height=36,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(8, 0))

        ctk.CTkButton(
            barra_inf,
            text="Eliminar",
            command=self._eliminar_actual,
            font=ctk.CTkFont(size=11),
            height=36,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="right")


        self._label_copia = ctk.CTkLabel(
            panel_der,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("
        )
        self._label_copia.grid(row=4, column=0, pady=(0, 4))



    def _poblar_lista(self):

        for w in self._frame_lista.winfo_children():
            w.destroy()

        categorias: dict[str, list] = {}
        for i, p in enumerate(self._plantillas):
            cat = p.get("categoria", "General")
            categorias.setdefault(cat, []).append((i, p))

        COLOR_CAT = {
            "HubSpot": ("#1f6aa5", "#4a9eff"),
            "Sunrun": ("#8b4500", "#f0a050"),
            "General": ("gray50", "gray50"),
        }

        fila = 0
        for cat, items in categorias.items():
            color = COLOR_CAT.get(cat, ("gray50", "gray50"))
            ctk.CTkLabel(
                self._frame_lista,
                text=cat.upper(),
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=color,
                anchor="w",
            ).grid(row=fila, column=0, sticky="w", padx=8, pady=(10, 2))
            fila += 1

            for idx, p in items:
                btn = ctk.CTkButton(
                    self._frame_lista,
                    text=p["titulo"],
                    anchor="w",
                    font=ctk.CTkFont(size=12),
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray80", "gray30"),
                    height=30,
                    command=lambda i=idx: self._seleccionar(i),
                )
                btn.grid(row=fila, column=0, sticky="ew", padx=4, pady=1)
                fila += 1


        if self._plantillas and self._indice_actual is None:
            self._seleccionar(0)

    def _seleccionar(self, indice: int):

        self._indice_actual = indice
        p = self._plantillas[indice]
        self._titulo_var.set(p["titulo"])
        self._cat_var.set(p.get("categoria", "General"))
        self._texto_box.delete("0.0", "end")
        self._texto_box.insert("0.0", p["texto"])
        self._label_copia.configure(text="")

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _copiar(self):
        texto = self._texto_box.get("0.0", "end").strip()
        if not texto:
            return
        self.clipboard_clear()
        self.clipboard_append(texto)
        self._label_copia.configure(text="✓ Copiado al portapapeles")
        self.after(2500, lambda: self._label_copia.configure(text=""))

    def _guardar_actual(self):
        titulo = self._titulo_var.get().strip()
        texto = self._texto_box.get("0.0", "end").strip()
        if not titulo:
            messagebox.showerror(
                "Campo vacío", "Escribe un título para la plantilla.", parent=self
            )
            return
        entrada = {"titulo": titulo, "categoria": self._cat_var.get(), "texto": texto}
        if self._indice_actual is not None:
            self._plantillas[self._indice_actual] = entrada
        else:
            self._plantillas.append(entrada)
            self._indice_actual = len(self._plantillas) - 1
        _guardar_plantillas(self._plantillas)
        self._poblar_lista()
        self._label_copia.configure(text="✓ Plantilla guardada")
        self.after(2500, lambda: self._label_copia.configure(text=""))

    def _nueva_plantilla(self):
        self._indice_actual = None
        self._titulo_var.set("")
        self._cat_var.set("General")
        self._texto_box.delete("0.0", "end")
        self._label_copia.configure(text="")

    def _eliminar_actual(self):
        if self._indice_actual is None:
            return
        titulo = self._plantillas[self._indice_actual]["titulo"]
        if not messagebox.askyesno(
            "Eliminar", f"¿Eliminar la plantilla «{titulo}»?", parent=self
        ):
            return
        self._plantillas.pop(self._indice_actual)
        self._indice_actual = None
        _guardar_plantillas(self._plantillas)
        # Limpiar editor
        self._titulo_var.set("")
        self._texto_box.delete("0.0", "end")
        self._poblar_lista()
````

## File: ui/ventana_comparacion.py
````python
import threading
import customtkinter as ctk
from tkinter import messagebox
from ui.custom_ctkframe import CustomCTkFrame
from core.comparador import comparar, datos_hs_desde_ticket
from scraping_sunrun import ScraperSunrun
from config.configuracion import cargar_config





COLORES_ESTADO = {
    "igual": {
        "bg": ("#d4edda", "#1a3a2a"),
        "texto": ("#155724", "#3fb950"),
        "icono": "✅",
    },
    "similar": {
        "bg": ("#fff3cd", "#3a3000"),
        "texto": ("#856404", "#d4a017"),
        "icono": "🟡",
    },
    "diferente": {
        "bg": ("#f8d7da", "#3a1a1a"),
        "texto": ("#721c24", "#f85149"),
        "icono": "❌",
    },
    "solo_hs": {
        "bg": ("#cce5ff", "#1a2a3a"),
        "texto": ("#004085", "#79c0ff"),
        "icono": "🔵",
    },
    "solo_sunrun": {
        "bg": ("#ffe5cc", "#3a2a1a"),
        "texto": ("#804000", "#f0a050"),
        "icono": "🟠",
    },
    "ambos_vacios": {
        "bg": ("#e2e3e5", "#2a2a2a"),
        "texto": ("#6c757d", "#6e7681"),
        "icono": "⚪",
    },
}

ETIQUETAS_ESTADO = {
    "igual": "IGUAL",
    "similar": "SIMILAR",
    "diferente": "DIFERENTE",
    "solo_hs": "SOLO HUBSPOT",
    "solo_sunrun": "SOLO SUNRUN",
    "ambos_vacios": "SIN DATOS",
}







class VentanaComparacion(CustomCTkFrame):















    def __init__(
        self,
        parent,
        datos_hubspot: dict = None,
        datos_sunrun: dict = None,
        log_callback=None,
    ):
        super().__init__(parent)
        self._log_ext = log_callback or (lambda m: None)
        self._datos_hs = datos_hubspot
        self._datos_sr = datos_sunrun

        self.update_idletasks()
        ancho, alto = 820, 560
        px = max(0, (self.winfo_screenwidth() - ancho) // 2)
        py = max(0, (self.winfo_screenheight() - alto) // 2)

        self._construir_ui()

        self.after(50, self._traer_al_frente)

        if datos_hubspot and datos_sunrun:
            self.after(100, self._mostrar_resultado_externo)

    def _traer_al_frente(self):

        try:




            root = self.winfo_toplevel()
            if root.state() == "iconic":
                root.deiconify()
            root.lift()
            root.focus_force()
            root.attributes("-topmost", True)
            self.after(200, lambda: root.attributes("-topmost", False))
        except Exception:
            pass

    def _cerrar(self):

        try:
            self.destroy()
        except Exception:
            pass



    def _construir_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)


        enc = ctk.CTkFrame(self, fg_color=("gray88", "gray20"), height=50)
        enc.grid(row=0, column=0, sticky="ew")
        enc.grid_propagate(False)

        ctk.CTkLabel(
            enc,
            text="  🔍  Comparación de datos: HubSpot ↔ Sunrun",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=16, pady=12)


        fila_busqueda = ctk.CTkFrame(self, fg_color=("gray95", "gray18"))
        fila_busqueda.grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 0))
        fila_busqueda.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            fila_busqueda,
            text="FSD:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, padx=(14, 8), pady=12)

        self._fsd_var = ctk.StringVar()
        self._entry_fsd = ctk.CTkEntry(
            fila_busqueda,
            textvariable=self._fsd_var,
            placeholder_text="Ej: FSD983316",
            font=ctk.CTkFont(size=12),
        )
        self._entry_fsd.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=12)
        self._entry_fsd.bind("<Return>", lambda e: self._lanzar_comparacion())

        self._btn_comparar = ctk.CTkButton(
            fila_busqueda,
            text="Comparar",
            command=self._lanzar_comparacion,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=110,
            height=34,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self._btn_comparar.grid(row=0, column=2, padx=(0, 14), pady=12)


        self._frame_resultados = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._frame_resultados.grid(
            row=2, column=0, sticky="nsew", padx=12, pady=(10, 0)
        )
        self._frame_resultados.grid_columnconfigure(0, weight=1)

        self._label_placeholder = ctk.CTkLabel(
            self._frame_resultados,
            text="Ingresa un número FSD y presiona Comparar.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )
        self._label_placeholder.grid(row=0, column=0, pady=40)


        self._status_var = ctk.StringVar(value="Listo")
        barra = ctk.CTkFrame(self, fg_color=("gray88", "gray20"), height=30)
        barra.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        barra.grid_propagate(False)
        ctk.CTkLabel(
            barra,
            textvariable=self._status_var,
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=12)

    def _lanzar_comparacion(self):
        fsd = self._fsd_var.get().strip()
        if not fsd:
            messagebox.showwarning("FSD vacío", "Ingresa un número FSD.", parent=self)
            return

        self._btn_comparar.configure(state="disabled")
        self._status_var.set(f"Buscando {fsd}...")
        self._limpiar_resultados()

        threading.Thread(
            target=self._proceso_comparacion, args=(fsd,), daemon=True
        ).start()

    def _proceso_comparacion(self, fsd: str):
        """
        Hilo secundario: obtiene datos de Sunrun (Chrome), luego de HubSpot
        (API), compara y actualiza la UI con self.after().
        """

        def ui_log(msg):
            self.after(0, lambda m=msg: self._log_ext(m))
            self.after(0, lambda m=msg: self._status_var.set(m.strip()))

        try:
            ui_log(f"  → Buscando {fsd} en Sunrun...")
            scraper = ScraperSunrun(log_callback=ui_log)
            datos_sr = scraper.obtener_datos_por_fsd(fsd)

            ui_log("  → Obteniendo datos desde HubSpot...")
            datos_hs = self._obtener_hubspot(fsd, ui_log)

            ui_log("  → Comparando campos...")
            resultado = comparar(datos_hs, datos_sr)
            resultado["fsd"] = fsd
            resultado["_sunrun_extra"] = {
                "appointment_date": datos_sr.get("appointment_date", ""),
                "case_reason": datos_sr.get("case_reason", ""),
            }

            self.after(0, lambda r=resultado: self._mostrar_resultado(r))

        except Exception as e:
            self.after(0, lambda err=e: self._mostrar_error(str(err)))
        finally:
            self.after(0, lambda: self._btn_comparar.configure(state="normal"))
            self.after(0, lambda: self._status_var.set("Listo"))

    def _obtener_hubspot(self, fsd: str, log) -> dict:
        _vacio = {
            "fsd": fsd,
            "ticket_id": None,
            "contact_id": None,
            "nombre": "",
            "id_cliente": "",
            "direccion": "",
            "telefono": "",
            "telefono_alterno": "",
            "email": "",
            "estado": "",
            "municipio": "",
            "zip": "",
            "nota": "",
            "fuente_nombre": "",
            "fuente_id": "",
            "fuente": "HubSpot",
        }
        try:
            from data.api import extraer_datos_hubspot

            datos = extraer_datos_hubspot(fsd)
            if datos.get("error"):
                log(f"  ⚠ HubSpot: {datos['error']}")
            return datos_hs_desde_ticket(datos)

        except ImportError:
            log("  ⚠  api.py no disponible. Usando datos vacíos para HubSpot.")
            return {**_vacio, "error": "Módulo  api.py no disponible."}

        except Exception as e:
            log(f"  ✗ Error al consultar HubSpot: {e}")
            return {**_vacio, "error": str(e)}



    def _limpiar_resultados(self):
        for widget in self._frame_resultados.winfo_children():
            widget.destroy()

    def _mostrar_resultado_externo(self):

        resultado = comparar(self._datos_hs, self._datos_sr)

        resultado["_sunrun_extra"] = {
            "appointment_date": self._datos_sr.get("appointment_date", ""),
            "case_reason": self._datos_sr.get("case_reason", ""),
        }

        self._mostrar_resultado(resultado)

    def _mostrar_resultado(self, resultado: dict):
        """
        Renderiza la tabla de comparación con colores por estado.

        FIX #4: antes se llamaba self.state() y self.deiconify() directamente
        sobre el Frame, lo que lanzaba AttributeError silenciado y nunca
        restauraba la ventana. Ahora se delega al toplevel real.
        """
        self._limpiar_resultados()

        # Restaurar toplevel si estaba minimizado y traer al frente
        try:
            root = self.winfo_toplevel()
            if root.state() == "iconic":
                root.deiconify()
            root.lift()
            root.focus_force()
        except Exception:
            pass

        frame = self._frame_resultados
        fila = 0


        hdr = ctk.CTkFrame(frame, fg_color=("gray85", "gray22"), border_width=1)
        hdr.grid(row=fila, column=0, sticky="ew", pady=(0, 8))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr,
            text=f"  Ticket: {resultado['fsd']}",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=10)
        fila += 1
        sunrun_extra = resultado.get("_sunrun_extra")

        if sunrun_extra:

            sr_frame = ctk.CTkFrame(
                frame,
                fg_color=("#ffe5cc", "#3a2a1a"),
                border_width=1,
            )

            sr_frame.grid(
                row=fila,
                column=0,
                sticky="ew",
                pady=(0, 8),
            )

            sr_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                sr_frame,
                text="☀ Sunrun",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#804000", "#f0a050"),
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=14,
                pady=(10, 6),
            )

            campos_extra = [
                ("Appointment Date", sunrun_extra.get("appointment_date", "")),
                ("Case Reason", sunrun_extra.get("case_reason", "")),
            ]

            for idx, (label, valor) in enumerate(campos_extra, start=1):

                ctk.CTkLabel(
                    sr_frame,
                    text=f"{label}:",
                    font=ctk.CTkFont(size=11, weight="bold"),
                ).grid(
                    row=idx,
                    column=0,
                    sticky="nw",
                    padx=(14, 8),
                    pady=2,
                )

                ctk.CTkLabel(
                    sr_frame,
                    text=valor or "-",
                    font=ctk.CTkFont(size=11),
                    wraplength=320,
                    justify="left",
                    anchor="w",
                ).grid(
                    row=idx,
                    column=1,
                    sticky="ew",
                    padx=(0, 14),
                    pady=2,
                )

            fila += 1


        if resultado.get("tiene_error") and resultado.get("errores"):
            err_frame = ctk.CTkFrame(
                frame, fg_color=("#f8d7da", "#3a1a1a"), border_width=1
            )
            err_frame.grid(row=fila, column=0, sticky="ew", pady=(0, 8))
            for err in resultado["errores"]:
                ctk.CTkLabel(
                    err_frame,
                    text=f"  ⚠ {err}",
                    font=ctk.CTkFont(size=11),
                    text_color=("
                    wraplength=700,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=4)
            fila += 1


        cols_hdr = ctk.CTkFrame(frame, fg_color=("gray80", "gray28"))
        cols_hdr.grid(row=fila, column=0, sticky="ew", pady=(0, 2))
        cols_hdr.grid_columnconfigure(0, weight=2)
        cols_hdr.grid_columnconfigure(1, weight=3)
        cols_hdr.grid_columnconfigure(2, weight=3)
        cols_hdr.grid_columnconfigure(3, weight=2)

        for i, titulo in enumerate(["Campo", "HubSpot", "Sunrun", "Estado"]):
            ctk.CTkLabel(
                cols_hdr,
                text=titulo,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("gray30", "gray70"),
            ).grid(row=0, column=i, sticky="w", padx=14, pady=6)
        fila += 1


        for campo_resultado in resultado["campos"]:
            self._fila_campo(frame, fila, campo_resultado)
            fila += 1


        fila += 1
        self._resumen(frame, fila, resultado["resumen"])

    def _fila_campo(self, parent, fila: int, cr: dict):
        estado = cr["estado"]
        colores = COLORES_ESTADO.get(estado, COLORES_ESTADO["ambos_vacios"])

        row_frame = ctk.CTkFrame(
            parent,
            fg_color=colores["bg"],
            border_width=1,
        )
        row_frame.grid(row=fila, column=0, sticky="ew", pady=2)
        row_frame.grid_columnconfigure(0, weight=2)
        row_frame.grid_columnconfigure(1, weight=3)
        row_frame.grid_columnconfigure(2, weight=3)
        row_frame.grid_columnconfigure(3, weight=2)

        def celda(texto, col, bold=False):
            ctk.CTkLabel(
                row_frame,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold" if bold else "normal"),
                text_color=colores["texto"],
                wraplength=180,
                justify="left",
                anchor="w",
            ).grid(row=0, column=col, sticky="w", padx=14, pady=10)

        celda(cr["campo"], col=0, bold=True)
        celda(cr["valor_hs"], col=1)
        celda(cr["valor_sr"], col=2)

        estado_txt = f"{colores['icono']} {ETIQUETAS_ESTADO.get(estado, estado)}"
        ctk.CTkLabel(
            row_frame,
            text=estado_txt,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colores["texto"],
        ).grid(row=0, column=3, sticky="w", padx=14, pady=10)

        if cr.get("nota") and estado not in ("igual", "ambos_vacios"):
            nota_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            nota_frame.grid(row=1, column=0, columnspan=4, sticky="ew")
            ctk.CTkLabel(
                nota_frame,
                text=f"  ℹ {cr['nota']}",
                font=ctk.CTkFont(size=10),
                text_color=colores["texto"],
            ).grid(row=0, column=0, sticky="w", padx=14, pady=(0, 6))

    def _resumen(self, parent, fila: int, resumen: dict):
        frame = ctk.CTkFrame(parent, fg_color=("gray88", "gray22"), border_width=1)
        frame.grid(row=fila, column=0, sticky="ew", pady=(12, 4))

        ctk.CTkLabel(
            frame,
            text="  Resumen:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(side="left", padx=(14, 16), pady=10)

        orden = [
            "igual",
            "similar",
            "diferente",
            "solo_hs",
            "solo_sunrun",
            "ambos_vacios",
        ]
        for estado in orden:
            count = resumen.get(estado, 0)
            if count == 0:
                continue
            col = COLORES_ESTADO[estado]
            ctk.CTkLabel(
                frame,
                text=f"{col['icono']} {ETIQUETAS_ESTADO[estado]}: {count}",
                font=ctk.CTkFont(size=10),
                text_color=col["texto"],
            ).pack(side="left", padx=8, pady=10)

    def _mostrar_error(self, mensaje: str):
        self._limpiar_resultados()
        ctk.CTkLabel(
            self._frame_resultados,
            text=f"✗ {mensaje}",
            font=ctk.CTkFont(size=12),
            text_color=("red", "#f85149"),
            wraplength=600,
        ).grid(row=0, column=0, pady=40)


if __name__ == "__main__":
    config = cargar_config()
    ctk.set_appearance_mode(config.get("tema", "dark"))
    root = ctk.CTk()
    root.withdraw()
    app = VentanaComparacion(root)
    root.mainloop()
````

## File: doku.md
````markdown
# **interfaz2.py**

  # 04-05-2026
  # Ejemplo de links para sunrun
* https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000pd7qf2AA/fsd1217790

* https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000iYmqV2AS/fsd1187405

#
  El dia de hoy empece la creacion de un script en Python para la automatización de capturas de pantallas con MSS y subida a sitios web con Selenium,
  con una interfaz gráfica en Tkinter.
  Implementé un medidor de región para seleccionar el área de captura.
  El sistema permite seleccionar una región de la pantalla, capturarla, y luego subirla a diferentes sitios web, algunos de los cuales requieren autenticación.
  Se puede controlar el modo headless para que Chrome no abra una ventana visible.
  La interfaz permite configurar el tamaño de la region, de forma manual y automatica con el medidor (boton),
  y también configurar un atajo de teclado para ejecutar la captura y subida, el cual se guarda en un archivo JSON de config.
  La idea de este proyecto es facilitar la captura y compartición de evidencias, para las plataformas de HubSpot y SunRun, que son las mas utilizadas en el trabajo a diario,
  y que conllevan muchos pasos manuales para subir las capturas a cada plataforma, con este sistema se busca automatizar ese proceso y ahorrar tiempo.
  Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
  Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

  # 05-05-2026

  En el dia de hoy, me enfoqué en implementar la funcionalidad de login para los sitios que lo requieren, utilizando Selenium para automatizar el proceso de autenticación.
  Creé una ventana modal de login que se muestra al iniciar la aplicación, donde se pueden ingresar y guardar las credenciales de cada sitio de forma
  segura utilizando la librería keyring.
  La función de subida ahora incluye el proceso de login automático antes de intentar subir la imagen,
  lo que permite manejar sitios con autenticación sin necesidad de ingresar las credenciales cada vez.
  Además, se agregó una validación para verificar que el login fue exitoso antes de proceder con la subida, y se muestra un mensaje de error si el login falla.
  Se implemento un sistema de cookies para intentar restaurar la sesión antes de hacer login, lo que puede evitar la necesidad de autenticarse en cada ejecución
  si las cookies siguen siendo válidas. Ademas de las cookies un boton para renovar la sesión, que borra las cookies guardadas y fuerza un login fresco en la próxima ejecución.
  Tambien añadi una opción para reutilizar una sesión de Chrome ya abierta, lo que permite aprovechar una sesión activa sin necesidad de hacer login automático cada vez,
  aunque requiere que el usuario inicie sesión manualmente en el navegador.
  Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
  Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

  arreglado
  realmente es necesario iniciar sesion cada vez que se quiera subir una captura a un sitio que requiere autenticacion?, ademas si el sitio se mantiene abierto siempre
  en el navegador, no se podria aprovechar esa sesion activa para subir las capturas sin necesidad de hacer login cada vez?

  arreglado
  Hay que arreglar el chrome con depuracion, ya que se abre bien, pero cuando se ejecuta la captura y subida, no detecta la sesión activa, aunque el Chrome abierto
   tenga sesión iniciada en el sitio, entonces hace el login automático, pero no funciona, no detecta que se hizo login exitoso,
   y no sube la imagen. Hay que revisar esa parte para que funcione correctamente con un Chrome ya abierto y con sesión activa.

  # 06-05-2026

  Hoy empece a arreglar el chrome con depuracion (cuando las paginas ya estan abiertas), el problema era que, aunque se detectaba
  la sesión activa en el Chrome abierto, al navegar a la página de subida, el sitio redirigía a la página de login, lo que
  indicaba que no se estaba aprovechando la sesión activa correctamente. Entonces cuando se tomaba la captura se abrian las pestañas
  correspondientes a cada sitio y se subian las capturas correctamente, pero la idea era que si el usuario ya tenia sesión iniciada
  en el Chrome abierto, se aprovechara esa sesión para subir las capturas sin necesidad de hacer login automático cada vez,
  pero no estaba funcionando así. Entonces, para solucionar esto, modifiqué el flujo para que después de detectar la sesión activa,
  se navegue directamente a la página de subida en las pestañas correspondientes donde ya habia una sesion iniciada, esperando que
  no se abrieran nuevas pestañas, ademas de esto se debe confirmar la subida de la imagen al sitio, con su respectivo boton.
  Se añadieron colores y se reorganizo la estructura de la interfaz, ahora se ve mas estetico, ademas la interfaz se adapta a la
  resolucion de la pantalla

  PENDIENTES: PONERLE LINEA DE TIEMPO, TIEMPO DE DESARROLLO, Y PROXIMOS PASOS, MEJORAS FUTURAS, ETC.

  # 07-05-2026
  Se añadio scroll para que el contenido de la interfaz se vea correctamente, ademas ahora al minimizar y maximizar, el contenido se adapta correctamente.
  Se migro todo el script de Tkinter a CustomTkinter con toda la funcionalidad preservada, lo que nos permitio hacer una interfaz mas estetica y mas facil de optimizar, CustomTkinter permite hacer que
   el tema de fondo de la aplicacion sea mas sencillo de utilizar o cambiar, lo cual no se podia hacer tan facil desde Tkinter, se quitaron todos los LOGS y se documento
  y se documento la funcionalidad del script, se le coloco un favicon sencillo.
  Se agrego una nueva funcionalidad, ahora se pueden guardar diferentes perfiles segun el tipo de monitor, ejemplo: (monitor 1- panel izquierdo) y se rellena automaticamente
  cuando se mide la pantalla se da un nombre y se guarda, y asi se crea un nuevo perfil, luego se puede ir cambiando de perfiles y dar al boton cargar, para usar
  la region guardada

  # 08-05-2026
  Se empezo a implementar el API de Hubspot y a hacer llamadas con FastAPI y su wrapper, de esta manera pudimos encontrar que propiedades de Hubspot eran las que necesitabamos y probar la funcionalidad del API, consiguiendo sacar y hacer las consultas correctamente, despues se probo con las FSD, pero nos dio algunos errores con las entidades "Contacto" y "Ticket", ADEMAS, se

  Pendientes: hacer que se guarde en config.json y que se pueda utilizar cualquier monitor conectado a la computadora principal

  CORRECCIONES APLICADAS:
  * 1 — `_make_status_bar: .grid(side=) → .pack(side=)`
  * 2 — `make_log_section` era código muerto (log_text se creaba dos veces); eliminado
  * 3 — `_log(): CTkTextbox` no soporta tags de color → usa `._textbox` interno de Tk
  * 4 — `_font_exists():` ahora usa `tkinter.font.families()` correctamente
  * 5 — `_status_dot/.grid(side=)` → `.pack(side=)` (mismo que  1, instancia distinta)
  * 6 — `status_frame` en `_build_ui: row=99` → `row=5`
  * 7 — `_proceso():` todos los `self._log()` pasan por `self.after()` `(thread-safety)`
  * 8 — `subir():` se le pasa un wrapper thread-safe en lugar del `_log` directo

  El codigo se hizo muy grande asi que lo separe en varios archivos, para que asi el desarrollo sea algo mas sencillo:

  * ssauto/
  * ├── main.py                   ← Punto de entrada (ejecutar este archivo)
  * ├── configuracion.py          ← Constantes, lista de sitios y config.json
  * ├── credenciales.py           ← Cookies de sesión y llavero del SO (keyring)
  * ├── medidor.py                ← Código del selector visual de región
  * ├── automatizacion.py         ← Driver de Chrome, captura y subida (Selenium + mss)
  * ├── ventana_credenciales.py   ← Ventana modal de usuario/contraseña
  * ├── ventana_principal.py      ← Ventana principal (CustomTkinter)
  * ├── config.json               ← Generado automáticamente al guardar ajustes
  * ├── cookies/                  ← Generado automáticamente al hacer login
  * └── screenshots/              ← Generado automáticamente al capturar

  Se empezo a realizar el script con web scraping + api, para automatizar varias cosas
  pendientes. realizar el web scraping para comparar los datos traidos de ahi con los de la api, determinar si son iguales o no, si son iguales se dejan iguales,
   si son diferentes se ponen los dos encima del otro, como una sugerencia, si en uno de los dos el dato esta vacio, se coloca el dato que este,
   ejemplo: sitio 1: nombre: no encontrado, pero en el sitio 2: nombre: Julian, se coloca el valor del sitio 2, para asi lograr una comparacion completa

# Mejoras necesarias (a corto plazo)

      1. Compatibilidad con macOS y Linux
  `_abrir_chrome_debug()` solo busca Chrome en rutas de Windows. Agregar detección del SO con `platform.system()` y las rutas correspondientes en cada sistema.

      2. Gestión de errores más granular
  Actualmente los errores de subida se logean pero no se reintentan. Implementar reintentos automáticos (p. ej. 3 intentos con espera exponencial) para fallos de red.

      3. Validación de la región capturada
  Si `width` o `height` es 0, `mss` lanzará un error silencioso. Agregar validación antes de llamar a `capturar()` y mostrar un mensaje claro al usuario.

      4. Pruebas automáticas
  No hay ningún test. Agregar al menos pruebas unitarias para `parsear_region`, `_keybind_legible` y `cargar_config` con `pytest`.

  ---

# Mejoras futuras (a mediano plazo)

      5. Soporte para múltiples perfiles de región
  Permitir guardar y cargar diferentes regiones con nombre (p. ej. "Monitor 1 - Panel izquierdo") en lugar de solo una.

      6. Programación por horario
  Agregar un campo de intervalo (en minutos) para que la captura y subida se ejecuten automáticamente de forma periódica usando `threading.Timer` o `schedule`.

      7. Historial de capturas
  Mostrar en la UI las últimas N capturas realizadas con miniatura, fecha y estado de subida. Guardar el historial en un archivo JSON local.

      8. Notificaciones del sistema
  Usar `plyer` o `winotify` (Windows) para mostrar una notificación nativa cuando el proceso complete o falle, incluso si la ventana está minimizada.

      9. Modo de línea de comandos (CLI)
  Exponer `capturar()` y `subir()` como comandos de consola para poder integrar SSAuto en scripts o tareas programadas del SO sin abrir la UI.

      10. Empaquetado como ejecutable
  Configurar `PyInstaller` o `Nuitka` para distribuir la app como un `.exe` sin requerir Python instalado.

  ---

     Cosas a considerar

  - **Seguridad de cookies**: Los archivos `.pkl` en la carpeta `cookies/` no están cifrados. Cualquiera con acceso al sistema puede leerlos. Para mayor seguridad, cifrarlos con `cryptography.fernet` usando una clave derivada del llavero del SO.
  - **Selector de confirmación**: `wait.until(EC.url_contains("secure"))` está hardcodeado para el sitio de demo de Herokuapp. Para sitios reales, cambiar esto a un selector configurable por sitio en `SITIOS`.
  - **WebDriverManager y offline**: Si la máquina no tiene internet, `ChromeDriverManager().install()` fallará. Considerar cachear el driver o permitir especificar la ruta manualmente.


  # 11/05/2026
  Se empezo a hacer pruebas con el web scraping y el API para la comparacion de datos de clientes.
  El bot se ejecuta en el puerto 9222 de Chrome esto para que la automatizacion sea efectiva.
  En ese perfil de Chrome se puede iniciar sesion normal con cualquier cuenta, PERO su uso es unica y exclusivamente para el uso de los bots, ya que permite que los perfiles de uso diario no se rompan, no se bloquee chrome, no se corrompan los perfiles y es mas seguro aislar, ademas ahi se guardan todos los datos de la sesion incluyendo, cookies, sesiones, las cuentas, extensiones, pestañas, preferencias, etc. Y es mejor para que el bot no sea detectado por el navegador

  ESTOY EN EL TICKET -> ACTIVIDADES -> NOTAS -> CREAR NOTA -> INTERFAZ NOTA, DONDE APARECE PARA ADJUNTAR ARCHIVOS Y SUBIR FOTOS O ESCRIBIR -> CREAR NOTA. ESE ES EL FLUJO DE INTERACCION EN HUBSPOT PARA SUBIR UNA NOTA

  # 12-05-2026
  Lo primero que arreglamos este dia fue el Chrome con depuracion en el puerto 9222, ya que no estaba abriendose correctamente, ademas de eso, cada que abriamos el Chrome con depuracion mediante el boton, no se nos abria el Chrome abierto si estaba abierto y cada vez se abria una nueva pestaña
  Casos de uso:
  * `usar_chrome_existente=True`  → se conecta al Chrome ya abierto en puerto 9222.
  * usar_chrome_existente=False → abre un Chrome nuevo (con o sin headless).
  #
  Mejoramos la automatizacion en Hubspot haciendo que el bot siga la ruta especifica.
  Se verifica la pestaña, el inicio de sesion, analizando el titulo de la pagina, la url, cada pestaña y se revisa si la URL tiene "Hubspot" o no
  Tambien ocultamos todos los indicadores de automatizacion en Chrome, ademas agregamos un boton para que el usuario decida si quiere que la nota se suba automaticamente por defecto esta activado, pero es preferible que el usuario verifique y suba la captura, la configuracion de este boton se sube a "config.json"
  Ahora el usuario puede elegir el monitor que desee y guardar su perfil en "config.json", la funcionalidad del medidor y de la captura funcionan desde cualquier monitor usado
  El Web Scraping de Sunrun tiene las bases, pero tiene errores, como: no abre el fsd rapido, se demora o no lo encuentra, pero cuando lo encuentra trae la informacion correcta desde los selectores correctos. El bot verifica cada pestaña, el inicio de sesion y busca la pestaña que tenga "sunrun" y ahi se empieza a ejecutar.


  # **13-05-2026** #
  
  Como casi toda la informacion del usuario esta en el subject (nombre del ticket) la idea era parsear la informacion encontrada ahi como el fsd, el nombre, el id (id-goformz) y la nota, para verificar y comparar la info con Sunrun mediante el comparador
   api.py — Extracción de datos desde HubSpot
  ============================================
  Flujo principal:

* 1. Buscar ticket por FSD  →  `_buscar_ticket_por_fsd()`
* 2. Parsear subject como fallback  →  `_parsear_asunto()`
* 3. Buscar contacto vinculado por id_goformz  → ` _buscar_contacto_por_id_goformz()`
* 4. Combinar todo (atributo directo gana sobre subject)  →  `extraer_datos_hubspot()`

  La función pública es:
      `extraer_datos_hubspot(fsd: str) -> dict`

  Devuelve un dict con claves estandarizadas listo para comparador.py.
  Si la info esta en los atributos (propiedades) correctos se ignora la informacion que haya en el subject, solo se usa la info de subject cuando el atributo en Hubspot se encuentra vacio, se extrae el fsd de el formato fsd-000000 y se transforma en 000000 (solo numeros) e igual desde Sunrun para que la comparacion se haga correctamente.
  Acepta cualquier formato de FSD (FSD-1236711, FSD1236711, 1236711, etc.) y se prueban variaciones de fsd. Como el unico atributo en comun de "Contacto" y "Ticket" es el id del cliente "id_goformz" se busca mediante este toda la informacion del cliente y se pone en la ventana de comparacion en la columna "Hubspot"

  # **Contacto:**
* HubSpot
* Nombre del cliente: firstname + lastname
* ID del Cliente: id_de_goformz__contacto_
* Direccion: direccion__fisica_
* Telefono principal: phone
* Telefono movil: telefono_alterno_del_cliente
* Email: email
* Estado (state): country
* County: municipio_de_residencia o state
* municipio_de_residencia - Municipio de residencia
* municipios_co__contacto_ - Municipios CO (Contacto)
* Ciudad / Municipio: municipio_de_residencia o state
* Zip Code: zip
   # **Ticket:**

* HubSpot
* Nombre del cliente: subject
* ID del Cliente: esta en el subject o id_goformz__servicios_tecnicos_
* Direccion: physical_address
* Telefono principal: phone
* Telefono movil: no hay
* Email: e_mail
* Estado (state): no hay
* County: pueblo_para_servicio_tecnico
* Ciudad / Municipio: pueblo_para_servicio_tecnico
* Zip Code: no hay
* Nota: nota_ticket__sac_

# 14-05-2026

  Mejora del Web Scraping en Hubspot, el bot busca el fsd automaticamente (lo escribe) mediante la barra de busqueda global, si lo encuentra le da click, si no,
  El bot realiza una espera breve para verificar si salieron resultados si no da enter y va a la pagina de resultados y le da click desde ahi, despues ya trae toda la info a la ventana de comparacion
  Soporta dos escenarios:
            A) Página de resultados de búsqueda global (/global-search/):
               Salesforce muestra los resultados en una tabla con links cuyo
               texto visible es "FSD-XXXXXXX". Se intentan múltiples XPaths
               para cubrir variaciones del DOM de Salesforce LWC.
            B) Cualquier otra página con link por href (fsd{numero}):
               Fallback clásico — href contiene fsd+número.

  ── Escenario A: página de resultados de búsqueda global ─────
  URL: /partners/s/global-search/FSD-XXXXXXX
  El DOM de resultados de Salesforce puede presentar el link con:
    1. Texto visible exacto "FSD-XXXXXXX"
    2. href que contiene fsd{numero} (el más fiable)
    3. Atributo title o aria-label con el nombre del registro
    4. Cualquier (a) dentro de la fila que contenga el número

  ── Escenario B: otra página de Sunrun (lista, home, etc.) ─── va a la barra de busqueda global y hace el flujo normal


  Este mismo dia empece a trabajar en el Formulario de Cotizacion de PlanetSolar


  # **=============== EXTRA ===================================================**

# **main2.py**

Hola Claude, vengo a mejorar mi proyecto, el web scraping funciona perfecto, pero me gustaria mejorar algunas cositas, mira: Sunrun tiene varias paginas donde el bot interactua verdad, por ejemplo la pagina principal, luego la barra global de busqueda, luego el icono morado o si no busca cierto, y ya ahi puede que se meta de una al fsd buscado o que aparezca en la lista de resultados, y luego se meta al fsd buscado, y ahi si haga el web scraping, pero siempre que le doy al boton "comparar" y digamos que ya estoy en una de esas partes, el bot empieza el proceso desde el principio, me gustaria que no se reiniciara el proceso y que detecte donde esta para que proceda, pero no que reinicie todo siempre, el ciclo que explique es un ejemplo, lo que busco es que me entiendas

Gracias a ti! 😄 Fue una sesión muy productiva — arreglamos bastante cosa:

* ✅ Selectores XPath del DOM de Sunrun
* ✅ Búsqueda global con dropdown MRU
* ✅ State, City, Zip Code y County
* ✅ Claves desajustadas en el comparador
* ✅ Ciudad duplicada renombrada
* ✅ Ventana de comparación desbloqueada
* ✅ Bug de "Mostrar escritorio"
* ✅ Ventana al frente al abrir

Hola Claude, ahora mismo estoy trabajando en un proyecto para mi empresa para automatizar varias cosas, una de ellas es la comparacion de datos entre dos paginas, ayer arregle el web scraping a una de ellas que es Sunrun y quedo funcionando perfecto. Ahora necesito mejorar la extraccion de la info de la otra pagina que es Hubspot, de esta cuento con el api, pero ahora mismo no estoy extrayendo los datos que necesito, ademas tengo un gran problema y es que en el nombre del TICKET (subject) hay varios datos que pueden o no pueden estar en otros atributos por ejemplo asi: FSD1240131 - Rivero Nieves - ID 245565, todo eso es el subject, pero tambien son atributos que ya estan o pueden estar en ticket en "fsd__(fsd puede estar o no)", "firstname + lastname", "id_goformz__servicios_tecnicos_" y "NOTA(la nota puede estar o no)" entonces mi idea es extraer esa info de SUBJECT y compararla con la info que este en sus respectivos atributos, si no esta se pone la que este y ya, de resto solo seria traer los datos, ademas, los tickets y los contactos solo tienen un atributo en comun, que no se llama igual pero que SI ES IGUAL, o sea el dato que tienen guardado es el mismo, pero se llaman diferente: id_goformz_servicios_tecnicos para TICKET y id_goformz_contacto para CONTACTO, realizar esa comparacion, es decir que sean iguales, y desde ahi arrancar a hacer la busqueda de la informacion en TICKET y en CONTACTO, para los atributos necesarios, el nombre de los otros atributos estan en Claude, luego la comparacion con los datos de SUNRUN, se hace con el FSD, hay otras cosas mas por agregar pero lo podemos hacer despues

  # **Contacto:**
* HubSpot
* Nombre del cliente: firstname + lastname
* ID del Cliente: id_de_goformz__contacto_
* Direccion: direccion__fisica_
* Telefono principal: phone
* Telefono movil: telefono_alterno_del_cliente
* Email: email
* Estado (state): country
* County: municipio_de_residencia o state
* municipio_de_residencia - Municipio de residencia
* municipios_co__contacto_ - Municipios CO (Contacto)
* Ciudad / Municipio: municipio_de_residencia o state
* Zip Code: zip
   # **Ticket:**

* HubSpot
* Nombre del cliente: subject
* ID del Cliente: esta en el subject o id_goformz__servicios_tecnicos_
* Direccion: physical_address
* Telefono principal: phone
* Telefono movil: no hay
* Email: e_mail
* Estado (state): no hay
* County: pueblo_para_servicio_tecnico
* Ciudad / Municipio: pueblo_para_servicio_tecnico
* Zip Code: no hay
* Nota: nota_ticket__sac_


para despues, decirle que maneje los 72 municipios que no importe si esta en mayusculas, minusculas, si tiene tildes, etc, que lo reconozca igual, tambien asi con los otros atributos, datos, propiedades o como se llamen xd

si el fsd__ en HUBSPOT esta vacio no esta buscando asi lo tenga en subject en HUBSPOT


Necesito crear un formulario que sea bonito, llamativo y no sea tan engorrioso o complicado de responder, en este momento tengo un formulario que esta creado en Hubspot, pero que es simplemente un cuadrado con varios inputs y lo que se pide, y arriba tiene el logo de planetsolar, pregunta por: nombre apellidos, numero de seguro social, pueblo, correo, numero de telefono, direccion, Coordenadas / PIN Location*, un lugar donde se sube un archivo que es Factura de Electricidad (LUMA)*, y detalles de equipos y precios, con una sugerencia: Precio x watts | Precio x batería(s) | Marca de Bateria | Minimo Offset | Adds | Deuda de LUMA | Enseres a considerar | Otros, despues abajo un boton que dice siguiente en amarillo para pasar a las siguiente pagina donde dice nombre del consultor y telefono del consultor, luego otra pagina donde hay informacion para aceptar el tratamiento de datos personales y ya ahi se envia, verdad, lo que yo quiero es que el formulario no sea tan sencillo, ya que parece un html, con un poco de css y ya xd. Mi idea es hacer uno mejor en typeform o en alguna plataforma que me recomiendes, ademas tambien necesito guardar esa informacion, igual creo que se puede guardar todo en Hubspot. O lo puedo crear yo mismo?

Si lo hago yo mismo, como seria la desplegada en internet? Si me hago entender, tendria que comprar un dominio y un servidor? Si se manejar la API, pero tengo esa duda.




# 20/05/2026
Se modifico un poco el UI, para que algunas opciones como "auto-submit" encajaran mejor y no se vieran descuadradas o en una proporcion incorrecta o fea.
Se creo el archivo .exe con la herramienta de Python  **Pyinstaller**, se verifico que partes del codigo eran mas usadas con **Coverage** herramienta utilizada para saber que partes del programa se ejecutaron realmente durante las pruebas e identificar codigo muerto.
Se creo `doku.md` para poner mi documentación y datos para tener contexto. (solo yo lo entiendo xd)


# **Comando para crear el .exe**

pyinstaller --onefile --windowed --collect-all customtkinter --add-data "config.json;." --add-data ".env;." main.py

* Se eliminaron los requierements.txt innecesarios, las carpetas que ya no utilizaba y se corrigieron errores en configuracion.py

# version.py
MAJOR.MINOR.PATCH

Ejemplo:
0.1.0
* MAJOR → cambios grandes que rompen cosas
* MINOR → nuevas funciones
* PATCH → arreglos pequeños
* 0.1.0  -> primera versión usable
* 0.2.0  -> agregaste login
* 0.2.1  -> arreglaste un bug
* 1.0.0  -> versión estable
* 2.0.0  -> cambiaste arquitectura/API




HOY ME SENTE CON EL EQUIPO DE SERVICIOS TECNICOS, MILESTONE, SALESFORCE PARA REVISAR EL TRABAJO SCRIPT PROGRAMA QUE HICE EN ESTAS 2 SEMANAS, PARA EMPEZAR EN LA REUNION MI JEFE CARLOS DIO CONTEXTO DEL TEMA DE LA REUNION EN LA REUNION ESTABAN: MARGARITA FERRO, NICZY ARIAS, LINA SIERRA Y CRISTIAN REYES, PARA EMPEZAR EXPLICO LA METODOLOGIA SCRUM, LUEGO PROCEDI A EXPLICAR EL FUNCIONAMIENTO DEL PROGRAMA Y VIERON COMO FUNCIONABA, EXPLIQUE EL SSAUTO Y EL COMPARADOR DE FSD Y DURANTE LA REUNION HUBIERON MUCHAS SUGERENCIAS, IDEAS Y PETICIONES, ENTRE ELLAS, MEJORAR EL COMPARADOR, MEJORAR LA INTERFAZ, MEJORAR LA BUSQUEDA POR MAS CAMPOS, AGREGAR MAS FLUJOS ETC PARA QUE EL PROGRAMA FUNCIONE MEJOR, COMO EVITANDO LA BUSQUEDA ENTRE PESTAÑAS Y ELIJA EN DONDE ESTE, MI IDEA ES AGREGAR VARIOS BOTONES Y MEJORAR LA INTERFAZ, BOTONES PARA CAPTURAS PREDETERMINADAS EN DISTINTOS SITIOS WEB O APLICACIONES Y BOTONES PARA COPIAR MENSAJES Y USAR PLANTILLAS, BOTON PARA ELEGIR SI SUBIR A SUNRUN Y A HUBSPOT O A AMBOS, PONER UN COLOR DEPENDIENDO DEL ESTADO DEL FSD EN SUNRUN, (MIRAR CUADERNO), PONER UNA INTERFAZ DISTINTA PARA LA VENTANA PRINCIPAL QUE SEA COMO UN BOTON QUE DIGA "CAPTURA" Y "COMPARADOR, DESDE AHI TAMBIEN QUE HAYA UN BOTON EN LA PARTE DE ARRIBA PARA LA CONFIGURACION




tengo 3 tipos de mensaje aqui estan:

FUERA DE SERVICIO***

Se llamó al número registrado, pero está fuera de servicio. Se envió un correo electrónico como método de contacto alternativo.

LS: 05/19/2026 A call was placed to the registered phone number, but it is out of service. An email was sent as an alternative method of contact.


****************************
BUZÓN DE VOZ***

Se llamó al cliente al número registrado, pero la llamada fue enviada al buzón de voz. Se envió un mensaje de texto y un correo electrónico.

LS: 05/21/2026 The customer was called at the registered number, but the call went to voicemail. A text message and an email were sent.


*********************************
NO CONTESTA***

Se llamó al cliente al número registrado, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico.

LS: 05/21/2026 The customer was called at the registered number, but did not answer. A text message and an email were sent as alternative methods of contact.

si puedes ver cada uno tiene una version en ingles y en español, quiero que la interfaz me permita elegir si copiar el que esta en ingles o el que esta en español, si puedes ver hay una fecha al principio de cada mensaje, quiero que esta fecha se ponga automaticamente con datetime o el que consideres necesario, tambien cada uno de estos mensajes puede tener maximo 2 numeros, entonces si el usuario ingresa 1 numero que aparezca "al" si son 2 o mas " a los ", que maneje plural/singular, y que aparezcan los numeros telefonicos en el mensaje, crea un prompt donde se indique lo que se tiene que hacer, di que no se rompa ninguna funcionalidad, debe revisar los archivos @ventana_plantillas.py y @template_filler, si es posible que estos 2 archivos sean combinados, o que el uno llame al otro, la idea es que las interfaces sean faciles de usar, que se pueda ver el mensaje en la ventana, y que tambien se pueda usar el @template_filler a un lado, luego que se pueda copiar como te dije. gracias bro


Para la mejor inteligencia en código: ollama run qwen2.5-coder:7b
Para máxima velocidad (ligero): ollama run qwen2.5-coder:3b
Para razonamiento lógico profundo: ollama run deepseek-r1:8b




necesito que cuando se suba el archivo de la captura, detecte y suba a la correcta, A LA QUE EL USUARIO ESTA EN ESE MOMENTO, EN LA QUE EL USUARIO ENTRO Y ESTA SOBRE ELLA, QUE NO BUSQUE OTRAS PESTAÑAS DE HUBSPOT ASI TENGA MUCHAS ABIERTAS, YA QUE ESTO ES UN ERROR MASIVO Y MUY IMPORTANTE, YA QUE LA INFORMACION SE PODRIA SUBIR A DONDE NO ES Y NO QUIERO ESO, TAMBIEN HAZ QUE LA INTERFAZ PUEDA ADAPTARSE A TODAS LAS PANTALLAS, YA QUE EN LAS PANTALLAS MUY GRANDES TIPO TV Y ASI, LA VENTANA SE VE FEA Y NO SE VE ENCUADRADA, EL CONTENIDO SE VE PEQUEÑO Y CON MUCHOS ESPACIOS VACIOS, CREAME UN PROMPT CON TODO LO ANTERIOR PLIS, QUE NO DAÑE NINGUNA FUNCIONALIDAD.


25/05/2026
Se implementó una nueva funcionalidad integral para la generación automática de mensajes de contacto mediante la nueva interfaz `@ventana_generador_mensajes`, integrada en la barra superior de configuración. Esta mejora incluye 4 tipos de mensajes predefinidos (Fuera de Servicio, Buzón de Voz, No Contesta y Confirmación de visita técnica), con soporte para manejo inteligente de números telefónicos, validaciones, detección singular/plural, fechas automáticas con `datetime`, cálculo de días hábiles con `pandas`, previsualización en tiempo real y copia automática al portapapeles. Además, se realizó una refactorización general de la arquitectura UI y servicios, abarcando más de 20 archivos enfocados en modularidad, mantenibilidad, compatibilidad y una experiencia de usuario más moderna utilizando `customtkinter`, sin introducir cambios breaking en la aplicación. Adapte los nuevos botones de aplicaciones añadidos a la ventana principal y se configuro el boton para medir la pantalla de cada boton. Ejemplo: B2Chat: Se mide la pantalla y despues se le da al boton para realizar la subida

Se implemento una nueva funcionalidad para la generacion de mensajes de contaccto, con nueva interfaz UI y mejores componentes. Fueron en total 21 archivos cambiados y creados enfocados en modularidad, mantenibilidad y nueva funcionalidad de usuario. La nueva ventana @ventana_generador_mensajes, es una ventana puesta en la barra superior de configuracion que permite abrir una interfaz desde donde se pueden copiar mensajes automaticamente, desde 2 idiomas, estos mensajes tienen un input para ingresar 2 numeros de contacto, tambien traen la fecha actual con datetime y se usa pandas para manejar los dias habiles, detecta plural-singular, se previsualiza el mensaje con la informacion, y se valida que los numeros de telefono ingresados si sean validos 
- 4 tipos de mensaje predefinidos:
  - Fuera de Servicio con datetime y variables de telefono
  - Buzón de Voz  con datetime y variables de telefono
  - No Contesta con datetime y variables de telefono
  - Confirma visita tecnica con pandas, dias habiles (business days) y datetime

## 📋 **RESUMEN DE PULL REQUEST - Cambios de Hoy**

### 🎯 **Descripción General**
Se ha implementado una **nueva funcionalidad integral de generación de mensajes de contacto** junto con mejoras significativas en la arquitectura de UI y refactorización de componentes. El trabajo incluye **20 archivos modificados/creados** enfocados en modularidad, mantenibilidad y nueva funcionalidad de usuario.

---

### 📊 **Estadísticas**
- **Total de archivos afectados**: 20
- **Archivos nuevos**: 1 módulo UI principal + documentación
- **Archivos modificados**: 19
- **Archivos eliminados**: 0

---

### ✨ **Cambios Principales por Categoría**

#### **1️⃣ NUEVO: Generador de Mensajes de Contacto**

**Archivo nuevo:**
- ✅ `ui/ventana_generador_mensajes.py` - **Módulo completo para generar mensajes estandarizados**

**Características implementadas:**
- 4 tipos de mensaje predefinidos:
  - Fuera de Servicio
  - Buzón de Voz  
  - No Contesta
  - Confirma visita tecnica
- 🌍 Soporte bilingüe (Español/Inglés)
- 📱 Manejo inteligente de 1-2 números telefónicos
- 🔄 Detección automática singular/plural
- 📅 Fecha automática (formato MM/DD/YYYY)
- 📋 Previsualización en tiempo real
- 🎨 Interfaz moderna con customtkinter

---

#### **2️⃣ Configuración & Almacenamiento**

**Modificados:**
- `config/plantillas.json` - Ampliado con nueva entrada "Respuesta"
- `config/apps_captura.py` - Estructura mejorada con documentación inline
- `config/configuracion.py` - (revisado para compatibilidad)
- `config/credenciales.py` - (sin cambios funcionales)

---

#### **3️⃣ Interfaz de Usuario (UI)**

**Archivos actualizados:**

| Archivo | Cambios |
|---------|---------|
| `ui/ventana_principal.py` | Refactorizada, más limpia y modular; integración con nuevo generador |
| `ui/ventana_plantillas.py` | UI para plantillas genéricas editables (sin cambios funcionales) |
| `ui/ventana_comparacion.py` | Ventana de comparación Sunrun vs HubSpot (mejorada) |
| `ui/ventana_credenciales.py` | Gestión de credenciales modal (refactorizada) |
| `ui/posicion_ventanas.py` | Utilitario de posicionamiento (sin cambios) |
| `ui/custom_ctkframe.py` | Frame personalizado reutilizable (sin cambios) |

---

#### **4️⃣ Servicios & Lógica**

**Archivos:**
- `services/sesion_service.py` - Gestión de sesiones de usuario
- `template_filler.py` - Generador de plantillas con placeholders (mejorado)

---

#### **5️⃣ Punto de Entrada**

**Actualizado:**
- `main.py` - ✅ Ahora importa y registra `VentanaGeneradorMensajes`
  ```python
  from ui.ventana_generador_mensajes import VentanaGeneradorMensajes
  ```

---

#### **6️⃣ Documentación**

**Nuevo:**
- 📄 `GENERADOR_MENSAJES.md` - **Documentación técnica completa** (197 líneas)
  - Descripción de características
  - Ejemplos de uso
  - Arquitectura de solución
  - Detalles técnicos de singular/plural
  - Validaciones implementadas
  - Notas sobre compatibilidad

---

#### **7️⃣ Utilidades & Core**

**Sin cambios pero compatibles:**
- `core/plugin_registry.py`
- `core/base_plugin.py`
- `core/browser.py`
- `core/captura.py`
- `core/comparador.py`
- `plugins/hubspot.py`
- `plugins/sunrun.py`
- `plugins/template_new_site.py`
- `data/api.py`
- `medidor.py`
- `version.py`
- `scraping_sunrun.py`

---

### 🔑 **Cambios Clave**

#### ✅ **Lo que se agregó:**
1. **Generador de Mensajes** - Nuevo módulo UI completamente funcional
2. **Plantilla "Respuesta"** - Nueva entrada en config/plantillas.json
3. **Integración en main.py** - Botón "Mensajes" en interfaz principal
4. **Documentación detallada** - Guía técnica de 197 líneas

#### 🔄 **Lo que se refactorizó:**
1. `ventana_principal.py` - Código más limpio y modular
2. `ventana_comparacion.py` - Mejoras en presentación
3. `template_filler.py` - Enhancements en generación de placeholders
4. `apps_captura.py` - Mejor documentación inline

#### ✨ **Lo que se mejoró:**
- Separación clara de responsabilidades
- Modularidad aumentada
- Compatibilidad 100% mantenida
- UI/UX más intuitiva

---

### 🎨 **Nuevas Características para el Usuario**

✅ **Botón "Mensajes"** en la barra superior  
✅ **4 plantillas de contacto** listas para usar  
✅ **Soporte bilingüe automático**  
✅ **Manejo inteligente de números telefónicos**  
✅ **Previsualización en tiempo real**  
✅ **Copia al portapapeles con un clic**  

---

### 🧪 **Compatibilidad & Testing**

✅ Sin cambios breaking en funcionalidad existente  
✅ Todos los módulos previos se mantienen funcionales  
✅ Estructura de plugins sigue siendo extensible  
✅ UI es 100% backward compatible  

---

### 📝 **Notas Importantes**

- El generador está diseñado específicamente para 3 tipos de mensajes de contacto
- Los mensajes se copian al portapapeles listos para usar
- La fecha se genera automáticamente en momento de creación
- Interfaz moderna con customtkinter, responsive a resoluciones

---

**Tipo de cambio:** ✨ Feature  
**Alcance:** UI + Generador de Mensajes  
**Breaking changes:** ❌ Ninguno  
**Documentación:** ✅ Completa  


TAREAS PENDIENTES

- MEJORAR EL WEB SCRAPING DE SUNRUN, CON LOS SELECTORES NECESARIOS, TERMINAR LA CONEXION CORRECTA CON HUBSPOT, PARA LA SUBIDA DE CAPTURAS DE PANTALLA, MEJORAR EL USO DE LOS MENSAJES AUTOMATICOS CON LA SUBIDA A HUBSPOT, MEJORAR LOS FILTROS DE BUSQUEDA EN LA COMPARACION Y AGREGAR MAS PROPIEDADES (ATRIBUTOS), INTENTAR BUSCAR POR CUALQUIER OTRO ATRIBUTO Y LUEGO CON FSD, LA SUBIDA DE CADA BOTON DE APLICACION QUE SE PUEDA DETECTAR LA APLICACION Y SE TOME LA CAPTURA Y SE SUBA CORRECTAMENTE


---

## Correcciones aplicadas — 26/05/2026 (revisión de bugs)

### BUG #1 — `deiconify_window()` con paréntesis en callbacks de `after()`
**Archivo:** `ui/ventana_principal.py` — método `_medir_region_app`, función interna `_esperar`  
**Problema:** En los dos paths de error del hilo (`except` del `literal_eval` y el bloque final de cancelación), se usaba `self.after(0, self.deiconify_window())`. Los paréntesis ejecutaban `deiconify_window()` inmediatamente en el hilo secundario (thread-unsafe), y pasaban `None` como callback a `after()`, así que la ventana nunca se restauraba si la medición fallaba o se cancelaba.  
**Fix:** `self.after(0, self.deiconify_window)` sin paréntesis en ambas ocurrencias del path de error.

---

### BUG #2 — `winfo_toplevel().iconify()` en lugar del wrapper del frame
**Archivo:** `ui/ventana_principal.py` — método `_medir_region_app`, bloque antes de lanzar el hilo  
**Problema:** Se llamaba `self.winfo_toplevel().iconify()` directamente en el hilo principal, salteando el wrapper `iconify_window()` definido en `CustomCTkFrame`. Aunque en la práctica funcionaba (el hilo principal puede tocar Tk), era inconsistente con el resto de la clase y potencialmente frágil si en el futuro `iconify_window` añade lógica extra.  
**Fix:** Reemplazado por `self.iconify_window()` para consistencia con el patrón del resto de la clase.

---

### BUG #3 — `self.iconify` en un Frame dentro de `_proceso_app`
**Archivo:** `ui/ventana_principal.py` — método `_proceso_app`, línea `self.after(0, self.iconify)`  
**Problema:** `App` hereda de `CustomCTkFrame` (un `CTkFrame`), no de un `Toplevel`. Los frames no tienen método `iconify()`. La llamada lanzaba `AttributeError` que era silenciada por el `try/except` general, dejando la ventana visible durante la captura de la app (la captura incluía la propia interfaz).  
**Fix:** Cambiado a `self.after(0, self.iconify_window)` que usa el wrapper correcto que delega a `winfo_toplevel().iconify()`.

---

### BUG #4 — `self.state()` y `self.deiconify()` sobre un Frame en `VentanaComparacion`
**Archivo:** `ui/ventana_comparacion.py` — métodos `_traer_al_frente` y `_mostrar_resultado`  
**Problema:** `VentanaComparacion` hereda de `CustomCTkFrame` (un Frame), no de `CTkToplevel`. Llamar `self.state()` sobre un Frame lanza `AttributeError` que el `try/except Exception: pass` silenciaba, haciendo que toda la lógica de "restaurar si estaba minimizado y traer al frente" simplemente nunca se ejecutara. El mismo problema en `_mostrar_resultado`.  
**Fix:** En ambos métodos se reemplazó `self.state()` y `self.deiconify()` por `root = self.winfo_toplevel()` seguido de `root.state()` y `root.deiconify()`, que apuntan correctamente al Toplevel real que contiene al frame.

---

### BUG #5 — Import de `pandas` a nivel de módulo en `ventana_generador_mensajes.py`
**Archivo:** `ui/ventana_generador_mensajes.py`  
**Problema:** `import pandas as pd` estaba al tope del archivo. Si `pandas` no está instalado (o falla al importar), toda la ventana de generador de mensajes crashea con `ImportError` al arrancar `main.py`, aunque `pandas` solo se use en la función `_obtener_fecha_habil_siguiente()`.  
**Fix:** Import lazy dentro de la función: `import pandas as pd` se movió adentro de `_obtener_fecha_habil_siguiente()`, y se añadió un fallback puro con `datetime` y `date.weekday()` por si `pandas` no está disponible. Así la ventana funciona completa incluso sin pandas (solo el cálculo de día hábil usa el fallback).



Dispatch Cancelled -> No es trabajable aparece en color rojo
Dispatch Reported -> No es trabajable aparece en color rojo
Dispatch Approved -> No es trabajable aparece en color rojo
Dispatch Acepted -> Es trabajable aparece en color verde con letra diferente
Dispatch Rejected -> Es trabajable aparece en color verde con letra diferente

Que aparezca en la parte de arriba de los resultados de busqueda y justo debajo aparezca la "Appointment Date" junto al "Case Reason"
Toda esta informacion solo aparece en Sunrun asi que se vea de forma organizada en la ventana de comparacion

repomix --ignore "doku.md"
repomix --compress --style markdown
repomix --compress --ignore "doku.md"
````

## File: scraping_sunrun.py
````python
import re
import time

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






URL_BASE_SUNRUN = "https://sunrun.my.site.com"


URL_LISTA_SUNRUN = (
    "https://sunrun.my.site.com/partners/s/fs-dispatch/FS_Dispatch__c/Default"
)




SEL_BUSQUEDA_GLOBAL = "div.forceSearchInputDesktop input[role='combobox']"

































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

SELECTOR_DISPATCH_STATE = (
    "//span[contains(@class,'test-id__field-label') "
    "and normalize-space(text())='Dispatch State']"
    "/ancestor::div[contains(@class,'label-stacked') "
    "or (contains(@class,'slds-form-element') "
    "and not(contains(@class,'slds-form-element__')))]"
    "//lightning-formatted-text"
)

SELECTOR_APPOINTMENT_DATE = (
    "//span[contains(@class,'test-id__field-label') "
    "and normalize-space(text())='Appointment Date']"
    "/ancestor::div[contains(@class,'label-stacked') "
    "or (contains(@class,'slds-form-element') "
    "and not(contains(@class,'slds-form-element__')))]"
    "//lightning-formatted-text"
)

SELECTOR_CASE_REASON = (
    "//span[contains(@class,'test-id__field-label') "
    "and normalize-space(text())='Case Reason']"
    "/ancestor::div[contains(@class,'label-stacked') "
    "or (contains(@class,'slds-form-element') "
    "and not(contains(@class,'slds-form-element__')))]"
    "//lightning-formatted-text"
)

SELECTOR_RELATED = "//a[@role='tab' " "and contains(normalize-space(.),'Related')]"

SELECTOR_UPLOAD_FILES_INPUT = (
    "//input[@type='file' " "and contains(@class,'slds-file-selector__input')]"
)

SELECTOR_UPLOAD_FILES_BUTTON = (
    "//span[normalize-space(text())='Upload Files']" "/ancestor::label"
)

SELECTOR_DROP_FILES = (
    "//span[contains(normalize-space(.),'Drop Files')]"
    "/ancestor::*[contains(@class,'slds-file-selector')]"
)


TIMEOUT = 15
TIMEOUT_LISTA = 30
PAUSA_FILTRO = 2.0
PAUSA_DETALLE = 1.5



SEL_MRU_DROPDOWN = "a.MRU_SCOPED"
TIMEOUT_MRU = 10







def _solo_digitos(fsd: str) -> str:








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


def _clic_con_nueva_pestana(driver, elemento, log_func, timeout: float = 15.0) -> bool:
    """
    Hace clic en un elemento que puede abrir una pestaña nueva (target="_blank").

    Si el clic genera una pestaña nueva, cambia el driver a esa pestaña.
    Si no genera pestaña nueva (navegación en la misma), no hace nada extra.

    Devuelve True si después del clic el driver está en una pestaña con
    contenido (readyState complete), False si hubo error.



































    Extrae datos de un ticket FS Dispatch en Sunrun.

    Siempre usa el Chrome ya abierto por el usuario (puerto 9222).
    Nunca abre un Chrome nuevo ni cierra el existente.

    Uso:
        scraper = ScraperSunrun(log_callback=mi_funcion_log)
        datos   = scraper.obtener_datos_por_fsd("1172172")










        Se conecta al Chrome abierto en puerto 9222 via BrowserFactory.
        Devuelve True si la conexión fue exitosa.
















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





























































































































































        Usa la barra global directamente sin navegar a la lista primero.
        Solo se llama cuando ya estamos en Sunrun (sesión confirmada).

        Igual que _buscar_en_lista pero sin el paso 1a (navegar a lista).
        Devuelve True si llegó a la página de detalle o de resultados.
























































































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
        appointment_date = self._extraer_campo(
            SELECTOR_APPOINTMENT_DATE, "Appointment Date"
        )
        case_reason = self._extraer_campo(SELECTOR_CASE_REASON, "Case Reason")




        self._log("  → Esperando renderizado de sección de dirección...")
        time.sleep(2.5)

        estado = self._extraer_campo(SELECTOR_ESTADO, "State")
        county = self._extraer_campo(SELECTOR_COUNTY, "County")
        ciudad = self._extraer_campo(SELECTOR_CIUDAD, "City")
        zip_code = self._extraer_campo(SELECTOR_ZIP, "Zip Code")


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
            "appointment_date": appointment_date,
            "case_reason": case_reason,
            "error": None,
        }



    def obtener_datos_por_fsd(self, fsd: str) -> dict:

















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

                self._log("  ✓ Ya en la página del ticket, extrayendo datos...")
                return self._extraer_detalle(fsd_numero)

            elif estado_actual == "en_resultados":

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


                self._log("  ✓ Ya en Sunrun, usando barra global de búsqueda...")
                if not self._buscar_desde_sunrun(fsd_numero):

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
            "appointment_date": "",
            "case_reason": "",
            "error": mensaje,
        }
````

## File: ui/ventana_principal.py
````python
import ast
import shutil
import subprocess
import sys
import threading
import tkinter.font
import time
from datetime import datetime
from pathlib import Path
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import cargar_auto_submit, guardar_auto_submit
from core.captura import CapturaService, ErrorCaptura
from core.plugin_registry import PluginRegistry
from services.sesion_service import SesionService
from config.configuracion import (
    PERFIL_POR_DEFECTO,
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
    obtener_monitores,
    obtener_nombres_monitores,
)
from config.credenciales import cargar_credenciales
from config.apps_captura import APPS_CAPTURA
from medidor import MEDIDOR_CODE
from ui.ventana_credenciales import VentanaCredenciales
from ui.custom_ctkframe import CustomCTkFrame

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

ctk.deactivate_automatic_dpi_awareness()


class App(CustomCTkFrame):


    def __init__(self, parent):
        super().__init__(parent)
        self._credenciales_sesion = {}
        self._keybind_actual = None
        self._btns_apps = {}
        self._regiones_apps = {}
        self._config = cargar_config()
        self._ui_scale = self._calcular_ui_scale()
        config = cargar_config()
        ctk.set_appearance_mode(config.get("tema", "dark"))
        self._construir_ui()

        self.update_idletasks()


        faltan_creds = any(
            p.necesita_login and not cargar_credenciales(p.nombre)[0]
            for p in PluginRegistry.con_login()
        )
        if faltan_creds:
            self.after(100, self._abrir_login_inicial)

    def _abrir_comparacion(self):
        from ui.ventana_comparacion import VentanaComparacion

        VentanaComparacion(self, log_callback=self._log)



    def _construir_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._frame_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        pad = self._r(8, 16, 28)
        self._frame_scroll.grid(row=0, column=0, sticky="nsew", padx=pad, pady=pad)
        self._frame_scroll.grid_columnconfigure(0, weight=1)

        padre = self._frame_scroll

        sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0)
        self._crear_panel_perfiles(sec1)
        self._separador(sec1)
        self._crear_selector_monitor(sec1)
        self._separador(sec1)
        self._crear_coordenadas(sec1)
        ctk.CTkButton(
            sec1,
            text="  Medir región en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=self._fs(11)),
            height=self._r(32, 36, 44),
        ).pack(fill="x", pady=(4, 0))

        sec2 = self._seccion(padre, "  SITIOS DE DESTINO", fila=1)
        self._crear_sitios_status(sec2)

        sec3 = self._seccion(padre, "  OPCIONES", fila=2)
        self._crear_opciones(sec3)


        sec_apps = self._seccion(padre, "  APLICACIONES DE CAPTURA", fila=3)
        self._crear_panel_apps(sec_apps)

        self.btn = ctk.CTkButton(
            padre,
            text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=self._fs(13), weight="bold"),
            height=self._r(42, 48, 58),
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.grid(row=4, column=0, sticky="ew", padx=0, pady=(8, 8))

        sec4 = self._seccion(padre, "  REGISTRO", fila=5, pady=(0, 8))
        self.log_texto = ctk.CTkTextbox(
            sec4,
            font=ctk.CTkFont(
                family=(
                    "Cascadia Code"
                    if self._fuente_existe("Cascadia Code")
                    else "Consolas"
                ),
                size=self._fs(10),
            ),
            wrap="word",
            height=self._r(140, 180, 260),
        )
        self.log_texto.pack(fill="both", expand=True)
        tb = self.log_texto._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("flecha", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

        self._crear_barra_estado(padre)

    def _seccion(self, padre, titulo, fila, col=0, colspan=2, pady=(0, 10)):
        frame = ctk.CTkFrame(padre, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(
            row=fila, column=col, columnspan=colspan, sticky="nsew", pady=pady, padx=0
        )
        padre.grid_columnconfigure(0, weight=1)
        enc = ctk.CTkFrame(
            frame, fg_color=("gray88", "gray25"), height=self._r(28, 32, 40)
        )
        enc.pack(fill="x")
        enc.pack_propagate(False)
        ctk.CTkLabel(
            enc,
            text=titulo,
            font=ctk.CTkFont(size=self._fs(11), weight="bold"),
            text_color=("gray30", "gray60"),
        ).pack(side="left", padx=self._r(14, 18, 28))
        cuerpo = ctk.CTkFrame(frame, fg_color="transparent")
        cuerpo.pack(fill="x", padx=self._r(14, 20, 32), pady=self._r(12, 16, 24))
        return cuerpo

    def _calcular_ui_scale(self) -> float:
        top = self.winfo_toplevel()
        sw, sh = top.winfo_screenwidth(), top.winfo_screenheight()
        return min(1.45, max(1.0, min(sw / 1920, sh / 1080)))

    def _r(self, base: int, mid: int | None = None, maximo: int | None = None) -> int:
        valor = int(round((mid if mid is not None else base) * self._ui_scale))
        return min(maximo or valor, max(base, valor))

    def _fs(self, base: int) -> int:
        return max(base, int(round(base * min(self._ui_scale, 1.28))))

    def _crear_panel_perfiles(self, padre):
        self._perfiles = cargar_perfiles()

        fila_selector = ctk.CTkFrame(padre, fg_color="transparent")
        fila_selector.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            fila_selector,
            text="Perfil:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self._perfil_var = ctk.StringVar(value="— sin perfiles —")
        self._perfil_menu = ctk.CTkOptionMenu(
            fila_selector,
            variable=self._perfil_var,
            values=self._nombres_perfiles(),
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False,
            width=220,
        )
        self._perfil_menu.pack(side="left", padx=(0, 8), fill="x", expand=True)
        ctk.CTkButton(
            fila_selector,
            text="Cargar",
            command=self._cargar_perfil_seleccionado,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

        fila_acciones = ctk.CTkFrame(padre, fg_color="transparent")
        fila_acciones.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            fila_acciones,
            text="Nombre:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self._perfil_nombre_var = ctk.StringVar()
        ctk.CTkEntry(
            fila_acciones,
            textvariable=self._perfil_nombre_var,
            placeholder_text="Ej: Monitor 1 — Panel izquierdo",
            font=ctk.CTkFont(size=11),
        ).pack(side="left", padx=(0, 8), fill="x", expand=True)
        ctk.CTkButton(
            fila_acciones,
            text="Guardar",
            command=self._guardar_perfil_actual,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            fila_acciones,
            text="Eliminar",
            command=self._eliminar_perfil_seleccionado,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="left")

        fila_pegar = ctk.CTkFrame(padre, fg_color="transparent")
        fila_pegar.pack(fill="x")
        ctk.CTkLabel(
            fila_pegar,
            text="Pegar región:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.region_paste_var = ctk.StringVar(value=str(PERFIL_POR_DEFECTO))
        entrada = ctk.CTkEntry(
            fila_pegar, textvariable=self.region_paste_var, font=ctk.CTkFont(size=11)
        )
        entrada.pack(side="left", padx=(0, 8), fill="x", expand=True)
        entrada.bind("<FocusOut>", self._parsear_region)
        entrada.bind("<Return>", self._parsear_region)
        self.region_paste = entrada
        ctk.CTkButton(
            fila_pegar,
            text="Aplicar",
            command=self._parsear_region,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

    def _crear_selector_monitor(self, padre):
        fila_monitor = ctk.CTkFrame(padre, fg_color="transparent")
        fila_monitor.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            fila_monitor,
            text="Monitor:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        nombres_monitores = obtener_nombres_monitores() or ["Monitor 1 (principal)"]
        monitor_guardado = int(self._config.get("ultimo_monitor", 1))
        valor_inicial = (
            nombres_monitores[monitor_guardado]
            if monitor_guardado < len(nombres_monitores)
            else nombres_monitores[0]
        )
        self._monitor_var = ctk.StringVar(value=valor_inicial)
        self._monitor_menu = ctk.CTkOptionMenu(
            fila_monitor,
            variable=self._monitor_var,
            values=nombres_monitores,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False,
            width=220,
        )
        self._monitor_menu.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self._monitor_info_label = ctk.CTkLabel(
            fila_monitor,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self._monitor_info_label.pack(side="left")
        self._monitor_var.trace_add("write", self._actualizar_info_monitor)
        self._actualizar_info_monitor()

    def _actualizar_info_monitor(self, *_):
        indice = self._monitor_var_indice()
        monitores = obtener_monitores()
        if 0 <= indice < len(monitores):
            m = monitores[indice]
            self._monitor_info_label.configure(text=f"{m['width']}×{m['height']} px")

    def _monitor_var_indice(self) -> int:
        nombres = obtener_nombres_monitores()
        try:
            return nombres.index(self._monitor_var.get())
        except ValueError:
            return 1

    def _nombres_perfiles(self) -> list[str]:
        nombres = list(self._perfiles.keys())
        return nombres if nombres else ["— sin perfiles —"]

    def _actualizar_menu_perfiles(self):
        nombres = self._nombres_perfiles()
        self._perfil_menu.configure(values=nombres)
        self._perfil_var.set(nombres[0])

    def _cargar_perfil_seleccionado(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._log("✗ No hay ningún perfil seleccionado.")
            return
        region = self._perfiles[nombre]
        self._aplicar_region(region)
        monitor_idx = region.get("monitor_index")
        if monitor_idx is not None:
            nombres = obtener_nombres_monitores()
            if 0 <= int(monitor_idx) < len(nombres):
                self._monitor_var.set(nombres[int(monitor_idx)])
        self._perfil_nombre_var.set(nombre)
        self._log(f"✓ Perfil cargado: «{nombre}» → {region}")

    def _guardar_perfil_actual(self):
        nombre = self._perfil_nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Nombre vacío", "Escribe un nombre para el perfil.")
            return
        region = {k: int(v.get() or 0) for k, v in self.region_vars.items()}
        region["monitor_index"] = self._monitor_var_indice()
        perfiles = cargar_perfiles()
        perfiles[nombre] = region
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._actualizar_menu_perfiles()
        self._perfil_var.set(nombre)
        self._log(f"✓ Perfil guardado: «{nombre}» → {region}")

    def _eliminar_perfil_seleccionado(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._log("✗ No hay ningún perfil seleccionado para eliminar.")
            return
        if not messagebox.askyesno(
            "Eliminar perfil", f"¿Eliminar el perfil «{nombre}»?"
        ):
            return
        perfiles = cargar_perfiles()
        perfiles.pop(nombre, None)
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._actualizar_menu_perfiles()
        self._log(f"✓ Perfil eliminado: «{nombre}»")

    def _crear_coordenadas(self, padre):
        frame_coords = ctk.CTkFrame(padre, fg_color="transparent")
        frame_coords.pack(fill="x", pady=(0, 10))
        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        for i, (etiqueta, valor) in enumerate(campos):
            caja = ctk.CTkFrame(
                frame_coords, fg_color=("gray90", "gray25"), border_width=1
            )
            caja.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))
            ctk.CTkLabel(
                caja,
                text=etiqueta.upper(),
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))
            var = ctk.StringVar(value=str(valor))
            ctk.CTkEntry(
                caja,
                textvariable=var,
                width=70,
                font=ctk.CTkFont(size=13, weight="bold"),
                justify="center",
                border_width=0,
            ).pack(pady=(0, 6))
            var.trace_add("write", self._sincronizar_paste)
            self.region_vars[etiqueta] = var

    def _crear_sitios_status(self, padre):
        self._frame_sitios = ctk.CTkFrame(padre, fg_color="transparent")
        self._frame_sitios.pack(fill="x", pady=(0, 8))
        self._actualizar_sitios_status()

        fila_botones = ctk.CTkFrame(padre, fg_color="transparent")
        fila_botones.pack(fill="x")
        ctk.CTkButton(
            fila_botones,
            text="Credenciales",
            command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            fila_botones,
            text="Renovar sesión",
            command=self._renovar_sesion,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left")

    def _crear_opciones(self, padre):
        self.destino_var = ctk.StringVar(value="AMBOS")
        fila_destino = ctk.CTkFrame(padre, fg_color="transparent")
        fila_destino.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            fila_destino,
            text="Subir a:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            width=60,
            anchor="w",
        ).pack(side="left", padx=(0, 8))

        self._btns_destino = {}
        opciones = PluginRegistry.nombres() + ["AMBOS"]
        for opcion in opciones:
            btn = ctk.CTkButton(
                fila_destino,
                text=opcion,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=88,
                height=28,
                corner_radius=6,
                fg_color=("#1f6aa5", "#1f6aa5"),
                hover_color=("#144e7a", "#144e7a"),
            )
            btn.pack(side="left", padx=(0, 4))
            self._btns_destino[opcion] = btn
            btn.configure(command=lambda o=opcion: self._seleccionar_destino(o))
        self._seleccionar_destino("AMBOS")
        self._separador(padre)

        self.headless_var = ctk.BooleanVar(value=False)
        self._fila_toggle(padre, "Modo sin ventana de Chrome", self.headless_var)
        self._separador(padre)

        self.chrome_existente_var = ctk.BooleanVar(value=True)
        fila_chrome = ctk.CTkFrame(padre, fg_color="transparent")
        fila_chrome.pack(fill="x", pady=(4, 0))
        ctk.CTkSwitch(
            fila_chrome,
            text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var,
            font=ctk.CTkFont(size=11),
        ).pack(side="left", expand=True, anchor="w")
        ctk.CTkButton(
            fila_chrome,
            text="Abrir Chrome con depuración",
            command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10),
            height=28,
        ).pack(side="right")
        self._separador(padre)

        self.auto_submit_var = ctk.BooleanVar(value=cargar_auto_submit())
        self._fila_toggle(padre, "Auto-submit nota (HubSpot)", self.auto_submit_var)
        self.auto_submit_var.trace_add(
            "write", lambda *_: guardar_auto_submit(self.auto_submit_var.get())
        )

        fila_atajo = ctk.CTkFrame(padre, fg_color="transparent")
        fila_atajo.pack(fill="x")
        ctk.CTkLabel(
            fila_atajo,
            text="Atajo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            fila_atajo, textvariable=self.keybind_var, font=ctk.CTkFont(size=11)
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            fila_atajo,
            text="Aplicar",
            command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")
        self.keybind_label = ctk.CTkLabel(
            padre, text="", font=ctk.CTkFont(size=10), text_color=("gray40", "gray60")
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        atajo_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(atajo_inicial, lambda e: self._ejecutar())
            self._keybind_actual = atajo_inicial
            self.keybind_var.set(atajo_inicial)
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(atajo_inicial)}",
                text_color=("green", "#3fb950"),
            )
        except Exception:
            self.keybind_label.configure(
                text="Atajo no válido", text_color=("red", "#f85149")
            )

    def _seleccionar_destino(self, opcion: str):
        self.destino_var.set(opcion)
        for nombre, btn in self._btns_destino.items():
            if nombre == opcion:
                btn.configure(
                    fg_color=("#238636", "#2ea043"), hover_color=("#1e7a30", "#26963a")
                )
            else:
                btn.configure(
                    fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40")
                )



    def _crear_panel_apps(self, padre):
        ctk.CTkLabel(
            padre,
            text="Un clic → captura la región de esa app y la sube al destino activo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        self._btns_apps = {}
        self._regiones_apps = {}

        config_actual = cargar_config()
        regiones_guardadas = config_actual.get("regiones_apps", {})

        for app in APPS_CAPTURA:
            nombre = app["nombre"]
            icono = app.get("icono", "")
            color_base = app.get("color", ("#1f6aa5", "#1a5496"))

            region_efectiva = regiones_guardadas.get(nombre, app["region"])
            self._regiones_apps[nombre] = region_efectiva

            fila = ctk.CTkFrame(padre, fg_color=("gray90", "gray22"), corner_radius=8)
            fila.pack(fill="x", pady=3)
            fila.grid_columnconfigure(0, weight=1)

            r = region_efectiva
            tooltip = f"{r['width']}×{r['height']} px"
            btn_main = ctk.CTkButton(
                fila,
                text=f"{icono}  {nombre}   ▶  Capturar y subir   ({tooltip})",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=38,
                corner_radius=7,
                anchor="w",
                fg_color=color_base,
                hover_color=(
                    self._oscurecer(color_base[0]),
                    self._oscurecer(color_base[1]),
                ),
                command=lambda a=app: self._ejecutar_app(a),
            )
            btn_main.grid(row=0, column=0, padx=(6, 4), pady=5, sticky="ew")
            self._btns_apps[nombre] = btn_main

            btn_cfg = ctk.CTkButton(
                fila,
                text="⚙",
                font=ctk.CTkFont(size=14),
                width=36,
                height=38,
                corner_radius=7,
                fg_color=("gray70", "gray35"),
                hover_color=("gray60", "gray45"),
                command=lambda a=app: self._medir_region_app(a),
            )
            btn_cfg.grid(row=0, column=1, padx=(0, 6), pady=5)

        self._label_estado_app = ctk.CTkLabel(
            padre,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
            anchor="w",
        )
        self._label_estado_app.pack(fill="x", pady=(4, 0))



    def _ejecutar_app(self, app: dict):
        nombre = app["nombre"]
        region = self._regiones_apps.get(nombre, app["region"])

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.configure(state="normal")
        self.log_texto.delete("0.0", "end")
        self.log_texto.configure(state="disabled")

        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando {region['width']}×{region['height']} px…"
        )

        threading.Thread(
            target=self._proceso_app,
            args=(app, region),
            daemon=True,
        ).start()

    def _proceso_app(self, app: dict, region: dict):
        nombre = app["nombre"]

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            ui(f"→ [{nombre}] Capturando {region['width']}×{region['height']} px…")

            # FIX #3: usar iconify_window() en lugar de self.iconify()
            # self.iconify() en un Frame lanza AttributeError; el wrapper
            # del CustomCTkFrame delega correctamente a winfo_toplevel().
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region)
            ui(f"✓ [{nombre}] Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_existente = self.chrome_existente_var.get()
            auto_submit = self.auto_submit_var.get()
            destino = self.destino_var.get()

            plugins = (
                PluginRegistry.todos()
                if destino == "AMBOS"
                else (
                    [PluginRegistry.obtener(destino)]
                    if PluginRegistry.existe(destino)
                    else []
                )
            )
            if not plugins:
                ui(f"✗ No hay plugins para destino: {destino}")

            for plugin in plugins:
                ui(f"→ [{nombre}] Subiendo a {plugin.nombre}…")
                SesionService.ejecutar_subida(
                    nombre_plugin=plugin.nombre,
                    ruta_imagen=ruta,
                    log=ui,
                    headless=headless,
                    usar_chrome_existente=usar_existente,
                    credenciales_sesion=self._credenciales_sesion,
                    opciones={"auto_submit_nota": auto_submit},
                )
                ui("")

            ui(f"✓ [{nombre}] Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            ahora = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._label_ultimo_proceso.configure(
                    text=f"Último proceso: {nombre} {ahora}"
                ),
            )
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✓ {nombre} — completado a las {ahora}"
                ),
            )
            self.after(0, self._actualizar_sitios_status)

        except ErrorCaptura as e:
            self.after(
                0, lambda err=e: self._log(f"✗ [{nombre}] Error de captura: {err}")
            )
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error de captura"
                ),
            )
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ [{nombre}] Error: {err}"))
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(text=f"  ✗ {nombre} — error"),
            )
        finally:
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, self._rehabilitar_btns_apps)

    def _rehabilitar_btns_apps(self):
        for btn in self._btns_apps.values():
            btn.configure(state="normal")



    def _medir_region_app(self, app: dict):
        nombre = app["nombre"]
        monitor_idx = app.get("monitor", self._monitor_var_indice())

        self._log(f"→ Midiendo región para {nombre}…")
        self._label_estado_app.configure(
            text=f"  ⏳ Medí la región de {nombre} en pantalla…"
        )

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")





        self.iconify_window()

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()

            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    try:
                        nueva_region = ast.literal_eval(linea.split("=", 1)[1].strip())

                        self._regiones_apps[nombre] = nueva_region

                        cfg = cargar_config()
                        cfg.setdefault("regiones_apps", {})[nombre] = nueva_region
                        guardar_config(cfg)

                        def _actualizar_ui(n=nombre, r=nueva_region):
                            if n in self._btns_apps:
                                tooltip = f"{r['width']}×{r['height']} px"
                                btn = self._btns_apps[n]
                                icono = next(
                                    (
                                        a["icono"]
                                        for a in APPS_CAPTURA
                                        if a["nombre"] == n
                                    ),
                                    "",
                                )
                                color_base = next(
                                    (
                                        a["color"]
                                        for a in APPS_CAPTURA
                                        if a["nombre"] == n
                                    ),
                                    ("#1f6aa5", "#1a5496"),
                                )
                                btn.configure(
                                    text=f"{icono}  {n}   ▶  Capturar y subir   ({tooltip})",
                                    fg_color=color_base,
                                )
                            self._label_estado_app.configure(
                                text=f"  ✓ {n} — nueva región: {r['width']}×{r['height']} px guardada"
                            )
                            self._log(f"✓ Región de {n} actualizada: {r}")

                        self.after(0, _actualizar_ui)
                        self.after(0, self.deiconify_window)  # FIX #1: sin ()
                        self.after(0, self._rehabilitar_btns_apps)
                        self.after(0, lambda: self.btn.configure(state="normal"))
                        return
                    except Exception as ex:
                        self.after(
                            0,
                            lambda e=ex: self._log(f"✗ No se pudo leer la región: {e}"),
                        )

            self.after(0, lambda: self._log(f"✗ Medición cancelada para {nombre}."))
            self.after(0, lambda: self._label_estado_app.configure(text=""))
            self.after(
                0, self.deiconify_window
            )  # FIX #1: sin () — antes era deiconify_window()
            self.after(0, self._rehabilitar_btns_apps)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    @staticmethod
    def _oscurecer(color_hex: str, factor: float = 0.80) -> str:
        try:
            h = color_hex.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return "#{:02x}{:02x}{:02x}".format(
                max(0, int(r * factor)),
                max(0, int(g * factor)),
                max(0, int(b * factor)),
            )
        except Exception:
            return "#444444"

    def _crear_barra_estado(self, padre):
        frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        frame_estado.grid(row=6, column=0, sticky="ew", pady=(4, 0))
        self._punto_estado = ctk.CTkLabel(
            frame_estado,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=("#2ea043", "#3fb950"),
        )
        self._punto_estado.pack(side="left")
        self.status_var = ctk.StringVar(value="Listo")
        ctk.CTkLabel(
            frame_estado,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(4, 0))
        self._label_ultimo_proceso = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_ultimo_proceso.pack(side="right")



    def _fila_toggle(self, padre, texto, var):
        fila = ctk.CTkFrame(padre, fg_color="transparent")
        fila.pack(fill="x", pady=4)
        ctk.CTkSwitch(fila, text=texto, variable=var, font=ctk.CTkFont(size=11)).pack(
            side="left"
        )

    def _separador(self, padre):
        ctk.CTkFrame(padre, fg_color=("gray80", "gray30"), height=1).pack(
            fill="x", pady=10
        )

    def _fuente_existe(self, nombre):
        return nombre in tkinter.font.families()

    def _keybind_legible(self, kb):
        return (
            kb.replace("<", "")
            .replace(">", "")
            .replace("Control", "Ctrl")
            .replace("Return", "Enter")
            .replace("-", "+")
        )



    def _actualizar_sitios_status(self):
        for widget in self._frame_sitios.winfo_children():
            widget.destroy()

        for plugin in PluginRegistry.todos():
            nombre = plugin.nombre
            tiene_sesion = Path(f"cookies/{nombre.replace(' ', '_')}.pkl").exists()
            tiene_creds = bool(cargar_credenciales(nombre)[0])

            fila = ctk.CTkFrame(
                self._frame_sitios, fg_color=("gray93", "gray25"), border_width=1
            )
            fila.pack(fill="x", pady=(0, 4))

            if not plugin.necesita_login:
                icono, estado, color = "○", "sin login", ("green", "#3fb950")
            elif tiene_sesion:
                icono, estado, color = "●", "sesión guardada", ("royalblue", "#79c0ff")
            elif tiene_creds:
                icono, estado, color = "◑", "credenciales OK", ("orange", "#d29922")
            else:
                icono, estado, color = "○", "sin configurar", ("red", "#f85149")

            ctk.CTkLabel(
                fila, text=f" {icono} {nombre}", font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(
                fila, text=f"  {estado}  ", font=ctk.CTkFont(size=10), text_color=color
            ).pack(side="right", padx=10, pady=6)



    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        tag = (
            "ok"
            if msg.startswith("✓")
            else "error" if msg.startswith("✗") else "flecha" if "→" in msg else "dim"
        )
        self.log_texto.configure(state="normal")
        tb = self.log_texto._textbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.log_texto.see("end")
        self.log_texto.configure(state="disabled")

    def _set_status(self, texto: str):
        self.status_var.set(texto)
        colores = {
            "Listo": ("#2ea043", "#3fb950"),
            "Ejecutando...": ("#d29922", "#d29922"),
            "Completado": ("#2ea043", "#3fb950"),
            "Error": ("#f85149", "#f85149"),
        }
        self._punto_estado.configure(
            text_color=colores.get(texto, ("gray40", "gray60"))
        )



    def _lanzar_medidor(self):
        monitor_idx = self._monitor_var_indice()
        self._log(f"→ Abre el medidor en {self._monitor_var.get()}…")
        self.btn.configure(state="disabled")
        self.winfo_toplevel().iconify()

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()
            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    try:
                        region = ast.literal_eval(linea.split("=", 1)[1].strip())
                        self.after(0, lambda r=region: self._aplicar_region(r))
                        self.after(0, self.deiconify)
                        return
                    except Exception:
                        pass
            self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region: dict):
        for clave in ("top", "left", "width", "height"):
            if clave in region:
                self.region_vars[clave].set(int(region[clave]))
        self.region_paste_var.set(
            str({k: v.get() for k, v in self.region_vars.items()})
        )
        self._log(f"✓ Región actualizada: {region}")
        self.btn.configure(state="normal")

    def _obtener_region_validada(self) -> dict:
        region = {}
        for clave, var in self.region_vars.items():
            texto = var.get().strip()
            if not texto:
                raise ValueError(f"El campo '{clave}' está vacío.")
            try:
                region[clave] = int(texto)
            except ValueError:
                raise ValueError(f"El campo '{clave}' debe ser un número entero.")
        if region["width"] <= 0:
            raise ValueError("Width debe ser mayor que 0.")
        if region["height"] <= 0:
            raise ValueError("Height debe ser mayor que 0.")
        return region

    def _parsear_region(self, event=None):
        texto = self.region_paste_var.get().strip()
        if "=" in texto:
            texto = texto.split("=", 1)[1].strip()
        try:
            region = ast.literal_eval(texto)
            for clave in ("top", "left", "width", "height"):
                if clave in region:
                    self.region_vars[clave].set(int(region[clave]))
        except Exception:
            messagebox.showerror(
                "Formato inválido",
                "Pega el diccionario con el formato:\n"
                "{'top': 392, 'left': 524, 'width': 934, 'height': 404}",
            )

    def _sincronizar_paste(self, *_):
        try:
            self.region_paste_var.set(
                str({k: v.get() for k, v in self.region_vars.items()})
            )
        except Exception:
            pass



    def _abrir_login_inicial(self):
        sitios_compat = [
            {"nombre": p.nombre, "necesita_login": p.necesita_login}
            for p in PluginRegistry.con_login()
        ]
        win = VentanaCredenciales(self, sitios_compat)
        self.wait_window(win)
        if getattr(win, "confirmado", False):
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")

    def _abrir_credenciales(self):
        sitios_compat = [
            {"nombre": p.nombre, "necesita_login": p.necesita_login}
            for p in PluginRegistry.con_login()
        ]
        win = VentanaCredenciales(self, sitios_compat)
        self.wait_window(win)
        if getattr(win, "confirmado", False):
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")
        self._actualizar_sitios_status()

    def _renovar_sesion(self):
        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

    def _abrir_chrome_debug(self):
        from core.browser import puerto_activo

        if puerto_activo():
            self._log("✓ Chrome con depuración ya está activo en el puerto 9222.")
            return
        rutas = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_exe = next((r for r in rutas if Path(r).exists()), None)
        if not chrome_exe:
            self._log(
                "✗ No se encontró Chrome. Ábrelo manualmente con --remote-debugging-port=9222"
            )
            return
        import subprocess

        subprocess.Popen(
            [
                chrome_exe,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome_sesion_ssauto",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222.")



    def _aplicar_keybind(self):
        nuevo = self.keybind_var.get().strip()
        if not nuevo:
            return
        if self._keybind_actual:
            try:
                self.unbind(self._keybind_actual)
            except Exception:
                pass
        try:
            self.bind(nuevo, lambda e: self._ejecutar())
            self._keybind_actual = nuevo
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(nuevo)}",
                text_color=("green", "#3fb950"),
            )
            self._config["keybind"] = nuevo
            cfg = cargar_config()
            cfg["keybind"] = nuevo
            guardar_config(cfg)
        except Exception as e:
            self.keybind_label.configure(
                text=f"Atajo inválido: {e}", text_color=("red", "#f85149")
            )
            self._keybind_actual = None

    def _capturar_tecla(self, event):
        partes = []
        if event.state & 0x4:
            partes.append("Control")
        if event.state & 0x1:
            partes.append("Shift")
        if event.state & 0x20000:
            partes.append("Alt")
        tecla = event.keysym
        if tecla in ("Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"):
            return "break"
        partes.append(tecla)
        self.keybind_var.set("<" + "-".join(partes) + ">")
        return "break"



    def _ejecutar(self):
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.configure(state="normal")
        self.log_texto.delete("0.0", "end")
        self.log_texto.configure(state="disabled")
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = self._obtener_region_validada()
            ui(f"→ Capturando región en {self._monitor_var.get()}: {region}")
            self.after(0, self.iconify)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_existente = self.chrome_existente_var.get()
            auto_submit = self.auto_submit_var.get()
            destino = self.destino_var.get()

            if destino == "AMBOS":
                plugins = PluginRegistry.todos()
            else:
                plugins = (
                    [PluginRegistry.obtener(destino)]
                    if PluginRegistry.existe(destino)
                    else []
                )

            if not plugins:
                ui(f"✗ No hay plugins registrados para: {destino}")

            for plugin in plugins:
                ui(f"→ Subiendo a: {plugin.nombre}")
                resultado = SesionService.ejecutar_subida(
                    nombre_plugin=plugin.nombre,
                    ruta_imagen=ruta,
                    log=ui,
                    headless=headless,
                    usar_chrome_existente=usar_existente,
                    credenciales_sesion=self._credenciales_sesion,
                    opciones={"auto_submit_nota": auto_submit},
                )
                ui("")

            ui("✓ Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            ahora = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._label_ultimo_proceso.configure(
                    text=f"Último proceso: {ahora}"
                ),
            )
            self.after(0, self._actualizar_sitios_status)

        except ErrorCaptura as e:
            self.after(0, lambda err=e: self._log(f"✗ Error de captura: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ Error general: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        finally:
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _al_cerrar(self):
        cfg = cargar_config()
        cfg["ultimo_monitor"] = self._monitor_var_indice()
        guardar_config(cfg)
        self._config = cfg
        self.destroy()
````

## File: readme.md
````markdown
# SSAuto

## Descripción

SSAuto es una herramienta de escritorio para automatizar capturas de pantalla de regiones específicas de la pantalla y subirlas a uno o varios sitios web.

La aplicación combina una interfaz gráfica (`CustomTkinter`), captura de pantalla (`mss`) y automatización de navegador (`Selenium`).

## Estructura principal del proyecto

- `main.py` — punto de entrada principal.
- `configuracion.py` — configuración general y definición de sitios.
- `credenciales.py` — manejo de credenciales, cookies y llavero del sistema.
- `medidor.py` — selector visual para definir la región de captura.
- `automatizacion.py` — control de Chrome/Selenium, captura y subida.
- `ventana_principal.py` — interfaz principal de la aplicación.
- `ventana_credenciales.py` — ventana de login y credenciales.
- `config.json` — archivo de configuración generado al guardar ajustes.
- `cookies/` — cookies de sesión guardadas automáticamente.
- `screenshots/` — capturas guardadas automáticamente.

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

### Dependencias clave

- `customtkinter`
- `selenium`
- `webdriver-manager`
- `mss`
- `keyring`

## Uso

Ejecuta la aplicación desde la carpeta raíz del proyecto:

```bash
python main.py
```

## Configuración

Al iniciar por primera vez, la aplicación crea o actualiza `config.json` con los ajustes de la región y la tecla rápida.

### Cambiar la configuración de sitios

Edita `configuracion.py` para ajustar los sitios que usa la aplicación.

Para agregar un sitio nuevo, copia un bloque existente en la lista `SITIOS` y modifica:

- `nombre`
- `necesita_login`
- `url_login`
- `url_upload`
- `selector_*`

Asegúrate de que los selectores coincidan con los campos del formulario del sitio destino.

## Carpetas generadas automáticamente

- `cookies/`: cookies de sesión almacenadas en archivos.
- `screenshots/`: capturas guardadas por la aplicación.

## Consideraciones importantes

- Las cookies se almacenan localmente y no están cifradas por defecto.
- Si no hay internet, `webdriver-manager` puede fallar al descargar `chromedriver`.
- El proyecto está orientado a Windows; otros sistemas operativos pueden necesitar ajustes.

## Sugerencias de mejora

- Implementar reintentos automáticos en caso de fallos de subida.
- Crear pruebas automatizadas con `pytest`.

## Contacto

Este README fue generado para documentar y facilitar el uso del proyecto SSAuto.

# **Creado por Julian Esteban Alvarez Segura - PlanetSolar SAS**
## Licencia
Este proyecto está bajo la [Licencia MIT](LICENSE).
````

## File: .gitignore
````
__pycache__/
.vscode/
cookies/
.venv
.env
debug/
venv

# PyInstaller
build/
dist/
*.spec

# Coverage
.coverage
htmlcov/
nosetests.xml
coverage.xml
*.cover

screenshots/
````

## File: requirements.txt
````
altgraph==0.17.5
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
attrs==26.1.0
black==26.3.1
boolean.py==5.0
CacheControl==0.14.4
certifi==2026.4.22
cffi==2.0.0
charset-normalizer==3.4.7
click==8.3.3
colorama==0.4.6
coverage==7.14.0
customtkinter==5.2.2
cyclonedx-python-lib==11.7.0
darkdetect==0.8.0
defusedxml==0.7.1
docopt==0.6.2
fastapi==0.136.1
filelock==3.29.0
h11==0.16.0
hubspot-api-client==12.0.0
idna==3.13
jaraco.classes==3.4.0
jaraco.context==6.1.2
jaraco.functools==4.4.0
keyring==25.7.0
license-expression==30.4.4
markdown-it-py==4.2.0
mdurl==0.1.2
more-itertools==11.0.2
MouseInfo==0.1.3
msgpack==1.1.2
mss==10.2.0
mypy_extensions==1.1.0
outcome==1.3.0.post0
packageurl-python==0.17.6
packaging==26.2
pandas==2.3.3
pathspec==1.1.1
pefile==2024.8.26
pillow==12.2.0
pip-api==0.0.34
pip-requirements-parser==32.0.1
pip_audit==2.10.0
pipreqs==0.4.13
platformdirs==4.9.6
py-serializable==2.1.0
PyAutoGUI==0.9.54
pycparser==3.0
pydantic==2.13.4
pydantic_core==2.46.4
PyGetWindow==0.0.9
Pygments==2.20.0
pyinstaller==6.20.0
pyinstaller-hooks-contrib==2026.5
PyMsgBox==2.0.1
pyparsing==3.3.2
pyperclip==1.11.0
PyRect==0.2.0
PyScreeze==1.0.1
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
pytokens==0.4.1
pytweening==1.2.0
pywin32-ctypes==0.2.3
RapidFuzz==3.14.5
requests==2.33.1
rich==15.0.0
screeninfo==0.8.1
selenium==4.43.0
setuptools==82.0.1
six==1.17.0
sniffio==1.3.1
sortedcontainers==2.4.0
starlette==1.0.0
tomli==2.4.1
tomli_w==1.2.0
trio==0.33.0
trio-websocket==0.12.2
typing-inspection==0.4.2
typing_extensions==4.15.0
undetected-chromedriver==3.5.5
urllib3==2.6.3
uvicorn==0.46.0
webdriver-manager==4.0.2
websocket-client==1.9.0
websockets==16.0
wsproto==1.3.2
yarg==0.1.10
````

## File: main.py
````python
import customtkinter as ctk

from config.configuracion import (
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_config,
    guardar_config,
    SITIOS,
)





from core.plugin_registry import PluginRegistry
from plugins.hubspot import HubSpotPlugin
from plugins.sunrun import SunrunPlugin

PluginRegistry.registrar(HubSpotPlugin())
PluginRegistry.registrar(SunrunPlugin())



from ui.ventana_principal import App
from ui.ventana_comparacion import VentanaComparacion
from ui.ventana_credenciales import VentanaCredenciales
from ui.ventana_plantillas import VentanaPlantillas
from ui.ventana_generador_mensajes import VentanaGeneradorMensajes


config = cargar_config()
ctk.set_appearance_mode(config.get("tema", TEMA_APARIENCIA))
ctk.set_default_color_theme(TEMA_COLOR)


launcher = ctk.CTk()
launcher.title("SSAuto")


def _clamp(valor: int, minimo: int, maximo: int) -> int:
    return max(minimo, min(valor, maximo))


def _configurar_ventana_responsive():
    sw, sh = launcher.winfo_screenwidth(), launcher.winfo_screenheight()
    escala = _clamp(int(min(sw / 1920, sh / 1080) * 100), 100, 165) / 100
    ctk.set_widget_scaling(escala)
    ctk.set_window_scaling(escala)

    ancho = _clamp(int(sw * 0.68), 900, 2560)
    alto = _clamp(int(sh * 0.78), 620, 1700)
    x = max(0, (sw - ancho) // 2)
    y = max(0, (sh - alto) // 2)
    launcher.geometry(f"{ancho}x{alto}+{x}+{y}")
    launcher.minsize(860, 560)


_configurar_ventana_responsive()


# ── Helpers ───────────────────────────────────────────────────────────


def mostrar_frame(frame):
    frame.tkraise()


def abrir_plantillas():
    VentanaPlantillas(launcher)


def abrir_generador():
    VentanaGeneradorMensajes(launcher)


def abrir_credenciales():
    win = VentanaCredenciales(launcher, SITIOS)
    if win.confirmado:
        vista_principal._credenciales_sesion = win.credenciales_sesion


def cambiar_tema(opcion: str):
    tema = "dark" if opcion == "Oscuro" else "light"
    ctk.set_appearance_mode(tema)
    cfg = cargar_config()
    cfg["tema"] = tema
    guardar_config(cfg)


tema_actual = config.get("tema", TEMA_APARIENCIA)
tema_var = ctk.StringVar(value="Oscuro" if tema_actual == "dark" else "Claro")




barra = ctk.CTkFrame(launcher, height=30, corner_radius=0)
barra.pack(fill="x", side="top")
barra.pack_propagate(False)


def _btn_barra(texto: str, comando, lado="left", acento=False) -> ctk.CTkButton:
    btn = ctk.CTkButton(
        barra,
        text=texto,
        command=comando,
        font=ctk.CTkFont(size=12),
        fg_color=("#1f6aa5", "#1f6aa5") if acento else "transparent",
        text_color=("gray10", "gray90"),
        hover_color=("#144e7a", "#144e7a") if acento else ("gray80", "gray30"),
        height=26,
        width=120,
        corner_radius=4,
    )
    btn.pack(side=lado, padx=2, pady=2)
    return btn


def _sep_barra():
    ctk.CTkFrame(barra, width=1, fg_color=("gray70", "gray40")).pack(
        side="left", fill="y", padx=4, pady=4
    )




contenedor = ctk.CTkFrame(launcher)
contenedor.pack(fill="both", expand=True)
contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(0, weight=1)

frame_principal = ctk.CTkFrame(contenedor)
frame_comparacion = ctk.CTkFrame(contenedor)

for frame in (frame_principal, frame_comparacion):
    frame.grid(row=0, column=0, sticky="nsew")

vista_principal = App(frame_principal)
vista_principal.pack(fill="both", expand=True)

vista_comparacion = VentanaComparacion(frame_comparacion)
vista_comparacion.pack(fill="both", expand=True)

mostrar_frame(frame_principal)



_btn_barra("Principal", lambda: mostrar_frame(frame_principal))
_btn_barra("Comparación", lambda: mostrar_frame(frame_comparacion))
_sep_barra()
_btn_barra("Credenciales", abrir_credenciales)
_btn_barra("Plantillas", abrir_plantillas)
_btn_barra("Mensajes", abrir_generador)

ctk.CTkOptionMenu(
    barra,
    variable=tema_var,
    values=["Oscuro", "Claro"],
    command=cambiar_tema,
    font=ctk.CTkFont(size=12),
    width=92,
    height=26,
    dynamic_resizing=False,
).pack(side="right", padx=6, pady=2)

ctk.CTkLabel(
    barra,
    text="Tema:",
    font=ctk.CTkFont(size=12),
    text_color=("gray10", "gray90"),
).pack(side="right", padx=(0, 2), pady=2)





def _al_minimizar(event):
    if launcher.state() == "iconic":
        barra.pack_forget()
    else:
        barra.pack(fill="x", side="top", before=contenedor)


launcher.bind("<Unmap>", _al_minimizar)
launcher.bind("<Map>", _al_minimizar)



if __name__ == "__main__":
    try:
        launcher.mainloop()
    except KeyboardInterrupt:
        pass
````

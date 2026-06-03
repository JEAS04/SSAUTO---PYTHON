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
- Files matching these patterns are excluded: node_modules/**, dist/**, .next/**, doms/**, doku.md, data/PROPIEDADES DE CONTACTO.TXT, data/PROPIEDADES DE TICKET.TXT
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.clinerules
.gitignore
AGENTS.md
config/apps_captura.py
config/config.json
config/configuracion.py
config/credenciales.py
config/plantillas.json
core/base_plugin.py
core/browser.py
core/captura.py
core/comparador.py
core/medidor_code.py
core/medidor_runner.py
core/monitors.py
core/plugin_registry.py
data/api.py
data/buscador.py
data/hubspot_constants.py
data/test.ticket.py
GENERADOR_MENSAJES.md
gsheets/__init__.py
gsheets/core/__init__.py
gsheets/core/playwright_capture.py
gsheets/data/__init__.py
gsheets/data/sheets_api.py
gsheets/requirements-gsheets.txt
gsheets/services/__init__.py
gsheets/services/ticket_capture_service.py
gsheets/tests/__init__.py
gsheets/tests/conftest.py
gsheets/tests/test_cell_parser.py
gsheets/tests/test_image_compositor.py
gsheets/tests/test_playwright_capture.py
gsheets/tests/test_sheets_api.py
gsheets/tests/test_ticket_capture_service.py
gsheets/utils/__init__.py
gsheets/utils/cell_parser.py
gsheets/utils/image_compositor.py
image.png
LICENSE
main.py
plugins/hubspot.py
plugins/sunrun.py
plugins/template_new_site.py
readme.md
repomix.config.json
requirements.txt
scraping/__init__.py
scraping/sunrun_selectors.py
scraping/sunrun.py
SELECTORES_SUNRUN.HTML
services/driver_provider.py
services/sesion_service.py
services/session_manager.py
test/test_buscar_fsd.py
test/test_fix_final.py
tests/__init__.py
tests/conftest.py
tests/test_apps_captura.py
tests/test_base_plugin.py
tests/test_colors.py
tests/test_comparador.py
tests/test_configuracion.py
tests/test_cookies.py
tests/test_credenciales.py
tests/test_fsd.py
tests/test_integration.py
tests/test_paths.py
tests/test_plantillas.py
tests/test_plugin_registry.py
ui/comparacion/tema.py
ui/custom_ctkframe.py
ui/posicion_ventanas.py
ui/template_filler.py
ui/ventana_comparacion.py
ui/ventana_credenciales.py
ui/ventana_generador_mensajes.py
ui/ventana_plantillas.py
ui/ventana_principal.py
ui/widgets/coordinate_inputs.py
ui/widgets/log_widget.py
ui/widgets/monitor_selector.py
ui/widgets/profile_manager.py
utils/__init__.py
utils/colors.py
utils/fsd.py
utils/iniciar_chrome_sesion.py
utils/paths.py
utils/recuperar_puerto.py
version.py
```

# Files

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

## File: AGENTS.md
````markdown
# AGENTS.md — SSAuto

## Commands

```bash
python main.py               # Run the app (GUI)
pytest tests/ -v             # Run all tests (273 tests, 0 failures)
python -c "import main"      # Smoke test: verify no import/runtime errors
```

No `pyproject.toml`, no typecheck/lint config. `black` is in requirements but not configured.

## Environment

- **Windows only** (uses `ctypes.windll` for DPI awareness, `mss` monitor APIs, `keyring` Windows backend)
- Requires `.env` file at project root with `ACCESS_TOKEN=<HubSpot private app token>`
- `webdriver-manager` downloads `chromedriver` on first run (needs internet)
- Runtime folders: `screenshots/`, `cookies/`, `doms/` (auto-generated)

## Architecture

### Entry & plugin system
- `main.py` registers all site plugins in `PluginRegistry`, then builds the tkinter UI
- New destinations: create `plugins/mi_sitio.py` inheriting `SitioPlugin`, then add 2 lines to `main.py` (`import` + `PluginRegistry.registrar()`)

### UI: `ui/ventana_principal.py`
- **Class** `App` extends `CustomCTkFrame` (not `CTkFrame` directly)
- **Window methods**: use `self.iconify_window()` / `self.deiconify_window()` from `CustomCTkFrame`. Never `self.iconify()` — that's a `tkinter.Frame` method and does not exist on `CTkFrame`.
- **Layout**: `_frame_scroll` (CTkScrollableFrame) has 3 grid columns — col 0 (weight=1), col 1 (weight=2 + minsize=980px), col 2 (weight=1). All sections grid into col 1 with `sticky="ew"`.
- **`_seccion(padre, titulo, fila, col=0, pady=...)`** — no longer takes `colspan`. Creates a bordered section frame with header + body; body uses `fill="both", expand=True`.
- **`_tarjeta(padre, titulo)`** — returns `(outer_frame, inner_frame)` for card-style sub-groups. Use `grid()` on the outer frame; pack content into inner.
- **2-column rows in sections**: use `grid_columnconfigure((0, 1), weight=1)` + `sticky="nsew"` on child frames. Do NOT use `pack(side="left")/pack(side="right")` — that leaves empty gaps.
- **Section assignments:**
  | Section | Builder method | Key widgets |
  |---------|---------------|-------------|
  | REGIÓN DE CAPTURA | `_crear_panel_captura()` | profiles, monitor, coords, main button (`self.btn`) |
  | DESTINO Y SESIÓN | `_crear_panel_destino()` | sitio status, `self.destino_var`, `self._btns_destino` |
  | CONFIGURACIÓN | `_crear_opciones()` | headless/chrome/auto-submit toggles, keybind |
  | APLICACIONES DE CAPTURA | `_crear_panel_apps()` | FSD toggle+input, per-app capture buttons |
  | REGISTRO | inline in `_construir_ui` | `LogWidget` |

### FSD (smart search)
- `self.usar_fsd_var`, `self.fsd_var`, `self.fsd_entry`, `self.fsd_btn_limpiar` are initialized in `_crear_panel_apps()`, NOT in `_crear_opciones()`.
- FSD was moved from CONFIGURACIÓN to APLICACIONES DE CAPTURA.

### Refactored module layout (files created during modularization)
- `utils/fsd.py` — `solo_digitos()`, `fsd_display()`, `normalizar_fsd()`
- `utils/colors.py` — `oscurecer()` (imported; no `self._oscurecer()` anywhere)
- `utils/paths.py` — `resource_path()`
- `core/monitors.py` — `obtener_monitores()`, `obtener_nombres_monitores()`, `obtener_monitor_por_indice()`
- `core/medidor_runner.py` — `ejecutar_medidor()`
- `ui/widgets/log_widget.py` — `LogWidget` (CTkTextbox subclass with `log()`/`clear()`)
- `ui/comparacion/tema.py` — `COLORES_ESTADO`, `ETIQUETAS_ESTADO`, `DISPATCH_STATES`
- `data/hubspot_constants.py` — HubSpot property name constants
- `scraping/sunrun_selectors.py` — XPath/CSS selectors with `PATRON_CAMPO` template

### APIs & plugins
- `data/api.py` — HubSpot REST client. Constants from `data/hubspot_constants.py`.
- `plugins/hubspot.py`, `plugins/sunrun.py` — upload plugins
- `services/sesion_service.py` — orchestrates capture → upload flow (used by both `_proceso` and `_proceso_app`)
- `core/browser.py` — Chrome/Selenium factory; imports Chrome paths/ports from `config/configuracion.py`
- `core/captura.py` — screenshot capture via `mss`

### Config
- `config/configuracion.py` — global config, toggles (headless, chrome_existente, auto_submit, destino), re-exports from `core/monitors.py` and `utils/paths.py`
- `config/credenciales.py` — keyring integration + cookie serialization
- `config/apps_captura.py` — `APPS_CAPTURA` list (name, icono, region, monitor, color per app)
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

## File: core/medidor_code.py
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

## File: core/medidor_runner.py
````python
import ast
import subprocess
import sys

from .medidor_code import MEDIDOR_CODE


def ejecutar_medidor(monitor_idx: int = 1, timeout: float = 60.0) -> dict | None:

















    proc = subprocess.Popen(
        [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    try:
        stdout, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return None

    for linea in stdout.splitlines():
        if linea.startswith("REGION ="):
            try:
                return ast.literal_eval(linea.split("=", 1)[1].strip())
            except Exception:
                return None
    return None
````

## File: core/monitors.py
````python
from typing import List


_monitores_cache: list | None = None


def obtener_monitores() -> list:










    global _monitores_cache
    if _monitores_cache is not None:
        return list(_monitores_cache)
    try:
        import mss

        with mss.MSS() as sct:
            _monitores_cache = sct.monitors
            return list(_monitores_cache)
    except Exception as e:
        print(f"[✗] Error detectando monitores: {e}")
        return []


def _invalidar_cache_monitores() -> None:
    """Fuerza la próxima llamada a obtener_monitores() a consultar mss."""
    global _monitores_cache
    _monitores_cache = None


def obtener_nombres_monitores() -> List[str]:
    """
    Devuelve una lista de nombres legibles para mostrar en la UI.

    Formato: "Monitor 1 (principal)", "Monitor 2", "Todos los monitores".























    Devuelve el dict del monitor en la posición 'indice' de la lista.

    indice : int - índice del monitor (0 = virtual, 1 = primer físico, ...)
    Returns dict | None
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

## File: data/hubspot_constants.py
````python
_T_FSD = "fsd__"
_T_FIRSTNAME = "firstname"
_T_LASTNAME = "lastname"
_T_ID_GOFORMZ = "id_goformz__servicios_tecnicos_"
_T_ADDRESS = "physical_address"
_T_PHONE = "phone"
_T_PHONE_ALT = "telefono_alterno"
_T_EMAIL = "e_mail"
_T_COUNTY = "pueblo_para_servicio_tecnico"
_T_SUBJECT = "subject"
_T_NOTA = "nota_ticket__sac_"
_T_STATE = "state"
_T_ZIP = "zip"

TICKET_PROPS = [
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
_C_STATE2 = "state"
_C_MUNICIPIO = "municipio_de_residencia"
_C_MUNICIPIO_CO = "municipios_co__contacto_"
_C_ZIP = "zip"

CONTACT_PROPS = [
    _C_FIRSTNAME,
    _C_LASTNAME,
    _C_ID_GOFORMZ,
    _C_ADDRESS,
    _C_PHONE,
    _C_PHONE_ALT,
    _C_EMAIL,
    _C_STATE,
    _C_STATE2,
    _C_MUNICIPIO,
    _C_MUNICIPIO_CO,
    _C_ZIP,
]



SEARCH_CONTACT_FIELDS = {
    "nombre": "firstname",
    "apellido": "lastname",
    "telefono": "phone",
    "correo": "email",
    "direccion": "direccion__fisica_",
    "id_cliente": "id_de_goformz__contacto_",
}

SEARCH_EXACT_FIELDS = {"telefono", "correo", "id_cliente"}
````

## File: data/test.ticket.py
````python
from api import _client, _T_FSD


ticket = _client.crm.tickets.basic_api.get_by_id(
    ticket_id="45625352988", properties=["fsd__", "subject"]
)
print(ticket.properties)
















































ticket = _client.crm.tickets.basic_api.get_by_id(
    ticket_id="45542153268",
    properties=["fsd__", "subject", "firstname", "id_goformz__servicios_tecnicos_"],
)
print(ticket.properties)


contact = _client.crm.contacts.basic_api.get_by_id(
    contact_id="137594126126",
    properties=["fsd__", "firstname", "email", "id_de_goformz__contacto_"],
)
print(contact.properties)
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
**Versión**: 0.1.1  
**Autor**: SSAuto Development Team
````

## File: gsheets/__init__.py
````python
from gsheets.utils.cell_parser import (
    parse_target_cell,
    col_letter_to_index,
    index_to_col_letter,
    CellReferences,
)
from gsheets.data.sheets_api import GoogleSheetsClient
from gsheets.core.playwright_capture import PlaywrightSheetsCapture
from gsheets.utils.image_compositor import compose_ticket_image
from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
    TicketCapturePayload,
)

__all__ = [

    "parse_target_cell",
    "col_letter_to_index",
    "index_to_col_letter",
    "CellReferences",

    "GoogleSheetsClient",

    "PlaywrightSheetsCapture",

    "compose_ticket_image",

    "TicketCaptureService",
    "TicketCaptureConfig",
    "TicketCapturePayload",
]

__version__ = "1.0.0"
````

## File: gsheets/core/__init__.py
````python
from gsheets.core.playwright_capture import PlaywrightSheetsCapture

__all__ = ["PlaywrightSheetsCapture"]
````

## File: gsheets/data/__init__.py
````python
from gsheets.data.sheets_api import GoogleSheetsClient, CellValues

__all__ = ["GoogleSheetsClient", "CellValues"]
````

## File: gsheets/data/sheets_api.py
````python
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



logger = logging.getLogger(__name__)



_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
_ENV_SERVICE_ACCOUNT = "GOOGLE_SERVICE_ACCOUNT_PATH"





type CellValues = dict[str, str | None]





class GoogleSheetsClient:








    def __init__(
        self,
        credentials_path: str | Path | None = None,
        scopes: list[str] | None = None,
    ) -> None:






        self._scopes = scopes or _SCOPES

        if credentials_path is None:
            credentials_path = os.getenv(_ENV_SERVICE_ACCOUNT, "")

        if not credentials_path:
            raise ValueError(
                "Se requiere un archivo de Service Account. "
                "Pase credentials_path o defina GOOGLE_SERVICE_ACCOUNT_PATH en .env"
            )

        self._credentials_path = Path(credentials_path)
        self._service = self._build_service()



    def _build_service(self):

        if not self._credentials_path.exists():
            raise FileNotFoundError(
                f"Archivo de credenciales no encontrado: {self._credentials_path}"
            )

        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(self._credentials_path), scopes=self._scopes
            )
        except Exception as exc:
            logger.error("Error al cargar credenciales Service Account: %s", exc)
            raise ValueError(
                f"No se pudieron cargar las credenciales desde "
                f"{self._credentials_path}: {exc}"
            ) from exc

        service = build("sheets", "v4", credentials=credentials)
        logger.info("Google Sheets API: servicio inicializado correctamente.")
        return service



    def read_cell(
        self,
        spreadsheet_id: str,
        cell_range: str,
        sheet_name: str | None = None,
    ) -> str | None:











        full_range = f"'{sheet_name}'!{cell_range}" if sheet_name else cell_range

        try:
            result = (
                self._service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=full_range)
                .execute()
            )
            values = result.get("values", [])
            if values and values[0]:
                return str(values[0][0])
            return None
        except HttpError as exc:
            logger.error("Error al leer celda %s: %s", cell_range, exc)
            raise RuntimeError(f"Error al leer celda {cell_range}: {exc}") from exc

    def read_cells(
        self,
        spreadsheet_id: str,
        cell_refs: list[str],
        sheet_name: str | None = None,
    ) -> CellValues:
        """
        Lee múltiples celdas en una sola llamada batch.

        Args:
            spreadsheet_id: ID del spreadsheet.
            cell_refs: Lista de referencias (ej. ["A3", "F3", "A6", "F6"]).
            sheet_name: Nombre de la hoja (opcional).

        Returns:
            Dict {referencia: valor}. Las celdas vacías retornan None.




































        Lee un rango completo (ej. "A1:F10") y retorna matriz de valores.

        Args:
            spreadsheet_id: ID del spreadsheet.
            range_str: Rango en notación A1 (ej. "Hoja1!A1:F10").

        Returns:
            Matriz de valores [fila][columna].

















        Obtiene todas las pestañas de un spreadsheet con sus propiedades.

        Args:
            spreadsheet_id: ID del spreadsheet.

        Returns:
            Lista de dicts con {title, sheetId, index} por cada pestaña.
            Ej: [{"title": "Enero", "sheetId": 0, "index": 0}, ...]


























        Extrae el spreadsheet ID de una URL de Google Sheets.

        Ejemplos:
            https://docs.google.com/spreadsheets/d/ABC123/edit
            ABC123  ->  ABC123
````

## File: gsheets/requirements-gsheets.txt
````
# gsheets — Google Sheets cell capture with Playwright + Sheets API + Pillow
# Core
playwright>=1.45.0
google-api-python-client>=2.140.0
google-auth>=2.35.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
pillow>=10.0.0

# Already in parent project:
# python-dotenv
# requests
# urllib3
````

## File: gsheets/services/__init__.py
````python
from gsheets.services.ticket_capture_service import TicketCaptureService

__all__ = ["TicketCaptureService"]
````

## File: gsheets/services/ticket_capture_service.py
````python
from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from gsheets.utils.cell_parser import parse_target_cell, CellReferences
from gsheets.data.sheets_api import GoogleSheetsClient, CellValues
from gsheets.core.playwright_capture import PlaywrightSheetsCapture
from gsheets.utils.image_compositor import compose_ticket_image



logger = logging.getLogger(__name__)



_BASE_DIR = Path(__file__).resolve().parent.parent
_SCREENSHOTS_DIR = _BASE_DIR / "screenshots"
_SESSIONS_DIR = _BASE_DIR / "sessions"





@dataclass
class TicketCapturePayload:


    cells: CellValues


    image_path: str


    references: CellReferences


    cell_screenshots: dict[str, str]


    target_cell: str



@dataclass
class TicketCaptureConfig:


    spreadsheet_id: str


    credentials_path: str | Path = ""
    """Ruta al archivo JSON de Service Account."""

    sheet_gid: str | int = "0"


    sheet_name: str | None = None


    headless: bool = True


    output_dir: str | Path | None = None


    composite_filename: str = "ticket_capture.png"






class TicketCaptureService:


















    def __init__(
        self,
        config: TicketCaptureConfig,
        log_callback: Callable[[str], None] | None = None,
    ) -> None:
        self._config = config
        self._log = log_callback or (lambda msg: logger.info(msg))


        self._output_dir = (
            Path(config.output_dir) if config.output_dir else _SCREENSHOTS_DIR
        )
        self._output_dir.mkdir(parents=True, exist_ok=True)


        self._sheets_client: GoogleSheetsClient | None = None
        creds_path = config.credentials_path or os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "")
        if creds_path:
            self._sheets_client = self._init_sheets_client(creds_path)

        # Playwright (se inicia bajo demanda)
        self._capture: PlaywrightSheetsCapture | None = None
        self._capture_owned = False  # True si nosotros iniciamos Playwright

    # ── Inicialización ────────────────────────────────────────────────────

    def _init_sheets_client(self, credentials_path: str | Path) -> GoogleSheetsClient:
        self._log("→ Inicializando cliente de Google Sheets API...")
        client = GoogleSheetsClient(credentials_path)
        self._log("✓ Cliente de Google Sheets API listo.")
        return client

    # ── Context manager ───────────────────────────────────────────────────

    async def __aenter__(self) -> "TicketCaptureService":
        await self._ensure_capture()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._capture and self._capture_owned:
            await self._capture.stop()
            self._capture = None
            self._capture_owned = False

    async def _ensure_capture(self) -> PlaywrightSheetsCapture:

        if self._capture is None:
            self._capture = PlaywrightSheetsCapture(
                headless=self._config.headless,
                session_dir=self._config.output_dir or _SESSIONS_DIR,
                screenshots_dir=self._output_dir,
                log_callback=self._log,
            )
            await self._capture.start()
            self._capture_owned = True
        return self._capture



    async def capture(self, cell_ref: str) -> TicketCapturePayload:













        self._log(f"=== INICIANDO CAPTURA PARA CELDA: {cell_ref} ===")

        # ── Paso 1: Parsear celda objetivo ──
        self._log(f"→ Paso 1/5: Parseando celda '{cell_ref}'...")
        refs_dict = parse_target_cell(cell_ref)
        references = CellReferences(
            top_left=refs_dict["top_left"],
            top_right=refs_dict["top_right"],
            bottom_left=refs_dict["bottom_left"],
            bottom_right=refs_dict["bottom_right"],
            target=cell_ref.strip().upper(),
        )
        all_refs = references.all_refs()
        self._log(
            f"✓ Referencias calculadas: {references.top_left}, "
            f"{references.top_right}, {references.bottom_left}, "
            f"{references.bottom_right}"
        )

        # ── Paso 2: Obtener valores desde Sheets API ──
        self._log("→ Paso 2/5: Leyendo valores desde Google Sheets API...")
        if self._sheets_client is None:
            raise RuntimeError(
                "Cliente de Google Sheets no configurado. "
                "Provea 'credentials_path' en TicketCaptureConfig."
            )

        spreadsheet_id = GoogleSheetsClient.extract_spreadsheet_id(
            self._config.spreadsheet_id
        )

        cell_values = self._sheets_client.read_cells(
            spreadsheet_id=spreadsheet_id,
            cell_refs=all_refs,
            sheet_name=self._config.sheet_name,
        )
        self._log(f"✓ Valores obtenidos: {cell_values}")

        # ── Paso 3: Capturar celdas con Playwright ──
        self._log("→ Paso 3/5: Capturando celdas con Playwright...")
        capture = await self._ensure_capture()

        sheet_url = (
            self._config.spreadsheet_id
            if "docs.google.com" in self._config.spreadsheet_id
            else f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        )


        effective_gid = self._config.sheet_gid
        if self._config.sheet_name:
            try:
                sheets = self._sheets_client.list_sheets(spreadsheet_id)
                for s in sheets:
                    if s["title"] == self._config.sheet_name:
                        effective_gid = s["sheetId"]
                        self._log(
                            f"→ Pestaña '{self._config.sheet_name}' → gid={effective_gid}"
                        )
                        break
                else:
                    self._log(
                        f"⚠ Pestaña '{self._config.sheet_name}' no encontrada. "
                        f"Usando gid={effective_gid}."
                    )
            except Exception as e:
                self._log(
                    f"⚠ No se pudo resolver el gid de '{self._config.sheet_name}': {e}. "
                    f"Usando gid={effective_gid}."
                )

        cell_screenshots = await capture.capture_cells(
            sheet_url=sheet_url,
            cell_refs=all_refs,
            output_dir=str(self._output_dir),
            sheet_gid=effective_gid,
            expected_values=cell_values,
        )
        self._log(f"✓ {len(cell_screenshots)} capturas individuales generadas.")

        # ── Paso 4: Componer imagen ──
        self._log("→ Paso 4/5: Generando imagen compuesta...")
        composite_path = str(self._output_dir / self._config.composite_filename)

        compose_ticket_image(
            top_left_path=cell_screenshots[references.top_left],
            top_right_path=cell_screenshots[references.top_right],
            bottom_left_path=cell_screenshots[references.bottom_left],
            bottom_right_path=cell_screenshots[references.bottom_right],
            output_path=composite_path,
            labels={
                "top_left": references.top_left,
                "top_right": references.top_right,
                "bottom_left": references.bottom_left,
                "bottom_right": references.bottom_right,
            },
        )
        self._log(f"✓ Imagen compuesta guardada: {composite_path}")

        # ── Paso 5: Construir payload ──
        self._log("→ Paso 5/5: Construyendo payload...")
        payload = TicketCapturePayload(
            cells=cell_values,
            image_path=composite_path,
            references=references,
            cell_screenshots=cell_screenshots,
            target_cell=cell_ref.strip().upper(),
        )

        self._log(f"=== CAPTURA COMPLETADA: {cell_ref} ===")
        return payload

    def capture_sync(self, cell_ref: str) -> TicketCapturePayload:
        """
        Versión síncrona de capture() para usar desde threads o tkinter.

        Ejecuta el flujo completo (parser → API → Playwright → composición)
        de forma bloqueante usando asyncio.run(). Ideal para llamar desde
        threading.Thread sin modificar el modelo de concurrencia del proyecto.

        Args:
            cell_ref: Referencia de celda (ej. "F6", "AA10").

        Returns:
            TicketCapturePayload con valores, imagen compuesta, y referencias.









capture() + stop() para asegurar que los recursos se limpien."""
        try:
            return await self.capture(cell_ref)
        finally:
            if self._capture and self._capture_owned:
                await self._capture.stop()
                self._capture = None
                self._capture_owned = False
                # Dar tiempo a que se drenen los pipes antes de cerrar el loop
                await asyncio.sleep(0.3)

    # ── Placeholder para HubSpot ──────────────────────────────────────────

    def upload_to_hubspot(self, payload: TicketCapturePayload) -> dict[str, Any]:
        """
        PLACEHOLDER — Conectar con lógica existente de HubSpot.

        Este método está reservado para recibir el payload generado por
        capture() y enviarlo a HubSpot usando la lógica ya implementada
        en data/api.py y plugins/hubspot.py.

        Args:
            payload: Payload generado por TicketCaptureService.capture().

        Returns:
            Diccionario con resultado de la operación (por definir).




















Cierra el navegador Playwright si está abierto."""
        if self._capture:
            await self._capture.stop()
            self._capture = None
            self._capture_owned = False

    @property
    def sheets_client(self) -> GoogleSheetsClient | None:
        """Acceso al cliente de Sheets API para operaciones adicionales."""
        return self._sheets_client

    @property
    def capture_instance(self) -> PlaywrightSheetsCapture | None:
        """Acceso a la instancia de Playwright para operaciones adicionales."""
        return self._capture
````

## File: gsheets/tests/__init__.py
````python

````

## File: gsheets/tests/conftest.py
````python
import pytest


def pytest_configure(config):


    try:
        config.option.asyncio_mode = "auto"
    except Exception:
        pass
````

## File: gsheets/tests/test_cell_parser.py
````python
import pytest
from gsheets.utils.cell_parser import (
    parse_target_cell,
    col_letter_to_index,
    index_to_col_letter,
    build_cell_references,
    CellReferences,
)





class TestParseTargetCell:
    def test_basic_f6(self):
        result = parse_target_cell("F6")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "F3"
        assert result["bottom_left"] == "A6"
        assert result["bottom_right"] == "F6"

    def test_large_cell_j20(self):
        result = parse_target_cell("J20")
        assert result == {
            "top_left": "A3",
            "top_right": "J3",
            "bottom_left": "A20",
            "bottom_right": "J20",
        }

    def test_double_letter_aa10(self):
        result = parse_target_cell("AA10")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "AA3"
        assert result["bottom_left"] == "A10"
        assert result["bottom_right"] == "AA10"

    def test_triple_letter_zz100(self):
        result = parse_target_cell("ZZ100")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "ZZ3"
        assert result["bottom_left"] == "A100"
        assert result["bottom_right"] == "ZZ100"

    def test_ab25(self):
        result = parse_target_cell("AB25")
        assert result == {
            "top_left": "A3",
            "top_right": "AB3",
            "bottom_left": "A25",
            "bottom_right": "AB25",
        }

    def test_a1_extreme_min_row(self):
        result = parse_target_cell("A1")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "A3"
        assert result["bottom_left"] == "A1"
        assert result["bottom_right"] == "A1"

    def test_lowercase_input(self):
        result = parse_target_cell("f6")
        assert result["bottom_right"] == "F6"

    def test_input_with_spaces(self):
        result = parse_target_cell("  F6  ")
        assert result["bottom_right"] == "F6"

    def test_single_letter_z1(self):
        result = parse_target_cell("Z1")
        assert result["top_right"] == "Z3"
        assert result["bottom_right"] == "Z1"

    def test_invalid_format_raises_valueerror(self):
        with pytest.raises(ValueError, match="Formato de celda inválido"):
            parse_target_cell("6F")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("")

    def test_only_letters_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("ABC")

    def test_only_numbers_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("123")

    def test_row_zero_raises(self):
        with pytest.raises(ValueError, match="fila"):
            parse_target_cell("A0")

    def test_negative_row_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("A-5")





class TestColLetterToIndex:
    def test_a_is_0(self):
        assert col_letter_to_index("A") == 0

    def test_b_is_1(self):
        assert col_letter_to_index("B") == 1

    def test_z_is_25(self):
        assert col_letter_to_index("Z") == 25

    def test_aa_is_26(self):
        assert col_letter_to_index("AA") == 26

    def test_ab_is_27(self):
        assert col_letter_to_index("AB") == 27

    def test_az_is_51(self):
        assert col_letter_to_index("AZ") == 51

    def test_ba_is_52(self):
        assert col_letter_to_index("BA") == 52

    def test_zz_is_701(self):
        assert col_letter_to_index("ZZ") == 701

    def test_aaa_is_702(self):
        assert col_letter_to_index("AAA") == 702

    def test_lowercase(self):
        assert col_letter_to_index("f") == 5





class TestIndexToColLetter:
    def test_0_is_a(self):
        assert index_to_col_letter(0) == "A"

    def test_25_is_z(self):
        assert index_to_col_letter(25) == "Z"

    def test_26_is_aa(self):
        assert index_to_col_letter(26) == "AA"

    def test_27_is_ab(self):
        assert index_to_col_letter(27) == "AB"

    def test_701_is_zz(self):
        assert index_to_col_letter(701) == "ZZ"

    def test_702_is_aaa(self):
        assert index_to_col_letter(702) == "AAA"

    def test_roundtrip(self):
        for col_letter in ["A", "B", "Z", "AA", "AB", "AZ", "BA", "ZZ", "ABC"]:
            idx = col_letter_to_index(col_letter)
            assert index_to_col_letter(idx) == col_letter





class TestBuildCellReferences:
    def test_returns_cell_references_object(self):
        refs = build_cell_references("F6")
        assert isinstance(refs, CellReferences)
        assert refs.target == "F6"
        assert refs.top_left == "A3"

    def test_all_refs_returns_list(self):
        refs = build_cell_references("F6")
        assert refs.all_refs() == ["A3", "F3", "A6", "F6"]

    def test_as_dict(self):
        refs = build_cell_references("AA10")
        d = refs.as_dict()
        assert d["bottom_right"] == "AA10"
        assert len(d) == 4





class TestCellReferencesDataclass:
    def test_frozen(self):
        refs = CellReferences("A3", "F3", "A6", "F6", "F6")
        with pytest.raises(Exception):
            refs.top_left = "B3"

    def test_equality(self):
        a = CellReferences("A3", "F3", "A6", "F6", "F6")
        b = CellReferences("A3", "F3", "A6", "F6", "F6")
        assert a == b
````

## File: gsheets/tests/test_image_compositor.py
````python
from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from gsheets.utils.image_compositor import compose_ticket_image





def _create_test_image(
    path: str | Path, width: int, height: int, color: tuple[int, int, int]
) -> Path:

    path = Path(path)
    img = Image.new("RGB", (width, height), color)
    img.save(path, "PNG")
    return path





@pytest.fixture
def cell_images(tmp_path):

    images = {}
    images["a3"] = _create_test_image(
        tmp_path / "a3.png", 100, 25, (255, 200, 200)
    )
    images["f3"] = _create_test_image(
        tmp_path / "f3.png", 120, 25, (200, 255, 200)
    )
    images["a6"] = _create_test_image(
        tmp_path / "a6.png", 100, 30, (200, 200, 255)
    )
    images["f6"] = _create_test_image(
        tmp_path / "f6.png", 120, 30, (255, 255, 200)
    )
    return images





class TestComposeTicketImage:
    def test_compose_creates_image(self, cell_images, tmp_path):
        output = tmp_path / "ticket_capture.png"

        result = compose_ticket_image(
            top_left_path=cell_images["a3"],
            top_right_path=cell_images["f3"],
            bottom_left_path=cell_images["a6"],
            bottom_right_path=cell_images["f6"],
            output_path=output,
        )

        assert output.exists()
        assert result == str(output.resolve())


        img = Image.open(output)


        assert img.width == 222
        assert img.height == 57

    def test_compose_different_sizes(self, tmp_path):

        tl = _create_test_image(tmp_path / "tl.png", 80, 20, (255, 0, 0))
        tr = _create_test_image(tmp_path / "tr.png", 150, 35, (0, 255, 0))
        bl = _create_test_image(tmp_path / "bl.png", 90, 40, (0, 0, 255))
        br = _create_test_image(tmp_path / "br.png", 140, 25, (255, 255, 0))

        output = tmp_path / "composed.png"
        compose_ticket_image(tl, tr, bl, br, output)

        img = Image.open(output)




        assert img.width == 90 + 150 + 2
        assert img.height == 35 + 40 + 2

    def test_compose_with_labels(self, cell_images, tmp_path):
        output = tmp_path / "with_labels.png"

        compose_ticket_image(
            top_left_path=cell_images["a3"],
            top_right_path=cell_images["f3"],
            bottom_left_path=cell_images["a6"],
            bottom_right_path=cell_images["f6"],
            output_path=output,
            labels={
                "top_left": "A3",
                "top_right": "F3",
                "bottom_left": "A6",
                "bottom_right": "F6",
            },
        )

        assert output.exists()

    def test_missing_file_raises(self, cell_images, tmp_path):
        output = tmp_path / "fail.png"

        with pytest.raises(FileNotFoundError):
            compose_ticket_image(
                top_left_path="nonexistent.png",
                top_right_path=cell_images["f3"],
                bottom_left_path=cell_images["a6"],
                bottom_right_path=cell_images["f6"],
                output_path=output,
            )

    def test_corrupt_file_raises(self, cell_images, tmp_path):
        corrupt = tmp_path / "corrupt.png"
        corrupt.write_text("not an image")

        output = tmp_path / "fail2.png"

        with pytest.raises(ValueError):
            compose_ticket_image(
                top_left_path=corrupt,
                top_right_path=cell_images["f3"],
                bottom_left_path=cell_images["a6"],
                bottom_right_path=cell_images["f6"],
                output_path=output,
            )
````

## File: gsheets/tests/test_playwright_capture.py
````python
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from gsheets.core.playwright_capture import PlaywrightSheetsCapture





def _build_mock_playwright():

    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.screenshot = AsyncMock()
    mock_page.reload = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.title = AsyncMock(return_value="Mi Hoja — Google Sheets")


    async def _smart_evaluate(js, arg=None):
        if arg is None:

            return "#waffle-grid-container, #colheaders, #rowheaders"
        if isinstance(arg, list):
            if len(arg) == 3 and isinstance(arg[0], str):

                return {
                    "x": 100, "y": 200, "w": 120, "h": 25,
                    "tag": "div", "cls": "cell-active", "text": "F6",
                    "hasBorder": True, "score": 10,
                }

            return {
                "x": 98, "y": 198, "w": 120, "h": 25,
                "tag": "div", "cls": "cell-active", "text": "F6",
                "hasBorder": True, "score": 10,
            }

        return {"x": 100, "y": 200, "width": 120, "height": 25}

    mock_page.evaluate = AsyncMock(side_effect=_smart_evaluate)
    type(mock_page).url = PropertyMock(
        return_value="https://docs.google.com/spreadsheets/d/ABC123/edit#gid=0&range=A3"
    )


    mock_context = AsyncMock()
    mock_context.pages = [mock_page]
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_context.close = AsyncMock()


    mock_browser = AsyncMock()
    mock_browser.contexts = [mock_context]
    mock_browser.close = AsyncMock()

    mock_pw_instance = AsyncMock()
    mock_pw_instance.chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)
    mock_pw_instance.chromium.launch_persistent_context = AsyncMock(
        return_value=mock_context
    )
    mock_pw_instance.stop = AsyncMock()

    return {
        "page": mock_page,
        "context": mock_context,
        "browser": mock_browser,
        "pw_instance": mock_pw_instance,
    }





@pytest.fixture
def mock_pw():

    mocks = _build_mock_playwright()
    with patch(
        "gsheets.core.playwright_capture.async_playwright"
    ) as mock_async_pw:
        mock_cm = MagicMock()
        mock_cm.start = AsyncMock(return_value=mocks["pw_instance"])
        mock_async_pw.return_value = mock_cm
        yield mocks





class TestPlaywrightSheetsCapture:
    @pytest.mark.asyncio
    async def test_start_connects_via_cdp(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        await cap.start()
        try:
            assert cap._context is not None
            assert cap._page is not None

            mock_pw["pw_instance"].chromium.connect_over_cdp.assert_called_once()
        finally:
            await cap.stop()

    def test_page_property_raises_when_not_started(self):
        cap = PlaywrightSheetsCapture(headless=True)
        with pytest.raises(RuntimeError, match="no ha sido iniciado"):
            _ = cap.page

    def test_extract_spreadsheet_id_from_url(self):
        url = "https://docs.google.com/spreadsheets/d/XYZ789/edit#gid=0"
        result = PlaywrightSheetsCapture._extract_spreadsheet_id(url)
        assert result == "XYZ789"

    def test_extract_spreadsheet_id_passthrough(self):
        result = PlaywrightSheetsCapture._extract_spreadsheet_id("ABC123")
        assert result == "ABC123"

    @pytest.mark.asyncio
    async def test_capture_cell_navigates_and_screenshots(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        path = await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="A3",
        )

        mock_pw["page"].goto.assert_called_once()
        assert "domcontentloaded" in str(mock_pw["page"].goto.call_args)

        assert mock_pw["page"].screenshot.call_count >= 2
        assert "a3" in path.lower()

    @pytest.mark.asyncio
    async def test_capture_cell_retry_on_none_rect(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        locate_calls = [0]

        async def mock_evaluate(js, arg=None):
            if arg is None:
                return "#waffle-grid-container"
            if isinstance(arg, list):
                return {"x": 100, "y": 200, "w": 100, "h": 20, "tag": "div", "cls": "", "text": "F6", "hasBorder": True, "score": 10}
            locate_calls[0] += 1
            if locate_calls[0] == 1:
                return None
            return {"x": 50, "y": 60, "width": 100, "height": 20}

        mock_pw["page"].evaluate = AsyncMock(side_effect=mock_evaluate)

        await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="F6",
        )

        assert locate_calls[0] >= 2
        mock_pw["page"].reload.assert_called_once()

    @pytest.mark.asyncio
    async def test_capture_cell_raises_when_unlocatable(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        async def mock_evaluate(js, arg=None):
            if arg is None:
                return "#waffle-grid-container"
            if isinstance(arg, list):
                return None
            return None

        mock_pw["page"].evaluate = AsyncMock(side_effect=mock_evaluate)
        mock_pw["page"].screenshot = AsyncMock()

        with pytest.raises(RuntimeError, match="No se pudo localizar"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="ZZ999",
            )

    @pytest.mark.asyncio
    async def test_login_redirect_raises_explicit_error(self, mock_pw):

        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]


        mock_pw["page"].title = AsyncMock(return_value="Sign in – Google Accounts")
        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://accounts.google.com/signin/v2/identifier?..."
        )

        with pytest.raises(RuntimeError, match="autenticada"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

    @pytest.mark.asyncio
    async def test_login_title_detection_raises(self, mock_pw):

        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]

        mock_pw["page"].title = AsyncMock(return_value="Sign in – Google Accounts")
        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://docs.google.com/spreadsheets/d/ABC123/edit"
        )

        with pytest.raises(RuntimeError, match="login de Google"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

    @pytest.mark.asyncio
    async def test_verify_google_auth_myaccount_check(self, mock_pw):

        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]


        await cap._verify_google_auth()

        assert cap._auth_verified is True
        first_call = mock_pw["page"].goto.call_args_list[0][0][0]
        assert "myaccount.google.com" in first_call

    @pytest.mark.asyncio
    async def test_verify_google_auth_redirect_detected(self, mock_pw):

        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]

        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://accounts.google.com/signin/v2/identifier?..."
        )

        with pytest.raises(RuntimeError, match="no está autenticada"):
            await cap._verify_google_auth()

        assert cap._auth_verified is False

    @pytest.mark.asyncio
    async def test_capture_cells_multiple(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        result = await cap.capture_cells(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_refs=["A3", "F3", "A6", "F6"],
        )

        assert len(result) == 4
        assert "A3" in result
        assert "F6" in result

    @pytest.mark.asyncio
    async def test_capture_cell_uses_exact_gid(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="A3",
            sheet_gid="42",
        )

        call_url = mock_pw["page"].goto.call_args[0][0]
        assert "gid=42" in call_url

    @pytest.mark.asyncio
    async def test_grid_not_found_generates_debug(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        mock_pw["page"].wait_for_selector = AsyncMock(
            side_effect=Exception("timeout")
        )
        mock_pw["page"].evaluate = AsyncMock(return_value=None)
        mock_pw["page"].screenshot = AsyncMock()

        with pytest.raises(RuntimeError, match="grid"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

        assert mock_pw["page"].screenshot.call_count >= 1

    def test_clear_session(self, tmp_path):
        profile_dir = tmp_path / "chrome_profile"
        profile_dir.mkdir()

        cap = PlaywrightSheetsCapture(headless=True, profile_dir=profile_dir)
        assert cap._profile_dir.exists()
        cap.clear_session()
        assert not cap._profile_dir.exists()

    def test_capture_cells_sync_wrapper(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        result = cap.capture_cells_sync(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_refs=["A3", "F6"],
        )

        assert len(result) == 2
        assert "A3" in result
        assert "F6" in result
        mock_pw["context"].close.assert_called_once()
        mock_pw["pw_instance"].stop.assert_called_once()
````

## File: gsheets/tests/test_sheets_api.py
````python
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gsheets.data.sheets_api import GoogleSheetsClient





@pytest.fixture
def fake_credentials_file():

    data = {
        "type": "service_account",
        "project_id": "test-project",
        "private_key_id": "abc123",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMOCK\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test-project.iam.gserviceaccount.com",
        "client_id": "123456789",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(data, f)
        path = f.name
    yield path
    Path(path).unlink(missing_ok=True)


@pytest.fixture
def mock_service():

    with patch(
        "gsheets.data.sheets_api.service_account.Credentials.from_service_account_file"
    ) as mock_creds:
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials

        with patch("gsheets.data.sheets_api.build") as mock_build:
            mock_sheets = MagicMock()
            mock_build.return_value = mock_sheets
            yield mock_sheets





class TestGoogleSheetsClient:
    def test_init_loads_credentials(self, fake_credentials_file, mock_service):
        client = GoogleSheetsClient(fake_credentials_file)
        assert client._service is not None

    def test_init_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            GoogleSheetsClient("nonexistent_file.json")

    def test_read_cell_returns_value(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["Hello"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "A3")

        assert result == "Hello"

    def test_read_cell_empty_returns_none(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {}

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "A3")

        assert result is None

    def test_read_cell_with_sheet_name(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["Data"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "B5", sheet_name="Hoja1")

        assert result == "Data"

    def test_read_cells_batch(self, fake_credentials_file, mock_service):
        mock_batch = mock_service.spreadsheets.return_value.values.return_value
        mock_batch.batchGet.return_value.execute.return_value = {
            "valueRanges": [
                {"values": [["val_a3"]]},
                {"values": [["val_f3"]]},
                {},
                {"values": [["val_f6"]]},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cells(
            "spreadsheet123", ["A3", "F3", "A6", "F6"]
        )

        assert result == {
            "A3": "val_a3",
            "F3": "val_f3",
            "A6": None,
            "F6": "val_f6",
        }

    def test_read_cells_with_sheet_name(self, fake_credentials_file, mock_service):
        mock_batch = mock_service.spreadsheets.return_value.values.return_value
        mock_batch.batchGet.return_value.execute.return_value = {
            "valueRanges": [
                {"values": [["x"]]},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cells(
            "spreadsheet123", ["A1"], sheet_name="MiHoja"
        )

        assert result == {"A1": "x"}

    def test_read_range(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["A", "B"], ["C", "D"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_range("spreadsheet123", "A1:B2")

        assert result == [["A", "B"], ["C", "D"]]

    def test_extract_spreadsheet_id_from_url(self):
        url = "https://docs.google.com/spreadsheets/d/ABC123xyz/edit#gid=0"
        result = GoogleSheetsClient.extract_spreadsheet_id(url)
        assert result == "ABC123xyz"

    def test_extract_spreadsheet_id_passthrough(self):
        result = GoogleSheetsClient.extract_spreadsheet_id("ABC123")
        assert result == "ABC123"

    def test_credentials_from_env(self, fake_credentials_file, mock_service, monkeypatch):

        monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_PATH", fake_credentials_file)
        client = GoogleSheetsClient()
        assert client._service is not None

    def test_no_credentials_raises(self, monkeypatch):

        monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_PATH", raising=False)
        with pytest.raises(ValueError, match="Service Account"):
            GoogleSheetsClient()

    def test_list_sheets(self, fake_credentials_file, mock_service):

        mock_get = mock_service.spreadsheets.return_value.get.return_value
        mock_get.execute.return_value = {
            "sheets": [
                {"properties": {"title": "Enero", "sheetId": 0, "index": 0}},
                {"properties": {"title": "Febrero", "sheetId": 1, "index": 1}},
                {"properties": {"title": "Marzo", "sheetId": 2, "index": 2}},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.list_sheets("spreadsheet123")

        assert len(result) == 3
        assert result[0]["title"] == "Enero"
        assert result[0]["sheetId"] == 0
        assert result[0]["index"] == 0
        assert result[2]["title"] == "Marzo"

    def test_list_sheets_empty(self, fake_credentials_file, mock_service):

        mock_get = mock_service.spreadsheets.return_value.get.return_value
        mock_get.execute.return_value = {"sheets": []}

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.list_sheets("spreadsheet123")

        assert result == []
````

## File: gsheets/tests/test_ticket_capture_service.py
````python
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
    TicketCapturePayload,
)





@pytest.fixture
def config():
    return TicketCaptureConfig(
        spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
        credentials_path="fake_creds.json",
        sheet_gid="0",
        headless=True,
        output_dir=None,
    )


@pytest.fixture
def mock_sheets_client():

    with patch(
        "gsheets.services.ticket_capture_service.GoogleSheetsClient"
    ) as mock:
        client = MagicMock()

        def _read_cells(spreadsheet_id, cell_refs, sheet_name=None):
            return {ref: f"value_{ref}" for ref in cell_refs}

        client.read_cells.side_effect = _read_cells
        # list_sheets retorna pestañas con títulos y gids
        client.list_sheets.return_value = [
            {"title": "Enero", "sheetId": 0, "index": 0},
            {"title": "Febrero", "sheetId": 1, "index": 1},
            {"title": "Jun", "sheetId": 123456, "index": 2},
        ]
        mock.return_value = client
        mock.extract_spreadsheet_id.return_value = "TEST123"
        yield mock


def _make_capture_cells_response(sheet_url, cell_refs, output_dir=None, sheet_gid="0", expected_values=None):

    return {ref: f"/tmp/{ref.lower()}.png" for ref in cell_refs}


@pytest.fixture
def mock_playwright_capture():

    with patch(
        "gsheets.services.ticket_capture_service.PlaywrightSheetsCapture"
    ) as mock:
        cap = AsyncMock()
        cap.start = AsyncMock()
        cap.stop = AsyncMock()
        cap.capture_cells = AsyncMock(
            side_effect=_make_capture_cells_response
        )
        mock.return_value = cap
        yield mock


@pytest.fixture
def mock_compose(tmp_path):

    output = str(tmp_path / "ticket_capture.png")
    with patch(
        "gsheets.services.ticket_capture_service.compose_ticket_image"
    ) as mock:
        mock.return_value = output
        yield mock





class TestTicketCaptureConfig:
    def test_defaults(self):
        config = TicketCaptureConfig(spreadsheet_id="ABC123")
        assert config.spreadsheet_id == "ABC123"
        assert config.sheet_gid == "0"
        assert config.headless is True
        assert config.composite_filename == "ticket_capture.png"
        assert config.sheet_name is None
        assert config.credentials_path == ""


class TestTicketCaptureService:
    @pytest.mark.asyncio
    async def test_capture_full_flow(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        payload = await service.capture("F6")

        assert isinstance(payload, TicketCapturePayload)
        assert payload.target_cell == "F6"
        assert payload.cells == {
            "A3": "value_A3",
            "F3": "value_F3",
            "A6": "value_A6",
            "F6": "value_F6",
        }
        assert "ticket_capture.png" in payload.image_path
        assert payload.references.top_left == "A3"
        assert payload.references.top_right == "F3"
        assert payload.references.bottom_left == "A6"
        assert payload.references.bottom_right == "F6"
        assert len(payload.cell_screenshots) == 4

        mock_compose.assert_called_once()

    @pytest.mark.asyncio
    async def test_capture_invalid_cell_raises(
        self, tmp_path, mock_sheets_client
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config, log_callback=lambda m: None)

        with pytest.raises(ValueError):
            await service.capture("")

    @pytest.mark.asyncio
    async def test_capture_with_sheet_name(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            sheet_name="Datos",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        await service.capture("J20")

        called_kwargs = mock_sheets_client.return_value.read_cells.call_args
        assert called_kwargs.kwargs["sheet_name"] == "Datos"

    @pytest.mark.asyncio
    async def test_capture_resolves_sheet_name_to_gid(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):

        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            sheet_name="Jun",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        await service.capture("F6")


        called_kwargs = mock_playwright_capture.return_value.capture_cells.call_args
        assert called_kwargs.kwargs["sheet_gid"] == 123456

    @pytest.mark.asyncio
    async def test_capture_without_credentials_raises(self, tmp_path, monkeypatch):

        monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_PATH", raising=False)
        config = TicketCaptureConfig(
            spreadsheet_id="TEST123",
            credentials_path="",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        with pytest.raises(RuntimeError, match="Google Sheets"):
            await service.capture("F6")

    @pytest.mark.asyncio
    async def test_context_manager(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        async with TicketCaptureService(config) as service:
            payload = await service.capture("AB25")

        assert payload.references.bottom_right == "AB25"
        mock_playwright_capture.return_value.stop.assert_called_once()

    def test_upload_to_hubspot_placeholder(self, tmp_path, mock_sheets_client):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        payload = TicketCapturePayload(
            cells={"A3": "test"},
            image_path="/tmp/img.png",
            references=MagicMock(),
            cell_screenshots={},
            target_cell="F6",
        )

        result = service.upload_to_hubspot(payload)

        assert result["status"] == "placeholder"
        assert "implementado" in result["message"]

    @pytest.mark.asyncio
    async def test_close(
        self, tmp_path, mock_sheets_client, mock_playwright_capture
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        service._capture = mock_playwright_capture.return_value
        await service.close()

        mock_playwright_capture.return_value.stop.assert_called_once()
        assert service._capture is None

    def test_capture_sync_wrapper(
        self, tmp_path, mock_sheets_client, mock_playwright_capture, mock_compose
    ):

        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        payload = service.capture_sync("F6")

        assert payload.target_cell == "F6"
        assert "ticket_capture.png" in payload.image_path
        assert len(payload.cell_screenshots) == 4

    def test_credentials_from_env(
        self, tmp_path, mock_sheets_client, mock_playwright_capture, mock_compose, monkeypatch
    ):

        monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_PATH", "/fake/path.json")
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="",  # vacío → debe tomarse del env
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        assert service._sheets_client is not None


class TestTicketCapturePayload:
    def test_payload_attributes(self):
        payload = TicketCapturePayload(
            cells={"A3": "hello", "F6": "world"},
            image_path="/tmp/test.png",
            references=MagicMock(),
            cell_screenshots={"A3": "/tmp/a3.png", "F6": "/tmp/f6.png"},
            target_cell="F6",
        )

        assert payload.cells["A3"] == "hello"
        assert payload.target_cell == "F6"
        assert "F6" in payload.cell_screenshots
````

## File: gsheets/utils/__init__.py
````python
from gsheets.utils.cell_parser import parse_target_cell, col_letter_to_index, index_to_col_letter, CellReferences
from gsheets.utils.image_compositor import compose_ticket_image

__all__ = [
    "parse_target_cell",
    "col_letter_to_index",
    "index_to_col_letter",
    "CellReferences",
    "compose_ticket_image",
]
````

## File: gsheets/utils/cell_parser.py
````python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any



_COL_FIJA = "A"
_FILA_FIJA = 3

_PATRON_CELDA = re.compile(r"^([A-Za-z]+)(\d+)$")

# ── Dataclass ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class CellReferences:
    """Cuatro referencias generadas a partir de una celda objetivo."""

    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    target: str

    def as_dict(self) -> dict[str, str]:
        return {
            "top_left": self.top_left,
            "top_right": self.top_right,
            "bottom_left": self.bottom_left,
            "bottom_right": self.bottom_right,
        }

    def all_refs(self) -> list[str]:
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]





def col_letter_to_index(col: str) -> int:

    col = col.upper()
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def index_to_col_letter(idx: int) -> str:

    result = ""
    while idx >= 0:
        result = chr((idx % 26) + ord("A")) + result
        idx = idx // 26 - 1
    return result





def parse_target_cell(cell_ref: str) -> dict[str, str]:












    cell_ref = cell_ref.strip().upper()
    match = _PATRON_CELDA.match(cell_ref)
    if not match:
        raise ValueError(
            f"Formato de celda inválido: '{cell_ref}'. "
            f"Se espera una o más letras seguidas de dígitos (ej. A1, AA10)."
        )

    col_letra = match.group(1)
    fila = int(match.group(2))

    if fila < 1:
        raise ValueError(f"Número de fila inválido: {fila}. Debe ser >= 1.")

    return {
        "top_left": f"{_COL_FIJA}{_FILA_FIJA}",
        "top_right": f"{col_letra}{_FILA_FIJA}",
        "bottom_left": f"{_COL_FIJA}{fila}",
        "bottom_right": cell_ref,
    }


def build_cell_references(cell_ref: str) -> CellReferences:












    refs = parse_target_cell(cell_ref)
    return CellReferences(
        top_left=refs["top_left"],
        top_right=refs["top_right"],
        bottom_left=refs["bottom_left"],
        bottom_right=refs["bottom_right"],
        target=cell_ref.strip().upper(),
    )
````

## File: gsheets/utils/image_compositor.py
````python
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image



logger = logging.getLogger(__name__)



_BORDER_COLOR = (200, 200, 200)
_BORDER_WIDTH = 2
_BG_COLOR = (255, 255, 255)





def compose_ticket_image(
    top_left_path: str | Path,
    top_right_path: str | Path,
    bottom_left_path: str | Path,
    bottom_right_path: str | Path,
    output_path: str | Path,
    border_width: int = _BORDER_WIDTH,
    border_color: tuple[int, int, int] = _BORDER_COLOR,
    labels: dict[str, str] | None = None,
) -> str:





















    output_path = Path(output_path)


    images = {
        "top_left": _load_image(top_left_path),
        "top_right": _load_image(top_right_path),
        "bottom_left": _load_image(bottom_left_path),
        "bottom_right": _load_image(bottom_right_path),
    }




    col_left_width = max(
        images["top_left"].width, images["bottom_left"].width
    )
    col_right_width = max(
        images["top_right"].width, images["bottom_right"].width
    )
    row_top_height = max(
        images["top_left"].height, images["top_right"].height
    )
    row_bottom_height = max(
        images["bottom_left"].height, images["bottom_right"].height
    )


    total_width = col_left_width + col_right_width + border_width
    total_height = row_top_height + row_bottom_height + border_width


    canvas = Image.new("RGB", (total_width, total_height), _BG_COLOR)



    _paste_resized(canvas, images["top_left"], 0, 0, col_left_width, row_top_height)
    _paste_resized(
        canvas,
        images["top_right"],
        col_left_width + border_width,
        0,
        col_right_width,
        row_top_height,
    )


    _paste_resized(
        canvas,
        images["bottom_left"],
        0,
        row_top_height + border_width,
        col_left_width,
        row_bottom_height,
    )
    _paste_resized(
        canvas,
        images["bottom_right"],
        col_left_width + border_width,
        row_top_height + border_width,
        col_right_width,
        row_bottom_height,
    )


    if labels:
        from PIL import ImageDraw, ImageFont

        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", size=12)
        except OSError:
            font = ImageFont.load_default()

        positions = {
            "top_left": (4, 2),
            "top_right": (col_left_width + border_width + 4, 2),
            "bottom_left": (4, row_top_height + border_width + 2),
            "bottom_right": (
                col_left_width + border_width + 4,
                row_top_height + border_width + 2,
            ),
        }
        for key, pos in positions.items():
            if key in labels:
                draw.text(pos, labels[key], fill=(100, 100, 100), font=font)


    canvas.save(str(output_path), "PNG")
    logger.info("Imagen compuesta guardada en %s", output_path)

    return str(output_path.resolve())





def _load_image(path: str | Path) -> Image.Image:

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Imagen no encontrada: {path}")
    try:
        img = Image.open(path)
        img.load()
        return img
    except Exception as exc:
        raise ValueError(f"No se pudo abrir la imagen {path}: {exc}") from exc


def _paste_resized(
    canvas: Image.Image,
    img: Image.Image,
    x: int,
    y: int,
    target_w: int,
    target_h: int,
) -> None:
    """Pega una imagen en el canvas, redimensionándola si es necesario."""
    if img.width == target_w and img.height == target_h:
        canvas.paste(img, (x, y))
    else:
        resized = img.resize((target_w, target_h), Image.LANCZOS)
        canvas.paste(resized, (x, y))
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
      "doms/**",
      "doku.md",
      "data/PROPIEDADES DE CONTACTO.TXT",
      "data/PROPIEDADES DE TICKET.TXT"
    ]
  }
}
````

## File: scraping/__init__.py
````python

````

## File: scraping/sunrun_selectors.py
````python
URL_BASE_SUNRUN = "https://sunrun.my.site.com"
URL_LISTA_SUNRUN = (
    "https://sunrun.my.site.com/partners/s/fs-dispatch/FS_Dispatch__c/Default"
)



SEL_BUSQUEDA_GLOBAL = "div.forceSearchInputDesktop input[role='combobox']"



SELECTOR_NUMERO_FSD = "//slot[@name='primaryField']//lightning-formatted-text"

PATRON_CAMPO = (
    "//span[contains(@class,'test-id__field-label') "
    "and normalize-space(text())='{}']"
    "/ancestor::div[contains(@class,'label-stacked') "
    "or (contains(@class,'slds-form-element') "
    "and not(contains(@class,'slds-form-element__')))]"
    "//lightning-formatted-text"
)

SELECTOR_NOMBRE = PATRON_CAMPO.format("Customer Name")
SELECTOR_DIRECCION = PATRON_CAMPO.format("Address")
SELECTOR_TELEFONO = PATRON_CAMPO.format("Customer Phone")
SELECTOR_MOVIL = PATRON_CAMPO.format("Mobile Phone")
SELECTOR_EMAIL = PATRON_CAMPO.format("Customer Email")
SELECTOR_ESTADO = PATRON_CAMPO.format("State")
SELECTOR_COUNTY = PATRON_CAMPO.format("County")
SELECTOR_CIUDAD = PATRON_CAMPO.format("City")
SELECTOR_ZIP = PATRON_CAMPO.format("Zip Code")

SELECTOR_DISPATCH_STATE = PATRON_CAMPO.format("Dispatch State")
SELECTOR_APPOINTMENT_DATE = PATRON_CAMPO.format("Appointment Date")
SELECTOR_CASE_REASON = PATRON_CAMPO.format("Case Reason")



SELECTOR_RELATED = "//a[@role='tab' and contains(normalize-space(.),'Related')]"
SELECTOR_UPLOAD_FILES_INPUT = (
    "//input[@type='file' and contains(@class,'slds-file-selector__input')]"
)
SELECTOR_UPLOAD_FILES_BUTTON = (
    "//span[normalize-space(text())='Upload Files']/ancestor::label"
)
SELECTOR_DROP_FILES = (
    "//span[contains(normalize-space(.),'Drop Files')]"
    "/ancestor::*[contains(@class,'slds-file-selector')]"
)



SEL_MRU_DROPDOWN = "a.MRU_SCOPED"



TIMEOUT = 15
TIMEOUT_LISTA = 30
TIMEOUT_MRU = 10
PAUSA_FILTRO = 2.0
PAUSA_DETALLE = 1.5
````

## File: scraping/sunrun.py
````python
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





































































        Lógica compartida de búsqueda con la barra global de Salesforce.

        Estrategias en orden:
          1. Dropdown MRU (rápido 3s → TIMEOUT_MRU si es necesario)
          2. ENTER → página de resultados globales → clic en link del ticket

        Asume que el driver ya está en una página de Sunrun con sesión activa.












































































































        Navega al detalle del FSD desde la pagina actual.
        Despacha a _clic_desde_resultados_globales o _clic_desde_otra_pagina
        segun la URL actual.













Escenario A: pagina de resultados de busqueda global (/global-search/)."""
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



    def obtener_datos_por_fsd(self, fsd: str) -> dict:

















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

                self._log("  ✓ Ya en la página del ticket, extrayendo datos...")
                return self._extraer_detalle(fsd_numero)

            elif estado_actual == "en_resultados":

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































































































Dict con todos los campos vacíos y el error registrado."""
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
````

## File: SELECTORES_SUNRUN.HTML
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

SELECTOR_DONE = (
    "//button[contains(@class,'slds-button')]"
    "//span[contains(@class,'label') and normalize-space()='Done']"
)

SELECTOR_DONE = (
    "//button[contains(@class,'uiButton--brand')]"
    "//span[@class=' label bBody' and normalize-space()='Done']"
)
````

## File: services/driver_provider.py
````python
from __future__ import annotations

from typing import Callable

from core.browser import BrowserFactory, ErrorBrowser, puerto_activo


class DriverProvider:


    def obtener(
        self,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
    ) -> tuple:





        if usar_chrome_existente:
            if not puerto_activo():
                raise RuntimeError(
                    "No hay Chrome con depuracion en puerto 9222. "
                    "Abrelo desde el boton 'Abrir Chrome con depuracion'."
                )
            log("  -> Conectando al Chrome existente (puerto 9222)...")
            driver = BrowserFactory.conectar_existente()
            log("  v Conectado.")
            return driver, False
        else:
            log("  -> Abriendo Chrome nuevo...")
            driver = BrowserFactory.nuevo(headless=headless)
            log("  v Chrome abierto.")
            return driver, True
````

## File: test/test_fix_final.py
````python
print("Buscando candidato 'Daisy' con FSD...")
print("=" * 60)

from data.api import HubSpotAPI

api = HubSpotAPI()
candidatos = api.buscar_contactos_por_criterio("Daisy", "nombre")

if not candidatos:
    print("❌ No se encontraron candidatos")
else:
    print(f"✅ Se encontraron {len(candidatos)} candidato(s)\n")

    for i, c in enumerate(candidatos[:3]):
        print(f"Candidato {i+1}:")
        print(f"  Nombre: {c.get('nombre')}")
        print(f"  Email: {c.get('email')}")
        print(f"  FSD: {repr(c.get('fsd'))}")

        if c.get("fsd"):
            print(f"  ✅ ¡¡¡FSD ENCONTRADO!!!")
        else:
            print(f"  ⚠️  Sin FSD")
        print()

print("=" * 60)
print("FIN DEL TEST")
````

## File: tests/__init__.py
````python

````

## File: tests/conftest.py
````python
import json
import os
import pickle
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def temp_config_file(temp_dir):
    config_path = temp_dir / "config.json"
    config_path.write_text(json.dumps({}), encoding="utf-8")
    return config_path


@pytest.fixture
def temp_config_json(temp_config_file):
    return temp_config_file


@pytest.fixture
def mock_config_file(temp_dir):
    config_path = temp_dir / "mock_config.json"
    return config_path


@pytest.fixture
def mock_archivo_config(monkeypatch, mock_config_file):
    from config import configuracion

    monkeypatch.setattr(configuracion, "ARCHIVO_CONFIG", str(mock_config_file))
    configuracion._invalidar_cache_config()
    return mock_config_file


@pytest.fixture
def config_con_datos_completos(mock_archivo_config):
    from config.configuracion import guardar_config

    datos = {
        "tema": "light",
        "ultimo_monitor": 2,
        "regiones_apps": {
            "Wolkbox": {"top": 100, "left": 0, "width": 800, "height": 600},
            "B2Chat": {"top": 200, "left": 100, "width": 900, "height": 500},
        },
        "monitores_apps": {"Wolkbox": 1, "B2Chat": 2},
        "perfiles_region": {
            "Perfil A": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            },
            "Perfil B": {
                "top": 50,
                "left": 100,
                "width": 1280,
                "height": 720,
            },
        },
        "keybind": "<Control-Shift-x>",
        "headless": True,
        "chrome_existente": False,
        "destino_subida": "HUBSPOT",
        "auto_submit_nota": True,
    }
    guardar_config(datos)
    return datos


@pytest.fixture
def mock_keyring():
    with patch("config.credenciales.keyring") as mock:
        store = {}

        def set_password(app, key, value):
            store[f"{app}/{key}"] = value

        def get_password(app, key):
            return store.get(f"{app}/{key}")

        def delete_password(app, key):
            store.pop(f"{app}/{key}", None)

        mock.set_password.side_effect = set_password
        mock.get_password.side_effect = get_password
        mock.delete_password.side_effect = delete_password

        yield mock


@pytest.fixture
def mock_cookies_dir(temp_dir):
    cookies_dir = temp_dir / "cookies"
    cookies_dir.mkdir(exist_ok=True)
    with patch("config.credenciales.Path") as mock_path:

        def path_side_effect(path_str):
            if path_str.startswith("cookies/"):
                return temp_dir / path_str
            return Path(path_str)

        mock_path.side_effect = path_side_effect
        yield cookies_dir


@pytest.fixture
def mock_keyring_empty(mock_keyring):
    return mock_keyring


@pytest.fixture
def temp_plantillas_file(temp_dir):
    plantillas_path = temp_dir / "plantillas.json"
    return plantillas_path


@pytest.fixture
def mock_plantillas_path(monkeypatch, temp_plantillas_file):
    import ui.ventana_plantillas as vp

    monkeypatch.setattr(vp, "PLANTILLAS_PATH", temp_plantillas_file)
    return temp_plantillas_file


@pytest.fixture
def datos_hubspot_mock():
    return {
        "fsd": "FSD-980124",
        "ticket_id": "12345",
        "contact_id": "67890",
        "nombre": "Juan Perez",
        "id_cliente": "GZ-001",
        "direccion": "Calle 123 #45-67",
        "telefono": "787-297-9317",
        "telefono_alterno": "787-111-2222",
        "email": "juan@example.com",
        "estado": "Puerto Rico",
        "municipio": "San Juan",
        "zip": "00901",
        "nota": "Cliente VIP",
        "fuente_nombre": "HubSpot Ticket",
        "fuente_id": "ticket-12345",
        "error": None,
    }


@pytest.fixture
def datos_sunrun_mock():
    return {
        "fsd": "FSD-980124",
        "nombre": "Juan Perez Garcia",
        "id_cliente": "GZ-001",
        "direccion": "Calle 123 #45-67",
        "telefono": "+17872979317",
        "telefono_movil": "787-111-2222",
        "email": "juan@example.com",
        "estado_pr": "Puerto Rico",
        "condado": "San Juan",
        "ciudad": "San Juan",
        "codigo_postal": "00901",
        "dispatch_state": "En Progreso",
        "appointment_date": "2025-06-15",
        "case_reason": "Instalación",
        "error": None,
    }


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.get_cookies.return_value = [
        {"name": "session", "value": "abc123", "domain": ".example.com"},
        {"name": "token", "value": "xyz789", "domain": ".example.com"},
    ]
    return driver
````

## File: tests/test_apps_captura.py
````python
import pytest

from config.apps_captura import APPS_CAPTURA


class TestAppsCaptura:
    def test_estructura_es_lista(self):
        assert isinstance(APPS_CAPTURA, list)

    def test_no_vacia(self):
        assert len(APPS_CAPTURA) > 0

    def test_cada_app_tiene_nombre(self):
        for app in APPS_CAPTURA:
            assert "nombre" in app
            assert isinstance(app["nombre"], str)
            assert len(app["nombre"]) > 0

    def test_cada_app_tiene_icono(self):
        for app in APPS_CAPTURA:
            assert "icono" in app
            assert isinstance(app["icono"], str)

    def test_cada_app_tiene_region(self):
        for app in APPS_CAPTURA:
            assert "region" in app
            assert isinstance(app["region"], dict)
            for clave in ("top", "left", "width", "height"):
                assert clave in app["region"]
                assert isinstance(app["region"][clave], int)

    def test_cada_app_tiene_monitor(self):
        for app in APPS_CAPTURA:
            assert "monitor" in app
            assert isinstance(app["monitor"], int)
            assert app["monitor"] >= 1

    def test_cada_app_tiene_color(self):
        for app in APPS_CAPTURA:
            assert "color" in app
            assert isinstance(app["color"], (tuple, list))
            assert len(app["color"]) == 2
            for c in app["color"]:
                assert isinstance(c, str)
                assert c.startswith("#")

    def test_region_valores_positivos_o_cero(self):
        for app in APPS_CAPTURA:
            r = app["region"]
            assert r["top"] >= 0
            assert r["left"] >= 0
            assert r["width"] > 0
            assert r["height"] > 0

    def test_nombres_unicos(self):
        nombres = [app["nombre"] for app in APPS_CAPTURA]
        assert len(nombres) == len(set(nombres))

    def test_nombres_razonables(self):
        nombres_validos = {"Wolkbox", "B2Chat", "Correo", "Calendar", "App 5"}
        for app in APPS_CAPTURA:
            assert app["nombre"] in nombres_validos

    def test_colores_siguen_paleta(self):
        colores_validos = {
            "#1f6aa5",
            "#1a5496",
            "#2d7a3a",
            "#256630",
            "#a05a00",
            "#8a4e00",
            "#6b3fa0",
            "#5a3488",
            "#1a7a6e",
            "#146058",
        }
        for app in APPS_CAPTURA:
            for c in app["color"]:
                assert c in colores_validos, f"Color {c} no esta en la paleta definida"

    def test_formato_color_hex_valido(self):
        import re

        hex_pattern = re.compile(r"^
        for app in APPS_CAPTURA:
            for c in app["color"]:
                assert hex_pattern.match(c), f"Color {c} no es hex valido"
````

## File: tests/test_base_plugin.py
````python
import pytest
from unittest.mock import MagicMock

from core.base_plugin import (
    ContextoSubida,
    RegionCaptura,
    ResultadoSubida,
    SitioPlugin,
)


class TestRegionCaptura:
    def test_creacion_basica(self):
        r = RegionCaptura(top=100, left=200, width=800, height=600)
        assert r.top == 100
        assert r.left == 200
        assert r.width == 800
        assert r.height == 600

    def test_as_dict(self):
        r = RegionCaptura(top=10, left=20, width=30, height=40)
        d = r.as_dict()
        assert d == {"top": 10, "left": 20, "width": 30, "height": 40}

    def test_as_dict_retorna_copia_segura(self):
        r = RegionCaptura(1, 2, 3, 4)
        d = r.as_dict()
        d["top"] = 999
        assert r.top == 1

    def test_valores_cero_son_validos(self):
        r = RegionCaptura(0, 0, 0, 0)
        assert r.as_dict() == {"top": 0, "left": 0, "width": 0, "height": 0}

    def test_valores_negativos_permitidos(self):
        r = RegionCaptura(top=-1, left=-1, width=100, height=100)
        assert r.as_dict() == {"top": -1, "left": -1, "width": 100, "height": 100}


class TestResultadoSubida:
    def test_exitoso_sin_mensaje(self):
        r = ResultadoSubida(exitoso=True)
        assert r.exitoso is True
        assert r.mensaje == ""
        assert r.detalle == ""

    def test_fallido_con_mensaje(self):
        r = ResultadoSubida(exitoso=False, mensaje="Error", detalle="Timeout")
        assert r.exitoso is False
        assert r.mensaje == "Error"
        assert r.detalle == "Timeout"

    def test_mensaje_y_detalle_opcionales(self):
        r = ResultadoSubida(exitoso=True)
        assert r.mensaje == ""
        assert r.detalle == ""


class TestContextoSubida:
    def test_creacion_minima(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/test.png",
            log=print,
            driver=MagicMock(),
        )
        assert ctx.ruta_imagen == "/tmp/test.png"
        assert ctx.log is print
        assert ctx.credenciales == {}
        assert ctx.opciones == {}
        assert ctx.fsd is None

    def test_con_credenciales(self):
        creds = {"usuario": "admin", "clave": "pass"}
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            credenciales=creds,
        )
        assert ctx.credenciales == creds

    def test_con_opciones(self):
        opts = {"auto_submit_nota": True}
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            opciones=opts,
        )
        assert ctx.opciones["auto_submit_nota"] is True

    def test_con_fsd(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            fsd="FSD-123456",
        )
        assert ctx.fsd == "FSD-123456"

    def test_fsd_none_por_defecto(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
        )
        assert ctx.fsd is None

    def test_credenciales_no_se_comparten_entre_instancias(self):
        ctx1 = ContextoSubida(ruta_imagen="/tmp/a.png", log=print, driver=MagicMock())
        ctx2 = ContextoSubida(ruta_imagen="/tmp/b.png", log=print, driver=MagicMock())
        ctx1.credenciales["user"] = "x"
        assert "user" not in ctx2.credenciales

    def test_opciones_no_se_comparten_entre_instancias(self):
        ctx1 = ContextoSubida(ruta_imagen="/tmp/a.png", log=print, driver=MagicMock())
        ctx2 = ContextoSubida(ruta_imagen="/tmp/b.png", log=print, driver=MagicMock())
        ctx1.opciones["flag"] = True
        assert "flag" not in ctx2.opciones


class TestSitioPlugin:
    def test_no_se_puede_instanciar_directamente(self):
        with pytest.raises(TypeError):
            SitioPlugin()

    def test_subclase_minima_funciona(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "TEST"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.nombre == "TEST"
        assert plugin.necesita_login is True
        assert plugin.usar_pagina_actual is False
        assert plugin.dominio == ""

    def test_subclase_override_propiedades(self):
        class SinLoginPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "PUBLICO"

            @property
            def necesita_login(self):
                return False

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = SinLoginPlugin()
        assert plugin.necesita_login is False

    def test_verificar_sesion_default_true(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "T"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.verificar_sesion(MagicMock(), print) is True

    def test_hacer_login_default_false(self):
        driver = MagicMock()
        log_calls = []

        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "T"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.hacer_login(driver, {}, log_calls.append) is False
        assert len(log_calls) > 0

    def test_describir(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "HUBSPOT"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        desc = plugin.describir()
        assert "HUBSPOT" in desc
        assert "con login" in desc

    def test_describir_con_pagina_actual(self):
        class ConPaginaPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "SUNRUN"

            @property
            def usar_pagina_actual(self):
                return True

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = ConPaginaPlugin()
        desc = plugin.describir()
        assert "página actual" in desc

    def test_plugin_recibe_contexto_completo(self):
        ctx_recibido = []

        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "CAPTURE"

            def subir(self, ctx):
                ctx_recibido.append(ctx)
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        ctx = ContextoSubida(
            ruta_imagen="/tmp/img.png",
            log=print,
            driver=MagicMock(),
            credenciales={"u": "p"},
            fsd="FSD-001",
        )
        resultado = plugin.subir(ctx)
        assert resultado.exitoso is True
        assert len(ctx_recibido) == 1
        assert ctx_recibido[0].fsd == "FSD-001"
````

## File: tests/test_colors.py
````python
import pytest

from utils.colors import oscurecer


class TestOscurecer:
    def test_oscurecer_color_basico(self):
        color = "#ffffff"
        oscuro = oscurecer(color)
        assert oscuro.startswith("#")
        assert len(oscuro) == 7

    def test_oscurecer_negro_se_mantiene_negro(self):
        assert oscurecer("#000000") == "#000000"

    def test_oscurecer_con_factor(self):
        color = "#808080"
        resultado = oscurecer(color, factor=0.5)
        assert resultado == "#404040"

    def test_factor_cero_da_negro(self):
        assert oscurecer("#ff0000", factor=0.0) == "#000000"

    def test_factor_uno_da_mismo_color(self):
        assert oscurecer("#2ea043", factor=1.0) == "#2ea043"

    def test_color_de_la_app(self):
        azul_oscuro = oscurecer("#1f6aa5")
        assert azul_oscuro.startswith("#")

    def test_formato_con_y_sin_numeral(self):
        with_hash = oscurecer("#ff8040")
        assert with_hash.startswith("#")
        assert len(with_hash) == 7

    def test_error_devuelve_default(self):
        resultado = oscurecer("")
        assert resultado == "

    def test_color_invalido_devuelve_default(self):
        resultado = oscurecer("rojo")
        assert resultado == "#444444"

    def test_formato_rgb_hex_valido(self):
        for color in ["#ff0000", "#00ff00", "#0000ff", "#123456", "#abcdef"]:
            resultado = oscurecer(color, factor=0.5)
            assert resultado.startswith("#")
            assert len(resultado) == 7

    def test_oscurecer_por_defecto_factor_80(self):
        blanco = "#ffffff"
        resultado = oscurecer(blanco)
        assert resultado == "#cccccc"
````

## File: tests/test_comparador.py
````python
import pytest
from unittest.mock import patch, MagicMock

from core.comparador import (
    _comparar_nombres,
    _norm,
    _normalizar_telefono,
    _similitud,
    _vacio,
    comparar,
    comparar_campo,
    datos_hs_desde_ticket,
)


class TestNorm:
    def test_normaliza_mayusculas(self):
        assert _norm("hola mundo") == "HOLA MUNDO"

    def test_elimina_tildes(self):
        resultado = _norm("María")
        assert "I" in resultado or resultado == "MARIA"

    def test_elimina_puntuacion(self):
        assert _norm("Hola, mundo; hoy: 'bien'") == "HOLA MUNDO HOY BIEN"

    def test_vacio_devuelve_vacio(self):
        assert _norm("") == ""

    def test_no_encontrado_devuelve_vacio(self):
        assert _norm("No encontrado") == ""

    def test_no_detectado_devuelve_vacio(self):
        assert _norm("No detectado") == ""

    def test_espacios_dobles_colapsados(self):
        resultado = _norm("hola    mundo")
        assert resultado == "HOLA MUNDO"

    def test_none_devuelve_vacio(self):
        assert _norm(None) == ""


class TestVacio:
    def test_vacio_identifica_none(self):
        assert _vacio(None) is True

    def test_vacio_identifica_cadena_vacia(self):
        assert _vacio("") is True

    def test_vacio_identifica_no_encontrado(self):
        assert _vacio("No encontrado") is True

    def test_vacio_identifica_valor_real(self):
        assert _vacio("Juan Perez") is False

    def test_vacio_identifica_espacios(self):
        assert _vacio("   ") is True


class TestNormalizarTelefono:
    def test_formato_internacional(self):
        assert _normalizar_telefono("+17872979317") == "7872979317"

    def test_formato_con_parentesis(self):
        assert _normalizar_telefono("(787)297-9317") == "7872979317"

    def test_formato_con_guiones(self):
        assert _normalizar_telefono("787-297-9317") == "7872979317"

    def test_con_codigo_pais_1_guiado(self):
        assert _normalizar_telefono("1-787-297-9317") == "7872979317"

    def test_vacio_devuelve_vacio(self):
        assert _normalizar_telefono("") == ""

    def test_none_devuelve_vacio(self):
        assert _normalizar_telefono(None) == ""

    def test_solo_10_digitos_se_mantienen(self):
        assert _normalizar_telefono("7872979317") == "7872979317"

    def test_numero_11_digitos_sin_codigo_1_se_mantiene(self):
        assert _normalizar_telefono("12345678901") == "2345678901"


class TestSimilitud:
    def test_iguales_devuelve_uno(self):
        assert _similitud("Hola", "Hola") == 1.0

    def test_distintos_devuelve_menor_que_uno(self):
        assert _similitud("Hola", "Chao") < 1.0

    def test_parecidos_devuelve_alto(self):
        sim = _similitud("Juan Perez", "Juan Peres")
        assert sim > 0.7


class TestCompararNombres:
    def test_exactos_devuelve_igual(self):
        r = _comparar_nombres("Juan Perez", "Juan Perez")
        assert r["estado"] == "igual"

    def test_tokens_contenidos_devuelve_similar(self):
        r = _comparar_nombres("Juan Perez", "Juan Perez Garcia")
        assert r["estado"] in ("igual", "similar")

    def test_completamente_diferentes(self):
        r = _comparar_nombres("Juan Perez", "Ana Lopez")
        assert r["estado"] in ("diferente", "similar")

    def test_con_tildes_y_mayusculas(self):
        r = _comparar_nombres("María José", "maria jose")
        assert r["estado"] in ("igual", "similar")


class TestCompararCampo:
    def test_ambos_vacios(self):
        r = comparar_campo("Telefono", "", "")
        assert r["estado"] == "ambos_vacios"

    def test_solo_hs(self):
        r = comparar_campo("Email", "a@b.com", "")
        assert r["estado"] == "solo_hs"

    def test_solo_sunrun(self):
        r = comparar_campo("Email", "", "a@b.com")
        assert r["estado"] == "solo_sunrun"

    def test_iguales(self):
        r = comparar_campo("Direccion", "Calle 123", "Calle 123")
        assert r["estado"] == "igual"

    def test_telefonos_formato_diferente_pero_iguales(self):
        r = comparar_campo("Telefono", "787-297-9317", "+17872979317")
        assert r["estado"] == "igual"

    def test_nombre_formato_diferente_tolerante(self):
        r = comparar_campo("Nombre", "Juan Perez", "Juan Perez Garcia")
        assert r["estado"] in ("igual", "similar")

    def test_campo_desconocido_comparacion_generica(self):
        r = comparar_campo("Ciudad", "San Juan", "San Juan")
        assert r["estado"] == "igual"

    def test_no_encontrado_se_trata_como_vacio(self):
        r = comparar_campo("Direccion", "No encontrado", "Calle 123")
        assert r["estado"] == "solo_sunrun"

    def test_resultado_tiene_campo(self):
        r = comparar_campo("Ciudad", "A", "B")
        assert r["campo"] == "Ciudad"

    def test_resultado_tiene_similitud(self):
        r = comparar_campo("Nombre", "Juan", "Juan")
        assert "similitud" in r
        assert 0.0 <= r["similitud"] <= 1.0

    def test_resultado_tiene_nota(self):
        r = comparar_campo("Email", "a@b", "a@b")
        assert "nota" in r
        assert r["nota"]

    def test_nombre_similar_pero_no_igual(self):
        r = comparar_campo("Nombre", "Juan Perez", "Juan Peres")
        assert r["estado"] in ("similar", "diferente")

    def test_solo_hs_cuando_hs_vacio(self):
        r = comparar_campo("Direccion", "Calle Falsa 123", "")
        assert r["estado"] == "solo_hs"
        assert r["valor_sr"] == "—"


class TestComparar:


    def test_comparacion_completa_sin_errores(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        assert "campos" in resultado
        assert "resumen" in resultado
        assert "fsd" in resultado
        assert not resultado["tiene_error"]

    def test_comparacion_con_error_en_hs(self):
        resultado = comparar(
            {"error": "Timeout API"}, {"nombre": "Test", "error": None}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 1

    def test_comparacion_con_error_en_sunrun(self):
        resultado = comparar(
            {"nombre": "Test", "error": None}, {"error": "Sunrun no responde"}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 1

    def test_comparacion_con_errores_en_ambos(self):
        resultado = comparar(
            {"error": "Error A"}, {"error": "Error B"}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 2

    def test_fsd_desde_hubspot(self):
        resultado = comparar(
            {"fsd": "FSD-999", "nombre": "X"},
            {"nombre": "X"},
        )
        assert resultado["fsd"] == "FSD-999"

    def test_fsd_desde_sunrun_cuando_hs_no_tiene(self):
        resultado = comparar(
            {"nombre": "X"},
            {"fsd": "FSD-888", "nombre": "X"},
        )
        assert resultado["fsd"] == "FSD-888"

    def test_fsd_desconocido_cuando_ninguno_tiene(self):
        resultado = comparar({}, {})
        assert resultado["fsd"] == "desconocido"

    def test_campos_comparables_en_resultado(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        nombres_campo = {c["campo"] for c in resultado["campos"]}
        assert "Nombre" in nombres_campo
        assert "Direccion" in nombres_campo
        assert "Telefono" in nombres_campo
        assert "Email" in nombres_campo

    def test_campos_solo_sunrun_incluidos(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        nombres_campo = {c["campo"] for c in resultado["campos"]}
        assert "Municipio" in nombres_campo

    def test_resumen_suma_consistente(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        r = resultado["resumen"]
        total_resumen = sum(r.values())
        assert total_resumen == len(resultado["campos"])

    def test_resumen_tiene_todas_las_claves(self):
        resultado = comparar({"nombre": "A"}, {"nombre": "A"})
        for clave in ("igual", "similar", "diferente", "solo_hs", "solo_sunrun", "ambos_vacios"):
            assert clave in resultado["resumen"]

    def test_datos_identicos_todo_igual(self):
        datos = {
            "nombre": "Juan Perez",
            "direccion": "Calle 123",
            "telefono": "7872979317",
            "email": "juan@test.com",
        }
        resultado = comparar(datos, datos)
        for campo in resultado["campos"]:
            if campo["campo"] != "Municipio":
                assert campo["estado"] in ("igual", "ambos_vacios"), f"Campo {campo['campo']} deberia ser igual, fue {campo['estado']}"

    def test_campos_completamente_diferentes(self):
        hs = {
            "nombre": "Juan Perez",
            "direccion": "Calle A",
            "telefono": "7871111111",
            "email": "juan@test.com",
        }
        sr = {
            "nombre": "Ana Lopez",
            "direccion": "Calle B",
            "telefono": "7872222222",
            "email": "ana@test.com",
        }
        resultado = comparar(hs, sr)
        estados = {c["estado"] for c in resultado["campos"]}
        assert "diferente" in estados

    def test_campo_parcial_solo_hs(self):
        hs = {"nombre": "Juan", "direccion": "Calle 123", "telefono": "7871111111", "email": "juan@test.com"}
        sr = {"nombre": "Juan"}
        resultado = comparar(hs, sr)
        estados = {c["estado"] for c in resultado["campos"]}
        assert "solo_hs" in estados


class TestDatosHsDesdeTicket:
    def test_campos_completos(self):
        ticket = {
            "fsd": "FSD-001",
            "ticket_id": "T1",
            "contact_id": "C1",
            "nombre": "Juan",
            "id_cliente": "GZ-1",
            "direccion": "Calle 1",
            "telefono": "123",
            "telefono_alterno": "456",
            "email": "j@j.com",
            "estado": "PR",
            "municipio": "SJ",
            "zip": "00901",
            "nota": "VIP",
            "fuente_nombre": "Ticket",
            "fuente_id": "T1",
            "error": None,
        }
        resultado = datos_hs_desde_ticket(ticket)
        assert resultado["fsd"] == "FSD-001"
        assert resultado["nombre"] == "Juan"
        assert resultado["fuente"] == "HubSpot"
        assert resultado["error"] is None

    def test_campos_faltantes_se_completan(self):
        ticket = {"fsd": "FSD-001", "nombre": "Juan"}
        resultado = datos_hs_desde_ticket(ticket)
        assert resultado["fsd"] == "FSD-001"
        assert resultado["telefono"] == ""

    def test_ticket_vacio(self):
        resultado = datos_hs_desde_ticket({})
        assert resultado["fuente"] == "HubSpot"
        assert resultado["fsd"] == ""

    def test_error_propagado(self):
        resultado = datos_hs_desde_ticket({"error": "Fallo"})
        assert resultado["error"] == "Fallo"
        assert resultado["fuente"] == "HubSpot"


class TestCompararCampoTelefono:
    def test_telefono_igual_normalizado(self):
        r = comparar_campo("Telefono", "(787) 297-9317", "+17872979317")
        assert r["estado"] == "igual"

    def test_telefono_alterno_igual_normalizado(self):
        r = comparar_campo("Telefono Alterno", "1-787-111-2222", "7871112222")
        assert r["estado"] == "igual"

    def test_telefono_diferente(self):
        r = comparar_campo("Telefono", "7871112222", "7873334444")
        assert r["estado"] == "diferente"

    def test_telefono_solo_hs(self):
        r = comparar_campo("Telefono", "7871112222", "")
        assert r["estado"] == "solo_hs"

    def test_telefono_vacio_ambos(self):
        r = comparar_campo("Telefono", "", "")
        assert r["estado"] == "ambos_vacios"
````

## File: tests/test_configuracion.py
````python
import json
import pytest
from unittest.mock import patch

from config.configuracion import (
    ARCHIVO_CONFIG,
    AUTO_SUBMIT_DEFAULT,
    CLAVE_AUTO_SUBMIT,
    CLAVE_CHROME_EXISTENTE,
    CLAVE_DESTINO_SUBIDA,
    CLAVE_HEADLESS,
    CLAVE_PERFILES,
    CHROME_EXISTENTE_DEFAULT,
    CHROME_PATHS,
    CHROME_USER_DATA,
    DESTINO_SUBIDA_DEFAULT,
    HEADLESS_DEFAULT,
    KEYRING_APP,
    PERFIL_POR_DEFECTO,
    PUERTO_DEBUG,
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_auto_submit,
    cargar_chrome_existente,
    cargar_config,
    cargar_destino_subida,
    cargar_headless,
    cargar_perfiles,
    guardar_auto_submit,
    guardar_chrome_existente,
    guardar_config,
    guardar_destino_subida,
    guardar_headless,
    guardar_perfiles,
)


class TestConstantes:


    def test_tema_apariencia_es_dark(self):
        assert TEMA_APARIENCIA == "dark"

    def test_tema_color_es_blue(self):
        assert TEMA_COLOR == "blue"

    def test_keyring_app_definido(self):
        assert KEYRING_APP == "AutoCapturaApp"

    def test_puerto_debug_es_9222(self):
        assert PUERTO_DEBUG == 9222

    def test_chrome_user_data_definido(self):
        assert "chrome_sesion_ssauto" in CHROME_USER_DATA

    def test_chrome_paths_es_lista_no_vacia(self):
        assert isinstance(CHROME_PATHS, list)
        assert len(CHROME_PATHS) >= 3

    def test_archivo_config_termina_en_config_json(self):
        assert ARCHIVO_CONFIG.endswith("config.json")

    def test_perfil_por_defecto_tiene_cuatro_claves(self):
        for clave in ("top", "left", "width", "height"):
            assert clave in PERFIL_POR_DEFECTO

    def test_claves_esperadas_definidas(self):
        assert CLAVE_AUTO_SUBMIT == "auto_submit_nota"
        assert CLAVE_HEADLESS == "headless"
        assert CLAVE_CHROME_EXISTENTE == "chrome_existente"
        assert CLAVE_DESTINO_SUBIDA == "destino_subida"
        assert CLAVE_PERFILES == "perfiles_region"

    def test_defaults_coherentes(self):
        assert AUTO_SUBMIT_DEFAULT is True
        assert HEADLESS_DEFAULT is False
        assert CHROME_EXISTENTE_DEFAULT is True
        assert DESTINO_SUBIDA_DEFAULT == "AMBOS"


class TestCargarConfig:


    def test_archivo_inexistente_devuelve_dict_vacio(self, mock_archivo_config):
        if mock_archivo_config.exists():
            mock_archivo_config.unlink()
        resultado = cargar_config()
        assert resultado == {}
        assert isinstance(resultado, dict)

    def test_archivo_vacio_devuelve_dict_vacio(self, mock_archivo_config):
        resultado = cargar_config()
        assert resultado == {}

    def test_carga_datos_validos(self, config_con_datos_completos):
        resultado = cargar_config()
        assert resultado["tema"] == "light"
        assert resultado["ultimo_monitor"] == 2
        assert resultado["headless"] is True
        assert resultado["chrome_existente"] is False

    def test_archivo_corrupto_devuelve_dict_vacio(self, mock_archivo_config):
        mock_archivo_config.write_text("esto no es json {{", encoding="utf-8")
        resultado = cargar_config()
        assert resultado == {}

    def test_carga_dict_vacio_no_tira_excepcion(self, mock_archivo_config):
        mock_archivo_config.write_text(json.dumps([]), encoding="utf-8")
        resultado = cargar_config()
        assert isinstance(resultado, list) or isinstance(resultado, dict)


class TestGuardarConfig:


    def test_guarda_y_recupera_datos_simples(self, mock_archivo_config):
        datos = {"tema": "dark", "keybind": "<Control-p>"}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["tema"] == "dark"
        assert cargado["keybind"] == "<Control-p>"

    def test_guarda_y_recupera_booleanos(self, mock_archivo_config):
        datos = {"headless": True, "chrome_existente": False}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["headless"] is True
        assert cargado["chrome_existente"] is False

    def test_guarda_y_recupera_enteros(self, mock_archivo_config):
        datos = {"ultimo_monitor": 3}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["ultimo_monitor"] == 3

    def test_guarda_y_recupera_anidados(self, mock_archivo_config):
        datos = {
            "regiones_apps": {
                "Wolkbox": {"top": 100, "left": 0, "width": 800, "height": 600}
            }
        }
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["regiones_apps"]["Wolkbox"]["width"] == 800

    def test_guarda_con_indentacion_legible(self, mock_archivo_config):
        datos = {"tema": "light"}
        guardar_config(datos)
        contenido = mock_archivo_config.read_text(encoding="utf-8")
        assert "  " in contenido
        assert "\n" in contenido

    def test_guarda_multiples_veces_no_corrompe(self, mock_archivo_config):
        guardar_config({"a": 1})
        guardar_config({"b": 2})
        cargado = cargar_config()
        assert cargado["b"] == 2

    def test_guarda_en_directorio_que_no_existe(self, temp_dir):
        from config import configuracion

        nuevo = temp_dir / "sub" / "config.json"
        with patch("config.configuracion.ARCHIVO_CONFIG", str(nuevo)):
            guardar_config({"ok": True})
            assert nuevo.exists()
            assert json.loads(nuevo.read_text()) == {"ok": True}

    def test_guarda_unicode_sin_problemas(self, mock_archivo_config):
        guardar_config({"nombre": "Canción"})
        cargado = cargar_config()
        assert cargado["nombre"] == "Canción"


class TestAutoSubmit:


    def test_cargar_default(self, mock_archivo_config):
        assert cargar_auto_submit() is True

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_auto_submit(True)
        assert cargar_auto_submit() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_auto_submit(False)
        assert cargar_auto_submit() is False

    def test_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"headless": True})
        guardar_auto_submit(False)
        config = cargar_config()
        assert config["headless"] is True
        assert config["auto_submit_nota"] is False


class TestHeadless:


    def test_cargar_default(self, mock_archivo_config):
        assert cargar_headless() is False

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_headless(True)
        assert cargar_headless() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_headless(True)
        guardar_headless(False)
        assert cargar_headless() is False

    def test_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"auto_submit_nota": True, "tema": "dark"})
        guardar_headless(True)
        config = cargar_config()
        assert config["auto_submit_nota"] is True
        assert config["tema"] == "dark"


class TestChromeExistente:


    def test_cargar_default(self, mock_archivo_config):
        assert cargar_chrome_existente() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_chrome_existente(False)
        assert cargar_chrome_existente() is False

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_chrome_existente(True)
        assert cargar_chrome_existente() is True


class TestDestinoSubida:


    def test_cargar_default(self, mock_archivo_config):
        assert cargar_destino_subida() == "AMBOS"

    def test_guardar_y_cargar_hubspot(self, mock_archivo_config):
        guardar_destino_subida("HUBSPOT")
        assert cargar_destino_subida() == "HUBSPOT"

    def test_guardar_y_cargar_sunrun(self, mock_archivo_config):
        guardar_destino_subida("SUNRUN")
        assert cargar_destino_subida() == "SUNRUN"

    def test_guardar_y_cargar_ambos(self, mock_archivo_config):
        guardar_destino_subida("HUBSPOT")
        guardar_destino_subida("AMBOS")
        assert cargar_destino_subida() == "AMBOS"


class TestPerfiles:


    def test_cargar_sin_perfiles_devuelve_dict_vacio(self, mock_archivo_config):
        assert cargar_perfiles() == {}

    def test_guardar_y_cargar_un_perfil(self, mock_archivo_config):
        perfil = {
            "Monitor 1": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            }
        }
        guardar_perfiles(perfil)
        cargado = cargar_perfiles()
        assert "Monitor 1" in cargado
        assert cargado["Monitor 1"]["width"] == 1920

    def test_guardar_y_cargar_multiples_perfiles(self, mock_archivo_config):
        perfiles = {
            "Perfil A": {"top": 10, "left": 20, "width": 800, "height": 600},
            "Perfil B": {"top": 30, "left": 40, "width": 1024, "height": 768},
        }
        guardar_perfiles(perfiles)
        cargado = cargar_perfiles()
        assert len(cargado) == 2
        assert "Perfil A" in cargado
        assert "Perfil B" in cargado

    def test_guardar_perfiles_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"tema": "dark", "headless": True})
        guardar_perfiles({"P1": {"top": 1, "left": 2, "width": 3, "height": 4}})
        config = cargar_config()
        assert config["tema"] == "dark"
        assert config["headless"] is True
        assert "P1" in config["perfiles_region"]

    def test_guardar_perfiles_sin_monitor_index(self, mock_archivo_config):
        guardar_perfiles({"P1": {"top": 1, "left": 2, "width": 3, "height": 4}})
        cargado = cargar_perfiles()
        assert "monitor_index" not in cargado["P1"]

    def test_eliminar_perfil_via_guardar(self, mock_archivo_config):
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}, "B": {"top": 5, "left": 6, "width": 7, "height": 8}})
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}})
        cargado = cargar_perfiles()
        assert "A" in cargado
        assert "B" not in cargado

    def test_vaciar_perfiles(self, mock_archivo_config):
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}})
        guardar_perfiles({})
        assert cargar_perfiles() == {}


class TestTema:


    def test_tema_default_cuando_no_existe(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("tema", "dark") == "dark"

    def test_tema_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"tema": "light"})
        config = cargar_config()
        assert config["tema"] == "light"

    def test_tema_cambia_entre_dark_y_light(self, mock_archivo_config):
        guardar_config({"tema": "light"})
        assert cargar_config()["tema"] == "light"
        guardar_config({"tema": "dark"})
        assert cargar_config()["tema"] == "dark"


class TestUltimoMonitor:


    def test_default_cuando_no_existe(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("ultimo_monitor", 1) == 1

    def test_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"ultimo_monitor": 2})
        assert cargar_config()["ultimo_monitor"] == 2

    def test_valor_cero(self, mock_archivo_config):
        guardar_config({"ultimo_monitor": 0})
        assert cargar_config()["ultimo_monitor"] == 0


class TestKeybind:


    def test_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"keybind": "<Control-p>"})
        assert cargar_config()["keybind"] == "<Control-p>"

    def test_combinacion_compleja(self, mock_archivo_config):
        guardar_config({"keybind": "<Control-Shift-Return>"})
        assert cargar_config()["keybind"] == "<Control-Shift-Return>"


class TestRegionesApps:


    def test_vacio_por_defecto(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("regiones_apps", {}) == {}

    def test_guarda_y_recupera_region(self, mock_archivo_config):
        guardar_config(
            {
                "regiones_apps": {
                    "Wolkbox": {"top": 50, "left": 100, "width": 600, "height": 400}
                }
            }
        )
        config = cargar_config()
        assert config["regiones_apps"]["Wolkbox"]["top"] == 50
        assert config["regiones_apps"]["Wolkbox"]["width"] == 600


class TestMonitoresApps:


    def test_vacio_por_defecto(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("monitores_apps", {}) == {}

    def test_guarda_y_recupera(self, mock_archivo_config):
        guardar_config({"monitores_apps": {"Wolkbox": 1, "B2Chat": 2}})
        config = cargar_config()
        assert config["monitores_apps"]["Wolkbox"] == 1
        assert config["monitores_apps"]["B2Chat"] == 2
````

## File: tests/test_cookies.py
````python
import pickle
import pytest
from unittest.mock import MagicMock, patch

from config.credenciales import guardar_cookies, cargar_cookies


@pytest.fixture
def temp_cwd(temp_dir, monkeypatch):

    monkeypatch.chdir(str(temp_dir))
    return temp_dir


class TestGuardarCookies:
    def test_guarda_cookies_en_directorio_cookies(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "HUBSPOT", carpeta=carpeta)
        archivo = carpeta / "HUBSPOT.pkl"
        assert archivo.exists()
        cookies = pickle.loads(archivo.read_bytes())
        assert len(cookies) == 2
        assert cookies[0]["name"] == "session"
        assert cookies[1]["name"] == "token"

    def test_reemplaza_espacios_por_guiones(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "Mi Sitio", carpeta=carpeta)
        archivo = carpeta / "Mi_Sitio.pkl"
        assert archivo.exists()

    def test_crea_directorio_cookies_si_no_existe(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "TEST", carpeta=carpeta)
        assert carpeta.is_dir()

    def test_guarda_cookies_vacio(self, temp_cwd):
        driver = MagicMock()
        driver.get_cookies.return_value = []
        carpeta = temp_cwd / "cookies"
        guardar_cookies(driver, "VACIO", carpeta=carpeta)
        archivo = carpeta / "VACIO.pkl"
        cookies = pickle.loads(archivo.read_bytes())
        assert cookies == []


class TestCargarCookies:
    def test_archivo_no_existe_devuelve_false(self, temp_cwd):
        driver = MagicMock()
        sitio = {"nombre": "NOEXISTE"}
        carpeta = temp_cwd / "cookies"
        resultado = cargar_cookies(driver, sitio, "https://example.com", carpeta=carpeta)
        assert resultado is False

    def test_carga_cookies_exitosamente(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        carpeta.mkdir(exist_ok=True)
        cookies_guardadas = [
            {"name": "session", "value": "abc123", "domain": "example.com"},
            {"name": "token", "value": "xyz", "domain": "example.com"},
        ]
        (carpeta / "HUBSPOT.pkl").write_bytes(
            pickle.dumps(cookies_guardadas)
        )

        driver = MagicMock()
        sitio = {"nombre": "HUBSPOT"}

        resultado = cargar_cookies(driver, sitio, "https://app.hubspot.com", carpeta=carpeta)
        assert resultado is True
        driver.get.assert_called_once_with("https://app.hubspot.com")
        assert driver.add_cookie.call_count == 2

    def test_carga_cookies_con_errores_individuales_no_detiene(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        carpeta.mkdir(exist_ok=True)
        cookies_guardadas = [
            {"name": "ok", "value": "v1"},
            {"name": "bad", "value": "v2"},
        ]
        (carpeta / "TEST.pkl").write_bytes(
            pickle.dumps(cookies_guardadas)
        )

        driver = MagicMock()
        driver.add_cookie.side_effect = [None, Exception("cookie rechazada")]

        sitio = {"nombre": "TEST"}

        resultado = cargar_cookies(driver, sitio, "https://example.com", carpeta=carpeta)
        assert resultado is True


class TestRoundTripCookies:


    def test_guardar_y_cargar_cookies(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        driver_save = MagicMock()
        cookies_originales = [
            {"name": "s", "value": "abc", "domain": ".site.com"},
        ]
        driver_save.get_cookies.return_value = cookies_originales

        guardar_cookies(driver_save, "TEST", carpeta=carpeta)

        driver_load = MagicMock()
        sitio = {"nombre": "TEST"}
        resultado = cargar_cookies(driver_load, sitio, "https://site.com", carpeta=carpeta)

        assert resultado is True
        driver_load.get.assert_called_once()
        driver_load.add_cookie.assert_called()
````

## File: tests/test_credenciales.py
````python
import pytest

from config.credenciales import (
    borrar_credenciales,
    cargar_credenciales,
    guardar_credenciales,
)


class TestGuardarCredenciales:
    def test_guardar_y_cargar_credenciales(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "secret123")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "admin"
        assert clave == "secret123"

    def test_guardar_vacio_funciona(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "", "")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == ""
        assert clave == ""

    def test_guardar_con_caracteres_especiales(self, mock_keyring):
        guardar_credenciales("SUNRUN", "user@domain", "p@$$w0rd!#")
        usuario, clave = cargar_credenciales("SUNRUN")
        assert usuario == "user@domain"
        assert clave == "p@$$w0rd!#"


class TestCargarCredenciales:
    def test_credenciales_inexistentes_devuelve_vacios(self, mock_keyring):
        usuario, clave = cargar_credenciales("NOEXISTE")
        assert usuario == ""
        assert clave == ""

    def test_credenciales_inexistentes_no_son_none(self, mock_keyring):
        usuario, clave = cargar_credenciales("NOEXISTE")
        assert usuario is not None
        assert clave is not None

    def test_credenciales_parciales(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "user", "")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "user"
        assert clave == ""


class TestBorrarCredenciales:
    def test_borrar_credenciales_existentes(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "pass")
        borrar_credenciales("HUBSPOT")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == ""
        assert clave == ""

    def test_borrar_credenciales_inexistentes_no_falla(self, mock_keyring):
        borrar_credenciales("NOEXISTE")

    def test_borrar_y_volver_a_guardar(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "user1", "pass1")
        borrar_credenciales("HUBSPOT")
        guardar_credenciales("HUBSPOT", "user2", "pass2")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "user2"
        assert clave == "pass2"


class TestMultiplesSitios:
    def test_sitios_independientes(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "hs_user", "hs_pass")
        guardar_credenciales("SUNRUN", "sr_user", "sr_pass")

        u1, c1 = cargar_credenciales("HUBSPOT")
        u2, c2 = cargar_credenciales("SUNRUN")

        assert u1 == "hs_user"
        assert c1 == "hs_pass"
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

    def test_borrar_un_sitio_no_afecta_otro(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "hs", "p1")
        guardar_credenciales("SUNRUN", "sr", "p2")
        borrar_credenciales("HUBSPOT")
        u, c = cargar_credenciales("SUNRUN")
        assert u == "sr"
        assert c == "p2"


class TestRoundTripCredenciales:


    def test_guardar_cargar_borrar_cargar(self, mock_keyring):
        guardar_credenciales("SITIO", "u", "p")
        assert cargar_credenciales("SITIO") == ("u", "p")
        borrar_credenciales("SITIO")
        assert cargar_credenciales("SITIO") == ("", "")

    def test_sobreescribir_credenciales(self, mock_keyring):
        guardar_credenciales("SITIO", "old_user", "old_pass")
        guardar_credenciales("SITIO", "new_user", "new_pass")
        assert cargar_credenciales("SITIO") == ("new_user", "new_pass")

    def test_guardar_credenciales_usa_keyring_app_correcto(self, mock_keyring):
        guardar_credenciales("X", "u", "p")
        mock_keyring.set_password.assert_any_call("AutoCapturaApp", "X_usuario", "u")
        mock_keyring.set_password.assert_any_call("AutoCapturaApp", "X_clave", "p")
````

## File: tests/test_fsd.py
````python
import pytest

from utils.fsd import solo_digitos, fsd_display, normalizar_fsd


class TestSoloDigitos:
    def test_solo_digitos_formato_estandar(self):
        assert solo_digitos("FSD-1172172") == "1172172"

    def test_solo_digitos_sin_guion(self):
        assert solo_digitos("FSD1172172") == "1172172"

    def test_solo_digitos_minusculas(self):
        assert solo_digitos("fsd 1172172") == "1172172"

    def test_solo_digitos_solo_numero(self):
        assert solo_digitos("1172172") == "1172172"

    def test_solo_digitos_vacio(self):
        assert solo_digitos("") == ""

    def test_solo_digitos_sin_digitos(self):
        assert solo_digitos("FSD-ABCDEF") == ""

    def test_solo_digitos_con_espacios(self):
        assert solo_digitos("  FSD - 980124  ") == "980124"

    def test_solo_digitos_con_caracteres_especiales(self):
        assert solo_digitos("FSD#980124!") == "980124"


class TestFsdDisplay:
    def test_formato_estandar(self):
        assert fsd_display("1172172") == "FSD-1172172"

    def test_con_ceros(self):
        assert fsd_display("000123") == "FSD-000123"

    def test_largo(self):
        resultado = fsd_display("9999999")
        assert resultado.startswith("FSD-")
        assert "9999999" in resultado


class TestNormalizarFsd:
    def test_none_devuelve_none(self):
        assert normalizar_fsd(None) is None

    def test_vacio_devuelve_none(self):
        assert normalizar_fsd("") is None

    def test_solo_espacios_devuelve_none(self):
        assert normalizar_fsd("   ") is None

    def test_no_string_devuelve_none(self):
        assert normalizar_fsd(12345) is None

    def test_formato_completo_se_mantiene(self):
        assert normalizar_fsd("FSD-980124") == "FSD-980124"

    def test_solo_digitos_agrega_fsd(self):
        assert normalizar_fsd("980124") == "FSD-980124"

    def test_minusculas_convierte_a_mayusculas(self):
        assert normalizar_fsd("fsd-980124") == "FSD-980124"

    def test_solo_digitos_con_espacio_medio(self):
        resultado = normalizar_fsd("fsd 980124")
        assert resultado is not None

    def test_con_espacios_alrededor(self):
        assert normalizar_fsd("  980124  ") == "FSD-980124"

    def test_texto_no_fsd_se_mantiene(self):
        assert normalizar_fsd("HOLA") == "HOLA"

    def test_fsd_corto(self):
        resultado = normalizar_fsd("123")
        assert resultado == "FSD-123"

    def test_solo_caracteres_no_numericos_no_agrega_fsd(self):
        assert normalizar_fsd("ABC-DEF") == "ABC-DEF"

    def test_con_digitos_y_guiones(self):
        assert normalizar_fsd("980-124") == "FSD-980-124"


class TestRoundTripFsd:


    def test_solo_digitos_luego_fsd_display(self):
        numero = solo_digitos("FSD-1172172")
        display = fsd_display(numero)
        assert display == "FSD-1172172"

    def test_normalizar_luego_extraer_digitos(self):
        normalizado = normalizar_fsd("fsd 980124")
        digitos = solo_digitos(normalizado)
        assert digitos == "980124"

    def test_caso_real_completo(self):
        for entrada in [
            "FSD-980124",
            "fsd-980124",
            "980124",
            "fsd 980124",
            "FSD980124",
        ]:
            normalizado = normalizar_fsd(entrada)
            if normalizado:
                digitos = solo_digitos(normalizado)
                assert digitos == "980124", f"Fallo con entrada: {entrada}"
````

## File: tests/test_integration.py
````python
import json
import os
import pickle
import sys
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from config.configuracion import (
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
    cargar_auto_submit,
    guardar_auto_submit,
    cargar_headless,
    guardar_headless,
    cargar_chrome_existente,
    guardar_chrome_existente,
    cargar_destino_subida,
    guardar_destino_subida,
)
from config.credenciales import (
    guardar_credenciales,
    cargar_credenciales,
    borrar_credenciales,
)


class TestConfigFullRoundTrip:


    TODAS_LAS_CLAVES = {
        "tema": "light",
        "ultimo_monitor": 2,
        "regiones_apps": {
            "Wolkbox": {"top": 10, "left": 20, "width": 800, "height": 600},
        },
        "monitores_apps": {"Wolkbox": 1},
        "perfiles_region": {
            "Perfil1": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            },
        },
        "keybind": "<Control-Shift-p>",
        "headless": True,
        "chrome_existente": False,
        "destino_subida": "HUBSPOT",
        "auto_submit_nota": True,
    }

    def test_round_trip_todas_las_claves(self, mock_archivo_config):
        guardar_config(self.TODAS_LAS_CLAVES)
        cargado = cargar_config()

        for clave, valor in self.TODAS_LAS_CLAVES.items():
            assert clave in cargado, f"Falta clave '{clave}' en config cargada"
            assert cargado[clave] == valor, (
                f"Clave '{clave}': esperado {valor}, obtenido {cargado[clave]}"
            )

    def test_reinicio_simulado(self, mock_archivo_config):
        """Simula cerrar y reabrir la app: guarda, limpia cache, recarga."""
        guardar_config(self.TODAS_LAS_CLAVES)

        import config.configuracion as cfg

        cargado1 = cargar_config()
        assert cargado1["tema"] == "light"

        mock_archivo_config.write_text(json.dumps(self.TODAS_LAS_CLAVES), encoding="utf-8")
        cargado2 = cargar_config()
        assert cargado2 == cargado1

    def test_config_vacia_se_completa_con_defaults(self, mock_archivo_config):
        guardar_config({})
        cargado = cargar_config()
        assert cargado == {}
        assert cargar_auto_submit() is True
        assert cargar_headless() is False
        assert cargar_chrome_existente() is True
        assert cargar_destino_subida() == "AMBOS"

    def test_config_parcial_no_sobreescribe_faltantes(self, mock_archivo_config):
        guardar_config({"tema": "dark"})
        config = cargar_config()
        assert config["tema"] == "dark"
        assert "headless" not in config
        assert cargar_headless() is False

    def test_cambios_progresivos_no_corrompen(self, mock_archivo_config):
        guardar_config({"tema": "dark"})
        guardar_headless(True)
        guardar_auto_submit(False)
        guardar_chrome_existente(False)
        guardar_destino_subida("SUNRUN")

        assert cargar_config()["tema"] == "dark"
        assert cargar_headless() is True
        assert cargar_auto_submit() is False
        assert cargar_chrome_existente() is False
        assert cargar_destino_subida() == "SUNRUN"


class TestPerfilesRoundTrip:


    def test_crear_cargar_modificar_eliminar_perfil(self, mock_archivo_config):
        perfiles = {
            "Monitor Principal": {
                "top": 0, "left": 0, "width": 1920, "height": 1080,
                "monitor_index": 1,
            },
        }
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert "Monitor Principal" in cargados
        assert cargados["Monitor Principal"]["width"] == 1920

        perfiles["Monitor Secundario"] = {
            "top": 0, "left": 1920, "width": 1280, "height": 720,
            "monitor_index": 2,
        }
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert len(cargados) == 2

        perfiles["Monitor Principal"]["height"] = 1200
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert cargados["Monitor Principal"]["height"] == 1200

        del perfiles["Monitor Principal"]
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert "Monitor Principal" not in cargados
        assert "Monitor Secundario" in cargados

    def test_nombre_con_caracteres_especiales(self, mock_archivo_config):
        guardar_perfiles({"Español/测试": {"top": 1, "left": 2, "width": 3, "height": 4}})
        assert "Español/测试" in cargar_perfiles()


class TestCredencialesCookiesIntegration:


    def test_credenciales_persisten_entre_llamadas(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "secret123")
        guardar_credenciales("SUNRUN", "sr_user", "sr_pass")

        u1, c1 = cargar_credenciales("HUBSPOT")
        u2, c2 = cargar_credenciales("SUNRUN")

        assert u1 == "admin"
        assert c1 == "secret123"
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

        borrar_credenciales("HUBSPOT")
        u1, c1 = cargar_credenciales("HUBSPOT")
        assert u1 == ""
        assert c1 == ""

        u2, c2 = cargar_credenciales("SUNRUN")
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

    def test_cookies_persisten_y_se_recuperan(self, temp_dir):
        cookies_dir = temp_dir / "cookies"
        cookies_dir.mkdir(exist_ok=True)

        cookies = [
            {"name": "session", "value": "abc", "domain": "test.com"},
            {"name": "lang", "value": "es", "domain": "test.com"},
        ]
        ruta = cookies_dir / "HUBSPOT.pkl"
        ruta.write_bytes(pickle.dumps(cookies))

        cargadas = pickle.loads(ruta.read_bytes())
        assert len(cargadas) == 2
        assert cargadas[0]["name"] == "session"
        assert cargadas[1]["value"] == "es"


class TestTemplateIntegration:


    def test_templates_survive_multiple_writes(self, mock_plantillas_path):
        from ui.ventana_plantillas import _cargar_plantillas, _guardar_plantillas

        t = _cargar_plantillas()
        original_len = len(t)

        for i in range(5):
            t.append({"titulo": f"Test {i}", "categoria": "General", "texto": f"Body {i}"})
            _guardar_plantillas(t)
            cargadas = _cargar_plantillas()
            assert len(cargadas) == original_len + i + 1

    def test_templates_no_se_corrompen_con_edicion(self, mock_plantillas_path):
        from ui.ventana_plantillas import _cargar_plantillas, _guardar_plantillas

        t = _cargar_plantillas()
        t[0]["texto"] = "EDITADO"
        _guardar_plantillas(t)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["texto"] == "EDITADO"

        t2 = _cargar_plantillas()
        t2[0]["categoria"] = "Sunrun"
        _guardar_plantillas(t2)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["categoria"] == "Sunrun"


class TestUIConfigAudit:







    UI_CONFIG_MAPPING = {
        "Tema (Oscuro/Claro)": "tema",
        "Monitor (último)": "ultimo_monitor",
        "Headless switch": "headless",
        "Chrome existente switch": "chrome_existente",
        "Auto-submit nota switch": "auto_submit_nota",
        "Destino subida": "destino_subida",
        "Keybind": "keybind",
        "Perfiles de region": "perfiles_region",
        "Regiones apps": "regiones_apps",
        "Monitores apps": "monitores_apps",
    }

    def test_todas_las_claves_ui_tienen_persistencia(self, mock_archivo_config):

        datos = {
            "tema": "dark",
            "ultimo_monitor": 1,
            "headless": False,
            "chrome_existente": True,
            "auto_submit_nota": False,
            "destino_subida": "SUNRUN",
            "keybind": "<Control-Return>",
            "perfiles_region": {"P1": {"top": 1, "left": 2, "width": 3, "height": 4}},
            "regiones_apps": {"AppX": {"top": 0, "left": 0, "width": 100, "height": 100}},
            "monitores_apps": {"AppX": 1},
        }
        guardar_config(datos)
        cargado = cargar_config()

        for ui_name, clave in self.UI_CONFIG_MAPPING.items():
            assert clave in cargado, (
                f"CONFIG NO PERSISTIDA: '{ui_name}' (clave '{clave}') NO esta en config.json"
            )
````

## File: tests/test_paths.py
````python
import os
import sys
import pytest

from utils.paths import resource_path


class TestResourcePath:
    def test_devuelve_ruta_absoluta(self):
        ruta = resource_path("config/config.json")
        assert os.path.isabs(ruta)

    def test_mantiene_estructura_de_directorios(self):
        ruta = resource_path("config/config.json")
        assert "config" in ruta
        assert "config.json" in ruta

    def test_con_archivo_raiz(self):
        ruta = resource_path("requirements.txt")
        assert "requirements.txt" in ruta

    def test_ruta_no_depende_de_meipass_sin_pyinstaller(self):
        ruta = resource_path("test.txt")
        directorio_actual = os.path.abspath(".")
        assert ruta.startswith(directorio_actual)

    def test_ruta_concatenacion_limpia(self):
        ruta = resource_path("config/config.json")
        assert "config" in ruta
        assert "config.json" in ruta
````

## File: tests/test_plantillas.py
````python
import json
import pytest
from unittest.mock import patch

import ui.ventana_plantillas as vp
from ui.ventana_plantillas import (
    PLANTILLAS_DEFAULT,
    _cargar_plantillas,
    _guardar_plantillas,
)


class TestPlantillasModulo:


    def test_cargar_sin_archivo_devuelve_default(self, mock_plantillas_path):
        if mock_plantillas_path.exists():
            mock_plantillas_path.unlink()
        plantillas = _cargar_plantillas()
        assert len(plantillas) == len(PLANTILLAS_DEFAULT)
        assert plantillas == PLANTILLAS_DEFAULT

    def test_cargar_con_archivo_existente(self, mock_plantillas_path):
        personalizadas = [{"titulo": "Test", "categoria": "General", "texto": "Hola"}]
        _guardar_plantillas(personalizadas)
        cargadas = _cargar_plantillas()
        assert cargadas == personalizadas

    def test_cargar_archivo_corrupto_devuelve_default(self, mock_plantillas_path):
        mock_plantillas_path.write_text("no es json valido {{{", encoding="utf-8")
        plantillas = _cargar_plantillas()
        assert plantillas == PLANTILLAS_DEFAULT

    def test_guardar_crea_directorio(self, temp_dir):
        sub = temp_dir / "subdir" / "plantillas.json"
        import ui.ventana_plantillas as vp_mod

        with patch("ui.ventana_plantillas.PLANTILLAS_PATH", sub):
            _guardar_plantillas([{"titulo": "X", "categoria": "G", "texto": "Y"}])
            assert sub.exists()

    def test_guardar_con_unicode(self, mock_plantillas_path):
        plantilla = [{"titulo": "Cañón", "categoria": "General", "texto": "áéíóú"}]
        _guardar_plantillas(plantilla)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["titulo"] == "Cañón"

    def test_guardar_multiples_plantillas(self, mock_plantillas_path):
        plantillas = [
            {"titulo": "A", "categoria": "General", "texto": "a"},
            {"titulo": "B", "categoria": "HubSpot", "texto": "b"},
            {"titulo": "C", "categoria": "Sunrun", "texto": "c"},
        ]
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert len(cargadas) == 3


class TestPlantillasDefault:


    def test_cantidad_plantillas_default(self):
        assert len(PLANTILLAS_DEFAULT) >= 6

    def test_todas_tienen_titulo(self):
        for p in PLANTILLAS_DEFAULT:
            assert p["titulo"]
            assert isinstance(p["titulo"], str)

    def test_todas_tienen_categoria(self):
        categorias = {p.get("categoria") for p in PLANTILLAS_DEFAULT}
        assert "HubSpot" in categorias or "hubspot" in [c.lower() for c in categorias]
        assert "Sunrun" in categorias or "sunrun" in [c.lower() for c in categorias]

    def test_todas_tienen_texto(self):
        for p in PLANTILLAS_DEFAULT:
            assert p["texto"]
            assert isinstance(p["texto"], str)

    def test_default_es_independiente_del_archivo(self, mock_plantillas_path):
        if mock_plantillas_path.exists():
            mock_plantillas_path.unlink()
        d1 = _cargar_plantillas()
        _guardar_plantillas([{"titulo": "Custom", "categoria": "X", "texto": "Y"}])
        d2 = _cargar_plantillas()
        assert len(d2) == 1
        assert d2[0]["titulo"] == "Custom"


class TestRoundTripPlantillas:


    def test_crear_leer_actualizar_eliminar(self, mock_plantillas_path):
        _guardar_plantillas(PLANTILLAS_DEFAULT.copy())

        plantillas = _cargar_plantillas()
        inicial = len(plantillas)

        plantillas.append({"titulo": "Nueva", "categoria": "General", "texto": "Nuevo texto"})
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        assert len(cargadas) == inicial + 1
        assert any(p["titulo"] == "Nueva" for p in cargadas)

        for p in plantillas:
            if p["titulo"] == "Nueva":
                p["texto"] = "Texto editado"
                break
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        nueva = next(p for p in cargadas if p["titulo"] == "Nueva")
        assert nueva["texto"] == "Texto editado"

        plantillas = [p for p in plantillas if p["titulo"] != "Nueva"]
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        assert len(cargadas) == inicial
        assert not any(p["titulo"] == "Nueva" for p in cargadas)

    def test_cambiar_categoria_persiste(self, mock_plantillas_path):
        plantillas = _cargar_plantillas()
        plantillas[0]["categoria"] = "Sunrun"
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["categoria"] == "Sunrun"

    def test_cambiar_titulo_persiste(self, mock_plantillas_path):
        plantillas = _cargar_plantillas()
        plantillas[0]["titulo"] = "Titulo Modificado"
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["titulo"] == "Titulo Modificado"
````

## File: tests/test_plugin_registry.py
````python
import pytest

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.plugin_registry import PluginRegistry


class _PluginFalso(SitioPlugin):
    def __init__(self, nombre, login=True):
        self._nombre = nombre
        self._login = login

    @property
    def nombre(self):
        return self._nombre

    @property
    def necesita_login(self):
        return self._login

    def subir(self, ctx):
        return ResultadoSubida(exitoso=True)


@pytest.fixture(autouse=True)
def _limpiar_registry():
    PluginRegistry.limpiar()
    yield
    PluginRegistry.limpiar()


class TestRegistrar:
    def test_registrar_un_plugin(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.existe("HUBSPOT")

    def test_registrar_multiples_plugins(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        assert len(PluginRegistry.todos()) == 2

    def test_registrar_reemplaza_plugin_existente(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert len(PluginRegistry.todos()) == 1


class TestObtener:
    def test_obtener_plugin_existe(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.obtener("HUBSPOT") is p

    def test_obtener_plugin_no_existe_lanza_keyerror(self):
        with pytest.raises(KeyError):
            PluginRegistry.obtener("NOEXISTE")

    def test_obtener_o_none_existe(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.obtener_o_none("HUBSPOT") is p

    def test_obtener_o_none_no_existe_devuelve_none(self):
        assert PluginRegistry.obtener_o_none("NOEXISTE") is None


class TestDesregistrar:
    def test_desregistrar_plugin_existente(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.desregistrar("HUBSPOT")
        assert not PluginRegistry.existe("HUBSPOT")

    def test_desregistrar_plugin_inexistente_no_falla(self):
        PluginRegistry.desregistrar("NOEXISTE")


class TestLimpiar:
    def test_limpiar_registry(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        PluginRegistry.limpiar()
        assert PluginRegistry.todos() == []


class TestTodos:
    def test_todos_vacio(self):
        assert PluginRegistry.todos() == []

    def test_todos_con_multiples(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        todos = PluginRegistry.todos()
        assert len(todos) == 2

    def test_todos_mantiene_orden(self):
        PluginRegistry.registrar(_PluginFalso("A"))
        PluginRegistry.registrar(_PluginFalso("B"))
        PluginRegistry.registrar(_PluginFalso("C"))
        nombres = [p.nombre for p in PluginRegistry.todos()]
        assert nombres == ["A", "B", "C"]


class TestNombres:
    def test_nombres_vacio(self):
        assert PluginRegistry.nombres() == []

    def test_nombres_con_plugins(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        assert set(PluginRegistry.nombres()) == {"HUBSPOT", "SUNRUN"}


class TestExiste:
    def test_existe_true(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert PluginRegistry.existe("HUBSPOT")

    def test_existe_false(self):
        assert not PluginRegistry.existe("NOEXISTE")


class TestConLogin:
    def test_con_login_filtra_correctamente(self):
        PluginRegistry.registrar(_PluginFalso("CON_LOGIN", login=True))
        PluginRegistry.registrar(_PluginFalso("SIN_LOGIN", login=False))
        PluginRegistry.registrar(_PluginFalso("CON_LOGIN2", login=True))

        con = PluginRegistry.con_login()
        nombres = {p.nombre for p in con}
        assert "CON_LOGIN" in nombres
        assert "CON_LOGIN2" in nombres
        assert "SIN_LOGIN" not in nombres

    def test_con_login_sin_plugins_devuelve_lista_vacia(self):
        assert PluginRegistry.con_login() == []


class TestFiltrar:
    def test_filtrar_por_nombres(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(["HUBSPOT"])
        assert len(resultado) == 1
        assert resultado[0].nombre == "HUBSPOT"

    def test_filtrar_ambos_devuelve_todos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(["AMBOS"])
        assert len(resultado) == 2

    def test_filtrar_lista_vacia_devuelve_todos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar([])
        assert len(resultado) == 2

    def test_filtrar_ignora_nombres_inexistentes(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        resultado = PluginRegistry.filtrar(["HUBSPOT", "NOEXISTO"])
        assert len(resultado) == 1
        assert resultado[0].nombre == "HUBSPOT"

    def test_filtrar_none_equivale_a_ambos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(None)
        assert len(resultado) == 2


class TestEdgeCases:
    def test_registrar_mismo_nombre_varias_veces(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert len(PluginRegistry.todos()) == 1
        assert PluginRegistry.existe("HUBSPOT")

    def test_desregistrar_despuis_de_limpiar_no_falla(self):
        PluginRegistry.limpiar()
        PluginRegistry.desregistrar("X")
````

## File: ui/comparacion/tema.py
````python
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
        "bg": ("#ffe5cc", "#3a2a1a"),
        "texto": ("#804000", "#f0a050"),
        "icono": "🟠",
    },
    "solo_sunrun": {
        "bg": ("#cce5ff", "#1a2a3a"),
        "texto": ("#004085", "#79c0ff"),
        "icono": "🔵",
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

DISPATCH_STATES = {
    "DISPATCH CANCELLED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH REPORTED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH APPROVED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH ACCEPTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
    "DISPATCH REJECTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
}

NO_TRABAJABLES = {"DISPATCH CANCELLED", "DISPATCH REPORTED", "DISPATCH APPROVED"}
TRABAJABLES = {"DISPATCH ACCEPTED", "DISPATCH REJECTED"}


def info_dispatch_state(estado: str) -> tuple[str, str, str]:







    estado = estado.strip().upper()
    info = DISPATCH_STATES.get(estado)
    if info is None:
        return "red", " -> No es trabajable", (("#721c24", "#f85149"), ("#f8d7da", "#3a1a1a"))
    return info["color"], f" -> {info['texto']}", (
        (("
        else (("#721c24", "#f85149"), ("#f8d7da", "#3a1a1a"))
    )
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

## File: ui/template_filler.py
````python
import re
import customtkinter as ctk
from .ventana_plantillas import PLANTILLAS_DEFAULT

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

## File: ui/widgets/coordinate_inputs.py
````python
import customtkinter as ctk
from tkinter import StringVar


class CoordinateInputsWidget(ctk.CTkFrame):


    def __init__(self, parent, valores_iniciales=None, on_change=None, font_size=9):
        super().__init__(parent, fg_color="transparent")
        self.region_vars = {}
        self._on_change = on_change

        campos = [
            ("top", 392),
            ("left", 524),
            ("width", 934),
            ("height", 404),
        ]

        iniciales = valores_iniciales or {}
        for i, (etiqueta, valor_default) in enumerate(campos):
            valor = iniciales.get(etiqueta, valor_default)
            caja = ctk.CTkFrame(
                self,
                fg_color=("gray90", "gray25"),
                border_width=1,
            )
            caja.pack(side="left", padx=(0 if i == 0 else 6, 0), ipadx=12)

            ctk.CTkLabel(
                caja, text=etiqueta.upper(),
                font=ctk.CTkFont(size=font_size, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))

            var = StringVar(value=str(valor))
            ctk.CTkEntry(
                caja, textvariable=var, width=80,
                font=ctk.CTkFont(size=font_size + 4, weight="bold"),
                justify="center", border_width=0,
            ).pack(pady=(0, 6))

            if on_change:
                var.trace_add("write", lambda *_, v=var: self._notificar())
            self.region_vars[etiqueta] = var

    def _notificar(self):
        if self._on_change:
            self._on_change()

    def aplicar_region(self, region: dict):

        for clave in ("top", "left", "width", "height"):
            if clave in region and clave in self.region_vars:
                self.region_vars[clave].set(str(int(region[clave])))

    def obtener_region(self) -> dict:

        return {
            clave: int(var.get() or 0)
            for clave, var in self.region_vars.items()
        }
````

## File: ui/widgets/log_widget.py
````python
import customtkinter as ctk
from datetime import datetime


class LogWidget(ctk.CTkTextbox):











    def __init__(self, parent, height: int = 160, font_size: int = 10, **kwargs):
        kwargs.setdefault("wrap", "word")
        kwargs.setdefault("height", height)
        kwargs.setdefault("font", ctk.CTkFont(family="Consolas", size=font_size))

        super().__init__(parent, **kwargs)

        tb = self._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("flecha", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

    def log(self, msg: str):

        ts = datetime.now().strftime("%H:%M:%S")
        tag = (
            "ok"
            if msg.startswith("✓")
            else "error"
            if msg.startswith("✗")
            else "flecha"
            if "→" in msg
            else "dim"
        )
        self.configure(state="normal")
        tb = self._textbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.see("end")
        self.configure(state="disabled")

    def clear(self):

        self.configure(state="normal")
        self.delete("0.0", "end")
        self.configure(state="disabled")
````

## File: ui/widgets/monitor_selector.py
````python
import customtkinter as ctk
from tkinter import StringVar


class MonitorSelectorWidget(ctk.CTkFrame):


    def __init__(
        self,
        parent,
        nombres_monitores: list[str],
        monitores_raw: list[dict],
        indice_inicial: int = 0,
        on_change=None,
    ):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._monitores_raw = monitores_raw
        self._nombres = nombres_monitores or ["Monitor 1 (principal)"]
        self._on_change = on_change

        valor_inicial = (
            self._nombres[indice_inicial]
            if 0 <= indice_inicial < len(self._nombres)
            else self._nombres[0]
        )

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            row, text="Monitor:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))

        self.monitor_var = StringVar(value=valor_inicial)
        self.monitor_menu = ctk.CTkOptionMenu(
            row, variable=self.monitor_var,
            values=self._nombres,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False, width=190,
        )
        self.monitor_menu.pack(side="left", padx=(0, 6))

        self.info_label = ctk.CTkLabel(
            row, text="", font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.info_label.pack(side="left")

        self._actualizar_info()
        self.monitor_var.trace_add("write", self._al_cambiar)

    def _al_cambiar(self, *_):
        self._actualizar_info()
        if self._on_change:
            self._on_change()

    def _actualizar_info(self):
        indice = self.obtener_indice()
        if 0 <= indice < len(self._monitores_raw):
            m = self._monitores_raw[indice]
            self.info_label.configure(text=f"{m['width']}x{m['height']} px")

    def obtener_indice(self) -> int:

        try:
            return self._nombres.index(self.monitor_var.get())
        except ValueError:
            return 1
````

## File: ui/widgets/profile_manager.py
````python
import customtkinter as ctk
from tkinter import StringVar, messagebox


class ProfileManagerWidget(ctk.CTkFrame):


    def __init__(
        self,
        parent,
        region_vars: dict[str, StringVar],
        perfiles_iniciales: dict,
        on_cargar_perfil=None,
        on_guardar_perfil=None,
        on_eliminar_perfil=None,
        on_aplicar_region=None,
        on_log=None,
    ):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._perfiles = perfiles_iniciales
        self.region_vars = region_vars
        self._on_cargar = on_cargar_perfil
        self._on_guardar = on_guardar_perfil
        self._on_eliminar = on_eliminar_perfil
        self._on_aplicar_region = on_aplicar_region
        self._on_log = on_log or (lambda _: None)


        pf1 = ctk.CTkFrame(self, fg_color="transparent")
        pf1.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf1, text="Perfil:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))

        nombres = self._nombres_perfiles()
        self._perfil_var = StringVar(value=nombres[0])
        self._perfil_menu = ctk.CTkOptionMenu(
            pf1, variable=self._perfil_var,
            values=nombres,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False, width=150,
        )
        self._perfil_menu.pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            pf1, text="Cargar", command=self._cargar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
        ).pack(side="left")


        pf2 = ctk.CTkFrame(self, fg_color="transparent")
        pf2.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf2, text="Nombre:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self._perfil_nombre_var = StringVar()
        ctk.CTkEntry(
            pf2, textvariable=self._perfil_nombre_var,
            placeholder_text="Ej: Monitor 1 - Panel izq.",
            font=ctk.CTkFont(size=11),
        ).pack(side="left", padx=(0, 6), fill="x", expand=True)
        ctk.CTkButton(
            pf2, text="Guardar", command=self._guardar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(0, 4))
        ctk.CTkButton(
            pf2, text="Eliminar", command=self._eliminar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="left")


        pf3 = ctk.CTkFrame(self, fg_color="transparent")
        pf3.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf3, text="Pegar region:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self.region_paste_var = StringVar(value=self._region_a_texto())
        entrada = ctk.CTkEntry(
            pf3, textvariable=self.region_paste_var, font=ctk.CTkFont(size=11),
        )
        entrada.pack(side="left", padx=(0, 6), fill="x", expand=True)
        entrada.bind("<FocusOut>", self._aplicar_region_pegada)
        entrada.bind("<Return>", self._aplicar_region_pegada)
        self.region_paste_entry = entrada
        ctk.CTkButton(
            pf3, text="Aplicar", command=self._aplicar_region_pegada,
            font=ctk.CTkFont(size=10), width=66, height=28,
        ).pack(side="left")

    def _region_a_texto(self) -> str:
        return str({k: v.get() for k, v in self.region_vars.items()})

    def _nombres_perfiles(self) -> list[str]:
        nombres = list(self._perfiles.keys())
        return nombres if nombres else ["- sin perfiles -"]

    def actualizar_menu(self):
        nombres = self._nombres_perfiles()
        self._perfil_menu.configure(values=nombres)
        self._perfil_var.set(nombres[0])

    def actualizar_perfiles(self, perfiles: dict):
        self._perfiles = perfiles
        self.actualizar_menu()

    def _cargar_perfil(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._on_log("x No hay ningun perfil seleccionado.")
            return
        region = self._perfiles[nombre]
        self._perfil_nombre_var.set(nombre)
        if self._on_cargar:
            self._on_cargar(nombre, region)

    def _guardar_perfil(self):
        nombre = self._perfil_nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Nombre vacio", "Escribe un nombre para el perfil.")
            return
        region = {k: int(v.get() or 0) for k, v in self.region_vars.items()}
        if self._on_guardar:
            self._on_guardar(nombre, region)

    def _eliminar_perfil(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._on_log("x No hay ningun perfil seleccionado para eliminar.")
            return
        if not messagebox.askyesno(
            "Eliminar perfil", f"Eliminar el perfil '{nombre}'?"
        ):
            return
        if self._on_eliminar:
            self._on_eliminar(nombre)

    def _aplicar_region_pegada(self, event=None):
        if self._on_aplicar_region:
            self._on_aplicar_region(self.region_paste_var.get().strip())

    def sincronizar_paste(self):
        self.region_paste_var.set(self._region_a_texto())
````

## File: utils/__init__.py
````python

````

## File: utils/colors.py
````python
def oscurecer(color_hex: str, factor: float = 0.80) -> str:












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
````

## File: utils/fsd.py
````python
import re


def solo_digitos(fsd: str) -> str:








    return re.sub(r"[^0-9]", "", fsd)


def fsd_display(numero: str) -> str:
    """Formato de display estándar: "FSD-1172172"."""
    return f"FSD-{numero}"


def normalizar_fsd(fsd: str | None) -> str | None:
    """
    Normaliza el FSD para búsqueda inteligente en pestañas.

    - Si es None, vacío o solo espacios: devuelve None
    - Si es "980124": convierte a "FSD-980124"
    - Si es "FSD-980124": lo mantiene igual
    - Case-insensitive: siempre devuelve mayúsculas
````

## File: utils/iniciar_chrome_sesion.py
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

## File: utils/paths.py
````python
import os
import sys
from pathlib import Path


def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_project_root() -> Path:






    return Path(__file__).resolve().parent.parent
````

## File: utils/recuperar_puerto.py
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
        monitor: int = 1,
    ) -> str:

















        from config.configuracion import obtener_monitor_por_indice

        region_dict = cls._normalizar_region(region)
        cls._validar_region(region_dict)


        mon_info = obtener_monitor_por_indice(monitor)
        if mon_info:

            region_ajustada = {
                "top": region_dict["top"] + mon_info.get("top", 0),
                "left": region_dict["left"] + mon_info.get("left", 0),
                "width": region_dict["width"],
                "height": region_dict["height"],
            }
        else:

            region_ajustada = region_dict

        destino = carpeta or cls.CARPETA_CAPTURAS
        destino.mkdir(parents=True, exist_ok=True)

        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = destino / f"captura_{marca}.png"

        try:
            with mss.MSS() as sct:
                captura = sct.grab(region_ajustada)
                mss.tools.to_png(captura.rgb, captura.size, output=str(ruta))
        except Exception as e:
            raise ErrorCaptura(
                f"Error al capturar región {region_ajustada}: {e}"
            ) from e

        return str(ruta.resolve())

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _normalizar_region(region) -> dict:
        """Acepta dict o RegionCaptura y devuelve siempre un dict con ints."""
        if hasattr(region, "as_dict"):
            region = region.as_dict()
        return {
            k: int(v)
            for k, v in region.items()
            if k in ("top", "left", "width", "height")
        }

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

## File: data/buscador.py
````python
from data.api import HubSpotAPI, buscar_fsd_por_id_cliente





SEARCH_STRATEGIES = {
    "fsd": {
        "field": "fsd__",
        "label": "FSD",
        "input_count": 1,
        "placeholder": "Ej: 983316",
    },
    "nombre": {
        "field": "firstname",
        "label": "Nombre",
        "input_count": 1,
        "placeholder": "Ej: Juan",
    },
    "apellido": {
        "field": "lastname",
        "label": "Apellido",
        "input_count": 1,
        "placeholder": "Ej: Pérez",
    },
    "telefono": {
        "field": "phone",
        "label": "Teléfono",
        "input_count": 1,
        "placeholder": "Ej: +17872979317",
    },
    "correo": {
        "field": "email",
        "label": "Correo electrónico",
        "input_count": 1,
        "placeholder": "Ej: contacto@ejemplo.com",
    },
    "direccion": {
        "field": "address",
        "label": "Dirección",
        "input_count": 1,
        "placeholder": "Ej: San Juan",
    },
    "id_cliente": {
        "field": "id_de_goformz__contacto_",
        "label": "ID Cliente",
        "input_count": 1,
        "placeholder": "Ej: 1234",
    },
}






def buscar_contactos(
    valor: str,
    tipo_busqueda: str,
):











    estrategia = SEARCH_STRATEGIES.get(tipo_busqueda)
    if not estrategia:
        return []

    api = HubSpotAPI()
    candidatos = api.buscar_contactos_por_criterio(valor, tipo_busqueda)


    for candidato in candidatos:
        id_cliente = candidato.get("id_cliente")


        if id_cliente and str(id_cliente).strip():
            try:
                fsd = buscar_fsd_por_id_cliente(str(id_cliente).strip())
                if fsd:
                    candidato["fsd"] = fsd
                else:
                    candidato["fsd"] = ""
            except Exception as e:
                print(
                    f"[ERROR] No se pudo extraer FSD para id_cliente={id_cliente}: {e}"
                )
                candidato["fsd"] = ""
        else:
            candidato["fsd"] = ""

    return candidatos
````

## File: gsheets/core/playwright_capture.py
````python
from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from gsheets.utils.cell_parser import col_letter_to_index



logger = logging.getLogger(__name__)



_SESSION_DIR = Path(__file__).resolve().parent.parent / "sessions"
_SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "screenshots"
_DEBUG_DIR = Path(__file__).resolve().parent.parent / "screenshots" / "debug"


_GRID_SELECTORS = [
    "#waffle-grid-container",
    "#grid-container",
    '[class*="waffle"]',
]
_COL_HEADER_SELECTORS = [
    "#colheaders",
    "#column-headers",
    '[id*="colheader"]',
    '[class*="column-header"]',
]
_ROW_HEADER_SELECTORS = [
    "#rowheaders",
    "#row-headers",
    '[id*="rowheader"]',
    '[class*="row-header"]',
]


_LOAD_TIMEOUT = 20_000
_GRID_TIMEOUT = 30_000
_RENDER_DELAY = 1_500
_RETRY_DELAY = 2_000
_RETRY_INTERVAL = 500
_MAX_GRID_RETRIES = 20





class PlaywrightSheetsCapture:

















    _SESSION_FILE = _SESSION_DIR / "google_sheets_state.json"
    _PROFILE_DIR_DEFAULT = _SESSION_DIR / "chrome_profile"

    def __init__(
        self,
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        session_dir: str | Path | None = None,
        screenshots_dir: str | Path | None = None,
        debug_dir: str | Path | None = None,
        profile_dir: str | Path | None = None,
        log_callback: Callable[[str], None] | None = None,
    ) -> None:
        self._headless = headless
        self._viewport = {"width": viewport_width, "height": viewport_height}
        self._session_dir = Path(session_dir) if session_dir else _SESSION_DIR
        self._screenshots_dir = (
            Path(screenshots_dir) if screenshots_dir else _SCREENSHOTS_DIR
        )
        self._debug_dir = Path(debug_dir) if debug_dir else _DEBUG_DIR
        self._session_path = self._session_dir / "google_sheets_state.json"
        self._profile_dir = (
            Path(profile_dir) if profile_dir else self._session_dir / "chrome_profile"
        )
        self._use_persistent = (
            bool(profile_dir) or True
        )
        self._log = log_callback or (lambda msg: logger.info(msg))

        self._playwright: Any = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._auth_verified = False


        self._session_dir.mkdir(parents=True, exist_ok=True)
        self._screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._debug_dir.mkdir(parents=True, exist_ok=True)
        if self._use_persistent:
            self._profile_dir.mkdir(parents=True, exist_ok=True)



    async def __aenter__(self) -> "PlaywrightSheetsCapture":
        await self.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.stop()



    _CDP_URL = "http://localhost:9222"

    async def start(self) -> None:












        self._playwright = await async_playwright().start()


        try:
            self._browser = await self._playwright.chromium.connect_over_cdp(
                self._CDP_URL, timeout=5_000
            )
            self._context = self._browser.contexts[0]
            self._page = (
                self._context.pages[0]
                if self._context.pages
                else await self._context.new_page()
            )
            self._log("→ Playwright conectado al Chrome existente (puerto 9222).")
            self._log("→ Reutilizando sesión de Google autenticada del proyecto.")
            return
        except Exception:
            self._log(
                "· Chrome en puerto 9222 no detectado, abriendo nuevo navegador..."
            )


        try:
            from core.browser import CHROME_USER_DATA
        except ImportError:
            CHROME_USER_DATA = str(self._profile_dir)

        context_options = {
            "headless": self._headless,
            "viewport": self._viewport,
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }

        self._context = await self._playwright.chromium.launch_persistent_context(
            user_data_dir=CHROME_USER_DATA,
            **context_options,
        )
        self._browser = None

        self._page = (
            self._context.pages[0]
            if self._context.pages
            else await self._context.new_page()
        )
        self._log(f"→ Playwright iniciado con perfil: {CHROME_USER_DATA}.")

    async def stop(self) -> None:
        """
        Cierra el navegador Playwright.

        Si se conectó vía CDP, solo desconecta (no cierra pestañas del usuario).
        Si se lanzó perfil persistente, cierra el contexto.
        """
        es_cdp = self._browser is not None

        if not es_cdp and self._context:
            await self._context.close()
            self._context = None

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        self._page = None
        self._log("→ Playwright detenido.")

    # ── Propiedades ───────────────────────────────────────────────────────

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError(
                "Playwright no ha sido iniciado. Llame a start() primero."
            )
        return self._page

    # ── Captura de celda individual ───────────────────────────────────────

    async def capture_cell(
        self,
        sheet_url: str,
        cell_ref: str,
        output_path: str | None = None,
        sheet_gid: str | int = "0",
        expected_value: str | None = None,
    ) -> str:

















        if output_path is None:
            output_path = str(self._screenshots_dir / f"{cell_ref.lower()}.png")

        output_path = str(Path(output_path).resolve())
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        spreadsheet_id = self._extract_spreadsheet_id(sheet_url)


        if not self._auth_verified:
            await self._verify_google_auth()


        target_url = (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            f"/edit
        )
        existing_page = await self._find_spreadsheet_page(spreadsheet_id)
        if existing_page:
            self._page = existing_page
            self._log(f"→ Spreadsheet {spreadsheet_id} ya abierto — reutilizando pestaña.")
        else:
            self._page = await self._open_new_page()
            self._log(f"→ Abriendo nueva pestaña: gid={sheet_gid}, celda {cell_ref}...")

        await self._page.bring_to_front()
        try:
            await self.page.goto(
                target_url, wait_until="domcontentloaded", timeout=_LOAD_TIMEOUT
            )
        except Exception as e:
            self._log(f"⚠ goto timeout/error: {e}")
            await self.page.goto(target_url, wait_until="load", timeout=_LOAD_TIMEOUT)


        current_url = self.page.url
        title = await self.page.title()
        self._log(f"· URL actual: {current_url[:150]}")
        self._log(f"· Título: {title[:100]}")

        # ── Validar que estamos en la página correcta ─────────────────
        await self._validate_page(spreadsheet_id, sheet_gid, cell_ref)

        # ── Esperar y verificar el grid con sondeo ────────────────────
        grid_ok = await self._wait_for_grid()
        if not grid_ok:
            await self._dump_debug_info("grid_not_found", cell_ref)
            raise RuntimeError(
                f"No se detectó el grid de Google Sheets para la celda {cell_ref}. "
                f"gid={sheet_gid}. Se generó screenshot de depuración."
            )

        # ── Localizar celda ───────────────────────────────────────────
        rect = await self._locate_cell(cell_ref)

        if rect is None:
            # Reintento con recarga completa
            self._log(f"· Reintentando localizar celda {cell_ref} (recarga)...")
            await asyncio.sleep(0.001 * _RETRY_DELAY)
            await self.page.reload(wait_until="domcontentloaded")
            await self._validate_page(spreadsheet_id, sheet_gid, cell_ref)
            grid_ok = await self._wait_for_grid()
            if not grid_ok:
                await self._dump_debug_info("grid_not_found_retry", cell_ref)
                raise RuntimeError(
                    f"No se detectó el grid tras recarga para {cell_ref}. "
                    f"gid={sheet_gid}."
                )
            rect = await self._locate_cell(cell_ref)

        if rect is None:
            await self._dump_debug_info("cell_not_found", cell_ref)
            raise RuntimeError(
                f"No se pudo localizar la celda {cell_ref} en gid={sheet_gid}. "
                f"Verifique que la celda exista en la pestaña seleccionada. "
                f"Se generó screenshot de depuración."
            )

        # ── Validar y refinar rect antes de capturar ──────────────────
        clip = await self._validate_and_refine_rect(
            cell_ref, rect, output_path, expected_value
        )

        # ── Capturar ──────────────────────────────────────────────────
        await self.page.screenshot(path=output_path, clip=clip)
        self._log(f"✓ Celda {cell_ref} capturada → {output_path}")
        return output_path

    async def capture_cells(
        self,
        sheet_url: str,
        cell_refs: list[str],
        output_dir: str | None = None,
        sheet_gid: str | int = "0",
        expected_values: dict[str, str | None] | None = None,
    ) -> dict[str, str]:











        results: dict[str, str] = {}
        for ref in cell_refs:
            path = await self.capture_cell(
                sheet_url=sheet_url,
                cell_ref=ref,
                output_path=(
                    str(Path(output_dir) / f"{ref.lower()}.png") if output_dir else None
                ),
                sheet_gid=sheet_gid,
                expected_value=(expected_values.get(ref) if expected_values else None),
            )
            results[ref] = path
        return results

    async def _find_spreadsheet_page(self, spreadsheet_id: str) -> Page | None:




        if self._browser is None and self._context is None:
            return None

        pages: list[Page] = []
        try:
            if self._browser:
                for ctx in self._browser.contexts:
                    pages.extend(ctx.pages)
            elif self._context:
                pages = self._context.pages
        except Exception:
            pass

        for page in pages:
            try:
                url = page.url
                if spreadsheet_id in url:
                    return page
            except Exception:
                continue

        return None

    async def _open_new_page(self) -> Page:

        if self._browser:
            for ctx in self._browser.contexts:
                if ctx.pages:
                    page = await ctx.new_page()
                    await page.bring_to_front()
                    return page
        if self._context:
            page = await self._context.new_page()
            await page.bring_to_front()
            return page
        raise RuntimeError("No hay browser ni contexto activo para abrir una pestaña.")

    async def _validate_page(
        self, spreadsheet_id: str, sheet_gid: str | int, cell_ref: str
    ) -> None:









        title = await self.page.title()
        current_url = self.page.url


        is_login_url = "accounts.google.com" in current_url
        is_login_title = "sign in" in title.lower() or "iniciar sesión" in title.lower()
        is_google_com = (
            current_url.startswith("https://www.google.com")
            and "spreadsheets" not in current_url
        )

        if is_login_url or is_login_title or is_google_com:
            await self._dump_debug_info("login_redirect", cell_ref)
            raise RuntimeError(
                "✗ Playwright fue redirigido a la pantalla de login de Google.\n"
                "   La sesión no está autenticada o expiró.\n\n"
                "   Solución:\n"
                "   1. Ejecuta con headless=False\n"
                "   2. Inicia sesión manualmente en Google en la ventana del navegador\n"
                "   3. Cierra la app normalmente (la sesión se guarda en el perfil)\n"
                "   4. Vuelve a ejecutar — la sesión se reutilizará automáticamente.\n\n"
                f"   URL actual: {current_url}\n"
                f"   Título: {title}"
            )

        # ── Validar que estamos en el spreadsheet correcto ────────────
        is_sheets = "docs.google.com/spreadsheets" in current_url
        has_gid = (
            f"gid={sheet_gid}" in current_url or f"
        )

        self._log(
            f"· Página: title='{title[:80]}', "
            f"sheets={is_sheets}, gid_match={has_gid}"
        )

        if not is_sheets:
            self._log(f"⚠ URL no es Google Sheets: {current_url[:120]}")

        if not has_gid:
            self._log(
                f"⚠ El gid={sheet_gid} no aparece en la URL. "
                f"Posible redirección. URL: {current_url[:120]}"
            )

    # ── Verificación de autenticación Google ───────────────────────────────

    async def _verify_google_auth(self) -> None:
        """
        Verifica que la sesión de Google esté autenticada.

        Abre una pestaña TEMPORAL en myaccount.google.com para no
        reemplazar pestañas existentes. Si la URL se mantiene en
        myaccount, la sesión está activa. Si redirige a
        accounts.google.com, la sesión expiró o nunca se autenticó.

        Solo se ejecuta una vez por ciclo de vida del navegador.
        """
        self._log("→ Verificando autenticación de Google...")
        temp_page = None
        try:
            temp_page = await self._context.new_page()
            await temp_page.goto(
                "https://myaccount.google.com",
                wait_until="domcontentloaded",
                timeout=15_000,
            )
        except Exception:
            pass

        current_url = temp_page.url if temp_page else ""
        self._log(f"   myaccount → {current_url[:120]}")

        if "accounts.google.com" in current_url:
            self._auth_verified = False
            if temp_page:
                await temp_page.close()
            raise RuntimeError(
                "✗ La sesión de Google no está autenticada.\n"
                "   Playwright fue redirigido a accounts.google.com.\n\n"
                "   Solución:\n"
                "   1. Ejecuta con headless=False\n"
                "   2. Inicia sesión manualmente en Google\n"
                "   3. Cierra la app normalmente (el perfil guarda la sesión)\n"
                "   4. Vuelve a ejecutar — la sesión se reutilizará.\n\n"
                f"   URL: {current_url}"
            )

        if temp_page:
            await temp_page.close()
        self._auth_verified = True
        self._log("✓ Sesión de Google autenticada.")

    # ── Espera del grid ───────────────────────────────────────────────────

    async def _wait_for_grid(self) -> bool:
        """
        Espera a que el grid de Google Sheets esté renderizado mediante sondeo.

        Google Sheets nunca llega a "networkidle" (WebSockets abiertos),
        por lo que usamos domcontentloaded + sondeo del DOM cada 500ms.

        Retorna True si se detectó el grid, False si se agotaron los reintentos.







                () => {
                    const selectors = [
                        '#waffle-grid-container', '#grid-container',
                        '[class*="waffle"]', '#colheaders', '#rowheaders',
                        '#formula-bar', '#t-formula-bar-input',
                    ];
                    const results = [];
                    for (const s of selectors) {
                        const el = document.querySelector(s);
                        if (el) results.push(s);
                    }
                    return results.length > 0 ? results.join(', ') : null;
                }




























        Localiza el rect exacto de la celda activa en Google Sheets (modo canvas).

        Google Sheets dibuja 4 divs .active-cell-border para los bordes de la
        celda seleccionada (top, bottom, left, right), cada uno de 2px de grosor.
        Reconstruimos el rect completo haciendo la unión de sus bounding boxes:

          top:    { x:221, y:327, w:456, h:2 }
          bottom: { x:221, y:419, w:456, h:2 }
          right:  { x:675, y:327, w:2,   h:94 }
          left:   { x:221, y:327, w:2,   h:94 }
          → rect: { x:221, y:327, w:456, h:94 }

        También intentamos el .selection-border-cover como fuente secundaria
        (cuando hay, tiene x/y/w correctos pero h puede ser solo 5px).



            (cellRef) => {
                // ── Estrategia 1: reconstruir rect desde los 4 bordes active-cell-border ──
                // Google Sheets dibuja exactamente 4 divs de 2px para los lados de la celda.
                // La unión de sus bounding boxes = el rect completo de la celda.
                const activeBorders = document.querySelectorAll('.active-cell-border');
                if (activeBorders.length >= 2) {
                    let minX = Infinity, minY = Infinity;
                    let maxX = -Infinity, maxY = -Infinity;
                    let found = 0;
                    for (const el of activeBorders) {
                        const r = el.getBoundingClientRect();
                        // Ignorar bordes con area cero (ocultos/reutilizados)
                        if (r.width < 1 || r.height < 1) continue;
                        // Solo bordes dentro del viewport (descartar los que están en x>2000)
                        if (r.x > window.innerWidth * 2 || r.y > window.innerHeight * 2) continue;
                        minX = Math.min(minX, r.x);
                        minY = Math.min(minY, r.y);
                        maxX = Math.max(maxX, r.x + r.width);
                        maxY = Math.max(maxY, r.y + r.height);
                        found++;
                    }
                    if (found >= 2 && maxX > minX && maxY > minY) {
                        return {
                            x:      Math.round(minX),
                            y:      Math.round(minY),
                            width:  Math.round(maxX - minX),
                            height: Math.round(maxY - minY),
                            source: 'active-cell-border-union',
                        };
                    }
                }

                // ── Estrategia 2: selection-border-cover con dimensiones válidas ──
                // Cuando existe, tiene x/y/w correctos. El h puede ser pequeño (5px)
                // pero si es > 10 es confiable.
                for (const el of document.querySelectorAll('.selection-border-cover')) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 20 && r.height > 10) {
                        return {
                            x:      Math.round(r.x),
                            y:      Math.round(r.y),
                            width:  Math.round(r.width),
                            height: Math.round(r.height),
                            source: 'selection-border-cover',
                        };
                    }
                }

                // ── Estrategia 3: canvas + offsets de headers (estimación) ────────
                const canvas      = document.querySelector('canvas');
                const colHeaderEl = document.querySelector('[class*="column-header"]');
                const rowHeaderEl = document.querySelector('[class*="row-header"]');
                if (!canvas) return null;

                const cr         = canvas.getBoundingClientRect();
                const colHeaderH = colHeaderEl ? colHeaderEl.getBoundingClientRect().height : 24;
                const rowHeaderW = rowHeaderEl ? rowHeaderEl.getBoundingClientRect().width  : 46;

                const match = cellRef.match(/^([A-Z]+)(\\d+)$/i);
                if (!match) return null;
                const colLetters = match[1].toUpperCase();
                const rowNum     = parseInt(match[2]);
                let colIdx = 0;
                for (let i = 0; i < colLetters.length; i++) {
                    colIdx = colIdx * 26 + (colLetters.charCodeAt(i) - 64);
                }
                colIdx -= 1;
                const rowIdx = rowNum - 1;

                return {
                    x:      Math.round(cr.x + rowHeaderW + colIdx * 100),
                    y:      Math.round(cr.y + colHeaderH + rowIdx * 21),
                    width:  100,
                    height: 21,
                    source: 'canvas-estimate',
                };
            }

















        Valida el rect devuelto por _locate_cell y lo prepara como clip de screenshot.

        Con la estrategia 'active-cell-border-union', _locate_cell ya devuelve el
        rect exacto de la celda (unión de los 4 bordes de 2px). Este método:
          1. Valida dimensiones mínimas.
          2. Para 'active-cell-border-union': descuenta 2px del borde para obtener
             el interior limpio de la celda, o los mantiene para ver el borde completo.
          3. Si el rect es dudoso, reintenta los overlays.
          4. Genera debug highlight.
          5. Retorna el clip final.

















                () => {
                    // Reintentar unión de active-cell-border
                    const borders = document.querySelectorAll('.active-cell-border');
                    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity, n = 0;
                    for (const el of borders) {
                        const r = el.getBoundingClientRect();
                        if (r.width < 1 || r.height < 1) continue;
                        if (r.x > window.innerWidth * 2 || r.y > window.innerHeight * 2) continue;
                        minX = Math.min(minX, r.x);   minY = Math.min(minY, r.y);
                        maxX = Math.max(maxX, r.x + r.width); maxY = Math.max(maxY, r.y + r.height);
                        n++;
                    }
                    if (n >= 2 && maxX > minX && maxY > minY) {
                        return { x: Math.round(minX), y: Math.round(minY),
                                 width: Math.round(maxX-minX), height: Math.round(maxY-minY),
                                 source: 'retry-active-cell-border' };
                    }
                    return null;
                }




















































Genera screenshot de depuración y registra contexto de la página."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"{reason}_{cell_ref}_{timestamp}"

        # Screenshot completo de la página
        try:
            ss_path = str(self._debug_dir / f"{prefix}_full.png")
            await self.page.screenshot(path=ss_path, full_page=False)
            self._log(f"· Debug screenshot: {ss_path}")
        except Exception as e:
            logger.warning("No se pudo generar screenshot de depuración: %s", e)

        # Contexto de la página
        try:
            title = await self.page.title()
            url = self.page.url
            self._log(f"· Debug — title: '{title[:100]}'")
            self._log(f"· Debug — url: {url[:200]}")

            # Extraer HTML relevante (contenedor del grid si existe)
            html_sample = await self.page.evaluate("""
                () => {
                    const grid = document.querySelector('#waffle-grid-container, #grid-container, [class*=\"waffle\"]');
                    if (grid) return grid.outerHTML.substring(0, 500);
                    return document.body ? document.body.innerHTML.substring(0, 500) : '(no body)';
                }









Extrae el spreadsheet ID de una URL o retorna el valor tal cual si ya es un ID."""
        import re

        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url_or_id)
        if match:
            return match.group(1)
        return url_or_id

    # ── Wrappers síncronos ─────────────────────────────────────────────

    def capture_cells_sync(
        self,
        sheet_url: str,
        cell_refs: list[str],
        output_dir: str | None = None,
        sheet_gid: str | int = "0",
        expected_values: dict[str, str | None] | None = None,
    ) -> dict[str, str]:
        """
        Versión síncrona de capture_cells (para usar desde threads/tkinter).

        Abre el navegador, captura todas las celdas, y cierra el navegador
        en una sola llamada bloqueante. Ideal para entornos sin asyncio.



















Start → capture → stop en un solo ciclo de vida."""
        await self.start()
        try:
            return await self.capture_cells(
                sheet_url=sheet_url,
                cell_refs=cell_refs,
                output_dir=output_dir,
                sheet_gid=sheet_gid,
                expected_values=expected_values,
            )
        finally:
            await self.stop()

    # ── Helpers públicos ──────────────────────────────────────────────────

    def clear_session(self) -> None:
        """
        Elimina el perfil persistente de Chrome.

        Borra cookies, localStorage y toda la sesión de Google.
        La próxima ejecución requerirá autenticación manual.
````

## File: services/session_manager.py
````python
from __future__ import annotations

from pathlib import Path
from typing import Callable

from core.base_plugin import SitioPlugin
from core.browser import esperar_carga
from config.credenciales import cargar_cookies, cargar_credenciales


class SessionManager:


    def __init__(self, driver):
        self.driver = driver

    def asegurar(
        self,
        plugin: SitioPlugin,
        log: Callable[[str], None],
        credenciales_sesion: dict,
    ) -> None:




        self._posicionar_pestana(plugin, log)

        if plugin.usar_pagina_actual:
            plugin.verificar_sesion(self.driver, log)
            return


        ruta_cookies = Path(f"cookies/{plugin.nombre}.pkl")
        if ruta_cookies.exists():
            log(f"  -> Restaurando sesion con cookies para {plugin.nombre}...")
            url_base = getattr(plugin, "URL_LOGIN", "")
            if url_base:
                try:
                    cargar_cookies(
                        self.driver, {"nombre": plugin.nombre}, url_base
                    )
                    esperar_carga(self.driver, timeout=5)
                    if plugin.verificar_sesion(self.driver, log):
                        return
                    log("  . Cookies invalidas, iniciando login...")
                except Exception as e:
                    log(f"  . Error restaurando cookies: {e}")

        # Login automatico
        credenciales = self._obtener_credenciales(
            plugin.nombre, credenciales_sesion
        )
        if credenciales:
            if plugin.hacer_login(self.driver, credenciales, log):
                return

        raise RuntimeError(
            f"No se pudo establecer sesion para {plugin.nombre}. "
            f"Verifica las credenciales en el menu 'Credenciales'."
        )

    def _posicionar_pestana(
        self, plugin: SitioPlugin, log: Callable[[str], None]
    ) -> None:
        """Valida la pestana del plugin y recorre tabs si hace falta."""
        if plugin.usar_pagina_actual and plugin.dominio:
            log(f"  -> Validando pestana activa de {plugin.nombre}...")
            try:
                url = self.driver.current_url.lower()
                if plugin.dominio.lower() not in url:
                    log(
                        f"  . Pestana activa no es {plugin.nombre}. "
                        f"El plugin buscara la pestana correcta."
                    )
                else:
                    log("  v Pestana activa validada.")
            except Exception:
                log(
                    f"  . Pestaña sin contexto — {plugin.nombre} "
                    f"buscara la correcta por su cuenta."
                )
        elif not plugin.usar_pagina_actual and plugin.dominio:
            log(
                f"  . [{plugin.nombre}] No se cambia de pestana "
                f"automaticamente."
            )

    @staticmethod
    def _es_tab_valida(driver, handle) -> bool:
        try:
            driver.switch_to.window(handle)
            driver.execute_script("return 1")
            return True
        except Exception:
            return False

    @staticmethod
    def _obtener_credenciales(nombre_plugin: str, sesion: dict) -> dict:

        if nombre_plugin in sesion:
            return sesion[nombre_plugin]
        usuario, clave = cargar_credenciales(nombre_plugin)
        if usuario:
            return {"usuario": usuario, "clave": clave}
        return {}
````

## File: test/test_buscar_fsd.py
````python
from data.api import buscar_fsd_por_id_cliente


print("=" * 60)
print("TEST 1: id_cliente='267334'")
print("=" * 60)

resultado = buscar_fsd_por_id_cliente("267334")
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")
print(f"Tipo: {type(resultado)}")

# Test 2: id_cliente vacío
print("\n" + "=" * 60)
print("TEST 2: id_cliente=''")
print("=" * 60)

resultado = buscar_fsd_por_id_cliente("")
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")

# Test 3: id_cliente None
print("\n" + "=" * 60)
print("TEST 3: id_cliente=None")
print("=" * 60)

resultado = buscar_fsd_por_id_cliente(None)
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")

# Test 4: buscar directamente un FSD conocido
print("\n" + "=" * 60)
print("TEST 4: Buscar FSD '1251275' directamente")
print("=" * 60)

from data.api import extraer_datos_hubspot

datos = extraer_datos_hubspot("1251275")
print(f"FSD extraído: {repr(datos.get('fsd'))}")
print(f"ID Cliente: {repr(datos.get('id_cliente'))}")
print(f"Error: {repr(datos.get('error'))}")

# Test 5: Usar el candidato que devuelve la búsqueda
print("\n" + "=" * 60)
print("TEST 5: Buscar candidato por nombre y extraer FSD")
print("=" * 60)

from data.api import HubSpotAPI

api = HubSpotAPI()
candidatos = api.buscar_contactos_por_criterio("Daisy", "nombre")

if candidatos:
    print(f"Se encontraron {len(candidatos)} candidato(s)")

    for i, c in enumerate(candidatos):
        print(f"\n  Candidato {i+1}:")
        print(f"    Nombre: {c.get('nombre')}")
        print(f"    id_cliente: {repr(c.get('id_cliente'))}")
        print(f"    fsd (antes): {repr(c.get('fsd'))}")

        # Intentar extraer FSD
        fsd = buscar_fsd_por_id_cliente(c.get("id_cliente", ""))
        print(f"    fsd (después de _buscar_fsd): {repr(fsd)}")
else:
    print("No se encontraron candidatos")

print("\n" + "=" * 60)
print("FIN DEL TEST")
print("=" * 60)
````

## File: ui/posicion_ventanas.py
````python
from __future__ import annotations

from core.monitors import obtener_monitores


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

## File: version.py
````python
__version__ = "0.1.1"
````

## File: config/configuracion.py
````python
import json
import os
import threading
from dataclasses import dataclass
from typing import Any

from utils.paths import resource_path
from core.monitors import (
    obtener_monitores,
    obtener_nombres_monitores,
    obtener_monitor_por_indice,
)
from core.browser import (
    PUERTO_DEBUG,
    CHROME_USER_DATA,
    CHROME_PATHS,
    obtener_chrome_exe,
)


TEMA_APARIENCIA = "dark"
TEMA_COLOR = "blue"


ARCHIVO_CONFIG = resource_path(os.path.join("config", "config.json"))
KEYRING_APP = "AutoCapturaApp"




@dataclass
class ToggleConfig:

    clave: str
    default: Any

    def cargar(self):
        config = cargar_config()
        return config.get(self.clave, self.default)

    def guardar(self, valor) -> None:
        config = cargar_config()
        config[self.clave] = valor
        guardar_config(config)

    def __call__(self):

        return self.cargar()




toggle_auto_submit = ToggleConfig("auto_submit_nota", True)
toggle_headless = ToggleConfig("headless", False)
toggle_chrome_existente = ToggleConfig("chrome_existente", True)
toggle_destino_subida = ToggleConfig("destino_subida", "AMBOS")




def cargar_auto_submit() -> bool:
    return toggle_auto_submit.cargar()

def guardar_auto_submit(valor: bool) -> None:
    toggle_auto_submit.guardar(valor)

def cargar_headless() -> bool:
    return toggle_headless.cargar()

def guardar_headless(valor: bool) -> None:
    toggle_headless.guardar(valor)

def cargar_chrome_existente() -> bool:
    return toggle_chrome_existente.cargar()

def guardar_chrome_existente(valor: bool) -> None:
    toggle_chrome_existente.guardar(valor)

def cargar_destino_subida() -> str:
    return toggle_destino_subida.cargar()

def guardar_destino_subida(valor: str) -> None:
    toggle_destino_subida.guardar(valor)



CLAVE_AUTO_SUBMIT = toggle_auto_submit.clave
AUTO_SUBMIT_DEFAULT = toggle_auto_submit.default
CLAVE_HEADLESS = toggle_headless.clave
HEADLESS_DEFAULT = toggle_headless.default
CLAVE_CHROME_EXISTENTE = toggle_chrome_existente.clave
CHROME_EXISTENTE_DEFAULT = toggle_chrome_existente.default
CLAVE_DESTINO_SUBIDA = toggle_destino_subida.clave
DESTINO_SUBIDA_DEFAULT = toggle_destino_subida.default



_config_cache: dict | None = None
_config_lock = threading.Lock()
_ultimo_error_config: str | None = None





def cargar_config() -> dict:













    global _config_cache
    with _config_lock:
        if _config_cache is not None:
            return dict(_config_cache)
    resultado: dict = {}
    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            resultado = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        ruta_backup = ARCHIVO_CONFIG + ".bak"
        try:
            with open(ruta_backup, "r", encoding="utf-8") as fb:
                resultado = json.load(fb)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    except Exception:
        pass
    with _config_lock:
        _config_cache = resultado
    return dict(resultado)


def _invalidar_cache_config() -> None:

    global _config_cache
    with _config_lock:
        _config_cache = None


_ultimo_error_config: str | None = None


def _obtener_ultimo_error_config() -> str | None:

    return _ultimo_error_config


def guardar_config(datos: dict) -> None:











    global _ultimo_error_config, _config_cache
    _ultimo_error_config = None
    with _config_lock:
        try:
            os.makedirs(os.path.dirname(ARCHIVO_CONFIG), exist_ok=True)
            tmp_path = ARCHIVO_CONFIG + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            if os.path.isfile(ARCHIVO_CONFIG):
                respaldo = ARCHIVO_CONFIG + ".bak"
                try:
                    with open(respaldo, "w", encoding="utf-8") as fb:
                        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as fo:
                            fb.write(fo.read())
                except Exception:
                    pass
            os.replace(tmp_path, ARCHIVO_CONFIG)
            _config_cache = dict(datos)
        except Exception as e:
            _ultimo_error_config = str(e)
            try:
                if os.path.isfile(ARCHIVO_CONFIG + ".tmp"):
                    os.unlink(ARCHIVO_CONFIG + ".tmp")
            except Exception:
                pass








CLAVE_PERFILES = "perfiles_region"



PERFIL_POR_DEFECTO = {"top": 392, "left": 524, "width": 934, "height": 404}


def cargar_perfiles() -> dict:






    config = cargar_config()
    return config.get(CLAVE_PERFILES, {})


def guardar_perfiles(perfiles: dict) -> None:










    config = cargar_config()
    config[CLAVE_PERFILES] = perfiles
    guardar_config(config)
````

## File: config/credenciales.py
````python
import pickle
import keyring
from pathlib import Path
from config.configuracion import KEYRING_APP
from utils.paths import get_project_root


_COOKIES_DIR = get_project_root() / "cookies"




def guardar_cookies(driver, sitio_nombre: str, carpeta: Path | None = None) -> None:












    dest = carpeta or _COOKIES_DIR
    dest.mkdir(exist_ok=True)
    ruta = dest / f"{sitio_nombre.replace(' ', '_')}.pkl"
    with open(ruta, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"[cookies] Guardadas en: {ruta}")


def cargar_cookies(
    driver, sitio: dict, url_base: str, carpeta: Path | None = None
) -> bool:
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
    carpeta  : directorio donde leer. Por defecto: <raíz>/cookies/
    """
    dest = carpeta or _COOKIES_DIR
    ruta = dest / f"{sitio['nombre'].replace(' ', '_')}.pkl"
    if not ruta.exists():
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
                print(f"[cookies] Omitida: {cookie.get('name')} — {e}")

    return True


# ── Credenciales en el llavero del SO ────────────────────────────────


def guardar_credenciales(sitio_nombre: str, usuario: str, clave: str) -> None:
    """
    Persiste usuario y contraseña en el llavero del sistema operativo.

    El llavero cifra los valores; nunca se escriben en texto plano en
    ningún archivo del proyecto.
    """
    try:
        keyring.set_password(KEYRING_APP, f"{sitio_nombre}_usuario", usuario)
        keyring.set_password(KEYRING_APP, f"{sitio_nombre}_clave", clave)
    except Exception as e:
        print(f"[credenciales] Error guardando en keyring: {e}")


def cargar_credenciales(sitio_nombre: str) -> tuple[str, str]:
    """
    Recupera usuario y contraseña desde el llavero del SO.

    Devuelve cadenas vacías si no se encuentran o si el keyring falla,
    para que el código llamador pueda verificar con `if not usuario`
    sin manejar None ni excepciones.
    """
    try:
        usuario = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_usuario") or ""
        clave = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_clave") or ""
    except Exception as e:
        print(f"[credenciales] Error leyendo de keyring: {e}")
        usuario, clave = "", ""
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
        ctk.set_appearance_mode(self._config.get("tema", "dark"))

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
        "en": "LS: {fecha}. A call was placed to the registered {number|numbers} {telefonos}, but {it is|they are} out of service. An email was sent as an alternative method of contact.",
    },
    "buzon_voz": {
        "titulo": "Buzón de Voz",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero la llamada fue enviada al buzón de voz. Se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers} {telefonos}, but the call went to voicemail. A text message and an email were sent.",
    },
    "no_contesta": {
        "titulo": "No Contesta",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers} {telefonos}, but did not answer. A text message and an email were sent as alternative methods of contact.",
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

    def _formatear_telefonos(self, telefonos: list[str], idioma: str = "es") -> str:
        if len(telefonos) == 1:
            return telefonos[0]

        conector = "and" if idioma == "en" else "y"

        if len(telefonos) == 2:
            return f"{telefonos[0]} {conector} {telefonos[1]}"

        return ", ".join(telefonos[:-1]) + f" {conector} {telefonos[-1]}"

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
            self._formatear_telefonos(telefonos, idioma) if requiere_telefonos else ""
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

## File: core/base_plugin.py
````python
from __future__ import annotations
import time
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
        return {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }


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
    driver: object  # WebDriver (tipado débil para no forzar selenium aquí)
    credenciales: dict = field(default_factory=dict)  # {"usuario": ..., "clave": ...}
    opciones: dict = field(
        default_factory=dict
    )
    fsd: str | None = None
    cancelado: object | None = None





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

    # ── Búsqueda de pestaña por FSD (compartido entre plugins) ────────

    def _encontrar_pestana_fsd(
        self, driver, log: Callable, fsd_objetivo: str | None = None
    ) -> bool:
        """
        Busca y activa la pestaña correspondiente al FSD objetivo.

        Si fsd_objetivo es None, delega en _encontrar_pestana_legacy().
        Si se proporciona, itera las pestañas abiertas buscando el FSD
        en el título y la URL (solo pestañas del dominio del plugin).

        Returns True si encontró/cambió a la pestaña correcta.
        """
        if not fsd_objetivo:
            return self._encontrar_pestana_legacy(driver, log)

        handles = driver.window_handles
        fsd_lower = fsd_objetivo.lower()
        fsd_sin_guion = fsd_lower.replace("fsd-", "fsd")
        fsd_numero = fsd_lower.replace("fsd-", "")

        log(
            f"  -> [{self.nombre}] Buscando pestaña con FSD: {fsd_objetivo} "
            f"({len(handles)} pestaña(s) abierta(s))..."
        )

        for handle in handles:
            try:
                driver.switch_to.window(handle)
                title = driver.title.lower()
                url = driver.current_url.lower()
            except Exception as e:
                if "no such execution context" in str(e).lower():
                    log(
                        f"  · [{self.nombre}] contexto inactivo en handle, intentando despertar..."
                    )
                    try:
                        driver.execute_cdp_cmd("Runtime.enable", {})
                        time.sleep(0.3)
                    except Exception:
                        pass
                    continue
                raise

            if self.dominio and self.dominio not in url:
                continue

            if fsd_lower in title or fsd_sin_guion in title:
                log(
                    f"  v [{self.nombre}] Pestaña encontrada por título: "
                    f"{driver.title}"
                )
                return True

            if fsd_numero in url:
                log(
                    f"  v [{self.nombre}] Pestaña encontrada por URL: "
                    f"{fsd_objetivo}"
                )
                return True

        log(f"  x [{self.nombre}] No se encontró pestaña para FSD: " f"{fsd_objetivo}")
        return False

    def _encontrar_pestana_legacy(self, driver, log: Callable) -> bool:
        """
        Modo legacy: búsqueda sin FSD específico.
        Override en plugins que necesiten lógica especial (ej: Sunrun).

        Por defecto, confía en la pestaña activa.
        """
        return True
````

## File: core/browser.py
````python
from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Callable

from selenium import webdriver
from subprocess import Popen
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("ssauto.browser")


PUERTO_DEBUG = 9222
CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
]

_chrome_exe_cache: str | None = None


_chromedriver_path: str | None = None


def _obtener_chromedriver_path() -> str:

    global _chromedriver_path
    if _chromedriver_path is not None and Path(_chromedriver_path).exists():
        return _chromedriver_path
    _chromedriver_path = ChromeDriverManager().install()
    return _chromedriver_path


def obtener_chrome_exe() -> str | None:

    global _chrome_exe_cache
    if _chrome_exe_cache is not None:
        return _chrome_exe_cache if os.path.isfile(_chrome_exe_cache) else None
    for p in CHROME_PATHS:
        if os.path.isfile(p):
            _chrome_exe_cache = p
            return p
    return None



_ultimo_chrome_proc: Popen | None = None


class ErrorBrowser(Exception):


    pass


class BrowserFactory:








    @classmethod
    def conectar_existente(cls, puerto: int = PUERTO_DEBUG) -> webdriver.Chrome:








        def puerto_activo_local():
            return puerto_activo("127.0.0.1", puerto)

        if not puerto_activo_local():
            chrome_path = obtener_chrome_exe()
            if not chrome_path:
                raise ErrorBrowser(f"Chrome no encontrado en el puerto: {puerto}.")

            global _ultimo_chrome_proc
            _ultimo_chrome_proc = Popen(
                [
                    chrome_path,
                    f"--remote-debugging-port={puerto}",
                    f"--user-data-dir={CHROME_USER_DATA}",
                    "--disable-popup-blocking",
                    "--disable-default-apps",
                ]
            )

            for intento in range(20):
                if puerto_activo_local():
                    break
                time.sleep(0.1 + intento * 0.05)

        opciones = webdriver.ChromeOptions()
        opciones.add_experimental_option("debuggerAddress", f"127.0.0.1:{puerto}")

        try:
            driver = webdriver.Chrome(
                service=Service(_obtener_chromedriver_path()),
                options=opciones,
            )
            _inyectar_antideteccion(driver)
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
                service=Service(_obtener_chromedriver_path()),
                options=opciones,
            )
            _inyectar_antideteccion(driver)
            return driver
        except Exception as e:
            raise ErrorBrowser(f"No se pudo abrir Chrome nuevo: {e}") from e

    @classmethod
    def crear(
        cls, headless: bool, usar_existente: bool, puerto: int = PUERTO_DEBUG
    ) -> webdriver.Chrome:
        """
        Punto de entrada unificado — elige el modo según los flags.

        Úsalo cuando la decisión depende de opciones del usuario (como en la UI).
        """
        if usar_existente:
            return cls.conectar_existente(puerto)
        return cls.nuevo(headless)

    # ── Antidetección ─────────────────────────────────────────────────


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
            logger.debug(
                f"Script antidetección no aplicado (esperado en Chrome moderno): {e}"
            )


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
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, WebDriverException

    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
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

## File: core/comparador.py
````python
import re
from rapidfuzz import fuzz
from data.api import HubSpotAPI, buscar_fsd_por_id_cliente






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
    """
    na = _norm(valor_hs)
    nb = _norm(valor_sr)

    # NUEVO: Normalizar separadores como espacios antes de tokenizar
    na = re.sub(r"[-/\\|]+", " ", na)
    nb = re.sub(r"[-/\\|]+", " ", nb)

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
























Encapsula las operaciones de busqueda y comparacion usadas por la UI."""

    def __init__(self, scraper=None):
        """
        Args:
            scraper: instancia de ScraperSunrun para DI en tests.
                     Si es None, se usa ScraperSunrun() bajo demanda.





Lazy init del scraper Sunrun (evita import en tests sin selenium)."""
        if self._scraper is not None:
            return self._scraper
        from scraping.sunrun import ScraperSunrun
        self._scraper = ScraperSunrun()
        return self._scraper

    def buscar_hubspot_por_estrategia(self, criterio, tipo_busqueda):
        """Envia la busqueda a HubSpotAPI."""
        return self.api.buscar_contactos_por_criterio(criterio, tipo_busqueda)

    def extraer_fsd_desde_candidato(self, candidato_hubspot):
        """
        Extrae el FSD de un candidato HubSpot.

        Estrategia:
        1. Si el candidato tiene campo 'fsd' directo -> usarlo
        2. Si tiene 'id_cliente' -> buscar FSD en tickets por id_goformz
        3. Si nada -> devolver vacio





























        Extrae FSD automaticamente, obtiene datos de HubSpot y Sunrun, y compara.




































































    Compara un campo individual entre HubSpot y Sunrun.

    Retorna un dict con:
      · campo       : nombre del campo
      · valor_hs    : valor en HubSpot (o "—" si vacío)
      · valor_sr    : valor en Sunrun (o "—" si vacío)
      · estado      : "igual", "similar", "diferente", "solo_hs", "solo_sunrun", "ambos_vacios"
      · similitud   : float entre 0.0 y 1.0
      · nota        : mensaje descriptivo






















































































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

## File: data/api.py
````python
import logging
import os
import re
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest as TicketSearchRequest
from hubspot.crm.contacts import PublicObjectSearchRequest as ContactSearchRequest
from hubspot.crm.tickets import ApiException as TicketApiException
from hubspot.crm.contacts import ApiException as ContactApiException
from data.hubspot_constants import (
    _T_FSD,
    _T_FIRSTNAME,
    _T_LASTNAME,
    _T_ID_GOFORMZ,
    _T_ADDRESS,
    _T_PHONE,
    _T_PHONE_ALT,
    _T_EMAIL,
    _T_COUNTY,
    _T_SUBJECT,
    _T_NOTA,
    _T_STATE,
    _T_ZIP,
    TICKET_PROPS,
    _C_FIRSTNAME,
    _C_LASTNAME,
    _C_ID_GOFORMZ,
    _C_ADDRESS,
    _C_PHONE,
    _C_PHONE_ALT,
    _C_EMAIL,
    _C_STATE,
    _C_STATE2,
    _C_MUNICIPIO,
    _C_MUNICIPIO_CO,
    _C_ZIP,
    CONTACT_PROPS,
    SEARCH_CONTACT_FIELDS,
    SEARCH_EXACT_FIELDS,
)

logger = logging.getLogger(__name__)

load_dotenv()





_client = None


def _get_client() -> HubSpot:

    global _client
    if _client is not None:
        return _client
    token = os.getenv("ACCESS_TOKEN") or ""
    if not token:
        raise RuntimeError(
            "ACCESS_TOKEN no configurado. "
            "Agrega ACCESS_TOKEN=<token> en el archivo .env del proyecto."
        )
    _client = HubSpot(access_token=token)
    return _client

# =========================================================
# HELPERS
# =========================================================


def _val(props: dict, key: str) -> str:
    v = props.get(key) or ""
    return v.strip()


def _limpiar_nombre(nombre: str) -> str:
    if not nombre:
        return ""

    if " / " in nombre:
        nombre = nombre.split(" / ")[0]

    elif "/" in nombre:
        nombre = nombre.split("/")[0]

    return nombre.strip()


def _parsear_asunto(asunto: str) -> dict:

    texto = asunto or ""

    # =====================================================
    # FSD
    # =====================================================

    fsd = ""

    m_fsd = re.search(
        r"\bFSD[-_\s]*(\d{4,})\b",
        texto,
        re.IGNORECASE,
    )

    if m_fsd:
        fsd = m_fsd.group(1)





    id_cliente = ""

    patrones = [
        r"\bID\s*[:
        r"\bCLIENTE\s*[:
        r"\bGOFORMZ\s*[:
    ]

    m_id = None
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)

        if m:
            id_cliente = m.group(1)
            m_id = m
            break







    nombre = ""

    try:
        if m_fsd and m_id:
            # extraer la sección entre el match de FSD y el match de ID
            start = m_fsd.end()
            end = m_id.start()
            mid = texto[start:end].strip(" -–—:\t\n\r")
            if mid:
                nombre = mid.strip()

        if not nombre:

            parts = re.split(r"[-–—|/]", texto)
            for p in parts:
                s = p.strip()
                if not s:
                    continue
                if re.search(r"\bFSD\b", s, re.IGNORECASE):
                    continue
                if re.search(r"\b(ID|CLIENTE|GOFORMZ)\b", s, re.IGNORECASE):
                    continue

                digits = re.sub(r"\D", "", s)
                if digits and len(digits) >= 3 and len(digits) / max(1, len(s)) > 0.4:
                    continue
                # heurística: debe contener letras y al menos una separación (nombre apellido)
                if re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", s) and len(s.split()) >= 1:
                    # preferir partes con 2 palabras
                    if len(s.split()) >= 2:
                        nombre = s
                        break
                    # si no hay partes con 2 palabras, tomar la primera válida
                    if not nombre:
                        nombre = s

        # limpiar nombre resultante (recortar separadores residuales)
        if nombre:
            nombre = nombre.strip()
            nombre = re.sub(r"^[\s\-–—_/:|]+|[\s\-–—_/:|]+$", "", nombre)
    except Exception:
        nombre = ""

    return {
        "fsd_parsed": fsd,
        "id_cliente": id_cliente,
        "nombre": nombre,
    }







class HubSpotAPI:


    def __init__(self, client=None):




        self.client = client if client is not None else _get_client()



    def _buscar_ticket_por_fsd(self, fsd: str):
        fsd_clean = fsd.strip()
        candidatos = [
            fsd_clean,
            fsd_clean.upper(),
            fsd_clean.replace(" ", ""),
            fsd_clean.upper().replace("-", ""),
        ]
        numeric_only = re.sub(r"\D", "", fsd_clean)
        if numeric_only:
            candidatos.append(numeric_only)
            candidatos.append(f"FSD-{numeric_only}")

        vistos = set()
        candidatos_finales = []
        for c in candidatos:
            if c not in vistos:
                vistos.add(c)
                candidatos_finales.append(c)

        for candidate in candidatos_finales:
            logger.info("Buscando ticket por FSD=%s", candidate)
            search_request = TicketSearchRequest(
                filter_groups=[{
                    "filters": [{
                        "propertyName": _T_FSD,
                        "operator": "EQ",
                        "value": candidate,
                    }]
                }],
                properties=TICKET_PROPS,
                limit=1,
            )
            try:
                response = self.client.crm.tickets.search_api.do_search(
                    public_object_search_request=search_request
                )
                if response.results:
                    ticket = response.results[0]
                    return {"ticket_id": ticket.id, "props": ticket.properties}
            except TicketApiException as e:
                logger.warning("Error buscando ticket FSD=%s: %s", candidate, e)
        return None

    def _buscar_contacto_por_id_goformz(self, id_goformz: str):
        if not id_goformz:
            return None
        search_request = ContactSearchRequest(
            filter_groups=[{
                "filters": [{
                    "propertyName": _C_ID_GOFORMZ,
                    "operator": "EQ",
                    "value": id_goformz,
                }]
            }],
            properties=CONTACT_PROPS,
            limit=1,
        )
        try:
            response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )
            if not response.results:
                return None
            contact = response.results[0]
            return {"contact_id": contact.id, "props": contact.properties}
        except ContactApiException as e:
            logger.warning("Error buscando contacto: %s", e)
            return None

    def _buscar_ticket_por_id_goformz(self, id_goformz: str):
        if not id_goformz:
            return None
        candidatos_id = [id_goformz]
        try:
            numero = int(id_goformz.replace(",", "").strip())
            con_coma = f"{numero:,}"
            if con_coma != id_goformz:
                candidatos_id.append(con_coma)
        except ValueError:
            pass

        for id_val in candidatos_id:
            search_request = TicketSearchRequest(
                filter_groups=[{
                    "filters": [{
                        "propertyName": _T_ID_GOFORMZ,
                        "operator": "EQ",
                        "value": id_val,
                    }]
                }],
                properties=TICKET_PROPS,
                limit=10,
            )
            try:
                response = self.client.crm.tickets.search_api.do_search(
                    public_object_search_request=search_request
                )
                if not response.results:
                    continue
                ticket_con_fsd = None
                ticket_fallback = None
                for ticket in response.results:
                    fsd_val = (ticket.properties or {}).get(_T_FSD, "")
                    if fsd_val and str(fsd_val).strip():
                        ticket_con_fsd = ticket
                        break
                    if ticket_fallback is None:
                        ticket_fallback = ticket
                ticket = ticket_con_fsd or ticket_fallback
                if ticket:
                    return {"ticket_id": ticket.id, "props": ticket.properties}
            except TicketApiException as e:
                logger.warning("Error buscando ticket por ID GoFormz=%s: %s", id_val, e)
        return None

    def buscar_fsd_por_id_cliente(self, id_cliente: str) -> str:

        if not id_cliente:
            return ""
        id_cliente_limpio = str(id_cliente).strip()
        if not id_cliente_limpio:
            return ""
        ticket = self._buscar_ticket_por_id_goformz(id_cliente_limpio)
        if not ticket:
            return ""
        props = ticket.get("props", {})
        fsd = props.get(_T_FSD, "")
        return str(fsd).strip() if fsd else ""

    def _buscar_fsd_por_contact_id(self, contact_id: str) -> str:
        """Busca el FSD de un ticket asociado a un contact_id."""
        if not contact_id:
            return ""
        contact_id_limpio = str(contact_id).strip()
        if not contact_id_limpio:
            return ""
        try:
            assoc_response = self.client.crm.associations.v4.basic_api.get_page(
                object_type="contacts",
                object_id=contact_id_limpio,
                to_object_type="tickets",
                limit=3,
            )
            if not assoc_response.results:
                return ""
            ticket_id = str(assoc_response.results[0].to_object_id)
            ticket = self.client.crm.tickets.basic_api.get_by_id(
                ticket_id=ticket_id,
                properties=[_T_FSD, _T_ID_GOFORMZ],
            )
            fsd = ticket.properties.get(_T_FSD, "")
            return str(fsd).strip() if fsd else ""
        except Exception as e:
            logger.warning("_buscar_fsd_por_contact_id(contact_id=%s): %s", contact_id, e)
            return ""

    def extraer_datos_hubspot(self, fsd: str):
        """Extrae todos los datos de un ticket HubSpot por FSD."""
        ticket_raw = self._buscar_ticket_por_fsd(fsd)
        if not ticket_raw:
            return {"error": f"No existe ticket para FSD={fsd}"}

        tp = ticket_raw["props"]
        ticket_id = ticket_raw["ticket_id"]
        asunto = _val(tp, _T_SUBJECT)
        parsed = _parsear_asunto(asunto)
        id_goformz = _val(tp, _T_ID_GOFORMZ) or parsed["id_cliente"]
        contacto_raw = self._buscar_contacto_por_id_goformz(id_goformz)
        cp = contacto_raw["props"] if contacto_raw else {}
        contact_id = contacto_raw["contact_id"] if contacto_raw else None

        nombre_contacto = (f"{_val(cp, _C_FIRSTNAME)} {_val(cp, _C_LASTNAME)}").strip()
        nombre_ticket = (f"{_val(tp, _T_FIRSTNAME)} {_val(tp, _T_LASTNAME)}").strip()
        nombre = nombre_contacto or nombre_ticket
        nombre = _limpiar_nombre(nombre)

        try:
            parsed_nombre = parsed.get("nombre") if isinstance(parsed, dict) else None
            if not nombre and parsed_nombre:
                nombre = parsed_nombre
        except Exception:
            pass

        return {
            "fsd": (_val(tp, _T_FSD) or parsed["fsd_parsed"] or fsd),
            "ticket_id": ticket_id,
            "contact_id": contact_id,
            "nombre": nombre,
            "id_cliente": (_val(cp, _C_ID_GOFORMZ) or id_goformz),
            "direccion": (_val(cp, _C_ADDRESS) or _val(tp, _T_ADDRESS)),
            "telefono": (_val(cp, _C_PHONE) or _val(tp, _T_PHONE)),
            "telefono_alterno": (_val(cp, _C_PHONE_ALT) or _val(tp, _T_PHONE_ALT)),
            "email": (_val(cp, _C_EMAIL) or _val(tp, _T_EMAIL)),
            "estado": (_val(cp, _C_STATE) or _val(cp, _C_STATE2) or _val(tp, _T_STATE)),
            "municipio": (
                _val(tp, _T_COUNTY) or _val(cp, _C_MUNICIPIO) or _val(cp, _C_MUNICIPIO_CO)
            ),
            "zip": (_val(cp, _C_ZIP) or _val(tp, _T_ZIP)),
            "nota": _val(tp, _T_NOTA),
            "error": None,
        }


    def buscar_contactos_por_criterio(self, criterio, tipo_busqueda):
        if tipo_busqueda == "fsd":
            datos = self.extraer_datos_hubspot(criterio)
            if datos.get("error"):
                return []
            return [datos]

        field = SEARCH_CONTACT_FIELDS.get(tipo_busqueda)
        if not field:
            return []

        query = str(criterio).strip()
        if not query:
            return []

        operator = "EQ" if tipo_busqueda in SEARCH_EXACT_FIELDS else "CONTAINS_TOKEN"

        search_request = ContactSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": field,
                            "operator": operator,
                            "value": query,
                        }
                    ]
                }
            ],
            properties=[
                "firstname",
                "lastname",
                "email",
                "phone",
                "telefono_alterno_del_cliente",
                "direccion__fisica_",
                "id_de_goformz__contacto_",
                "municipio_de_residencia",
                "municipios_co__contacto_",
                "country",
                "state",
                "zip",
            ],
            limit=10,
        )

        try:
            response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )

            candidatos = []
            for contacto in response.results:
                props = contacto.properties or {}
                id_cliente = props.get("id_de_goformz__contacto_", "")

                candidato = {
                    "contact_id": contacto.id,
                    "nombre": (
                        f"{props.get('firstname', '')} {props.get('lastname', '')}"
                    ).strip(),
                    "email": props.get("email", ""),
                    "telefono": props.get("phone", ""),
                    "telefono_alterno": props.get("telefono_alterno_del_cliente", ""),
                    "direccion": props.get("direccion__fisica_", ""),
                    "municipio": (
                        props.get("municipio_de_residencia", "")
                        or props.get("municipios_co__contacto_", "")
                    ),
                    "estado": (props.get("country", "") or props.get("state", "")),
                    "zip": props.get("zip", ""),
                    "id_cliente": id_cliente,
                    "fsd": "",
                }

                if id_cliente and str(id_cliente).strip():
                    fsd = self.buscar_fsd_por_id_cliente(str(id_cliente).strip())
                    candidato["fsd"] = fsd
                else:
                    fsd = self._buscar_fsd_por_contact_id(contacto.id)
                    candidato["fsd"] = fsd

                candidatos.append(candidato)
            return candidatos

        except ContactApiException as e:
            logger.warning("Error buscando contactos: %s", e)
            return []






def buscar_fsd_por_id_cliente(id_cliente: str) -> str:

    return HubSpotAPI().buscar_fsd_por_id_cliente(id_cliente)


def extraer_datos_hubspot(fsd: str):

    return HubSpotAPI().extraer_datos_hubspot(fsd)






if __name__ == "__main__":

    import sys

    fsd_test = sys.argv[1] if len(sys.argv) > 1 else "983316"

    datos = extraer_datos_hubspot(fsd_test)

    print()

    for k, v in datos.items():
        print(f"{k:<25}: {v}")

    print()
````

## File: plugins/sunrun.py
````python
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









    @property
    def nombre(self) -> str:
        return "SUNRUN"

    @property
    def necesita_login(self) -> bool:
        return True

    @property
    def usar_pagina_actual(self) -> bool:


        return True

    @property
    def dominio(self) -> str:
        return "sunrun.my.site.com"



    URL_LOGIN = "https://sunrun.my.site.com/partner/login?locale=us"
    SEL_USER = "#username"
    SEL_PASS = "#password"
    SEL_BTN_LOGIN = "#Login"


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



    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:

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

            log("  → [Sunrun] Refrescando página para limpiar estado…")
            driver.refresh()
            esperar_carga(driver, timeout=15)


            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, self.SEL_RELATED))
                )
                log("  ✓ [Sunrun] Componentes de Salesforce cargados.")
            except TimeoutException:
                log("  ⚠ [Sunrun] RELATED no detectado tras refresh — continuando igual.")


            self._clic_related(driver, log)

            if _check():
                log("  ⚠ [Sunrun] Cancelado antes de enviar archivo.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")


            self._enviar_archivo(driver, log, ruta_abs)

            if _check():
                log("  ⚠ [Sunrun] Cancelado antes de confirmar subida.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")


            ok = self._confirmar_subida(driver, log, ruta_abs)
            if ok:
                if _check():
                    log("  ⚠ [Sunrun] Cancelado antes de cerrar modal.")
                    return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")


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


        log("  → [Sunrun] Buscando pestaña RELATED…")


        self._cerrar_modal_residual(driver, log)

        espera = WebDriverWait(driver, self.TIMEOUT)
        try:
            btn_related = espera.until(
                EC.presence_of_element_located((By.XPATH, self.SEL_RELATED))
            )


            driver.execute_script("arguments[0].scrollIntoView(true);", btn_related)


            espera.until(EC.element_to_be_clickable((By.XPATH, self.SEL_RELATED)))


            try:
                btn_related.click()
                log("  ✓ [Sunrun] Clic en RELATED (click normal).")
            except Exception as e:

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































        Espera que la subida termine y hace clic en DONE.
        Retorna True si se hizo clic, False si no se pudo cerrar el modal.







































































        Espera a que cualquier spinner o barra de progreso de subida desaparezca.
        Salesforce procesa el archivo en background incluso después de mostrar
        '1 of 1 file uploaded'; si se cierra el modal antes de que termine,
        el archivo no queda asociado al registro.




















        Salesforce procesa el archivo tras el send_keys.
        Esperamos a que el nombre del archivo aparezca listado en el modal
        como señal de que la subida se completó.

        Si el selector específico no aparece, hace fallback a timeout fijo
        asumiendo que Salesforce procesó silenciosamente.
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


    XPATH_ACTIVIDADES = [
        "//a[contains(@data-tab-id,'activity') or contains(@data-tab-id,'1')]",
        "//a[contains(@href,'activity') and contains(@class,'tab')]",
        "//a[contains(text(),'Actividades') or contains(text(),'Activities')]",
        "//button[contains(text(),'Actividades') or contains(text(),'Activities')]",
        "//*[@role='tab' and (contains(text(),'Actividades') or contains(text(),'Activities'))]",
        "//a[contains(@aria-label,'Activities') or contains(@aria-label,'Actividades')]",
    ]


    XPATH_NOTAS = [
        "//button[contains(text(),'Notas') or contains(text(),'Notes')]",
        "//a[contains(text(),'Notas') or contains(text(),'Notes')]",
        "//*[contains(@data-test-id,'note') or contains(@data-test-id,'Note')]",
        "//*[contains(@aria-label,'Note') or contains(@aria-label,'Nota')]",
        "//span[contains(text(),'Notas') or contains(text(),'Notes')]/..",
    ]

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

        log(f"  → [HubSpot] Iniciando subida: {ruta_abs}")
        esperar_carga(driver)

        try:
            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._validar_contexto_activo(driver, contexto_activo)
            self._paso_actividades(driver, log, contexto_activo)

            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_notas(driver, log, contexto_activo)

            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_crear_nota(driver, log, contexto_activo)

            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_editor(driver, log, contexto_activo)

            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_adjuntar(driver, log, ruta_abs, contexto_activo)

            if _check():
                log("  ⚠ [HubSpot] Cancelado.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
                )

            self._paso_esperar_archivo(driver, log, ruta_abs, contexto_activo)

            if not auto_submit:
                log("  ✓ [HubSpot] Archivo adjunto. Guardado manual pendiente.")
                return ResultadoSubida(
                    exitoso=True, mensaje="Archivo adjunto (guardado manual)"
                )

            if _check():
                log("  ⚠ [HubSpot] Cancelado antes de guardar.")
                return ResultadoSubida(
                    exitoso=False, mensaje="Cancelado por el usuario."
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


            session = driver.execute_cdp_cmd(
                "Target.attachToTarget", {"targetId": target_id, "flatten": True}
            )
            session_id = session.get("sessionId")
            if not session_id:
                log("  · [HubSpot] CDP: no se obtuvo sessionId.")
                return False


            driver.execute_cdp_cmd("Runtime.enable", {})
            time.sleep(0.3)


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

                    try:
                        handle_actual = driver.current_window_handle
                        ctx = {
                            "handle": handle_actual,
                            "url": url,
                            "title": title,
                        }
                        log(f"  ✓ [HubSpot] Contexto activo (CDP): {handle_actual}")
                        return ctx
                    except Exception as e:
                        log(f"  · [HubSpot] No se pudo obtener handle actual: {e}")

                    for handle in driver.window_handles:
                        try:
                            driver.switch_to.window(handle)
                            ctx = {"handle": handle, "url": url, "title": title}
                            log(f"  ✓ [HubSpot] Contexto por fallback handle: {handle}")
                            return ctx
                        except Exception:
                            continue

        except Exception as e:
            log(f"  · [HubSpot] CDP falló: {str(e)[:80]}")

        raise RuntimeError(
            "No se encontró ninguna pestaña de un registro (ticket/contacto). "
            "Abre el ticket de HubSpot en Chrome antes de ejecutar."
        )

    def _validar_contexto_activo(self, driver, ctx: dict) -> None:
        url_conocida = ctx.get("url", "")
        if url_conocida and self.dominio in url_conocida:
            return

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


























        Da foco al editor e inserta texto vía JS para que React habilite el toolbar.
        Sin este paso el FileButton no aparece en el DOM.

















                    var el = arguments[0];
                    el.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('insertText', false, 'Nota de captura.');
                    ['input', 'change', 'keyup'].forEach(function(t) {
                        el.dispatchEvent(new Event(t, { bubbles: true }));
                    });
````

## File: services/sesion_service.py
````python
from __future__ import annotations

from typing import Callable

from core.base_plugin import ContextoSubida, ResultadoSubida
from core.plugin_registry import PluginRegistry
from utils.fsd import normalizar_fsd
from services.driver_provider import DriverProvider
from services.session_manager import SessionManager


class SesionService:
















    def __init__(self, driver_provider=None):




        self._driver_provider = driver_provider or DriverProvider()

    def ejecutar_subida(
        self,
        nombre_plugin: str,
        ruta_imagen: str,
        log: Callable[[str], None],
        headless: bool = False,
        usar_chrome_existente: bool = True,
        credenciales_sesion: dict | None = None,
        opciones: dict | None = None,
        fsd: str | None = None,
        cancel_event: object | None = None,
    ) -> ResultadoSubida:






        plugin = PluginRegistry.obtener(nombre_plugin)
        driver = None
        driver_propio = False

        try:

            driver, driver_propio = self._driver_provider.obtener(
                log, headless, usar_chrome_existente
            )

            if cancel_event and hasattr(cancel_event, 'is_set') and cancel_event.is_set():
                log(f"  ⚠ [{nombre_plugin}] Cancelado antes de iniciar sesión.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # 2. Asegurar sesion
            session = SessionManager(driver)
            session.asegurar(plugin, log, credenciales_sesion or {})

            if cancel_event and hasattr(cancel_event, 'is_set') and cancel_event.is_set():
                log(f"  ⚠ [{nombre_plugin}] Cancelado antes de subir.")
                return ResultadoSubida(exitoso=False, mensaje="Cancelado por el usuario.")

            # 3. Llamar al plugin
            credenciales = SessionManager._obtener_credenciales(
                plugin.nombre, credenciales_sesion or {}
            )
            fsd_normalizado = normalizar_fsd(fsd)
            ctx = ContextoSubida(
                ruta_imagen=ruta_imagen,
                log=log,
                driver=driver,
                credenciales=credenciales,
                opciones=opciones or {},
                fsd=fsd_normalizado,
                cancelado=cancel_event,
            )
            log(f"  -> [{plugin.nombre}] Iniciando subida...")
            resultado = plugin.subir(ctx)

            if resultado.exitoso:
                log(f"  v [{plugin.nombre}] {resultado.mensaje}")
            else:
                log(f"  x [{plugin.nombre}] {resultado.mensaje}")

            return resultado

        except Exception as e:
            log(f"  x [{nombre_plugin}] Error inesperado: {e}")
            return ResultadoSubida(exitoso=False, mensaje=str(e))

        finally:
            if driver_propio and driver:
                try:
                    driver.quit()
                    log(f"  . [{nombre_plugin}] Chrome cerrado.")
                except Exception:
                    pass
````

## File: config/config.json
````json
{
  "tema": "dark",
  "ultimo_monitor": 0,
  "regiones_apps": {
    "Wolkbox": {
      "top": 280,
      "left": 104,
      "width": 341,
      "height": 105
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
    },
    "B2Chat": {
      "top": 375,
      "left": 1109,
      "width": 0,
      "height": 0
    },
    "Correo": {
      "top": 296,
      "left": 1452,
      "width": 226,
      "height": 121
    }
  },
  "keybind": "<Control-p>",
  "perfiles_region": {
    "Monitor 1": {
      "monitor_index": 1
    },
    "Monitor 2": {
      "monitor_index": 1
    }
  },
  "auto_submit_nota": false,
  "monitores_apps": {
    "Wolkbox": 1,
    "App 5": 0,
    "B2Chat": 0,
    "Calendar": 0
  },
  "headless": false,
  "chrome_existente": true,
  "destino_subida": "HUBSPOT",
  "ultima_celda_calendar": "g20",
  "ultima_pestana_calendar": "Jun"
}
````

## File: ui/ventana_comparacion.py
````python
import customtkinter as ctk
from ui.custom_ctkframe import CustomCTkFrame
from core.comparador import Comparador, comparar
from config.configuracion import cargar_config
from data.buscador import SEARCH_STRATEGIES
from ui.comparacion.tema import COLORES_ESTADO, ETIQUETAS_ESTADO, DISPATCH_STATES, info_dispatch_state






class VentanaComparacion(CustomCTkFrame):
















    def __init__(
        self,
        parent,
        datos_hubspot: dict = None,
        datos_sunrun: dict = None,
        log_callback=None,
        comparador=None,
        ventana_principal_o_comparador=None,
    ):

        super().__init__(parent)
        self._log_ext = log_callback or (lambda m: None)
        self._datos_hs = datos_hubspot
        self._datos_sr = datos_sunrun

        self.comparador = comparador

        if self.comparador is None and ventana_principal_o_comparador is not None:
            if hasattr(ventana_principal_o_comparador, "comparador"):
                self.comparador = ventana_principal_o_comparador.comparador
            else:
                self.comparador = ventana_principal_o_comparador

        if self.comparador is None and hasattr(parent, "comparador"):
            self.comparador = parent.comparador

        if self.comparador is None:
            self.comparador = Comparador()

        self.update_idletasks()
        ancho, alto = 820, 560
        px = max(0, (self.winfo_screenwidth() - ancho) // 2)
        py = max(0, (self.winfo_screenheight() - alto) // 2)
        self.search_strategy = "fsd"
        self.candidatos_hubspot = []
        self.candidato_seleccionado = None
        self.radio_var = ctk.IntVar()
        self.criterio_inputs = []
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



        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)


        enc = ctk.CTkFrame(self, fg_color=("gray88", "gray20"), height=50)
        enc.grid(row=0, column=0, sticky="ew")
        enc.grid_propagate(False)

        ctk.CTkLabel(
            enc,
            text="  🔍  Comparación de datos: HubSpot ↔ Sunrun",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=16, pady=12)


        frame_busqueda = ctk.CTkFrame(self, fg_color=("gray95", "gray18"))
        frame_busqueda.grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 0))

        frame_busqueda.grid_columnconfigure(0, weight=0)
        frame_busqueda.grid_columnconfigure(1, weight=1)


        ctk.CTkLabel(
            frame_busqueda,
            text="Tipo de Búsqueda",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 4))



        estrategias = [v["label"] for v in SEARCH_STRATEGIES.values()]

        self.combo_tipo_busqueda = ctk.CTkComboBox(
            frame_busqueda,
            values=estrategias,
            state="readonly",
            height=34,
            width=220,
            font=ctk.CTkFont(size=12),
            command=self._al_cambiar_tipo_busqueda,
        )

        self.combo_tipo_busqueda.grid(
            row=1, column=0, sticky="w", padx=(14, 8), pady=(0, 14)
        )

        self.combo_tipo_busqueda.set(SEARCH_STRATEGIES["fsd"]["label"])


        def _abrir_combo(e):
            self.combo_tipo_busqueda._open_dropdown_menu()

        self.combo_tipo_busqueda.bind("<Button-1>", _abrir_combo)
        for hijo in self.combo_tipo_busqueda.winfo_children():
            hijo.bind("<Button-1>", _abrir_combo)


        self.frame_inputs = ctk.CTkFrame(frame_busqueda, fg_color="transparent")

        self.frame_inputs.grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=(0, 14))

        self.frame_inputs.grid_columnconfigure(0, weight=1)





        self._btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="🔍 Buscar en HubSpot",
            command=self._buscar_candidatos,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )

        self._btn_buscar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 14))


        self._frame_main = ctk.CTkFrame(self, fg_color="transparent")

        self._frame_main.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 0),
        )
        self._frame_main.grid_rowconfigure(3, weight=1)
        self._frame_main.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self._frame_main,
            text="Resultados en HubSpot",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.frame_tabla = ctk.CTkFrame(
            self._frame_main,
            fg_color=("gray95", "gray18"),
            height=120,
        )

        self.frame_tabla.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )
        self.frame_tabla.grid_propagate(False)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        self._label_placeholder_tabla = ctk.CTkLabel(
            self.frame_tabla,
            text="No hay resultados todavía.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

        self._label_placeholder_tabla.grid(
            row=0,
            column=0,
            pady=30,
        )

        self._btn_comparar = ctk.CTkButton(
            self._frame_main,
            text="▶ Comparar Seleccionado",
            command=self._lanzar_comparacion_mejorada,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#1976D2", "#1565C0"),
            hover_color=("#1565C0", "#0D47A1"),
        )

        self._btn_comparar.grid(row=2, column=0, sticky="ew", pady=(10, 10))


        self._frame_resultados = ctk.CTkScrollableFrame(
            self._frame_main,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )

        self._frame_resultados.grid(row=3, column=0, sticky="nsew")

        self._frame_resultados.grid_columnconfigure(0, weight=1)


        self._label_placeholder = ctk.CTkLabel(
            self._frame_resultados,
            text="Selecciona un candidato y presiona Comparar.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

        self._label_placeholder.grid(row=0, column=0, pady=40)


        self._al_cambiar_tipo_busqueda(SEARCH_STRATEGIES[self.search_strategy]["label"])


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

    def ui_log(self, mensaje: str, tipo: str = "info"):




        self._status_var.set(mensaje)


        print(f"[{tipo.upper()}] {mensaje}")

        # Refrescar UI
        self.update_idletasks()

    def _al_cambiar_tipo_busqueda(self, nuevo_tipo_label):
        """Se dispara cuando cambia el dropdown de tipo de búsqueda"""

        # Encontrar la clave del tipo seleccionado
        self.search_strategy = [
            k for k, v in SEARCH_STRATEGIES.items() if v["label"] == nuevo_tipo_label
        ][0]


        for widget in self.frame_inputs.winfo_children():
            widget.destroy()


        estrategia = SEARCH_STRATEGIES[self.search_strategy]
        input_count = estrategia["input_count"]

        self.criterio_inputs = []

        if input_count == 1:
            entrada = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder", "Buscar..."),
                height=34,
                font=ctk.CTkFont(size=12),
            )
            entrada.pack(fill="x")
            entrada.bind("<Return>", lambda e: self._buscar_candidatos())
            self.criterio_inputs.append(entrada)

        elif input_count == 2:
            entrada1 = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder_1", "Campo 1"),
                height=34,
                font=ctk.CTkFont(size=12),
            )
            entrada1.pack(fill="x", pady=(0, 5))
            entrada1.bind("<Return>", lambda e: self._buscar_candidatos())
            self.criterio_inputs.append(entrada1)

            entrada2 = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder_2", "Campo 2"),
                height=34,
                font=ctk.CTkFont(size=12),
            )
            entrada2.pack(fill="x")
            entrada2.bind("<Return>", lambda e: self._buscar_candidatos())
            self.criterio_inputs.append(entrada2)

    def _obtener_criterio_busqueda(self):


        estrategia = SEARCH_STRATEGIES[self.search_strategy]
        input_count = estrategia["input_count"]

        if input_count == 1:
            return self.criterio_inputs[0].get()
        elif input_count == 2:
            return {
                "criterio1": self.criterio_inputs[0].get(),
                "criterio2": self.criterio_inputs[1].get(),
            }

    def _buscar_candidatos(self):

        criterio = self._obtener_criterio_busqueda()

        if not criterio or (isinstance(criterio, dict) and not all(criterio.values())):
            self.ui_log("❌ Rellena todos los campos de búsqueda", "error")
            return

        self.ui_log("🔄 Buscando en HubSpot...", "info")

        try:
            self.candidatos_hubspot = self.comparador.buscar_hubspot_por_estrategia(
                criterio, self.search_strategy
            )

            if not self.candidatos_hubspot:
                self.ui_log("❌ No se encontraron resultados", "warning")
                return

            self._mostrar_candidatos()
            self.ui_log(
                f"✅ Se encontraron {len(self.candidatos_hubspot)} resultado(s)",
                "success",
            )

        except Exception as e:
            self.ui_log(f"❌ Error en búsqueda: {str(e)}", "error")

    def _mostrar_candidatos(self):

        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        self.radio_var.set(-1)

        for idx, candidato in enumerate(self.candidatos_hubspot):
            frame_fila = ctk.CTkFrame(
                self.frame_tabla,
                fg_color=("#e8e8e8", "#2a2a2a"),
                corner_radius=5,
                cursor="hand2",
            )
            frame_fila.pack(fill="x", pady=3, padx=5)

            def seleccionar(e, i=idx):
                self.radio_var.set(i)

            rb = ctk.CTkRadioButton(
                frame_fila, text="", variable=self.radio_var, value=idx
            )
            rb.pack(side="left", padx=5)

            nombre = candidato.get("nombre", "N/A")
            direccion = candidato.get("direccion", "N/A")
            municipio = candidato.get("municipio", "N/A")
            fsd = candidato.get("fsd", "N/A")

            info_text = f"{nombre} | {direccion} | {municipio} | FSD: {fsd}"

            lbl = ctk.CTkLabel(
                frame_fila,
                text=info_text,
                font=("Segoe UI", 10),
                text_color=("#333333", "#CCCCCC"),
                justify="left",
                cursor="hand2",
            )
            lbl.pack(side="left", padx=10, fill="x", expand=True)


            frame_fila.bind("<Button-1>", seleccionar)
            lbl.bind("<Button-1>", seleccionar)

    def _obtener_candidato_seleccionado(self):

        idx = self.radio_var.get()
        if idx >= 0 and idx < len(self.candidatos_hubspot):
            return self.candidatos_hubspot[idx]
        return None

    def _lanzar_comparacion_mejorada(self):

        candidato = self._obtener_candidato_seleccionado()

        if not candidato:
            self.ui_log("⚠️  Selecciona un candidato para comparar", "warning")
            return

        self.ui_log("🔄 Extrayendo FSD y buscando en Sunrun...", "info")

        try:
            resultado = self.comparador.comparar_con_fsd_automatico(candidato)

            if "error" in resultado:
                self.ui_log(f"❌ {resultado['error']}", "error")
                return

            self._mostrar_resultado(resultado)
            self.ui_log("✅ Comparación completada", "success")

        except Exception as e:
            self.ui_log(f"❌ Error en comparación: {str(e)}", "error")

    def _limpiar_resultados(self):
        for widget in self._frame_resultados.winfo_children():
            widget.destroy()

    def _mostrar_resultado_externo(self):

        resultado = comparar(self._datos_hs, self._datos_sr)

        resultado["_sunrun_extra"] = {
            "dispatch_state": self._datos_sr.get("dispatch_state", ""),
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


        self._btn_copiar = ctk.CTkButton(
            hdr,
            text="📋 Copiar",
            width=90,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            border_width=1,
            border_color=("gray60", "gray50"),
            text_color=("gray30", "gray70"),
            hover_color=("gray80", "gray30"),
            command=lambda r=resultado: self._copiar_resultado(r),
        )
        self._btn_copiar.grid(row=0, column=1, sticky="e", padx=14, pady=8)

        fila += 1
        sunrun_extra = resultado.get("_sunrun_extra")
        hubspot_extra = resultado.get("_hubspot_extra")

        if sunrun_extra or hubspot_extra:
            container = ctk.CTkFrame(frame, fg_color="transparent")
            container.grid(row=fila, column=0, sticky="ew", pady=(0, 8))
            container.grid_columnconfigure((0, 1), weight=1, uniform="info")

        if sunrun_extra:
            estado_dispatch = sunrun_extra.get("dispatch_state", "").strip().upper()
            _, _, (header_color, frame_color) = info_dispatch_state(estado_dispatch)

            sr_frame = ctk.CTkFrame(
                container,
                fg_color=frame_color,
                border_width=1,
            )

            sr_frame.grid(
                row=0,
                column=0,
                sticky="nsew",
                padx=(0, 4),
            )

            sr_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                sr_frame,
                text="☀ Sunrun",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=header_color,
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=14,
                pady=(10, 6),
            )

            campos_extra = [
                ("Dispatch State", sunrun_extra.get("dispatch_state", "")),
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

                color = None
                font_weight = "normal"

                if label == "Dispatch State":
                    estado = str(valor).strip().upper()
                    color_ds, sufijo, _ = info_dispatch_state(estado)
                    if color_ds:
                        color = color_ds
                        font_weight = "bold"
                        valor = f"{valor}{sufijo}"

                ctk.CTkLabel(
                    sr_frame,
                    text=valor or "-",
                    font=ctk.CTkFont(size=11, weight=font_weight),
                    wraplength=280,
                    justify="left",
                    anchor="w",
                    text_color=color,
                ).grid(
                    row=idx,
                    column=1,
                    sticky="ew",
                    padx=(0, 14),
                    pady=2,
                )



        if hubspot_extra:
            col_hs = 1 if sunrun_extra else 0
            padx_hs = (4, 0) if sunrun_extra else (0, 0)

            hs_frame = ctk.CTkFrame(
                container,
                fg_color=("#ffe5cc", "#3a2a1a"),
                border_width=1,
            )

            hs_frame.grid(
                row=0,
                column=col_hs,
                sticky="nsew",
                padx=padx_hs,
            )

            hs_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                hs_frame,
                text="⬡ HubSpot",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("#804000", "#f0a050"),
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=14,
                pady=(10, 6),
            )

            campos_hs = [
                ("Ticket ID", hubspot_extra.get("ticket_id", "")),
                ("Contact ID", hubspot_extra.get("contact_id", "")),
            ]

            for idx, (label, valor) in enumerate(campos_hs, start=1):
                if not valor:
                    continue

                ctk.CTkLabel(
                    hs_frame,
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
                    hs_frame,
                    text=str(valor),
                    font=ctk.CTkFont(size=11),
                    wraplength=280,
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

    def _copiar_resultado(self, resultado: dict):

        lineas = []
        lineas.append(f"COMPARACIÓN FSD: {resultado.get('fsd', '')}")
        lineas.append("=" * 50)

        # Datos Sunrun extra
        sunrun_extra = resultado.get("_sunrun_extra", {})
        if sunrun_extra:
            lineas.append("\n☀ SUNRUN")
            for k, v in sunrun_extra.items():
                if v:
                    lineas.append(f"  {k.replace('_', ' ').title()}: {v}")

        # Campos comparados
        lineas.append("\n📋 CAMPOS COMPARADOS")
        lineas.append(f"{'Campo':<20} {'HubSpot':<25} {'Sunrun':<25} Estado")
        lineas.append("-" * 80)
        for cr in resultado.get("campos", []):
            campo = str(cr.get("campo", "")).ljust(20)
            val_hs = str(cr.get("valor_hs") or "-").ljust(25)
            val_sr = str(cr.get("valor_sr") or "-").ljust(25)
            estado = ETIQUETAS_ESTADO.get(cr.get("estado", ""), cr.get("estado", ""))
            lineas.append(f"{campo} {val_hs} {val_sr} {estado}")

        # Resumen
        resumen = resultado.get("resumen", {})
        if resumen:
            lineas.append("\n📊 RESUMEN")
            for estado, count in resumen.items():
                if count:
                    lineas.append(f"  {ETIQUETAS_ESTADO.get(estado, estado)}: {count}")

        texto = "\n".join(lineas)

        try:
            self.clipboard_clear()
            self.clipboard_append(texto)

            self._btn_copiar.configure(text="✅ Copiado", state="disabled")
            self.after(
                2000,
                lambda: self._btn_copiar.configure(text="📋 Copiar", state="normal"),
            )
        except Exception as e:
            self.ui_log(f"No se pudo copiar: {e}", "error")

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

## File: .gitignore
````
__pycache__/
.pytest_cache/
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

# gsheets — auto-generated + secrets
gsheets/sessions/
gsheets/screenshots/
gsheets/*.json
````

## File: readme.md
````markdown
# SSAuto

## Descripción

SSAuto es una herramienta de escritorio para Windows que automatiza capturas de pantalla de regiones específicas y las sube a portales web (HubSpot y Sunrun). Incluye un comparador de datos entre HubSpot y Sunrun con visualización de estado de dispatch, un generador de mensajes de contacto estandarizados, y botones de captura rápida para múltiples aplicaciones.

Combina `customtkinter` (GUI), `mss` (captura de pantalla) y `Selenium` (automatización de navegador). La arquitectura es modular, con un sistema de plugins para agregar nuevos sitios de destino.

## Estructura del proyecto

```
ssauto/
├── main.py                         # Punto de entrada (registro de plugins, UI)
├── version.py                      # Versión (0.1.1)
├── requirements.txt                # Dependencias del proyecto
├── .env                            # Variables de entorno (tokens, credenciales)
├── AGENTS.md                       # Instrucciones para agentes de IA
├── doku.md                         # Documentación y bitácora de desarrollo
├── GENERADOR_MENSAJES.md           # Documentación del generador de mensajes
├── image.png                       # Favicon de la aplicación
├── LICENSE                         # Licencia MIT
├── repomix.config.json             # Configuración de empaquetado Repomix
├── SELECTORES_SUNRUN.HTML          # Selectores alternativos de Sunrun (referencia)
│
├── config/
│   ├── configuracion.py            # Configuración global, carga/guardado
│   ├── credenciales.py             # Keyring + serialización de cookies
│   ├── apps_captura.py             # Apps de captura rápida (Wolkbox, B2Chat, etc.)
│   ├── config.json                 # Configuración de runtime
│   ├── config.json.bak             # Backup automático de configuración
│   └── plantillas.json             # Plantillas de mensajes
│
├── core/
│   ├── base_plugin.py              # Contrato ABC para plugins de sitios
│   ├── plugin_registry.py          # Registro estático de plugins
│   ├── browser.py                  # Factoría de Chrome/Selenium
│   ├── captura.py                  # Servicio de captura de pantalla (mss)
│   ├── comparador.py               # Motor de comparación HubSpot vs Sunrun
│   ├── medidor_code.py             # Código del medidor visual ejecutado como subproceso
│   ├── medidor_runner.py           # Ejecutor del medidor de región visual
│   └── monitors.py                 # Detección de monitores (mss)
│
├── services/
│   ├── driver_provider.py          # Factoría de drivers Chrome (nuevo/existente/puerto 9222)
│   ├── sesion_service.py           # Orquestación de subida (UI ↔ plugins)
│   └── session_manager.py          # Gestión de sesiones y cookies por plugin
│
├── scraping/
│   ├── sunrun.py                   # Scraper de datos de Sunrun (Salesforce)
│   └── sunrun_selectors.py         # Selectores XPath/CSS centralizados para Sunrun
│
├── plugins/
│   ├── hubspot.py                  # Plugin de subida a HubSpot
│   ├── sunrun.py                   # Plugin de subida a Sunrun (Salesforce)
│   └── template_new_site.py        # Plantilla para crear nuevos plugins
│
├── ui/
│   ├── ventana_principal.py        # Ventana principal (captura, regiones, ajustes)
│   ├── ventana_comparacion.py      # Comparación de datos HubSpot ↔ Sunrun
│   ├── ventana_credenciales.py     # Formulario de credenciales por sitio
│   ├── ventana_plantillas.py       # Editor de plantillas de mensajes
│   ├── ventana_generador_mensajes.py # Generador de mensajes de contacto
│   ├── template_filler.py          # Utilidades de relleno de plantillas (plural/singular)
│   ├── custom_ctkframe.py          # CTkFrame extendido (conveniencia)
│   ├── posicion_ventanas.py        # Posicionamiento de ventanas hijas
│   ├── comparacion/
│   │   └── tema.py                 # Colores de estado y dispatch states (trabajable/no)
│   └── widgets/
│       ├── coordinate_inputs.py    # Inputs de coordenadas (x, y, w, h)
│       ├── log_widget.py           # Widget de registro (CTkTextbox)
│       ├── monitor_selector.py     # Selector de monitor
│       └── profile_manager.py      # Gestor de perfiles de región
│
├── data/
│   ├── api.py                      # Cliente de HubSpot REST API
│   ├── buscador.py                 # Estrategias de búsqueda de contactos
│   ├── hubspot_constants.py        # Constantes de propiedades HubSpot (tickets/contactos)
│   ├── PROPIEDADES DE CONTACTO.TXT # Referencia de propiedades de contacto HubSpot
│   ├── PROPIEDADES DE TICKET.TXT   # Referencia de propiedades de ticket HubSpot
│   └── test.ticket.py              # Ticket de prueba para desarrollo
│
├── utils/
│   ├── colors.py                   # Utilidades de color (oscurecer)
│   ├── fsd.py                      # Normalización y display de FSD
│   ├── paths.py                    # Resolución de rutas (resource_path)
│   ├── iniciar_chrome_sesion.py    # Lanza Chrome con puerto de depuración 9222
│   └── recuperar_puerto.py         # Diagnóstico y recuperación del puerto 9222
│
├── tests/                          # Suite de tests principal (273 tests)
│   ├── conftest.py                 # Fixtures compartidos
│   ├── test_apps_captura.py        # Tests de configuración de apps
│   ├── test_base_plugin.py         # Tests del contrato ABC
│   ├── test_colors.py              # Tests de utilidades de color
│   ├── test_comparador.py          # Tests del motor de comparación
│   ├── test_configuracion.py       # Tests de carga/guardado de config
│   ├── test_credenciales.py        # Tests de keyring + cookies
│   ├── test_fsd.py                 # Tests de normalización FSD
│   ├── test_integration.py         # Tests de integración
│   ├── test_paths.py               # Tests de resolución de rutas
│   ├── test_plantillas.py          # Tests de plantillas de mensajes
│   └── test_plugin_registry.py     # Tests del registro de plugins
│
├── test/                           # Suite de tests legacy (sin tests activos)
│
├── gsheets/                        # Captura de celdas de Google Sheets
│   ├── __init__.py                  # Punto de entrada (TicketCaptureService)
│   ├── requirements-gsheets.txt     # Dependencias específicas de gsheets
│   ├── utils/
│   │   ├── cell_parser.py           # Parser de referencias A1 (F6 → A3,F3,A6,F6)
│   │   └── image_compositor.py      # Compositor de grilla 2×2 (Pillow)
│   ├── data/
│   │   └── sheets_api.py            # Cliente de Google Sheets API v4 (Service Account)
│   ├── core/
│   │   └── playwright_capture.py    # Captura visual de celdas con Playwright
│   ├── services/
│   │   └── ticket_capture_service.py # Orquestador (parser → API → Playwright → imagen)
│   └── tests/                       # Tests del módulo gsheets (83 tests)
│
├── screenshots/                    # Capturas generadas en runtime
├── cookies/                        # Cookies de sesión guardadas
└── doms/                           # Snapshots de DOM para depuración
```

## Requisitos

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

### Dependencias clave

| Categoría | Paquetes |
|---|---|
| GUI | `customtkinter`, `darkdetect` |
| Navegador | `selenium`, `webdriver-manager`, `playwright` |
| Captura | `mss`, `PyAutoGUI` |
| HubSpot API | `hubspot-api-client` |
| Google Sheets | `google-api-python-client`, `google-auth` |
| Imágenes | `Pillow` |
| Seguridad | `keyring` |
| Datos | `pandas`, `numpy`, `rapidfuzz` |
| Testing | `coverage`, `pytest`, `pytest-asyncio` |

## Configuración inicial

1. Crea un archivo `.env` en la raíz con el token de HubSpot:
   ```
   ACCESS_TOKEN=tu_token_de_app_privada
   ```

2. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

3. Configura las credenciales de cada sitio desde el botón **Credenciales** (se almacenan en el llavero del sistema operativo).

## Uso

### Captura y subida

1. Define la región de pantalla con el botón **Medir** o introduce coordenadas manualmente.
2. Selecciona el sitio de destino (HubSpot, Sunrun o Ambos).
3. Presiona la tecla rápida (por defecto `Ctrl+Enter`) para capturar y subir automáticamente.
4. El botón **Detener** (rojo) permite cancelar el proceso en curso en cualquier momento.

El sistema detecta automáticamente el FSD desde el título de la ventana de Chrome al ejecutar la captura. También se puede ingresar un FSD manualmente en el campo de búsqueda inteligente.

### Captura por aplicación

El panel **APLICACIONES DE CAPTURA** contiene botones dedicados para capturar y subir desde aplicaciones específicas:

| Botón | Descripción |
|---|---|
| Wolkbox | Captura del panel de llamadas |
| B2Chat | Captura de conversaciones de chat |
| Correo | Captura de bandeja de correo |
| Calendar | Captura de celdas de Google Sheets (ver sección abajo) |
| App 5 | Captura de aplicación personalizada |

Cada botón tiene su propia región y monitor configurable. Usa el botón ⚙ junto a cada app para redefinir la región de captura con el medidor visual. Las regiones se persisten automáticamente en `config/config.json`.

### Calendar — Google Sheets

El botón **Calendar** abre un modal para capturar celdas de Google Sheets. El flujo interno:

1. Parsea la referencia de celda (ej. `F6`) en 4 coordenadas A1 (A3, F3, A6, F6).
2. Lee los valores de las 4 celdas desde Google Sheets API v4.
3. Captura visualmente cada celda con Playwright (navegador real o perfil persistente).
4. Compone las 4 capturas en una imagen 2×2 con Pillow.
5. Genera un payload con valores + imagen + referencias.

**Requisitos adicionales en `.env`:**
```
GOOGLE_SERVICE_ACCOUNT_PATH=ruta/al/service-account.json
SHEETS_SPREADSHEET_ID=url-o-id-del-spreadsheet
```

La pestaña y la celda usadas en la última captura se persisten automáticamente en `config/config.json` para rellenar el modal en la siguiente ejecución.

### Comparación de datos

La pestaña **Comparación** permite buscar contactos en HubSpot por FSD, nombre, teléfono, correo o dirección, y compararlos campo por campo contra los datos registrados en Sunrun. Las diferencias se resaltan por colores:

- ✅ **Verde** — datos iguales en ambas plataformas
- 🟡 **Amarillo** — datos similares (p. ej. diferencias mínimas de formato)
- ❌ **Rojo** — datos diferentes entre HubSpot y Sunrun
- 🟠 **Naranja** — dato solo presente en una plataforma

#### Estado de Dispatch

En la parte superior de los resultados de comparación se muestra el estado del dispatch de Sunrun con código de color:

- 🟢 **Trabajable** — Dispatch Accepted o Dispatch Rejected
- 🔴 **No trabajable** — Dispatch Cancelled, Dispatch Reported o Dispatch Approved

Junto al estado se muestran la **Appointment Date** y el **Case Reason** extraídos de Sunrun.

#### Búsqueda multi-atributo

El comparador soporta múltiples estrategias de búsqueda en HubSpot:

- Por FSD (directo, el más preciso)
- Por nombre, teléfono, correo o dirección (búsqueda flexible)

Cuando se busca por un atributo distinto al FSD, el sistema encuentra contactos candidatos en HubSpot, extrae su FSD asociado, y con ese FSD ejecuta la comparación completa contra Sunrun. Esto permite encontrar registros incluso cuando no se conoce el FSD de antemano.

### Generador de mensajes

La pestaña **Plantillas** ofrece plantillas de mensajes por categoría (HubSpot, Sunrun, General) con editor completo. La pestaña **Mensajes** genera mensajes de contacto estandarizados:

- Fuera de Servicio
- Buzón de Voz
- No Contesta
- Confirmación de visita técnica

Cada mensaje está disponible en español e inglés, con fecha automática (`datetime`), manejo inteligente de singular/plural para números telefónicos, previsualización en tiempo real y copia al portapapeles con un clic.

### Chrome

La aplicación puede conectarse a una instancia de Chrome ya abierta (puerto 9222) o lanzar una nueva. Para usar una sesión existente:

```bash
python utils/iniciar_chrome_sesion.py
```

Para diagnosticar problemas con el puerto de depuración:

```bash
python utils/recuperar_puerto.py
```

## Agregar un sitio nuevo

1. Copia `plugins/template_new_site.py` y renómbralo.
2. Implementa los métodos de `SitioPlugin`: `nombre`, `subir()`, selectores y flujo.
3. Registra el plugin en `main.py`:
   ```python
   from plugins.mi_sitio import MiSitioPlugin
   PluginRegistry.registrar(MiSitioPlugin())
   ```

## Carpetas generadas automáticamente

- `screenshots/` — capturas guardadas por la aplicación.
- `cookies/` — cookies de sesión serializadas.
- `doms/` — snapshots de DOM para depuración del scraping.

## Tests

```bash
pytest tests/ -v                    # Suite principal (273 tests)
pytest gsheets/tests/ -v            # Tests del módulo Google Sheets (83 tests)
```

## Consideraciones

- Diseñado para Windows. Otros SO pueden necesitar ajustes en `mss` (monitores), `keyring` (llavero) y `ctypes.windll` (DPI y detección de ventanas).
- La detección automática de FSD usa `ctypes.windll.user32.EnumWindows` para leer títulos de ventanas visibles de Chrome — específico de Windows.
- `webdriver-manager` requiere conexión a internet para descargar `chromedriver` la primera vez.
- El perfil persistente de Chrome se almacena en `C:\chrome_sesion_ssauto` y es compartido entre Selenium y Playwright.

---

**Creado por Julian Esteban Alvarez Segura - PlanetSolar SAS**

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).
````

## File: ui/ventana_principal.py
````python
import ast
import os
import shutil
import threading
import tkinter.font
import time
from datetime import datetime
from pathlib import Path
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import (
    cargar_auto_submit,
    guardar_auto_submit,
    cargar_headless,
    guardar_headless,
    cargar_chrome_existente,
    guardar_chrome_existente,
    cargar_destino_subida,
    guardar_destino_subida,
)
from core.captura import CapturaService, ErrorCaptura
from core.plugin_registry import PluginRegistry
from services.sesion_service import SesionService
from config.configuracion import (
    PERFIL_POR_DEFECTO,
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
)
from core.monitors import (
    obtener_monitores,
    obtener_nombres_monitores,
)
from config.credenciales import cargar_credenciales
from config.credenciales import _COOKIES_DIR as COOKIES_DIR
from config.apps_captura import APPS_CAPTURA
from core.medidor_runner import ejecutar_medidor
from ui.ventana_credenciales import VentanaCredenciales
from ui.custom_ctkframe import CustomCTkFrame
from ui.widgets.log_widget import LogWidget
from utils.colors import oscurecer
from utils.fsd import normalizar_fsd
from scraping.sunrun import ScraperSunrun
from ui.widgets.coordinate_inputs import CoordinateInputsWidget
from ui.widgets.monitor_selector import MonitorSelectorWidget
from ui.widgets.profile_manager import ProfileManagerWidget


from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
)
from gsheets.data.sheets_api import GoogleSheetsClient

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
        self._proceso_en_curso = False
        self._cancelado = threading.Event()
        self._fsd_detectado = None
        self._servicio = SesionService()
        ctk.set_appearance_mode(self._config.get("tema", "dark"))
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
        self._frame_scroll.grid_columnconfigure(
            1, weight=2, minsize=self._r(880, 980, 1120)
        )
        self._frame_scroll.grid_columnconfigure(2, weight=1)

        padre = self._frame_scroll

        sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0, col=1)
        self._crear_panel_captura(sec1)

        sec_apps = self._seccion(padre, "  APLICACIONES DE CAPTURA", fila=1, col=1)
        self._crear_panel_apps(sec_apps)

        sec2 = self._seccion(padre, "  DESTINO Y SESIÓN", fila=2, col=1)
        self._crear_panel_destino(sec2)

        sec3 = self._seccion(padre, "  CONFIGURACIÓN", fila=3, col=1)
        self._crear_opciones(sec3)

        sec4 = self._seccion(
            padre, "  REGISTRO", fila=4, col=1, pady=(0, 8)
        )
        fuente = (
            "Cascadia Code"
            if self._fuente_existe("Cascadia Code")
            else "Consolas"
        )
        self.log_texto = LogWidget(
            sec4,
            font=ctk.CTkFont(family=fuente, size=self._fs(10)),
            height=self._r(140, 180, 260),
        )
        self.log_texto.pack(fill="both", expand=True)

        self._crear_barra_estado(padre, col=1)

    def _seccion(self, padre, titulo, fila, col=0, pady=(0, 10)):
        frame = ctk.CTkFrame(padre, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(row=fila, column=col, sticky="ew", pady=pady)

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
        cuerpo.pack(
            fill="both", expand=True,
            padx=self._r(14, 20, 32), pady=self._r(12, 16, 24),
        )
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

    def _obtener_monitor_app(self, app: dict) -> int:




        nombre = app["nombre"]
        config = cargar_config()
        monitores_guardados = config.get("monitores_apps", {})

        return monitores_guardados.get(nombre, app.get("monitor", 1))

    def _cambiar_monitor_app(self, app: dict, nombre_monitor: str):




        nombre = app["nombre"]
        nombres = obtener_nombres_monitores()

        try:
            indice = nombres.index(nombre_monitor)
        except ValueError:
            self._log(f"[✗] Monitor no válido: {nombre_monitor}")
            return

        config = cargar_config()
        if "monitores_apps" not in config:
            config["monitores_apps"] = {}

        config["monitores_apps"][nombre] = indice
        guardar_config(config)

        self._log(f"✓ Monitor de '{nombre}' → {nombre_monitor}")

    def _crear_panel_captura(self, padre):
        self._perfiles = cargar_perfiles()
        self.region_vars = {}

        monitores_raw = obtener_monitores()
        nombres_monitores = obtener_nombres_monitores()
        monitor_guardado = int(self._config.get("ultimo_monitor", 1))


        r0 = ctk.CTkFrame(padre, fg_color="transparent")
        r0.pack(fill="x", pady=(0, 4))
        r0.grid_columnconfigure((0, 1), weight=1)

        self._profile_widget = ProfileManagerWidget(
            r0,
            region_vars=self.region_vars,
            perfiles_iniciales=self._perfiles,
            on_cargar_perfil=self._on_cargar_perfil,
            on_guardar_perfil=self._on_guardar_perfil,
            on_eliminar_perfil=self._on_eliminar_perfil,
            on_aplicar_region=self._parsear_region,
            on_log=self._log,
        )
        self._profile_widget.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        self._monitor_widget = MonitorSelectorWidget(
            r0,
            nombres_monitores=nombres_monitores,
            monitores_raw=monitores_raw,
            indice_inicial=monitor_guardado,
            on_change=self._on_monitor_change,
        )
        self._monitor_widget.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        self._monitor_var = self._monitor_widget.monitor_var


        coord_row = ctk.CTkFrame(padre, fg_color="transparent")
        coord_row.pack(fill="x", pady=(2, 4))

        self._coord_widget = CoordinateInputsWidget(
            coord_row,
            valores_iniciales=PERFIL_POR_DEFECTO,
            on_change=self._on_coords_change,
        )
        self._coord_widget.pack(side="left", fill="x", expand=True)
        self.region_vars = self._coord_widget.region_vars

        self.btn_detener = ctk.CTkButton(
            coord_row, text="  Detener",
            command=self._detener,
            font=ctk.CTkFont(size=self._fs(11), weight="bold"),
            height=self._r(30, 34, 40),
            fg_color=("#d73a49", "#f85149"),
            hover_color=("#b6232e", "#da3633"),
            state="disabled",
        )
        self.btn_detener.pack(side="right", padx=(8, 0))


        b_row = ctk.CTkFrame(padre, fg_color="transparent")
        b_row.pack(fill="x")
        ctk.CTkButton(
            b_row, text="  Medir region en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=self._fs(11)),
            height=self._r(32, 36, 44),
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray25"),
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.btn = ctk.CTkButton(
            b_row, text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=self._fs(12), weight="bold"),
            height=self._r(36, 42, 50),
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.pack(side="right", fill="x", expand=True, padx=(4, 0))



    def _on_monitor_change(self, *_):
        indice = self._monitor_widget.obtener_indice()
        cfg = cargar_config()
        cfg["ultimo_monitor"] = indice
        guardar_config(cfg)

    def _on_coords_change(self):
        self._profile_widget.sincronizar_paste()

    def _on_cargar_perfil(self, nombre, region):
        self._aplicar_region(region)
        monitor_idx = region.get("monitor_index")
        if monitor_idx is not None:
            nombres = obtener_nombres_monitores()
            if 0 <= int(monitor_idx) < len(nombres):
                self._monitor_var.set(nombres[int(monitor_idx)])
        self._log(f"v Perfil cargado: '{nombre}' -> {region}")

    def _on_guardar_perfil(self, nombre, region):
        region["monitor_index"] = self._monitor_widget.obtener_indice()
        perfiles = cargar_perfiles()
        perfiles[nombre] = region
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil guardado: '{nombre}' -> {region}")

    def _on_eliminar_perfil(self, nombre):
        perfiles = cargar_perfiles()
        perfiles.pop(nombre, None)
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil eliminado: '{nombre}'")

    def _crear_panel_destino(self, padre):
        r0 = ctk.CTkFrame(padre, fg_color="transparent")
        r0.pack(fill="x")
        r0.grid_columnconfigure((0, 1), weight=1)


        c_sitios = ctk.CTkFrame(r0, fg_color="transparent")
        c_sitios.grid(row=0, column=0, sticky="nsew", padx=(0, 3))
        c_sitios.grid_columnconfigure(0, weight=1)

        self._frame_sitios = ctk.CTkFrame(c_sitios, fg_color="transparent")
        self._frame_sitios.pack(fill="x")
        self._actualizar_sitios_status()

        btn_row = ctk.CTkFrame(c_sitios, fg_color="transparent")
        btn_row.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(
            btn_row, text="Credenciales", command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10), width=110, height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btn_row, text="Renovar sesión", command=self._renovar_sesion,
            font=ctk.CTkFont(size=10), width=110, height=28,
        ).pack(side="left")


        c_dest = ctk.CTkFrame(r0, fg_color="transparent")
        c_dest.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        c_dest.grid_columnconfigure(0, weight=1)

        self.destino_var = ctk.StringVar(value=cargar_destino_subida())
        db = ctk.CTkFrame(c_dest, fg_color="transparent")
        db.pack(anchor="w", pady=2)
        ctk.CTkLabel(
            db, text="Subir a:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self._btns_destino = {}
        for opcion in PluginRegistry.nombres() + ["AMBOS"]:
            btn = ctk.CTkButton(
                db, text=opcion,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=72, height=28, corner_radius=6,
                fg_color=("#1f6aa5", "#1f6aa5"),
                hover_color=("#144e7a", "#144e7a"),
            )
            btn.pack(side="left", padx=(0, 4))
            self._btns_destino[opcion] = btn
            btn.configure(command=lambda o=opcion: self._seleccionar_destino(o))
        self._seleccionar_destino(self.destino_var.get())

    def _crear_opciones(self, padre):
        gap = self._r(6, 8, 10)

        cont = ctk.CTkFrame(padre, fg_color="transparent")
        cont.pack(fill="x")
        cont.grid_columnconfigure((0, 1), weight=1)
        cont.grid_rowconfigure(0, weight=1)


        g0, i0 = self._tarjeta(cont, "Comportamiento")
        g0.grid(row=0, column=0, sticky="nsew", padx=(0, gap))

        self.headless_var = ctk.BooleanVar(value=cargar_headless())
        self.headless_var.trace_add(
            "write", lambda *_: guardar_headless(self.headless_var.get())
        )
        ctk.CTkSwitch(
            i0, text="Modo sin ventana de Chrome",
            variable=self.headless_var, font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)

        self.chrome_existente_var = ctk.BooleanVar(value=cargar_chrome_existente())
        self.chrome_existente_var.trace_add(
            "write", lambda *_: guardar_chrome_existente(self.chrome_existente_var.get())
        )
        hc = ctk.CTkFrame(i0, fg_color="transparent")
        hc.pack(fill="x", pady=2)
        ctk.CTkSwitch(
            hc, text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var, font=ctk.CTkFont(size=11),
        ).pack(side="left")
        ctk.CTkButton(
            hc, text="Abrir Chrome", command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10), height=28, width=110,
        ).pack(side="right")

        self.auto_submit_var = ctk.BooleanVar(value=cargar_auto_submit())
        self.auto_submit_var.trace_add(
            "write", lambda *_: guardar_auto_submit(self.auto_submit_var.get())
        )
        ctk.CTkSwitch(
            i0, text="Auto-submit nota (HubSpot)",
            variable=self.auto_submit_var, font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)


        g1, i1 = self._tarjeta(cont, "Herramientas")
        g1.grid(row=0, column=1, sticky="nsew", padx=(0, 0))

        hb = ctk.CTkFrame(i1, fg_color="transparent")
        hb.pack(fill="x", pady=2)
        ctk.CTkLabel(
            hb, text="Atajo:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            hb, textvariable=self.keybind_var, font=ctk.CTkFont(size=11),
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            hb, text="Aplicar", command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10), width=68, height=28,
        ).pack(side="left")
        self.keybind_label = ctk.CTkLabel(
            i1, text="", font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        atajo_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.winfo_toplevel().bind(atajo_inicial, lambda e: self._ejecutar())
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
        guardar_destino_subida(opcion)
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
        self._btns_apps = {}
        self._regiones_apps = {}


        self.usar_fsd_var = ctk.BooleanVar(value=True)
        fsd_row = ctk.CTkFrame(padre, fg_color=("gray92", "gray22"), border_width=1, corner_radius=6)
        fsd_row.pack(fill="x", pady=(0, 8))

        fsd_inner = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_inner.pack(fill="x", padx=10, pady=(6, 4))
        ctk.CTkSwitch(
            fsd_inner, text="Búsqueda inteligente por FSD",
            variable=self.usar_fsd_var, font=ctk.CTkFont(size=11),
            command=self._actualizar_estado_fsd,
        ).pack(anchor="w")

        fsd_input = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_input.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkLabel(
            fsd_input, text="FSD:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.fsd_var = ctk.StringVar(value="")
        self.fsd_entry = ctk.CTkEntry(
            fsd_input, textvariable=self.fsd_var, font=ctk.CTkFont(size=11),
            placeholder_text="Ej: 980124 o FSD-980124", state="disabled",
        )
        self.fsd_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.fsd_btn_limpiar = ctk.CTkButton(
            fsd_input, text="Limpiar", command=self._limpiar_fsd,
            font=ctk.CTkFont(size=10), width=68, height=28, state="disabled",
        )
        self.fsd_btn_limpiar.pack(side="left")

        self.fsd_btn_buscar = ctk.CTkButton(
            fsd_input, text="Buscar en Sunrun", command=self._buscar_fsd_sunrun,
            font=ctk.CTkFont(size=10), width=110, height=28,
        )
        self.fsd_btn_buscar.pack(side="right", padx=(4, 0))

        self.fsd_entry.configure(state="normal")
        self.fsd_btn_limpiar.configure(state="normal")
        self.fsd_btn_buscar.configure(state="normal")


        grid = ctk.CTkFrame(padre, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1, uniform="app_col")

        config_actual = cargar_config()
        regiones_guardadas = config_actual.get("regiones_apps", {})
        nombres_monitores = obtener_nombres_monitores()

        for idx, app in enumerate(APPS_CAPTURA):
            nombre = app["nombre"]
            icono = app.get("icono", "")
            color_base = app.get("color", ("#1f6aa5", "#1a5496"))
            region_efectiva = regiones_guardadas.get(nombre, app["region"])
            self._regiones_apps[nombre] = region_efectiva

            col = idx % 2
            row = idx // 2
            gap = self._r(4, 6, 8)

            card = ctk.CTkFrame(
                grid, fg_color=("gray90", "gray22"), corner_radius=8,
            )
            card.grid(
                row=row, column=col,
                sticky="ew",
                padx=(0 if col == 0 else gap, gap if col == 0 else 0),
                pady=(0, gap * 2),
            )

            r = region_efectiva
            es_calendar = nombre == "Calendar"
            btn_main = ctk.CTkButton(
                card,
                text=f"{icono}  {nombre}   ▶  {'Capturar celda' if es_calendar else 'Capturar'}   ({r['width']}×{r['height']} px)",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=38, corner_radius=7, anchor="w",
                fg_color=color_base,
                hover_color=(oscurecer(color_base[0]), oscurecer(color_base[1])),
                command=lambda a=app: self._abrir_modal_calendar() if a["nombre"] == "Calendar" else self._ejecutar_app(a),
            )
            btn_main.pack(fill="x", padx=6, pady=(5, 2))
            self._btns_apps[nombre] = btn_main

            bot_row = ctk.CTkFrame(card, fg_color="transparent")
            bot_row.pack(fill="x", padx=6, pady=(2, 5))

            monitor_actual = self._obtener_monitor_app(app)
            nombre_monitor_actual = (
                nombres_monitores[monitor_actual]
                if 0 <= monitor_actual < len(nombres_monitores)
                else nombres_monitores[0]
            )
            dropdown_monitor = ctk.CTkComboBox(
                bot_row,
                values=nombres_monitores,
                variable=ctk.StringVar(value=nombre_monitor_actual),
                command=lambda sel, a=app: self._cambiar_monitor_app(a, sel),
                width=160, height=34, corner_radius=7,
                font=ctk.CTkFont(size=9),
                dropdown_font=ctk.CTkFont(size=9),
                state="readonly",
            )
            dropdown_monitor.pack(side="left", fill="x", expand=True, padx=(0, 4))

            if not es_calendar:
                ctk.CTkButton(
                    bot_row, text="⚙",
                    font=ctk.CTkFont(size=14),
                    width=36, height=34, corner_radius=7,
                    fg_color=("gray70", "gray35"),
                    hover_color=("gray60", "gray45"),
                    command=lambda a=app: self._medir_region_app(a),
                ).pack(side="right")



    def _ejecutar_app(self, app: dict):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        nombre = app["nombre"]
        region = self._regiones_apps.get(nombre, app["region"])
        monitor_idx = self._obtener_monitor_app(app)

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()

        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando {region['width']}×{region['height']} px…"
        )

        threading.Thread(
            target=self._proceso_app,
            args=(app, region, monitor_idx),
            daemon=True,
        ).start()

    def _subir_a_destinos(self, ruta, ui, prefix=""):
        """Sube la imagen capturada a los destinos configurados."""
        headless = self.headless_var.get()
        usar_existente = self.chrome_existente_var.get()
        auto_submit = self.auto_submit_var.get()
        destino = self.destino_var.get()
        fsd = self._obtener_fsd_actual()
        if not fsd:
            fsd = self._fsd_detectado

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
            ui(f"{prefix}✗ No hay plugins para destino: {destino}")

        for plugin in plugins:
            if self._cancelado.is_set():
                ui(f"{prefix}⚠ Cancelado antes de subir a {plugin.nombre}.")
                break
            ui(f"{prefix}→ Subiendo a {plugin.nombre}…")
            fsd_plugin = fsd
            self._servicio.ejecutar_subida(
                nombre_plugin=plugin.nombre,
                ruta_imagen=ruta,
                log=ui,
                headless=headless,
                usar_chrome_existente=usar_existente,
                credenciales_sesion=self._credenciales_sesion,
                opciones={"auto_submit_nota": auto_submit},
                fsd=fsd_plugin,
                cancel_event=self._cancelado,
            )
            ui("")

    def _proceso_app(self, app: dict, region: dict, monitor_idx: int):
        nombre = app["nombre"]
        prefix = f"[{nombre}] "

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            ui(f"{prefix}Capturando {region['width']}×{region['height']} px…")
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region, monitor=monitor_idx)
            ui(f"✓ {prefix}Imagen guardada: {ruta}")
            ui("")

            self._subir_a_destinos(ruta, ui, prefix)

            ui(f"✓ {prefix}Proceso completado.")
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
                0, lambda err=e: self._log(f"✗ {prefix}Error de captura: {err}")
            )
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error de captura"
                ),
            )
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ {prefix}Error: {err}"))
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(text=f"  ✗ {nombre} — error"),
            )
        finally:
            self._proceso_en_curso = False
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, self._rehabilitar_btns_apps)

    def _rehabilitar_btns_apps(self):
        for btn in self._btns_apps.values():
            btn.configure(state="normal")
        self.fsd_btn_buscar.configure(state="normal")
        self.btn_detener.configure(state="disabled")



    def _abrir_modal_calendar(self):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return

        sheet_url = os.getenv("SHEETS_SPREADSHEET_ID", "")
        service_account = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "")

        if not service_account:
            messagebox.showwarning(
                "Configuración requerida",
                "Falta GOOGLE_SERVICE_ACCOUNT_PATH en el archivo .env\n"
                "Agrega la ruta al JSON de tu Service Account de Google.",
            )
            return

        if not sheet_url:
            messagebox.showwarning(
                "Configuración requerida",
                "Falta SHEETS_SPREADSHEET_ID en el archivo .env\n"
                "Agrega el ID o URL de tu Google Sheets.",
            )
            return


        modal = ctk.CTkToplevel(self)
        modal.title("Calendar — Google Sheets")
        modal.resizable(False, False)
        modal.transient(self)
        modal.withdraw()

        modal.grid_columnconfigure(0, weight=1)


        ctk.CTkLabel(
            modal,
            text="Pestaña:",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        ).grid(row=1, column=0, pady=(0, 2), padx=28, sticky="w")


        _config = cargar_config()
        ultima_pestana = _config.get("ultima_pestana_calendar", "")

        sheet_var = ctk.StringVar(value=ultima_pestana or "Cargando...")
        sheet_dropdown = ctk.CTkComboBox(
            modal,
            values=[ultima_pestana] if ultima_pestana else ["Cargando pestañas..."],
            variable=sheet_var,
            state="disabled" if not ultima_pestana else "readonly",
            width=240,
            height=34,
            font=ctk.CTkFont(size=12),
            dropdown_font=ctk.CTkFont(size=12),
        )
        sheet_dropdown.grid(row=2, column=0, pady=(0, 12), padx=28)


        ctk.CTkLabel(
            modal,
            text="Referencia de celda (ej. F6, AA10):",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        ).grid(row=3, column=0, pady=(0, 4), padx=28, sticky="w")

        ultima_celda = _config.get("ultima_celda_calendar", "")

        cell_var = ctk.StringVar(value=ultima_celda)
        cell_entry = ctk.CTkEntry(
            modal,
            textvariable=cell_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            placeholder_text="F6",
            width=240,
            height=38,
            justify="center",
        )
        cell_entry.grid(row=4, column=0, pady=(0, 12), padx=28)
        cell_entry.focus_set()
        if ultima_celda:
            cell_entry.icursor("end")


        _sheet_names: list[str] = []
        _ultima_pestana_inicial = ultima_pestana


        def _on_enter(event):
            _ejecutar()

        cell_entry.bind("<Return>", _on_enter)

        def _ejecutar():
            cell_ref = cell_var.get().strip()
            if not cell_ref:
                messagebox.showwarning("Celda requerida", "Ingresa una referencia de celda (ej. F6).", parent=modal)
                return
            sheet_name = sheet_var.get().strip() if _sheet_names else None

            config = cargar_config()
            config["ultima_celda_calendar"] = cell_ref
            if sheet_name:
                config["ultima_pestana_calendar"] = sheet_name
            guardar_config(config)
            modal.destroy()
            self._ejecutar_captura_calendar(cell_ref, sheet_url, service_account, sheet_name)


        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.grid(row=5, column=0, pady=(0, 16), padx=28, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            font=ctk.CTkFont(size=12),
            fg_color=("gray70", "gray35"),
            hover_color=("gray60", "gray45"),
            command=modal.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Capturar",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=_ejecutar,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")


        def _load_sheets():
            nonlocal _sheet_names
            try:
                sheets_client = GoogleSheetsClient(service_account)
                spreadsheet_id = GoogleSheetsClient.extract_spreadsheet_id(sheet_url)
                sheets = sheets_client.list_sheets(spreadsheet_id)
                _sheet_names = [s["title"] for s in sheets]
                self._log(f"→ Pestañas detectadas: {', '.join(_sheet_names)}")

                sheet_dropdown.configure(values=_sheet_names, state="readonly")
                if _sheet_names:
                    if _ultima_pestana_inicial and _ultima_pestana_inicial in _sheet_names:
                        sheet_var.set(_ultima_pestana_inicial)
                    else:
                        sheet_var.set(_sheet_names[0])
            except Exception as e:
                self._log(f"✗ No se pudieron obtener las pestañas: {e}")
                sheet_dropdown.configure(values=["(sin pestañas)"], state="disabled")
                sheet_var.set("")

        modal.after(10, _load_sheets)

        # Posicionar y mostrar
        from ui.posicion_ventanas import ubicar_junto_a_padre
        modal.deiconify()
        ubicar_junto_a_padre(modal, self)
        modal.grab_set()
        modal.wait_window()

    def _ejecutar_captura_calendar(
        self, cell_ref: str, sheet_url: str, service_account: str,
        sheet_name: str | None = None,
    ):
        nombre = "Calendar"
        prefix = f"[{nombre}] "
        sheet_label = f" ({sheet_name})" if sheet_name else ""

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        self._proceso_en_curso = True
        self._fsd_detectado = None
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()
        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando celda {cell_ref}{sheet_label}…"
        )

        def _ejecutar():
            try:
                ui(f"{prefix}→ Iniciando captura de celda {cell_ref} desde Google Sheets{sheet_label}…")
                config = TicketCaptureConfig(
                    spreadsheet_id=sheet_url,
                    credentials_path=service_account,
                    sheet_name=sheet_name,
                    headless=True,
                )
                service = TicketCaptureService(config, log_callback=ui)
                payload = service.capture_sync(cell_ref)

                ui(f"{prefix}✓ Valores obtenidos:")
                for ref, val in payload.cells.items():
                    ui(f"{prefix}    {ref}: {val or '(vacío)'}")

                ui(f"{prefix}✓ Imagen compuesta: {payload.image_path}")
                ui("")

                # Subir la imagen compuesta a los destinos configurados
                self._subir_a_destinos(payload.image_path, ui, prefix)

                ui(f"{prefix}✓ Proceso completado.")
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
                        text=f"  ✓ {nombre} — celda {cell_ref}{sheet_label} capturada a las {ahora}"
                    ),
                )
                self.after(0, self._actualizar_sitios_status)

            except Exception as e:
                self.after(
                    0, lambda err=e: self._log(f"✗ {prefix}Error: {err}")
                )
                self.after(0, lambda: self._set_status("Error"))
                self.after(
                    0,
                    lambda: self._label_estado_app.configure(
                        text=f"  ✗ {nombre} — error al capturar celda {cell_ref}"
                    ),
                )
            finally:
                self._proceso_en_curso = False
                self.after(0, self.deiconify_window)
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_ejecutar, daemon=True).start()



    def _medir_region_app(self, app: dict):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        nombre = app["nombre"]
        monitor_idx = self._obtener_monitor_app(app)

        self._log(f"→ Midiendo región para {nombre}…")
        self._label_estado_app.configure(
            text=f"  ⏳ Medí la región de {nombre} en pantalla…"
        )

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self.iconify_window()

        def _esperar():
            try:
                nueva_region = ejecutar_medidor(monitor_idx)

                if nueva_region is None:
                    self.after(0, lambda: self._log(f"✗ Medición cancelada para {nombre}."))
                    self.after(0, lambda: self._label_estado_app.configure(text=""))
                    self.after(0, self.deiconify_window)
                    self.after(0, self._rehabilitar_btns_apps)
                    self.after(0, lambda: self.btn.configure(state="normal"))
                    return

                self._regiones_apps[nombre] = nueva_region
                cfg = cargar_config()
                cfg.setdefault("regiones_apps", {})[nombre] = nueva_region
                self.after(0, lambda c=cfg: guardar_config(c))

                def _actualizar_ui():
                    if nombre in self._btns_apps:
                        tooltip = f"{nueva_region['width']}×{nueva_region['height']} px"
                        btn = self._btns_apps[nombre]
                        icono = next((a["icono"] for a in APPS_CAPTURA if a["nombre"] == nombre), "")
                        color_base = next((a["color"] for a in APPS_CAPTURA if a["nombre"] == nombre), ("#1f6aa5", "#1a5496"))
                        btn.configure(
                            text=f"{icono}  {nombre}   ▶  Capturar y subir   ({tooltip})",
                            fg_color=color_base,
                        )
                    self._label_estado_app.configure(
                        text=f"  ✓ {nombre} — nueva región: {nueva_region['width']}×{nueva_region['height']} px guardada"
                    )
                    self._log(f"✓ Región de {nombre} actualizada: {nueva_region}")
                    self.deiconify_window()
                    self._rehabilitar_btns_apps()
                    self.btn.configure(state="normal")

                self.after(0, _actualizar_ui)
            except Exception as e:
                self.after(0, lambda err=e: self._log(f"✗ [{nombre}] Error en medidor: {err}"))
                self.after(0, lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error en medidor"
                ))
                self.after(0, self.deiconify_window)
                self.after(0, self._rehabilitar_btns_apps)
                self.after(0, lambda: self.btn.configure(state="normal"))
            finally:
                self.after(0, lambda: setattr(self, '_proceso_en_curso', False))

        threading.Thread(target=_esperar, daemon=True).start()

    def _crear_barra_estado(self, padre, col=0):
        frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        frame_estado.grid(row=6, column=col, sticky="ew", pady=(4, 0))
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
        self._label_estado_app = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_estado_app.pack(side="left", padx=(12, 0), fill="x", expand=True)
        self._label_ultimo_proceso = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_ultimo_proceso.pack(side="right")



    def _tarjeta(self, padre, titulo):
        frame = ctk.CTkFrame(
            padre, fg_color=("gray92", "gray22"), border_width=1, corner_radius=6
        )
        ctk.CTkLabel(
            frame,
            text=f"  {titulo}",
            font=ctk.CTkFont(size=self._fs(10)),
            text_color=("gray55", "gray55"),
        ).pack(anchor="w", pady=(4, 2), padx=2)
        interior = ctk.CTkFrame(frame, fg_color="transparent")
        interior.pack(fill="x", padx=10, pady=(0, 6))
        return frame, interior

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

    def _actualizar_estado_fsd(self):

        if self.usar_fsd_var.get():
            self.fsd_entry.configure(state="normal")
            self.fsd_btn_limpiar.configure(state="normal")
            self.fsd_btn_buscar.configure(state="normal")
            self._log("✓ Búsqueda inteligente por FSD activada.")
        else:
            self.fsd_entry.configure(state="disabled")
            self.fsd_btn_limpiar.configure(state="disabled")
            self.fsd_btn_buscar.configure(state="disabled")
            self.fsd_var.set("")
            self._log("✗ Búsqueda inteligente por FSD desactivada.")

    def _limpiar_fsd(self):
        """Limpia el campo FSD."""
        self.fsd_var.set("")
        self._log("✓ Campo FSD limpiado.")

    def _obtener_fsd_actual(self) -> str | None:
        """Devuelve el FSD si está habilitado, None en caso contrario."""
        if not self.usar_fsd_var.get():
            return None
        fsd = self.fsd_var.get().strip()
        return fsd if fsd else None

    @staticmethod
    def _detectar_fsd_de_chrome() -> str | None:
        """
        Lee el título de ventanas visibles de Chrome vía Windows API y extrae
        el primer FSD que encuentre (patrón FSD-XXXXXX o FSDXXXXXX).
        Se llama con la app minimizada para que Chrome esté en primer plano.
        """
        import re
        user32 = ctypes.windll.user32

        fsd_encontrado = [None]

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def enum_proc(hwnd, _lparam):
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            if "Google Chrome" not in title and "Chromium" not in title:
                return True
            match = re.search(r'FSD[-\s]*(\d+)', title, re.IGNORECASE)
            if match:
                fsd = f"FSD-{match.group(1)}"
                fsd_encontrado[0] = fsd
                return False
            return True

        user32.EnumWindows(WNDENUMPROC(enum_proc), 0)
        return fsd_encontrado[0]

    def _buscar_fsd_sunrun(self):
        """
        Ejecuta SOLO la búsqueda FSD en Sunrun (navega al ticket) sin scraping.

        Usa exactamente la misma lógica que el módulo de scraping (ScraperSunrun),
        pero se detiene en la página de detalle del ticket sin extraer datos.
        """
        fsd = self.fsd_var.get().strip()
        if not fsd:
            self._log("✗ Ingresa un número FSD para buscar.")
            return

        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return

        self._proceso_en_curso = True
        self.fsd_btn_buscar.configure(state="disabled")
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Buscando FSD en Sunrun...")

        def _buscar():
            try:

                def ui(msg):
                    self.after(0, lambda m=msg: self._log(m))

                ui(f"→ Buscando FSD en Sunrun: {normalizar_fsd(fsd)}")
                scraper = ScraperSunrun(log_callback=ui)
                resultado = scraper.navegar_a_fsd(fsd)
                if resultado["ok"]:
                    ui(f"✓ {resultado['mensaje']}")
                else:
                    ui(f"✗ {resultado['mensaje']}")
                self.after(0, lambda: self._set_status("Listo"))
            except Exception as e:
                self.after(0, lambda err=e: self._log(f"✗ Error en búsqueda FSD: {err}"))
                self.after(0, lambda: self._set_status("Error"))
            finally:
                self._proceso_en_curso = False
                self.after(0, self.deiconify_window)
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_buscar, daemon=True).start()



    def _actualizar_sitios_status(self):
        for widget in self._frame_sitios.winfo_children():
            widget.destroy()

        for plugin in PluginRegistry.todos():
            nombre = plugin.nombre
            tiene_sesion = (COOKIES_DIR / f"{nombre.replace(' ', '_')}.pkl").exists()
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
        self.log_texto.log(msg)

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



    def _monitor_var_indice(self) -> int:
        return self._monitor_widget.obtener_indice()

    def _lanzar_medidor(self):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        monitor_idx = self._monitor_var_indice()
        self._log(f"→ Abre el medidor en {self._monitor_var.get()}…")
        self.btn.configure(state="disabled")
        self.iconify_window()

        def _esperar():
            region = ejecutar_medidor(monitor_idx)
            if region is not None:
                self.after(0, lambda r=region: self._aplicar_region(r))
            else:
                self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region: dict):
        self._coord_widget.aplicar_region(region)
        self._profile_widget.sincronizar_paste()
        self._log(f"v Region actualizada: {region}")
        self.btn.configure(state="normal")

    def _obtener_region_validada(self) -> dict:
        region = {}
        for clave, var in self.region_vars.items():
            texto = var.get().strip()
            if not texto:
                raise ValueError(f"El campo '{clave}' esta vacio.")
            try:
                region[clave] = int(texto)
            except ValueError:
                raise ValueError(f"El campo '{clave}' debe ser un numero entero.")
        if region["width"] <= 0:
            raise ValueError("Width debe ser mayor que 0.")
        if region["height"] <= 0:
            raise ValueError("Height debe ser mayor que 0.")
        return region

    def _parsear_region(self, texto: str):
        texto = (texto or "").strip()
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
        self._profile_widget.sincronizar_paste()



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
        if COOKIES_DIR.exists():
            shutil.rmtree(COOKIES_DIR)
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

    def _abrir_chrome_debug(self):
        from core.browser import puerto_activo, CHROME_USER_DATA, CHROME_PATHS, obtener_chrome_exe

        if puerto_activo():
            self._log("✓ Chrome con depuración ya está activo en el puerto 9222.")
            return
        chrome_exe = obtener_chrome_exe()
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
                f"--user-data-dir={CHROME_USER_DATA}",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222.")

    # ── Keybind ───────────────────────────────────────────────────────

    def _aplicar_keybind(self):
        nuevo = self.keybind_var.get().strip()
        if not nuevo:
            return
        if self._keybind_actual:
            try:
                self.winfo_toplevel().unbind(self._keybind_actual)
            except Exception:
                pass
        try:
            self.winfo_toplevel().bind(nuevo, lambda e: self._ejecutar())
            self._keybind_actual = nuevo
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(nuevo)}",
                text_color=("green", "#3fb950"),
            )
            self._config = cfg = cargar_config()
            cfg["keybind"] = nuevo
            guardar_config(cfg)
            self._config = cfg
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



    def _detener(self):
        self._cancelado.set()
        self._log("⚠ Deteniendo proceso...")
        self.btn_detener.configure(state="disabled")
        self._set_status("Cancelando...")



    def _ejecutar(self):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        self._cancelado.clear()
        self.btn.configure(state="disabled")
        self.btn_detener.configure(state="normal")
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.fsd_btn_buscar.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = self._obtener_region_validada()
            monitor_idx = self._monitor_var_indice()
            ui(f"→ Capturando región en {self._monitor_var.get()}: {region}")
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            self._fsd_detectado = self._detectar_fsd_de_chrome()
            if self._fsd_detectado:
                ui(f"→ FSD detectado automáticamente: {self._fsd_detectado}")

            ruta = CapturaService.capturar(region, monitor=monitor_idx)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            if self._cancelado.is_set():
                ui("⚠ Proceso cancelado antes de subir.")
                self.after(0, lambda: self._set_status("Cancelado"))
                return

            self._subir_a_destinos(ruta, ui)

            if self._cancelado.is_set():
                ui("⚠ Proceso cancelado.")
                self.after(0, lambda: self._set_status("Cancelado"))
                return

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
            self._proceso_en_curso = False
            self._cancelado.clear()
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, lambda: self.btn_detener.configure(state="disabled"))
            self.after(0, self._rehabilitar_btns_apps)
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
cryptography==48.0.0
customtkinter==5.2.2
cyclonedx-python-lib==11.7.0
darkdetect==0.8.0
defusedxml==0.7.1
docopt==0.6.2
fastapi==0.136.1
filelock==3.29.0
git-filter-repo==2.47.0
google-api-core==2.30.3
google-api-python-client==2.197.0
google-auth==2.53.0
google-auth-httplib2==0.4.0
google-auth-oauthlib==1.4.0
googleapis-common-protos==1.75.0
greenlet==3.5.1
h11==0.16.0
httplib2==0.31.2
hubspot-api-client==12.0.0
idna==3.13
iniconfig==2.3.0
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
oauthlib==3.3.1
outcome==1.3.0.post0
packageurl-python==0.17.6
packaging==26.2
pathspec==1.1.1
pefile==2024.8.26
pillow==12.2.0
pip-api==0.0.34
pip-requirements-parser==32.0.1
pip_audit==2.10.0
pipreqs==0.4.13
platformdirs==4.9.6
playwright==1.60.0
pluggy==1.6.0
proto-plus==1.28.0
protobuf==7.35.0
py-serializable==2.1.0
pyasn1==0.6.3
pyasn1_modules==0.4.2
PyAutoGUI==0.9.54
pycparser==3.0
pydantic==2.13.4
pydantic_core==2.46.4
pyee==13.0.1
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
pytest==9.0.3
pytest-asyncio==1.4.0
pytest-mock==3.15.1
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
pytokens==0.4.1
pytweening==1.2.0
pywin32-ctypes==0.2.3
RapidFuzz==3.14.5
requests==2.33.1
requests-oauthlib==2.0.0
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
uritemplate==4.2.0
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
from version import __version__
from config.configuracion import (
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_config,
    guardar_config,
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
    sitios_compat = [
        {"nombre": p.nombre, "necesita_login": p.necesita_login}
        for p in PluginRegistry.con_login()
    ]
    win = VentanaCredenciales(launcher, sitios_compat)
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

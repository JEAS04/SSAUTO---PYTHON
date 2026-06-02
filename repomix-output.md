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
data/PROPIEDADES DE CONTACTO.TXT
data/PROPIEDADES DE TICKET.TXT
data/test.ticket.py
doku.md
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

## File: data/PROPIEDADES DE CONTACTO.TXT
````
CONTACT PROPERTIES:

a_qu_plaza_se_postula -> PS FaceBook ¿A qué plaza se postula? -> string
a_qu_plaza_solicita -> ¿A qué plaza solicita? -> string
aceptacion_terminos_y_condiciones -> Aceptación Términos y Condiciones -> enumeration
acepto_los_terminos_y_condiciones_del_concurso_brilla_gratis_con_planet -> Acepto los términos y condiciones del concurso Brilla Gratis con Planet ! -> enumeration
actualmente_tiene_sistema_solar_instalado -> ¿Actualmente tiene sistema solar instalado? -> string
actualmente_tienes_placas_solares_instaladas -> ¿Actualmente tienes placas solares instaladas? -> string
address -> Street Address -> string
agendador__inside_sales_ -> Agendador (Inside Sales) -> enumeration
annualrevenue -> Annual Revenue -> string
asignado_a_inside_sales -> Asignado a Inside Sales -> enumeration
asignado_por -> PS Assigned by -> enumeration
associatedcompanyid -> Primary Associated Company ID -> number
associatedcompanylastupdated -> Associated Company Last Updated -> number
bateria__contacto_ -> Tiempo Autonomia Todas las Cargas (Contacto) -> enumeration
bateria__negocios_ -> Cargas Bateria (Contacto) -> enumeration
campana -> PS FaceBook Generac -> string
canal -> Evento | Concurso | Leads -> enumeration
cantidad_tipo_de_bateria__contacto_ -> Cantidad Tipo de Batería (Contacto) -> number
cantidad_tipo_de_cargador__contacto_ -> Cantidad Tipo de Cargador (Contacto) -> number
cantidad_tipo_de_inversor__contacto_ -> Cantidad Tipo de Inversor (Contacto) -> number
cantidad_tipo_de_panel__contacto_ -> Cantidad Tipo de Panel (Contacto) -> number
cerrador_concurso -> Cerrador Concurso | Brilla 2026 -> enumeration
cita_nueva_o_reagendada -> Cita Nueva o Reagendada (Inside Sales) -> enumeration
city -> City -> string
closedate -> Close Date -> datetime
comentario_de_ventas -> PS Webform Note -> string
comentarios_division_comercial -> Notas Adicionales (Contacto) -> string
company -> Company Name -> string
company_size -> Company size -> string
concurso__evento_ -> Concurso (Evento) -> enumeration
consultor__baby_boomers_expo_2024_ -> Consultor (Baby Boomers Expo 2024) -> string
consultor__booth_ -> Consultor (Booth) -> string
consultor__sanse_caguas_2025_ -> Consultor (Sanse Caguas 2025) -> string
consultor__sanse_san_juan_2025_ -> Consultor (Sanse San Juan 2025) -> string
consultor_comercial_asignado__contacto_ -> Consultor Comercial (Contacto) -> string
contratado__jobs_ -> Contratado (Jobs) -> enumeration
cotizacion__contacto_ -> Cotización (Contacto) -> string
country -> Country/Region -> string
createdate -> Create Date -> datetime
cual_es_su_empirica_aproximada -> Cual es su empirica aproximada? -> string
cual_es_su_pago_aproximado_de_energia -> ¿Cuál es su pago aproximado de energía? -> number
cual_es_tu_aproximado_de_luma -> Cual es tu aproximado de LUMA? -> string
cuanto_es_la_cantidad_adeudada_en_luma -> Cuanto es la cantidad adeudada en LUMA? -> string
cuanto_es_regularmente_su_factura_de_luma -> Cuanto es regularmente su factura de luma? -> string
cuanto_es_su_pago_regular_de_luma -> Cuanto es su pago regular de LUMA? -> string
cuanto_paga_de_su_factura_de_luma -> Cuanto paga de su factura de Luma? -> string
cuanto_paga_regularmente_de_su_factura_de_luma -> ¿Cuanto paga regularmente de su factura de LUMA? -> string
cuanto_paga_regularmente_de_su_factura_de_luma_ -> ¿Cuanto paga regularmente de su factura de LUMA -> string
cuanto_paga_regularmente_en_luma -> ¿Cuanto paga regularmente en LUMA? -> string
cuanto_paga_regularmente_en_su_factura_de_luma_ -> Cuanto paga regularmente en su factura de LUMA -> string
cuanto_pagas_actualmente_de_tu_factura -> Cuanto pagas actualmente de tu factura -> string
cuanto_pagas_de_luz_mensual -> Cuanto pagas de luz mensual? -> string
cuanto_pagas_de_tu_factura_regular_de_luma -> Cuanto pagas de tu factura regular de LUMA? -> string
cuanto_pagas_regularmente_de_tu_factura_de_luma -> ¿Cuanto pagas regularmente de tu factura de LUMA? -> string
cuanto_pagas_regularmente_de_tu_factura_de_luma_ -> Cuanto pagas regularmente de tu factura de LUMA -> string
cuanto_pagas_regularmente_de_tu_factura_de_luz_ -> Cuanto pagas regularmente de tu factura de LUZ -> string
cuanto_pagas_regularmente_en_tu_factura_de_luma -> ¿Cuanto pagas regularmente en tu factura de LUMA? -> string
cuentas_con_autotransportacin_propia -> ¿Cuentas con auto/transportación propia? -> string
cul_describe_mejor_tu_perfil -> ¿Cuál describe mejor tu perfil? -> string
cul_es_el_promedio_de_tu_factura_mensual_de_electricidad -> ¿Cuál es el promedio de tu factura mensual de electricidad? -> string
cul_es_el_promedio_mensual_de_tu_factura_elctrica -> ¿Cuál es el promedio mensual de tu factura eléctrica? -> string
cul_es_su_pago_aproximado_de_energa -> ¿Cuál es su pago aproximado de energía? -> string
cul_es_su_zona_de_ubicacin -> ¿Cuál es su zona de ubicación? -> string
cul_es_tu_consumo_mensual_aproximado_de_electricidad -> ¿Cuál es tu consumo mensual aproximado de electricidad? -> string
cul_es_tu_consumo_mensual_aproximado_de_luz -> ¿Cuál es tu consumo mensual aproximado de luz? -> string
cul_es_tu_consumo_mensual_de_luz_aproximado -> ¿Cuál es tu consumo mensual de luz aproximado? -> string
cul_es_tu_consumo_mensual_promedio_de_electricidad -> ¿Cuál es tu consumo mensual promedio de electricidad? -> string
cul_es_tu_factura_mensual_de_luz -> ¿Cuál es tu factura mensual de luz? -> string
cul_es_tu_factura_promedio_de_luz -> ¿Cuál es tu factura promedio de luz? -> string
cul_es_tu_factura_promedio_mensual_de_electricidad -> ¿Cuál es tu factura promedio mensual de electricidad? -> string
cul_es_tu_gasto_promedio_mensual_de_luz -> ¿Cuál es tu gasto promedio mensual de luz? -> string
cul_horario_es_conveniente_para_ser_contactad -> ¿Cuál horario es conveniente para ser contactad@? -> string
cunto_pagas_en_energa_en_promedio_por_mes_ -> ¿Cuánto pagas en energía en promedio por mes? * -> string
cuota_por_cita -> Cuota por Cita -> number
currentlyinworkflow -> Currently in workflow (discontinued) -> enumeration
cybertruck_notas -> Cybertruck Notas -> string
date_of_birth -> Date of birth -> string
days_to_close -> Days To Close -> number
de_cuanto_es_su_factura_de_luma_regularmente -> De cuanto es su factura de LUMA regularmente? -> string
de_que_pueblo_es -> De que pueblo es? -> string
degree -> Degree -> string
departamento -> PS Webform Work Deparment -> enumeration
deseas_instalacin_en_menos_de_30_das -> ¿Deseas instalación en menos de 30 días? -> string
deseas_ser_parte_de_nuestra_red_de_instaladoresdistribuidores -> ¿Deseas ser parte de nuestra red de instaladores/distribuidores? -> string
direccion__fisica_ -> Direccion (Fisica) -> string
direccion_postal -> Direccion (Postal) -> string
disclaimer -> Disclaimer -> enumeration
disponibilidad_para_comenzar -> Disponibilidad para comenzar -> string
dnde_deseas_instalar_el_sistema_solar_si_resultas_ganadora -> ¿Dónde deseas instalar el sistema solar si resultas ganador(a)? -> string
dueno_de_la_propiedad__contactos_ -> Dueño de la propiedad (Contactos) -> string
el_hogar_donde_interesa_el_sistema_es_de_su_propiedad -> El hogar donde interesa el sistema es de su propiedad? -> string
el_hogar_donde_te_interesa_instalar_sistema_es_de_su_propiedad -> El hogar donde te interesa instalar sistema es de su propiedad? -> string
email -> Email -> string
email_consultor_comercial__contacto_ -> Email Consultor Comercial (Contacto) -> string
email_del_representate_costco -> Email del Representate (Costco) -> string
en_cual_pueblo_reside -> ¿En cual pueblo reside? -> string
en_cunto_tiempo_planea_implementar_energa_solar -> ¿En cuánto tiempo planea implementar energía solar? -> string
en_qu_horario_es_conveniente_ser_contactado_a -> ¿En qué horario es conveniente ser contactado (a)? -> string
en_qu_municipio_resides -> ¿En qué municipio resides? -> string
en_qu_municipio_resides_ -> ¿En qué municipio resides? -> string
en_qu_municipios_o_regiones_trabajas_principalmente -> ¿En qué municipios o regiones trabajas principalmente? -> string
en_qu_tipo_de_propiedad_te_interesa_instalar_el_sistema -> ¿En qué tipo de propiedad te interesa instalar el sistema? -> string
en_que_horario_es_conveniente_ser_contactad -> ¿En que horario es conveniente ser contactad@? -> string
en_que_pueblo_reside -> ¿En que pueblo reside? -> string
en_que_pueblo_resides -> ¿En que pueblo resides? -> string
en_que_usted_est_interesado_a_si_vive_en_un_edificio_no_aplica -> ¿En que usted está interesado (a)? *Si vive en un edificio no aplica* -> string
engagements_last_meeting_booked -> Date of last meeting booked in meetings tool -> datetime
engagements_last_meeting_booked_campaign -> Campaign of last booking in meetings tool -> string
engagements_last_meeting_booked_medium -> Medium of last booking in meetings tool -> string
engagements_last_meeting_booked_source -> Source of last booking in meetings tool -> string
enviar_archivo -> PS Webform Upload Resume -> string
eres_duenoa_de_la_propiedad -> ¿Eres dueño(a) de la propiedad? -> enumeration
eres_dueo_de_la_propiedad -> ¿Eres dueño de la propiedad? -> string
eres_dueo_de_tu_casa -> ¿Eres dueño de tu casa? -> string
eres_dueo_de_tu_hogar_ -> ¿Eres dueño de tu hogar? -> string
eres_dueo_de_tu_residencia -> ¿Eres dueño de tu residencia? -> string
eres_el_dueo_legal_de_la_propiedad_o_cuentas_con_su_autorizacin -> ¿Eres el dueño legal de la propiedad o cuentas con su autorización? -> string
eres_la_persona_que_puede_autorizar_mejoras_estructurales_en_la_propiedad -> ¿Eres la persona que puede autorizar mejoras estructurales en la propiedad? -> string
es_dueo_de_la_propiedad -> Es dueño de la propiedad? -> string
espacio_en_metros_disponible__contacto_ -> Espacio Disponible en m2 (Contacto) -> string
esta_conciente_que_para_participar_tiene_que_adquirir_el_sistema_con_planet_solar -> Esta conciente que para participar tiene que adquirir el sistema con Planet Solar -> string
estas_en_casa_del_cliente_ -> Estas en casa del Cliente? (Inside Sales) -> enumeration
estatus -> Estatus -> string
estatus_de_llamada -> Estatus de Llamada (Jobs) -> enumeration
fax -> Fax Number -> string
fecha_de_atencion -> PS Date Attention -> date
fecha_de_cita__costco___captura_de_leads -> Fecha de Cita (Costco) -> date
fecha_de_cita__evento_copharma_ -> Fecha de Cita (Evento CoopPharma) -> date
fecha_de_cita__inside_sales_ -> Fecha de Cita (Inside Sales) -> datetime
fecha_de_nacimiento_ -> ¿Fecha de Nacimiento? -> date
fecha_de_primera_interaccion -> Fecha de llamada (Jobs) -> datetime
fecha_de_registro -> PS Date Registration -> date
fecha_de_registro__brilla_grartis_con_planet -> Fecha de Registro | Brilla 2026 -> datetime
fecha_de_trabajado_inside_sales -> Fecha de Trabajado (Inside Sales) -> date
fecha_del_sorteo -> Fecha del Sorteo | Brilla 2026 -> enumeration
fecha_estimada_de_contrato__contacto_ -> Fecha Estimada de Contrato (Contacto) -> date
fecha_prp__asignado -> Fecha PRP | Asignado -> datetime
fecha_prp__trabajado -> Fecha PRP | Trabajado -> datetime
field_of_study -> Field of study -> string
first_conversion_date -> First Conversion Date -> datetime
first_conversion_event_name -> First Conversion -> string
first_deal_created_date -> First Deal Created Date -> datetime
firstname -> First Name -> string
followercount -> Follower Count -> number
forma_de_pago__contacto_ -> Forma de Pago (Contacto) -> enumeration
fotos_de_la_fachada__contacto_ -> Fotos de la Fachada (Contacto) -> string
fotos_del_contador__contacto_ -> Fotos de Equipos Electricos (Contacto) -> string
fotos_del_techo_internas_y_externas__contacto_ -> Fotos del Techo Internas y Externas (Contacto) -> string
fuente_del_lead__control_ -> Fuente del Lead (Control) -> enumeration
gender -> Gender -> string
gerente__inside_sales_ -> Consultor Asignado (Inside Sales) -> enumeration
gerente_de_ventas__contacto_ -> Gerente de Ventas (Contacto) -> enumeration
gerente_division_comercial__contacto_ -> Gerente Division Comercial (Contacto) -> enumeration
graduation_date -> Graduation date -> string
has_trabajado_en_energa_solar_o_servicios_afines -> ¿Has trabajado en energía solar o servicios afines? -> string
hs_additional_emails -> Additional email addresses -> enumeration
hs_all_accessible_team_ids -> All teams -> enumeration
hs_all_assigned_business_unit_ids -> Brands -> enumeration
hs_all_contact_vids -> All vids for a contact -> enumeration
hs_all_owner_ids -> All owner IDs -> enumeration
hs_all_team_ids -> All team IDs -> enumeration
hs_analytics_average_page_views -> Average Pageviews -> number
hs_analytics_first_referrer -> First Referring Site -> string
hs_analytics_first_timestamp -> Time First Seen -> datetime
hs_analytics_first_touch_converting_campaign -> First Touch Converting Campaign -> string
hs_analytics_first_url -> First Page Seen -> string
hs_analytics_first_visit_timestamp -> Time of First Session -> datetime
hs_analytics_last_referrer -> Last Referring Site -> string
hs_analytics_last_timestamp -> Time Last Seen -> datetime
hs_analytics_last_touch_converting_campaign -> Last Touch Converting Campaign -> string
hs_analytics_last_url -> Last Page Seen -> string
hs_analytics_last_visit_timestamp -> Time of Last Session -> datetime
hs_analytics_num_event_completions -> Number of event completions -> number
hs_analytics_num_page_views -> Number of Pageviews -> number
hs_analytics_num_visits -> Number of Sessions -> number
hs_analytics_revenue -> Event Revenue -> number
hs_analytics_source -> Original Traffic Source -> enumeration
hs_analytics_source_composite_data -> Original Traffic Source Composite Data -> string
hs_analytics_source_data_1 -> Original Traffic Source Drill-Down 1 -> string
hs_analytics_source_data_2 -> Original Traffic Source Drill-Down 2 -> string
hs_associated_target_accounts -> Associated Target Accounts -> number
hs_avatar_filemanager_key -> Avatar FileManager key -> string
hs_bing_ad_clicked -> Bing ad clicked -> bool
hs_bing_click_id -> Bing click id -> string
hs_buying_role -> Buying Role -> enumeration
hs_calculated_form_submissions -> The 800 most recent form submissions for a contact -> enumeration
hs_calculated_merged_vids -> Merged vids with timestamps of a contact -> enumeration
hs_calculated_mobile_number -> Calculated Mobile Number in International Format -> string
hs_calculated_phone_number -> Calculated Phone Number in International Format -> string
hs_calculated_phone_number_area_code -> Calculated Phone Number Area Code -> string
hs_calculated_phone_number_country_code -> Calculated Phone Number Country Code -> string
hs_calculated_phone_number_region_code -> Calculated Phone Number Region -> string
hs_chat_assistant_iql_date -> Chat Assistant IQL Date -> datetime
hs_chat_assistant_source -> Chat Assistant Source -> enumeration
hs_chat_assistant_summary -> Chat Assistant:Summary -> string
hs_clicked_linkedin_ad -> Clicked on a LinkedIn Ad -> enumeration
hs_contact_creation_legal_basis_source_instance_id -> Contact creation legal basis source instance ID -> string
hs_contact_enrichment_opt_out -> Enrichment opt out -> bool
hs_contact_enrichment_opt_out_timestamp -> Enrichment opt out timestamp -> datetime
hs_content_membership_email -> Member email -> string
hs_content_membership_email_confirmed -> Email Confirmed -> bool
hs_content_membership_follow_up_enqueued_at -> Time enrolled in registration follow up emails -> datetime
hs_content_membership_notes -> Membership Notes -> string
hs_content_membership_registered_at -> Registered At -> datetime
hs_content_membership_registration_domain_sent_to -> Domain to which registration email was sent -> string
hs_content_membership_registration_email_sent_at -> Time registration email was sent -> datetime
hs_content_membership_status -> Status -> enumeration
hs_conversations_visitor_email -> Conversations visitor email -> string
hs_count_is_unworked -> Count of unengaged contacts -> number
hs_count_is_worked -> Count of engaged contacts -> number
hs_country_region_code -> Country/Region Code -> string
hs_created_by_conversations -> Created By Conversations -> bool
hs_created_by_user_id -> Created by user ID -> number
hs_createdate -> Object create date/time -> datetime
hs_cross_account_note -> Cross-Account Note -> string
hs_cross_sell_opportunity -> Cross-sell Opportunity -> bool
hs_current_customer -> Current Customer -> enumeration
hs_currently_enrolled_in_prospecting_agent -> Currently Enrolled in Prospecting Agent -> bool
hs_customer_agent_lead_status -> Customer Agent Lead Status -> enumeration
hs_data_privacy_ads_consent -> Ads Consent from Forms -> bool
hs_document_last_revisited -> Recent Document Revisit Date -> datetime
hs_email_bad_address -> Invalid email address -> bool
hs_email_bounce -> Marketing emails bounced -> number
hs_email_click -> Marketing emails clicked -> number
hs_email_customer_quarantined_reason -> Email address quarantine reason -> enumeration
hs_email_delivered -> Marketing emails delivered -> number
hs_email_domain -> Email Domain -> string
hs_email_first_click_date -> First marketing email click date -> datetime
hs_email_first_open_date -> First marketing email open date -> datetime
hs_email_first_reply_date -> First marketing email reply date -> datetime
hs_email_first_send_date -> First marketing email send date -> datetime
hs_email_hard_bounce_reason -> Email hard bounce reason -> string
hs_email_hard_bounce_reason_enum -> Email hard bounce reason -> enumeration
hs_email_is_ineligible -> Is globally ineligible -> bool
hs_email_last_click_date -> Last marketing email click date -> datetime
hs_email_last_email_name -> Last marketing email name -> string
hs_email_last_open_date -> Last marketing email open date -> datetime
hs_email_last_reply_date -> Last marketing email reply date -> datetime
hs_email_last_send_date -> Last marketing email send date -> datetime
hs_email_live_sourcing_restricted -> Email live sourcing restricted -> bool
hs_email_open -> Marketing emails opened -> number
hs_email_optimal_send_day_of_week -> Optimal Marketing Email Send Day of Week -> string
hs_email_optimal_send_time_of_day -> Optimal Marketing Email Send Time of Day  -> string
hs_email_optout -> Unsubscribed from all email -> bool
hs_email_optout_364428593 -> Opted out of email: Marketing Information -> enumeration
hs_email_optout_364428595 -> Opted out of email: Marketing Information -> enumeration
hs_email_optout_364428625 -> Opted out of email: Marketing Information -> enumeration
hs_email_optout_36748909 -> Opted out of email: Marketing Information -> enumeration
hs_email_optout_52655928 -> Opted out of email: One to One -> enumeration
hs_email_optout_78563758 -> Opted out of email: Customer Service Communication -> enumeration
hs_email_quarantined -> Email Address Quarantined -> bool
hs_email_quarantined_reason -> Email address automated quarantine reason -> enumeration
hs_email_recipient_fatigue_recovery_time -> Email Address Recipient Fatigue Next Available Sending Time -> datetime
hs_email_replied -> Marketing emails replied -> number
hs_email_sends_since_last_engagement -> Sends Since Last Engagement -> number
hs_email_type -> Email type -> enumeration
hs_emailconfirmationstatus -> Marketing email confirmation status -> enumeration
hs_employment_change_detected_date -> Employment change detected date -> date
hs_enriched_email_bounce_detected -> Enriched Email Bounce Detected (Deprecated) -> bool
hs_excluded_from_cross_account_data_mirroring -> Excluded from cross-account data mirroring -> bool
hs_facebook_ad_clicked -> Clicked Facebook ad -> bool
hs_facebook_click_id -> Facebook click id -> string
hs_facebookid -> Facebook ID -> string
hs_feedback_last_ces_survey_date -> Last CES survey date -> datetime
hs_feedback_last_ces_survey_follow_up -> Last CES survey comment -> string
hs_feedback_last_ces_survey_rating -> Last CES survey rating -> number
hs_feedback_last_csat_survey_date -> Last CSAT survey date -> datetime
hs_feedback_last_csat_survey_follow_up -> Last CSAT survey comment -> string
hs_feedback_last_csat_survey_rating -> Last CSAT survey rating -> number
hs_feedback_last_nps_follow_up -> Last NPS survey comment -> string
hs_feedback_last_nps_rating -> Last NPS survey rating (deprecated) -> enumeration
hs_feedback_last_nps_rating_number -> Latest NPS survey rating -> number
hs_feedback_last_survey_date -> Last NPS survey date -> datetime
hs_feedback_show_nps_web_survey -> Should be shown an NPS web survey -> bool
hs_first_closed_order_id -> First Closed Order ID -> number
hs_first_engagement_object_id -> ID of first engagement -> number
hs_first_order_closed_date -> First Order Closed Date -> datetime
hs_first_outreach_date -> First outreach date -> datetime
hs_first_subscription_create_date -> First subscription create date -> datetime
hs_full_name_or_email -> Full name or email -> string
hs_geohash_1 -> geohash_1 -> string
hs_geohash_2 -> geohash_2 -> string
hs_geohash_3 -> geohash_3 -> string
hs_geohash_4 -> geohash_4 -> string
hs_geohash_5 -> geohash_5 -> string
hs_geohash_6 -> geohash_6 -> string
hs_google_click_id -> Google ad click id -> string
hs_googleplusid -> googleplus ID -> string
hs_gps_error -> GPS Error -> string
hs_gps_latitude -> Latitudes -> string
hs_gps_longitude -> Longitudes -> string
hs_has_active_subscription -> Contact has an active subscription -> number
hs_inferred_language_codes -> Inferred Language Codes -> enumeration
hs_intent_paid_up_to_date -> Intent paid up to date -> date
hs_intent_signals_enabled -> Intent Signals active -> bool
hs_ip_timezone -> IP Timezone -> string
hs_is_contact -> Is a contact -> bool
hs_is_enriched -> Has been enriched -> bool
hs_is_merge_revertible -> Is Merge Revertible -> bool
hs_is_unworked -> Contact unworked -> bool
hs_job_change_detected_date -> Job change detected date -> date
hs_journey_stage -> Journey Stage -> enumeration
hs_language -> Preferred language -> enumeration
hs_last_metered_enrichment_timestamp -> Last Metered Enrichment Timestamp -> datetime
hs_last_sales_activity_date -> last sales activity date old -> datetime
hs_last_sales_activity_timestamp -> Last Engagement Date -> datetime
hs_last_sales_activity_type -> Last Engagement Type -> enumeration
hs_last_sms_send_date -> Last Sms Send Date -> datetime
hs_last_sms_send_name -> Last SMS Send Name -> string
hs_lastmodifieddate -> Object last modified date/time -> datetime
hs_latest_disqualified_lead_date -> Latest Disqualified Lead Date -> datetime
hs_latest_meeting_activity -> Latest meeting activity -> datetime
hs_latest_open_lead_date -> Latest Open Lead Date -> datetime
hs_latest_qualified_lead_date -> Latest Qualified Lead Date -> datetime
hs_latest_sequence_ended_date -> Last sequence ended date -> datetime
hs_latest_sequence_enrolled -> Last sequence enrolled -> number
hs_latest_sequence_enrolled_date -> Last sequence enrolled date -> datetime
hs_latest_sequence_finished_date -> Last sequence finished date -> datetime
hs_latest_sequence_unenrolled_date -> Last sequence unenrolled date -> datetime
hs_latest_source -> Latest Traffic Source -> enumeration
hs_latest_source_composite_data -> Latest Traffic Source Composite Data -> string
hs_latest_source_data_1 -> Latest Traffic Source Drill-Down 1 -> string
hs_latest_source_data_2 -> Latest Traffic Source Drill-Down 2 -> string
hs_latest_source_timestamp -> Latest Traffic Source Date -> datetime
hs_latest_subscription_create_date -> Latest subscription create date -> datetime
hs_latitude -> Latitude -> number
hs_lead_status -> Lead Status -> enumeration
hs_legal_basis -> Legal basis for processing contact's data -> enumeration
hs_linkedin_ad_clicked -> Clicked LinkedIn Ad -> enumeration
hs_linkedin_click_id -> LinkedIn click id -> string
hs_linkedin_url -> LinkedIn URL -> string
hs_linkedinid -> Linkedin ID -> string
hs_live_enrichment_deadline -> Live enrichment deadline -> datetime
hs_longitude -> Longitude -> number
hs_manual_campaign_ids -> Manual campaign ids -> number
hs_marketable_reason_id -> Marketing contact status source name -> string
hs_marketable_reason_type -> Marketing contact status source type -> enumeration
hs_marketable_status -> Marketing contact status -> enumeration
hs_marketable_until_renewal -> Marketing contact until next update -> enumeration
hs_membership_has_accessed_private_content -> Member has accessed private content -> number
hs_membership_last_private_content_access_date -> Membership last private content access date -> datetime
hs_merged_object_ids -> Merged Contact IDs -> enumeration
hs_messaging_engagement_score -> messaging_engagement_score -> number
hs_mobile_sdk_push_tokens -> Mobile Sdk Push Tokens -> string
hs_notes_last_activity -> Last Activity -> object_coordinates
hs_notes_next_activity -> Next Activity -> object_coordinates
hs_notes_next_activity_type -> Next Activity Type -> enumeration
hs_num_associated_open_deals -> Number of open deals -> number
hs_object_id -> Record ID -> number
hs_object_source -> Record creation source -> string
hs_object_source_detail_1 -> Record source detail 1 -> string
hs_object_source_detail_2 -> Record source detail 2 -> string
hs_object_source_detail_3 -> Record source detail 3 -> string
hs_object_source_id -> Record creation source ID -> string
hs_object_source_label -> Record source -> enumeration
hs_object_source_user_id -> Record creation source user ID -> number
hs_owning_teams -> Owning Teams -> enumeration
hs_persona -> Persona -> enumeration
hs_pinned_engagement_id -> Pinned engagement ID -> number
hs_pipeline -> Pipeline -> enumeration
hs_predictivecontactscore -> Predictive Lead Score -> number
hs_predictivecontactscore_v2 -> Likelihood to close -> number
hs_predictivecontactscorebucket -> Lead Rating -> enumeration
hs_predictivescoringtier -> Contact priority -> enumeration
hs_prospecting_agent_actively_enrolled_count -> Prospecting Agent Actively Enrolled Count -> number
hs_prospecting_agent_enrollment_status -> Prospecting Agent Enrollment Status -> enumeration
hs_prospecting_agent_last_enrolled -> Prospecting Agent Last Enrolled -> datetime
hs_prospecting_agent_sender -> Prospecting Agent Sender -> enumeration
hs_prospecting_agent_total_enrolled_count -> Prospecting Agent Total Enrolled Count -> number
hs_quarantined_emails -> Quarantined Emails -> string
hs_read_only -> Read only object -> bool
hs_recent_closed_order_date -> Recent Closed Order Date -> datetime
hs_registered_member -> Registered member -> number
hs_registration_method -> Registration Method -> string
hs_returning_to_office_detected_date -> Returning to office detected date -> date
hs_role -> Employment Role -> enumeration
hs_sa_first_engagement_date -> Date of first engagement -> datetime
hs_sa_first_engagement_descr -> Description of first engagement -> enumeration
hs_sa_first_engagement_object_type -> Type of first engagement -> enumeration
hs_sales_email_last_clicked -> Recent Sales Email Clicked Date -> datetime
hs_sales_email_last_opened -> Recent Sales Email Opened Date -> datetime
hs_sales_email_last_replied -> Recent Sales Email Replied Date -> datetime
hs_searchable_calculated_international_mobile_number -> Calculated Mobile Number with country code -> string
hs_searchable_calculated_international_phone_number -> Calculated Phone Number with country code -> string
hs_searchable_calculated_mobile_number -> Calculated Mobile Number without country code -> phone_number
hs_searchable_calculated_phone_number -> Calculated Phone Number without country code -> phone_number
hs_seniority -> Employment Seniority -> enumeration
hs_sequences_actively_enrolled_count -> Number of sequences actively enrolled -> number
hs_sequences_enrolled_count -> Number of sequences enrolled -> number
hs_sequences_is_enrolled -> Currently in Sequence -> bool
hs_shared_team_ids -> Shared teams -> enumeration
hs_shared_user_ids -> Shared users -> enumeration
hs_social_facebook_clicks -> Facebook Clicks -> number
hs_social_google_plus_clicks -> Google Plus Clicks -> number
hs_social_last_engagement -> Most Recent Social Click -> datetime
hs_social_linkedin_clicks -> LinkedIn Clicks -> number
hs_social_num_broadcast_clicks -> Broadcast Clicks -> number
hs_social_twitter_clicks -> Twitter Clicks -> number
hs_source_object_id -> Source Object ID -> number
hs_source_portal_id -> Source Portal ID -> number
hs_sourced_contact_origin -> Sourced Contact Origin -> enumeration
hs_state_code -> State/Region Code -> string
hs_sub_role -> Employment Sub Role -> enumeration
hs_testpurge -> testpurge -> string
hs_testrollback -> testrollback -> string
hs_tiktok_ad_clicked -> TikTok ad clicked -> bool
hs_tiktok_click_id -> TikTok click id -> string
hs_time_between_contact_creation_and_deal_close -> Time between contact creation and deal close -> number
hs_time_between_contact_creation_and_deal_creation -> Time between contact creation and deal creation -> number
hs_time_to_first_engagement -> Lead response time -> number
hs_time_to_move_from_lead_to_customer -> Time to move from lead to customer -> number
hs_time_to_move_from_marketingqualifiedlead_to_customer -> Time to move from marketing qualified lead to customer -> number
hs_time_to_move_from_opportunity_to_customer -> Time to move from opportunity to customer -> number
hs_time_to_move_from_salesqualifiedlead_to_customer -> Time to move from sales qualified lead to customer -> number
hs_time_to_move_from_subscriber_to_customer -> Time to move from subscriber to customer -> number
hs_timezone -> Time Zone -> enumeration
hs_twitterid -> Twitter ID -> string
hs_unique_creation_key -> Unique creation key -> string
hs_updated_by_user_id -> Updated by user ID -> number
hs_user_ids_of_all_notification_followers -> User IDs of all notification followers -> enumeration
hs_user_ids_of_all_notification_unfollowers -> User IDs of all notification unfollowers -> enumeration
hs_user_ids_of_all_owners -> User IDs of all owners -> enumeration
hs_v2_cumulative_time_in_1293308728 -> Cumulative time in "Intento de Contacto (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293308730 -> Cumulative time in "Propuesta Enviada (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293548298 -> Cumulative time in "En Conversacion (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293548443 -> Cumulative time in "Inside Leads (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293549229 -> Cumulative time in "Negociacion (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293550221 -> Cumulative time in "Interes Confirmado (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_1293560724 -> Cumulative time in "Negativo | Perdido (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_customer -> Cumulative time in "Cierre | Ganado (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_lead -> Cumulative time in "Nuevo Leads (Lifecycle Stage Pipeline)" -> number
hs_v2_cumulative_time_in_opportunity -> Cumulative time in "Opportunity (Lifecycle Stage Pipeline)" -> number
hs_v2_date_entered_1293308728 -> Date entered "Intento de Contacto (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293308730 -> Date entered "Propuesta Enviada (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293548298 -> Date entered "En Conversacion (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293548443 -> Date entered "Inside Leads (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293549229 -> Date entered "Negociacion (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293550221 -> Date entered "Interes Confirmado (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_1293560724 -> Date entered "Negativo | Perdido (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_current_stage -> Date entered current stage -> datetime
hs_v2_date_entered_customer -> Date entered "Cierre | Ganado (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_lead -> Date entered "Nuevo Leads (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_entered_opportunity -> Date entered "Opportunity (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293308728 -> Date exited "Intento de Contacto (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293308730 -> Date exited "Propuesta Enviada (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293548298 -> Date exited "En Conversacion (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293548443 -> Date exited "Inside Leads (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293549229 -> Date exited "Negociacion (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293550221 -> Date exited "Interes Confirmado (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_1293560724 -> Date exited "Negativo | Perdido (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_customer -> Date exited "Cierre | Ganado (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_lead -> Date exited "Nuevo Leads (Lifecycle Stage Pipeline)" -> datetime
hs_v2_date_exited_opportunity -> Date exited "Opportunity (Lifecycle Stage Pipeline)" -> datetime
hs_v2_latest_time_in_1293308728 -> Latest time in "Intento de Contacto (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293308730 -> Latest time in "Propuesta Enviada (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293548298 -> Latest time in "En Conversacion (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293548443 -> Latest time in "Inside Leads (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293549229 -> Latest time in "Negociacion (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293550221 -> Latest time in "Interes Confirmado (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_1293560724 -> Latest time in "Negativo | Perdido (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_customer -> Latest time in "Cierre | Ganado (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_lead -> Latest time in "Nuevo Leads (Lifecycle Stage Pipeline)" -> number
hs_v2_latest_time_in_opportunity -> Latest time in "Opportunity (Lifecycle Stage Pipeline)" -> number
hs_v2_time_in_current_stage -> Time in current stage -> datetime
hs_was_imported -> Performed in an import -> bool
hs_whatsapp_phone_number -> WhatsApp Phone Number -> string
hs_why_this_contact -> Why This Contact -> string
hubspot_owner_assigneddate -> Owner assigned date -> datetime
hubspot_owner_id -> Contact owner -> enumeration
hubspot_team_id -> HubSpot Team -> enumeration
hubspotscore -> HubSpot Score -> number
id_de_goformz__contacto_ -> ID de GoFormz (Contacto) -> number
inbox_url -> PS FaceBook Inbox URL -> string
industry -> Industry -> string
intento_de_contacto__inside_sales_ -> Intento de Contacto (Inside Sales) -> enumeration
interes__costco___captura_de_leads_ -> Interes (Costco) -> enumeration
interes__evento_copharma_ -> Interes (Evento CoopPharma) -> enumeration
interes_tipo_de_compra__contacto_ -> Interes Tipo de Compra (Contacto) -> enumeration
ip_city -> IP City -> string
ip_country -> IP Country -> string
ip_country_code -> IP Country Code -> string
ip_latlon -> IP Latitude & Longitude -> string
ip_state -> IP State/Region -> string
ip_state_code -> IP State Code/Region Code -> string
ip_zipcode -> IP Zipcode -> string
job_function -> Job function -> string
jobtitle -> Job Title -> string
kloutscoregeneral -> Klout Score -> number
kw_tipo_de_panel__contacto_ -> kW Tipo de Panel (Contacto) -> number
la_casa_es_de_su_popiedad -> La casa es de su Popiedad? -> string
lastmodifieddate -> Last Modified Date -> datetime
lastname -> Last Name -> string
latitud__contacto_ -> Latitud (Contacto) -> string
lifecyclestage -> Lifecycle Stage -> enumeration
linkedinbio -> LinkedIn Bio -> string
linkedinconnections -> LinkedIn Connections -> number
longitud__contacto_ -> Longitud (Contacto) -> string
marital_status -> Marital Status -> string
material_del_techo__contacto_ -> Material del Techo (Contacto) -> enumeration
mejor_horario_para_contactarte -> Mejor horario para contactarte: -> string
message -> Message -> string
military_status -> Military status -> string
mobilephone -> Mobile Phone Number -> string
municipio_de_residencia -> Municipio de residencia -> string
municipios_co__contacto_ -> Municipios CO (Contacto) -> enumeration
nombre_de_la_empresa__evento_cooppharma_ -> Nombre de la Empresa (Evento CoopPharma) -> string
nombre_del_consultor__cambaceo_ -> Nombre del Consultor (Cambaceo) -> string
nos_visitas_como -> ¿Nos visitas como? -> string
notas -> Notas -> string
notas__booth_ -> Notas (Booth) -> string
notas__costco___captura_de_leads_ -> Notas (Costco) -> string
notas__evento_baby_boomers_expo_2024_ -> Notas (Evento Baby Boomers Expo 2024) -> string
notas__evento_copharma_ -> Notas (Evento CoopPharma) -> string
notas__sanse_caguas_2025_ -> Notas (Sanse Caguas 2025) -> string
notas__sanse_san_juan_2025_ -> Notas (Sanse San Juan 2025) -> string
notes_last_contacted -> Last Contacted -> datetime
notes_last_updated -> Last Activity Date -> datetime
notes_next_activity_date -> Next Activity Date -> datetime
num_associated_deals -> Number of Associated Deals -> number
num_contacted_notes -> Number of times contacted -> number
num_conversion_events -> Number of Form Submissions -> number
num_notes -> Number of Sales Activities -> number
num_unique_conversion_events -> Number of Unique Forms Submitted -> number
numemployees -> Number of Employees -> enumeration
numero_de_cliente__contacto_ -> Número de Cliente (Contacto) -> number
numero_de_cuenta_luma__contactos_ -> ID localidad | LUMA (Contactos) -> number
numero_de_seguro_social -> Número de seguro social (Inside Sales) -> number
owneremail -> HubSpot Owner Email (legacy) -> string
ownername -> HubSpot Owner Name (legacy) -> string
pago_luma -> Pago LUMA (Facebook Form) -> string
participaciones_concurso -> Participaciones Concurso | Brilla 2026 -> enumeration
permitir_entrada_a_master_2 -> Permitir entrada a Master #2 -> bool
phone -> Phone Number -> string
photo -> Photo -> string
pin_de_ubicacion -> PIN de Ubicacion -> string
por_que_medio_te_enteraste_de_nosotros___inside_sales_ -> ¿Por que medio te enteraste de nosotros? (Inside Sales) -> enumeration
posicion -> Posicion -> string
post_cita___fecha__inside_sales_ -> Post Cita | Fecha (Inside Sales) -> date
post_cita___medio__inside_sales_ -> Post Cita | Medio (Inside sales) -> enumeration
post_cita___status__inside_sales_ -> Post Cita | Status (Inside Sales) -> enumeration
preferencia_de_cita -> Preferencia de Cita (Costco) -> enumeration
preferencia_de_cita__evento_copharma_ -> Preferencia de Cita (Evento CoopPharma) -> enumeration
preferencia_de_cita__formulario_ -> Preferencia de Cita (Formulario) -> enumeration
producto_interesado -> PS Webform Product Interested -> enumeration
promotor_a____costco___captura_de_leads -> Representante (Costco) -> enumeration
propietario_adicional_costco_ -> Propietario Adicional -> enumeration
ps_col_departamentos -> Departamento CO (Contacto) -> enumeration
ps_consultant_email -> PS Consultant Email -> string
ps_country -> PS País -> enumeration
ps_event_name -> Nombre del Evento (Old) -> enumeration
ps_interes_comentarios -> PS Interés/Comentarios -> string
ps_marca_a_la_que_pertenece -> PS Marca a la que pertenece -> enumeration
ps_otros_type_of_bussiness -> PS Otros Type of Bussiness -> string
ps_pdf_1 -> PS PDF 1 -> string
ps_producto_de_interes -> PS Producto de Interés -> enumeration
ps_telephone_prefix_1 -> PS Telephone Prefix 1 -> enumeration
ps_type_of_business -> PS Type of Business -> enumeration
pueblo__desplegable -> Municipios PR (Contactos) -> enumeration
pueblo_donde_vives -> Pueblo donde vives? -> string
puesto_del_contacto__contacto_ -> Puesto del Cliente (Contacto) -> string
qu_es_ms_importante_para_ti -> ¿Qué es más importante para ti? -> string
qu_productos_te_interesan -> ¿Qué productos te interesan? -> string
qu_te_interesa_ms -> ¿Qué te interesa más? -> string
qu_tipo_de_sistema_te_interesa -> ¿Qué tipo de sistema te interesa? -> string
qu_tipo_de_solucin_te_interesa -> ¿Qué tipo de solución te interesa? -> string
que_busca_en_un_sistema_de_energa_renovable -> Que busca en un sistema de energía renovable? -> string
que_deseas_de_tu_sistema_de_energia_renovable_con_planet_solar -> Que deseas de tu sistema de energia renovable con Planet Solar? -> string
que_estas_solicitando___inside_sales_ -> Que estas solicitando? (Inside Sales) -> enumeration
que_necesitas_cotizar -> ¿Qué necesitas cotizar? -> enumeration
que_posicin_estas_buscando -> ¿Que posición estas buscando? -> string
que_tipo_de_sistema_desea_cotizar_ -> ¿Que tipo de sistema desea cotizar? -> string
que_tipo_de_techo_tiene_su_propiedad -> Que tipo de techo tiene su propiedad -> string
quien_lo_refirio -> ¿Alguien te refirió al concurso? -> string
recent_conversion_date -> Recent Conversion Date -> datetime
recent_conversion_event_name -> Recent Conversion -> string
recent_deal_amount -> Recent Deal Amount -> number
recent_deal_close_date -> Recent Deal Close Date -> datetime
recheck_validacion -> Recheck Validacion -> enumeration
recibo_de_luma -> Ultima Factura de Electricidad (Contactos) -> string
regin_de_inters_ -> Región de interés -> string
region_asociada -> PS Region Assigned -> enumeration
registro_del_concurso -> Registro del Concurso | Brilla 2026 -> enumeration
relationship_status -> Relationship Status -> string
retencion_por_lead_asignado__brilla_2026 -> Retención por Lead Asignado | Brilla 2026 -> bool
salutation -> Salutation -> string
school -> School -> string
seniority -> Seniority -> string
si_no_resultas_ganadora_te_gustara_recibir_una_evaluacin_gratuita_para_conocer_cunto_podras_ahorrar -> Si no resultas ganador(a), ¿te gustaría recibir una evaluación gratuita para conocer cuánto podrías ahorrar con energía solar? -> string
start_date -> Start date -> string
state -> State/Region -> string
su_recibo_de_luz_esta_a_nombre_suyo_ -> ¿Su recibo de Luz esta a nombre suyo?  -> enumeration
sunhouz___estado_de_lead -> PS Lead Calification -> enumeration
surveymonkeyeventlastupdated -> SurveyMonkey Event Last Updated -> number
te_interesa_recibir_capacitaciones_sobre_productos_sunhouz -> ¿Te interesa recibir capacitaciones sobre productos Sunhouz? -> string
telefono_alterno_del_cliente -> Teléfono Alterno del Cliente -> string
telefono_del_consultor__contacto_ -> Teléfono del Consultor (Contacto) -> string
tiempo_asignacion_de_propietario_vs_ultima_actividad -> Tiempo Asignacion de Propietario vs Ultima Actividad -> number
tiempo_autonomia_cargas_criticas__negocios___clonada_ -> Tiempo Autonomia Cargas Esenciales (Contacto) -> enumeration
tiene_casa_propia_o_rentada -> Tiene casa propia o rentada? -> string
tiene_de_empirica_de_credito_mas_de_650_ -> Tiene de empirica de credito mas de 650 -> string
tiene_mas_de_650_de_empirica_de_credito -> Tiene mas de 650 de empirica de credito? -> string
tienes_experiencia_previa_instalando_sistemas_solares -> ¿Tienes experiencia previa instalando sistemas solares? -> string
tienes_generador_o_sistema_solar_actualmente -> ¿Tienes generador o sistema solar actualmente? -> string
tipo_de_bateria__contacto_ -> Tipo de Batería (Contacto) -> enumeration
tipo_de_cargador__contacto_ -> Tipo de Cargador (Contacto) -> enumeration
tipo_de_cliente_sunhouz_pa -> ¿Cual es tu Perfil? -> enumeration
tipo_de_instalacion -> Tipo de Instalacion -> enumeration
tipo_de_inversor__contacto_ -> Tipo de Inversor (Contacto) -> enumeration
tipo_de_montaje -> Tipo de Montaje (Contacto) -> enumeration
tipo_de_negociacion_residencial_o_comercial__clonado_ -> Tipo de negociación Residencial o Comercial (Contacto) -> enumeration
tipo_de_negocio__contactos_ -> Tipo de Negocio (Contacto) -> enumeration
tipo_de_propiedad_ -> Tipo de Propiedad -> string
tipo_de_representante__costco_ -> Tipo de Representante (Costco) -> enumeration
tipo_de_servicio_electrico__contacto_ -> Tipo de Servicio Eléctrico (Contacto) -> enumeration
tipo_de_sistema_requerido -> Tipo de sistema requerido -> string
tipo_de_solicitud_pqr -> Tipo de Solicitud PQR -> enumeration
tipo_de_techo -> Material Superficie Techo (Contacto) -> enumeration
total_cargas_criticas_del_dia_kwh__contacto_ -> Total Cargas Esenciales del Dia kWh (Contacto) -> string
total_revenue -> Total Revenue -> number
twitterbio -> Twitter Bio -> string
twitterhandle -> Twitter Username -> string
twitterprofilephoto -> Twitter Profile Photo -> string
ubicacion_propiedad__contacto_ -> Ubicacion Propiedad (Contacto) -> string
ultimos_4_numeros_del_seguro_social_ -> ¿Últimos 4 Números del Seguro Social? -> number
usted_es_dueno_de_la_propiedad -> Usted es dueno de la propiedad? -> string
usted_es_dueno_del_hogar_ -> ¿Usted es dueño del Hogar? -> enumeration
validacion_concurso -> Validacion Concurso | Brilla 2026 -> enumeration
via_de_ingreso_del_lead___inside_sales_ -> ¿Via de ingreso del Lead? (Inside Sales) -> enumeration
webinareventlastupdated -> Webinar Event Last Updated -> number
website -> Website URL -> string
work_email -> Work email -> string
ya_cuentas_con_sistema_solar_instalado -> ¿Ya cuentas con sistema solar instalado? -> string
zip -> Postal Code -> string


PARA LA BUSQUEDA Y COMPARACION NECESITAMOS:
FALTA hs_ticket_id -> ID de ticket
hs_object_id -> ID de registro
_C_FIRSTNAME = "firstname"
_C_LASTNAME = "lastname"
_C_ID_GOFORMZ = "id_de_goformz__contacto_"
_C_ADDRESS = "direccion__fisica_"
_C_PHONE = "phone"
_C_PHONE_ALT = "telefono_alterno_del_cliente"
_C_EMAIL = "email"
_C_STATE = "country"  # "Estado" está en el campo country
_C_MUNICIPIO = "municipio_de_residencia"
_C_MUNICIPIO_CO = "municipios_co__contacto_"
_C_STATE2 = "state"
_C_ZIP = "zip"
````

## File: data/PROPIEDADES DE TICKET.TXT
````
estatus_quickbooks_comisiones -> Estatus Quickbooks Comisiones
estatus_quickbooks_underwriting -> Estatus Quickbooks (Underwriting)
estatus_rrhh -> Estatus RRHH
estatus_sunrun -> Sunrun | Status
factura_con_cargo_100_usd -> Factura con Cargo 100 USD
factura_luma -> Factura Luma
fce___agendar__low_fico_score_ -> FCE - Agendar (low fico score)
fce___aprobacion_cliente___sunrun -> FCE - Aprobacion Cliente | Sunrun
fce___cambio_de_pk_y_o___de_cliente -> FCE - Cambio de PK y/o # de Cliente
fce___costos_aprobados__adicionales_ -> FCE - Costos Adicionales Aprobados
fce___cover_sheet_pendiente -> FCE - Cover Sheet Pendiente
fce___diseno -> FCE - Diseño
fce___en_proceso_para_agendar -> FCE - En Proceso para Agendar
fce___listo_para_agendar -> FCE - Listo para agendar
fce___revision_del_caso -> FCE - Revisión del Caso
fce___visita -> FCE - Visita
fce___visita_tecnica_realizada -> FCE - Visita técnica realizada
fce___visitado__low_fico_score_ -> FCE - Visitado (low fico score)
fce___visitas_tecnicas -> FCE - Visitas técnicas
fecha_aprobado_m1 -> Fecha Aprobado M1
fecha_de_aporbacion___sati__clonado_ -> Fecha de Aporbacion - SATI
fecha_de_aprobado -> Fecha de Aprobado
fecha_de_aprobado_m3 -> Fecha de aprobado M3
fecha_de_cierre__revision_ -> Fecha de Cierre (Revision)
fecha_de_cierre_luma -> Fecha de Cierre LUMA Reparacion
fecha_de_comienzo_rrhh -> Fecha de Comienzo RRHH
fecha_de_construccion -> IF | Fecha de Construccion
fecha_de_creacion__sra_parent_proposal_ -> Fecha de Creacion (SRA Parent Proposal) (Tickets)
fecha_de_entrega_de_carpeta -> Fecha de Entrega de Carpeta
fecha_de_firma_de_contrato__ticket_ -> Fecha de firma de contrato (Ticket)
fecha_de_instalacion -> Fecha de Instalación Agendada (Tickets)
fecha_de_instalacion_completada -> Fecha de Instalacion Completada (Tickets)
fecha_de_nacimiento -> Fecha de Nacimiento
fecha_de_ntp -> FCE - Fecha de NTP (Tickets)
fecha_de_orden_puesta -> Fecha de Orden Puesta Reparacion
fecha_de_primer_pago -> Comision | Fecha 1ra Etapa Trabajada
fecha_de_programacion -> Fecha de programación
fecha_de_referido__interventor_ -> FCE - Fecha de Referido (Interventor)
fecha_de_referido_a_revisado -> Fecha Revisado
fecha_de_referido_a_revision -> Fecha a Revision
fecha_de_reparacion_terminada -> Fecha de Reparación Terminada
fecha_de_revision_m1 -> Fecha de revisión M1
fecha_de_revision_m2 -> Fecha de revisión M2
fecha_de_segundo_pago -> Comision | Fecha 2da Etapa Trabajada
fecha_de_solicitud___sati__clonado_ -> Fecha de Solicitud - SATI
fecha_de_solicitud_de_cancelacion -> Fecha de Solicitud de Cancelación
fecha_de_sometido_a_luma -> Fecha de Sometido a Luma
fecha_de_sometido_m1 -> Fecha de Sometido M1
fecha_de_sometido_m2 -> Fecha Aprobado M2
fecha_de_sometido_m2_ -> Fecha de Sometido M2
fecha_de_sometido_m3 -> Fecha de Sometido M3
fecha_de_sra__tickets_ -> Fecha de SRA (Tickets)
fecha_de_terminacion -> Fecha de Terminación RRHH
fecha_de_trabajado -> Fecha de Trabajado
fecha_de_ultima_actualizacion_luma -> Fecha de última actualización LUMA
fecha_de_ultimo_intento -> Fecha de último intento
fecha_de_visita_luma -> Fecha de Visita LUMA Reparacion
fecha_de_visita_tecnica -> Fecha de Visita Tecnica
fecha_de_visitsa_de_ing -> Fecha de visita Delineante de Campo (Tickets)
fecha_delineado -> Fecha Delineado
fecha_detenido__ingeneria_ -> FCE - Detenido
fecha_entrega_m1 -> Fecha Entrega M1
fecha_entrega_m2 -> Fecha Entrega M2
fecha_entrega_m3 -> Fecha Entrega M3
fecha_escalado_a_cotizacion -> Fecha Escalado a Cotizacion
fecha_escalado_regulacion -> Fecha Escalado Regulación
fecha_expiracion_credito__underwriting_ -> Sunrun | Fecha Expiracion Credito (Underwriting)
fecha_finalizado_regulacion -> Fecha Finalizado Regulación
fecha_inicio_m1 -> Fecha Inicio M1
fecha_inicio_m2 -> Fecha Inicio M2
fecha_inicio_m3 -> Fecha Inicio M3
fecha_llamada_de_bienvenida -> Fecha Llamada de Bienvenida
fecha_recibido__revision_ -> Fecha Recibido (Revision)
fecha_referido_a_sunrun -> Fecha Referido a Sunrun
fecha_referido_reubicacion_a_c -> Fecha referido reubicación A/C
fecha_revision_m3 -> Fecha revisión M3
fecha_tarifa_aplicada_luma -> Fecha tarifa aplicada LUMA
fecha_terminacion_reubicacion_a_c -> Fecha terminación reubicación A/C
fecha_ultima_revision__milestone_ -> Fecha Ultima revisión (Milestone)
fic -> FIC
final_payment_receipt_status -> ⍟ Final Payment Receipt Status
financial_status_installation -> ⍟ Financial Status Installation
financiamiento -> Financiamiento
first_agent_reply_date -> First agent email response date
formulario_de_reembolso_100_usd -> Formulario de Reembolso 100 USD
foto_medidor -> Foto Medidor
fotos__millestone_ -> 4 Fotos (Milestone)
fsd__ -> FSD #
gateway_s_n -> Gateway S/N
gd_permits -> ⍟ GD Permits
green_line -> Green Line
hora_de_instalacion -> Hora de instalación
hora_de_programacion -> Hora de programación
hora_de_visita_de_ing -> Hora de Visita Delineante de Campo 
hs_added_to_waitlist_at -> Added to waitlist at
hs_all_accessible_team_ids -> All teams
hs_all_assigned_business_unit_ids -> Brands
hs_all_associated_contact_companies -> All associated contact companies
hs_all_associated_contact_emails -> All associated contact emails
hs_all_associated_contact_firstnames -> All associated contact first names
hs_all_associated_contact_lastnames -> All associated contact last names
hs_all_associated_contact_mobilephones -> All associated contact mobile phones
hs_all_associated_contact_phones -> All associated contact phones
hs_all_conversation_mentions -> All conversation mentions
hs_all_owner_ids -> All owner IDs
hs_all_team_ids -> All team IDs
hs_all_topics_added_by_user -> All topics added by user
hs_all_topics_mentioned -> All topics mentioned
hs_all_topics_removed_by_user -> All topics removed by user
hs_applied_sla_rule_config_at -> Applied SLA Rule Config Date
hs_applied_sla_rule_config_id -> Applied SLA Rule Config ID
hs_applied_sla_schedule_at -> Applied SLA Schedule Date
hs_applied_sla_schedule_id -> Applied SLA Schedule Id
hs_assigned_team_ids -> Assigned Teams
hs_assignment_method -> Assignment Method
hs_auto_generated_from_thread_id -> Auto-generated from thread id
hs_conversations_originating_message_id -> Originating Conversations Message Id
hs_conversations_originating_thread_id -> Conversations originating thread id
hs_copied_at -> Copied at
hs_copied_by_user -> Copied by user
hs_copied_from_ticket -> Copied ticket
hs_copied_ticket_source -> Copied ticket source
hs_created_by_user_id -> Created by user ID
hs_createdate -> HubSpot create date
hs_current_generic_channel_id -> Current channel
hs_custom_inbox -> Custom inbox ID
hs_customer_agent_escalated_time -> Customer Agent escalated time
hs_customer_agent_matched_segment -> Customer Agent Matched Segment
hs_customer_agent_ticket_status -> Customer Agent ticket status
hs_cx_score_range -> CX Score range
hs_draft_user_ids -> Draft UserIds
hs_email_subject -> Email subject
hs_external_object_ids -> External object ids
hs_feedback_last_ces_follow_up -> Last CES survey comment
hs_feedback_last_ces_rating -> Last CES survey rating
hs_feedback_last_nps_rating_number -> Latest NPS survey rating
hs_feedback_last_survey_date -> Last CES survey date
hs_file_upload -> File upload
hs_first_agent_message_sent_at -> First agent response date
hs_first_agent_message_sent_by -> First responding rep
hs_first_assignee_type -> First Assignee Type
hs_first_visitor_message_sentiment -> (Deprecated) First message sentiment
hs_first_visitor_message_sentiment_score -> First message sentiment score
hs_form_id -> Form
hs_form_submission_conversion_id -> Form submission conversion ID 
hs_has_live_chat_ended_or_email_sent -> Has live chat ended or email sent
hs_help_desk_onboarding_ticket -> Help Desk onboarding ticket
hs_helpdesk_sort_timestamp -> Helpdesk Sort Timestamp
hs_in_helpdesk -> In Help Desk
hs_in_waitlist -> In Waitlist
hs_inbox_id -> Inbox ID
hs_is_closed -> Closed
hs_is_closed_in_time_to_close_sla_count -> Is Closed in Time to Close Sla Count
hs_is_closed_in_time_to_first_response_sla_count -> Is Closed in Time to First Response Sla Count
hs_is_latest_message_failed -> Is latest message failed
hs_is_latest_message_hidden_from_all -> Is latest message hidden from all
hs_is_one_touch_ticket -> First contact resolution
hs_is_visible_in_help_desk -> Is Visible in Help desk
hs_last_closed_date -> Last Closed Date
hs_last_csat_comment -> Last CSAT survey comment
hs_last_csat_date -> Last CSAT survey date
hs_last_csat_rating -> Last CSAT survey rating
hs_last_email_activity -> Last email activity
hs_last_email_date -> Last email date
hs_last_email_details -> Last email details
hs_last_email_type -> Last Email Type
hs_last_message_from_visitor -> Last message from visitor
hs_last_message_received_at -> Last message received date
hs_last_message_sent_at -> Last response date
hs_last_nps_survey_comment -> Last NPS survey comment
hs_last_visitor_message_sentiment -> (Deprecated) Last message sentiment
hs_last_visitor_message_sentiment_score -> Latest message sentiment score
hs_lastactivitydate -> Last activity date
hs_lastcontacted -> Last contacted date
hs_lastmodifieddate -> Last modified date
hs_latest_message_attachment_types -> Latest message attachment types
hs_latest_message_is_forwarded_email -> Latest message is forwarded email
hs_latest_message_is_thread_comment -> Latest message is thread comment
hs_latest_message_seen_by_agent_ids -> Latest message seen by agent ids
hs_latest_message_visible_to_visitor -> Latest message visible to visitor
hs_latest_message_visible_to_visitor_sent_at -> Latest message visible to visitor sent at
hs_mentioned_note_user_ids -> mentioned_note_user_ids
hs_mentions_resolved_user_ids -> hs_mentions_resolved_user_ids
hs_mentions_user_ids -> mentions_user_ids
hs_merged_object_ids -> Merged Ticket IDs
hs_most_relevant_sla_status -> Most relevant SLA status
hs_most_relevant_sla_type -> Most Relevant SLA Type
hs_msteams_message_id -> Microsoft Teams message ID for this ticket.
hs_nextactivitydate -> Next activity date
hs_notes_last_activity -> Last Activity
hs_notes_next_activity -> Next Activity
hs_notes_next_activity_type -> Next Activity Type
hs_num_associated_companies -> Number of Associated Companies
hs_num_associated_conversations -> Number of Associated Conversations
hs_num_times_contacted -> Number of times contacted
hs_number_of_touches -> Number of touches
hs_object_id -> Record ID
hs_object_source -> Record creation source
hs_object_source_detail_1 -> Record source detail 1
hs_object_source_detail_2 -> Record source detail 2
hs_object_source_detail_3 -> Record source detail 3
hs_object_source_id -> Record creation source ID
hs_object_source_label -> Record source
hs_object_source_user_id -> Record creation source user ID
hs_originating_channel_instance_id -> Originating channel account
hs_originating_email_engagement_id -> Originating email engagement id
hs_originating_generic_channel_id -> Originating channel type
hs_outbound_ticket -> Outbound ticket
hs_overall_visitor_messages_sentiment -> (Deprecated) Average ticket sentiment
hs_overall_visitor_messages_sentiment_score -> Average ticket sentiment score
hs_owning_teams -> Owning Teams
hs_pinned_engagement_id -> Pinned Engagement ID
hs_pipeline -> Pipeline
hs_pipeline_stage -> Ticket status
hs_predicted_cx_score -> CX Score
hs_predicted_cx_score_evidence -> CX Score explanation
hs_primary_company -> Primary Company
hs_primary_company_id -> Primary Company ID
hs_primary_company_name -> Primary Company Name
hs_primary_topic -> Primary topic
hs_read_only -> Read only object
hs_resolution -> Resolution
hs_retroactive_sla_update_at -> Retroactive SLA update at
hs_sales_email_last_replied -> Recent Sales Email Replied Date
hs_seen_by_agent_ids -> Users interaction
hs_shared_team_ids -> Shared teams
hs_shared_user_ids -> Shared users
hs_sla_operating_hours -> SLA operating hours
hs_sla_pause_status -> SLA Pause Status
hs_snoozed_by_user_ids -> Snoozed by
hs_snoozed_for_portal -> Portal-wide snooze
hs_source_object_id -> Source Object ID
hs_source_url -> Source url
hs_summarized_ticket_owner_type -> Summarized Ticket Owner Type
hs_tag_ids -> Ticket Tags
hs_thread_ids_to_restore -> Thread IDs To Restore
hs_ticket_category -> Category
hs_ticket_id -> Ticket ID
hs_ticket_language_ai_tag -> Language
hs_ticket_owner_type -> Ticket Owner Type
hs_ticket_priority -> Priority
hs_ticket_reopened_at -> Ticket reopen date
hs_time_to_close_in_operating_hours -> Time to close in SLA hours
hs_time_to_close_sla_at -> Time to Close SLA Due Date
hs_time_to_close_sla_status -> Time to Close SLA Ticket Status
hs_time_to_first_assign -> Time to first assign
hs_time_to_first_rep_assignment -> Time to first rep assignment
hs_time_to_first_response_in_operating_hours -> Time to first response in SLA hours
hs_time_to_first_response_sla_at -> Time to First Response SLA Due Date
hs_time_to_first_response_sla_status -> Time to First Response SLA Status
hs_time_to_next_response_sla_at -> Time to Next Response SLA Due Date
hs_time_to_next_response_sla_status -> Time to Next Response SLA Status
hs_unique_creation_key -> Unique creation key
hs_updated_by_user_id -> Updated by user ID
hs_user_ids_of_all_notification_followers -> User IDs of all notification followers
hs_user_ids_of_all_notification_unfollowers -> User IDs of all notification unfollowers
hs_user_ids_of_all_owners -> User IDs of all owners
hs_v2_cumulative_time_in_1018188674 -> Cumulative time in "Aprobacion Cliente | Sunrun (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1018249902 -> Cumulative time in "Referido a Ingeniería (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1018249903 -> Cumulative time in "Revisado Ingeniería (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1025503852 -> Cumulative time in "Revisado para Correcion  (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1031435540 -> Cumulative time in "Cover Sheet Pendiente (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1032111691 -> Cumulative time in "RMA (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1053695278 -> Cumulative time in "Save Harbor (* Pipeline Cobros)"
hs_v2_cumulative_time_in_1058736546 -> Cumulative time in "Nuevo (Milestone | Auditoria)"
hs_v2_cumulative_time_in_1058736549 -> Cumulative time in "Cerrados (Milestone | Auditoria)"
hs_v2_cumulative_time_in_1083492720 -> Cumulative time in "Instalación (M1 Activation) (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1083581608 -> Cumulative time in "Instalación (M1 Activation) (* Pipeline Milestone)"
hs_v2_cumulative_time_in_1088159648 -> Cumulative time in "Visitado | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1088164985 -> Cumulative time in "Low Fico Score (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_1088244992 -> Cumulative time in "Agendar | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1091291653 -> Cumulative time in "Esperando por Supervisor (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1091599168 -> Cumulative time in "Visitas Tecnicas (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1092210044 -> Cumulative time in "Visita Tecnica Realizada (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_1093095435 -> Cumulative time in "Escalado a Instalaciones (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1113633190 -> Cumulative time in "FSD No Facturable (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1123459752 -> Cumulative time in "Voltaje por Aprobacion (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1126725247 -> Cumulative time in "Agendado para corrección (* Pipeline Instalación)"
hs_v2_cumulative_time_in_1179036221 -> Cumulative time in "RMA Aprobado (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1181412865 -> Cumulative time in "RMA Nuevos (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1219240306 -> Cumulative time in "Nuevo (Soporte IT)"
hs_v2_cumulative_time_in_1219240309 -> Cumulative time in "Cerrados (Soporte IT)"
hs_v2_cumulative_time_in_1219240310 -> Cumulative time in "Aida (Soporte IT)"
hs_v2_cumulative_time_in_1219240738 -> Cumulative time in "José (Soporte IT)"
hs_v2_cumulative_time_in_1219240739 -> Cumulative time in "Julio (Soporte IT)"
hs_v2_cumulative_time_in_1236310282 -> Cumulative time in "FSD en Espera (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_1243095464 -> Cumulative time in "Crear Sunrun (Soporte IT)"
hs_v2_cumulative_time_in_134014525 -> Cumulative time in "Detenido (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134014526 -> Cumulative time in "NTP (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134020487 -> Cumulative time in "Cancelado (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_134027565 -> Cumulative time in "Validacion Takeoff / Planos (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134027566 -> Cumulative time in "Status con Cliente (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134027567 -> Cumulative time in "Instalación agendada (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134027568 -> Cumulative time in "Instalación (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134027571 -> Cumulative time in "Instalación (Finalizada) (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134027572 -> Cumulative time in "Cancelado (* Pipeline Instalación)"
hs_v2_cumulative_time_in_134032674 -> Cumulative time in "Listo para agendar (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134032675 -> Cumulative time in "Visita (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134032676 -> Cumulative time in "Diseño (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134032677 -> Cumulative time in "Revisión del Caso (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_134041631 -> Cumulative time in "Nuevo negocio cerrado (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_134041632 -> Cumulative time in "Revisión de Documentación (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_134041634 -> Cumulative time in "Aprobado (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_136703554 -> Cumulative time in "Primera comisión (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_136703555 -> Cumulative time in "Segunda comisión (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_136703556 -> Cumulative time in "Finalizado (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_136703557 -> Cumulative time in "Chargeback (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_138301819 -> Cumulative time in "En espera (* Pipeline Instalación)"
hs_v2_cumulative_time_in_138309889 -> Cumulative time in "En espera (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_147710512 -> Cumulative time in "Caso para Intervención (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_147710513 -> Cumulative time in "Cancelado (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_147751293 -> Cumulative time in "Caso para Intervención (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_147766428 -> Cumulative time in "Caso para Intervención (* Pipeline Instalación)"
hs_v2_cumulative_time_in_152726450 -> Cumulative time in "No Trabajado (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_152726451 -> Cumulative time in "Cancelado (* Pipeline Comisiones)"
hs_v2_cumulative_time_in_152919313 -> Cumulative time in "Detenida por Cliente (* Pipeline Instalación)"
hs_v2_cumulative_time_in_152919318 -> Cumulative time in "Detenida por Planet (* Pipeline Instalación)"
hs_v2_cumulative_time_in_165909623 -> Cumulative time in "Cambio de PK y/o # de Cliente (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_168008722 -> Cumulative time in "Avisos de Cambio (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_169997202 -> Cumulative time in "Aviso Procesado (* Pipeline Underwriting)"
hs_v2_cumulative_time_in_186507924 -> Cumulative time in "Vieques (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_191731373 -> Cumulative time in "Emergencias (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_191737251 -> Cumulative time in "2020 (PR | Casos 2020 - 2023)"
hs_v2_cumulative_time_in_191737252 -> Cumulative time in "2021 (PR | Casos 2020 - 2023)"
hs_v2_cumulative_time_in_191737253 -> Cumulative time in "2022 (PR | Casos 2020 - 2023)"
hs_v2_cumulative_time_in_191737254 -> Cumulative time in "2023 (PR | Casos 2020 - 2023)"
hs_v2_cumulative_time_in_195009694 -> Cumulative time in "En Proceso para Agendar (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_196426615 -> Cumulative time in "FSD por Someter (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_196426616 -> Cumulative time in "FSD Aprobados para Facturar (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_196426617 -> Cumulative time in "FSD Facturados (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_199023516 -> Cumulative time in "Costos Adicionales (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_199211069 -> Cumulative time in "FSD Esperando Aprobacion (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_199370301 -> Cumulative time in "Costos Aprobados (Adicionales) (* Pipeline Ingeniería)"
hs_v2_cumulative_time_in_200459375 -> Cumulative time in "Pendiente a Reagendar (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_211950939 -> Cumulative time in "Servicios Facturables (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_218856602 -> Cumulative time in "FSD Rechazados (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_231665319 -> Cumulative time in "Nuevo (PR | Consultores)"
hs_v2_cumulative_time_in_231665322 -> Cumulative time in "Creado (PR | Consultores)"
hs_v2_cumulative_time_in_235407171 -> Cumulative time in "En Espera (* Pipeline Milestone)"
hs_v2_cumulative_time_in_235407172 -> Cumulative time in "M1 Sometido (* Pipeline Milestone)"
hs_v2_cumulative_time_in_235407173 -> Cumulative time in "M1 Pendiente (* Pipeline Milestone)"
hs_v2_cumulative_time_in_235407174 -> Cumulative time in "M1 Denegado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_236632415 -> Cumulative time in "RMA Agendar (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_253494171 -> Cumulative time in "Pruebas de 5 Minutos (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_253568900 -> Cumulative time in "FSD Cancelados (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_261600095 -> Cumulative time in "Aprobado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_261673302 -> Cumulative time in "Cancelado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274828 -> Cumulative time in "M2 Sometido (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274829 -> Cumulative time in "M2 Pendiente (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274830 -> Cumulative time in "M2 Denegado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274831 -> Cumulative time in "M3 Sometido (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274832 -> Cumulative time in "M3 Pendiente (* Pipeline Milestone)"
hs_v2_cumulative_time_in_262274833 -> Cumulative time in "M3 Denegado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_264272401 -> Cumulative time in "Caso Nuevo M2 (* Pipeline Milestone)"
hs_v2_cumulative_time_in_264272402 -> Cumulative time in "Caso Nuevo M3 (* Pipeline Milestone)"
hs_v2_cumulative_time_in_78008665 -> Cumulative time in "Abierto (SAC | Servicio al Cliente)"
hs_v2_cumulative_time_in_78008666 -> Cumulative time in "Esperando al Cliente (SAC | Servicio al Cliente)"
hs_v2_cumulative_time_in_78008667 -> Cumulative time in "Esperando por nosotros (SAC | Servicio al Cliente)"
hs_v2_cumulative_time_in_78008668 -> Cumulative time in "Cerrados (SAC | Servicio al Cliente)"
hs_v2_cumulative_time_in_78802773 -> Cumulative time in "RMA Pendiente (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78802775 -> Cumulative time in "Cerrado (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78824121 -> Cumulative time in "Abierto (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78824192 -> Cumulative time in "Filtraciones (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78824193 -> Cumulative time in "Esperando por Cliente (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78824194 -> Cumulative time in "Agendado (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_78824225 -> Cumulative time in "Reagendado (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_939234425 -> Cumulative time in "M3 Listo para Someter (* Pipeline Milestone)"
hs_v2_cumulative_time_in_949635432 -> Cumulative time in "Riesgo ITC M1 (* Pipeline Milestone)"
hs_v2_cumulative_time_in_949635433 -> Cumulative time in "Riesgo ITC M2 (* Pipeline Milestone)"
hs_v2_cumulative_time_in_949635434 -> Cumulative time in "Riesgo ITC M3 (* Pipeline Milestone)"
hs_v2_cumulative_time_in_952458767 -> Cumulative time in "En Espera (* Pipeline Cobros)"
hs_v2_cumulative_time_in_952458770 -> Cumulative time in "Cancelados (* Pipeline Cobros)"
hs_v2_cumulative_time_in_952781376 -> Cumulative time in "Instalado (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953152099 -> Cumulative time in "PAID - Completado (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953152123 -> Cumulative time in "Cash | Costco | Coop (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953152124 -> Cumulative time in "Programa Federal (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953152125 -> Cumulative time in "Sunrun (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953241204 -> Cumulative time in "Deposit (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953241205 -> Cumulative time in "90% (* Pipeline Cobros)"
hs_v2_cumulative_time_in_953241206 -> Cumulative time in "M1 (* Pipeline Cobros)"
hs_v2_cumulative_time_in_958636181 -> Cumulative time in "Pruebas Agendadas con LUMA (ST | Servicios Técnicos)"
hs_v2_cumulative_time_in_958767384 -> Cumulative time in "Instalacion (Incompleta) (* Pipeline Instalación)"
hs_v2_cumulative_time_in_959775549 -> Cumulative time in "Caso Revisado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_959775550 -> Cumulative time in "Caso para Revision (* Pipeline Milestone)"
hs_v2_cumulative_time_in_960193688 -> Cumulative time in "Instalación (Finalizada) (* Pipeline Milestone)"
hs_v2_cumulative_time_in_983710527 -> Cumulative time in "Riesgo ITC Aprobado (* Pipeline Milestone)"
hs_v2_cumulative_time_in_990340191 -> Cumulative time in "Escalado Sunrun (* Pipeline Milestone)"
hs_v2_cumulative_time_in_990974471 -> Cumulative time in "Etapa 1 Revision de Caso (* Pipeline Instalación)"
hs_v2_cumulative_time_in_991306553 -> Cumulative time in "M1 Listo para Someter (* Pipeline Milestone)"
hs_v2_cumulative_time_in_991306554 -> Cumulative time in "M2 Listo para Someter (* Pipeline Milestone)"
hs_v2_cumulative_time_in_995581552 -> Cumulative time in "En Proceso de Cancelacion (* Pipeline Milestone)"
hs_v2_cumulative_time_in_998746970 -> Cumulative time in "Voltaje (* Pipeline Instalación)"
hs_v2_cumulative_time_in_998746971 -> Cumulative time in "Etapa 2 Revision de Caso (* Pipeline Instalación)"
hs_v2_date_entered_1018188674 -> Date entered "Aprobacion Cliente | Sunrun (* Pipeline Ingeniería)"
hs_v2_date_entered_1018249902 -> Date entered "Referido a Ingeniería (* Pipeline Instalación)"
hs_v2_date_entered_1018249903 -> Date entered "Revisado Ingeniería (* Pipeline Instalación)"
hs_v2_date_entered_1025503852 -> Date entered "Revisado para Correcion  (* Pipeline Instalación)"
hs_v2_date_entered_1031435540 -> Date entered "Cover Sheet Pendiente (* Pipeline Ingeniería)"
hs_v2_date_entered_1032111691 -> Date entered "RMA (* Pipeline Instalación)"
hs_v2_date_entered_1053695278 -> Date entered "Save Harbor (* Pipeline Cobros)"
hs_v2_date_entered_1058736546 -> Date entered "Nuevo (Milestone | Auditoria)"
hs_v2_date_entered_1058736549 -> Date entered "Cerrados (Milestone | Auditoria)"
hs_v2_date_entered_1083492720 -> Date entered "Instalación (M1 Activation) (* Pipeline Instalación)"
hs_v2_date_entered_1083581608 -> Date entered "Instalación (M1 Activation) (* Pipeline Milestone)"
hs_v2_date_entered_1088159648 -> Date entered "Visitado | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_date_entered_1088164985 -> Date entered "Low Fico Score (* Pipeline Underwriting)"
hs_v2_date_entered_1088244992 -> Date entered "Agendar | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_date_entered_1091291653 -> Date entered "Esperando por Supervisor (ST | Servicios Técnicos)"
hs_v2_date_entered_1091599168 -> Date entered "Visitas Tecnicas (* Pipeline Ingeniería)"
hs_v2_date_entered_1092210044 -> Date entered "Visita Tecnica Realizada (* Pipeline Ingeniería)"
hs_v2_date_entered_1093095435 -> Date entered "Escalado a Instalaciones (ST | Servicios Técnicos)"
hs_v2_date_entered_1113633190 -> Date entered "FSD No Facturable (ST | Servicios Técnicos)"
hs_v2_date_entered_1123459752 -> Date entered "Voltaje por Aprobacion (* Pipeline Instalación)"
hs_v2_date_entered_1126725247 -> Date entered "Agendado para corrección (* Pipeline Instalación)"
hs_v2_date_entered_1179036221 -> Date entered "RMA Aprobado (ST | Servicios Técnicos)"
hs_v2_date_entered_1181412865 -> Date entered "RMA Nuevos (ST | Servicios Técnicos)"
hs_v2_date_entered_1219240306 -> Date entered "Nuevo (Soporte IT)"
hs_v2_date_entered_1219240309 -> Date entered "Cerrados (Soporte IT)"
hs_v2_date_entered_1219240310 -> Date entered "Aida (Soporte IT)"
hs_v2_date_entered_1219240738 -> Date entered "José (Soporte IT)"
hs_v2_date_entered_1219240739 -> Date entered "Julio (Soporte IT)"
hs_v2_date_entered_1236310282 -> Date entered "FSD en Espera (ST | Servicios Técnicos)"
hs_v2_date_entered_1243095464 -> Date entered "Crear Sunrun (Soporte IT)"
hs_v2_date_entered_134014525 -> Date entered "Detenido (* Pipeline Ingeniería)"
hs_v2_date_entered_134014526 -> Date entered "NTP (* Pipeline Ingeniería)"
hs_v2_date_entered_134020487 -> Date entered "Cancelado (* Pipeline Underwriting)"
hs_v2_date_entered_134027565 -> Date entered "Validacion Takeoff / Planos (* Pipeline Instalación)"
hs_v2_date_entered_134027566 -> Date entered "Status con Cliente (* Pipeline Instalación)"
hs_v2_date_entered_134027567 -> Date entered "Instalación agendada (* Pipeline Instalación)"
hs_v2_date_entered_134027568 -> Date entered "Instalación (* Pipeline Instalación)"
hs_v2_date_entered_134027571 -> Date entered "Instalación (Finalizada) (* Pipeline Instalación)"
hs_v2_date_entered_134027572 -> Date entered "Cancelado (* Pipeline Instalación)"
hs_v2_date_entered_134032674 -> Date entered "Listo para agendar (* Pipeline Ingeniería)"
hs_v2_date_entered_134032675 -> Date entered "Visita (* Pipeline Ingeniería)"
hs_v2_date_entered_134032676 -> Date entered "Diseño (* Pipeline Ingeniería)"
hs_v2_date_entered_134032677 -> Date entered "Revisión del Caso (* Pipeline Ingeniería)"
hs_v2_date_entered_134041631 -> Date entered "Nuevo negocio cerrado (* Pipeline Underwriting)"
hs_v2_date_entered_134041632 -> Date entered "Revisión de Documentación (* Pipeline Underwriting)"
hs_v2_date_entered_134041634 -> Date entered "Aprobado (* Pipeline Underwriting)"
hs_v2_date_entered_136703554 -> Date entered "Primera comisión (* Pipeline Comisiones)"
hs_v2_date_entered_136703555 -> Date entered "Segunda comisión (* Pipeline Comisiones)"
hs_v2_date_entered_136703556 -> Date entered "Finalizado (* Pipeline Comisiones)"
hs_v2_date_entered_136703557 -> Date entered "Chargeback (* Pipeline Comisiones)"
hs_v2_date_entered_138301819 -> Date entered "En espera (* Pipeline Instalación)"
hs_v2_date_entered_138309889 -> Date entered "En espera (* Pipeline Ingeniería)"
hs_v2_date_entered_147710512 -> Date entered "Caso para Intervención (* Pipeline Ingeniería)"
hs_v2_date_entered_147710513 -> Date entered "Cancelado (* Pipeline Ingeniería)"
hs_v2_date_entered_147751293 -> Date entered "Caso para Intervención (* Pipeline Underwriting)"
hs_v2_date_entered_147766428 -> Date entered "Caso para Intervención (* Pipeline Instalación)"
hs_v2_date_entered_152726450 -> Date entered "No Trabajado (* Pipeline Comisiones)"
hs_v2_date_entered_152726451 -> Date entered "Cancelado (* Pipeline Comisiones)"
hs_v2_date_entered_152919313 -> Date entered "Detenida por Cliente (* Pipeline Instalación)"
hs_v2_date_entered_152919318 -> Date entered "Detenida por Planet (* Pipeline Instalación)"
hs_v2_date_entered_165909623 -> Date entered "Cambio de PK y/o # de Cliente (* Pipeline Ingeniería)"
hs_v2_date_entered_168008722 -> Date entered "Avisos de Cambio (* Pipeline Underwriting)"
hs_v2_date_entered_169997202 -> Date entered "Aviso Procesado (* Pipeline Underwriting)"
hs_v2_date_entered_186507924 -> Date entered "Vieques (ST | Servicios Técnicos)"
hs_v2_date_entered_191731373 -> Date entered "Emergencias (ST | Servicios Técnicos)"
hs_v2_date_entered_191737251 -> Date entered "2020 (PR | Casos 2020 - 2023)"
hs_v2_date_entered_191737252 -> Date entered "2021 (PR | Casos 2020 - 2023)"
hs_v2_date_entered_191737253 -> Date entered "2022 (PR | Casos 2020 - 2023)"
hs_v2_date_entered_191737254 -> Date entered "2023 (PR | Casos 2020 - 2023)"
hs_v2_date_entered_195009694 -> Date entered "En Proceso para Agendar (* Pipeline Ingeniería)"
hs_v2_date_entered_196426615 -> Date entered "FSD por Someter (ST | Servicios Técnicos)"
hs_v2_date_entered_196426616 -> Date entered "FSD Aprobados para Facturar (ST | Servicios Técnicos)"
hs_v2_date_entered_196426617 -> Date entered "FSD Facturados (ST | Servicios Técnicos)"
hs_v2_date_entered_199023516 -> Date entered "Costos Adicionales (* Pipeline Ingeniería)"
hs_v2_date_entered_199211069 -> Date entered "FSD Esperando Aprobacion (ST | Servicios Técnicos)"
hs_v2_date_entered_199370301 -> Date entered "Costos Aprobados (Adicionales) (* Pipeline Ingeniería)"
hs_v2_date_entered_200459375 -> Date entered "Pendiente a Reagendar (ST | Servicios Técnicos)"
hs_v2_date_entered_211950939 -> Date entered "Servicios Facturables (ST | Servicios Técnicos)"
hs_v2_date_entered_218856602 -> Date entered "FSD Rechazados (ST | Servicios Técnicos)"
hs_v2_date_entered_231665319 -> Date entered "Nuevo (PR | Consultores)"
hs_v2_date_entered_231665322 -> Date entered "Creado (PR | Consultores)"
hs_v2_date_entered_235407171 -> Date entered "En Espera (* Pipeline Milestone)"
hs_v2_date_entered_235407172 -> Date entered "M1 Sometido (* Pipeline Milestone)"
hs_v2_date_entered_235407173 -> Date entered "M1 Pendiente (* Pipeline Milestone)"
hs_v2_date_entered_235407174 -> Date entered "M1 Denegado (* Pipeline Milestone)"
hs_v2_date_entered_236632415 -> Date entered "RMA Agendar (ST | Servicios Técnicos)"
hs_v2_date_entered_253494171 -> Date entered "Pruebas de 5 Minutos (ST | Servicios Técnicos)"
hs_v2_date_entered_253568900 -> Date entered "FSD Cancelados (ST | Servicios Técnicos)"
hs_v2_date_entered_261600095 -> Date entered "Aprobado (* Pipeline Milestone)"
hs_v2_date_entered_261673302 -> Date entered "Cancelado (* Pipeline Milestone)"
hs_v2_date_entered_262274828 -> Date entered "M2 Sometido (* Pipeline Milestone)"
hs_v2_date_entered_262274829 -> Date entered "M2 Pendiente (* Pipeline Milestone)"
hs_v2_date_entered_262274830 -> Date entered "M2 Denegado (* Pipeline Milestone)"
hs_v2_date_entered_262274831 -> Date entered "M3 Sometido (* Pipeline Milestone)"
hs_v2_date_entered_262274832 -> Date entered "M3 Pendiente (* Pipeline Milestone)"
hs_v2_date_entered_262274833 -> Date entered "M3 Denegado (* Pipeline Milestone)"
hs_v2_date_entered_264272401 -> Date entered "Caso Nuevo M2 (* Pipeline Milestone)"
hs_v2_date_entered_264272402 -> Date entered "Caso Nuevo M3 (* Pipeline Milestone)"
hs_v2_date_entered_78008665 -> Date entered "Abierto (SAC | Servicio al Cliente)"
hs_v2_date_entered_78008666 -> Date entered "Esperando al Cliente (SAC | Servicio al Cliente)"
hs_v2_date_entered_78008667 -> Date entered "Esperando por nosotros (SAC | Servicio al Cliente)"
hs_v2_date_entered_78008668 -> Date entered "Cerrados (SAC | Servicio al Cliente)"
hs_v2_date_entered_78802773 -> Date entered "RMA Pendiente (ST | Servicios Técnicos)"
hs_v2_date_entered_78802775 -> Date entered "Cerrado (ST | Servicios Técnicos)"
hs_v2_date_entered_78824121 -> Date entered "Abierto (ST | Servicios Técnicos)"
hs_v2_date_entered_78824192 -> Date entered "Filtraciones (ST | Servicios Técnicos)"
hs_v2_date_entered_78824193 -> Date entered "Esperando por Cliente (ST | Servicios Técnicos)"
hs_v2_date_entered_78824194 -> Date entered "Agendado (ST | Servicios Técnicos)"
hs_v2_date_entered_78824225 -> Date entered "Reagendado (ST | Servicios Técnicos)"
hs_v2_date_entered_939234425 -> Date entered "M3 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_entered_949635432 -> Date entered "Riesgo ITC M1 (* Pipeline Milestone)"
hs_v2_date_entered_949635433 -> Date entered "Riesgo ITC M2 (* Pipeline Milestone)"
hs_v2_date_entered_949635434 -> Date entered "Riesgo ITC M3 (* Pipeline Milestone)"
hs_v2_date_entered_952458767 -> Date entered "En Espera (* Pipeline Cobros)"
hs_v2_date_entered_952458770 -> Date entered "Cancelados (* Pipeline Cobros)"
hs_v2_date_entered_952781376 -> Date entered "Instalado (* Pipeline Cobros)"
hs_v2_date_entered_953152099 -> Date entered "PAID - Completado (* Pipeline Cobros)"
hs_v2_date_entered_953152123 -> Date entered "Cash | Costco | Coop (* Pipeline Cobros)"
hs_v2_date_entered_953152124 -> Date entered "Programa Federal (* Pipeline Cobros)"
hs_v2_date_entered_953152125 -> Date entered "Sunrun (* Pipeline Cobros)"
hs_v2_date_entered_953241204 -> Date entered "Deposit (* Pipeline Cobros)"
hs_v2_date_entered_953241205 -> Date entered "90% (* Pipeline Cobros)"
hs_v2_date_entered_953241206 -> Date entered "M1 (* Pipeline Cobros)"
hs_v2_date_entered_958636181 -> Date entered "Pruebas Agendadas con LUMA (ST | Servicios Técnicos)"
hs_v2_date_entered_958767384 -> Date entered "Instalacion (Incompleta) (* Pipeline Instalación)"
hs_v2_date_entered_959775549 -> Date entered "Caso Revisado (* Pipeline Milestone)"
hs_v2_date_entered_959775550 -> Date entered "Caso para Revision (* Pipeline Milestone)"
hs_v2_date_entered_960193688 -> Date entered "Instalación (Finalizada) (* Pipeline Milestone)"
hs_v2_date_entered_983710527 -> Date entered "Riesgo ITC Aprobado (* Pipeline Milestone)"
hs_v2_date_entered_990340191 -> Date entered "Escalado Sunrun (* Pipeline Milestone)"
hs_v2_date_entered_990974471 -> Date entered "Etapa 1 Revision de Caso (* Pipeline Instalación)"
hs_v2_date_entered_991306553 -> Date entered "M1 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_entered_991306554 -> Date entered "M2 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_entered_995581552 -> Date entered "En Proceso de Cancelacion (* Pipeline Milestone)"
hs_v2_date_entered_998746970 -> Date entered "Voltaje (* Pipeline Instalación)"
hs_v2_date_entered_998746971 -> Date entered "Etapa 2 Revision de Caso (* Pipeline Instalación)"
hs_v2_date_entered_current_stage -> Date entered current stage
hs_v2_date_exited_1018188674 -> Date exited "Aprobacion Cliente | Sunrun (* Pipeline Ingeniería)"
hs_v2_date_exited_1018249902 -> Date exited "Referido a Ingeniería (* Pipeline Instalación)"
hs_v2_date_exited_1018249903 -> Date exited "Revisado Ingeniería (* Pipeline Instalación)"
hs_v2_date_exited_1025503852 -> Date exited "Revisado para Correcion  (* Pipeline Instalación)"
hs_v2_date_exited_1031435540 -> Date exited "Cover Sheet Pendiente (* Pipeline Ingeniería)"
hs_v2_date_exited_1032111691 -> Date exited "RMA (* Pipeline Instalación)"
hs_v2_date_exited_1053695278 -> Date exited "Save Harbor (* Pipeline Cobros)"
hs_v2_date_exited_1058736546 -> Date exited "Nuevo (Milestone | Auditoria)"
hs_v2_date_exited_1058736549 -> Date exited "Cerrados (Milestone | Auditoria)"
hs_v2_date_exited_1083492720 -> Date exited "Instalación (M1 Activation) (* Pipeline Instalación)"
hs_v2_date_exited_1083581608 -> Date exited "Instalación (M1 Activation) (* Pipeline Milestone)"
hs_v2_date_exited_1088159648 -> Date exited "Visitado | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_date_exited_1088164985 -> Date exited "Low Fico Score (* Pipeline Underwriting)"
hs_v2_date_exited_1088244992 -> Date exited "Agendar | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_date_exited_1091291653 -> Date exited "Esperando por Supervisor (ST | Servicios Técnicos)"
hs_v2_date_exited_1091599168 -> Date exited "Visitas Tecnicas (* Pipeline Ingeniería)"
hs_v2_date_exited_1092210044 -> Date exited "Visita Tecnica Realizada (* Pipeline Ingeniería)"
hs_v2_date_exited_1093095435 -> Date exited "Escalado a Instalaciones (ST | Servicios Técnicos)"
hs_v2_date_exited_1113633190 -> Date exited "FSD No Facturable (ST | Servicios Técnicos)"
hs_v2_date_exited_1123459752 -> Date exited "Voltaje por Aprobacion (* Pipeline Instalación)"
hs_v2_date_exited_1126725247 -> Date exited "Agendado para corrección (* Pipeline Instalación)"
hs_v2_date_exited_1179036221 -> Date exited "RMA Aprobado (ST | Servicios Técnicos)"
hs_v2_date_exited_1181412865 -> Date exited "RMA Nuevos (ST | Servicios Técnicos)"
hs_v2_date_exited_1219240306 -> Date exited "Nuevo (Soporte IT)"
hs_v2_date_exited_1219240309 -> Date exited "Cerrados (Soporte IT)"
hs_v2_date_exited_1219240310 -> Date exited "Aida (Soporte IT)"
hs_v2_date_exited_1219240738 -> Date exited "José (Soporte IT)"
hs_v2_date_exited_1219240739 -> Date exited "Julio (Soporte IT)"
hs_v2_date_exited_1236310282 -> Date exited "FSD en Espera (ST | Servicios Técnicos)"
hs_v2_date_exited_1243095464 -> Date exited "Crear Sunrun (Soporte IT)"
hs_v2_date_exited_134014525 -> Date exited "Detenido (* Pipeline Ingeniería)"
hs_v2_date_exited_134014526 -> Date exited "NTP (* Pipeline Ingeniería)"
hs_v2_date_exited_134020487 -> Date exited "Cancelado (* Pipeline Underwriting)"
hs_v2_date_exited_134027565 -> Date exited "Validacion Takeoff / Planos (* Pipeline Instalación)"
hs_v2_date_exited_134027566 -> Date exited "Status con Cliente (* Pipeline Instalación)"
hs_v2_date_exited_134027567 -> Date exited "Instalación agendada (* Pipeline Instalación)"
hs_v2_date_exited_134027568 -> Date exited "Instalación (* Pipeline Instalación)"
hs_v2_date_exited_134027571 -> Date exited "Instalación (Finalizada) (* Pipeline Instalación)"
hs_v2_date_exited_134027572 -> Date exited "Cancelado (* Pipeline Instalación)"
hs_v2_date_exited_134032674 -> Date exited "Listo para agendar (* Pipeline Ingeniería)"
hs_v2_date_exited_134032675 -> Date exited "Visita (* Pipeline Ingeniería)"
hs_v2_date_exited_134032676 -> Date exited "Diseño (* Pipeline Ingeniería)"
hs_v2_date_exited_134032677 -> Date exited "Revisión del Caso (* Pipeline Ingeniería)"
hs_v2_date_exited_134041631 -> Date exited "Nuevo negocio cerrado (* Pipeline Underwriting)"
hs_v2_date_exited_134041632 -> Date exited "Revisión de Documentación (* Pipeline Underwriting)"
hs_v2_date_exited_134041634 -> Date exited "Aprobado (* Pipeline Underwriting)"
hs_v2_date_exited_136703554 -> Date exited "Primera comisión (* Pipeline Comisiones)"
hs_v2_date_exited_136703555 -> Date exited "Segunda comisión (* Pipeline Comisiones)"
hs_v2_date_exited_136703556 -> Date exited "Finalizado (* Pipeline Comisiones)"
hs_v2_date_exited_136703557 -> Date exited "Chargeback (* Pipeline Comisiones)"
hs_v2_date_exited_138301819 -> Date exited "En espera (* Pipeline Instalación)"
hs_v2_date_exited_138309889 -> Date exited "En espera (* Pipeline Ingeniería)"
hs_v2_date_exited_147710512 -> Date exited "Caso para Intervención (* Pipeline Ingeniería)"
hs_v2_date_exited_147710513 -> Date exited "Cancelado (* Pipeline Ingeniería)"
hs_v2_date_exited_147751293 -> Date exited "Caso para Intervención (* Pipeline Underwriting)"
hs_v2_date_exited_147766428 -> Date exited "Caso para Intervención (* Pipeline Instalación)"
hs_v2_date_exited_152726450 -> Date exited "No Trabajado (* Pipeline Comisiones)"
hs_v2_date_exited_152726451 -> Date exited "Cancelado (* Pipeline Comisiones)"
hs_v2_date_exited_152919313 -> Date exited "Detenida por Cliente (* Pipeline Instalación)"
hs_v2_date_exited_152919318 -> Date exited "Detenida por Planet (* Pipeline Instalación)"
hs_v2_date_exited_165909623 -> Date exited "Cambio de PK y/o # de Cliente (* Pipeline Ingeniería)"
hs_v2_date_exited_168008722 -> Date exited "Avisos de Cambio (* Pipeline Underwriting)"
hs_v2_date_exited_169997202 -> Date exited "Aviso Procesado (* Pipeline Underwriting)"
hs_v2_date_exited_186507924 -> Date exited "Vieques (ST | Servicios Técnicos)"
hs_v2_date_exited_191731373 -> Date exited "Emergencias (ST | Servicios Técnicos)"
hs_v2_date_exited_191737251 -> Date exited "2020 (PR | Casos 2020 - 2023)"
hs_v2_date_exited_191737252 -> Date exited "2021 (PR | Casos 2020 - 2023)"
hs_v2_date_exited_191737253 -> Date exited "2022 (PR | Casos 2020 - 2023)"
hs_v2_date_exited_191737254 -> Date exited "2023 (PR | Casos 2020 - 2023)"
hs_v2_date_exited_195009694 -> Date exited "En Proceso para Agendar (* Pipeline Ingeniería)"
hs_v2_date_exited_196426615 -> Date exited "FSD por Someter (ST | Servicios Técnicos)"
hs_v2_date_exited_196426616 -> Date exited "FSD Aprobados para Facturar (ST | Servicios Técnicos)"
hs_v2_date_exited_196426617 -> Date exited "FSD Facturados (ST | Servicios Técnicos)"
hs_v2_date_exited_199023516 -> Date exited "Costos Adicionales (* Pipeline Ingeniería)"
hs_v2_date_exited_199211069 -> Date exited "FSD Esperando Aprobacion (ST | Servicios Técnicos)"
hs_v2_date_exited_199370301 -> Date exited "Costos Aprobados (Adicionales) (* Pipeline Ingeniería)"
hs_v2_date_exited_200459375 -> Date exited "Pendiente a Reagendar (ST | Servicios Técnicos)"
hs_v2_date_exited_211950939 -> Date exited "Servicios Facturables (ST | Servicios Técnicos)"
hs_v2_date_exited_218856602 -> Date exited "FSD Rechazados (ST | Servicios Técnicos)"
hs_v2_date_exited_231665319 -> Date exited "Nuevo (PR | Consultores)"
hs_v2_date_exited_231665322 -> Date exited "Creado (PR | Consultores)"
hs_v2_date_exited_235407171 -> Date exited "En Espera (* Pipeline Milestone)"
hs_v2_date_exited_235407172 -> Date exited "M1 Sometido (* Pipeline Milestone)"
hs_v2_date_exited_235407173 -> Date exited "M1 Pendiente (* Pipeline Milestone)"
hs_v2_date_exited_235407174 -> Date exited "M1 Denegado (* Pipeline Milestone)"
hs_v2_date_exited_236632415 -> Date exited "RMA Agendar (ST | Servicios Técnicos)"
hs_v2_date_exited_253494171 -> Date exited "Pruebas de 5 Minutos (ST | Servicios Técnicos)"
hs_v2_date_exited_253568900 -> Date exited "FSD Cancelados (ST | Servicios Técnicos)"
hs_v2_date_exited_261600095 -> Date exited "Aprobado (* Pipeline Milestone)"
hs_v2_date_exited_261673302 -> Date exited "Cancelado (* Pipeline Milestone)"
hs_v2_date_exited_262274828 -> Date exited "M2 Sometido (* Pipeline Milestone)"
hs_v2_date_exited_262274829 -> Date exited "M2 Pendiente (* Pipeline Milestone)"
hs_v2_date_exited_262274830 -> Date exited "M2 Denegado (* Pipeline Milestone)"
hs_v2_date_exited_262274831 -> Date exited "M3 Sometido (* Pipeline Milestone)"
hs_v2_date_exited_262274832 -> Date exited "M3 Pendiente (* Pipeline Milestone)"
hs_v2_date_exited_262274833 -> Date exited "M3 Denegado (* Pipeline Milestone)"
hs_v2_date_exited_264272401 -> Date exited "Caso Nuevo M2 (* Pipeline Milestone)"
hs_v2_date_exited_264272402 -> Date exited "Caso Nuevo M3 (* Pipeline Milestone)"
hs_v2_date_exited_78008665 -> Date exited "Abierto (SAC | Servicio al Cliente)"
hs_v2_date_exited_78008666 -> Date exited "Esperando al Cliente (SAC | Servicio al Cliente)"
hs_v2_date_exited_78008667 -> Date exited "Esperando por nosotros (SAC | Servicio al Cliente)"
hs_v2_date_exited_78008668 -> Date exited "Cerrados (SAC | Servicio al Cliente)"
hs_v2_date_exited_78802773 -> Date exited "RMA Pendiente (ST | Servicios Técnicos)"
hs_v2_date_exited_78802775 -> Date exited "Cerrado (ST | Servicios Técnicos)"
hs_v2_date_exited_78824121 -> Date exited "Abierto (ST | Servicios Técnicos)"
hs_v2_date_exited_78824192 -> Date exited "Filtraciones (ST | Servicios Técnicos)"
hs_v2_date_exited_78824193 -> Date exited "Esperando por Cliente (ST | Servicios Técnicos)"
hs_v2_date_exited_78824194 -> Date exited "Agendado (ST | Servicios Técnicos)"
hs_v2_date_exited_78824225 -> Date exited "Reagendado (ST | Servicios Técnicos)"
hs_v2_date_exited_939234425 -> Date exited "M3 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_exited_949635432 -> Date exited "Riesgo ITC M1 (* Pipeline Milestone)"
hs_v2_date_exited_949635433 -> Date exited "Riesgo ITC M2 (* Pipeline Milestone)"
hs_v2_date_exited_949635434 -> Date exited "Riesgo ITC M3 (* Pipeline Milestone)"
hs_v2_date_exited_952458767 -> Date exited "En Espera (* Pipeline Cobros)"
hs_v2_date_exited_952458770 -> Date exited "Cancelados (* Pipeline Cobros)"
hs_v2_date_exited_952781376 -> Date exited "Instalado (* Pipeline Cobros)"
hs_v2_date_exited_953152099 -> Date exited "PAID - Completado (* Pipeline Cobros)"
hs_v2_date_exited_953152123 -> Date exited "Cash | Costco | Coop (* Pipeline Cobros)"
hs_v2_date_exited_953152124 -> Date exited "Programa Federal (* Pipeline Cobros)"
hs_v2_date_exited_953152125 -> Date exited "Sunrun (* Pipeline Cobros)"
hs_v2_date_exited_953241204 -> Date exited "Deposit (* Pipeline Cobros)"
hs_v2_date_exited_953241205 -> Date exited "90% (* Pipeline Cobros)"
hs_v2_date_exited_953241206 -> Date exited "M1 (* Pipeline Cobros)"
hs_v2_date_exited_958636181 -> Date exited "Pruebas Agendadas con LUMA (ST | Servicios Técnicos)"
hs_v2_date_exited_958767384 -> Date exited "Instalacion (Incompleta) (* Pipeline Instalación)"
hs_v2_date_exited_959775549 -> Date exited "Caso Revisado (* Pipeline Milestone)"
hs_v2_date_exited_959775550 -> Date exited "Caso para Revision (* Pipeline Milestone)"
hs_v2_date_exited_960193688 -> Date exited "Instalación (Finalizada) (* Pipeline Milestone)"
hs_v2_date_exited_983710527 -> Date exited "Riesgo ITC Aprobado (* Pipeline Milestone)"
hs_v2_date_exited_990340191 -> Date exited "Escalado Sunrun (* Pipeline Milestone)"
hs_v2_date_exited_990974471 -> Date exited "Etapa 1 Revision de Caso (* Pipeline Instalación)"
hs_v2_date_exited_991306553 -> Date exited "M1 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_exited_991306554 -> Date exited "M2 Listo para Someter (* Pipeline Milestone)"
hs_v2_date_exited_995581552 -> Date exited "En Proceso de Cancelacion (* Pipeline Milestone)"
hs_v2_date_exited_998746970 -> Date exited "Voltaje (* Pipeline Instalación)"
hs_v2_date_exited_998746971 -> Date exited "Etapa 2 Revision de Caso (* Pipeline Instalación)"
hs_v2_latest_time_in_1018188674 -> Latest time in "Aprobacion Cliente | Sunrun (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1018249902 -> Latest time in "Referido a Ingeniería (* Pipeline Instalación)"
hs_v2_latest_time_in_1018249903 -> Latest time in "Revisado Ingeniería (* Pipeline Instalación)"
hs_v2_latest_time_in_1025503852 -> Latest time in "Revisado para Correcion  (* Pipeline Instalación)"
hs_v2_latest_time_in_1031435540 -> Latest time in "Cover Sheet Pendiente (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1032111691 -> Latest time in "RMA (* Pipeline Instalación)"
hs_v2_latest_time_in_1053695278 -> Latest time in "Save Harbor (* Pipeline Cobros)"
hs_v2_latest_time_in_1058736546 -> Latest time in "Nuevo (Milestone | Auditoria)"
hs_v2_latest_time_in_1058736549 -> Latest time in "Cerrados (Milestone | Auditoria)"
hs_v2_latest_time_in_1083492720 -> Latest time in "Instalación (M1 Activation) (* Pipeline Instalación)"
hs_v2_latest_time_in_1083581608 -> Latest time in "Instalación (M1 Activation) (* Pipeline Milestone)"
hs_v2_latest_time_in_1088159648 -> Latest time in "Visitado | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1088164985 -> Latest time in "Low Fico Score (* Pipeline Underwriting)"
hs_v2_latest_time_in_1088244992 -> Latest time in "Agendar | Low Fico Score (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1091291653 -> Latest time in "Esperando por Supervisor (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1091599168 -> Latest time in "Visitas Tecnicas (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1092210044 -> Latest time in "Visita Tecnica Realizada (* Pipeline Ingeniería)"
hs_v2_latest_time_in_1093095435 -> Latest time in "Escalado a Instalaciones (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1113633190 -> Latest time in "FSD No Facturable (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1123459752 -> Latest time in "Voltaje por Aprobacion (* Pipeline Instalación)"
hs_v2_latest_time_in_1126725247 -> Latest time in "Agendado para corrección (* Pipeline Instalación)"
hs_v2_latest_time_in_1179036221 -> Latest time in "RMA Aprobado (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1181412865 -> Latest time in "RMA Nuevos (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1219240306 -> Latest time in "Nuevo (Soporte IT)"
hs_v2_latest_time_in_1219240309 -> Latest time in "Cerrados (Soporte IT)"
hs_v2_latest_time_in_1219240310 -> Latest time in "Aida (Soporte IT)"
hs_v2_latest_time_in_1219240738 -> Latest time in "José (Soporte IT)"
hs_v2_latest_time_in_1219240739 -> Latest time in "Julio (Soporte IT)"
hs_v2_latest_time_in_1236310282 -> Latest time in "FSD en Espera (ST | Servicios Técnicos)"
hs_v2_latest_time_in_1243095464 -> Latest time in "Crear Sunrun (Soporte IT)"
hs_v2_latest_time_in_134014525 -> Latest time in "Detenido (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134014526 -> Latest time in "NTP (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134020487 -> Latest time in "Cancelado (* Pipeline Underwriting)"
hs_v2_latest_time_in_134027565 -> Latest time in "Validacion Takeoff / Planos (* Pipeline Instalación)"
hs_v2_latest_time_in_134027566 -> Latest time in "Status con Cliente (* Pipeline Instalación)"
hs_v2_latest_time_in_134027567 -> Latest time in "Instalación agendada (* Pipeline Instalación)"
hs_v2_latest_time_in_134027568 -> Latest time in "Instalación (* Pipeline Instalación)"
hs_v2_latest_time_in_134027571 -> Latest time in "Instalación (Finalizada) (* Pipeline Instalación)"
hs_v2_latest_time_in_134027572 -> Latest time in "Cancelado (* Pipeline Instalación)"
hs_v2_latest_time_in_134032674 -> Latest time in "Listo para agendar (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134032675 -> Latest time in "Visita (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134032676 -> Latest time in "Diseño (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134032677 -> Latest time in "Revisión del Caso (* Pipeline Ingeniería)"
hs_v2_latest_time_in_134041631 -> Latest time in "Nuevo negocio cerrado (* Pipeline Underwriting)"
hs_v2_latest_time_in_134041632 -> Latest time in "Revisión de Documentación (* Pipeline Underwriting)"
hs_v2_latest_time_in_134041634 -> Latest time in "Aprobado (* Pipeline Underwriting)"
hs_v2_latest_time_in_136703554 -> Latest time in "Primera comisión (* Pipeline Comisiones)"
hs_v2_latest_time_in_136703555 -> Latest time in "Segunda comisión (* Pipeline Comisiones)"
hs_v2_latest_time_in_136703556 -> Latest time in "Finalizado (* Pipeline Comisiones)"
hs_v2_latest_time_in_136703557 -> Latest time in "Chargeback (* Pipeline Comisiones)"
hs_v2_latest_time_in_138301819 -> Latest time in "En espera (* Pipeline Instalación)"
hs_v2_latest_time_in_138309889 -> Latest time in "En espera (* Pipeline Ingeniería)"
hs_v2_latest_time_in_147710512 -> Latest time in "Caso para Intervención (* Pipeline Ingeniería)"
hs_v2_latest_time_in_147710513 -> Latest time in "Cancelado (* Pipeline Ingeniería)"
hs_v2_latest_time_in_147751293 -> Latest time in "Caso para Intervención (* Pipeline Underwriting)"
hs_v2_latest_time_in_147766428 -> Latest time in "Caso para Intervención (* Pipeline Instalación)"
hs_v2_latest_time_in_152726450 -> Latest time in "No Trabajado (* Pipeline Comisiones)"
hs_v2_latest_time_in_152726451 -> Latest time in "Cancelado (* Pipeline Comisiones)"
hs_v2_latest_time_in_152919313 -> Latest time in "Detenida por Cliente (* Pipeline Instalación)"
hs_v2_latest_time_in_152919318 -> Latest time in "Detenida por Planet (* Pipeline Instalación)"
hs_v2_latest_time_in_165909623 -> Latest time in "Cambio de PK y/o # de Cliente (* Pipeline Ingeniería)"
hs_v2_latest_time_in_168008722 -> Latest time in "Avisos de Cambio (* Pipeline Underwriting)"
hs_v2_latest_time_in_169997202 -> Latest time in "Aviso Procesado (* Pipeline Underwriting)"
hs_v2_latest_time_in_186507924 -> Latest time in "Vieques (ST | Servicios Técnicos)"
hs_v2_latest_time_in_191731373 -> Latest time in "Emergencias (ST | Servicios Técnicos)"
hs_v2_latest_time_in_191737251 -> Latest time in "2020 (PR | Casos 2020 - 2023)"
hs_v2_latest_time_in_191737252 -> Latest time in "2021 (PR | Casos 2020 - 2023)"
hs_v2_latest_time_in_191737253 -> Latest time in "2022 (PR | Casos 2020 - 2023)"
hs_v2_latest_time_in_191737254 -> Latest time in "2023 (PR | Casos 2020 - 2023)"
hs_v2_latest_time_in_195009694 -> Latest time in "En Proceso para Agendar (* Pipeline Ingeniería)"
hs_v2_latest_time_in_196426615 -> Latest time in "FSD por Someter (ST | Servicios Técnicos)"
hs_v2_latest_time_in_196426616 -> Latest time in "FSD Aprobados para Facturar (ST | Servicios Técnicos)"
hs_v2_latest_time_in_196426617 -> Latest time in "FSD Facturados (ST | Servicios Técnicos)"
hs_v2_latest_time_in_199023516 -> Latest time in "Costos Adicionales (* Pipeline Ingeniería)"
hs_v2_latest_time_in_199211069 -> Latest time in "FSD Esperando Aprobacion (ST | Servicios Técnicos)"
hs_v2_latest_time_in_199370301 -> Latest time in "Costos Aprobados (Adicionales) (* Pipeline Ingeniería)"
hs_v2_latest_time_in_200459375 -> Latest time in "Pendiente a Reagendar (ST | Servicios Técnicos)"
hs_v2_latest_time_in_211950939 -> Latest time in "Servicios Facturables (ST | Servicios Técnicos)"
hs_v2_latest_time_in_218856602 -> Latest time in "FSD Rechazados (ST | Servicios Técnicos)"
hs_v2_latest_time_in_231665319 -> Latest time in "Nuevo (PR | Consultores)"
hs_v2_latest_time_in_231665322 -> Latest time in "Creado (PR | Consultores)"
hs_v2_latest_time_in_235407171 -> Latest time in "En Espera (* Pipeline Milestone)"
hs_v2_latest_time_in_235407172 -> Latest time in "M1 Sometido (* Pipeline Milestone)"
hs_v2_latest_time_in_235407173 -> Latest time in "M1 Pendiente (* Pipeline Milestone)"
hs_v2_latest_time_in_235407174 -> Latest time in "M1 Denegado (* Pipeline Milestone)"
hs_v2_latest_time_in_236632415 -> Latest time in "RMA Agendar (ST | Servicios Técnicos)"
hs_v2_latest_time_in_253494171 -> Latest time in "Pruebas de 5 Minutos (ST | Servicios Técnicos)"
hs_v2_latest_time_in_253568900 -> Latest time in "FSD Cancelados (ST | Servicios Técnicos)"
hs_v2_latest_time_in_261600095 -> Latest time in "Aprobado (* Pipeline Milestone)"
hs_v2_latest_time_in_261673302 -> Latest time in "Cancelado (* Pipeline Milestone)"
hs_v2_latest_time_in_262274828 -> Latest time in "M2 Sometido (* Pipeline Milestone)"
hs_v2_latest_time_in_262274829 -> Latest time in "M2 Pendiente (* Pipeline Milestone)"
hs_v2_latest_time_in_262274830 -> Latest time in "M2 Denegado (* Pipeline Milestone)"
hs_v2_latest_time_in_262274831 -> Latest time in "M3 Sometido (* Pipeline Milestone)"
hs_v2_latest_time_in_262274832 -> Latest time in "M3 Pendiente (* Pipeline Milestone)"
hs_v2_latest_time_in_262274833 -> Latest time in "M3 Denegado (* Pipeline Milestone)"
hs_v2_latest_time_in_264272401 -> Latest time in "Caso Nuevo M2 (* Pipeline Milestone)"
hs_v2_latest_time_in_264272402 -> Latest time in "Caso Nuevo M3 (* Pipeline Milestone)"
hs_v2_latest_time_in_78008665 -> Latest time in "Abierto (SAC | Servicio al Cliente)"
hs_v2_latest_time_in_78008666 -> Latest time in "Esperando al Cliente (SAC | Servicio al Cliente)"
hs_v2_latest_time_in_78008667 -> Latest time in "Esperando por nosotros (SAC | Servicio al Cliente)"
hs_v2_latest_time_in_78008668 -> Latest time in "Cerrados (SAC | Servicio al Cliente)"
hs_v2_latest_time_in_78802773 -> Latest time in "RMA Pendiente (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78802775 -> Latest time in "Cerrado (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78824121 -> Latest time in "Abierto (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78824192 -> Latest time in "Filtraciones (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78824193 -> Latest time in "Esperando por Cliente (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78824194 -> Latest time in "Agendado (ST | Servicios Técnicos)"
hs_v2_latest_time_in_78824225 -> Latest time in "Reagendado (ST | Servicios Técnicos)"
hs_v2_latest_time_in_939234425 -> Latest time in "M3 Listo para Someter (* Pipeline Milestone)"
hs_v2_latest_time_in_949635432 -> Latest time in "Riesgo ITC M1 (* Pipeline Milestone)"
hs_v2_latest_time_in_949635433 -> Latest time in "Riesgo ITC M2 (* Pipeline Milestone)"
hs_v2_latest_time_in_949635434 -> Latest time in "Riesgo ITC M3 (* Pipeline Milestone)"
hs_v2_latest_time_in_952458767 -> Latest time in "En Espera (* Pipeline Cobros)"
hs_v2_latest_time_in_952458770 -> Latest time in "Cancelados (* Pipeline Cobros)"
hs_v2_latest_time_in_952781376 -> Latest time in "Instalado (* Pipeline Cobros)"
hs_v2_latest_time_in_953152099 -> Latest time in "PAID - Completado (* Pipeline Cobros)"
hs_v2_latest_time_in_953152123 -> Latest time in "Cash | Costco | Coop (* Pipeline Cobros)"
hs_v2_latest_time_in_953152124 -> Latest time in "Programa Federal (* Pipeline Cobros)"
hs_v2_latest_time_in_953152125 -> Latest time in "Sunrun (* Pipeline Cobros)"
hs_v2_latest_time_in_953241204 -> Latest time in "Deposit (* Pipeline Cobros)"
hs_v2_latest_time_in_953241205 -> Latest time in "90% (* Pipeline Cobros)"
hs_v2_latest_time_in_953241206 -> Latest time in "M1 (* Pipeline Cobros)"
hs_v2_latest_time_in_958636181 -> Latest time in "Pruebas Agendadas con LUMA (ST | Servicios Técnicos)"
hs_v2_latest_time_in_958767384 -> Latest time in "Instalacion (Incompleta) (* Pipeline Instalación)"
hs_v2_latest_time_in_959775549 -> Latest time in "Caso Revisado (* Pipeline Milestone)"
hs_v2_latest_time_in_959775550 -> Latest time in "Caso para Revision (* Pipeline Milestone)"
hs_v2_latest_time_in_960193688 -> Latest time in "Instalación (Finalizada) (* Pipeline Milestone)"
hs_v2_latest_time_in_983710527 -> Latest time in "Riesgo ITC Aprobado (* Pipeline Milestone)"
hs_v2_latest_time_in_990340191 -> Latest time in "Escalado Sunrun (* Pipeline Milestone)"
hs_v2_latest_time_in_990974471 -> Latest time in "Etapa 1 Revision de Caso (* Pipeline Instalación)"
hs_v2_latest_time_in_991306553 -> Latest time in "M1 Listo para Someter (* Pipeline Milestone)"
hs_v2_latest_time_in_991306554 -> Latest time in "M2 Listo para Someter (* Pipeline Milestone)"
hs_v2_latest_time_in_995581552 -> Latest time in "En Proceso de Cancelacion (* Pipeline Milestone)"
hs_v2_latest_time_in_998746970 -> Latest time in "Voltaje (* Pipeline Instalación)"
hs_v2_latest_time_in_998746971 -> Latest time in "Etapa 2 Revision de Caso (* Pipeline Instalación)"
hs_v2_time_in_current_stage -> Time in current stage
hs_waitlist_routing_targets -> Waitlist routing targets
hs_waitlist_sort_value -> Waitlist sort value
hs_was_imported -> Performed in an import
hubspot_owner_assigneddate -> Owner assigned date
hubspot_owner_id -> Ticket owner
hubspot_team_id -> HubSpot team
id_del_caso -> ID del caso
id_del_negocio_asociado -> ID del Negocio Asociado
id_goformz__servicios_tecnicos_ -> ID GoFormz (Servicios Tecnicos)
id_localidad_luma -> ID Localidad Luma
if_____serie_bateria -> IF | # Serie Bateria
if_____serie_micros -> IF | # Serie Micros
if_____serie_paneles -> IF | # Serie Paneles
if___certificacion_electrica -> IF | Certificación Electrica
if___contrato_de_vivienda -> IF | Contrato de Vivienda
if___documento_de_plomo -> IF | Documento de Plomo
if___documents_status -> IF | Documents Status
if___fotos_bateria -> IF | Fotos Bateria
if___fotos_micros -> IF | Fotos Micros
if___fotos_paneles -> IF | Fotos Paneles
if___pago_luma__100 -> IF | Pago Luma $100
if___ronda_de_incentivo -> IF | Ronda de Incentivo
if___sometido_a_vivenda -> IF | Sometido a Vivenda
if___status___incentivo_federal -> IF | Status - Incentivo Federal
if___trace_number -> IF | Trace Number
if___venta_total -> IF | Venta Total
informacion_del_cliente -> Información del cliente
ingeniero_de_instalacion -> Ingeniero de instalación
ingeniero_electrico -> Ingeniero eléctrico
instalacion__m1_activation___tickets_ -> Instalación (M1 Activation) (Tickets)
instalacion_finalizada___revision -> Fecha de Instalacion Finalizada para Revision (Tickets)
installation_commissioning -> ⍟ Installation Commissioning
installation_report_4_photos -> ⍟ Installation Report 4 Photos
installation_status -> ⍟ Installation Status
installed -> ⍟ Installed
intentos_de_llamada_cliente -> Intentos de Llamada Cliente
internet_disponible -> Internet Disponible
interventor_asignado__interventor_ -> Interventor Asignado (Interventor)
inversor_es__a_instalar__tickets_ -> Inversor(es) a Instalar (Tickets)
inversor_es__qty_a_instalar__tickets_ -> Inversor(es) QTY a Instalar (Tickets)
investor -> ⍟ Inverters
kilos_d_c_a_instalar__tickets_ -> kW a Instalar (Tickets)
l1___l2 -> L1 + L2
last_engagement_date -> Date of last engagement
last_reply_date -> Last customer reply date
link_de_compra -> Link de Compra
link_schedule -> Link Schedule
lista_de_control_de_underwriting -> Check List Underwriting
loan_or_lease_sign_off_date -> ⍟ Loan Or Lease Sign Off Date
low_fico_fee___confirmacion -> Low Fico Fee # Confirmacion
low_fico_score_status -> Low Fico Fee Status (Tickets)
luma___fecha_de_querella -> LUMA | Fecha de Querella
luma___num_de_querella -> LUMA | Num de Querella
m1_check_list -> M1 Check-List
m1_sometido -> M1 sometido
m1_verificacion -> M1 verification
m2___m3__millestone_ -> M2 & M3 (Milestone)
m2_sometido -> M2 sometido
manufacturero_para_servicios_tecnicos -> Manufacturero (Servicios Tecnicos)
marcado_revisian -> Marcado Revision
master -> Master
mayor_a_25ac -> Mayor a 25AC
meca___case_age_in_days -> MECA - Case Age in Days
meca___description -> MECA - Description
meca___subject -> MECA - Subject
medio_de_atencion__sac_ -> Medio de atención (SAC)
medio_de_atencion__servicios_tecnicos_ -> Medio de atención (Servicios Tecnicos)
mes -> ⍟ Month
mn_aprobada_para_servicios_tecnicos -> MN Aprobada (Servicios Tecnicos)
motivo__revision_ -> Motivo (Revision)
motivo_del_pendiente_m1 -> Motivo del pendiente M1
motivo_del_pendiente_m2 -> Motivo del pendiente M2
motivo_del_pendiente_m3 -> Motivo del pendiente M3
n1st_commission -> ⍟ 1ST Commission
n2nd_commission -> ⍟ 2ND Commission
name_of_spouse_or_co_debtor -> ⍟ Name of Spouse or Co-Debtor
negocio_con_ntp -> Negocio con NTP (Tickets)
negocios_instalados__tickets_ -> Negocio Instalado (Tickets)
net_measurement_permit_status -> ⍟ Net Measurement Permit Status
nombre_corporacion -> Nombre Corporación
nombre_del_gerente -> Nombre del Gerente
nombre_sub_director -> Nombre Sub-Director
nota_de_cotizacion_de_paneles -> Nota de Servicio Facturable
nota_de_interventor -> Nota (Interventor)
nota_form_consultor -> Nota Form Consultor
nota_ticket__sac_ -> Nota Ticket (SAC)
nota_ultima_revision_milestone -> Nota Última Revisión Milestone
notas__revision_ -> Notas (Revision)
note_glossary -> Note Glossary
notes_last_contacted -> Last Contacted (Ticket Note)
notes_last_updated -> Last Activity Date (Ticket Note)
notes_next_activity_date -> Next Activity Date (Ticket Note)
nps_follow_up_answer -> NPS follow up
nps_follow_up_question_version -> NPS follow up question
nps_score -> Conversation NPS score
num_contacted_notes -> Number of times contacted (Ticket Note)
num_notes -> Number of Sales Activities
number_of_batteries -> ⍟ Number of Batteries
number_of_inverters -> ⍟ Number Of Inverters
numero_cuenta_luma -> Número Cuenta Luma
numero_de_casos_revisados__auditoria_ -> Número de casos trabajados (Auditoria)
numero_de_mn -> Número de MN (Ticket)
other_1___other_2 -> ⍟ Other 1 / Other 2
paid -> ⍟ Paid
paid_additional_charge -> ⍟ Paid Additional Charge
panel_model -> ⍟ Panel Model
paneles_a_instalar__tickets_ -> Paneles a Instalar (Tickets)
paneles_qty_a_instalar__tickets_ -> Paneles QTY a Instalar (Tickets)
payment_confirmation -> Payment Confirmation
payment_status -> Payment Status
pendiente_m1 -> Pendiente M1
pendiente_m2 -> Pendiente M2
pendiente_m3 -> Pendiente M3
permisology -> ⍟ Permisology
permit_electrical_certification -> ⍟ Permit Electrical Certification
personal_de_reubicacion_a_c -> Personal de reubicación A/C
personas_a_pagar -> Personas a pagar
phone -> ⍟ Phone
physical_address -> ⍟ Physical Address
plano -> Plano
po_colocado -> PO Colocado
position -> ⍟ Position
primer_pago -> 1ra Comisión Trabajada
primer_pago_realizado -> Primer pago realizado
propietario_adicional_ticket__costco_ -> Propietario Adicional
prueba_tarifa_aplicada -> Prueba Tarifa Aplicada
ps_engineering_status -> ⍟ Ps Engineering Status
pueblo_para_servicio_tecnico -> Municipios PR (Tickets)
purchase_type -> ⍟ Purchase Type
quien_solicita___sati -> Quien Solicita - SATI
rack_a_instalar__tickets_ -> Rack a Instalar (Tickets)
rango_irregular_de_voltaje__tickets_ -> Rango Irregular de Voltaje (Tickets)
razon_de_cancelacion -> Razon de Cancelacion
razon_de_escalamiento -> Razón de Escalamiento
razon_de_referido_a_interventor -> Razón - (Interventor)
razon_de_visita -> Razón de Visita
reconocimiento_y_garantia -> IF | Reconocimiento y Garantia
reembolso_100_usd -> Reembolso 100 USD
referido_a_sunrun -> Referido a Sunrun
referido_por__interventor_ -> Referido por (Interventor)
region -> ⍟ Region
region__tickets_ -> Región (Tickets)
region_consultor -> Region_Consultor
regulacion_voltaje_tickets -> Regulación Voltaje (Tickets)
repair -> ⍟ Repair
reparacion_electrica -> Reparacion Electrica
reparacion_por -> Reparacion por
reporte_fotos -> Reporte Fotos
reporte_programacion -> Reporte Programación
residential_commercial -> ⍟ Residential/Commercial
resolucion_corporativa -> Resolución Corporativa
resolucion_soporte_it -> Resolución (Soporte IT)
responsable_del_caso_m1 -> Responsable del caso M1
responsable_del_caso_m2 -> Responsable del caso M2
responsable_del_caso_m3 -> Responsable del caso M3
reubicacion_a_c_facturada -> Reubicación A/C facturada
reubicacion_de_a_c -> Reubicación de A/C
revison_por -> Revison por
sales_status -> ⍟ Sales Status
sales_team -> ⍟ Sales Team
segundo_pago -> 2da Comisión Trabajada
segundo_pago_realizado -> Segundo pago realizado
semana_de_instalacion -> Semana de instalación
situacion_de_reparacion -> Situación de Reparación
solar_insurance -> ⍟ Solar Insurance
solarinsurance_precio__tickets_ -> SolarInsure Precio (Tickets)
solarinsure__tickets_ -> SolarInsure (Tickets)
sometido_sin_gateway -> Sometido sin Gateway
source_ref -> Reference to source-specific object
source_thread_id -> Reference to email thread
source_type -> Source
ss_natural -> SS Natural
ss_patronal -> SS Patronal
status_de_interventor -> Estatus (Interventor)
subject -> Ticket name
sunrun -> ⍟ Sunrun Status
sunrun_4_photos -> ⍟ Sunrun 4 Photos
sunrun___epc_price -> Sunrun | EPC Price
sunrun___m1_amount_paid -> Sunrun | M1 amount paid
sunrun___m1_payment -> Sunrun | M1 Payment
sunrun___m1_payment_date -> Sunrun | M1 payment date
sunrun___m3_amount_paid -> Sunrun | M3 amount paid
sunrun___m3_payment -> Sunrun | M3 Payment
sunrun___m3_payment_date -> Sunrun | M3 payment date
sunrun___service_contract_id__key__milestone -> Sunrun | Service Contract ID (Key) Milestone
sunrun___system_size_dc -> Sunrun | System Size DC
sunrun__servicios_tecnicos_ -> Sunrun (Servicios Tecnicos)
sunrun_commissioning -> ⍟ Sunrun Commissioning
sunrun_contract_id -> Sunrun | Service Contract ID (Ticket)
sunrun_contract_id__ -> ⍟ Sunrun Contract ID ˅
sunrun_final_completion_date -> Sunrun | Final Completion Date
sunrun_granted -> Sunrun | NTP Granted
sunrun_link_portal -> ⍟ Sunrun Link Portal
sunrun_m1_proof__panel_inverter_delivery -> Sunrun | M1 proof: panel/inverter delivery
sunrun_m2_proof__substantial_completion -> Sunrun | M2 proof: substantial completion
sunrun_m3_proof_upload_date -> Sunrun | M3 Proof Upload Date
sunrun_pk -> Sunrun | Proposal: Proposal ID Reportado
sunrun_pk__ -> ⍟ Sunrun PK ˅
sunrun_pk_actualizado -> Sunrun | Proposal: Proposal ID Actualizado
sunrun_pto -> Sunrun | PTO
sunrun_signoff -> Sunrun | SR Signoff
system_programming -> ⍟ System Programming
tags -> Tags
takeoff_engineering -> ⍟ Takeoff Engineering
team_leader -> Team Leader
tecnico_asignado_permisologia -> Tecnico Asignado Permisología
tecnico_de_datos_permisologia -> Tecnico de Datos Permisología
telefono_empleado_rrhh -> Telefono Empleado RRHH
telefono_llamada__sac_ -> Telefono Llamada (SAC)
tiempo_entre_fechas__ing -> Tiempo Entre Firma de Contrato e Instalacion Finalizada
tiempo_entre_firma_de_contrato_y_ntp -> Tiempo Entre Firma de Contrato y NTP
tiempo_entre_instalacion__y_m1_proof -> Tiempo Entre Instalacion  y M1 Proof
tiempo_entre_m1_proof_y_m2_proof -> Tiempo Entre M1 Proof y M2 Proof
tiempo_entre_m2_proof_y_m3_proof -> Tiempo Entre M2 Proof y M3 Proof
tiempo_entre_m3_proof_y_m3_payment_day -> Tiempo Entre M3 Proof y M3 Payment Day
tiempo_entre_ntp_e_instalacion_finalizada -> Tiempo Entre NTP e Instalacion Finalizada
time_to_close -> Time to close
time_to_first_agent_reply -> Time to first agent email reply
tipificacion__sac_ -> Tipificación (SAC)
tipificacion__servicios_tecnicos_ -> Tipificación (Servicios Tecnicos)
tipificacion_de_auditoria -> Tipificación de Entrada (Auditoría)
tipificacion_de_salida__auditoria_ -> Tipificación de Salida (Auditoría)
tipo_de_cliente -> Tipo de cliente
tipo_de_compra_residencial -> Tipo de compra residencial
tipo_de_de_servicio_facturable -> Tipo de Servicio Facturable
tipo_de_intervencion -> Tipo de Intervención (Auditoria)
tipo_de_negociacion -> Tipo de negociación
tipo_de_pago -> Metodo de Pago (Tickets)
tipo_de_propiedad__residencial___comercial___tickets_ -> Tipo de Propiedad (Residencial | Comercial) (Tickets)
tipo_de_servicio__servicios_tecnicos_ -> Tipo de Servicio (Servicios Tecnicos)
tipo_de_solicitud_soporte_it -> Tipo de Solicitud (Soporte IT)
tipo_de_solicitud_sunrun_soporte_it -> Tipo de Solicitud Sunrun (Soporte IT)
tipo_de_visita -> Tipo de Visita
town -> ⍟ Town
underwriting -> ⍟ Underwriting
unidades_reubicadas_a_c -> Unidades reubicadas A/C
usuario___luma -> Usuario - LUMA (Tickets)
visita_de_programacion_requerida -> Visita de programación requerida
weeks -> ⍟ Weeks
welcome_call -> ⍟ Welcome Call


PARA LA BUSQUEDA Y COMPARACION NECESITAMOS
_T_FSD = "fsd__"
_T_FIRSTNAME = "firstname"  # algunos tickets lo tienen
_T_LASTNAME = "lastname"
_T_ID_GOFORMZ = "id_goformz__servicios_tecnicos_"
_T_ADDRESS = "physical_address"
_T_PHONE = "phone"
_T_EMAIL = "e_mail"
_T_COUNTY = "pueblo_para_servicio_tecnico"
_T_SUBJECT = "subject"
_T_NOTA = "nota_ticket__sac_"  # ajusta si "nota" tiene otro nombre interno
_T_PHONE_ALT = "telefono_alterno"
_T_STATE = "state"
_T_ZIP = "zip"
_T_CITY = "city"
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
**Versión**: 1.0.0  
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


def cargar_cookies(driver, sitio: dict, url_base: str, carpeta: Path | None = None) -> bool:
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
  "ultimo_monitor": 1,
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
  "destino_subida": "AMBOS",
  "ultima_celda_calendar": "g20",
  "ultima_pestana_calendar": "Jun"
}
````

## File: readme.md
````markdown
# SSAuto

## Descripción

SSAuto es una herramienta de escritorio para Windows que automatiza capturas de pantalla de regiones específicas y las sube a portales web (HubSpot y Sunrun). También incluye un comparador de datos entre HubSpot y Sunrun, y un generador de mensajes de contacto estandarizados.

Combina `customtkinter` (GUI), `mss` (captura de pantalla) y `Selenium` (automatización de navegador). La arquitectura es modular, con un sistema de plugins para agregar nuevos sitios de destino.

## Estructura del proyecto

```
ssauto/
├── main.py                         # Punto de entrada (registro de plugins, UI)
├── version.py                      # Versión (0.1.1)
├── medidor.py                      # Selector visual de región de pantalla
├── scraping_sunrun.py              # Scraper de datos de Sunrun (Salesforce)
├── template_filler.py              # Generador de mensajes (legacy)
├── iniciar_chrome_sesion.py        # Lanza Chrome con puerto de depuración 9222
├── recuperar_puerto.py             # Diagnóstico y recuperación del puerto 9222
├── requirements.txt                # Dependencias del proyecto
├── .env                            # ACCESS_TOKEN de HubSpot
│
├── config/
│   ├── configuracion.py            # Configuración global, SITIOS, carga/guardado
│   ├── credenciales.py             # Keyring + serialización de cookies
│   ├── apps_captura.py             # Apps de captura rápida (Wolkbox, B2Chat, etc.)
│   ├── config.json                 # Configuración de runtime
│   └── plantillas.json             # Plantillas de mensajes
│
├── core/
│   ├── base_plugin.py              # Contrato ABC para plugins de sitios
│   ├── plugin_registry.py          # Registro estático de plugins
│   ├── browser.py                  # Factoría de Chrome/Selenium
│   ├── captura.py                  # Servicio de captura de pantalla (mss)
│   ├── comparador.py               # Motor de comparación HubSpot vs Sunrun
│   ├── monitors.py                 # Detección de monitores (mss)
│   └── medidor_runner.py           # Ejecutor del medidor de región visual
│
├── services/
│   ├── sesion_service.py           # Orquestación de subida (UI ↔ plugins)
│   └── session_manager.py          # Gestión de sesiones y cookies por plugin
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
│   ├── custom_ctkframe.py          # CTkFrame extendido (conveniencia)
│   ├── posicion_ventanas.py        # Posicionamiento de ventanas hijas
│   └── widgets/
│       ├── coordinate_inputs.py    # Inputs de coordenadas (x, y, w, h)
│       ├── log_widget.py           # Widget de registro (CTkTextbox)
│       ├── monitor_selector.py     # Selector de monitor
│       └── profile_manager.py      # Gestor de perfiles de región
│
├── data/
│   ├── api.py                      # Cliente de HubSpot REST API
│   ├── buscador.py                 # Estrategias de búsqueda de contactos
│   └── PROPIEDADES DE *.TXT        # Referencias de propiedades de HubSpot
│
├── test/
│   ├── test_buscar_fsd.py          # Tests de búsqueda de FSD
│   └── test_fix_final.py           # Tests de búsqueda de contactos
│
├── gsheets/                        # Captura de celdas de Google Sheets
│   ├── __init__.py                  # Punto de entrada (TicketCaptureService)
│   ├── utils/
│   ├── colors.py                   # Utilidades de color (oscurecer)
│   ├── fsd.py                      # Normalización y display de FSD
│   └── paths.py                    # Resolución de rutas (resource_path)
│   │   ├── cell_parser.py           # Parser de referencias A1 (F6 → A3,F3,A6,F6)
│   │   └── image_compositor.py      # Compositor de grilla 2×2 (Pillow)
│   ├── data/
│   │   └── sheets_api.py            # Cliente de Google Sheets API v4 (Service Account)
│   ├── core/
│   │   └── playwright_capture.py    # Captura visual de celdas con Playwright
│   ├── services/
│   │   └── ticket_capture_service.py # Orquestador (parser → API → Playwright → imagen)
│   ├── sessions/                    # Perfil persistente de Chrome para Playwright
│   └── tests/                       # Tests del módulo gsheets (16 tests)
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

### Calendar — Google Sheets

El botón **Calendar** en el panel de aplicaciones abre un modal para capturar celdas de Google Sheets. El flujo interno:

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

La pestaña **Comparison** permite buscar contactos en HubSpot por FSD, nombre, teléfono, correo o dirección, y compararlos campo por campo contra los datos registrados en Sunrun. Las diferencias se resaltan por colores.

### Generador de mensajes

La pestaña **Templates** ofrece plantillas de mensajes por categoría (HubSpot, Sunrun, General) con editor completo. La pestaña **Messages** genera mensajes de contacto estandarizados (fuera de servicio, buzón de voz, no contesta) en español e inglés con manejo automático de singular/plural y fechas.

### Chrome

La aplicación puede conectarse a una instancia de Chrome ya abierta (puerto 9222) o lanzar una nueva. Para usar una sesión existente:

```bash
python iniciar_chrome_sesion.py
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
pytest tests/ -v                    # Todos los tests (273 tests)
pytest gsheets/tests/ -v            # Tests del módulo Google Sheets (16 tests)
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


26/05/2026
Dispatch Cancelled -> No es trabajable aparece en color rojo
Dispatch Reported -> No es trabajable aparece en color rojo
Dispatch Approved -> No es trabajable aparece en color rojo
Dispatch Accepted -> Es trabajable aparece en color verde con letra diferente
Dispatch Rejected -> Es trabajable aparece en color verde con letra diferente

Que aparezca en la parte de arriba de los resultados de busqueda y justo debajo aparezca la "Appointment Date" junto al "Case Reason"
Toda esta informacion solo aparece en Sunrun asi que se vea de forma organizada en la ventana de comparacion

repomix --ignore "doku.md"
repomix --compress --style markdown
repomix --compress --ignore "doku.md"


Tareas realizadas hoy, se puso el Estado del dispatch de sunrun en la ventana de comparacion, para esto se tuvo que extraer cada uno de los selectores correctos para cada variable en formato XPATH, ademas unos extra para el bot de selenium, los selectores estan en @scraping_sunrun.py y son:

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

Con estos selectores se pudo hacer el web scraping correctamente y sacar toda la informacion de Sunrun, en la ventana de comparacion debajo de la barra de busqueda, estan los resultados de esta busqueda y se pueden ver con los colores verde para los trabajable y rojo para los no trabajables, tambien se arreglo el puerto 9222 que no estaba funcionando, no estaba abriendo la sesion abierta anteriormente y abria otra pestaña, se uso repomix para el uso de IA.
Se le puso un dropdown a cada boton de captura de aplicacion para guardar el tamaño tomado de la pantalla despues de realizar la medicion.




Hay que arreglar el nombre en el comparador
ejemplos de nombre:

FSD1251074 - FRANCES BARCELO - ID 245852
FSD1251053 - MARLA SANTIAGO - ID 252735
FSD1251006 - Lillian Lee - ID 271098
FSD1223020 - Evelissette Carrion-261284-sin produccion
FSD1220201 - Ernesto Ivan suarez rivera - SININFO - Paneles solares
FSD1220222 - Aurea Santiago Torres - 229613 -Gateway Not Reporting
FSD1221131 - PATRICIA QUINTANA - 238096 - VERIFICAR SISTEMA
FSD1219280 - MARIA RIVERA VAZQUEZ - 227535 - METERING
FSD1219870 - MAYRA ACOSTA - 267923 - VERIFICAR SISTEMA
FSD1198643 - DENNIS AYALA/ HEIDI TORRES- 220484-UPGRADE BATERIA
FSD1205902 - LUIS MELENDEZ - 265580 - METERING
FSD1208393 - EDUARDO CORREA DIAZ - 256836 - VERIFICAR SISTEMA
FSD1205910- ANGEL L MACHIN RIVERA- 212826- UPGRADE BATERIA
FSD1208909 - JOSE VIDAL - 265025 - METERING
FSD1205223 - BENJAMIN GAUTHIER RODRIGUEZ - 216093 - METERING


Se arreglo el nombre en el comparador, ahora se parsea el fsd - nombre - id - y se quitan los comentarios.
TAMBIEN SE PARSEAN SIMBOLOS RAROS COMO [-/\\|] ETC.
PROXIMO: HACER QUE SE VEA TODO EL SUBJECT MEJOR PARA MAS CLARIDAD. BUSQUEDA POR DEMAS ATRIBUTOS Y SUBIDA A SUNRUN Y A AMBAS PLATAFORMAS. ORC IMPLEMENTADO, CAPTURA DE EXCEL Y RECORTE AUTOMATICO DE CELDAS PARA UNA MEJOR CAPTURA

27/05/2026
Hola, estoy haciendo un script de automatizacion, uso selenium y web scraping, y tengo una ventana de comparacion, en esta ventana se realiza la comparacion entre 2 sitios web, uno es sunrun y el otro es hubspot, quiero mejorar la busqueda, mi idea es agregar varios atributos  mas para la busqueda, PERO, esto es algo complejo porque resulta que la unica forma de comparar entre los 2 sitios web es con el FSD, sin este no se puede buscar bien, PERO, estuve pensando y si se puede hacer algo, creo que hacer la busqueda internamente mediante el fsd es una buena idea, o sea, digamos que busco por direccion -> el comparador encuentra algo por la API de hubspot, de ahi saca los atributos importantes como el nombre, la direccion, municipio, etc y encuentra el FSD, al encontrar el FSD realiza la comparacion con Sunrun que es la pagina donde utilizo web scraping, esto si se puede hacer? la idea es implementar esta funcionalidad sin dañar ninguna otra funcionalidad y que los atributos de busqueda sean elegidos con un dropdown o algo mejor, que sugieres hacer? se puede implementar? gracias


Que alegria que si se pueda implementar! Gracias por entender la idea, bueno ahora te pasare algunos metodos y archivos que tengo: 
comparador.py
_norm
_comparar_nombres
_similitud
_vacio
_normalizar_telefono
comparar_campo
comparar
datos_hs_desde_ticket


api.py
tengo varios diccionarios con atributos, municipios, comentarios
_norm
_detectar_municipio
_parsear_asunto
_val
_buscar_ticket_por_fsd
_buscar_contacto_por_id_goformz
_limpiar_nombre_hubspot
extraer_datos_hubspot
extraer_ticket_por_fsd

ventana_comparacion.py
class VentanaComparacion en customtkinter
__init__
_traer_al_frente
_cerrar
_construir_ui
_lanzar_comparacion
ui_log
_obtener_hubspot
_limpiar_resultados
_mostrar_resultado_externo
_mostrar_resultado
_fila_campo
celda
_resumen
_mostrar_error

para que me des masomenos la idea de donde hacer los cambios, recuerda que lo tengo construido en customtkinter

comparador.py
├── Agregar método: _buscar_hubspot_por_estrategia()
│   └── Usa extraer_datos_hubspot() existente pero con filtros flexibles
├── Agregar método: _extraer_fsd_desde_candidato()
│   └── Saca el FSD de un candidato HubSpot
└── Método existente comparar() sigue igual
    └── Ahora puede recibir FSD como parámetro

api.py
├── Agregar diccionario: SEARCH_STRATEGIES
│   └── Define tipos de búsqueda disponibles
├── Agregar método: buscar_contactos_por_criterio()
│   └── Búsqueda flexible según estrategia
└── Métodos existentes: no tocar

ventana_comparacion.py (AQUÍ ES DONDE MÁS CAMBIOS)
├── EN __init__:
│   ├── Agregar variable: self.search_strategy = "direccion"
│   └── Agregar variable: self.candidatos_hubspot = []
│
├── EN _construir_ui():
│   ├── NUEVA SECCIÓN: Frame de búsqueda mejorada
│   │   ├── Dropdown: tipo de búsqueda (SEARCH_STRATEGIES)
│   │   ├── Input(s) dinámico(s) según tipo
│   │   └── Botón: "Buscar en HubSpot"
│   │
│   ├── NUEVA SECCIÓN: Tabla de candidatos
│   │   ├── Tabla con Nombre, Dirección, Municipio, FSD
│   │   ├── Columna izquierda: Radio buttons
│   │   └── Botón: "Comparar seleccionado"
│   │
│   └── SECCIÓN EXISTENTE: Comparación (igual pero mejorada)
│       └── Ahora recibe datos del candidato seleccionado
│
├── NUEVOS MÉTODOS:
│   ├── _al_cambiar_tipo_busqueda(tipo)
│   │   └── Actualiza inputs dinámicos según SEARCH_STRATEGIES
│   ├── _obtener_criterio_busqueda()
│   │   └── Lee los inputs según tipo seleccionado
│   ├── _buscar_candidatos()
│   │   └── Llama a comparador._buscar_hubspot_por_estrategia()
│   ├── _mostrar_candidatos()
│   │   └── Llena la tabla con resultados
│   ├── _obtener_candidato_seleccionado()
│   │   └── Devuelve el candidato elegido
│   └── _lanzar_comparacion_mejorada()
│       └── Nueva versión de _lanzar_comparacion() con FSD automático
│
└── MÉTODOS EXISTENTES (refactorizar levemente):
    └── _lanzar_comparacion() → puede llamar a _lanzar_comparacion_mejorada()


Los contactos NO TIENEN id_cliente, tienen contact_id.
Eso significa que en HubSpot:

CONTACTOS tienen contact_id (referencia interna de HubSpot)
TICKETS tienen id_goformz__servicios_tecnicos_ (el ID del cliente que buscas)

La solución es: Cuando buscas por nombre/email/etc y obtienes un contacto, necesitas buscar el TICKET asociado usando el contact_id para obtener el FSD.
Perfecto, ahora veo el problema. La línea 459 intenta obtener id_de_goformz__contacto_ del CONTACTO, pero ese campo NO EXISTE en los contactos.
El id_de_goformz__contacto_ es un campo que está en los CONTACTOS pero parece que es None o no está en los resultados que devuelve HubSpot.
La solución es: Buscar los TICKETS por firstname + lastname para encontrar el id_goformz__servicios_tecnicos_ que es lo que necesitas.

¡Casi! La coma no es el problema — el ticket SÍ se encuentra. El problema es otro: fsd__ está None en ese ticket.
Mira el subject: 'Daisy I Soto Santiago-267334-Orientación Sunrun' — no tiene FSD. Este ticket es de orientación, no de servicio técnico. El FSD está en otro ticket del mismo cliente.
El fix es buscar todos los tickets del cliente, no solo el primero, y quedarse con el que tenga fsd__ llenado:
El diagnóstico exacto: el ticket 39542009896 existe y tiene el id_cliente correcto, pero es un ticket de "Orientación Sunrun" — no tiene FSD porque no es una orden de servicio técnico. El cliente 267334 tiene múltiples tickets y el FSD está en otro.
El fix hace dos cosas:

Trae hasta 10 tickets del mismo id_cliente en vez de solo el primero
Elige el que tenga fsd__ llenado — si ninguno lo tiene, usa el primero como antes

También agregué manejo del formato con coma (267,334 vs 267334) por si aparece en otros casos.
Prueba y dime qué sale en consola ahora.

El diagnóstico completo
Cuando buscas por FSD, el flujo es directo: ticket → FSD. Fácil.Pero cuando buscas por correo/teléfono/nombre, el flujo es: contacto → id_cliente → ticket → FSD. Y en ese camino había 4 cosas rotas.

Bug 1 — Campo de dirección incorrecto
En _SEARCH_CONTACT_FIELDS tenías "direccion": "address". Ese campo address existe en tickets, no en contactos. En contactos el campo real se llama direccion__fisica_. Por eso la dirección siempre llegaba None.

# ❌ Antes
"direccion": "address"

# ✅ Después  
"direccion": "direccion__fisica_"

Bug 2 — Operador de búsqueda incorrecto
Todo usaba CONTAINS_TOKEN, que sirve para texto libre como nombres. Pero un teléfono como +19394004759 HubSpot no lo tokeniza — no lo parte en palabras. Necesita EQ (igual exacto).

# ❌ Antes — siempre CONTAINS_TOKEN
operator = "CONTAINS_TOKEN"

# ✅ Después — depende del campo
operator = "EQ" if tipo_busqueda in {"telefono", "correo", "id_cliente"} else "CONTAINS_TOKEN"

Bug 3 — _buscar_fsd_por_contact_id usaba una propiedad no filtrable
Cuando el contacto no tiene id_cliente, el fallback buscaba tickets filtrando por hs_all_contact_ids. El problema es que esa propiedad no es filtrable en la Search API de HubSpot — la API simplemente la ignora y devuelve vacío sin dar error. Lo reemplacé con la API de asociaciones, que es la forma correcta:

# ❌ Antes — filtro que HubSpot ignora silenciosamente
TicketSearchRequest(filters=[{"propertyName": "hs_all_contact_ids", ...}])

# ✅ Después — API de asociaciones: contacto → sus tickets
assoc_response = _client.crm.associations.v4.basic_api.get_page(
    object_type="contacts",
    object_id=contact_id,
    to_object_type="tickets",
)
ticket_id = assoc_response.results[0].to_object_id
ticket = _client.crm.tickets.basic_api.get_by_id(ticket_id)

Bug 4 — El más tramposo: limit=1 traía el ticket equivocado
Este fue el que encontramos juntos al final. El cliente 267334 tenía varios tickets:

Ticket de "Orientación Sunrun" → fsd__ = None ← este llegaba primero
Ticket de servicio técnico → fsd__ = "983XXX" ← este era el que necesitabas

Con limit=1 HubSpot devolvía el primero que encontraba (orden interno de HubSpot, no el más relevante). El fix fue pedir hasta 10 y elegir inteligentemente:

# ❌ Antes — trae el primero que aparezca, puede no tener FSD
limit=1
return response.results[0]

# ✅ Después — trae varios y elige el que tenga FSD
limit=10

ticket_con_fsd = None
ticket_fallback = None

for ticket in response.results:
    fsd_val = ticket.properties.get("fsd__", "")
    if fsd_val and str(fsd_val).strip():
        ticket_con_fsd = ticket  # ← este es el bueno
        break
    if ticket_fallback is None:
        ticket_fallback = ticket  # ← por si ninguno tiene FSD

# Usar el que tiene FSD, o el primero si ninguno lo tiene
ticket = ticket_con_fsd or ticket_fallback

La lógica es: recorre los tickets uno por uno, en cuanto encuentres uno con fsd__ llenado, para ahí. Si ninguno tiene FSD, usa el primero de todos como antes (no rompe nada, solo no tendrá FSD).

En resumen, el error ❌ No se pudo extraer FSD del candidato era el síntoma final de una cadena larga — los bugs 1, 2 y 3 hacían que la búsqueda fallara antes de llegar a los tickets, y el bug 4 hacía que aunque llegara, trajera el ticket equivocado.

ver @image.png

28/05/2026
Se arreglo una parte de la ventana_comparacion para que los resultados de busqueda no taparan los resultados de comparacion, se trabajo en el archivo plugin_sunrun que es el archivo que controla la subida de archivos / capturas a sunrun, la idea es que detecte la pestaña con el fsd-0000000 y haga el proceso de subida, la pestaña debe estar abierta desde antes, PERO, me gustaria mejorar eso y tengo 4 opciones:
1- input manual con el fsd
2- leer el fsd desde el nombre del archivo (no sirve)
3- clipboard - ocr - pdf (me gustaria)
4- que el usuario pueda elegir entre las distintas pestañas abiertas: con el fsd
1. FSD-980124
2. FSD-981555
3. FSD-777222
realmente se pueden implementar las 4 pero la mejor por ahora es la 1

Lo complicado es que el bot detecte la pestaña correcta, para esto se agrego un input donde el usuario ingresa el fsd y el bot busca entre las pestañas abiertas mediante su titulo hasta encontrar la que tenga el fsd igual al ingresado, se agrego un switch para poder poner o quitar esta opcion, no importa como este ingresado el fsd si tiene guion o no tiene "fsd" escrito el lo va a encontrar, las subidas a cada plataforma funcionan excelente, FALTA: agregar ocr y la captura por celda al calendar, falta agregar el id del ticket a los campos comparados, tambien falta hacer la busqueda pero con subida en el fsd con sunrun, usar parte del scraping_sunrun para los selectores, ya que desde ahi se hace la busqueda del fsd para luego sacar la info del fsd. Actualmente la subida funciona, la comparacion igual, las demas ventanas tambien

COVERAGE
coverage run main.py
coverage lcov
coverage html
Start-Process htmlcov/index.html


Hola mi rey, necesito configurar la subida a SUNRUN, en mi script de automatizacion para subida de capturas, ya tengo los selectores y todo, te digo el flujo y le damos, cuando el usuario esta en un fsd-0000000, en la interfaz hay un boton que dice RELATED, hay que darle a ese boton y esperar un momento a que cargue el contenido, ahi es donde estan las notas "notes y attachments" y hay un boton que dice "upload files" ahi ya se abre el administrador de archivos para subir el archivo, la verdad el flujo no es complicado,

OTRA COSA NOTAS:

"Actúa como un desarrollador frontend experto. Escribe el código HTML y CSS para [describe tu componente, ej: una tarjeta de producto]. El diseño debe verse profesional, minimalista y humano. Sigue estas reglas estrictas:Usa un sistema de espaciado consistente (ej. usando variables CSS para márgenes y rellenos).No uses sombras paralelas (box-shadow) exageradas; usa bordes muy sutiles o espacios en blanco (white space) para la separación.La tipografía debe ser limpia, usando fuentes modernas del sistema (ej. system-ui, -apple-system).El diseño debe ser adaptable (responsive) por naturaleza utilizando Flexbox o Grid, sin depender de alturas fijas.Evita que parezca generado por IA; usa transiciones suaves, colores coherentes y una paleta de colores contenida."

29/05/2026

¡Perdón por la confusión! Déjame explicártelo de forma súper sencilla, porque tienes toda la razón en asustarte si lo ves así, pero no funciona como piensas.
Tu suscripción NO se va a acabar en un día. El truco es que OpenCode Go te da "dinero de mentira" para gastar en tokens.

¿Cómo funciona realmente el dinero que ves?
Tú pagas $10 reales al mes de tu bolsillo. A cambio, OpenCode te regala un límite de consumo virtual equivalente a $60 de saldo al mes en peticiones de inteligencia artificial.
Ese mensaje de $0.03 spent (3 centavos gastados) se va restando de ese regalo de $60 virtuales, no de tus $10 reales.

Los límites reales de tu plan (El sistema de control)
Para evitar que un usuario gaste todos los $60 virtuales el primer día y sature los servidores, el sistema te pone "candados" de tiempo:
Límite de 5 horas: Puedes gastar un máximo de $12 virtuales cada 5 horas.
Límite semanal: Puedes gastar un máximo de $30 virtuales a la vigencia de la semana.
Límite mensual: Puedes gastar un máximo de $60 virtuales al mes.

Si en un día de trabajo súper intenso te acabas el presupuesto asignado para esas horas, no tienes que pagar más dinero. Lo que sucede es:
El sistema te frena temporalmente para proteger el servidor.
Solo debes esperar a que se cumpla el ciclo de tiempo (las 5 horas o la semana) para que tu saldo se vuelva a rellenar automáticamente a tope gratis
Si te urge seguir programando de inmediato y no quieres esperar, puedes cambiarte a un modelo "Flash" (como DeepSeek V4 Flash), que son prácticamente ilimitados porque consumen casi cero centavos.
En resumen: Quédate tranquilo. Tus $10 te cubren todo el mes de uso normal. El contador de centavos es solo una métrica para que veas qué tan "caro" o "barato" es el modelo de IA que elegiste.

Jajaja, lo siento de verdad! No era mi intención darte ese susto. 🙏Quédate totalmente tranquilo. Esos centavos que ves en la pantalla son solo el contador interno del programa con sus "monedas del juego". Nadie te va a cobrar de más, ni te vas a quedar sin IA a mitad de la tarde. Tu mes de suscripción está 100% asegurado.Ahora que ya sabemos que tu saldo está a salvo y que todo está bien configurado en tu VS Code, ¿qué te parece si empezamos a tirar código?Si quieres, dime qué tecnología estás usando (Python, JavaScript, React, HTML...) o qué función quieres programar, y ponemos a trabajar a ese asistente para sacarle el jugo a la suscripción.


Algunos de los switches no se estaban guardando entonces no estaban persistiendo en el archivo de config.json algunas como:

Modo sin ventana de Chrome ventana_principal.py:506 headless_var False

Usar Chrome ya abierto (puerto 9222) ventana_principal. py: 510 chrome_existente_var True

Destino de subida (HUBSPOT/SUNRUN/AMBOS) ventana_principal.py:475 destino_var "AMBOS"

Búsqueda inteligente por FSD (toggle) ventana_principal.py:536 usar_fsd_var False

Ninguno de estos switches/selectores tiene codigo para guardar su valor en config. json.

Configuración con persistencia ROTA

Último monitor -> Se lee al iniciar (ventana_principal.py:327), pero el codigo que lo guarda esta en _al_cerrar() (ventana_principal.py:1411-1414), un metodo que nunca se llama - no esta vinculado a WM_DELETE_WINDOW ni a ningun protocolo de cierre. Es codigo muerto.

Configuraciones que SI se persisten correctamente

- Tema (oscuro/claro) + config.json["tema"]
- Atajo de teclado (keybind) + config. json["keybind"]
- Auto-submit nota (HubSpot) + config. json["auto_submit_nota"]
- Perfiles de region + config.json["perfiles_region"]
- Regiones por aplicacion + config. json["regiones_apps"]
- Monitores por aplicacion + config. json["monitores_apps"]
- Credenciales OS Keychain (keyring)
- Plantillas de mensajes + config/plantillas. json
- Cookies de sesion cookies/ *. pkl

Resumen

3 toggles principales (headless, Chrome existente, destino de subida) y 1 toggle opcional (FSD) no tienen ninguna logica de persistencia. Ademas, la
seleccion de monitor tiene codigo de guardado que nunca se ejecuta por no estar vinculado al evento de cierre de ventana.

Cambios aplicados. Resumen de lo modificado:

config/configuracion.py - nuevas claves (headless, chrome_existente, destino_subida) con sus helpers cargar _* /guardar _*.

ui/ventana_principal.py - 4 correcciones:

1. headless_var + carga desde config + trace para guardar al cambiar
2. chrome_existente_var + carga desde config + trace para guardar al cambiar
3. destino_var carga desde config + guarda en _seleccionar_destino(). Tambien se corrigio que la inicializacion sobreescribia el valor cargado con
"AMBOS" hardcodeado
4. ultimo_monitor + se agrego persistencia en _actualizar_info_monitor() (trace existente). El metodo muerto _al_cerrar() fue eliminado

Todas las configuraciones nuevas aparecen ahora en config. json con sus valores por defecto.

README actualizado. Los cambios principales:
- Estructura de directorios actualizada con la arquitectura modular actual (config/, core/, services/, plugins/, ui/, data/)
- Nuevas funcionalidades documentadas: comparador HubSpot/Sunrun, generador de mensajes, editor de plantillas
- Sección de configuración inicial (.env, credenciales)
- Instrucciones para agregar nuevos plugins
- Referencias a archivos obsoletos eliminadas (configuracion.py, automatizacion.py, etc.)


Es muy común al empezar con agentes de código. Muchas IAs interpretan "revisa" como una tarea de auditoría y te devuelven un informe, pero no hacen cambios.

La clave es ser explícito sobre qué quieres que haga después del análisis.

Por ejemplo, en lugar de:

Revisa que todas las configuraciones y switches persistentes se guarden correctamente.

Prueba:

Revisa todo el proyecto y detecta configuraciones, switches, toggles o preferencias que deberían persistirse. No te limites a generar un informe. Implementa los cambios necesarios en el código para que se guarden y restauren correctamente. Al finalizar, muestra los archivos modificados y explica brevemente qué cambiaste.

O incluso más directo:

Actúa como desarrollador. Analiza el código, identifica configuraciones que no se estén guardando correctamente y corrige el problema. Aplica los cambios directamente en los archivos del proyecto. No quiero solo un diagnóstico; quiero una implementación funcional.

Si usas OpenCode o herramientas similares, suele funcionar bien este flujo:

Análisis

Inspecciona el proyecto y enumera todas las configuraciones que deberían persistirse.

Plan

Propón un plan de cambios concreto.

Implementación

Ahora implementa todos los cambios del plan directamente en el código.

Verificación

Comprueba que cada configuración se carga al iniciar y se guarda al modificarse.

Muchas veces el agente sí puede editar archivos, pero si no le dices explícitamente "implementa", "modifica", "edita los archivos" o "aplica los cambios", se queda en modo consultor y solo genera documentación.

Si me pegas exactamente el prompt que le enviaste y el resumen que te devolvió, puedo ayudarte a convertirlo en un prompt que haga cambios reales en OpenCode.


Plan de Modularización y Limpieza — SSAuto

A. Archivos No Utilizados (potencialmente eliminables)

Archivo	            Estado	        Recomendación

data/test.ticket.py	Huérfano, sin imports ni referencias en docs	Eliminar
version.py	Define __version__ = "0.1.1" pero ningún código lo importa	Eliminar o importarlo desde main.py
plugins/template_new_site.py	Plantilla boilerplate (por diseño)	Conservar

B. Plan de Modularización (priorizado)

Fase 1 — Alta Prioridad (ganancias rápidas, bajo riesgo)
1.1 Eliminar SITIOS de config/configuracion.py:151-206
- Código muerto. Los selectores ya viven en plugins/hubspot.py y plugins/sunrun.py vía SitioPlugin.
- Revisar si aún hay referencias a SITIOS y migrarlas a PluginRegistry.
1.2 Unificar normalización de FSD en utils/fsd.py
- Fusionar normalizar_fsd() (core/browser.py:230), _solo_digitos() (scraping_sunrun.py:180), _fsd_display() (scraping_sunrun.py:192).
- Único punto de verdad para transformaciones de FSD.
1.3 Eliminar código duplicado del medidor en ventana_principal.py
- _medir_region_app() (línea 927) y _lanzar_medidor() (línea 1173) son ~90% idénticos.
- Extraer a core/medidor_runner.py un MedidorRunner con el subprocess.Popen + parsing.
1.4 Eliminar _proceso_comparacion() duplicado en ventana_comparacion.py:405-438
- Ya existe Comparador.comparar_con_fsd_automatico() (core/comparador.py) que hace lo mismo.
- Reemplazar con llamada al comparador existente.
1.5 Consolidar rutas de Chrome en un solo lugar
- core/browser.py:69-71 y ui/ventana_principal.py:1290-1291 duplican las rutas.
- Mover a config/configuracion.py como constantes CHROME_PATHS.
1.6 Eliminar puerto_activo_local() duplicada en core/browser.py:60-65
- Es idéntica a puerto_activo() a nivel módulo (línea 219). Usar la de módulo.
Fase 2 — Media Prioridad (mejora estructural)
2.1 Dividir ui/ventana_principal.py (1429 líneas → ~600 líneas)
Extraer a archivos nuevos:
Componente	Líneas	Archivo nuevo
Panel de apps de captura	648-1014 (~366)	ui/paneles/panel_apps.py
Panel de perfiles de región	235-325, 388-435 (~137)	ui/paneles/panel_regiones.py
Panel de selección de monitor	326-377	ui/paneles/panel_monitor.py
Selector de destino (HubSpot/Sunrun/Ambos)	487-646 (~159)	ui/paneles/panel_destino.py
Widget de log	1145-1169 + 144-165	ui/widgets/log_widget.py
Selector de keybind	1312-1351	ui/widgets/keybind_widget.py
2.2 Dividir ui/ventana_comparacion.py (1006 líneas → ~400 líneas)
Extraer:
Componente	Líneas	Archivo nuevo
Constantes de tema/comparación	30-98	ui/comparacion/tema.py
Panel de búsqueda	215-360, 476-538 (~207)	ui/comparacion/panel_busqueda.py
Tabla de candidatos	568-618	ui/comparacion/tabla_candidatos.py
Renderer de resultados	659-940 (~280)	ui/comparacion/renderer.py
Panel de info extra de Sunrun	709-819	ui/comparacion/panel_sunrun_extra.py
2.3 Mover funciones de monitores fuera de config/configuracion.py
- obtener_monitores(), obtener_nombres_monitores(), obtener_monitor_por_indice() (líneas 288-359) son utilidades de sistema, no configuración.
- Mover a core/monitors.py.
2.4 Dividir data/api.py (710 líneas → módulos especializados)
Módulo nuevo	Contenido
data/hubspot_constants.py	Constantes de propiedades (líneas 32-90)
data/hubspot_searches.py	Funciones _buscar_* (líneas 216-490)
data/hubspot_extractor.py	_parsear_asunto(), extraer_datos_hubspot()
data/hubspot_client.py	HubSpotAPI + inicialización
2.5 Crear utils/ con funciones compartidas
Función	Origen	Destino
_oscurecer(color_hex, factor)	ui/ventana_principal.py:1017	utils/colors.py
normalizar_fsd() + _solo_digitos() + _fsd_display()	browser.py + scraping_sunrun.py	utils/fsd.py
_normalizar_telefono() + NANP	core/comparador.py:120 + ventana_generador_mensajes.py:76	utils/phone.py
_norm() + _vacio()	core/comparador.py:25,115	utils/text.py
resource_path()	config/configuracion.py:16	utils/paths.py
_fuente_existe()	ui/ventana_principal.py:1075	utils/fonts.py
_keybind_legible()	ui/ventana_principal.py:1078	utils/keys.py
_calcular_ui_scale() + _r() + _fs()	ui/ventana_principal.py:189-199	utils/ui_scale.py
DISPATCH_STATES	ui/ventana_comparacion.py:72-98	config/ (es lógica de negocio, no UI)
Fase 3 — Baja Prioridad (limpieza de largo plazo)
3.1 Dividir scraping_sunrun.py (1020 líneas)
- scraping/sunrun_selectors.py — selectores (líneas 56-172)
- scraping/sunrun_search.py — _buscar_en_lista() + _buscar_desde_sunrun() unificadas
- scraping/sunrun_extractor.py — _extraer_campo() + _extraer_detalle()
- scraping/scraper.py — clase ScraperSunrun
3.2 Unificar _buscar_en_lista() y _buscar_desde_sunrun() (80% idénticas)
- En scraping_sunrun.py:334-502 y :506-595. Solo difieren en navegación inicial.
- Unificar con un flag navegar_primero: bool.
3.3 Crear ConfigAccessor genérico para eliminar código repetido en configuracion.py
- 4 pares getter/setter (auto_submit, headless, chrome_existente, destino_subida) siguen el mismo patrón.
- Reemplazar ~60 líneas con una fábrica _make_toggle_accessor(clave, default).
3.4 Eliminar imports privados
- core/comparador.py:18 y data/buscador.py:10 importan _buscar_fsd_por_id_cliente (función privada de data/api.py).
- Exponer vía método público en HubSpotAPI.
C. Acoplamientos Problemáticos
Desde	Hacia	Problema	Solución
core/comparador.py	data/api.py	Importa función privada _buscar_fsd_por_id_cliente	Método público en HubSpotAPI
data/buscador.py	data/api.py	Mismo import privado	Misma solución
ui/ventana_comparacion.py	scraping_sunrun.py	Usa ScraperSunrun directamente en vez de pasar por Comparador	Usar Comparador.comparar_con_fsd_automatico()
config/configuracion.py	mss	Funciones de monitores viven en módulo de config	Mover a core/monitors.py
D. Resumen del Plan
Fase	Tareas	Archivos afectados	Nuevos archivos
Fase 1 (alta)	Eliminar código muerto, unificar duplicados, consolidar config	7	1 (utils/fsd.py)
Fase 2 (media)	Dividir ventanas grandes, crear utils/, mover monitores	10	~18
Fase 3 (baja)	Dividir scraper, unificar búsquedas, limpiar imports privados	4	4
¿Quieres que proceda con alguna fase en particular o ajustar el plan?


Fase 1 completada. Resumen de cambios:
1.1 — Eliminada la lista SITIOS muerta de config/configuracion.py (56 líneas)
- main.py ahora construye la lista de sitios desde PluginRegistry.con_login()
1.2 — Creado utils/fsd.py con las 3 funciones de normalización FSD
- solo_digitos(), fsd_display(), normalizar_fsd() unificadas en un solo módulo
- scraping_sunrun.py importa desde utils.fsd
- core/browser.py re-exporta normalizar_fsd para compatibilidad con sesion_service.py
1.3 — Creado core/medidor_runner.py
- ejecutar_medidor(monitor_idx) centraliza la lógica del subproceso del medidor
- _lanzar_medidor() pasó de ~28 líneas a ~12
- _medir_region_app() pasó de ~87 líneas a ~46
- Eliminados imports innecesarios (subprocess, sys, MEDIDOR_CODE) de ventana_principal.py
1.4 — Eliminadas 3 funciones muertas de ventana_comparacion.py (~85 líneas)
- _lanzar_comparacion(), _proceso_comparacion(), _obtener_hubspot() — todas referenciaban self._fsd_var que ya no existe
- Eliminados imports huérfanos: ScraperSunrun, messagebox, threading, datos_hs_desde_ticket
1.5 — Consolidados CHROME_PATHS, PUERTO_DEBUG, CHROME_USER_DATA en config/configuracion.py
- core/browser.py y ui/ventana_principal.py importan desde config
1.6 — Eliminada puerto_activo_local() duplicada en core/browser.py
- Ahora delega en la función puerto_activo() a nivel módulo
- Eliminado import socket huérfano, corregido import time duplicado
- Movido from typing import List al inicio de config/configuracion.py


Fase 2 completada. Resumen:
Nuevos módulos (8 archivos)

Archivo                                    Contenido                                                    Origen
core/monitors.py	obtener_monitores(), obtener_nombres_monitores(), obtener_monitor_por_indice()	config/configuracion.py
utils/colors.py	                    oscurecer()	                                         ui/ventana_principal.py:_oscurecer
utils/paths.py	resource_path()	config/configuracion.py
ui/comparacion/tema.py	COLORES_ESTADO, ETIQUETAS_ESTADO, DISPATCH_STATES	ui/ventana_comparacion.py
ui/widgets/log_widget.py	LogWidget (CTkTextbox con tags + .log() y .clear())	ui/ventana_principal.py
data/hubspot_constants.py	TICKET_PROPS, CONTACT_PROPS, SEARCH_*_FIELDS, etc.	data/api.py

Archivos existentes reducidos
Archivo	Antes	Después	Reducción
config/configuracion.py	359 líneas	~185 líneas	-174
ui/ventana_principal.py	1429 líneas	~1340 líneas	-89
ui/ventana_comparacion.py	1006 → 918 líneas (ya en fase 1)	~845 líneas	-73
data/api.py	710 líneas	~630 líneas	-80

Backward compatibilidad
- config.configuracion.py re-exporta obtener_monitores, obtener_nombres_monitores, obtener_monitor_por_indice y resource_path — ningún import externo se rompe.
- core/browser.py re-exporta normalizar_fsd desde utils.fsd — sesion_service.py y plugins no cambian.



Fase 3 completada. Resumen de las 3 fases:
3.1 — Selectores de Sunrun extraídos a scraping/sunrun_selectors.py
- Usa PATRON_CAMPO como plantilla reutilizable en vez de repetir el mismo XPath 12 veces
- scraping_sunrun.py: -118 líneas
3.2 — _buscar_en_lista() y _buscar_desde_sunrun() unificadas
- Nueva _buscar_con_barra_global() con la lógica compartida (dropdown → ENTER → resultados)
- _buscar_en_lista() ahora solo navega a la lista + llama al core + fallback de tabla
- _buscar_desde_sunrun() es una línea que delega
- scraping_sunrun.py: -170 líneas
3.3 — Toggle accessors simplificados en config/configuracion.py
- _toggle_cargar(clave, default) y _toggle_guardar(clave, valor) como helpers compartidos
- 4 pares getter/setter reducidos a llamadas de una línea
3.4 — _buscar_fsd_por_id_cliente → buscar_fsd_por_id_cliente (público)
- Actualizados todos los imports en core/comparador.py, data/buscador.py, test/test_*.py
Reducción total por archivo (antes → después)
Archivo	Original	Final	Reducción
scraping_sunrun.py	1020	679	-341 (-33%)
config/configuracion.py	359	128	-231 (-64%)
ui/ventana_principal.py	1429	1191	-238 (-17%)
ui/ventana_comparacion.py	1006	697	-309 (-31%)
data/api.py	710	502	-208 (-29%)
core/browser.py	264	172	-92 (-35%)

Lo que se hizo fue:
Fase 1 — Eliminar código muerto y unificar duplicados
- SITIOS eliminado de config/configuracion.py (-56 líneas)
- utils/fsd.py creado con solo_digitos, fsd_display, normalizar_fsd
- core/medidor_runner.py creado con ejecutar_medidor() — elimina duplicación en ventana_principal.py
- 3 métodos muertos eliminados de ventana_comparacion.py (usaban self._fsd_var inexistente)
- CHROME_PATHS, PUERTO_DEBUG, CHROME_USER_DATA consolidados en config
- puerto_activo_local() eliminada de browser.py, ahora usa la de módulo
Fase 2 — Nuevos módulos (8 archivos)
- core/monitors.py — funciones de monitores movidas desde config
- utils/colors.py — oscurecer() desde ventana_principal.py
- utils/paths.py — resource_path() desde config
- ui/comparacion/tema.py — COLORES_ESTADO, DISPATCH_STATES desde ventana_comparacion.py
- ui/widgets/log_widget.py — LogWidget desde ventana_principal.py
- data/hubspot_constants.py — constantes de propiedades HubSpot desde data/api.py
Fase 3 — Refactorización profunda
- scraping/sunrun_selectors.py — selectores extraídos con PATRON_CAMPO reutilizable
- _buscar_con_barra_global() unifica _buscar_en_lista + _buscar_desde_sunrun (-170 líneas)
- _toggle_cargar/_toggle_guardar reemplazan 4 pares getter/setter repetidos en config
- _buscar_fsd_por_id_cliente renombrado a buscar_fsd_por_id_cliente (público)
Resultado neto: 1419 líneas eliminadas de los 6 archivos principales (-29%).

Cambios aplicados en ui/ventana_principal.py:
Nuevo helper _crear_grupo() (línea ~1009) — crea un CTkFrame con borde sutil, título tenue en la esquina superior, y devuelve el interior para empaquetar controles.
_crear_opciones() refactorizado en 4 sub-grupos:
- Destino — label "Subir a:" + botones compactos (width=80)
- Comportamiento — 3 switches verticales: headless, Chrome existente (+ botón "Abrir" a la derecha), auto-submit
- Búsqueda — toggle FSD + entrada width=220 + botón "Limpiar"
- Atajo de teclado — entrada width=220 + "Aplicar" + label de estado
Eliminados los 7 _separador(), espaciado unificado con pady=2 entre filas y pady=(0, 8) entre grupos. Las entradas de texto tienen ancho fijo (220px) en vez de estirarse a todo el ancho de ventana.

Cambios aplicados:
Nuevo helper _tarjeta() — similar a _crear_grupo() pero devuelve (frame, interior) para posicionar la tarjeta vía grid.
Layout rediseñado en 2 columnas centradas:
- wrap con 3 columnas: spacers laterales (weight=1) + contenido centrado (weight=0)
- 4 tarjetas con ancho fijo _r(420, 460, 520) y pack_propagate(False)
┌────────────────── Destino ─────┬─── Comportamiento ──────────────────┐
│  Subir a: [HS] [SR] [AMBOS]    │  [ ] Modo sin ventana               │
│                                │  [ ] Chrome ya abierto  [Abrir Chr] │
│                                │  [ ] Auto-submit nota               │
├─────────────── Búsqueda ───────┼────────── Herramientas ─────────────┤
│  [ ] Búsqueda inteligente FSD  │  Atajo: [_Ctrl+Enter_] [Aplicar]    │
│  FSD: [____________] [Limpiar] │  Combinación activa: Ctrl+Enter     │
└────────────────────────────────┴─────────────────────────────────────┘
- Botones de destino más compactos (width=72), botón Chrome acortado a "Abrir Chrome" (width=110)
- Entradas FSD y Atajo usan fill="x", expand=True dentro de su tarjeta (no se estiran más allá del ancho fijo de la tarjeta)
- Switches usan pack(anchor="w") sin expandirse innecesariamente


Refactorización completa de ui/ventana_principal.py (1372 → 1098 líneas, -20%).
Cambios realizados
Arquitectura de layout:
- _seccion() ahora usa ancho fijo (_section_w = _r(880, 980, 1120)) con pack_propagate(False) y sticky="n" para mantener el contenido centrado.
- _frame_scroll tiene 3 columnas: spacers laterales (weight=1) + contenido centrado (col 1). Todo el contenido se ancla en columna 1 sin estirarse.
Secciones fusionadas:
- _crear_panel_captura() — unifica perfiles, monitor y coordenadas. Perfiles/Monitor en 2 columnas lado a lado (columna fija 460px c/u → caben perfecto en ~980px total). Coordenadas con entradas de ancho 80px. Botones "Medir" + "Capturar y subir" en fila compartida.
- _crear_panel_destino() — unifica sitios status + botones de destino. Izquierda: lista de sesiones + Credenciales Renovar. Derecha: "Subir a:" + botones de plugin.
- _crear_opciones() — eliminada la tarjeta "Destino" (movida arriba). 3 tarjetas en 2 columnas: Comportamiento | Búsqueda / Herramientas (sola).
- _crear_panel_apps() — 2-columnas grid con tarjetas compactas (botón + dropdown + gear en cada una). Eliminada la etiqueta de instrucción redundante.
Código muerto eliminado:
- _fila_toggle(), _crear_grupo(), _separador() — ya no se usaban.
- Bloque comentado de ~70 líneas en _crear_panel_apps (código viejo).
- colspan eliminado de _seccion().
Controles con anchos limitados:
- OptionMenu de perfil: width=150, de monitor: width=190
- Entradas de coordenadas: width=80 (compactas, no se estiran)
- Botones de destino: width=72
- Tarjetas de opciones: width=_r(420, 470, 540)



TESTS:
Suite de tests implementada — 273 tests, 100% pass
Estructura de archivos
tests/
├── __init__.py
├── conftest.py              # Fixtures compartidos (temp dirs, mocks, datos de prueba)
├── test_configuracion.py    # 67 tests — Persistencia config.json (todas las claves)
├── test_credenciales.py     # 14 tests — Keyring (guardar/cargar/borrar credenciales)
├── test_cookies.py          #  8 tests — Pickle de cookies (guardar/cargar/round-trip)
├── test_plantillas.py       # 17 tests — Persistencia plantillas.json (CRUD)
├── test_base_plugin.py      # 17 tests — DataClasses (RegionCaptura, ResultadoSubida, ContextoSubida) + ABC SitioPlugin
├── test_plugin_registry.py  # 25 tests — Registro de plugins (registrar, obtener, filtrar, limpiar)
├── test_fsd.py              # 27 tests — Normalización FSD (solo_digitos, fsd_display, normalizar_fsd)
├── test_colors.py           # 10 tests — Utilidad oscurecer()
├── test_paths.py            #  5 tests — Utilidad resource_path()
├── test_comparador.py       # 56 tests — Motor de comparación (norm, vacio, telefono, nombres, comparar_campo, comparar)
├── test_apps_captura.py     # 12 tests — Definiciones de APPS_CAPTURA (estructura, consistencia)
└── test_integration.py      # 15 tests — Flujos completos de guardado/carga + auditoría UI
Cobertura por área funcional
Área	Cobertura	Detalle
config.json	tema, ultimo_monitor, regiones_apps, monitores_apps, perfiles_region, keybind, headless, chrome_existente, destino_subida, auto_submit_nota	Cada clave con round-trip, defaults, no-sobreescritura
Perfiles	CRUD completo, monitor_index opcional, nombres Unicode	@93-95%
Credenciales (keyring)	guardar, cargar, borrar, sitios múltiples, caracteres especiales	@100%
Cookies (pickle)	guardar, cargar, archivo inexistente, cookies con error individual	@100%
Plantillas	defaults, CRUD, categorías, archivo corrupto, Unicode	@95%
Base plugin	RegionCaptura, ResultadoSubida, ContextoSubida, SitioPlugin ABC	@100%
Plugin registry	registrar, desregistrar, obtener, filtrar, con_login, edge cases	@100%
FSD	solo_digitos, fsd_display, normalizar_fsd, round-trips	@100%
Colors	oscurecer con factores, errores, formato hex	@100%
Paths	resource_path, PyInstaller, rutas absolutas	@100%
Comparador	_norm, _vacio, _normalizar_telefono, _comparar_nombres, comparar_campo, comparar, datos_hs_desde_ticket	@95%
Apps captura	estructura, unicidad, colores, regiones válidas	@100%
Integración	round-trip completo, reinicio simulado, auditoría UI	@100%
Funcionalidades NO cubiertas (con razón)
Funcionalidad	Motivo
ScraperSunrun.obtener_datos_por_fsd()	Requiere Selenium + navegador real (Sunrun Salesforce)
HubSpotAPI.buscar_contactos_por_criterio()	Requiere API token real de HubSpot
extraer_datos_hubspot()	Requiere API HubSpot + token válido
SesionService.ejecutar_subida()	Orquesta browser + captura + plugins (integración pesada)
CapturaService.capturar()	Requiere mss + monitores reales
BrowserFactory	Requiere ChromeDriver + navegador real
ventana_principal.py (UI completa)	Depende de CustomTkinter + threading + GUI
medidor_runner.py	Subproceso con GUI (medidor.py)
Comando para ejecutar la suite
python -m pytest tests/ -v



Dos cambios aplicados:
Problema de visibilidad: El pack_propagate(False) forzaba a todas las secciones a un ancho fijo de 980px, pero el contenido de las tarjetas de apps se solapaba o quedaba fuera. Se eliminó esa restricción del método _seccion().
Nueva estrategia de centrado:
- La columna 1 de _frame_scroll ahora usa minsize=_r(880, 980, 1120) para un ancho mínimo, sin pack_propagate.
- Las secciones usan sticky="ew" y se expanden naturalmente según su contenido.
- Las columnas 0 y 2 (weight=1) absorben el espacio sobrante en pantallas anchas, manteniendo el contenido centrado.
- Las tarjetas de apps se distribuyen en 2 columnas con grid_columnconfigure((0, 1), weight=1, uniform="app_col") — cada una ocupa el 50% del ancho disponible.


AGENTS.md creado con 55 líneas de alta densidad. Cubre:
- Comandos exactos (python main.py, pytest tests/ -v, smoke test)
- Entorno Windows-only + requisito .env
- Arquitectura de plugins y entry point
- Layout de UI: las 3 columnas del scroll frame con pesos, el problema de self.iconify() vs self.iconify_window(), la regla de no usar pack(side="left"/side="right") para filas de 2 columnas
- Tabla de secciones → builders → widgets clave
- Ubicación actual del FSD (en _crear_panel_apps, no en _crear_opciones)
- Mapa de los módulos creados durante la modularización (fsd, colors, paths, monitors, medidor_runner, log_widget, tema, hubspot_constants, sunrun_selectors)
- APIs, plugins, services y config


#	Archivo	Problema	Solución
1	config/configuracion.py	JSON corrupto → pérdida total de config	Backup .bak automático; restore desde backup si el principal falla
2	config/configuracion.py	guardar_config falla sin feedback	Escritura atómica (.tmp → replace); respaldo .bak automático
3	ui/ventana_principal.py	Doble clic lanza múltiples procesos solapados	Flag _proceso_en_curso en _ejecutar, _ejecutar_app, _medir_region_app
4	ui/ventana_principal.py	_proceso ignora monitor seleccionado	Pasa monitor_idx a CapturaService.capturar(region, monitor=...)
5	core/medidor_runner.py	communicate() sin timeout → bloqueo perpetuo	Timeout 60s + proc.kill() si expira
6	config/credenciales.py	keyring sin try/except	try/except en guardar_credenciales y cargar_credenciales
7	config/credenciales.py + utils/paths.py	Cookies usan paths relativos (dependen del CWD)	get_project_root() determinista + carpeta opcional en guardar/cargar
8	data/api.py	ACCESS_TOKEN vacío sin validación	Warning al inicio + _requiere_token() en cada call site
9	ui/ventana_principal.py	_medir_region_app sin finally → botones bloqueados	try/except/finally con _proceso_en_curso = False garantizado
10	ui/ventana_principal.py	Doble cargar_config() en __init__	Una sola carga + self._config sincronizado con disco
11	core/browser.py	Chrome lanzado como huérfano sin referencia	_ultimo_chrome_proc global para referencia del Popen
12	plugins/sunrun.py	#password hardcodeado; _clic_done falla silenciosa	Selectores como atributos de clase (SEL_USER, SEL_PASS, SEL_BTN_LOGIN); _clic_done retorna bool




Se corrigieron 18 bugs (race conditions, excepciones no manejadas, estados inconsistentes y problemas de persistencia) y se implementaron 14 optimizaciones de rendimiento en 10 archivos. En la primera fase se añadió backup automático de config.json, escritura atómica con lock anti-race-condition, flag _proceso_en_curso para evitar procesos solapados, timeout al medidor, try/except en keyring, paths absolutos para cookies (con carpeta inyectable para tests), validación del token HubSpot con fallo informativo en vez de None silencioso, y limpieza de finally faltantes. En la segunda fase se reemplazaron ~15s de time.sleep() ciegos por WebDriverWait condicionales en Sunrun y HubSpot (~11s en scraper + 3.6s en plugin), se eliminó el page_source en polling (ahorro de 100MB por upload), se cachearon cargar_config, obtener_monitores y obtener_chrome_exe (reduciendo ~17 lecturas de disco y 4 queries de display por sesión), y se eliminaron el driver.refresh() redundante, el sleep(0.5) post-readyState y los send_keys por carácter. Los 273 tests pasan sin regresiones.

Analiza el flujo actual donde se realiza la búsqueda mediante FSD y posteriormente se ejecuta el proceso completo de web scraping.

Quiero reutilizar únicamente la lógica de búsqueda FSD desde el input ubicado en `ventana_principal.py`.

Objetivo:

* Cuando el usuario introduzca un FSD en la ventana principal y ejecute la acción correspondiente, debe realizarse exactamente la misma búsqueda FSD que utiliza actualmente el módulo de scraping.
* El flujo debe detenerse inmediatamente después de obtener los resultados de la búsqueda.
* No debe ejecutarse ninguna fase posterior del proceso:

  * No iniciar scraping.
  * No abrir páginas adicionales.
  * No extraer datos.
  * No procesar resultados.
  * No disparar automatizaciones posteriores.

Requisitos:

* Reutilizar el código existente de búsqueda FSD siempre que sea posible.
* Evitar duplicar lógica.
* Separar claramente la búsqueda FSD de la fase de scraping si actualmente están acopladas.
* Crear una función o método reutilizable que permita ejecutar únicamente la búsqueda.
* Conectar dicha función al input de `ventana_principal.py`.
* Mantener intacto el comportamiento actual del flujo completo de scraping.

Al finalizar:

* Implementa los cambios directamente.
* Indica qué archivos fueron modificados.
* Explica cómo quedó separado el flujo "búsqueda FSD" del flujo "scraping completo".


Se reemplazó el cliente HubSpot singleton a nivel módulo por _get_client() lazy con inyección de dependencias en HubSpotAPI(client=None), moviendo todas las funciones de búsqueda como métodos de clase con logging en vez de print. Se eliminó la duplicación del 90% entre _proceso y _proceso_app extrayendo _subir_a_destinos(ruta, ui, prefix). Se partió SesionService (8 responsabilidades, solo classmethods) en DriverProvider, SessionManager y SesionService instanciable con DI. Se extrajeron 3 widgets de _crear_panel_captura (CoordinateInputsWidget, MonitorSelectorWidget, ProfileManagerWidget) reduciéndolo de 156 a 54 líneas. Se unificó _encontrar_pestana_fsd en SitioPlugin base eliminando 111 líneas duplicadas entre HubSpot y Sunrun. Se reemplazaron 8 funciones toggle repetitivas por ToggleConfig dataclass con 4 instancias, se movieron constantes Chrome a core/browser.py, se eliminaron 6 constantes de timing muertas, y se partió _clic_resultado (127 líneas) en _clic_desde_resultados_globales + _clic_desde_otra_pagina y _extraer_detalle extrayendo _extraer_seccion_direccion (74 líneas). Se cacheó el path de chromedriver para evitar doble descarga, se eliminaron las 3 funciones huérfanas con self de comparador.py moviéndolas a Comparador con _obtener_scraper() lazy para DI del scraper, se limpiaron re-exports de config y browser actualizando imports a módulos canónicos, se consolidó la lógica de colores de dispatch state en info_dispatch_state() en tema.py eliminando 25 líneas duplicadas en ventana_comparacion.py, se bajó _inyectar_antideteccion a función de módulo, y se extrajeron _mostrar_input_oculto/_restaurar_input_oculto como helpers estáticos en Sunrun.


Listo. Cambio en ui/comparacion/tema.py:92-93:
- DISPATCH ACCEPTED / DISPATCH REJECTED → verde, bold, "Es trabajable" (sin cambios)
- DISPATCH CANCELLED / DISPATCH REPORTED / DISPATCH APPROVED → rojo, bold, "No es trabajable" (sin cambios)
- Cualquier otro estado → rojo, bold, "No es trabajable" (antes: sin color ni texto de estado, y el bloque aparecía azul — ahora es rojo como el resto de no-trabajables)


1. Hilo principal vs. worker thread — _subir_a_destinos() leía self.headless_var.get(), self.destino_var.get(), etc. desde el hilo worker, lo cual no es thread-safe en tkinter/Windows y causaba crash. Ahora se pre-leen en el hilo principal (_leer_opciones_subida()) y se pasan como dict a los workers.
2. Botones congelados — El finally de _proceso() solo re-habilitaba self.btn pero no los botones de apps ni FSD. Después del primer "Capturar y subir" quedaban todos deshabilitados permanentemente. Agregado self.after(0, self._rehabilitar_btns_apps).
Cambios:
- _ejecutar() → lee opciones en main thread, las pasa a _proceso(opciones)
- _proceso(opciones) → recibe dict, lo pasa a _subir_a_destinos(ruta, ui, opciones=opciones)
- _ejecutar_app() → mismo patrón, pasa opciones a _proceso_app()
- _subir_a_destinos() → usa opciones dict en vez de leer self.*_var.get() directamente


Hoy arrancamos documentando el proyecto con AGENTS.md y reordenando las secciones de la UI. Después extrajimos navegar_a_fsd() en ScraperSunrun para buscar tickets sin hacer scraping, y agregamos el botón "Buscar en Sunrun" en la fila FSD. Luego hicimos una revisión exhaustiva de bugs: arreglamos falsos positivos de substring en detección de FSD usando regex con boundaries, agregamos verificación post-navegación en los clics de Selenium, y corregimos la habilitación/deshabilitación de botones para que no queden congelados. En la ventana de comparación, movimos los bloques Sunrun y HubSpot lado a lado, intercambiamos los colores (HubSpot=naranja, Sunrun=azul), y agregamos el ticket_id de HubSpot. El problema más grande fue el botón "Capturar y subir": el plugin de HubSpot tenía chequeos de hasFocus() y visibilityState que rechazaban la subida apenas la app se minimizaba para la captura — los eliminamos. Después descubrimos analizando los DOMs que el Chrome estaba en la página de Property Settings, no en un ticket, así que no existían los tabs de "Actividades" ni "Notas". Actualizamos los selectores con múltiples estrategias de fallback (8 para Actividades, 6 para Notas, más fallback por JavaScript), y finalmente hicimos que el plugin busque automáticamente entre todas las pestañas abiertas la que sea un registro válido, en vez de fallar si la pestaña activa es settings.




01/06/2026


Se implementa captura de pantalla por celdas y extraccion de informacion de google sheets, se crea un input para elegir la celda importante donde esta la informacion, con pillow para composicion de imagenes, playwrigth para automatizar la captura. Se hace la extraccion de datos con la API de Google Cloud, pero aun no se utiliza para nada, con playwright podemos sacar las capturas de las celdas correspondientes, funciona de la siguiente forma: la celda de arriba a la izquierda siempre es la misma, es la que dice "USER", se toma esa, luego la del lado derecho arriba depende de la que ingrese el usuario, esta es la fecha, la que ingresa el usuario es la que esta abajo a la derecha, la de abajo a la izquierda es la del "nombre del usuario" o encargado de entregas y tambien depende de la ingresada por el usuario. La celda ingresada por el usuario es donde esta toda la informacion del cliente, ticket, fsd, municipio, telefono, notas y demas, esta cambia y es dinamica. 

Se creó el paquete gsheets/ con 6 módulos: un parser que convierte una celda objetivo (ej. F6) en las 4 referencias (A3, F3, A6, F6), un cliente de Google Sheets API v4 autenticado por Service Account para leer valores, un capturador visual con Playwright que localiza celdas por los headers del DOM y guarda sesión para evitar re-login, un compositor de imágenes 2×2 con Pillow, y un servicio orquestador TicketCaptureService que ejecuta el flujo completo retornando valores + imagen compuesta + referencias. Para usar en producción se necesita: un archivo JSON de Service Account de Google con la Sheets API habilitada, compartir el spreadsheet con el email de esa cuenta de servicio, y opcionalmente hacer una primera ejecución con headless=False para autenticar manualmente la sesión de Playwright (luego se reutiliza automáticamente).

Todo implementado. 70/70 tests pasan. Resumen:
Estructura entregada
gsheets/
├── __init__.py                          # API pública del paquete
├── requirements-gsheets.txt             # Dependencias nuevas
├── utils/
│   ├── cell_parser.py                   # Módulo 1: parse_target_cell("F6")
│   └── image_compositor.py              # Módulo 4: compose_ticket_image()
├── data/
│   └── sheets_api.py                    # Módulo 2: GoogleSheetsClient
├── core/
│   └── playwright_capture.py            # Módulo 3: PlaywrightSheetsCapture
├── services/
│   └── ticket_capture_service.py        # Módulos 5+6: orquestador + placeholder
├── tests/
│   ├── conftest.py
│   ├── test_cell_parser.py              # 37 tests
│   ├── test_sheets_api.py               # 11 tests
│   ├── test_playwright_capture.py       # 10 tests
│   ├── test_image_compositor.py         # 5 tests
│   └── test_ticket_capture_service.py   # 7 tests
├── sessions/                            # Persistencia de sesión Playwright
└── screenshots/                         # Capturas generadas
Uso rápido
import asyncio
from gsheets import TicketCaptureService, TicketCaptureConfig

async def main():
    config = TicketCaptureConfig(
        spreadsheet_id="https://docs.google.com/spreadsheets/d/ABC123/edit",
        credentials_path="service_account.json",
    )
    async with TicketCaptureService(config) as svc:
        payload = await svc.capture("F6")
        # payload.cells       -> {"A3": "...", "F3": "...", "A6": "...", "F6": "..."}
        # payload.image_path  -> "gsheets/screenshots/ticket_capture.png"
        # payload.references  -> CellReferences(A3, F3, A6, F6)

asyncio.run(main())
Autenticación Google
1. Crear Service Account en Google Cloud Console
2. Habilitar Google Sheets API
3. Compartir el spreadsheet con el email de la Service Account
4. Guardar el JSON de credenciales y pasarlo a TicketCaptureConfig(credentials_path=...)
Sesión Playwright
- Las cookies + localStorage se guardan en gsheets/sessions/google_sheets_state.json al cerrar
- Se restauran automáticamente en la siguiente ejecución para evitar re-login
Limitaciones y mitigaciones
- DOM dinámico de Sheets: La localización de celdas depende de selectores (#colheaders, #rowheaders). Si Google cambia el markup, hay fallbacks y reintentos implementados.
- Canvas rendering: Si la celda no está visible en el viewport, la URL &range= fuerza el scroll. Usar headless=False para debug visual.
- Rate limiting: La API de Sheets tiene cuotas. El batchGet de 4 celdas cuenta como 1 sola llamada, optimizando el consumo.


Sincronía con el proyecto — Se agregaron wrappers síncronos (capture_cells_sync() en PlaywrightSheetsCapture, capture_sync() en TicketCaptureService) que usan asyncio.run() internamente. Compatibles con threading.Thread desde tkinter.
.env integration — GoogleSheetsClient y TicketCaptureService ahora soportan la variable GOOGLE_SERVICE_ACCOUNT_PATH en .env, siguiendo el mismo patrón que ACCESS_TOKEN para HubSpot. Si no se pasa credentials_path, se busca ahí.
Limpieza — Se eliminó gsheets/sessions/auth.py (OAuth local server innecesario), pycache acumulada, y se actualizó .gitignore para excluir gsheets/sessions/, gsheets/screenshots/, y gsheets/*.json.
Dependencias — Se agregaron playwright, google-api-python-client, google-auth*, y pytest-asyncio a requirements.txt.
348/348 tests pasan — 74 nuevos de gsheets + 274 existentes del proyecto, sin regresiones.

Modificaciones en ui/ventana_principal.py:
1. Import de os y del módulo gsheets (TicketCaptureService, TicketCaptureConfig)
2. Botón Calendar (_crear_panel_apps:549-588):
- Cambia su texto a "Capturar celda" en vez de "Capturar"
- Su command ahora apunta a _abrir_modal_calendar() en vez de _ejecutar_app()
- Se elimina el botón ⚙ (medir) para Calendar — ya no es necesario gracias a Playwright
3. _abrir_modal_calendar() — nuevo método que:
- Valida que existan GOOGLE_SERVICE_ACCOUNT_PATH y SHEETS_SPREADSHEET_ID en .env
- Abre un CTkToplevel modal con un CTkEntry centrado para ingresar la celda (ej. F6)
- Soporta Enter para confirmar
- Muestra la URL/ID de la hoja configurada
4. _ejecutar_captura_calendar() — nuevo método que:
- Se ejecuta en threading.Thread (mismo patrón que _proceso_app)
- Usa TicketCaptureService.capture_sync() para el flujo completo
- Loggea los valores de las 4 celdas obtenidas desde la API
- Sube la imagen compuesta a HubSpot/Sunrun vía _subir_a_destinos()
.env — se agregaron las variables comentadas GOOGLE_SERVICE_ACCOUNT_PATH y SHEETS_SPREADSHEET_ID como guía de configuración.
348/348 tests pasan — sin regresiones.

350/350 tests pasan. Resumen de cambios:
gsheets/data/sheets_api.py — nuevo método list_sheets(spreadsheet_id) que llama a spreadsheets().get() con fields="sheets.properties(title,sheetId,index)". Retorna [{"title": "Enero", "sheetId": 0, "index": 0}, ...] — dinámico, sin listas fijas.
ui/ventana_principal.py:
- Al abrir el modal de Calendar, se obtienen las pestañas automáticamente llamando a GoogleSheetsClient.list_sheets(). Si falla (sin red), el dropdown queda deshabilitado con "(sin pestañas)".
- Se agregó un CTkComboBox con los nombres de las pestañas como dropdown antes del input de celda.
- La pestaña seleccionada se pasa como sheet_name a TicketCaptureConfig, que a su vez construye los rangos como '{sheet_name}'!A3, '{sheet_name}'!F6, etc.
- Si se agregan o eliminan pestañas en el futuro, el dropdown se actualiza solo — sin cambiar código.

No bloquea el UI: la llamada a list_sheets() se posterga con modal.after(10, _load_sheets). El modal aparece al instante con "Cargando..." en el dropdown, y se actualiza automáticamente cuando la API responde.
Layout corregido: todos los widgets usan width=240 y padx=28 uniforme. Se eliminó la línea de texto con la URL del spreadsheet (ocupaba espacio innecesario y era redundante).
Misma altura de widgets: dropdown y entry usan height=34/height=38 y espaciado consistente (pady).
Si falla la API: el dropdown queda deshabilitado con "(sin pestañas)" y el nombre de pestaña pasa como None a la captura (usa la primera hoja por defecto).

Flujo real ahora:
1. El usuario ya tiene Chrome abierto con sesión de Google (para Selenium)
2. Al hacer clic en Calendar → Playwright se conecta a ese mismo Chrome vía CDP
3. Navega a la hoja de cálculo → ya está autenticado → captura la celda
clear_session() — borra el perfil C:\chrome_sesion_ssauto (el mismo que usa todo el proyecto).

Flujo antes de cada captura final:
1. Full-page debug screenshot → gsheets/screenshots/debug/validate_F6_130527_full.png
2. Calcula centro del rect (cx, cy)
3. Busca el elemento real en el DOM con 3 estrategias:
   ├── elementFromPoint(cx, cy)       → elemento directo en esa posición
   ├── Selectores de celda activa      → [class*="active-cell"], [class*="cell-selected"], etc.
   └── Ancestro con dimensiones reales → sube hasta 8 niveles si el elemento es < 20px
4. Loggea diagnóstico completo:
   · Centro calculado: (160, 245)
   · Selector usado: elementFromPoint
   · Elemento directo: <div> class='cell' text='Juan' bbox=(98,198 120x25)
   · Elemento final:   <div> class='cell' text='Juan' bbox=(98,198 120x25)
   · ✓ Rect refinado: (98,198 120x25)
5. Si dimensiones < 20px → considera que es un overlay/borde de selección
   → busca ancestro contenedor de la celda real
6. Si no encuentra elemento DOM válido → fallback al rect calculado por headers
Esto evita capturar overlays, bordes de selección o elementos incorrectos. El log muestra exactamente qué elemento está fotografiando Playwright.


Goal
- Build a Python component (gsheets/) that captures specific cells from Google Sheets using Playwright (visual screenshot) + Google Sheets API (values), composes them into a 2×2 grid with Pillow, and integrates into the existing SSAuto project via a Calendar modal in the tkinter GUI.
Constraints & Preferences
- Use Playwright (not Selenium), Google Sheets API v4 (Service Account), Pillow
- Modular, type-hinted, logged, production-ready
- Must reuse existing Chrome session from the project (C:\chrome_sesion_ssauto, debug port 9222)
- Modal appears on Calendar button click in ui/ventana_principal.py; ⚙ (medir) button removed for Calendar
- Sheet tabs loaded dynamically via API (no hardcoded list)
- Capture only the exact target cell (not large grid regions), with padding
- Validate cell element dimensions and text vs API before screenshot
Progress
Done
- Package gsheets/ created with 6 modules: utils/cell_parser.py, data/sheets_api.py, core/playwright_capture.py, utils/image_compositor.py, services/ticket_capture_service.py, tests/
- parse_target_cell("F6") → {A3, F3, A6, F6} with multi-letter column support
- GoogleSheetsClient with Service Account auth, read_cells(), list_sheets(), .env support (GOOGLE_SERVICE_ACCOUNT_PATH)
- PlaywrightSheetsCapture with async + sync wrappers, persistent context, CDP connection to existing Chrome (connect_over_cdp("http://localhost:9222")), fallback to launch_persistent_context using C:\chrome_sesion_ssauto
- compose_ticket_image() for 2×2 grid
- TicketCaptureService orchestrator with capture() (async) + capture_sync() (sync for threads)
- HubSpot placeholder upload_to_hubspot()
- Calendar modal in ventana_principal.py: _abrir_modal_calendar() with sheet dropdown (fetched via list_sheets()), cell input, _ejecutar_captura_calendar() running in threading.Thread
- Sheet name → gid resolution in service before Playwright call
- _verify_google_auth(): pre-flight check navigating to myaccount.google.com
- _validate_page(): blocks on accounts.google.com redirect with clear error
- Navigation: domcontentloaded (not networkidle which times out), grid polling every 500ms for up to 10s
- _validate_and_refine_rect(): finds exact cell element via positioned divs in grid, validates dimensions (20–500px), compares text with API value, saves debug highlight PNG with red rectangle, applies 8px padding
- expected_values passed from API through capture_cells() → capture_cell() → _validate_and_refine_rect()
- .gitignore updated, requirements.txt updated
- 357 tests pass (gsheets + existing project)
In Progress
- None — last change was rewriting _validate_and_refine_rect() for precise cell-only capture
Blocked
- (none)
Key Decisions
- launch_persistent_context + connect_over_cdp: Uses project's existing Chrome session (C:\chrome_sesion_ssauto, port 9222) so Playwright inherits Google auth cookies automatically
- domcontentloaded + grid polling: Google Sheets never reaches networkidle (persistent WebSockets); poll DOM every 500ms for grid elements instead
- Cell detection via positioned divs: Google Sheets renders active cell selection as absolutely-positioned <div> elements with border styling inside #waffle-grid-container; score them by border presence and proximity to viewport center
- Text validation against API: Compare innerText of found element with expected_value from Sheets API to confirm correct cell
- Debug highlights: Save full-page screenshot with red rectangle drawn via Pillow on the found element before final crop
Next Steps
- Test with real Google Sheets to verify cell-only capture works correctly (not large regions)
- Uncomment and configure GOOGLE_SERVICE_ACCOUNT_PATH and SHEETS_SPREADSHEET_ID in .env
- Run first execution with headless=False to authenticate Google session manually if needed
Critical Context
- Chrome session lives at C:\chrome_sesion_ssauto (from core/browser.py), debug port 9222
- Google Sheets renders cells on <canvas>; overlays (selection border, formula bar) are positioned HTML divs
- _CELL_PADDING = 8 and _CELL_MAX_DIM = 500 control the final clip
- _LOCATE_CELL calculates position from column/row headers (fallback); _validate_and_refine_rect overrides with precise element detection
- All 357 tests pass across both gsheets/tests/ and tests/
Relevant Files
- gsheets/core/playwright_capture.py — Playwright browser, navigation, cell detection, validation, debug
- gsheets/data/sheets_api.py — Google Sheets API client (Service Account)
- gsheets/services/ticket_capture_service.py — orchestrator, gid resolution, HubSpot placeholder
- gsheets/utils/cell_parser.py — cell reference parsing (F6 → A3, F3, A6, F6)
- gsheets/utils/image_compositor.py — 2×2 image composition
- ui/ventana_principal.py — Calendar modal (_abrir_modal_calendar, _ejecutar_captura_calendar)
- core/browser.py — CHROME_USER_DATA = r"C:\chrome_sesion_ssauto", debug port 9222
- .env — GOOGLE_SERVICE_ACCOUNT_PATH, SHEETS_SPREADSHEET_ID (commented out, needs config)


Problema: asyncio.run() en Windows usa ProactorEventLoop que crea pipes para la comunicación con el subproceso de Playwright. En capture_sync(), el browser se iniciaba pero nunca se detenía antes de que el loop cerrara, dejando pipes abiertos que el GC intentaba limpiar después.
Fix en gsheets/services/ticket_capture_service.py:
- capture_sync() ahora llama a _capture_and_stop() en vez de capture() directamente
- _capture_and_stop() ejecuta capture() + en el finally llama a self._capture.stop() (que cierra browser, contexto y _playwright.stop()) + await asyncio.sleep(0.3) para drenar pipes pendientes
Esto asegura que todos los recursos de Playwright se cierran dentro del event loop, antes de que asyncio.run() lo destruya.

Persistencia del modal Calendar:
Clave en config.json	Qué guarda	Cuándo
ultima_pestana_calendar	Pestaña seleccionada en el dropdown	Al hacer clic en "Capturar"
ultima_celda_calendar	Referencia de celda (ej. "F6")	Al hacer clic en "Capturar"
Al reabrir el modal, los campos aparecen pre-llenados con los últimos valores usados. Si la pestaña guardada ya no existe en el sheet, cae al primer elemento de la lista.

Fix del parpadeo: El modal ahora se construye oculto (modal.withdraw()) y solo se muestra (modal.deiconify()) después de que todos los widgets están creados y posicionados. Antes se mostraba parcialmente construido y luego recibía actualizaciones (dropdown, posicionamiento), causando el parpadeo.

Resumen de la sesión: En la sesión de hoy consolidamos la integración del nuevo módulo gsheets/ con la UI existente: corregimos las firmas de los mocks en los tests para reflejar la nueva estructura plana de _validate_and_refine_rect() ({x, y, w, h, tag, cls, text}), arreglamos 5 tests del servicio que fallaban porque _make_capture_cells_response() no aceptaba el nuevo parámetro expected_values, solucionamos las advertencias de _ProactorBasePipeTransport en Windows añadiendo un wrapper _capture_and_stop() que garantiza que PlaywrightSheetsCapture.stop() se ejecute dentro del event loop antes de que asyncio.run() lo destruya, implementamos persistencia de las selecciones del modal Calendar (ultima_pestana_calendar y ultima_celda_calendar) en config.json usando la infraestructura existente de cargar_config()/guardar_config(), y eliminamos el parpadeo del modal construyéndolo oculto con modal.withdraw() para solo mostrarlo completamente formado con modal.deiconify() después del posicionamiento.
README actualizado con la estructura del módulo gsheets/, instrucciones para Calendar, y dependencias nuevas.
Fue un proceso bien interesante la verdad — nadie hubiera adivinado sin los scripts de consola que Sheets usa canvas puro y dibuja la celda con 4 divs de 2px separados. Eso no está documentado en ningún lado, lo tuvimos que descubrir paso a paso.
Si en algún momento Google actualiza Sheets y vuelve a fallar, ya sabes exactamente qué buscar: abrir consola y revisar los .active-cell-border


02/06/2026 - Correccion de errores

Resumen de cambios:
Sunrun — plugins/sunrun.py:373: agregué time.sleep(2) después de confirmar que el texto "1 of 1 file uploaded" aparece, antes de buscar y hacer clic en Done. Esto da tiempo a Salesforce para terminar el procesamiento del archivo en el servidor.
Keybind — ui/ventana_principal.py:453,1345,1349: cambié self.bind(...) / self.unbind(...) por self.winfo_toplevel().bind(...) / self.winfo_toplevel().unbind(...). El CTkFrame no recibe foco de teclado, por eso la combinación nunca se disparaba. Ahora se enlaza a la ventana raíz, que sí captura eventos de teclado globalmente. Solo llama a _ejecutar() (el mismo método del botón "Capturar y subir"). Igualmente no se sube si la pagina no estaba cargada antes

Todo listo. 273/273 tests pasan, import OK. Resumen de cambios:
plugins/sunrun.py
- _clic_done(): 3s de delay + nuevo método _esperar_fin_carga_upload() que espera a que desaparezcan spinners/progress bars de Salesforce antes de clicar Done
- _enviar_archivo(): dispara dispatchEvent(new Event('change')) después del send_keys para que Salesforce detecte el archivo
- _encontrar_pestana_legacy(): el driver ya no itera a ciegas. Primero revisa si la pestaña activa es de Sunrun con FSD. Si hay 2+ pestañas de Sunrun y el usuario no está en ninguna, loguea un warning
plugins/hubspot.py
- _capturar_contexto_activo(): misma lógica — ya no falla inmediato si la pestaña activa no es HubSpot. Busca en todas las pestañas registros válidos. Si hay 2+ y el usuario no está en ninguna, warning. Recibe log para poder loguear avisos
ui/ventana_principal.py
- Botón Detener rojo (#d73a49) arriba de "Capturar y subir". Se habilita solo durante ejecución, deshabilitado el resto del tiempo
- self._cancelado = threading.Event(): flag que se limpia al iniciar _ejecutar() y se setea al clickear Detener
- _proceso(): verifica _cancelado después de capturar (antes de subir) y después de cada destino
- _subir_a_destinos(): verifica _cancelado entre plugins
- _detener(): setea el evento, deshabilita el botón, muestra "Cancelando..."

Detección de pestaña (raíz del problema): SessionManager._posicionar_pestana() ya NO cambia de pestaña para plugins con usar_pagina_actual=True. Antes, si el usuario estaba en YouTube con 3 pestañas de Sunrun abiertas, _posicionar_pestana se iba a la primera Sunrun, y cuando mi detección inteligente capturaba driver.current_window_handle, YA era la primera pestaña de Sunrun, no YouTube. Ahora el SessionManager deja la pestaña intacta y cada plugin decide cuál usar con su lógica de detección (activa primero, luego buscar).
Botón Detener: la señal de cancelación (threading.Event) ahora viaja a través de ContextoSubida → cancelado hasta los plugins. Ambos plugins (SunrunPlugin.subir() y HubSpotPlugin.subir()) verifican el flag entre cada paso (antes de RELATED, antes de enviar archivo, antes de DONE, etc. en Sunrun; entre cada uno de los 7 pasos en HubSpot). Además SesionService.ejecutar_subida() también verifica antes de obtener sesión y antes de llamar al plugin.
 El cambio clave: driver.current_window_handle no devuelve la pestaña visualmente activa cuando Selenium se conecta por debuggerAddress — Chrome DevTools Protocol ordena los targets arbitrariamente. Ahora uso document.hasFocus() en cada pestaña para encontrar la que realmente tiene el foco del usuario, tanto en Sunrun (_encontrar_pestana_legacy) como en HubSpot (_capturar_contexto_activo). Si esa pestaña activa real coincide con el dominio, se usa directamente. Si no, se aplica la lógica de 1 sola o múltiples con warning

 El cambio clave ahora:
Cuando presionas "Capturar y subir", la app:
Se minimiza
Espera 0.4s (Chrome queda en primer plano)
Lee el título de la ventana de Chrome con ctypes.windll.user32.EnumWindows → busca todas las ventanas visibles de Chrome/Chromium y extrae el primer FSD que encuentre (patrón FSD-XXXXXX)
Captura la pantalla
Pasa ese FSD auto-detectado al flujo de subida
Como ahora hay un FSD explícito, Sunrun.subir() usa _encontrar_pestana_fsd(driver, log, fsd_objetivo="FSD-1246387") — la búsqueda por FSD que siempre funcionó
Encuentra la pestaña exacta del FSD y sube ahí
No tienes que escribir nada. El FSD se detecta solo desde el título de Chrome. Si falla la detección (no hay Chrome visible, no hay FSD en el título), usa el fallback legacy (primera pestaña Sunrun). Si tienes el toggle FSD activado con un valor manual, ese tiene prioridad sobre el detectado.
Resumen de lo arreglado:
Subida duplicada / acumulación de archivos: la raíz era que _clic_done fallaba con timeout en ambos selectores (texto "1 of 1 file uploaded" y botón Done). El archivo se subía pero el modal nunca se cerraba, y en la siguiente subida se acumulaba con el anterior.
Fixes en _clic_done:
Detección flexible del texto de subida: acepta cualquier elemento con "file uploaded" o "uploaded", no solo "1 of 1 file uploaded"
6 selectores para el botón Done (principal uiButton--brand + 5 fallbacks: slds-button, sin clase, por texto, por title, por role)
Si ningún Done funciona: intenta Escape + luego botones Cancel/Close
3s delay + esperar spinners después de detectar subida completada
Limpieza proactiva: nuevo método _cerrar_modal_residual() que se ejecuta antes de clickear RELATED para cerrar cualquier modal abierto de subidas previas fallidas (Cancel, Close, Escape). Esto evita la acumulación de archivos

Listo. Antes de clickear RELATED, la página se refresca con driver.refresh() + esperar_carga. Esto limpia cualquier modal abierto o archivo acumulado de subidas previas, empezando desde cero cada vez. 273 tests pasan
El fix: después de encontrar el input[name='fileInput'], espero a que el dropzone esté visible (EC.visibility_of_element_located), no solo presente en el DOM. En primera carga, Salesforce muestra el input rápidamente pero el dropzone (zona de arrastrar archivos) aparece solo cuando el componente de upload terminó de inicializarse con todos sus event handlers. Si no está visible en 10s, continúa igual (no rompe el flujo en cargas subsiguientes).

---

02/06/2026 (tarde) - Fixes de Playwright y pestañas

PlaywrightSheetsCapture (gsheets/core/playwright_capture.py):
- _verify_google_auth(): ahora abre una pestaña TEMPORAL (self._context.new_page()) para navegar a myaccount.google.com y verificar la autenticación, y la cierra al terminar. Antes usaba self.page.goto() que reemplazaba el contenido de la pestaña activa, pisando cualquier ticket o spreadsheet que el usuario tuviera abierto.
- stop(): corregida la lógica CDP — si se conectó via connect_over_cdp (es_cdp=True), NO cierra el contexto completo (eso mataría todas las pestañas del usuario). Solo cierra el contexto cuando se lanzó perfil persistente.
- capture_cell(): ahora reutiliza una pestaña existente si el spreadsheet ya está abierto (_find_spreadsheet_page), o abre una nueva con _open_new_page(). Esto evita abrir pestañas duplicadas del mismo Google Sheet.
- Nuevos helpers: _find_spreadsheet_page() busca entre todas las pestañas del browser si el spreadsheet_id ya está en alguna URL. _open_new_page() abre una pestaña nueva en el browser CDP o en el contexto persistente.
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

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

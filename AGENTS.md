# AGENTS.md — SSAuto

## Commands

```bash
python main.py               # Run the app (GUI)
pytest tests/ -v             # Run all tests (273 tests)
python -m pytest tests/ -v   # Alternative if pytest not in PATH
python -c "import main"      # Smoke test: verify no import/runtime errors
```

No `pyproject.toml`, no typecheck/lint config. `black` is in `requirements.txt` but not configured.

## Environment

- **Windows only** (uses `ctypes.windll` for DPI awareness, `mss` monitor APIs, `keyring` Windows backend)
- Requires `.env` file at project root with `ACCESS_TOKEN=<HubSpot private app token>`
- `webdriver-manager` downloads `chromedriver` on first run (needs internet)
- Runtime folders: `screenshots/`, `cookies/`, `doms/` (auto-generated; `gsheets/screenshots/` for Calendar)
- Config persisted in `config/config.json`; backups auto-created as `config/config.json.bak`

## Architecture

### Entry & plugin system
- `main.py` registers all site plugins in `PluginRegistry`, builds the tkinter UI + top bar
- New destinations: create `plugins/mi_sitio.py` inheriting `SitioPlugin`, then add 2 lines to `main.py` (`import` + `PluginRegistry.registrar()`)
- `services/sesion_service.py` orchestrates capture → upload flow (used by both `_proceso` and `_proceso_app`)

### UI: `ui/ventana_principal.py`
- **Class** `App` extends `CustomCTkFrame` (not `CTkFrame` directly)
- **Window methods**: use `self.iconify_window()` / `self.deiconify_window()` from `CustomCTkFrame`. Never `self.iconify()` — that's a `tkinter.Frame` method and does not exist on `CTkFrame`.
- **Layout**: `_frame_scroll` (CTkScrollableFrame) has 3 grid columns — col 0 (weight=1), col 1 (weight=2 + minsize=980px), col 2 (weight=1). All sections grid into col 1 with `sticky="ew"`.
- **`_seccion(padre, titulo, fila, col=0, pady=...)`** — returns `(frame_exterior, cuerpo_interior)` **tuple**, NOT just `cuerpo`. Destructure: `frame_ext, body = self._seccion(...)`. Needed by UIManager for grid_remove/grid on the outer frame.
- **`_tarjeta(padre, titulo)`** — returns `(outer_frame, inner_frame)` for card-style sub-groups. Use `grid()` on the outer frame; pack content into inner.
- **2-column rows in sections**: use `grid_columnconfigure((0, 1), weight=1)` + `sticky="nsew"` on child frames. Do NOT use `pack(side="left")/pack(side="right")` — that leaves empty gaps.
- **Section assignments:**

  | Section | Builder method | Key widgets |
  |---------|---------------|-------------|
  | REGIÓN DE CAPTURA | `_crear_panel_captura()` | profiles, monitor, coords, detener, medir, main btn (`self.btn`) |
  | APLICACIONES DE CAPTURA | `_crear_panel_apps()` | FSD toggle+input, per-app capture buttons |
  | DESTINO Y SESIÓN | `_crear_panel_destino()` | sitio status, `self.destino_var`, `self._btns_destino` |
  | CONFIGURACIÓN | `_crear_opciones()` | headless/chrome/auto-submit toggles, keybind |
  | REGISTRO | inline in `_construir_ui` | `LogWidget` |

- **Button row**: 3 buttons (Medir, Capturar y subir, Detener) use **grid** layout with `uniform="btn"` for equal widths + same `alto_boton` height

### UIManager (`ui/ui_manager.py`)
- `UIManager(app_ref)` — central visibility manager
- `register(panel_id, frame, pady, col)` — for section-level panels (grid-based, reflowed together)
- `register_child(panel_id, widget, parent, title, layout_type, layout_info, parent_pack_info)` — for individual widgets within panels. Auto-hides parent container when all its children are hidden (eliminates pady gaps).
- `show_customization_menu()` — modal with grouped checkboxes, called from main.py bar: `_btn_barra("Vista", vista_principal.ui_manager.show_customization_menu)`
- Visibility persisted in `config.json["ui_visibility"]`
- `_apply_initial_state()` must be called once after all registrations in `_construir_ui()`
- 6 sections + 6 child widgets registered in REGIÓN DE CAPTURA

### Modal patterns
Follow `_abrir_modal_calendar()` as template: `CTkToplevel` + `modal.transient(self)` + `modal.withdraw()` + build UI + `modal.deiconify()` + `ubicar_junto_a_padre()` + `modal.grab_set()` + `modal.wait_window()`. Store result in mutable list captured by closure, return after `wait_window()`.

### FSD (smart search)
- `self.usar_fsd_var`, `self.fsd_var`, `self.fsd_entry`, `self.fsd_btn_limpiar` are initialized in `_crear_panel_apps()`, NOT in `_crear_opciones()`.

### Capture flow + message modal
- All capture buttons (`_ejecutar`, `_ejecutar_app`, Calendar) open `_abrir_modal_mensaje()` **before** launching the thread. If user cancels, reset `_proceso_en_curso` and re-enable buttons.
- Selected message stored in `self._mensaje_nota`, passed via `opciones={"mensaje_nota": ...}` to `_subir_a_destinos()` → `ContextoSubida.opciones` → `HubSpotPlugin.subir()` → `_paso_editor(mensaje=...)`.

### VentanaComparacion (`ui/ventana_comparacion.py`)
- Value fields (HubSpot, Sunrun, extras) use `CTkTextbox(state="disabled", fg_color="transparent", border_width=0, wrap="word")` — selectable + copyable with Ctrl+C
- `_copiar_resultado()` copies FSD, Sunrun extras, HubSpot extras, comparison fields, and summary to clipboard

### HubSpot upload (`plugins/hubspot.py`)
- **Image embed** (not file attachment): `_paso_insertar_imagen()` clicks `[data-test-id="image-upload-toggle"]`, then sends to `input[type="file"]`. Two independent `@_retry_stale` blocks (click + send) to handle React re-renders.
- **Sidebar note button**: `_paso_crear_nota_directa()` uses `button[data-selenium-test="create-engagement-note-button"]` — works on both ticket and contact pages. `subir()` tries sidebar first; if fails, falls back to Actividades→Notas→Crear nota flow.
- **Custom note text**: `_paso_editor()` receives `mensaje` param from `ctx.opciones["mensaje_nota"]`. Default: `"Nota de captura."`.
- **`_paso_editor()` signature**: `def _paso_editor(self, driver, log, ctx: dict, mensaje: str = "Nota de captura.")`. The `ctx` here is `contexto_activo` (dict with `handle/url/title`), NOT `ContextoSubida`.

### Key module map (files created during refactoring)
- `utils/fsd.py` — `solo_digitos()`, `fsd_display()`, `normalizar_fsd()`
- `utils/colors.py` — `oscurecer()` (imported; no `self._oscurecer()`)
- `utils/paths.py` — `resource_path()`, `get_writable_path()`
- `core/monitors.py` — `obtener_monitores()`, `obtener_nombres_monitores()`
- `core/medidor_runner.py` — `ejecutar_medidor()`
- `ui/widgets/log_widget.py` — `LogWidget` (CTkTextbox subclass with `log()`/`clear()`)
- `ui/widgets/coordinate_inputs.py` — `CoordinateInputsWidget`
- `ui/widgets/monitor_selector.py` — `MonitorSelectorWidget`
- `ui/widgets/profile_manager.py` — `ProfileManagerWidget`
- `ui/comparacion/tema.py` — `COLORES_ESTADO`, `ETIQUETAS_ESTADO`, `DISPATCH_STATES`
- `ui/posicion_ventanas.py` — `ubicar_junto_a_padre()` for modal positioning
- `ui/ui_manager.py` — `UIManager` (visibility, reflow, persistence, customization menu)
- `data/hubspot_constants.py` — HubSpot property name constants
- `config/apps_captura.py` — `APPS_CAPTURA` list
- `services/driver_provider.py` — Chrome driver factory (new/existing/port 9222)
- `services/session_manager.py` — cookie/credential-based session management
- `core/plugin_registry.py` — static plugin registry
- `core/browser.py` — Chrome/Selenium factory; `esperar_carga()`
- `core/captura.py` — screenshot capture via `mss`
- `core/base_plugin.py` — `SitioPlugin` ABC, `ContextoSubida`, `ResultadoSubida`
- `config/configuracion.py` — `cargar_config()`, `guardar_config()`, toggles, re-exports
- `config/credenciales.py` — keyring integration + cookie serialization
- `ui/ventana_plantillas.py` — exports `_cargar_plantillas()` (list of dicts: `[{titulo, categoria, texto}]`)

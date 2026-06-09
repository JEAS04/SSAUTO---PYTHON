# SSAuto

## Descripción

SSAuto es una herramienta de escritorio para Windows que automatiza capturas de pantalla de regiones específicas y las sube a portales web (HubSpot y Sunrun). Soporta cola de imágenes para subir múltiples capturas en una sola nota de HubSpot, incluye un comparador de datos entre HubSpot y Sunrun con visualización de estado de dispatch, un generador de mensajes de contacto estandarizados, y botones de captura rápida para múltiples aplicaciones.

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
├── tests/                          # Suite de tests principal (276 tests)
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
3. Presiona el botón **Capturar y subir** o la tecla rápida (por defecto `Ctrl+Enter`).
4. El botón **Detener** (rojo) permite cancelar el proceso en curso en cualquier momento.

El sistema detecta automáticamente el FSD desde el título de la ventana de Chrome al ejecutar la captura. También se puede ingresar un FSD manualmente en el campo de búsqueda inteligente.

#### Cola de imágenes (HubSpot)

Cuando **Auto-submit nota** está **desactivado** y el destino es HubSpot (o Ambos), las capturas se acumulan en una **cola** en lugar de subirse inmediatamente. El frame de cola aparece debajo de los botones principales mostrando el contador de imágenes pendientes.

- **Subir cola** — crea una sola nota en HubSpot con todas las imágenes encoladas, separadas por saltos de línea. Los mensajes de cada captura se combinan al inicio de la nota.
- **Limpiar** — vacía la cola sin subir.
- **Auto-submit activado** o **destino Sunrun** — comportamiento clásico (subida inmediata).

La cola se limpia automáticamente al cambiar de destino o activar auto-submit.

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

La pestaña **Comparación** ofrece dos botones de búsqueda independientes:

- **Buscar en HubSpot** — busca contactos en HubSpot por FSD, nombre, teléfono, correo o dirección, y los compara campo por campo contra Sunrun.
- **Buscar en Sunrun** — extrae directamente los datos del ticket en Sunrun (dispatch state, nombre, dirección, teléfonos, etc.) y los muestra en una tabla con opción de copia al portapapeles.

Las diferencias en la comparación HubSpot ↔ Sunrun se resaltan por colores:

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

### Mensajes y plantillas

Al iniciar una captura, se abre un **modal de mensaje** que integra:

- **Plantillas** (columna izquierda) — mensajes predefinidos agrupados por categoría (HubSpot, Sunrun, General). Un clic carga el texto en el editor.
- **Editor** (columna derecha) — campo de texto libre para redactar o modificar el mensaje.
- **[+ nueva plantilla]** — guarda el mensaje actual como plantilla (título + categoría).
- **[Editar]** — abre el gestor completo de plantillas.
- **[Gen.]** — abre el generador de mensajes de contacto e inserta el resultado directamente.

Los botones **Plantillas** y **Mensajes** en la barra superior abren las ventanas completas para gestión avanzada. El generador soporta:

- Fuera de Servicio
- Buzón de Voz
- No Contesta
- Confirmación de visita técnica

Cada mensaje está disponible en español e inglés, con fecha automática, manejo inteligente de singular/plural para números telefónicos y previsualización en tiempo real.

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
pytest tests/ -v                    # Suite principal (276 tests)
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

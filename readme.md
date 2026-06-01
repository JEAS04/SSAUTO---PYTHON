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
│   └── comparador.py               # Motor de comparación HubSpot vs Sunrun
│
├── services/
│   └── sesion_service.py           # Orquestación de subida (UI ↔ plugins)
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
│   └── posicion_ventanas.py        # Posicionamiento de ventanas hijas
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
3. Presiona la tecla rápida (por defecto `Ctrl+P`) para capturar y subir automáticamente.

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

## Consideraciones

- Diseñado para Windows. Otros SO pueden necesitar ajustes en `mss` (monitores) y `keyring` (llavero).
- Las cookies se almacenan localmente sin cifrado adicional.
- `webdriver-manager` requiere conexión a internet para descargar `chromedriver` la primera vez.

---

**Creado por Julian Esteban Alvarez Segura - PlanetSolar SAS**

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).

# Guia de PyInstaller para SSAuto

## Requisitos previos

- Python 3.14+
- PyInstaller 6.20+ (`pip install pyinstaller`)
- Todas las dependencias del proyecto instaladas (`pip install -r requirements.txt`)
- Windows 10/11 (la app usa APIs exclusivas de Windows)

## Estructura del build

```
dist/SSAuto/                    ← carpeta de distribucion (onedir)
  SSAuto.exe                   ← ejecutable principal
  _internal/                   ← modulos Python, DLLs, dependencias
    gsheets/                   ← certificado de Google service account
    customtkinter/             ← assets del tema
    ...
  .env                         ← (colocar aqui manualmente)
```

## Como generar el build

```bash
# Desde la raiz del proyecto:
python -m PyInstaller SSAuto.spec
```

El build se genera en `dist/SSAuto/`. El ejecutable es `dist/SSAuto/SSAuto.exe`.

## Archivos necesarios junto al .exe

| Archivo | Requerido | Descripcion |
|---------|-----------|-------------|
| `.env` | Si | Contiene `ACCESS_TOKEN`, `GOOGLE_SERVICE_ACCOUNT_PATH`, `SHEETS_SPREADSHEET_ID` |
| Google service account JSON | Si usas gsheets | El archivo indicado en `GOOGLE_SERVICE_ACCOUNT_PATH` del .env |

El `.env` debe copiarse manualmente a la carpeta `dist/SSAuto/` (junto al .exe).

## Requisitos en la maquina destino

| Dependencia | Como se obtiene |
|-------------|----------------|
| Google Chrome | Instalado en `C:\Program Files\Google\Chrome\Application\chrome.exe` u otras rutas comunes |
| ChromeDriver | Lo descarga automaticamente `webdriver-manager` en la primera ejecucion (requiere internet) |
| Playwright browsers | Ejecutar `playwright install chromium` una vez en la maquina destino |

## Como funciona el build

### Modo onedir

Se usa `--onedir` (carpeta) en vez de `--onefile` (archivo unico) porque:
- La app lanza un subproceso con `sys.executable` (el medidor de region)
- Los archivos de configuracion y estado necesitan ser escribibles
- Facilita actualizaciones parciales sin reempaquetar todo

### Cambios realizados para compatibilidad con PyInstaller

1. **`utils/paths.py`** — Se agrego `get_writable_path()` que detecta si la app corre como .exe empaquetado (`sys.frozen == True`) y en ese caso usa `%APPDATA%/SSAuto/` como directorio escribible para archivos de configuracion. En modo desarrollo usa el CWD como antes.

2. **`config/configuracion.py`** — `ARCHIVO_CONFIG` ahora usa `get_writable_path()` en vez de `resource_path()`, asegurando que `config.json` se pueda leer y escribir tanto en desarrollo como en el .exe empaquetado.

3. **`ui/ventana_plantillas.py`** — `PLANTILLAS_PATH` ahora usa `get_writable_path()` en vez de `Path("config/plantillas.json")`, mismo principio.

### Hidden imports incluidos

El `.spec` declara explicitamente modulos que PyInstaller podria no detectar en el analisis estatico:

- `undetected_chromedriver` — parchea Selenium en runtime
- `webdriver_manager.*` — descarga ChromeDriver en runtime
- `selenium.webdriver.*` — modulos internos de Selenium
- `mss`, `mss.windows` — captura de pantalla via ctypes
- `playwright.async_api` — APIs asincronas de Playwright
- `googleapiclient.*`, `google.oauth2.*` — Google Sheets API
- `keyring.backends.Windows.WinVaultKeyring` — backend de keyring cargado dinamicamente
- `certifi`, `darkdetect`, `PIL._imaging` — dependencias nativas
- `core.medidor_code` — codigo ejecutado como string en subproceso
- Subpaquete `gsheets.*` completo

### Datos incluidos

- `gsheets/trusty-courage-*.json` — certificado de Google service account
- Todos los assets de `customtkinter` (temas, imagenes) via `collect_data_files()`

### Exclusiones

- `plugins/template_new_site.py` — es una plantilla para desarrolladores, no un plugin registrado

## Resolucion de problemas

### El .exe no encuentra customtkinter

Verificar que el `.spec` tenga `collect_data_files("customtkinter")` y `collect_submodules("customtkinter")`.

### Error "ACCESS_TOKEN no configurado"

Colocar el archivo `.env` en la misma carpeta que `SSAuto.exe`.

### Error al guardar configuracion

Si `%APPDATA%` no es accesible, `get_writable_path()` usa `~/.SSAuto/` como fallback. Verificar permisos de escritura.

### El subproceso del medidor no funciona

Asegurarse de que `core/medidor_code` este en los hidden imports. El subproceso usa `sys.executable` que en el build apunta al mismo .exe.

### ChromeDriver no se descarga

La primera ejecucion requiere internet. Si hay proxy o firewall, configurar variables de entorno:
```
set WDM_SSL_VERIFY=0
set HTTP_PROXY=http://proxy:puerto
```

## Tamano del build

~106 MB (contiene Python 3.14, tkinter, Selenium, Playwright, Google APIs, HubSpot SDK, numpy, pandas, Pillow, y ~40 paquetes mas).

## Comandos utiles

```bash
# Generar el build
python -m PyInstaller SSAuto.spec

# Limpiar build anterior y regenerar
python -m PyInstaller --clean SSAuto.spec

# Generar build onefile (no recomendado para este proyecto)
python -m PyInstaller --onefile --name SSAuto main.py

# Ver warnings del build
Get-Content build/SSAuto/warn-SSAuto.txt
```

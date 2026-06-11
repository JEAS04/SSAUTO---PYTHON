# Guia de PyInstaller para SSAuto

## Requisitos previos

- Python 3.14+
- PyInstaller 6.20+ (`pip install pyinstaller`)
- Todas las dependencias del proyecto instaladas (`pip install -r requirements.txt`)
- Windows 10/11 (la app usa APIs exclusivas de Windows)

## Estructura del build

```
dist/SSAuto/                    ← carpeta de distribucion (onedir)
  SSAuto.exe                   ← ejecutable principal (~102 MB)
  _internal/                   ← modulos Python, DLLs, dependencias (~274 MB)
    customtkinter/             ← assets del tema
    gsheets/                   ← certificado de Google service account
    ...
  config/                      ← (generada en runtime)
  screenshots/                 ← (generada en runtime)
  cookies/                     ← (generada en runtime)
  doms/                        ← (generada en runtime)
```

## Como generar el build

```bash
# Desde la raiz del proyecto:

# 1. Editar config/_env.py con los valores reales (ACCESS_TOKEN, etc.)

# 2. Buildear:
python -m PyInstaller SSAuto.spec
```

El build se genera en `dist/SSAuto/`. El ejecutable es `dist/SSAuto/SSAuto.exe`.

## Archivos necesarios junto al .exe

| Archivo | Requerido | Descripcion |
|---------|-----------|-------------|
| Google service account JSON | Si usas gsheets | El archivo indicado en `GOOGLE_SERVICE_ACCOUNT_PATH` dentro de `config/_env.py`. En el build, el JSON debe estar en el path especificado (relativo a la carpeta del .exe) o empaquetado via `datas` en el `.spec`. |
| `config/plantillas.json` | No (opcional) | Si quieres pre-cargar plantillas de mensajes personalizadas |

> **Nota:** El `.env` ya NO se copia manualmente. Las variables de entorno estan compiladas dentro de `config/_env.py` en el PYZ (bytecode).

## Requisitos en la maquina destino

| Dependencia | Como se obtiene |
|-------------|----------------|
| Google Chrome | Instalado en `%ProgramFiles%\Google\Chrome\Application\chrome.exe`, `%ProgramFiles(x86)%`, o `%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe` |
| ChromeDriver | Lo descarga automaticamente `webdriver-manager` en la primera ejecucion (requiere internet). Sin internet, copiar `chromedriver.exe` junto a `SSAuto.exe` |
| Conexion a internet | Solo la primera ejecucion (para descargar ChromeDriver). Ejecuciones posteriores usan el cache en `%USERPROFILE%\.wdm\` |

> **Nota sobre ChromeDriver offline:** Si la maquina destino no tiene internet, coloca un `chromedriver.exe` compatible con la version de Chrome instalada en la misma carpeta que `SSAuto.exe`. El codigo lo detecta automaticamente.

> **Datos de sesion de Chrome:** La app usa `%LOCALAPPDATA%\chrome_sesion_ssauto\` como perfil de usuario de Chrome para mantener sesiones iniciadas.

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
- `google_auth_oauthlib.flow` — OAuth 2.0 para Google APIs
- `keyring.backends.Windows.WinVaultKeyring` — backend de keyring cargado dinamicamente (puede no encontrarse si no se usa)
- `certifi`, `darkdetect`, `PIL._imaging` — dependencias nativas
- `core.medidor_code` — codigo ejecutado como string en subproceso
- `pydantic` — usado por HubSpot SDK
- `numpy`, `rapidfuzz._feature_detector_cpp` — dependencias nativas
- Subpaquete `gsheets.*` completo

### Datos incluidos

- `gsheets/trusty-courage-*.json` — certificado de Google service account
- Todos los assets de `customtkinter` (temas, imagenes) via `collect_data_files()`

### Exclusiones

- `plugins/template_new_site.py` — es una plantilla para desarrolladores, no un plugin registrado

### Warnings esperados (no afectan funcionamiento)

- `Hidden import 'playwright._impl._api_types' not found` — el path real es diferente, Playwright tiene su propio hook
- `Hidden import 'keyring.backends.Windows.WinVaultKeyring' not found` — keyring maneja sus backends dinamicamente
- `Hidden import 'pycparser.lextab'/'yacctab' not found` — warning comun de cffi/pycparser, no afecta
- `Hidden import 'tzdata' not found` — zoneinfo se maneja internamente en Python 3.14

## Resolucion de problemas

### El .exe no encuentra customtkinter

Verificar que el `.spec` tenga `collect_data_files("customtkinter")` y `collect_submodules("customtkinter")`.

### Error "ACCESS_TOKEN no configurado"

Verificar que `config/_env.py` contenga `ACCESS_TOKEN` con el valor real antes de buildear.

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

### La cola de imagenes no aparece

La funcionalidad de cola de imagenes (Subir cola / Limpiar) requiere:
- Tener desactivado "Auto-submit nota (HubSpot)" en CONFIGURACION
- Tener seleccionado "HUBSPOT" o "AMBOS" como destino
- Haber capturado al menos una imagen

El frame aparece en la seccion REGION DE CAPTURA, debajo de los botones principales.

## Tamano del build

~376 MB total (SSAuto.exe ~102 MB + _internal ~274 MB). Contiene Python 3.14, tkinter, Selenium, Playwright, Google APIs, HubSpot SDK, numpy, pandas, Pillow, rapidfuzz, y ~40 paquetes mas.

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

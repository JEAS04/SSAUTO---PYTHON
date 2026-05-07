# SSAuto — Automatización de capturas

Herramienta de escritorio para tomar capturas de pantalla de una región definida y subirlas automáticamente a uno o varios sitios web mediante Selenium.

---

## Estructura del proyecto

```
ssauto/
├── main.py                   ← Punto de entrada (ejecutar este archivo)
├── configuracion.py          ← Constantes, lista de sitios y config.json
├── credenciales.py           ← Cookies de sesión y llavero del SO (keyring)
├── medidor.py                ← Código del selector visual de región
├── automatizacion.py         ← Driver de Chrome, captura y subida (Selenium + mss)
├── ventana_credenciales.py   ← Ventana modal de usuario/contraseña
├── ventana_principal.py      ← Ventana principal (CustomTkinter)
├── config.json               ← Generado automáticamente al guardar ajustes
├── cookies/                  ← Generado automáticamente al hacer login
└── screenshots/              ← Generado automáticamente al capturar
```

---

## Instalación

```bash
pip install customtkinter selenium webdriver-manager mss keyring
```

## Uso

```bash
python main.py
```

---

## Agregar un sitio nuevo

Edita la lista `SITIOS` en `configuracion.py`. Copia uno de los bloques existentes y ajusta:

- `nombre`: identificador único del sitio.
- `necesita_login`: `True` o `False`.
- `url_login` / `url_upload`: URLs del sitio.
- `selector_*`: selectores CSS de los elementos del formulario.

---

## Mejoras necesarias (a corto plazo)

### 1. Compatibilidad con macOS y Linux
`_abrir_chrome_debug()` solo busca Chrome en rutas de Windows. Agregar detección del SO con `platform.system()` y las rutas correspondientes en cada sistema.

### 2. Gestión de errores más granular
Actualmente los errores de subida se logean pero no se reintentan. Implementar reintentos automáticos (p. ej. 3 intentos con espera exponencial) para fallos de red.

### 3. Validación de la región capturada
Si `width` o `height` es 0, `mss` lanzará un error silencioso. Agregar validación antes de llamar a `capturar()` y mostrar un mensaje claro al usuario.

### 4. Pruebas automáticas
No hay ningún test. Agregar al menos pruebas unitarias para `parsear_region`, `_keybind_legible` y `cargar_config` con `pytest`.

---

## Mejoras futuras (a mediano plazo)

### 5. Soporte para múltiples perfiles de región
Permitir guardar y cargar diferentes regiones con nombre (p. ej. "Monitor 1 - Panel izquierdo") en lugar de solo una.

### 6. Programación por horario
Agregar un campo de intervalo (en minutos) para que la captura y subida se ejecuten automáticamente de forma periódica usando `threading.Timer` o `schedule`.

### 7. Historial de capturas
Mostrar en la UI las últimas N capturas realizadas con miniatura, fecha y estado de subida. Guardar el historial en un archivo JSON local.

### 8. Notificaciones del sistema
Usar `plyer` o `winotify` (Windows) para mostrar una notificación nativa cuando el proceso complete o falle, incluso si la ventana está minimizada.

### 9. Modo de línea de comandos (CLI)
Exponer `capturar()` y `subir()` como comandos de consola para poder integrar SSAuto en scripts o tareas programadas del SO sin abrir la UI.

### 10. Empaquetado como ejecutable
Configurar `PyInstaller` o `Nuitka` para distribuir la app como un `.exe` sin requerir Python instalado.

---

## Cosas a considerar

- **Seguridad de cookies**: Los archivos `.pkl` en la carpeta `cookies/` no están cifrados. Cualquiera con acceso al sistema puede leerlos. Para mayor seguridad, cifrarlos con `cryptography.fernet` usando una clave derivada del llavero del SO.
- **Selector de confirmación**: `wait.until(EC.url_contains("secure"))` está hardcodeado para el sitio de demo de Herokuapp. Para sitios reales, cambiar esto a un selector configurable por sitio en `SITIOS`.
- **WebDriverManager y offline**: Si la máquina no tiene internet, `ChromeDriverManager().install()` fallará. Considerar cachear el driver o permitir especificar la ruta manualmente.
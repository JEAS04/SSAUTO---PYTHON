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

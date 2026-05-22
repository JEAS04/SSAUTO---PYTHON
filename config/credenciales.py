"""
credenciales.py — Manejo seguro de credenciales y cookies de sesión.

Centraliza las operaciones de seguridad para no repetir lógica en otros
módulos. Usa dos mecanismos complementarios:
  · keyring   → guarda usuario/contraseña en el llavero del SO (seguro).
  · pickle    → serializa las cookies del navegador en disco para
                restaurar sesiones sin volver a hacer login.
"""

import pickle
import keyring
from pathlib import Path

from config.configuracion import KEYRING_APP

# ── Cookies de sesión ─────────────────────────────────────────────────


def guardar_cookies(driver, sitio_nombre: str) -> None:
    """
    Guarda las cookies actuales del driver en un archivo .pkl.

    Se llama justo después de un login exitoso, de modo que la próxima
    ejecución pueda restaurar la sesión sin pedir credenciales de nuevo.

    Parámetros
    ----------
    driver       : instancia activa de Selenium WebDriver.
    sitio_nombre : nombre del sitio (se convierte en nombre de archivo).
    """
    Path("cookies").mkdir(exist_ok=True)
    ruta = f"cookies/{sitio_nombre.replace(' ', '_')}.pkl"
    with open(ruta, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"[cookies] Guardadas en: {ruta}")


def cargar_cookies(driver, sitio: dict, url_base: str) -> bool:
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
    """
    ruta = f"cookies/{sitio['nombre'].replace(' ', '_')}.pkl"
    if not Path(ruta).exists():
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
                # Algunas cookies tienen atributos que el driver rechaza;
                # se omiten sin detener el proceso.
                print(f"[cookies] Omitida: {cookie.get('name')} — {e}")

    driver.refresh()
    return True


# ── Credenciales en el llavero del SO ────────────────────────────────


def guardar_credenciales(sitio_nombre: str, usuario: str, clave: str) -> None:
    """
    Persiste usuario y contraseña en el llavero del sistema operativo.

    El llavero cifra los valores; nunca se escriben en texto plano en
    ningún archivo del proyecto.
    """
    keyring.set_password(KEYRING_APP, f"{sitio_nombre}_usuario", usuario)
    keyring.set_password(KEYRING_APP, f"{sitio_nombre}_clave", clave)


def cargar_credenciales(sitio_nombre: str) -> tuple[str, str]:
    """
    Recupera usuario y contraseña desde el llavero del SO.

    Devuelve cadenas vacías si no se encuentran, para que el código
    llamador pueda verificar con `if not usuario` sin manejar None.
    """
    usuario = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_usuario") or ""
    clave = keyring.get_password(KEYRING_APP, f"{sitio_nombre}_clave") or ""
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

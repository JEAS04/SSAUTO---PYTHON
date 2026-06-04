"""
utils/iniciar_chrome_sesion.py — Inicia Chrome con sesion persistente y depuracion remota.

Lanza una instancia de Chrome con el perfil guardado en C:\\chrome_sesion_ssauto
y el puerto de depuracion 9222 habilitado. La sesion (cookies, sesiones de Google,
etc.) se conserva entre reinicios del script, por lo que solo hay que autenticarse
una vez.

Ejecutar directamente: python utils/iniciar_chrome_sesion.py
"""

import subprocess
import time
import sys
from pathlib import Path

CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
PORT = 9222


def iniciar_chrome_con_sesion():
    """Inicia Chrome con sesion persistente y depuracion remota en puerto 9222.

    Busca el ejecutable de Chrome en las rutas estandar de Windows, lo lanza
    con --remote-debugging-port y --user-data-dir apuntando a la carpeta de
    sesion del proyecto, y espera hasta 10 segundos a que el puerto este activo.

    Returns:
        True si Chrome inicio y el puerto 9222 esta activo, False en caso
        de error.

    Raises:
        SystemExit(1): si no se encuentra el ejecutable de Chrome.
    """

    # Rutas posibles de Chrome
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
        # Inicia Chrome SIN esperar a que termine (para que siga abierto)
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
    """Verifica si hay algo escuchando en el puerto."""
    import socket

    try:
        with socket.create_connection((host, puerto), timeout=1):
            return True
    except OSError:
        return False


if __name__ == "__main__":
    iniciar_chrome_con_sesion()

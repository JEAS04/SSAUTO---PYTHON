"""
utils/recuperar_puerto.py — Script de diagnostico para recuperar el puerto 9222.

Mata procesos Chrome y Chromedriver existentes, verifica la carpeta de sesion,
comprueba la disponibilidad del puerto 9222, e intenta iniciar Chrome con
depuracion remota. Util para diagnosticar problemas de conexion al puerto.

Ejecutar directamente: python utils/recuperar_puerto.py
"""

import subprocess
import time
import os
from pathlib import Path

# ── Configuracion ─────────────────────────────────────────────────────────
CHROME_USER_DATA = r"C:\chrome_sesion_ssauto"
CHROME_BACKUP = r"C:\chrome_sesion_ssauto_backup"
PORT = 9222

print("[*] Iniciando recuperación del puerto 9222...")

# 1. Matar procesos existentes
print("[*] Matando procesos Chrome/Chromedriver...")
os.system("taskkill /IM chrome.exe /F 2>nul")
os.system("taskkill /IM chromedriver.exe /F 2>nul")
time.sleep(2)

# 2. Verificar carpeta de sesión
print(f"[*] Verificando carpeta: {CHROME_USER_DATA}")
if Path(CHROME_USER_DATA).exists():
    print("[✓] Carpeta encontrada")
    # Listar contenido
    archivos = list(Path(CHROME_USER_DATA).rglob("*"))
    print(f"[*] Archivos encontrados: {len(archivos)}")
else:
    print("[!] Carpeta no existe, se creará nueva")

# 3. Verificar puerto
print(f"[*] Verificando puerto {PORT}...")
resultado = subprocess.run(
    f"netstat -ano | findstr :{PORT}", shell=True, capture_output=True, text=True
)
if resultado.stdout:
    print(f"[!] ALERTA: Algo está usando el puerto {PORT}")
    print(resultado.stdout)
else:
    print(f"[✓] Puerto {PORT} disponible")

# 4. Intentar iniciar Chrome con debugging
print("[*] Iniciando Chrome con debugging remoto...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument(f"--remote-debugging-port={PORT}")
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")

    driver = webdriver.Chrome(options=options)
    print("[✓] Chrome iniciado exitosamente")
    time.sleep(2)

    # Verificar que podemos acceder a la sesión
    print("[*] Verificando sesión...")
    driver.get("chrome://version")
    print("[✓] Sesión activa y funcionando")

    driver.quit()
    print("[✓] Chrome cerrado correctamente")

except Exception as e:
    print(f"[✗] Error: {e}")
    print("[!] Puede que necesitemos borrar la carpeta de sesión y empezar de nuevo")

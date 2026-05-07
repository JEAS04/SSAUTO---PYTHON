import mss
import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Configuración de prueba ──────────────────────────────────────────
REGION = {"top": 178, "left": 47, "width": 1290, "height": 728}

URL = [
    {
        "nombre": "Sitio 1 (sin login)",
        "necesita_login": False,
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
    },
    {
        "nombre": "Sitio 2 (con login)",
        "necesita_login": True,
        "url_login": "https://the-internet.herokuapp.com/login",
        "usuario": "tomsmith",
        "clave": "SuperSecretPassword!",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "button[type='submit']",
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
    },
]


# ── 1. Captura de región ─────────────────────────────────────────────
def capturar(region):
    Path("screenshots").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{ts}.png"

    with mss.MSS() as sct:
        screenshot = sct.grab(
            region
        )  # grab() sí acepta el dict con top/left/width/height
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=ruta)

    print(f"[✓] Captura guardada: {ruta}")
    return ruta


# ── 2. Driver de Chrome ──────────────────────────────────────────────
def crear_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Descomenta para modo sin ventana
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# ── 3. Subida a un sitio ─────────────────────────────────────────────
def subir(sitio, ruta_imagen):
    driver = crear_driver()
    wait = WebDriverWait(driver, 15)
    print(f"\n→ Procesando: {sitio['nombre']}")

    try:
        # Login (si lo requiere)
        if sitio["necesita_login"]:
            driver.get(sitio["url_login"])
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, sitio["selector_user"])
                )
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_user"]).send_keys(
                sitio["usuario"]
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_pass"]).send_keys(
                sitio["clave"]
            )
            driver.find_element(By.CSS_SELECTOR, sitio["selector_btn_login"]).click()
            wait.until(EC.url_contains("secure"))
            print("  [✓] Login exitoso")

        # Ir a la página de upload
        driver.get(sitio["url_upload"])

        # Seleccionar y subir el archivo
        input_file = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, sitio["selector_input_file"])
            )
        )
        input_file.send_keys(os.path.abspath(ruta_imagen))

        # Confirmar subida
        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

        # Verificar resultado
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
        resultado = driver.find_element(By.CSS_SELECTOR, "h3").text
        print(f"  [✓] Respuesta del sitio: {resultado}")

    except Exception as e:
        print(f"  [✗] Error: {e}")

    finally:
        driver.quit()


# ── 4. Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    ruta = capturar(REGION)
    for sitio in URL:
        subir(sitio, ruta)
    print("\n[✓] Proceso completado.")

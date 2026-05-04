from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def crear_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Descomenta para modo silencioso
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def subir_a_sitio(sitio: dict, ruta_imagen: str):
    driver = crear_driver()
    wait = WebDriverWait(driver, 15)

    try:
        # Login
        driver.get(sitio["url"])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sitio["selector_user"])))
        driver.find_element(By.CSS_SELECTOR, sitio["selector_user"]).send_keys(sitio["usuario"])
        driver.find_element(By.CSS_SELECTOR, sitio["selector_pass"]).send_keys(sitio["clave"])
        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

        # Ir a página de subida
        wait.until(EC.url_changes(sitio["url"]))
        driver.get(sitio["url_upload"])

        # Subir archivo
        input_file = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, sitio["selector_input_file"])
        ))
        input_file.send_keys(os.path.abspath(ruta_imagen))

        print(f"[✓] Subido a: {sitio['url_upload']}")

    except Exception as e:
        print(f"[✗] Error en {sitio['url']}: {e}")

    finally:
        driver.quit()
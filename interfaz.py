import tkinter as tk
from tkinter import ttk, messagebox
import mss
import mss.tools
import os
import threading
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Configuración de sitios de prueba ────────────────────────────────
SITIOS = [
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


# ── Lógica de captura y subida ───────────────────────────────────────
def capturar(region):
    Path("screenshots").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{ts}.png"
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=ruta)
    return ruta


def crear_driver(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def subir(sitio, ruta_imagen, headless, log):
    driver = crear_driver(headless)
    wait = WebDriverWait(driver, 15)
    try:
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
            log(f"  ✓ Login exitoso en {sitio['nombre']}")

        driver.get(sitio["url_upload"])
        input_file = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, sitio["selector_input_file"])
            )
        )
        input_file.send_keys(os.path.abspath(ruta_imagen))
        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
        resultado = driver.find_element(By.CSS_SELECTOR, "h3").text
        log(f"  ✓ {sitio['nombre']}: {resultado}")
    except Exception as e:
        log(f"  ✗ Error en {sitio['nombre']}: {e}")
    finally:
        driver.quit()


# ── Interfaz gráfica ─────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automatización de capturas")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)
        self._build_ui()

    def _build_ui(self):
        # ── Región de captura ──
        frame_region = ttk.LabelFrame(
            self, text="Región de captura (píxeles)", padding=10
        )
        frame_region.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        labels = ["Top", "Left", "Width", "Height"]
        defaults = [100, 0, 900, 500]
        self.region_vars = {}

        for i, (lbl, val) in enumerate(zip(labels, defaults)):
            ttk.Label(frame_region, text=lbl).grid(row=0, column=i * 2, padx=(0, 4))
            var = tk.IntVar(value=val)
            ttk.Entry(frame_region, textvariable=var, width=7).grid(
                row=0, column=i * 2 + 1, padx=(0, 12)
            )
            self.region_vars[lbl.lower()] = var

        # ── Opciones ──
        frame_opts = ttk.LabelFrame(self, text="Opciones", padding=10)
        frame_opts.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_opts,
            text="Modo headless (sin ventana de Chrome)",
            variable=self.headless_var,
        ).grid(row=0, column=0, sticky="w")

        # ── Botón ejecutar ──
        self.btn = ttk.Button(self, text="▶  Capturar y subir", command=self._ejecutar)
        self.btn.grid(row=2, column=0, columnspan=2, pady=(0, 12), sticky="ew")

        # ── Log ──
        frame_log = ttk.LabelFrame(self, text="Registro", padding=10)
        frame_log.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.log_text = tk.Text(
            frame_log,
            height=14,
            width=62,
            state="disabled",
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief="flat",
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(frame_log, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

        # Etiqueta de estado
        self.status_var = tk.StringVar(value="Listo")
        ttk.Label(self, textvariable=self.status_var, foreground="gray").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

    def _log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _ejecutar(self):
        self.btn.configure(state="disabled")
        self.status_var.set("Ejecutando...")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            self._log(f"→ Capturando región: {region}")
            ruta = capturar(region)
            self._log(f"✓ Imagen guardada: {ruta}\n")

            headless = self.headless_var.get()
            for sitio in SITIOS:
                self._log(f"→ Subiendo a: {sitio['nombre']}")
                subir(sitio, ruta, headless, self._log)
                self._log("")

            self._log("✓ Proceso completado.")
            self.status_var.set("Completado")
        except Exception as e:
            self._log(f"✗ Error general: {e}")
            self.status_var.set("Error")
        finally:
            self.btn.configure(state="normal")


if __name__ == "__main__":
    App().mainloop()

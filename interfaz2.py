import tkinter as tk
from tkinter import ttk, messagebox
import mss
import mss.tools
import os
import threading
import subprocess
import sys
import ast
import json
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ── Sitios de prueba ─────────────────────────────────────────────────
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

# ── Medidor de región (código inline) ────────────────────────────────
MEDIDOR_CODE = '''
import tkinter as tk
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    ctypes.windll.user32.SetProcessDPIAware()

class MedidorDeRegion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="cross")
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_clic)
        self.inicio_x = None
        self.inicio_y = None
        self.rectangulo = None
        self.texto = None

    def al_hacer_clic(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y,
            outline="red", width=2)
        self.texto = self.canvas.create_text(
            self.inicio_x + 10, self.inicio_y - 10,
            text="0 x 0", fill="white", font=("Arial", 12, "bold"), anchor="nw")

    def al_arrastrar(self, event):
        self.canvas.coords(self.rectangulo, self.inicio_x, self.inicio_y, event.x, event.y)
        ancho = abs(event.x - self.inicio_x)
        alto = abs(event.y - self.inicio_y)
        self.canvas.itemconfig(self.texto, text=f"{ancho} x {alto} px")
        self.canvas.coords(self.texto, event.x + 10, event.y + 10)

    def al_soltar_clic(self, event):
        top = min(self.inicio_y, event.y)
        left = min(self.inicio_x, event.x)
        width = abs(event.x - self.inicio_x)
        height = abs(event.y - self.inicio_y)
        REGION = {"top": top, "left": left, "width": width, "height": height}
        print(f"REGION = {REGION}", flush=True)
        self.root.destroy()

    def iniciar(self):
        self.root.mainloop()

app = MedidorDeRegion()
app.iniciar()
'''
CONFIG_FILE = "config.json"

# ── Funciones de configuración ─────────────────────────────────────

def cargar_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_config(datos: dict):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(datos, f, indent=2)
        print(f"[✓] Config guardada: {datos}")   # ← quítalo después
    except Exception as e:
        print(f"[✗] Error guardando config: {e}") # ← quítalo después

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
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def subir(sitio, ruta_imagen, headless, log):
    driver = crear_driver(headless)
    wait = WebDriverWait(driver, 15)
    try:
        if sitio["necesita_login"]:
            driver.get(sitio["url_login"])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sitio["selector_user"])))
            driver.find_element(By.CSS_SELECTOR, sitio["selector_user"]).send_keys(sitio["usuario"])
            driver.find_element(By.CSS_SELECTOR, sitio["selector_pass"]).send_keys(sitio["clave"])
            driver.find_element(By.CSS_SELECTOR, sitio["selector_btn_login"]).click()
            wait.until(EC.url_contains("secure"))
            log(f"  ✓ Login exitoso en {sitio['nombre']}")
        driver.get(sitio["url_upload"])
        input_file = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, sitio["selector_input_file"])
        ))
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
        self._keybind_actual = None
        self._config = cargar_config()          # carga al iniciar
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)  # intercepta el cierre
        
    def _build_ui(self):
        # ── Región de captura ──
        frame_region = ttk.LabelFrame(self, text="Región de captura", padding=10)
        frame_region.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        keybind_guardado = self._config.get("keybind", "<Control-Return>")
        self.keybind_var = tk.StringVar(value=keybind_guardado)

        # Fila 1: pegar diccionario completo
        ttk.Label(frame_region, text="Pegar REGION:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.region_paste = ttk.Entry(frame_region, width=52)
        self.region_paste.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self.region_paste.insert(0, "{'top': 392, 'left': 524, 'width': 934, 'height': 404}")
        self.region_paste.bind("<FocusOut>", self._parse_region)
        self.region_paste.bind("<Return>", self._parse_region)
        ttk.Button(frame_region, text="Aplicar", command=self._parse_region).grid(row=0, column=2)

        # Separador
        ttk.Separator(frame_region, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=8)

        # Fila 2: campos individuales
        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        frame_campos = ttk.Frame(frame_region)
        frame_campos.grid(row=2, column=0, columnspan=3, sticky="w", pady=(4, 0))
        for i, (lbl, val) in enumerate(campos):
            ttk.Label(frame_campos, text=lbl.capitalize()).grid(
                row=0, column=0 + i * 2, padx=(0 if i == 0 else 12, 4), sticky="e")
            var = tk.IntVar(value=val)
            ttk.Entry(frame_campos, textvariable=var, width=7).grid(
                row=0, column=1 + i * 2, padx=(0, 4))
            var.trace_add("write", self._sync_paste)
            self.region_vars[lbl] = var

        # ── Opciones ──
        frame_opts = ttk.LabelFrame(self, text="Opciones", padding=10)
        frame_opts.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opts, text="Modo headless (sin ventana de Chrome)",
                        variable=self.headless_var).grid(row=0, column=0, sticky="w")

        # ── Botón ejecutar ──
        self.btn = ttk.Button(self, text="▶  Capturar y subir", command=self._ejecutar)
        self.btn.grid(row=2, column=0, columnspan=2, pady=(0, 12), sticky="ew")
        # ── En _build_ui, después de crear self.btn ──

        # Keybind configurable
        frame_key = ttk.LabelFrame(self, text="Atajo de teclado — Capturar y subir", padding=10)
        frame_key.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(frame_key, text="Combinación:").grid(row=0, column=0, padx=(0, 8))
        self.keybind_var = tk.StringVar(value="<Control-Return>")
        self.keybind_entry = ttk.Entry(frame_key, textvariable=self.keybind_var, width=22)
        self.keybind_entry.grid(row=0, column=1, padx=(0, 8))
        ttk.Button(frame_key, text="Aplicar atajo", command=self._aplicar_keybind).grid(row=0, column=2)
        self.keybind_label = ttk.Label(frame_key, text="Activo: Ctrl+Enter", foreground="gray")
        self.keybind_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(6, 0))

        self._keybind_actual = None
        self._aplicar_keybind()  # registra el atajo por defecto al iniciar

        # ── Log ──
        frame_log = ttk.LabelFrame(self, text="Registro", padding=10)
        frame_log.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.log_text = tk.Text(frame_log, height=14, width=62,
                                state="disabled", font=("Consolas", 10),
                                bg="#1e1e1e", fg="#d4d4d4",
                                insertbackground="white", relief="flat")
        self.log_text.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(frame_log, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

        # ── Estado ──
        self.status_var = tk.StringVar(value="Listo") 
        ttk.Label(self, textvariable=self.status_var, 
                  foreground="gray").grid(row=5, column=0, columnspan=2, 
                                          sticky="w", pady=(8, 0))

    # ── Helpers de región ────────────────────────────────────────────
    def _parse_region(self, event=None):
        """Lee el campo de texto y actualiza los 4 campos individuales."""
        texto = self.region_paste.get().strip()
        # Acepta: REGION = {...}  o  solo  {...}
        if "=" in texto:
            texto = texto.split("=", 1)[1].strip()
        try:
            region = ast.literal_eval(texto)
            for key in ("top", "left", "width", "height"):
                if key in region:
                    self.region_vars[key].set(int(region[key]))
        except Exception:
            messagebox.showerror("Formato inválido",
                                 "Pega el diccionario con el formato:\n"
                                 "{'top': 392, 'left': 524, 'width': 934, 'height': 404}")

    def _sync_paste(self, *_):
        """Actualiza el campo de texto cuando se editan los campos individuales."""
        try:
            d = {k: v.get() for k, v in self.region_vars.items()}
            self.region_paste.delete(0, "end")
            self.region_paste.insert(0, str(d))
        except Exception:
            pass

    def _lanzar_medidor(self):
        """Lanza el medidor en un proceso aparte y captura su salida."""
        self._log("→ Abre el medidor — haz clic y arrastra en pantalla...")
        self.btn.configure(state="disabled")
        self.iconify()  # Minimiza la ventana para facilitar la selección

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            stdout, _ = proc.communicate()

            # Busca la línea "REGION = {...}"
            for linea in stdout.splitlines():
                if linea.startswith("REGION ="): 
                    valor = linea.split("=", 1)[1].strip()
                    try:
                        region = ast.literal_eval(valor)
                        # Actualiza la UI desde el hilo principal
                        self.after(0, lambda r=region: self._aplicar_region(r))
                        self.after(0, self.deiconify)  # Restaura al terminar de medir
                        
                        return
                    except Exception:
                        pass
            self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify)  # Restaura la ventana aunque haya error  
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region):
        for key in ("top", "left", "width", "height"):
            if key in region:
                self.region_vars[key].set(int(region[key]))
        self._log(f"✓ Región actualizada: {region}")
        self.btn.configure(state="normal")

    # ── Proceso principal ────────────────────────────────────────────
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

    # ── Keybind dinámico ─────────────────────────────────────────────

    def _aplicar_keybind(self):
        nuevo = self.keybind_var.get().strip()
        if not nuevo:
            return
        if self._keybind_actual:
            try:
                self.unbind(self._keybind_actual)
            except Exception:
                pass
        try:
            self.bind(nuevo, lambda e: self._ejecutar())
            self._keybind_actual = nuevo
            legible = (nuevo.replace("<", "").replace(">", "")
                       .replace("Control", "Ctrl")
                       .replace("Return", "Enter")
                       .replace("-", "+"))
            self.keybind_label.config(text=f"Activo: {legible}", foreground="gray")
            self._config["keybind"] = nuevo     # guarda el keybind validado
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.config(text=f"Atajo inválido: {e}", foreground="red")
            self._keybind_actual = None

    def _al_cerrar(self):
        print(f"[cerrar] _config al cerrar: {self._config}")
        print(f"[cerrar] _keybind_actual: {self._keybind_actual}")
        guardar_config(self._config)
        self.destroy()    

    #── Proceso principal ────────────────────────────────────────────
    def _proceso(self):
        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            self._log(f"→ Capturando región: {region}")

            self.after(0, self.iconify)       # minimiza antes de capturar
            import time; time.sleep(0.4)      # pequeña pausa para que minimice
            ruta = capturar(region)
            self.after(0, self.deiconify)     # restaura al guardar

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
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))


if __name__ == "__main__":
    App().mainloop()
    
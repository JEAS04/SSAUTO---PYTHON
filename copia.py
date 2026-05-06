import tkinter as tk
from tkinter import ttk, messagebox
import mss
import mss.tools
import os
import pickle
import threading
import subprocess
import sys
import ast
import json
import keyring
import time
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
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "button[type='submit']",
        "url_base_upload": "https://miejemplo.com/upload",
        "url_upload": "https://the-internet.herokuapp.com/upload",
        "selector_input_file": "#file-upload",
        "selector_submit": "#file-submit",
    },
]

# ── Medidor de región (código inline) ────────────────────────────────
MEDIDOR_CODE = """
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
"""
CONFIG_FILE = "config.json"
keyring_APP = "AutoCapturaApp"


# ── Funciones de manejo de cookies ─────────────────────────


def guardar_cookies(driver, sitio_nombre):
    Path("cookies").mkdir(exist_ok=True)
    ruta = f"cookies/{sitio_nombre.replace(' ', '_')}.pkl"
    with open(ruta, "wb") as f:
        pickle.dump(driver.get_cookies(), f)


def cargar_cookies(driver, sitio, url_base):
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
                print(f"[cookies] Skipped: {cookie.get('name')} — {e}")
    driver.refresh()
    return True


def guardar_credenciales(sitio_nombre, usuario, clave):
    keyring.set_password(keyring_APP, f"{sitio_nombre}_usuario", usuario)
    keyring.set_password(keyring_APP, f"{sitio_nombre}_clave", clave)


def cargar_credenciales(sitio_nombre):
    usuario = keyring.get_password(keyring_APP, f"{sitio_nombre}_usuario") or ""
    clave = keyring.get_password(keyring_APP, f"{sitio_nombre}_clave") or ""
    return usuario, clave


def borrar_credenciales(sitio_nombre):
    try:
        keyring.delete_password(keyring_APP, f"{sitio_nombre}_usuario")
    except Exception:
        pass
    try:
        keyring.delete_password(keyring_APP, f"{sitio_nombre}_clave")
    except Exception:
        pass


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
    except Exception as e:
        print(f"[✗] Error guardando config: {e}")


# ── Creación del driver ───────────────────────────────────────────────


def crear_driver(headless: bool, usar_chrome_existente: bool = False):
    """
    - usar_chrome_existente=True  → se conecta al Chrome ya abierto en puerto 9222.
    - usar_chrome_existente=False → abre un Chrome nuevo (con o sin headless).
    """
    options = webdriver.ChromeOptions()

    if usar_chrome_existente:
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # No se pasan flags de headless ni sandbox: el Chrome ya está corriendo.
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    # Chrome nuevo
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# ── Lógica de captura ────────────────────────────────────────────────


def capturar(region):
    Path("screenshots").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{ts}.png"
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=ruta)
    return ruta


# ── Lógica de subida ─────────────────────────────────────────────────


def subir(
    sitio,
    ruta_imagen,
    headless,
    log,
    credenciales_sesion=None,
    usar_chrome_existente=False,
):
    """
    Sube `ruta_imagen` al `sitio`.

    Flujo para sitios con login:
      A) usar_chrome_existente=True
         → Se conecta al Chrome del usuario (puerto 9222).
         → Verifica si ya hay sesión activa navegando a url_upload.
         → Si hay sesión  → sube directamente.
         → Si no la hay  → avisa al usuario para que inicie sesión manualmente
                           (no intenta login automático para no interferir con su sesión).
      B) usar_chrome_existente=False
         → Abre Chrome nuevo.
         → Intenta restaurar sesión con cookies.
         → Si las cookies son válidas → sube.
         → Si no                      → hace login automático, guarda cookies y sube.
    """
    # ── BUG CORREGIDO: se pasa usar_chrome_existente a crear_driver ──
    driver = crear_driver(headless, usar_chrome_existente)
    wait = WebDriverWait(driver, 15)
    nombre = sitio.get("nombre", "sitio")

    try:
        # ── PASO 1: gestión de sesión ────────────────────────────────
        if sitio["necesita_login"]:

            if usar_chrome_existente:
                # ── Modo Chrome existente ────────────────────────────
                # Navegamos a la página de subida para saber si hay sesión.
                log(f"  → Verificando sesión activa en Chrome abierto para {nombre}…")
                driver.get(sitio["url_upload"])
                time.sleep(1.5)  # espera a que se resuelva la redirección

                url_actual = driver.current_url.lower()
                # Consideramos que hay sesión si NO fuimos redirigidos al login.
                if "login" in url_actual or "signin" in url_actual:
                    log(f"  ✗ No hay sesión activa en Chrome para {nombre}.")
                    log(
                        f"  → Inicia sesión manualmente en el navegador y vuelve a intentar."
                    )
                    return  # salimos: no podemos hacer login automático aquí

                log(f"  ✓ Sesión activa detectada en Chrome para {nombre}.")
                # La sesión está activa y ya estamos en url_upload → vamos directo a subir.

            else:
                # ── Modo Chrome nuevo ────────────────────────────────
                sesion_restaurada = False
                ruta_cookies = f"cookies/{nombre.replace(' ', '_')}.pkl"

                if Path(ruta_cookies).exists():
                    log(f"  → Intentando restaurar sesión con cookies…")
                    cargar_cookies(driver, sitio, sitio["url_login"])
                    driver.get(sitio["url_upload"])
                    time.sleep(1.5)
                    url_actual = driver.current_url.lower()
                    if "login" not in url_actual and "signin" not in url_actual:
                        log(f"  ✓ Sesión restaurada con cookies para {nombre}.")
                        sesion_restaurada = True
                    else:
                        log(f"  ✗ Cookies expiradas o inválidas, realizando login…")

                if not sesion_restaurada:
                    # Obtener credenciales (sesión > keyring)
                    usuario, clave = "", ""
                    if credenciales_sesion and nombre in credenciales_sesion:
                        usuario = credenciales_sesion[nombre]["usuario"]
                        clave = credenciales_sesion[nombre]["clave"]
                    else:
                        usuario, clave = cargar_credenciales(nombre)

                    if not usuario or not clave:
                        log(
                            f"  ✗ No hay credenciales para {nombre}. Abre 'Credenciales' y configúralas."
                        )
                        return

                    # Login
                    driver.get(sitio["url_login"])
                    wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, sitio["selector_user"])
                        )
                    )
                    driver.find_element(
                        By.CSS_SELECTOR, sitio["selector_user"]
                    ).send_keys(usuario)
                    driver.find_element(
                        By.CSS_SELECTOR, sitio["selector_pass"]
                    ).send_keys(clave)
                    driver.find_element(
                        By.CSS_SELECTOR, sitio["selector_btn_login"]
                    ).click()

                    # Esperar confirmación de login exitoso.
                    # Ajusta "secure" al fragmento de URL que aparece tras login en tu sitio real.
                    try:
                        wait.until(EC.url_contains("secure"))
                    except Exception:
                        log(
                            f"  ✗ Login fallido para {nombre}: la URL no cambió como se esperaba."
                        )
                        driver.save_screenshot(
                            f"debug_login_{nombre.replace(' ', '_')}.png"
                        )
                        return

                    guardar_cookies(driver, nombre)
                    log(f"  ✓ Login exitoso, cookies guardadas para {nombre}.")

                    # Navegar a la página de subida después del login
                    driver.get(sitio["url_upload"])

        else:
            # Sitio sin login: navegar directamente
            driver.get(sitio["url_upload"])

        # ── PASO 2: subida del archivo ───────────────────────────────
        log(f"  → Subiendo imagen a {nombre}…")

        input_file = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, sitio["selector_input_file"])
            )
        )
        input_file.send_keys(os.path.abspath(ruta_imagen))
        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

        # Esperar confirmación de subida exitosa.
        # Se busca el selector de confirmación definido en el sitio, o se intenta h3/h1 como fallback.
        selector_ok = sitio.get("selector_confirmacion", "h3, h1")
        palabras_ok = [
            p.lower()
            for p in sitio.get(
                "palabras_confirmacion", ["uploaded", "success", "exitoso", "subido"]
            )
        ]
        try:
            elemento = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_ok))
            )
            resultado = elemento.text.strip()
            if any(p in resultado.lower() for p in palabras_ok):
                log(f"  ✓ {nombre}: subida exitosa → {resultado}")
            else:
                log(f'  ✗ {nombre}: respuesta inesperada → "{resultado}"')
                driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")
        except Exception:
            log(
                f"  ✗ {nombre}: no se pudo confirmar la subida (timeout esperando confirmación)."
            )
            driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")

    except Exception as e:
        log(f"  ✗ Error inesperado en {nombre}: {e}")
        try:
            driver.save_screenshot(f"debug_error_{nombre.replace(' ', '_')}.png")
        except Exception:
            pass

    finally:
        if usar_chrome_existente:
            # Nunca cerramos el Chrome del usuario.
            pass
        else:
            driver.quit()


# ── Interfaz de Login ─────────────────────────────────────────────────


class LoginWindow(tk.Toplevel):
    """Ventana de credenciales por sitio, aparece antes de la app principal."""

    def __init__(self, parent, sitios):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancelar)
        self.confirmado = False
        self._build_ui()
        self.transient(parent)
        self.wait_window()

    def _build_ui(self):
        ttk.Label(
            self,
            text="Configura las credenciales por sitio",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 14), sticky="w")
        self.campos = {}

        last_frame = None
        for i, sitio in enumerate(self.sitios):
            if not sitio.get("necesita_login"):
                continue
            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)
            frame = ttk.LabelFrame(self, text=nombre, padding=10)
            frame.grid(row=i + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            last_frame = frame

            ttk.Label(frame, text="Usuario:").grid(
                row=0, column=0, sticky="e", pady=(0, 8)
            )
            var_user = tk.StringVar(value=usuario_guardado)
            ttk.Entry(frame, textvariable=var_user, width=28).grid(
                row=0, column=1, pady=(0, 6)
            )

            ttk.Label(frame, text="Contraseña:").grid(
                row=1, column=0, sticky="e", pady=(0, 8)
            )
            var_pass = tk.StringVar(value=clave_guardada)
            ttk.Entry(frame, textvariable=var_pass, width=28, show="*").grid(
                row=1, column=1
            )

            var_remember = tk.BooleanVar(value=tiene_guardado)
            ttk.Checkbutton(
                frame, text="Recordar credenciales", variable=var_remember
            ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

            self.campos[nombre] = {
                "usuario": var_user,
                "clave": var_pass,
                "recordar": var_remember,
            }

        frame_btns = ttk.Frame(self)
        frame_btns.grid(row=99, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(frame_btns, text="Continuar", command=self._confirmar).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(frame_btns, text="Cancelar", command=self._cancelar).pack(
            side="right"
        )

    def _confirmar(self):
        for nombre, vars_ in self.campos.items():
            if not vars_["usuario"].get().strip() or not vars_["clave"].get().strip():
                messagebox.showerror(
                    "Campos vacíos",
                    f"Completa usuario y contraseña para:\n{nombre}",
                    parent=self,
                )
                return

        for nombre, vars_ in self.campos.items():
            if vars_["recordar"].get():
                guardar_credenciales(
                    nombre, vars_["usuario"].get(), vars_["clave"].get()
                )
            else:
                borrar_credenciales(nombre)

        self.credenciales_sesion = {
            nombre: {"usuario": vars_["usuario"].get(), "clave": vars_["clave"].get()}
            for nombre, vars_ in self.campos.items()
        }
        self.confirmado = True
        self.destroy()

    def _cancelar(self):
        self.confirmado = False
        self.destroy()


# ── Interfaz gráfica ──────────────────────────────────────────────────


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Automatización de capturas")
        self._credenciales_sesion = {}
        self.resizable(False, False)
        self.configure(padx=20, pady=20)
        self._keybind_actual = None
        self._config = cargar_config()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        falta_alguna = any(
            sitio.get("necesita_login") and not cargar_credenciales(sitio["nombre"])[0]
            for sitio in SITIOS
        )
        if falta_alguna:

            def _abrir_login_inicial():
                win = LoginWindow(self, SITIOS)
                if win.confirmado:
                    self._credenciales_sesion = win.credenciales_sesion
                    self._log("✓ Credenciales actualizadas en sesión.")

            self.after(100, _abrir_login_inicial)

    def _build_ui(self):
        # ── Región de captura ──
        frame_region = ttk.LabelFrame(self, text="Región de captura", padding=10)
        frame_region.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(frame_region, text="Pegar REGION:").grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )
        self.region_paste = ttk.Entry(frame_region, width=52)
        self.region_paste.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self.region_paste.insert(
            0, "{'top': 392, 'left': 524, 'width': 934, 'height': 404}"
        )
        self.region_paste.bind("<FocusOut>", self._parse_region)
        self.region_paste.bind("<Return>", self._parse_region)
        ttk.Button(frame_region, text="Aplicar", command=self._parse_region).grid(
            row=0, column=2
        )

        ttk.Separator(frame_region, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=8
        )

        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        frame_campos = ttk.Frame(frame_region)
        frame_campos.grid(row=2, column=0, columnspan=3, sticky="w", pady=(4, 0))
        for i, (lbl, val) in enumerate(campos):
            ttk.Label(frame_campos, text=lbl.capitalize()).grid(
                row=0, column=0 + i * 2, padx=(0 if i == 0 else 12, 4), sticky="e"
            )
            var = tk.IntVar(value=val)
            ttk.Entry(frame_campos, textvariable=var, width=7).grid(
                row=0, column=1 + i * 2, padx=(0, 4)
            )
            var.trace_add("write", self._sync_paste)
            self.region_vars[lbl] = var

        ttk.Button(
            frame_region,
            text="🖱  Medir región en pantalla",
            command=self._lanzar_medidor,
        ).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 0))

        # ── Opciones ──
        frame_opts = ttk.LabelFrame(self, text="Opciones", padding=10)
        frame_opts.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        self.headless_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_opts,
            text="Modo headless (sin ventana de Chrome)",
            variable=self.headless_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(
            frame_opts, text="Credenciales", command=self._abrir_credenciales
        ).grid(row=0, column=1, padx=(20, 0))
        ttk.Button(
            frame_opts, text="Renovar sesión", command=self._renovar_sesion
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        self.chrome_existente_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_opts,
            text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var,
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Button(
            frame_opts,
            text="Abrir Chrome con depuración",
            command=self._abrir_chrome_debug,
        ).grid(row=2, column=1, padx=(20, 0))

        # ── Botón ejecutar ──
        self.btn = ttk.Button(self, text="▶  Capturar y subir", command=self._ejecutar)
        self.btn.grid(row=2, column=0, columnspan=2, pady=(0, 12), sticky="ew")

        # ── Keybind configurable ──
        frame_key = ttk.LabelFrame(
            self, text="Atajo de teclado — Capturar y subir", padding=10
        )
        frame_key.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(frame_key, text="Combinación:").grid(
            row=0, column=0, padx=(0, 8), sticky="we"
        )
        self.keybind_var = tk.StringVar(value="Ejemplo: Ctrl+Enter")
        self.keybind_entry = ttk.Entry(
            frame_key, textvariable=self.keybind_var, width=40, foreground="gray"
        )
        self.keybind_entry.grid(row=0, column=1, padx=(0, 8))
        ttk.Button(frame_key, text="Aplicar atajo", command=self._aplicar_keybind).grid(
            row=0, column=2
        )
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        self.keybind_label = ttk.Label(frame_key, text="", foreground="black")
        self.keybind_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(6, 0))

        keybind_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(keybind_inicial, lambda e: self._ejecutar())
            self._keybind_actual = keybind_inicial
            legible = (
                keybind_inicial.replace("<", "")
                .replace(">", "")
                .replace("Control", "Ctrl")
                .replace("Return", "Enter")
                .replace("-", "+")
            )
            self.keybind_label.config(text=f"Combinación activa: {legible}")
        except Exception:
            self.keybind_label.config(text="Atajo no válido", foreground="red")

        # ── Log ──
        frame_log = ttk.LabelFrame(self, text="Registro", padding=10)
        frame_log.grid(row=4, column=0, columnspan=2, sticky="nsew")
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

        # ── Estado ──
        self.status_var = tk.StringVar(value="Listo")
        ttk.Label(self, textvariable=self.status_var, foreground="gray").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

    def _abrir_credenciales(self):
        win = LoginWindow(self, SITIOS)
        if win.confirmado:
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")

    def _parse_region(self, event=None):
        texto = self.region_paste.get().strip()
        if "=" in texto:
            texto = texto.split("=", 1)[1].strip()
        try:
            region = ast.literal_eval(texto)
            for key in ("top", "left", "width", "height"):
                if key in region:
                    self.region_vars[key].set(int(region[key]))
        except Exception:
            messagebox.showerror(
                "Formato inválido",
                "Pega el diccionario con el formato:\n"
                "{'top': 392, 'left': 524, 'width': 934, 'height': 404}",
            )

    def _sync_paste(self, *_):
        try:
            d = {k: v.get() for k, v in self.region_vars.items()}
            self.region_paste.delete(0, "end")
            self.region_paste.insert(0, str(d))
        except Exception:
            pass

    def _lanzar_medidor(self):
        self._log("→ Abre el medidor — haz clic y arrastra en pantalla...")
        self.btn.configure(state="disabled")
        self.iconify()

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()
            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    valor = linea.split("=", 1)[1].strip()
                    try:
                        region = ast.literal_eval(valor)
                        self.after(0, lambda r=region: self._aplicar_region(r))
                        self.after(0, self.deiconify)
                        return
                    except Exception:
                        pass
            self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region):
        for key in ("top", "left", "width", "height"):
            if key in region:
                self.region_vars[key].set(int(region[key]))
        self._log(f"✓ Región actualizada: {region}")
        self.btn.configure(state="normal")

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
            legible = (
                nuevo.replace("<", "")
                .replace(">", "")
                .replace("Control", "Ctrl")
                .replace("Return", "Enter")
                .replace("-", "+")
            )
            self.keybind_label.config(text=f"Activo: {legible}", foreground="gray")
            self._config["keybind"] = nuevo
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.config(text=f"Atajo inválido: {e}", foreground="red")
            self._keybind_actual = None

    def _al_cerrar(self):
        guardar_config(self._config)
        self.destroy()

    def _proceso(self):
        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            self._log(f"→ Capturando región: {region}")

            self.after(0, self.iconify)
            time.sleep(0.4)
            ruta = capturar(region)
            self.after(0, self.deiconify)

            self._log(f"✓ Imagen guardada: {ruta}\n")
            headless = self.headless_var.get()
            usar_chrome_existente = self.chrome_existente_var.get()
            for sitio in SITIOS:
                self._log(f"→ Subiendo a: {sitio['nombre']}")
                subir(
                    sitio,
                    ruta,
                    headless,
                    self._log,
                    self._credenciales_sesion,
                    usar_chrome_existente,
                )
                self._log("")
            self._log("✓ Proceso completado.")
            self.status_var.set("Completado")
        except Exception as e:
            self._log(f"✗ Error general: {e}")
            self.status_var.set("Error")
        finally:
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _renovar_sesion(self):
        import shutil

        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")

    def _abrir_chrome_debug(self):
        rutas_chrome = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_exe = next((r for r in rutas_chrome if Path(r).exists()), None)
        if not chrome_exe:
            self._log(
                "✗ No se encontró Chrome. Ábrelo manualmente con --remote-debugging-port=9222"
            )
            return
        subprocess.Popen(
            [
                chrome_exe,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome_sesion_ssauto",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222")
        self._log("→ Inicia sesión en los sitios y luego ejecuta la captura.")

    def _capturar_tecla(self, event):
        partes = []
        if event.state & 0x4:
            partes.append("Control")
        if event.state & 0x1:
            partes.append("Shift")
        if event.state & 0x20000:
            partes.append("Alt")
        tecla = event.keysym
        if tecla in ("Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"):
            return "break"
        partes.append(tecla)
        combinacion = "<" + "-".join(partes) + ">"
        self.keybind_var.set(combinacion)
        return "break"


if __name__ == "__main__":
    App().mainloop()

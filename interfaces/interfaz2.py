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
import subprocess
import shutil
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
        # "url_login": "https://miejemplo.com/login",
        # "usuario": "tomsmith",
        # "clave": "SuperSecretPassword!",
        "selector_user": "#username",
        "selector_pass": "#password",
        "selector_btn_login": "button[type='submit']",
        "url_base_upload": "https://miejemplo.com/upload",  # ← sin número
        "url_upload": "https://the-internet.herokuapp.com/upload",
        # "url_upload": "https://miejemplo.com/upload/1",     # ← respaldo fijo
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
keyring_APP = "AutoCapturaApp"  # nombre para keyring (si decides usarlo en el futuro)

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
    except:
        pass
    try:
        keyring.delete_password(keyring_APP, f"{sitio_nombre}_clave")
    except:
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
        print(f"[✓] Config guardada: {datos}")  # ← quítalo después
    except Exception as e:
        print(f"[✗] Error guardando config: {e}")  # ← quítalo después


# ── Creación del driver ───────────────────────────────────────────────


def crear_driver(headless: bool, usar_chrome_existente: bool = False):
    """
    casos de uso para crear_driver:
    - usar_chrome_existente=True  → se conecta al Chrome ya abierto en puerto 9222.
    - usar_chrome_existente=False → abre un Chrome nuevo (con o sin headless).
    """
    options = webdriver.ChromeOptions()

    if usar_chrome_existente:
        # Conectarse al Chrome ya abierto
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # No se pasan flags de headless ni sandbox: el chrome ya esta abierto.
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    # Comportamiento original: abrir Chrome nuevo
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


# ── Lógica de captura y subida ───────────────────────────────────────
def capturar(region):
    Path("screenshots").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{ts}.png"
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=ruta)
    return ruta


# ── Lógica de subida ─────────────────────────────────────────────────


# La función subir ahora maneja tanto el caso de login como el de sitios sin login, e incluye validaciones para asegurar que la sesión esté activa antes de intentar subir
#  la imagen. Si el sitio requiere login, primero intenta restaurar la sesión con cookies, y si eso falla, procede a hacer login con las credenciales proporcionadas.
#  Después de un login exitoso, guarda las cookies para futuras ejecuciones. Durante la subida, espera a que se confirme que la imagen fue subida correctamente antes
#  de registrar el resultado.
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
    driver = crear_driver(headless, usar_chrome_existente)
    wait = WebDriverWait(driver, 15)
    # sesion_activa = True  # asume sesión activa, se validará más adelante
    nombre = sitio.get("nombre", "sitio")

    try:
        if sitio["necesita_login"]:
            # url_base = sitio["url_login"]
            # sesion_activa = False

            if usar_chrome_existente:
                # ── Reutilizar la pestaña activa en lugar de abrir una nueva ──
                # pestaña_original = driver.current_window_handle
                # driver.switch_to.window(pestaña_original)
                # Verificar si ya hay sesión activa en el Chrome abierto
                log(
                    f"  → Verificando sesión activa en Chrome abierto para {sitio['nombre']}..."
                )
                driver.get(sitio["url_upload"])
                time.sleep(
                    1.5
                )  # pequeña pausa para que cargue y redirija si no hay sesión

                url_actual = driver.current_url.lower()

                if "login" in url_actual or "signin" in url_actual:
                    log(f"  ✗ No hay sesión activa en Chrome para {nombre}.")
                    log(
                        f"  → Inicia sesión manualmente en el navegador y vuelve a intentar."
                    )
                    return  # salimos: no podemos hacer login automático aquí

                log(f"  ✓ Sesión activa detectada en Chrome: {sitio['nombre']}")

            else:
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
                    # Obtener credenciales (sesion > keyring)
                    usuario, clave = "", ""
                    if credenciales_sesion and nombre in credenciales_sesion:
                        usuario = credenciales_sesion[nombre].get("usuario", "")
                        clave = credenciales_sesion[nombre].get("clave", "")
                    else:
                        usuario, clave = cargar_credenciales(nombre)

                    if not usuario or not clave:
                        log(
                            f"  ✗ No hay credenciales para {nombre}. Abre 'Credenciales' en las opciones para configurarlas."
                        )
                        return

                    # ── LOGIN ─────────────────────────────

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

                    try:
                        wait.until(EC.url_contains("secure"))
                    except Exception:
                        log(
                            f"  ✗ Error al iniciar sesión para {nombre}: la URL no cambió como se esperaba."
                        )
                        return

                    guardar_cookies(driver, nombre)
                    log(f"  ✓ Login exitoso, cookies guardadas: {nombre}")

                    # Navegar a la página de subida después del login
                    driver.get(sitio["url_upload"])

        else:
            driver.get(sitio["url_upload"])

        # ── SUBIDA ────────────────────────────
        log(f"  → Subiendo imagen a {sitio['nombre']}…")

        input_file = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, sitio["selector_input_file"])
            )
        )
        input_file.send_keys(os.path.abspath(ruta_imagen))

        # Guardar el texto actual del h3/h1 ANTES de subir (para comparar después)
        selector_ok = sitio.get("selector_confirmacion", "h3, h1")
        palabras_ok = [
            p.lower()
            for p in sitio.get(
                "palabras_confirmacion", ["uploaded", "success", "exitoso", "subido"]
            )
        ]
        try:
            texto_antes = (
                driver.find_element(By.CSS_SELECTOR, selector_ok).text.strip().lower()
            )
        except Exception:
            texto_antes = ""

        driver.find_element(By.CSS_SELECTOR, sitio["selector_submit"]).click()

        # Esperar hasta que el texto cambie respecto al que había antes
        try:
            wait_confirmacion = WebDriverWait(driver, 30)
            wait_confirmacion.until(
                lambda d: d.find_element(By.CSS_SELECTOR, selector_ok)
                .text.strip()
                .lower()
                != texto_antes
            )
            resultado = driver.find_element(By.CSS_SELECTOR, selector_ok).text.strip()

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
            pass  # no cerrar el Chrome que el usuario tiene abierto - nunca se cierra el Chrome del usuario.
        else:
            driver.quit()

    usuario, clave = cargar_credenciales(
        sitio["nombre"]
    )  # Esto hay que comentarlo despues
    print("DEBUG CREDENCIALES:", usuario, clave)  # Esto hay que comentarlo despues


# ────────────────────────────Interfaz de Login────────────────────────────


class LoginWindow(tk.Toplevel):
    """Ventana de credenciales por sitio, aparece antes de la app principal"""

    def __init__(self, parent, sitios):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")  # para {sitios['nombre']}
        self.resizable(False, False)
        self.configure(padx=20, pady=20)
        self.grab_set()  # esto hace un modal, bloqueando la ventana principal
        self.protocol("WM_DELETE_WINDOW", self._cancelar)
        self.confirmado = False  # intercepta el cierre
        self._build_ui()
        self.transient(parent)  # se muestra encima de la ventana principal
        self.wait_window()  # espera a que se cierre esta ventana antes de continuar

    def _build_ui(self):
        ttk.Label(
            self,
            text="Configura las credenciales por sitio",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 14), sticky="w")
        self.campos = (
            {}
        )  # {nombre_sitio: {"usuario": var, "clave": var, "recordar": var}}

        for i, sitio in enumerate(self.sitios):
            if not sitio.get("necesita_login"):
                continue
            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)
            frame = ttk.LabelFrame(self, text=nombre, padding=10)
            frame.grid(row=i + 1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

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

        # Botones de acción────────────────────────────

        frame.btns = ttk.Frame(self)
        frame.btns.grid(row=99, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(frame.btns, text="Continuar", command=self._confirmar).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(frame.btns, text="Cancelar", command=self._cancelar).pack(
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


# ── Interfaz gráfica ─────────────────────────────────────────────────
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Automatización de capturas")
        self._credenciales_sesion = {}
        self.resizable(False, False)
        self.configure(padx=20, pady=20)
        self._keybind_actual = None
        self._config = cargar_config()  # carga al iniciar
        print(f"[inicio] config cargada: {self._config}")
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)  # intercepta el cierre

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

        # Fila 1: pegar diccionario completo
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

        # Separador
        ttk.Separator(frame_region, orient="horizontal").grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=8
        )

        # Fila 2: campos individuales
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

        # ── Opciones ────────────────────────────
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
        # ── En _build_ui, después de crear self.btn ──

        # Keybind configurable
        frame_key = ttk.LabelFrame(
            self, text="Atajo de teclado — Capturar y subir", padding=10
        )
        frame_key.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Label(frame_key, text="Combinación:").grid(
            row=0, column=0, padx=(0, 8), sticky="we"
        )
        self.keybind_var = tk.StringVar(
            value="Ejemplo: Ctrl+Enter"
        )  # (value="<Control-Return>")
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

        # Registra el keybind guardado SIN llamar _aplicar_keybind (para no sobreescribir config)
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
            messagebox.showerror(
                "Formato inválido",
                "Pega el diccionario con el formato:\n"
                "{'top': 392, 'left': 524, 'width': 934, 'height': 404}",
            )

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
                text=True,
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
            legible = (
                nuevo.replace("<", "")
                .replace(">", "")
                .replace("Control", "Ctrl")
                .replace("Return", "Enter")
                .replace("-", "+")
            )
            self.keybind_label.config(text=f"Activo: {legible}", foreground="gray")
            self._config["keybind"] = nuevo  # guarda el keybind validado
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.config(text=f"Atajo inválido: {e}", foreground="red")
            self._keybind_actual = None

    def _al_cerrar(self):
        print(f"[cerrar] _config al cerrar: {self._config}")
        print(f"[cerrar] _keybind_actual: {self._keybind_actual}")
        guardar_config(self._config)
        self.destroy()

    # ── Proceso principal ────────────────────────────────────────────
    def _proceso(self):
        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            self._log(f"→ Capturando región: {region}")

            self.after(0, self.iconify)  # minimiza antes de capturar
            time.sleep(0.4)  # pequeña pausa para que minimice
            ruta = capturar(region)
            self.after(0, self.deiconify)  # restaura al guardars

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
        """Borra cookies guardadas para forzar un login fresco."""

        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")

    def _abrir_chrome_debug(self):
        """Lanza Chrome con el puerto de depuración remota."""

        rutas_chrome = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_exe = next((r for r in rutas_chrome if Path(r).exists()), None)

        if not chrome_exe:
            self._log(
                "✗ No se encontró Chrome. Abre chrome.exe manualmente con --remote-debugging-port=9222"
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
        self._log("→ Inicia sesión en los sitios y luego ejecuta la captura")

    def _capturar_tecla(self, event):
        """Detecta la combinación presionada y la escribe automáticamente."""
        partes = []
        if event.state & 0x4:
            partes.append("Control")
        if event.state & 0x1:
            partes.append("Shift")
        if event.state & 0x20000:
            partes.append("Alt")

        tecla = event.keysym
        # Ignorar si solo se presiona un modificador solo
        if tecla in ("Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"):
            return "break"

        partes.append(tecla)
        combinacion = "<" + "-".join(partes) + ">"
        self.keybind_var.set(combinacion)
        return "break"  # evita que el caracter se escriba en el campo


if __name__ == "__main__":
    App().mainloop()


# 04-05-2026

# El dia de hoy empece la creacion de un script en Python para la automatización de capturas de pantallas con MSS y subida a sitios web con Selenium,
# con una interfaz gráfica en Tkinter.
# Implementé un medidor de región para seleccionar el área de captura.
# El sistema permite seleccionar una región de la pantalla, capturarla, y luego subirla a diferentes sitios web, algunos de los cuales requieren autenticación.
# Se puede controlar el modo headless para que Chrome no abra una ventana visible.
# La interfaz permite configurar el tamaño de la region, de forma manual y automatica con el medidor (boton),
# y también configurar un atajo de teclado para ejecutar la captura y subida, el cual se guarda en un archivo JSON de config.
# La idea de este proyecto es facilitar la captura y compartición de evidencias, para las plataformas de HubSpot y SunRun, que son las mas utilizadas en el trabajo a diario,
# y que conllevan muchos pasos manuales para subir las capturas a cada plataforma, con este sistema se busca automatizar ese proceso y ahorrar tiempo.
# Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
# Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

# 05-05-2026

# En el dia de hoy, me enfoqué en implementar la funcionalidad de login para los sitios que lo requieren, utilizando Selenium para automatizar el proceso de autenticación.
# Creé una ventana modal de login que se muestra al iniciar la aplicación, donde se pueden ingresar y guardar las credenciales de cada sitio de forma
# segura utilizando la librería keyring.
# La función de subida ahora incluye el proceso de login automático antes de intentar subir la imagen,
# lo que permite manejar sitios con autenticación sin necesidad de ingresar las credenciales cada vez.
# Además, se agregó una validación para verificar que el login fue exitoso antes de proceder con la subida, y se muestra un mensaje de error si el login falla.
# Se implemento un sistema de cookies para intentar restaurar la sesión antes de hacer login, lo que puede evitar la necesidad de autenticarse en cada ejecución
# si las cookies siguen siendo válidas. Ademas de las cookies un boton para renovar la sesión, que borra las cookies guardadas y fuerza un login fresco en la próxima ejecución.
# Tambien añadi una opción para reutilizar una sesión de Chrome ya abierta, lo que permite aprovechar una sesión activa sin necesidad de hacer login automático cada vez,
# aunque requiere que el usuario inicie sesión manualmente en el navegador.
# Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
# Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

# arreglado
# realmente es necesario iniciar sesion cada vez que se quiera subir una captura a un sitio que requiere autenticacion?, ademas si el sitio se mantiene abierto siempre
# en el navegador, no se podria aprovechar esa sesion activa para subir las capturas sin necesidad de hacer login cada vez?

# arreglado
# Hay que arreglar el chrome con depuracion, ya que se abre bien, pero cuando se ejecuta la captura y subida, no detecta la sesión activa, aunque el Chrome abierto
#  tenga sesión iniciada en el sitio, entonces hace el login automático, pero no funciona, no detecta que se hizo login exitoso,
#  y no sube la imagen. Hay que revisar esa parte para que funcione correctamente con un Chrome ya abierto y con sesión activa.

# 06-05-2026

# Hoy empece a arreglar el chrome con depuracion (cuando las paginas ya estan abiertas), el problema era que, aunque se detectaba
# la sesión activa en el Chrome abierto, al navegar a la página de subida, el sitio redirigía a la página de login, lo que
# indicaba que no se estaba aprovechando la sesión activa correctamente. Entonces cuando se tomaba la captura se abrian las pestañas
# correspondientes a cada sitio y se subian las capturas correctamente, pero la idea era que si el usuario ya tenia sesión iniciada
# en el Chrome abierto, se aprovechara esa sesión para subir las capturas sin necesidad de hacer login automático cada vez,
# pero no estaba funcionando así. Entonces, para solucionar esto, modifiqué el flujo para que después de detectar la sesión activa,
# se navegue directamente a la página de subida en las pestañas correspondientes donde ya habia una sesion iniciada, esperando que
# no se abrieran nuevas pestañas, ademas de esto se debe confirmar la subida de la imagen al sitio, con su respectivo boton.
# Se añadieron colores y se reorganizo la estructura de la interfaz, ahora se ve mas estetico, ademas la interfaz se adapta a la
# resolucion de la pantalla

# PENDIENTES: PONERLE LINEA DE TIEMPO, TIEMPO DE DESARROLLO, Y PROXIMOS PASOS, MEJORAS FUTURAS, ETC.

# 07-05-2026
# Se añadio scroll para que el contenido de la interfaz se vea correctamente, ademas ahora al minimizar y maximizar, el contenido se adapta correctamente.
# Se migro todo el script de Tkinter a CustomTkinter con toda la funcionalidad preservada, lo que nos permitio hacer una interfaz mas estetica y mas facil de optimizar, CustomTkinter permite hacer que
#  el tema de fondo de la aplicacion sea mas sencillo de utilizar o cambiar, lo cual no se podia hacer tan facil desde Tkinter, se quitaron todos los LOGS y se documento
# y se documento la funcionalidad del script, se le coloco un favicon sencillo.
# Se agrego una nueva funcionalidad, ahora se pueden guardar diferentes perfiles segun el tipo de monitor, ejemplo: (monitor 1- panel izquierdo) y se rellena automaticamente
# cuando se mide la pantalla se da un nombre y se guarda, y asi se crea un nuevo perfil, luego se puede ir cambiando de perfiles y dar al boton cargar, para usar
# la region guardada

# pendientes: hacer que se guarde en config.json y que se pueda utilizar cualquier monitor conectado a la computadora principal

# CORRECCIONES APLICADAS:
# 1 — _make_status_bar: .grid(side=) → .pack(side=)
# 2 — _make_log_section era código muerto (log_text se creaba dos veces); eliminado
# 3 — _log(): CTkTextbox no soporta tags de color → usa ._textbox interno de Tk
# 4 — _font_exists(): ahora usa tkinter.font.families() correctamente
# 5 — _status_dot/.grid(side=) → .pack(side=) (mismo que #1, instancia distinta)
# 6 — status_frame en _build_ui: row=99 → row=5
# 7 — _proceso(): todos los self._log() pasan por self.after() (thread-safety)
# 8 — subir(): se le pasa un wrapper thread-safe en lugar del _log directo

# El codigo se hizo muy grande asi que lo separe en varios archivos, para que asi el desarrollo sea algo mas sencillo

# ssauto/
# ├── main.py                   ← Punto de entrada (ejecutar este archivo)
# ├── configuracion.py          ← Constantes, lista de sitios y config.json
# ├── credenciales.py           ← Cookies de sesión y llavero del SO (keyring)
# ├── medidor.py                ← Código del selector visual de región
# ├── automatizacion.py         ← Driver de Chrome, captura y subida (Selenium + mss)
# ├── ventana_credenciales.py   ← Ventana modal de usuario/contraseña
# ├── ventana_principal.py      ← Ventana principal (CustomTkinter)
# ├── config.json               ← Generado automáticamente al guardar ajustes
# ├── cookies/                  ← Generado automáticamente al hacer login
# └── screenshots/              ← Generado automáticamente al capturar

# Se empezo a realizar el script con web scraping + api, para automatizar varias cosas
# pendientes. realizar el web scraping para comparar los datos traidos de ahi con los de la api, determinar si son iguales o no, si son iguales se dejan iguales,
#  si son diferentes se ponen los dos encima del otro, como una sugerencia, si en uno de los dos el dato esta vacio, se coloca el dato que este,
#  ejemplo: sitio 1: nombre: no encontrado, pero en el sitio 2: nombre: Julian, se coloca el valor del sitio 2, para asi lograr una comparacion completa

## Mejoras necesarias (a corto plazo)

# ### 1. Compatibilidad con macOS y Linux
# `_abrir_chrome_debug()` solo busca Chrome en rutas de Windows. Agregar detección del SO con `platform.system()` y las rutas correspondientes en cada sistema.

# ### 2. Gestión de errores más granular
# Actualmente los errores de subida se logean pero no se reintentan. Implementar reintentos automáticos (p. ej. 3 intentos con espera exponencial) para fallos de red.

# ### 3. Validación de la región capturada
# Si `width` o `height` es 0, `mss` lanzará un error silencioso. Agregar validación antes de llamar a `capturar()` y mostrar un mensaje claro al usuario.

# ### 4. Pruebas automáticas
# No hay ningún test. Agregar al menos pruebas unitarias para `parsear_region`, `_keybind_legible` y `cargar_config` con `pytest`.

# ---

# ## Mejoras futuras (a mediano plazo)

# ### 5. Soporte para múltiples perfiles de región
# Permitir guardar y cargar diferentes regiones con nombre (p. ej. "Monitor 1 - Panel izquierdo") en lugar de solo una.

# ### 6. Programación por horario
# Agregar un campo de intervalo (en minutos) para que la captura y subida se ejecuten automáticamente de forma periódica usando `threading.Timer` o `schedule`.

# ### 7. Historial de capturas
# Mostrar en la UI las últimas N capturas realizadas con miniatura, fecha y estado de subida. Guardar el historial en un archivo JSON local.

# ### 8. Notificaciones del sistema
# Usar `plyer` o `winotify` (Windows) para mostrar una notificación nativa cuando el proceso complete o falle, incluso si la ventana está minimizada.

# ### 9. Modo de línea de comandos (CLI)
# Exponer `capturar()` y `subir()` como comandos de consola para poder integrar SSAuto en scripts o tareas programadas del SO sin abrir la UI.

# ### 10. Empaquetado como ejecutable
# Configurar `PyInstaller` o `Nuitka` para distribuir la app como un `.exe` sin requerir Python instalado.

# ---

# ## Cosas a considerar

# - **Seguridad de cookies**: Los archivos `.pkl` en la carpeta `cookies/` no están cifrados. Cualquiera con acceso al sistema puede leerlos. Para mayor seguridad, cifrarlos con `cryptography.fernet` usando una clave derivada del llavero del SO.
# - **Selector de confirmación**: `wait.until(EC.url_contains("secure"))` está hardcodeado para el sitio de demo de Herokuapp. Para sitios reales, cambiar esto a un selector configurable por sitio en `SITIOS`.
# - **WebDriverManager y offline**: Si la máquina no tiene internet, `ChromeDriverManager().install()` fallará. Considerar cachear el driver o permitir especificar la ruta manualmente.


# 11/05/2026
# Se empezo a hacer pruebas con el web scraping y el API para la comparacion de datos de clientes.
# El bot se ejecuta en el puerto 9222 de Chrome esto para que la automatizacion sea efectiva.
# En ese perfil de Chrome se puede iniciar sesion normal con cualquier cuenta, PERO su uso es unica y exclusivamente para el uso de los bots, ya que permite que los perfiles de uso diario no se rompan, no se bloquee chrome, no se corrompan los perfiles y es mas seguro aislar, ademas ahi se guardan todos los datos de la sesion incluyendo, cookies, sesiones, las cuentas, extensiones, pestañas, preferencias, etc. Y es mejor para que el bot no sea detectado por el navegador

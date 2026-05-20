"""
SSAuto — Automatización de capturas (CustomTkinter)
"""

import customtkinter as ctk
import tkinter.font
from tkinter import messagebox
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
import shutil
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# ── config de los temas ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
keyring_APP = "AutoCapturaApp"

# ── Funciones de manejo de cookies ───────────────────────────────────


def guardar_cookies(driver, sitio_nombre):
    Path("cookies").mkdir(exist_ok=True)
    ruta = f"cookies/{sitio_nombre.replace(' ', '_')}.pkl"
    with open(ruta, "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print(f"[cookies] Guardadas en: {ruta}")


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


# ── Funciones de configuración ────────────────────────────────────────


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
    Crea y devuelve una instancia de ChromeDriver configurada.

    Casos de uso:
    - usar_chrome_existente=True  → se conecta al Chrome ya abierto en puerto 9222.
    - usar_chrome_existente=False → abre un Chrome nuevo (con o sin headless).

    Nota: Se evitan opciones experimentales obsoletas (excludeSwitches,
    useAutomationExtension) que causan errores con ChromeDriver moderno.
    El antifingerprinting se logra exclusivamente vía --disable-blink-features.
    """
    import logging

    _log_driver = logging.getLogger("ssauto.driver")

    options = webdriver.ChromeOptions()

    # ── Antifingerprinting: ocultar indicadores de automatización ──────
    # NOTA: excludeSwitches y useAutomationExtension ya no son compatibles
    # con ChromeDriver moderno (causan "invalid argument: unrecognized chrome
    # option"). Se reemplazan por --disable-blink-features que es el método
    # oficial y soportado.
    options.add_argument("--disable-blink-features=AutomationControlled")

    try:
        if usar_chrome_existente:
            # Conectarse al Chrome ya abierto en puerto 9222
            _log_driver.info("Conectando a Chrome existente en puerto 9222...")
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            # No se pasan flags de headless ni sandbox: el Chrome ya está abierto.

        else:
            _log_driver.info("Abriendo nuevo Chrome...")
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        # ── Inicializar WebDriver con manejo de errores ──────────────────
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # ── Opcional: ocultar navigator.webdriver ─────────────────────────
        # En Chrome 147+ esta propiedad ya no es redefinible cuando se
        # conecta a una sesión real de usuario (remote debugging 9222).
        # Se envuelve en try/catch para evitar el error:
        #   "Cannot redefine property: webdriver"
        # El logging permite diagnosticar si la inyección falla.
        try:
            driver.execute_script("""
            try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            } catch(e) {
                // Chrome 147+ no permite redefinir navigator.webdriver
                // en sesiones de depuración reales. Esto es normal y seguro.
            }
            """)
        except Exception as _js_err:
            _log_driver.debug(
                f"Script de navigator.webdriver no se pudo inyectar "
                f"(esperado en Chrome moderno): {_js_err}"
            )

        _log_driver.info("ChromeDriver inicializado correctamente.")
        return driver

    except Exception as e:
        _log_driver.error(f"Error al inicializar ChromeDriver: {e}")
        raise


# ── Lógica de captura ─────────────────────────────────────────────────


def capturar(region):
    Path("screenshots").mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"screenshots/captura_{ts}.png"
    with mss.MSS() as sct:
        screenshot = sct.grab(region)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=ruta)
    return ruta


# ── Lógica de subida ──────────────────────────────────────────────────

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
    nombre = sitio.get("nombre", "sitio")

    try:
        if sitio["necesita_login"]:
            if usar_chrome_existente:
                # ── Reutilizar la pestaña activa en lugar de abrir una nueva ──
                # pestaña_original = driver.current_window_handle
                # driver.switch_to.window(pestaña_original)
                # Verificar si ya hay sesión activa en el Chrome abierto
                log(f"  → Verificando sesión activa en Chrome abierto para {nombre}...")
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
                log(f"  ✓ Sesión activa detectada en Chrome: {nombre}")
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
                            f"  ✗ No hay credenciales para {nombre}. Abre 'Credenciales' para configurarlas."
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
                            f"  ✗ Error al iniciar sesión para {nombre}: URL no cambió."
                        )
                        return

                    # Navegar a la página de subida después del login
                    guardar_cookies(driver, nombre)
                    log(f"  ✓ Login exitoso, cookies guardadas: {nombre}")
                    driver.get(sitio["url_upload"])
        else:
            driver.get(sitio["url_upload"])

        # ── SUBIDA ────────────────────────────
        log(f"  → Subiendo imagen a {nombre}…")
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
            log(f"  ✗ {nombre}: no se pudo confirmar la subida (timeout).")
            driver.save_screenshot(f"debug_upload_{nombre.replace(' ', '_')}.png")

    except Exception as e:
        log(f"  ✗ Error inesperado en {nombre}: {e}")
        try:
            driver.save_screenshot(f"debug_error_{nombre.replace(' ', '_')}.png")
        except Exception:
            pass
    finally:
        if (
            not usar_chrome_existente
        ):  # no cerrar el Chrome que el usuario tiene abierto - nunca se cierra el Chrome del usuario.
            driver.quit()


# ────────────────────────────Interfaz de Login────────────────────────────
# ── Ventana de Login (CustomTkinter) ─────────────────────────────────


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, sitios):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")  # para {sitios['nombre']}
        self.resizable(False, False)
        self.grab_set()  # esto hace un modal, bloqueando la ventana principal
        self.confirmado = False  # intercepta el cierre
        self._build_ui()
        self.transient(parent)  # se muestra encima de la ventana principal
        self.wait_window()  # espera a que se cierre esta ventana antes de continuar

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Configurar credenciales",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, pady=(16, 12), padx=20, sticky="w")

        self.campos = {}
        row_index = 1
        for sitio in self.sitios:
            if not sitio.get("necesita_login"):
                continue
            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)

            frame = ctk.CTkFrame(self, fg_color=("gray95", "gray20"), border_width=1)
            frame.grid(row=row_index, column=0, sticky="ew", padx=20, pady=(0, 10))
            frame.grid_columnconfigure(1, weight=1)
            row_index += 1

            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("royalblue", "#4a9eff"),
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(10, 6))

            var_user = ctk.StringVar(value=usuario_guardado)
            var_pass = ctk.StringVar(value=clave_guardada)

            ctk.CTkLabel(
                frame,
                text="Usuario",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=1, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_user,
                width=220,
                font=ctk.CTkFont(size=11),
            ).grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=4)

            ctk.CTkLabel(
                frame,
                text="Contraseña",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=2, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_pass,
                width=220,
                show="*",
                font=ctk.CTkFont(size=11),
            ).grid(row=2, column=1, sticky="ew", padx=(0, 14), pady=4)

            var_remember = ctk.BooleanVar(value=tiene_guardado)
            ctk.CTkSwitch(
                frame,
                text="  Recordar credenciales",
                variable=var_remember,
                font=ctk.CTkFont(size=11),
            ).grid(row=3, column=0, columnspan=2, sticky="w", padx=14, pady=(6, 12))

            self.campos[nombre] = {
                "usuario": var_user,
                "clave": var_pass,
                "recordar": var_remember,
            }

        # ──────────────────────────── Botones de acción ────────────────────────────

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=row_index + 1, column=0, sticky="e", padx=20, pady=(4, 16))
        btn_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self._cancelar,
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            width=100,
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            btn_frame,
            text="Continuar",
            command=self._confirmar,
            font=ctk.CTkFont(size=11, weight="bold"),
            width=100,
        ).pack(side="right")

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

# ── App principal (CustomTkinter) ─────────────────────────────────────


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("SSAuto — Automatización de capturas")
        self._credenciales_sesion = {}
        self.resizable(True, True)
        self._keybind_actual = None
        self._config = cargar_config()  # carga al iniciar
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)  # intercepta el cierre

        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        default_w = min(880, screen_w - 40)
        default_h = min(760, screen_h - 80)
        pos_x = max(0, (screen_w - default_w) // 2)
        pos_y = max(0, (screen_h - default_h) // 2)
        self.geometry(f"{default_w}x{default_h}+{pos_x}+{pos_y}")
        self.minsize(480, 400)

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

    # ── Helpers de UI ─────────────────────────────────────────────────

    def _section(self, parent, title, row, col=0, colspan=2, pady=(0, 10)):
        frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(
            row=row, column=col, columnspan=colspan, sticky="nsew", pady=pady, padx=0
        )
        parent.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(frame, fg_color=("gray88", "gray25"), height=28)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray30", "gray60"),
        ).pack(side="left", padx=14)

        body = ctk.CTkFrame(frame, fg_color="transparent")
        body.pack(fill="x", padx=14, pady=12)
        return body

    def _make_paste_entry(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            row,
            text="Pegar región:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))

        self.region_paste_var = ctk.StringVar(
            value="{'top': 392, 'left': 524, 'width': 934, 'height': 404}"
        )
        entry = ctk.CTkEntry(
            row,
            textvariable=self.region_paste_var,
            font=ctk.CTkFont(size=11),
        )
        entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        entry.bind("<FocusOut>", self._parse_region)
        entry.bind("<Return>", self._parse_region)
        self.region_paste = entry

        ctk.CTkButton(
            row,
            text="Aplicar",
            command=self._parse_region,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

    def _make_coords(self, parent):
        coords_frame = ctk.CTkFrame(parent, fg_color="transparent")
        coords_frame.pack(fill="x", pady=(0, 10))

        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        for i, (lbl, val) in enumerate(campos):
            box = ctk.CTkFrame(
                coords_frame,
                fg_color=("gray90", "gray25"),
                border_width=1,
            )
            box.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))

            ctk.CTkLabel(
                box,
                text=lbl.upper(),
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))

            var = ctk.IntVar(value=val)
            entry = ctk.CTkEntry(
                box,
                textvariable=var,
                width=70,
                font=ctk.CTkFont(size=13, weight="bold"),
                justify="center",
                border_width=0,
            )
            entry.pack(pady=(0, 6))
            var.trace_add("write", self._sync_paste)
            self.region_vars[lbl] = var

    def _make_sitios_status(self, parent):
        self._sitios_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self._sitios_frame.pack(fill="x", pady=(0, 8))
        self._actualizar_sitios_status()

        btns_row = ctk.CTkFrame(parent, fg_color="transparent")
        btns_row.pack(fill="x")
        ctk.CTkButton(
            btns_row,
            text="Credenciales",
            command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btns_row,
            text="Renovar sesión",
            command=self._renovar_sesion,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left")

        # ── Opciones ────────────────────────────

    def opciones(self, parent):
        self.headless_var = ctk.BooleanVar(value=False)
        self._toggle_row(
            parent, "Modo headless (sin ventana de Chrome)", self.headless_var
        )
        self._separador(parent)

        self.chrome_existente_var = ctk.BooleanVar(value=False)
        self._toggle_row(
            parent, "Usar Chrome ya abierto (puerto 9222)", self.chrome_existente_var
        )
        ctk.CTkButton(
            parent,
            text="Abrir Chrome con depuración",
            command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10),
            height=28,
        ).pack(anchor="e", pady=(4, 0))

        self._separador(parent)

        key_row = ctk.CTkFrame(parent, fg_color="transparent")
        key_row.pack(fill="x")
        ctk.CTkLabel(
            key_row,
            text="Atajo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            key_row,
            textvariable=self.keybind_var,
            font=ctk.CTkFont(size=11),
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            key_row,
            text="Aplicar",
            command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

        self.keybind_label = ctk.CTkLabel(
            parent,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        keybind_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(keybind_inicial, lambda e: self._ejecutar())
            self._keybind_actual = keybind_inicial
            self.keybind_var.set(keybind_inicial)
            legible = self._keybind_legible(keybind_inicial)
            self.keybind_label.configure(
                text=f"Combinación activa: {legible}",
                text_color=("green", "#3fb950"),
            )
        except Exception:
            self.keybind_label.configure(
                text="Atajo no válido",
                text_color=("red", "#f85149"),
            )

    # ── FIX #4: _font_exists usa families() correctamente ─────────────
    def _font_exists(self, name):
        return name in tkinter.font.families()

    # ── Build UI principal ────────────────────────────────────────────

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._scrollable_frame.grid_columnconfigure(0, weight=1)

        parent = self._scrollable_frame

        # ── 1. Región de captura ──────────────────────────────────────
        sec = self._section(parent, "  REGIÓN DE CAPTURA", row=0)
        self._make_paste_entry(sec)
        self._separador(sec)
        self._make_coords(sec)

        ctk.CTkButton(
            sec,
            text="  Medir región en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=11),
            height=32,
        ).pack(fill="x", pady=(4, 0))

        # ── 2. Sitios de destino ──────────────────────────────────────
        sec2 = self._section(parent, "  SITIOS DE DESTINO", row=1)
        self._make_sitios_status(sec2)

        # ── 3. Opciones ───────────────────────────────────────────────
        sec3 = self._section(parent, "  OPCIONES", row=2)
        self.opciones(sec3)

        # ── 4. Botón ejecutar ─────────────────────────────────────────
        self.btn = ctk.CTkButton(
            parent,
            text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=42,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.grid(row=3, column=0, sticky="ew", padx=0, pady=(8, 8))

        # ── 5. Log ────────────────────────────────────────────────────
        # FIX #2: _make_log_section eliminado; log_text se crea UNA sola vez aquí
        sec4 = self._section(parent, "  REGISTRO", row=4, pady=(0, 8))

        self.log_text = ctk.CTkTextbox(
            sec4,
            font=ctk.CTkFont(
                family=(
                    "Cascadia Code"
                    if self._font_exists("Cascadia Code")
                    else "Consolas"
                ),
                size=10,
            ),
            wrap="word",
            height=140,
        )
        self.log_text.pack(fill="both", expand=True)

        # FIX #3: configurar tags de color en el widget interno de Tk
        tb = self.log_text._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("arrow", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

        # ── 6. Barra de estado ────────────────────────────────────────
        # FIX #6: row=5 (consecutivo) en lugar de row=99
        self._make_status_bar(parent)

    def _toggle_row(self, parent, text, var):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)
        ctk.CTkSwitch(
            row,
            text=text,
            variable=var,
            font=ctk.CTkFont(size=11),
        ).pack(side="left")

    def _separador(self, parent):
        ctk.CTkFrame(parent, fg_color=("gray80", "gray30"), height=1).pack(
            fill="x", pady=10
        )

    def _actualizar_sitios_status(self):
        for w in self._sitios_frame.winfo_children():
            w.destroy()
        for sitio in SITIOS:
            nombre = sitio["nombre"]
            tiene_sesion = Path(f"cookies/{nombre.replace(' ', '_')}.pkl").exists()
            tiene_creds = bool(cargar_credenciales(nombre)[0])

            row = ctk.CTkFrame(
                self._sitios_frame,
                fg_color=("gray93", "gray25"),
                border_width=1,
            )
            row.pack(fill="x", pady=(0, 4))

            if not sitio["necesita_login"]:
                icono, estado, color = "○", "sin login", ("green", "#3fb950")
            elif tiene_sesion:
                icono, estado, color = "●", "sesión guardada", ("royalblue", "#79c0ff")
            elif tiene_creds:
                icono, estado, color = "◑", "credenciales OK", ("orange", "#d29922")
            else:
                icono, estado, color = "○", "sin configurar", ("red", "#f85149")

            ctk.CTkLabel(
                row,
                text=f" {icono} {nombre}",
                font=ctk.CTkFont(size=11),
            ).pack(side="left", padx=10, pady=6)

            ctk.CTkLabel(
                row,
                text=f"  {estado}  ",
                font=ctk.CTkFont(size=10),
                text_color=color,
            ).pack(side="right", padx=10, pady=6)

    # ── FIX #1 y #5: _make_status_bar usa .pack() en lugar de .grid(side=) ──
    def _make_status_bar(self, parent):
        # FIX #6: row=5 consecutivo al layout real
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.grid(row=5, column=0, sticky="ew", pady=(4, 0))

        self._status_dot = ctk.CTkLabel(
            status_frame,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=("#2ea043", "#3fb950"),
        )
        self._status_dot.pack(
            side="left"
        )  # FIX #1/#5: .pack() en lugar de .grid(side=)

        self.status_var = ctk.StringVar(value="Listo")
        ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(
            side="left", padx=(4, 0)
        )  # FIX #1/#5

        self._last_run_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._last_run_label.pack(side="right")  # FIX #1/#5

    # ── Helpers ───────────────────────────────────────────────────────

    def _keybind_legible(self, kb):
        return (
            kb.replace("<", "")
            .replace(">", "")
            .replace("Control", "Ctrl")
            .replace("Return", "Enter")
            .replace("-", "+")
        )

    def _parse_region(self, event=None):
        texto = self.region_paste_var.get().strip()
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
            self.region_paste_var.set(str(d))
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

    # ── FIX #3: _log usa el widget interno _textbox para tags de color ──
    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")

        if msg.startswith("✓"):
            tag = "ok"
        elif msg.startswith("✗"):
            tag = "error"
        elif msg.startswith("→") or msg.startswith("  →"):
            tag = "arrow"
        else:
            tag = "dim"

        self.log_text.configure(state="normal")
        tb = self.log_text._textbox  # widget tk.Text interno
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_status(self, text, color=None):
        self.status_var.set(text)
        dot_color = {
            "Listo": ("#2ea043", "#3fb950"),
            "Ejecutando...": ("#d29922", "#d29922"),
            "Completado": ("#2ea043", "#3fb950"),
            "Error": ("#f85149", "#f85149"),
        }.get(text, ("gray40", "gray60"))
        self._status_dot.configure(text_color=dot_color)

    def _ejecutar(self):
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_text.configure(state="normal")
        self.log_text.delete("0.0", "end")
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
            legible = self._keybind_legible(nuevo)
            self.keybind_label.configure(
                text=f"Combinación activa: {legible}",
                text_color=("green", "#3fb950"),
            )
            self._config["keybind"] = nuevo
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.configure(
                text=f"Atajo inválido: {e}",
                text_color=("red", "#f85149"),
            )
            self._keybind_actual = None

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
        self.keybind_var.set("<" + "-".join(partes) + ">")
        return "break"

    def _abrir_credenciales(self):
        win = LoginWindow(self, SITIOS)
        if win.confirmado:
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")
        self._actualizar_sitios_status()

    def _renovar_sesion(self):
        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

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
        self._log("→ Inicia sesión en los sitios y luego ejecuta la captura")

    # ── FIX #7 y #8: _proceso usa self.after() para toda actualización de UI ──
    def _proceso(self):
        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            ui(f"→ Capturando región: {region}")
            self.after(0, self.iconify)
            time.sleep(0.4)
            ruta = capturar(region)
            self.after(0, self.deiconify)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_chrome_existente = self.chrome_existente_var.get()
            for sitio in SITIOS:
                ui(f"→ Subiendo a: {sitio['nombre']}")
                # FIX #8: pasamos ui (thread-safe) como callback de log
                subir(
                    sitio,
                    ruta,
                    headless,
                    ui,
                    self._credenciales_sesion,
                    usar_chrome_existente,
                )
                ui("")

            ui("✓ Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            now = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._last_run_label.configure(text=f"Último proceso: {now}"),
            )
            self.after(0, self._actualizar_sitios_status)

        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ Error general: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        finally:
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _al_cerrar(self):
        guardar_config(self._config)
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

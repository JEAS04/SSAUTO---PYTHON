import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font
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

# ── Colores de la interfaz ────────────────────────────────────────────
COLORS = {
    "bg_dark": "#0d1117",
    "bg_panel": "#161b22",
    "bg_input": "#21262d",
    "bg_hover": "#30363d",
    "border": "#30363d",
    "border_focus": "#388bfd",
    "accent": "#388bfd",
    "accent_hover": "#1f6feb",
    "success": "#3fb950",
    "error": "#f85149",
    "warning": "#d29922",
    "info": "#79c0ff",
    "text_primary": "#e6edf3",
    "text_muted": "#8b949e",
    "text_dim": "#484f58",
    "btn_green": "#238636",
    "btn_green_hov": "#2ea043",
    "badge_ok_bg": "#1a4a2e",
    "badge_ok_fg": "#3fb950",
    "badge_ses_bg": "#0d2149",
    "badge_ses_fg": "#79c0ff",
    "badge_warn_bg": "#3d2900",
    "badge_warn_fg": "#d29922",
    "badge_err_bg": "#3d0c0c",
    "badge_err_fg": "#f85149",
}


# ── Toggle widget ─────────────────────────────────────────────────────
class Toggle(tk.Frame):
    def __init__(self, parent, variable, **kwargs):
        bg = kwargs.pop("bg", COLORS["bg_panel"])
        super().__init__(parent, bg=bg, **kwargs)
        self.var = variable
        self.canvas = tk.Canvas(self, width=44, height=22, highlightthickness=0, bg=bg)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._toggle)
        self.canvas.bind("<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.var.trace_add("write", self._dibujar)
        self._dibujar()

    def _toggle(self, _=None):
        self.var.set(not self.var.get())

    def _dibujar(self, *_):
        self.canvas.delete("all")
        on = self.var.get()
        track_color = COLORS["accent"] if on else COLORS["bg_hover"]
        # Track
        self.canvas.create_oval(1, 3, 19, 19, fill=track_color, outline="")
        self.canvas.create_oval(25, 3, 43, 19, fill=track_color, outline="")
        self.canvas.create_rectangle(10, 3, 34, 19, fill=track_color, outline="")
        # Thumb
        x = 30 if on else 13
        self.canvas.create_oval(x - 9, 2, x + 9, 20, fill="white", outline="")


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
    except:
        pass
    try:
        keyring.delete_password(keyring_APP, f"{sitio_nombre}_clave")
    except:
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
    options = webdriver.ChromeOptions()
    if usar_chrome_existente:
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


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


def subir(
    sitio,
    ruta_imagen,
    headless,
    log,
    credenciales_sesion=None,
    usar_chrome_existente=False,
):
    driver = crear_driver(headless, usar_chrome_existente)
    wait = WebDriverWait(driver, 15)
    nombre = sitio.get("nombre", "sitio")

    try:
        if sitio["necesita_login"]:
            if usar_chrome_existente:
                log(f"  → Verificando sesión activa en Chrome abierto para {nombre}...")
                driver.get(sitio["url_upload"])
                time.sleep(1.5)
                url_actual = driver.current_url.lower()
                if "login" in url_actual or "signin" in url_actual:
                    log(f"  ✗ No hay sesión activa en Chrome para {nombre}.")
                    log(
                        f"  → Inicia sesión manualmente en el navegador y vuelve a intentar."
                    )
                    return
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
        if usar_chrome_existente:
            pass
        else:
            driver.quit()


# ── Ventana de Login ──────────────────────────────────────────────────


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, sitios):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_dark"], padx=24, pady=24)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancelar)
        self.confirmado = False
        self._build_ui()
        self.transient(parent)
        self.wait_window()

    def _build_ui(self):
        # Título
        tk.Label(
            self,
            text="Configurar credenciales",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
        ).grid(row=0, column=0, columnspan=2, pady=(0, 18), sticky="w")

        self.campos = {}
        for i, sitio in enumerate(self.sitios):
            if not sitio.get("necesita_login"):
                continue
            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)

            # Frame del sitio
            frame = tk.Frame(
                self,
                bg=COLORS["bg_panel"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )
            frame.grid(
                row=i + 1,
                column=0,
                columnspan=2,
                sticky="ew",
                pady=(0, 12),
                ipadx=12,
                ipady=12,
            )

            tk.Label(
                frame,
                text=nombre,
                font=("Segoe UI", 10, "bold"),
                bg=COLORS["bg_panel"],
                fg=COLORS["accent"],
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 8))

            for row_i, (lbl_text, show, default) in enumerate(
                [
                    ("Usuario", "", usuario_guardado),
                    ("Contraseña", "*", clave_guardada),
                ],
                start=1,
            ):
                tk.Label(
                    frame,
                    text=lbl_text,
                    font=("Segoe UI", 9),
                    bg=COLORS["bg_panel"],
                    fg=COLORS["text_muted"],
                ).grid(row=row_i, column=0, sticky="e", padx=(12, 8), pady=4)
                var = tk.StringVar(value=default)
                entry = tk.Entry(
                    frame,
                    textvariable=var,
                    width=26,
                    show=show,
                    font=("Segoe UI", 9),
                    bg=COLORS["bg_input"],
                    fg=COLORS["text_primary"],
                    insertbackground=COLORS["text_primary"],
                    relief="flat",
                    bd=4,
                    highlightbackground=COLORS["border"],
                    highlightthickness=1,
                )
                entry.grid(row=row_i, column=1, padx=(0, 12), pady=4)
                if lbl_text == "Usuario":
                    var_user = var
                else:
                    var_pass = var

            var_remember = tk.BooleanVar(value=tiene_guardado)
            frame_tog = tk.Frame(frame, bg=COLORS["bg_panel"])
            frame_tog.grid(
                row=3, column=0, columnspan=2, sticky="w", padx=12, pady=(6, 10)
            )
            Toggle(frame_tog, var_remember, bg=COLORS["bg_panel"]).pack(side="left")
            tk.Label(
                frame_tog,
                text="  Recordar credenciales",
                font=("Segoe UI", 9),
                bg=COLORS["bg_panel"],
                fg=COLORS["text_muted"],
            ).pack(side="left")

            self.campos[nombre] = {
                "usuario": var_user,
                "clave": var_pass,
                "recordar": var_remember,
            }

        # Botones
        frame_btns = tk.Frame(self, bg=COLORS["bg_dark"])
        frame_btns.grid(row=99, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        self._make_btn(
            frame_btns, "Cancelar", self._cancelar, bg=COLORS["bg_panel"]
        ).pack(side="right", padx=(8, 0))
        self._make_btn(
            frame_btns,
            "Continuar",
            self._confirmar,
            bg=COLORS["accent"],
            fg=COLORS["bg_dark"],
        ).pack(side="right")

    def _make_btn(self, parent, text, cmd, bg=None, fg=None):
        bg = bg or COLORS["bg_panel"]
        fg = fg or COLORS["text_primary"]
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["text_primary"],
        )
        return btn

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


# ── App principal ─────────────────────────────────────────────────────


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("SSAuto — Automatización de capturas")
        self._credenciales_sesion = {}
        self.resizable(True, True)
        self.configure(bg=COLORS["bg_dark"])
        self._keybind_actual = None
        self._config = cargar_config()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        # ── Ajustar tamaño inicial sin salirse de la pantalla ──────────
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = min(self.winfo_reqwidth(), screen_w - 40)
        win_h = min(self.winfo_reqheight(), screen_h - 80)
        pos_x = max(0, (screen_w - win_w) // 2)
        pos_y = max(0, (screen_h - win_h) // 2)
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.minsize(380, 300)
        self.maxsize(screen_w, screen_h)

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
        frame = tk.Frame(
            parent,
            bg=COLORS["bg_panel"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=pady)
        parent.grid_columnconfigure(0, weight=1)

        header = tk.Frame(frame, bg=COLORS["bg_hover"])
        header.pack(fill="x")
        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["bg_hover"],
            fg=COLORS["text_muted"],
            padx=12,
            pady=6,
        ).pack(side="left")

        body = tk.Frame(frame, bg=COLORS["bg_panel"], padx=12, pady=10)
        body.pack(fill="x")
        return body

    def _label(self, parent, text, muted=False, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 9),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_muted"] if muted else COLORS["text_primary"],
            **kwargs,
        )

    def _entry(self, parent, var, width=20, show=""):
        return tk.Entry(
            parent,
            textvariable=var,
            width=width,
            show=show,
            font=("Segoe UI", 9),
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            relief="flat",
            bd=4,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )

    def _btn(self, parent, text, cmd, accent=False, small=False):
        bg = COLORS["accent"] if accent else COLORS["bg_input"]
        fg = COLORS["bg_dark"] if accent else COLORS["text_primary"]
        font_size = 8 if small else 9
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=bg,
            fg=fg,
            font=("Segoe UI", font_size),
            relief="flat",
            bd=0,
            padx=10 if small else 14,
            pady=4 if small else 6,
            cursor="hand2",
            activebackground=COLORS["accent_hover"],
            activeforeground="white",
        )
        return btn

    def _badge(self, parent, text, style="ok"):
        styles = {
            "ok": (COLORS["badge_ok_bg"], COLORS["badge_ok_fg"]),
            "ses": (COLORS["badge_ses_bg"], COLORS["badge_ses_fg"]),
            "warn": (COLORS["badge_warn_bg"], COLORS["badge_warn_fg"]),
            "err": (COLORS["badge_err_bg"], COLORS["badge_err_fg"]),
        }
        bg, fg = styles.get(style, styles["ok"])
        return tk.Label(
            parent, text=text, font=("Segoe UI", 8), bg=bg, fg=fg, padx=8, pady=2
        )

    def _separador(self, parent):
        tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", pady=8)

    # ── Build UI principal ────────────────────────────────────────────

    def _build_ui(self):

        # ── Contenedor scrolleable principal ──────────────────────────
        # Outer container to hold canvas + scrollbar, filling window
        outer = tk.Frame(self, bg=COLORS["bg_dark"])
        outer.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(outer, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview,
            bg=COLORS["bg_panel"],
            troughcolor=COLORS["bg_dark"],
            relief="flat",
        )
        self._scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])

        self._scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
            (0, 0),
            window=self._scrollable_frame,
            anchor="nw",
            width=canvas.winfo_reqwidth(),
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Store reference to unbind later if needed
        self._canvas = canvas
        self._scrollbar = scrollbar

        # Also update inner frame width when canvas resizes
        def _configure_canvas(event):
            canvas.itemconfig(1, width=event.width)  # item 1 is the window
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _configure_canvas)

        # ── Ahora construimos dentro de self._scrollable_frame ────────
        parent = self._scrollable_frame

        # Give scrollable_frame a grid layout
        parent.grid_columnconfigure(0, weight=1)

        # ── 1. Región de captura ──────────────────────────────────────
        sec = self._section(parent, "  REGIÓN DE CAPTURA", row=0)

        row0 = tk.Frame(sec, bg=COLORS["bg_panel"])
        row0.pack(fill="x", pady=(0, 6))
        self._label(row0, "Pegar región:", muted=True).pack(side="left", padx=(0, 8))
        self.region_paste_var = tk.StringVar(
            value="{'top': 392, 'left': 524, 'width': 934, 'height': 404}"
        )
        self.region_paste = self._entry(row0, self.region_paste_var, width=30)
        self.region_paste.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.region_paste.bind("<FocusOut>", self._parse_region)
        self.region_paste.bind("<Return>", self._parse_region)
        self._btn(row0, "Aplicar", self._parse_region, small=True).pack(side="left")

        self._separador(sec)

        # Coords
        coords_frame = tk.Frame(sec, bg=COLORS["bg_panel"])
        coords_frame.pack(fill="x", pady=(0, 8))
        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        for i, (lbl, val) in enumerate(campos):
            box = tk.Frame(
                coords_frame,
                bg=COLORS["bg_input"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )
            box.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))
            tk.Label(
                box,
                text=lbl.upper(),
                font=("Segoe UI", 7),
                bg=COLORS["bg_input"],
                fg=COLORS["text_dim"],
                pady=4,
            ).pack()
            var = tk.IntVar(value=val)
            tk.Entry(
                box,
                textvariable=var,
                width=6,
                font=("Segoe UI", 10, "bold"),
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                insertbackground=COLORS["text_primary"],
                relief="flat",
                bd=0,
                justify="center",
            ).pack(pady=(0, 6))
            var.trace_add("write", self._sync_paste)
            self.region_vars[lbl] = var

        self._btn(sec, "  Medir región en pantalla", self._lanzar_medidor).pack(
            fill="x", pady=(4, 0)
        )

        # ── 2. Sitios de destino ──────────────────────────────────────
        sec2 = self._section(parent, "  SITIOS DE DESTINO", row=1)
        self._sitios_frame = tk.Frame(sec2, bg=COLORS["bg_panel"])
        self._sitios_frame.pack(fill="x", pady=(0, 8))
        self._actualizar_sitios_status()

        btns_row = tk.Frame(sec2, bg=COLORS["bg_panel"])
        btns_row.pack(fill="x")
        self._btn(btns_row, "Credenciales", self._abrir_credenciales, small=True).pack(
            side="left", padx=(0, 6)
        )
        self._btn(btns_row, "Renovar sesión", self._renovar_sesion, small=True).pack(
            side="left"
        )

        # ── 3. Opciones ───────────────────────────────────────────────
        sec3 = self._section(parent, "  OPCIONES", row=2)

        self.headless_var = tk.BooleanVar(value=False)
        self._toggle_row(
            sec3, "Modo headless (sin ventana de Chrome)", self.headless_var
        )
        self._separador(sec3)

        self.chrome_existente_var = tk.BooleanVar(value=False)
        self._toggle_row(
            sec3, "Usar Chrome ya abierto (puerto 9222)", self.chrome_existente_var
        )
        self._btn(
            sec3, "Abrir Chrome con depuración", self._abrir_chrome_debug, small=True
        ).pack(anchor="e", pady=(4, 0))

        self._separador(sec3)

        # Keybind
        key_row = tk.Frame(sec3, bg=COLORS["bg_panel"])
        key_row.pack(fill="x")
        self._label(key_row, "Atajo:", muted=True).pack(side="left", padx=(0, 8))
        self.keybind_var = tk.StringVar()
        self.keybind_entry = self._entry(key_row, self.keybind_var, width=15)
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        self._btn(key_row, "Aplicar", self._aplicar_keybind, small=True).pack(
            side="left"
        )

        self.keybind_label = tk.Label(
            sec3,
            text="",
            font=("Segoe UI", 8),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_muted"],
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        keybind_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(keybind_inicial, lambda e: self._ejecutar())
            self._keybind_actual = keybind_inicial
            self.keybind_var.set(keybind_inicial)
            legible = self._keybind_legible(keybind_inicial)
            self.keybind_label.config(
                text=f"Combinación activa: {legible}", fg=COLORS["success"]
            )
        except Exception:
            self.keybind_label.config(text="Atajo no válido", fg=COLORS["error"])

        # ── 4. Botón ejecutar ─────────────────────────────────────────
        self.btn = tk.Button(
            parent,
            text="  Capturar y subir",
            command=self._ejecutar,
            bg=COLORS["btn_green"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            pady=10,
            cursor="hand2",
            activebackground=COLORS["btn_green_hov"],
            activeforeground="white",
        )
        self.btn.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(12, 8))

        # ── 5. Log ────────────────────────────────────────────────────
        sec4 = self._section(parent, "  REGISTRO", row=4, pady=(0, 8))

        self.log_text = tk.Text(
            sec4,
            height=6,
            width=64,
            state="disabled",
            font=(
                ("Cascadia Code", 9)
                if self._font_exists("Cascadia Code")
                else ("Consolas", 9)
            ),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            insertbackground="white",
            relief="flat",
            selectbackground=COLORS["bg_hover"],
            padx=8,
            pady=8,
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(
            sec4,
            command=self.log_text.yview,
            bg=COLORS["bg_panel"],
            troughcolor=COLORS["bg_dark"],
            relief="flat",
        )
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

        # Tags de color para el log
        self.log_text.tag_config("ok", foreground=COLORS["success"])
        self.log_text.tag_config("error", foreground=COLORS["error"])
        self.log_text.tag_config("arrow", foreground=COLORS["info"])
        self.log_text.tag_config("warn", foreground=COLORS["warning"])
        self.log_text.tag_config("dim", foreground=COLORS["text_muted"])
        self.log_text.tag_config("ts", foreground=COLORS["text_dim"])

        # ── 6. Barra de estado ────────────────────────────────────────
        status_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        status_frame.grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=(4, 0)
        )

        self._status_dot = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 10),
            bg=COLORS["bg_dark"],
            fg=COLORS["success"],
        )
        self._status_dot.pack(side="left")

        self.status_var = tk.StringVar(value="Listo")
        tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"],
        ).pack(side="left", padx=(4, 0))

        self._last_run_label = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 8),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_dim"],
        )
        self._last_run_label.pack(side="right")

    def _font_exists(self, name):
        try:
            tk.font.Font(family=name)
            return True
        except Exception:
            return False

    def _toggle_row(self, parent, text, var):
        row = tk.Frame(parent, bg=COLORS["bg_panel"])
        row.pack(fill="x", pady=3)
        Toggle(row, var, bg=COLORS["bg_panel"]).pack(side="left", padx=(0, 10))
        tk.Label(
            row,
            text=text,
            font=("Segoe UI", 9),
            bg=COLORS["bg_panel"],
            fg=COLORS["text_primary"],
        ).pack(side="left")

    def _actualizar_sitios_status(self):
        for w in self._sitios_frame.winfo_children():
            w.destroy()
        for sitio in SITIOS:
            nombre = sitio["nombre"]
            tiene_sesion = Path(f"cookies/{nombre.replace(' ', '_')}.pkl").exists()
            tiene_creds = bool(cargar_credenciales(nombre)[0])

            row = tk.Frame(
                self._sitios_frame,
                bg=COLORS["bg_input"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
            )
            row.pack(fill="x", pady=(0, 4))

            if not sitio["necesita_login"]:
                icono, estado, estilo = "○", "sin login", "ok"
            elif tiene_sesion:
                icono, estado, estilo = "●", "sesión guardada", "ses"
            elif tiene_creds:
                icono, estado, estilo = "◑", "credenciales OK", "warn"
            else:
                icono, estado, estilo = "○", "sin configurar", "err"

            tk.Label(
                row,
                text=f" {icono} {nombre}",
                font=("Segoe UI", 9),
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"],
                padx=8,
                pady=6,
            ).pack(side="left")
            self._badge(row, estado, estilo).pack(side="right", padx=8, pady=5)

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

    def _log(self, msg):
        self.log_text.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")

        # Tag según contenido
        if msg.startswith("✓"):
            tag = "ok"
        elif msg.startswith("✗"):
            tag = "error"
        elif msg.startswith("→") or msg.startswith("  →"):
            tag = "arrow"
        elif msg.strip() == "":
            tag = "dim"
        else:
            tag = "dim"

        self.log_text.insert("end", f"[{ts}] ", "ts")
        self.log_text.insert("end", msg + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_status(self, text, color=None):
        self.status_var.set(text)
        dot_color = {
            "Listo": COLORS["success"],
            "Ejecutando...": COLORS["warning"],
            "Completado": COLORS["success"],
            "Error": COLORS["error"],
        }.get(text, COLORS["text_muted"])
        self._status_dot.config(fg=dot_color)

    def _ejecutar(self):
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
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
            legible = self._keybind_legible(nuevo)
            self.keybind_label.config(
                text=f"Combinación activa: {legible}", fg=COLORS["success"]
            )
            self._config["keybind"] = nuevo
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.config(text=f"Atajo inválido: {e}", fg=COLORS["error"])
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

    def _proceso(self):
        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            self._log(f"→ Capturando región: {region}")
            self.after(0, self.iconify)
            time.sleep(0.4)
            ruta = capturar(region)
            self.after(0, self.deiconify)
            self._log(f"✓ Imagen guardada: {ruta}")
            self._log("")

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
            self._set_status("Completado")
            now = datetime.now().strftime("%H:%M:%S")
            self.after(
                0, lambda: self._last_run_label.config(text=f"Último proceso: {now}")
            )
            self.after(0, self._actualizar_sitios_status)

        except Exception as e:
            self._log(f"✗ Error general: {e}")
            self._set_status("Error")
        finally:
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _al_cerrar(self):
        guardar_config(self._config)
        self.destroy()


if __name__ == "__main__":
    App().mainloop()

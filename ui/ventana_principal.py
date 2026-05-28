"""
ui/ventana_principal.py — Ventana principal de SSAuto (refactorizada).

Cambios respecto a la versión anterior:
  - Ya no importa automatizacion.py directamente.
  - Usa SesionService.ejecutar_subida() para toda la lógica de subida.
  - Usa PluginRegistry.todos() para construir la lista de sitios.
  - La UI no sabe nada de Selenium ni de selectores CSS.
"""

import ast
import shutil
import subprocess
import sys
import threading
import tkinter.font
import time
from datetime import datetime
from pathlib import Path
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import cargar_auto_submit, guardar_auto_submit
from core.captura import CapturaService, ErrorCaptura
from core.plugin_registry import PluginRegistry
from services.sesion_service import SesionService
from config.configuracion import (
    PERFIL_POR_DEFECTO,
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
    obtener_monitores,
    obtener_nombres_monitores,
)
from config.credenciales import cargar_credenciales
from config.apps_captura import APPS_CAPTURA
from medidor import MEDIDOR_CODE
from ui.ventana_credenciales import VentanaCredenciales
from ui.custom_ctkframe import CustomCTkFrame

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

ctk.deactivate_automatic_dpi_awareness()


class App(CustomCTkFrame):
    """Ventana principal de SSAuto."""

    def __init__(self, parent):
        super().__init__(parent)
        self._credenciales_sesion = {}
        self._keybind_actual = None
        self._btns_apps = {}  # {nombre: CTkButton} — referencia para deshabilitar
        self._regiones_apps = {}  # {nombre: dict} — regiones efectivas por app
        self._config = cargar_config()
        self._ui_scale = self._calcular_ui_scale()
        config = cargar_config()
        ctk.set_appearance_mode(config.get("tema", "dark"))
        self._construir_ui()

        self.update_idletasks()

        # Abrir credenciales si falta alguna
        faltan_creds = any(
            p.necesita_login and not cargar_credenciales(p.nombre)[0]
            for p in PluginRegistry.con_login()
        )
        if faltan_creds:
            self.after(100, self._abrir_login_inicial)

    def _abrir_comparacion(self):
        from ui.ventana_comparacion import VentanaComparacion

        VentanaComparacion(self, log_callback=self._log)

    # ── UI ────────────────────────────────────────────────────────────

    def _construir_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._frame_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        pad = self._r(8, 16, 28)
        self._frame_scroll.grid(row=0, column=0, sticky="nsew", padx=pad, pady=pad)
        self._frame_scroll.grid_columnconfigure(0, weight=1)

        padre = self._frame_scroll

        sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0)
        self._crear_panel_perfiles(sec1)
        self._separador(sec1)
        self._crear_selector_monitor(sec1)
        self._separador(sec1)
        self._crear_coordenadas(sec1)
        ctk.CTkButton(
            sec1,
            text="  Medir región en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=self._fs(11)),
            height=self._r(32, 36, 44),
        ).pack(fill="x", pady=(4, 0))

        sec2 = self._seccion(padre, "  SITIOS DE DESTINO", fila=1)
        self._crear_sitios_status(sec2)

        sec3 = self._seccion(padre, "  OPCIONES", fila=2)
        self._crear_opciones(sec3)

        # ── Sección APLICACIONES (nueva) ──────────────────────────────
        sec_apps = self._seccion(padre, "  APLICACIONES DE CAPTURA", fila=3)
        self._crear_panel_apps(sec_apps)

        self.btn = ctk.CTkButton(
            padre,
            text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=self._fs(13), weight="bold"),
            height=self._r(42, 48, 58),
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.grid(row=4, column=0, sticky="ew", padx=0, pady=(8, 8))

        sec4 = self._seccion(padre, "  REGISTRO", fila=5, pady=(0, 8))
        self.log_texto = ctk.CTkTextbox(
            sec4,
            font=ctk.CTkFont(
                family=(
                    "Cascadia Code"
                    if self._fuente_existe("Cascadia Code")
                    else "Consolas"
                ),
                size=self._fs(10),
            ),
            wrap="word",
            height=self._r(140, 180, 260),
        )
        self.log_texto.pack(fill="both", expand=True)
        tb = self.log_texto._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("flecha", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

        self._crear_barra_estado(padre)

    def _seccion(self, padre, titulo, fila, col=0, colspan=2, pady=(0, 10)):
        frame = ctk.CTkFrame(padre, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(
            row=fila, column=col, columnspan=colspan, sticky="nsew", pady=pady, padx=0
        )
        padre.grid_columnconfigure(0, weight=1)
        enc = ctk.CTkFrame(
            frame, fg_color=("gray88", "gray25"), height=self._r(28, 32, 40)
        )
        enc.pack(fill="x")
        enc.pack_propagate(False)
        ctk.CTkLabel(
            enc,
            text=titulo,
            font=ctk.CTkFont(size=self._fs(11), weight="bold"),
            text_color=("gray30", "gray60"),
        ).pack(side="left", padx=self._r(14, 18, 28))
        cuerpo = ctk.CTkFrame(frame, fg_color="transparent")
        cuerpo.pack(fill="x", padx=self._r(14, 20, 32), pady=self._r(12, 16, 24))
        return cuerpo

    def _calcular_ui_scale(self) -> float:
        top = self.winfo_toplevel()
        sw, sh = top.winfo_screenwidth(), top.winfo_screenheight()
        return min(1.45, max(1.0, min(sw / 1920, sh / 1080)))

    def _r(self, base: int, mid: int | None = None, maximo: int | None = None) -> int:
        valor = int(round((mid if mid is not None else base) * self._ui_scale))
        return min(maximo or valor, max(base, valor))

    def _fs(self, base: int) -> int:
        return max(base, int(round(base * min(self._ui_scale, 1.28))))

    def _obtener_monitor_app(self, app: dict) -> int:
        """
        Devuelve el índice del monitor para una app.
        Primero busca en config guardada, si no existe usa el por defecto del app.
        """
        nombre = app["nombre"]
        config = cargar_config()
        monitores_guardados = config.get("monitores_apps", {})

        return monitores_guardados.get(nombre, app.get("monitor", 1))

    def _cambiar_monitor_app(self, app: dict, nombre_monitor: str):
        """
        Guarda el monitor elegido para una app en config.json.
        Se dispara cuando el usuario cambia el dropdown.
        """
        nombre = app["nombre"]
        nombres = obtener_nombres_monitores()

        try:
            indice = nombres.index(nombre_monitor)
        except ValueError:
            self._log(f"[✗] Monitor no válido: {nombre_monitor}")
            return

        config = cargar_config()
        if "monitores_apps" not in config:
            config["monitores_apps"] = {}

        config["monitores_apps"][nombre] = indice
        guardar_config(config)

        self._log(f"✓ Monitor de '{nombre}' → {nombre_monitor}")

    def _crear_panel_perfiles(self, padre):
        self._perfiles = cargar_perfiles()

        fila_selector = ctk.CTkFrame(padre, fg_color="transparent")
        fila_selector.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            fila_selector,
            text="Perfil:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self._perfil_var = ctk.StringVar(value="— sin perfiles —")
        self._perfil_menu = ctk.CTkOptionMenu(
            fila_selector,
            variable=self._perfil_var,
            values=self._nombres_perfiles(),
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False,
            width=220,
        )
        self._perfil_menu.pack(side="left", padx=(0, 8), fill="x", expand=True)
        ctk.CTkButton(
            fila_selector,
            text="Cargar",
            command=self._cargar_perfil_seleccionado,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

        fila_acciones = ctk.CTkFrame(padre, fg_color="transparent")
        fila_acciones.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            fila_acciones,
            text="Nombre:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self._perfil_nombre_var = ctk.StringVar()
        ctk.CTkEntry(
            fila_acciones,
            textvariable=self._perfil_nombre_var,
            placeholder_text="Ej: Monitor 1 — Panel izquierdo",
            font=ctk.CTkFont(size=11),
        ).pack(side="left", padx=(0, 8), fill="x", expand=True)
        ctk.CTkButton(
            fila_acciones,
            text="Guardar",
            command=self._guardar_perfil_actual,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            fila_acciones,
            text="Eliminar",
            command=self._eliminar_perfil_seleccionado,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="left")

        fila_pegar = ctk.CTkFrame(padre, fg_color="transparent")
        fila_pegar.pack(fill="x")
        ctk.CTkLabel(
            fila_pegar,
            text="Pegar región:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.region_paste_var = ctk.StringVar(value=str(PERFIL_POR_DEFECTO))
        entrada = ctk.CTkEntry(
            fila_pegar, textvariable=self.region_paste_var, font=ctk.CTkFont(size=11)
        )
        entrada.pack(side="left", padx=(0, 8), fill="x", expand=True)
        entrada.bind("<FocusOut>", self._parsear_region)
        entrada.bind("<Return>", self._parsear_region)
        self.region_paste = entrada
        ctk.CTkButton(
            fila_pegar,
            text="Aplicar",
            command=self._parsear_region,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

    def _crear_selector_monitor(self, padre):
        fila_monitor = ctk.CTkFrame(padre, fg_color="transparent")
        fila_monitor.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(
            fila_monitor,
            text="Monitor:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        nombres_monitores = obtener_nombres_monitores() or ["Monitor 1 (principal)"]
        monitor_guardado = int(self._config.get("ultimo_monitor", 1))
        valor_inicial = (
            nombres_monitores[monitor_guardado]
            if monitor_guardado < len(nombres_monitores)
            else nombres_monitores[0]
        )
        self._monitor_var = ctk.StringVar(value=valor_inicial)
        self._monitor_menu = ctk.CTkOptionMenu(
            fila_monitor,
            variable=self._monitor_var,
            values=nombres_monitores,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False,
            width=220,
        )
        self._monitor_menu.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self._monitor_info_label = ctk.CTkLabel(
            fila_monitor,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self._monitor_info_label.pack(side="left")
        self._monitor_var.trace_add("write", self._actualizar_info_monitor)
        self._actualizar_info_monitor()

    def _actualizar_info_monitor(self, *_):
        indice = self._monitor_var_indice()
        monitores = obtener_monitores()
        if 0 <= indice < len(monitores):
            m = monitores[indice]
            self._monitor_info_label.configure(text=f"{m['width']}×{m['height']} px")

    def _monitor_var_indice(self) -> int:
        nombres = obtener_nombres_monitores()
        try:
            return nombres.index(self._monitor_var.get())
        except ValueError:
            return 1

    def _nombres_perfiles(self) -> list[str]:
        nombres = list(self._perfiles.keys())
        return nombres if nombres else ["— sin perfiles —"]

    def _actualizar_menu_perfiles(self):
        nombres = self._nombres_perfiles()
        self._perfil_menu.configure(values=nombres)
        self._perfil_var.set(nombres[0])

    def _cargar_perfil_seleccionado(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._log("✗ No hay ningún perfil seleccionado.")
            return
        region = self._perfiles[nombre]
        self._aplicar_region(region)
        monitor_idx = region.get("monitor_index")
        if monitor_idx is not None:
            nombres = obtener_nombres_monitores()
            if 0 <= int(monitor_idx) < len(nombres):
                self._monitor_var.set(nombres[int(monitor_idx)])
        self._perfil_nombre_var.set(nombre)
        self._log(f"✓ Perfil cargado: «{nombre}» → {region}")

    def _guardar_perfil_actual(self):
        nombre = self._perfil_nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Nombre vacío", "Escribe un nombre para el perfil.")
            return
        region = {k: int(v.get() or 0) for k, v in self.region_vars.items()}
        region["monitor_index"] = self._monitor_var_indice()
        perfiles = cargar_perfiles()
        perfiles[nombre] = region
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._actualizar_menu_perfiles()
        self._perfil_var.set(nombre)
        self._log(f"✓ Perfil guardado: «{nombre}» → {region}")

    def _eliminar_perfil_seleccionado(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._log("✗ No hay ningún perfil seleccionado para eliminar.")
            return
        if not messagebox.askyesno(
            "Eliminar perfil", f"¿Eliminar el perfil «{nombre}»?"
        ):
            return
        perfiles = cargar_perfiles()
        perfiles.pop(nombre, None)
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._actualizar_menu_perfiles()
        self._log(f"✓ Perfil eliminado: «{nombre}»")

    def _crear_coordenadas(self, padre):
        frame_coords = ctk.CTkFrame(padre, fg_color="transparent")
        frame_coords.pack(fill="x", pady=(0, 10))
        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]
        for i, (etiqueta, valor) in enumerate(campos):
            caja = ctk.CTkFrame(
                frame_coords, fg_color=("gray90", "gray25"), border_width=1
            )
            caja.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))
            ctk.CTkLabel(
                caja,
                text=etiqueta.upper(),
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))
            var = ctk.StringVar(value=str(valor))
            ctk.CTkEntry(
                caja,
                textvariable=var,
                width=70,
                font=ctk.CTkFont(size=13, weight="bold"),
                justify="center",
                border_width=0,
            ).pack(pady=(0, 6))
            var.trace_add("write", self._sincronizar_paste)
            self.region_vars[etiqueta] = var

    def _crear_sitios_status(self, padre):
        self._frame_sitios = ctk.CTkFrame(padre, fg_color="transparent")
        self._frame_sitios.pack(fill="x", pady=(0, 8))
        self._actualizar_sitios_status()

        fila_botones = ctk.CTkFrame(padre, fg_color="transparent")
        fila_botones.pack(fill="x")
        ctk.CTkButton(
            fila_botones,
            text="Credenciales",
            command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            fila_botones,
            text="Renovar sesión",
            command=self._renovar_sesion,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left")

    def _crear_opciones(self, padre):
        self.destino_var = ctk.StringVar(value="AMBOS")
        fila_destino = ctk.CTkFrame(padre, fg_color="transparent")
        fila_destino.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            fila_destino,
            text="Subir a:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            width=60,
            anchor="w",
        ).pack(side="left", padx=(0, 8))

        self._btns_destino = {}
        opciones = PluginRegistry.nombres() + ["AMBOS"]
        for opcion in opciones:
            btn = ctk.CTkButton(
                fila_destino,
                text=opcion,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=88,
                height=28,
                corner_radius=6,
                fg_color=("#1f6aa5", "#1f6aa5"),
                hover_color=("#144e7a", "#144e7a"),
            )
            btn.pack(side="left", padx=(0, 4))
            self._btns_destino[opcion] = btn
            btn.configure(command=lambda o=opcion: self._seleccionar_destino(o))
        self._seleccionar_destino("AMBOS")
        self._separador(padre)

        self.headless_var = ctk.BooleanVar(value=False)
        self._fila_toggle(padre, "Modo sin ventana de Chrome", self.headless_var)
        self._separador(padre)

        self.chrome_existente_var = ctk.BooleanVar(value=True)
        fila_chrome = ctk.CTkFrame(padre, fg_color="transparent")
        fila_chrome.pack(fill="x", pady=(4, 0))
        ctk.CTkSwitch(
            fila_chrome,
            text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var,
            font=ctk.CTkFont(size=11),
        ).pack(side="left", expand=True, anchor="w")
        ctk.CTkButton(
            fila_chrome,
            text="Abrir Chrome con depuración",
            command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10),
            height=28,
        ).pack(side="right")
        self._separador(padre)

        self.auto_submit_var = ctk.BooleanVar(value=cargar_auto_submit())
        self._fila_toggle(padre, "Auto-submit nota (HubSpot)", self.auto_submit_var)
        self.auto_submit_var.trace_add(
            "write", lambda *_: guardar_auto_submit(self.auto_submit_var.get())
        )
        self._separador(padre)

        # ── FSD (Búsqueda inteligente) ────────────────────────────────
        self.usar_fsd_var = ctk.BooleanVar(value=False)
        fila_fsd_toggle = ctk.CTkFrame(padre, fg_color="transparent")
        fila_fsd_toggle.pack(fill="x", pady=(4, 0))
        ctk.CTkSwitch(
            fila_fsd_toggle,
            text="Búsqueda inteligente por FSD",
            variable=self.usar_fsd_var,
            font=ctk.CTkFont(size=11),
            command=self._actualizar_estado_fsd,
        ).pack(side="left", expand=True, anchor="w")

        fila_fsd = ctk.CTkFrame(padre, fg_color="transparent")
        fila_fsd.pack(fill="x", pady=(4, 0))
        ctk.CTkLabel(
            fila_fsd,
            text="FSD:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.fsd_var = ctk.StringVar(value="")
        self.fsd_entry = ctk.CTkEntry(
            fila_fsd,
            textvariable=self.fsd_var,
            placeholder_text="Ej: 980124 o FSD-980124",
            font=ctk.CTkFont(size=11),
            state="disabled",
        )
        self.fsd_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        ctk.CTkButton(
            fila_fsd,
            text="Limpiar",
            command=self._limpiar_fsd,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
            state="disabled",
        ).pack(side="left")
        self.fsd_btn_limpiar = fila_fsd.winfo_children()[-1]
        self._separador(padre)

        fila_atajo = ctk.CTkFrame(padre, fg_color="transparent")
        fila_atajo.pack(fill="x")
        ctk.CTkLabel(
            fila_atajo,
            text="Atajo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            fila_atajo, textvariable=self.keybind_var, font=ctk.CTkFont(size=11)
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            fila_atajo,
            text="Aplicar",
            command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")
        self.keybind_label = ctk.CTkLabel(
            padre, text="", font=ctk.CTkFont(size=10), text_color=("gray40", "gray60")
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        atajo_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(atajo_inicial, lambda e: self._ejecutar())
            self._keybind_actual = atajo_inicial
            self.keybind_var.set(atajo_inicial)
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(atajo_inicial)}",
                text_color=("green", "#3fb950"),
            )
        except Exception:
            self.keybind_label.configure(
                text="Atajo no válido", text_color=("red", "#f85149")
            )

    def _seleccionar_destino(self, opcion: str):
        self.destino_var.set(opcion)
        for nombre, btn in self._btns_destino.items():
            if nombre == opcion:
                btn.configure(
                    fg_color=("#238636", "#2ea043"), hover_color=("#1e7a30", "#26963a")
                )
            else:
                btn.configure(
                    fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40")
                )

    # ── Panel de aplicaciones de captura ─────────────────────────────

    def _crear_panel_apps(self, padre):
        ctk.CTkLabel(
            padre,
            text="Un clic → captura la región de esa app y la sube al destino activo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        self._btns_apps = {}
        self._regiones_apps = {}

        config_actual = cargar_config()
        regiones_guardadas = config_actual.get("regiones_apps", {})
        for app in APPS_CAPTURA:
            nombre = app["nombre"]
            icono = app.get("icono", "")
            color_base = app.get("color", ("#1f6aa5", "#1a5496"))

            region_efectiva = regiones_guardadas.get(nombre, app["region"])
            self._regiones_apps[nombre] = region_efectiva

            fila = ctk.CTkFrame(padre, fg_color=("gray90", "gray22"), corner_radius=8)
            fila.pack(fill="x", pady=3)
            fila.grid_columnconfigure(0, weight=1)  # El botón main ocupa lo máximo

            # ═══ FILA 1: Botón principal (full width) ═══
            r = region_efectiva
            tooltip = f"{r['width']}×{r['height']} px"
            btn_main = ctk.CTkButton(
                fila,
                text=f"{icono}  {nombre}   ▶  Capturar y subir   ({tooltip})",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=38,
                corner_radius=7,
                anchor="w",
                fg_color=color_base,
                hover_color=(
                    self._oscurecer(color_base[0]),
                    self._oscurecer(color_base[1]),
                ),
                command=lambda a=app: self._ejecutar_app(a),
            )
            btn_main.grid(
                row=0, column=0, columnspan=3, padx=6, pady=(5, 2), sticky="ew"
            )
            self._btns_apps[nombre] = btn_main

            # ═══ FILA 2: Dropdown + Botón ⚙ ═══
            nombres_monitores = obtener_nombres_monitores()
            monitor_actual = self._obtener_monitor_app(app)
            nombre_monitor_actual = (
                nombres_monitores[monitor_actual]
                if 0 <= monitor_actual < len(nombres_monitores)
                else nombres_monitores[0]
            )

            dropdown_monitor = ctk.CTkComboBox(
                fila,
                values=nombres_monitores,
                variable=ctk.StringVar(value=nombre_monitor_actual),
                command=lambda sel, a=app: self._cambiar_monitor_app(a, sel),
                width=160,
                height=34,
                corner_radius=7,
                font=ctk.CTkFont(size=9),
                dropdown_font=ctk.CTkFont(size=9),
                state="readonly",
            )
            dropdown_monitor.grid(
                row=1, column=0, padx=(6, 4), pady=(2, 5), sticky="ew"
            )

            btn_cfg = ctk.CTkButton(
                fila,
                text="⚙",
                font=ctk.CTkFont(size=14),
                width=36,
                height=34,
                corner_radius=7,
                fg_color=("gray70", "gray35"),
                hover_color=("gray60", "gray45"),
                command=lambda a=app: self._medir_region_app(a),
            )
            btn_cfg.grid(row=1, column=2, padx=(0, 6), pady=(2, 5))

        # todos los botones en la misma fila :
        # for app in APPS_CAPTURA:
        #     nombre = app["nombre"]
        #     icono = app.get("icono", "")
        #     color_base = app.get("color", ("#1f6aa5", "#1a5496"))

        #     region_efectiva = regiones_guardadas.get(nombre, app["region"])
        #     self._regiones_apps[nombre] = region_efectiva

        #     fila = ctk.CTkFrame(padre, fg_color=("gray90", "gray22"), corner_radius=8)
        #     fila.pack(fill="x", pady=3)
        #     fila.grid_columnconfigure(0, weight=1)  # Botón main ocupa espacio restante

        #     r = region_efectiva
        #     tooltip = f"{r['width']}×{r['height']} px"
        #     btn_main = ctk.CTkButton(
        #         fila,
        #         text=f"{icono}  {nombre}   ▶  Capturar y subir   ({tooltip})",
        #         font=ctk.CTkFont(size=12, weight="bold"),
        #         height=38,
        #         corner_radius=7,
        #         anchor="w",
        #         fg_color=color_base,
        #         hover_color=(
        #             self._oscurecer(color_base[0]),
        #             self._oscurecer(color_base[1]),
        #         ),
        #         command=lambda a=app: self._ejecutar_app(a),
        #     )
        #     btn_main.grid(row=0, column=0, padx=(6, 4), pady=5, sticky="ew")
        #     self._btns_apps[nombre] = btn_main

        #     # Dropdown de monitor
        #     nombres_monitores = obtener_nombres_monitores()
        #     monitor_actual = self._obtener_monitor_app(app)
        #     nombre_monitor_actual = (
        #         nombres_monitores[monitor_actual]
        #         if 0 <= monitor_actual < len(nombres_monitores)
        #         else nombres_monitores[0]
        #     )

        #     dropdown_monitor = ctk.CTkComboBox(
        #         fila,
        #         values=nombres_monitores,
        #         variable=ctk.StringVar(value=nombre_monitor_actual),
        #         command=lambda sel, a=app: self._cambiar_monitor_app(a, sel),
        #         width=160,
        #         height=38,
        #         corner_radius=7,
        #         font=ctk.CTkFont(size=9),
        #         dropdown_font=ctk.CTkFont(size=9),
        #         state="readonly",
        #     )
        #     dropdown_monitor.grid(row=0, column=1, padx=4, pady=5)

        #     # Botón ⚙
        #     btn_cfg = ctk.CTkButton(
        #         fila,
        #         text="⚙",
        #         font=ctk.CTkFont(size=14),
        #         width=36,
        #         height=38,
        #         corner_radius=7,
        #         fg_color=("gray70", "gray35"),
        #         hover_color=("gray60", "gray45"),
        #         command=lambda a=app: self._medir_region_app(a),
        #     )
        #     btn_cfg.grid(row=0, column=2, padx=(0, 6), pady=5)

    # ── Lanzador de app ───────────────────────────────────────────────

    def _ejecutar_app(self, app: dict):
        nombre = app["nombre"]
        region = self._regiones_apps.get(nombre, app["region"])
        monitor_idx = self._obtener_monitor_app(app)

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.configure(state="normal")
        self.log_texto.delete("0.0", "end")
        self.log_texto.configure(state="disabled")

        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando {region['width']}×{region['height']} px…"
        )

        threading.Thread(
            target=self._proceso_app,
            args=(app, region, monitor_idx),
            daemon=True,
        ).start()

    def _proceso_app(self, app: dict, region: dict, monitor_idx: int):
        nombre = app["nombre"]

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            ui(f"→ [{nombre}] Capturando {region['width']}×{region['height']} px…")

            # FIX #3: usar iconify_window() en lugar de self.iconify()
            # self.iconify() en un Frame lanza AttributeError; el wrapper
            # del CustomCTkFrame delega correctamente a winfo_toplevel().
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region, monitor=monitor_idx)
            ui(f"✓ [{nombre}] Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_existente = self.chrome_existente_var.get()
            auto_submit = self.auto_submit_var.get()
            destino = self.destino_var.get()
            fsd = self._obtener_fsd_actual()  # FSD para búsqueda inteligente

            plugins = (
                PluginRegistry.todos()
                if destino == "AMBOS"
                else (
                    [PluginRegistry.obtener(destino)]
                    if PluginRegistry.existe(destino)
                    else []
                )
            )
            if not plugins:
                ui(f"✗ No hay plugins para destino: {destino}")

            for plugin in plugins:
                ui(f"→ [{nombre}] Subiendo a {plugin.nombre}…")
                SesionService.ejecutar_subida(
                    nombre_plugin=plugin.nombre,
                    ruta_imagen=ruta,
                    log=ui,
                    headless=headless,
                    usar_chrome_existente=usar_existente,
                    credenciales_sesion=self._credenciales_sesion,
                    opciones={"auto_submit_nota": auto_submit},
                    fsd=fsd,
                )
                ui("")

            ui(f"✓ [{nombre}] Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            ahora = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._label_ultimo_proceso.configure(
                    text=f"Último proceso: {nombre} {ahora}"
                ),
            )
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✓ {nombre} — completado a las {ahora}"
                ),
            )
            self.after(0, self._actualizar_sitios_status)

        except ErrorCaptura as e:
            self.after(
                0, lambda err=e: self._log(f"✗ [{nombre}] Error de captura: {err}")
            )
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error de captura"
                ),
            )
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ [{nombre}] Error: {err}"))
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(text=f"  ✗ {nombre} — error"),
            )
        finally:
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, self._rehabilitar_btns_apps)

    def _rehabilitar_btns_apps(self):
        for btn in self._btns_apps.values():
            btn.configure(state="normal")

    # ── Medidor de región por app ─────────────────────────────────────

    def _medir_region_app(self, app: dict):
        nombre = app["nombre"]
        monitor_idx = self._obtener_monitor_app(app)

        self._log(f"→ Midiendo región para {nombre}…")
        self._label_estado_app.configure(
            text=f"  ⏳ Medí la región de {nombre} en pantalla…"
        )

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")

        # FIX #2: usar el wrapper iconify_window() en vez de
        # winfo_toplevel().iconify() directamente (que no va por after
        # y se llama en el hilo principal, lo cual estaba bien, pero
        # ahora es consistente con el resto de la clase).
        self.iconify_window()

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()

            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    try:
                        nueva_region = ast.literal_eval(linea.split("=", 1)[1].strip())

                        self._regiones_apps[nombre] = nueva_region

                        cfg = cargar_config()
                        cfg.setdefault("regiones_apps", {})[nombre] = nueva_region
                        guardar_config(cfg)

                        def _actualizar_ui(n=nombre, r=nueva_region):
                            if n in self._btns_apps:
                                tooltip = f"{r['width']}×{r['height']} px"
                                btn = self._btns_apps[n]
                                icono = next(
                                    (
                                        a["icono"]
                                        for a in APPS_CAPTURA
                                        if a["nombre"] == n
                                    ),
                                    "",
                                )
                                color_base = next(
                                    (
                                        a["color"]
                                        for a in APPS_CAPTURA
                                        if a["nombre"] == n
                                    ),
                                    ("#1f6aa5", "#1a5496"),
                                )
                                btn.configure(
                                    text=f"{icono}  {n}   ▶  Capturar y subir   ({tooltip})",
                                    fg_color=color_base,
                                )
                            self._label_estado_app.configure(
                                text=f"  ✓ {n} — nueva región: {r['width']}×{r['height']} px guardada"
                            )
                            self._log(f"✓ Región de {n} actualizada: {r}")

                        self.after(0, _actualizar_ui)
                        self.after(0, self.deiconify_window)  # FIX #1: sin ()
                        self.after(0, self._rehabilitar_btns_apps)
                        self.after(0, lambda: self.btn.configure(state="normal"))
                        return
                    except Exception as ex:
                        self.after(
                            0,
                            lambda e=ex: self._log(f"✗ No se pudo leer la región: {e}"),
                        )

            self.after(0, lambda: self._log(f"✗ Medición cancelada para {nombre}."))
            self.after(0, lambda: self._label_estado_app.configure(text=""))
            self.after(
                0, self.deiconify_window
            )  # FIX #1: sin () — antes era deiconify_window()
            self.after(0, self._rehabilitar_btns_apps)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    @staticmethod
    def _oscurecer(color_hex: str, factor: float = 0.80) -> str:
        try:
            h = color_hex.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return "#{:02x}{:02x}{:02x}".format(
                max(0, int(r * factor)),
                max(0, int(g * factor)),
                max(0, int(b * factor)),
            )
        except Exception:
            return "#444444"

    def _crear_barra_estado(self, padre):
        frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        frame_estado.grid(row=6, column=0, sticky="ew", pady=(4, 0))
        self._punto_estado = ctk.CTkLabel(
            frame_estado,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=("#2ea043", "#3fb950"),
        )
        self._punto_estado.pack(side="left")
        self.status_var = ctk.StringVar(value="Listo")
        ctk.CTkLabel(
            frame_estado,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(4, 0))
        self._label_estado_app = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_estado_app.pack(side="left", padx=(12, 0), fill="x", expand=True)
        self._label_ultimo_proceso = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_ultimo_proceso.pack(side="right")

    # ── Helpers UI ────────────────────────────────────────────────────

    def _fila_toggle(self, padre, texto, var):
        fila = ctk.CTkFrame(padre, fg_color="transparent")
        fila.pack(fill="x", pady=4)
        ctk.CTkSwitch(fila, text=texto, variable=var, font=ctk.CTkFont(size=11)).pack(
            side="left"
        )

    def _separador(self, padre):
        ctk.CTkFrame(padre, fg_color=("gray80", "gray30"), height=1).pack(
            fill="x", pady=10
        )

    def _fuente_existe(self, nombre):
        return nombre in tkinter.font.families()

    def _keybind_legible(self, kb):
        return (
            kb.replace("<", "")
            .replace(">", "")
            .replace("Control", "Ctrl")
            .replace("Return", "Enter")
            .replace("-", "+")
        )

    def _actualizar_estado_fsd(self):
        """Habilita/deshabilita el campo FSD según el switch."""
        if self.usar_fsd_var.get():
            self.fsd_entry.configure(state="normal")
            self.fsd_btn_limpiar.configure(state="normal")
            self._log("✓ Búsqueda inteligente por FSD activada.")
        else:
            self.fsd_entry.configure(state="disabled")
            self.fsd_btn_limpiar.configure(state="disabled")
            self.fsd_var.set("")
            self._log("✗ Búsqueda inteligente por FSD desactivada.")

    def _limpiar_fsd(self):
        """Limpia el campo FSD."""
        self.fsd_var.set("")
        self._log("✓ Campo FSD limpiado.")

    def _obtener_fsd_actual(self) -> str | None:
        """Devuelve el FSD si está habilitado, None en caso contrario."""
        if not self.usar_fsd_var.get():
            return None
        fsd = self.fsd_var.get().strip()
        return fsd if fsd else None

    # ── Sitios status ─────────────────────────────────────────────────

    def _actualizar_sitios_status(self):
        for widget in self._frame_sitios.winfo_children():
            widget.destroy()

        for plugin in PluginRegistry.todos():
            nombre = plugin.nombre
            tiene_sesion = Path(f"cookies/{nombre.replace(' ', '_')}.pkl").exists()
            tiene_creds = bool(cargar_credenciales(nombre)[0])

            fila = ctk.CTkFrame(
                self._frame_sitios, fg_color=("gray93", "gray25"), border_width=1
            )
            fila.pack(fill="x", pady=(0, 4))

            if not plugin.necesita_login:
                icono, estado, color = "○", "sin login", ("green", "#3fb950")
            elif tiene_sesion:
                icono, estado, color = "●", "sesión guardada", ("royalblue", "#79c0ff")
            elif tiene_creds:
                icono, estado, color = "◑", "credenciales OK", ("orange", "#d29922")
            else:
                icono, estado, color = "○", "sin configurar", ("red", "#f85149")

            ctk.CTkLabel(
                fila, text=f" {icono} {nombre}", font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(
                fila, text=f"  {estado}  ", font=ctk.CTkFont(size=10), text_color=color
            ).pack(side="right", padx=10, pady=6)

    # ── Log ───────────────────────────────────────────────────────────

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        tag = (
            "ok"
            if msg.startswith("✓")
            else "error" if msg.startswith("✗") else "flecha" if "→" in msg else "dim"
        )
        self.log_texto.configure(state="normal")
        tb = self.log_texto._textbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.log_texto.see("end")
        self.log_texto.configure(state="disabled")

    def _set_status(self, texto: str):
        self.status_var.set(texto)
        colores = {
            "Listo": ("#2ea043", "#3fb950"),
            "Ejecutando...": ("#d29922", "#d29922"),
            "Completado": ("#2ea043", "#3fb950"),
            "Error": ("#f85149", "#f85149"),
        }
        self._punto_estado.configure(
            text_color=colores.get(texto, ("gray40", "gray60"))
        )

    # ── Medidor ───────────────────────────────────────────────────────

    def _lanzar_medidor(self):
        monitor_idx = self._monitor_var_indice()
        self._log(f"→ Abre el medidor en {self._monitor_var.get()}…")
        self.btn.configure(state="disabled")
        self.winfo_toplevel().iconify()

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()
            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    try:
                        region = ast.literal_eval(linea.split("=", 1)[1].strip())
                        self.after(0, lambda r=region: self._aplicar_region(r))
                        self.after(0, self.deiconify)
                        return
                    except Exception:
                        pass
            self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region: dict):
        for clave in ("top", "left", "width", "height"):
            if clave in region:
                self.region_vars[clave].set(int(region[clave]))
        self.region_paste_var.set(
            str({k: v.get() for k, v in self.region_vars.items()})
        )
        self._log(f"✓ Región actualizada: {region}")
        self.btn.configure(state="normal")

    def _obtener_region_validada(self) -> dict:
        region = {}
        for clave, var in self.region_vars.items():
            texto = var.get().strip()
            if not texto:
                raise ValueError(f"El campo '{clave}' está vacío.")
            try:
                region[clave] = int(texto)
            except ValueError:
                raise ValueError(f"El campo '{clave}' debe ser un número entero.")
        if region["width"] <= 0:
            raise ValueError("Width debe ser mayor que 0.")
        if region["height"] <= 0:
            raise ValueError("Height debe ser mayor que 0.")
        return region

    def _parsear_region(self, event=None):
        texto = self.region_paste_var.get().strip()
        if "=" in texto:
            texto = texto.split("=", 1)[1].strip()
        try:
            region = ast.literal_eval(texto)
            for clave in ("top", "left", "width", "height"):
                if clave in region:
                    self.region_vars[clave].set(int(region[clave]))
        except Exception:
            messagebox.showerror(
                "Formato inválido",
                "Pega el diccionario con el formato:\n"
                "{'top': 392, 'left': 524, 'width': 934, 'height': 404}",
            )

    def _sincronizar_paste(self, *_):
        try:
            self.region_paste_var.set(
                str({k: v.get() for k, v in self.region_vars.items()})
            )
        except Exception:
            pass

    # ── Sesión ────────────────────────────────────────────────────────

    def _abrir_login_inicial(self):
        sitios_compat = [
            {"nombre": p.nombre, "necesita_login": p.necesita_login}
            for p in PluginRegistry.con_login()
        ]
        win = VentanaCredenciales(self, sitios_compat)
        self.wait_window(win)
        if getattr(win, "confirmado", False):
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")

    def _abrir_credenciales(self):
        sitios_compat = [
            {"nombre": p.nombre, "necesita_login": p.necesita_login}
            for p in PluginRegistry.con_login()
        ]
        win = VentanaCredenciales(self, sitios_compat)
        self.wait_window(win)
        if getattr(win, "confirmado", False):
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")
        self._actualizar_sitios_status()

    def _renovar_sesion(self):
        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

    def _abrir_chrome_debug(self):
        from core.browser import puerto_activo

        if puerto_activo():
            self._log("✓ Chrome con depuración ya está activo en el puerto 9222.")
            return
        rutas = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_exe = next((r for r in rutas if Path(r).exists()), None)
        if not chrome_exe:
            self._log(
                "✗ No se encontró Chrome. Ábrelo manualmente con --remote-debugging-port=9222"
            )
            return
        import subprocess

        subprocess.Popen(
            [
                chrome_exe,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome_sesion_ssauto",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222.")

    # ── Keybind ───────────────────────────────────────────────────────

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
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(nuevo)}",
                text_color=("green", "#3fb950"),
            )
            self._config["keybind"] = nuevo
            cfg = cargar_config()
            cfg["keybind"] = nuevo
            guardar_config(cfg)
        except Exception as e:
            self.keybind_label.configure(
                text=f"Atajo inválido: {e}", text_color=("red", "#f85149")
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

    # ── Proceso principal ─────────────────────────────────────────────

    def _ejecutar(self):
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.configure(state="normal")
        self.log_texto.delete("0.0", "end")
        self.log_texto.configure(state="disabled")
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = self._obtener_region_validada()
            ui(f"→ Capturando región en {self._monitor_var.get()}: {region}")
            self.after(0, self.iconify)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_existente = self.chrome_existente_var.get()
            auto_submit = self.auto_submit_var.get()
            destino = self.destino_var.get()
            fsd = self._obtener_fsd_actual()  # FSD para búsqueda inteligente

            if destino == "AMBOS":
                plugins = PluginRegistry.todos()
            else:
                plugins = (
                    [PluginRegistry.obtener(destino)]
                    if PluginRegistry.existe(destino)
                    else []
                )

            if not plugins:
                ui(f"✗ No hay plugins registrados para: {destino}")

            for plugin in plugins:
                ui(f"→ Subiendo a: {plugin.nombre}")
                resultado = SesionService.ejecutar_subida(
                    nombre_plugin=plugin.nombre,
                    ruta_imagen=ruta,
                    log=ui,
                    headless=headless,
                    usar_chrome_existente=usar_existente,
                    credenciales_sesion=self._credenciales_sesion,
                    opciones={"auto_submit_nota": auto_submit},
                    fsd=fsd,
                )
                ui("")

            ui("✓ Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            ahora = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._label_ultimo_proceso.configure(
                    text=f"Último proceso: {ahora}"
                ),
            )
            self.after(0, self._actualizar_sitios_status)

        except ErrorCaptura as e:
            self.after(0, lambda err=e: self._log(f"✗ Error de captura: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ Error general: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        finally:
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _al_cerrar(self):
        cfg = cargar_config()
        cfg["ultimo_monitor"] = self._monitor_var_indice()
        guardar_config(cfg)
        self._config = cfg
        self.destroy()

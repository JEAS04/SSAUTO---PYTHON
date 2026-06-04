"""
ui/ventana_principal.py — Ventana principal de SSAuto (refactorizada).

Cambios respecto a la versión anterior:
  - Ya no importa automatizacion.py directamente.
  - Usa SesionService.ejecutar_subida() para toda la lógica de subida.
  - Usa PluginRegistry.todos() para construir la lista de sitios.
  - La UI no sabe nada de Selenium ni de selectores CSS.
"""

import ast
import os
import shutil
import threading
import tkinter.font
import time
from datetime import datetime
from pathlib import Path
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import (
    cargar_auto_submit,
    guardar_auto_submit,
    cargar_headless,
    guardar_headless,
    cargar_chrome_existente,
    guardar_chrome_existente,
    cargar_destino_subida,
    guardar_destino_subida,
)
from core.captura import CapturaService, ErrorCaptura
from core.plugin_registry import PluginRegistry
from services.sesion_service import SesionService
from config.configuracion import (
    PERFIL_POR_DEFECTO,
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
)
from core.monitors import (
    obtener_monitores,
    obtener_nombres_monitores,
)
from config.credenciales import cargar_credenciales
from config.credenciales import _COOKIES_DIR as COOKIES_DIR
from config.apps_captura import APPS_CAPTURA
from core.medidor_runner import ejecutar_medidor
from ui.ventana_credenciales import VentanaCredenciales
from ui.custom_ctkframe import CustomCTkFrame
from ui.widgets.log_widget import LogWidget
from utils.colors import oscurecer
from utils.fsd import normalizar_fsd
from scraping.sunrun import ScraperSunrun
from ui.widgets.coordinate_inputs import CoordinateInputsWidget
from ui.widgets.monitor_selector import MonitorSelectorWidget
from ui.widgets.profile_manager import ProfileManagerWidget

# ── Google Sheets (Calendar) ────────────────────────────────────────────
from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
)
from gsheets.data.sheets_api import GoogleSheetsClient

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
        self._proceso_en_curso = False  # anti-reentrada
        self._cancelado = threading.Event()  # cancelación del proceso principal
        self._fsd_detectado = None
        self._servicio = SesionService()
        ctk.set_appearance_mode(self._config.get("tema", "dark"))
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
        self._frame_scroll.grid_columnconfigure(
            1, weight=2, minsize=self._r(880, 980, 1120)
        )
        self._frame_scroll.grid_columnconfigure(2, weight=1)

        padre = self._frame_scroll

        sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0, col=1)
        self._crear_panel_captura(sec1)

        sec_apps = self._seccion(padre, "  APLICACIONES DE CAPTURA", fila=1, col=1)
        self._crear_panel_apps(sec_apps)

        sec2 = self._seccion(padre, "  DESTINO Y SESIÓN", fila=2, col=1)
        self._crear_panel_destino(sec2)

        sec3 = self._seccion(padre, "  CONFIGURACIÓN", fila=3, col=1)
        self._crear_opciones(sec3)

        sec4 = self._seccion(
            padre, "  REGISTRO", fila=4, col=1, pady=(0, 8)
        )
        fuente = (
            "Cascadia Code"
            if self._fuente_existe("Cascadia Code")
            else "Consolas"
        )
        self.log_texto = LogWidget(
            sec4,
            font=ctk.CTkFont(family=fuente, size=self._fs(10)),
            height=self._r(140, 180, 260),
        )
        self.log_texto.pack(fill="both", expand=True)

        self._crear_barra_estado(padre, col=1)

    def _seccion(self, padre, titulo, fila, col=0, pady=(0, 10)):
        """Crea una seccion con encabezado y borde para organizar la UI.

        Cada seccion es un CTkFrame con un encabezado gris y un cuerpo
        transparente donde se empaquetan los widgets hijos.

        Args:
            padre: widget padre (el CTkScrollableFrame).
            titulo: texto del encabezado.
            fila: fila en el grid del padre.
            col: columna en el grid del padre.
            pady: padding vertical de la seccion.

        Returns:
            CTkFrame interior (cuerpo) donde empaquetar los widgets.
        """
        frame = ctk.CTkFrame(padre, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(row=fila, column=col, sticky="ew", pady=pady)

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
        cuerpo.pack(
            fill="both", expand=True,
            padx=self._r(14, 20, 32), pady=self._r(12, 16, 24),
        )
        return cuerpo

    def _calcular_ui_scale(self) -> float:
        """Calcula un factor de escala entre 1.0 y 1.45 basado en la resolucion.

        Compara la pantalla actual con Full HD (1920x1080) para determinar
        cuanto escalar textos, paddings y tamaños de widgets. El factor se
        usa en _r() y _fs() para adaptar la UI a distintas resoluciones.
        """
        top = self.winfo_toplevel()
        sw, sh = top.winfo_screenwidth(), top.winfo_screenheight()
        return min(1.45, max(1.0, min(sw / 1920, sh / 1080)))

    def _r(self, base: int, mid: int | None = None, maximo: int | None = None) -> int:
        """Escala un valor de padding/tamaño segun la resolucion de pantalla.

        Args:
            base: valor minimo (se usa si mid es None).
            mid: valor a escalar (default: base).
            maximo: limite superior opcional.

        Returns:
            Entero escalado, nunca menor que base.
        """
        valor = int(round((mid if mid is not None else base) * self._ui_scale))
        return min(maximo or valor, max(base, valor))

    def _fs(self, base: int) -> int:
        """Escala un tamaño de fuente con tope de 1.28x para legibilidad.

        Args:
            base: tamaño de fuente base en puntos.

        Returns:
            Tamaño escalado, nunca menor que base.
        """
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

    def _crear_panel_captura(self, padre):
        self._perfiles = cargar_perfiles()
        self.region_vars = {}

        monitores_raw = obtener_monitores()
        nombres_monitores = obtener_nombres_monitores()
        monitor_guardado = int(self._config.get("ultimo_monitor", 1))

        # ── Row 0: Perfiles (left) | Monitor (right) ─────────────
        r0 = ctk.CTkFrame(padre, fg_color="transparent")
        r0.pack(fill="x", pady=(0, 4))
        r0.grid_columnconfigure((0, 1), weight=1)

        self._profile_widget = ProfileManagerWidget(
            r0,
            region_vars=self.region_vars,
            perfiles_iniciales=self._perfiles,
            on_cargar_perfil=self._on_cargar_perfil,
            on_guardar_perfil=self._on_guardar_perfil,
            on_eliminar_perfil=self._on_eliminar_perfil,
            on_aplicar_region=self._parsear_region,
            on_log=self._log,
        )
        self._profile_widget.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        self._monitor_widget = MonitorSelectorWidget(
            r0,
            nombres_monitores=nombres_monitores,
            monitores_raw=monitores_raw,
            indice_inicial=monitor_guardado,
            on_change=self._on_monitor_change,
        )
        self._monitor_widget.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        self._monitor_var = self._monitor_widget.monitor_var

        # ── Row 1: Coordenadas + Detener ──────────────────────────
        coord_row = ctk.CTkFrame(padre, fg_color="transparent")
        coord_row.pack(fill="x", pady=(2, 4))

        self._coord_widget = CoordinateInputsWidget(
            coord_row,
            valores_iniciales=PERFIL_POR_DEFECTO,
            on_change=self._on_coords_change,
        )
        self._coord_widget.pack(side="left", fill="x", expand=True)
        self.region_vars = self._coord_widget.region_vars

        self.btn_detener = ctk.CTkButton(
            coord_row, text="  Detener",
            command=self._detener,
            font=ctk.CTkFont(size=self._fs(11), weight="bold"),
            height=self._r(30, 34, 40),
            fg_color=("#d73a49", "#f85149"),
            hover_color=("#b6232e", "#da3633"),
            state="disabled",
        )
        self.btn_detener.pack(side="right", padx=(8, 0))

        # ── Row 2: Botones de accion ─────────────────────────────
        b_row = ctk.CTkFrame(padre, fg_color="transparent")
        b_row.pack(fill="x")
        ctk.CTkButton(
            b_row, text="  Medir region en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=self._fs(11)),
            height=self._r(32, 36, 44),
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray25"),
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.btn = ctk.CTkButton(
            b_row, text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=self._fs(12), weight="bold"),
            height=self._r(36, 42, 50),
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.pack(side="right", fill="x", expand=True, padx=(4, 0))

    # ── Widget callbacks ─────────────────────────────────────────────

    def _on_monitor_change(self, *_):
        indice = self._monitor_widget.obtener_indice()
        cfg = cargar_config()
        cfg["ultimo_monitor"] = indice
        guardar_config(cfg)

    def _on_coords_change(self):
        self._profile_widget.sincronizar_paste()

    def _on_cargar_perfil(self, nombre, region):
        self._aplicar_region(region)
        monitor_idx = region.get("monitor_index")
        if monitor_idx is not None:
            nombres = obtener_nombres_monitores()
            if 0 <= int(monitor_idx) < len(nombres):
                self._monitor_var.set(nombres[int(monitor_idx)])
        self._log(f"v Perfil cargado: '{nombre}' -> {region}")

    def _on_guardar_perfil(self, nombre, region):
        region["monitor_index"] = self._monitor_widget.obtener_indice()
        perfiles = cargar_perfiles()
        perfiles[nombre] = region
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil guardado: '{nombre}' -> {region}")

    def _on_eliminar_perfil(self, nombre):
        perfiles = cargar_perfiles()
        perfiles.pop(nombre, None)
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil eliminado: '{nombre}'")

    def _crear_panel_destino(self, padre):
        r0 = ctk.CTkFrame(padre, fg_color="transparent")
        r0.pack(fill="x")
        r0.grid_columnconfigure((0, 1), weight=1)

        # Left: Sitios status
        c_sitios = ctk.CTkFrame(r0, fg_color="transparent")
        c_sitios.grid(row=0, column=0, sticky="nsew", padx=(0, 3))
        c_sitios.grid_columnconfigure(0, weight=1)

        self._frame_sitios = ctk.CTkFrame(c_sitios, fg_color="transparent")
        self._frame_sitios.pack(fill="x")
        self._actualizar_sitios_status()

        btn_row = ctk.CTkFrame(c_sitios, fg_color="transparent")
        btn_row.pack(fill="x", pady=(4, 0))
        ctk.CTkButton(
            btn_row, text="Credenciales", command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10), width=110, height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btn_row, text="Renovar sesión", command=self._renovar_sesion,
            font=ctk.CTkFont(size=10), width=110, height=28,
        ).pack(side="left")

        # Right: Destino
        c_dest = ctk.CTkFrame(r0, fg_color="transparent")
        c_dest.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        c_dest.grid_columnconfigure(0, weight=1)

        self.destino_var = ctk.StringVar(value=cargar_destino_subida())
        db = ctk.CTkFrame(c_dest, fg_color="transparent")
        db.pack(anchor="w", pady=2)
        ctk.CTkLabel(
            db, text="Subir a:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self._btns_destino = {}
        for opcion in PluginRegistry.nombres() + ["AMBOS"]:
            btn = ctk.CTkButton(
                db, text=opcion,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=72, height=28, corner_radius=6,
                fg_color=("#1f6aa5", "#1f6aa5"),
                hover_color=("#144e7a", "#144e7a"),
            )
            btn.pack(side="left", padx=(0, 4))
            self._btns_destino[opcion] = btn
            btn.configure(command=lambda o=opcion: self._seleccionar_destino(o))
        self._seleccionar_destino(self.destino_var.get())

    def _crear_opciones(self, padre):
        gap = self._r(6, 8, 10)

        cont = ctk.CTkFrame(padre, fg_color="transparent")
        cont.pack(fill="x")
        cont.grid_columnconfigure((0, 1), weight=1)
        cont.grid_rowconfigure(0, weight=1)

        # ── Col 0: Comportamiento ──────────────────────────────────
        g0, i0 = self._tarjeta(cont, "Comportamiento")
        g0.grid(row=0, column=0, sticky="nsew", padx=(0, gap))

        self.headless_var = ctk.BooleanVar(value=cargar_headless())
        self.headless_var.trace_add(
            "write", lambda *_: guardar_headless(self.headless_var.get())
        )
        ctk.CTkSwitch(
            i0, text="Modo sin ventana de Chrome",
            variable=self.headless_var, font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)

        self.chrome_existente_var = ctk.BooleanVar(value=cargar_chrome_existente())
        self.chrome_existente_var.trace_add(
            "write", lambda *_: guardar_chrome_existente(self.chrome_existente_var.get())
        )
        hc = ctk.CTkFrame(i0, fg_color="transparent")
        hc.pack(fill="x", pady=2)
        ctk.CTkSwitch(
            hc, text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var, font=ctk.CTkFont(size=11),
        ).pack(side="left")
        ctk.CTkButton(
            hc, text="Abrir Chrome", command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10), height=28, width=110,
        ).pack(side="right")

        self.auto_submit_var = ctk.BooleanVar(value=cargar_auto_submit())
        self.auto_submit_var.trace_add(
            "write", lambda *_: guardar_auto_submit(self.auto_submit_var.get())
        )
        ctk.CTkSwitch(
            i0, text="Auto-submit nota (HubSpot)",
            variable=self.auto_submit_var, font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)

        # ── Col 1: Herramientas ────────────────────────────────────
        g1, i1 = self._tarjeta(cont, "Herramientas")
        g1.grid(row=0, column=1, sticky="nsew", padx=(0, 0))

        hb = ctk.CTkFrame(i1, fg_color="transparent")
        hb.pack(fill="x", pady=2)
        ctk.CTkLabel(
            hb, text="Atajo:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            hb, textvariable=self.keybind_var, font=ctk.CTkFont(size=11),
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            hb, text="Aplicar", command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10), width=68, height=28,
        ).pack(side="left")
        self.keybind_label = ctk.CTkLabel(
            i1, text="", font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        atajo_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.winfo_toplevel().bind(atajo_inicial, lambda e: self._ejecutar())
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
        """Actualiza el destino de subida y refleja el cambio en los botones.

        Args:
            opcion: nombre del plugin destino ("HUBSPOT", "SUNRUN", "AMBOS").

        Efectos secundarios:
            - Persiste la eleccion en config.json via guardar_destino_subida().
            - Cambia el color de los botones para resaltar el seleccionado.
        """
        self.destino_var.set(opcion)
        guardar_destino_subida(opcion)
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
        self._btns_apps = {}
        self._regiones_apps = {}

        # ── FSD (Búsqueda inteligente) ────────────────────────────────
        self.usar_fsd_var = ctk.BooleanVar(value=True)
        fsd_row = ctk.CTkFrame(padre, fg_color=("gray92", "gray22"), border_width=1, corner_radius=6)
        fsd_row.pack(fill="x", pady=(0, 8))

        fsd_inner = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_inner.pack(fill="x", padx=10, pady=(6, 4))
        ctk.CTkSwitch(
            fsd_inner, text="Búsqueda inteligente por FSD",
            variable=self.usar_fsd_var, font=ctk.CTkFont(size=11),
            command=self._actualizar_estado_fsd,
        ).pack(anchor="w")

        fsd_input = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_input.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkLabel(
            fsd_input, text="FSD:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.fsd_var = ctk.StringVar(value="")
        self.fsd_entry = ctk.CTkEntry(
            fsd_input, textvariable=self.fsd_var, font=ctk.CTkFont(size=11),
            placeholder_text="Ej: 980124 o FSD-980124", state="disabled",
        )
        self.fsd_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.fsd_btn_limpiar = ctk.CTkButton(
            fsd_input, text="Limpiar", command=self._limpiar_fsd,
            font=ctk.CTkFont(size=10), width=68, height=28, state="disabled",
        )
        self.fsd_btn_limpiar.pack(side="left")

        self.fsd_btn_buscar = ctk.CTkButton(
            fsd_input, text="Buscar en Sunrun", command=self._buscar_fsd_sunrun,
            font=ctk.CTkFont(size=10), width=110, height=28,
        )
        self.fsd_btn_buscar.pack(side="right", padx=(4, 0))

        self.fsd_entry.configure(state="normal")
        self.fsd_btn_limpiar.configure(state="normal")
        self.fsd_btn_buscar.configure(state="normal")

        # ── Grid de apps ──────────────────────────────────────────────
        grid = ctk.CTkFrame(padre, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1, uniform="app_col")

        config_actual = cargar_config()
        regiones_guardadas = config_actual.get("regiones_apps", {})
        nombres_monitores = obtener_nombres_monitores()

        for idx, app in enumerate(APPS_CAPTURA):
            nombre = app["nombre"]
            icono = app.get("icono", "")
            color_base = app.get("color", ("#1f6aa5", "#1a5496"))
            region_efectiva = regiones_guardadas.get(nombre, app["region"])
            self._regiones_apps[nombre] = region_efectiva

            col = idx % 2
            row = idx // 2
            gap = self._r(4, 6, 8)

            card = ctk.CTkFrame(
                grid, fg_color=("gray90", "gray22"), corner_radius=8,
            )
            card.grid(
                row=row, column=col,
                sticky="ew",
                padx=(0 if col == 0 else gap, gap if col == 0 else 0),
                pady=(0, gap * 2),
            )

            r = region_efectiva
            es_calendar = nombre == "Calendar"
            btn_main = ctk.CTkButton(
                card,
                text=f"{icono}  {nombre}   ▶  {'Capturar celda' if es_calendar else 'Capturar'}   ({r['width']}×{r['height']} px)",
                font=ctk.CTkFont(size=12, weight="bold"),
                height=38, corner_radius=7, anchor="w",
                fg_color=color_base,
                hover_color=(oscurecer(color_base[0]), oscurecer(color_base[1])),
                command=lambda a=app: self._abrir_modal_calendar() if a["nombre"] == "Calendar" else self._ejecutar_app(a),
            )
            btn_main.pack(fill="x", padx=6, pady=(5, 2))
            self._btns_apps[nombre] = btn_main

            bot_row = ctk.CTkFrame(card, fg_color="transparent")
            bot_row.pack(fill="x", padx=6, pady=(2, 5))

            monitor_actual = self._obtener_monitor_app(app)
            nombre_monitor_actual = (
                nombres_monitores[monitor_actual]
                if 0 <= monitor_actual < len(nombres_monitores)
                else nombres_monitores[0]
            )
            dropdown_monitor = ctk.CTkComboBox(
                bot_row,
                values=nombres_monitores,
                variable=ctk.StringVar(value=nombre_monitor_actual),
                command=lambda sel, a=app: self._cambiar_monitor_app(a, sel),
                width=160, height=34, corner_radius=7,
                font=ctk.CTkFont(size=9),
                dropdown_font=ctk.CTkFont(size=9),
                state="readonly",
            )
            dropdown_monitor.pack(side="left", fill="x", expand=True, padx=(0, 4))

            if not es_calendar:
                ctk.CTkButton(
                    bot_row, text="⚙",
                    font=ctk.CTkFont(size=14),
                    width=36, height=34, corner_radius=7,
                    fg_color=("gray70", "gray35"),
                    hover_color=("gray60", "gray45"),
                    command=lambda a=app: self._medir_region_app(a),
                ).pack(side="right")

    # ── Lanzador de app ───────────────────────────────────────────────

    def _ejecutar_app(self, app: dict):
        """Lanza la captura y subida para una aplicacion especifica en un hilo.

        Args:
            app: dict de APPS_CAPTURA con nombre, region, monitor, icono, color.

        Efectos secundarios:
            - Minimiza la ventana principal.
            - Deshabilita todos los botones durante la ejecucion.
            - Inicia un thread daemon que ejecuta _proceso_app.
        """
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        nombre = app["nombre"]
        region = self._regiones_apps.get(nombre, app["region"])
        monitor_idx = self._obtener_monitor_app(app)

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()

        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando {region['width']}×{region['height']} px…"
        )

        threading.Thread(
            target=self._proceso_app,
            args=(app, region, monitor_idx),
            daemon=True,
        ).start()

    def _subir_a_destinos(self, ruta, ui, prefix=""):
        """Sube la imagen capturada a los destinos configurados."""
        headless = self.headless_var.get()
        usar_existente = self.chrome_existente_var.get()
        auto_submit = self.auto_submit_var.get()
        destino = self.destino_var.get()
        fsd = self._obtener_fsd_actual()
        if not fsd:
            fsd = self._fsd_detectado

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
            ui(f"{prefix}✗ No hay plugins para destino: {destino}")

        for plugin in plugins:
            if self._cancelado.is_set():
                ui(f"{prefix}⚠ Cancelado antes de subir a {plugin.nombre}.")
                break
            ui(f"{prefix}→ Subiendo a {plugin.nombre}…")
            fsd_plugin = fsd
            self._servicio.ejecutar_subida(
                nombre_plugin=plugin.nombre,
                ruta_imagen=ruta,
                log=ui,
                headless=headless,
                usar_chrome_existente=usar_existente,
                credenciales_sesion=self._credenciales_sesion,
                opciones={"auto_submit_nota": auto_submit},
                fsd=fsd_plugin,
                cancel_event=self._cancelado,
            )
            ui("")

    def _proceso_app(self, app: dict, region: dict, monitor_idx: int):
        """Ejecuta el ciclo completo de captura y subida para una app (en hilo).

        Args:
            app: dict de APPS_CAPTURA.
            region: dict con top/left/width/height de la region a capturar.
            monitor_idx: indice del monitor donde capturar.

        Efectos secundarios:
            - Minimiza y restaura la ventana principal.
            - Actualiza el log, la barra de estado y los indicadores de sitios.
        """
        nombre = app["nombre"]
        prefix = f"[{nombre}] "

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            ui(f"{prefix}Capturando {region['width']}×{region['height']} px…")
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            ruta = CapturaService.capturar(region, monitor=monitor_idx)
            ui(f"✓ {prefix}Imagen guardada: {ruta}")
            ui("")

            self._subir_a_destinos(ruta, ui, prefix)

            ui(f"✓ {prefix}Proceso completado.")
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
                0, lambda err=e: self._log(f"✗ {prefix}Error de captura: {err}")
            )
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error de captura"
                ),
            )
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ {prefix}Error: {err}"))
            self.after(0, lambda: self._set_status("Error"))
            self.after(
                0,
                lambda: self._label_estado_app.configure(text=f"  ✗ {nombre} — error"),
            )
        finally:
            self._proceso_en_curso = False
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, self._rehabilitar_btns_apps)

    def _rehabilitar_btns_apps(self):
        """Rehabilita todos los botones de apps y el de busqueda FSD."""
        for btn in self._btns_apps.values():
            btn.configure(state="normal")
        self.fsd_btn_buscar.configure(state="normal")
        self.btn_detener.configure(state="disabled")

    # ── Modal Calendar — captura de celda Google Sheets ───────────────

    def _abrir_modal_calendar(self):
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return

        sheet_url = os.getenv("SHEETS_SPREADSHEET_ID", "")
        service_account = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "")

        if not service_account:
            messagebox.showwarning(
                "Configuración requerida",
                "Falta GOOGLE_SERVICE_ACCOUNT_PATH en el archivo .env\n"
                "Agrega la ruta al JSON de tu Service Account de Google.",
            )
            return

        if not sheet_url:
            messagebox.showwarning(
                "Configuración requerida",
                "Falta SHEETS_SPREADSHEET_ID en el archivo .env\n"
                "Agrega el ID o URL de tu Google Sheets.",
            )
            return

        # ── Construir modal ──────────────────────────────────────────
        modal = ctk.CTkToplevel(self)
        modal.title("Calendar — Google Sheets")
        modal.resizable(False, False)
        modal.transient(self)
        modal.withdraw()  # ocultar durante construcción para evitar parpadeo

        modal.grid_columnconfigure(0, weight=1)

        # ── Dropdown de pestañas ─────────────────────────────────────
        ctk.CTkLabel(
            modal,
            text="Pestaña:",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        ).grid(row=1, column=0, pady=(0, 2), padx=28, sticky="w")

        # Cargar pestaña persistida
        _config = cargar_config()
        ultima_pestana = _config.get("ultima_pestana_calendar", "")

        sheet_var = ctk.StringVar(value=ultima_pestana or "Cargando...")
        sheet_dropdown = ctk.CTkComboBox(
            modal,
            values=[ultima_pestana] if ultima_pestana else ["Cargando pestañas..."],
            variable=sheet_var,
            state="disabled" if not ultima_pestana else "readonly",
            width=240,
            height=34,
            font=ctk.CTkFont(size=12),
            dropdown_font=ctk.CTkFont(size=12),
        )
        sheet_dropdown.grid(row=2, column=0, pady=(0, 12), padx=28)

        # ── Input de celda ───────────────────────────────────────────
        ctk.CTkLabel(
            modal,
            text="Referencia de celda (ej. F6, AA10):",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        ).grid(row=3, column=0, pady=(0, 4), padx=28, sticky="w")

        ultima_celda = _config.get("ultima_celda_calendar", "")

        cell_var = ctk.StringVar(value=ultima_celda)
        cell_entry = ctk.CTkEntry(
            modal,
            textvariable=cell_var,
            font=ctk.CTkFont(size=14, weight="bold"),
            placeholder_text="F6",
            width=240,
            height=38,
            justify="center",
        )
        cell_entry.grid(row=4, column=0, pady=(0, 12), padx=28)
        cell_entry.focus_set()
        if ultima_celda:
            cell_entry.icursor("end")

        # ── Referencia almacenada para el callback ───────────────────
        _sheet_names: list[str] = []
        _ultima_pestana_inicial = ultima_pestana

        # Bind Enter key
        def _on_enter(event):
            _ejecutar()

        cell_entry.bind("<Return>", _on_enter)

        def _ejecutar():
            cell_ref = cell_var.get().strip()
            if not cell_ref:
                messagebox.showwarning("Celda requerida", "Ingresa una referencia de celda (ej. F6).", parent=modal)
                return
            sheet_name = sheet_var.get().strip() if _sheet_names else None
            # Persistir selecciones
            config = cargar_config()
            config["ultima_celda_calendar"] = cell_ref
            if sheet_name:
                config["ultima_pestana_calendar"] = sheet_name
            guardar_config(config)
            modal.destroy()
            self._ejecutar_captura_calendar(cell_ref, sheet_url, service_account, sheet_name)

        # ── Botones ──────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.grid(row=5, column=0, pady=(0, 16), padx=28, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            font=ctk.CTkFont(size=12),
            fg_color=("gray70", "gray35"),
            hover_color=("gray60", "gray45"),
            command=modal.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Capturar",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=_ejecutar,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        # ── Cargar pestañas en background (postergado para no bloquear) ──
        def _load_sheets():
            nonlocal _sheet_names
            try:
                sheets_client = GoogleSheetsClient(service_account)
                spreadsheet_id = GoogleSheetsClient.extract_spreadsheet_id(sheet_url)
                sheets = sheets_client.list_sheets(spreadsheet_id)
                _sheet_names = [s["title"] for s in sheets]
                self._log(f"→ Pestañas detectadas: {', '.join(_sheet_names)}")

                sheet_dropdown.configure(values=_sheet_names, state="readonly")
                if _sheet_names:
                    if _ultima_pestana_inicial and _ultima_pestana_inicial in _sheet_names:
                        sheet_var.set(_ultima_pestana_inicial)
                    else:
                        sheet_var.set(_sheet_names[0])
            except Exception as e:
                self._log(f"✗ No se pudieron obtener las pestañas: {e}")
                sheet_dropdown.configure(values=["(sin pestañas)"], state="disabled")
                sheet_var.set("")

        modal.after(10, _load_sheets)

        # Posicionar y mostrar
        from ui.posicion_ventanas import ubicar_junto_a_padre
        modal.deiconify()
        ubicar_junto_a_padre(modal, self)
        modal.grab_set()
        modal.wait_window()

    def _ejecutar_captura_calendar(
        self, cell_ref: str, sheet_url: str, service_account: str,
        sheet_name: str | None = None,
    ):
        nombre = "Calendar"
        prefix = f"[{nombre}] "
        sheet_label = f" ({sheet_name})" if sheet_name else ""

        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        self._proceso_en_curso = True
        self._fsd_detectado = None
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()
        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando celda {cell_ref}{sheet_label}…"
        )

        def _ejecutar():
            try:
                ui(f"{prefix}→ Iniciando captura de celda {cell_ref} desde Google Sheets{sheet_label}…")
                config = TicketCaptureConfig(
                    spreadsheet_id=sheet_url,
                    credentials_path=service_account,
                    sheet_name=sheet_name,
                    headless=True,
                )
                service = TicketCaptureService(config, log_callback=ui)
                payload = service.capture_sync(cell_ref)

                ui(f"{prefix}✓ Valores obtenidos:")
                for ref, val in payload.cells.items():
                    ui(f"{prefix}    {ref}: {val or '(vacío)'}")

                ui(f"{prefix}✓ Imagen compuesta: {payload.image_path}")
                ui("")

                # Subir la imagen compuesta a los destinos configurados
                self._subir_a_destinos(payload.image_path, ui, prefix)

                ui(f"{prefix}✓ Proceso completado.")
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
                        text=f"  ✓ {nombre} — celda {cell_ref}{sheet_label} capturada a las {ahora}"
                    ),
                )
                self.after(0, self._actualizar_sitios_status)

            except Exception as e:
                self.after(
                    0, lambda err=e: self._log(f"✗ {prefix}Error: {err}")
                )
                self.after(0, lambda: self._set_status("Error"))
                self.after(
                    0,
                    lambda: self._label_estado_app.configure(
                        text=f"  ✗ {nombre} — error al capturar celda {cell_ref}"
                    ),
                )
            finally:
                self._proceso_en_curso = False
                self.after(0, self.deiconify_window)
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_ejecutar, daemon=True).start()

    # ── Medidor de región por app ─────────────────────────────────────

    def _medir_region_app(self, app: dict):
        """Lanza el medidor de region para redefinir el area de captura de una app.

        Args:
            app: dict de APPS_CAPTURA con nombre y monitor.

        Efectos secundarios:
            - Minimiza la ventana principal.
            - Abre el overlay de medicion en el monitor de la app.
            - Persiste la nueva region en config.json bajo 'regiones_apps'.
            - Actualiza el texto del boton de la app con las nuevas dimensiones.
        """
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        nombre = app["nombre"]
        monitor_idx = self._obtener_monitor_app(app)

        self._log(f"→ Midiendo región para {nombre}…")
        self._label_estado_app.configure(
            text=f"  ⏳ Medí la región de {nombre} en pantalla…"
        )

        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self.iconify_window()

        def _esperar():
            try:
                nueva_region = ejecutar_medidor(monitor_idx)

                if nueva_region is None:
                    self.after(0, lambda: self._log(f"✗ Medición cancelada para {nombre}."))
                    self.after(0, lambda: self._label_estado_app.configure(text=""))
                    self.after(0, self.deiconify_window)
                    self.after(0, self._rehabilitar_btns_apps)
                    self.after(0, lambda: self.btn.configure(state="normal"))
                    return

                self._regiones_apps[nombre] = nueva_region
                cfg = cargar_config()
                cfg.setdefault("regiones_apps", {})[nombre] = nueva_region
                self.after(0, lambda c=cfg: guardar_config(c))

                def _actualizar_ui():
                    if nombre in self._btns_apps:
                        tooltip = f"{nueva_region['width']}×{nueva_region['height']} px"
                        btn = self._btns_apps[nombre]
                        icono = next((a["icono"] for a in APPS_CAPTURA if a["nombre"] == nombre), "")
                        color_base = next((a["color"] for a in APPS_CAPTURA if a["nombre"] == nombre), ("#1f6aa5", "#1a5496"))
                        btn.configure(
                            text=f"{icono}  {nombre}   ▶  Capturar y subir   ({tooltip})",
                            fg_color=color_base,
                        )
                    self._label_estado_app.configure(
                        text=f"  ✓ {nombre} — nueva región: {nueva_region['width']}×{nueva_region['height']} px guardada"
                    )
                    self._log(f"✓ Región de {nombre} actualizada: {nueva_region}")
                    self.deiconify_window()
                    self._rehabilitar_btns_apps()
                    self.btn.configure(state="normal")

                self.after(0, _actualizar_ui)
            except Exception as e:
                self.after(0, lambda err=e: self._log(f"✗ [{nombre}] Error en medidor: {err}"))
                self.after(0, lambda: self._label_estado_app.configure(
                    text=f"  ✗ {nombre} — error en medidor"
                ))
                self.after(0, self.deiconify_window)
                self.after(0, self._rehabilitar_btns_apps)
                self.after(0, lambda: self.btn.configure(state="normal"))
            finally:
                self.after(0, lambda: setattr(self, '_proceso_en_curso', False))

        threading.Thread(target=_esperar, daemon=True).start()

    def _crear_barra_estado(self, padre, col=0):
        """Construye la barra de estado inferior con punto indicador y labels.

        Args:
            padre: widget padre (CTkScrollableFrame).
            col: columna del grid donde ubicar la barra.
        """
        frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        frame_estado.grid(row=6, column=col, sticky="ew", pady=(4, 0))
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

    def _tarjeta(self, padre, titulo):
        """Crea una tarjeta (card) con borde y titulo pequeno.

        Args:
            padre: widget padre.
            titulo: texto del encabezado de la tarjeta.

        Returns:
            Tupla (frame_exterior, frame_interior). Empaquetar widgets dentro
            de frame_interior.
        """
        frame = ctk.CTkFrame(
            padre, fg_color=("gray92", "gray22"), border_width=1, corner_radius=6
        )
        ctk.CTkLabel(
            frame,
            text=f"  {titulo}",
            font=ctk.CTkFont(size=self._fs(10)),
            text_color=("gray55", "gray55"),
        ).pack(anchor="w", pady=(4, 2), padx=2)
        interior = ctk.CTkFrame(frame, fg_color="transparent")
        interior.pack(fill="x", padx=10, pady=(0, 6))
        return frame, interior

    def _fuente_existe(self, nombre):
        """Verifica si una familia tipografica esta instalada en el sistema.

        Args:
            nombre: nombre de la fuente (ej. "Cascadia Code").

        Returns:
            True si la fuente esta disponible.
        """
        return nombre in tkinter.font.families()

    def _keybind_legible(self, kb):
        """Convierte un keybind de Tkinter a formato legible.

        "<Control-Return>" -> "Ctrl+Enter"
        "<Shift-Alt-x>"    -> "Shift+Alt+x"

        Args:
            kb: string de keybind en formato Tkinter.

        Returns:
            Version legible para mostrar en la UI.
        """
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
            self.fsd_btn_buscar.configure(state="normal")
            self._log("✓ Búsqueda inteligente por FSD activada.")
        else:
            self.fsd_entry.configure(state="disabled")
            self.fsd_btn_limpiar.configure(state="disabled")
            self.fsd_btn_buscar.configure(state="disabled")
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

    @staticmethod
    def _detectar_fsd_de_chrome() -> str | None:
        """
        Lee el título de ventanas visibles de Chrome vía Windows API y extrae
        el primer FSD que encuentre (patrón FSD-XXXXXX o FSDXXXXXX).
        Se llama con la app minimizada para que Chrome esté en primer plano.
        """
        import re
        user32 = ctypes.windll.user32

        fsd_encontrado = [None]

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def enum_proc(hwnd, _lparam):
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            if "Google Chrome" not in title and "Chromium" not in title:
                return True
            match = re.search(r'FSD[-\s]*(\d+)', title, re.IGNORECASE)
            if match:
                fsd = f"FSD-{match.group(1)}"
                fsd_encontrado[0] = fsd
                return False
            return True

        user32.EnumWindows(WNDENUMPROC(enum_proc), 0)
        return fsd_encontrado[0]

    def _buscar_fsd_sunrun(self):
        """
        Ejecuta SOLO la búsqueda FSD en Sunrun (navega al ticket) sin scraping.

        Usa exactamente la misma lógica que el módulo de scraping (ScraperSunrun),
        pero se detiene en la página de detalle del ticket sin extraer datos.
        """
        fsd = self.fsd_var.get().strip()
        if not fsd:
            self._log("✗ Ingresa un número FSD para buscar.")
            return

        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return

        self._proceso_en_curso = True
        self.fsd_btn_buscar.configure(state="disabled")
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.btn.configure(state="disabled")
        self._set_status("Buscando FSD en Sunrun...")

        def _buscar():
            try:

                def ui(msg):
                    self.after(0, lambda m=msg: self._log(m))

                ui(f"→ Buscando FSD en Sunrun: {normalizar_fsd(fsd)}")
                scraper = ScraperSunrun(log_callback=ui)
                resultado = scraper.navegar_a_fsd(fsd)
                if resultado["ok"]:
                    ui(f"✓ {resultado['mensaje']}")
                else:
                    ui(f"✗ {resultado['mensaje']}")
                self.after(0, lambda: self._set_status("Listo"))
            except Exception as e:
                self.after(0, lambda err=e: self._log(f"✗ Error en búsqueda FSD: {err}"))
                self.after(0, lambda: self._set_status("Error"))
            finally:
                self._proceso_en_curso = False
                self.after(0, self.deiconify_window)
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_buscar, daemon=True).start()

    # ── Sitios status ─────────────────────────────────────────────────

    def _actualizar_sitios_status(self):
        for widget in self._frame_sitios.winfo_children():
            widget.destroy()

        for plugin in PluginRegistry.todos():
            nombre = plugin.nombre
            tiene_sesion = (COOKIES_DIR / f"{nombre.replace(' ', '_')}.pkl").exists()
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
        """Registra un mensaje en el widget de log de la ventana principal.

        Args:
            msg: texto a registrar. Se le agrega marca de tiempo automaticamente.
        """
        self.log_texto.log(msg)

    def _set_status(self, texto: str):
        """Actualiza el texto e indicador de color de la barra de estado.

        Args:
            texto: nuevo estado ("Listo", "Ejecutando...", "Completado", "Error").
        """
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

    def _monitor_var_indice(self) -> int:
        """Obtiene el indice numerico del monitor seleccionado en el dropdown."""
        return self._monitor_widget.obtener_indice()

    def _lanzar_medidor(self):
        """Minimiza la ventana y lanza el overlay de medicion de region.

        Abre el medidor en el monitor seleccionado. Cuando el usuario
        termina de dibujar el rectangulo, se actualizan los campos de
        coordenadas con la region seleccionada.

        Efectos secundarios:
            - Minimiza la ventana principal durante la medicion.
            - Bloquea el boton principal para evitar doble ejecucion.
        """
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        monitor_idx = self._monitor_var_indice()
        self._log(f"→ Abre el medidor en {self._monitor_var.get()}…")
        self.btn.configure(state="disabled")
        self.iconify_window()

        def _esperar():
            region = ejecutar_medidor(monitor_idx)
            if region is not None:
                self.after(0, lambda r=region: self._aplicar_region(r))
            else:
                self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region: dict):
        """Actualiza los campos de coordenadas con los valores de un dict.

        Args:
            region: dict con claves top, left, width, height (enteros).
        """
        self._coord_widget.aplicar_region(region)
        self._profile_widget.sincronizar_paste()
        self._log(f"v Region actualizada: {region}")
        self.btn.configure(state="normal")

    def _obtener_region_validada(self) -> dict:
        """Lee y valida los campos de coordenadas del formulario.

        Returns:
            Dict con claves top, left, width, height como enteros.

        Raises:
            ValueError: si algun campo esta vacio, no es numerico, o tiene
                        width/height <= 0.
        """
        region = {}
        for clave, var in self.region_vars.items():
            texto = var.get().strip()
            if not texto:
                raise ValueError(f"El campo '{clave}' esta vacio.")
            try:
                region[clave] = int(texto)
            except ValueError:
                raise ValueError(f"El campo '{clave}' debe ser un numero entero.")
        if region["width"] <= 0:
            raise ValueError("Width debe ser mayor que 0.")
        if region["height"] <= 0:
            raise ValueError("Height debe ser mayor que 0.")
        return region

    def _parsear_region(self, texto: str):
        """Parsea una region desde texto pegado (dict o formato 'REGION = {...}').

        Acepta tanto el formato del medidor ("REGION = {'top': ...}") como
        un dict de Python directamente.

        Args:
            texto: string con la representacion de un dict de region.

        Efectos secundarios:
            - Actualiza los campos de coordenadas si el parseo es exitoso.
            - Muestra un mensaje de error si el formato no es valido.
        """
        texto = (texto or "").strip()
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
        """Sincroniza el campo 'Pegar region' con las coordenadas actuales."""
        self._profile_widget.sincronizar_paste()

    # ── Sesión ────────────────────────────────────────────────────────

    def _abrir_login_inicial(self):
        """Abre la ventana de credenciales si faltan al iniciar la app.

        Se llama en __init__ despues de construir la UI si algun plugin
        con login no tiene credenciales guardadas.
        """
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
        """Abre la ventana de credenciales para editar usuarios y contrasenas.

        Efectos secundarios:
            - Si el usuario confirma, actualiza self._credenciales_sesion.
            - Refresca los indicadores de estado de sesion.
        """
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
        """Elimina las cookies guardadas para forzar un nuevo login.

        Borra el directorio cookies/ y actualiza los indicadores de estado.
        La proxima ejecucion requerira autenticacion fresca.
        """
        if COOKIES_DIR.exists():
            shutil.rmtree(COOKIES_DIR)
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

    def _abrir_chrome_debug(self):
        """Abre Chrome con depuracion remota en puerto 9222.

        Si Chrome ya esta activo en el puerto, solo notifica. Si no,
        busca el ejecutable y lo lanza con los flags necesarios.

        Efectos secundarios:
            - Lanza un subproceso de Chrome (subprocess.Popen, no bloqueante).
        """
        from core.browser import puerto_activo, CHROME_USER_DATA, CHROME_PATHS, obtener_chrome_exe

        if puerto_activo():
            self._log("✓ Chrome con depuración ya está activo en el puerto 9222.")
            return
        chrome_exe = obtener_chrome_exe()
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
                f"--user-data-dir={CHROME_USER_DATA}",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222.")

    # ── Keybind ───────────────────────────────────────────────────────

    def _aplicar_keybind(self):
        """Registra el atajo de teclado ingresado para ejecutar captura y subida.

        Desvincula el atajo anterior (si existe), vincula el nuevo a
        self._ejecutar(), y persiste la configuracion en config.json.

        Efectos secundarios:
            - Modifica el binding de teclas de la ventana raiz.
            - Guarda en config.json bajo la clave 'keybind'.
        """
        nuevo = self.keybind_var.get().strip()
        if not nuevo:
            return
        if self._keybind_actual:
            try:
                self.winfo_toplevel().unbind(self._keybind_actual)
            except Exception:
                pass
        try:
            self.winfo_toplevel().bind(nuevo, lambda e: self._ejecutar())
            self._keybind_actual = nuevo
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(nuevo)}",
                text_color=("green", "#3fb950"),
            )
            self._config = cfg = cargar_config()
            cfg["keybind"] = nuevo
            guardar_config(cfg)
            self._config = cfg
        except Exception as e:
            self.keybind_label.configure(
                text=f"Atajo inválido: {e}", text_color=("red", "#f85149")
            )
            self._keybind_actual = None

    def _capturar_tecla(self, event):
        """Captura una combinacion de teclas y la muestra en el campo de atajo.

        Detecta modificadores (Control, Shift, Alt) via event.state y los
        combina con la tecla presionada en formato Tkinter (<Control-x>).

        Args:
            event: evento KeyPress de Tkinter.

        Returns:
            "break" para evitar que la tecla se propague al Entry.
        """
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

    # ── Detener proceso ────────────────────────────────────────────────

    def _detener(self):
        """Solicita la cancelacion del proceso en curso via threading.Event."""
        self._cancelado.set()
        self._log("⚠ Deteniendo proceso...")
        self.btn_detener.configure(state="disabled")
        self._set_status("Cancelando...")

    # ── Proceso principal ─────────────────────────────────────────────

    def _ejecutar(self):
        """Inicia el ciclo de captura y subida principal en un hilo separado.

        Valida la region, minimiza la ventana, captura la pantalla, detecta
        el FSD automaticamente del titulo de Chrome, y sube a los destinos
        configurados. Bloquea la UI durante la ejecucion para evitar
        multiples procesos simultaneos.
        """
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return
        self._proceso_en_curso = True
        self._cancelado.clear()
        self.btn.configure(state="disabled")
        self.btn_detener.configure(state="normal")
        for btn in self._btns_apps.values():
            btn.configure(state="disabled")
        self.fsd_btn_buscar.configure(state="disabled")
        self._set_status("Ejecutando...")
        self.log_texto.clear()
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        """Ejecuta el flujo principal de captura y subida (corre en hilo secundario).

        Flujo:
          1. Valida y lee la region de captura.
          2. Minimiza la ventana para no interferir.
          3. Detecta el FSD automaticamente de la ventana de Chrome activa.
          4. Captura la region con mss.
          5. Sube la imagen a los destinos configurados.
          6. Restaura la ventana y actualiza el estado.

        Efectos secundarios:
            - Usa self.after() para toda interaccion con la UI desde el hilo.
        """
        def ui(msg):
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = self._obtener_region_validada()
            monitor_idx = self._monitor_var_indice()
            ui(f"→ Capturando región en {self._monitor_var.get()}: {region}")
            self.after(0, self.iconify_window)
            time.sleep(0.4)

            self._fsd_detectado = self._detectar_fsd_de_chrome()
            if self._fsd_detectado:
                ui(f"→ FSD detectado automáticamente: {self._fsd_detectado}")

            ruta = CapturaService.capturar(region, monitor=monitor_idx)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            if self._cancelado.is_set():
                ui("⚠ Proceso cancelado antes de subir.")
                self.after(0, lambda: self._set_status("Cancelado"))
                return

            self._subir_a_destinos(ruta, ui)

            if self._cancelado.is_set():
                ui("⚠ Proceso cancelado.")
                self.after(0, lambda: self._set_status("Cancelado"))
                return

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
            self._proceso_en_curso = False
            self._cancelado.clear()
            self.after(0, self.deiconify_window)
            self.after(0, lambda: self.btn.configure(state="normal"))
            self.after(0, lambda: self.btn_detener.configure(state="disabled"))
            self.after(0, self._rehabilitar_btns_apps)



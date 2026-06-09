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
from ui.ventana_plantillas import _cargar_plantillas, _guardar_plantillas
from ui.custom_ctkframe import CustomCTkFrame
from ui.ui_manager import UIManager
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
    """Ventana principal de SSAuto.

    Args:
        parent: widget padre de tkinter/CustomTkinter donde se incrusta la app.
    """

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
        self._cola_imagenes: list[str] = (
            []
        )  # cola de capturas para HubSpot (auto_submit OFF)
        self._cola_mensajes: list[str] = []  # mensajes asociados a cada captura
        self._servicio = SesionService()
        self.ui_manager = UIManager(self)
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
        """Abre la ventana de comparacion de propiedades entre HubSpot y Sunrun.

        Efectos secundarios:
            - Instancia y muestra VentanaComparacion pasando self._log como
              callback de registro.
        """
        from ui.ventana_comparacion import VentanaComparacion

        VentanaComparacion(self, log_callback=self._log)

    # ── UI ────────────────────────────────────────────────────────────

    def _construir_ui(self):
        """Construye la UI completa de la ventana principal.

        Crea el frame scrolleable, las secciones (region de captura, apps,
        destino, opciones, registro y barra de estado) y registra todos los
        paneles y widgets hijos en el UIManager para control de visibilidad.

        Efectos secundarios:
            - Configura el grid del frame principal y del scroll.
            - Registra secciones y widgets en self.ui_manager.
            - Llama a _apply_initial_state() para aplicar visibilidad
              persistida desde config.json.
        """
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

        frame_captura, sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0, col=1)
        self._crear_panel_captura(sec1)
        self.ui_manager.register("captura", frame_captura)

        frame_apps, sec_apps = self._seccion(
            padre, "  APLICACIONES DE CAPTURA", fila=1, col=1
        )
        self._crear_panel_apps(sec_apps)
        self.ui_manager.register("apps", frame_apps)

        frame_dest, sec2 = self._seccion(padre, "  DESTINO Y SESIÓN", fila=2, col=1)
        self._crear_panel_destino(sec2)
        self.ui_manager.register("destino", frame_dest)

        frame_cfg, sec3 = self._seccion(padre, "  CONFIGURACIÓN", fila=3, col=1)
        self._crear_opciones(sec3)
        self.ui_manager.register("opciones", frame_cfg)

        frame_log, sec4 = self._seccion(padre, "  REGISTRO", fila=4, col=1, pady=(0, 8))
        fuente = "Cascadia Code" if self._fuente_existe("Cascadia Code") else "Consolas"
        self.log_texto = LogWidget(
            sec4,
            font=ctk.CTkFont(family=fuente, size=self._fs(10)),
            height=self._r(140, 180, 260),
        )
        self.log_texto.pack(fill="both", expand=True)
        self.ui_manager.register("registro", frame_log, pady=(0, 8))

        self._crear_barra_estado(padre, col=1)
        self.ui_manager.register("barra_estado", self._frame_estado, pady=(4, 0))

        self.ui_manager._apply_initial_state()

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
            Tupla (frame_exterior, cuerpo_interior). frame_exterior es
            el CTkFrame con borde; cuerpo_interior es donde empaquetar
            los widgets hijos.
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
            fill="both",
            expand=True,
            padx=self._r(14, 20, 32),
            pady=self._r(12, 16, 24),
        )
        return frame, cuerpo

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
        """Crea el panel de region de captura con perfiles, monitor y coordenadas.

        Args:
            padre: widget padre donde empaquetar el panel.

        Efectos secundarios:
            - Inicializa self._perfiles, self.region_vars, self._profile_widget,
              self._monitor_widget, self._coord_widget y los botones de accion.
            - Inicializa el frame de cola de imagenes (oculto por defecto).
            - Registra widgets hijos en el UIManager.
        """
        self._perfiles = cargar_perfiles()
        self.region_vars = {}

        monitores_raw = obtener_monitores()
        nombres_monitores = obtener_nombres_monitores()
        monitor_guardado = int(self._config.get("ultimo_monitor", 1))

        # ── Row 0: Perfiles (left) | Monitor (right) ─────────────
        self._row_perfiles_monitor = ctk.CTkFrame(padre, fg_color="transparent")
        self._row_perfiles_monitor.pack(fill="x", pady=(0, 4))
        self._row_perfiles_monitor.grid_columnconfigure((0, 1), weight=1)

        self._profile_widget = ProfileManagerWidget(
            self._row_perfiles_monitor,
            region_vars=self.region_vars,
            perfiles_iniciales=self._perfiles,
            on_cargar_perfil=self._on_cargar_perfil,
            on_guardar_perfil=self._on_guardar_perfil,
            on_eliminar_perfil=self._on_eliminar_perfil,
            on_aplicar_region=self._parsear_region,
            on_log=self._log,
        )
        self._profile_widget.grid(row=0, column=0, sticky="nsew", padx=(0, 3))
        self.ui_manager.register_child(
            "capt_perfiles",
            self._profile_widget,
            self._row_perfiles_monitor,
            "    Perfiles",
            "grid",
            {"row": 0, "column": 0, "sticky": "nsew", "padx": (0, 3)},
            parent_pack_info={"fill": "x", "pady": (0, 4)},
        )

        self._monitor_widget = MonitorSelectorWidget(
            self._row_perfiles_monitor,
            nombres_monitores=nombres_monitores,
            monitores_raw=monitores_raw,
            indice_inicial=monitor_guardado,
            on_change=self._on_monitor_change,
        )
        self._monitor_widget.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        self._monitor_var = self._monitor_widget.monitor_var
        self.ui_manager.register_child(
            "capt_monitor",
            self._monitor_widget,
            self._row_perfiles_monitor,
            "    Monitor",
            "grid",
            {"row": 0, "column": 1, "sticky": "nsew", "padx": (3, 0)},
            parent_pack_info={"fill": "x", "pady": (0, 4)},
        )

        # ── Row 1: Coordenadas ────────────────────────────────────
        self._row_coords = ctk.CTkFrame(padre, fg_color="transparent")
        self._row_coords.pack(fill="x", pady=(2, 4))

        self._coord_widget = CoordinateInputsWidget(
            self._row_coords,
            valores_iniciales=PERFIL_POR_DEFECTO,
            on_change=self._on_coords_change,
        )
        self._coord_widget.pack(side="left", fill="x", expand=True)
        self.region_vars = self._coord_widget.region_vars
        self.ui_manager.register_child(
            "capt_coordenadas",
            self._coord_widget,
            self._row_coords,
            "    Coordenadas",
            "pack",
            {"side": "left", "fill": "x", "expand": True},
            parent_pack_info={"fill": "x", "pady": (2, 4)},
        )

        # ── Row 2: Medir | Capturar y subir | Detener ────────────
        self._row_botones = ctk.CTkFrame(padre, fg_color="transparent")
        self._row_botones.pack(fill="x")
        self._row_botones.grid_columnconfigure((0, 1, 2), weight=1, uniform="btn")

        alto_boton = self._r(32, 36, 44)

        self._btn_medir = ctk.CTkButton(
            self._row_botones,
            text="  Medir region en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=self._fs(11)),
            height=alto_boton,
            fg_color=("gray75", "gray30"),
            hover_color=("gray65", "gray25"),
        )
        self._btn_medir.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.ui_manager.register_child(
            "capt_btn_medir",
            self._btn_medir,
            self._row_botones,
            "    Boton Medir region",
            "grid",
            {"row": 0, "column": 0, "sticky": "ew", "padx": (0, 4)},
            parent_pack_info={"fill": "x"},
        )

        self.btn = ctk.CTkButton(
            self._row_botones,
            text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=self._fs(12), weight="bold"),
            height=alto_boton,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.grid(row=0, column=1, sticky="ew", padx=(2, 2))
        self.ui_manager.register_child(
            "capt_btn_capturar",
            self.btn,
            self._row_botones,
            "    Boton Capturar y subir",
            "grid",
            {"row": 0, "column": 1, "sticky": "ew", "padx": (2, 2)},
            parent_pack_info={"fill": "x"},
        )

        self.btn_detener = ctk.CTkButton(
            self._row_botones,
            text="  Detener",
            command=self._detener,
            font=ctk.CTkFont(size=self._fs(11), weight="bold"),
            height=alto_boton,
            fg_color=("#d73a49", "#f85149"),
            hover_color=("#b6232e", "#da3633"),
            state="disabled",
        )
        self.btn_detener.grid(row=0, column=2, sticky="ew", padx=(4, 0))
        self.ui_manager.register_child(
            "capt_btn_detener",
            self.btn_detener,
            self._row_botones,
            "    Boton Detener",
            "grid",
            {"row": 0, "column": 2, "sticky": "ew", "padx": (4, 0)},
            parent_pack_info={"fill": "x"},
        )

        # ── Row 3: Cola de imágenes (HubSpot, auto_submit OFF) ───────
        self._frame_cola = ctk.CTkFrame(padre, fg_color="transparent")
        self._label_cola = ctk.CTkLabel(
            self._frame_cola,
            text="Cola: 0 imágenes",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray70"),
        )
        self._label_cola.pack(side="left", padx=(0, 8))

        self._btn_subir_cola = ctk.CTkButton(
            self._frame_cola,
            text="Subir cola",
            font=ctk.CTkFont(size=11, weight="bold"),
            width=90,
            height=28,
            corner_radius=6,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
            command=self._subir_cola_hubspot,
        )
        self._btn_subir_cola.pack(side="left", padx=(0, 4))

        self._btn_limpiar_cola = ctk.CTkButton(
            self._frame_cola,
            text="Limpiar",
            font=ctk.CTkFont(size=10),
            width=60,
            height=28,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            command=self._limpiar_cola,
        )
        self._btn_limpiar_cola.pack(side="left")

        self._frame_cola.pack_forget()

    # ── Widget callbacks ─────────────────────────────────────────────

    def _on_monitor_change(self, *_):
        """Persiste el indice del monitor seleccionado en config.json."""
        indice = self._monitor_widget.obtener_indice()
        cfg = cargar_config()
        cfg["ultimo_monitor"] = indice
        guardar_config(cfg)

    def _on_coords_change(self):
        """Sincroniza el campo 'Pegar region' cuando cambian las coordenadas."""
        self._profile_widget.sincronizar_paste()

    def _on_cargar_perfil(self, nombre, region):
        """Callback al cargar un perfil guardado desde el ProfileManagerWidget.

        Args:
            nombre: nombre del perfil cargado.
            region: dict con top/left/width/height y opcionalmente monitor_index.

        Efectos secundarios:
            - Aplica la region a los campos de coordenadas.
            - Cambia el monitor si el perfil incluye monitor_index.
        """
        self._aplicar_region(region)
        monitor_idx = region.get("monitor_index")
        if monitor_idx is not None:
            nombres = obtener_nombres_monitores()
            if 0 <= int(monitor_idx) < len(nombres):
                self._monitor_var.set(nombres[int(monitor_idx)])
        self._log(f"v Perfil cargado: '{nombre}' -> {region}")

    def _on_guardar_perfil(self, nombre, region):
        """Callback al guardar un perfil desde el ProfileManagerWidget.

        Args:
            nombre: nombre del perfil a guardar.
            region: dict con top/left/width/height de la region actual.

        Efectos secundarios:
            - Agrega monitor_index a la region.
            - Persiste en perfiles.json via guardar_perfiles().
            - Actualiza la lista de perfiles en el widget.
        """
        region["monitor_index"] = self._monitor_widget.obtener_indice()
        perfiles = cargar_perfiles()
        perfiles[nombre] = region
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil guardado: '{nombre}' -> {region}")

    def _on_eliminar_perfil(self, nombre):
        """Callback al eliminar un perfil desde el ProfileManagerWidget.

        Args:
            nombre: nombre del perfil a eliminar.

        Efectos secundarios:
            - Elimina el perfil de perfiles.json via guardar_perfiles().
            - Actualiza la lista de perfiles en el widget.
        """
        perfiles = cargar_perfiles()
        perfiles.pop(nombre, None)
        guardar_perfiles(perfiles)
        self._perfiles = perfiles
        self._profile_widget.actualizar_perfiles(perfiles)
        self._log(f"v Perfil eliminado: '{nombre}'")

    def _crear_panel_destino(self, padre):
        """Crea el panel de destino y sesion con indicadores de sitios y selectores.

        Args:
            padre: widget padre donde empaquetar el panel.

        Efectos secundarios:
            - Construye los indicadores de estado de sesion para cada plugin.
            - Crea los botones de destino (HubSpot, Sunrun, AMBOS).
            - Inicializa self.destino_var, self._btns_destino.
            - Vincula cambios de destino con _verificar_limpiar_cola().
        """
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
            btn_row,
            text="Credenciales",
            command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btn_row,
            text="Renovar sesión",
            command=self._renovar_sesion,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left")

        # Right: Destino
        c_dest = ctk.CTkFrame(r0, fg_color="transparent")
        c_dest.grid(row=0, column=1, sticky="nsew", padx=(3, 0))
        c_dest.grid_columnconfigure(0, weight=1)

        self.destino_var = ctk.StringVar(value=cargar_destino_subida())
        self.destino_var.trace_add("write", lambda *_: self._verificar_limpiar_cola())
        db = ctk.CTkFrame(c_dest, fg_color="transparent")
        db.pack(anchor="w", pady=2)
        ctk.CTkLabel(
            db,
            text="Subir a:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self._btns_destino = {}
        for opcion in PluginRegistry.nombres() + ["AMBOS"]:
            btn = ctk.CTkButton(
                db,
                text=opcion,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=72,
                height=28,
                corner_radius=6,
                fg_color=("#1f6aa5", "#1f6aa5"),
                hover_color=("#144e7a", "#144e7a"),
            )
            btn.pack(side="left", padx=(0, 4))
            self._btns_destino[opcion] = btn
            btn.configure(command=lambda o=opcion: self._seleccionar_destino(o))
        self._seleccionar_destino(self.destino_var.get())

    def _crear_opciones(self, padre):
        """Crea el panel de configuracion con switches de comportamiento y atajos.

        Args:
            padre: widget padre donde empaquetar el panel.

        Efectos secundarios:
            - Inicializa switches para headless, Chrome existente y auto-submit.
            - Inicializa el campo de atajo de teclado (keybind).
            - Los switches persisten automaticamente al cambiar via sus trace_add.
              El switch auto_submit tambien dispara _verificar_limpiar_cola().
        """
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
            i0,
            text="Modo sin ventana de Chrome",
            variable=self.headless_var,
            font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)

        self.chrome_existente_var = ctk.BooleanVar(value=cargar_chrome_existente())
        self.chrome_existente_var.trace_add(
            "write",
            lambda *_: guardar_chrome_existente(self.chrome_existente_var.get()),
        )
        hc = ctk.CTkFrame(i0, fg_color="transparent")
        hc.pack(fill="x", pady=2)
        ctk.CTkSwitch(
            hc,
            text="Usar Chrome ya abierto (puerto 9222)",
            variable=self.chrome_existente_var,
            font=ctk.CTkFont(size=11),
        ).pack(side="left")
        ctk.CTkButton(
            hc,
            text="Abrir Chrome",
            command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10),
            height=28,
            width=110,
        ).pack(side="right")

        self.auto_submit_var = ctk.BooleanVar(value=cargar_auto_submit())
        self.auto_submit_var.trace_add(
            "write",
            lambda *_: (
                guardar_auto_submit(self.auto_submit_var.get()),
                self._verificar_limpiar_cola(),
            ),
        )
        ctk.CTkSwitch(
            i0,
            text="Auto-submit nota (HubSpot)",
            variable=self.auto_submit_var,
            font=ctk.CTkFont(size=11),
        ).pack(anchor="w", pady=2)

        # ── Col 1: Herramientas ────────────────────────────────────
        g1, i1 = self._tarjeta(cont, "Herramientas")
        g1.grid(row=0, column=1, sticky="nsew", padx=(0, 0))

        hb = ctk.CTkFrame(i1, fg_color="transparent")
        hb.pack(fill="x", pady=2)
        ctk.CTkLabel(
            hb,
            text="Atajo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            hb,
            textvariable=self.keybind_var,
            font=ctk.CTkFont(size=11),
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)
        ctk.CTkButton(
            hb,
            text="Aplicar",
            command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10),
            width=68,
            height=28,
        ).pack(side="left")
        self.keybind_label = ctk.CTkLabel(
            i1,
            text="",
            font=ctk.CTkFont(size=10),
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
        """Crea el panel de aplicaciones de captura con busqueda FSD y grid de apps.

        Incluye el panel de busqueda inteligente por FSD (switch, campo de texto,
        botones de limpiar y buscar en Sunrun) y una grilla de tarjetas con botones
        de captura, selectores de monitor y botones de medicion por app.

        Args:
            padre: widget padre donde empaquetar el panel.

        Efectos secundarios:
            - Inicializa self._btns_apps, self._regiones_apps.
            - Inicializa self.usar_fsd_var, self.fsd_var, self.fsd_entry y
              self.fsd_btn_limpiar (las variables FSD se inicializan aqui,
              no en _crear_opciones).
            - Construye tarjetas dinamicas para cada entrada de APPS_CAPTURA.
        """
        self._btns_apps = {}
        self._regiones_apps = {}

        # ── FSD (Búsqueda inteligente) ────────────────────────────────
        self.usar_fsd_var = ctk.BooleanVar(value=True)
        fsd_row = ctk.CTkFrame(
            padre, fg_color=("gray92", "gray22"), border_width=1, corner_radius=6
        )
        fsd_row.pack(fill="x", pady=(0, 8))

        fsd_inner = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_inner.pack(fill="x", padx=10, pady=(6, 4))
        ctk.CTkSwitch(
            fsd_inner,
            text="Búsqueda inteligente por FSD",
            variable=self.usar_fsd_var,
            font=ctk.CTkFont(size=11),
            command=self._actualizar_estado_fsd,
        ).pack(anchor="w")

        fsd_input = ctk.CTkFrame(fsd_row, fg_color="transparent")
        fsd_input.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkLabel(
            fsd_input,
            text="FSD:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))
        self.fsd_var = ctk.StringVar(value="")
        self.fsd_entry = ctk.CTkEntry(
            fsd_input,
            textvariable=self.fsd_var,
            font=ctk.CTkFont(size=11),
            placeholder_text="Ej: 980124 o FSD-980124",
        )
        self.fsd_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        self.fsd_btn_limpiar = ctk.CTkButton(
            fsd_input,
            text="Limpiar",
            command=self._limpiar_fsd,
            font=ctk.CTkFont(size=10),
            width=68,
            height=28,
        )
        self.fsd_btn_limpiar.pack(side="left")

        self.fsd_btn_buscar = ctk.CTkButton(
            fsd_input,
            text="Buscar en Sunrun",
            command=self._buscar_fsd_sunrun,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        )
        self.fsd_btn_buscar.pack(side="right", padx=(4, 0))

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
                grid,
                fg_color=("gray90", "gray22"),
                corner_radius=8,
            )
            card.grid(
                row=row,
                column=col,
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
                height=38,
                corner_radius=7,
                anchor="w",
                fg_color=color_base,
                hover_color=(oscurecer(color_base[0]), oscurecer(color_base[1])),
                command=lambda a=app: (
                    self._abrir_modal_calendar()
                    if a["nombre"] == "Calendar"
                    else self._ejecutar_app(a)
                ),
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
                width=160,
                height=34,
                corner_radius=7,
                font=ctk.CTkFont(size=9),
                dropdown_font=ctk.CTkFont(size=9),
                state="readonly",
            )
            dropdown_monitor.pack(side="left", fill="x", expand=True, padx=(0, 4))

            if not es_calendar:
                ctk.CTkButton(
                    bot_row,
                    text="⚙",
                    font=ctk.CTkFont(size=14),
                    width=36,
                    height=34,
                    corner_radius=7,
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

        mensaje = self._abrir_modal_mensaje(f"Capturar {nombre}")
        if mensaje is None:
            self._proceso_en_curso = False
            self.btn.configure(state="normal")
            self._rehabilitar_btns_apps()
            self._set_status("Listo")
            return
        self._mensaje_nota = mensaje

        self._label_estado_app.configure(
            text=f"  ▶  {nombre} — capturando {region['width']}×{region['height']} px…"
        )

        threading.Thread(
            target=self._proceso_app,
            args=(app, region, monitor_idx),
            daemon=True,
        ).start()

    def _subir_a_destinos(self, ruta, ui, prefix=""):
        """Sube la imagen capturada a los destinos configurados.

        Si auto_submit esta desactivado y el destino es HubSpot o AMBOS, la imagen
        se encola en self._cola_imagenes en lugar de subirse inmediatamente. Las
        imagenes encoladas se suben juntas al llamar a _subir_cola_hubspot().

        Args:
            ruta: ruta absoluta del archivo de imagen a subir.
            ui: funcion callback para loguear mensajes (debe ser thread-safe).
            prefix: prefijo opcional para los mensajes de log (ej. "[App] ").

        Efectos secundarios:
            - En modo cola: agrega la imagen a self._cola_imagenes y actualiza
              la UI via _actualizar_cola_ui.
            - En modo directo: llama a self._servicio.ejecutar_subida() por
              cada plugin destino.
            - Respeta self._cancelado para cancelacion entre plugins.
            - Retorna temprano (sin error) si no hay plugins para el destino
              seleccionado.
        """
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
            return

        for plugin in plugins:
            if self._cancelado.is_set():
                ui(f"{prefix}⚠ Cancelado antes de subir a {plugin.nombre}.")
                break

            # Modo cola: HubSpot con auto_submit OFF + destino incluye HubSpot
            if (
                plugin.nombre == "HUBSPOT"
                and not auto_submit
                and destino in ("HUBSPOT", "AMBOS")
            ):
                self._cola_imagenes.append(ruta)
                self._cola_mensajes.append(getattr(self, "_mensaje_nota", "") or "")
                n = len(self._cola_imagenes)
                ui(f"{prefix}→ Imagen encolada ({n} en cola)")
                self.after(0, self._actualizar_cola_ui)
                continue

            ui(f"{prefix}→ Subiendo a {plugin.nombre}…")
            fsd_plugin = fsd
            self._servicio.ejecutar_subida(
                nombre_plugin=plugin.nombre,
                ruta_imagen=ruta,
                log=ui,
                headless=headless,
                usar_chrome_existente=usar_existente,
                credenciales_sesion=self._credenciales_sesion,
                opciones={
                    "auto_submit_nota": auto_submit,
                    "mensaje_nota": getattr(self, "_mensaje_nota", None) or "",
                },
                fsd=fsd_plugin,
                cancel_event=self._cancelado,
            )
            ui("")

    def _actualizar_cola_ui(self):
        """Muestra u oculta el frame de cola de imagenes segun las condiciones.

        El frame se muestra solo si hay imagenes encoladas, auto_submit esta
        desactivado y el destino es HubSpot o AMBOS. En cualquier otro caso se
        oculta.

        Efectos secundarios:
            - Muestra/oculta self._frame_cola con pack()/pack_forget().
            - Actualiza el texto del label con la cantidad de imagenes.
            - Habilita/deshabilita los botones Subir cola y Limpiar.
        """
        n = len(self._cola_imagenes)
        if (
            n > 0
            and not self.auto_submit_var.get()
            and self.destino_var.get() in ("HUBSPOT", "AMBOS")
        ):
            self._frame_cola.pack(fill="x", pady=(12, 0))
            self._label_cola.configure(text=f"Cola: {n} imágen(es)")
            self._btn_subir_cola.configure(state="normal")
            self._btn_limpiar_cola.configure(state="normal")
        else:
            self._frame_cola.pack_forget()

    def _verificar_limpiar_cola(self):
        """Descarta la cola si las condiciones ya no permiten cola activa.

        Si hay imagenes encoladas pero el usuario activa auto_submit o cambia
        el destino a algo distinto de HubSpot/AMBOS, la cola se descarta
        automaticamente con una advertencia en el log.

        Efectos secundarios:
            - Llama a _limpiar_cola(silencioso=False) cuando corresponde.
            - Se dispara desde los trace_add de destino_var y auto_submit_var.
        """
        if self._cola_imagenes:
            auto_submit = self.auto_submit_var.get()
            destino = self.destino_var.get()
            if auto_submit or destino not in ("HUBSPOT", "AMBOS"):
                self._limpiar_cola(silencioso=False)

    def _limpiar_cola(self, silencioso=True):
        """Vacia la cola de imagenes y mensajes asociados.

        Args:
            silencioso: si es True no emite mensaje en el log. Si es False,
                        registra una advertencia explicando el motivo del
                        descarte.

        Efectos secundarios:
            - Vacia self._cola_imagenes y self._cola_mensajes.
            - Actualiza la visibilidad del frame de cola via _actualizar_cola_ui.
        """
        if not self._cola_imagenes:
            return
        self._cola_imagenes.clear()
        self._cola_mensajes.clear()
        self._actualizar_cola_ui()
        if not silencioso:
            self._log("⚠ Cola descartada (cambio de destino o auto-submit).")

    def _subir_cola_hubspot(self):
        """Sube todas las imagenes encoladas a HubSpot en una sola nota.

        Combina los mensajes de cada captura separados por '---' y los envia
        junto con todas las imagenes en una unica llamada a SesionService.
        Bloquea la UI durante el proceso y la restaura al finalizar.

        Efectos secundarios:
            - Deshabilita los botones principales y de cola.
            - Ejecuta self._servicio.ejecutar_subida() con rutas_imagenes
              multiple (la primera como ruta_imagen, todas como lista extra).
            - En exito: vacia la cola, actualiza UI y barra de estado.
            - En error: registra el error en el log.
            - En finally: restaura los botones, libera _proceso_en_curso y
              limpia _cancelado.

        Raises:
            Las excepciones se capturan internamente; no se propagan al
            llamador.
        """
        if not self._cola_imagenes:
            return
        if self._proceso_en_curso:
            self._log("✗ Ya hay un proceso en curso. Espera a que termine.")
            return

        self._proceso_en_curso = True
        self.btn.configure(state="disabled")
        self._btn_subir_cola.configure(state="disabled")
        self._btn_limpiar_cola.configure(state="disabled")

        rutas = list(self._cola_imagenes)
        mensajes = list(self._cola_mensajes)
        auto_submit = self.auto_submit_var.get()
        headless = self.headless_var.get()
        usar_existente = self.chrome_existente_var.get()
        fsd = self._obtener_fsd_actual() or self._fsd_detectado

        # Combinar mensajes: cada uno en su propia línea, separados por ---
        mensaje_combinado = (
            "\n---\n".join(m for m in mensajes if m.strip()) or "Nota de captura."
        )

        def _hilo():
            ui = lambda msg: self.after(0, lambda m=msg: self._log(m))
            ui(f"→ Subiendo cola de {len(rutas)} imágenes a HubSpot…")

            try:
                self._servicio.ejecutar_subida(
                    nombre_plugin="HUBSPOT",
                    ruta_imagen=rutas[0],
                    rutas_imagenes=rutas,
                    log=ui,
                    headless=headless,
                    usar_chrome_existente=usar_existente,
                    credenciales_sesion=self._credenciales_sesion,
                    opciones={
                        "auto_submit_nota": auto_submit,
                        "mensaje_nota": mensaje_combinado,
                    },
                    fsd=fsd,
                    cancel_event=self._cancelado,
                )

                self._cola_imagenes.clear()
                self._cola_mensajes.clear()
                self.after(0, self._actualizar_cola_ui)
                ahora = datetime.now().strftime("%H:%M:%S")
                self.after(
                    0,
                    lambda: self._label_ultimo_proceso.configure(
                        text=f"Último proceso: cola ({len(rutas)} img) {ahora}"
                    ),
                )
                self.after(0, lambda: self._set_status("Completado"))
                self.after(0, self._actualizar_sitios_status)
            except Exception as e:
                self.after(0, lambda: self._log(f"✗ Error subiendo cola: {e}"))
                self.after(0, lambda: self._set_status("Error"))
            finally:
                self._proceso_en_curso = False
                self._cancelado.clear()
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, lambda: self.btn_detener.configure(state="disabled"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_hilo, daemon=True).start()

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
            self.after(0, lambda err=e: self._log(f"✗ {prefix}Error de captura: {err}"))
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

    # ── Modal Mensaje — seleccion de plantilla antes de capturar ──────

    def _abrir_modal_mensaje(self, titulo_btn: str = "Capturar y subir"):
        """Abre un modal para seleccionar/editar el mensaje de la nota.

        Integra plantillas rápidas, gestión de plantillas (vía VentanaPlantillas)
        y generador de mensajes de contacto (vía VentanaGeneradorMensajes).

        Args:
            titulo_btn: texto para el boton principal de accion.

        Returns:
            str con el mensaje seleccionado, o None si el usuario cancela.
        """
        resultado = [None]  # mutable para capturar desde closure

        modal = ctk.CTkToplevel(self)
        modal.title("Mensaje de la nota")
        modal.geometry("820x540")
        modal.minsize(640, 400)
        modal.resizable(True, True)
        modal.transient(self)
        modal.withdraw()

        modal.grid_columnconfigure(0, weight=1)
        modal.grid_columnconfigure(1, weight=2)
        modal.grid_rowconfigure(0, weight=1)

        # ── Columna izquierda: lista de plantillas ──────────────────
        left = ctk.CTkFrame(modal, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 4), pady=(12, 8))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # Cabecera izquierda con botones
        hdr_left = ctk.CTkFrame(left, fg_color="transparent")
        hdr_left.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ctk.CTkLabel(
            hdr_left,
            text="Plantillas",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(side="left")
        ctk.CTkButton(
            hdr_left,
            text="Editar",
            font=ctk.CTkFont(size=10),
            width=48,
            height=22,
            fg_color="transparent",
            border_width=1,
            command=lambda: self._abrir_editor_plantillas(modal, _poblar),
        ).pack(side="right", padx=(4, 0))

        scroll_plantillas = ctk.CTkScrollableFrame(
            left,
            fg_color="transparent",
            width=220,
        )
        scroll_plantillas.grid(row=1, column=0, sticky="nsew")
        scroll_plantillas.grid_columnconfigure(0, weight=1)

        # ── Columna derecha: preview / edicion ──────────────────────
        right = ctk.CTkFrame(modal, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(4, 16), pady=(12, 8))
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        hdr_right = ctk.CTkFrame(right, fg_color="transparent")
        hdr_right.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(
            hdr_right,
            text="Mensaje de la nota",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(side="left")
        ctk.CTkButton(
            hdr_right,
            text="Gen.",
            font=ctk.CTkFont(size=10),
            width=36,
            height=22,
            fg_color="transparent",
            border_width=1,
            command=lambda: self._abrir_generador_mensajes(modal, texto_nota),
        ).pack(side="right")

        texto_nota = ctk.CTkTextbox(
            right,
            font=ctk.CTkFont(size=11),
            wrap="word",
        )
        texto_nota.pack(fill="both", expand=True)

        # ── Funciones auxiliares ────────────────────────────────────
        def _cargar_template_lista():
            """Carga las plantillas desde archivo."""
            return _cargar_plantillas()

        def _poblar():
            """Reconstruye la lista de plantillas en el scroll."""
            for w in scroll_plantillas.winfo_children():
                w.destroy()
            plantillas = _cargar_template_lista()
            categorias = {}
            for p in plantillas:
                cat = p.get("categoria", "General")
                categorias.setdefault(cat, []).append(p)

            row = 0
            for cat in ["HubSpot", "Sunrun", "General"]:
                items = categorias.get(cat, [])
                if not items:
                    continue
                ctk.CTkLabel(
                    scroll_plantillas,
                    text=cat,
                    font=ctk.CTkFont(size=10, weight="bold"),
                    text_color=("gray50", "gray50"),
                ).grid(row=row, column=0, sticky="w", pady=(8, 2), padx=4)
                row += 1

                for p in items:
                    titulo = p.get("titulo", "Sin título")
                    texto = p.get("texto", "")
                    btn = ctk.CTkButton(
                        scroll_plantillas,
                        text=f"  {titulo}",
                        font=ctk.CTkFont(size=11),
                        anchor="w",
                        fg_color="transparent",
                        text_color=("gray30", "gray70"),
                        hover_color=("gray85", "gray30"),
                        height=28,
                        command=lambda t=texto: _seleccionar(t),
                    )
                    btn.grid(row=row, column=0, sticky="ew", pady=1, padx=2)
                    row += 1

        def _seleccionar(texto):
            texto_nota.configure(state="normal")
            texto_nota.delete("1.0", "end")
            texto_nota.insert("1.0", texto)
            texto_nota.configure(state="normal")

        _poblar()

        # ── Botón "+ nueva" ─────────────────────────────────────────
        def _nueva_plantilla():
            texto = texto_nota.get("1.0", "end-1c").strip()
            self._abrir_nueva_plantilla(modal, texto, _poblar)

        btn_nueva = ctk.CTkButton(
            left,
            text="+ nueva plantilla",
            font=ctk.CTkFont(size=10),
            height=28,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
            command=_nueva_plantilla,
        )
        btn_nueva.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        # ── Fila de botones ─────────────────────────────────────────
        btn_row = ctk.CTkFrame(modal, fg_color="transparent")
        btn_row.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(4, 12))
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=1)
        btn_row.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(
            btn_row,
            text="Limpiar",
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray35"),
            hover_color=("gray60", "gray45"),
            command=lambda: _seleccionar(""),
        ).grid(row=0, column=0, padx=(0, 4), sticky="ew")

        ctk.CTkButton(
            btn_row,
            text="Cancelar",
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray35"),
            hover_color=("gray60", "gray45"),
            command=modal.destroy,
        ).grid(row=0, column=1, padx=(2, 2), sticky="ew")

        def _confirmar():
            resultado[0] = texto_nota.get("1.0", "end-1c").strip() or None
            modal.destroy()

        ctk.CTkButton(
            btn_row,
            text=f"  Continuar: {titulo_btn}",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
            command=_confirmar,
        ).grid(row=0, column=2, padx=(4, 0), sticky="ew")

        modal.bind("<Return>", lambda e: _confirmar())
        modal.bind("<Escape>", lambda e: modal.destroy())

        from ui.posicion_ventanas import ubicar_junto_a_padre

        modal.deiconify()
        ubicar_junto_a_padre(modal, self)
        texto_nota.focus_set()
        modal.grab_set()
        modal.wait_window()

        return resultado[0]

    # ── Helpers del modal de mensaje ───────────────────────────────────

    def _abrir_editor_plantillas(self, parent, on_close=None):
        """Abre la ventana de edicion de plantillas como modal.

        Args:
            parent: ventana padre (el modal de mensaje).
            on_close: callback opcional que se ejecuta al cerrar el editor.
                      Tipicamente repuebla la lista de plantillas del modal.

        Efectos secundarios:
            - Abre VentanaPlantillas como ventana hija de parent.
            - Bloquea con parent.wait_window() hasta que el editor se cierre.
            - Si se proporciona on_close, lo ejecuta tras cerrar.
        """
        from ui.ventana_plantillas import VentanaPlantillas

        win = VentanaPlantillas(parent)
        parent.wait_window(win)
        if on_close:
            on_close()

    def _abrir_generador_mensajes(self, parent, texto_widget):
        """Abre el generador de mensajes de contacto e inserta el resultado.

        Args:
            parent: ventana padre (el modal de mensaje).
            texto_widget: CTkTextbox donde insertar el mensaje generado.

        Efectos secundarios:
            - Abre VentanaGeneradorMensajes como ventana hija de parent.
            - Bloquea con parent.wait_window() hasta que el generador cierre.
            - Si el generador produce un resultado (gen.resultado), reemplaza
              el contenido del texto_widget con el mensaje generado.
        """
        from ui.ventana_generador_mensajes import VentanaGeneradorMensajes

        gen = VentanaGeneradorMensajes(parent)
        # wait_window no funciona con grab_set en customtkinter bien,
        # pero el generador cierra automaticamente al copiar (self.destroy)
        parent.wait_window(gen)
        if gen.resultado:
            texto_widget.configure(state="normal")
            texto_widget.delete("1.0", "end")
            texto_widget.insert("1.0", gen.resultado)
            texto_widget.configure(state="normal")

    def _abrir_nueva_plantilla(self, parent, texto_inicial: str, on_save=None):
        """Abre un popup modal para guardar el texto actual como nueva plantilla.

        Args:
            parent: ventana padre (el modal de mensaje).
            texto_inicial: texto a precargar en el campo de mensaje del popup.
            on_save: callback opcional ejecutado tras guardar exitosamente.
                     Tipicamente repuebla la lista de plantillas del modal.

        Efectos secundarios:
            - Muestra un popup con campos de titulo, categoria y mensaje.
            - Al guardar, persiste la plantilla en plantillas.json via
              _guardar_plantillas() y cierra el popup.
            - Si on_save esta definido, lo ejecuta tras el guardado.
        """
        popup = ctk.CTkToplevel(parent)
        popup.title("Nueva plantilla")
        popup.resizable(False, False)
        popup.transient(parent)
        popup.withdraw()

        popup.grid_columnconfigure(0, weight=0)
        popup.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            popup,
            text="Título:",
            font=ctk.CTkFont(size=11),
        ).grid(row=0, column=0, sticky="w", padx=(16, 4), pady=(16, 4))
        titulo_var = ctk.StringVar()
        ctk.CTkEntry(
            popup,
            textvariable=titulo_var,
            font=ctk.CTkFont(size=12),
            width=260,
        ).grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=(16, 4))

        ctk.CTkLabel(
            popup,
            text="Categoría:",
            font=ctk.CTkFont(size=11),
        ).grid(row=1, column=0, sticky="w", padx=(16, 4), pady=4)
        cat_var = ctk.StringVar(value="General")
        ctk.CTkOptionMenu(
            popup,
            variable=cat_var,
            values=["General", "HubSpot", "Sunrun"],
            font=ctk.CTkFont(size=11),
            width=120,
        ).grid(row=1, column=1, sticky="w", padx=(0, 16), pady=4)

        ctk.CTkLabel(
            popup,
            text="Mensaje:",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, sticky="nw", padx=(16, 4), pady=(8, 4))
        texto_box = ctk.CTkTextbox(
            popup,
            font=ctk.CTkFont(size=11),
            wrap="word",
            height=100,
            width=300,
        )
        texto_box.grid(row=2, column=1, sticky="ew", padx=(0, 16), pady=(8, 4))
        if texto_inicial:
            texto_box.insert("1.0", texto_inicial)

        def _guardar():
            titulo = titulo_var.get().strip()
            if not titulo:
                from tkinter import messagebox

                messagebox.showwarning(
                    "Campo vacío", "Escribe un título.", parent=popup
                )
                return
            texto = texto_box.get("1.0", "end-1c").strip()
            plantillas = _cargar_plantillas()
            plantillas.append(
                {
                    "titulo": titulo,
                    "categoria": cat_var.get(),
                    "texto": texto,
                }
            )
            _guardar_plantillas(plantillas)
            popup.destroy()
            if on_save:
                on_save()

        btn_row_p = ctk.CTkFrame(popup, fg_color="transparent")
        btn_row_p.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=16, pady=(12, 16)
        )
        btn_row_p.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_row_p,
            text="Cancelar",
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray35"),
            command=popup.destroy,
        ).grid(row=0, column=0, padx=(0, 4), sticky="ew")

        ctk.CTkButton(
            btn_row_p,
            text="Guardar",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("#1f6aa5", "#1f6aa5"),
            command=_guardar,
        ).grid(row=0, column=1, padx=(4, 0), sticky="ew")

        popup.bind("<Return>", lambda e: _guardar())
        popup.bind("<Escape>", lambda e: popup.destroy())

        from ui.posicion_ventanas import ubicar_junto_a_padre

        popup.deiconify()
        ubicar_junto_a_padre(popup, parent)
        popup.grab_set()
        popup.wait_window()

    # ── Modal Calendar — captura de celda Google Sheets ───────────────

    def _abrir_modal_calendar(self):
        """Abre el modal de captura de celda de Google Sheets (Calendar).

        Permite seleccionar la pestana y la referencia de celda (ej. F6).
        Las pestanas se cargan en un hilo secundario para no bloquear la UI.
        Al confirmar, persiste la ultima celda y pestana en config.json
        y lanza la captura via _ejecutar_captura_calendar() pasando antes
        por el modal de mensaje (_abrir_modal_mensaje).

        Efectos secundarios:
            - Valida que las variables de entorno GOOGLE_SERVICE_ACCOUNT_PATH
              y SHEETS_SPREADSHEET_ID esten configuradas.
            - Carga las pestanas de Google Sheets en background (thread).
            - Abre _abrir_modal_mensaje antes de ejecutar la captura.
        """
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
                messagebox.showwarning(
                    "Celda requerida",
                    "Ingresa una referencia de celda (ej. F6).",
                    parent=modal,
                )
                return
            sheet_name = sheet_var.get().strip() if _sheet_names else None
            config = cargar_config()
            config["ultima_celda_calendar"] = cell_ref
            if sheet_name:
                config["ultima_pestana_calendar"] = sheet_name
            guardar_config(config)
            modal.destroy()

            mensaje = self._abrir_modal_mensaje("Capturar celda")
            if mensaje is None:
                return
            self._mensaje_nota = mensaje

            self._ejecutar_captura_calendar(
                cell_ref, sheet_url, service_account, sheet_name
            )

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

                def _aplicar():
                    self._log(f"→ Pestañas detectadas: {', '.join(_sheet_names)}")
                    sheet_dropdown.configure(values=_sheet_names, state="readonly")
                    if _sheet_names:
                        if (
                            _ultima_pestana_inicial
                            and _ultima_pestana_inicial in _sheet_names
                        ):
                            sheet_var.set(_ultima_pestana_inicial)
                        else:
                            sheet_var.set(_sheet_names[0])

                self.after(0, _aplicar)
            except Exception as e:
                def _error():
                    self._log(f"✗ No se pudieron obtener las pestañas: {e}")
                    sheet_dropdown.configure(values=["(sin pestañas)"], state="disabled")
                    sheet_var.set("")

                self.after(0, _error)

        threading.Thread(target=_load_sheets, daemon=True).start()

        # Posicionar y mostrar
        from ui.posicion_ventanas import ubicar_junto_a_padre

        modal.deiconify()
        ubicar_junto_a_padre(modal, self)
        modal.grab_set()
        modal.wait_window()

    def _ejecutar_captura_calendar(
        self,
        cell_ref: str,
        sheet_url: str,
        service_account: str,
        sheet_name: str | None = None,
    ):
        """Ejecuta la captura de una celda de Google Sheets y la sube a los destinos.

        Usa TicketCaptureService para tomar una captura compuesta de la celda
        indicada y luego sube la imagen via _subir_a_destinos(). Corre en un
        hilo secundario para no bloquear la UI.

        Args:
            cell_ref: referencia de celda (ej. "F6", "AA10").
            sheet_url: ID o URL de la spreadsheet de Google Sheets.
            service_account: ruta al JSON de la service account de Google.
            sheet_name: nombre opcional de la pestana a usar.

        Efectos secundarios:
            - Deshabilita los botones de apps y el boton principal.
            - Logea los valores de las celdas capturadas.
            - Sube la imagen compuesta a los destinos configurados.
            - Restaura los botones y el estado de la UI en el finally.
        """
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
                ui(
                    f"{prefix}→ Iniciando captura de celda {cell_ref} desde Google Sheets{sheet_label}…"
                )
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
                self.after(0, lambda err=e: self._log(f"✗ {prefix}Error: {err}"))
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
                    self.after(
                        0, lambda: self._log(f"✗ Medición cancelada para {nombre}.")
                    )
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
                        icono = next(
                            (a["icono"] for a in APPS_CAPTURA if a["nombre"] == nombre),
                            "",
                        )
                        color_base = next(
                            (a["color"] for a in APPS_CAPTURA if a["nombre"] == nombre),
                            ("#1f6aa5", "#1a5496"),
                        )
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
                self.after(
                    0, lambda err=e: self._log(f"✗ [{nombre}] Error en medidor: {err}")
                )
                self.after(
                    0,
                    lambda: self._label_estado_app.configure(
                        text=f"  ✗ {nombre} — error en medidor"
                    ),
                )
                self.after(0, self.deiconify_window)
                self.after(0, self._rehabilitar_btns_apps)
                self.after(0, lambda: self.btn.configure(state="normal"))
            finally:
                self.after(0, lambda: setattr(self, "_proceso_en_curso", False))

        threading.Thread(target=_esperar, daemon=True).start()

    def _crear_barra_estado(self, padre, col=0):
        """Construye la barra de estado inferior con punto indicador y labels.

        Args:
            padre: widget padre (CTkScrollableFrame).
            col: columna del grid donde ubicar la barra.
        """
        self._frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        self._frame_estado.grid(row=6, column=col, sticky="ew", pady=(4, 0))
        self._punto_estado = ctk.CTkLabel(
            self._frame_estado,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=("#2ea043", "#3fb950"),
        )
        self._punto_estado.pack(side="left")
        self.status_var = ctk.StringVar(value="Listo")
        ctk.CTkLabel(
            self._frame_estado,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(4, 0))
        self._label_estado_app = ctk.CTkLabel(
            self._frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_estado_app.pack(side="left", padx=(12, 0), fill="x", expand=True)
        self._label_ultimo_proceso = ctk.CTkLabel(
            self._frame_estado,
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
        """Detecta el FSD desde el titulo de ventanas visibles de Chrome.

        Enumera las ventanas del sistema via Windows API (EnumWindows) y busca
        en los titulos de ventanas de Chrome/Chromium un patron FSD-XXXXXX o
        FSDXXXXXX. Se llama con la app minimizada para que Chrome este en
        primer plano.

        Returns:
            str con el FSD detectado (formato "FSD-XXXXXX"), o None si no se
            encuentra ninguno.
        """
        import re

        user32 = ctypes.windll.user32

        fsd_encontrado = [None]

        WNDENUMPROC = ctypes.WINFUNCTYPE(
            ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p
        )

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
            match = re.search(r"FSD[-\s]*(\d+)", title, re.IGNORECASE)
            if match:
                fsd = f"FSD-{match.group(1)}"
                fsd_encontrado[0] = fsd
                return False
            return True

        user32.EnumWindows(WNDENUMPROC(enum_proc), 0)
        return fsd_encontrado[0]

    def _buscar_fsd_sunrun(self):
        """Busca un FSD en Sunrun navegando al ticket sin extraer datos.

        Usa ScraperSunrun.navegar_a_fsd() para navegar a la pagina de detalle
        del ticket. No realiza scraping de datos, solo navegacion. Corre en
        un hilo secundario para no bloquear la UI.

        Efectos secundarios:
            - Deshabilita botones durante la ejecucion.
            - Minimiza la ventana principal.
            - Logea el resultado de la navegacion.
            - Restaura los botones y el estado en el finally.
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
                self.after(
                    0, lambda err=e: self._log(f"✗ Error en búsqueda FSD: {err}")
                )
                self.after(0, lambda: self._set_status("Error"))
            finally:
                self._proceso_en_curso = False
                self.after(0, self.deiconify_window)
                self.after(0, lambda: self.btn.configure(state="normal"))
                self.after(0, self._rehabilitar_btns_apps)

        threading.Thread(target=_buscar, daemon=True).start()

    # ── Sitios status ─────────────────────────────────────────────────

    def _actualizar_sitios_status(self):
        """Reconstruye los indicadores de estado de sesion para todos los plugins.

        Para cada plugin registrado verifica si tiene cookies guardadas,
        credenciales configuradas o no necesita login, y muestra el estado
        correspondiente con iconos de color (● verde = sesion activa,
        ◑ naranja = credenciales OK, ○ rojo = sin configurar).

        Efectos secundarios:
            - Destruye y recrea todos los widgets dentro de self._frame_sitios.
        """
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
                self.after(
                    0, lambda: self._log("✗ No se pudo leer la región del medidor.")
                )
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
        if win.confirmado:
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
        if win.confirmado:
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
        from core.browser import (
            puerto_activo,
            CHROME_USER_DATA,
            CHROME_PATHS,
            obtener_chrome_exe,
        )

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

        mensaje = self._abrir_modal_mensaje("Capturar y subir")
        if mensaje is None:
            self._proceso_en_curso = False
            self.btn.configure(state="normal")
            self.btn_detener.configure(state="disabled")
            self._rehabilitar_btns_apps()
            self._set_status("Listo")
            return
        self._mensaje_nota = mensaje

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

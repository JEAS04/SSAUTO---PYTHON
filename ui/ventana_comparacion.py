"""
ventana_comparacion.py — Ventana que muestra la comparación entre Sunrun y HubSpot.

Muestra una tabla con los tres campos comparados, coloreada según el estado
de cada campo:
  · Verde   → igual (coinciden exactamente)
  · Amarillo → similar (pequeñas diferencias tipográficas)
  · Rojo    → diferente (valores distintos)
  · Azul    → solo en HubSpot
  · Naranja → solo en Sunrun
  · Gris    → ambos vacíos

La ventana también permite ingresar un FSD manualmente y lanzar
la comparación desde aquí, sin necesidad de ir a la ventana principal.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox
from ui.custom_ctkframe import CustomCTkFrame
from core.comparador import Comparador, comparar, datos_hs_desde_ticket
from scraping_sunrun import ScraperSunrun
from config.configuracion import cargar_config
from data.buscador import SEARCH_STRATEGIES

# ══════════════════════════════════════════════════════════════════════
#  Colores por estado (modo oscuro / modo claro)
# ══════════════════════════════════════════════════════════════════════

COLORES_ESTADO = {
    "igual": {
        "bg": ("#d4edda", "#1a3a2a"),
        "texto": ("#155724", "#3fb950"),
        "icono": "✅",
    },
    "similar": {
        "bg": ("#fff3cd", "#3a3000"),
        "texto": ("#856404", "#d4a017"),
        "icono": "🟡",
    },
    "diferente": {
        "bg": ("#f8d7da", "#3a1a1a"),
        "texto": ("#721c24", "#f85149"),
        "icono": "❌",
    },
    "solo_hs": {
        "bg": ("#cce5ff", "#1a2a3a"),
        "texto": ("#004085", "#79c0ff"),
        "icono": "🔵",
    },
    "solo_sunrun": {
        "bg": ("#ffe5cc", "#3a2a1a"),
        "texto": ("#804000", "#f0a050"),
        "icono": "🟠",
    },
    "ambos_vacios": {
        "bg": ("#e2e3e5", "#2a2a2a"),
        "texto": ("#6c757d", "#6e7681"),
        "icono": "⚪",
    },
}

ETIQUETAS_ESTADO = {
    "igual": "IGUAL",
    "similar": "SIMILAR",
    "diferente": "DIFERENTE",
    "solo_hs": "SOLO HUBSPOT",
    "solo_sunrun": "SOLO SUNRUN",
    "ambos_vacios": "SIN DATOS",
}

DISPATCH_STATES = {
    "DISPATCH CANCELLED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH REPORTED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH APPROVED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH ACCEPTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
    "DISPATCH REJECTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
}

# ══════════════════════════════════════════════════════════════════════
#  Ventana principal de comparación
# ══════════════════════════════════════════════════════════════════════


class VentanaComparacion(CustomCTkFrame):
    """
    Ventana modal que muestra la comparación de datos entre Sunrun y HubSpot.

    Puede abrirse:
      A) Desde la ventana principal pasando datos ya obtenidos.
      B) Vacía, dejando al usuario ingresar el FSD y lanzar la comparación.

    Parámetros
    ----------
    parent          : ventana padre (App)
    datos_hubspot   : dict con datos de HubSpot (opcional, si ya se obtuvieron)
    datos_sunrun    : dict con datos de Sunrun (opcional, si ya se obtuvieron)
    log_callback    : función de log de la ventana principal
    ventana_principal_o_comparador : referencia a la ventana principal o al comparador
    """

    def __init__(
        self,
        parent,
        datos_hubspot: dict = None,
        datos_sunrun: dict = None,
        log_callback=None,
        comparador=None,
        ventana_principal_o_comparador=None,
    ):

        super().__init__(parent)
        self._log_ext = log_callback or (lambda m: None)
        self._datos_hs = datos_hubspot
        self._datos_sr = datos_sunrun

        self.comparador = comparador

        if self.comparador is None and ventana_principal_o_comparador is not None:
            if hasattr(ventana_principal_o_comparador, "comparador"):
                self.comparador = ventana_principal_o_comparador.comparador
            else:
                self.comparador = ventana_principal_o_comparador

        if self.comparador is None and hasattr(parent, "comparador"):
            self.comparador = parent.comparador

        if self.comparador is None:
            self.comparador = Comparador()

        self.update_idletasks()
        ancho, alto = 820, 560
        px = max(0, (self.winfo_screenwidth() - ancho) // 2)
        py = max(0, (self.winfo_screenheight() - alto) // 2)
        self.search_strategy = "direccion"
        self.candidatos_hubspot = []
        self.candidato_seleccionado = None
        self.radio_var = ctk.IntVar()
        self._construir_ui()

        self.after(50, self._traer_al_frente)

        if datos_hubspot and datos_sunrun:
            self.after(100, self._mostrar_resultado_externo)

    def _traer_al_frente(self):
        """Asegura que la ventana aparezca al frente al abrirse."""
        try:
            # FIX #4: VentanaComparacion hereda de CustomCTkFrame (un Frame,
            # no un Toplevel), así que self.state() no existe y lanzaba
            # AttributeError silenciado. Ahora subimos al toplevel real
            # con winfo_toplevel() antes de llamar state()/deiconify().
            root = self.winfo_toplevel()
            if root.state() == "iconic":
                root.deiconify()
            root.lift()
            root.focus_force()
            root.attributes("-topmost", True)
            self.after(200, lambda: root.attributes("-topmost", False))
        except Exception:
            pass

    def _cerrar(self):
        """Cierra la ventana de comparación limpiamente."""
        try:
            self.destroy()
        except Exception:
            pass

    # ── Construcción de la UI ─────────────────────────────────────────

    def _construir_ui(self):
        """Construye la UI completa"""

        # CONFIGURACIÓN GENERAL
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # ── Encabezado ────────────────────────────────────────────────

        enc = ctk.CTkFrame(self, fg_color=("gray88", "gray20"), height=50)
        enc.grid(row=0, column=0, sticky="ew")
        enc.grid_propagate(False)

        ctk.CTkLabel(
            enc,
            text="  🔍  Comparación de datos: HubSpot ↔ Sunrun",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=16, pady=12)

        # FRAME SUPERIOR (BÚSQUEDA)
        frame_busqueda = ctk.CTkFrame(self, fg_color=("gray95", "gray18"))
        frame_busqueda.grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 0))

        frame_busqueda.grid_columnconfigure(0, weight=1)

        # Label
        ctk.CTkLabel(
            frame_busqueda,
            text="Tipo de Búsqueda",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

        # ComboBox estrategias

        estrategias = [v["label"] for v in SEARCH_STRATEGIES.values()]

        self.combo_tipo_busqueda = ctk.CTkComboBox(
            frame_busqueda,
            values=estrategias,
            state="readonly",
            command=self._al_cambiar_tipo_busqueda,
        )

        self.combo_tipo_busqueda.grid(
            row=1, column=0, sticky="ew", padx=14, pady=(0, 10)
        )

        self.combo_tipo_busqueda.set(SEARCH_STRATEGIES["direccion"]["label"])

        # FRAME INPUTS DINÁMICOS
        self.frame_inputs = ctk.CTkFrame(frame_busqueda, fg_color="transparent")

        self.frame_inputs.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))

        self.frame_inputs.grid_columnconfigure(0, weight=1)

        # INPUT FSD DEFAULT
        self._fsd_var = ctk.StringVar()

        self._entry_fsd = ctk.CTkEntry(
            self.frame_inputs,
            textvariable=self._fsd_var,
            placeholder_text="Ej: FSD983316",
            font=ctk.CTkFont(size=12),
            height=34,
        )

        self._entry_fsd.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=2)

        self._entry_fsd.bind("<Return>", lambda e: self._buscar_candidatos())

        # BOTÓN BUSCAR
        self._btn_buscar = ctk.CTkButton(
            frame_busqueda,
            text="🔍 Buscar en HubSpot",
            command=self._buscar_candidatos,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )

        self._btn_buscar.grid(row=3, column=0, sticky="ew", padx=14, pady=(0, 14))

        # ÁREA PRINCIPAL         # ── Área de resultados ────────────────────────────────────────
        self._frame_main = ctk.CTkFrame(self, fg_color="transparent")

        self._frame_main.grid(row=2, column=0, sticky="nsew", padx=12, pady=(10, 0))

        self._frame_main.grid_columnconfigure(0, weight=1)
        self._frame_main.grid_rowconfigure(1, weight=1)
        self._frame_main.grid_rowconfigure(3, weight=2)

        # TABLA CANDIDATOS
        ctk.CTkLabel(
            self._frame_main,
            text="Resultados en HubSpot",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.frame_tabla = ctk.CTkScrollableFrame(
            self._frame_main,
            fg_color=("gray95", "gray18"),
            height=180,
        )

        self.frame_tabla.grid(row=1, column=0, sticky="nsew")

        self.frame_tabla.grid_columnconfigure(0, weight=1)

        # Placeholder tabla
        self._label_placeholder_tabla = ctk.CTkLabel(
            self.frame_tabla,
            text="No hay resultados todavía.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

        self._label_placeholder_tabla.grid(row=0, column=0, pady=30)

        # BOTÓN COMPARAR
        self._btn_comparar = ctk.CTkButton(
            self._frame_main,
            text="▶ Comparar Seleccionado",
            command=self._lanzar_comparacion_mejorada,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#1976D2", "#1565C0"),
            hover_color=("#1565C0", "#0D47A1"),
        )

        self._btn_comparar.grid(row=2, column=0, sticky="ew", pady=(10, 10))

        # FRAME RESULTADOS
        self._frame_resultados = ctk.CTkScrollableFrame(
            self._frame_main,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )

        self._frame_resultados.grid(row=3, column=0, sticky="nsew")

        self._frame_resultados.grid_columnconfigure(0, weight=1)

        # Placeholder resultados
        self._label_placeholder = ctk.CTkLabel(
            self._frame_resultados,
            text="Selecciona un candidato y presiona Comparar.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

        self._label_placeholder.grid(row=0, column=0, pady=40)

        # ── Barra de estado ───────────────────────────────────────────
        self._status_var = ctk.StringVar(value="Listo")

        barra = ctk.CTkFrame(self, fg_color=("gray88", "gray20"), height=30)

        barra.grid(row=3, column=0, sticky="ew", pady=(8, 0))

        barra.grid_propagate(False)

        ctk.CTkLabel(
            barra,
            textvariable=self._status_var,
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=12)

    def ui_log(self, mensaje: str, tipo: str = "info"):
        """
        Actualiza barra de estado y opcionalmente imprime logs.
        """

        self._status_var.set(mensaje)

        # Opcional: imprimir en consola
        print(f"[{tipo.upper()}] {mensaje}")

        # Refrescar UI
        self.update_idletasks()

    def _lanzar_comparacion(self):
        fsd = self._fsd_var.get().strip()
        if not fsd:
            messagebox.showwarning("FSD vacío", "Ingresa un número FSD.", parent=self)
            return

        self._btn_comparar.configure(state="disabled")
        self._status_var.set(f"Buscando {fsd}...")
        self._limpiar_resultados()

        threading.Thread(
            target=self._proceso_comparacion, args=(fsd,), daemon=True
        ).start()

    def _proceso_comparacion(self, fsd: str):
        """
        Hilo secundario: obtiene datos de Sunrun (Chrome), luego de HubSpot
        (API), compara y actualiza la UI con self.after().
        """

        def ui_log(msg):
            self.after(0, lambda m=msg: self._log_ext(m))
            self.after(0, lambda m=msg: self._status_var.set(m.strip()))

        try:
            ui_log(f"  → Buscando {fsd} en Sunrun...")
            scraper = ScraperSunrun(log_callback=ui_log)
            datos_sr = scraper.obtener_datos_por_fsd(fsd)

            ui_log("  → Obteniendo datos desde HubSpot...")
            datos_hs = self._obtener_hubspot(fsd, ui_log)

            ui_log("  → Comparando campos...")
            resultado = comparar(datos_hs, datos_sr)
            resultado["fsd"] = fsd
            resultado["_sunrun_extra"] = {
                "dispatch_state": datos_sr.get("dispatch_state", ""),
                "appointment_date": datos_sr.get("appointment_date", ""),
                "case_reason": datos_sr.get("case_reason", ""),
            }

            self.after(0, lambda r=resultado: self._mostrar_resultado(r))

        except Exception as e:
            self.after(0, lambda err=e: self._mostrar_error(str(err)))
        finally:
            self.after(0, lambda: self._btn_comparar.configure(state="normal"))
            self.after(0, lambda: self._status_var.set("Listo"))

    def _obtener_hubspot(self, fsd: str, log) -> dict:
        _vacio = {
            "fsd": fsd,
            "ticket_id": None,
            "contact_id": None,
            "nombre": "",
            "id_cliente": "",
            "direccion": "",
            "telefono": "",
            "telefono_alterno": "",
            "email": "",
            "estado": "",
            "municipio": "",
            "zip": "",
            "nota": "",
            "fuente_nombre": "",
            "fuente_id": "",
            "fuente": "HubSpot",
        }
        try:
            from data.api import extraer_datos_hubspot

            datos = extraer_datos_hubspot(fsd)
            if datos.get("error"):
                log(f"  ⚠ HubSpot: {datos['error']}")
            return datos_hs_desde_ticket(datos)

        except ImportError:
            log("  ⚠  api.py no disponible. Usando datos vacíos para HubSpot.")
            return {**_vacio, "error": "Módulo  api.py no disponible."}

        except Exception as e:
            log(f"  ✗ Error al consultar HubSpot: {e}")
            return {**_vacio, "error": str(e)}

    # ── Renderizado de resultados ──────────────────────────────────────
    def _al_cambiar_tipo_busqueda(self, nuevo_tipo_label):
        """Se dispara cuando cambia el dropdown de tipo de búsqueda"""

        # Encontrar la clave del tipo seleccionado
        self.search_strategy = [
            k for k, v in SEARCH_STRATEGIES.items() if v["label"] == nuevo_tipo_label
        ][0]

        # Limpiar inputs previos
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

        # Crear inputs dinámicos según cantidad
        estrategia = SEARCH_STRATEGIES[self.search_strategy]
        input_count = estrategia["input_count"]

        self.criterio_inputs = []

        if input_count == 1:
            entrada = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder", "Buscar..."),
            )
            entrada.pack(fill="x")
            self.criterio_inputs.append(entrada)

        elif input_count == 2:
            entrada1 = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder_1", "Campo 1"),
            )
            entrada1.pack(fill="x", pady=(0, 5))
            self.criterio_inputs.append(entrada1)

            entrada2 = ctk.CTkEntry(
                self.frame_inputs,
                placeholder_text=estrategia.get("placeholder_2", "Campo 2"),
            )
            entrada2.pack(fill="x")
            self.criterio_inputs.append(entrada2)

    def _obtener_criterio_busqueda(self):
        """Lee los inputs según tipo seleccionado"""

        estrategia = SEARCH_STRATEGIES[self.search_strategy]
        input_count = estrategia["input_count"]

        if input_count == 1:
            return self.criterio_inputs[0].get()
        elif input_count == 2:
            return {
                "criterio1": self.criterio_inputs[0].get(),
                "criterio2": self.criterio_inputs[1].get(),
            }

    def _buscar_candidatos(self):
        """Busca candidatos en HubSpot según criterio"""
        criterio = self._obtener_criterio_busqueda()

        if not criterio or (isinstance(criterio, dict) and not all(criterio.values())):
            self.ui_log("❌ Rellena todos los campos de búsqueda", "error")
            return

        self.ui_log("🔄 Buscando en HubSpot...", "info")

        try:
            self.candidatos_hubspot = self.comparador.buscar_hubspot_por_estrategia(
                criterio, self.search_strategy
            )

            if not self.candidatos_hubspot:
                self.ui_log("❌ No se encontraron resultados", "warning")
                return

            self._mostrar_candidatos()
            self.ui_log(
                f"✅ Se encontraron {len(self.candidatos_hubspot)} resultado(s)",
                "success",
            )

        except Exception as e:
            self.ui_log(f"❌ Error en búsqueda: {str(e)}", "error")

    def _mostrar_candidatos(self):
        """Muestra los candidatos en la tabla"""
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        self.radio_var.set(-1)

        for idx, candidato in enumerate(self.candidatos_hubspot):
            frame_fila = ctk.CTkFrame(
                self.frame_tabla, fg_color="#2a2a2a", corner_radius=5
            )
            frame_fila.pack(fill="x", pady=3, padx=5)

            # Radio button
            rb = ctk.CTkRadioButton(
                frame_fila, text="", variable=self.radio_var, value=idx
            )
            rb.pack(side="left", padx=5)

            # Datos del candidato
            nombre = candidato.get("nombre", "N/A")
            direccion = candidato.get("direccion", "N/A")
            municipio = candidato.get("municipio", "N/A")
            fsd = candidato.get("fsd", "N/A")

            info_text = f"{nombre} | {direccion} | {municipio} | FSD: {fsd}"

            ctk.CTkLabel(
                frame_fila,
                text=info_text,
                font=("Segoe UI", 10),
                text_color="#CCCCCC",
                justify="left",
            ).pack(side="left", padx=10, fill="x", expand=True)

    def _obtener_candidato_seleccionado(self):
        """Devuelve el candidato seleccionado o None"""
        idx = self.radio_var.get()
        if idx >= 0 and idx < len(self.candidatos_hubspot):
            return self.candidatos_hubspot[idx]
        return None

    def _lanzar_comparacion_mejorada(self):
        """Nueva versión que usa el candidato seleccionado"""
        candidato = self._obtener_candidato_seleccionado()

        if not candidato:
            self.ui_log("⚠️  Selecciona un candidato para comparar", "warning")
            return

        self.ui_log("🔄 Extrayendo FSD y buscando en Sunrun...", "info")

        try:
            resultado = self.comparador.comparar_con_fsd_automatico(candidato)

            if "error" in resultado:
                self.ui_log(f"❌ {resultado['error']}", "error")
                return

            self._mostrar_resultado(resultado)
            self.ui_log("✅ Comparación completada", "success")

        except Exception as e:
            self.ui_log(f"❌ Error en comparación: {str(e)}", "error")

    def _limpiar_resultados(self):
        for widget in self._frame_resultados.winfo_children():
            widget.destroy()

    def _mostrar_resultado_externo(self):

        resultado = comparar(self._datos_hs, self._datos_sr)

        resultado["_sunrun_extra"] = {
            "dispatch_state": self._datos_sr.get("dispatch_state", ""),
            "appointment_date": self._datos_sr.get("appointment_date", ""),
            "case_reason": self._datos_sr.get("case_reason", ""),
        }

        self._mostrar_resultado(resultado)

    def _mostrar_resultado(self, resultado: dict):
        """
        Renderiza la tabla de comparación con colores por estado.

        FIX #4: antes se llamaba self.state() y self.deiconify() directamente
        sobre el Frame, lo que lanzaba AttributeError silenciado y nunca
        restauraba la ventana. Ahora se delega al toplevel real.
        """
        self._limpiar_resultados()

        # Restaurar toplevel si estaba minimizado y traer al frente
        try:
            root = self.winfo_toplevel()
            if root.state() == "iconic":
                root.deiconify()
            root.lift()
            root.focus_force()
        except Exception:
            pass

        frame = self._frame_resultados
        fila = 0

        # ── Encabezado del ticket ─────────────────────────────────────
        hdr = ctk.CTkFrame(frame, fg_color=("gray85", "gray22"), border_width=1)
        hdr.grid(row=fila, column=0, sticky="ew", pady=(0, 8))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr,
            text=f"  Ticket: {resultado['fsd']}",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=10)
        fila += 1
        sunrun_extra = resultado.get("_sunrun_extra")

        if sunrun_extra:
            estado_dispatch = sunrun_extra.get("dispatch_state", "").strip().upper()

            header_color = ("#804000", "#f0a050")
            frame_color = ("#ffe5cc", "#3a2a1a")

            if estado_dispatch in [
                "DISPATCH CANCELLED",
                "DISPATCH REPORTED",
                "DISPATCH APPROVED",
            ]:
                header_color = ("#721c24", "#f85149")
                frame_color = ("#f8d7da", "#3a1a1a")

            elif estado_dispatch in [
                "DISPATCH ACCEPTED",
                "DISPATCH REJECTED",
            ]:
                header_color = ("#155724", "#3fb950")
                frame_color = ("#d4edda", "#1a3a2a")

            sr_frame = ctk.CTkFrame(
                frame,
                fg_color=frame_color,
                border_width=1,
            )

            sr_frame.grid(
                row=fila,
                column=0,
                sticky="ew",
                pady=(0, 8),
            )

            sr_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                sr_frame,
                text="☀ Sunrun",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=header_color,
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=14,
                pady=(10, 6),
            )

            campos_extra = [
                ("Dispatch State", sunrun_extra.get("dispatch_state", "")),
                ("Appointment Date", sunrun_extra.get("appointment_date", "")),
                ("Case Reason", sunrun_extra.get("case_reason", "")),
            ]

            for idx, (label, valor) in enumerate(campos_extra, start=1):

                ctk.CTkLabel(
                    sr_frame,
                    text=f"{label}:",
                    font=ctk.CTkFont(size=11, weight="bold"),
                ).grid(
                    row=idx,
                    column=0,
                    sticky="nw",
                    padx=(14, 8),
                    pady=2,
                )

                color = None
                font_weight = "normal"

                if label == "Dispatch State":

                    estado = str(valor).strip().upper()

                    if estado in [
                        "DISPATCH CANCELLED",
                        "DISPATCH REPORTED",
                        "DISPATCH APPROVED",
                    ]:
                        color = "red"
                        font_weight = "bold"
                        valor = f"{valor} → No es trabajable"

                    elif estado in [
                        "DISPATCH ACCEPTED",
                        "DISPATCH REJECTED",
                    ]:
                        color = "green"
                        font_weight = "bold"
                        valor = f"{valor} → Es trabajable"

                ctk.CTkLabel(
                    sr_frame,
                    text=valor or "-",
                    font=ctk.CTkFont(size=11, weight=font_weight),
                    wraplength=320,
                    justify="left",
                    anchor="w",
                    text_color=color,
                ).grid(
                    row=idx,
                    column=1,
                    sticky="ew",
                    padx=(0, 14),
                    pady=2,
                )
        fila += 1

        # ── Errores (si los hay) ──────────────────────────────────────
        if resultado.get("tiene_error") and resultado.get("errores"):
            err_frame = ctk.CTkFrame(
                frame, fg_color=("#f8d7da", "#3a1a1a"), border_width=1
            )
            err_frame.grid(row=fila, column=0, sticky="ew", pady=(0, 8))
            for err in resultado["errores"]:
                ctk.CTkLabel(
                    err_frame,
                    text=f"  ⚠ {err}",
                    font=ctk.CTkFont(size=11),
                    text_color=("#721c24", "#f85149"),
                    wraplength=700,
                    justify="left",
                ).pack(anchor="w", padx=14, pady=4)
            fila += 1

        # ── Encabezados de columnas ───────────────────────────────────
        cols_hdr = ctk.CTkFrame(frame, fg_color=("gray80", "gray28"))
        cols_hdr.grid(row=fila, column=0, sticky="ew", pady=(0, 2))
        cols_hdr.grid_columnconfigure(0, weight=2)
        cols_hdr.grid_columnconfigure(1, weight=3)
        cols_hdr.grid_columnconfigure(2, weight=3)
        cols_hdr.grid_columnconfigure(3, weight=2)

        for i, titulo in enumerate(["Campo", "HubSpot", "Sunrun", "Estado"]):
            ctk.CTkLabel(
                cols_hdr,
                text=titulo,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=("gray30", "gray70"),
            ).grid(row=0, column=i, sticky="w", padx=14, pady=6)
        fila += 1

        # ── Filas de campos ───────────────────────────────────────────
        for campo_resultado in resultado["campos"]:
            self._fila_campo(frame, fila, campo_resultado)
            fila += 1

        # ── Resumen ───────────────────────────────────────────────────
        fila += 1
        self._resumen(frame, fila, resultado["resumen"])

    def _fila_campo(self, parent, fila: int, cr: dict):
        estado = cr["estado"]
        colores = COLORES_ESTADO.get(estado, COLORES_ESTADO["ambos_vacios"])

        row_frame = ctk.CTkFrame(
            parent,
            fg_color=colores["bg"],
            border_width=1,
        )
        row_frame.grid(row=fila, column=0, sticky="ew", pady=2)
        row_frame.grid_columnconfigure(0, weight=2)
        row_frame.grid_columnconfigure(1, weight=3)
        row_frame.grid_columnconfigure(2, weight=3)
        row_frame.grid_columnconfigure(3, weight=2)

        def celda(texto, col, bold=False):
            ctk.CTkLabel(
                row_frame,
                text=texto,
                font=ctk.CTkFont(size=11, weight="bold" if bold else "normal"),
                text_color=colores["texto"],
                wraplength=180,
                justify="left",
                anchor="w",
            ).grid(row=0, column=col, sticky="w", padx=14, pady=10)

        celda(cr["campo"], col=0, bold=True)
        celda(cr["valor_hs"], col=1)
        celda(cr["valor_sr"], col=2)

        estado_txt = f"{colores['icono']} {ETIQUETAS_ESTADO.get(estado, estado)}"
        ctk.CTkLabel(
            row_frame,
            text=estado_txt,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colores["texto"],
        ).grid(row=0, column=3, sticky="w", padx=14, pady=10)

        if cr.get("nota") and estado not in ("igual", "ambos_vacios"):
            nota_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            nota_frame.grid(row=1, column=0, columnspan=4, sticky="ew")
            ctk.CTkLabel(
                nota_frame,
                text=f"  ℹ {cr['nota']}",
                font=ctk.CTkFont(size=10),
                text_color=colores["texto"],
            ).grid(row=0, column=0, sticky="w", padx=14, pady=(0, 6))

    def _resumen(self, parent, fila: int, resumen: dict):
        frame = ctk.CTkFrame(parent, fg_color=("gray88", "gray22"), border_width=1)
        frame.grid(row=fila, column=0, sticky="ew", pady=(12, 4))

        ctk.CTkLabel(
            frame,
            text="  Resumen:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).pack(side="left", padx=(14, 16), pady=10)

        orden = [
            "igual",
            "similar",
            "diferente",
            "solo_hs",
            "solo_sunrun",
            "ambos_vacios",
        ]
        for estado in orden:
            count = resumen.get(estado, 0)
            if count == 0:
                continue
            col = COLORES_ESTADO[estado]
            ctk.CTkLabel(
                frame,
                text=f"{col['icono']} {ETIQUETAS_ESTADO[estado]}: {count}",
                font=ctk.CTkFont(size=10),
                text_color=col["texto"],
            ).pack(side="left", padx=8, pady=10)

    def _mostrar_error(self, mensaje: str):
        self._limpiar_resultados()
        ctk.CTkLabel(
            self._frame_resultados,
            text=f"✗ {mensaje}",
            font=ctk.CTkFont(size=12),
            text_color=("red", "#f85149"),
            wraplength=600,
        ).grid(row=0, column=0, pady=40)


if __name__ == "__main__":
    config = cargar_config()
    ctk.set_appearance_mode(config.get("tema", "dark"))
    root = ctk.CTk()
    root.withdraw()
    app = VentanaComparacion(root)
    root.mainloop()

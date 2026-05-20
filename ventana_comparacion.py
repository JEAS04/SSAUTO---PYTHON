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

from comparador import comparar, datos_hs_desde_ticket
from scraping_sunrun import ScraperSunrun

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


# ══════════════════════════════════════════════════════════════════════
#  Ventana principal de comparación
# ══════════════════════════════════════════════════════════════════════


class VentanaComparacion(ctk.CTkToplevel):
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
    """

    def __init__(
        self,
        parent,
        datos_hubspot: dict = None,
        datos_sunrun: dict = None,
        log_callback=None,
    ):
        super().__init__(parent)
        self.title("Comparación HubSpot ↔ Sunrun")
        self.resizable(True, True)
        # grab_set() removido: causaba bloqueo de la ventana principal.
        # transient() removido: causaba que la ventana desapareciera al usar
        # "Mostrar escritorio" de Windows y no se pudiera recuperar.
        # La ventana ahora es independiente (toplevel normal).

        self._log_ext = log_callback or (lambda m: None)
        self._datos_hs = datos_hubspot
        self._datos_sr = datos_sunrun

        # Tamaño y centrado
        self.update_idletasks()
        ancho, alto = 820, 560
        px = max(0, (self.winfo_screenwidth() - ancho) // 2)
        py = max(0, (self.winfo_screenheight() - alto) // 2)
        self.geometry(f"{ancho}x{alto}+{px}+{py}")
        self.minsize(600, 400)

        self._construir_ui()

        # Manejar cierre con X correctamente
        self.protocol("WM_DELETE_WINDOW", self._cerrar)

        # Traer al frente al abrir
        self.after(50, self._traer_al_frente)

        # Si ya vienen datos, mostrarlos directamente
        if datos_hubspot and datos_sunrun:
            self.after(100, self._mostrar_resultado_externo)

    def _traer_al_frente(self):
        """Asegura que la ventana aparezca al frente al abrirse."""
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            self.attributes("-topmost", True)
            self.after(200, lambda: self.attributes("-topmost", False))
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

        # ── Fila de búsqueda ──────────────────────────────────────────
        fila_busqueda = ctk.CTkFrame(self, fg_color=("gray95", "gray18"))
        fila_busqueda.grid(row=1, column=0, sticky="ew", padx=12, pady=(10, 0))
        fila_busqueda.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            fila_busqueda,
            text="FSD:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, padx=(14, 8), pady=12)

        self._fsd_var = ctk.StringVar()
        self._entry_fsd = ctk.CTkEntry(
            fila_busqueda,
            textvariable=self._fsd_var,
            placeholder_text="Ej: FSD983316",
            font=ctk.CTkFont(size=12),
        )
        self._entry_fsd.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=12)
        self._entry_fsd.bind("<Return>", lambda e: self._lanzar_comparacion())

        self._btn_comparar = ctk.CTkButton(
            fila_busqueda,
            text="Comparar",
            command=self._lanzar_comparacion,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=110,
            height=34,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self._btn_comparar.grid(row=0, column=2, padx=(0, 14), pady=12)

        # ── Área de resultados ────────────────────────────────────────
        self._frame_resultados = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._frame_resultados.grid(
            row=2, column=0, sticky="nsew", padx=12, pady=(10, 0)
        )
        self._frame_resultados.grid_columnconfigure(0, weight=1)

        # Placeholder inicial
        self._label_placeholder = ctk.CTkLabel(
            self._frame_resultados,
            text="Ingresa un número FSD y presiona Comparar.",
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

    # ── Lanzar comparación desde el campo FSD ─────────────────────────

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
            # 1. Sunrun via scraping
            ui_log(f"  → Buscando {fsd} en Sunrun...")
            scraper = ScraperSunrun(log_callback=ui_log)
            datos_sr = scraper.obtener_datos_por_fsd(fsd)

            # 2. HubSpot via API
            ui_log("  → Obteniendo datos desde HubSpot...")
            datos_hs = self._obtener_hubspot(fsd, ui_log)

            # 3. Comparar
            ui_log("  → Comparando campos...")
            resultado = comparar(datos_hs, datos_sr)
            resultado["fsd"] = fsd

            # 4. Mostrar en la UI (hilo principal)
            self.after(0, lambda r=resultado: self._mostrar_resultado(r))

        except Exception as e:
            self.after(0, lambda err=e: self._mostrar_error(str(err)))
        finally:
            self.after(0, lambda: self._btn_comparar.configure(state="normal"))
            self.after(0, lambda: self._status_var.set("Listo"))

    def _obtener_hubspot(self, fsd: str, log) -> dict:
        """
        Obtiene los datos del ticket + contacto de HubSpot usando  api.py.
        Importa dinámicamente para no acoplar el módulo si la API no está disponible.
        """
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
            from api import extraer_datos_hubspot

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

    def _limpiar_resultados(self):
        """Elimina todos los widgets del área de resultados."""
        for widget in self._frame_resultados.winfo_children():
            widget.destroy()

    def _mostrar_resultado_externo(self):
        """Muestra datos ya obtenidos externamente (pasados al constructor)."""
        resultado = comparar(self._datos_hs, self._datos_sr)
        self._mostrar_resultado(resultado)

    def _mostrar_resultado(self, resultado: dict):
        """
        Renderiza la tabla de comparación con colores por estado.
        Tras comparar, trae la ventana al frente si estaba minimizada.
        """
        self._limpiar_resultados()
        # Restaurar si estaba minimizada y traer al frente
        try:
            if self.state() == "iconic":
                self.deiconify()
            self.lift()
            self.focus_force()
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
        cols_hdr.grid_columnconfigure(0, weight=2)  # campo
        cols_hdr.grid_columnconfigure(1, weight=3)  # HubSpot
        cols_hdr.grid_columnconfigure(2, weight=3)  # Sunrun
        cols_hdr.grid_columnconfigure(3, weight=2)  # estado

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
        """Renderiza una fila de la tabla para un campo comparado."""
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

        # Celda de estado con icono
        estado_txt = f"{colores['icono']} {ETIQUETAS_ESTADO.get(estado, estado)}"
        ctk.CTkLabel(
            row_frame,
            text=estado_txt,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=colores["texto"],
        ).grid(row=0, column=3, sticky="w", padx=14, pady=10)

        # Tooltip de nota (fila expandida si hay nota relevante)
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
        """Muestra el resumen de conteos por estado al final de la tabla."""
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
        """Muestra un error general en el área de resultados."""
        self._limpiar_resultados()
        ctk.CTkLabel(
            self._frame_resultados,
            text=f"✗ {mensaje}",
            font=ctk.CTkFont(size=12),
            text_color=("red", "#f85149"),
            wraplength=600,
        ).grid(row=0, column=0, pady=40)

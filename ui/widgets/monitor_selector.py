"""
ui/widgets/monitor_selector.py — Selector de monitor con info de resolucion.
"""

import customtkinter as ctk
from tkinter import StringVar


class MonitorSelectorWidget(ctk.CTkFrame):
    """Dropdown de monitores con etiqueta de dimensiones.

    Muestra una lista de monitores detectados (ej. "Monitor 1 (principal)")
    y al lado la resolucion en pixeles (ej. "1920x1080 px"). Al cambiar la
    seleccion, dispara un callback opcional.

    Args:
        parent: widget padre.
        nombres_monitores: lista de nombres legibles (de obtener_nombres_monitores).
        monitores_raw: lista de dicts de monitores (de obtener_monitores).
        indice_inicial: indice del monitor seleccionado por defecto.
        on_change: callback sin argumentos al cambiar la seleccion.
    """

    def __init__(
        self,
        parent,
        nombres_monitores: list[str],
        monitores_raw: list[dict],
        indice_inicial: int = 0,
        on_change=None,
    ):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._monitores_raw = monitores_raw
        self._nombres = nombres_monitores or ["Monitor 1 (principal)"]
        self._on_change = on_change

        valor_inicial = (
            self._nombres[indice_inicial]
            if 0 <= indice_inicial < len(self._nombres)
            else self._nombres[0]
        )

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=2)

        ctk.CTkLabel(
            row, text="Monitor:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))

        self.monitor_var = StringVar(value=valor_inicial)
        self.monitor_menu = ctk.CTkOptionMenu(
            row, variable=self.monitor_var,
            values=self._nombres,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False, width=190,
        )
        self.monitor_menu.pack(side="left", padx=(0, 6))

        self.info_label = ctk.CTkLabel(
            row, text="", font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.info_label.pack(side="left")

        self._actualizar_info()
        self.monitor_var.trace_add("write", self._al_cambiar)

    def _al_cambiar(self, *_):
        self._actualizar_info()
        if self._on_change:
            self._on_change()

    def _actualizar_info(self):
        indice = self.obtener_indice()
        if 0 <= indice < len(self._monitores_raw):
            m = self._monitores_raw[indice]
            self.info_label.configure(text=f"{m['width']}x{m['height']} px")

    def obtener_indice(self) -> int:
        """Devuelve el indice del monitor seleccionado (0 = virtual)."""
        try:
            return self._nombres.index(self.monitor_var.get())
        except ValueError:
            return 1

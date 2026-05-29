"""
ui/widgets/coordinate_inputs.py — Campos de coordenadas de captura (top/left/width/height).
"""

import customtkinter as ctk
from tkinter import StringVar


class CoordinateInputsWidget(ctk.CTkFrame):
    """Fila de 4 campos numericos etiquetados: TOP, LEFT, WIDTH, HEIGHT."""

    def __init__(self, parent, valores_iniciales=None, on_change=None, font_size=9):
        super().__init__(parent, fg_color="transparent")
        self.region_vars = {}
        self._on_change = on_change

        campos = [
            ("top", 392),
            ("left", 524),
            ("width", 934),
            ("height", 404),
        ]

        iniciales = valores_iniciales or {}
        for i, (etiqueta, valor_default) in enumerate(campos):
            valor = iniciales.get(etiqueta, valor_default)
            caja = ctk.CTkFrame(
                self,
                fg_color=("gray90", "gray25"),
                border_width=1,
            )
            caja.pack(side="left", padx=(0 if i == 0 else 6, 0), ipadx=12)

            ctk.CTkLabel(
                caja, text=etiqueta.upper(),
                font=ctk.CTkFont(size=font_size, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))

            var = StringVar(value=str(valor))
            ctk.CTkEntry(
                caja, textvariable=var, width=80,
                font=ctk.CTkFont(size=font_size + 4, weight="bold"),
                justify="center", border_width=0,
            ).pack(pady=(0, 6))

            if on_change:
                var.trace_add("write", lambda *_, v=var: self._notificar())
            self.region_vars[etiqueta] = var

    def _notificar(self):
        if self._on_change:
            self._on_change()

    def aplicar_region(self, region: dict):
        """Actualiza los campos con valores de un dict de region."""
        for clave in ("top", "left", "width", "height"):
            if clave in region and clave in self.region_vars:
                self.region_vars[clave].set(str(int(region[clave])))

    def obtener_region(self) -> dict:
        """Devuelve los valores actuales como dict de enteros."""
        return {
            clave: int(var.get() or 0)
            for clave, var in self.region_vars.items()
        }

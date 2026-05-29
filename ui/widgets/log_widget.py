"""
ui/widgets/log_widget.py — Widget de registro con marcas de tiempo y colores.

Extraído de ui/ventana_principal.py para reutilización y reducción del
tamaño del archivo principal.
"""

import customtkinter as ctk
from datetime import datetime


class LogWidget(ctk.CTkTextbox):
    """
    Area de texto con colores para logs en tiempo real.

    Tags disponibles:
      - "ts"    : marca de tiempo (gris)
      - "ok"    : éxito (verde)
      - "error" : error (rojo)
      - "flecha": progreso (azul)
      - "dim"   : mensaje genérico (gris claro)
    """

    def __init__(self, parent, height: int = 160, font_size: int = 10, **kwargs):
        kwargs.setdefault("wrap", "word")
        kwargs.setdefault("height", height)
        kwargs.setdefault("font", ctk.CTkFont(family="Consolas", size=font_size))

        super().__init__(parent, **kwargs)

        tb = self._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("flecha", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

    def log(self, msg: str):
        """Añade una línea al log con marca de tiempo y color según prefijo."""
        ts = datetime.now().strftime("%H:%M:%S")
        tag = (
            "ok"
            if msg.startswith("✓")
            else "error"
            if msg.startswith("✗")
            else "flecha"
            if "→" in msg
            else "dim"
        )
        self.configure(state="normal")
        tb = self._textbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.see("end")
        self.configure(state="disabled")

    def clear(self):
        """Limpia todo el contenido del log."""
        self.configure(state="normal")
        self.delete("0.0", "end")
        self.configure(state="disabled")

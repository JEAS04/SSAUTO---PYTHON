"""
ui/widgets/log_widget.py — Widget de registro con marcas de tiempo, colores y archivo.
"""

import os
import sys
import customtkinter as ctk
from datetime import datetime
from pathlib import Path


def _log_dir() -> Path:
    if getattr(sys, "frozen", False):
        from utils.paths import get_writable_path
        return Path(get_writable_path("logs"))
    return Path("logs")


class LogWidget(ctk.CTkTextbox):
    """Area de texto solo-lectura con colores para logs en tiempo real.

    Cada linea se inserta con una marca de tiempo y un color segun el
    prefijo del mensaje:
      - "ok"    (verde) : lineas que empiezan con ✓
      - "error" (rojo)  : lineas que empiezan con ✗
      - "flecha"(azul)  : lineas que contienen →
      - "dim"   (gris)  : resto de mensajes
      - "ts"    (gris oscuro) : marca de tiempo [HH:MM:SS]

    Ademas, escribe cada linea a un archivo en logs/ con fecha y hora
    en el nombre (ej. logs/log_20260611_143025.txt).

    Args:
        parent: widget padre.
        height: altura en lineas de texto (default 160).
        font_size: tamano de fuente (default 10).
        **kwargs: argumentos adicionales pasados a CTkTextbox.
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

        self._log_path: Path | None = None

    def _ensure_log_file(self):
        if self._log_path is not None:
            return
        destino = _log_dir()
        destino.mkdir(parents=True, exist_ok=True)
        nombre = datetime.now().strftime("log_%Y%m%d_%H%M%S.txt")
        self._log_path = destino / nombre

    def log(self, msg: str):
        """Añade una línea al log con marca de tiempo y color según prefijo.
        Tambien la escribe a disco en logs/log_YYYYMMDD_HHMMSS.txt."""
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
        linea = f"[{ts}] {msg}"
        self.configure(state="normal")
        tb = self._textbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.see("end")
        self.configure(state="disabled")

        self._ensure_log_file()
        try:
            with open(self._log_path, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
        except OSError:
            pass

    def clear(self):
        """Limpia todo el contenido del log."""
        self.configure(state="normal")
        self.delete("0.0", "end")
        self.configure(state="disabled")

"""
main.py — Punto de entrada de SSAuto.

Este es el único archivo que se ejecuta directamente:
    python main.py

Solo aplica el tema visual e instancia la ventana principal.
Toda la lógica está en los módulos del proyecto.
"""

import customtkinter as ctk
from configuracion import TEMA_APARIENCIA, TEMA_COLOR
from ventana_principal import App

# Aplicar tema antes de crear cualquier widget.
ctk.set_appearance_mode(TEMA_APARIENCIA)
ctk.set_default_color_theme(TEMA_COLOR)

if __name__ == "__main__":
    app = App()
    app.mainloop()

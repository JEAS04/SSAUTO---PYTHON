"""
main.py — Punto de entrada de SSAuto.

Este es el único archivo que se ejecuta directamente:
    python main.py

Solo aplica el tema visual e instancia la ventana principal.
Toda la lógica está en los módulos del proyecto.
"""

import customtkinter as ctk
from config.configuracion import (
    TEMA_APARIENCIA,
    TEMA_COLOR,
    guardar_config,
    cargar_config,
)
from ui.ventana_principal import App
import subprocess
import sys
import os

# Aplicar tema antes de crear cualquier widget.
from config.configuracion import cargar_config

config = cargar_config()

ctk.set_appearance_mode(config.get("tema", TEMA_APARIENCIA))
ctk.set_default_color_theme(TEMA_COLOR)


def cambiar_tema(opcion):
    tema = "dark" if opcion == "Oscuro" else "light"

    ctk.set_appearance_mode(tema)
    config = cargar_config()
    config["tema"] = tema
    guardar_config(config)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def abrir_principal():
    resultado = subprocess.run(
        [sys.executable, "-m", "ui.ventana_principal"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )

    print(resultado.stdout)
    print(resultado.stderr)


def abrir_comparacion():
    subprocess.Popen(
        [sys.executable, "-m", "ui.ventana_comparacion"],
        cwd=BASE_DIR,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )


App = ctk.CTk()
App.title("Sistema")
App.geometry("400x250")

titulo = ctk.CTkLabel(App, text="Selecciona una interfaz", font=("Arial", 22))
titulo.pack(pady=30)

btn_principal = ctk.CTkButton(
    App, text="Abrir Ventana Principal", command=abrir_principal, width=220, height=40
)
btn_principal.pack(pady=10)

btn_comparacion = ctk.CTkButton(
    App,
    text="Abrir Ventana Comparación",
    command=abrir_comparacion,
    width=220,
    height=40,
)
btn_comparacion.pack(pady=10)

launcher = ctk.CTk()
modo_oscuro = ctk.StringVar(value=TEMA_APARIENCIA)

launcher.title("Fassy")
selector_tema = ctk.CTkOptionMenu(
    launcher, values=["Oscuro", "Claro"], command=cambiar_tema
)
tema_actual = "Oscuro" if TEMA_APARIENCIA == "dark" else "Claro"

selector_tema.set(tema_actual)
selector_tema.pack(pady=10)
tema_guardado = config.get("tema", "dark")

selector_tema.set("Oscuro" if tema_guardado == "dark" else "Claro")
launcher.geometry("400x250")

titulo = ctk.CTkLabel(launcher, text="Selecciona una interfaz", font=("Arial", 22))
titulo.pack(pady=30)

btn_principal = ctk.CTkButton(
    launcher,
    text="Abrir Ventana Principal",
    command=abrir_principal,
    width=220,
    height=40,
)
btn_principal.pack(pady=10)

btn_comparacion = ctk.CTkButton(
    launcher,
    text="Abrir Ventana Comparación",
    command=abrir_comparacion,
    width=220,
    height=40,
)
btn_comparacion.pack(pady=10)

if __name__ == "__main__":
    try:
        launcher.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        os._exit(0)

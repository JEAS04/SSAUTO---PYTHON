"""
main.py — Punto de entrada de SSAuto (refactorizado).

Responsabilidades de este archivo:
  1. Registrar los plugins de sitios en PluginRegistry.
  2. Aplicar tema visual.
  3. Construir la ventana raíz y montar las vistas.

Para agregar un sitio nuevo:
  1. Crear plugins/mi_sitio.py heredando de SitioPlugin.
  2. Agregar las dos líneas de import + registrar() aquí abajo.
  3. Nada más.
"""

import customtkinter as ctk

from config.configuracion import (
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_config,
    guardar_config,
    SITIOS,
)

# ── Registro de plugins ───────────────────────────────────────────────
# Único lugar donde se declaran los sitios disponibles.
# Para agregar uno nuevo: import + registrar(), sin tocar nada más.

from core.plugin_registry import PluginRegistry
from plugins.hubspot import HubSpotPlugin
from plugins.sunrun import SunrunPlugin

PluginRegistry.registrar(HubSpotPlugin())
PluginRegistry.registrar(SunrunPlugin())
# PluginRegistry.registrar(NuevoSitioPlugin())  ← así de fácil

# ── Imports de UI ─────────────────────────────────────────────────────
from ui.ventana_principal import App
from ui.ventana_comparacion import VentanaComparacion
from ui.ventana_credenciales import VentanaCredenciales
from ui.ventana_plantillas import VentanaPlantillas

# ── Tema ──────────────────────────────────────────────────────────────
config = cargar_config()
ctk.set_appearance_mode(config.get("tema", TEMA_APARIENCIA))
ctk.set_default_color_theme(TEMA_COLOR)

# ── Ventana raíz ──────────────────────────────────────────────────────
launcher = ctk.CTk()
launcher.geometry("900x620")
launcher.title("SSAuto")


# ── Helpers ───────────────────────────────────────────────────────────

def mostrar_frame(frame):
    frame.tkraise()


def abrir_plantillas():
    VentanaPlantillas(launcher)


def abrir_credenciales():
    win = VentanaCredenciales(launcher, SITIOS)
    if win.confirmado:
        vista_principal._credenciales_sesion = win.credenciales_sesion


def cambiar_tema(opcion: str):
    tema = "dark" if opcion == "Oscuro" else "light"
    ctk.set_appearance_mode(tema)
    cfg = cargar_config()
    cfg["tema"] = tema
    guardar_config(cfg)


# ── Barra superior ────────────────────────────────────────────────────

barra = ctk.CTkFrame(launcher, height=30, corner_radius=0)
barra.pack(fill="x", side="top")
barra.pack_propagate(False)


def _btn_barra(texto: str, comando, lado="left", acento=False) -> ctk.CTkButton:
    btn = ctk.CTkButton(
        barra,
        text=texto,
        command=comando,
        font=ctk.CTkFont(size=12),
        fg_color=("#1f6aa5", "#1f6aa5") if acento else "transparent",
        text_color=("gray10", "gray90"),
        hover_color=("#144e7a", "#144e7a") if acento else ("gray80", "gray30"),
        height=26,
        width=120,
        corner_radius=4,
    )
    btn.pack(side=lado, padx=2, pady=2)
    return btn


def _sep_barra():
    ctk.CTkFrame(barra, width=1, fg_color=("gray70", "gray40")).pack(
        side="left", fill="y", padx=4, pady=4
    )


# ── Layout principal ──────────────────────────────────────────────────

contenedor = ctk.CTkFrame(launcher)
contenedor.pack(fill="both", expand=True)
contenedor.grid_rowconfigure(0, weight=1)
contenedor.grid_columnconfigure(0, weight=1)

frame_principal = ctk.CTkFrame(contenedor)
frame_comparacion = ctk.CTkFrame(contenedor)

for frame in (frame_principal, frame_comparacion):
    frame.grid(row=0, column=0, sticky="nsew")

vista_principal = App(frame_principal)
vista_principal.pack(fill="both", expand=True)

vista_comparacion = VentanaComparacion(frame_comparacion)
vista_comparacion.pack(fill="both", expand=True)

mostrar_frame(frame_principal)

# ── Botones de navegación ─────────────────────────────────────────────

_btn_barra("Principal", lambda: mostrar_frame(frame_principal))
_btn_barra("Comparación", lambda: mostrar_frame(frame_comparacion))
_sep_barra()
_btn_barra("Credenciales", abrir_credenciales)
_btn_barra("Plantillas", abrir_plantillas)


# ── Minimizar: ocultar barra para que no flote ───────────────────────

def _al_minimizar(event):
    if launcher.state() == "iconic":
        barra.pack_forget()
    else:
        barra.pack(fill="x", side="top", before=contenedor)


launcher.bind("<Unmap>", _al_minimizar)
launcher.bind("<Map>", _al_minimizar)

# ── Arranque ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        launcher.mainloop()
    except KeyboardInterrupt:
        pass
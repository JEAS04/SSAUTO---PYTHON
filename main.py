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
from version import __version__
from config.configuracion import (
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_config,
    guardar_config,
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
from ui.ventana_generador_mensajes import VentanaGeneradorMensajes

# ── Tema ──────────────────────────────────────────────────────────────
config = cargar_config()
ctk.set_appearance_mode(config.get("tema", TEMA_APARIENCIA))
ctk.set_default_color_theme(TEMA_COLOR)

# ── Ventana raíz ──────────────────────────────────────────────────────
launcher = ctk.CTk()
launcher.title("SSAuto")


def _clamp(valor: int, minimo: int, maximo: int) -> int:
    """Restringe un valor entero entre minimo y maximo, ambos inclusive."""
    return max(minimo, min(valor, maximo))


def _configurar_ventana_responsive():
    """Ajusta escala, tamano y posicion de la ventana segun la resolucion.

    Calcula una escala proporcional entre 1.0 y 1.65 basada en la relacion
    de aspecto de la pantalla respecto a Full HD (1920x1080). La ventana
    ocupa ~68 % del ancho y ~78 % del alto de la pantalla, centrada.

    Efectos secundarios:
        - Modifica las escalas globales de widgets y ventana de CustomTkinter.
        - Establece la geometria y el tamano minimo de la ventana raiz.
    """
    sw, sh = launcher.winfo_screenwidth(), launcher.winfo_screenheight()
    escala = _clamp(int(min(sw / 1920, sh / 1080) * 100), 100, 165) / 100
    ctk.set_widget_scaling(escala)
    ctk.set_window_scaling(escala)

    ancho = _clamp(int(sw * 0.68), 900, 2560)
    alto = _clamp(int(sh * 0.78), 620, 1700)
    x = max(0, (sw - ancho) // 2)
    y = max(0, (sh - alto) // 2)
    launcher.geometry(f"{ancho}x{alto}+{x}+{y}")
    launcher.minsize(860, 560)


_configurar_ventana_responsive()


# ── Helpers ───────────────────────────────────────────────────────────


def mostrar_frame(frame):
    """Eleva el frame indicado al frente del contenedor apilado.

    Usa tkraise() para traer un frame al frente en un layout de tipo
    stacked (todos los frames ocupan la misma celda del grid).

    Args:
        frame: instancia de ctk.CTkFrame a mostrar.
    """
    frame.tkraise()


def abrir_plantillas():
    """Abre la ventana modal de plantillas de mensajes rapidos.

    Efectos secundarios:
        - Crea una instancia de VentanaPlantillas como toplevel modal.
    """
    VentanaPlantillas(launcher)


def abrir_generador():
    """Abre la ventana modal del generador de mensajes de contacto.

    Efectos secundarios:
        - Crea una instancia de VentanaGeneradorMensajes como toplevel modal.
    """
    VentanaGeneradorMensajes(launcher)


def abrir_credenciales():
    """Abre la ventana modal de credenciales para los sitios que requieren login.

    Si el usuario confirma, actualiza las credenciales en memoria de la vista
    principal para usarlas en la sesion actual sin reiniciar la app.

    Efectos secundarios:
        - Si win.confirmado es True, modifica
          vista_principal._credenciales_sesion.
    """
    sitios_compat = [
        {"nombre": p.nombre, "necesita_login": p.necesita_login}
        for p in PluginRegistry.con_login()
    ]
    win = VentanaCredenciales(launcher, sitios_compat)
    if win.confirmado:
        vista_principal._credenciales_sesion = win.credenciales_sesion
        vista_principal._actualizar_sitios_status()


def cambiar_tema(opcion: str):
    """Cambia el tema visual entre claro y oscuro.

    Actualiza la apariencia de CustomTkinter y persiste la eleccion en
    config.json para que sobreviva a reinicios de la aplicacion.

    Args:
        opcion: "Oscuro" o "Claro" (valor del CTkOptionMenu de la barra).

    Efectos secundarios:
        - Cambia la apariencia global de todos los widgets CustomTkinter.
        - Escribe el tema en config.json.
    """
    tema = "dark" if opcion == "Oscuro" else "light"
    ctk.set_appearance_mode(tema)
    cfg = cargar_config()
    cfg["tema"] = tema
    guardar_config(cfg)


tema_actual = config.get("tema", TEMA_APARIENCIA)
tema_var = ctk.StringVar(value="Oscuro" if tema_actual == "dark" else "Claro")


# ── Barra superior ────────────────────────────────────────────────────

barra = ctk.CTkFrame(launcher, height=30, corner_radius=0)
barra.pack(fill="x", side="top")
barra.pack_propagate(False)


def _btn_barra(texto: str, comando, lado="left", acento=False) -> ctk.CTkButton:
    """Crea un boton estilizado para la barra de navegacion superior.

    Args:
        texto: etiqueta del boton.
        comando: callback a invocar al hacer clic.
        lado: lado de empaquetado en la barra ("left" o "right").
        acento: si True, usa color de acento azul; si False, es transparente.

    Returns:
        Instancia de ctk.CTkButton ya empaquetada en la barra.
    """
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
    """Inserta un separador visual vertical de 1 px en la barra de navegacion."""
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
_btn_barra("Mensajes", abrir_generador)
_sep_barra()
_btn_barra("Vista", vista_principal.ui_manager.show_customization_menu)

ctk.CTkOptionMenu(
    barra,
    variable=tema_var,
    values=["Oscuro", "Claro"],
    command=cambiar_tema,
    font=ctk.CTkFont(size=12),
    width=92,
    height=26,
    dynamic_resizing=False,
).pack(side="right", padx=6, pady=2)

ctk.CTkLabel(
    barra,
    text="Tema:",
    font=ctk.CTkFont(size=12),
    text_color=("gray10", "gray90"),
).pack(side="right", padx=(0, 2), pady=2)


# ── Minimizar: ocultar barra para que no flote ───────────────────────


def _al_minimizar(event):
    """Oculta o restaura la barra superior cuando la ventana se minimiza/restaura.

    Evita que la barra de navegacion flote como ventana independiente cuando
    la ventana principal esta minimizada.

    Args:
        event: evento de mapeo/desmapeo de Tkinter (<Unmap> o <Map>).
    """
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

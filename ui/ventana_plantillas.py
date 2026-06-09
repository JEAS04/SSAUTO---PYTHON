"""
ventana_plantillas.py — Ventana de plantillas de mensajes rápidos.

Permite copiar al portapapeles mensajes predefinidos con un solo clic.
Las plantillas se guardan en config/plantillas.json y son editables
directamente desde la interfaz.
"""

import json
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from ui.posicion_ventanas import ubicar_junto_a_padre
from utils.paths import get_writable_path

PLANTILLAS_PATH = Path(get_writable_path("config/plantillas.json"))

PLANTILLAS_DEFAULT = [
    {
        "titulo": "Saludo inicial",
        "categoria": "HubSpot",
        "texto": "Hola [Nombre], espero que estés muy bien. Me comunico para hacerte seguimiento sobre tu solicitud. ¿Tienes alguna duda o necesitas información adicional?",
    },
    {
        "titulo": "Nota de seguimiento",
        "categoria": "HubSpot",
        "texto": "Se realizó llamada al cliente [Nombre] el [Fecha]. Se discutió [Tema]. Próximo paso: [Acción]. Fecha estimada: [Fecha siguiente].",
    },
    {
        "titulo": "Confirmación de cita",
        "categoria": "HubSpot",
        "texto": "Hola [Nombre], confirmamos tu cita para el día [Fecha] a las [Hora]. Por favor avísanos con anticipación si necesitas reagendar.",
    },
    {
        "titulo": "Actualización de estado",
        "categoria": "Sunrun",
        "texto": "Actualización de estado para el caso [ID]: El sistema se encuentra en etapa [Estado]. Tiempo estimado de resolución: [Tiempo].",
    },
    {
        "titulo": "Cierre de caso",
        "categoria": "Sunrun",
        "texto": "El caso [ID] ha sido cerrado exitosamente el [Fecha]. Motivo de cierre: [Motivo]. Si tiene alguna consulta adicional no dude en contactarnos.",
    },
    {
        "titulo": "Sin respuesta",
        "categoria": "General",
        "texto": "Hola [Nombre], intentamos comunicarnos contigo sin éxito. Por favor contáctanos al [Teléfono] o responde este mensaje para continuar con tu proceso.",
    },
]


def _cargar_plantillas() -> list:
    """Carga las plantillas desde config/plantillas.json.

    Returns:
        list de dicts con formato [{titulo, categoria, texto}, ...].
        Si el archivo no existe o hay error de parseo, retorna las
        PLANTILLAS_DEFAULT.
    """
    if PLANTILLAS_PATH.exists():
        try:
            return json.loads(PLANTILLAS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return PLANTILLAS_DEFAULT.copy()


def _guardar_plantillas(plantillas: list):
    """Persiste la lista de plantillas en config/plantillas.json.

    Crea el directorio si no existe y escribe con indent=2 y UTF-8.

    Args:
        plantillas: list de dicts [{titulo, categoria, texto}, ...] a guardar.
    """
    PLANTILLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLANTILLAS_PATH.write_text(
        json.dumps(plantillas, ensure_ascii=False, indent=2), encoding="utf-8"
    )


class VentanaPlantillas(ctk.CTkToplevel):
    """
    Ventana de plantillas de mensajes rápidos.

    Panel izquierdo : lista de plantillas agrupadas por categoría.
    Panel derecho   : editor de la plantilla seleccionada + botón Copiar.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Plantillas de mensajes")
        self.geometry("780x520")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._plantillas = _cargar_plantillas()
        self._indice_actual: int | None = None

        self._construir_ui()
        ubicar_junto_a_padre(self, parent)
        self._poblar_lista()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Panel izquierdo: lista ─────────────────────────────────────
        panel_izq = ctk.CTkFrame(
            self, width=240, corner_radius=0, fg_color=("gray92", "gray17")
        )
        panel_izq.grid(row=0, column=0, sticky="nsew")
        panel_izq.grid_propagate(False)
        panel_izq.grid_rowconfigure(1, weight=1)
        panel_izq.grid_columnconfigure(0, weight=1)

        # Cabecera izquierda
        ctk.CTkLabel(
            panel_izq,
            text="PLANTILLAS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))

        # Lista scrollable
        self._frame_lista = ctk.CTkScrollableFrame(
            panel_izq,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._frame_lista.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        self._frame_lista.grid_columnconfigure(0, weight=1)

        # Botón nueva plantilla
        ctk.CTkButton(
            panel_izq,
            text="+ Nueva plantilla",
            command=self._nueva_plantilla,
            font=ctk.CTkFont(size=11),
            height=32,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).grid(row=2, column=0, sticky="ew", padx=8, pady=8)

        # ── Panel derecho: editor ──────────────────────────────────────
        panel_der = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        panel_der.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        panel_der.grid_rowconfigure(2, weight=1)
        panel_der.grid_columnconfigure(0, weight=1)

        # Título de la plantilla
        ctk.CTkLabel(
            panel_der,
            text="Título",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 2))

        fila_titulo = ctk.CTkFrame(panel_der, fg_color="transparent")
        fila_titulo.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        fila_titulo.grid_columnconfigure(0, weight=1)

        self._titulo_var = ctk.StringVar()
        ctk.CTkEntry(
            fila_titulo,
            textvariable=self._titulo_var,
            font=ctk.CTkFont(size=13, weight="bold"),
            placeholder_text="Nombre de la plantilla",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        # Selector de categoría
        self._cat_var = ctk.StringVar(value="General")
        ctk.CTkOptionMenu(
            fila_titulo,
            variable=self._cat_var,
            values=["General", "HubSpot", "Sunrun"],
            font=ctk.CTkFont(size=11),
            width=110,
        ).grid(row=0, column=1)

        # Cuerpo del texto
        ctk.CTkLabel(
            panel_der,
            text="Mensaje",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
        ).grid(row=2, column=0, sticky="nw", padx=16, pady=(0, 2))

        self._texto_box = ctk.CTkTextbox(
            panel_der,
            font=ctk.CTkFont(size=12),
            wrap="word",
        )
        self._texto_box.grid(row=2, column=0, sticky="nsew", padx=16, pady=(18, 8))

        # Barra de botones inferior
        barra_inf = ctk.CTkFrame(panel_der, fg_color="transparent")
        barra_inf.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 14))

        ctk.CTkButton(
            barra_inf,
            text="📋  Copiar al portapapeles",
            command=self._copiar,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        ).pack(side="left")

        ctk.CTkButton(
            barra_inf,
            text="Guardar cambios",
            command=self._guardar_actual,
            font=ctk.CTkFont(size=11),
            height=36,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(8, 0))

        ctk.CTkButton(
            barra_inf,
            text="Eliminar",
            command=self._eliminar_actual,
            font=ctk.CTkFont(size=11),
            height=36,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="right")

        # Label de confirmación de copia
        self._label_copia = ctk.CTkLabel(
            panel_der,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("#238636", "#3fb950"),
        )
        self._label_copia.grid(row=4, column=0, pady=(0, 4))

    # ── Lista ─────────────────────────────────────────────────────────────────

    def _poblar_lista(self):
        """Reconstruye los botones de la lista izquierda."""
        for w in self._frame_lista.winfo_children():
            w.destroy()

        categorias: dict[str, list] = {}
        for i, p in enumerate(self._plantillas):
            cat = p.get("categoria", "General")
            categorias.setdefault(cat, []).append((i, p))

        COLOR_CAT = {
            "HubSpot": ("#1f6aa5", "#4a9eff"),
            "Sunrun": ("#8b4500", "#f0a050"),
            "General": ("gray50", "gray50"),
        }

        fila = 0
        for cat, items in categorias.items():
            color = COLOR_CAT.get(cat, ("gray50", "gray50"))
            ctk.CTkLabel(
                self._frame_lista,
                text=cat.upper(),
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=color,
                anchor="w",
            ).grid(row=fila, column=0, sticky="w", padx=8, pady=(10, 2))
            fila += 1

            for idx, p in items:
                btn = ctk.CTkButton(
                    self._frame_lista,
                    text=p["titulo"],
                    anchor="w",
                    font=ctk.CTkFont(size=12),
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray80", "gray30"),
                    height=30,
                    command=lambda i=idx: self._seleccionar(i),
                )
                btn.grid(row=fila, column=0, sticky="ew", padx=4, pady=1)
                fila += 1

        # Seleccionar la primera si existe
        if self._plantillas and self._indice_actual is None:
            self._seleccionar(0)

    def _seleccionar(self, indice: int):
        """Carga la plantilla indicada en el editor."""
        self._indice_actual = indice
        p = self._plantillas[indice]
        self._titulo_var.set(p["titulo"])
        self._cat_var.set(p.get("categoria", "General"))
        self._texto_box.delete("0.0", "end")
        self._texto_box.insert("0.0", p["texto"])
        self._label_copia.configure(text="")

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _copiar(self):
        texto = self._texto_box.get("0.0", "end").strip()
        if not texto:
            return
        self.clipboard_clear()
        self.clipboard_append(texto)
        self._label_copia.configure(text="✓ Copiado al portapapeles")
        self.after(2500, lambda: self._label_copia.configure(text=""))

    def _guardar_actual(self):
        titulo = self._titulo_var.get().strip()
        texto = self._texto_box.get("0.0", "end").strip()
        if not titulo:
            messagebox.showerror(
                "Campo vacío", "Escribe un título para la plantilla.", parent=self
            )
            return
        entrada = {"titulo": titulo, "categoria": self._cat_var.get(), "texto": texto}
        if self._indice_actual is not None:
            self._plantillas[self._indice_actual] = entrada
        else:
            self._plantillas.append(entrada)
            self._indice_actual = len(self._plantillas) - 1
        _guardar_plantillas(self._plantillas)
        self._poblar_lista()
        self._label_copia.configure(text="✓ Plantilla guardada")
        self.after(2500, lambda: self._label_copia.configure(text=""))

    def _nueva_plantilla(self):
        self._indice_actual = None
        self._titulo_var.set("")
        self._cat_var.set("General")
        self._texto_box.delete("0.0", "end")
        self._label_copia.configure(text="")

    def _eliminar_actual(self):
        if self._indice_actual is None:
            return
        titulo = self._plantillas[self._indice_actual]["titulo"]
        if not messagebox.askyesno(
            "Eliminar", f"¿Eliminar la plantilla «{titulo}»?", parent=self
        ):
            return
        self._plantillas.pop(self._indice_actual)
        self._indice_actual = None
        _guardar_plantillas(self._plantillas)
        # Limpiar editor
        self._titulo_var.set("")
        self._texto_box.delete("0.0", "end")
        self._poblar_lista()

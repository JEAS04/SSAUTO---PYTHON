"""
ui/widgets/profile_manager.py — Gestor de perfiles de region de captura.

Dropdown de perfiles + carga, entrada de nombre + guardar/eliminar,
entrada de region pegada + aplicar.
"""

import customtkinter as ctk
from tkinter import StringVar, messagebox


class ProfileManagerWidget(ctk.CTkFrame):
    """Widget autonomo para gestion de perfiles de region de captura."""

    def __init__(
        self,
        parent,
        region_vars: dict[str, StringVar],
        perfiles_iniciales: dict,
        on_cargar_perfil=None,
        on_guardar_perfil=None,
        on_eliminar_perfil=None,
        on_aplicar_region=None,
        on_log=None,
    ):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self._perfiles = perfiles_iniciales
        self.region_vars = region_vars
        self._on_cargar = on_cargar_perfil
        self._on_guardar = on_guardar_perfil
        self._on_eliminar = on_eliminar_perfil
        self._on_aplicar_region = on_aplicar_region
        self._on_log = on_log or (lambda _: None)

        # Row 0: Perfil dropdown + Cargar
        pf1 = ctk.CTkFrame(self, fg_color="transparent")
        pf1.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf1, text="Perfil:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))

        nombres = self._nombres_perfiles()
        self._perfil_var = StringVar(value=nombres[0])
        self._perfil_menu = ctk.CTkOptionMenu(
            pf1, variable=self._perfil_var,
            values=nombres,
            font=ctk.CTkFont(size=11),
            dynamic_resizing=False, width=150,
        )
        self._perfil_menu.pack(side="left", padx=(0, 6))
        ctk.CTkButton(
            pf1, text="Cargar", command=self._cargar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
        ).pack(side="left")

        # Row 1: Nombre + Guardar + Eliminar
        pf2 = ctk.CTkFrame(self, fg_color="transparent")
        pf2.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf2, text="Nombre:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self._perfil_nombre_var = StringVar()
        ctk.CTkEntry(
            pf2, textvariable=self._perfil_nombre_var,
            placeholder_text="Ej: Monitor 1 - Panel izq.",
            font=ctk.CTkFont(size=11),
        ).pack(side="left", padx=(0, 6), fill="x", expand=True)
        ctk.CTkButton(
            pf2, text="Guardar", command=self._guardar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        ).pack(side="left", padx=(0, 4))
        ctk.CTkButton(
            pf2, text="Eliminar", command=self._eliminar_perfil,
            font=ctk.CTkFont(size=10), width=66, height=28,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
        ).pack(side="left")

        # Row 2: Pegar region + Aplicar
        pf3 = ctk.CTkFrame(self, fg_color="transparent")
        pf3.pack(fill="x", pady=2)
        ctk.CTkLabel(
            pf3, text="Pegar region:", font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 6))
        self.region_paste_var = StringVar(value=self._region_a_texto())
        entrada = ctk.CTkEntry(
            pf3, textvariable=self.region_paste_var, font=ctk.CTkFont(size=11),
        )
        entrada.pack(side="left", padx=(0, 6), fill="x", expand=True)
        entrada.bind("<FocusOut>", self._aplicar_region_pegada)
        entrada.bind("<Return>", self._aplicar_region_pegada)
        self.region_paste_entry = entrada
        ctk.CTkButton(
            pf3, text="Aplicar", command=self._aplicar_region_pegada,
            font=ctk.CTkFont(size=10), width=66, height=28,
        ).pack(side="left")

    def _region_a_texto(self) -> str:
        return str({k: v.get() for k, v in self.region_vars.items()})

    def _nombres_perfiles(self) -> list[str]:
        nombres = list(self._perfiles.keys())
        return nombres if nombres else ["- sin perfiles -"]

    def actualizar_menu(self):
        nombres = self._nombres_perfiles()
        self._perfil_menu.configure(values=nombres)
        self._perfil_var.set(nombres[0])

    def actualizar_perfiles(self, perfiles: dict):
        self._perfiles = perfiles
        self.actualizar_menu()

    def _cargar_perfil(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._on_log("x No hay ningun perfil seleccionado.")
            return
        region = self._perfiles[nombre]
        self._perfil_nombre_var.set(nombre)
        if self._on_cargar:
            self._on_cargar(nombre, region)

    def _guardar_perfil(self):
        nombre = self._perfil_nombre_var.get().strip()
        if not nombre:
            messagebox.showerror("Nombre vacio", "Escribe un nombre para el perfil.")
            return
        region = {k: int(v.get() or 0) for k, v in self.region_vars.items()}
        if self._on_guardar:
            self._on_guardar(nombre, region)

    def _eliminar_perfil(self):
        nombre = self._perfil_var.get()
        if nombre not in self._perfiles:
            self._on_log("x No hay ningun perfil seleccionado para eliminar.")
            return
        if not messagebox.askyesno(
            "Eliminar perfil", f"Eliminar el perfil '{nombre}'?"
        ):
            return
        if self._on_eliminar:
            self._on_eliminar(nombre)

    def _aplicar_region_pegada(self, event=None):
        if self._on_aplicar_region:
            self._on_aplicar_region(self.region_paste_var.get().strip())

    def sincronizar_paste(self):
        self.region_paste_var.set(self._region_a_texto())

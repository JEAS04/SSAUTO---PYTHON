"""
ventana_credenciales.py — Ventana modal para configurar usuario y contraseña.

Se abre cuando el usuario hace clic en 'Credenciales' o cuando la app
detecta al arrancar que faltan credenciales para algún sitio con login.

Al confirmar, las credenciales quedan en:
  · El llavero del SO  (si el usuario marcó 'Recordar').
  · self.credenciales_sesion (dict en memoria para la sesión actual).
"""

import customtkinter as ctk
from tkinter import messagebox
from config.configuracion import cargar_config
from config.credenciales import (
    cargar_credenciales,
    guardar_credenciales,
    borrar_credenciales,
)


class VentanaCredenciales(ctk.CTkToplevel):
    """
    Ventana modal que muestra un formulario por cada sitio que requiera login.

    Uso típico desde la ventana principal:
        win = VentanaCredenciales(self, SITIOS)
        if win.confirmado:
            self._credenciales_sesion = win.credenciales_sesion

    Atributos públicos
    ------------------
    confirmado           : True si el usuario hizo clic en 'Continuar'.
    credenciales_sesion  : dict {nombre_sitio: {usuario, clave}} en memoria.
    """

    def __init__(self, parent, sitios: list):
        super().__init__(parent)
        self.sitios = sitios
        self.title("Credenciales")
        self.resizable(False, False)
        # grab_set() hace que esta ventana sea modal:
        # bloquea la interacción con la ventana principal mientras está abierta.
        self.grab_set()
        self.confirmado = False
        self._construir_ui()
        # transient() la mantiene siempre encima de la ventana principal.
        self.transient(parent)
        # wait_window() pausa la ejecución hasta que esta ventana se cierre.
        self.wait_window()
        self._config = cargar_config()
        config = cargar_config()
        ctk.set_appearance_mode(config.get("tema", "dark"))

    def _construir_ui(self):
        """Construye el formulario con un bloque por cada sitio con login."""
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Configurar credenciales",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, pady=(16, 12), padx=20, sticky="w")

        self.campos = {}  # {nombre_sitio: {usuario, clave, recordar}}
        indice_fila = 1

        for sitio in self.sitios:
            if not sitio.get("necesita_login"):
                continue  # Los sitios sin login no necesitan credenciales.

            nombre = sitio["nombre"]
            usuario_guardado, clave_guardada = cargar_credenciales(nombre)
            tiene_guardado = bool(usuario_guardado and clave_guardada)

            # Marco individual para cada sitio.
            frame = ctk.CTkFrame(self, fg_color=("gray95", "gray20"), border_width=1)
            frame.grid(row=indice_fila, column=0, sticky="ew", padx=20, pady=(0, 10))
            frame.grid_columnconfigure(1, weight=1)
            indice_fila += 1

            ctk.CTkLabel(
                frame,
                text=nombre,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("royalblue", "#4a9eff"),
            ).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(10, 6))

            var_usuario = ctk.StringVar(value=usuario_guardado)
            var_clave = ctk.StringVar(value=clave_guardada)

            # Campo usuario
            ctk.CTkLabel(
                frame,
                text="Usuario",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=1, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_usuario,
                width=220,
                font=ctk.CTkFont(size=11),
            ).grid(row=1, column=1, sticky="ew", padx=(0, 14), pady=4)

            # Campo contraseña (caracteres ocultos con show="*")
            ctk.CTkLabel(
                frame,
                text="Contraseña",
                font=ctk.CTkFont(size=11),
                text_color=("gray40", "gray60"),
            ).grid(row=2, column=0, sticky="e", padx=(14, 6), pady=4)
            ctk.CTkEntry(
                frame,
                textvariable=var_clave,
                width=220,
                show="*",
                font=ctk.CTkFont(size=11),
            ).grid(row=2, column=1, sticky="ew", padx=(0, 14), pady=4)

            # Switch para recordar credenciales en el llavero del SO.
            var_recordar = ctk.BooleanVar(value=tiene_guardado)
            ctk.CTkSwitch(
                frame,
                text="  Recordar credenciales",
                variable=var_recordar,
                font=ctk.CTkFont(size=11),
            ).grid(row=3, column=0, columnspan=2, sticky="w", padx=14, pady=(6, 12))

            self.campos[nombre] = {
                "usuario": var_usuario,
                "clave": var_clave,
                "recordar": var_recordar,
            }

        # Botones de acción al pie de la ventana.
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.grid(
            row=indice_fila + 1, column=0, sticky="e", padx=20, pady=(4, 16)
        )
        frame_botones.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self._cancelar,
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            width=100,
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            frame_botones,
            text="Continuar",
            command=self._confirmar,
            font=ctk.CTkFont(size=11, weight="bold"),
            width=100,
        ).pack(side="right")

    def _confirmar(self):
        """
        Valida que todos los campos estén completos, guarda o borra las
        credenciales en el llavero según el switch 'Recordar', y cierra.
        """
        # Validar que no queden campos vacíos antes de guardar.
        for nombre, vars_ in self.campos.items():
            if not vars_["usuario"].get().strip() or not vars_["clave"].get().strip():
                messagebox.showerror(
                    "Campos vacíos",
                    f"Completa usuario y contraseña para:\n{nombre}",
                    parent=self,
                )
                return

        # Guardar o eliminar según el switch 'Recordar'.
        for nombre, vars_ in self.campos.items():
            if vars_["recordar"].get():
                guardar_credenciales(
                    nombre, vars_["usuario"].get(), vars_["clave"].get()
                )
            else:
                borrar_credenciales(nombre)

        # Guardar también en memoria para la sesión actual (sin tocar el disco).
        self.credenciales_sesion = {
            nombre: {
                "usuario": vars_["usuario"].get(),
                "clave": vars_["clave"].get(),
            }
            for nombre, vars_ in self.campos.items()
        }

        self.confirmado = True
        self.destroy()

    def _cancelar(self):
        """Cierra la ventana sin guardar nada."""
        self.confirmado = False
        self.destroy()

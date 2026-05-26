"""
ventana_generador_mensajes.py — Generador de mensajes de contacto.

Permite generar mensajes estandarizados para diferentes situaciones de contacto:
- Fuera de servicio
- Buzón de voz
- No contesta

Cada mensaje puede generarse en español o inglés, con manejo automático
de singular/plural según la cantidad de números telefónicos ingresados.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date as date_type
import re
from ui.posicion_ventanas import ubicar_junto_a_padre

# ── Plantillas de mensajes ────────────────────────────────────────────────────

PLANTILLAS_MENSAJES = {
    "fuera_servicio": {
        "titulo": "Fuera de Servicio",
        "es": "LS: {fecha}. Se llamó {al número|a los números} {telefonos}, pero {está|están} fuera de servicio. Se envió un correo electrónico como método de contacto alternativo.",
        "en": "LS: {fecha}. A call was placed to the registered phone {number|numbers}, but {it is|they are} out of service. An email was sent as an alternative method of contact.",
    },
    "buzon_voz": {
        "titulo": "Buzón de Voz",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero la llamada fue enviada al buzón de voz. Se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers}, but the call went to voicemail. A text message and an email were sent.",
    },
    "no_contesta": {
        "titulo": "No Contesta",
        "es": "LS: {fecha}. Se llamó {al cliente|a los clientes} {al número|a los números} {telefonos}, pero no respondió. Como alternativa de contacto, se envió un mensaje de texto y un correo electrónico.",
        "en": "LS: {fecha}. The customer was called at the registered {number|numbers}, but did not answer. A text message and an email were sent as alternative methods of contact.",
    },
    "confirma_visita_tecnica": {
        "titulo": "Cliente confirma visita técnica",
        "requiere_telefonos": False,
        "es": "Cliente confirma visita técnica en chat para el {fecha_habil_siguiente}.",
        "en": "Customer confirms technical visit in chat for {fecha_habil_siguiente}.",
    },
}


def _obtener_fecha() -> str:
    """Retorna la fecha actual en formato MM/DD/YYYY."""
    return datetime.now().strftime("%m/%d/%Y")


def _obtener_fecha_habil_siguiente() -> str:
    """
    Retorna el próximo día hábil (lunes a viernes) en formato MM/DD/YYYY.

    FIX #5: import lazy de pandas — si pandas no está disponible se usa
    una implementación pura con datetime para no romper toda la ventana.
    """
    try:
        import pandas as pd  # import lazy: solo cuando se necesita

        fecha_actual = pd.Timestamp(datetime.now().date())
        fecha_habil_siguiente = fecha_actual + pd.offsets.BusinessDay(1)
        return fecha_habil_siguiente.strftime("%m/%d/%Y")
    except ImportError:
        # Fallback sin pandas: avanza días hasta encontrar lunes-viernes
        dia = datetime.now().date()
        dia_siguiente = date_type.fromordinal(dia.toordinal() + 1)
        while dia_siguiente.weekday() >= 5:  # 5=sábado, 6=domingo
            dia_siguiente = date_type.fromordinal(dia_siguiente.toordinal() + 1)
        return dia_siguiente.strftime("%m/%d/%Y")


CODIGOS_AREA_PR = {"787", "939"}


def _normalizar_telefono_nanp(telefono: str) -> tuple[str, str | None]:
    """
    Valida y formatea un número telefónico NANP de Puerto Rico.

    Formatos aceptados de entrada:
    - 7 dígitos locales: 5551234, 555-1234
    - 10 dígitos con área PR: 7875551234, (787) 555-1234
    - 11 dígitos con país: 17875551234, +1 787 555 1234

    Retorna (telefono_formateado, error). Si hay error, el teléfono formateado
    será cadena vacía.
    """
    original = telefono.strip()
    digitos = re.sub(r"\D", "", original)

    if len(digitos) < 7:
        return "", f"'{original}' debe tener al menos 7 dígitos."

    if len(digitos) == 7:
        return f"{digitos[:3]}-{digitos[3:]}", None

    if len(digitos) == 10:
        codigo_area = digitos[:3]
        if codigo_area not in CODIGOS_AREA_PR:
            return (
                "",
                f"'{original}' debe usar un código de área de Puerto Rico: 787 o 939.",
            )
        return f"({codigo_area}) {digitos[3:6]}-{digitos[6:]}", None

    if len(digitos) == 11:
        codigo_pais = digitos[0]
        codigo_area = digitos[1:4]
        if codigo_pais != "1":
            return "", f"'{original}' debe usar el código de país NANP +1."
        if codigo_area not in CODIGOS_AREA_PR:
            return (
                "",
                f"'{original}' debe usar un código de área de Puerto Rico: 787 o 939.",
            )
        return f"+1 ({codigo_area}) {digitos[4:7]}-{digitos[7:]}", None

    return "", f"'{original}' debe tener 7, 10 u 11 dígitos."


def _procesar_texto(
    plantilla: str, cantidad_numeros: int, telefonos_str: str, idioma: str
) -> str:
    """
    Procesa una plantilla reemplazando:
    - {singular|plural} según la cantidad de números
    - {telefonos} con la lista de números
    - {fecha} con la fecha actual
    - {fecha_habil_siguiente} con el próximo día hábil
    """
    texto = plantilla

    texto = texto.replace("{fecha}", _obtener_fecha())
    texto = texto.replace("{fecha_habil_siguiente}", _obtener_fecha_habil_siguiente())
    texto = texto.replace("{telefonos}", telefonos_str)

    def reemplazar_plural(match: re.Match) -> str:
        singular = match.group(1)
        plural = match.group(2)
        return singular if cantidad_numeros == 1 else plural

    texto = re.sub(r"\{([^|}]+)\|([^}]+)\}", reemplazar_plural, texto)

    return texto


class VentanaGeneradorMensajes(ctk.CTkToplevel):
    """
    Ventana para generar mensajes de contacto estandarizados.

    Permite seleccionar tipo de mensaje, idioma, ingresar hasta 2 números
    telefónicos, previsualizar el mensaje y copiarlo al portapapeles.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Generador de Mensajes de Contacto")
        self.geometry("700x650")
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._tipo_mensaje_var = ctk.StringVar(value="fuera_servicio")
        self._idioma_var = ctk.StringVar(value="es")

        self._construir_ui()
        ubicar_junto_a_padre(self, parent)
        self._actualizar_preview()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        margen_x = 20
        margen_y = 10

        # ── Título ────────────────────────────────────────────────────────────
        lbl_titulo = ctk.CTkLabel(
            self,
            text="📝 Generador de Mensajes de Contacto",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        lbl_titulo.grid(row=0, column=0, sticky="w", padx=margen_x, pady=(margen_y, 0))

        lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Selecciona un tipo de mensaje, ingresa los números y genera el texto",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        lbl_subtitulo.grid(
            row=1, column=0, sticky="w", padx=margen_x, pady=(0, margen_y)
        )

        # ── Panel de configuración ────────────────────────────────────────────
        panel_config = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_config.grid(
            row=2, column=0, sticky="ew", padx=margen_x, pady=(0, margen_y)
        )
        panel_config.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_config,
            text="Tipo de mensaje:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        opciones_tipo = [
            (clave, plantilla["titulo"])
            for clave, plantilla in PLANTILLAS_MENSAJES.items()
        ]
        self._combo_tipo = ctk.CTkOptionMenu(
            panel_config,
            variable=self._tipo_mensaje_var,
            values=[clave for clave, _ in opciones_tipo],
            command=self._al_cambiar_tipo_mensaje,
            font=ctk.CTkFont(size=11),
        )
        self._combo_tipo.grid(row=0, column=1, sticky="w", padx=12, pady=(12, 4))

        ctk.CTkLabel(
            panel_config,
            text="Idioma:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=4)

        frame_idioma = ctk.CTkFrame(panel_config, fg_color="transparent")
        frame_idioma.grid(row=1, column=1, sticky="w", padx=12, pady=4)

        self._radio_es = ctk.CTkRadioButton(
            frame_idioma,
            text="Español",
            variable=self._idioma_var,
            value="es",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=11),
        )
        self._radio_es.pack(side="left", padx=(0, 16))

        self._radio_en = ctk.CTkRadioButton(
            frame_idioma,
            text="Ingles",
            variable=self._idioma_var,
            value="en",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=11),
        )
        self._radio_en.pack(side="left")

        # ── Números telefónicos ───────────────────────────────────────────────
        panel_telefonos = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_telefonos.grid(
            row=3, column=0, sticky="ew", padx=margen_x, pady=(0, margen_y)
        )
        panel_telefonos.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_telefonos,
            text="📞 Números telefónicos:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        lbl_info = ctk.CTkLabel(
            panel_telefonos,
            text="NANP PR: 555-1234, (787) 555-1234 o +1 (939) 555-1234",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        lbl_info.grid(row=0, column=1, sticky="w", padx=4, pady=(12, 4))

        ctk.CTkLabel(
            panel_telefonos,
            text="Número 1:",
            font=ctk.CTkFont(size=11),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=4)

        self._entry_tel1 = ctk.CTkEntry(
            panel_telefonos,
            placeholder_text="Ej: (787) 555-1234",
            font=ctk.CTkFont(size=12),
        )
        self._entry_tel1.grid(row=1, column=1, sticky="ew", padx=12, pady=4)
        self._entry_tel1.bind("<KeyRelease>", lambda e: self._actualizar_preview())

        ctk.CTkLabel(
            panel_telefonos,
            text="Número 2:",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, sticky="w", padx=12, pady=(4, 12))

        self._entry_tel2 = ctk.CTkEntry(
            panel_telefonos,
            placeholder_text="Opcional: +1 (939) 555-1234",
            font=ctk.CTkFont(size=12),
        )
        self._entry_tel2.grid(row=2, column=1, sticky="ew", padx=12, pady=(4, 12))
        self._entry_tel2.bind("<KeyRelease>", lambda e: self._actualizar_preview())

        # ── Previsualización ──────────────────────────────────────────────────
        panel_preview = ctk.CTkFrame(self, fg_color=("gray95", "gray20"))
        panel_preview.grid(
            row=4, column=0, sticky="nsew", padx=margen_x, pady=(0, margen_y)
        )
        panel_preview.grid_rowconfigure(1, weight=1)
        panel_preview.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_preview,
            text="📄 Previsualización:",
            font=ctk.CTkFont(size=11, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        self._textbox_preview = ctk.CTkTextbox(
            panel_preview,
            font=ctk.CTkFont(size=12),
            wrap="word",
            state="disabled",
        )
        self._textbox_preview.grid(
            row=1, column=0, sticky="nsew", padx=12, pady=(0, 12)
        )

        # ── Botones de acción ─────────────────────────────────────────────────
        panel_botones = ctk.CTkFrame(self, fg_color="transparent")
        panel_botones.grid(
            row=5, column=0, sticky="e", padx=margen_x, pady=(0, margen_y)
        )

        self._btn_copiar = ctk.CTkButton(
            panel_botones,
            text="📋 Copiar Mensaje",
            command=self._copiar_mensaje,
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36,
            width=160,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self._btn_copiar.pack(side="right", padx=(8, 0))

        self._btn_generar = ctk.CTkButton(
            panel_botones,
            text="🔄 Generar",
            command=self._actualizar_preview,
            font=ctk.CTkFont(size=12),
            height=36,
            width=120,
            fg_color=("#1f6aa5", "#1f6aa5"),
            hover_color=("#144e7a", "#144e7a"),
        )
        self._btn_generar.pack(side="right")

        self._label_estado = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("#238636", "#3fb950"),
        )
        self._label_estado.grid(row=6, column=0, sticky="e", padx=margen_x, pady=(0, 4))

    # ── Lógica ────────────────────────────────────────────────────────────────

    def _obtener_telefonos(self) -> tuple[list[str], list[str]]:
        telefonos = []
        errores = []

        tel1 = self._entry_tel1.get().strip()
        if tel1:
            telefono_formateado, error = _normalizar_telefono_nanp(tel1)
            if error:
                errores.append(f"Número 1: {error}")
            else:
                telefonos.append(telefono_formateado)

        tel2 = self._entry_tel2.get().strip()
        if tel2:
            telefono_formateado, error = _normalizar_telefono_nanp(tel2)
            if error:
                errores.append(f"Número 2: {error}")
            else:
                telefonos.append(telefono_formateado)

        return telefonos, errores

    def _formatear_telefonos(self, telefonos: list[str]) -> str:
        if len(telefonos) == 1:
            return telefonos[0]
        elif len(telefonos) == 2:
            return f"{telefonos[0]} y {telefonos[1]}"
        return ", ".join(telefonos)

    def _requiere_telefonos(self) -> bool:
        tipo = self._tipo_mensaje_var.get()
        return PLANTILLAS_MENSAJES[tipo].get("requiere_telefonos", True)

    def _al_cambiar_tipo_mensaje(self, *_):
        self._actualizar_estado_telefonos()
        self._actualizar_preview()

    def _actualizar_estado_telefonos(self):
        requiere_telefonos = self._requiere_telefonos()
        estado = "normal" if requiere_telefonos else "disabled"
        self._entry_tel1.configure(state=estado)
        self._entry_tel2.configure(state=estado)

    def _actualizar_preview(self, *_):
        tipo = self._tipo_mensaje_var.get()
        idioma = self._idioma_var.get()
        telefonos, errores = self._obtener_telefonos()
        plantilla = PLANTILLAS_MENSAJES[tipo]
        requiere_telefonos = self._requiere_telefonos()
        self._preview_valido = False

        if requiere_telefonos and errores:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0",
                "Corrige los números telefónicos:\n"
                + "\n".join(f"• {error}" for error in errores)
                + "\n\nFormatos aceptados: 555-1234, (787) 555-1234, +1 (939) 555-1234.",
            )
            self._textbox_preview.configure(state="disabled")
            return

        if requiere_telefonos and not telefonos:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0", "Ingresa al menos un número telefónico para generar el mensaje."
            )
            self._textbox_preview.configure(state="disabled")
            return

        if requiere_telefonos and len(telefonos) > 2:
            self._textbox_preview.configure(state="normal")
            self._textbox_preview.delete("0.0", "end")
            self._textbox_preview.insert(
                "0.0", "Máximo 2 números telefónicos permitidos."
            )
            self._textbox_preview.configure(state="disabled")
            return

        texto_plantilla = plantilla[idioma]
        telefonos_str = (
            self._formatear_telefonos(telefonos) if requiere_telefonos else ""
        )
        mensaje = _procesar_texto(
            texto_plantilla, len(telefonos), telefonos_str, idioma
        )

        self._textbox_preview.configure(state="normal")
        self._textbox_preview.delete("0.0", "end")
        self._textbox_preview.insert("0.0", mensaje)
        self._textbox_preview.configure(state="disabled")
        self._preview_valido = True

    def _copiar_mensaje(self):
        mensaje = self._textbox_preview.get("0.0", "end").strip()

        if not mensaje or not getattr(self, "_preview_valido", False):
            messagebox.showwarning(
                "Sin mensaje", "Genera un mensaje válido antes de copiar.", parent=self
            )
            return

        self.clipboard_clear()
        self.clipboard_append(mensaje)

        self._label_estado.configure(text="✓ Mensaje copiado al portapapeles")
        self.after(2500, lambda: self._label_estado.configure(text=""))

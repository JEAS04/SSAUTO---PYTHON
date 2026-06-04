"""
ui/template_filler.py — Generador de mensajes con plantillas (standalone).

Script independiente que levanta una ventana de CustomTkinter para generar
mensajes personalizados usando plantillas predefinidas. Permite seleccionar
una plantilla, ingresar datos personales y de clientes, y generar un mensaje
con manejo automatico de singular/plural.

Ejecutar directamente: python ui/template_filler.py
"""

import re
import customtkinter as ctk
from .ventana_plantillas import PLANTILLAS_DEFAULT

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x600")
app.title("Generador de Mensajes")


# ------------------------------------------------------------
# FUNCIONES AUXILIARES: plural / singular
# ------------------------------------------------------------
def plural(cantidad: int, singular: str, plural_form: str = "") -> str:
    """Retorna la forma singular o plural de una palabra segun la cantidad.

    Args:
        cantidad: numero de elementos.
        singular: forma singular de la palabra.
        plural_form: forma plural. Si no se da, se usa singular + "s".

    Returns:
        La palabra en singular si cantidad == 1, en plural en caso contrario.

    Examples:
        plural(1, "cliente")   -> "cliente"
        plural(3, "cliente")   -> "clientes"
        plural(1, "pez", "peces") -> "pez"
    """
    if not plural_form:
        plural_form = singular + "s"
    return singular if cantidad == 1 else plural_form


def s(
    cantidad: int,
    singular: str,
    plural_form: str = "",
) -> str:
    """Alias corto de plural() para usarlo inline en f-strings."""
    return plural(cantidad, singular, plural_form)


def _reemplazar_plurales(texto: str) -> str:
    """
    Reemplaza tokens con sintaxis `{palabra|palabras}` dentro del texto
    según la cantidad definida en el contexto global *__ctx_cantidad__*.

    Ejemplo:
        "Tengo {1} {cliente|clientes}" → "Tengo 1 cliente"  si cantidad==1
        "Tengo {3} {cliente|clientes}" → "Tengo 3 clientes" si cantidad==3
    """
    # La cantidad se pasa como variable global para no modificar todas las firmas
    cantidad = globals().get("__ctx_cantidad__", 1)

    def _reemplazar(m: re.Match) -> str:
        a, b = m.group(1), m.group(2)
        return a if cantidad == 1 else b

    return re.sub(r"\{([^|}]+)\|([^}]+)\}", _reemplazar, texto)


# ------------------------------------------------------------
# FUNCIÓN GENERADORA
# ------------------------------------------------------------
def generar_mensaje():
    """Genera el mensaje combinando plantilla y datos del formulario.

    Sustituye placeholders [Nombre], [Cargo], [Empresa], [Cliente], etc.
    en la plantilla seleccionada con los valores ingresados por el usuario.
    Tambien maneja tokens de plural {singular|plural} y limpia placeholders
    no reemplazados dejandolos como «placeholder».

    Efectos secundarios:
        - Lee las entradas del formulario (entry_nombre, entry_cargo, etc.).
        - Escribe el resultado en el widget textbox.
    """

    nombre = entry_nombre.get()
    cargo = entry_cargo.get()
    empresa = entry_empresa.get()

    # Variables de plantilla
    template_seleccionada = template_var.get()
    if template_seleccionada == "--- Personalizado ---":
        plantilla_texto = ""
    else:
        # Buscar el texto de la plantilla seleccionada
        plantilla_texto = ""
        for p in PLANTILLAS_DEFAULT:
            if p["titulo"] == template_seleccionada:
                plantilla_texto = p["texto"]
                break

    # Variable múltiple: clientes
    clientes_raw = entry_clientes.get().split(",")
    clientes = [c.strip() for c in clientes_raw if c.strip()]
    cantidad_clientes = len(clientes)

    # Guardar cantidad en contexto global para _reemplazar_plurales
    globals()["__ctx_cantidad__"] = cantidad_clientes

    # Construir texto de clientes con plural/singular
    if cantidad_clientes == 1:
        texto_clientes = f"el cliente {clientes[0]}"
    else:
        texto_clientes = "los clientes " + ", ".join(clientes)

    # ── Construir mensaje ────────────────────────────────────
    # Si hay plantilla seleccionada: sustituir placeholders
    if plantilla_texto:
        mensaje = plantilla_texto[:]
        # Placeholders estándar
        mensaje = mensaje.replace("[Nombre]", nombre)
        mensaje = mensaje.replace("[nombre]", nombre)
        mensaje = mensaje.replace("[Cargo]", cargo)
        mensaje = mensaje.replace("[cargo]", cargo)
        mensaje = mensaje.replace("[Empresa]", empresa)
        mensaje = mensaje.replace("[empresa]", empresa)
        mensaje = mensaje.replace("[Cliente]", texto_clientes)
        mensaje = mensaje.replace("[cliente]", texto_clientes)
        mensaje = mensaje.replace("[clientes]", ", ".join(clientes))

        # Reemplazar tokens plurales {singular|plural}
        mensaje = _reemplazar_plurales(mensaje)

        # Limpiar placeholders sin reemplazar
        mensaje = re.sub(r"\[([^\]]+)\]", r"«\1»", mensaje)
    else:
        # Mensaje libre / personalizado
        mensaje = f"""
Mi nombre es {nombre} y le escribo en calidad de {cargo} en {empresa}.

Este mensaje va dirigido a {texto_clientes}.
        """.strip()

    textbox.delete("1.0", "end")
    textbox.insert("1.0", mensaje)


# ------------------------------------------------------------
# INTERFAZ
# ------------------------------------------------------------

titulo = ctk.CTkLabel(app, text="Generador de Mensajes", font=("Arial", 24))
titulo.pack(pady=20)

# Selector de plantilla
tk_templates = ["--- Personalizado ---"] + [p["titulo"] for p in PLANTILLAS_DEFAULT]
template_var = ctk.StringVar(value=tk_templates[0])
ctk.CTkOptionMenu(
    app,
    variable=template_var,
    values=tk_templates,
    font=ctk.CTkFont(size=12),
    width=400,
).pack(pady=5)

ctk.CTkLabel(
    app,
    text="Selecciona una plantilla o usa «Personalizado»",
    font=ctk.CTkFont(size=10),
    text_color=("gray50", "gray60"),
).pack(pady=(0, 10))

entry_nombre = ctk.CTkEntry(app, placeholder_text="Tu Nombre", width=400)
entry_nombre.pack(pady=6)

entry_cargo = ctk.CTkEntry(app, placeholder_text="Tu Cargo", width=400)
entry_cargo.pack(pady=6)

entry_empresa = ctk.CTkEntry(app, placeholder_text="Nombre de la Empresa", width=400)
entry_empresa.pack(pady=6)

entry_clientes = ctk.CTkEntry(
    app, placeholder_text="Clientes separados por coma", width=400
)
entry_clientes.pack(pady=6)

btn_generar = ctk.CTkButton(app, text="Generar Mensaje", command=generar_mensaje)
btn_generar.pack(pady=15)

textbox = ctk.CTkTextbox(app, width=600, height=200)
textbox.pack(pady=10)

app.mainloop()

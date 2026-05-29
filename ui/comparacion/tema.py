"""
ui/comparacion/tema.py — Constantes de tema para la ventana de comparación.

Colores por estado de comparación y definiciones de dispatch states de Sunrun.
Extraído de ui/ventana_comparacion.py.
"""

COLORES_ESTADO = {
    "igual": {
        "bg": ("#d4edda", "#1a3a2a"),
        "texto": ("#155724", "#3fb950"),
        "icono": "✅",
    },
    "similar": {
        "bg": ("#fff3cd", "#3a3000"),
        "texto": ("#856404", "#d4a017"),
        "icono": "🟡",
    },
    "diferente": {
        "bg": ("#f8d7da", "#3a1a1a"),
        "texto": ("#721c24", "#f85149"),
        "icono": "❌",
    },
    "solo_hs": {
        "bg": ("#ffe5cc", "#3a2a1a"),
        "texto": ("#804000", "#f0a050"),
        "icono": "🟠",
    },
    "solo_sunrun": {
        "bg": ("#cce5ff", "#1a2a3a"),
        "texto": ("#004085", "#79c0ff"),
        "icono": "🔵",
    },
    "ambos_vacios": {
        "bg": ("#e2e3e5", "#2a2a2a"),
        "texto": ("#6c757d", "#6e7681"),
        "icono": "⚪",
    },
}

ETIQUETAS_ESTADO = {
    "igual": "IGUAL",
    "similar": "SIMILAR",
    "diferente": "DIFERENTE",
    "solo_hs": "SOLO HUBSPOT",
    "solo_sunrun": "SOLO SUNRUN",
    "ambos_vacios": "SIN DATOS",
}

DISPATCH_STATES = {
    "DISPATCH CANCELLED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH REPORTED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH APPROVED": {
        "trabajable": False,
        "color": "red",
        "texto": "No es trabajable",
    },
    "DISPATCH ACCEPTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
    "DISPATCH REJECTED": {
        "trabajable": True,
        "color": "green",
        "texto": "Es trabajable",
    },
}

NO_TRABAJABLES = {"DISPATCH CANCELLED", "DISPATCH REPORTED", "DISPATCH APPROVED"}
TRABAJABLES = {"DISPATCH ACCEPTED", "DISPATCH REJECTED"}


def info_dispatch_state(estado: str) -> tuple[str, str, str]:
    """
    Devuelve (color, texto_sufijo, header_color) para un dispatch state.

    color: "red" | "green" | None
    texto_sufijo: " -> No es trabajable" | " -> Es trabajable" | ""
    header_color: (light, dark) para el encabezado Sunrun
    """
    estado = estado.strip().upper()
    info = DISPATCH_STATES.get(estado)
    if info is None:
        return "red", " -> No es trabajable", (("#721c24", "#f85149"), ("#f8d7da", "#3a1a1a"))
    return info["color"], f" -> {info['texto']}", (
        (("#155724", "#3fb950"), ("#d4edda", "#1a3a2a")) if info["trabajable"]
        else (("#721c24", "#f85149"), ("#f8d7da", "#3a1a1a"))
    )

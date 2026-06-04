"""
config/apps_captura.py — Aplicaciones de captura rápida.

Cada entrada es un lanzador completo: al hacer clic en su botón,
se captura la región definida aquí y se sube automáticamente al
destino activo (el que tengas seleccionado en "Subir a:").

Para cambiar la región de una app:
  Opción A (rápida): usar el botón ⚙ que aparece junto a la app en la UI,
                     medís la nueva región y se actualiza en config.json.
  Opción B (manual): editar el dict "region" directamente aquí.

Para agregar una nueva app: copiar un bloque y rellenar los campos.

Campos:
  nombre  : str   — etiqueta del botón (corta, máx ~12 chars)
  icono   : str   — emoji decorativo
  region  : dict  — top, left, width, height en píxeles
  monitor : int   — índice del monitor (1 = principal, 2 = secundario…)
  color   : tuple — (color_claro, color_oscuro) en hex CSS
"""

# Paleta de colores disponible
_AZUL = ("#1f6aa5", "#1a5496")
_VERDE = ("#2d7a3a", "#256630")
_NARANJA = ("#a05a00", "#8a4e00")
_VIOLETA = ("#6b3fa0", "#5a3488")
_TEAL = ("#1a7a6e", "#146058")
_YELLOW = ("#f4c542", "#d9a81e")

APPS_CAPTURA = [
    {
        "nombre": "Wolkbox",
        "icono": "📞",
        "region": {"top": 100, "left": 0, "width": 800, "height": 600},
        "monitor": 1,
        "color": _AZUL,
    },
    {
        "nombre": "B2Chat",
        "icono": "💬",
        "region": {"top": 200, "left": 100, "width": 900, "height": 500},
        "monitor": 1,
        "color": _VIOLETA,
    },
    {
        "nombre": "Correo",
        "icono": "📧",
        "region": {"top": 150, "left": 50, "width": 1000, "height": 700},
        "monitor": 1,
        "color": _NARANJA,
    },
    {
        "nombre": "Calendar",
        "icono": "📅",
        "region": {"top": 300, "left": 200, "width": 850, "height": 550},
        "monitor": 1,
        "color": _VERDE,
    },
    {
        "nombre": "App 5",
        "icono": "📊",
        "region": {"top": 80, "left": 0, "width": 1920, "height": 980},
        "monitor": 1,
        "color": _TEAL,
    },
    {
        "nombre": "App 6",
        "icono": "📊",
        "region": {"top": 80, "left": 0, "width": 1920, "height": 980},
        "monitor": 1,
        "color": _YELLOW,
    },
]

"""
utils/colors.py — Utilidades de manipulación de colores.
"""


def oscurecer(color_hex: str, factor: float = 0.80) -> str:
    """
    Oscurece un color hexadecimal multiplicando cada canal RGB por factor.

    Parameters
    ----------
    color_hex : color en formato "#RRGGBB"
    factor    : multiplicador por canal (0.0 = negro, 1.0 = sin cambio)

    Returns
    -------
    Color oscurecido en formato "#RRGGBB", o "#444444" si hay error.
    """
    try:
        h = color_hex.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return "#{:02x}{:02x}{:02x}".format(
            max(0, int(r * factor)),
            max(0, int(g * factor)),
            max(0, int(b * factor)),
        )
    except Exception:
        return "#444444"

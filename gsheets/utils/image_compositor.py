"""
Módulo 4 — Composición de imagen de ticket.

Toma 4 capturas de celdas y las compone en una grilla 2x2:
    +-----------+-----------+
    |    A3     |    F3     |
    +-----------+-----------+
    |    A6     |    F6     |
    +-----------+-----------+

Mantiene resolución original de cada celda.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

# ── Logger ────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

_BORDER_COLOR = (200, 200, 200)  # Gris claro para bordes entre celdas
_BORDER_WIDTH = 2
_BG_COLOR = (255, 255, 255)  # Blanco de fondo


# ── Composición principal ─────────────────────────────────────────────────────


def compose_ticket_image(
    top_left_path: str | Path,
    top_right_path: str | Path,
    bottom_left_path: str | Path,
    bottom_right_path: str | Path,
    output_path: str | Path,
    border_width: int = _BORDER_WIDTH,
    border_color: tuple[int, int, int] = _BORDER_COLOR,
    labels: dict[str, str] | None = None,
) -> str:
    """
    Compone 4 imágenes de celdas en una grilla 2x2 y guarda el resultado.

    Args:
        top_left_path: Ruta a la captura de la celda superior izquierda (ej. A3).
        top_right_path: Ruta a la captura de la celda superior derecha (ej. F3).
        bottom_left_path: Ruta a la captura de la celda inferior izquierda (ej. A6).
        bottom_right_path: Ruta a la captura de la celda inferior derecha (ej. F6).
        output_path: Ruta donde guardar la imagen compuesta.
        border_width: Ancho del borde entre celdas en píxeles.
        border_color: Color RGB del borde.
        labels: Diccionario opcional con etiquetas para cada celda
                (ej. {"top_left": "A3", ...}). Se dibujan sobre la celda.

    Returns:
        Ruta absoluta de la imagen generada.

    Raises:
        FileNotFoundError: Si alguna imagen de entrada no existe.
        ValueError: Si las imágenes no se pueden abrir.
    """
    output_path = Path(output_path)

    # Cargar las 4 imágenes
    images = {
        "top_left": _load_image(top_left_path),
        "top_right": _load_image(top_right_path),
        "bottom_left": _load_image(bottom_left_path),
        "bottom_right": _load_image(bottom_right_path),
    }

    # Normalizar dimensiones por fila y columna
    # Las celdas de la misma columna deben tener el mismo ancho
    # Las celdas de la misma fila deben tener el mismo alto
    col_left_width = max(
        images["top_left"].width, images["bottom_left"].width
    )
    col_right_width = max(
        images["top_right"].width, images["bottom_right"].width
    )
    row_top_height = max(
        images["top_left"].height, images["top_right"].height
    )
    row_bottom_height = max(
        images["bottom_left"].height, images["bottom_right"].height
    )

    # Tamaño total del canvas
    total_width = col_left_width + col_right_width + border_width
    total_height = row_top_height + row_bottom_height + border_width

    # Crear canvas
    canvas = Image.new("RGB", (total_width, total_height), _BG_COLOR)

    # Pegar cada imagen en su posición
    # Fila superior
    _paste_resized(canvas, images["top_left"], 0, 0, col_left_width, row_top_height)
    _paste_resized(
        canvas,
        images["top_right"],
        col_left_width + border_width,
        0,
        col_right_width,
        row_top_height,
    )

    # Fila inferior
    _paste_resized(
        canvas,
        images["bottom_left"],
        0,
        row_top_height + border_width,
        col_left_width,
        row_bottom_height,
    )
    _paste_resized(
        canvas,
        images["bottom_right"],
        col_left_width + border_width,
        row_top_height + border_width,
        col_right_width,
        row_bottom_height,
    )

    # Dibujar etiquetas si se solicitaron
    if labels:
        from PIL import ImageDraw, ImageFont

        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", size=12)  # type: ignore[attr-defined]
        except OSError:
            font = ImageFont.load_default()  # type: ignore[attr-defined]

        positions = {
            "top_left": (4, 2),
            "top_right": (col_left_width + border_width + 4, 2),
            "bottom_left": (4, row_top_height + border_width + 2),
            "bottom_right": (
                col_left_width + border_width + 4,
                row_top_height + border_width + 2,
            ),
        }
        for key, pos in positions.items():
            if key in labels:
                draw.text(pos, labels[key], fill=(100, 100, 100), font=font)

    # Guardar
    canvas.save(str(output_path), "PNG")
    logger.info("Imagen compuesta guardada en %s", output_path)

    return str(output_path.resolve())


# ── Helpers ───────────────────────────────────────────────────────────────────


def _load_image(path: str | Path) -> Image.Image:
    """Carga una imagen desde disco con manejo de errores."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Imagen no encontrada: {path}")
    try:
        img = Image.open(path)
        img.load()
        return img
    except Exception as exc:
        raise ValueError(f"No se pudo abrir la imagen {path}: {exc}") from exc


def _paste_resized(
    canvas: Image.Image,
    img: Image.Image,
    x: int,
    y: int,
    target_w: int,
    target_h: int,
) -> None:
    """Pega una imagen en el canvas, redimensionándola si es necesario."""
    if img.width == target_w and img.height == target_h:
        canvas.paste(img, (x, y))
    else:
        resized = img.resize((target_w, target_h), Image.LANCZOS)
        canvas.paste(resized, (x, y))

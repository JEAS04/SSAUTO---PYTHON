"""gsheets.utils — Parseo de celdas y composicion de imagenes.

Expone parse_target_cell para convertir referencias como "F6" en las
cuatro celdas A3/F3/A6/F6, y compose_ticket_image para unirlas en
una grilla 2x2.
"""

from gsheets.utils.cell_parser import parse_target_cell, col_letter_to_index, index_to_col_letter, CellReferences
from gsheets.utils.image_compositor import compose_ticket_image

__all__ = [
    "parse_target_cell",
    "col_letter_to_index",
    "index_to_col_letter",
    "CellReferences",
    "compose_ticket_image",
]

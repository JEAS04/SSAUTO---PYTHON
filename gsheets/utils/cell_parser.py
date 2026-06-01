"""
Módulo 1 — Parser de referencia de celda.

Convierte una referencia tipo "F6" en las cuatro celdas de interés:
  A3, {col}3, A{row}, {col}{row}
Soporta columnas de una o varias letras (A..ZZZ).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

# ── Constantes ────────────────────────────────────────────────────────────────

_COL_FIJA = "A"
_FILA_FIJA = 3

_PATRON_CELDA = re.compile(r"^([A-Za-z]+)(\d+)$")

# ── Dataclass ─────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class CellReferences:
    """Cuatro referencias generadas a partir de una celda objetivo."""

    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    target: str

    def as_dict(self) -> dict[str, str]:
        return {
            "top_left": self.top_left,
            "top_right": self.top_right,
            "bottom_left": self.bottom_left,
            "bottom_right": self.bottom_right,
        }

    def all_refs(self) -> list[str]:
        return [self.top_left, self.top_right, self.bottom_left, self.bottom_right]


# ── Conversiones columna <-> índice ───────────────────────────────────────────


def col_letter_to_index(col: str) -> int:
    """Convierte letra(s) de columna a índice base-cero.  A=0, B=1, ..., Z=25, AA=26."""
    col = col.upper()
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def index_to_col_letter(idx: int) -> str:
    """Convierte índice base-cero a letra(s) de columna.  0=A, 25=Z, 26=AA."""
    result = ""
    while idx >= 0:
        result = chr((idx % 26) + ord("A")) + result
        idx = idx // 26 - 1
    return result


# ── Parser principal ──────────────────────────────────────────────────────────


def parse_target_cell(cell_ref: str) -> dict[str, str]:
    """
    A partir de una referencia como "F6", calcula las cuatro celdas de interés.

    Args:
        cell_ref: Referencia de celda (ej. "F6", "AA10", "ZZ100").

    Returns:
        Dict con claves: top_left, top_right, bottom_left, bottom_right.

    Raises:
        ValueError: Si el formato de la celda es inválido.
    """
    cell_ref = cell_ref.strip().upper()
    match = _PATRON_CELDA.match(cell_ref)
    if not match:
        raise ValueError(
            f"Formato de celda inválido: '{cell_ref}'. "
            f"Se espera una o más letras seguidas de dígitos (ej. A1, AA10)."
        )

    col_letra = match.group(1)
    fila = int(match.group(2))

    if fila < 1:
        raise ValueError(f"Número de fila inválido: {fila}. Debe ser >= 1.")

    return {
        "top_left": f"{_COL_FIJA}{_FILA_FIJA}",
        "top_right": f"{col_letra}{_FILA_FIJA}",
        "bottom_left": f"{_COL_FIJA}{fila}",
        "bottom_right": cell_ref,
    }


def build_cell_references(cell_ref: str) -> CellReferences:
    """
    Retorna un objeto CellReferences con las cuatro referencias.

    Args:
        cell_ref: Referencia de celda objetivo.

    Returns:
        CellReferences con las cuatro celdas calculadas.

    Raises:
        ValueError: Si el formato de la celda es inválido.
    """
    refs = parse_target_cell(cell_ref)
    return CellReferences(
        top_left=refs["top_left"],
        top_right=refs["top_right"],
        bottom_left=refs["bottom_left"],
        bottom_right=refs["bottom_right"],
        target=cell_ref.strip().upper(),
    )

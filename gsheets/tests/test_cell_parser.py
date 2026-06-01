"""
Tests para el parser de celdas (Módulo 1).
"""

import pytest
from gsheets.utils.cell_parser import (
    parse_target_cell,
    col_letter_to_index,
    index_to_col_letter,
    build_cell_references,
    CellReferences,
)


# ── parse_target_cell ─────────────────────────────────────────────────────


class TestParseTargetCell:
    def test_basic_f6(self):
        result = parse_target_cell("F6")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "F3"
        assert result["bottom_left"] == "A6"
        assert result["bottom_right"] == "F6"

    def test_large_cell_j20(self):
        result = parse_target_cell("J20")
        assert result == {
            "top_left": "A3",
            "top_right": "J3",
            "bottom_left": "A20",
            "bottom_right": "J20",
        }

    def test_double_letter_aa10(self):
        result = parse_target_cell("AA10")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "AA3"
        assert result["bottom_left"] == "A10"
        assert result["bottom_right"] == "AA10"

    def test_triple_letter_zz100(self):
        result = parse_target_cell("ZZ100")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "ZZ3"
        assert result["bottom_left"] == "A100"
        assert result["bottom_right"] == "ZZ100"

    def test_ab25(self):
        result = parse_target_cell("AB25")
        assert result == {
            "top_left": "A3",
            "top_right": "AB3",
            "bottom_left": "A25",
            "bottom_right": "AB25",
        }

    def test_a1_extreme_min_row(self):
        result = parse_target_cell("A1")
        assert result["top_left"] == "A3"
        assert result["top_right"] == "A3"
        assert result["bottom_left"] == "A1"
        assert result["bottom_right"] == "A1"

    def test_lowercase_input(self):
        result = parse_target_cell("f6")
        assert result["bottom_right"] == "F6"

    def test_input_with_spaces(self):
        result = parse_target_cell("  F6  ")
        assert result["bottom_right"] == "F6"

    def test_single_letter_z1(self):
        result = parse_target_cell("Z1")
        assert result["top_right"] == "Z3"
        assert result["bottom_right"] == "Z1"

    def test_invalid_format_raises_valueerror(self):
        with pytest.raises(ValueError, match="Formato de celda inválido"):
            parse_target_cell("6F")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("")

    def test_only_letters_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("ABC")

    def test_only_numbers_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("123")

    def test_row_zero_raises(self):
        with pytest.raises(ValueError, match="fila"):
            parse_target_cell("A0")

    def test_negative_row_raises(self):
        with pytest.raises(ValueError):
            parse_target_cell("A-5")


# ── col_letter_to_index ───────────────────────────────────────────────────


class TestColLetterToIndex:
    def test_a_is_0(self):
        assert col_letter_to_index("A") == 0

    def test_b_is_1(self):
        assert col_letter_to_index("B") == 1

    def test_z_is_25(self):
        assert col_letter_to_index("Z") == 25

    def test_aa_is_26(self):
        assert col_letter_to_index("AA") == 26

    def test_ab_is_27(self):
        assert col_letter_to_index("AB") == 27

    def test_az_is_51(self):
        assert col_letter_to_index("AZ") == 51

    def test_ba_is_52(self):
        assert col_letter_to_index("BA") == 52

    def test_zz_is_701(self):
        assert col_letter_to_index("ZZ") == 701

    def test_aaa_is_702(self):
        assert col_letter_to_index("AAA") == 702

    def test_lowercase(self):
        assert col_letter_to_index("f") == 5


# ── index_to_col_letter ───────────────────────────────────────────────────


class TestIndexToColLetter:
    def test_0_is_a(self):
        assert index_to_col_letter(0) == "A"

    def test_25_is_z(self):
        assert index_to_col_letter(25) == "Z"

    def test_26_is_aa(self):
        assert index_to_col_letter(26) == "AA"

    def test_27_is_ab(self):
        assert index_to_col_letter(27) == "AB"

    def test_701_is_zz(self):
        assert index_to_col_letter(701) == "ZZ"

    def test_702_is_aaa(self):
        assert index_to_col_letter(702) == "AAA"

    def test_roundtrip(self):
        for col_letter in ["A", "B", "Z", "AA", "AB", "AZ", "BA", "ZZ", "ABC"]:
            idx = col_letter_to_index(col_letter)
            assert index_to_col_letter(idx) == col_letter


# ── build_cell_references ─────────────────────────────────────────────────


class TestBuildCellReferences:
    def test_returns_cell_references_object(self):
        refs = build_cell_references("F6")
        assert isinstance(refs, CellReferences)
        assert refs.target == "F6"
        assert refs.top_left == "A3"

    def test_all_refs_returns_list(self):
        refs = build_cell_references("F6")
        assert refs.all_refs() == ["A3", "F3", "A6", "F6"]

    def test_as_dict(self):
        refs = build_cell_references("AA10")
        d = refs.as_dict()
        assert d["bottom_right"] == "AA10"
        assert len(d) == 4


# ── CellReferences dataclass ──────────────────────────────────────────────


class TestCellReferencesDataclass:
    def test_frozen(self):
        refs = CellReferences("A3", "F3", "A6", "F6", "F6")
        with pytest.raises(Exception):
            refs.top_left = "B3"  # type: ignore[misc]

    def test_equality(self):
        a = CellReferences("A3", "F3", "A6", "F6", "F6")
        b = CellReferences("A3", "F3", "A6", "F6", "F6")
        assert a == b

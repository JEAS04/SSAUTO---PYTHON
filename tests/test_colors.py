"""
Tests de utilidades de colores.

Cubre:
  - oscurecer: ajuste de luminosidad
"""

import pytest

from utils.colors import oscurecer


class TestOscurecer:
    def test_oscurecer_color_basico(self):
        color = "#ffffff"
        oscuro = oscurecer(color)
        assert oscuro.startswith("#")
        assert len(oscuro) == 7

    def test_oscurecer_negro_se_mantiene_negro(self):
        assert oscurecer("#000000") == "#000000"

    def test_oscurecer_con_factor(self):
        color = "#808080"
        resultado = oscurecer(color, factor=0.5)
        assert resultado == "#404040"

    def test_factor_cero_da_negro(self):
        assert oscurecer("#ff0000", factor=0.0) == "#000000"

    def test_factor_uno_da_mismo_color(self):
        assert oscurecer("#2ea043", factor=1.0) == "#2ea043"

    def test_color_de_la_app(self):
        azul_oscuro = oscurecer("#1f6aa5")
        assert azul_oscuro.startswith("#")

    def test_formato_con_y_sin_numeral(self):
        with_hash = oscurecer("#ff8040")
        assert with_hash.startswith("#")
        assert len(with_hash) == 7

    def test_error_devuelve_default(self):
        resultado = oscurecer("")
        assert resultado == "#444444"

    def test_color_invalido_devuelve_default(self):
        resultado = oscurecer("rojo")
        assert resultado == "#444444"

    def test_formato_rgb_hex_valido(self):
        for color in ["#ff0000", "#00ff00", "#0000ff", "#123456", "#abcdef"]:
            resultado = oscurecer(color, factor=0.5)
            assert resultado.startswith("#")
            assert len(resultado) == 7

    def test_oscurecer_por_defecto_factor_80(self):
        blanco = "#ffffff"
        resultado = oscurecer(blanco)
        assert resultado == "#cccccc"

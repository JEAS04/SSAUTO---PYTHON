"""
Tests de utilidades FSD.

Cubre:
  - solo_digitos: extraccion de digitos
  - fsd_display: formato de display
  - normalizar_fsd: normalizacion completa
"""

import pytest

from utils.fsd import solo_digitos, fsd_display, normalizar_fsd


class TestSoloDigitos:
    def test_solo_digitos_formato_estandar(self):
        assert solo_digitos("FSD-1172172") == "1172172"

    def test_solo_digitos_sin_guion(self):
        assert solo_digitos("FSD1172172") == "1172172"

    def test_solo_digitos_minusculas(self):
        assert solo_digitos("fsd 1172172") == "1172172"

    def test_solo_digitos_solo_numero(self):
        assert solo_digitos("1172172") == "1172172"

    def test_solo_digitos_vacio(self):
        assert solo_digitos("") == ""

    def test_solo_digitos_sin_digitos(self):
        assert solo_digitos("FSD-ABCDEF") == ""

    def test_solo_digitos_con_espacios(self):
        assert solo_digitos("  FSD - 980124  ") == "980124"

    def test_solo_digitos_con_caracteres_especiales(self):
        assert solo_digitos("FSD#980124!") == "980124"


class TestFsdDisplay:
    def test_formato_estandar(self):
        assert fsd_display("1172172") == "FSD-1172172"

    def test_con_ceros(self):
        assert fsd_display("000123") == "FSD-000123"

    def test_largo(self):
        resultado = fsd_display("9999999")
        assert resultado.startswith("FSD-")
        assert "9999999" in resultado


class TestNormalizarFsd:
    def test_none_devuelve_none(self):
        assert normalizar_fsd(None) is None

    def test_vacio_devuelve_none(self):
        assert normalizar_fsd("") is None

    def test_solo_espacios_devuelve_none(self):
        assert normalizar_fsd("   ") is None

    def test_no_string_devuelve_none(self):
        assert normalizar_fsd(12345) is None

    def test_formato_completo_se_mantiene(self):
        assert normalizar_fsd("FSD-980124") == "FSD-980124"

    def test_solo_digitos_agrega_fsd(self):
        assert normalizar_fsd("980124") == "FSD-980124"

    def test_minusculas_convierte_a_mayusculas(self):
        assert normalizar_fsd("fsd-980124") == "FSD-980124"

    def test_solo_digitos_con_espacio_medio(self):
        resultado = normalizar_fsd("fsd 980124")
        assert resultado is not None

    def test_con_espacios_alrededor(self):
        assert normalizar_fsd("  980124  ") == "FSD-980124"

    def test_texto_no_fsd_se_mantiene(self):
        assert normalizar_fsd("HOLA") == "HOLA"

    def test_fsd_corto(self):
        resultado = normalizar_fsd("123")
        assert resultado == "FSD-123"

    def test_solo_caracteres_no_numericos_no_agrega_fsd(self):
        assert normalizar_fsd("ABC-DEF") == "ABC-DEF"

    def test_con_digitos_y_guiones(self):
        assert normalizar_fsd("980-124") == "FSD-980-124"


class TestRoundTripFsd:
    """Flujo completo de normalizacion."""

    def test_solo_digitos_luego_fsd_display(self):
        numero = solo_digitos("FSD-1172172")
        display = fsd_display(numero)
        assert display == "FSD-1172172"

    def test_normalizar_luego_extraer_digitos(self):
        normalizado = normalizar_fsd("fsd 980124")
        digitos = solo_digitos(normalizado)
        assert digitos == "980124"

    def test_caso_real_completo(self):
        for entrada in [
            "FSD-980124",
            "fsd-980124",
            "980124",
            "fsd 980124",
            "FSD980124",
        ]:
            normalizado = normalizar_fsd(entrada)
            if normalizado:
                digitos = solo_digitos(normalizado)
                assert digitos == "980124", f"Fallo con entrada: {entrada}"

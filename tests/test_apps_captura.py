"""
Tests de apps_captura (definiciones estaticas).

Verifica:
  - Estructura de cada app
  - Campos requeridos presentes
  - Valores razonables
"""

import pytest

from config.apps_captura import APPS_CAPTURA


class TestAppsCaptura:
    def test_estructura_es_lista(self):
        assert isinstance(APPS_CAPTURA, list)

    def test_no_vacia(self):
        assert len(APPS_CAPTURA) > 0

    def test_cada_app_tiene_nombre(self):
        for app in APPS_CAPTURA:
            assert "nombre" in app
            assert isinstance(app["nombre"], str)
            assert len(app["nombre"]) > 0

    def test_cada_app_tiene_icono(self):
        for app in APPS_CAPTURA:
            assert "icono" in app
            assert isinstance(app["icono"], str)

    def test_cada_app_tiene_region(self):
        for app in APPS_CAPTURA:
            assert "region" in app
            assert isinstance(app["region"], dict)
            for clave in ("top", "left", "width", "height"):
                assert clave in app["region"]
                assert isinstance(app["region"][clave], int)

    def test_cada_app_tiene_monitor(self):
        for app in APPS_CAPTURA:
            assert "monitor" in app
            assert isinstance(app["monitor"], int)
            assert app["monitor"] >= 1

    def test_cada_app_tiene_color(self):
        for app in APPS_CAPTURA:
            assert "color" in app
            assert isinstance(app["color"], (tuple, list))
            assert len(app["color"]) == 2
            for c in app["color"]:
                assert isinstance(c, str)
                assert c.startswith("#")

    def test_region_valores_positivos_o_cero(self):
        for app in APPS_CAPTURA:
            r = app["region"]
            assert r["top"] >= 0
            assert r["left"] >= 0
            assert r["width"] > 0
            assert r["height"] > 0

    def test_nombres_unicos(self):
        nombres = [app["nombre"] for app in APPS_CAPTURA]
        assert len(nombres) == len(set(nombres))

    def test_nombres_razonables(self):
        nombres_validos = {"Wolkbox", "B2Chat", "Correo", "Calendar", "App 5", "App 6"}
        for app in APPS_CAPTURA:
            assert app["nombre"] in nombres_validos

    def test_colores_siguen_paleta(self):
        colores_validos = {
            "#1f6aa5",
            "#1a5496",
            "#2d7a3a",
            "#256630",
            "#a05a00",
            "#8a4e00",
            "#6b3fa0",
            "#5a3488",
            "#1a7a6e",
            "#146058",
            "#f4c542",
            "#d9a81e",
        }
        for app in APPS_CAPTURA:
            for c in app["color"]:
                assert c in colores_validos, f"Color {c} no esta en la paleta definida"

    def test_formato_color_hex_valido(self):
        import re

        hex_pattern = re.compile(r"^#[0-9a-fA-F]{6}$")
        for app in APPS_CAPTURA:
            for c in app["color"]:
                assert hex_pattern.match(c), f"Color {c} no es hex valido"

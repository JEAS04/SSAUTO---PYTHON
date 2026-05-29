"""
Tests de utilidades de path.

Cubre:
  - resource_path: ruta a recursos
"""

import os
import sys
import pytest

from utils.paths import resource_path


class TestResourcePath:
    def test_devuelve_ruta_absoluta(self):
        ruta = resource_path("config/config.json")
        assert os.path.isabs(ruta)

    def test_mantiene_estructura_de_directorios(self):
        ruta = resource_path("config/config.json")
        assert "config" in ruta
        assert "config.json" in ruta

    def test_con_archivo_raiz(self):
        ruta = resource_path("requirements.txt")
        assert "requirements.txt" in ruta

    def test_ruta_no_depende_de_meipass_sin_pyinstaller(self):
        ruta = resource_path("test.txt")
        directorio_actual = os.path.abspath(".")
        assert ruta.startswith(directorio_actual)

    def test_ruta_concatenacion_limpia(self):
        ruta = resource_path("config/config.json")
        assert "config" in ruta
        assert "config.json" in ruta

"""
Tests de persistencia de plantillas (plantillas.json).

Cubre:
  - Carga de plantillas por defecto cuando no existe archivo
  - Guardado y carga de plantillas
  - Edicion, creacion, eliminacion
  - Categoria y estructura
"""

import json
import pytest
from unittest.mock import patch

import ui.ventana_plantillas as vp
from ui.ventana_plantillas import (
    PLANTILLAS_DEFAULT,
    _cargar_plantillas,
    _guardar_plantillas,
)


class TestPlantillasModulo:
    """Pruebas a nivel de modulo (funciones puras)."""

    def test_cargar_sin_archivo_devuelve_default(self, mock_plantillas_path):
        if mock_plantillas_path.exists():
            mock_plantillas_path.unlink()
        plantillas = _cargar_plantillas()
        assert len(plantillas) == len(PLANTILLAS_DEFAULT)
        assert plantillas == PLANTILLAS_DEFAULT

    def test_cargar_con_archivo_existente(self, mock_plantillas_path):
        personalizadas = [{"titulo": "Test", "categoria": "General", "texto": "Hola"}]
        _guardar_plantillas(personalizadas)
        cargadas = _cargar_plantillas()
        assert cargadas == personalizadas

    def test_cargar_archivo_corrupto_devuelve_default(self, mock_plantillas_path):
        mock_plantillas_path.write_text("no es json valido {{{", encoding="utf-8")
        plantillas = _cargar_plantillas()
        assert plantillas == PLANTILLAS_DEFAULT

    def test_guardar_crea_directorio(self, temp_dir):
        sub = temp_dir / "subdir" / "plantillas.json"
        import ui.ventana_plantillas as vp_mod

        with patch("ui.ventana_plantillas.PLANTILLAS_PATH", sub):
            _guardar_plantillas([{"titulo": "X", "categoria": "G", "texto": "Y"}])
            assert sub.exists()

    def test_guardar_con_unicode(self, mock_plantillas_path):
        plantilla = [{"titulo": "Cañón", "categoria": "General", "texto": "áéíóú"}]
        _guardar_plantillas(plantilla)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["titulo"] == "Cañón"

    def test_guardar_multiples_plantillas(self, mock_plantillas_path):
        plantillas = [
            {"titulo": "A", "categoria": "General", "texto": "a"},
            {"titulo": "B", "categoria": "HubSpot", "texto": "b"},
            {"titulo": "C", "categoria": "Sunrun", "texto": "c"},
        ]
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert len(cargadas) == 3


class TestPlantillasDefault:
    """Verificacion de las plantillas por defecto."""

    def test_cantidad_plantillas_default(self):
        assert len(PLANTILLAS_DEFAULT) >= 6

    def test_todas_tienen_titulo(self):
        for p in PLANTILLAS_DEFAULT:
            assert p["titulo"]
            assert isinstance(p["titulo"], str)

    def test_todas_tienen_categoria(self):
        categorias = {p.get("categoria") for p in PLANTILLAS_DEFAULT}
        assert "HubSpot" in categorias or "hubspot" in [c.lower() for c in categorias]
        assert "Sunrun" in categorias or "sunrun" in [c.lower() for c in categorias]

    def test_todas_tienen_texto(self):
        for p in PLANTILLAS_DEFAULT:
            assert p["texto"]
            assert isinstance(p["texto"], str)

    def test_default_es_independiente_del_archivo(self, mock_plantillas_path):
        if mock_plantillas_path.exists():
            mock_plantillas_path.unlink()
        d1 = _cargar_plantillas()
        _guardar_plantillas([{"titulo": "Custom", "categoria": "X", "texto": "Y"}])
        d2 = _cargar_plantillas()
        assert len(d2) == 1
        assert d2[0]["titulo"] == "Custom"


class TestRoundTripPlantillas:
    """Flujos completos de edicion de plantillas."""

    def test_crear_leer_actualizar_eliminar(self, mock_plantillas_path):
        _guardar_plantillas(PLANTILLAS_DEFAULT.copy())

        plantillas = _cargar_plantillas()
        inicial = len(plantillas)

        plantillas.append({"titulo": "Nueva", "categoria": "General", "texto": "Nuevo texto"})
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        assert len(cargadas) == inicial + 1
        assert any(p["titulo"] == "Nueva" for p in cargadas)

        for p in plantillas:
            if p["titulo"] == "Nueva":
                p["texto"] = "Texto editado"
                break
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        nueva = next(p for p in cargadas if p["titulo"] == "Nueva")
        assert nueva["texto"] == "Texto editado"

        plantillas = [p for p in plantillas if p["titulo"] != "Nueva"]
        _guardar_plantillas(plantillas)

        cargadas = _cargar_plantillas()
        assert len(cargadas) == inicial
        assert not any(p["titulo"] == "Nueva" for p in cargadas)

    def test_cambiar_categoria_persiste(self, mock_plantillas_path):
        plantillas = _cargar_plantillas()
        plantillas[0]["categoria"] = "Sunrun"
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["categoria"] == "Sunrun"

    def test_cambiar_titulo_persiste(self, mock_plantillas_path):
        plantillas = _cargar_plantillas()
        plantillas[0]["titulo"] = "Titulo Modificado"
        _guardar_plantillas(plantillas)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["titulo"] == "Titulo Modificado"

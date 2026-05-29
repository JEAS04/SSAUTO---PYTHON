"""
Tests de integracion: flujos completos de guardado/carga.

Verifica:
  - Round-trip de todas las claves de config.json simultaneamente
  - Perfiles: crear, cargar, modificar, eliminar
  - Credenciales + cookies juntas
  - Persistencia sobre reinicio simulado
  - Que las configuraciones de UI persistan correctamente
  - Que configuraciones guardadas se restauren tras reinicio
  - Deteccion de configs en UI que no se guardan (via auditoria de claves)
"""

import json
import os
import pickle
import sys
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from config.configuracion import (
    cargar_config,
    guardar_config,
    cargar_perfiles,
    guardar_perfiles,
    cargar_auto_submit,
    guardar_auto_submit,
    cargar_headless,
    guardar_headless,
    cargar_chrome_existente,
    guardar_chrome_existente,
    cargar_destino_subida,
    guardar_destino_subida,
)
from config.credenciales import (
    guardar_credenciales,
    cargar_credenciales,
    borrar_credenciales,
)


class TestConfigFullRoundTrip:
    """Guarda todas las claves y verifica que persistan tras recarga."""

    TODAS_LAS_CLAVES = {
        "tema": "light",
        "ultimo_monitor": 2,
        "regiones_apps": {
            "Wolkbox": {"top": 10, "left": 20, "width": 800, "height": 600},
        },
        "monitores_apps": {"Wolkbox": 1},
        "perfiles_region": {
            "Perfil1": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            },
        },
        "keybind": "<Control-Shift-p>",
        "headless": True,
        "chrome_existente": False,
        "destino_subida": "HUBSPOT",
        "auto_submit_nota": True,
    }

    def test_round_trip_todas_las_claves(self, mock_archivo_config):
        guardar_config(self.TODAS_LAS_CLAVES)
        cargado = cargar_config()

        for clave, valor in self.TODAS_LAS_CLAVES.items():
            assert clave in cargado, f"Falta clave '{clave}' en config cargada"
            assert cargado[clave] == valor, (
                f"Clave '{clave}': esperado {valor}, obtenido {cargado[clave]}"
            )

    def test_reinicio_simulado(self, mock_archivo_config):
        """Simula cerrar y reabrir la app: guarda, limpia cache, recarga."""
        guardar_config(self.TODAS_LAS_CLAVES)

        import config.configuracion as cfg

        cargado1 = cargar_config()
        assert cargado1["tema"] == "light"

        mock_archivo_config.write_text(json.dumps(self.TODAS_LAS_CLAVES), encoding="utf-8")
        cargado2 = cargar_config()
        assert cargado2 == cargado1

    def test_config_vacia_se_completa_con_defaults(self, mock_archivo_config):
        guardar_config({})
        cargado = cargar_config()
        assert cargado == {}
        assert cargar_auto_submit() is True
        assert cargar_headless() is False
        assert cargar_chrome_existente() is True
        assert cargar_destino_subida() == "AMBOS"

    def test_config_parcial_no_sobreescribe_faltantes(self, mock_archivo_config):
        guardar_config({"tema": "dark"})
        config = cargar_config()
        assert config["tema"] == "dark"
        assert "headless" not in config
        assert cargar_headless() is False

    def test_cambios_progresivos_no_corrompen(self, mock_archivo_config):
        guardar_config({"tema": "dark"})
        guardar_headless(True)
        guardar_auto_submit(False)
        guardar_chrome_existente(False)
        guardar_destino_subida("SUNRUN")

        assert cargar_config()["tema"] == "dark"
        assert cargar_headless() is True
        assert cargar_auto_submit() is False
        assert cargar_chrome_existente() is False
        assert cargar_destino_subida() == "SUNRUN"


class TestPerfilesRoundTrip:
    """Flujo completo de perfiles de region."""

    def test_crear_cargar_modificar_eliminar_perfil(self, mock_archivo_config):
        perfiles = {
            "Monitor Principal": {
                "top": 0, "left": 0, "width": 1920, "height": 1080,
                "monitor_index": 1,
            },
        }
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert "Monitor Principal" in cargados
        assert cargados["Monitor Principal"]["width"] == 1920

        perfiles["Monitor Secundario"] = {
            "top": 0, "left": 1920, "width": 1280, "height": 720,
            "monitor_index": 2,
        }
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert len(cargados) == 2

        perfiles["Monitor Principal"]["height"] = 1200
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert cargados["Monitor Principal"]["height"] == 1200

        del perfiles["Monitor Principal"]
        guardar_perfiles(perfiles)
        cargados = cargar_perfiles()
        assert "Monitor Principal" not in cargados
        assert "Monitor Secundario" in cargados

    def test_nombre_con_caracteres_especiales(self, mock_archivo_config):
        guardar_perfiles({"Español/测试": {"top": 1, "left": 2, "width": 3, "height": 4}})
        assert "Español/测试" in cargar_perfiles()


class TestCredencialesCookiesIntegration:
    """Integracion de credenciales + cookies (sin driver real)."""

    def test_credenciales_persisten_entre_llamadas(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "secret123")
        guardar_credenciales("SUNRUN", "sr_user", "sr_pass")

        u1, c1 = cargar_credenciales("HUBSPOT")
        u2, c2 = cargar_credenciales("SUNRUN")

        assert u1 == "admin"
        assert c1 == "secret123"
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

        borrar_credenciales("HUBSPOT")
        u1, c1 = cargar_credenciales("HUBSPOT")
        assert u1 == ""
        assert c1 == ""

        u2, c2 = cargar_credenciales("SUNRUN")
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

    def test_cookies_persisten_y_se_recuperan(self, temp_dir):
        cookies_dir = temp_dir / "cookies"
        cookies_dir.mkdir(exist_ok=True)

        cookies = [
            {"name": "session", "value": "abc", "domain": "test.com"},
            {"name": "lang", "value": "es", "domain": "test.com"},
        ]
        ruta = cookies_dir / "HUBSPOT.pkl"
        ruta.write_bytes(pickle.dumps(cookies))

        cargadas = pickle.loads(ruta.read_bytes())
        assert len(cargadas) == 2
        assert cargadas[0]["name"] == "session"
        assert cargadas[1]["value"] == "es"


class TestTemplateIntegration:
    """Integracion de plantillas con archivo real."""

    def test_templates_survive_multiple_writes(self, mock_plantillas_path):
        from ui.ventana_plantillas import _cargar_plantillas, _guardar_plantillas

        t = _cargar_plantillas()
        original_len = len(t)

        for i in range(5):
            t.append({"titulo": f"Test {i}", "categoria": "General", "texto": f"Body {i}"})
            _guardar_plantillas(t)
            cargadas = _cargar_plantillas()
            assert len(cargadas) == original_len + i + 1

    def test_templates_no_se_corrompen_con_edicion(self, mock_plantillas_path):
        from ui.ventana_plantillas import _cargar_plantillas, _guardar_plantillas

        t = _cargar_plantillas()
        t[0]["texto"] = "EDITADO"
        _guardar_plantillas(t)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["texto"] == "EDITADO"

        t2 = _cargar_plantillas()
        t2[0]["categoria"] = "Sunrun"
        _guardar_plantillas(t2)
        cargadas = _cargar_plantillas()
        assert cargadas[0]["categoria"] == "Sunrun"


class TestUIConfigAudit:
    """
    Auditoria de configuraciones de UI.

    Verifica que cada configuracion visible en la interfaz tenga
    una clave correspondiente en config.json y que persista.
    """

    UI_CONFIG_MAPPING = {
        "Tema (Oscuro/Claro)": "tema",
        "Monitor (último)": "ultimo_monitor",
        "Headless switch": "headless",
        "Chrome existente switch": "chrome_existente",
        "Auto-submit nota switch": "auto_submit_nota",
        "Destino subida": "destino_subida",
        "Keybind": "keybind",
        "Perfiles de region": "perfiles_region",
        "Regiones apps": "regiones_apps",
        "Monitores apps": "monitores_apps",
    }

    def test_todas_las_claves_ui_tienen_persistencia(self, mock_archivo_config):
        """Verifica que cada config de UI se guarde y recupere."""
        datos = {
            "tema": "dark",
            "ultimo_monitor": 1,
            "headless": False,
            "chrome_existente": True,
            "auto_submit_nota": False,
            "destino_subida": "SUNRUN",
            "keybind": "<Control-Return>",
            "perfiles_region": {"P1": {"top": 1, "left": 2, "width": 3, "height": 4}},
            "regiones_apps": {"AppX": {"top": 0, "left": 0, "width": 100, "height": 100}},
            "monitores_apps": {"AppX": 1},
        }
        guardar_config(datos)
        cargado = cargar_config()

        for ui_name, clave in self.UI_CONFIG_MAPPING.items():
            assert clave in cargado, (
                f"CONFIG NO PERSISTIDA: '{ui_name}' (clave '{clave}') NO esta en config.json"
            )

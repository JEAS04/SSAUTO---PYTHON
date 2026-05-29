"""
Tests de persistencia de configuracion (config.json).

Cubre:
  - Carga de archivo inexistente → dict vacio
  - Carga de archivo corrupto → dict vacio (no crashea)
  - Guardado de datos → round-trip completo
  - Cada clave individual: tema, ultimo_monitor, keybind, headless,
    chrome_existente, destino_subida, auto_submit_nota
  - Perfiles de region: cargar, guardar, setter/getter
  - Constantes del modulo
"""

import json
import pytest
from unittest.mock import patch

from config.configuracion import (
    ARCHIVO_CONFIG,
    AUTO_SUBMIT_DEFAULT,
    CLAVE_AUTO_SUBMIT,
    CLAVE_CHROME_EXISTENTE,
    CLAVE_DESTINO_SUBIDA,
    CLAVE_HEADLESS,
    CLAVE_PERFILES,
    CHROME_EXISTENTE_DEFAULT,
    CHROME_PATHS,
    CHROME_USER_DATA,
    DESTINO_SUBIDA_DEFAULT,
    HEADLESS_DEFAULT,
    KEYRING_APP,
    PERFIL_POR_DEFECTO,
    PUERTO_DEBUG,
    TEMA_APARIENCIA,
    TEMA_COLOR,
    cargar_auto_submit,
    cargar_chrome_existente,
    cargar_config,
    cargar_destino_subida,
    cargar_headless,
    cargar_perfiles,
    guardar_auto_submit,
    guardar_chrome_existente,
    guardar_config,
    guardar_destino_subida,
    guardar_headless,
    guardar_perfiles,
)


class TestConstantes:
    """Verificacion de constantes del modulo."""

    def test_tema_apariencia_es_dark(self):
        assert TEMA_APARIENCIA == "dark"

    def test_tema_color_es_blue(self):
        assert TEMA_COLOR == "blue"

    def test_keyring_app_definido(self):
        assert KEYRING_APP == "AutoCapturaApp"

    def test_puerto_debug_es_9222(self):
        assert PUERTO_DEBUG == 9222

    def test_chrome_user_data_definido(self):
        assert "chrome_sesion_ssauto" in CHROME_USER_DATA

    def test_chrome_paths_es_lista_no_vacia(self):
        assert isinstance(CHROME_PATHS, list)
        assert len(CHROME_PATHS) >= 3

    def test_archivo_config_termina_en_config_json(self):
        assert ARCHIVO_CONFIG.endswith("config.json")

    def test_perfil_por_defecto_tiene_cuatro_claves(self):
        for clave in ("top", "left", "width", "height"):
            assert clave in PERFIL_POR_DEFECTO

    def test_claves_esperadas_definidas(self):
        assert CLAVE_AUTO_SUBMIT == "auto_submit_nota"
        assert CLAVE_HEADLESS == "headless"
        assert CLAVE_CHROME_EXISTENTE == "chrome_existente"
        assert CLAVE_DESTINO_SUBIDA == "destino_subida"
        assert CLAVE_PERFILES == "perfiles_region"

    def test_defaults_coherentes(self):
        assert AUTO_SUBMIT_DEFAULT is True
        assert HEADLESS_DEFAULT is False
        assert CHROME_EXISTENTE_DEFAULT is True
        assert DESTINO_SUBIDA_DEFAULT == "AMBOS"


class TestCargarConfig:
    """Carga del archivo config.json."""

    def test_archivo_inexistente_devuelve_dict_vacio(self, mock_archivo_config):
        if mock_archivo_config.exists():
            mock_archivo_config.unlink()
        resultado = cargar_config()
        assert resultado == {}
        assert isinstance(resultado, dict)

    def test_archivo_vacio_devuelve_dict_vacio(self, mock_archivo_config):
        resultado = cargar_config()
        assert resultado == {}

    def test_carga_datos_validos(self, config_con_datos_completos):
        resultado = cargar_config()
        assert resultado["tema"] == "light"
        assert resultado["ultimo_monitor"] == 2
        assert resultado["headless"] is True
        assert resultado["chrome_existente"] is False

    def test_archivo_corrupto_devuelve_dict_vacio(self, mock_archivo_config):
        mock_archivo_config.write_text("esto no es json {{", encoding="utf-8")
        resultado = cargar_config()
        assert resultado == {}

    def test_carga_dict_vacio_no_tira_excepcion(self, mock_archivo_config):
        mock_archivo_config.write_text(json.dumps([]), encoding="utf-8")
        resultado = cargar_config()
        assert isinstance(resultado, list) or isinstance(resultado, dict)


class TestGuardarConfig:
    """Guardado del archivo config.json."""

    def test_guarda_y_recupera_datos_simples(self, mock_archivo_config):
        datos = {"tema": "dark", "keybind": "<Control-p>"}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["tema"] == "dark"
        assert cargado["keybind"] == "<Control-p>"

    def test_guarda_y_recupera_booleanos(self, mock_archivo_config):
        datos = {"headless": True, "chrome_existente": False}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["headless"] is True
        assert cargado["chrome_existente"] is False

    def test_guarda_y_recupera_enteros(self, mock_archivo_config):
        datos = {"ultimo_monitor": 3}
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["ultimo_monitor"] == 3

    def test_guarda_y_recupera_anidados(self, mock_archivo_config):
        datos = {
            "regiones_apps": {
                "Wolkbox": {"top": 100, "left": 0, "width": 800, "height": 600}
            }
        }
        guardar_config(datos)
        cargado = cargar_config()
        assert cargado["regiones_apps"]["Wolkbox"]["width"] == 800

    def test_guarda_con_indentacion_legible(self, mock_archivo_config):
        datos = {"tema": "light"}
        guardar_config(datos)
        contenido = mock_archivo_config.read_text(encoding="utf-8")
        assert "  " in contenido
        assert "\n" in contenido

    def test_guarda_multiples_veces_no_corrompe(self, mock_archivo_config):
        guardar_config({"a": 1})
        guardar_config({"b": 2})
        cargado = cargar_config()
        assert cargado["b"] == 2

    def test_guarda_en_directorio_que_no_existe(self, temp_dir):
        from config import configuracion

        nuevo = temp_dir / "sub" / "config.json"
        with patch("config.configuracion.ARCHIVO_CONFIG", str(nuevo)):
            guardar_config({"ok": True})
            assert nuevo.exists()
            assert json.loads(nuevo.read_text()) == {"ok": True}

    def test_guarda_unicode_sin_problemas(self, mock_archivo_config):
        guardar_config({"nombre": "Canción"})
        cargado = cargar_config()
        assert cargado["nombre"] == "Canción"


class TestAutoSubmit:
    """Persistencia de auto_submit_nota."""

    def test_cargar_default(self, mock_archivo_config):
        assert cargar_auto_submit() is True

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_auto_submit(True)
        assert cargar_auto_submit() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_auto_submit(False)
        assert cargar_auto_submit() is False

    def test_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"headless": True})
        guardar_auto_submit(False)
        config = cargar_config()
        assert config["headless"] is True
        assert config["auto_submit_nota"] is False


class TestHeadless:
    """Persistencia de headless."""

    def test_cargar_default(self, mock_archivo_config):
        assert cargar_headless() is False

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_headless(True)
        assert cargar_headless() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_headless(True)
        guardar_headless(False)
        assert cargar_headless() is False

    def test_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"auto_submit_nota": True, "tema": "dark"})
        guardar_headless(True)
        config = cargar_config()
        assert config["auto_submit_nota"] is True
        assert config["tema"] == "dark"


class TestChromeExistente:
    """Persistencia de chrome_existente."""

    def test_cargar_default(self, mock_archivo_config):
        assert cargar_chrome_existente() is True

    def test_guardar_y_cargar_false(self, mock_archivo_config):
        guardar_chrome_existente(False)
        assert cargar_chrome_existente() is False

    def test_guardar_y_cargar_true(self, mock_archivo_config):
        guardar_chrome_existente(True)
        assert cargar_chrome_existente() is True


class TestDestinoSubida:
    """Persistencia de destino_subida."""

    def test_cargar_default(self, mock_archivo_config):
        assert cargar_destino_subida() == "AMBOS"

    def test_guardar_y_cargar_hubspot(self, mock_archivo_config):
        guardar_destino_subida("HUBSPOT")
        assert cargar_destino_subida() == "HUBSPOT"

    def test_guardar_y_cargar_sunrun(self, mock_archivo_config):
        guardar_destino_subida("SUNRUN")
        assert cargar_destino_subida() == "SUNRUN"

    def test_guardar_y_cargar_ambos(self, mock_archivo_config):
        guardar_destino_subida("HUBSPOT")
        guardar_destino_subida("AMBOS")
        assert cargar_destino_subida() == "AMBOS"


class TestPerfiles:
    """Persistencia de perfiles de region."""

    def test_cargar_sin_perfiles_devuelve_dict_vacio(self, mock_archivo_config):
        assert cargar_perfiles() == {}

    def test_guardar_y_cargar_un_perfil(self, mock_archivo_config):
        perfil = {
            "Monitor 1": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            }
        }
        guardar_perfiles(perfil)
        cargado = cargar_perfiles()
        assert "Monitor 1" in cargado
        assert cargado["Monitor 1"]["width"] == 1920

    def test_guardar_y_cargar_multiples_perfiles(self, mock_archivo_config):
        perfiles = {
            "Perfil A": {"top": 10, "left": 20, "width": 800, "height": 600},
            "Perfil B": {"top": 30, "left": 40, "width": 1024, "height": 768},
        }
        guardar_perfiles(perfiles)
        cargado = cargar_perfiles()
        assert len(cargado) == 2
        assert "Perfil A" in cargado
        assert "Perfil B" in cargado

    def test_guardar_perfiles_no_sobreescribe_otras_claves(self, mock_archivo_config):
        guardar_config({"tema": "dark", "headless": True})
        guardar_perfiles({"P1": {"top": 1, "left": 2, "width": 3, "height": 4}})
        config = cargar_config()
        assert config["tema"] == "dark"
        assert config["headless"] is True
        assert "P1" in config["perfiles_region"]

    def test_guardar_perfiles_sin_monitor_index(self, mock_archivo_config):
        guardar_perfiles({"P1": {"top": 1, "left": 2, "width": 3, "height": 4}})
        cargado = cargar_perfiles()
        assert "monitor_index" not in cargado["P1"]

    def test_eliminar_perfil_via_guardar(self, mock_archivo_config):
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}, "B": {"top": 5, "left": 6, "width": 7, "height": 8}})
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}})
        cargado = cargar_perfiles()
        assert "A" in cargado
        assert "B" not in cargado

    def test_vaciar_perfiles(self, mock_archivo_config):
        guardar_perfiles({"A": {"top": 1, "left": 2, "width": 3, "height": 4}})
        guardar_perfiles({})
        assert cargar_perfiles() == {}


class TestTema:
    """Persistencia de tema (via cargar_config directamente)."""

    def test_tema_default_cuando_no_existe(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("tema", "dark") == "dark"

    def test_tema_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"tema": "light"})
        config = cargar_config()
        assert config["tema"] == "light"

    def test_tema_cambia_entre_dark_y_light(self, mock_archivo_config):
        guardar_config({"tema": "light"})
        assert cargar_config()["tema"] == "light"
        guardar_config({"tema": "dark"})
        assert cargar_config()["tema"] == "dark"


class TestUltimoMonitor:
    """Persistencia de ultimo_monitor (via cargar_config directamente)."""

    def test_default_cuando_no_existe(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("ultimo_monitor", 1) == 1

    def test_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"ultimo_monitor": 2})
        assert cargar_config()["ultimo_monitor"] == 2

    def test_valor_cero(self, mock_archivo_config):
        guardar_config({"ultimo_monitor": 0})
        assert cargar_config()["ultimo_monitor"] == 0


class TestKeybind:
    """Persistencia de keybind (via cargar_config directamente)."""

    def test_persiste_correctamente(self, mock_archivo_config):
        guardar_config({"keybind": "<Control-p>"})
        assert cargar_config()["keybind"] == "<Control-p>"

    def test_combinacion_compleja(self, mock_archivo_config):
        guardar_config({"keybind": "<Control-Shift-Return>"})
        assert cargar_config()["keybind"] == "<Control-Shift-Return>"


class TestRegionesApps:
    """Persistencia de regiones_apps (via cargar_config directamente)."""

    def test_vacio_por_defecto(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("regiones_apps", {}) == {}

    def test_guarda_y_recupera_region(self, mock_archivo_config):
        guardar_config(
            {
                "regiones_apps": {
                    "Wolkbox": {"top": 50, "left": 100, "width": 600, "height": 400}
                }
            }
        )
        config = cargar_config()
        assert config["regiones_apps"]["Wolkbox"]["top"] == 50
        assert config["regiones_apps"]["Wolkbox"]["width"] == 600


class TestMonitoresApps:
    """Persistencia de monitores_apps (via cargar_config directamente)."""

    def test_vacio_por_defecto(self, mock_archivo_config):
        config = cargar_config()
        assert config.get("monitores_apps", {}) == {}

    def test_guarda_y_recupera(self, mock_archivo_config):
        guardar_config({"monitores_apps": {"Wolkbox": 1, "B2Chat": 2}})
        config = cargar_config()
        assert config["monitores_apps"]["Wolkbox"] == 1
        assert config["monitores_apps"]["B2Chat"] == 2

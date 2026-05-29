"""
Fixtures compartidos para toda la suite de tests.
"""

import json
import os
import pickle
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

TEST_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TEST_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def temp_config_file(temp_dir):
    config_path = temp_dir / "config.json"
    config_path.write_text(json.dumps({}), encoding="utf-8")
    return config_path


@pytest.fixture
def temp_config_json(temp_config_file):
    return temp_config_file


@pytest.fixture
def mock_config_file(temp_dir):
    config_path = temp_dir / "mock_config.json"
    return config_path


@pytest.fixture
def mock_archivo_config(monkeypatch, mock_config_file):
    from config import configuracion

    monkeypatch.setattr(configuracion, "ARCHIVO_CONFIG", str(mock_config_file))
    configuracion._invalidar_cache_config()
    return mock_config_file


@pytest.fixture
def config_con_datos_completos(mock_archivo_config):
    from config.configuracion import guardar_config

    datos = {
        "tema": "light",
        "ultimo_monitor": 2,
        "regiones_apps": {
            "Wolkbox": {"top": 100, "left": 0, "width": 800, "height": 600},
            "B2Chat": {"top": 200, "left": 100, "width": 900, "height": 500},
        },
        "monitores_apps": {"Wolkbox": 1, "B2Chat": 2},
        "perfiles_region": {
            "Perfil A": {
                "top": 100,
                "left": 200,
                "width": 1920,
                "height": 1080,
                "monitor_index": 1,
            },
            "Perfil B": {
                "top": 50,
                "left": 100,
                "width": 1280,
                "height": 720,
            },
        },
        "keybind": "<Control-Shift-x>",
        "headless": True,
        "chrome_existente": False,
        "destino_subida": "HUBSPOT",
        "auto_submit_nota": True,
    }
    guardar_config(datos)
    return datos


@pytest.fixture
def mock_keyring():
    with patch("config.credenciales.keyring") as mock:
        store = {}

        def set_password(app, key, value):
            store[f"{app}/{key}"] = value

        def get_password(app, key):
            return store.get(f"{app}/{key}")

        def delete_password(app, key):
            store.pop(f"{app}/{key}", None)

        mock.set_password.side_effect = set_password
        mock.get_password.side_effect = get_password
        mock.delete_password.side_effect = delete_password

        yield mock


@pytest.fixture
def mock_cookies_dir(temp_dir):
    cookies_dir = temp_dir / "cookies"
    cookies_dir.mkdir(exist_ok=True)
    with patch("config.credenciales.Path") as mock_path:

        def path_side_effect(path_str):
            if path_str.startswith("cookies/"):
                return temp_dir / path_str
            return Path(path_str)

        mock_path.side_effect = path_side_effect
        yield cookies_dir


@pytest.fixture
def mock_keyring_empty(mock_keyring):
    return mock_keyring


@pytest.fixture
def temp_plantillas_file(temp_dir):
    plantillas_path = temp_dir / "plantillas.json"
    return plantillas_path


@pytest.fixture
def mock_plantillas_path(monkeypatch, temp_plantillas_file):
    import ui.ventana_plantillas as vp

    monkeypatch.setattr(vp, "PLANTILLAS_PATH", temp_plantillas_file)
    return temp_plantillas_file


@pytest.fixture
def datos_hubspot_mock():
    return {
        "fsd": "FSD-980124",
        "ticket_id": "12345",
        "contact_id": "67890",
        "nombre": "Juan Perez",
        "id_cliente": "GZ-001",
        "direccion": "Calle 123 #45-67",
        "telefono": "787-297-9317",
        "telefono_alterno": "787-111-2222",
        "email": "juan@example.com",
        "estado": "Puerto Rico",
        "municipio": "San Juan",
        "zip": "00901",
        "nota": "Cliente VIP",
        "fuente_nombre": "HubSpot Ticket",
        "fuente_id": "ticket-12345",
        "error": None,
    }


@pytest.fixture
def datos_sunrun_mock():
    return {
        "fsd": "FSD-980124",
        "nombre": "Juan Perez Garcia",
        "id_cliente": "GZ-001",
        "direccion": "Calle 123 #45-67",
        "telefono": "+17872979317",
        "telefono_movil": "787-111-2222",
        "email": "juan@example.com",
        "estado_pr": "Puerto Rico",
        "condado": "San Juan",
        "ciudad": "San Juan",
        "codigo_postal": "00901",
        "dispatch_state": "En Progreso",
        "appointment_date": "2025-06-15",
        "case_reason": "Instalación",
        "error": None,
    }


@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.get_cookies.return_value = [
        {"name": "session", "value": "abc123", "domain": ".example.com"},
        {"name": "token", "value": "xyz789", "domain": ".example.com"},
    ]
    return driver
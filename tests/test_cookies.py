"""
Tests de cookies de sesion (pickle).

Cubre:
  - guardar_cookies
  - cargar_cookies (archivo existe y no existe)
  - Estructura de los datos guardados
"""

import pickle
import pytest
from unittest.mock import MagicMock, patch

from config.credenciales import guardar_cookies, cargar_cookies


@pytest.fixture
def temp_cwd(temp_dir, monkeypatch):
    """Cambia al directorio temporal para tests de cookies."""
    monkeypatch.chdir(str(temp_dir))
    return temp_dir


class TestGuardarCookies:
    def test_guarda_cookies_en_directorio_cookies(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "HUBSPOT", carpeta=carpeta)
        archivo = carpeta / "HUBSPOT.pkl"
        assert archivo.exists()
        cookies = pickle.loads(archivo.read_bytes())
        assert len(cookies) == 2
        assert cookies[0]["name"] == "session"
        assert cookies[1]["name"] == "token"

    def test_reemplaza_espacios_por_guiones(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "Mi Sitio", carpeta=carpeta)
        archivo = carpeta / "Mi_Sitio.pkl"
        assert archivo.exists()

    def test_crea_directorio_cookies_si_no_existe(self, temp_cwd, mock_driver):
        carpeta = temp_cwd / "cookies"
        guardar_cookies(mock_driver, "TEST", carpeta=carpeta)
        assert carpeta.is_dir()

    def test_guarda_cookies_vacio(self, temp_cwd):
        driver = MagicMock()
        driver.get_cookies.return_value = []
        carpeta = temp_cwd / "cookies"
        guardar_cookies(driver, "VACIO", carpeta=carpeta)
        archivo = carpeta / "VACIO.pkl"
        cookies = pickle.loads(archivo.read_bytes())
        assert cookies == []


class TestCargarCookies:
    def test_archivo_no_existe_devuelve_false(self, temp_cwd):
        driver = MagicMock()
        sitio = {"nombre": "NOEXISTE"}
        carpeta = temp_cwd / "cookies"
        resultado = cargar_cookies(driver, sitio, "https://example.com", carpeta=carpeta)
        assert resultado is False

    def test_carga_cookies_exitosamente(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        carpeta.mkdir(exist_ok=True)
        cookies_guardadas = [
            {"name": "session", "value": "abc123", "domain": "example.com"},
            {"name": "token", "value": "xyz", "domain": "example.com"},
        ]
        (carpeta / "HUBSPOT.pkl").write_bytes(
            pickle.dumps(cookies_guardadas)
        )

        driver = MagicMock()
        sitio = {"nombre": "HUBSPOT"}

        resultado = cargar_cookies(driver, sitio, "https://app.hubspot.com", carpeta=carpeta)
        assert resultado is True
        driver.get.assert_called_once_with("https://app.hubspot.com")
        assert driver.add_cookie.call_count == 2

    def test_carga_cookies_con_errores_individuales_no_detiene(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        carpeta.mkdir(exist_ok=True)
        cookies_guardadas = [
            {"name": "ok", "value": "v1"},
            {"name": "bad", "value": "v2"},
        ]
        (carpeta / "TEST.pkl").write_bytes(
            pickle.dumps(cookies_guardadas)
        )

        driver = MagicMock()
        driver.add_cookie.side_effect = [None, Exception("cookie rechazada")]

        sitio = {"nombre": "TEST"}

        resultado = cargar_cookies(driver, sitio, "https://example.com", carpeta=carpeta)
        assert resultado is True


class TestRoundTripCookies:
    """Flujo completo: guardar -> cargar."""

    def test_guardar_y_cargar_cookies(self, temp_cwd):
        carpeta = temp_cwd / "cookies"
        driver_save = MagicMock()
        cookies_originales = [
            {"name": "s", "value": "abc", "domain": ".site.com"},
        ]
        driver_save.get_cookies.return_value = cookies_originales

        guardar_cookies(driver_save, "TEST", carpeta=carpeta)

        driver_load = MagicMock()
        sitio = {"nombre": "TEST"}
        resultado = cargar_cookies(driver_load, sitio, "https://site.com", carpeta=carpeta)

        assert resultado is True
        driver_load.get.assert_called_once()
        driver_load.add_cookie.assert_called()

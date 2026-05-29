"""
Tests de gestion de credenciales (keyring).

Cubre:
  - guardar_credenciales → cargar_credenciales round-trip
  - borrar_credenciales
  - Cargar credenciales que no existen devuelve strings vacios
  - Multiples sitios independientes
"""

import pytest

from config.credenciales import (
    borrar_credenciales,
    cargar_credenciales,
    guardar_credenciales,
)


class TestGuardarCredenciales:
    def test_guardar_y_cargar_credenciales(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "secret123")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "admin"
        assert clave == "secret123"

    def test_guardar_vacio_funciona(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "", "")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == ""
        assert clave == ""

    def test_guardar_con_caracteres_especiales(self, mock_keyring):
        guardar_credenciales("SUNRUN", "user@domain", "p@$$w0rd!#")
        usuario, clave = cargar_credenciales("SUNRUN")
        assert usuario == "user@domain"
        assert clave == "p@$$w0rd!#"


class TestCargarCredenciales:
    def test_credenciales_inexistentes_devuelve_vacios(self, mock_keyring):
        usuario, clave = cargar_credenciales("NOEXISTE")
        assert usuario == ""
        assert clave == ""

    def test_credenciales_inexistentes_no_son_none(self, mock_keyring):
        usuario, clave = cargar_credenciales("NOEXISTE")
        assert usuario is not None
        assert clave is not None

    def test_credenciales_parciales(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "user", "")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "user"
        assert clave == ""


class TestBorrarCredenciales:
    def test_borrar_credenciales_existentes(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "admin", "pass")
        borrar_credenciales("HUBSPOT")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == ""
        assert clave == ""

    def test_borrar_credenciales_inexistentes_no_falla(self, mock_keyring):
        borrar_credenciales("NOEXISTE")

    def test_borrar_y_volver_a_guardar(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "user1", "pass1")
        borrar_credenciales("HUBSPOT")
        guardar_credenciales("HUBSPOT", "user2", "pass2")
        usuario, clave = cargar_credenciales("HUBSPOT")
        assert usuario == "user2"
        assert clave == "pass2"


class TestMultiplesSitios:
    def test_sitios_independientes(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "hs_user", "hs_pass")
        guardar_credenciales("SUNRUN", "sr_user", "sr_pass")

        u1, c1 = cargar_credenciales("HUBSPOT")
        u2, c2 = cargar_credenciales("SUNRUN")

        assert u1 == "hs_user"
        assert c1 == "hs_pass"
        assert u2 == "sr_user"
        assert c2 == "sr_pass"

    def test_borrar_un_sitio_no_afecta_otro(self, mock_keyring):
        guardar_credenciales("HUBSPOT", "hs", "p1")
        guardar_credenciales("SUNRUN", "sr", "p2")
        borrar_credenciales("HUBSPOT")
        u, c = cargar_credenciales("SUNRUN")
        assert u == "sr"
        assert c == "p2"


class TestRoundTripCredenciales:
    """Flujos completos de guardado/carga/borrado."""

    def test_guardar_cargar_borrar_cargar(self, mock_keyring):
        guardar_credenciales("SITIO", "u", "p")
        assert cargar_credenciales("SITIO") == ("u", "p")
        borrar_credenciales("SITIO")
        assert cargar_credenciales("SITIO") == ("", "")

    def test_sobreescribir_credenciales(self, mock_keyring):
        guardar_credenciales("SITIO", "old_user", "old_pass")
        guardar_credenciales("SITIO", "new_user", "new_pass")
        assert cargar_credenciales("SITIO") == ("new_user", "new_pass")

    def test_guardar_credenciales_usa_keyring_app_correcto(self, mock_keyring):
        guardar_credenciales("X", "u", "p")
        mock_keyring.set_password.assert_any_call("AutoCapturaApp", "X_usuario", "u")
        mock_keyring.set_password.assert_any_call("AutoCapturaApp", "X_clave", "p")

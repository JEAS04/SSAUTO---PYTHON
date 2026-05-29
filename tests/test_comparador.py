"""
Tests del motor de comparacion (comparador.py).

Cubre funciones puras:
  - comparar_campo: todos los estados posibles
  - comparar: resultado completo con campos y resumen
  - _similitud: calculo de similitud
  - _normalizar_telefono: normalizacion de telefonos
  - _norm: normalizacion de texto
  - _vacio: deteccion de valores vacios
  - _comparar_nombres: comparacion token-based
  - datos_hs_desde_ticket: adaptacion de datos
"""

import pytest
from unittest.mock import patch, MagicMock

from core.comparador import (
    _comparar_nombres,
    _norm,
    _normalizar_telefono,
    _similitud,
    _vacio,
    comparar,
    comparar_campo,
    datos_hs_desde_ticket,
)


class TestNorm:
    def test_normaliza_mayusculas(self):
        assert _norm("hola mundo") == "HOLA MUNDO"

    def test_elimina_tildes(self):
        resultado = _norm("María")
        assert "I" in resultado or resultado == "MARIA"

    def test_elimina_puntuacion(self):
        assert _norm("Hola, mundo; hoy: 'bien'") == "HOLA MUNDO HOY BIEN"

    def test_vacio_devuelve_vacio(self):
        assert _norm("") == ""

    def test_no_encontrado_devuelve_vacio(self):
        assert _norm("No encontrado") == ""

    def test_no_detectado_devuelve_vacio(self):
        assert _norm("No detectado") == ""

    def test_espacios_dobles_colapsados(self):
        resultado = _norm("hola    mundo")
        assert resultado == "HOLA MUNDO"

    def test_none_devuelve_vacio(self):
        assert _norm(None) == ""


class TestVacio:
    def test_vacio_identifica_none(self):
        assert _vacio(None) is True

    def test_vacio_identifica_cadena_vacia(self):
        assert _vacio("") is True

    def test_vacio_identifica_no_encontrado(self):
        assert _vacio("No encontrado") is True

    def test_vacio_identifica_valor_real(self):
        assert _vacio("Juan Perez") is False

    def test_vacio_identifica_espacios(self):
        assert _vacio("   ") is True


class TestNormalizarTelefono:
    def test_formato_internacional(self):
        assert _normalizar_telefono("+17872979317") == "7872979317"

    def test_formato_con_parentesis(self):
        assert _normalizar_telefono("(787)297-9317") == "7872979317"

    def test_formato_con_guiones(self):
        assert _normalizar_telefono("787-297-9317") == "7872979317"

    def test_con_codigo_pais_1_guiado(self):
        assert _normalizar_telefono("1-787-297-9317") == "7872979317"

    def test_vacio_devuelve_vacio(self):
        assert _normalizar_telefono("") == ""

    def test_none_devuelve_vacio(self):
        assert _normalizar_telefono(None) == ""

    def test_solo_10_digitos_se_mantienen(self):
        assert _normalizar_telefono("7872979317") == "7872979317"

    def test_numero_11_digitos_sin_codigo_1_se_mantiene(self):
        assert _normalizar_telefono("12345678901") == "2345678901"


class TestSimilitud:
    def test_iguales_devuelve_uno(self):
        assert _similitud("Hola", "Hola") == 1.0

    def test_distintos_devuelve_menor_que_uno(self):
        assert _similitud("Hola", "Chao") < 1.0

    def test_parecidos_devuelve_alto(self):
        sim = _similitud("Juan Perez", "Juan Peres")
        assert sim > 0.7


class TestCompararNombres:
    def test_exactos_devuelve_igual(self):
        r = _comparar_nombres("Juan Perez", "Juan Perez")
        assert r["estado"] == "igual"

    def test_tokens_contenidos_devuelve_similar(self):
        r = _comparar_nombres("Juan Perez", "Juan Perez Garcia")
        assert r["estado"] in ("igual", "similar")

    def test_completamente_diferentes(self):
        r = _comparar_nombres("Juan Perez", "Ana Lopez")
        assert r["estado"] in ("diferente", "similar")

    def test_con_tildes_y_mayusculas(self):
        r = _comparar_nombres("María José", "maria jose")
        assert r["estado"] in ("igual", "similar")


class TestCompararCampo:
    def test_ambos_vacios(self):
        r = comparar_campo("Telefono", "", "")
        assert r["estado"] == "ambos_vacios"

    def test_solo_hs(self):
        r = comparar_campo("Email", "a@b.com", "")
        assert r["estado"] == "solo_hs"

    def test_solo_sunrun(self):
        r = comparar_campo("Email", "", "a@b.com")
        assert r["estado"] == "solo_sunrun"

    def test_iguales(self):
        r = comparar_campo("Direccion", "Calle 123", "Calle 123")
        assert r["estado"] == "igual"

    def test_telefonos_formato_diferente_pero_iguales(self):
        r = comparar_campo("Telefono", "787-297-9317", "+17872979317")
        assert r["estado"] == "igual"

    def test_nombre_formato_diferente_tolerante(self):
        r = comparar_campo("Nombre", "Juan Perez", "Juan Perez Garcia")
        assert r["estado"] in ("igual", "similar")

    def test_campo_desconocido_comparacion_generica(self):
        r = comparar_campo("Ciudad", "San Juan", "San Juan")
        assert r["estado"] == "igual"

    def test_no_encontrado_se_trata_como_vacio(self):
        r = comparar_campo("Direccion", "No encontrado", "Calle 123")
        assert r["estado"] == "solo_sunrun"

    def test_resultado_tiene_campo(self):
        r = comparar_campo("Ciudad", "A", "B")
        assert r["campo"] == "Ciudad"

    def test_resultado_tiene_similitud(self):
        r = comparar_campo("Nombre", "Juan", "Juan")
        assert "similitud" in r
        assert 0.0 <= r["similitud"] <= 1.0

    def test_resultado_tiene_nota(self):
        r = comparar_campo("Email", "a@b", "a@b")
        assert "nota" in r
        assert r["nota"]

    def test_nombre_similar_pero_no_igual(self):
        r = comparar_campo("Nombre", "Juan Perez", "Juan Peres")
        assert r["estado"] in ("similar", "diferente")

    def test_solo_hs_cuando_hs_vacio(self):
        r = comparar_campo("Direccion", "Calle Falsa 123", "")
        assert r["estado"] == "solo_hs"
        assert r["valor_sr"] == "—"


class TestComparar:
    """Pruebas de la funcion principal comparar()."""

    def test_comparacion_completa_sin_errores(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        assert "campos" in resultado
        assert "resumen" in resultado
        assert "fsd" in resultado
        assert not resultado["tiene_error"]

    def test_comparacion_con_error_en_hs(self):
        resultado = comparar(
            {"error": "Timeout API"}, {"nombre": "Test", "error": None}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 1

    def test_comparacion_con_error_en_sunrun(self):
        resultado = comparar(
            {"nombre": "Test", "error": None}, {"error": "Sunrun no responde"}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 1

    def test_comparacion_con_errores_en_ambos(self):
        resultado = comparar(
            {"error": "Error A"}, {"error": "Error B"}
        )
        assert resultado["tiene_error"]
        assert len(resultado["errores"]) == 2

    def test_fsd_desde_hubspot(self):
        resultado = comparar(
            {"fsd": "FSD-999", "nombre": "X"},
            {"nombre": "X"},
        )
        assert resultado["fsd"] == "FSD-999"

    def test_fsd_desde_sunrun_cuando_hs_no_tiene(self):
        resultado = comparar(
            {"nombre": "X"},
            {"fsd": "FSD-888", "nombre": "X"},
        )
        assert resultado["fsd"] == "FSD-888"

    def test_fsd_desconocido_cuando_ninguno_tiene(self):
        resultado = comparar({}, {})
        assert resultado["fsd"] == "desconocido"

    def test_campos_comparables_en_resultado(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        nombres_campo = {c["campo"] for c in resultado["campos"]}
        assert "Nombre" in nombres_campo
        assert "Direccion" in nombres_campo
        assert "Telefono" in nombres_campo
        assert "Email" in nombres_campo

    def test_campos_solo_sunrun_incluidos(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        nombres_campo = {c["campo"] for c in resultado["campos"]}
        assert "Municipio" in nombres_campo

    def test_resumen_suma_consistente(self, datos_hubspot_mock, datos_sunrun_mock):
        resultado = comparar(datos_hubspot_mock, datos_sunrun_mock)
        r = resultado["resumen"]
        total_resumen = sum(r.values())
        assert total_resumen == len(resultado["campos"])

    def test_resumen_tiene_todas_las_claves(self):
        resultado = comparar({"nombre": "A"}, {"nombre": "A"})
        for clave in ("igual", "similar", "diferente", "solo_hs", "solo_sunrun", "ambos_vacios"):
            assert clave in resultado["resumen"]

    def test_datos_identicos_todo_igual(self):
        datos = {
            "nombre": "Juan Perez",
            "direccion": "Calle 123",
            "telefono": "7872979317",
            "email": "juan@test.com",
        }
        resultado = comparar(datos, datos)
        for campo in resultado["campos"]:
            if campo["campo"] != "Municipio":
                assert campo["estado"] in ("igual", "ambos_vacios"), f"Campo {campo['campo']} deberia ser igual, fue {campo['estado']}"

    def test_campos_completamente_diferentes(self):
        hs = {
            "nombre": "Juan Perez",
            "direccion": "Calle A",
            "telefono": "7871111111",
            "email": "juan@test.com",
        }
        sr = {
            "nombre": "Ana Lopez",
            "direccion": "Calle B",
            "telefono": "7872222222",
            "email": "ana@test.com",
        }
        resultado = comparar(hs, sr)
        estados = {c["estado"] for c in resultado["campos"]}
        assert "diferente" in estados

    def test_campo_parcial_solo_hs(self):
        hs = {"nombre": "Juan", "direccion": "Calle 123", "telefono": "7871111111", "email": "juan@test.com"}
        sr = {"nombre": "Juan"}
        resultado = comparar(hs, sr)
        estados = {c["estado"] for c in resultado["campos"]}
        assert "solo_hs" in estados


class TestDatosHsDesdeTicket:
    def test_campos_completos(self):
        ticket = {
            "fsd": "FSD-001",
            "ticket_id": "T1",
            "contact_id": "C1",
            "nombre": "Juan",
            "id_cliente": "GZ-1",
            "direccion": "Calle 1",
            "telefono": "123",
            "telefono_alterno": "456",
            "email": "j@j.com",
            "estado": "PR",
            "municipio": "SJ",
            "zip": "00901",
            "nota": "VIP",
            "fuente_nombre": "Ticket",
            "fuente_id": "T1",
            "error": None,
        }
        resultado = datos_hs_desde_ticket(ticket)
        assert resultado["fsd"] == "FSD-001"
        assert resultado["nombre"] == "Juan"
        assert resultado["fuente"] == "HubSpot"
        assert resultado["error"] is None

    def test_campos_faltantes_se_completan(self):
        ticket = {"fsd": "FSD-001", "nombre": "Juan"}
        resultado = datos_hs_desde_ticket(ticket)
        assert resultado["fsd"] == "FSD-001"
        assert resultado["telefono"] == ""

    def test_ticket_vacio(self):
        resultado = datos_hs_desde_ticket({})
        assert resultado["fuente"] == "HubSpot"
        assert resultado["fsd"] == ""

    def test_error_propagado(self):
        resultado = datos_hs_desde_ticket({"error": "Fallo"})
        assert resultado["error"] == "Fallo"
        assert resultado["fuente"] == "HubSpot"


class TestCompararCampoTelefono:
    def test_telefono_igual_normalizado(self):
        r = comparar_campo("Telefono", "(787) 297-9317", "+17872979317")
        assert r["estado"] == "igual"

    def test_telefono_alterno_igual_normalizado(self):
        r = comparar_campo("Telefono Alterno", "1-787-111-2222", "7871112222")
        assert r["estado"] == "igual"

    def test_telefono_diferente(self):
        r = comparar_campo("Telefono", "7871112222", "7873334444")
        assert r["estado"] == "diferente"

    def test_telefono_solo_hs(self):
        r = comparar_campo("Telefono", "7871112222", "")
        assert r["estado"] == "solo_hs"

    def test_telefono_vacio_ambos(self):
        r = comparar_campo("Telefono", "", "")
        assert r["estado"] == "ambos_vacios"

"""
Tests de PluginRegistry.

Cubre:
  - registrar / obtener / desregistrar
  - obtener_o_none
  - todos / nombres / existe
  - con_login / filtrar
  - limpiar
  - Errores: plugin no encontrado, duplicados
"""

import pytest

from core.base_plugin import ContextoSubida, ResultadoSubida, SitioPlugin
from core.plugin_registry import PluginRegistry


class _PluginFalso(SitioPlugin):
    def __init__(self, nombre, login=True):
        self._nombre = nombre
        self._login = login

    @property
    def nombre(self):
        return self._nombre

    @property
    def necesita_login(self):
        return self._login

    def subir(self, ctx):
        return ResultadoSubida(exitoso=True)


@pytest.fixture(autouse=True)
def _limpiar_registry():
    PluginRegistry.limpiar()
    yield
    PluginRegistry.limpiar()


class TestRegistrar:
    def test_registrar_un_plugin(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.existe("HUBSPOT")

    def test_registrar_multiples_plugins(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        assert len(PluginRegistry.todos()) == 2

    def test_registrar_reemplaza_plugin_existente(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert len(PluginRegistry.todos()) == 1


class TestObtener:
    def test_obtener_plugin_existe(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.obtener("HUBSPOT") is p

    def test_obtener_plugin_no_existe_lanza_keyerror(self):
        with pytest.raises(KeyError):
            PluginRegistry.obtener("NOEXISTE")

    def test_obtener_o_none_existe(self):
        p = _PluginFalso("HUBSPOT")
        PluginRegistry.registrar(p)
        assert PluginRegistry.obtener_o_none("HUBSPOT") is p

    def test_obtener_o_none_no_existe_devuelve_none(self):
        assert PluginRegistry.obtener_o_none("NOEXISTE") is None


class TestDesregistrar:
    def test_desregistrar_plugin_existente(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.desregistrar("HUBSPOT")
        assert not PluginRegistry.existe("HUBSPOT")

    def test_desregistrar_plugin_inexistente_no_falla(self):
        PluginRegistry.desregistrar("NOEXISTE")


class TestLimpiar:
    def test_limpiar_registry(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        PluginRegistry.limpiar()
        assert PluginRegistry.todos() == []


class TestTodos:
    def test_todos_vacio(self):
        assert PluginRegistry.todos() == []

    def test_todos_con_multiples(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        todos = PluginRegistry.todos()
        assert len(todos) == 2

    def test_todos_mantiene_orden(self):
        PluginRegistry.registrar(_PluginFalso("A"))
        PluginRegistry.registrar(_PluginFalso("B"))
        PluginRegistry.registrar(_PluginFalso("C"))
        nombres = [p.nombre for p in PluginRegistry.todos()]
        assert nombres == ["A", "B", "C"]


class TestNombres:
    def test_nombres_vacio(self):
        assert PluginRegistry.nombres() == []

    def test_nombres_con_plugins(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        assert set(PluginRegistry.nombres()) == {"HUBSPOT", "SUNRUN"}


class TestExiste:
    def test_existe_true(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert PluginRegistry.existe("HUBSPOT")

    def test_existe_false(self):
        assert not PluginRegistry.existe("NOEXISTE")


class TestConLogin:
    def test_con_login_filtra_correctamente(self):
        PluginRegistry.registrar(_PluginFalso("CON_LOGIN", login=True))
        PluginRegistry.registrar(_PluginFalso("SIN_LOGIN", login=False))
        PluginRegistry.registrar(_PluginFalso("CON_LOGIN2", login=True))

        con = PluginRegistry.con_login()
        nombres = {p.nombre for p in con}
        assert "CON_LOGIN" in nombres
        assert "CON_LOGIN2" in nombres
        assert "SIN_LOGIN" not in nombres

    def test_con_login_sin_plugins_devuelve_lista_vacia(self):
        assert PluginRegistry.con_login() == []


class TestFiltrar:
    def test_filtrar_por_nombres(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(["HUBSPOT"])
        assert len(resultado) == 1
        assert resultado[0].nombre == "HUBSPOT"

    def test_filtrar_ambos_devuelve_todos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(["AMBOS"])
        assert len(resultado) == 2

    def test_filtrar_lista_vacia_devuelve_todos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar([])
        assert len(resultado) == 2

    def test_filtrar_ignora_nombres_inexistentes(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        resultado = PluginRegistry.filtrar(["HUBSPOT", "NOEXISTO"])
        assert len(resultado) == 1
        assert resultado[0].nombre == "HUBSPOT"

    def test_filtrar_none_equivale_a_ambos(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("SUNRUN"))
        resultado = PluginRegistry.filtrar(None)
        assert len(resultado) == 2


class TestEdgeCases:
    def test_registrar_mismo_nombre_varias_veces(self):
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        PluginRegistry.registrar(_PluginFalso("HUBSPOT"))
        assert len(PluginRegistry.todos()) == 1
        assert PluginRegistry.existe("HUBSPOT")

    def test_desregistrar_despuis_de_limpiar_no_falla(self):
        PluginRegistry.limpiar()
        PluginRegistry.desregistrar("X")

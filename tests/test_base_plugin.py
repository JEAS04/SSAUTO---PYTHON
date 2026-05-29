"""
Tests de base_plugin: dataclasses y ABC.

Cubre:
  - RegionCaptura: creacion, as_dict
  - ResultadoSubida: creacion, valores por defecto
  - ContextoSubida: creacion, campos opcionales
  - SitioPlugin ABC: herencia, propiedades abstractas, metodos con default
"""

import pytest
from unittest.mock import MagicMock

from core.base_plugin import (
    ContextoSubida,
    RegionCaptura,
    ResultadoSubida,
    SitioPlugin,
)


class TestRegionCaptura:
    def test_creacion_basica(self):
        r = RegionCaptura(top=100, left=200, width=800, height=600)
        assert r.top == 100
        assert r.left == 200
        assert r.width == 800
        assert r.height == 600

    def test_as_dict(self):
        r = RegionCaptura(top=10, left=20, width=30, height=40)
        d = r.as_dict()
        assert d == {"top": 10, "left": 20, "width": 30, "height": 40}

    def test_as_dict_retorna_copia_segura(self):
        r = RegionCaptura(1, 2, 3, 4)
        d = r.as_dict()
        d["top"] = 999
        assert r.top == 1

    def test_valores_cero_son_validos(self):
        r = RegionCaptura(0, 0, 0, 0)
        assert r.as_dict() == {"top": 0, "left": 0, "width": 0, "height": 0}

    def test_valores_negativos_permitidos(self):
        r = RegionCaptura(top=-1, left=-1, width=100, height=100)
        assert r.as_dict() == {"top": -1, "left": -1, "width": 100, "height": 100}


class TestResultadoSubida:
    def test_exitoso_sin_mensaje(self):
        r = ResultadoSubida(exitoso=True)
        assert r.exitoso is True
        assert r.mensaje == ""
        assert r.detalle == ""

    def test_fallido_con_mensaje(self):
        r = ResultadoSubida(exitoso=False, mensaje="Error", detalle="Timeout")
        assert r.exitoso is False
        assert r.mensaje == "Error"
        assert r.detalle == "Timeout"

    def test_mensaje_y_detalle_opcionales(self):
        r = ResultadoSubida(exitoso=True)
        assert r.mensaje == ""
        assert r.detalle == ""


class TestContextoSubida:
    def test_creacion_minima(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/test.png",
            log=print,
            driver=MagicMock(),
        )
        assert ctx.ruta_imagen == "/tmp/test.png"
        assert ctx.log is print
        assert ctx.credenciales == {}
        assert ctx.opciones == {}
        assert ctx.fsd is None

    def test_con_credenciales(self):
        creds = {"usuario": "admin", "clave": "pass"}
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            credenciales=creds,
        )
        assert ctx.credenciales == creds

    def test_con_opciones(self):
        opts = {"auto_submit_nota": True}
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            opciones=opts,
        )
        assert ctx.opciones["auto_submit_nota"] is True

    def test_con_fsd(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
            fsd="FSD-123456",
        )
        assert ctx.fsd == "FSD-123456"

    def test_fsd_none_por_defecto(self):
        ctx = ContextoSubida(
            ruta_imagen="/tmp/x.png",
            log=print,
            driver=MagicMock(),
        )
        assert ctx.fsd is None

    def test_credenciales_no_se_comparten_entre_instancias(self):
        ctx1 = ContextoSubida(ruta_imagen="/tmp/a.png", log=print, driver=MagicMock())
        ctx2 = ContextoSubida(ruta_imagen="/tmp/b.png", log=print, driver=MagicMock())
        ctx1.credenciales["user"] = "x"
        assert "user" not in ctx2.credenciales

    def test_opciones_no_se_comparten_entre_instancias(self):
        ctx1 = ContextoSubida(ruta_imagen="/tmp/a.png", log=print, driver=MagicMock())
        ctx2 = ContextoSubida(ruta_imagen="/tmp/b.png", log=print, driver=MagicMock())
        ctx1.opciones["flag"] = True
        assert "flag" not in ctx2.opciones


class TestSitioPlugin:
    def test_no_se_puede_instanciar_directamente(self):
        with pytest.raises(TypeError):
            SitioPlugin()

    def test_subclase_minima_funciona(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "TEST"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.nombre == "TEST"
        assert plugin.necesita_login is True
        assert plugin.usar_pagina_actual is False
        assert plugin.dominio == ""

    def test_subclase_override_propiedades(self):
        class SinLoginPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "PUBLICO"

            @property
            def necesita_login(self):
                return False

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = SinLoginPlugin()
        assert plugin.necesita_login is False

    def test_verificar_sesion_default_true(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "T"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.verificar_sesion(MagicMock(), print) is True

    def test_hacer_login_default_false(self):
        driver = MagicMock()
        log_calls = []

        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "T"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        assert plugin.hacer_login(driver, {}, log_calls.append) is False
        assert len(log_calls) > 0

    def test_describir(self):
        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "HUBSPOT"

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        desc = plugin.describir()
        assert "HUBSPOT" in desc
        assert "con login" in desc

    def test_describir_con_pagina_actual(self):
        class ConPaginaPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "SUNRUN"

            @property
            def usar_pagina_actual(self):
                return True

            def subir(self, ctx):
                return ResultadoSubida(exitoso=True)

        plugin = ConPaginaPlugin()
        desc = plugin.describir()
        assert "página actual" in desc

    def test_plugin_recibe_contexto_completo(self):
        ctx_recibido = []

        class MiPlugin(SitioPlugin):
            @property
            def nombre(self):
                return "CAPTURE"

            def subir(self, ctx):
                ctx_recibido.append(ctx)
                return ResultadoSubida(exitoso=True)

        plugin = MiPlugin()
        ctx = ContextoSubida(
            ruta_imagen="/tmp/img.png",
            log=print,
            driver=MagicMock(),
            credenciales={"u": "p"},
            fsd="FSD-001",
        )
        resultado = plugin.subir(ctx)
        assert resultado.exitoso is True
        assert len(ctx_recibido) == 1
        assert ctx_recibido[0].fsd == "FSD-001"

"""
core/plugin_registry.py — Registro central de plugins de sitios.

El registro es el único lugar donde el resto del sistema conoce qué sitios
existen. La UI, los servicios y la configuración no importan los plugins
directamente — los piden al registro por nombre o los listan todos.

Uso en main.py:
    from plugins.hubspot import HubSpotPlugin
    from plugins.sunrun import SunrunPlugin
    from core.plugin_registry import PluginRegistry

    PluginRegistry.registrar(HubSpotPlugin())
    PluginRegistry.registrar(SunrunPlugin())

Uso en servicios/UI:
    todos = PluginRegistry.todos()
    hs = PluginRegistry.obtener("HUBSPOT")
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.base_plugin import SitioPlugin


class PluginRegistry:
    """
    Registro estático (clase, no instancia) de plugins de sitios.

    Diseño intencional: estático para que cualquier módulo pueda consultarlo
    sin necesitar una referencia a un objeto central. Los plugins se registran
    una sola vez al arrancar la app en main.py.
    """

    _plugins: dict[str, "SitioPlugin"] = {}

    # ── Registro ──────────────────────────────────────────────────────

    @classmethod
    def registrar(cls, plugin: "SitioPlugin") -> None:
        """
        Registra un plugin. Si ya existe un plugin con ese nombre, lo reemplaza.

        Llamar en main.py al arrancar, antes de construir la UI.
        """
        cls._plugins[plugin.nombre] = plugin

    @classmethod
    def desregistrar(cls, nombre: str) -> None:
        """Elimina un plugin del registro (útil en tests)."""
        cls._plugins.pop(nombre, None)

    @classmethod
    def limpiar(cls) -> None:
        """Elimina todos los plugins (útil en tests)."""
        cls._plugins.clear()

    # ── Consultas ─────────────────────────────────────────────────────

    @classmethod
    def obtener(cls, nombre: str) -> "SitioPlugin":
        """
        Devuelve el plugin por nombre exacto.

        Lanza KeyError si no existe — error temprano mejor que silencioso.
        """
        if nombre not in cls._plugins:
            disponibles = list(cls._plugins.keys())
            raise KeyError(
                f"Plugin '{nombre}' no registrado. "
                f"Disponibles: {disponibles}"
            )
        return cls._plugins[nombre]

    @classmethod
    def obtener_o_none(cls, nombre: str) -> "SitioPlugin | None":
        """Versión segura de obtener() que devuelve None si no existe."""
        return cls._plugins.get(nombre)

    @classmethod
    def todos(cls) -> list["SitioPlugin"]:
        """Lista de todos los plugins registrados, en orden de registro."""
        return list(cls._plugins.values())

    @classmethod
    def nombres(cls) -> list[str]:
        """Lista de nombres de todos los plugins registrados."""
        return list(cls._plugins.keys())

    @classmethod
    def existe(cls, nombre: str) -> bool:
        return nombre in cls._plugins

    # ── Filtros útiles ────────────────────────────────────────────────

    @classmethod
    def con_login(cls) -> list["SitioPlugin"]:
        """Plugins que requieren autenticación."""
        return [p for p in cls.todos() if p.necesita_login]

    @classmethod
    def filtrar(cls, nombres: list[str]) -> list["SitioPlugin"]:
        """
        Devuelve los plugins cuyos nombres están en la lista.
        Útil cuando el usuario elige "HUBSPOT" o "AMBOS" en la UI.
        """
        if not nombres or nombres == ["AMBOS"]:
            return cls.todos()
        return [cls._plugins[n] for n in nombres if n in cls._plugins]

    # ── Debug ─────────────────────────────────────────────────────────

    @classmethod
    def __repr__(cls) -> str:
        plugins = [p.describir() for p in cls.todos()]
        return f"PluginRegistry({plugins})"
"""
core/base_plugin.py — Contrato (ABC) que todo sitio debe cumplir.

Para agregar un sitio nuevo al proyecto:
  1. Crear plugins/mi_sitio.py con una clase que herede de SitioPlugin.
  2. Implementar los métodos abstractos.
  3. Registrarlo en main.py con PluginRegistry.registrar(MiSitioPlugin()).

Eso es todo. No hay que tocar configuracion.py, automatizacion.py ni la UI.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

# ── Tipos compartidos ─────────────────────────────────────────────────


@dataclass
class RegionCaptura:
    top: int
    left: int
    width: int
    height: int

    def as_dict(self) -> dict:
        return {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }


@dataclass
class ResultadoSubida:
    """Resultado estructurado que cada plugin devuelve tras intentar subir."""

    exitoso: bool
    mensaje: str = ""
    detalle: str = ""


@dataclass
class ContextoSubida:
    """
    Todo lo que un plugin necesita para ejecutar la subida.

    Se construye en el servicio y se pasa al plugin — el plugin no toca
    la UI ni la configuración global.
    """

    ruta_imagen: str
    log: Callable[[str], None]
    driver: object  # WebDriver (tipado débil para no forzar selenium aquí)
    credenciales: dict = field(default_factory=dict)  # {"usuario": ..., "clave": ...}
    opciones: dict = field(
        default_factory=dict
    )  # flags extra por sitio (auto_submit, etc.)
    fsd: str | None = None  # FSD para búsqueda inteligente de pestaña


# ── Contrato base ─────────────────────────────────────────────────────


class SitioPlugin(ABC):
    """
    Clase base para todos los sitios de destino.

    Cada plugin encapsula:
      - Nombre y metadatos del sitio.
      - URLs y selectores CSS/XPath (como atributos de clase, no en config global).
      - Lógica de verificación de sesión.
      - Lógica de subida de archivos.

    Los plugins NO importan nada de CustomTkinter ni de la UI.
    Los plugins NO leen config.json directamente.
    Los plugins reciben todo lo que necesitan a través de ContextoSubida.
    """

    # ── Metadatos (override en la subclase) ───────────────────────────

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Identificador único del sitio. Ej: "HUBSPOT", "SUNRUN"."""
        ...

    @property
    def necesita_login(self) -> bool:
        """True si el sitio requiere autenticación. Override si no necesita."""
        return True

    @property
    def usar_pagina_actual(self) -> bool:
        """
        True si el plugin trabaja sobre la pestaña ya abierta por el usuario
        (sin navegar a una URL fija). Típico de HubSpot donde el usuario
        ya tiene abierto el ticket correcto.
        """
        return False

    @property
    def dominio(self) -> str:
        """
        Subcadena de la URL del sitio, usada para encontrar la pestaña
        correcta entre las abiertas en Chrome. Ej: "app.hubspot.com".
        """
        return ""

    # ── Métodos abstractos ────────────────────────────────────────────

    @abstractmethod
    def subir(self, ctx: ContextoSubida) -> ResultadoSubida:
        """
        Lógica completa de subida del archivo.

        Recibe el contexto con todo lo necesario (driver, ruta, log, etc.)
        y devuelve un ResultadoSubida con el estado final.

        El driver YA está conectado y posicionado en la pestaña correcta
        cuando este método se llama — el SesionService se encargó de eso.
        """
        ...

    # ── Métodos con implementación por defecto (override opcional) ─────

    def verificar_sesion(self, driver, log: Callable) -> bool:
        """
        Verifica si hay sesión activa en el driver para este sitio.

        Devuelve True si la sesión está activa, False si hay que hacer login.
        La implementación por defecto siempre devuelve True (útil para sitios
        donde el usuario maneja la sesión manualmente en Chrome).

        Override en plugins que puedan detectar redirección a login.
        """
        return True

    def hacer_login(self, driver, credenciales: dict, log: Callable) -> bool:
        """
        Realiza el login automático en el sitio.

        Devuelve True si el login fue exitoso.
        La implementación por defecto no hace nada (retorna False).

        Override en plugins que soporten login automático.
        """
        log(f"  ⚠ El plugin '{self.nombre}' no implementa login automático.")
        return False

    def describir(self) -> str:
        """Descripción legible del plugin para mostrar en la UI."""
        login = "con login" if self.necesita_login else "sin login"
        pagina = " · usa página actual" if self.usar_pagina_actual else ""
        return f"{self.nombre} ({login}{pagina})"

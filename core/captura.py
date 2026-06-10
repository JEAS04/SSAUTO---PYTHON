"""
core/captura.py — Captura de pantalla sin dependencias de UI.

Módulo puro: solo recibe coordenadas, toma la captura y devuelve la ruta.
No importa Tkinter ni CustomTkinter.
Testeable desde línea de comandos sin abrir ninguna ventana.

Uso:
    from core.captura import CapturaService
    ruta = CapturaService.capturar({"top": 0, "left": 0, "width": 1920, "height": 1080})
"""

from __future__ import annotations

import sys as _sys
from datetime import datetime
from pathlib import Path
from typing import Union

import mss
import mss.tools


class ErrorCaptura(Exception):
    """Error específico de captura para distinguirlo de errores genéricos."""

    pass


class CapturaService:
    """
    Servicio de captura de pantalla.

    Todos los métodos son de clase — no necesita instanciarse.
    """

    if getattr(_sys, "frozen", False):
        from utils.paths import get_writable_path
        CARPETA_CAPTURAS = Path(get_writable_path("screenshots"))
    else:
        CARPETA_CAPTURAS = Path("screenshots")

    # ── Captura principal ─────────────────────────────────────────────

    @classmethod
    def capturar(
        cls,
        region: Union[dict, "RegionCaptura"],  # type: ignore[name-defined]
        carpeta: Path | None = None,
        monitor: int = 1,  # ← solo informativo, el medidor ya da coords absolutas
    ) -> str:
        """
        Toma una captura de la región indicada y la guarda en disco.

        Parámetros
        ----------
        region  : dict con top/left/width/height en coordenadas absolutas
                  (el medidor ya las entrega así, no sumar offset de monitor).
        carpeta : dónde guardar. Por defecto: ./screenshots/
        monitor : índice del monitor (1=principal, 2=secundario, ...) — solo informativo.

        Devuelve
        --------
        str : ruta absoluta del archivo generado.

        Lanza
        ------
        ErrorCaptura si la región es inválida o falla mss.
        """
        region_dict = cls._normalizar_region(region)
        cls._validar_region(region_dict)

        destino = carpeta or cls.CARPETA_CAPTURAS
        destino.mkdir(parents=True, exist_ok=True)

        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = destino / f"captura_{marca}.png"

        try:
            with mss.MSS() as sct:
                captura = sct.grab(region_dict)
                mss.tools.to_png(captura.rgb, captura.size, output=str(ruta))
        except Exception as e:
            raise ErrorCaptura(
                f"Error al capturar región {region_dict}: {e}"
            ) from e

        return str(ruta.resolve())

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _normalizar_region(region) -> dict:
        """Acepta dict o RegionCaptura y devuelve siempre un dict con ints."""
        if hasattr(region, "as_dict"):
            region = region.as_dict()
        return {
            k: int(v)
            for k, v in region.items()
            if k in ("top", "left", "width", "height")
        }

    @staticmethod
    def _validar_region(region: dict) -> None:
        """Lanza ErrorCaptura si la región tiene valores inválidos."""
        claves = ("top", "left", "width", "height")
        faltantes = [c for c in claves if c not in region]
        if faltantes:
            raise ErrorCaptura(f"Faltan campos en la región: {faltantes}")
        if region["width"] <= 0:
            raise ErrorCaptura(f"width debe ser > 0, recibido: {region['width']}")
        if region["height"] <= 0:
            raise ErrorCaptura(f"height debe ser > 0, recibido: {region['height']}")

    @classmethod
    def listar_capturas(cls, carpeta: Path | None = None) -> list[Path]:
        """Lista todas las capturas guardadas, de más nueva a más vieja."""
        destino = carpeta or cls.CARPETA_CAPTURAS
        if not destino.exists():
            return []
        return sorted(destino.glob("captura_*.png"), reverse=True)

    @classmethod
    def limpiar_antiguas(cls, mantener: int = 50, carpeta: Path | None = None) -> int:
        """
        Borra las capturas más antiguas, manteniendo las N más recientes.
        Devuelve el número de archivos borrados.
        """
        archivos = cls.listar_capturas(carpeta)
        a_borrar = archivos[mantener:]
        for archivo in a_borrar:
            try:
                archivo.unlink()
            except Exception:
                pass
        return len(a_borrar)

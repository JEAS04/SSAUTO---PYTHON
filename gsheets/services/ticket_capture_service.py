"""
Módulo 5 — Servicio orquestador TicketCaptureService.

Flujo completo:
  1. Recibir celda objetivo (ej. "F6").
  2. Calcular las 4 referencias (parser).
  3. Obtener valores desde Google Sheets API.
  4. Capturar las 4 celdas con Playwright.
  5. Generar imagen compuesta (grilla 2x2).
  6. Retornar payload con toda la información.

Módulo 6 — Placeholder para integración con HubSpot.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys as _sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from gsheets.utils.cell_parser import parse_target_cell, CellReferences
from gsheets.data.sheets_api import GoogleSheetsClient, CellValues
from gsheets.core.playwright_capture import PlaywrightSheetsCapture
from gsheets.utils.image_compositor import compose_ticket_image

# ── Logger ────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Event loop policy para Windows (evita errores en frozen builds) ──────────
if _sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# ── Directorios por defecto ───────────────────────────────────────────────────

if getattr(_sys, "frozen", False):
    from utils.paths import get_writable_path
    _BASE_DIR = Path(get_writable_path("gsheets"))
else:
    _BASE_DIR = Path(__file__).resolve().parent.parent
_SCREENSHOTS_DIR = _BASE_DIR / "screenshots"
_SESSIONS_DIR = _BASE_DIR / "sessions"


# ── Tipos / Dataclasses ───────────────────────────────────────────────────────


@dataclass
class TicketCapturePayload:
    """Payload retornado por TicketCaptureService tras una captura exitosa."""

    cells: CellValues
    """Valores obtenidos desde Google Sheets API: {"A3": ..., "F3": ..., ...}"""

    image_path: str
    """Ruta absoluta a la imagen compuesta (ticket_capture.png)."""

    references: CellReferences
    """Referencias de celda calculadas."""

    cell_screenshots: dict[str, str]
    """Rutas de las capturas individuales: {"A3": "a3.png", ...}"""

    target_cell: str
    """Celda objetivo original (ej. "F6")."""


@dataclass
class TicketCaptureConfig:
    """Configuración para TicketCaptureService."""

    spreadsheet_id: str
    """ID del spreadsheet de Google Sheets."""

    credentials_path: str | Path = ""
    """Ruta al archivo JSON de Service Account."""

    sheet_gid: str | int = "0"
    """GID de la hoja dentro del spreadsheet."""

    sheet_name: str | None = None
    """Nombre de la hoja (opcional, para la API)."""

    headless: bool = True
    """Si True, Playwright corre en modo headless."""

    output_dir: str | Path | None = None
    """Directorio base de salida para capturas e imagen compuesta."""

    composite_filename: str = "ticket_capture.png"
    """Nombre del archivo de imagen compuesta."""


# ── Servicio orquestador ──────────────────────────────────────────────────────


class TicketCaptureService:
    """
    Servicio principal que orquesta la captura completa de un ticket.

    Uso:
        config = TicketCaptureConfig(
            spreadsheet_id="ABC123...",
            credentials_path="credenciales.json",
        )
        service = TicketCaptureService(config)
        payload = await service.capture("F6")
        # payload.cells, payload.image_path, payload.references

    También puede usarse como context manager para controlar el ciclo
    de vida de Playwright manualmente:
        async with TicketCaptureService(config) as service:
            payload = await service.capture("F6")
    """

    def __init__(
        self,
        config: TicketCaptureConfig,
        log_callback: Callable[[str], None] | None = None,
    ) -> None:
        self._config = config
        self._log = log_callback or (lambda msg: logger.info(msg))

        # Directorio de salida
        self._output_dir = (
            Path(config.output_dir) if config.output_dir else _SCREENSHOTS_DIR
        )
        self._output_dir.mkdir(parents=True, exist_ok=True)

        # Cliente de Google Sheets API
        self._sheets_client: GoogleSheetsClient | None = None
        creds_path = config.credentials_path or os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "")
        if creds_path:
            self._sheets_client = self._init_sheets_client(creds_path)

        # Playwright (se inicia bajo demanda)
        self._capture: PlaywrightSheetsCapture | None = None
        self._capture_owned = False  # True si nosotros iniciamos Playwright

    # ── Inicialización ────────────────────────────────────────────────────

    def _init_sheets_client(self, credentials_path: str | Path) -> GoogleSheetsClient:
        self._log("→ Inicializando cliente de Google Sheets API...")
        client = GoogleSheetsClient(credentials_path)
        self._log("✓ Cliente de Google Sheets API listo.")
        return client

    # ── Context manager ───────────────────────────────────────────────────

    async def __aenter__(self) -> "TicketCaptureService":
        await self._ensure_capture()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._capture and self._capture_owned:
            await self._capture.stop()
            self._capture = None
            self._capture_owned = False

    async def _ensure_capture(self) -> PlaywrightSheetsCapture:
        """Asegura que haya una instancia de PlaywrightSheetsCapture iniciada."""
        if self._capture is None:
            self._capture = PlaywrightSheetsCapture(
                headless=self._config.headless,
                session_dir=self._config.output_dir or _SESSIONS_DIR,
                screenshots_dir=self._output_dir,
                log_callback=self._log,
            )
            await self._capture.start()
            self._capture_owned = True
        return self._capture

    # ── Método principal ──────────────────────────────────────────────────

    async def capture(self, cell_ref: str) -> TicketCapturePayload:
        """
        Ejecuta el flujo completo de captura para una celda objetivo.

        Args:
            cell_ref: Referencia de celda (ej. "F6", "AA10").

        Returns:
            TicketCapturePayload con valores, imagen compuesta, y referencias.

        Raises:
            ValueError: Si la celda tiene formato inválido.
            RuntimeError: Si falla la API de Sheets, Playwright, o la composición.
        """
        self._log(f"=== INICIANDO CAPTURA PARA CELDA: {cell_ref} ===")

        # ── Paso 1: Parsear celda objetivo ──
        self._log(f"→ Paso 1/5: Parseando celda '{cell_ref}'...")
        refs_dict = parse_target_cell(cell_ref)
        references = CellReferences(
            top_left=refs_dict["top_left"],
            top_right=refs_dict["top_right"],
            bottom_left=refs_dict["bottom_left"],
            bottom_right=refs_dict["bottom_right"],
            target=cell_ref.strip().upper(),
        )
        all_refs = references.all_refs()
        self._log(
            f"✓ Referencias calculadas: {references.top_left}, "
            f"{references.top_right}, {references.bottom_left}, "
            f"{references.bottom_right}"
        )

        # ── Paso 2: Obtener valores desde Sheets API ──
        self._log("→ Paso 2/5: Leyendo valores desde Google Sheets API...")
        if self._sheets_client is None:
            raise RuntimeError(
                "Cliente de Google Sheets no configurado. "
                "Provea 'credentials_path' en TicketCaptureConfig."
            )

        spreadsheet_id = GoogleSheetsClient.extract_spreadsheet_id(
            self._config.spreadsheet_id
        )

        cell_values = self._sheets_client.read_cells(
            spreadsheet_id=spreadsheet_id,
            cell_refs=all_refs,
            sheet_name=self._config.sheet_name,
        )
        self._log(f"✓ Valores obtenidos: {cell_values}")

        # ── Paso 3: Capturar celdas con Playwright ──
        self._log("→ Paso 3/5: Capturando celdas con Playwright...")
        capture = await self._ensure_capture()

        sheet_url = (
            self._config.spreadsheet_id
            if "docs.google.com" in self._config.spreadsheet_id
            else f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        )

        # ── Resolver sheet_name → sheet_gid vía la API ────────────────
        effective_gid = self._config.sheet_gid
        if self._config.sheet_name:
            try:
                sheets = self._sheets_client.list_sheets(spreadsheet_id)
                for s in sheets:
                    if s["title"] == self._config.sheet_name:
                        effective_gid = s["sheetId"]
                        self._log(
                            f"→ Pestaña '{self._config.sheet_name}' → gid={effective_gid}"
                        )
                        break
                else:
                    self._log(
                        f"⚠ Pestaña '{self._config.sheet_name}' no encontrada. "
                        f"Usando gid={effective_gid}."
                    )
            except Exception as e:
                self._log(
                    f"⚠ No se pudo resolver el gid de '{self._config.sheet_name}': {e}. "
                    f"Usando gid={effective_gid}."
                )

        cell_screenshots = await capture.capture_cells(
            sheet_url=sheet_url,
            cell_refs=all_refs,
            output_dir=str(self._output_dir),
            sheet_gid=effective_gid,
            expected_values=cell_values,
        )
        self._log(f"✓ {len(cell_screenshots)} capturas individuales generadas.")

        # ── Paso 4: Componer imagen ──
        self._log("→ Paso 4/5: Generando imagen compuesta...")
        composite_path = str(self._output_dir / self._config.composite_filename)

        compose_ticket_image(
            top_left_path=cell_screenshots[references.top_left],
            top_right_path=cell_screenshots[references.top_right],
            bottom_left_path=cell_screenshots[references.bottom_left],
            bottom_right_path=cell_screenshots[references.bottom_right],
            output_path=composite_path,
            labels={
                "top_left": references.top_left,
                "top_right": references.top_right,
                "bottom_left": references.bottom_left,
                "bottom_right": references.bottom_right,
            },
        )
        self._log(f"✓ Imagen compuesta guardada: {composite_path}")

        # ── Paso 5: Construir payload ──
        self._log("→ Paso 5/5: Construyendo payload...")
        payload = TicketCapturePayload(
            cells=cell_values,
            image_path=composite_path,
            references=references,
            cell_screenshots=cell_screenshots,
            target_cell=cell_ref.strip().upper(),
        )

        self._log(f"=== CAPTURA COMPLETADA: {cell_ref} ===")
        return payload

    def capture_sync(self, cell_ref: str) -> TicketCapturePayload:
        """
        Versión síncrona de capture() para usar desde threads o tkinter.

        Ejecuta el flujo completo (parser → API → Playwright → composición)
        de forma bloqueante usando asyncio.run(). Ideal para llamar desde
        threading.Thread sin modificar el modelo de concurrencia del proyecto.

        Args:
            cell_ref: Referencia de celda (ej. "F6", "AA10").

        Returns:
            TicketCapturePayload con valores, imagen compuesta, y referencias.
        """
        try:
            return asyncio.run(self._capture_and_stop(cell_ref))
        finally:
            # Limpiar recursos restantes que el loop asyncio pudo dejar abiertos
            self._capture = None
            self._capture_owned = False

    async def _capture_and_stop(self, cell_ref: str) -> TicketCapturePayload:
        """capture() + stop() para asegurar que los recursos se limpien."""
        try:
            return await self.capture(cell_ref)
        finally:
            if self._capture and self._capture_owned:
                await self._capture.stop()
                self._capture = None
                self._capture_owned = False
                # Dar tiempo a que se drenen los pipes antes de cerrar el loop
                await asyncio.sleep(0.3)

    # ── Placeholder para HubSpot ──────────────────────────────────────────

    def upload_to_hubspot(self, payload: TicketCapturePayload) -> dict[str, Any]:
        """
        PLACEHOLDER — Conectar con lógica existente de HubSpot.

        Este método está reservado para recibir el payload generado por
        capture() y enviarlo a HubSpot usando la lógica ya implementada
        en data/api.py y plugins/hubspot.py.

        Args:
            payload: Payload generado por TicketCaptureService.capture().

        Returns:
            Diccionario con resultado de la operación (por definir).
        """
        self._log("· upload_to_hubspot() — PLACEHOLDER — sin implementar aún.")
        return {
            "status": "placeholder",
            "message": (
                "upload_to_hubspot() no está implementado. "
                "Conecte aquí la lógica de HubSpot usando payload.cells, "
                "payload.image_path, y payload.references."
            ),
            "payload": {
                "cells": payload.cells,
                "image_path": payload.image_path,
                "references": payload.references.as_dict(),
                "target_cell": payload.target_cell,
            },
        }

    # ── Limpieza ──────────────────────────────────────────────────────────

    async def close(self) -> None:
        """Cierra el navegador Playwright si está abierto."""
        if self._capture:
            await self._capture.stop()
            self._capture = None
            self._capture_owned = False

    @property
    def sheets_client(self) -> GoogleSheetsClient | None:
        """Acceso al cliente de Sheets API para operaciones adicionales."""
        return self._sheets_client

    @property
    def capture_instance(self) -> PlaywrightSheetsCapture | None:
        """Acceso a la instancia de Playwright para operaciones adicionales."""
        return self._capture

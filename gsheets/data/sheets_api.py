"""
Módulo 2 — Cliente de Google Sheets API.

Autenticación mediante Service Account (archivo JSON de credenciales).
Soporta configuración vía variable de entorno GOOGLE_SERVICE_ACCOUNT_PATH.

Uso:
    client = GoogleSheetsClient("credenciales.json")
    # o si la variable GOOGLE_SERVICE_ACCOUNT_PATH está en .env:
    client = GoogleSheetsClient()
"""

from __future__ import annotations

import logging
import os
import sys as _sys
from pathlib import Path
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.paths import resource_path

# ── Logger ────────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
_ENV_SERVICE_ACCOUNT = "GOOGLE_SERVICE_ACCOUNT_PATH"


# ── Tipos ─────────────────────────────────────────────────────────────────────


type CellValues = dict[str, str | None]


# ── Cliente ───────────────────────────────────────────────────────────────────


class GoogleSheetsClient:
    """
    Cliente autenticado para leer valores de Google Sheets vía Service Account.

    Uso:
        client = GoogleSheetsClient("credenciales.json")
        valores = client.read_cells("SHEET_ID", ["A3", "F3", "A6", "F6"])
    """

    def __init__(
        self,
        credentials_path: str | Path | None = None,
        scopes: list[str] | None = None,
    ) -> None:
        """
        Args:
            credentials_path: Ruta al archivo JSON de Service Account.
                              Si es None, se busca en GOOGLE_SERVICE_ACCOUNT_PATH del .env.
            scopes: Alcances OAuth. Por defecto, solo lectura de spreadsheets.
        """
        self._scopes = scopes or _SCOPES

        if credentials_path is None:
            credentials_path = os.getenv(_ENV_SERVICE_ACCOUNT, "")

        if not credentials_path:
            raise ValueError(
                "Se requiere un archivo de Service Account. "
                "Pase credentials_path o defina GOOGLE_SERVICE_ACCOUNT_PATH en .env"
            )

        self._credentials_path = Path(credentials_path)
        if not self._credentials_path.exists() and not self._credentials_path.is_absolute():
            alt = Path(resource_path(credentials_path))
            if alt.exists():
                self._credentials_path = alt

        self._service = self._build_service()

    # ── Inicialización del servicio ───────────────────────────────────────

    def _build_service(self):
        """Construye y retorna el servicio autenticado de Sheets v4."""
        if not self._credentials_path.exists():
            raise FileNotFoundError(
                f"Archivo de credenciales no encontrado: {self._credentials_path}"
            )

        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(self._credentials_path), scopes=self._scopes
            )
        except Exception as exc:
            logger.error("Error al cargar credenciales Service Account: %s", exc)
            raise ValueError(
                f"No se pudieron cargar las credenciales desde "
                f"{self._credentials_path}: {exc}"
            ) from exc

        service = build("sheets", "v4", credentials=credentials)
        logger.info("Google Sheets API: servicio inicializado correctamente.")
        return service

    # ── Lectura de celdas ─────────────────────────────────────────────────

    def read_cell(
        self,
        spreadsheet_id: str,
        cell_range: str,
        sheet_name: str | None = None,
    ) -> str | None:
        """
        Lee el valor de una celda individual.

        Args:
            spreadsheet_id: ID del spreadsheet (extraído de la URL).
            cell_range: Referencia de celda (ej. "A3", "F6").
            sheet_name: Nombre de la hoja. Si no se especifica, se usa la primera.

        Returns:
            Valor de la celda como string, o None si está vacía.
        """
        full_range = f"'{sheet_name}'!{cell_range}" if sheet_name else cell_range

        try:
            result = (
                self._service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=full_range)
                .execute()
            )
            values = result.get("values", [])
            if values and values[0]:
                return str(values[0][0])
            return None
        except HttpError as exc:
            logger.error("Error al leer celda %s: %s", cell_range, exc)
            raise RuntimeError(f"Error al leer celda {cell_range}: {exc}") from exc

    def read_cells(
        self,
        spreadsheet_id: str,
        cell_refs: list[str],
        sheet_name: str | None = None,
    ) -> CellValues:
        """
        Lee múltiples celdas en una sola llamada batch.

        Args:
            spreadsheet_id: ID del spreadsheet.
            cell_refs: Lista de referencias (ej. ["A3", "F3", "A6", "F6"]).
            sheet_name: Nombre de la hoja (opcional).

        Returns:
            Dict {referencia: valor}. Las celdas vacías retornan None.
        """
        if sheet_name:
            ranges = [f"'{sheet_name}'!{ref}" for ref in cell_refs]
        else:
            ranges = list(cell_refs)

        try:
            result = (
                self._service.spreadsheets()
                .values()
                .batchGet(spreadsheetId=spreadsheet_id, ranges=ranges)
                .execute()
            )

            values: CellValues = {}
            for i, ref in enumerate(cell_refs):
                vr = result.get("valueRanges", [])
                if i < len(vr) and "values" in vr[i] and vr[i]["values"]:
                    values[ref] = str(vr[i]["values"][0][0])
                else:
                    values[ref] = None

            logger.info(
                "Leídas %d celdas del spreadsheet %s", len(cell_refs), spreadsheet_id
            )
            return values
        except HttpError as exc:
            logger.error("Error en batchGet: %s", exc)
            raise RuntimeError(f"Error al leer celdas en batch: {exc}") from exc

    def read_range(
        self,
        spreadsheet_id: str,
        range_str: str,
    ) -> list[list[str]]:
        """
        Lee un rango completo (ej. "A1:F10") y retorna matriz de valores.

        Args:
            spreadsheet_id: ID del spreadsheet.
            range_str: Rango en notación A1 (ej. "Hoja1!A1:F10").

        Returns:
            Matriz de valores [fila][columna].
        """
        try:
            result = (
                self._service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_str)
                .execute()
            )
            return result.get("values", [])
        except HttpError as exc:
            logger.error("Error al leer rango %s: %s", range_str, exc)
            raise RuntimeError(f"Error al leer rango {range_str}: {exc}") from exc

    # ── Utilidades ────────────────────────────────────────────────────────

    def list_sheets(self, spreadsheet_id: str) -> list[dict[str, str | int]]:
        """
        Obtiene todas las pestañas de un spreadsheet con sus propiedades.

        Args:
            spreadsheet_id: ID del spreadsheet.

        Returns:
            Lista de dicts con {title, sheetId, index} por cada pestaña.
            Ej: [{"title": "Enero", "sheetId": 0, "index": 0}, ...]
        """
        try:
            result = (
                self._service.spreadsheets()
                .get(
                    spreadsheetId=spreadsheet_id,
                    fields="sheets.properties(title,sheetId,index)",
                )
                .execute()
            )
            sheets = result.get("sheets", [])
            return [
                {
                    "title": s["properties"]["title"],
                    "sheetId": s["properties"].get("sheetId", 0),
                    "index": s["properties"].get("index", i),
                }
                for i, s in enumerate(sheets)
            ]
        except HttpError as exc:
            logger.error("Error al listar pestañas: %s", exc)
            raise RuntimeError(f"Error al listar pestañas: {exc}") from exc

    @staticmethod
    def extract_spreadsheet_id(url_or_id: str) -> str:
        """
        Extrae el spreadsheet ID de una URL de Google Sheets.

        Ejemplos:
            https://docs.google.com/spreadsheets/d/ABC123/edit#gid=0  ->  ABC123
            ABC123  ->  ABC123
        """
        import re

        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url_or_id)
        if match:
            return match.group(1)
        return url_or_id

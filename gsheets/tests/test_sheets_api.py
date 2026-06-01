"""
Tests para el cliente de Google Sheets API (Módulo 2).
Usa mocking para no depender de credenciales reales.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from gsheets.data.sheets_api import GoogleSheetsClient


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def fake_credentials_file():
    """Archivo JSON de Service Account falso."""
    data = {
        "type": "service_account",
        "project_id": "test-project",
        "private_key_id": "abc123",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMOCK\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test-project.iam.gserviceaccount.com",
        "client_id": "123456789",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(data, f)
        path = f.name
    yield path
    Path(path).unlink(missing_ok=True)


@pytest.fixture
def mock_service():
    """Mock del servicio de Google Sheets API y credenciales."""
    with patch(
        "gsheets.data.sheets_api.service_account.Credentials.from_service_account_file"
    ) as mock_creds:
        mock_credentials = MagicMock()
        mock_creds.return_value = mock_credentials

        with patch("gsheets.data.sheets_api.build") as mock_build:
            mock_sheets = MagicMock()
            mock_build.return_value = mock_sheets
            yield mock_sheets


# ── GoogleSheetsClient ────────────────────────────────────────────────────


class TestGoogleSheetsClient:
    def test_init_loads_credentials(self, fake_credentials_file, mock_service):
        client = GoogleSheetsClient(fake_credentials_file)
        assert client._service is not None

    def test_init_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            GoogleSheetsClient("nonexistent_file.json")

    def test_read_cell_returns_value(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["Hello"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "A3")

        assert result == "Hello"

    def test_read_cell_empty_returns_none(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {}

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "A3")

        assert result is None

    def test_read_cell_with_sheet_name(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["Data"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cell("spreadsheet123", "B5", sheet_name="Hoja1")

        assert result == "Data"

    def test_read_cells_batch(self, fake_credentials_file, mock_service):
        mock_batch = mock_service.spreadsheets.return_value.values.return_value
        mock_batch.batchGet.return_value.execute.return_value = {
            "valueRanges": [
                {"values": [["val_a3"]]},
                {"values": [["val_f3"]]},
                {},
                {"values": [["val_f6"]]},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cells(
            "spreadsheet123", ["A3", "F3", "A6", "F6"]
        )

        assert result == {
            "A3": "val_a3",
            "F3": "val_f3",
            "A6": None,
            "F6": "val_f6",
        }

    def test_read_cells_with_sheet_name(self, fake_credentials_file, mock_service):
        mock_batch = mock_service.spreadsheets.return_value.values.return_value
        mock_batch.batchGet.return_value.execute.return_value = {
            "valueRanges": [
                {"values": [["x"]]},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_cells(
            "spreadsheet123", ["A1"], sheet_name="MiHoja"
        )

        assert result == {"A1": "x"}

    def test_read_range(self, fake_credentials_file, mock_service):
        mock_values = mock_service.spreadsheets.return_value.values.return_value
        mock_values.get.return_value.execute.return_value = {
            "values": [["A", "B"], ["C", "D"]]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.read_range("spreadsheet123", "A1:B2")

        assert result == [["A", "B"], ["C", "D"]]

    def test_extract_spreadsheet_id_from_url(self):
        url = "https://docs.google.com/spreadsheets/d/ABC123xyz/edit#gid=0"
        result = GoogleSheetsClient.extract_spreadsheet_id(url)
        assert result == "ABC123xyz"

    def test_extract_spreadsheet_id_passthrough(self):
        result = GoogleSheetsClient.extract_spreadsheet_id("ABC123")
        assert result == "ABC123"

    def test_credentials_from_env(self, fake_credentials_file, mock_service, monkeypatch):
        """Si no se pasa path, se usa GOOGLE_SERVICE_ACCOUNT_PATH."""
        monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_PATH", fake_credentials_file)
        client = GoogleSheetsClient()  # sin argumento, usa .env
        assert client._service is not None

    def test_no_credentials_raises(self, monkeypatch):
        """Error claro si no hay credenciales ni en .env."""
        monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_PATH", raising=False)
        with pytest.raises(ValueError, match="Service Account"):
            GoogleSheetsClient()

    def test_list_sheets(self, fake_credentials_file, mock_service):
        """list_sheets retorna lista de pestañas con title, sheetId, index."""
        mock_get = mock_service.spreadsheets.return_value.get.return_value
        mock_get.execute.return_value = {
            "sheets": [
                {"properties": {"title": "Enero", "sheetId": 0, "index": 0}},
                {"properties": {"title": "Febrero", "sheetId": 1, "index": 1}},
                {"properties": {"title": "Marzo", "sheetId": 2, "index": 2}},
            ]
        }

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.list_sheets("spreadsheet123")

        assert len(result) == 3
        assert result[0]["title"] == "Enero"
        assert result[0]["sheetId"] == 0
        assert result[0]["index"] == 0
        assert result[2]["title"] == "Marzo"

    def test_list_sheets_empty(self, fake_credentials_file, mock_service):
        """list_sheets con spreadsheet sin pestañas retorna lista vacía."""
        mock_get = mock_service.spreadsheets.return_value.get.return_value
        mock_get.execute.return_value = {"sheets": []}

        client = GoogleSheetsClient(fake_credentials_file)
        result = client.list_sheets("spreadsheet123")

        assert result == []

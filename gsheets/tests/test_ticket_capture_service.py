"""
Tests para TicketCaptureService (Módulo 5 + 6).
Pruebas unitarias con mocking de Sheets API y Playwright.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
    TicketCapturePayload,
)


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def config():
    return TicketCaptureConfig(
        spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
        credentials_path="fake_creds.json",
        sheet_gid="0",
        headless=True,
        output_dir=None,
    )


@pytest.fixture
def mock_sheets_client():
    """Mock de GoogleSheetsClient."""
    with patch(
        "gsheets.services.ticket_capture_service.GoogleSheetsClient"
    ) as mock:
        client = MagicMock()
        # Retornar valores según las celdas que se pidan
        def _read_cells(spreadsheet_id, cell_refs, sheet_name=None):
            return {ref: f"value_{ref}" for ref in cell_refs}

        client.read_cells.side_effect = _read_cells
        # list_sheets retorna pestañas con títulos y gids
        client.list_sheets.return_value = [
            {"title": "Enero", "sheetId": 0, "index": 0},
            {"title": "Febrero", "sheetId": 1, "index": 1},
            {"title": "Jun", "sheetId": 123456, "index": 2},
        ]
        mock.return_value = client
        mock.extract_spreadsheet_id.return_value = "TEST123"
        yield mock


def _make_capture_cells_response(sheet_url, cell_refs, output_dir=None, sheet_gid="0", expected_values=None):
    """Genera respuesta dinámica de capture_cells según las referencias."""
    return {ref: f"/tmp/{ref.lower()}.png" for ref in cell_refs}


@pytest.fixture
def mock_playwright_capture():
    """Mock de PlaywrightSheetsCapture."""
    with patch(
        "gsheets.services.ticket_capture_service.PlaywrightSheetsCapture"
    ) as mock:
        cap = AsyncMock()
        cap.start = AsyncMock()
        cap.stop = AsyncMock()
        cap.capture_cells = AsyncMock(
            side_effect=_make_capture_cells_response
        )
        mock.return_value = cap
        yield mock


@pytest.fixture
def mock_compose(tmp_path):
    """Mock de compose_ticket_image que usa un path real."""
    output = str(tmp_path / "ticket_capture.png")
    with patch(
        "gsheets.services.ticket_capture_service.compose_ticket_image"
    ) as mock:
        mock.return_value = output
        yield mock


# ── Tests ─────────────────────────────────────────────────────────────────


class TestTicketCaptureConfig:
    def test_defaults(self):
        config = TicketCaptureConfig(spreadsheet_id="ABC123")
        assert config.spreadsheet_id == "ABC123"
        assert config.sheet_gid == "0"
        assert config.headless is True
        assert config.composite_filename == "ticket_capture.png"
        assert config.sheet_name is None
        assert config.credentials_path == ""


class TestTicketCaptureService:
    @pytest.mark.asyncio
    async def test_capture_full_flow(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        payload = await service.capture("F6")

        assert isinstance(payload, TicketCapturePayload)
        assert payload.target_cell == "F6"
        assert payload.cells == {
            "A3": "value_A3",
            "F3": "value_F3",
            "A6": "value_A6",
            "F6": "value_F6",
        }
        assert "ticket_capture.png" in payload.image_path
        assert payload.references.top_left == "A3"
        assert payload.references.top_right == "F3"
        assert payload.references.bottom_left == "A6"
        assert payload.references.bottom_right == "F6"
        assert len(payload.cell_screenshots) == 4
        # Verify compose was called with all four screenshot paths
        mock_compose.assert_called_once()

    @pytest.mark.asyncio
    async def test_capture_invalid_cell_raises(
        self, tmp_path, mock_sheets_client
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config, log_callback=lambda m: None)

        with pytest.raises(ValueError):
            await service.capture("")

    @pytest.mark.asyncio
    async def test_capture_with_sheet_name(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            sheet_name="Datos",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        await service.capture("J20")

        called_kwargs = mock_sheets_client.return_value.read_cells.call_args
        assert called_kwargs.kwargs["sheet_name"] == "Datos"

    @pytest.mark.asyncio
    async def test_capture_resolves_sheet_name_to_gid(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        """Si sheet_name coincide con list_sheets, se usa el gid correspondiente."""
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            sheet_name="Jun",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        await service.capture("F6")

        # Verificar que capture_cells recibió el gid correcto (123456 para "Jun")
        called_kwargs = mock_playwright_capture.return_value.capture_cells.call_args
        assert called_kwargs.kwargs["sheet_gid"] == 123456

    @pytest.mark.asyncio
    async def test_capture_without_credentials_raises(self, tmp_path, monkeypatch):
        # Asegurar que no haya env vars de tests anteriores
        monkeypatch.delenv("GOOGLE_SERVICE_ACCOUNT_PATH", raising=False)
        config = TicketCaptureConfig(
            spreadsheet_id="TEST123",
            credentials_path="",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        with pytest.raises(RuntimeError, match="Google Sheets"):
            await service.capture("F6")

    @pytest.mark.asyncio
    async def test_context_manager(
        self,
        tmp_path,
        mock_sheets_client,
        mock_playwright_capture,
        mock_compose,
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        async with TicketCaptureService(config) as service:
            payload = await service.capture("AB25")

        assert payload.references.bottom_right == "AB25"
        mock_playwright_capture.return_value.stop.assert_called_once()

    def test_upload_to_hubspot_placeholder(self, tmp_path, mock_sheets_client):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        payload = TicketCapturePayload(
            cells={"A3": "test"},
            image_path="/tmp/img.png",
            references=MagicMock(),
            cell_screenshots={},
            target_cell="F6",
        )

        result = service.upload_to_hubspot(payload)

        assert result["status"] == "placeholder"
        assert "implementado" in result["message"]

    @pytest.mark.asyncio
    async def test_close(
        self, tmp_path, mock_sheets_client, mock_playwright_capture
    ):
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        service._capture = mock_playwright_capture.return_value
        await service.close()

        mock_playwright_capture.return_value.stop.assert_called_once()
        assert service._capture is None

    def test_capture_sync_wrapper(
        self, tmp_path, mock_sheets_client, mock_playwright_capture, mock_compose
    ):
        """capture_sync() ejecuta el flujo completo de forma bloqueante."""
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="fake.json",
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)

        payload = service.capture_sync("F6")

        assert payload.target_cell == "F6"
        assert "ticket_capture.png" in payload.image_path
        assert len(payload.cell_screenshots) == 4

    def test_credentials_from_env(
        self, tmp_path, mock_sheets_client, mock_playwright_capture, mock_compose, monkeypatch
    ):
        """Si no se pasa credentials_path, se usa GOOGLE_SERVICE_ACCOUNT_PATH."""
        monkeypatch.setenv("GOOGLE_SERVICE_ACCOUNT_PATH", "/fake/path.json")
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/TEST123/edit",
            credentials_path="",  # vacío → debe tomarse del env
            output_dir=tmp_path,
        )
        service = TicketCaptureService(config)
        assert service._sheets_client is not None


class TestTicketCapturePayload:
    def test_payload_attributes(self):
        payload = TicketCapturePayload(
            cells={"A3": "hello", "F6": "world"},
            image_path="/tmp/test.png",
            references=MagicMock(),
            cell_screenshots={"A3": "/tmp/a3.png", "F6": "/tmp/f6.png"},
            target_cell="F6",
        )

        assert payload.cells["A3"] == "hello"
        assert payload.target_cell == "F6"
        assert "F6" in payload.cell_screenshots

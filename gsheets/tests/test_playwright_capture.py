"""
Tests para PlaywrightSheetsCapture (Módulo 3).
Usa mocking extensivo para no requerir navegador real.

Cambios respecto a la versión anterior:
  - launch_persistent_context en vez de launch + new_context
  - No usa storage_state (el perfil persiste automáticamente)
  - _validate_page bloquea redirecciones al login de Google
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from gsheets.core.playwright_capture import PlaywrightSheetsCapture


# ── Helpers ───────────────────────────────────────────────────────────────


def _build_mock_playwright():
    """Construye el árbol completo de mocks de Playwright (CDP + persistent context)."""
    mock_page = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.screenshot = AsyncMock()
    mock_page.reload = AsyncMock()
    mock_page.wait_for_selector = AsyncMock()
    mock_page.title = AsyncMock(return_value="Mi Hoja — Google Sheets")

    # evaluate inteligente: distingue entre grid polling, _locate_cell y _validate_and_refine_rect
    async def _smart_evaluate(js, arg=None):
        if arg is None:
            # grid polling → retornar selectores válidos
            return "#waffle-grid-container, #colheaders, #rowheaders"
        if isinstance(arg, list):
            if len(arg) == 3 and isinstance(arg[0], str):
                # _validate_and_refine_rect: [cellRef, minDim, maxDim]
                return {
                    "x": 100, "y": 200, "w": 120, "h": 25,
                    "tag": "div", "cls": "cell-active", "text": "F6",
                    "hasBorder": True, "score": 10,
                }
            # _validate_and_refine_rect anterior: [cx, cy, cellRef]
            return {
                "x": 98, "y": 198, "w": 120, "h": 25,
                "tag": "div", "cls": "cell-active", "text": "F6",
                "hasBorder": True, "score": 10,
            }
        # _locate_cell → rect calculado
        return {"x": 100, "y": 200, "width": 120, "height": 25}

    mock_page.evaluate = AsyncMock(side_effect=_smart_evaluate)
    type(mock_page).url = PropertyMock(
        return_value="https://docs.google.com/spreadsheets/d/ABC123/edit#gid=0&range=A3"
    )

    # launch_persistent_context retorna el contexto directamente (fallback)
    mock_context = AsyncMock()
    mock_context.pages = [mock_page]
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_context.close = AsyncMock()

    # connect_over_cdp retorna un browser con contexts (estrategia principal)
    mock_browser = AsyncMock()
    mock_browser.contexts = [mock_context]
    mock_browser.close = AsyncMock()

    mock_pw_instance = AsyncMock()
    mock_pw_instance.chromium.connect_over_cdp = AsyncMock(return_value=mock_browser)
    mock_pw_instance.chromium.launch_persistent_context = AsyncMock(
        return_value=mock_context
    )
    mock_pw_instance.stop = AsyncMock()

    return {
        "page": mock_page,
        "context": mock_context,
        "browser": mock_browser,
        "pw_instance": mock_pw_instance,
    }


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def mock_pw():
    """Mock de async_playwright que retorna objetos awaitables."""
    mocks = _build_mock_playwright()
    with patch(
        "gsheets.core.playwright_capture.async_playwright"
    ) as mock_async_pw:
        mock_cm = MagicMock()
        mock_cm.start = AsyncMock(return_value=mocks["pw_instance"])
        mock_async_pw.return_value = mock_cm
        yield mocks


# ── Tests ─────────────────────────────────────────────────────────────────


class TestPlaywrightSheetsCapture:
    @pytest.mark.asyncio
    async def test_start_connects_via_cdp(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        await cap.start()
        try:
            assert cap._context is not None
            assert cap._page is not None
            # connect_over_cdp fue llamado (estrategia principal)
            mock_pw["pw_instance"].chromium.connect_over_cdp.assert_called_once()
        finally:
            await cap.stop()

    def test_page_property_raises_when_not_started(self):
        cap = PlaywrightSheetsCapture(headless=True)
        with pytest.raises(RuntimeError, match="no ha sido iniciado"):
            _ = cap.page

    def test_extract_spreadsheet_id_from_url(self):
        url = "https://docs.google.com/spreadsheets/d/XYZ789/edit#gid=0"
        result = PlaywrightSheetsCapture._extract_spreadsheet_id(url)
        assert result == "XYZ789"

    def test_extract_spreadsheet_id_passthrough(self):
        result = PlaywrightSheetsCapture._extract_spreadsheet_id("ABC123")
        assert result == "ABC123"

    @pytest.mark.asyncio
    async def test_capture_cell_navigates_and_screenshots(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True  # saltar verificación de auth

        path = await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="A3",
        )

        mock_pw["page"].goto.assert_called_once()
        assert "domcontentloaded" in str(mock_pw["page"].goto.call_args)
        # screenshot: 1 captura final de celda
        assert mock_pw["page"].screenshot.call_count >= 1
        assert "a3" in path.lower()

    @pytest.mark.asyncio
    async def test_capture_cell_retry_on_none_rect(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        locate_calls = [0]

        async def mock_evaluate(js, arg=None):
            if arg is None:
                return "#waffle-grid-container"
            if isinstance(arg, list):
                return {"x": 100, "y": 200, "w": 100, "h": 20, "tag": "div", "cls": "", "text": "F6", "hasBorder": True, "score": 10}
            locate_calls[0] += 1
            if locate_calls[0] == 1:
                return None
            return {"x": 50, "y": 60, "width": 100, "height": 20}

        mock_pw["page"].evaluate = AsyncMock(side_effect=mock_evaluate)

        await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="F6",
        )

        assert locate_calls[0] >= 2  # falló la primera, éxito en el retry
        mock_pw["page"].reload.assert_called_once()

    @pytest.mark.asyncio
    async def test_capture_cell_raises_when_unlocatable(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        async def mock_evaluate(js, arg=None):
            if arg is None:
                return "#waffle-grid-container"
            if isinstance(arg, list):
                return None  # validation: no encuentra nada
            return None  # celda no encontrada en _locate_cell

        mock_pw["page"].evaluate = AsyncMock(side_effect=mock_evaluate)
        mock_pw["page"].screenshot = AsyncMock()

        with pytest.raises(RuntimeError, match="No se pudo localizar"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="ZZ999",
            )

    @pytest.mark.asyncio
    async def test_login_redirect_raises_explicit_error(self, mock_pw):
        """Si la URL es accounts.google.com, lanza error claro."""
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]

        # Simular redirección al login
        mock_pw["page"].title = AsyncMock(return_value="Sign in – Google Accounts")
        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://accounts.google.com/signin/v2/identifier?..."
        )

        with pytest.raises(RuntimeError, match="autenticada"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

    @pytest.mark.asyncio
    async def test_login_title_detection_raises(self, mock_pw):
        """Si el título contiene 'Sign in', lanza error."""
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]

        mock_pw["page"].title = AsyncMock(return_value="Sign in – Google Accounts")
        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://docs.google.com/spreadsheets/d/ABC123/edit"
        )

        with pytest.raises(RuntimeError, match="login de Google"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

    @pytest.mark.asyncio
    async def test_verify_google_auth_myaccount_check(self, mock_pw):
        """_verify_google_auth navega a myaccount.google.com y verifica la URL."""
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        # page.url = sheets URL (no contiene accounts.google.com) → pasa

        await cap._verify_google_auth()

        assert cap._auth_verified is True
        first_call = mock_pw["page"].goto.call_args_list[0][0][0]
        assert "myaccount.google.com" in first_call

    @pytest.mark.asyncio
    async def test_verify_google_auth_redirect_detected(self, mock_pw):
        """Si myaccount redirige a accounts.google.com, lanza error."""
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]

        type(mock_pw["page"]).url = PropertyMock(
            return_value="https://accounts.google.com/signin/v2/identifier?..."
        )

        with pytest.raises(RuntimeError, match="no está autenticada"):
            await cap._verify_google_auth()

        assert cap._auth_verified is False

    @pytest.mark.asyncio
    async def test_capture_cells_multiple(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        result = await cap.capture_cells(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_refs=["A3", "F3", "A6", "F6"],
        )

        assert len(result) == 4
        assert "A3" in result
        assert "F6" in result

    @pytest.mark.asyncio
    async def test_capture_cell_uses_exact_gid(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        await cap.capture_cell(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_ref="A3",
            sheet_gid="42",
        )

        call_url = mock_pw["page"].goto.call_args[0][0]
        assert "gid=42" in call_url

    @pytest.mark.asyncio
    async def test_grid_not_found_raises_error(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        mock_pw["page"].wait_for_selector = AsyncMock(
            side_effect=Exception("timeout")
        )
        mock_pw["page"].evaluate = AsyncMock(return_value=None)

        with pytest.raises(RuntimeError, match="grid"):
            await cap.capture_cell(
                sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
                cell_ref="A3",
            )

    def test_clear_session(self, tmp_path):
        profile_dir = tmp_path / "chrome_profile"
        profile_dir.mkdir()

        cap = PlaywrightSheetsCapture(headless=True, profile_dir=profile_dir)
        assert cap._profile_dir.exists()
        cap.clear_session()
        assert not cap._profile_dir.exists()

    def test_capture_cells_sync_wrapper(self, mock_pw):
        cap = PlaywrightSheetsCapture(headless=True)
        cap._playwright = mock_pw["pw_instance"]
        cap._context = mock_pw["context"]
        cap._page = mock_pw["page"]
        cap._auth_verified = True

        result = cap.capture_cells_sync(
            sheet_url="https://docs.google.com/spreadsheets/d/ABC123/edit",
            cell_refs=["A3", "F6"],
        )

        assert len(result) == 2
        assert "A3" in result
        assert "F6" in result
        mock_pw["context"].close.assert_called_once()
        mock_pw["pw_instance"].stop.assert_called_once()

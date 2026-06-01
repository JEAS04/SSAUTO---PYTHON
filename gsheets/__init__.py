"""
gsheets — Captura de celdas de Google Sheets con Playwright + Sheets API + Pillow.

Flujo principal:
  1. parse_target_cell("F6")           → calcula A3, F3, A6, F6
  2. GoogleSheetsClient.read_cells()   → obtiene valores desde la API
  3. PlaywrightSheetsCapture           → captura visual de cada celda
  4. compose_ticket_image()            → compone grilla 2x2
  5. TicketCaptureService.capture()    → orquestador completo

Uso asíncrono:
    import asyncio
    from gsheets import TicketCaptureService, TicketCaptureConfig

    async def main():
        config = TicketCaptureConfig(
            spreadsheet_id="https://docs.google.com/spreadsheets/d/ABC123/edit",
            credentials_path="service_account.json",
        )
        async with TicketCaptureService(config) as svc:
            payload = await svc.capture("F6")
            print(payload.cells)
            print(payload.image_path)

    asyncio.run(main())

Uso síncrono (desde threads o tkinter):
    from gsheets import TicketCaptureService, TicketCaptureConfig

    config = TicketCaptureConfig(
        spreadsheet_id="https://docs.google.com/spreadsheets/d/ABC123/edit",
        # credentials_path también puede definirse vía GOOGLE_SERVICE_ACCOUNT_PATH en .env
    )
    service = TicketCaptureService(config)
    payload = service.capture_sync("F6")
    print(payload.cells)
    print(payload.image_path)
"""

from gsheets.utils.cell_parser import (
    parse_target_cell,
    col_letter_to_index,
    index_to_col_letter,
    CellReferences,
)
from gsheets.data.sheets_api import GoogleSheetsClient
from gsheets.core.playwright_capture import PlaywrightSheetsCapture
from gsheets.utils.image_compositor import compose_ticket_image
from gsheets.services.ticket_capture_service import (
    TicketCaptureService,
    TicketCaptureConfig,
    TicketCapturePayload,
)

__all__ = [
    # Parser
    "parse_target_cell",
    "col_letter_to_index",
    "index_to_col_letter",
    "CellReferences",
    # API
    "GoogleSheetsClient",
    # Playwright
    "PlaywrightSheetsCapture",
    # Imagen
    "compose_ticket_image",
    # Servicio
    "TicketCaptureService",
    "TicketCaptureConfig",
    "TicketCapturePayload",
]

__version__ = "1.0.0"

"""gsheets.services — Servicio orquestador de captura de tickets.

Expone TicketCaptureService que coordina parser, Sheets API, Playwright
y composicion de imagenes en un solo flujo.
"""

from gsheets.services.ticket_capture_service import TicketCaptureService

__all__ = ["TicketCaptureService"]

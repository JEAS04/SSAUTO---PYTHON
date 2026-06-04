"""gsheets.core — Captura visual de celdas con Playwright.

Expone PlaywrightSheetsCapture para navegar a Google Sheets, localizar
celdas por referencia A1 y capturar cada una como imagen PNG.
"""

from gsheets.core.playwright_capture import PlaywrightSheetsCapture

__all__ = ["PlaywrightSheetsCapture"]

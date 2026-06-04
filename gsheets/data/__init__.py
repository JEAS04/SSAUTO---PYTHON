"""gsheets.data — Cliente de Google Sheets API.

Expone GoogleSheetsClient para leer valores de celdas via Service Account
y el tipo CellValues para anotaciones.
"""

from gsheets.data.sheets_api import GoogleSheetsClient, CellValues

__all__ = ["GoogleSheetsClient", "CellValues"]

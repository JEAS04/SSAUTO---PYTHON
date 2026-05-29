"""
scraping/sunrun_selectors.py — Selectores CSS/XPath del portal Sunrun.

Extraído de scraping_sunrun.py. Si el DOM de Sunrun cambia,
solo actualiza este archivo.
"""

# ── URLs ───────────────────────────────────────────────────────────────

URL_BASE_SUNRUN = "https://sunrun.my.site.com"
URL_LISTA_SUNRUN = (
    "https://sunrun.my.site.com/partners/s/fs-dispatch/FS_Dispatch__c/Default"
)

# ── Barra de búsqueda global ──────────────────────────────────────────

SEL_BUSQUEDA_GLOBAL = "div.forceSearchInputDesktop input[role='combobox']"

# ── Datos del cliente ─────────────────────────────────────────────────

SELECTOR_NUMERO_FSD = "//slot[@name='primaryField']//lightning-formatted-text"

PATRON_CAMPO = (
    "//span[contains(@class,'test-id__field-label') "
    "and normalize-space(text())='{}']"
    "/ancestor::div[contains(@class,'label-stacked') "
    "or (contains(@class,'slds-form-element') "
    "and not(contains(@class,'slds-form-element__')))]"
    "//lightning-formatted-text"
)

SELECTOR_NOMBRE = PATRON_CAMPO.format("Customer Name")
SELECTOR_DIRECCION = PATRON_CAMPO.format("Address")
SELECTOR_TELEFONO = PATRON_CAMPO.format("Customer Phone")
SELECTOR_MOVIL = PATRON_CAMPO.format("Mobile Phone")
SELECTOR_EMAIL = PATRON_CAMPO.format("Customer Email")
SELECTOR_ESTADO = PATRON_CAMPO.format("State")
SELECTOR_COUNTY = PATRON_CAMPO.format("County")
SELECTOR_CIUDAD = PATRON_CAMPO.format("City")
SELECTOR_ZIP = PATRON_CAMPO.format("Zip Code")

SELECTOR_DISPATCH_STATE = PATRON_CAMPO.format("Dispatch State")
SELECTOR_APPOINTMENT_DATE = PATRON_CAMPO.format("Appointment Date")
SELECTOR_CASE_REASON = PATRON_CAMPO.format("Case Reason")

# ── Upload ─────────────────────────────────────────────────────────────

SELECTOR_RELATED = "//a[@role='tab' and contains(normalize-space(.),'Related')]"
SELECTOR_UPLOAD_FILES_INPUT = (
    "//input[@type='file' and contains(@class,'slds-file-selector__input')]"
)
SELECTOR_UPLOAD_FILES_BUTTON = (
    "//span[normalize-space(text())='Upload Files']/ancestor::label"
)
SELECTOR_DROP_FILES = (
    "//span[contains(normalize-space(.),'Drop Files')]"
    "/ancestor::*[contains(@class,'slds-file-selector')]"
)

# ── Dropdown MRU ──────────────────────────────────────────────────────

SEL_MRU_DROPDOWN = "a.MRU_SCOPED"

# ── Tiempos ────────────────────────────────────────────────────────────

TIMEOUT = 15
TIMEOUT_LISTA = 30
TIMEOUT_MRU = 10
PAUSA_FILTRO = 2.0
PAUSA_DETALLE = 1.5

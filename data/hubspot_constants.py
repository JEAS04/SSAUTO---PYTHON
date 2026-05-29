"""
data/hubspot_constants.py — Nombres de propiedades de HubSpot CRM.

Centraliza todas las constantes de propiedades de tickets y contactos
que estaban dispersas en data/api.py.
"""

# ── Propiedades de tickets ────────────────────────────────────────────

_T_FSD = "fsd__"
_T_FIRSTNAME = "firstname"
_T_LASTNAME = "lastname"
_T_ID_GOFORMZ = "id_goformz__servicios_tecnicos_"
_T_ADDRESS = "physical_address"
_T_PHONE = "phone"
_T_PHONE_ALT = "telefono_alterno"
_T_EMAIL = "e_mail"
_T_COUNTY = "pueblo_para_servicio_tecnico"
_T_SUBJECT = "subject"
_T_NOTA = "nota_ticket__sac_"
_T_STATE = "state"
_T_ZIP = "zip"

TICKET_PROPS = [
    _T_SUBJECT,
    _T_FSD,
    _T_ID_GOFORMZ,
    _T_FIRSTNAME,
    _T_LASTNAME,
    _T_ADDRESS,
    _T_PHONE,
    _T_PHONE_ALT,
    _T_EMAIL,
    _T_COUNTY,
    _T_STATE,
    _T_ZIP,
    _T_NOTA,
]

# ── Propiedades de contactos ──────────────────────────────────────────

_C_FIRSTNAME = "firstname"
_C_LASTNAME = "lastname"
_C_ID_GOFORMZ = "id_de_goformz__contacto_"
_C_ADDRESS = "direccion__fisica_"
_C_PHONE = "phone"
_C_PHONE_ALT = "telefono_alterno_del_cliente"
_C_EMAIL = "email"
_C_STATE = "country"
_C_STATE2 = "state"
_C_MUNICIPIO = "municipio_de_residencia"
_C_MUNICIPIO_CO = "municipios_co__contacto_"
_C_ZIP = "zip"

CONTACT_PROPS = [
    _C_FIRSTNAME,
    _C_LASTNAME,
    _C_ID_GOFORMZ,
    _C_ADDRESS,
    _C_PHONE,
    _C_PHONE_ALT,
    _C_EMAIL,
    _C_STATE,
    _C_STATE2,
    _C_MUNICIPIO,
    _C_MUNICIPIO_CO,
    _C_ZIP,
]

# ── Mapa de campos de búsqueda de contactos ───────────────────────────

SEARCH_CONTACT_FIELDS = {
    "nombre": "firstname",
    "apellido": "lastname",
    "telefono": "phone",
    "correo": "email",
    "direccion": "direccion__fisica_",
    "id_cliente": "id_de_goformz__contacto_",
}

SEARCH_EXACT_FIELDS = {"telefono", "correo", "id_cliente"}

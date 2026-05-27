# api.py
"""
Extracción estable de datos HubSpot.
NO contiene lógica de búsquedas múltiples.
"""

import os
import re
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest as TicketSearchRequest
from hubspot.crm.contacts import PublicObjectSearchRequest as ContactSearchRequest
from hubspot.crm.tickets import ApiException as TicketApiException
from hubspot.crm.contacts import ApiException as ContactApiException

# =========================================================
# INIT
# =========================================================

load_dotenv()

_token = os.getenv("ACCESS_TOKEN")

_client = HubSpot(access_token=_token)

# =========================================================
# PROPIEDADES HUBSPOT
# =========================================================

# ---------- TICKETS ----------

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

_TICKET_PROPS = [
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

# ---------- CONTACTOS ----------

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

_CONTACT_PROPS = [
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

# =========================================================
# HELPERS
# =========================================================


def _val(props: dict, key: str) -> str:
    v = props.get(key) or ""
    return v.strip()


def _limpiar_nombre(nombre: str) -> str:
    if not nombre:
        return ""

    if " / " in nombre:
        nombre = nombre.split(" / ")[0]

    elif "/" in nombre:
        nombre = nombre.split("/")[0]

    return nombre.strip()


def _parsear_asunto(asunto: str) -> dict:

    texto = asunto or ""

    # =====================================================
    # FSD
    # =====================================================

    fsd = ""

    m_fsd = re.search(
        r"\bFSD[-_\s]*(\d{4,})\b",
        texto,
        re.IGNORECASE,
    )

    if m_fsd:
        fsd = m_fsd.group(1)

    # =====================================================
    # ID CLIENTE
    # =====================================================

    id_cliente = ""

    patrones = [
        r"\bID\s*[:#-]?\s*(\d{4,})\b",
        r"\bCLIENTE\s*[:#-]?\s*(\d{4,})\b",
        r"\bGOFORMZ\s*[:#-]?\s*(\d{4,})\b",
    ]

    m_id = None
    for patron in patrones:
        m = re.search(patron, texto, re.IGNORECASE)

        if m:
            id_cliente = m.group(1)
            m_id = m
            break

    # =====================================================
    # NOMBRE (puede estar dentro del subject)
    # Intentos por orden: entre FSD y ID, por partes separadas por '-' o '|' ,
    # o heurística de tokens con letras (2 palabras típicamente).
    # =====================================================

    nombre = ""

    try:
        if m_fsd and m_id:
            # extraer la sección entre el match de FSD y el match de ID
            start = m_fsd.end()
            end = m_id.start()
            mid = texto[start:end].strip(" -–—:\t\n\r")
            if mid:
                nombre = mid.strip()

        if not nombre:
            # dividir por separadores comunes y elegir la parte que parezca un nombre
            parts = re.split(r"[-–—|/]", texto)
            for p in parts:
                s = p.strip()
                if not s:
                    continue
                if re.search(r"\bFSD\b", s, re.IGNORECASE):
                    continue
                if re.search(r"\b(ID|CLIENTE|GOFORMZ)\b", s, re.IGNORECASE):
                    continue
                # evitar partes que sean mayoritariamente dígitos
                digits = re.sub(r"\D", "", s)
                if digits and len(digits) >= 3 and len(digits) / max(1, len(s)) > 0.4:
                    continue
                # heurística: debe contener letras y al menos una separación (nombre apellido)
                if re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", s) and len(s.split()) >= 1:
                    # preferir partes con 2 palabras
                    if len(s.split()) >= 2:
                        nombre = s
                        break
                    # si no hay partes con 2 palabras, tomar la primera válida
                    if not nombre:
                        nombre = s

        # limpiar nombre resultante (recortar separadores residuales)
        if nombre:
            nombre = nombre.strip()
            nombre = re.sub(r"^[\s\-–—_/:|]+|[\s\-–—_/:|]+$", "", nombre)
    except Exception:
        nombre = ""

    return {
        "fsd_parsed": fsd,
        "id_cliente": id_cliente,
        "nombre": nombre,
    }


# =========================================================
# TICKET POR FSD
# =========================================================


def _buscar_ticket_por_fsd(fsd: str):

    fsd_clean = fsd.strip()

    candidatos = []

    candidatos.append(fsd_clean)

    candidatos.append(fsd_clean.upper())

    candidatos.append(fsd_clean.replace(" ", ""))

    candidatos.append(fsd_clean.upper().replace("-", ""))

    numeric_only = re.sub(r"\D", "", fsd_clean)

    if numeric_only:
        candidatos.append(numeric_only)

    if numeric_only:
        candidatos.append(f"FSD-{numeric_only}")

    # quitar duplicados

    vistos = set()

    candidatos_finales = []

    for c in candidatos:
        if c not in vistos:
            vistos.add(c)
            candidatos_finales.append(c)

    # buscar

    for candidate in candidatos_finales:

        print(f"[HubSpot] Buscando FSD='{candidate}'")

        search_request = TicketSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": _T_FSD,
                            "operator": "EQ",
                            "value": candidate,
                        }
                    ]
                }
            ],
            properties=_TICKET_PROPS,
            limit=1,
        )

        try:

            response = _client.crm.tickets.search_api.do_search(
                public_object_search_request=search_request
            )

            if response.results:

                ticket = response.results[0]

                return {
                    "ticket_id": ticket.id,
                    "props": ticket.properties,
                }

        except TicketApiException as e:

            print(f"[HubSpot] Error buscando ticket FSD={candidate}: {e}")

    return None


# =========================================================
# CONTACTO POR ID GOFORMZ
# =========================================================


def _buscar_contacto_por_id_goformz(id_goformz: str):

    if not id_goformz:
        return None

    search_request = ContactSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "propertyName": _C_ID_GOFORMZ,
                        "operator": "EQ",
                        "value": id_goformz,
                    }
                ]
            }
        ],
        properties=_CONTACT_PROPS,
        limit=1,
    )

    try:

        response = _client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )

        if not response.results:
            return None

        contact = response.results[0]

        return {
            "contact_id": contact.id,
            "props": contact.properties,
        }

    except ContactApiException as e:

        print(f"[HubSpot] Error buscando contacto: {e}")

        return None


# =========================================================
# TICKET POR ID GOFORMZ
# =========================================================


def _buscar_ticket_por_id_goformz(id_goformz: str):

    if not id_goformz:
        return None

    # Intentar también con formato con coma (HubSpot a veces guarda "267,334")
    candidatos_id = [id_goformz]
    try:
        numero = int(id_goformz.replace(",", "").strip())
        con_coma = f"{numero:,}"
        if con_coma != id_goformz:
            candidatos_id.append(con_coma)
    except ValueError:
        pass

    for id_val in candidatos_id:
        search_request = TicketSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": _T_ID_GOFORMZ,
                            "operator": "EQ",
                            "value": id_val,
                        }
                    ]
                }
            ],
            properties=_TICKET_PROPS,
            limit=10,  # Traer varios — puede haber tickets sin FSD del mismo cliente
        )

        try:
            response = _client.crm.tickets.search_api.do_search(
                public_object_search_request=search_request
            )

            if not response.results:
                continue

            # Preferir el ticket que tenga fsd__ llenado
            ticket_con_fsd = None
            ticket_fallback = None

            for ticket in response.results:
                fsd_val = (ticket.properties or {}).get(_T_FSD, "")
                if fsd_val and str(fsd_val).strip():
                    ticket_con_fsd = ticket
                    break
                if ticket_fallback is None:
                    ticket_fallback = ticket

            ticket = ticket_con_fsd or ticket_fallback
            if ticket:
                return {"ticket_id": ticket.id, "props": ticket.properties}

        except TicketApiException as e:
            print(f"[HubSpot] Error buscando ticket por ID GoFormz={id_val}: {e}")

    return None


# =========================================================
# BUSCAR FSD POR ID CLIENTE (MEJORADA)
# =========================================================


def _buscar_fsd_por_id_cliente(id_cliente: str) -> str:
    """
    Busca el FSD asociado a un id_cliente.
    Realiza búsqueda en tickets por id_goformz__servicios_tecnicos_
    y retorna la propiedad fsd__.

    Args:
        id_cliente: ID del cliente a buscar

    Returns:
        FSD encontrado o string vacío si no existe
    """
    # Validar entrada
    if not id_cliente:
        return ""

    id_cliente_limpio = str(id_cliente).strip()
    if not id_cliente_limpio:
        return ""

    # Buscar el ticket
    ticket = _buscar_ticket_por_id_goformz(id_cliente_limpio)

    if not ticket:
        return ""

    # Extraer FSD del ticket
    props = ticket.get("props", {})
    fsd = props.get(_T_FSD, "")

    return str(fsd).strip() if fsd else ""


def _buscar_fsd_por_contact_id(contact_id: str) -> str:
    """
    Busca el FSD de un ticket asociado a un contact_id.

    Usa la API de asociaciones de HubSpot:
      contacto → tickets asociados → leer fsd__ del primer ticket.

    hs_all_contact_ids NO es filtrable en la Search API, por eso
    el enfoque anterior no funcionaba.
    """
    if not contact_id:
        return ""

    contact_id_limpio = str(contact_id).strip()
    if not contact_id_limpio:
        return ""

    try:
        # Paso 1: obtener IDs de tickets asociados al contacto
        assoc_response = _client.crm.associations.v4.basic_api.get_page(
            object_type="contacts",
            object_id=contact_id_limpio,
            to_object_type="tickets",
            limit=3,
        )

        if not assoc_response.results:
            return ""

        # Tomar el primer ticket asociado
        ticket_id = str(assoc_response.results[0].to_object_id)

        # Paso 2: leer la propiedad fsd__ de ese ticket
        ticket = _client.crm.tickets.basic_api.get_by_id(
            ticket_id=ticket_id,
            properties=[_T_FSD, _T_ID_GOFORMZ],
        )

        fsd = ticket.properties.get(_T_FSD, "")
        return str(fsd).strip() if fsd else ""

    except Exception as e:
        print(f"[HubSpot] _buscar_fsd_por_contact_id(contact_id={contact_id}): {e}")
        return ""


# =========================================================
# API WRAPPER
# =========================================================


_SEARCH_CONTACT_FIELDS = {
    "nombre": "firstname",
    "apellido": "lastname",
    "telefono": "phone",
    "correo": "email",
    "direccion": "direccion__fisica_",  # FIX: en contactos la dirección es este campo
    "id_cliente": "id_de_goformz__contacto_",
}

# Campos que requieren EQ en vez de CONTAINS_TOKEN (valores exactos o numéricos)
_SEARCH_EXACT_FIELDS = {"telefono", "correo", "id_cliente"}


class HubSpotAPI:
    def __init__(self):
        self.client = _client

    def buscar_contactos_por_criterio(self, criterio, tipo_busqueda):
        if tipo_busqueda == "fsd":
            datos = extraer_datos_hubspot(criterio)
            if datos.get("error"):
                return []
            return [datos]

        field = _SEARCH_CONTACT_FIELDS.get(tipo_busqueda)
        if not field:
            return []

        query = str(criterio).strip()
        if not query:
            return []

        # FIX: teléfono, correo e id_cliente son valores exactos → usar EQ.
        # nombre, apellido y dirección son texto libre → usar CONTAINS_TOKEN.
        operator = "EQ" if tipo_busqueda in _SEARCH_EXACT_FIELDS else "CONTAINS_TOKEN"

        search_request = ContactSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": field,
                            "operator": operator,
                            "value": query,
                        }
                    ]
                }
            ],
            properties=[
                "firstname",
                "lastname",
                "email",
                "phone",
                "telefono_alterno_del_cliente",
                "direccion__fisica_",  # FIX: campo real de dirección en contactos
                "id_de_goformz__contacto_",
                "municipio_de_residencia",
                "municipios_co__contacto_",
                "country",
                "state",
                "zip",
            ],
            limit=10,
        )

        try:
            response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )

            candidatos = []
            for contacto in response.results:
                props = contacto.properties or {}
                id_cliente = props.get("id_de_goformz__contacto_", "")

                candidato = {
                    "contact_id": contacto.id,
                    "nombre": (
                        f"{props.get('firstname', '')} {props.get('lastname', '')}"
                    ).strip(),
                    "email": props.get("email", ""),
                    "telefono": props.get("phone", ""),
                    "telefono_alterno": props.get("telefono_alterno_del_cliente", ""),
                    "direccion": props.get("direccion__fisica_", ""),  # FIX
                    "municipio": (
                        props.get("municipio_de_residencia", "")
                        or props.get("municipios_co__contacto_", "")
                    ),
                    "estado": (props.get("country", "") or props.get("state", "")),
                    "zip": props.get("zip", ""),
                    "id_cliente": id_cliente,
                    "fsd": "",
                }

                # Enriquecer con FSD: primero por id_cliente, fallback por contact_id
                if id_cliente and str(id_cliente).strip():
                    fsd = _buscar_fsd_por_id_cliente(str(id_cliente).strip())
                    candidato["fsd"] = fsd
                else:
                    fsd = _buscar_fsd_por_contact_id(contacto.id)
                    candidato["fsd"] = fsd

                candidatos.append(candidato)
            return candidatos

        except ContactApiException as e:
            print(f"[HubSpot] Error buscando contactos: {e}")
            return []


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================


def extraer_datos_hubspot(fsd: str):

    ticket_raw = _buscar_ticket_por_fsd(fsd)

    if not ticket_raw:

        return {"error": f"No existe ticket para FSD={fsd}"}

    tp = ticket_raw["props"]

    ticket_id = ticket_raw["ticket_id"]

    # =====================================================
    # SUBJECT
    # =====================================================

    asunto = _val(tp, _T_SUBJECT)

    parsed = _parsear_asunto(asunto)

    # =====================================================
    # ID GOFORMZ
    # =====================================================

    id_goformz = _val(tp, _T_ID_GOFORMZ) or parsed["id_cliente"]

    # =====================================================
    # CONTACTO
    # =====================================================

    contacto_raw = _buscar_contacto_por_id_goformz(id_goformz)

    cp = contacto_raw["props"] if contacto_raw else {}

    contact_id = contacto_raw["contact_id"] if contacto_raw else None

    # =====================================================
    # NOMBRE
    # =====================================================

    nombre_contacto = (f"{_val(cp, _C_FIRSTNAME)} " f"{_val(cp, _C_LASTNAME)}").strip()

    nombre_ticket = (f"{_val(tp, _T_FIRSTNAME)} " f"{_val(tp, _T_LASTNAME)}").strip()

    nombre = nombre_contacto or nombre_ticket

    nombre = _limpiar_nombre(nombre)

    # incorporar nombre parseado desde el subject si no existe aún
    try:
        parsed_nombre = parsed.get("nombre") if isinstance(parsed, dict) else None
        if not nombre and parsed_nombre:
            nombre = parsed_nombre
    except Exception:
        pass

    # =====================================================
    # RESULTADO
    # =====================================================

    return {
        "fsd": (_val(tp, _T_FSD) or parsed["fsd_parsed"] or fsd),
        "ticket_id": ticket_id,
        "contact_id": contact_id,
        "nombre": nombre,
        "id_cliente": (_val(cp, _C_ID_GOFORMZ) or id_goformz),
        "direccion": (_val(cp, _C_ADDRESS) or _val(tp, _T_ADDRESS)),
        "telefono": (_val(cp, _C_PHONE) or _val(tp, _T_PHONE)),
        "telefono_alterno": (_val(cp, _C_PHONE_ALT) or _val(tp, _T_PHONE_ALT)),
        "email": (_val(cp, _C_EMAIL) or _val(tp, _T_EMAIL)),
        "estado": (_val(cp, _C_STATE) or _val(cp, _C_STATE2) or _val(tp, _T_STATE)),
        "municipio": (
            _val(tp, _T_COUNTY) or _val(cp, _C_MUNICIPIO) or _val(cp, _C_MUNICIPIO_CO)
        ),
        "zip": (_val(cp, _C_ZIP) or _val(tp, _T_ZIP)),
        "nota": _val(tp, _T_NOTA),
        "error": None,
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    import sys

    fsd_test = sys.argv[1] if len(sys.argv) > 1 else "983316"

    datos = extraer_datos_hubspot(fsd_test)

    print()

    for k, v in datos.items():
        print(f"{k:<25}: {v}")

    print()

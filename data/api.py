# api.py
"""
Extracción estable de datos HubSpot.
NO contiene lógica de búsquedas múltiples.
"""

import logging
import os
import re
import sys as _sys
import config._env  # noqa: F401 — sets os.environ (dev: .env, prod: compiled)
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest as TicketSearchRequest
from hubspot.crm.contacts import PublicObjectSearchRequest as ContactSearchRequest
from hubspot.crm.tickets import ApiException as TicketApiException
from hubspot.crm.contacts import ApiException as ContactApiException
from data.hubspot_constants import (
    _T_FSD,
    _T_FIRSTNAME,
    _T_LASTNAME,
    _T_ID_GOFORMZ,
    _T_ADDRESS,
    _T_PHONE,
    _T_PHONE_ALT,
    _T_EMAIL,
    _T_COUNTY,
    _T_SUBJECT,
    _T_NOTA,
    _T_STATE,
    _T_ZIP,
    TICKET_PROPS,
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
    CONTACT_PROPS,
    SEARCH_CONTACT_FIELDS,
    SEARCH_EXACT_FIELDS,
)

logger = logging.getLogger(__name__)

# =========================================================
# Lazy singleton client
# =========================================================

_client = None


def _get_client() -> HubSpot:
    """Crea y cachea el cliente HubSpot autenticado con ACCESS_TOKEN.

    Implementa un singleton lazy: la primera llamada lee ACCESS_TOKEN de las
    variables de entorno (.env) y construye el cliente; las llamadas
    subsiguientes devuelven la misma instancia cacheada.

    Returns:
        Instancia autenticada de HubSpot.

    Raises:
        RuntimeError: si ACCESS_TOKEN no esta configurado en el .env.
    """
    global _client
    if _client is not None:
        return _client
    token = os.getenv("ACCESS_TOKEN") or ""
    if not token:
        raise RuntimeError(
            "ACCESS_TOKEN no configurado. "
            "Agrega ACCESS_TOKEN=<token> en el archivo .env del proyecto."
        )
    _client = HubSpot(access_token=token)
    return _client

# =========================================================
# HELPERS
# =========================================================


def _val(props: dict, key: str) -> str:
    """Extrae un valor de un dict de propiedades HubSpot de forma segura.

    Args:
        props: diccionario de propiedades (puede ser None).
        key: clave a buscar.

    Returns:
        Valor como string sin espacios al inicio/final. Vacio ("") si la
        clave no existe o el valor es None.
    """
    v = props.get(key) or ""
    return v.strip()


def _limpiar_nombre(nombre: str) -> str:
    """Limpia un nombre eliminando sufijos separados por barras.

    En HubSpot algunos nombres vienen con formato "Nombre / Apellido" o
    "Nombre/Apellido". Esta funcion toma solo la primera parte. Si el
    nombre esta vacio retorna cadena vacia.

    Args:
        nombre: string con el nombre completo potencialmente con barras.

    Returns:
        Nombre limpio sin sufijos separados por /.
    """
    if not nombre:
        return ""

    if " / " in nombre:
        nombre = nombre.split(" / ")[0]

    elif "/" in nombre:
        nombre = nombre.split("/")[0]

    return nombre.strip()


def _parsear_asunto(asunto: str) -> dict:
    """Extrae FSD, ID de cliente y nombre desde el asunto de un ticket.

    El asunto de los tickets de HubSpot sigue convenciones como
    "FSD-12345 Nombre Cliente ID:67890". Esta funcion aplica regex
    y heuristicas para extraer cada componente.

    Args:
        asunto: texto del campo subject del ticket.

    Returns:
        Dict con claves: fsd_parsed, id_cliente, nombre. Cada valor es
        un string (vacio si no se pudo extraer).
    """
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
# API WRAPPER - all HubSpot operations live here
# =========================================================


class HubSpotAPI:
    """Cliente HubSpot con todas las operaciones de busqueda y extraccion.

    Encapsula busquedas de tickets por FSD e ID de GoFormz, busquedas de
    contactos, extraccion de datos completos y enriquecimiento con FSD.

    Attributes:
        client: instancia autenticada del SDK de HubSpot.
    """

    def __init__(self, client=None):
        """
        Args:
            client: instancia de HubSpot. Si es None, se usa el singleton lazy
                    via _get_client() que lee ACCESS_TOKEN del .env.
        """
        self.client = client if client is not None else _get_client()

    # ── search primitives ──────────────────────────────────────

    def _buscar_ticket_por_fsd(self, fsd: str):
        """Busca un ticket de HubSpot por su numero FSD con multiples variantes.

        Prueba el FSD tal cual, en mayusculas, sin espacios, sin guiones,
        y solo los digitos. Itera las variantes hasta encontrar el ticket
        o agotar las opciones.

        Args:
            fsd: numero FSD en cualquier formato.

        Returns:
            Dict con ticket_id y props si se encuentra, None si no.
        """
        fsd_clean = fsd.strip()
        candidatos = [
            fsd_clean,
            fsd_clean.upper(),
            fsd_clean.replace(" ", ""),
            fsd_clean.upper().replace("-", ""),
        ]
        numeric_only = re.sub(r"\D", "", fsd_clean)
        if numeric_only:
            candidatos.append(numeric_only)
            candidatos.append(f"FSD-{numeric_only}")

        vistos = set()
        candidatos_finales = []
        for c in candidatos:
            if c not in vistos:
                vistos.add(c)
                candidatos_finales.append(c)

        for candidate in candidatos_finales:
            logger.info("Buscando ticket por FSD=%s", candidate)
            search_request = TicketSearchRequest(
                filter_groups=[{
                    "filters": [{
                        "propertyName": _T_FSD,
                        "operator": "EQ",
                        "value": candidate,
                    }]
                }],
                properties=TICKET_PROPS,
                limit=1,
            )
            try:
                response = self.client.crm.tickets.search_api.do_search(
                    public_object_search_request=search_request
                )
                if response.results:
                    ticket = response.results[0]
                    return {"ticket_id": ticket.id, "props": ticket.properties}
            except TicketApiException as e:
                logger.warning("Error buscando ticket FSD=%s: %s", candidate, e)
        return None

    def _buscar_contacto_por_id_goformz(self, id_goformz: str):
        """Busca un contacto en HubSpot por su ID de GoFormz.

        Args:
            id_goformz: ID de GoFormz del contacto.

        Returns:
            Dict con contact_id y props si se encuentra, None si no.
        """
        if not id_goformz:
            return None
        search_request = ContactSearchRequest(
            filter_groups=[{
                "filters": [{
                    "propertyName": _C_ID_GOFORMZ,
                    "operator": "EQ",
                    "value": id_goformz,
                }]
            }],
            properties=CONTACT_PROPS,
            limit=1,
        )
        try:
            response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )
            if not response.results:
                return None
            contact = response.results[0]
            return {"contact_id": contact.id, "props": contact.properties}
        except ContactApiException as e:
            logger.warning("Error buscando contacto: %s", e)
            return None

    def _buscar_ticket_por_id_goformz(self, id_goformz: str):
        """Busca tickets asociados a un ID de GoFormz, priorizando los que tienen FSD.

        Args:
            id_goformz: ID de GoFormz del ticket.

        Returns:
            Dict con ticket_id y props del mejor candidato, o None.
        """
        if not id_goformz:
            return None
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
                filter_groups=[{
                    "filters": [{
                        "propertyName": _T_ID_GOFORMZ,
                        "operator": "EQ",
                        "value": id_val,
                    }]
                }],
                properties=TICKET_PROPS,
                limit=10,
            )
            try:
                response = self.client.crm.tickets.search_api.do_search(
                    public_object_search_request=search_request
                )
                if not response.results:
                    continue
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
                logger.warning("Error buscando ticket por ID GoFormz=%s: %s", id_val, e)
        return None

    def buscar_fsd_por_id_cliente(self, id_cliente: str) -> str:
        """Busca el FSD asociado a un ID de cliente via sus tickets en HubSpot.

        Args:
            id_cliente: ID de GoFormz del cliente.

        Returns:
            FSD como string (vacio si no se encuentra).
        """
        if not id_cliente:
            return ""
        id_cliente_limpio = str(id_cliente).strip()
        if not id_cliente_limpio:
            return ""
        ticket = self._buscar_ticket_por_id_goformz(id_cliente_limpio)
        if not ticket:
            return ""
        props = ticket.get("props", {})
        fsd = props.get(_T_FSD, "")
        return str(fsd).strip() if fsd else ""

    def _buscar_fsd_por_contact_id(self, contact_id: str) -> str:
        """Busca el FSD del primer ticket asociado a un contacto en HubSpot.

        Usa la API de asociaciones v4 para encontrar tickets vinculados al
        contacto y extrae el FSD del primer resultado.

        Args:
            contact_id: ID interno de HubSpot del contacto.

        Returns:
            FSD como string (vacio si no se encuentra o falla la API).
        """
        if not contact_id:
            return ""
        contact_id_limpio = str(contact_id).strip()
        if not contact_id_limpio:
            return ""
        try:
            assoc_response = self.client.crm.associations.v4.basic_api.get_page(
                object_type="contacts",
                object_id=contact_id_limpio,
                to_object_type="tickets",
                limit=3,
            )
            if not assoc_response.results:
                return ""
            ticket_id = str(assoc_response.results[0].to_object_id)
            ticket = self.client.crm.tickets.basic_api.get_by_id(
                ticket_id=ticket_id,
                properties=[_T_FSD, _T_ID_GOFORMZ],
            )
            fsd = ticket.properties.get(_T_FSD, "")
            return str(fsd).strip() if fsd else ""
        except Exception as e:
            logger.warning("_buscar_fsd_por_contact_id(contact_id=%s): %s", contact_id, e)
            return ""

    def extraer_datos_hubspot(self, fsd: str):
        """Extrae todos los datos relevantes de un ticket de HubSpot por FSD.

        Busca el ticket, parsea el asunto, busca el contacto asociado por
        ID de GoFormz, y combina la informacion de ambas fuentes (ticket y
        contacto) en un solo dict.

        Args:
            fsd: numero FSD en cualquier formato.

        Returns:
            Dict con claves: fsd, ticket_id, contact_id, nombre, id_cliente,
            direccion, telefono, telefono_alterno, email, estado, municipio,
            zip, nota, fuente_nombre, fuente_id, error.
            La clave error es None si todo fue bien, o contiene el mensaje
            si algo fallo.
        """
        ticket_raw = self._buscar_ticket_por_fsd(fsd)
        if not ticket_raw:
            return {"error": f"No existe ticket para FSD={fsd}"}

        tp = ticket_raw["props"]
        ticket_id = ticket_raw["ticket_id"]
        asunto = _val(tp, _T_SUBJECT)
        parsed = _parsear_asunto(asunto)
        id_goformz = _val(tp, _T_ID_GOFORMZ) or parsed["id_cliente"]
        contacto_raw = self._buscar_contacto_por_id_goformz(id_goformz)
        cp = contacto_raw["props"] if contacto_raw else {}
        contact_id = contacto_raw["contact_id"] if contacto_raw else None

        nombre_contacto = (f"{_val(cp, _C_FIRSTNAME)} {_val(cp, _C_LASTNAME)}").strip()
        nombre_ticket = (f"{_val(tp, _T_FIRSTNAME)} {_val(tp, _T_LASTNAME)}").strip()
        nombre = nombre_contacto or nombre_ticket
        nombre = _limpiar_nombre(nombre)

        try:
            parsed_nombre = parsed.get("nombre") if isinstance(parsed, dict) else None
            if not nombre and parsed_nombre:
                nombre = parsed_nombre
        except Exception:
            pass

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


    def buscar_contactos_por_criterio(self, criterio, tipo_busqueda):
        """Busca contactos en HubSpot segun un criterio y tipo de busqueda.

        Para busquedas por FSD, delega en extraer_datos_hubspot(). Para otros
        tipos (nombre, apellido, telefono, correo, direccion, id_cliente),
        usa la API de busqueda de contactos con el operador adecuado (EQ para
        campos exactos, CONTAINS_TOKEN para texto) y enriquece cada resultado
        con su FSD asociado.

        Args:
            criterio: valor a buscar.
            tipo_busqueda: uno de "fsd", "nombre", "apellido", "telefono",
                           "correo", "direccion", "id_cliente".

        Returns:
            Lista de dicts con los contactos encontrados y sus FSD asociados.
        """
        if tipo_busqueda == "fsd":
            datos = self.extraer_datos_hubspot(criterio)
            if datos.get("error"):
                return []
            return [datos]

        field = SEARCH_CONTACT_FIELDS.get(tipo_busqueda)
        if not field:
            return []

        query = str(criterio).strip()
        if not query:
            return []

        operator = "EQ" if tipo_busqueda in SEARCH_EXACT_FIELDS else "CONTAINS_TOKEN"

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
                "direccion__fisica_",
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
                    "direccion": props.get("direccion__fisica_", ""),
                    "municipio": (
                        props.get("municipio_de_residencia", "")
                        or props.get("municipios_co__contacto_", "")
                    ),
                    "estado": (props.get("country", "") or props.get("state", "")),
                    "zip": props.get("zip", ""),
                    "id_cliente": id_cliente,
                    "fsd": "",
                }

                if id_cliente and str(id_cliente).strip():
                    fsd = self.buscar_fsd_por_id_cliente(str(id_cliente).strip())
                    candidato["fsd"] = fsd
                else:
                    fsd = self._buscar_fsd_por_contact_id(contacto.id)
                    candidato["fsd"] = fsd

                candidatos.append(candidato)
            return candidatos

        except ContactApiException as e:
            logger.warning("Error buscando contactos: %s", e)
            return []


# =========================================================
# Backward-compatible module-level wrappers
# =========================================================

def buscar_fsd_por_id_cliente(id_cliente: str) -> str:
    """Wrapper retrocompatible. Preferir HubSpotAPI().buscar_fsd_por_id_cliente().

    Args:
        id_cliente: ID de GoFormz del cliente.

    Returns:
        FSD como string, o vacio si no se encuentra.
    """
    return HubSpotAPI().buscar_fsd_por_id_cliente(id_cliente)


def extraer_datos_hubspot(fsd: str):
    """Wrapper retrocompatible. Preferir HubSpotAPI().extraer_datos_hubspot().

    Args:
        fsd: numero FSD en cualquier formato.

    Returns:
        Dict con todos los datos del ticket y contacto asociado.
    """
    return HubSpotAPI().extraer_datos_hubspot(fsd)


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

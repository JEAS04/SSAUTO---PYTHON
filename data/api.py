"""
 api.py — Extracción de datos desde HubSpot
============================================
Flujo principal:
  1. Buscar ticket por FSD  →  _buscar_ticket_por_fsd()
  2. Parsear subject como fallback  →  _parsear_asunto()
  3. Buscar contacto vinculado por id_goformz  →  _buscar_contacto_por_id_goformz()
  4. Combinar todo (atributo directo gana sobre subject)  →  extraer_datos_hubspot()

La función pública es:
    extraer_datos_hubspot(fsd: str) -> dict

Devuelve un dict con claves estandarizadas listo para comparador.py.
"""

import os
import re
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest as TicketSearchRequest
from hubspot.crm.tickets import ApiException as TicketApiException
from hubspot.crm.contacts import PublicObjectSearchRequest as ContactSearchRequest
from hubspot.crm.contacts import ApiException as ContactApiException

# ──────────────────────────────────────────────
# Inicialización del cliente
# ──────────────────────────────────────────────
load_dotenv()
_token = os.getenv("ACCESS_TOKEN")
_client = HubSpot(access_token=_token)

# ──────────────────────────────────────────────
# Nombres internos de propiedades en HubSpot
# ──────────────────────────────────────────────

# TICKET
_T_FSD = "fsd__"
_T_FIRSTNAME = "firstname"  # algunos tickets lo tienen
_T_LASTNAME = "lastname"
_T_ID_GOFORMZ = "id_goformz__servicios_tecnicos_"
_T_ADDRESS = "physical_address"
_T_PHONE = "phone"
_T_EMAIL = "e_mail"
_T_COUNTY = "pueblo_para_servicio_tecnico"
_T_SUBJECT = "subject"
_T_NOTA = "nota_ticket__sac_"  # ajusta si "nota" tiene otro nombre interno
_T_PHONE_ALT = "telefono_alterno"
_T_STATE = "state"
_T_ZIP = "zip"
_T_CITY = "city"

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
    _T_CITY,
    _T_NOTA,
]

# CONTACTO
_C_FIRSTNAME = "firstname"
_C_LASTNAME = "lastname"
_C_ID_GOFORMZ = "id_de_goformz__contacto_"
_C_ADDRESS = "direccion__fisica_"
_C_PHONE = "phone"
_C_PHONE_ALT = "telefono_alterno_del_cliente"
_C_EMAIL = "email"
_C_STATE = "country"  # "Estado" está en el campo country
_C_MUNICIPIO = "municipio_de_residencia"
_C_MUNICIPIO_CO = "municipios_co__contacto_"
_C_STATE2 = "state"
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
    _C_MUNICIPIO,
    _C_MUNICIPIO_CO,
    _C_STATE2,
    _C_ZIP,
]

# ──────────────────────────────────────────────
# Municipios de Puerto Rico (para parseo del subject)
# ──────────────────────────────────────────────
_MUNICIPIOS_PR = [
    "Adjuntas",
    "Aguada",
    "Aguadilla",
    "Aguas Buenas",
    "Aibonito",
    "Añasco",
    "Arecibo",
    "Arroyo",
    "Barceloneta",
    "Barranquitas",
    "Bayamón",
    "Cabo Rojo",
    "Caguas",
    "Camuy",
    "Canóvanas",
    "Carolina",
    "Cataño",
    "Cayey",
    "Ceiba",
    "Ciales",
    "Cidra",
    "Coamo",
    "Comerío",
    "Corozal",
    "Culebra",
    "Dorado",
    "Fajardo",
    "Florida",
    "Guánica",
    "Guayama",
    "Guayanilla",
    "Guaynabo",
    "Gurabo",
    "Hatillo",
    "Hormigueros",
    "Humacao",
    "Isabela",
    "Jayuya",
    "Juana Díaz",
    "Juncos",
    "Lajas",
    "Lares",
    "Las Marías",
    "Las Piedras",
    "Loíza",
    "Luquillo",
    "Manatí",
    "Maricao",
    "Maunabo",
    "Mayagüez",
    "Moca",
    "Morovis",
    "Naguabo",
    "Naranjito",
    "Orocovis",
    "Patillas",
    "Peñuelas",
    "Ponce",
    "Quebradillas",
    "Rincón",
    "Río Grande",
    "Sabana Grande",
    "Salinas",
    "San Germán",
    "San Juan",
    "San Lorenzo",
    "San Sebastián",
    "Santa Isabel",
    "Toa Alta",
    "Toa Baja",
    "Trujillo Alto",
    "Utuado",
    "Vega Alta",
    "Vega Baja",
    "Vieques",
    "Villalba",
    "Yabucoa",
    "Yauco",
]

_COMENTARIOS_KEYWORDS = [
    "sininfo",
    "sin info",
    "sin produccion",
    "sin producción",
    "verificar",
    "metering",
    "upgrade",
    "bateria",
    "batería",
    "gateway",
    "not reporting",
    "down",
    "error",
    "issue",
    "problema",
    "falla",
    "reparacion",
    "reparación",
    "mantenimiento",
    "pendiente",
]

# Ordenados largo→corto para que "San Juan" gane sobre "Juan"
_MUNICIPIOS_SORTED = sorted(_MUNICIPIOS_PR, key=len, reverse=True)


def _norm(texto: str) -> str:
    """Minúsculas + elimina tildes."""
    for src, dst in zip("áéíóúüñàèìòùÁÉÍÓÚÜÑ", "aeiouunaeiouAEIOUUN"):
        texto = texto.replace(src, dst)
    return texto.lower()


_MUNICIPIOS_NORM = {_norm(m): m for m in _MUNICIPIOS_SORTED}


def _detectar_municipio(asunto: str) -> str:
    """Detecta el municipio de PR dentro del subject."""
    asunto_norm = _norm(asunto)
    for norm, original in _MUNICIPIOS_NORM.items():
        patron = r"(?<![a-z])" + re.escape(norm) + r"(?![a-z])"
        if re.search(patron, asunto_norm):
            return original
    return ""


def _parsear_asunto(asunto: str) -> dict:
    """..."""
    texto = asunto
    print(f"\n[DEBUG] Input: {asunto}")

    # 1. Extraer FSD
    fsd_parsed = ""
    m_fsd = re.search(r"\bFSD[-\s]*(\d+)\b", texto, re.IGNORECASE)
    if m_fsd:
        fsd_parsed = m_fsd.group(1)
        texto = texto[: m_fsd.start()] + texto[m_fsd.end() :]
        print(f"[DEBUG] Tras quitar FSD: {texto}")

    # 2. Extraer ID cliente
    id_cliente = ""
    m_id = re.search(r"\bID\s*(\d{4,})\b", texto, re.IGNORECASE)
    if m_id:
        id_cliente = m_id.group(1)
        texto = texto[: m_id.start()] + texto[m_id.end() :]
    else:
        m_num = re.search(r"\b(\d{4,})\b", texto)
        if m_num:
            id_cliente = m_num.group(1)
            texto = texto[: m_num.start()] + texto[m_num.end() :]
    print(f"[DEBUG] Tras quitar ID {id_cliente}: {texto}")

    # 3. Detectar municipio
    municipio = _detectar_municipio(texto)
    if municipio:
        texto = re.sub(
            r"\b" + re.escape(municipio) + r"\b", "", texto, flags=re.IGNORECASE
        )
    print(f"[DEBUG] Tras quitar municipio: {texto}")

    # 4. Quitar comentarios
    for keyword in _COMENTARIOS_KEYWORDS:
        patron = r"\b" + re.escape(keyword) + r"\b"
        m = re.search(patron, texto, re.IGNORECASE)
        if m:
            print(f"[DEBUG] Encontrado keyword '{keyword}' en posición {m.start()}")
            texto = texto[: m.start()]
            break
    print(f"[DEBUG] Tras quitar comentarios: {texto}")

    # 5. Limpiar
    texto = re.sub(r"[-\\|]+", " ", texto)
    print(f"[DEBUG] Tras limpiar separadores: {texto}")

    texto = re.sub(r"\b\d+\b", "", texto)
    print(f"[DEBUG] Tras quitar números: {texto}")

    texto = re.sub(r"\s+", " ", texto).strip()
    print(f"[DEBUG] Tras colapsar espacios: {texto}")

    nombre = texto.title() if texto else ""
    print(f"[DEBUG] Nombre final: {nombre}\n")

    return {
        "fsd_parsed": fsd_parsed,
        "nombre": nombre,
        "id_cliente": id_cliente,
        "municipio": municipio,
    }


# ──────────────────────────────────────────────
# Helpers internos HubSpot
# ──────────────────────────────────────────────


def _val(props: dict, key: str) -> str:
    """Devuelve el valor limpio de una propiedad o cadena vacía."""
    v = props.get(key) or ""
    return v.strip()


def _buscar_ticket_por_fsd(fsd: str) -> dict | None:
    """
    Busca el ticket en HubSpot cuyo campo fsd__ coincide exactamente.
    Devuelve el dict de propiedades raw + ticket_id, o None si no existe.

    Acepta cualquier formato de FSD (FSD-1236711, FSD1236711, 1236711, etc.)
    y prueba múltiples variaciones hasta encontrar el ticket.
    """
    fsd_clean = fsd.strip()

    # ── 1. Generar variaciones candidatas ──────────────────────────────────
    candidates = []

    # (a) Entrada original
    candidates.append(fsd_clean)

    # (b) En mayúsculas
    candidates.append(fsd_clean.upper())

    # (c) Sin espacios
    candidates.append(fsd_clean.replace(" ", ""))

    # (d) Sin guion (en mayúsculas)
    candidates.append(fsd_clean.upper().replace("-", ""))

    # (e) Solo números
    numeric_only = re.sub(r"\D", "", fsd_clean)
    if numeric_only:
        candidates.append(numeric_only)

    # (f) Formateado como FSD-<número>
    if numeric_only:
        candidates.append(f"FSD-{numeric_only}")

    # Eliminar duplicados preservando orden
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    # ── 2. Probar cada variación secuencialmente ───────────────────────────
    for candidate in unique_candidates:
        print(f"[HubSpot] Buscando ticket con FSD='{candidate}'")

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
            page = _client.crm.tickets.search_api.do_search(
                public_object_search_request=search_request
            )
            if page.results:
                ticket = page.results[0]
                print(
                    f"[HubSpot] ✓ Ticket encontrado con FSD='{candidate}' "
                    f"(id={ticket.id})"
                )
                return {"ticket_id": ticket.id, "props": ticket.properties}
        except TicketApiException as e:
            print(f"[HubSpot] Error buscando FSD='{candidate}': {e}")

    # ── 3. Ninguna variación dio resultado ─────────────────────────────────
    print(
        f"[HubSpot] ✗ No se encontró ningún ticket para FSD='{fsd_clean}' "
        f"(variaciones probadas: {unique_candidates})"
    )
    return None


def _buscar_contacto_por_id_goformz(id_goformz: str) -> dict | None:
    """
    Busca el contacto cuyo id_de_goformz__contacto_ coincide con id_goformz.
    Devuelve el dict de propiedades raw + contact_id, o None si no existe.
    """
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
        page = _client.crm.contacts.search_api.do_search(
            public_object_search_request=search_request
        )
        if not page.results:
            return None
        contact = page.results[0]
        return {"contact_id": contact.id, "props": contact.properties}

    except ContactApiException as e:
        print(f"[HubSpot] Error buscando contacto id_goformz={id_goformz}: {e}")
        return None


def _limpiar_nombre_hubspot(nombre: str) -> str:
    """
    Limpia nombres que vienen de HubSpot con formatos raros.
    Ej: "Dennis Ayala / DENIS AYALA" → "Dennis Ayala"
        "Juan / Perez" → "Juan Perez"
    """
    if not nombre:
        return ""

    # Si hay barra, tomar la PRIMERA parte (nombre principal)
    if " / " in nombre:
        nombre = nombre.split(" / ")[0].strip()
    elif "/" in nombre:
        nombre = nombre.split("/")[0].strip()

    return nombre


# ──────────────────────────────────────────────
# Función pública principal
# ──────────────────────────────────────────────


def extraer_datos_hubspot(fsd: str) -> dict:
    """
    Extrae y unifica los datos de un ticket y su contacto relacionado.

    Regla de prioridad (campo por campo):
        1. Atributo directo del CONTACTO  (más completo y confiable)
        2. Atributo directo del TICKET
        3. Valor parseado del subject      (fallback)

    Parámetros
    ----------
    fsd : str
        Número FSD con o sin prefijo ("FSD983316" o "983316").

    Devuelve
    --------
    dict con las siguientes claves estandarizadas:
        fsd, ticket_id, contact_id,
        nombre, id_cliente,
        direccion, telefono, telefono_alterno,
        email, estado, municipio, zip,
        nota,
        fuente_nombre, fuente_id,      ← indica de dónde vino cada dato clave
        error                          ← None si todo OK, mensaje si hubo problema
    """

    # ── 1. Buscar ticket ──────────────────────────────────────────────────
    ticket_raw = _buscar_ticket_por_fsd(fsd)
    if ticket_raw is None:
        return {
            "fsd": fsd,
            "ticket_id": None,
            "contact_id": None,
            "nombre": "",
            "id_cliente": "",
            "direccion": "",
            "telefono": "",
            "telefono_alterno": "",
            "email": "",
            "estado": "",
            "municipio": "",
            "zip": "",
            "nota": "",
            "fuente_nombre": "",
            "fuente_id": "",
            "error": f"No se encontró ticket con FSD={fsd}",
        }

    tp = ticket_raw["props"]
    ticket_id = ticket_raw["ticket_id"]

    # ── 2. Parsear subject como fallback ──────────────────────────────────
    asunto = _val(tp, _T_SUBJECT)
    parsed = _parsear_asunto(asunto)

    # ── 3. Obtener id_goformz del ticket (atributo directo o del subject) ─
    id_goformz_ticket = _val(tp, _T_ID_GOFORMZ) or parsed["id_cliente"]

    # ── 4. Buscar contacto relacionado ────────────────────────────────────
    contacto_raw = _buscar_contacto_por_id_goformz(id_goformz_ticket)
    cp = contacto_raw["props"] if contacto_raw else {}
    contact_id = contacto_raw["contact_id"] if contacto_raw else None

    # ── 5. Helpers de selección con trazabilidad ─────────────────────────
    def primero(*pares) -> tuple[str, str]:
        """
        Recibe pares (valor, etiqueta_fuente).
        Devuelve el primer par cuyo valor no esté vacío.
        """
        for valor, fuente in pares:
            if valor:
                return valor, fuente
        return "", "no encontrado"

    # ── 6. Construir nombre ───────────────────────────────────────────────
    nombre_contacto = f"{_val(cp, _C_FIRSTNAME)} {_val(cp, _C_LASTNAME)}".strip()
    nombre_ticket = f"{_val(tp, _T_FIRSTNAME)} {_val(tp, _T_LASTNAME)}".strip()
    nombre, fuente_nombre = primero(
        (nombre_contacto, "contacto"),
        (nombre_ticket, "ticket"),
        (parsed["nombre"], "subject"),
    )
    nombre = _limpiar_nombre_hubspot(nombre)
    # ── 7. Construir id_cliente ───────────────────────────────────────────
    id_cliente, fuente_id = primero(
        (_val(cp, _C_ID_GOFORMZ), "contacto"),
        (id_goformz_ticket, "ticket"),
        (parsed["id_cliente"], "subject"),
    )

    # ── 8. Resto de campos (contacto > ticket > subject/vacío) ───────────
    direccion, _ = primero(
        (_val(cp, _C_ADDRESS), "contacto"),
        (_val(tp, _T_ADDRESS), "ticket"),
    )
    telefono, _ = primero(
        (_val(cp, _C_PHONE), "contacto"),
        (_val(tp, _T_PHONE), "ticket"),
    )
    telefono_alterno, _ = primero(
        (_val(cp, _C_PHONE_ALT), "contacto"),
        (_val(tp, _T_PHONE_ALT), "ticket"),
    )

    email, _ = primero(
        (_val(cp, _C_EMAIL), "contacto"),
        (_val(tp, _T_EMAIL), "ticket"),
    )

    # Estado: campo country del contacto, o state como alternativa
    estado, _ = primero(
        (_val(cp, _C_STATE), "contacto.country"),
        (_val(cp, _C_STATE2), "contacto.state"),
        (_val(tp, _T_STATE), "ticket"),
    )

    # Municipio: atributo directo del ticket, luego contacto, luego subject
    municipio, _ = primero(
        (_val(tp, _T_COUNTY), "ticket"),
        (_val(cp, _C_MUNICIPIO), "contacto"),
        (_val(cp, _C_MUNICIPIO_CO), "contacto_co"),
        (parsed["municipio"], "subject"),
    )

    zip_code, _ = primero(
        (_val(cp, _C_ZIP), "contacto"),
        (_val(tp, _T_ZIP), "ticket"),
    )

    # FSD canónico (del atributo directo del ticket)
    fsd_canon = _val(tp, _T_FSD) or parsed["fsd_parsed"] or fsd

    nota = _val(tp, _T_NOTA)

    # ── 9. Resultado final ────────────────────────────────────────────────
    return {
        # Identificadores
        "fsd": fsd_canon,
        "ticket_id": ticket_id,
        "contact_id": contact_id,
        # Datos del cliente
        "nombre": nombre,
        "id_cliente": id_cliente,
        "direccion": direccion,
        "telefono": telefono,
        "telefono_alterno": telefono_alterno,
        "email": email,
        "estado": estado,
        "municipio": municipio,
        "zip": zip_code,
        "nota": nota,
        # Metadatos de trazabilidad
        "fuente_nombre": fuente_nombre,
        "fuente_id": fuente_id,
        # Control de errores
        "error": None,
    }


def extraer_ticket_por_fsd(fsd: str) -> dict:
    """
    Alias de compatibilidad para ventana_comparacion.py.
    """
    return extraer_datos_hubspot(fsd)


# ──────────────────────────────────────────────
# Bloque de prueba rápida (python  api.py)
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    fsd_test = sys.argv[1] if len(sys.argv) > 1 else "983316"
    print(f"\nBuscando FSD: {fsd_test}\n")
    datos = extraer_datos_hubspot(fsd_test)
    ancho = 30
    for k, v in datos.items():
        print(f"  {k:<{ancho}}: {v}")
    print()

import os
import re
from dotenv import load_dotenv
from hubspot import HubSpot
from hubspot.crm.tickets import PublicObjectSearchRequest, ApiException

load_dotenv()
token = os.getenv("ACCESS_TOKEN")
client = HubSpot(access_token=token)

MUNICIPIOS_PR = [
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

# Pre-compilamos para máxima velocidad
# Ordenados de mayor a menor para que "San Juan" gane sobre "Juan"
_MUNICIPIOS_SORTED = sorted(MUNICIPIOS_PR, key=len, reverse=True)


def _norm(texto: str) -> str:
    """Minúsculas + quita tildes."""
    for a, b in zip("áéíóúüñàèìòù", "aeiouunaeiou"):
        texto = texto.replace(a, b)
    return texto.lower()


_MUNICIPIOS_NORM = {_norm(m): m for m in _MUNICIPIOS_SORTED}


def detectar_municipio(asunto: str) -> str:
    asunto_norm = _norm(asunto)
    for norm, original in _MUNICIPIOS_NORM.items():
        # \b no funciona bien con tildes, usamos lookahead/lookbehind manual
        patron = r"(?<![a-z])" + re.escape(norm) + r"(?![a-z])"
        if re.search(patron, asunto_norm):
            return original
    return "No detectado"


def parsear_asunto(asunto: str, municipio: str) -> tuple[str, str]:
    """
    Extrae nombre e ID cliente del asunto.
    Elimina: FSD######, el municipio, prefijos ID, números sueltos.
    Lo que queda de texto puro = nombre.
    """
    texto = asunto

    # 1. Quitar el bloque FSD (ej: "FSD983316")
    texto = re.sub(r"\bFSD[-\s]*\d*\b", "", texto, flags=re.IGNORECASE)

    # 2. Extraer ID cliente: "ID 250630" o número de 4+ dígitos solo
    id_cliente = "No encontrado"
    match_id = re.search(r"\bID\s*(\d{4,})\b", texto, re.IGNORECASE)
    if match_id:
        id_cliente = match_id.group(1)
        texto = texto[: match_id.start()] + texto[match_id.end() :]
    else:
        match_num = re.search(r"\b(\d{4,})\b", texto)
        if match_num:
            id_cliente = match_num.group(1)
            texto = texto[: match_num.start()] + texto[match_num.end() :]

    # 3. Quitar municipio (case-insensitive, con tildes o sin ellas)
    if municipio != "No detectado":
        texto = re.sub(re.escape(_norm(municipio)), "", _norm(texto))
        # Trabajamos sobre texto normalizado desde aquí para la limpieza
    else:
        texto = _norm(texto)

    # 4. Quitar separadores, dígitos sueltos y espacios extra
    texto = re.sub(r"[-|/\\]+", " ", texto)
    texto = re.sub(r"\b\d+\b", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto).strip()

    # 5. Capitalizar cada palabra del nombre
    nombre = texto.title() if texto else "No encontrado"

    return nombre, id_cliente


def extraer_tickets():
    NOMBRE_INTERNO_FSD = "fsd__"

    search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {"propertyName": NOMBRE_INTERNO_FSD, "operator": "HAS_PROPERTY"}
                ]
            }
        ],
        properties=["subject", NOMBRE_INTERNO_FSD, "hs_object_id"],
        limit=10,
    )

    try:
        results_page = client.crm.tickets.search_api.do_search(
            public_object_search_request=search_request
        )

        if not results_page.results:
            print("No se encontraron tickets con FSD lleno.")
            return

        ancho = 95
        print("\n" + "═" * ancho)
        print(
            f"  {'TICKET ID':<14} │ {'FSD':<12} │ {'NOMBRE':<25} │ {'MUNICIPIO':<16} │ {'ID CLIENTE'}"
        )
        print("═" * ancho)

        for ticket in results_page.results:
            p = ticket.properties
            asunto = p.get("subject", "")
            fsd = p.get(NOMBRE_INTERNO_FSD, "N/A")
            ticket_id = ticket.id

            municipio = detectar_municipio(asunto)
            nombre, id_cliente = parsear_asunto(asunto, municipio)

            print(
                f"  {ticket_id:<14} │ "
                f"{fsd:<12} │ "
                f"{nombre[:25]:<25} │ "
                f"{municipio[:16]:<16} │ "
                f"{id_cliente}"
            )

        print("═" * ancho)
        print(f"  Total: {len(results_page.results)} tickets\n")

    except ApiException as e:
        print(f"❌ Error de API: {e}")


def extraer_ticket_por_fsd(fsd: str) -> dict | None:
    """
    Busca en HubSpot el ticket cuyo campo FSD coincide con el valor dado.

    Parámetros
    ----------
    fsd : string con el número FSD, con o sin prefijo (ej: "FSD983316" o "983316").

    Devuelve
    --------
    dict con claves: fsd, nombre, id_cliente, municipio, ticket_id
    None si no se encuentra ningún ticket con ese FSD.
    """
    from hubspot.crm.tickets import PublicObjectSearchRequest, ApiException

    # Normalizar: quitar el prefijo FSD si viene incluido y cualquier guión
    fsd_numero = fsd.upper().replace("FSD", "").replace("-", "").strip()

    NOMBRE_INTERNO_FSD = "fsd__"

    # Búsqueda exacta por el valor del campo FSD
    search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "propertyName": NOMBRE_INTERNO_FSD,
                        "operator": "EQ",  # igual exacto
                        "value": fsd_numero,
                    }
                ]
            }
        ],
        properties=["subject", NOMBRE_INTERNO_FSD, "hs_object_id"],
        limit=1,  # solo necesitamos el primero que coincida
    )

    try:
        results_page = client.crm.tickets.search_api.do_search(
            public_object_search_request=search_request
        )

        if not results_page.results:
            return None  # No se encontró

        ticket = results_page.results[0]
        p = ticket.properties
        asunto = p.get("subject", "")
        fsd_real = p.get(NOMBRE_INTERNO_FSD, fsd_numero)

        municipio = detectar_municipio(asunto)
        nombre, id_cliente = parsear_asunto(asunto, municipio)

        return {
            "fsd": fsd_real,
            "nombre": nombre,
            "id_cliente": id_cliente,
            "municipio": municipio,
            "ticket_id": ticket.id,
            "asunto": asunto,
            "error": None,
        }

    except ApiException as e:
        print(f"[HubSpot API] Error al buscar FSD {fsd}: {e}")
        return {
            "fsd": fsd_numero,
            "nombre": "No encontrado",
            "id_cliente": "No encontrado",
            "municipio": "No detectado",
            "ticket_id": None,
            "asunto": "",
            "error": str(e),
        }


# from hubspot.crm.properties import ApiException

# props = client.crm.properties.core_api.get_all(object_type="tickets")

# for p in props.results:
#     print(p.name, "-", p.label)

from hubspot.crm.properties import ApiException

props = client.crm.properties.core_api.get_all(object_type="contacts")

for p in props.results:
    print(p.name, "-", p.label)

if __name__ == "__main__":
    extraer_tickets()


# necesito usar ciertos atributos que ya tengo anotados y usarlos para la comparacion con el scraping de SUNRUN, los usuarios de CONTACTO se identifican por id_de_goformz__contacto_ (id cliente), ademas en el nombre del ticket (subject) esta el fsd__ de ticket, nombre apellido (firstname, lastname) de contacto, id_goformz__servicios_tecnicos_ (id cliente) de contacto y una nota (notas), todo esto puede estar en la api con los mismos atributos, ademas tambien necesito el atributo municipio(pueblo_para_servicio_tecnico), Ticket ID o id de ticket (hs_ticket_id) y id de registro o Record ID (hs_object_id). Cabe resaltar que en el subject, en algunos tickets si esta toda esa informacion pero en otros se encuentra incompleta, la unica forma de identificar a ambos es por su id de GOFORMZ: id_de_goformz__contacto_ y id_goformz__servicios_tecnicos_ - ID GoFormz (Servicios Tecnicos)

# tampoco
# no me esta realizando la busqueda por fsd-000000, ni fsd000000, deberia admitir ambos y hasta sin la palabra fsd escrita, tampoco me esta usando el chrome ya abierto (default), y por lo tanto tampoco hace el web scraping a SUNRUN. Cabe recalcar que ya tengo la sesion abierta en chrome y comprobe que la http://localhost:9222/json/version dijera "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/a5b8b551-c718-42fc-8d09-028825ae09f4" y TCP 127.0.0.1:9222 LISTENING -> TCP    127.0.0.1:9222         0.0.0.0:0              LISTENING       13928
# Nombre de imagen               PID Nombre de sesión Núm. de ses Uso de memor
# ========================= ======== ================ =========== ============
# chrome.exe                   13928 Console                    6   191,196 KB pero no se abre el chrome que ya tengo abierto para eso, se abre uno nuevo o no carga nada del web scraping

# bro, esto me imprime un monton de atributos o propiedades de TICKET, no esta mal, me sirve para ver que atributos tiene pero si son un monton XD
# from hubspot.crm.properties import ApiException

# props = client.crm.properties.core_api.get_all(object_type="tickets")

# for p in props.results:
#     print(p.name, "-", p.label)

# necesito usar ciertos atributos que ya tengo anotados y usarlos para la comparacion con el scraping de SUNRUN, los usuarios de CONTACTO se identifican por id_de_goformz__contacto_ (id cliente), ademas en el nombre del ticket (subject) esta el fsd__ de ticket, nombre apellido (firstname, lastname) de contacto, id_goformz__servicios_tecnicos_ (id cliente) de contacto y una nota (notas), todo esto puede estar en la api con los mismos atributos, ademas tambien necesito el atributo municipio(pueblo_para_servicio_tecnico), Ticket ID o id de ticket (hs_ticket_id) y id de registro o Record ID (hs_object_id). Cabe resaltar que en el subject, en algunos tickets si esta toda esa informacion pero en otros se encuentra incompleta, la unica forma de identificar a ambos es por su id de GOFORMZ: id_de_goformz__contacto_ y id_goformz__servicios_tecnicos_ - ID GoFormz (Servicios Tecnicos)


# #tampoco
# # no me esta realizando la busqueda por fsd-000000, ni fsd000000, deberia admitir ambos y hasta sin la palabra fsd escrita, tampoco me esta usando el chrome ya abierto (default), y por lo tanto tampoco hace el web scraping a SUNRUN. Cabe recalcar que ya tengo la sesion abierta en chrome y comprobe que la http://localhost:9222/json/version dijera "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/a5b8b551-c718-42fc-8d09-028825ae09f4" y TCP 127.0.0.1:9222 LISTENING -> TCP    127.0.0.1:9222         0.0.0.0:0              LISTENING       13928
# # Nombre de imagen               PID Nombre de sesión Núm. de ses Uso de memor
# # ========================= ======== ================ =========== ============
# # chrome.exe                   13928 Console                    6   191,196 KB pero no se abre el chrome que ya tengo abierto para eso, se abre uno nuevo o no carga nada del web scraping

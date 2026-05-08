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


if __name__ == "__main__":
    extraer_tickets()

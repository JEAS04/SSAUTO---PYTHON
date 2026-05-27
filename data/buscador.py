# buscador.py
"""
Búsquedas adicionales HubSpot.

NO altera api.py
NO mezcla arquitecturas
NO usa clases innecesarias
"""

from data.api import HubSpotAPI, _buscar_fsd_por_id_cliente

# =========================================================
# CONFIG
# =========================================================

SEARCH_STRATEGIES = {
    "fsd": {
        "field": "fsd__",
        "label": "FSD",
        "input_count": 1,
        "placeholder": "Ej: 983316",
    },
    "nombre": {
        "field": "firstname",
        "label": "Nombre",
        "input_count": 1,
        "placeholder": "Ej: Juan",
    },
    "apellido": {
        "field": "lastname",
        "label": "Apellido",
        "input_count": 1,
        "placeholder": "Ej: Pérez",
    },
    "telefono": {
        "field": "phone",
        "label": "Teléfono",
        "input_count": 1,
        "placeholder": "Ej: +17872979317",
    },
    "correo": {
        "field": "email",
        "label": "Correo electrónico",
        "input_count": 1,
        "placeholder": "Ej: contacto@ejemplo.com",
    },
    "direccion": {
        "field": "address",
        "label": "Dirección",
        "input_count": 1,
        "placeholder": "Ej: San Juan",
    },
    "id_cliente": {
        "field": "id_de_goformz__contacto_",
        "label": "ID Cliente",
        "input_count": 1,
        "placeholder": "Ej: 1234",
    },
}

# =========================================================
# BUSCAR CONTACTOS
# =========================================================


def buscar_contactos(
    valor: str,
    tipo_busqueda: str,
):
    """
    Busca contactos según criterio y enriquece con FSD si aplica.

    Args:
        valor: valor a buscar
        tipo_busqueda: tipo de búsqueda (fsd, nombre, apellido, etc)

    Returns:
        Lista de candidatos enriquecidos con FSD
    """

    estrategia = SEARCH_STRATEGIES.get(tipo_busqueda)
    if not estrategia:
        return []

    api = HubSpotAPI()
    candidatos = api.buscar_contactos_por_criterio(valor, tipo_busqueda)

    # Enriquecer con FSD para cada candidato
    for candidato in candidatos:
        id_cliente = candidato.get("id_cliente")

        # Solo buscar FSD si hay un id_cliente válido
        if id_cliente and str(id_cliente).strip():
            try:
                fsd = _buscar_fsd_por_id_cliente(str(id_cliente).strip())
                if fsd:
                    candidato["fsd"] = fsd
                else:
                    candidato["fsd"] = ""
            except Exception as e:
                print(
                    f"[ERROR] No se pudo extraer FSD para id_cliente={id_cliente}: {e}"
                )
                candidato["fsd"] = ""
        else:
            candidato["fsd"] = ""

    return candidatos

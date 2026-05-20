"""
Script para ver la estructura del JSON de un ticket de HubSpot.
Uso: python ver_estructura_ticket.py <ticket_id>
"""

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

TICKET_API_URL = "https://api.hubapi.com/crm/v3/objects/tickets"
token = os.getenv("ACCESS_TOKEN")


def print_json_structure(data, indent=0):
    """Recorre el JSON e imprime las claves y tipos de cada campo."""
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"{prefix}|-- {key}: {{")
                print_json_structure(value, indent + 1)
                print(f"{prefix}|-- }}")
            elif isinstance(value, list):
                print(f"{prefix}|-- {key}: [")
                if value:
                    print(f"{prefix}|--   (lista de {len(value)} elemento(s))")
                    print_json_structure(value[0], indent + 2)
                print(f"{prefix}|-- ]")
            else:
                tipo = type(value).__name__
                print(f"{prefix}|-- {key}: ({tipo}) = {repr(value)}")
    elif isinstance(data, list):
        for i, item in enumerate(data[:3]):
            print(f"{prefix}|-- [{i}]:")
            print_json_structure(item, indent + 1)
        if len(data) > 3:
            print(f"{prefix}|-- ... y {len(data) - 3} más")
    else:
        print(f"{prefix}|-- {repr(data)}")


def main(ticket_id: str):

    if not token:
        print("ERROR: No se encontró ACCESS_TOKEN en el archivo .env")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{TICKET_API_URL}/{ticket_id}"

    try:
        response = requests.get(url, headers=headers)

        print(f"Status Code: {response.status_code}\n")

        if response.status_code == 401:
            print("ERROR: Token inválido.")
            return

        if response.status_code == 404:
            print("ERROR: Ticket no encontrado.")
            return

        response.raise_for_status()

        data = response.json()

        print("=" * 60)
        print("ESTRUCTURA DEL JSON DEL TICKET")
        print("=" * 60)
        print()
        print_json_structure(data)
        print()
        print("=" * 60)
        print("JSON COMPLETO (formateado)")
        print("=" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"ERROR de conexión: {e}")
    except json.JSONDecodeError as e:
        print(f"ERROR al decodificar JSON: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python ver_estructura_ticket.py <ticket_id>")
        print("Ejemplo: python ver_estructura_ticket.py 123456789")
        sys.exit(1)

    ticket_id = sys.argv[1]
    main(ticket_id)

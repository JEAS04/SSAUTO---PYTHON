"""
Script para ver la estructura de los campos highly_sensitive y sensitive
de un ticket de HubSpot. Estos campos suelen contener JSON anidado.

Uso: python ver_estructura_sensitive.py <ticket_id>
      python ver_estructura_sensitive.py <ticket_id> --raw
"""

import requests
import os
import json
import sys
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
                # Truncar representaciones largas para mejor lectura
                rep = repr(value)
                if len(rep) > 120:
                    rep = rep[:120] + "..."
                print(f"{prefix}|-- {key}: ({tipo}) = {rep}")
    elif isinstance(data, list):
        for i, item in enumerate(data[:3]):
            print(f"{prefix}|-- [{i}]:")
            print_json_structure(item, indent + 1)
        if len(data) > 3:
            print(f"{prefix}|-- ... y {len(data) - 3} más")
    else:
        print(f"{prefix}|-- {repr(data)}")


def try_parse_json(value):
    """Intenta parsear un string como JSON; retorna el objeto o None."""
    if not isinstance(value, str):
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        return None


def main(ticket_id: str, show_raw: bool = False):

    if not token:
        print("ERROR: No se encontró ACCESS_TOKEN en el archivo .env")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    url = f"{TICKET_API_URL}/{ticket_id}?properties=highly_sensitive,sensitive"

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

        print("=" * 70)
        print("ESTRUCTURA GENERAL DEL TICKET")
        print("=" * 70)
        print()
        print_json_structure(data)
        print()

        # Extraer las propiedades del ticket
        properties = data.get("properties", {})

        for campo in ["highly_sensitive", "sensitive"]:
            valor = properties.get(campo)

            print("=" * 70)
            print(f"CAMPO: '{campo}'")
            print("=" * 70)

            if valor is None:
                print(f"(El campo '{campo}' no existe o es nulo)")
                print()
                continue

            print(f"Tipo: {type(valor).__name__}")
            print(f"Valor raw: {repr(valor)[:200]}")
            print()

            # Intentar parsear como JSON
            parsed = try_parse_json(valor)
            if parsed is not None:
                print(f"→ El campo '{campo}' contiene JSON válido.\n")
                print("--- Estructura del JSON interno ---")
                print_json_structure(parsed)
                print()
                print("--- JSON formateado ---")
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
            else:
                print(f"→ El campo '{campo}' NO es JSON. Es texto plano.")
                print(f"   Contenido: {valor[:500]}")

            print()

        # Si se solicita raw, mostrar el JSON completo
        if show_raw:
            print("=" * 70)
            print("JSON COMPLETO (raw)")
            print("=" * 70)
            print(json.dumps(data, indent=2, ensure_ascii=False))

    except requests.exceptions.RequestException as e:
        print(f"ERROR de conexión: {e}")
    except json.JSONDecodeError as e:
        print(f"ERROR al decodificar JSON: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ver_estructura_sensitive.py <ticket_id> [--raw]")
        print("Ejemplo: python ver_estructura_sensitive.py 1554989368")
        print("         python ver_estructura_sensitive.py 1554989368 --raw")
        sys.exit(1)

    ticket_id = sys.argv[1]
    show_raw = "--raw" in sys.argv
    main(ticket_id, show_raw)

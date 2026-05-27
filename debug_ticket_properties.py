#!/usr/bin/env python3
"""
debug_ticket_properties.py — Ver qué propiedades tiene un TICKET
"""

from data.api import _buscar_ticket_por_fsd

# Buscar un ticket conocido
fsd = "1251275"
print(f"Buscando TICKET con FSD={fsd}...")
print("=" * 80)

ticket_data = _buscar_ticket_por_fsd(fsd)

if ticket_data:
    ticket_id = ticket_data.get("ticket_id")
    props = ticket_data.get("props", {})

    print(f"Ticket ID: {ticket_id}\n")
    print("TODAS LAS PROPIEDADES DEL TICKET:")
    print("=" * 80)

    for clave in sorted(props.keys()):
        valor = props[clave]
        print(f"{clave:<40}: {repr(valor)}")

    print("\n" + "=" * 80)
    print("PROPIEDADES QUE CONTIENEN 'contact' o 'Contact':")
    print("=" * 80)
    for clave in sorted(props.keys()):
        if "contact" in clave.lower():
            valor = props[clave]
            print(f"{clave:<40}: {repr(valor)}")
else:
    print(f"❌ No se encontró ticket para FSD={fsd}")

print("\n" + "=" * 80)
print("FIN DEL DEBUG")

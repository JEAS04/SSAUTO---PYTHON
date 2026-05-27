#!/usr/bin/env python3
"""
debug_propiedades_contacto.py — Ver las propiedades REALES de un contacto
"""

from data.api import HubSpotAPI

api = HubSpotAPI()
candidatos = api.buscar_contactos_por_criterio("Daisy", "nombre")

if candidatos:
    print(f"Encontrados {len(candidatos)} candidatos\n")

    primer_candidato = candidatos[0]
    print("=" * 80)
    print("PRIMER CANDIDATO - ESTRUCTURA COMPLETA:")
    print("=" * 80)

    for clave, valor in primer_candidato.items():
        print(f"{clave:<20}: {repr(valor)}")

    print("\n" + "=" * 80)
    print("Datos clave:")
    print("=" * 80)
    print(f"¿Tiene id_cliente? {bool(primer_candidato.get('id_cliente'))}")
    print(f"¿Tiene contact_id? {bool(primer_candidato.get('contact_id'))}")
    print(f"¿Tiene email? {bool(primer_candidato.get('email'))}")

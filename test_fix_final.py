#!/usr/bin/env python3
"""
test_fix_final.py — Verificar que el fix funciona
"""

print("Buscando candidato 'Daisy' con FSD...")
print("=" * 60)

from data.api import HubSpotAPI

api = HubSpotAPI()
candidatos = api.buscar_contactos_por_criterio("Daisy", "nombre")

if not candidatos:
    print("❌ No se encontraron candidatos")
else:
    print(f"✅ Se encontraron {len(candidatos)} candidato(s)\n")

    for i, c in enumerate(candidatos[:3]):  # Mostrar solo los primeros 3
        print(f"Candidato {i+1}:")
        print(f"  Nombre: {c.get('nombre')}")
        print(f"  Email: {c.get('email')}")
        print(f"  FSD: {repr(c.get('fsd'))}")

        if c.get("fsd"):
            print(f"  ✅ ¡¡¡FSD ENCONTRADO!!!")
        else:
            print(f"  ⚠️  Sin FSD")
        print()

print("=" * 60)
print("FIN DEL TEST")

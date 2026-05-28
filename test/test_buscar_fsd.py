#!/usr/bin/env python3
"""
test_buscar_fsd.py — Test mínimo de _buscar_fsd_por_id_cliente
Copia este archivo a tu proyecto y ejecuta: python test_buscar_fsd.py
"""

from data.api import _buscar_fsd_por_id_cliente

# Test 1: id_cliente válido (267334 del ejemplo)
print("=" * 60)
print("TEST 1: id_cliente='267334'")
print("=" * 60)

resultado = _buscar_fsd_por_id_cliente("267334")
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")
print(f"Tipo: {type(resultado)}")

# Test 2: id_cliente vacío
print("\n" + "=" * 60)
print("TEST 2: id_cliente=''")
print("=" * 60)

resultado = _buscar_fsd_por_id_cliente("")
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")

# Test 3: id_cliente None
print("\n" + "=" * 60)
print("TEST 3: id_cliente=None")
print("=" * 60)

resultado = _buscar_fsd_por_id_cliente(None)
print(f"Resultado: {repr(resultado)}")
print(f"¿Es vacío? {not resultado}")

# Test 4: buscar directamente un FSD conocido
print("\n" + "=" * 60)
print("TEST 4: Buscar FSD '1251275' directamente")
print("=" * 60)

from data.api import extraer_datos_hubspot

datos = extraer_datos_hubspot("1251275")
print(f"FSD extraído: {repr(datos.get('fsd'))}")
print(f"ID Cliente: {repr(datos.get('id_cliente'))}")
print(f"Error: {repr(datos.get('error'))}")

# Test 5: Usar el candidato que devuelve la búsqueda
print("\n" + "=" * 60)
print("TEST 5: Buscar candidato por nombre y extraer FSD")
print("=" * 60)

from data.api import HubSpotAPI

api = HubSpotAPI()
candidatos = api.buscar_contactos_por_criterio("Daisy", "nombre")

if candidatos:
    print(f"Se encontraron {len(candidatos)} candidato(s)")

    for i, c in enumerate(candidatos):
        print(f"\n  Candidato {i+1}:")
        print(f"    Nombre: {c.get('nombre')}")
        print(f"    id_cliente: {repr(c.get('id_cliente'))}")
        print(f"    fsd (antes): {repr(c.get('fsd'))}")

        # Intentar extraer FSD
        fsd = _buscar_fsd_por_id_cliente(c.get("id_cliente", ""))
        print(f"    fsd (después de _buscar_fsd): {repr(fsd)}")
else:
    print("No se encontraron candidatos")

print("\n" + "=" * 60)
print("FIN DEL TEST")
print("=" * 60)

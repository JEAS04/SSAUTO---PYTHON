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


def normalizar(texto):
    """Quita tildes y pasa a minúsculas para comparar."""
    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ñ": "n",
        "à": "a",
        "è": "e",
        "ì": "i",
        "ò": "o",
        "ù": "u",
    }
    texto = texto.lower()
    for con_tilde, sin_tilde in reemplazos.items():
        texto = texto.replace(con_tilde, sin_tilde)
    return texto


def detectar_municipio(asunto):
    asunto_norm = normalizar(asunto)
    # Ordenamos de mayor a menor longitud para que "San Juan" no sea opacado por "Juan"
    for municipio in sorted(MUNICIPIOS_PR, key=len, reverse=True):
        if normalizar(municipio) in asunto_norm:
            return municipio
    return "No detectado"


def parsear_asunto(asunto, municipio):
    """
    Extrae nombre e ID del cliente del asunto.
    Formato esperado: "FSD983316 - David Cruz Rosario - ID 250630 - San Juan"
    """
    # Quitamos el municipio del asunto para no confundirlo con el nombre
    asunto_limpio = re.sub(
        re.escape(municipio), "", asunto, flags=re.IGNORECASE
    ).strip()

    partes = [p.strip() for p in asunto_limpio.split("-") if p.strip()]

    nombre = "No encontrado"
    id_cliente = "No encontrado"

    for parte in partes:
        # Detectar ID cliente: "ID 250630" o solo "250630"
        match_id = re.search(r"\bID\s*(\d{4,})\b", parte, re.IGNORECASE)
        if match_id:
            id_cliente = match_id.group(1)
            continue

        # Número puro de 4+ dígitos → ID cliente
        if re.fullmatch(r"\d{4,}", parte):
            id_cliente = parte
            continue

        # Si empieza con FSD → ignorar
        if re.match(r"^FSD\d+", parte, re.IGNORECASE):
            continue

        # Lo que queda y tiene solo letras/espacios → nombre
        if re.fullmatch(r"[A-Za-záéíóúüñÁÉÍÓÚÜÑ\s]+", parte) and len(parte) > 2:
            nombre = parte

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

        # Encabezado
        print(
            f"\n{'TICKET ID':<15} | {'FSD':<12} | {'NOMBRE':<25} | {'MUNICIPIO':<16} | {'ID CLIENTE'}"
        )
        print("─" * 90)

        for ticket in results_page.results:
            p = ticket.properties
            asunto = p.get("subject", "")
            fsd = p.get(NOMBRE_INTERNO_FSD, "N/A")
            ticket_id = ticket.id

            municipio = detectar_municipio(asunto)
            nombre, id_cliente = parsear_asunto(asunto, municipio)

            print(
                f"{ticket_id:<15} | "
                f"{fsd:<12} | "
                f"{nombre[:25]:<25} | "
                f"{municipio[:16]:<16} | "
                f"{id_cliente}"
            )

        print("─" * 90)
        print(f"Total: {len(results_page.results)} tickets\n")

    except ApiException as e:
        print(f"❌ Error de API: {e}")


if __name__ == "__main__":
    extraer_tickets()

# import os
# from dotenv import load_dotenv
# from hubspot import HubSpot
# from hubspot.crm.tickets import PublicObjectSearchRequest, ApiException

# # 1. Carga de configuración
# load_dotenv()
# token = os.getenv("ACCESS_TOKEN")
# client = HubSpot(access_token=token)


# def extraer_tickets_con_fsd():
#     # REEMPLAZA 'fsd__' por el nombre interno exacto que viste en el icono </>
#     NOMBRE_INTERNO_FSD = "fsd__"

#     # Configuramos la búsqueda filtrada
#     search_request = PublicObjectSearchRequest(
#         filter_groups=[
#             {
#                 "filters": [
#                     {
#                         "propertyName": NOMBRE_INTERNO_FSD,
#                         "operator": "HAS_PROPERTY",  # Solo trae los que NO están vacíos
#                     }
#                 ]
#             }
#         ],
#         properties=["subject", NOMBRE_INTERNO_FSD, "hs_object_id"],
#         limit=20,  # Puedes subirlo hasta 100
#     )

#     try:
#         print(f"Buscando tickets con la propiedad '{NOMBRE_INTERNO_FSD}' completa...")
#         results_page = client.crm.tickets.search_api.do_search(
#             public_object_search_request=search_request
#         )

#         if not results_page.results:
#             print(
#                 "No se encontraron tickets con ese dato lleno. Revisa el nombre interno."
#             )
#             return

#         for ticket in results_page.results:
#             p = ticket.properties
#             asunto = p.get("subject", "Sin asunto")
#             valor_fsd = p.get(NOMBRE_INTERNO_FSD)
#             print(f"✅ Ticket ID: {ticket.id} | FSD: {valor_fsd} | Asunto: {asunto}")

#     except ApiException as e:
#         print(f"Error en la búsqueda: {e}")

#         try:
#             # Intenta traer UN solo ticket pidiendo el campo fsd__
#             # Reemplaza 'fsd__' por el nombre interno que viste en el icono </>
#             test_ticket = client.crm.tickets.basic_api.get_page(
#                 limit=1, properties=["fsd__"]
#             )
#             print("¡El Token está perfecto y tiene acceso! ✅")
#             print(f"Resultado: {test_ticket.results[0].properties}")
#         except Exception as e:
#             print(f"El problema es el Token: {e}")


# def extraer_datos_separados():
#     NOMBRE_INTERNO_FSD = "fsd__"

#     search_request = PublicObjectSearchRequest(
#         filter_groups=[
#             {
#                 "filters": [
#                     {"propertyName": NOMBRE_INTERNO_FSD, "operator": "HAS_PROPERTY"}
#                 ]
#             }
#         ],
#         properties=["subject", NOMBRE_INTERNO_FSD, "hs_object_id"],
#         limit=20,
#     )

#     try:
#         results_page = client.crm.tickets.search_api.do_search(
#             public_object_search_request=search_request
#         )

#         print(f"{'FSD':<15} | {'NOMBRE':<25} | {'ID CLIENTE':<12} | {'TICKET ID'}")
#         print("-" * 70)

#         for ticket in results_page.results:
#             p = ticket.properties
#             asunto = p.get("subject", "")
#             fsd_real = p.get(NOMBRE_INTERNO_FSD)

#             # Separamos el asunto usando el guion '-'
#             # Ejemplo: "FSD983316 - David Cruz Rosario - ID 250630"
#             partes = [parte.strip() for parte in asunto.split("-")]

#             # Intentamos asignar cada parte basándonos en tu formato
#             nombre_cliente = partes[1] if len(partes) > 1 else "No encontrado"
#             id_cliente = (
#                 partes[2].replace("ID", "").strip()
#                 if len(partes) > 2
#                 else "No encontrado"
#             )

#             print(
#                 f"{fsd_real:<15} | {nombre_cliente[:25]:<25} | {id_cliente:<12} | {ticket.id}"
#             )

#     except ApiException as e:
#         print(f"Error: {e}")


# extraer_datos_separados()


# def extraer_datos_limpios():
#     NOMBRE_INTERNO_FSD = "fsd__"
#     search_request = PublicObjectSearchRequest(
#         filter_groups=[
#             {
#                 "filters": [
#                     {"propertyName": NOMBRE_INTERNO_FSD, "operator": "HAS_PROPERTY"}
#                 ]
#             }
#         ],
#         properties=["subject", NOMBRE_INTERNO_FSD],
#         limit=20,
#     )

#     try:
#         results_page = client.crm.tickets.search_api.do_search(
#             public_object_search_request=search_request
#         )
#         print(f"{'FSD REAL':<15} | {'NOMBRE':<25} | {'ID CLIENTE':<12}")
#         print("-" * 60)

#         for ticket in results_page.results:
#             p = ticket.properties
#             asunto = p.get("subject", "")
#             fsd_desde_propiedad = p.get(
#                 NOMBRE_INTERNO_FSD
#             )  # Este es el valor real y seguro

#             partes = [parte.strip() for parte in asunto.split("-")]

#             # Lógica inteligente para encontrar el ID y el Nombre
#             nombre = "No encontrado"
#             id_cliente = "No encontrado"

#             for p_text in partes:
#                 # Si es un número de 6 dígitos y no es el FSD, es el ID del cliente
#                 if p_text.isdigit() and len(p_text) >= 5:
#                     id_cliente = p_text
#                 elif "ID" in p_text.upper():
#                     id_cliente = p_text.upper().replace("ID", "").strip()
#                 # Si no tiene números y no es el FSD, probablemente es el nombre
#                 elif not any(char.isdigit() for char in p_text) and len(p_text) > 3:
#                     nombre = p_text

#             print(f"{fsd_desde_propiedad:<15} | {nombre[:25]:<25} | {id_cliente:<12}")

#     except ApiException as e:
#         print(f"Error: {e}")


# extraer_datos_limpios()


# def extraer_datos_con_municipios():
#     NOMBRE_INTERNO_FSD = "fsd__"

#     # 1. Lista de municipios de Puerto Rico (puedes completarla)
#     municipios_pr = [
#         "Adjuntas",
#         "Aguada",
#         "Aguadilla",
#         "Aguas Buenas",
#         "Aibonito",
#         "Añasco",
#         "Arecibo",
#         "Arroyo",
#         "Barceloneta",
#         "Barranquitas",
#         "Bayamón",
#         "Cabo Rojo",
#         "Caguas",
#         "Camuy",
#         "Canóvanas",
#         "Carolina",
#         "Cataño",
#         "Cayey",
#         "Ceiba",
#         "Ciales",
#         "Cidra",
#         "Coamo",
#         "Comerío",
#         "Corozal",
#         "Culebra",
#         "Dorado",
#         "Fajardo",
#         "Florida",
#         "Guánica",
#         "Guayama",
#         "Guayanilla",
#         "Guaynabo",
#         "Gurabo",
#         "Hatillo",
#         "Hormigueros",
#         "Humacao",
#         "Isabela",
#         "Jayuya",
#         "Juana Díaz",
#         "Juncos",
#         "Lajas",
#         "Lares",
#         "Las Marías",
#         "Las Piedras",
#         "Loíza",
#         "Luquillo",
#         "Manatí",
#         "Maricao",
#         "Maunabo",
#         "Mayagüez",
#         "Moca",
#         "Morovis",
#         "Naguabo",
#         "Naranjito",
#         "Orocovis",
#         "Patillas",
#         "Peñuelas",
#         "Ponce",
#         "Quebradillas",
#         "Rincón",
#         "Río Grande",
#         "Sabana Grande",
#         "Salinas",
#         "San Germán",
#         "San Juan",
#         "San Lorenzo",
#         "San Sebastián",
#         "Santa Isabel",
#         "Toa Alta",
#         "Toa Baja",
#         "Trujillo Alto",
#         "Utuado",
#         "Vega Alta",
#         "Vega Baja",
#         "Vieques",
#         "Villalba",
#         "Yabucoa",
#         "Yauco",
#     ]

#     search_request = PublicObjectSearchRequest(
#         filter_groups=[
#             {
#                 "filters": [
#                     {"propertyName": NOMBRE_INTERNO_FSD, "operator": "HAS_PROPERTY"}
#                 ]
#             }
#         ],
#         properties=["subject", NOMBRE_INTERNO_FSD],
#         limit=20,
#     )

#     try:
#         results_page = client.crm.tickets.search_api.do_search(
#             public_object_search_request=search_request
#         )

#         # Agregamos la columna MUNICIPIO
#         print(f"{'FSD':<15} | {'NOMBRE':<20} | {'MUNICIPIO':<15} | {'ID CLIENTE'}")
#         print("-" * 75)

#         for ticket in results_page.results:
#             asunto = ticket.properties.get("subject", "")
#             fsd_real = ticket.properties.get(NOMBRE_INTERNO_FSD)

#             # 2. Lógica para detectar municipio
#             municipio_encontrado = "No detectado"
#             for m in municipios_pr:
#                 if m.lower() in asunto.lower():  # Buscamos sin importar mayúsculas
#                     municipio_encontrado = m
#                     break

#             # Limpieza básica de las otras partes
#             partes = [p.strip() for p in asunto.split("-")]
#             nombre = "No encontrado"
#             id_cliente = "No encontrado"

#             for p_text in partes:
#                 if p_text.isdigit() and len(p_text) >= 5:
#                     id_cliente = p_text
#                 elif not any(char.isdigit() for char in p_text) and len(p_text) > 3:
#                     # Evitamos que el municipio se guarde como nombre
#                     if p_text.lower() not in [m.lower() for m in municipios_pr]:
#                         nombre = p_text

#             print(
#                 f"{fsd_real:<15} | {nombre[:20]:<20} | {municipio_encontrado:<15} | {id_cliente}"
#             )

#     except Exception as e:
#         print(f"Error: {e}")


# extraer_datos_con_municipios()


# if __name__ == "__main__":
#     extraer_tickets_con_fsd()


# import os
# import json
# from dotenv import load_dotenv
# from hubspot import HubSpot
# from hubspot.crm.contacts import ApiException

# # Cargar token desde el .env
# load_dotenv()
# token = os.getenv("ACCESS_TOKEN")
# # print(f"Token cargado: {token[:10]}...")


# def ejecutar_lectura_controlada():
#     client = HubSpot(access_token=token)

#     try:
#         # Usamos 'get_page' en lugar de 'get_all'
#         # limit: cuántos traer (máximo 100 por página)
#         respuesta = client.crm.contacts.basic_api.get_page(
#             limit=10, properties=["firstname", "lastname", "email"]
#         )

#         for contacto in respuesta.results:
#             p = contacto.properties
#             print(f"ID: {contacto.id} - {p.get('firstname')} {p.get('lastname')}")

#         print(f"\n--- Se mostraron {len(respuesta.results)} contactos ---")

#         if respuesta.paging:
#             print(f"Hay más contactos, pero nos detuvimos aquí para que no explote. 🧨")
#     except ApiException as e:
#         print(f"Error: {e}")


# from datetime import datetime
# import re

# # ... (tu configuración de cliente de HubSpot anterior)


# def procesar_tickets_fsd():

#     ticket_id_real = "45143648594"
#     client = HubSpot(access_token=token)
#     # Traemos los tickets. 'subject' es donde vive el nombre desordenado
#     # respuesta = client.crm.tickets.basic_api.get_page(
#     #     limit=20, properties=["subject", "fsd__"]
#     # )

#     ticket = client.crm.tickets.basic_api.get_by_id(
#         ticket_id_real,
#         print(f"Ticket: {p.get('subject')} | FSD Real: {p.get('fsd__')}"),
#     )


# print(f"Sujeto: {ticket.properties.get('subject')}")
# print(f"VALOR FSD: {ticket.properties.get('fsd__')}")
# client = HubSpot(access_token=token)


# # Vamos a pedirle a HubSpot TODAS las propiedades que tengan valor
# # para ver cuál es la que tiene el número FSD
# respuesta = client.crm.tickets.basic_api.get_page(limit=5)

# for ticket in respuesta.results:
#     print(f"\n--- Analizando Ticket ID: {ticket.id} ---")
#     # Esto imprimirá todos los nombres internos de las propiedades que TIENEN datos
#     print(ticket.properties.keys())

# procesar_tickets_fsd()


# def serializador(obj):
#     if isinstance(obj, datetime):
#         return obj.isoformat()  # Convierte la fecha a formato ISO 8601
#     raise TypeError(f"Tipo {type(obj)} no serializable")


# client = HubSpot(access_token=token)


# respuesta = client.crm.contacts.basic_api.get_page(
#     limit=1, properties=["email", "nombre_interno_sensible"]
# )  # Pedimos solo 1 para analizar
# for contacto in respuesta.results:
#     # .to_dict() convierte el objeto del SDK en un diccionario estándar
#     # Añadimos default=str al final
#     # print(json.dumps(contacto.to_dict(), indent=4, default=str))
#     print(f"\n--- Analizando Ticket ID: {contacto.id} ---")
#     print(contacto.properties)
#     print(json.dumps(contacto.to_dict(), indent=4, default=serializador))

# # NO pongas el parámetro 'properties'.
# # Si no lo pones, HubSpot devuelve las básicas + cualquier propiedad con valor.
# respuesta = client.crm.contacts.basic_api.get_page(limit=5)

# for contacto in respuesta.results:
#     # Aquí verás los nombres internos reales en las llaves del diccionario
#     print(contacto.properties.keys())


# if __name__ == "__main__":
#     ejecutar_lectura_controlada()


# # Pedimos contactos e indicamos que incluya los IDs de tickets vinculados
# respuesta = client.crm.contacts.basic_api.get_page(limit=5, associations=["tickets"])

# for contacto in respuesta.results:
#     email = contacto.properties.get("email")
#     print(f"\nContacto: {email}")

#     # Revisamos si tiene tickets asociados
#     if contacto.associations and "tickets" in contacto.associations:
#         tickets = contacto.associations["tickets"].results
#         for t in tickets:
#             print(f"  -> Tiene el Ticket ID: {t.id}")
#     else:
#         print("  -> Sin tickets asociados.")

# # Cambia 'ID_DE_UN_TICKET_REAL' por uno que veas en tu HubSpot con FSD
# ticket_id = "ID_DE_UN_TICKET_REAL"

# # Pedimos el ticket con absolutamente todas sus propiedades
# ticket_full = client.crm.tickets.basic_api.get_by_id(
#     ticket_id, properties_with_history=[]
# )
# print(ticket_full.properties)


# # Analizamos un contacto (usa un ID real de un contacto que sepas que tiene FSD)
# contacto = client.crm.contacts.basic_api.get_by_id("ID_DE_CONTACTO_REAL")
# print(contacto.properties.keys())


# def extraer_datos_limpios():
#     NOMBRE_INTERNO_FSD = "fsd__"
#     search_request = PublicObjectSearchRequest(
#         filter_groups=[
#             {
#                 "filters": [
#                     {"propertyName": NOMBRE_INTERNO_FSD, "operator": "HAS_PROPERTY"}
#                 ]
#             }
#         ],
#         properties=["subject", NOMBRE_INTERNO_FSD],
#         limit=20,
#     )

#     try:
#         results_page = client.crm.tickets.search_api.do_search(
#             public_object_search_request=search_request
#         )
#         print(f"{'FSD REAL':<15} | {'NOMBRE':<25} | {'ID CLIENTE':<12}")
#         print("-" * 60)

#         for ticket in results_page.results:
#             p = ticket.properties
#             asunto = p.get("subject", "")
#             fsd_desde_propiedad = p.get(
#                 NOMBRE_INTERNO_FSD
#             )  # Este es el valor real y seguro

#             partes = [parte.strip() for parte in asunto.split("-")]

#             # Lógica inteligente para encontrar el ID y el Nombre
#             nombre = "No encontrado"
#             id_cliente = "No encontrado"

#             for p_text in partes:
#                 # Si es un número de 6 dígitos y no es el FSD, es el ID del cliente
#                 if p_text.isdigit() and len(p_text) >= 5:
#                     id_cliente = p_text
#                 elif "ID" in p_text.upper():
#                     id_cliente = p_text.upper().replace("ID", "").strip()
#                 # Si no tiene números y no es el FSD, probablemente es el nombre
#                 elif not any(char.isdigit() for char in p_text) and len(p_text) > 3:
#                     nombre = p_text

#             print(f"{fsd_desde_propiedad:<15} | {nombre[:25]:<25} | {id_cliente:<12}")

#     except ApiException as e:
#         print(f"Error: {e}")


# extraer_datos_limpios()

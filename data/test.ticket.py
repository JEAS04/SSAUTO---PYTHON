"""
data/test.ticket.py — Script de prueba para inspeccionar propiedades de HubSpot.

Este archivo es un script exploratorio (no un test automatizado) que consulta
directamente la API de HubSpot para inspeccionar las propiedades de tickets
y contactos durante el desarrollo. No se ejecuta en la suite de tests.

Uso:
    python data/test.ticket.py
"""

from api import _client, _T_FSD

# CONTACTO SOLO FSD Y SUBJECT
ticket = _client.crm.tickets.basic_api.get_by_id(
    ticket_id="45625352988", properties=["fsd__", "subject"]
)
print(ticket.properties)


# from api import _client, _T_FSD

# CONTACTO FSD, NOMBRE Y EMAIL
# contact = _client.crm.contacts.basic_api.get_by_id(
#     contact_id="275010", properties=["fsd__", "firstname", "email"]
# )

# print(contact.properties)

# from api import _client

# # TICKET TODOS LOS CAMPOS
# ticket = _client.crm.tickets.basic_api.get_by_id(ticket_id="45625352988")

# print(ticket.properties)

# contact = _client.crm.contacts.basic_api.get_by_id(contact_id="224297960788")

# print(ticket.properties)

# from api import _client

# # PROPIEDADES DE CONTACTOS
# contact_properties = _client.crm.properties.core_api.get_all(object_type="contacts")

# print("\nCONTACT PROPERTIES:\n")

# for prop in contact_properties.results:
#     print(f"{prop.name} -> {prop.label} -> {prop.type}")  # print(prop.name)


# from api import _client

# # PROPIEDADES DE TICKETS
# ticket_properties = _client.crm.properties.core_api.get_all(object_type="tickets")

# print("\nTICKET PROPERTIES:\n")

# for prop in ticket_properties.results:
#     print(f"{prop.name} -> {prop.label}")

# PARA LAS PRIMERAS 100
# for prop in ticket_properties.results[:100]:


# CONTACTO SOLO FSD Y SUBJECT
ticket = _client.crm.tickets.basic_api.get_by_id(
    ticket_id="45542153268",
    properties=["fsd__", "subject", "firstname", "id_goformz__servicios_tecnicos_"],
)
print(ticket.properties)


contact = _client.crm.contacts.basic_api.get_by_id(
    contact_id="137594126126",
    properties=["fsd__", "firstname", "email", "id_de_goformz__contacto_"],
)
print(contact.properties)

# necesito usar ciertos atributos que ya tengo anotados y usarlos para la comparacion con el scraping de SUNRUN, los usuarios de CONTACTO se identifican por id_de_goformz__contacto_ (id cliente), ademas en el nombre del ticket (subject) esta el fsd__ de ticket, nombre apellido (firstname, lastname) de contacto, id_goformz__servicios_tecnicos_ (id cliente) de contacto y una nota (notas), todo esto puede estar en la api con los mismos atributos, ademas tambien necesito el atributo municipio(pueblo_para_servicio_tecnico), Ticket ID o id de ticket (hs_ticket_id) y id de registro o Record ID (hs_object_id). Cabe resaltar que en el subject, en algunos tickets si esta toda esa informacion pero en otros se encuentra incompleta, la unica forma de identificar a ambos es por su id de GOFORMZ: id_de_goformz__contacto_ y id_goformz__servicios_tecnicos_ - ID GoFormz (Servicios Tecnicos)

# tampoco
# no me esta realizando la busqueda por fsd-000000, ni fsd000000, deberia admitir ambos y hasta sin la palabra fsd escrita, tampoco me esta usando el chrome ya abierto (default), y por lo tanto tampoco hace el web scraping a SUNRUN. Cabe recalcar que ya tengo la sesion abierta en chrome y comprobe que la http://localhost:9222/json/version dijera "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/a5b8b551-c718-42fc-8d09-028825ae09f4" y TCP 127.0.0.1:9222 LISTENING -> TCP    127.0.0.1:9222         0.0.0.0:0              LISTENING       13928
# Nombre de imagen               PID Nombre de sesión Núm. de ses Uso de memor
# ========================= ======== ================ =========== ============
# chrome.exe                   13928 Console                    6   191,196 KB pero no se abre el chrome que ya tengo abierto para eso, se abre uno nuevo o no carga nada del web scraping

# bro, esto me imprime un monton de atributos o propiedades de TICKET, no esta mal, me sirve para ver que atributos tiene pero si son un monton XD
# from hubspot.crm.properties import ApiException

# props = client.crm.properties.core_api.get_all(object_type="tickets")

# for p in props.results:
#     print(p.name, "-", p.label)

# necesito usar ciertos atributos que ya tengo anotados y usarlos para la comparacion con el scraping de SUNRUN, los usuarios de CONTACTO se identifican por id_de_goformz__contacto_ (id cliente), ademas en el nombre del ticket (subject) esta el fsd__ de ticket, nombre apellido (firstname, lastname) de contacto, id_goformz__servicios_tecnicos_ (id cliente) de contacto y una nota (notas), todo esto puede estar en la api con los mismos atributos, ademas tambien necesito el atributo municipio(pueblo_para_servicio_tecnico), Ticket ID o id de ticket (hs_ticket_id) y id de registro o Record ID (hs_object_id). Cabe resaltar que en el subject, en algunos tickets si esta toda esa informacion pero en otros se encuentra incompleta, la unica forma de identificar a ambos es por su id de GOFORMZ: id_de_goformz__contacto_ y id_goformz__servicios_tecnicos_ - ID GoFormz (Servicios Tecnicos)


# #tampoco
# # no me esta realizando la busqueda por fsd-000000, ni fsd000000, deberia admitir ambos y hasta sin la palabra fsd escrita, tampoco me esta usando el chrome ya abierto (default), y por lo tanto tampoco hace el web scraping a SUNRUN. Cabe recalcar que ya tengo la sesion abierta en chrome y comprobe que la http://localhost:9222/json/version dijera "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/a5b8b551-c718-42fc-8d09-028825ae09f4" y TCP 127.0.0.1:9222 LISTENING -> TCP    127.0.0.1:9222         0.0.0.0:0              LISTENING       13928
# # Nombre de imagen               PID Nombre de sesión Núm. de ses Uso de memor
# # ========================= ======== ================ =========== ============
# # chrome.exe                   13928 Console                    6   191,196 KB pero no se abre el chrome que ya tengo abierto para eso, se abre uno nuevo o no carga nada del web scraping

# PARA TRAER TODOS LOS ATRIBUTOS O PROPIEDADES QUE HAYAN EN TICKETS
# from hubspot.crm.properties import ApiException

# props = client.crm.properties.core_api.get_all(object_type="tickets")

# for p in props.results:
#     print(p.name, "-", p.label)
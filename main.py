"""
main.py — Punto de entrada de SSAuto.

Este es el único archivo que se ejecuta directamente:
    python main.py

Solo aplica el tema visual e instancia la ventana principal.
Toda la lógica está en los módulos del proyecto.
"""

# https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000pd7qf2AA/fsd1217790
# https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000iYmqV2AS/fsd1187405
import customtkinter as ctk
from configuracion import TEMA_APARIENCIA, TEMA_COLOR
from ventana_principal import App

# Aplicar tema antes de crear cualquier widget.
ctk.set_appearance_mode(TEMA_APARIENCIA)
ctk.set_default_color_theme(TEMA_COLOR)

if __name__ == "__main__":
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass


# Hola Claude, vengo a mejorar mi proyecto, el web scraping funciona perfecto, pero me gustaria mejorar algunas cositas, mira: Sunrun tiene varias paginas donde el bot interactua verdad, por ejemplo la pagina principal, luego la barra global de busqueda, luego el icono morado o si no busca cierto, y ya ahi puede que se meta de una al fsd buscado o que aparezca en la lista de resultados, y luego se meta al fsd buscado, y ahi si haga el web scraping, pero siempre que le doy al boton "comparar" y digamos que ya estoy en una de esas partes, el bot empieza el proceso desde el principio, me gustaria que no se reiniciara el proceso y que detecte donde esta para que proceda, pero no que reinicie todo siempre, el ciclo que explique es un ejemplo, lo que busco es que me entiendas

# Gracias a ti! 😄 Fue una sesión muy productiva — arreglamos bastante cosa:

# ✅ Selectores XPath del DOM de Sunrun
# ✅ Búsqueda global con dropdown MRU
# ✅ State, City, Zip Code y County
# ✅ Claves desajustadas en el comparador
# ✅ Ciudad duplicada renombrada
# ✅ Ventana de comparación desbloqueada
# ✅ Bug de "Mostrar escritorio"
# ✅ Ventana al frente al abrir

# Hola Claude, ahora mismo estoy trabajando en un proyecto para mi empresa para automatizar varias cosas, una de ellas es la comparacion de datos entre dos paginas, ayer arregle el web scraping a una de ellas que es Sunrun y quedo funcionando perfecto. Ahora necesito mejorar la extraccion de la info de la otra pagina que es Hubspot, de esta cuento con el api, pero ahora mismo no estoy extrayendo los datos que necesito, ademas tengo un gran problema y es que en el nombre del TICKET (subject) hay varios datos que pueden o no pueden estar en otros atributos por ejemplo asi: FSD1240131 - Rivero Nieves - ID 245565, todo eso es el subject, pero tambien son atributos que ya estan o pueden estar en ticket en "fsd__(fsd puede estar o no)", "firstname + lastname", "id_goformz__servicios_tecnicos_" y "NOTA(la nota puede estar o no)" entonces mi idea es extraer esa info de SUBJECT y compararla con la info que este en sus respectivos atributos, si no esta se pone la que este y ya, de resto solo seria traer los datos, ademas, los tickets y los contactos solo tienen un atributo en comun, que no se llama igual pero que SI ES IGUAL, o sea el dato que tienen guardado es el mismo, pero se llaman diferente: id_goformz_servicios_tecnicos para TICKET y id_goformz_contacto para CONTACTO, realizar esa comparacion, es decir que sean iguales, y desde ahi arrancar a hacer la busqueda de la informacion en TICKET y en CONTACTO, para los atributos necesarios, el nombre de los otros atributos estan en Claude, luego la comparacion con los datos de SUNRUN, se hace con el FSD, hay otras cosas mas por agregar pero lo podemos hacer despues

# Contacto:
# HubSpot
# Nombre del cliente: firstname + lastname
# ID del Cliente: id_de_goformz__contacto_
# Direccion: direccion__fisica_
# Telefono principal: phone
# Telefono movil: telefono_alterno_del_cliente
# Email: email
# Estado (state): country
# County: municipio_de_residencia o state
# municipio_de_residencia - Municipio de residencia
# municipios_co__contacto_ - Municipios CO (Contacto)
# Ciudad / Municipio: municipio_de_residencia o state
# Zip Code: zip

# Ticket:
# HubSpot
# Nombre del cliente: subject
# ID del Cliente: esta en el subject o id_goformz__servicios_tecnicos_
# Direccion: physical_address
# Telefono principal: phone
# Telefono movil: no hay
# Email: e_mail
# Estado (state): no hay
# County: pueblo_para_servicio_tecnico
# Ciudad / Municipio: pueblo_para_servicio_tecnico
# Zip Code: no hay
# Nota: nota_ticket__sac_


# para despues, decirle que maneje los 72 municipios que no importe si esta en mayusculas, minusculas, si tiene tildes, etc, que lo reconozca igual, tambien asi con los otros atributos, datos, propiedades o como se llamen xd

# si el fsd__ en HUBSPOT esta vacio no esta buscando asi lo tenga en subject en HUBSPOT


# Necesito crear un formulario que sea bonito, llamativo y no sea tan engorrioso o complicado de responder, en este momento tengo un formulario que esta creado en Hubspot, pero que es simplemente un cuadrado con varios inputs y lo que se pide, y arriba tiene el logo de planetsolar, pregunta por: nombre apellidos, numero de seguro social, pueblo, correo, numero de telefono, direccion, Coordenadas / PIN Location*, un lugar donde se sube un archivo que es Factura de Electricidad (LUMA)*, y detalles de equipos y precios, con una sugerencia: Precio x watts | Precio x batería(s) | Marca de Bateria | Minimo Offset | Adds | Deuda de LUMA | Enseres a considerar | Otros, despues abajo un boton que dice siguiente en amarillo para pasar a las siguiente pagina donde dice nombre del consultor y telefono del consultor, luego otra pagina donde hay informacion para aceptar el tratamiento de datos personales y ya ahi se envia, verdad, lo que yo quiero es que el formulario no sea tan sencillo, ya que parece un html, con un poco de css y ya xd. Mi idea es hacer uno mejor en typeform o en alguna plataforma que me recomiendes, ademas tambien necesito guardar esa informacion, igual creo que se puede guardar todo en Hubspot. O lo puedo crear yo mismo?

# Si lo hago yo mismo, como seria la desplegada en internet? Si me hago entender, tendria que comprar un dominio y un servidor? Si se manejar la API, pero tengo esa duda.

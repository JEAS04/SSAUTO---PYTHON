  # **interfaz2.py**

  # 04-05-2026
  # Ejemplo de links para sunrun
* https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000pd7qf2AA/fsd1217790

* https://sunrun.my.site.com/partners/s/fs-dispatch/a0QUJ00000iYmqV2AS/fsd1187405

#
  El dia de hoy empece la creacion de un script en Python para la automatización de capturas de pantallas con MSS y subida a sitios web con Selenium,
  con una interfaz gráfica en Tkinter.
  Implementé un medidor de región para seleccionar el área de captura.
  El sistema permite seleccionar una región de la pantalla, capturarla, y luego subirla a diferentes sitios web, algunos de los cuales requieren autenticación.
  Se puede controlar el modo headless para que Chrome no abra una ventana visible.
  La interfaz permite configurar el tamaño de la region, de forma manual y automatica con el medidor (boton),
  y también configurar un atajo de teclado para ejecutar la captura y subida, el cual se guarda en un archivo JSON de config.
  La idea de este proyecto es facilitar la captura y compartición de evidencias, para las plataformas de HubSpot y SunRun, que son las mas utilizadas en el trabajo a diario,
  y que conllevan muchos pasos manuales para subir las capturas a cada plataforma, con este sistema se busca automatizar ese proceso y ahorrar tiempo.
  Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
  Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

  # 05-05-2026

  En el dia de hoy, me enfoqué en implementar la funcionalidad de login para los sitios que lo requieren, utilizando Selenium para automatizar el proceso de autenticación.
  Creé una ventana modal de login que se muestra al iniciar la aplicación, donde se pueden ingresar y guardar las credenciales de cada sitio de forma
  segura utilizando la librería keyring.
  La función de subida ahora incluye el proceso de login automático antes de intentar subir la imagen,
  lo que permite manejar sitios con autenticación sin necesidad de ingresar las credenciales cada vez.
  Además, se agregó una validación para verificar que el login fue exitoso antes de proceder con la subida, y se muestra un mensaje de error si el login falla.
  Se implemento un sistema de cookies para intentar restaurar la sesión antes de hacer login, lo que puede evitar la necesidad de autenticarse en cada ejecución
  si las cookies siguen siendo válidas. Ademas de las cookies un boton para renovar la sesión, que borra las cookies guardadas y fuerza un login fresco en la próxima ejecución.
  Tambien añadi una opción para reutilizar una sesión de Chrome ya abierta, lo que permite aprovechar una sesión activa sin necesidad de hacer login automático cada vez,
  aunque requiere que el usuario inicie sesión manualmente en el navegador.
  Las pruebas se realizaron con dos sitios de ejemplo, uno sin login y otro con login, utilizando Selenium para manejar la autenticación y la subida de archivos.
  Los sitios son: https://the-internet.herokuapp.com/upload (sin login) y https://the-internet.herokuapp.com/login (con login de prueba: tomsmith/SuperSecretPassword!).

  arreglado
  realmente es necesario iniciar sesion cada vez que se quiera subir una captura a un sitio que requiere autenticacion?, ademas si el sitio se mantiene abierto siempre
  en el navegador, no se podria aprovechar esa sesion activa para subir las capturas sin necesidad de hacer login cada vez?

  arreglado
  Hay que arreglar el chrome con depuracion, ya que se abre bien, pero cuando se ejecuta la captura y subida, no detecta la sesión activa, aunque el Chrome abierto
   tenga sesión iniciada en el sitio, entonces hace el login automático, pero no funciona, no detecta que se hizo login exitoso,
   y no sube la imagen. Hay que revisar esa parte para que funcione correctamente con un Chrome ya abierto y con sesión activa.

  # 06-05-2026

  Hoy empece a arreglar el chrome con depuracion (cuando las paginas ya estan abiertas), el problema era que, aunque se detectaba
  la sesión activa en el Chrome abierto, al navegar a la página de subida, el sitio redirigía a la página de login, lo que
  indicaba que no se estaba aprovechando la sesión activa correctamente. Entonces cuando se tomaba la captura se abrian las pestañas
  correspondientes a cada sitio y se subian las capturas correctamente, pero la idea era que si el usuario ya tenia sesión iniciada
  en el Chrome abierto, se aprovechara esa sesión para subir las capturas sin necesidad de hacer login automático cada vez,
  pero no estaba funcionando así. Entonces, para solucionar esto, modifiqué el flujo para que después de detectar la sesión activa,
  se navegue directamente a la página de subida en las pestañas correspondientes donde ya habia una sesion iniciada, esperando que
  no se abrieran nuevas pestañas, ademas de esto se debe confirmar la subida de la imagen al sitio, con su respectivo boton.
  Se añadieron colores y se reorganizo la estructura de la interfaz, ahora se ve mas estetico, ademas la interfaz se adapta a la
  resolucion de la pantalla

  PENDIENTES: PONERLE LINEA DE TIEMPO, TIEMPO DE DESARROLLO, Y PROXIMOS PASOS, MEJORAS FUTURAS, ETC.

  # 07-05-2026
  Se añadio scroll para que el contenido de la interfaz se vea correctamente, ademas ahora al minimizar y maximizar, el contenido se adapta correctamente.
  Se migro todo el script de Tkinter a CustomTkinter con toda la funcionalidad preservada, lo que nos permitio hacer una interfaz mas estetica y mas facil de optimizar, CustomTkinter permite hacer que
   el tema de fondo de la aplicacion sea mas sencillo de utilizar o cambiar, lo cual no se podia hacer tan facil desde Tkinter, se quitaron todos los LOGS y se documento
  y se documento la funcionalidad del script, se le coloco un favicon sencillo.
  Se agrego una nueva funcionalidad, ahora se pueden guardar diferentes perfiles segun el tipo de monitor, ejemplo: (monitor 1- panel izquierdo) y se rellena automaticamente
  cuando se mide la pantalla se da un nombre y se guarda, y asi se crea un nuevo perfil, luego se puede ir cambiando de perfiles y dar al boton cargar, para usar
  la region guardada

  # 08-05-2026
  Se empezo a implementar el API de Hubspot y a hacer llamadas con FastAPI y su wrapper, de esta manera pudimos encontrar que propiedades de Hubspot eran las que necesitabamos y probar la funcionalidad del API, consiguiendo sacar y hacer las consultas correctamente, despues se probo con las FSD, pero nos dio algunos errores con las entidades "Contacto" y "Ticket", ADEMAS, se

  Pendientes: hacer que se guarde en config.json y que se pueda utilizar cualquier monitor conectado a la computadora principal

  CORRECCIONES APLICADAS:
  * 1 — `_make_status_bar: .grid(side=) → .pack(side=)`
  * 2 — `make_log_section` era código muerto (log_text se creaba dos veces); eliminado
  * 3 — `_log(): CTkTextbox` no soporta tags de color → usa `._textbox` interno de Tk
  * 4 — `_font_exists():` ahora usa `tkinter.font.families()` correctamente
  * 5 — `_status_dot/.grid(side=)` → `.pack(side=)` (mismo que  1, instancia distinta)
  * 6 — `status_frame` en `_build_ui: row=99` → `row=5`
  * 7 — `_proceso():` todos los `self._log()` pasan por `self.after()` `(thread-safety)`
  * 8 — `subir():` se le pasa un wrapper thread-safe en lugar del `_log` directo

  El codigo se hizo muy grande asi que lo separe en varios archivos, para que asi el desarrollo sea algo mas sencillo:

  * ssauto/
  * ├── main.py                   ← Punto de entrada (ejecutar este archivo)
  * ├── configuracion.py          ← Constantes, lista de sitios y config.json
  * ├── credenciales.py           ← Cookies de sesión y llavero del SO (keyring)
  * ├── medidor.py                ← Código del selector visual de región
  * ├── automatizacion.py         ← Driver de Chrome, captura y subida (Selenium + mss)
  * ├── ventana_credenciales.py   ← Ventana modal de usuario/contraseña
  * ├── ventana_principal.py      ← Ventana principal (CustomTkinter)
  * ├── config.json               ← Generado automáticamente al guardar ajustes
  * ├── cookies/                  ← Generado automáticamente al hacer login
  * └── screenshots/              ← Generado automáticamente al capturar

  Se empezo a realizar el script con web scraping + api, para automatizar varias cosas
  pendientes. realizar el web scraping para comparar los datos traidos de ahi con los de la api, determinar si son iguales o no, si son iguales se dejan iguales,
   si son diferentes se ponen los dos encima del otro, como una sugerencia, si en uno de los dos el dato esta vacio, se coloca el dato que este,
   ejemplo: sitio 1: nombre: no encontrado, pero en el sitio 2: nombre: Julian, se coloca el valor del sitio 2, para asi lograr una comparacion completa

# Mejoras necesarias (a corto plazo)

      1. Compatibilidad con macOS y Linux
  `_abrir_chrome_debug()` solo busca Chrome en rutas de Windows. Agregar detección del SO con `platform.system()` y las rutas correspondientes en cada sistema.

      2. Gestión de errores más granular
  Actualmente los errores de subida se logean pero no se reintentan. Implementar reintentos automáticos (p. ej. 3 intentos con espera exponencial) para fallos de red.

      3. Validación de la región capturada
  Si `width` o `height` es 0, `mss` lanzará un error silencioso. Agregar validación antes de llamar a `capturar()` y mostrar un mensaje claro al usuario.

      4. Pruebas automáticas
  No hay ningún test. Agregar al menos pruebas unitarias para `parsear_region`, `_keybind_legible` y `cargar_config` con `pytest`.

  ---

# Mejoras futuras (a mediano plazo)

      5. Soporte para múltiples perfiles de región
  Permitir guardar y cargar diferentes regiones con nombre (p. ej. "Monitor 1 - Panel izquierdo") en lugar de solo una.

      6. Programación por horario
  Agregar un campo de intervalo (en minutos) para que la captura y subida se ejecuten automáticamente de forma periódica usando `threading.Timer` o `schedule`.

      7. Historial de capturas
  Mostrar en la UI las últimas N capturas realizadas con miniatura, fecha y estado de subida. Guardar el historial en un archivo JSON local.

      8. Notificaciones del sistema
  Usar `plyer` o `winotify` (Windows) para mostrar una notificación nativa cuando el proceso complete o falle, incluso si la ventana está minimizada.

      9. Modo de línea de comandos (CLI)
  Exponer `capturar()` y `subir()` como comandos de consola para poder integrar SSAuto en scripts o tareas programadas del SO sin abrir la UI.

      10. Empaquetado como ejecutable
  Configurar `PyInstaller` o `Nuitka` para distribuir la app como un `.exe` sin requerir Python instalado.

  ---

     Cosas a considerar

  - **Seguridad de cookies**: Los archivos `.pkl` en la carpeta `cookies/` no están cifrados. Cualquiera con acceso al sistema puede leerlos. Para mayor seguridad, cifrarlos con `cryptography.fernet` usando una clave derivada del llavero del SO.
  - **Selector de confirmación**: `wait.until(EC.url_contains("secure"))` está hardcodeado para el sitio de demo de Herokuapp. Para sitios reales, cambiar esto a un selector configurable por sitio en `SITIOS`.
  - **WebDriverManager y offline**: Si la máquina no tiene internet, `ChromeDriverManager().install()` fallará. Considerar cachear el driver o permitir especificar la ruta manualmente.


  # 11/05/2026
  Se empezo a hacer pruebas con el web scraping y el API para la comparacion de datos de clientes.
  El bot se ejecuta en el puerto 9222 de Chrome esto para que la automatizacion sea efectiva.
  En ese perfil de Chrome se puede iniciar sesion normal con cualquier cuenta, PERO su uso es unica y exclusivamente para el uso de los bots, ya que permite que los perfiles de uso diario no se rompan, no se bloquee chrome, no se corrompan los perfiles y es mas seguro aislar, ademas ahi se guardan todos los datos de la sesion incluyendo, cookies, sesiones, las cuentas, extensiones, pestañas, preferencias, etc. Y es mejor para que el bot no sea detectado por el navegador

  ESTOY EN EL TICKET -> ACTIVIDADES -> NOTAS -> CREAR NOTA -> INTERFAZ NOTA, DONDE APARECE PARA ADJUNTAR ARCHIVOS Y SUBIR FOTOS O ESCRIBIR -> CREAR NOTA. ESE ES EL FLUJO DE INTERACCION EN HUBSPOT PARA SUBIR UNA NOTA

  # 12-05-2026
  Lo primero que arreglamos este dia fue el Chrome con depuracion en el puerto 9222, ya que no estaba abriendose correctamente, ademas de eso, cada que abriamos el Chrome con depuracion mediante el boton, no se nos abria el Chrome abierto si estaba abierto y cada vez se abria una nueva pestaña
  Casos de uso:
  * `usar_chrome_existente=True`  → se conecta al Chrome ya abierto en puerto 9222.
  * usar_chrome_existente=False → abre un Chrome nuevo (con o sin headless).
  #
  Mejoramos la automatizacion en Hubspot haciendo que el bot siga la ruta especifica.
  Se verifica la pestaña, el inicio de sesion, analizando el titulo de la pagina, la url, cada pestaña y se revisa si la URL tiene "Hubspot" o no
  Tambien ocultamos todos los indicadores de automatizacion en Chrome, ademas agregamos un boton para que el usuario decida si quiere que la nota se suba automaticamente por defecto esta activado, pero es preferible que el usuario verifique y suba la captura, la configuracion de este boton se sube a "config.json"
  Ahora el usuario puede elegir el monitor que desee y guardar su perfil en "config.json", la funcionalidad del medidor y de la captura funcionan desde cualquier monitor usado
  El Web Scraping de Sunrun tiene las bases, pero tiene errores, como: no abre el fsd rapido, se demora o no lo encuentra, pero cuando lo encuentra trae la informacion correcta desde los selectores correctos. El bot verifica cada pestaña, el inicio de sesion y busca la pestaña que tenga "sunrun" y ahi se empieza a ejecutar.


  # **13-05-2026** #
  
  Como casi toda la informacion del usuario esta en el subject (nombre del ticket) la idea era parsear la informacion encontrada ahi como el fsd, el nombre, el id (id-goformz) y la nota, para verificar y comparar la info con Sunrun mediante el comparador
   api.py — Extracción de datos desde HubSpot
  ============================================
  Flujo principal:

* 1. Buscar ticket por FSD  →  `_buscar_ticket_por_fsd()`
* 2. Parsear subject como fallback  →  `_parsear_asunto()`
* 3. Buscar contacto vinculado por id_goformz  → ` _buscar_contacto_por_id_goformz()`
* 4. Combinar todo (atributo directo gana sobre subject)  →  `extraer_datos_hubspot()`

  La función pública es:
      `extraer_datos_hubspot(fsd: str) -> dict`

  Devuelve un dict con claves estandarizadas listo para comparador.py.
  Si la info esta en los atributos (propiedades) correctos se ignora la informacion que haya en el subject, solo se usa la info de subject cuando el atributo en Hubspot se encuentra vacio, se extrae el fsd de el formato fsd-000000 y se transforma en 000000 (solo numeros) e igual desde Sunrun para que la comparacion se haga correctamente.
  Acepta cualquier formato de FSD (FSD-1236711, FSD1236711, 1236711, etc.) y se prueban variaciones de fsd. Como el unico atributo en comun de "Contacto" y "Ticket" es el id del cliente "id_goformz" se busca mediante este toda la informacion del cliente y se pone en la ventana de comparacion en la columna "Hubspot"

  # **Contacto:**
* HubSpot
* Nombre del cliente: firstname + lastname
* ID del Cliente: id_de_goformz__contacto_
* Direccion: direccion__fisica_
* Telefono principal: phone
* Telefono movil: telefono_alterno_del_cliente
* Email: email
* Estado (state): country
* County: municipio_de_residencia o state
* municipio_de_residencia - Municipio de residencia
* municipios_co__contacto_ - Municipios CO (Contacto)
* Ciudad / Municipio: municipio_de_residencia o state
* Zip Code: zip
   # **Ticket:**

* HubSpot
* Nombre del cliente: subject
* ID del Cliente: esta en el subject o id_goformz__servicios_tecnicos_
* Direccion: physical_address
* Telefono principal: phone
* Telefono movil: no hay
* Email: e_mail
* Estado (state): no hay
* County: pueblo_para_servicio_tecnico
* Ciudad / Municipio: pueblo_para_servicio_tecnico
* Zip Code: no hay
* Nota: nota_ticket__sac_

# 14-05-2026

  Mejora del Web Scraping en Hubspot, el bot busca el fsd automaticamente (lo escribe) mediante la barra de busqueda global, si lo encuentra le da click, si no,
  El bot realiza una espera breve para verificar si salieron resultados si no da enter y va a la pagina de resultados y le da click desde ahi, despues ya trae toda la info a la ventana de comparacion
  Soporta dos escenarios:
            A) Página de resultados de búsqueda global (/global-search/):
               Salesforce muestra los resultados en una tabla con links cuyo
               texto visible es "FSD-XXXXXXX". Se intentan múltiples XPaths
               para cubrir variaciones del DOM de Salesforce LWC.
            B) Cualquier otra página con link por href (fsd{numero}):
               Fallback clásico — href contiene fsd+número.

  ── Escenario A: página de resultados de búsqueda global ─────
  URL: /partners/s/global-search/FSD-XXXXXXX
  El DOM de resultados de Salesforce puede presentar el link con:
    1. Texto visible exacto "FSD-XXXXXXX"
    2. href que contiene fsd{numero} (el más fiable)
    3. Atributo title o aria-label con el nombre del registro
    4. Cualquier (a) dentro de la fila que contenga el número

  ── Escenario B: otra página de Sunrun (lista, home, etc.) ─── va a la barra de busqueda global y hace el flujo normal


  Este mismo dia empece a trabajar en el Formulario de Cotizacion de PlanetSolar


  # **=============== EXTRA ===================================================**

# **main2.py**

Hola Claude, vengo a mejorar mi proyecto, el web scraping funciona perfecto, pero me gustaria mejorar algunas cositas, mira: Sunrun tiene varias paginas donde el bot interactua verdad, por ejemplo la pagina principal, luego la barra global de busqueda, luego el icono morado o si no busca cierto, y ya ahi puede que se meta de una al fsd buscado o que aparezca en la lista de resultados, y luego se meta al fsd buscado, y ahi si haga el web scraping, pero siempre que le doy al boton "comparar" y digamos que ya estoy en una de esas partes, el bot empieza el proceso desde el principio, me gustaria que no se reiniciara el proceso y que detecte donde esta para que proceda, pero no que reinicie todo siempre, el ciclo que explique es un ejemplo, lo que busco es que me entiendas

Gracias a ti! 😄 Fue una sesión muy productiva — arreglamos bastante cosa:

* ✅ Selectores XPath del DOM de Sunrun
* ✅ Búsqueda global con dropdown MRU
* ✅ State, City, Zip Code y County
* ✅ Claves desajustadas en el comparador
* ✅ Ciudad duplicada renombrada
* ✅ Ventana de comparación desbloqueada
* ✅ Bug de "Mostrar escritorio"
* ✅ Ventana al frente al abrir

Hola Claude, ahora mismo estoy trabajando en un proyecto para mi empresa para automatizar varias cosas, una de ellas es la comparacion de datos entre dos paginas, ayer arregle el web scraping a una de ellas que es Sunrun y quedo funcionando perfecto. Ahora necesito mejorar la extraccion de la info de la otra pagina que es Hubspot, de esta cuento con el api, pero ahora mismo no estoy extrayendo los datos que necesito, ademas tengo un gran problema y es que en el nombre del TICKET (subject) hay varios datos que pueden o no pueden estar en otros atributos por ejemplo asi: FSD1240131 - Rivero Nieves - ID 245565, todo eso es el subject, pero tambien son atributos que ya estan o pueden estar en ticket en "fsd__(fsd puede estar o no)", "firstname + lastname", "id_goformz__servicios_tecnicos_" y "NOTA(la nota puede estar o no)" entonces mi idea es extraer esa info de SUBJECT y compararla con la info que este en sus respectivos atributos, si no esta se pone la que este y ya, de resto solo seria traer los datos, ademas, los tickets y los contactos solo tienen un atributo en comun, que no se llama igual pero que SI ES IGUAL, o sea el dato que tienen guardado es el mismo, pero se llaman diferente: id_goformz_servicios_tecnicos para TICKET y id_goformz_contacto para CONTACTO, realizar esa comparacion, es decir que sean iguales, y desde ahi arrancar a hacer la busqueda de la informacion en TICKET y en CONTACTO, para los atributos necesarios, el nombre de los otros atributos estan en Claude, luego la comparacion con los datos de SUNRUN, se hace con el FSD, hay otras cosas mas por agregar pero lo podemos hacer despues

  # **Contacto:**
* HubSpot
* Nombre del cliente: firstname + lastname
* ID del Cliente: id_de_goformz__contacto_
* Direccion: direccion__fisica_
* Telefono principal: phone
* Telefono movil: telefono_alterno_del_cliente
* Email: email
* Estado (state): country
* County: municipio_de_residencia o state
* municipio_de_residencia - Municipio de residencia
* municipios_co__contacto_ - Municipios CO (Contacto)
* Ciudad / Municipio: municipio_de_residencia o state
* Zip Code: zip
   # **Ticket:**

* HubSpot
* Nombre del cliente: subject
* ID del Cliente: esta en el subject o id_goformz__servicios_tecnicos_
* Direccion: physical_address
* Telefono principal: phone
* Telefono movil: no hay
* Email: e_mail
* Estado (state): no hay
* County: pueblo_para_servicio_tecnico
* Ciudad / Municipio: pueblo_para_servicio_tecnico
* Zip Code: no hay
* Nota: nota_ticket__sac_


para despues, decirle que maneje los 72 municipios que no importe si esta en mayusculas, minusculas, si tiene tildes, etc, que lo reconozca igual, tambien asi con los otros atributos, datos, propiedades o como se llamen xd

si el fsd__ en HUBSPOT esta vacio no esta buscando asi lo tenga en subject en HUBSPOT


Necesito crear un formulario que sea bonito, llamativo y no sea tan engorrioso o complicado de responder, en este momento tengo un formulario que esta creado en Hubspot, pero que es simplemente un cuadrado con varios inputs y lo que se pide, y arriba tiene el logo de planetsolar, pregunta por: nombre apellidos, numero de seguro social, pueblo, correo, numero de telefono, direccion, Coordenadas / PIN Location*, un lugar donde se sube un archivo que es Factura de Electricidad (LUMA)*, y detalles de equipos y precios, con una sugerencia: Precio x watts | Precio x batería(s) | Marca de Bateria | Minimo Offset | Adds | Deuda de LUMA | Enseres a considerar | Otros, despues abajo un boton que dice siguiente en amarillo para pasar a las siguiente pagina donde dice nombre del consultor y telefono del consultor, luego otra pagina donde hay informacion para aceptar el tratamiento de datos personales y ya ahi se envia, verdad, lo que yo quiero es que el formulario no sea tan sencillo, ya que parece un html, con un poco de css y ya xd. Mi idea es hacer uno mejor en typeform o en alguna plataforma que me recomiendes, ademas tambien necesito guardar esa informacion, igual creo que se puede guardar todo en Hubspot. O lo puedo crear yo mismo?

Si lo hago yo mismo, como seria la desplegada en internet? Si me hago entender, tendria que comprar un dominio y un servidor? Si se manejar la API, pero tengo esa duda.




# 20/05/2026
Se modifico un poco el UI, para que algunas opciones como "auto-submit" encajaran mejor y no se vieran descuadradas o en una proporcion incorrecta o fea.
Se creo el archivo .exe con la herramienta de Python  **Pyinstaller**, se verifico que partes del codigo eran mas usadas con **Coverage** herramienta utilizada para saber que partes del programa se ejecutaron realmente durante las pruebas e identificar codigo muerto.
Se creo `doku.md` para poner mi documentación y datos para tener contexto. (solo yo lo entiendo xd)


# **Comando para crear el .exe**

pyinstaller --onefile --windowed --collect-all customtkinter --add-data "config.json;." --add-data ".env;." main.py

* Se eliminaron los requierements.txt innecesarios, las carpetas que ya no utilizaba y se corrigieron errores en configuracion.py

# version.py
MAJOR.MINOR.PATCH

Ejemplo:
0.1.0
* MAJOR → cambios grandes que rompen cosas
* MINOR → nuevas funciones
* PATCH → arreglos pequeños
* 0.1.0  -> primera versión usable
* 0.2.0  -> agregaste login
* 0.2.1  -> arreglaste un bug
* 1.0.0  -> versión estable
* 2.0.0  -> cambiaste arquitectura/API




HOY ME SENTE CON EL EQUIPO DE SERVICIOS TECNICOS, MILESTONE, SALESFORCE PARA REVISAR EL TRABAJO SCRIPT PROGRAMA QUE HICE EN ESTAS 2 SEMANAS, PARA EMPEZAR EN LA REUNION MI JEFE CARLOS DIO CONTEXTO DEL TEMA DE LA REUNION EN LA REUNION ESTABAN: MARGARITA FERRO, NICZY ARIAS, LINA SIERRA Y CRISTIAN REYES, PARA EMPEZAR EXPLICO LA METODOLOGIA SCRUM, LUEGO PROCEDI A EXPLICAR EL FUNCIONAMIENTO DEL PROGRAMA Y VIERON COMO FUNCIONABA, EXPLIQUE EL SSAUTO Y EL COMPARADOR DE FSD Y DURANTE LA REUNION HUBIERON MUCHAS SUGERENCIAS, IDEAS Y PETICIONES, ENTRE ELLAS, MEJORAR EL COMPARADOR, MEJORAR LA INTERFAZ, MEJORAR LA BUSQUEDA POR MAS CAMPOS, AGREGAR MAS FLUJOS ETC PARA QUE EL PROGRAMA FUNCIONE MEJOR, COMO EVITANDO LA BUSQUEDA ENTRE PESTAÑAS Y ELIJA EN DONDE ESTE, MI IDEA ES AGREGAR VARIOS BOTONES Y MEJORAR LA INTERFAZ, BOTONES PARA CAPTURAS PREDETERMINADAS EN DISTINTOS SITIOS WEB O APLICACIONES Y BOTONES PARA COPIAR MENSAJES Y USAR PLANTILLAS, BOTON PARA ELEGIR SI SUBIR A SUNRUN Y A HUBSPOT O A AMBOS, PONER UN COLOR DEPENDIENDO DEL ESTADO DEL FSD EN SUNRUN, (MIRAR CUADERNO), PONER UNA INTERFAZ DISTINTA PARA LA VENTANA PRINCIPAL QUE SEA COMO UN BOTON QUE DIGA "CAPTURA" Y "COMPARADOR, DESDE AHI TAMBIEN QUE HAYA UN BOTON EN LA PARTE DE ARRIBA PARA LA CONFIGURACION
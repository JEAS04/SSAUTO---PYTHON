import pyautogui

# Definimos la región que queremos capturar:
# (X inicial, Y inicial, Ancho, Alto)
region_a_capturar = (100, 200, 500, 400) 

# Realizamos la captura sólo de esa zona
captura = pyautogui.screenshot(region=region_a_capturar)

# Guardamos la imagen en el disco
captura.save("captura_region.png")

print(f"Has capturado una región de: {region_a_capturar[2]} px de ancho por {region_a_capturar[3]} px de alto.")

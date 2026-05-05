import tkinter as tk
from PIL import ImageGrab


class CapturadorRecorte:
    def __init__(self):
        self.root = tk.Tk()
        # Hace que la ventana no tenga bordes y cubra toda la pantalla
        self.root.overrideredirect(True)
        self.root.geometry(
            f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0"
        )
        self.root.attributes("-alpha", 0.3)  # Hace la ventana semi-transparente
        self.root.config(cursor="cross")  # Cambia el cursor a una cruz

        # Crea un lienzo donde dibujaremos el rectángulo
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)

        # Eventos del ratón
        self.canvas.bind("<ButtonPress-1>", self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_clic)

        self.inicio_x = None
        self.inicio_y = None
        self.rectangulo = None

    def al_hacer_clic(self, event):
        # Guarda las coordenadas iniciales
        self.inicio_x = event.x
        self.inicio_y = event.y
        # Crea el rectángulo en pantalla
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x,
            self.inicio_y,
            self.inicio_x,
            self.inicio_y,
            outline="red",
            width=2,
        )

    def al_arrastrar(self, event):
        # Actualiza las dimensiones del rectángulo mientras arrastras
        self.canvas.coords(
            self.rectangulo, self.inicio_x, self.inicio_y, event.x, event.y
        )

    def al_soltar_clic(self, event):
        # Coordenadas finales
        fin_x, fin_y = event.x, event.y

        # Calcula los límites exactos de la caja (bounding box)
        x1 = min(self.inicio_x, fin_x)
        y1 = min(self.inicio_y, fin_y)
        x2 = max(self.inicio_x, fin_x)
        y2 = max(self.inicio_y, fin_y)

        # Calcula el ancho y el alto
        ancho = x2 - x1
        alto = y2 - y1

        # Cierra la interfaz para que no salga en la captura de pantalla
        self.root.withdraw()
        self.root.update()

        if ancho > 10 and alto > 10:
            print(f"📍 Región seleccionada:")
            print(f"   Coordenada inicial: (X: {x1}, Y: {y1})")
            print(f"   Dimensiones: Ancho: {ancho} px | Alto: {alto} px")

            # Toma la captura de pantalla de la región (X1, Y1, X2, Y2)
            captura = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            captura.save("captura_seleccionada.png")
            print("💾 Imagen guardada como 'captura_seleccionada.png'")
        else:
            print("⚠️ Selección demasiado pequeña. No se tomó captura.")

        self.root.destroy()

    def iniciar(self):
        self.root.mainloop()


# Ejecutar el programa
if __name__ == "__main__":
    print("Haz clic y arrastra para seleccionar el área que deseas capturar.")
    app = CapturadorRecorte()
    app.iniciar()

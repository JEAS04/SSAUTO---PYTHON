import tkinter as tk
import ctypes

# ESTA LÍNEA DEBE IR ANTES DE CREAR LA VENTANA TKINTER
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # Para Windows 8.1 y 10/11
except:
    ctypes.windll.user32.SetProcessDPIAware() # Para versiones más antiguas

class MedidorDeRegion:
    def __init__(self):
        self.root = tk.Tk()
        # Ventana sin bordes que cubre toda la pantalla
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.attributes("-alpha", 0.3)  # Hace la ventana semi-transparente
        self.root.config(cursor="cross")

        # Lienzo para dibujar
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)

        # Eventos del ratón
        self.canvas.bind("<ButtonPress-1>", self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>", self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>", self.al_soltar_clic)

        self.inicio_x = None
        self.inicio_y = None
        self.rectangulo = None
        self.texto = None

    def al_hacer_clic(self, event):
        self.inicio_x = event.x
        self.inicio_y = event.y
        # Crea el rectángulo
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, 
            outline="red", width=2
        )
        # Crea el texto que mostrará las medidas
        self.texto = self.canvas.create_text(
            self.inicio_x + 10, self.inicio_y - 10, 
            text="0 x 0", fill="white", font=("Arial", 12, "bold"), anchor="nw"
        )

    def al_arrastrar(self, event):
        # Actualiza las dimensiones del rectángulo
        self.canvas.coords(self.rectangulo, self.inicio_x, self.inicio_y, event.x, event.y)
        
        # Calcula el ancho y el alto actuales
        ancho = abs(event.x - self.inicio_x)
        alto = abs(event.y - self.inicio_y)
        
        # Actualiza el texto con las medidas en tiempo real
        self.canvas.itemconfig(self.texto, text=f"{ancho} x {alto} px")
        
        # Mueve el texto junto al cursor para que siempre sea visible
        self.canvas.coords(self.texto, event.x + 10, event.y + 10)

    def al_soltar_clic(self, event):
        # Calcula dimensiones finales
        ancho = abs(event.x - self.inicio_x)
        alto = abs(event.y - self.inicio_y)
        
        x_inicial = min(self.inicio_x, event.x)
        y_inicial = min(self.inicio_y, event.y)

        print(f"\n📍 Medición final:")
        print(f"   Origen en pantalla: (X: {x_inicial}, Y: {y_inicial})")
        print(f"   Dimensiones finales: {ancho} de ancho x {alto} de alto (píxeles)")

        # No se ejecuta ninguna captura ni guardado de archivo aquí
        self.root.destroy()

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Haz clic y arrastra para medir cualquier región de tu pantalla.")
    app = MedidorDeRegion()
    app.iniciar()

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
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)

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
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, 
            outline="red", width=2
        )
        self.texto = self.canvas.create_text(
            self.inicio_x + 10, self.inicio_y - 10, 
            text="0 x 0", fill="white", font=("Arial", 12, "bold"), anchor="nw"
        )

    def al_arrastrar(self, event):
        self.canvas.coords(self.rectangulo, self.inicio_x, self.inicio_y, event.x, event.y)
        ancho = abs(event.x - self.inicio_x)
        alto = abs(event.y - self.inicio_y)
        self.canvas.itemconfig(self.texto, text=f"{ancho} x {alto} px")
        self.canvas.coords(self.texto, event.x + 10, event.y + 10)

    def al_soltar_clic(self, event):
        # Calcula el punto superior izquierdo (top, left)
        # min() asegura que funcione aunque arrastres de abajo hacia arriba
        top = min(self.inicio_y, event.y)
        left = min(self.inicio_x, event.x)
        
        # Calcula las dimensiones
        width = abs(event.x - self.inicio_x)
        height = abs(event.y - self.inicio_y)

        # Crea el diccionario con el formato exacto que pediste
        REGION = {
            "top": top,
            "left": left,
            "width": width,
            "height": height
        }

        # Imprime el resultado en consola
        print("\n📋 Copia tu región aquí:")
        print(f"REGION = {REGION}")

        self.root.destroy()

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Haz clic y arrastra para obtener el diccionario de la región.")
    app = MedidorDeRegion()
    app.iniciar()

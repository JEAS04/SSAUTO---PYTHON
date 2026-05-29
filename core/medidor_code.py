"""
core/medidor_code — Herramienta visual para seleccionar una región de pantalla.

Contiene el código del medidor como string (MEDIDOR_CODE) porque se lanza
en un subproceso separado con `subprocess.Popen([sys.executable, "-c", ...])`.
Esto es necesario porque el medidor necesita su propia ventana Tkinter a
pantalla completa sin bloquear la ventana principal de la aplicación.

El subproceso imprime la región seleccionada en stdout con el formato:
    REGION = {'top': 392, 'left': 524, 'width': 934, 'height': 404}
La app principal captura esa salida y actualiza los campos de coordenadas.
"""

# Código completo del medidor como string.
# Se usa -c para no requerir un archivo .py extra distribuido con la app.
# Soporta un argumento opcional --monitor <índice> para elegir en qué
# monitor mostrar la superposición. Con 0 (Todos los monitores) usa la
# ventana virtual del escritorio completo; con 1, 2, … se limita a ese
# monitor físico.
MEDIDOR_CODE = """
import tkinter as tk
import ctypes
import sys

# Necesario en Windows para que las coordenadas sean correctas en
# pantallas con escala (ej. 150 % DPI); sin esto, las coords estarían
# desplazadas en monitores de alta resolución.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass  # En macOS/Linux no hay windll, se ignora sin error.


# ── Detectar monitor desde argumentos ────────────────────────────────
# Busca "--monitor X" en sys.argv. Si no se encuentra, usa monitor 0
# (virtual / todos los monitores) para mantener compatibilidad.
try:
    idx = sys.argv.index("--monitor")
    MONITOR_IDX = int(sys.argv[idx + 1])
except (ValueError, IndexError):
    MONITOR_IDX = 0


def _obtener_monitores():
    \"\"\"Usa mss para obtener la lista de monitores.\"\"\"
    try:
        import mss
        with mss.MSS() as sct:
            return sct.monitors
    except Exception:
        return []


MONITORES = _obtener_monitores()


def _bounds_monitor(indice):
    \"\"\"
    Devuelve (x, y, ancho, alto) del monitor en la posición `indice`.
    Si el índice está fuera de rango, devuelve el escritorio virtual (índice 0).
    \"\"\"
    if 0 <= indice < len(MONITORES):
        m = MONITORES[indice]
    else:
        m = MONITORES[0]
    return m["left"], m["top"], m["width"], m["height"]

# Desplazamiento del monitor donde se mostrará la ventana.
MON_X, MON_Y, MON_W, MON_H = _bounds_monitor(MONITOR_IDX)


class MedidorDeRegion:
    \"\"\"
    Ventana transparente que permite al usuario dibujar un rectángulo
    y obtener sus coordenadas (top, left, width, height).

    Si se especificó un monitor distinto de 0, la ventana se posiciona
    únicamente sobre ese monitor. Con monitor 0 (virtual) cubre toda el
    área del escritorio.
    \"\"\"

    def __init__(self):
        self.root = tk.Tk()
        # Sin bordes ni barra de título: ocupa toda la pantalla o el monitor elegido.
        self.root.overrideredirect(True)
        self.root.geometry(f"{MON_W}x{MON_H}+{MON_X}+{MON_Y}")
        # Semitransparente para que el usuario vea lo que va a capturar.
        self.root.attributes("-alpha", 0.3)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>",   self.al_hacer_clic)
        self.canvas.bind("<B1-Motion>",        self.al_arrastrar)
        self.canvas.bind("<ButtonRelease-1>",  self.al_soltar_clic)

        # Estado interno del dibujo
        self.inicio_x  = None
        self.inicio_y  = None
        self.rectangulo = None
        self.texto      = None

    def al_hacer_clic(self, event):
        \"\"\"Registra el punto de inicio y crea el rectángulo vacío.\"\"\"
        self.inicio_x = event.x
        self.inicio_y = event.y
        self.rectangulo = self.canvas.create_rectangle(
            self.inicio_x, self.inicio_y,
            self.inicio_x, self.inicio_y,
            outline="red", width=2,
        )
        # Texto que muestra las dimensiones mientras se arrastra.
        self.texto = self.canvas.create_text(
            self.inicio_x + 10, self.inicio_y - 10,
            text="0 x 0", fill="white",
            font=("Arial", 12, "bold"), anchor="nw",
        )

    def al_arrastrar(self, event):
        \"\"\"Actualiza el rectángulo y el texto de dimensiones en tiempo real.\"\"\"
        self.canvas.coords(
            self.rectangulo,
            self.inicio_x, self.inicio_y,
            event.x, event.y,
        )
        ancho = abs(event.x - self.inicio_x)
        alto  = abs(event.y - self.inicio_y)
        self.canvas.itemconfig(self.texto, text=f"{ancho} x {alto} px")
        # El texto sigue al cursor para no tapar el rectángulo.
        self.canvas.coords(self.texto, event.x + 10, event.y + 10)

    def al_soltar_clic(self, event):
        \"\"\"
        Calcula la región final y la imprime en stdout.

        La app principal lee esta línea del subproceso para obtener las
        coordenadas sin necesitar archivos temporales.

        Nota: las coordenadas devueltas son absolutas (pantalla virtual),
        no relativas al monitor. Esto es necesario porque mss.grab()
        espera coordenadas absolutas.
        \"\"\"
        top    = MON_Y + min(self.inicio_y, event.y)
        left   = MON_X + min(self.inicio_x, event.x)
        width  = abs(event.x - self.inicio_x)
        height = abs(event.y - self.inicio_y)
        region = {"top": top, "left": left, "width": width, "height": height}
        # flush=True garantiza que el pipe lo reciba aunque no haya salto de línea.
        print(f"REGION = {region}", flush=True)
        self.root.destroy()

    def iniciar(self):
        \"\"\"Lanza el loop de eventos de Tkinter.\"\"\"
        self.root.mainloop()


app = MedidorDeRegion()
app.iniciar()
"""

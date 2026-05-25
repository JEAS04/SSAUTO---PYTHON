"""
custom_ctkframe.py — Clase base CustomCTkFrame con métodos para controlar la ventana raíz.

Proporciona métodos wrapper para iconify, deiconify y geometry sobre la ventana raíz.
"""

import customtkinter as ctk


class CustomCTkFrame(ctk.CTkFrame):
    """
    Clase base que extiende CTkFrame con métodos para controlar la ventana raíz.

    Métodos agregados:
    ------------------
    get_root()              → Obtiene la ventana raíz (winfo_toplevel)
    iconify_window()        → Minimiza la ventana raíz
    deiconify_window()      → Restaura la ventana raíz
    set_window_geometry(str)→ Configura la geometría de la ventana raíz
    """

    def get_root(self):
        """
        Obtiene la ventana raíz (toplevel).

        Returns:
            tk.Tk | tk.Toplevel : La ventana raíz del frame actual.
        """
        return self.winfo_toplevel()

    def iconify_window(self):
        """
        Minimiza la ventana raíz.

        Este método obtiene la ventana raíz y la minimiza (state='iconic').
        No hace nada si ya está minimizada.
        """
        root = self.get_root()
        try:
            root.iconify()
        except Exception as e:
            print(f"Error al minimizar ventana: {e}")

    def deiconify_window(self):
        """
        Restaura la ventana raíz si está minimizada.

        Este método obtiene la ventana raíz y la restaura (state='normal').
        También trae la ventana al frente.
        """
        root = self.get_root()
        try:
            root.deiconify()
            root.lift()
            root.focus_force()
        except Exception as e:
            print(f"Error al restaurar ventana: {e}")

    def set_window_geometry(self, geometry: str):
        """
        Configura la geometría (tamaño y posición) de la ventana raíz.

        Parameters:
        -----------
        geometry : str
            Geometría en formato "WIDTHxHEIGHT+X+Y"
            Ejemplo: "800x600+100+50"
        """
        root = self.get_root()
        try:
            root.geometry(geometry)
        except Exception as e:
            print(f"Error al establecer geometría: {e}")

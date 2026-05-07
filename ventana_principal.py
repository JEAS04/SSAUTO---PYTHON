"""
ventana_principal.py — Ventana principal de SSAuto (clase App).

Construye y gestiona toda la interfaz gráfica de CustomTkinter:
región de captura, lista de sitios, opciones de Chrome, atajo de teclado,
registro de actividad y barra de estado.

La lógica de negocio (captura, subida, login) vive en automatizacion.py;
aquí solo se construye la UI y se conectan los eventos a esas funciones.
"""

import ast
import shutil
import subprocess
import sys
import threading
import tkinter.font
import time
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

from automatizacion import capturar, subir
from configuracion import SITIOS, cargar_config, guardar_config
from credenciales import cargar_credenciales
from medidor import MEDIDOR_CODE
from ventana_credenciales import VentanaCredenciales


class App(ctk.CTk):
    """
    Ventana principal de la aplicación SSAuto.

    Orquesta la interacción entre el usuario y los módulos de automatización.
    Toda actualización de la UI desde hilos secundarios se hace con self.after()
    para evitar problemas de concurrencia con Tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title("SSAuto — Automatización de capturas")
        self.resizable(True, True)

        # Estado interno de la sesión.
        self._credenciales_sesion = {}  # credenciales en memoria (no en disco)
        self._keybind_actual = None
        self._config = cargar_config()

        self._construir_ui()

        # Interceptar el cierre para guardar la config antes de salir.
        self.protocol("WM_DELETE_WINDOW", self._al_cerrar)

        # Centrar la ventana en la pantalla.
        self.update_idletasks()
        ancho = min(880, self.winfo_screenwidth() - 40)
        alto = min(760, self.winfo_screenheight() - 80)
        pos_x = max(0, (self.winfo_screenwidth() - ancho) // 2)
        pos_y = max(0, (self.winfo_screenheight() - alto) // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.minsize(480, 400)

        # Si falta alguna credencial, abrir el diálogo de login al iniciar.
        faltan_creds = any(
            s.get("necesita_login") and not cargar_credenciales(s["nombre"])[0]
            for s in SITIOS
        )
        if faltan_creds:
            self.after(100, self._abrir_login_inicial)

    # ── Construcción de la UI ─────────────────────────────────────────

    def _construir_ui(self):
        """Construye el layout principal con todas las secciones."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame desplazable para que el contenido no se corte en pantallas pequeñas.
        self._frame_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_hover_color=("gray60", "gray40"),
        )
        self._frame_scroll.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._frame_scroll.grid_columnconfigure(0, weight=1)

        padre = self._frame_scroll

        # 1. Región de captura: campo para pegar dict y controles individuales.
        sec1 = self._seccion(padre, "  REGIÓN DE CAPTURA", fila=0)
        self._crear_entrada_pegar(sec1)
        self._separador(sec1)
        self._crear_coordenadas(sec1)
        ctk.CTkButton(
            sec1,
            text="  Medir región en pantalla",
            command=self._lanzar_medidor,
            font=ctk.CTkFont(size=11),
            height=32,
        ).pack(fill="x", pady=(4, 0))

        # 2. Sitios de destino: muestra estado de sesión/credenciales de cada sitio.
        sec2 = self._seccion(padre, "  SITIOS DE DESTINO", fila=1)
        self._crear_sitios_status(sec2)

        # 3. Opciones: headless, chrome existente y atajo de teclado.
        sec3 = self._seccion(padre, "  OPCIONES", fila=2)
        self._crear_opciones(sec3)

        # 4. Botón principal.
        self.btn = ctk.CTkButton(
            padre,
            text="  Capturar y subir",
            command=self._ejecutar,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=42,
            fg_color=("#238636", "#2ea043"),
            hover_color=("#1e7a30", "#26963a"),
        )
        self.btn.grid(row=3, column=0, sticky="ew", padx=0, pady=(8, 8))

        # 5. Registro de actividad con colores por tipo de mensaje.
        sec4 = self._seccion(padre, "  REGISTRO", fila=4, pady=(0, 8))
        self.log_texto = ctk.CTkTextbox(
            sec4,
            font=ctk.CTkFont(
                family=(
                    "Cascadia Code"
                    if self._fuente_existe("Cascadia Code")
                    else "Consolas"
                ),
                size=10,
            ),
            wrap="word",
            height=140,
        )
        self.log_texto.pack(fill="both", expand=True)

        # Configurar colores de los tags en el widget interno de Tk.
        tb = self.log_texto._textbox
        tb.tag_configure("ok", foreground="#3fb950")
        tb.tag_configure("error", foreground="#f85149")
        tb.tag_configure("flecha", foreground="#79c0ff")
        tb.tag_configure("dim", foreground="#8b949e")
        tb.tag_configure("ts", foreground="#6e7681")

        # 6. Barra de estado en la parte inferior.
        self._crear_barra_estado(padre)

    def _seccion(self, padre, titulo: str, fila: int, col=0, colspan=2, pady=(0, 10)):
        """
        Crea y devuelve un frame con encabezado y cuerpo para agrupar controles.

        Evita repetir el mismo bloque de código de grid/pack para cada sección
        de la interfaz.
        """
        frame = ctk.CTkFrame(padre, fg_color=("gray95", "gray20"), border_width=1)
        frame.grid(
            row=fila, column=col, columnspan=colspan, sticky="nsew", pady=pady, padx=0
        )
        padre.grid_columnconfigure(0, weight=1)

        # Encabezado gris con el título de la sección.
        encabezado = ctk.CTkFrame(frame, fg_color=("gray88", "gray25"), height=28)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)
        ctk.CTkLabel(
            encabezado,
            text=titulo,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray30", "gray60"),
        ).pack(side="left", padx=14)

        # Cuerpo de la sección donde se colocan los controles hijos.
        cuerpo = ctk.CTkFrame(frame, fg_color="transparent")
        cuerpo.pack(fill="x", padx=14, pady=12)
        return cuerpo

    def _crear_entrada_pegar(self, padre):
        """
        Crea el campo de texto para pegar un dict de región completo.

        Permite copiar la salida del medidor directamente y aplicarla
        de una vez, sin escribir cada coordenada a mano.
        """
        fila = ctk.CTkFrame(padre, fg_color="transparent")
        fila.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            fila,
            text="Pegar región:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))

        self.region_paste_var = ctk.StringVar(
            value="{'top': 392, 'left': 524, 'width': 934, 'height': 404}"
        )
        entrada = ctk.CTkEntry(
            fila,
            textvariable=self.region_paste_var,
            font=ctk.CTkFont(size=11),
        )
        entrada.pack(side="left", padx=(0, 8), fill="x", expand=True)
        # Aplicar automáticamente al perder el foco o presionar Enter.
        entrada.bind("<FocusOut>", self._parsear_region)
        entrada.bind("<Return>", self._parsear_region)
        self.region_paste = entrada

        ctk.CTkButton(
            fila,
            text="Aplicar",
            command=self._parsear_region,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

    def _crear_coordenadas(self, padre):
        """
        Crea los cuatro campos numéricos individuales (top, left, width, height).

        Cada campo tiene un IntVar que, al cambiar, actualiza el campo de texto
        'Pegar región' en tiempo real mediante self._sincronizar_paste.
        """
        frame_coords = ctk.CTkFrame(padre, fg_color="transparent")
        frame_coords.pack(fill="x", pady=(0, 10))

        self.region_vars = {}
        campos = [("top", 392), ("left", 524), ("width", 934), ("height", 404)]

        for i, (etiqueta, valor) in enumerate(campos):
            caja = ctk.CTkFrame(
                frame_coords, fg_color=("gray90", "gray25"), border_width=1
            )
            caja.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))

            ctk.CTkLabel(
                caja,
                text=etiqueta.upper(),
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=("gray50", "gray50"),
            ).pack(pady=(6, 0))

            var = ctk.IntVar(value=valor)
            ctk.CTkEntry(
                caja,
                textvariable=var,
                width=70,
                font=ctk.CTkFont(size=13, weight="bold"),
                justify="center",
                border_width=0,
            ).pack(pady=(0, 6))
            var.trace_add("write", self._sincronizar_paste)
            self.region_vars[etiqueta] = var

    def _crear_sitios_status(self, padre):
        """
        Crea el panel que muestra el estado de autenticación de cada sitio
        y los botones 'Credenciales' y 'Renovar sesión'.
        """
        self._frame_sitios = ctk.CTkFrame(padre, fg_color="transparent")
        self._frame_sitios.pack(fill="x", pady=(0, 8))
        self._actualizar_sitios_status()

        # Botones de gestión de sesión debajo de la lista de sitios.
        fila_botones = ctk.CTkFrame(padre, fg_color="transparent")
        fila_botones.pack(fill="x")

        ctk.CTkButton(
            fila_botones,
            text="Credenciales",
            command=self._abrir_credenciales,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            fila_botones,
            text="Renovar sesión",
            command=self._renovar_sesion,
            font=ctk.CTkFont(size=10),
            width=110,
            height=28,
        ).pack(side="left")

    def _crear_opciones(self, padre):
        """
        Crea los toggles de modo headless, Chrome existente y el atajo de teclado.
        """
        # Toggle: modo headless (Chrome sin ventana visible)
        self.headless_var = ctk.BooleanVar(value=False)
        self._fila_toggle(
            padre, "Modo headless (sin ventana de Chrome)", self.headless_var
        )
        self._separador(padre)

        # Toggle: usar Chrome ya abierto por el usuario en puerto 9222
        self.chrome_existente_var = ctk.BooleanVar(value=False)
        self._fila_toggle(
            padre, "Usar Chrome ya abierto (puerto 9222)", self.chrome_existente_var
        )

        ctk.CTkButton(
            padre,
            text="Abrir Chrome con depuración",
            command=self._abrir_chrome_debug,
            font=ctk.CTkFont(size=10),
            height=28,
        ).pack(anchor="e", pady=(4, 0))

        self._separador(padre)

        # Campo para configurar el atajo de teclado global.
        fila_atajo = ctk.CTkFrame(padre, fg_color="transparent")
        fila_atajo.pack(fill="x")

        ctk.CTkLabel(
            fila_atajo,
            text="Atajo:",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(0, 8))

        self.keybind_var = ctk.StringVar()
        self.keybind_entry = ctk.CTkEntry(
            fila_atajo,
            textvariable=self.keybind_var,
            font=ctk.CTkFont(size=11),
        )
        self.keybind_entry.pack(side="left", padx=(0, 8), fill="x", expand=True)
        # Captura la tecla presionada en vez de mostrar el carácter.
        self.keybind_entry.bind("<KeyPress>", self._capturar_tecla)

        ctk.CTkButton(
            fila_atajo,
            text="Aplicar",
            command=self._aplicar_keybind,
            font=ctk.CTkFont(size=10),
            width=70,
            height=28,
        ).pack(side="left")

        # Etiqueta informativa que muestra el atajo activo.
        self.keybind_label = ctk.CTkLabel(
            padre,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray40", "gray60"),
        )
        self.keybind_label.pack(anchor="w", pady=(4, 0))

        # Aplicar el atajo guardado en config al iniciar.
        atajo_inicial = self._config.get("keybind", "<Control-Return>")
        try:
            self.bind(atajo_inicial, lambda e: self._ejecutar())
            self._keybind_actual = atajo_inicial
            self.keybind_var.set(atajo_inicial)
            self.keybind_label.configure(
                text=f"Combinación activa: {self._keybind_legible(atajo_inicial)}",
                text_color=("green", "#3fb950"),
            )
        except Exception:
            self.keybind_label.configure(
                text="Atajo no válido",
                text_color=("red", "#f85149"),
            )

    def _crear_barra_estado(self, padre):
        """
        Crea la barra inferior con el indicador de estado (●) y la hora
        del último proceso ejecutado.
        """
        frame_estado = ctk.CTkFrame(padre, fg_color="transparent")
        frame_estado.grid(row=5, column=0, sticky="ew", pady=(4, 0))

        self._punto_estado = ctk.CTkLabel(
            frame_estado,
            text="●",
            font=ctk.CTkFont(size=12),
            text_color=("#2ea043", "#3fb950"),
        )
        self._punto_estado.pack(side="left")

        self.status_var = ctk.StringVar(value="Listo")
        ctk.CTkLabel(
            frame_estado,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
        ).pack(side="left", padx=(4, 0))

        self._label_ultimo_proceso = ctk.CTkLabel(
            frame_estado,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        )
        self._label_ultimo_proceso.pack(side="right")

    # ── Helpers de UI ─────────────────────────────────────────────────

    def _fila_toggle(self, padre, texto: str, var: ctk.BooleanVar):
        """Crea una fila con un switch (on/off) y su etiqueta descriptiva."""
        fila = ctk.CTkFrame(padre, fg_color="transparent")
        fila.pack(fill="x", pady=4)
        ctk.CTkSwitch(fila, text=texto, variable=var, font=ctk.CTkFont(size=11)).pack(
            side="left"
        )

    def _separador(self, padre):
        """Línea horizontal de un píxel para separar secciones visualmente."""
        ctk.CTkFrame(padre, fg_color=("gray80", "gray30"), height=1).pack(
            fill="x", pady=10
        )

    def _fuente_existe(self, nombre: str) -> bool:
        """Devuelve True si la fuente está instalada en el sistema."""
        return nombre in tkinter.font.families()

    def _keybind_legible(self, kb: str) -> str:
        """Convierte el formato interno de Tkinter a uno más legible para el usuario."""
        return (
            kb.replace("<", "")
            .replace(">", "")
            .replace("Control", "Ctrl")
            .replace("Return", "Enter")
            .replace("-", "+")
        )

    # ── Actualización de estado de sitios ────────────────────────────

    def _actualizar_sitios_status(self):
        """
        Redibuja la lista de sitios con su estado actual de sesión.

        Se llama al iniciar, después de modificar credenciales y después
        de renovar la sesión, para que el usuario siempre vea el estado real.
        """
        # Limpiar la lista antes de redibujar.
        for widget in self._frame_sitios.winfo_children():
            widget.destroy()

        for sitio in SITIOS:
            nombre = sitio["nombre"]
            tiene_sesion = Path(f"cookies/{nombre.replace(' ', '_')}.pkl").exists()
            tiene_creds = bool(cargar_credenciales(nombre)[0])

            fila = ctk.CTkFrame(
                self._frame_sitios, fg_color=("gray93", "gray25"), border_width=1
            )
            fila.pack(fill="x", pady=(0, 4))

            # Icono y texto de estado según la situación del sitio.
            if not sitio["necesita_login"]:
                icono, estado, color = "○", "sin login", ("green", "#3fb950")
            elif tiene_sesion:
                icono, estado, color = "●", "sesión guardada", ("royalblue", "#79c0ff")
            elif tiene_creds:
                icono, estado, color = "◑", "credenciales OK", ("orange", "#d29922")
            else:
                icono, estado, color = "○", "sin configurar", ("red", "#f85149")

            ctk.CTkLabel(
                fila, text=f" {icono} {nombre}", font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(
                fila, text=f"  {estado}  ", font=ctk.CTkFont(size=10), text_color=color
            ).pack(side="right", padx=10, pady=6)

    # ── Registro de actividad ─────────────────────────────────────────

    def _log(self, msg: str):
        """
        Agrega una línea al registro de actividad con timestamp y color.

        Usa el widget interno _textbox para poder aplicar tags de color, ya
        que CTkTextbox no expone esa funcionalidad directamente.
        """
        ts = datetime.now().strftime("%H:%M:%S")

        if msg.startswith("✓"):
            tag = "ok"
        elif msg.startswith("✗"):
            tag = "error"
        elif msg.startswith("→") or msg.startswith("  →"):
            tag = "flecha"
        else:
            tag = "dim"

        self.log_texto.configure(state="normal")
        tb = self.log_texto._textbox  # widget tk.Text interno de CTkTextbox
        tb.insert("end", f"[{ts}] ", "ts")
        tb.insert("end", msg + "\n", tag)
        self.log_texto.see("end")
        self.log_texto.configure(state="disabled")

    def _set_status(self, texto: str):
        """
        Actualiza el texto y el color del indicador de estado en la barra inferior.
        """
        self.status_var.set(texto)
        colores = {
            "Listo": ("#2ea043", "#3fb950"),
            "Ejecutando...": ("#d29922", "#d29922"),
            "Completado": ("#2ea043", "#3fb950"),
            "Error": ("#f85149", "#f85149"),
        }
        self._punto_estado.configure(
            text_color=colores.get(texto, ("gray40", "gray60"))
        )

    # ── Lógica del medidor de región ──────────────────────────────────

    def _lanzar_medidor(self):
        """
        Lanza el medidor de región en un subproceso separado y espera su resultado.

        Se minimiza la ventana principal para no tapar la pantalla mientras
        el usuario selecciona la región. La reabre al recibir el resultado.
        """
        self._log("→ Abre el medidor — haz clic y arrastra en pantalla...")
        self.btn.configure(state="disabled")
        self.iconify()  # Minimizar ventana principal.

        def _esperar():
            proc = subprocess.Popen(
                [sys.executable, "-c", MEDIDOR_CODE],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            stdout, _ = proc.communicate()
            for linea in stdout.splitlines():
                if linea.startswith("REGION ="):
                    valor = linea.split("=", 1)[1].strip()
                    try:
                        region = ast.literal_eval(valor)
                        # Actualizar la UI desde el hilo principal.
                        self.after(0, lambda r=region: self._aplicar_region(r))
                        self.after(0, self.deiconify)
                        return
                    except Exception:
                        pass
            self.after(0, lambda: self._log("✗ No se pudo leer la región del medidor."))
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

        threading.Thread(target=_esperar, daemon=True).start()

    def _aplicar_region(self, region: dict):
        """Actualiza los cuatro campos de coordenadas con los valores del medidor."""
        for clave in ("top", "left", "width", "height"):
            if clave in region:
                self.region_vars[clave].set(int(region[clave]))
        self._log(f"✓ Región actualizada: {region}")
        self.btn.configure(state="normal")

    def _parsear_region(self, event=None):
        """
        Parsea el contenido del campo 'Pegar región' y actualiza los campos individuales.

        Acepta tanto el dict puro como el formato 'REGION = {...}'.
        """
        texto = self.region_paste_var.get().strip()
        if "=" in texto:
            texto = texto.split("=", 1)[1].strip()
        try:
            region = ast.literal_eval(texto)
            for clave in ("top", "left", "width", "height"):
                if clave in region:
                    self.region_vars[clave].set(int(region[clave]))
        except Exception:
            messagebox.showerror(
                "Formato inválido",
                "Pega el diccionario con el formato:\n"
                "{'top': 392, 'left': 524, 'width': 934, 'height': 404}",
            )

    def _sincronizar_paste(self, *_):
        """
        Sincroniza el campo 'Pegar región' cuando el usuario edita
        alguna de las coordenadas individuales.
        """
        try:
            d = {k: v.get() for k, v in self.region_vars.items()}
            self.region_paste_var.set(str(d))
        except Exception:
            pass

    # ── Acciones de sesión ────────────────────────────────────────────

    def _abrir_login_inicial(self):
        """Abre el diálogo de credenciales automáticamente al iniciar si faltan datos."""
        win = VentanaCredenciales(self, SITIOS)
        if win.confirmado:
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")

    def _abrir_credenciales(self):
        """Abre el diálogo de credenciales desde el botón 'Credenciales'."""
        win = VentanaCredenciales(self, SITIOS)
        if win.confirmado:
            self._credenciales_sesion = win.credenciales_sesion
            self._log("✓ Credenciales actualizadas en sesión.")
        self._actualizar_sitios_status()

    def _renovar_sesion(self):
        """Borra todas las cookies guardadas para forzar un login completo en la próxima ejecución."""
        if Path("cookies").exists():
            shutil.rmtree("cookies")
        self._log("→ Cookies eliminadas. Se hará login en la próxima ejecución.")
        self._actualizar_sitios_status()

    def _abrir_chrome_debug(self):
        """
        Abre Google Chrome con el flag de depuración remota en el puerto 9222.

        Necesario para que la opción 'Usar Chrome ya abierto' pueda conectarse.
        Solo funciona en Windows porque busca el ejecutable en rutas predefinidas.
        """
        rutas_chrome = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        chrome_exe = next((r for r in rutas_chrome if Path(r).exists()), None)
        if not chrome_exe:
            self._log(
                "✗ No se encontró Chrome. Ábrelo manualmente con --remote-debugging-port=9222"
            )
            return
        subprocess.Popen(
            [
                chrome_exe,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\chrome_sesion_ssauto",
            ]
        )
        self._log("✓ Chrome abierto con depuración en puerto 9222")
        self._log("→ Inicia sesión en los sitios y luego ejecuta la captura")

    # ── Atajo de teclado ──────────────────────────────────────────────

    def _aplicar_keybind(self):
        """
        Registra el atajo de teclado introducido en el campo 'Atajo'
        y lo guarda en config para que persista entre ejecuciones.
        """
        nuevo = self.keybind_var.get().strip()
        if not nuevo:
            return

        # Desregistrar el atajo anterior antes de aplicar el nuevo.
        if self._keybind_actual:
            try:
                self.unbind(self._keybind_actual)
            except Exception:
                pass

        try:
            self.bind(nuevo, lambda e: self._ejecutar())
            self._keybind_actual = nuevo
            legible = self._keybind_legible(nuevo)
            self.keybind_label.configure(
                text=f"Combinación activa: {legible}",
                text_color=("green", "#3fb950"),
            )
            self._config["keybind"] = nuevo
            guardar_config(self._config)
        except Exception as e:
            self.keybind_label.configure(
                text=f"Atajo inválido: {e}",
                text_color=("red", "#f85149"),
            )
            self._keybind_actual = None

    def _capturar_tecla(self, event):
        """
        Intercepta la pulsación de tecla en el campo de atajo y construye
        el string en formato Tkinter (p. ej. <Control-Shift-F5>).

        Devuelve 'break' para evitar que el carácter se inserte en el campo.
        """
        partes = []
        if event.state & 0x4:
            partes.append("Control")
        if event.state & 0x1:
            partes.append("Shift")
        if event.state & 0x20000:
            partes.append("Alt")

        tecla = event.keysym
        # Ignorar si solo se presionó un modificador sin tecla principal.
        if tecla in ("Control_L", "Control_R", "Shift_L", "Shift_R", "Alt_L", "Alt_R"):
            return "break"

        partes.append(tecla)
        self.keybind_var.set("<" + "-".join(partes) + ">")
        return "break"

    # ── Proceso principal ─────────────────────────────────────────────

    def _ejecutar(self):
        """
        Inicia el proceso de captura y subida en un hilo secundario.

        Se corre en hilo separado para no bloquear la UI mientras trabaja.
        """
        self.btn.configure(state="disabled")
        self._set_status("Ejecutando...")
        # Limpiar el log antes de cada ejecución.
        self.log_texto.configure(state="normal")
        self.log_texto.delete("0.0", "end")
        self.log_texto.configure(state="disabled")
        threading.Thread(target=self._proceso, daemon=True).start()

    def _proceso(self):
        """
        Lógica del proceso completo: captura → subida a cada sitio.

        Toda actualización de la UI se hace con self.after() porque este
        método se ejecuta en un hilo secundario.
        """

        def ui(msg):
            # Wrapper thread-safe para llamar a _log desde el hilo secundario.
            self.after(0, lambda m=msg: self._log(m))

        try:
            region = {k: v.get() for k, v in self.region_vars.items()}
            ui(f"→ Capturando región: {region}")

            # Minimizar antes de capturar para no incluir la propia ventana.
            self.after(0, self.iconify)
            time.sleep(0.4)
            ruta = capturar(region)
            self.after(0, self.deiconify)
            ui(f"✓ Imagen guardada: {ruta}")
            ui("")

            headless = self.headless_var.get()
            usar_chrome_existente = self.chrome_existente_var.get()

            for sitio in SITIOS:
                ui(f"→ Subiendo a: {sitio['nombre']}")
                subir(
                    sitio,
                    ruta,
                    headless,
                    ui,
                    self._credenciales_sesion,
                    usar_chrome_existente,
                )
                ui("")

            ui("✓ Proceso completado.")
            self.after(0, lambda: self._set_status("Completado"))
            ahora = datetime.now().strftime("%H:%M:%S")
            self.after(
                0,
                lambda: self._label_ultimo_proceso.configure(
                    text=f"Último proceso: {ahora}"
                ),
            )
            self.after(0, self._actualizar_sitios_status)

        except Exception as e:
            self.after(0, lambda err=e: self._log(f"✗ Error general: {err}"))
            self.after(0, lambda: self._set_status("Error"))
        finally:
            # Siempre restaurar la ventana y habilitar el botón al terminar.
            self.after(0, self.deiconify)
            self.after(0, lambda: self.btn.configure(state="normal"))

    def _al_cerrar(self):
        """Guarda la configuración en disco antes de cerrar la ventana."""
        guardar_config(self._config)
        self.destroy()

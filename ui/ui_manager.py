"""
ui/ui_manager.py — Gestor de visibilidad y layout de paneles para SSAuto.

Proporciona un UIManager que controla que paneles/secciones y widgets
individuales estan visibles, persiste las preferencias del usuario en
config.json, y reconstruye dinamicamente el layout.

Soporta dos tipos de elementos registrados:
  - Secciones (type="section"): frames grid al CTkScrollableFrame.
    Al ocultar una seccion, las demas se reordenan sin huecos via _reflow().
  - Hijos (type="pack"/"grid"): widgets individuales dentro de una seccion.
    Se ocultan/muestran con pack_forget()/pack() o grid_remove()/grid().
    El contenedor padre se oculta automaticamente cuando todos sus hijos
    estan ocultos, eliminando huecos visuales.

Patron de uso:
    manager = UIManager(app_ref)
    manager.register("captura", frame_outer)
    manager.register_child("btn_capt", btn, parent_row,
                           "Boton Capturar", "pack", {...},
                           parent_pack_info={"fill": "x", "pady": (0, 4)})
    manager._apply_initial_state()
"""

import customtkinter as ctk
from config.configuracion import cargar_config, guardar_config


class UIManager:
    """Gestiona visibilidad, reflow de layout y persistencia de paneles.

    Args:
        app_ref: referencia a la instancia App.
    """

    CONFIG_KEY = "ui_visibility"

    SECTION_ORDER = [
        "captura",
        "apps",
        "destino",
        "opciones",
        "registro",
        "barra_estado",
    ]

    CHILD_ORDER = [
        "capt_perfiles",
        "capt_monitor",
        "capt_coordenadas",
        "capt_btn_detener",
        "capt_btn_medir",
        "capt_btn_capturar",
    ]

    PANEL_ORDER = SECTION_ORDER + CHILD_ORDER

    DEFAULT_VISIBILITY = {
        "captura": True,
        "apps": True,
        "destino": True,
        "opciones": True,
        "registro": True,
        "barra_estado": True,
        "capt_perfiles": True,
        "capt_monitor": True,
        "capt_coordenadas": True,
        "capt_btn_detener": True,
        "capt_btn_medir": True,
        "capt_btn_capturar": True,
    }

    PANEL_TITLES = {
        "captura": "Region de Captura",
        "apps": "Aplicaciones de Captura",
        "destino": "Destino y Sesion",
        "opciones": "Configuracion",
        "registro": "Registro (Log)",
        "barra_estado": "Barra de Estado",
        "capt_perfiles": "    Perfiles",
        "capt_monitor": "    Monitor",
        "capt_coordenadas": "    Coordenadas",
        "capt_btn_detener": "    Boton Detener",
        "capt_btn_medir": "    Boton Medir region",
        "capt_btn_capturar": "    Boton Capturar y subir",
    }

    PANEL_SECTION = {
        "captura": "captura",
        "capt_perfiles": "captura",
        "capt_monitor": "captura",
        "capt_coordenadas": "captura",
        "capt_btn_detener": "captura",
        "capt_btn_medir": "captura",
        "capt_btn_capturar": "captura",
        "apps": "apps",
        "destino": "destino",
        "opciones": "opciones",
        "registro": "registro",
        "barra_estado": "barra_estado",
    }

    SECTION_TITLES = {
        "captura": "Region de Captura",
        "apps": "Aplicaciones de Captura",
        "destino": "Destino y Sesion",
        "opciones": "Configuracion",
        "registro": "Registro (Log)",
        "barra_estado": "Barra de Estado",
    }

    def __init__(self, app_ref):
        self._app = app_ref
        self._panels = {}
        self._visibility = dict(self.DEFAULT_VISIBILITY)
        self._parent_pack = {}       # parent widget -> pack kwargs
        self._parent_children = {}   # parent widget -> [panel_id, ...]
        self._load_visibility()

    # ── Registration ─────────────────────────────────────────────────

    def register(self, panel_id, frame, pady=(0, 10), col=1):
        """Registra una seccion principal para control de visibilidad.

        Las secciones usan grid() en el CTkScrollableFrame y participan
        en el reflow automatico.
        """
        self._panels[panel_id] = {
            "widget": frame,
            "type": "section",
            "pady": pady,
            "col": col,
        }

    def register_child(self, panel_id, widget, parent, title,
                       layout_type="pack", layout_info=None,
                       parent_pack_info=None):
        """Registra un widget hijo para control de visibilidad individual.

        Los widgets hijos usan pack() o grid() dentro de su contenedor
        padre. Cuando todos los hijos de un mismo padre estan ocultos,
        el padre se oculta automaticamente para evitar huecos.

        Args:
            panel_id: identificador unico (ej. "capt_btn_capturar").
            widget: el widget tkinter a mostrar/ocultar.
            parent: widget contenedor padre.
            title: titulo para mostrar en el menu.
            layout_type: "pack" o "grid".
            layout_info: dict con opciones de pack/grid para restaurar.
            parent_pack_info: dict con opciones de pack para restaurar
                              el contenedor padre cuando vuelva a mostrarse.
        """
        self._panels[panel_id] = {
            "widget": widget,
            "type": layout_type,
            "parent": parent,
            "layout_info": layout_info or {},
            "pady": None,
            "col": None,
        }
        self.PANEL_TITLES.setdefault(panel_id, title)

        if parent_pack_info:
            self._parent_pack[id(parent)] = (parent, parent_pack_info)
        self._parent_children.setdefault(id(parent), []).append(panel_id)

    def unregister(self, panel_id):
        """Elimina un panel del registro."""
        info = self._panels.pop(panel_id, None)
        if info and info.get("parent"):
            pid = id(info["parent"])
            if pid in self._parent_children:
                self._parent_children[pid].remove(panel_id)

    # ── Visibility ────────────────────────────────────────────────────

    def is_visible(self, panel_id):
        """Devuelve True si el panel esta visible."""
        return self._visibility.get(panel_id, True)

    def show(self, panel_id):
        """Muestra un panel/widget y reordena el layout si es necesario."""
        if panel_id not in self._panels:
            return
        self._visibility[panel_id] = True
        self._save_visibility()
        info = self._panels[panel_id]
        if info["type"] == "section":
            self._reflow()
        else:
            self._show_child(info)

    def hide(self, panel_id):
        """Oculta un panel/widget y reordena el layout si es necesario."""
        if panel_id not in self._panels:
            return
        self._visibility[panel_id] = False
        self._save_visibility()
        info = self._panels[panel_id]
        if info["type"] == "section":
            self._reflow()
        else:
            self._hide_child(info)

    def toggle(self, panel_id):
        """Alterna la visibilidad de un panel."""
        if self.is_visible(panel_id):
            self.hide(panel_id)
        else:
            self.show(panel_id)

    def _show_child(self, info):
        """Restaura un widget hijo. Re-packea el padre si estaba oculto."""
        parent = info.get("parent")
        if parent is not None:
            parent_id_key = id(parent)
            if parent_id_key in self._parent_pack:
                parent_w, pack_info = self._parent_pack[parent_id_key]
                if not parent_w.winfo_ismapped():
                    parent_w.pack(**pack_info)

        if info["type"] == "pack":
            info["widget"].pack(**info["layout_info"])
        elif info["type"] == "grid":
            info["widget"].grid(**info["layout_info"])

    def _hide_child(self, info):
        """Oculta un widget hijo. Oculta el padre si todos sus hijos
        registrados estan ocultos, eliminando el pady/gap sobrante."""
        if info["type"] == "pack":
            info["widget"].pack_forget()
        elif info["type"] == "grid":
            info["widget"].grid_remove()

        parent = info.get("parent")
        if parent is not None:
            self._auto_hide_parent_if_empty(parent)

    def _auto_hide_parent_if_empty(self, parent):
        """Oculta el contenedor padre si todos sus hijos registrados
        estan ocultos. Elimina el gap del pady del contenedor vacio."""
        parent_id_key = id(parent)
        sibling_ids = self._parent_children.get(parent_id_key, [])
        all_hidden = all(
            not self._visibility.get(sid, True) for sid in sibling_ids
        )
        if all_hidden and parent_id_key in self._parent_pack:
            parent_w, _ = self._parent_pack[parent_id_key]
            parent_w.pack_forget()

    def _apply_initial_state(self):
        """Aplica el estado de visibilidad cargado.

        Oculta los hijos que deban estar ocultos, luego aplica
        auto-hide de padres vacios, y finalmente reflow de secciones.
        """
        # 1. Ocultar hijos no visibles (sin tocar padres aun)
        for panel_id, info in self._panels.items():
            if info["type"] != "section":
                if not self._visibility.get(panel_id, True):
                    if info["type"] == "pack":
                        info["widget"].pack_forget()
                    elif info["type"] == "grid":
                        info["widget"].grid_remove()

        # 2. Auto-ocultar padres cuyos hijos esten todos ocultos
        for parent_id_key, (parent_w, _) in self._parent_pack.items():
            sibling_ids = self._parent_children.get(parent_id_key, [])
            all_hidden = all(
                not self._visibility.get(sid, True) for sid in sibling_ids
            )
            if all_hidden:
                parent_w.pack_forget()

        # 3. Reflow de secciones
        self._reflow()

    # ── Layout reflow ─────────────────────────────────────────────────

    def _reflow(self):
        """Reasigna filas grid a las secciones visibles secuencialmente."""
        row = 0
        for panel_id in self.SECTION_ORDER:
            if panel_id not in self._panels:
                continue
            info = self._panels[panel_id]
            if self._visibility.get(panel_id, True):
                info["widget"].grid(
                    row=row,
                    column=info["col"],
                    sticky="ew",
                    pady=info["pady"],
                )
                row += 1
            else:
                info["widget"].grid_remove()

    # ── Persistence ───────────────────────────────────────────────────

    def _load_visibility(self):
        config = cargar_config()
        saved = config.get(self.CONFIG_KEY, {})
        if isinstance(saved, dict):
            for panel_id in self.DEFAULT_VISIBILITY:
                self._visibility[panel_id] = saved.get(
                    panel_id, self.DEFAULT_VISIBILITY[panel_id]
                )

    def _save_visibility(self):
        config = cargar_config()
        config[self.CONFIG_KEY] = dict(self._visibility)
        guardar_config(config)

    # ── Customization menu ────────────────────────────────────────────

    def get_panels(self):
        result = []
        for panel_id in self.PANEL_ORDER:
            if panel_id in self._panels:
                result.append({
                    "id": panel_id,
                    "title": self.PANEL_TITLES.get(panel_id, panel_id),
                    "visible": self._visibility.get(panel_id, True),
                    "section": self.PANEL_SECTION.get(panel_id, ""),
                })
        return result

    def show_customization_menu(self):
        """Abre ventana modal con toggles por elemento, agrupados por seccion."""
        modal = ctk.CTkToplevel(self._app)
        modal.title("Personalizar interfaz")
        modal.resizable(False, False)
        modal.transient(self._app)
        modal.withdraw()

        modal.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            modal,
            text="Mostrar / ocultar paneles",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).grid(row=0, column=0, pady=(16, 4), padx=24, sticky="w")

        ctk.CTkLabel(
            modal,
            text="Los cambios se aplican al instante.",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray50"),
        ).grid(row=1, column=0, pady=(0, 12), padx=24, sticky="w")

        ctk.CTkFrame(
            modal, height=1, fg_color=("gray80", "gray35")
        ).grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 8))

        panels = self.get_panels()
        last_section = None
        row_idx = 3

        for panel in panels:
            sec = panel.get("section", "")

            if sec != last_section and sec:
                if last_section is not None:
                    ctk.CTkFrame(
                        modal, height=1, fg_color=("gray85", "gray35")
                    ).grid(row=row_idx, column=0, sticky="ew",
                           padx=20, pady=(6, 2))
                    row_idx += 1

                ctk.CTkLabel(
                    modal,
                    text=self.SECTION_TITLES.get(sec, sec),
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=("gray40", "gray55"),
                ).grid(row=row_idx, column=0, pady=(4, 2), padx=24, sticky="w")
                row_idx += 1
                last_section = sec

            var = ctk.BooleanVar(value=panel["visible"])

            switch = ctk.CTkSwitch(
                modal,
                text=f"  {panel['title']}",
                variable=var,
                font=ctk.CTkFont(size=12),
                command=lambda pid=panel["id"], v=var: self._on_menu_toggle(pid, v),
            )
            switch.grid(row=row_idx, column=0, pady=(2, 2), padx=24, sticky="w")
            row_idx += 1

        ctk.CTkFrame(
            modal, height=1, fg_color=("gray80", "gray35")
        ).grid(row=row_idx, column=0, sticky="ew", padx=20, pady=(8, 0))
        row_idx += 1

        ctk.CTkButton(
            modal,
            text="Cerrar",
            font=ctk.CTkFont(size=12),
            fg_color=("gray70", "gray35"),
            hover_color=("gray60", "gray45"),
            command=modal.destroy,
        ).grid(row=row_idx, column=0, pady=(12, 16), padx=24, sticky="ew")

        from ui.posicion_ventanas import ubicar_junto_a_padre

        modal.deiconify()
        ubicar_junto_a_padre(modal, self._app)
        modal.grab_set()
        modal.wait_window()

    def _on_menu_toggle(self, panel_id, var):
        """Callback de los switches del menu — aplica el cambio al instante."""
        if var.get():
            self.show(panel_id)
        else:
            self.hide(panel_id)

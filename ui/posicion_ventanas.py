"""
Window positioning helpers for secondary SSAuto windows.

The goal is to open child windows beside the main window on the same physical
monitor, instead of letting Windows/Tk place them on monitor 1 by default.
"""

from __future__ import annotations

from core.monitors import obtener_monitores


def _parse_geometry(widget) -> tuple[int, int, int, int]:
    """Return (x, y, width, height) for a Tk widget/toplevel."""
    widget.update_idletasks()
    return (
        int(widget.winfo_rootx()),
        int(widget.winfo_rooty()),
        int(widget.winfo_width()),
        int(widget.winfo_height()),
    )


def _monitor_for_rect(x: int, y: int, width: int, height: int) -> dict | None:
    """Return the physical monitor containing the rectangle center."""
    monitors = obtener_monitores()
    if not monitors:
        return None

    center_x = x + width // 2
    center_y = y + height // 2
    physical_monitors = monitors[1:] if len(monitors) > 1 else monitors

    for monitor in physical_monitors:
        left = int(monitor.get("left", 0))
        top = int(monitor.get("top", 0))
        right = left + int(monitor.get("width", 0))
        bottom = top + int(monitor.get("height", 0))
        if left <= center_x < right and top <= center_y < bottom:
            return monitor

    return physical_monitors[0] if physical_monitors else monitors[0]


def _clamp(value: int, minimum: int, maximum: int) -> int:
    if maximum < minimum:
        return minimum
    return max(minimum, min(value, maximum))


def _tk_offset(value: int) -> str:
    """Return a signed Tk geometry offset: +100, -100, +0."""
    return f"{value:+d}"


def ubicar_junto_a_padre(ventana, padre, margen: int = 12) -> None:
    """
    Place a child window next to its parent on the parent's current monitor.

    It prefers the right side, falls back to the left side, and finally clamps
    the window inside the monitor if there is not enough horizontal space.
    """
    try:
        parent_top = padre.winfo_toplevel()
        parent_x, parent_y, parent_w, parent_h = _parse_geometry(parent_top)
        ventana.update_idletasks()

        # A newly-created Tk window can briefly report 1x1. Use requested size
        # as a lower bound to avoid shrinking modal windows.
        win_w = max(int(ventana.winfo_width()), int(ventana.winfo_reqwidth()))
        win_h = max(int(ventana.winfo_height()), int(ventana.winfo_reqheight()))

        monitor = _monitor_for_rect(parent_x, parent_y, parent_w, parent_h)
        if monitor:
            mon_left = int(monitor.get("left", 0))
            mon_top = int(monitor.get("top", 0))
            mon_right = mon_left + int(
                monitor.get("width", ventana.winfo_screenwidth())
            )
            mon_bottom = mon_top + int(
                monitor.get("height", ventana.winfo_screenheight())
            )
        else:
            mon_left, mon_top = 0, 0
            mon_right = ventana.winfo_screenwidth()
            mon_bottom = ventana.winfo_screenheight()

        right_x = parent_x + parent_w + margen
        left_x = parent_x - win_w - margen

        if right_x + win_w <= mon_right:
            x = right_x
        elif left_x >= mon_left:
            x = left_x
        else:
            x = _clamp(right_x, mon_left + margen, mon_right - win_w - margen)

        ideal_y = parent_y + max(0, (parent_h - win_h) // 2)
        y = _clamp(ideal_y, mon_top + margen, mon_bottom - win_h - margen)

        ventana.geometry(f"{win_w}x{win_h}{_tk_offset(x)}{_tk_offset(y)}")
    except Exception:
        # Never prevent a child window from opening if monitor detection fails.
        pass

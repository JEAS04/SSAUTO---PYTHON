"""
core/monitors.py — Detección y consulta de monitores conectados.

Extraído de config/configuracion.py donde no pertenecía (son utilidades
de sistema, no constantes de configuración).
"""

from typing import List

# ── Cache de monitores (evita abrir mss.MSS() repetidamente) ──────────
_monitores_cache: list | None = None


def obtener_monitores() -> list:
    """
    Devuelve la lista de monitores detectados por mss.

    El índice 0 es el monitor virtual (todos los monitores combinados).
    Los índices 1, 2, ... son monitores físicos individuales.
    Cada monitor es un dict con: left, top, width, height.

    El resultado se cachea en memoria para evitar abrir mss.MSS()
    repetidamente durante la misma sesión.
    """
    global _monitores_cache
    if _monitores_cache is not None:
        return list(_monitores_cache)
    try:
        import mss

        with mss.MSS() as sct:
            _monitores_cache = sct.monitors
            return list(_monitores_cache)
    except Exception as e:
        print(f"[✗] Error detectando monitores: {e}")
        return []


def _invalidar_cache_monitores() -> None:
    """Fuerza la próxima llamada a obtener_monitores() a consultar mss."""
    global _monitores_cache
    _monitores_cache = None


def obtener_nombres_monitores() -> List[str]:
    """
    Devuelve una lista de nombres legibles para mostrar en la UI.

    Formato: "Monitor 1 (principal)", "Monitor 2", "Todos los monitores".
    """
    monitores = obtener_monitores()
    nombres = []
    for i, mon in enumerate(monitores):
        if i == 0:
            nombres.append("Todos los monitores")
        elif mon.get("is_primary"):
            nombre_extra = mon.get("name", "").strip()
            if nombre_extra:
                nombres.append(f"Monitor {i} — {nombre_extra} (principal)")
            else:
                nombres.append(f"Monitor {i} (principal)")
        else:
            nombre_extra = mon.get("name", "").strip()
            if nombre_extra:
                nombres.append(f"Monitor {i} — {nombre_extra}")
            else:
                nombres.append(f"Monitor {i}")
    return nombres


def obtener_monitor_por_indice(indice: int) -> dict:
    """
    Devuelve el dict del monitor en la posición 'indice' de la lista.

    indice : int - índice del monitor (0 = virtual, 1 = primer físico, ...)
    Returns dict | None
    """
    monitores = obtener_monitores()
    indice = int(indice)
    if 0 <= indice < len(monitores):
        return monitores[indice]
    return None

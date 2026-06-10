"""
core/medidor_runner.py — Ejecuta el medidor de región de pantalla como subproceso.

Extrae la lógica duplicada de ui/ventana_principal.py donde tanto
_lanzar_medidor() como _medir_region_app() lanzaban el mismo subproceso
con ~90% de código repetido.
"""

import ast
import subprocess
import sys

from .medidor_code import MEDIDOR_CODE


def ejecutar_medidor(monitor_idx: int = 1, timeout: float = 60.0) -> dict | None:
    """
    Ejecuta el medidor de región como subproceso bloqueante.

    Lanza el script MEDIDOR_CODE en un intérprete Python aparte con la
    pantalla completa del monitor indicado. El medidor dibuja un overlay
    para que el usuario seleccione una región y al terminar imprime
    "REGION = {top, left, width, height}" en stdout.

    Parameters
    ----------
    monitor_idx : monitor físico (1 = primero, 2 = segundo, ...). 0 es el virtual.
    timeout     : segundos máximos de espera. Tras el timeout, se mata el subproceso.

    Returns
    -------
    dict con claves top, left, width, height, o None si se canceló/falló.
    """
    if getattr(sys, "frozen", False):
        cmd = [sys.executable, "--medidor", str(monitor_idx)]
    else:
        cmd = [sys.executable, "-c", MEDIDOR_CODE, "--monitor", str(monitor_idx)]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    try:
        stdout, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return None

    for linea in stdout.splitlines():
        if linea.startswith("REGION ="):
            try:
                return ast.literal_eval(linea.split("=", 1)[1].strip())
            except Exception:
                return None
    return None

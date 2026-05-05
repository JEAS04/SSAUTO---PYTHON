import mss
from datetime import datetime
from pathlib import Path


def capturar_region(region: dict, carpeta="screenshots") -> str:
    Path(carpeta).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"{carpeta}/captura_{timestamp}.png"

    with mss.mss() as sct:
        sct.shot(mon=region, output=ruta)

    print(f"[✓] Captura guardada: {ruta}")
    return ruta

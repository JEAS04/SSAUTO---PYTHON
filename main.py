from captura import capturar_region
from uploader import subir_a_sitio
from config import REGION, URL

def main():
    # 1. Capturar
    ruta = capturar_region(REGION)

    # 2. Subir a cada sitio
    for sitio in URL:
        print(f"\n→ Procesando: {sitio['url']}")
        subir_a_sitio(sitio, ruta)

if __name__ == "__main__":
    main()
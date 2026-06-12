import subprocess
import os


def firmar_resultado_setup():
    # Asegura el directorio del proyecto
    ruta_proyecto = r"C:\Users\PERMICOL1\ssauto"
    os.chdir(ruta_proyecto)

    # El comando exacto de PowerShell que te funcionó para los 194 MB
    comando_firma = (
        '& "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.26100.0\\x64\\signtool.exe" '
        'sign /f "C:\\certificado.pfx" /p "123456" /fd SHA256 /td SHA256 '
        "/tr http://digicert.com /NPH .\\setup\\SSAuto_Setup.exe"
    )

    print("Firmando el instalador generado...")
    resultado = subprocess.run(["powershell", "-Command", comando_firma], shell=True)

    if resultado.returncode == 0:
        print("\n¡Instalador firmado con éxito!")
    else:
        print("\nError al firmar el instalador.")


if __name__ == "__main__":
    firmar_resultado_setup()

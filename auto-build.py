import subprocess
import sys
import os


def ejecutar_compilacion_y_firma():
    # Asegura que el script corra en la ruta de tu proyecto
    ruta_proyecto = r"C:\Users\PERMICOL1\ssauto"
    os.chdir(ruta_proyecto)

    # 1. Comando de PyInstaller
    comando_pyinstaller = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "SSAuto.spec",
    ]

    print("Iniciando PyInstaller...")
    resultado_build = subprocess.run(comando_pyinstaller, shell=True)

    if resultado_build.returncode != 0:
        print("Error: PyInstaller falló. Se cancela la firma.")
        return

    print("PyInstaller finalizó con éxito.\n")

    # 2. Comando de Firma en PowerShell (Ruta validada y correcta)
    comando_firma = (
        '& "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.26100.0\\x64\\signtool.exe" '
        'sign /f "C:\\certificado.pfx" /p "123456" /fd SHA256 /td SHA256 '
        "/tr http://timestamp.digicert.com .\\dist\\SSAuto\\SSAuto.exe"
    )

    print("Iniciando firma digital en PowerShell...")
    resultado_firma = subprocess.run(
        ["powershell", "-Command", comando_firma], shell=True
    )

    if resultado_firma.returncode == 0:
        print("\nProceso completado con éxito: ¡Archivo firmado!")
    else:
        print("\nError al intentar firmar el archivo.")


if __name__ == "__main__":
    ejecutar_compilacion_y_firma()

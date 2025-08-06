#!/usr/bin/env python3
"""
Instalador offline/online de dependencias Python para el agente IA.
- Si hay carpeta ./wheels y no hay Internet, instala desde ahí.
- Si hay Internet, instala normalmente.
- Chequea versión de Python y pip.
"""
import os
import sys
import subprocess
import shutil

def check_python():
    if sys.version_info < (3, 8):
        print("[ERROR] Python >= 3.8 requerido.")
        sys.exit(1)

def check_pip():
    try:
        import pip
    except ImportError:
        print("[ERROR] pip no está instalado. Instálalo manualmente.")
        sys.exit(1)

def has_internet():
    import socket
    try:
        socket.create_connection(("pypi.org", 443), timeout=2)
        return True
    except Exception:
        return False

def install_online():
    print("[INFO] Instalando dependencias desde PyPI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_offline():
    print("[INFO] Instalando dependencias desde ./wheels (offline)...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "--no-index", "--find-links=./wheels", "-r", "requirements.txt"
    ])

def main():
    check_python()
    check_pip()
    wheels_dir = os.path.join(os.path.dirname(__file__), "wheels")
    if os.path.isdir(wheels_dir):
        if has_internet():
            modo = input("¿Instalar online (o) u offline (f)? [o/f]: ").strip().lower()
            if modo == "f":
                install_offline()
            else:
                install_online()
        else:
            install_offline()
    else:
        print("[INFO] No se encontró carpeta ./wheels, usando instalación online.")
        install_online()
    print("[OK] Dependencias instaladas.")

if __name__ == "__main__":
    main()

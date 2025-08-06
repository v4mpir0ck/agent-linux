#!/usr/bin/env python3
"""
Instalador universal para el agente IA (offline/online)
- Instala dependencias desde wheels/ si está offline
- Si hay Internet, instala/actualiza desde PyPI
- Compatible con Windows, Linux y WSL
"""
import os
import sys
import subprocess
import shutil

def is_connected():
    import socket
    try:
        # Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except Exception:
        return False

def pip_install(args):
    cmd = [sys.executable, "-m", "pip"] + args
    print(f"\033[94m[INSTALADOR] Ejecutando: {' '.join(cmd)}\033[0m")
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        print(f"\033[91m[ERROR] {e}\033[0m")
        sys.exit(1)

def main():
    wheels_dir = os.path.join(os.path.dirname(__file__), "wheels")
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    print("\033[96mInstalador del agente IA\033[0m")
    print("Buscando Python y pip...")
    if not shutil.which("pip"):
        print("\033[91m[ERROR] pip no está instalado.\033[0m")
        sys.exit(1)
    if not os.path.exists(req_file):
        print(f"\033[91m[ERROR] No se encontró requirements.txt en {req_file}\033[0m")
        sys.exit(1)
    online = is_connected()
    if online:
        print("\033[92m[OK] Conexión a Internet detectada. Instalando desde PyPI...\033[0m")
        pip_install(["install", "-r", req_file, "--upgrade"])
    else:
        print("\033[93m[AVISO] No hay Internet. Instalando desde wheels/...\033[0m")
        if not os.path.isdir(wheels_dir):
            print(f"\033[91m[ERROR] No se encontró la carpeta wheels/ en {wheels_dir}\033[0m")
            sys.exit(1)
        pip_install(["install", "--no-index", "--find-links", wheels_dir, "-r", req_file])
    print("\033[92m[OK] Dependencias instaladas correctamente.\033[0m")
    print("\033[96mPuedes ejecutar el agente con: python agent.py\033[0m")

if __name__ == "__main__":
    main()

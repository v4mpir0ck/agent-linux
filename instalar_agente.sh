#!/bin/bash
# Instalador universal para el agente IA (offline/online)
# Ejecuta el instalador Python con la versión adecuada

set -e

done
# Detectar Python 3.x
PYTHON_BIN=""
for bin in python3 python; do
    if command -v $bin >/dev/null 2>&1; then
        ver=$($bin -c 'import sys; print(sys.version_info[0])')
        if [ "$ver" = "3" ]; then
            PYTHON_BIN=$bin
            break
        fi
    fi



# Si no hay Python 3, intentar instalarlo automáticamente según la distribución
if [ -z "$PYTHON_BIN" ]; then
    echo "[INFO] Python 3 no encontrado. Intentando instalarlo..."
    if command -v apt-get >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema Debian/Ubuntu. Instalando con apt-get..."
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
        PYTHON_BIN=python3
    elif command -v dnf >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema Fedora/CentOS/RHEL (dnf). Instalando con dnf..."
        sudo dnf install -y python3 python3-pip
        PYTHON_BIN=python3
    elif command -v yum >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema CentOS/RHEL (yum). Instalando con yum..."
        sudo yum install -y python3 python3-pip
        PYTHON_BIN=python3
    else
        echo "[ERROR] No se pudo instalar Python automáticamente. Instálalo manualmente."
        exit 1
    fi
fi

# Ejecutar el instalador Python
$PYTHON_BIN "$(dirname "$0")/instalar_agente.py"

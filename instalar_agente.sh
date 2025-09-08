#!/bin/bash
# Instalador automático del agente IA
# Descarga el binario portable y lo instala en el PATH del sistema


set -e

# Detectar familia del SO
OS_FAMILY=""
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        ubuntu|debian)
            OS_FAMILY="ubuntu"
            ;;
        rhel|centos|fedora|rocky|almalinux|ubi8)
            OS_FAMILY="ubi8"
            ;;
        *)
            OS_FAMILY="$ID"
            ;;
    esac
else
    echo "[ERROR] No se pudo detectar la familia del SO."
    exit 1
fi




# Seleccionar URL de binario según la familia del SO
if [ "$OS_FAMILY" = "ubi8" ]; then
    RELEASE_URL="https://github.com/v4mpir0ck/agent-linux/releases/download/v1.0.18-Dockerfile.ubi8/agent"
elif [ "$OS_FAMILY" = "ubuntu" ]; then
    RELEASE_URL="https://github.com/v4mpir0ck/agent-linux/releases/download/v1.0.13-Dockerfile.ubuntu/agent"
else
    echo "[ERROR] Solo se soportan instalaciones automáticas para Ubuntu y UBI8. Por favor descarga el binario manualmente para tu sistema."
    exit 1
fi

INSTALL_PATH="/usr/local/bin/agent"
if [ ! -w "/usr/local/bin" ]; then
    echo "[ERROR] No tienes permisos de escritura en /usr/local/bin. Ejecuta este script como root o con sudo."
    exit 1
fi

curl -L "$RELEASE_URL" -o "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"
echo "[OK] Agente instalado en $INSTALL_PATH"


# Copiar binarios de herramientas según la familia del SO
TOOLS_DIR="$(dirname "$0")/bin/$OS_FAMILY"
BINARIOS_COPIADOS=0
if [ -d "$TOOLS_DIR" ]; then
    for tool in nmap netstat lsof ss tcpdump; do
        SRC="$TOOLS_DIR/$tool"
        DEST="/usr/local/bin/$tool"
        if [ -f "$SRC" ]; then
            cp "$SRC" "$DEST"
            chmod +x "$DEST"
            echo "[OK] Binario $tool copiado a $DEST"
            BINARIOS_COPIADOS=$((BINARIOS_COPIADOS+1))
        else
            echo "[WARN] Binario $tool no encontrado en $TOOLS_DIR"
        fi
    done
    if [ $BINARIOS_COPIADOS -eq 0 ]; then
        echo "[WARN] No se copió ningún binario auxiliar. El agente usará los del sistema si existen."
    fi
else
    echo "[WARN] No se encontró carpeta de binarios para $OS_FAMILY, se usarán los del sistema si existen."
fi

echo "\n[INFO] Instalación finalizada. Puedes ejecutar el agente con: agent"


# Verificar instalación
if "$INSTALL_PATH" --help >/dev/null 2>&1; then
    echo "[OK] El agente se ha instalado correctamente en $INSTALL_PATH"
else
    echo "[ERROR] No se pudo instalar el agente."
    echo "[DEBUG] Salida de ejecución:"
    "$INSTALL_PATH" --help || true
    exit 1
fi

# Mensaje de uso
cat <<EOF

Para lanzar el agente ejecuta:
  agent

EOF

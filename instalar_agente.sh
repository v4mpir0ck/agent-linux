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

# Obtener la última release desde GitHub API
REPO="v4mpir0ck/agent-linux"
API_URL="https://api.github.com/repos/$REPO/releases/latest"
RELEASE_URL=$(curl -s $API_URL | grep "browser_download_url" | grep "$OS_FAMILY" | cut -d '"' -f 4)

if [ -z "$RELEASE_URL" ]; then
    echo "[ERROR] No se encontró binario para la familia $OS_FAMILY en la última release."
    exit 1
fi

INSTALL_PATH="/usr/local/bin/agent"
curl -L "$RELEASE_URL" -o "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"

# Copiar configuración encriptada si existe en el mismo directorio que el script
CONFIG_SRC="$(dirname "$0")/azure_openai_token.enc"
CONFIG_DEST="/usr/local/bin/azure_openai_token.enc"
if [ -f "$CONFIG_SRC" ]; then
    cp "$CONFIG_SRC" "$CONFIG_DEST"
    echo "[OK] Configuración encriptada copiada a $CONFIG_DEST"
fi

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

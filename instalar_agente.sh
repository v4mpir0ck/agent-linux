#!/bin/bash
# Instalador automático del agente IA
# Descarga el binario portable y lo instala en el PATH del sistema

set -e

REPO_URL="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/dist/agent"
INSTALL_PATH="/usr/local/bin/agent"

# Descargar el binario
curl -L "$REPO_URL" -o "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"

# Verificar instalación
if "$INSTALL_PATH" --help >/dev/null 2>&1; then
    echo "[OK] El agente se ha instalado correctamente en $INSTALL_PATH"
else
    echo "[ERROR] No se pudo instalar el agente."
    exit 1
fi

# Mensaje de uso
cat <<EOF

Para lanzar el agente ejecuta:
  agent

EOF

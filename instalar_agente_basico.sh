#!/bin/bash
# Instalador básico para el agente
# Copia el binario generado y lo renombra a 'agente'

set -e

# Descarga el binario desde el repo público de GitHub
BIN_URL="https://github.com/v4mpir0ck/agent-linux/raw/main/mapfre/agente/dist/agente"
BIN_TMP="/tmp/agente.bin"
BIN_DEST="/usr/local/bin/agente"

echo "Descargando el binario desde $BIN_URL..."
curl -L "$BIN_URL" -o "$BIN_TMP"
if [ "$(id -u)" -eq 0 ]; then
	mv "$BIN_TMP" "$BIN_DEST"
	chmod +x "$BIN_DEST"
else
	sudo mv "$BIN_TMP" "$BIN_DEST"
	sudo chmod +x "$BIN_DEST"
fi

echo "Agente instalado en $BIN_DEST"

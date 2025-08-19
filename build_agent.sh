#!/bin/bash
# Script para compilar y empaquetar el agente portable con Nuitka
# Uso: ./build_agent.sh

set -e

SCRIPT_DIR="$(cd -- "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."
DIST_DIR="$SCRIPT_DIR/dist"
MAIN_FILE="$SCRIPT_DIR/__main__.py"
BIN_NAME="agent"

# Limpieza de binarios y restos anteriores
rm -rf "$DIST_DIR"/* "$PROJECT_ROOT/build" "$PROJECT_ROOT/__pycache__" "$PROJECT_ROOT/.nuitka-cache" "$PROJECT_ROOT/dist"/*

# Compilación con Nuitka
/tmp/agente-venv/bin/python3 -m nuitka --onefile --standalone --output-dir="$DIST_DIR" --output-filename="$BIN_NAME" "$MAIN_FILE"

# Renombrar el binario para quitar extensión .bin si existe
if [ -f "$DIST_DIR/$BIN_NAME.bin" ]; then
    mv "$DIST_DIR/$BIN_NAME.bin" "$DIST_DIR/$BIN_NAME"
fi

chmod +x "$DIST_DIR/$BIN_NAME"
echo "\n[OK] Binario generado en $DIST_DIR/$BIN_NAME"

#!/bin/bash
# Instalador universal para el agente IA (offline/online)
# Ejecuta el instalador Python con la versión adecuada


set -e

# Obtener el directorio donde está este script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PYTHON_BIN=""
for bin in python3 python; do
    if command -v $bin >/dev/null 2>&1; then
        ver=$($bin -c 'import sys; print(sys.version_info[0])')
        if [ "$ver" = "3" ]; then
            PYTHON_BIN=$bin
            break
        fi
    fi
done


# Si no hay Python 3, intentar instalarlo automáticamente según la distribución
if [ -z "$PYTHON_BIN" ]; then
    echo "[INFO] Python 3 no encontrado. Intentando instalarlo..."
    if command -v apt-get >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema Debian/Ubuntu. Instalando con apt-get..."
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
        PYTHON_BIN=python3
    elif command -v dnf >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema Fedora/CentOS/RHEL (dnf). Instalando con dnf..."
        sudo dnf install -y python3 python3-pip gcc python3-devel rust cargo
        python3 -m pip install --upgrade pip setuptools wheel setuptools-rust
        # Crear enlace simbólico python -> python3 si no existe
        if ! command -v python >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
            ln -sf $(command -v python3) /usr/local/bin/python
            echo "[INFO] Enlace simbólico creado: python -> python3"
        fi
        PYTHON_BIN=python3
    elif command -v yum >/dev/null 2>&1; then
        echo "[INFO] Detectado sistema CentOS/RHEL (yum). Instalando con yum..."
        sudo yum install -y python3 python3-pip
        # Crear enlace simbólico python -> python3 si no existe
        if ! command -v python >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
            ln -sf $(command -v python3) /usr/local/bin/python
            echo "[INFO] Enlace simbólico creado: python -> python3"
        fi
        PYTHON_BIN=python3
    else
        echo "[ERROR] No se pudo instalar Python automáticamente. Instálalo manualmente."
        echo "[SUGERENCIA] Puedes ejecutar el agente manualmente con: python3 instalar_agente.py"
        exit 1
    fi

fi

PIP_BIN=""
# Comprobar si pip está instalado, si no, instalarlo
if ! $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
    echo "[INFO] pip no está instalado. Intentando instalarlo..."
    if command -v apt-get >/dev/null 2>&1; then
        echo "[INFO] Instalando pip con apt-get..."
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command -v dnf >/dev/null 2>&1; then
        echo "[INFO] Instalando pip con dnf..."
        sudo dnf install -y python3-pip || true
        # Si aún no está, intentar con ensurepip
        if ! $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
            echo "[INFO] Intentando instalar pip con ensurepip..."
            $PYTHON_BIN -m ensurepip --upgrade || true
        fi
    elif command -v yum >/dev/null 2>&1; then
        echo "[INFO] Instalando pip con yum..."
        sudo yum install -y python3-pip || true
        # Si aún no está, intentar con ensurepip
        if ! $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
            echo "[INFO] Intentando instalar pip con ensurepip..."
            $PYTHON_BIN -m ensurepip --upgrade || true
        fi
    fi
    # Si aún no está, usar get-pip.py
    if ! $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
        echo "[INFO] Instalando pip con get-pip.py..."
        curl -sSLo "$SCRIPT_DIR/get-pip.py" https://bootstrap.pypa.io/get-pip.py
        $PYTHON_BIN "$SCRIPT_DIR/get-pip.py"
        rm -f "$SCRIPT_DIR/get-pip.py"
    fi

    # Si sigue sin estar, error
    if ! $PYTHON_BIN -m pip --version >/dev/null 2>&1; then
        echo "[ERROR] No se pudo instalar pip automáticamente. Instálalo manualmente."
        exit 1
    fi
fi

# Crear enlace simbólico para pip si no existe
if ! command -v pip >/dev/null 2>&1; then
    # Buscar pip3
    if command -v pip3 >/dev/null 2>&1; then
        ln -sf $(command -v pip3) /usr/local/bin/pip
        echo "[INFO] Enlace simbólico creado: pip -> pip3"
    else
        # Buscar el binario de pip instalado por python3 -m pip
        PIP_BIN=$($PYTHON_BIN -m pip -V 2>/dev/null | awk '{print $4}')
        if [ -n "$PIP_BIN" ] && [ -f "$PIP_BIN" ]; then
            ln -sf "$PIP_BIN" /usr/local/bin/pip
            echo "[INFO] Enlace simbólico creado: pip -> $PIP_BIN"
        fi
    fi
fi


# URLs para descargas
REPO_RAW_AGENTE="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/"
REPO_RAW_ROOT="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/"

NEEDED_FILES=(
  "instalar_agente.py"
  "install_requirements.py"
  "requirements.txt"
  "agent.py"
  "llm_client.py"
  "encrypt_token.py"
)

for f in "${NEEDED_FILES[@]}"; do
  if [ ! -f "$SCRIPT_DIR/$f" ]; then
    echo "[INFO] Descargando $f desde el repo..."
    curl -o "$SCRIPT_DIR/$f" "$REPO_RAW_AGENTE$f"
  fi
done






# Comprobar wheels/ y descargar automáticamente la carpeta de Google Drive si no existe
if [ ! -d "$SCRIPT_DIR/wheels" ]; then
  echo "[INFO] No se encontró la carpeta wheels. Intentando descargar la carpeta completa desde Google Drive..."
  # Instalar gdown si no está
  if ! command -v gdown >/dev/null 2>&1; then
    echo "[INFO] Instalando gdown para descargar desde Google Drive..."
    $PYTHON_BIN -m pip install --no-cache-dir gdown || sudo $PYTHON_BIN -m pip install --no-cache-dir gdown
  fi
  # Descargar la carpeta wheels desde Google Drive (ID de la carpeta)
  GDRIVE_FOLDER_ID="1u1ME2pREDk8i20nW2h7xq0282Ansf1JT"
  gdown --folder --id "$GDRIVE_FOLDER_ID" -O "$SCRIPT_DIR"
  # Si wheels.zip existe, descomprimirlo
  if [ -f "$SCRIPT_DIR/wheels.zip" ]; then
    echo "[INFO] wheels.zip detectado. Descomprimiendo..."
    unzip -o "$SCRIPT_DIR/wheels.zip" -d "$SCRIPT_DIR"
    rm -f "$SCRIPT_DIR/wheels.zip"
    # Si no existe la carpeta wheels pero hay archivos .whl, muévelos a wheels/
    if [ ! -d "$SCRIPT_DIR/wheels" ]; then
      mkdir -p "$SCRIPT_DIR/wheels"
      find "$SCRIPT_DIR" -maxdepth 1 -type f -name '*.whl' -exec mv {} "$SCRIPT_DIR/wheels/" \;
      echo "[INFO] Archivos .whl movidos a wheels/"
    fi
  fi
  # Verificar que wheels/ existe tras la descarga/descompresión
  if [ ! -d "$SCRIPT_DIR/wheels" ]; then
    echo "[ERROR] La carpeta wheels no se creó correctamente tras descargar la carpeta de Google Drive."
    echo "Descárgala manualmente desde: https://drive.google.com/drive/folders/1u1ME2pREDk8i20nW2h7xq0282Ansf1JT?usp=sharing"
    exit 1
  fi
fi


# Ejecutar el instalador Python
# --- Instalar herramientas de red si no existen ---
BIN_DIR="$SCRIPT_DIR/bin"
mkdir -p "$BIN_DIR"

# URLs de binarios en tu repo (ajusta si cambian los nombres)
REPO_BIN_BASE="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/bin/"

declare -A BINARIES=(
  [nmap]="nmap"
  [busybox]="busybox"
)

# Función para instalar binario si no existe
install_bin() {
  local bin_name="$1"
  local bin_path="$BIN_DIR/$bin_name"
  if command -v "$bin_name" >/dev/null 2>&1; then
    echo "[INFO] $bin_name ya está instalado en el sistema."
  elif [ -x "$bin_path" ]; then
    echo "[INFO] $bin_name ya existe en $bin_path."
  else
    echo "[INFO] Descargando $bin_name desde el repo..."
    curl -L -o "$bin_path" "$REPO_BIN_BASE${BINARIES[$bin_name]}"
    chmod +x "$bin_path"
  fi
}

# Instalar nmap y busybox
for bin in "nmap" "busybox"; do
  install_bin "$bin"
done

# Crear enlaces simbólicos para nc y traceroute si no existen
for link in nc traceroute; do
  if [ ! -e "$BIN_DIR/$link" ]; then
    ln -sf busybox "$BIN_DIR/$link"
    echo "[INFO] Enlace simbólico creado: $link -> busybox"
  fi
done

# Añadir bin a PATH si no está
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) export PATH="$BIN_DIR:$PATH" ;;
esac

# Ejecutar el instalador Python
$PYTHON_BIN "$SCRIPT_DIR/instalar_agente.py"

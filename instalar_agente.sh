# Crear entorno virtual si no existe y usarlo para todo
if [ ! -d "$HOME/agente-venv" ]; then
  echo "[INFO] Creando entorno virtual en $HOME/agente-venv..."
  python3 -m venv "$HOME/agente-venv"
fi
PYTHON_BIN="$HOME/agente-venv/bin/python3"
if [ -z "$PYTHON_BIN" ]; then
  echo "[ERROR] No se detectó el binario de Python. Revisa la variable PYTHON_BIN y la lógica de detección."
  exit 1
fi
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel pyinstaller
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel pyinstaller
# Crear entorno virtual si no existe y usarlo para todo
if [ ! -d "$HOME/agente-venv" ]; then
  echo "[INFO] Creando entorno virtual en $HOME/agente-venv..."
  python3 -m venv "$HOME/agente-venv"
fi
PYTHON_BIN="$HOME/agente-venv/bin/python3"
export PYTHONPATH="$HOME/.local/lib/python3.10/site-packages:$PYTHONPATH"
if [ -z "$PYTHON_BIN" ]; then
  echo "[WARN] No se detectó el binario de Python. Intentando instalar python3 automáticamente..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
    PYTHON_BIN="$(which python3)"
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-pip
    PYTHON_BIN="$(which python3)"
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y python3 python3-pip
    PYTHON_BIN="$(which python3)"
  fi
  if [ -z "$PYTHON_BIN" ]; then
    echo "[ERROR] No se pudo instalar ni detectar el binario de Python. Revisa la variable PYTHON_BIN y la lógica de detección."
    exit 1
  fi
fi
# Instala pyinstaller en el entorno correcto y verifica instalación
# Instala pyinstaller y verifica instalación correctamente
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel pyinstaller
if ! $PYTHON_BIN -m pip show pyinstaller >/dev/null 2>&1; then
  echo "[ERROR] PyInstaller no se instaló correctamente en $PYTHON_BIN. Revisa la instalación o instala manualmente con: $PYTHON_BIN -m pip install pyinstaller"
  exit 1
fi
# Si se usa entorno virtual, instala dependencias si no están
if [[ "$PYTHON_BIN" == "$HOME/agente-venv/bin/python"* ]]; then
  echo "[INFO] Instalando dependencias en el entorno virtual si no están presentes..."
  $PYTHON_BIN -m pip install --upgrade pip setuptools wheel
  $PYTHON_BIN -m pip show pyinstaller >/dev/null 2>&1 || $PYTHON_BIN -m pip install pyinstaller
fi
PYTHON_BIN=""
if [ -d "$HOME/agente-venv/bin" ]; then
  if [ -x "$HOME/agente-venv/bin/python3" ]; then
    PYTHON_BIN="$HOME/agente-venv/bin/python3"
  elif [ -x "$HOME/agente-venv/bin/python" ]; then
    PYTHON_BIN="$HOME/agente-venv/bin/python"
  fi
fi
if [ -z "$PYTHON_BIN" ]; then
  if [ -x "$HOME/.local/bin/python3" ]; then
    PYTHON_BIN="$HOME/.local/bin/python3"
  else
    PYTHON_BIN="$(which python3)"
  fi
fi
if [ -z "$PYTHON_BIN" ]; then
  echo "[ERROR] No se detectó el binario de Python. Revisa la variable PYTHON_BIN y la lógica de detección."
  exit 1
fi
export PATH="$HOME/.local/bin:$PATH"
if [ -x "$HOME/.local/bin/python3" ]; then
  PYTHON_BIN="$HOME/.local/bin/python3"
else
  PYTHON_BIN="$(which python3)"
fi
# Abort if running with sudo to avoid losing user environment
if [ "$(id -u)" -eq 0 ]; then
  echo "[ERROR] No ejecutes este script con sudo. Ejecuta como usuario normal para que se usen los paquetes de usuario."
  exit 1
fi
#!/bin/bash
# Instalador universal para el agente IA (offline/online)
# Ejecuta el instalador Python con la versión adecuada


set -e


# Directorio base fijo para toda la instalación
BASE_DIR="/tmp/agente"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

PYTHON_BIN="$HOME/agente-venv/bin/python3"
if [ ! -x "$PYTHON_BIN" ]; then
  echo "[ERROR] El binario de Python del entorno virtual no existe. Revisa la creación del entorno virtual."
  exit 1
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
            echo "[INFO] Enlace simbólico creado: python -> python3"
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


# Descargar siempre todos los archivos necesarios en BASE_DIR
NEEDED_FILES=(
  "instalar_agente.py"
  "install_requirements.py"
  "requirements.txt"
  "agent.py"
  "llm_client.py"
  "encrypt_token.py"
)


for f in "${NEEDED_FILES[@]}"; do
  echo "[INFO] Descargando $f desde el repo..."
  curl -sSLo "$BASE_DIR/$f" "$REPO_RAW_AGENTE$f"
done
# --- Parchear requirements.txt para dependencias problemáticas ---
if [ -f "$BASE_DIR/requirements.txt" ]; then
  sed -i 's/^murmurhash==1.0.2$/murmurhash==1.0.9/' "$BASE_DIR/requirements.txt"
  sed -i -E 's/^(pyyaml|PyYAML)[^=]*([=<>!]+)[^ ]*/pyyaml==6.0/i' "$BASE_DIR/requirements.txt"
fi

### --- INICIO wheels (comentado por si se necesita en el futuro) ---




BIN_DIR="$BASE_DIR/bin"
mkdir -p "$BIN_DIR"

# URLs de binarios en tu repo (ajusta si cambian los nombres)
REPO_BIN_BASE="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/bin/"

declare -A BINARIES=(
  [nmap]="nmap"
  [busybox]="busybox"
  [netstat]="netstat"
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

for bin in "nmap" "busybox" "netstat"; do
  install_bin "$bin"
done

for link in nc traceroute; do
  if [ ! -e "$BIN_DIR/$link" ]; then
    ln -sf busybox "$BIN_DIR/$link"
    echo "[INFO] Enlace simbólico creado: $link -> busybox"
  fi
done

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) export PATH="$BIN_DIR:$PATH" ;;
esac

# Ejecutar el instalador Python

# --- Actualizar pip, setuptools y wheel antes de instalar dependencias ---

# --- Instalar dependencias de compilación en Linux ---
if command -v apt-get >/dev/null 2>&1; then
  echo "[INFO] Instalando build-essential y python3-dev para compilación de paquetes nativos..."
  sudo apt-get update
  sudo apt-get install -y build-essential python3-dev
fi

echo "[INFO] Actualizando pip, setuptools y wheel..."
$PYTHON_BIN -m pip install --upgrade pip setuptools wheel

if [ -d "$WHEELS_DIR" ]; then
  whl_count=$(find "$WHEELS_DIR" -type f -name '*.whl' | wc -l)
  if [ "$whl_count" -gt 0 ]; then
    echo "[INFO] Instalando dependencias desde wheels locales..."
    $PYTHON_BIN -m pip install --no-index --find-links="$WHEELS_DIR" -r "$BASE_DIR/requirements.txt" --upgrade || true
  fi
fi

# --- Ejecutar el instalador Python principal ---

# --- Generar ejecutable con PyInstaller incluyendo binarios y wheels ---
echo "[INFO] Generando ejecutable del agente con PyInstaller..."
echo "[DEBUG] Usando PYTHON_BIN: $PYTHON_BIN"
# Activar el entorno virtual antes de instalar PyInstaller
source "$HOME/agente-venv/bin/activate"
pip install --upgrade pyinstaller
if ! pyinstaller --version >/dev/null 2>&1; then
  echo "[ERROR] PyInstaller no está disponible en el entorno virtual. Reinstalando..."
  pip install pyinstaller
  if ! pyinstaller --version >/dev/null 2>&1; then
    echo "[ERROR] PyInstaller sigue sin estar disponible en el entorno virtual. Revisa la instalación manualmente."
    deactivate
    exit 1
  fi
fi
cd "$BASE_DIR"
PYINSTALL_BINARIES=""
for f in bin/*; do
  [ -f "$f" ] && PYINSTALL_BINARIES="$PYINSTALL_BINARIES --add-binary $f:bin"
done
pyinstaller --onefile $PYINSTALL_BINARIES $PYINSTALL_DATA agent.py
echo "[INFO] Ejecutable generado en $BASE_DIR/dist/agent"

# --- Ejecutar el instalador Python principal ---
$PYTHON_BIN "$BASE_DIR/instalar_agente.py"

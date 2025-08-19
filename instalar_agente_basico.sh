#!/bin/bash
# Instalador básico para el agente
# Copia el binario generado y lo renombra a 'agente'

set -e

# Detectar si es root y definir SUDO antes de cualquier uso
if [ "$(id -u)" -eq 0 ]; then
	SUDO=""
else
	SUDO="sudo"
fi
# Detectar si es root y definir SUDO
if [ "$(id -u)" -eq 0 ]; then
	SUDO=""
else
	SUDO="sudo"
fi

# Requisitos mínimos
REQUIRED_PYTHON="3.10"
REQUIRED_GLIBC="2.35"

# Actualizar Python si es necesario
PYTHON_VERSION=$(python3 --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
if [ "$PYTHON_VERSION" != "$REQUIRED_PYTHON" ]; then
	echo "[INFO] Instalando Python $REQUIRED_PYTHON..."
		if command -v apt-get >/dev/null 2>&1; then
			$SUDO apt-get update
			$SUDO apt-get install -y software-properties-common
			$SUDO add-apt-repository -y ppa:deadsnakes/ppa
			$SUDO apt-get update
			$SUDO apt-get install -y python3.10 python3.10-venv python3.10-distutils python3-pip
		elif command -v yum >/dev/null 2>&1; then
			$SUDO yum install -y python3
			echo "[WARN] Instala Python 3.10 manualmente si no está disponible en el sistema."
		elif command -v dnf >/dev/null 2>&1; then
			$SUDO dnf install -y python3
			echo "[WARN] Instala Python 3.10 manualmente si no está disponible en el sistema."
		else
			echo "[ERROR] No se detectó gestor de paquetes compatible para instalar Python."
			exit 1
		fi
fi

# Actualizar GLIBC si es necesario
GLIBC_VERSION=$(ldd --version | head -n1 | awk '{print $NF}')
if [ "$(printf '%s\n' "$REQUIRED_GLIBC" "$GLIBC_VERSION" | sort -V | head -n1)" != "$REQUIRED_GLIBC" ]; then
	echo "[INFO] Actualizando GLIBC a $REQUIRED_GLIBC..."
		if command -v apt-get >/dev/null 2>&1; then
			$SUDO apt-get update
			$SUDO apt-get install -y libc6
		elif command -v yum >/dev/null 2>&1; then
			$SUDO yum update -y glibc
		elif command -v dnf >/dev/null 2>&1; then
			$SUDO dnf upgrade -y glibc
		else
			echo "[ERROR] No se detectó gestor de paquetes compatible para actualizar GLIBC."
			exit 1
		fi
	echo "[WARN] Si la versión de GLIBC sigue siendo antigua, considera actualizar el sistema operativo o usar una imagen base más moderna."
fi

BIN_URL="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/dist/agente"
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

# Probar el binario y compilar localmente si falla por GLIBC/Python
echo "[INFO] Probando binario instalado..."
$BIN_DEST --help >/dev/null 2>&1
if [ $? -ne 0 ]; then
	echo "[WARN] El binario descargado no es compatible con este sistema. Intentando compilar localmente..."
	# Descargar fuentes y requirements
	REPO_URL="https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/agente"
	mkdir -p /tmp/agente_src
	curl -O https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/requirements.txt -o /tmp/agente_src/requirements.txt
	for file in __main__.py agent.py alertas.py configuracion.py conectividad.py herramientas.py informe.py llm_client.py main.py procesos.py sistema.py usuarios.py wizard.py; do
		curl -o /tmp/agente_src/$file "$REPO_URL/$file"
	done
	# Instalar dependencias de build
	if command -v apt-get >/dev/null 2>&1; then
		$SUDO apt-get update
		$SUDO apt-get install -y python3-pip python3-venv build-essential libffi-dev libssl-dev
	elif command -v yum >/dev/null 2>&1; then
		$SUDO yum install -y python3-pip python3-venv gcc libffi-devel openssl-devel
	elif command -v dnf >/dev/null 2>&1; then
		$SUDO dnf install -y python3-pip python3-venv gcc libffi-devel openssl-devel
	fi
	python3 -m venv /tmp/agente-venv
	source /tmp/agente-venv/bin/activate
	pip install --upgrade pip setuptools wheel
	pip install -r /tmp/agente_src/requirements.txt
	pip install pyinstaller
	pyinstaller --onefile /tmp/agente_src/__main__.py --name agente
	if [ -f dist/agente ]; then
		mv dist/agente $BIN_DEST
		chmod +x $BIN_DEST
		echo "[OK] Binario agente compilado localmente y reemplazado en $BIN_DEST"
	else
		echo "[ERROR] Falló la compilación local. Revisa dependencias y fuentes."
		exit 1
	fi
fi

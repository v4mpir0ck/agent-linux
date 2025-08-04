# Dockerfile para probar la instalación offline/online del agente IA
FROM python:3.10-slim

WORKDIR /agente

# Copia solo lo necesario para la instalación y prueba
COPY requirements.txt ./
COPY wheels/ ./wheels/
COPY instalar_agente.py ./
COPY instalar_agente.sh ./
COPY install_requirements.py ./
COPY agent.py ./
COPY llm_client.py ./
COPY encrypt_token.py ./

# Permisos para el instalador shell
RUN chmod +x instalar_agente.sh

# Por defecto, solo muestra ayuda de instalación
CMD ["/bin/bash"]

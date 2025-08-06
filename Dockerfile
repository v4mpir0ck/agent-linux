# Dockerfile para probar la instalación offline/online del agente IA
FROM python:3.10-slim

WORKDIR /agente

# Solo descarga y ejecuta el instalador bash desde el repo público
RUN apt-get update && apt-get install -y git curl
WORKDIR /agente
RUN curl -O https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/instalar_agente.sh && chmod +x instalar_agente.sh

# Por defecto, entra en bash para que el usuario pueda lanzar el instalador
CMD ["/bin/bash"]

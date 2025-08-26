# Instalación automática del agente IA

Este script instala el binario portable del agente IA en tu sistema Linux.

## ¿Cómo funciona?
- Detecta automáticamente la familia de tu sistema operativo (Ubuntu/Debian, UBI8/RHEL/CentOS, etc.).
- Descarga el binario más reciente desde la última release de GitHub, según tu SO.
- Instala el binario en `/usr/local/bin/agent`.
- Copia la configuración encriptada si existe (`azure_openai_token.enc`).

## Uso
```bash
sudo ./instalar_agente.sh
```

## Requisitos
- curl
- Acceso a internet
- Permisos de sudo/root

## Notas
- El binario se publica automáticamente en GitHub Releases por la pipeline CI/CD.

---
[Volver al README principal](README.md)

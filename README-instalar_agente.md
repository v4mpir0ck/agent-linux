# Instalación automática del agente IA

Este script instala el binario portable del agente IA en tu sistema Linux.

## ¿Cómo funciona?

## Uso
```bash
sudo ./instalar_agente.sh
```

## Requisitos

## Notas
El instalador detecta la familia de tu sistema operativo (por ejemplo, Ubuntu, UBI8, etc.) y copia automáticamente los binarios de las herramientas de red necesarias (`nmap`, `netstat`, `lsof`, `ss`, `tcpdump`) desde la carpeta `bin/<distro>/` incluida en el paquete.

Si no se encuentran binarios para tu distribución, el agente intentará usar los del sistema. Si tampoco están disponibles, deberás instalarlos manualmente usando el gestor de paquetes correspondiente.

Esto garantiza que el agente funcione de forma portable y sin dependencias externas en la mayoría de entornos Linux.

---

---
[Volver al README principal](README.md)

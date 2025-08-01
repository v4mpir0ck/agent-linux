# 🧠 Agente IA para Linux

## Descripción

Este agente es una herramienta inteligente que interpreta instrucciones en lenguaje natural y ejecuta comandos en sistemas Linux. Utiliza un modelo LLM para sugerir el comando más adecuado, lo ejecuta de forma segura y muestra el resultado en formato profesional:

- **Sugerencia y encabezado**: Se muestran en tablas ASCII con colores y títulos centrados.
- **Resultado del comando**: Se muestra en crudo, respetando el formato original del output.
- **Opciones rápidas**: Siempre visibles al final para facilitar la interacción.
- **Confirmación**: Solicita confirmación para comandos delicados que puedan modificar el sistema.
- **Memoria de contexto**: Guarda resultados relevantes para mejorar futuras respuestas.

## Ejemplo de flujo

```mermaid
graph TD
    A[Usuario escribe instrucción] --> B[Agente consulta LLM]
    B --> C[Sugerencia y comando en tabla]
    C --> D[Ejecuta comando]
    D --> E[Resultado en crudo]
    E --> F[Opciones rápidas]
    D -->|Comando peligroso| G[Solicita confirmación]
    G -->|Usuario confirma| D
```

## Ejemplo visual

```
+---------------------------------------------------------------+
|                   SUGERENCIA DEL LLM                         |
+---------------------------------------------------------------+
| Mostrar servidores DNS del sistema                            |
|  Comando sugerido:                                            |
| cat /etc/resolv.conf                                          |
+---------------------------------------------------------------+
+---------------------------------------------------------------+
|                 RESULTADO DEL COMANDO                         |
+---------------------------------------------------------------+
# Output crudo aquí
+---------------------------------------------------------------+
[Opciones rápidas] sistema | cpu | memoria | disco | red | procesos | usuarios | servicio <nombre> | dns | salir
```

## Instalación y uso

1. Clona el repositorio en tu máquina Linux:
   ```bash
   git clone <URL-del-repo>
   cd agente
   pip install -r requirements.txt
   ```
2. Ejecuta el agente:
   ```bash
   python agent.py
   ```
3. Escribe instrucciones naturales, por ejemplo:
   - "Ver la memoria RAM"
   - "Estado de la red"
   - "Mostrar usuarios conectados"

## Seguridad
- El agente detecta comandos peligrosos y solicita confirmación antes de ejecutarlos.
- El output se muestra siempre en formato profesional y legible.

## Diagrama de arquitectura

```mermaid
flowchart LR
    User[Usuario] -->|Instrucción| Agent[Agente IA]
    Agent -->|Prompt| LLM[Modelo LLM]
    LLM -->|Sugerencia y comando| Agent
    Agent -->|Ejecuta| Linux[Shell Linux]
    Linux -->|Output| Agent
    Agent -->|Visualiza| User
```

## Autor
- DXC / MAPFRE

## Licencia
MIT

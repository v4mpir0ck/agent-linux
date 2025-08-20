# Binario portable y uso remoto

## Generación del binario
- Compila con `build_agent.sh` usando Nuitka y libpython estática.
- El binario se genera en `agente/dist/agent`.
- Limpieza automática de temporales.

## Instalación remota
- Usa `instalar_agente.sh` para descargar el binario y la configuración encriptada.
- El binario queda listo en `/usr/local/bin/agent`.

## Configuración encriptada
- El archivo `azure_openai_token.enc` se copia junto al binario si existe.
- Permite tener el modelo configurado en cualquier destino.

## Compatibilidad
- Compila el binario en la misma distro donde lo vas a usar (UBI8, Ubuntu, etc.).
- Usa los Dockerfiles del repo para builds reproducibles.

## Ejemplo de uso
```bash
agent
```

[Volver al README principal](README.md)

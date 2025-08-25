# Binario portable y uso remoto

> Este componente forma parte de la línea **Agente IA para Linux** y se integra con la línea **Pipelines CI/CD** del proyecto.

## Generación del binario
- El binario se genera automáticamente desde la pipeline CI/CD de GitHub Actions.
- La pipeline compila el binario usando `build_agent.sh`, Nuitka y libpython estática.
- El binario se publica en GitHub Releases y se almacena en `agente/dist/agent`.
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

---

[Volver al README principal](README.md)

# Binario portable y uso remoto

> Este componente forma parte de la línea **Agente IA para Linux** y se integra con la línea **Pipelines CI/CD** del proyecto.

## Generación del binario
- El binario se genera automáticamente desde la pipeline CI/CD de GitHub Actions.
- La pipeline compila el binario usando `build_agent.sh`, Nuitka y libpython estática.
- El binario se publica en GitHub Releases.
- Limpieza automática de temporales.

## Instalación remota



## Herramientas de red portables

El binario portable se acompaña de las herramientas de red (`nmap`, `netstat`, `lsof`, `ss`, `tcpdump`) compiladas para cada distribución soportada. El instalador detecta tu sistema y copia automáticamente estos binarios junto al agente. Si no se encuentran, se usarán los del sistema.

## Compatibilidad
- Compila el binario en la misma distro donde lo vas a usar (UBI8, Ubuntu, etc.).
- Usa los Dockerfiles del repo para builds reproducibles.

## Ejemplo de uso
```bash
agent
```

---

[Volver al README principal](README.md)

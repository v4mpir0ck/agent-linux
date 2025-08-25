- [Historial de releases y binarios generados](README-releases.md)
# 🧠 Agente IA para Linux

Este README cubre la visión general y el uso rápido del agente. Para detalles sobre binarios, pipelines y estructura, consulta los enlaces:

- [Binario portable y uso remoto](README-binario.md)
- [Pipeline CI/CD y releases](README-pipeline.md)
- [Estructura del repositorio](README-estructura.md)


## Instalación rápida (binario portable)

**Descarga el binario desde [GitHub Releases](https://github.com/v4mpir0ck/agent-linux/releases/latest) según tu distribución:**

### Fedora / RHEL / UBI
```bash
curl -L -o agent "https://github.com/v4mpir0ck/agent-linux/releases/latest/download/agent-Dockerfile.ubi8"
chmod +x agent
./agent
```

### Ubuntu
```bash
curl -L -o agent "https://github.com/v4mpir0ck/agent-linux/releases/latest/download/agent-Dockerfile.ubuntu"
chmod +x agent
./agent
```

Esto descarga el binario específico y lo ejecuta directamente. Consulta [README-releases.md](README-releases.md) para ver todos los binarios disponibles.

## Descripción

Agente inteligente para ejecutar comandos en Linux usando LLM, con CLI interactivo, seguridad y portabilidad.

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

## Instalación y uso clásico (Python)

1. Clona el repositorio
```bash
git clone <URL-del-repo>
cd agente
```
2. Instalación de dependencias (offline/online)
```bash
./instalar_agente.sh
```
3. Configura el token seguro de Azure OpenAI (solo si usas LLM Azure)
```bash
python encrypt_token.py
```
4. Ejecuta el agente
```bash
python agent.py
```

## Autor y licencia
- Javier Lazaro
- MIT

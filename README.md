- [Historial de releases y binarios generados](README-releases.md)
# 🧠 Agente IA para Linux

Este README cubre la visión general y el uso rápido del agente. Para detalles sobre binarios, pipelines y estructura, consulta los enlaces:

- [Binario portable y uso remoto](README-binario.md)
- [Pipeline CI/CD y releases](README-pipeline.md)
- [Estructura del repositorio](README-estructura.md)

## Instalación rápida (binario portable)

> **Para instalar el agente en cualquier sistema solo necesitas ejecutar:**
> ```bash
> curl -O https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/instalar_agente.sh && chmod +x instalar_agente.sh && ./instalar_agente.sh
> ```
> Esto descarga e instala el binario y la configuración encriptada si existe.

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

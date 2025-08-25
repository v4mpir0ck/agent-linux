# Estructura del repositorio

```
agente/
  __main__.py
  build_agent.sh
  instalar_agente.sh
  dist/
    agent
    azure_openai_token.enc
  dockerfiles/
    Dockerfile.ubi8-test
    Dockerfile.ubuntu
  ...otros scripts y módulos Python...
```

## Carpetas y archivos clave
- `agente/`: Código fuente y scripts.
- `dockerfiles/`: Dockerfiles para builds reproducibles.
- `build_agent.sh`: Script para compilar el binario.
- `instalar_agente.sh`: Instalador remoto.


[Volver al README principal](README.md)

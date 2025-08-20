# Pipeline CI/CD y releases

## Workflow de GitHub Actions
- Permite compilar el binario en diferentes Dockerfiles (UBI8, Ubuntu, CentOS).
- Elige el Dockerfile y el tag del release al lanzar manualmente.
- Publica el binario como artefacto y en GitHub Releases.

## Ejemplo de lanzamiento
- Ve a GitHub Actions → `Build Agent Binario y Publicar Release` → `Run workflow`.
- Elige el Dockerfile y el tag.

## Tags y releases
- Usa tags descriptivos: `v1.0.0-ubi8`, `v1.0.0-ubuntu`, etc.
- Cada release tiene su binario para la distro correspondiente.

## Añadir nuevos Dockerfiles
- Añade el Dockerfile en `dockerfiles/`.
- Actualiza la matriz en el workflow.

[Volver al README principal](README.md)

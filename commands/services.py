import subprocess

def estado_servicio(servicio):
    try:
        result = subprocess.run(["systemctl", "is-active", servicio], capture_output=True, universal_newlines=True)
        return f"{servicio}: {result.stdout.strip()}"
    except Exception:
        return f"No se pudo obtener el estado de {servicio}"

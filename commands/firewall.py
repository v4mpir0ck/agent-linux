import subprocess

def estado_firewall(return_data=False):
    try:
        result = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
        output = result.stdout
        if return_data:
            activo = 'active' in output.lower()
            reglas = []
            for line in output.splitlines():
                if line.strip() and (line.startswith('To') or line.startswith('---')):
                    continue
                if line.strip() and not line.lower().startswith('status:') and not line.lower().startswith('logging'):
                    reglas.append(line.strip())
            return {'activo': activo, 'reglas': reglas}
        else:
            return output
    except Exception:
        return "No se pudo obtener el estado del firewall (1ufw instalado?)"

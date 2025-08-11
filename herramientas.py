import subprocess

def ejecutar_herramienta(nombre):
    herramientas = {
        'nmap': 'nmap -sS localhost',
        'netstat': 'netstat -tulnp',
        'lsof': 'lsof -i',
        'ss': 'ss -tuln',
        'tcpdump': 'tcpdump -c 10'
    }
    if nombre not in herramientas:
        return f"Herramienta no soportada: {nombre}"
    comando = herramientas[nombre]
    confirm = input(f"¿Deseas ejecutar '{comando}'? (sí/no): ")
    if confirm.strip().lower() not in ["si", "sí", "s", "yes", "y"]:
        return f"[NO EJECUTADO] {comando}"
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=20)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

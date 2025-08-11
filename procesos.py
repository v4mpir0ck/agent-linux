import subprocess

def info_procesos():
    comando = 'ps aux --sort=-%mem | head -10'
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

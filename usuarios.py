import subprocess

def info_usuarios():
    comando = 'who'
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=5)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

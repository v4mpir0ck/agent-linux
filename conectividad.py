import subprocess

def test_ping(host='8.8.8.8'):
    comando = f'ping -c 4 {host}'
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

def test_traceroute(host='8.8.8.8'):
    comando = f'traceroute {host}'
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=20)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

def test_velocidad():
    comando = 'curl -s https://speedtest.tele2.net/10MB.zip -o /dev/null && echo "Descarga completada"'
    try:
        output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=60)
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"

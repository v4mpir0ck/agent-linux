def ejecutar_herramientas():
    herramientas = {
        'nmap': 'Escaneo de puertos locales (nmap -sS localhost)',
        'netstat': 'Ver conexiones y puertos abiertos (netstat -tulnp)',
        'lsof': 'Listar procesos usando red (lsof -i)',
        'ss': 'Ver sockets y puertos (ss -tuln)',
        'tcpdump': 'Captura de paquetes de red (tcpdump -c 10)'
    }
    ejemplos = {
        'nmap': 'Detectar puertos abiertos y servicios en localhost.',
        'netstat': 'Ver qué procesos están escuchando en la red.',
        'lsof': 'Saber qué procesos usan la red en este momento.',
        'ss': 'Ver sockets activos y puertos en uso.',
        'tcpdump': 'Capturar tráfico de red para análisis rápido.'
    }
    print("\033[96mHerramientas disponibles:\033[0m")
    for idx, (herr, desc) in enumerate(herramientas.items(), 1):
        print(f"  {idx}. {herr} - {desc}")
    print("\nEjemplos de uso:")
    for herr, ej in ejemplos.items():
        print(f"  {herr}: {ej}")
    print("\nSelecciona una herramienta por nombre (o escribe 'salir' para cancelar):")
    nombre = input("> ").strip().lower()
    if nombre == 'salir':
        return "Operación cancelada."
    # Permitir seleccionar por número
    if nombre.isdigit():
        idx = int(nombre) - 1
        if 0 <= idx < len(herramientas):
            nombre = list(herramientas.keys())[idx]
        else:
            return f"Herramienta no soportada: {nombre}"
    if nombre not in herramientas:
        return f"Herramienta no soportada: {nombre}"
    import os
    import getpass
    user_home_bin = f"/home/{getpass.getuser()}/agente/bin"
    tmp_bin = "/tmp/agente/bin"
    base_cmd = herramientas[nombre].split('(')[-1].replace(')','').strip()
    tool = nombre
    bin_tool_paths = [
        os.path.join(user_home_bin, tool),
        os.path.join(tmp_bin, tool),
        os.path.join(os.path.dirname(__file__), 'bin', tool)
    ]
    bin_used = None
    for bin_path in bin_tool_paths:
        if os.path.isfile(bin_path):
            bin_used = bin_path
            if os.access(bin_path, os.X_OK):
                cmd_parts = base_cmd.split()
                # Si la ruta tiene espacios, poner comillas
                if ' ' in bin_path:
                    cmd_parts[0] = f'"{bin_path}"'
                else:
                    cmd_parts[0] = bin_path
                comando = ' '.join(cmd_parts)
            else:
                print(f"\033[91m[AVISO] El binario '{bin_path}' no tiene permisos de ejecución.\033[0m")
                print(f"\033[93mPuedes solucionarlo con: chmod +x {bin_path}\033[0m")
                print(f"\033[93mSe usará el comando del sistema en su lugar.\033[0m")
                comando = base_cmd
            break
    else:
        comando = base_cmd
    confirm = input(f"¿Deseas ejecutar '{comando}'? (sí/no): ")
    if confirm.strip().lower() not in ["si", "sí", "s", "yes", "y"]:
        return f"[NO EJECUTADO] {comando}"
    import stat
    # Mostrar permisos del binario si se usa uno local
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=20)
        output = result.stdout
        if result.returncode != 0:
            output += f"\n[ERROR] Código de salida: {result.returncode}\nSTDERR: {result.stderr}"
    except Exception as e:
        output = f"[Error o Simulación] {e}"
    return f"$ {comando}\n{output}"
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

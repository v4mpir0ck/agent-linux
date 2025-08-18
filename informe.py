import os
import subprocess

# Importa el cliente LLM
try:
    from llm_client import query_llm
except ImportError:
    from llm_client import query_llm

def generar_informe():
    """
    Genera un informe de estado del sistema ejecutando comandos sugeridos por IA.
    Pregunta antes de ejecutar comandos peligrosos y guarda el resultado en un fichero txt.
    """
    # Solicita al LLM una lista de comandos útiles para analizar el sistema
    prompt = (
        "Eres un asistente Linux. Sugiere una lista de comandos shell útiles para generar un informe completo del sistema (máximo 10), "
        "incluyendo info de OS, CPU, RAM, disco, red, procesos, usuarios, servicios, logs. "
        "Indica si algún comando puede ser peligroso (por ejemplo, modificar archivos, reiniciar servicios, escanear puertos). "
        "Devuelve solo los comandos, uno por línea, y una breve explicación de cada uno."
    )
    respuesta_llm = query_llm(prompt)
    comandos = []
    explicaciones = []
    for linea in respuesta_llm.splitlines():
        if linea.strip():
            # Separar comando y explicación si están juntos
            if ':' in linea:
                expl, cmd = linea.split(':', 1)
                comandos.append(cmd.strip())
                explicaciones.append(expl.strip())
            else:
                comandos.append(linea.strip())
                explicaciones.append('')
    # Ejecuta los comandos uno a uno, preguntando antes si son peligrosos
    informe = []
    for idx, cmd in enumerate(comandos):
        expl = explicaciones[idx] if idx < len(explicaciones) else ''
        peligroso = any(w in cmd for w in ['rm ', 'reboot', 'shutdown', 'mkfs', 'dd ', 'killall', 'systemctl restart', 'nmap'])
        if peligroso:
            confirm = input(f"El comando '{cmd}' puede ser peligroso. ¿Deseas ejecutarlo? (sí/no): ")
            if confirm.strip().lower() not in ["si", "sí", "s", "yes", "y"]:
                informe.append(f"[NO EJECUTADO] {cmd} - {expl}")
                continue
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
        except Exception as e:
            output = f"[Error o Simulación] {e}"
        informe.append(f"# {expl}\n$ {cmd}\n{output}\n{'-'*60}")
    # Guarda el informe en un fichero
    ruta = os.path.abspath("informe_sistema.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(informe))
    return ruta

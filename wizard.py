def run_wizard():
    """
    Diagnóstico guiado de problemas comunes en Linux, para uso desde el agente.
    Ejecuta el flujo interactivo y devuelve un resumen textual.
    """
    try:
        resultado = ejecutar_wizard()
        return resultado
    except Exception as e:
        return f"[Error en wizard] {e}"
import subprocess
try:
    from .llm_client import query_llm
except ImportError:
    from llm_client import query_llm

def ejecutar_wizard():
    pasos = [
        "Obtener contexto relevante del sistema (estado general, recursos, servicios, red, disco, logs recientes)",
        "Identificar posibles problemas a partir del contexto obtenido",
        "Sugerir acciones correctivas solo si se detectan problemas claros"
    ]
    acciones_ejecutadas = []
    cuadro_ancho = 90
    print("\n\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
    print("\033[96m|{:^88}|\033[0m".format('AUTO-REPARACIÓN IA: Diagnóstico y acciones'))
    print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
    for idx, paso in enumerate(pasos):
        if idx == 0:
            prompt = (
                "Eres un asistente de troubleshooting Linux. "
                "Sugiere de forma concisa una secuencia de comandos shell (máximo 5) para obtener toda la información relevante del sistema (estado general, recursos, servicios, red, disco, logs recientes). "
                "No propongas acciones correctivas aún. Devuelve solo los comandos, uno por línea, y una breve explicación de cada uno."
            )
            respuesta_llm = query_llm(prompt)
            print("\033[96m|{:^88}|\033[0m".format("Comandos de diagnóstico sugeridos:"))
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            for linea in respuesta_llm.splitlines():
                print(f"\033[96m| {linea[:86].ljust(86)} |\033[0m")
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            confirm = input("¿Deseas ejecutar estos comandos de diagnóstico? (sí/no): ")
            if confirm.strip().lower() in ["si", "sí", "s", "yes", "y"]:
                for linea in respuesta_llm.splitlines():
                    if linea.strip() and not linea.strip().startswith("#") and (" " in linea or linea.strip().startswith("/")):
                        try:
                            output = subprocess.check_output(linea, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
                        except Exception as e:
                            output = f"[Error o Simulación] {e}"
                        print("\033[92m+{}+\033[0m".format('-'*cuadro_ancho))
                        print(f"\033[92m| Comando: {linea[:70].ljust(70)} |\033[0m")
                        print("\033[92m|{:^88}|\033[0m".format('RESULTADO'))
                        for l in output.splitlines() or [output]:
                            print(f"\033[92m| {l[:86].ljust(86)} |\033[0m")
                        print("\033[92m+{}+\033[0m\n".format('-'*cuadro_ancho))
                acciones_ejecutadas.append("Diagnóstico ejecutado")
        elif idx == 1:
            prompt = (
                "A partir de la información obtenida en el paso anterior, sugiere de forma concisa posibles problemas detectados en el sistema. "
                "No propongas aún acciones correctivas. Devuelve solo el análisis de problemas, uno por línea."
            )
            analisis_llm = query_llm(prompt)
            print("\033[96m|{:^88}|\033[0m".format("Análisis de problemas sugerido por IA:"))
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            for linea in analisis_llm.splitlines():
                print(f"\033[96m| {linea[:86].ljust(86)} |\033[0m")
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            acciones_ejecutadas.append("Análisis de problemas realizado")
        elif idx == 2:
            prompt = (
                "Si se detectaron problemas claros en el paso anterior, sugiere solo los comandos shell necesarios para corregirlos, uno por línea, con breve explicación. "
                "Si no hay problemas, responde: 'No se detectaron problemas que requieran acción.'"
            )
            acciones_llm = query_llm(prompt)
            print("\033[96m|{:^88}|\033[0m".format("Acciones correctivas sugeridas por IA:"))
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            for linea in acciones_llm.splitlines():
                print(f"\033[96m| {linea[:86].ljust(86)} |\033[0m")
            print("\033[96m+{}+\033[0m".format('-'*cuadro_ancho))
            if "No se detectaron problemas" not in acciones_llm:
                confirm = input("¿Deseas ejecutar estas acciones correctivas? (sí/no): ")
                if confirm.strip().lower() in ["si", "sí", "s", "yes", "y"]:
                    for linea in acciones_llm.splitlines():
                        if linea.strip() and not linea.strip().startswith("#") and (" " in linea or linea.strip().startswith("/")):
                            try:
                                output = subprocess.check_output(linea, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
                            except Exception as e:
                                output = f"[Error o Simulación] {e}"
                            print("\033[92m+{}+\033[0m".format('-'*cuadro_ancho))
                            print(f"\033[92m| Comando: {linea[:70].ljust(70)} |\033[0m")
                            print("\033[92m|{:^88}|\033[0m".format('RESULTADO'))
                            for l in output.splitlines() or [output]:
                                print(f"\033[92m| {l[:86].ljust(86)} |\033[0m")
                            print("\033[92m+{}+\033[0m\n".format('-'*cuadro_ancho))
                    acciones_ejecutadas.append("Acciones correctivas ejecutadas")
    if acciones_ejecutadas:
        resumen = '\n'.join(f"✔️ {a}" for a in acciones_ejecutadas)
        return f"[Auto-reparación] Pasos realizados:\n{resumen}\nProceso completado."
    else:
        return "[Auto-reparación] No se ha realizado ninguna acción."

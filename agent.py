



def print_help():
    import shutil
    def center_text(text, width):
        return text.center(width)
    def wrap_text(text, width):
        import textwrap
        return textwrap.wrap(text, width)
    box_width = min(90, shutil.get_terminal_size((80, 20)).columns - 2)
    opciones = [
        "🖥️  sistema: Info del sistema operativo",
        "🧮  cpu: Info de la CPU",
        "💾  memoria: Info de la memoria RAM",
        "📀  disco: Info de discos y particiones",
        "🌐  red: Info de interfaces de red",
        "📡  conectividad: Chequeo de conexión a Internet",
        "🛡️  firewall: Estado del firewall",
        "📊  procesos: Procesos más consumidores",
        "👥  usuarios: Usuarios conectados",
        "🔧  servicio <nombre>: Estado de un servicio (ej: servicio sshd)",
        "🗂️  dns: Muestra servidores DNS del sistema",
        "----------------------------------------------------------",
        "Para salir: salir, exit, quit.",
        "Para ver este menú: ayuda, opciones, qué puedes hacer, etc.",
        # Opciones avanzadas anteriores:
        # "🔒 confirmación: Ejecuta comandos peligrosos tras confirmación ('confirmar')",
        # "📝 contexto: El agente recuerda instrucciones previas en la sesión",
        # "🤖 integración LLM: Puedes pedir cualquier instrucción en lenguaje natural",
        # "💡 ejemplo: 'crea un archivo de texto', 'muestra los usuarios conectados', 'reinicia el servicio sshd'"
    ]
    avanzadas = [
        "🧭  wizard: Diagnóstico y auto-reparación guiada de problemas comunes",
        "📄  informe: Generar resumen de estado del sistema",
        "🚨  alertas: Sugerir acciones ante problemas detectados",
        "⚙️  configuración: Mostrar y comparar archivos clave",
        "🛠️  herramientas: Ejecutar nmap, netstat, lsof, ss, tcpdump",
        "🔗  conectividad externa: Test de acceso a endpoints y APIs",
        "🌐  ping: Diagnóstico de red (ping, traceroute, test de velocidad)",
    ]
    # Tabla opciones básicas
    banner = "\033[96m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[96m|{}|\033[0m\n".format(center_text('🧠  Agente IA para Linux  🧠', box_width))
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    for opcion in opciones:
        for linea in wrap_text(opcion, box_width-2):
            banner += f"| \033[96m{linea.ljust(box_width-2)}\033[0m |\n"
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    # Tabla opciones avanzadas
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[95m|{}|\033[0m\n".format(center_text('Opciones avanzadas', box_width))
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    for opcion in avanzadas:
        for linea in wrap_text(opcion, box_width-2):
            banner += f"| \033[95m{linea.ljust(box_width-2)}\033[0m |\n"
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    return banner
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class Agent:
    def handle_instruction(self, instruccion):
        # Soporte para confirmación de comandos delicados
        if hasattr(self, 'pendiente_confirmacion') and self.pendiente_confirmacion and instruccion.strip().lower() == 'confirmar':
            import subprocess
            comando = self.pendiente_confirmacion['comando']
            sugerencia = self.pendiente_confirmacion['sugerencia']
            resultado_top = "\033[92m🟩━━━━━━━━━━ RESULTADO DEL COMANDO ━━━━━━━━🟩\033[0m"
            resultado_bottom = "\033[92m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
            try:
                resultado = subprocess.check_output(comando, shell=True, universal_newlines=True)
                resumen = f"Resultado de '{comando}':\n{resultado.strip()}"
                self.memoria_contexto.append(resumen)
                self.pendiente_confirmacion = None
                return f"{sugerencia}\n\n\n\n{resultado_top}\n\033[92m{resultado.strip()}\033[0m\n{resultado_bottom}"
            except Exception as e:
                self.pendiente_confirmacion = None
                return f"{sugerencia}\n\n\n\n\033[91m🟥━━ ERROR AL EJECUTAR COMANDO ━━🟥\033[0m\n\033[91m{e}\033[0m\n\033[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"


        instr = instruccion.lower().strip()
        tokens = instr.split()

        # --- WIZARD (Diagnóstico y auto-reparación guiada) ---
        if "wizard" in instr or "auto-reparación" in instr or "autoreparación" in instr:
            import subprocess
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
                try:
                    from .llm_client import query_llm
                except ImportError:
                    from llm_client import query_llm
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
                        # Ejecutar cada comando sugerido (solo líneas que parecen comandos)
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

        # ...resto de la función original...
        try:
            from .llm_client import query_llm
        except ImportError:
            from llm_client import query_llm
        import re
        import subprocess
        # Prompt extendido para el LLM (sin markdown)
        system_prompt = (
            "Eres un agente Python que puede ejecutar comandos en el sistema Linux del usuario. "
            "Si el usuario pide una acción, responde con el comando bash necesario en texto plano, sin usar markdown ni bloques de código. "
            "Primero da una breve explicación, luego el comando en una línea aparte. "
            "Ejemplo de formato: \nExplicación breve\ncomando"
        )
        # Inicializa memoria_contexto si no existe
        if not hasattr(self, 'memoria_contexto'):
            self.memoria_contexto = []
        contexto = "\n".join([f"- {item}" for item in self.memoria_contexto])
        if contexto:
            prompt = f"[CONTEXT]\n{contexto}\n\n[INSTRUCCIÓN]\n{instruccion}"
        else:
            prompt = instruccion
        full_prompt = f"{system_prompt}\n\nUsuario: {prompt}"

        respuesta = query_llm(full_prompt)
        # Procesar respuesta: buscar explicación y comando (sin markdown)
        lineas = respuesta.strip().splitlines()
        explicacion = ""
        comando = ""
        # Buscar la primera línea que parece comando (contiene espacio y no es explicación)
        for idx, linea in enumerate(lineas):
            if idx == 0:
                explicacion = linea.strip()
            elif linea.strip() and not linea.strip().startswith('#') and (" " in linea or linea.strip().startswith("/")):
                comando = linea.strip()
                break
        # Si no se detecta comando, intentar buscar en el resto
        if not comando:
            for linea in lineas[1:]:
                if linea.strip() and not linea.strip().startswith('#') and (" " in linea or linea.strip().startswith("/")):
                    comando = linea.strip()
                    break
        # Mostrar explicación en caja
        box_width = 60
        def box(text, color=96):
            from textwrap import wrap
            lines = wrap(text, box_width-2)
            out = f"\033[{color}m+{'-'*box_width}+\033[0m\n"
            for l in lines:
                out += f"\033[{color}m| {l.ljust(box_width-2)} |\033[0m\n"
            out += f"\033[{color}m+{'-'*box_width}+\033[0m"
            return out
        output = ""
        resumen = ""
        if comando:
            import subprocess
            try:
                output = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=15)
                resumen = f"Comando ejecutado: {comando}\nResultado:\n{output.strip()}"
            except Exception as e:
                output = f"[Error o Simulación] {e}"
                resumen = f"Comando ejecutado: {comando}\nError:\n{e}"
            if not hasattr(self, 'memoria_contexto'):
                self.memoria_contexto = []
            self.memoria_contexto.append(resumen)
            return (
                box(explicacion, 96) + "\n" +
                box(f"Comando sugerido: {comando}", 95) + "\n" +
                box("Resultado ejecución:", 92) + "\n" +
                f"\033[92m{output.strip()}\033[0m\n" +
                f"\033[92m+{'-'*box_width}+\033[0m"
            )
        else:
            return box(respuesta, 96)

    def _extraer_valor(self, tokens, claves):
        # Busca el valor después de una clave
        for i, t in enumerate(tokens):
            if t in claves and i+1 < len(tokens):
                return tokens[i+1]
        return None




# --- BLOQUE DE EJECUCIÓN INTERACTIVO ---
if __name__ == "__main__":
    print("\n\033[96mAgente IA para Linux (modo interactivo)\033[0m")
    print("Escribe 'salir' para terminar.\n")
    # Mostrar info de LLM
    try:
        try:
            from .llm_client import LLM_ENDPOINT, LLM_MODEL
        except ImportError:
            from llm_client import LLM_ENDPOINT, LLM_MODEL
        llm_endpoint = LLM_ENDPOINT
        llm_model = LLM_MODEL
        llm_status = "\033[92mOK\033[0m" if llm_endpoint and llm_model else "\033[91mNO CONFIGURADO\033[0m"
        print(f"\033[94m[LLM] Endpoint: {llm_endpoint if llm_endpoint else 'NO CONFIGURADO'}\033[0m")
        print(f"\033[94m[LLM] Modelo: {llm_model if llm_model else 'NO CONFIGURADO'}\033[0m")
        print(f"\033[94m[LLM] Estado: {llm_status}\033[0m\n")
    except Exception as e:
        print(f"\033[91m[LLM] No se pudo obtener la configuración del modelo: {e}\033[0m\n")
    print(print_help())
    agent = Agent()
    while True:
        try:
            print("\033[93m┌{}┐\033[0m".format('─'*40))
            print("\033[93m│{:^40s}│\033[0m".format('Introduce tu instrucción'))
            print("\033[93m└{}┘\033[0m".format('─'*40))
            instr = input("\033[93mINSTRUCCIÓN > \033[0m").strip()
            if instr.lower() in ["salir", "exit", "quit"]:
                print("\n\033[92mHasta luego.\033[0m")
                break
            if instr.lower() in ["ayuda", "opciones", "menu", "qué puedes hacer", "help"]:
                print(print_help())
                continue
            resp = agent.handle_instruction(instr)
            print(resp)
        except (KeyboardInterrupt, EOFError):
            print("\n\033[92mHasta luego.\033[0m")
            break

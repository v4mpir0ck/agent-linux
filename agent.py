import os
def guardar_llm_config(endpoint, deployment, api_version, key):
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    with open(env_path, 'w') as f:
        f.write(f'AZURE_OPENAI_ENDPOINT={endpoint}\n')
        f.write(f'AZURE_OPENAI_DEPLOYMENT={deployment}\n')
        f.write(f'AZURE_OPENAI_API_VERSION={api_version}\n')
        f.write(f'AZURE_OPENAI_KEY={key}\n')

def cargar_llm_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    config = {}
    if os.path.isfile(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k] = v
    return config
import conectividad  # Necesario para que Nuitka lo incluya en el binario
import alertas
import configuracion
# import encrypt_token  # Eliminado: ya no se usa lógica de encriptado
import herramientas
import informe
import llm_client
# import main  # Eliminado para evitar conflicto de importación circular
import procesos
import sistema
import update_releases_md
import usuarios
import wizard




def print_help():
    import shutil
    def center_text(text, width):
        return text.center(width)
    def wrap_text(text, width):
        import textwrap
        return textwrap.wrap(text, width)
    box_width = min(90, shutil.get_terminal_size((80, 20)).columns - 2)
    opciones = [
        " 🖥️   sistema: Info del sistema operativo",
        " 🧮  cpu: Info de la CPU",
        " 💾  memoria: Info de la memoria RAM",
        " 📀  disco: Info de discos y particiones",
        " 🌐  red: Info de interfaces de red",
        " 📡  conectividad: Chequeo de conexión a Internet",
        " 🛡️   firewall: Estado del firewall",
        " 📊  procesos: Procesos más consumidores",
        " 👥  usuarios: Usuarios conectados",
        " 🔧  servicio <nombre>: Estado de un servicio (ej: servicio sshd)",
        " 🗂️   dns: Muestra servidores DNS del sistema",
        " ----------------------------------------------------------",
        " Para salir: salir, exit, quit.",
        " Para ver este menú: ayuda, opciones, qué puedes hacer, etc.",
        # Opciones avanzadas anteriores:
        # "🔒 confirmación: Ejecuta comandos peligrosos tras confirmación ('confirmar')",
        # "📝 contexto: El agente recuerda instrucciones previas en la sesión",
        # "🤖 integración LLM: Puedes pedir cualquier instrucción en lenguaje natural",
        # "💡 ejemplo: 'crea un archivo de texto', 'muestra los usuarios conectados', 'reinicia el servicio sshd'"
    ]
    avanzadas = [
        " 🧭  wizard: Diagnóstico y auto-reparación guiada de problemas comunes",
        " 📄  informe: Generar resumen de estado del sistema",
        " 🚨  alertas: Sugerir acciones ante problemas detectados",
        " ⚙️   configuración: Mostrar y comparar archivos clave",
        " 🛠️   herramientas: Ejecutar nmap, netstat, lsof, ss, tcpdump",
        " 🔗  conectividad externa: Test de acceso a endpoints y APIs",
        " 🌐  ping: Diagnóstico de red (ping, traceroute, test de velocidad)",
    ]
    # Tabla opciones básicas
    banner = "\033[96m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[96m|{}|\033[0m\n".format(center_text('Agente IA para Linux', box_width))
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    for opcion in opciones:
        for linea in wrap_text(opcion, box_width-4):
            banner += f"➤ \033[96m{linea.ljust(box_width-4)}\033[0m\n"
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    # Sin barra final
    # Tabla opciones avanzadas
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[95m|{}|\033[0m\n".format(center_text('Opciones avanzadas', box_width))
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    for opcion in avanzadas:
        for linea in wrap_text(opcion, box_width-4):
            banner += f"➤ \033[95m{linea.ljust(box_width-4)}\033[0m\n"
    banner += "\033[95m+{}+\033[0m\n".format('-'*box_width)
    # Sin barra final
    return banner
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class Agent:
    def handle_instruction(self, instruccion):
        comando = None
        instr = instruccion.lower().strip()
        tokens = instr.split()
        # --- INTERCEPTACIÓN DE AYUDA/MENÚ ---
        help_keywords = [
            "ayuda", "help", "opciones", "qué puedes hacer", "menu", "menú", "mostrar ayuda", "mostrar opciones", "ver ayuda", "ver opciones"
        ]
        if any(kw in instr for kw in help_keywords):
            return print_help()
        # --- INTERCEPTACIÓN DE OPCIONES AVANZADAS ---
        interceptores = [
            {
                "nombre": "informe",
                "frases": [
                    "generar informe", "informe del sistema", "informe completo", "resumen del sistema", "informe general", "genera un informe", "quiero un informe", "muestra un informe", "haz un informe", "informe sobre el sistema", "crear informe", "informe detallado", "informe linux", "informe máquina", "informe de estado", "informe de recursos", "informe de salud", "system report", "system summary", "system info report", "generate report", "show report", "create report", "full report", "health report", "status report", "linux report", "machine report"
                ],
                "modulo": "informe",
                "funcion": "generar_informe",
                "mensaje": "\033[95mInforme generado en:\033[0m {resultado}"
            },
            {
                "nombre": "wizard",
                "frases": [
                    "diagnóstico guiado", "auto-reparación", "wizard", "diagnostico asistido", "diagnóstico asistido", "diagnóstico automático", "diagnóstico inteligente", "guided troubleshooting", "auto repair", "run wizard", "start wizard", "diagnostic wizard"
                ],
                "modulo": "wizard",
                "funcion": "run_wizard",
                "mensaje": "\033[95mDiagnóstico guiado ejecutado.\033[0m\n{resultado}"
            },
            {
                "nombre": "alertas",
                "frases": [
                    "alertas", "alertas del sistema", "sugerir acciones", "problemas detectados", "mostrar alertas", "ver alertas", "system alerts", "show alerts", "suggest actions", "problem alerts"
                ],
                "modulo": "alertas",
                "funcion": "mostrar_alertas",
                "mensaje": "\033[95mAlertas del sistema:\033[0m\n{resultado}"
            },
            {
                "nombre": "configuracion",
                "frases": [
                    "configuración", "archivos clave", "mostrar configuración", "comparar configuración", "ver configuración", "system config", "show config", "compare config", "key files"
                ],
                "modulo": "configuracion",
                "funcion": "mostrar_configuracion",
                "mensaje": "\033[95mConfiguración del sistema:\033[0m\n{resultado}"
            },
            {
                "nombre": "herramientas",
                "frases": [
                    "herramientas", "ejecutar nmap", "ejecutar netstat", "ejecutar lsof", "ejecutar ss", "ejecutar tcpdump", "usar herramientas", "ver herramientas", "network tools", "run nmap", "run netstat", "run lsof", "run ss", "run tcpdump", "show tools"
                ],
                "modulo": "herramientas",
                "funcion": "ejecutar_herramientas",
                "mensaje": "\033[95mHerramientas ejecutadas:\033[0m\n{resultado}"
            },
            {
                "nombre": "conectividad",
                "frases": [
                    "conectividad externa", "test de acceso", "test de endpoints", "test de apis", "probar conectividad", "diagnóstico de red", "test de velocidad", "external connectivity", "test endpoints", "test apis", "network diagnosis", "speed test", "run ping", "run traceroute"
                ],
                "modulo": "conectividad",
                "funcion": "test_conectividad",
                "mensaje": "\033[95mTest de conectividad externa:\033[0m\n{resultado}"
            },
            {
                "nombre": "ping",
                "frases": [
                    "ping", "diagnóstico de red", "test de ping", "hacer ping", "probar ping", "network ping", "run ping", "ping test"
                ],
                "modulo": "conectividad",
                "funcion": "test_ping",
                "mensaje": "\033[95mTest de ping:\033[0m\n{resultado}"
            }
        ]
        # --- Configuración LLM interactiva ---
        if instr.startswith("configurar llm") or instr.startswith("set llm"):
            print("Introduce los datos de configuración del LLM:")
            endpoint = input("Endpoint: ").strip()
            deployment = input("Deployment: ").strip()
            api_version = input("API Version: ").strip()
            key = input("API Key: ").strip()
            guardar_llm_config(endpoint, deployment, api_version, key)
            return "Configuración LLM guardada en .env."

        for interceptor in interceptores:
            if any(frase in instr for frase in interceptor["frases"]) or interceptor["nombre"] in instr:
                # --- ALERTAS INTELIGENTES ---
                if interceptor["nombre"] == "alertas":
                    # 1. Pedir al LLM los comandos de diagnóstico recomendados
                    try:
                        from llm_client import query_llm
                    except ImportError:
                        from llm_client import query_llm
                    system_prompt = (
                        "Eres un agente Python experto en Linux. Sugiere una lista de comandos de diagnóstico para detectar problemas en el sistema. "
                        "Responde solo con la lista de comandos, uno por línea, sin explicación ni markdown. Ejemplo: df -h\ntop -b -n1\nntpq -p"
                    )
                    contexto = "\n".join([f"- {item}" for item in getattr(self, 'memoria_contexto', [])])
                    prompt = f"[CONTEXT]\n{contexto}\n\n[INSTRUCCIÓN]\n{instruccion}" if contexto else instruccion
                    full_prompt = f"{system_prompt}\n\nUsuario: {prompt}"
                    respuesta = query_llm(full_prompt)
                    comandos = [linea.strip() for linea in respuesta.strip().splitlines() if linea.strip() and not linea.startswith('#')]
                    # 2. Ejecutar los comandos y recopilar resultados
                    resultados = []
                    import subprocess
                    for cmd in comandos:
                        try:
                            salida = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
                        except Exception as e:
                            salida = f"[Error] {e}"
                        resultados.append({"comando": cmd, "salida": salida})
                    # 3. Pasar resultados al módulo alertas para procesar
                    try:
                        import alertas
                    except ImportError:
                        import alertas
                    if hasattr(alertas, "procesar_resultados"):
                        alertas_generadas = alertas.procesar_resultados(resultados)
                    else:
                        # Fallback: usar mostrar_alertas si existe
                        alertas_generadas = getattr(alertas, "mostrar_alertas", lambda: [])()
                    self.ultimas_alertas = alertas_generadas
                    # 4. Mostrar agrupadas y con colores
                    niveles = {"critico": [], "warning": [], "info": []}
                    for alerta in alertas_generadas:
                        nivel = alerta.get("nivel", "info").lower()
                        if nivel not in niveles:
                            nivel = "info"
                        niveles[nivel].append(alerta)
                    def color_nivel(nivel):
                        return {"critico": 91, "warning": 93, "info": 96}.get(nivel, 96)
                    out = ""
                    for nivel in ["critico", "warning", "info"]:
                        if niveles[nivel]:
                            out += f"\033[{color_nivel(nivel)}m{'='*60}\033[0m\n"
                            out += f"\033[{color_nivel(nivel)}m{nivel.upper():^60}\033[0m\n"
                            out += f"\033[{color_nivel(nivel)}m{'='*60}\033[0m\n"
                            out += f"\033[{color_nivel(nivel)}m{'MENSAJE':<40}{'SUGERENCIA':<20}\033[0m\n"
                            for alerta in niveles[nivel]:
                                out += f"\033[{color_nivel(nivel)}m{alerta.get('mensaje','')[:39]:<40}{alerta.get('sugerencia','')[:19]:<20}\033[0m\n"
                            out += f"\033[{color_nivel(nivel)}m{'-'*60}\033[0m\n"
                    return out
                # --- Otros módulos avanzados ---
                try:
                    modulo = __import__(interceptor["modulo"])
                except ImportError:
                    modulo = __import__(interceptor["modulo"])
                funcion = getattr(modulo, interceptor["funcion"], None)
                if funcion:
                    resultado = funcion()
                    return interceptor["mensaje"].format(resultado=resultado)
        # Si no coincide con ningún interceptor, usar LLM
        # ...existing code...
        # --- Cargar config LLM desde .env si existe ---
        llm_config = cargar_llm_config()
        try:
            from llm_client import query_llm
            if llm_config:
                # Si el módulo lo permite, setear config
                if hasattr(llm_client, 'set_config'):
                    llm_client.set_config(llm_config)
        except ImportError:
            from llm_client import query_llm
        import re
        import subprocess
        system_prompt = (
            "Eres un agente experto en Linux con amplios conocimientos sobre administración de sistemas, redes y seguridad y cloud, devops en azure, aws y k8s"
            "Eres un agente IA entrenado específicamente con el contenido de los repositorios de Mapfre y mawdy. "
            "Prioriza ese conocimiento fine-tuned para responder preguntas, usando el modelo entrenado. "
            "Si el usuario pide una acción, responde con el comando bash necesario en texto plano, sin usar markdown ni bloques de código. "
            "Primero da una breve explicación, luego el comando en una línea aparte. "
            "Ejemplo de formato: \nExplicación breve\ncomando"
        )
        if not hasattr(self, 'memoria_contexto'):
            self.memoria_contexto = []
        contexto = "\n".join([f"- {item}" for item in self.memoria_contexto])
        if contexto:
            prompt = f"[CONTEXT]\n{contexto}\n\n[INSTRUCCIÓN]\n{instruccion}"
        else:
            prompt = instruccion
        full_prompt = f"{system_prompt}\n\nUsuario: {prompt}"
        respuesta = query_llm(full_prompt)
        lineas = respuesta.strip().splitlines()
        explicacion = ""
        comando = None
        for idx, linea in enumerate(lineas):
            if idx == 0:
                explicacion = linea.strip()
            elif linea.strip() and not linea.strip().startswith('#') and (" " in linea or linea.strip().startswith("/")):
                comando = linea.strip()
                break
        if not comando:
            for linea in lineas[1:]:
                if linea.strip() and not linea.strip().startswith('#') and (" " in linea or linea.strip().startswith("/")):
                    comando = linea.strip()
                    break
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
    try:
        import readline
    except ImportError:
        pass
    print("\n\033[96mAgente IA para Linux (modo interactivo)\033[0m")
    print("Escribe 'salir' para terminar.\n")
    # Mostrar info de LLM
    try:
        from llm_client import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
        llm_endpoint = AZURE_OPENAI_ENDPOINT
        llm_model = AZURE_OPENAI_DEPLOYMENT
        llm_status = "\033[92mOK\033[0m" if llm_endpoint and llm_model else "\033[91mNO CONFIGURADO\033[0m"
        print(f"\033[94m[LLM] Endpoint: {llm_endpoint if llm_endpoint else 'NO CONFIGURADO'}\033[0m")
        print(f"\033[94m[LLM] Modelo: {llm_model if llm_model else 'NO CONFIGURADO'}\033[0m")
        print(f"\033[94m[LLM] Estado: {llm_status}\033[0m\n")
    except Exception as e:
        print(f"\033[91m[LLM] No se pudo obtener la configuración del modelo: {e}\033[0m\n")
    print("\033[91m[AVISO] Todas las opciones pasan por el LLM, por lo que el resultado puede variar según el contexto proporcionado.\033[0m\n")
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

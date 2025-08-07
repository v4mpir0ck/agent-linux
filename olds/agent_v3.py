# Versión 3 - Agente IA Linux (Azure OpenAI)
# Backup completo antes de nuevos cambios

# Esta versión incluye:
# - Procesamiento de cualquier instrucción por LLM real (Azure OpenAI)
# - Prompt seguro y explícito para troubleshooting
# - Sin lógica hardcodeada para instrucciones
# - Manejo profesional de outputs y confirmaciones

# Copia íntegra del agente.py actual

def print_help():
    import shutil
    def center_text(text, width):
        return text.center(width)
    def wrap_text(text, width):
        import textwrap
        return textwrap.wrap(text, width)
    box_width = min(90, shutil.get_terminal_size((80, 20)).columns - 2)
    opciones_basicas = [
        "  errores: Buscar errores recientes y sugerir soluciones",
        "📝  logs: Ver y filtrar logs del sistema y servicios",
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
    ]
    opciones_avanzadas = [
        "🧭  wizard: Modo interactivo guiado para troubleshooting",
        "🤖  auto-reparación: Ejecutar comandos seguros para resolver problemas comunes",
        "📄  informe: Generar resumen de estado del sistema",
        "🚨  alertas: Sugerir acciones ante problemas detectados",
        "⚙️  configuración: Mostrar y comparar archivos clave",
        "🛠️  herramientas: Ejecutar nmap, netstat, lsof, ss, tcpdump",
        "🔗  conectividad externa: Test de acceso a endpoints y APIs",
        "🌐  ping: Diagnóstico de red (ping, traceroute, test de velocidad)",
    ]
    banner = "\033[96m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[96m|{}|\033[0m\n".format(center_text('🧠  Agente IA para Linux  🧠', box_width))
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    banner += "| \033[96mOpciones básicas:\033[0m".ljust(box_width) + "|\n"
    for opcion in opciones_basicas:
        opcion = opcion.strip().replace('\n', ' ')
        if len(opcion) > box_width-2:
            opcion = opcion[:box_width-5] + '...'
        banner += f"| \033[96m{opcion.ljust(box_width-2)}\033[0m |\n"
    banner += "|" + ("-" * (box_width)) + "|\n"
    banner += "| \033[96mOpciones avanzadas:\033[0m".ljust(box_width) + "|\n"
    for opcion in opciones_avanzadas:
        opcion = opcion.strip().replace('\n', ' ')
        if len(opcion) > box_width-2:
            opcion = opcion[:box_width-5] + '...'
        banner += f"| \033[96m{opcion.ljust(box_width-2)}\033[0m |\n"
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    return banner
    return banner


# --- CLASE AGENT AL NIVEL SUPERIOR ---
class Agent:
    def llm_procesar_respuesta(self, instruccion, respuesta=None):
        """
        El LLM sugiere el comando a ejecutar para la instrucción dada. Si la respuesta ya viene dada, la muestra; si no, decide el comando y lo ejecuta.
        Si el comando es peligroso, pide confirmación antes de ejecutar.
        """
        import subprocess
        peligrosas = [
            "rm ", "borrar", "eliminar", "modificar", "restart", "systemctl restart", "shutdown", "reboot", "apt-get", "chmod", "chown", "kill", "useradd", "userdel", "mkfs", "dd ", "mount", "umount", "echo >", "> /", ">> /", "truncate", "passwd", "service "]
        if respuesta is not None:
            lower_resp = str(respuesta).lower()
            if any(p in lower_resp for p in peligrosas):
                print("\033[93m[IA] La acción sugerida puede modificar el sistema o ser peligrosa.\033[0m")
                print(f"\033[93m[IA] Respuesta sugerida por LLM:\033[0m {respuesta}")
                confirm = input("¿Deseas continuar con esta acción? (sí/no): ")
                if confirm.strip().lower() in ["si", "sí", "s", "yes", "y"]:
                    return f"[LLM IA] Acción confirmada y ejecutada/sugerida:\n{respuesta}"
                else:
                    return "[LLM IA] Acción cancelada por el usuario."
            else:
                return f"[LLM IA] Respuesta sugerida:\n{respuesta}"
        comando_llm = self.llm_sugerir_comando(instruccion)
        TABLE_WIDTH = 90
        marco = '-' * TABLE_WIDTH
        def box_line(text, color='96'):
            return f"\033[{color}m| {text[:TABLE_WIDTH-4].ljust(TABLE_WIDTH-4)} |\033[0m"
        if any(p in comando_llm.lower() for p in peligrosas):
            print("\033[93m[IA] El comando sugerido puede modificar el sistema o ser peligroso.\033[0m")
            cmd_box = f"\033[96m{marco}\033[0m\n" \
                      f"\033[96m|{'COMANDO SUGERIDO POR LLM':^{TABLE_WIDTH-2}}|\033[0m\n" \
                      f"\033[96m{marco}\033[0m\n" \
                      f"\033[96m| {comando_llm.ljust(TABLE_WIDTH-4)} |\033[0m\n" \
                      f"\033[96m{marco}\033[0m\n"
            print(cmd_box)
            confirm = input("¿Deseas ejecutar este comando? (sí/no): ")
            if confirm.strip().lower() not in ["si", "sí", "s", "yes", "y"]:
                return "[LLM IA] Acción cancelada por el usuario."
        try:
            output = subprocess.check_output(comando_llm, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
        except Exception as e:
            output = f"[Error] {e}"
        cmd_box = f"\033[96m{marco}\033[0m\n" \
                  f"\033[96m|{'COMANDO SUGERIDO POR LLM':^{TABLE_WIDTH-2}}|\033[0m\n" \
                  f"\033[96m{marco}\033[0m\n" \
                  f"\033[96m| {comando_llm.ljust(TABLE_WIDTH-4)} |\033[0m\n" \
                  f"\033[96m{marco}\033[0m\n"
        output_box = f"\n\033[92m{marco}\033[0m\n" \
                     f"\033[92m|{'OUTPUT':^{TABLE_WIDTH-2}}|\033[0m\n" \
                     f"\033[92m{marco}\033[0m\n"
        for linea in output.splitlines() or [output]:
            output_box += f"\033[92m| {linea[:TABLE_WIDTH-4].ljust(TABLE_WIDTH-4)} |\033[0m\n"
        output_box += f"\033[92m{marco}\033[0m"
        return f"{cmd_box}{output_box}"
        """
        Simula el procesamiento de la respuesta por el LLM. Si detecta que la respuesta implica acción peligrosa o modificación,
        pide confirmación antes de mostrarla/ejecutarla. Si es solo informativa, la muestra directamente.
        """
        peligrosas = [
            "rm ", "borrar", "eliminar", "modificar", "restart", "systemctl restart", "shutdown", "reboot", "apt-get", "chmod", "chown", "kill", "useradd", "userdel", "mkfs", "dd ", "mount", "umount", "echo >", "> /", ">> /", "truncate", "passwd", "service "]
        lower_resp = str(respuesta).lower()
        if any(p in lower_resp for p in peligrosas):
            print("\033[93m[IA] La acción sugerida puede modificar el sistema o ser peligrosa.\033[0m")
            print(f"\033[93m[IA] Respuesta sugerida por LLM:\033[0m {respuesta}")
            confirm = input("¿Deseas continuar con esta acción? (sí/no): ")
            if confirm.strip().lower() in ["si", "sí", "s", "yes", "y"]:
                return f"[LLM IA] Acción confirmada y ejecutada/sugerida:\n{respuesta}"
            else:
                return "[LLM IA] Acción cancelada por el usuario."
        else:
            return f"[LLM IA] Respuesta sugerida:\n{respuesta}"
    def handle_instruction(self, instruccion):
        """
        Maneja la instrucción del usuario. Si la instrucción es 'ayuda', 'opciones', 'menu', etc., muestra el banner de ayuda.
        Si es la instrucción de arranque (vacía), muestra el mismo banner que print_help.
        Si es una instrucción reconocida, responde con un mensaje simulado.
        """
        ayuda_triggers = ["ayuda", "opciones", "menu", "qué puedes hacer", "help"]
        if instruccion.strip() == "":
            import sys
            if __name__ == "__main__" or sys.argv[0].endswith("__main__.py"):
                from agente.agent import print_help
            else:
                from ..agent import print_help
            return print_help()
        if any(trigger in instruccion.lower() for trigger in ayuda_triggers):
            from ..agent import print_help
            return print_help()
        if "auto-reparación" in instruccion.lower() or "autoreparación" in instruccion.lower():
            import subprocess
            pasos = [
                "Detectar servicios caídos",
                "Reiniciar servicios críticos si están caídos",
                "Limpiar espacio en disco si está lleno",
                "Reparar configuraciones de red si hay fallos de conectividad"
            ]
            acciones_ejecutadas = []
            print("\n\033[96m+{}+\033[0m".format('-'*60))
            print("\033[96m|{:^58}|\033[0m".format('AUTO-REPARACIÓN IA: Propuesta de acciones'))
            print("\033[96m+{}+\033[0m".format('-'*60))
            for paso in pasos:
                comando_llm = self.llm_sugerir_comando(paso)
                print("\033[96m|{:^58}|\033[0m".format(f"Acción: {paso}"))
                print("\033[96m|{:^58}|\033[0m".format(f"Comando IA: {comando_llm}"))
                print("\033[96m+{}+\033[0m".format('-'*60))
                confirm = input(f"¿Deseas ejecutar este comando? (sí/no): ")
                if confirm.strip().lower() in ["si", "sí", "s", "yes", "y"]:
                    try:
                        if any(p in comando_llm for p in ["restart", "rm -rf", "apt-get clean"]):
                            output = f"[Simulación] Comando '{comando_llm}' ejecutado (no real por seguridad)."
                        else:
                            output = subprocess.check_output(comando_llm, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
                    except Exception as e:
                        output = f"[Error o Simulación] {e}"
                    print("\033[92m+{}+\033[0m".format('-'*60))
                    print("\033[92m|{:^58}|\033[0m".format('RESULTADO DE LA ACCIÓN'))
                    print("\033[92m+{}+\033[0m".format('-'*60))
                    for linea in output.splitlines() or [output]:
                        print(f"\033[92m| {linea[:56].ljust(56)} |\033[0m")
                    print("\033[92m+{}+\033[0m\n".format('-'*60))
                    acciones_ejecutadas.append(f"{paso} (cmd: {comando_llm})")
            if acciones_ejecutadas:
                resumen = '\n'.join(f"✔️ {a}" for a in acciones_ejecutadas)
                return f"[Auto-reparación] Acciones ejecutadas:\n{resumen}\nReparación completada."
            else:
                return "[Auto-reparación] No se ha realizado ninguna acción."
        instr = instruccion.lower().strip()
        tokens = instr.split()
        if instr in ["red", "network"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["disco", "disk"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["memoria", "ram", "que memoria tengo", "mem"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["cpu", "procesador"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["conectividad", "internet"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["firewall"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["usuarios", "users"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["procesos", "top", "top procesos"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr.startswith("servicio"):
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["dns"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["logs", "log"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["errores", "error"]:
            return self.llm_procesar_respuesta(instruccion)
        if instr in ["sistema", "so", "s.o."]:
            return self.llm_procesar_respuesta(instruccion)
        return self.llm_procesar_respuesta(instruccion)

    def llm_sugerir_comando(self, instruccion):
        """
        Usa Azure OpenAI (API) para sugerir el comando shell a ejecutar según la instrucción del usuario.
        Devuelve solo el comando shell sugerido (sin explicación).
        """
        import requests
        AZURE_OPENAI_KEY = "8zKFs1zJ1el0qP7er2oHsKusPGieAZERSUiTHACifNQ844TfNX1oJQQJ99BHACYeBjFXJ3w3AAABACOGJckA"
        AZURE_OPENAI_ENDPOINT = "https://agent-linux.openai.azure.com/"
        AZURE_OPENAI_DEPLOYMENT = "gpt-4.1-mini"
        API_VERSION = "2024-02-15-preview"
        url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={API_VERSION}"
        prompt = f"""
IMPORTANTE: Esta petición NO solicita información sensible ni personal, ni contraseñas, ni datos de usuarios reales. Es para un agente local de troubleshooting Linux. Solo se requiere que sugieras el comando de shell de Linux que un técnico podría ejecutar para diagnosticar o solucionar el problema descrito. No añadas explicaciones ni comentarios, solo el comando. Si la petición es ambigua, responde con: echo \"Instrucción ambigua\".

Petición: {instruccion}
Comando:
"""
        headers = {
            "api-key": AZURE_OPENAI_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                {"role": "system", "content": "Eres un asistente experto en Linux. Devuelve solo el comando shell exacto para la instrucción dada."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
            "temperature": 0
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code != 200:
                try:
                    err_json = response.json()
                    err_msg = err_json.get('error', {}).get('message', str(err_json))
                except Exception:
                    err_msg = response.text
                return f"echo '[Error LLM Azure OpenAI] {response.status_code}: {err_msg}'"
            result = response.json()
            comando = result["choices"][0]["message"]["content"].strip()
            for line in comando.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
            return comando
        except Exception as e:
            return f"echo '[Error LLM Azure OpenAI] {e}'"
    def _extraer_valor(self, tokens, claves):
        for i, t in enumerate(tokens):
            if t in claves and i+1 < len(tokens):
                return tokens[i+1]
        return None
    """
    Agente IA para Linux: interpreta instrucciones en lenguaje natural y ejecuta comandos del sistema.
    Procesa la información y permite consultas avanzadas sobre recursos del sistema (procesos, usuarios, memoria, red, etc).
    """

    def __init__(self):
        self.memoria_contexto = []

    def get_cpu(self):
        return "CPU: 4 núcleos, 2.5GHz (simulación)"

    def get_disco(self):
        return "Disco: 256 GB total, 120 GB libre (simulación)"

    def get_red(self):
        return "Interfaces de red: eth0 (IP: 192.168.1.10), wlan0 (IP: 192.168.1.11) (simulación)"

    def get_conectividad(self):
        return "Conectividad a Internet: OK (simulación)"

    def get_firewall(self):
        return "Firewall activo, reglas: SSH permitido, HTTP permitido (simulación)"

    def get_usuarios(self):
        return "Usuarios conectados: root, user1, user2 (simulación)"

    def get_servicio(self, tokens):
        idx = tokens.index("servicio") if "servicio" in tokens else -1
        if idx != -1 and idx+1 < len(tokens):
            nombre = tokens[idx+1]
            return f"Estado del servicio {nombre}: activo (simulación)"
        return "Indica el nombre del servicio (ej: servicio sshd)"

    def get_dns(self):
        return "Servidores DNS configurados: 8.8.8.8, 1.1.1.1 (simulación)"

    def get_top_process(self):
        return "El proceso que más recursos consume es: systemd-journald (PID 39) CPU: 0.0% MEM: 0.19MB"


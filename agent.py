
def print_help():
    import shutil
    def center_text(text, width):
        return text.center(width)
    def wrap_text(text, width):
        import textwrap
        return textwrap.wrap(text, width)
    box_width = shutil.get_terminal_size((80, 20)).columns - 2
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
        "",
        "Puedes usar frases naturales como 'quiero ver la memoria', 'estado de la red', 'cuánta ram hay', etc.",
        "Para salir: salir, exit, quit.",
        "Para ver este menú: ayuda, opciones, qué puedes hacer, etc."
    ]
    banner = "\033[96m+{}+\033[0m\n".format('-'*box_width)
    banner += "\033[96m|{}|\033[0m\n".format(center_text('🧠  Agente IA para Linux  🧠', box_width))
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    for opcion in opciones:
        for linea in wrap_text(opcion, box_width-2):
            banner += f"| \033[96m{linea.ljust(box_width-2)}\033[0m |\n"
    banner += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    return banner
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
                resultado = subprocess.check_output(comando, shell=True, text=True)
                resumen = f"Resultado de '{comando}':\n{resultado.strip()}"
                self.memoria_contexto.append(resumen)
                self.pendiente_confirmacion = None
                return f"{sugerencia}\n\n\n\n{resultado_top}\n\033[92m{resultado.strip()}\033[0m\n{resultado_bottom}"
            except Exception as e:
                self.pendiente_confirmacion = None
                return f"{sugerencia}\n\n\n\n\033[91m🟥━━ ERROR AL EJECUTAR COMANDO ━━🟥\033[0m\n\033[91m{e}\033[0m\n\033[91m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
        from agente.llm_client import query_llm
        import re
        import subprocess
        # Prompt extendido para el LLM
        system_prompt = (
            "Eres un agente Python que puede ejecutar comandos en el sistema Linux del usuario. "
            "Si el usuario pide una acción, responde con el comando bash necesario en un bloque de código, sin decir que no tienes acceso. "
            "No expliques que eres una IA, solo responde con el comando y una breve explicación si es útil. "
            "Ejemplo de formato: \nExplicación breve\n```bash\ncomando\n```"
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
        # Buscar bloque de código bash en la respuesta
        match = re.search(r"```bash[\s\S]*?```", respuesta)
        if match:
            bloque = match.group(0)
            # Separar explicación y bloque bash
            partes = respuesta.split(bloque)
            explicacion = partes[0].strip() if len(partes) > 1 else ""
            # Simular caja markdown con borde y color
            # Florituras y etiquetas decorativas
            # Utilidades para centrar y envolver texto
            def center_text(text, width):
                return text.center(width)
            def wrap_text(text, width):
                import textwrap
                return textwrap.wrap(text, width)
            import shutil
            box_width = shutil.get_terminal_size((80, 20)).columns - 2
            # Caja ASCII para sugerencia
            sugerencia_box = "\033[93m+{}+\033[0m\n".format('-'*box_width)
            sugerencia_box += "\033[93m|{}|\033[0m\n".format(center_text('SUGERENCIA DEL LLM', box_width))
            sugerencia_box += "\033[93m+{}+\033[0m\n".format('-'*box_width)
            # Explicación envuelta
            for linea in wrap_text(explicacion, box_width-2):
                sugerencia_box += f"| \033[93m{linea.ljust(box_width-2)}\033[0m |\n"
            # Comando sugerido
            sugerencia_box += f"|\033[96m{'  Comando sugerido:'.ljust(box_width-2)}\033[0m|\n"
            comando_sugerido = bloque.replace('```bash','').replace('```','').strip()
            for linea in wrap_text(comando_sugerido, box_width-2):
                sugerencia_box += f"| \033[96m{linea.ljust(box_width-2)}\033[0m |\n"
            sugerencia_box += "\033[93m+{}+\033[0m\n".format('-'*box_width)
            # Caja ASCII para resultado
            resultado_box = "\033[92m+{}+\033[0m\n".format('-'*box_width)
            resultado_box += "\033[92m|{}|\033[0m\n".format(center_text('RESULTADO DEL COMANDO', box_width))
            resultado_box += "\033[92m+{}+\033[0m\n".format('-'*box_width)
            # Caja ASCII para error
            error_box = "\033[91m+{}+\033[0m\n".format('-'*box_width)
            error_box += "\033[91m|{}|\033[0m\n".format(center_text('ERROR AL EJECUTAR COMANDO', box_width))
            error_box += "\033[91m+{}+\033[0m\n".format('-'*box_width)
            # Extraer solo el comando para ejecutar
            comando_match = re.search(r"```bash\s*([^`]+)```", bloque)
            comando = comando_match.group(1).strip() if comando_match else None
            if comando:
                # Detectar comandos delicados
                peligrosos = [
                    "rm ", "mv ", "chmod ", "chown ", "dd ", "shutdown", "reboot", "systemctl stop", "systemctl restart",
                    "userdel", "groupdel", "passwd", "usermod", "groupmod"
                ]
                requiere_confirmacion = any(p in comando for p in peligrosos)
                if requiere_confirmacion:
                    self.pendiente_confirmacion = {'comando': comando, 'sugerencia': sugerencia_box}
                    return f"\033[91m⚠️  ATENCIÓN: El comando sugerido puede modificar o eliminar datos del sistema.\033[0m\n\033[93mPor favor, confirma manualmente si deseas ejecutarlo:\033[0m\n\n{sugerencia_box}\n\nPara ejecutar, responde: 'confirmar'"
                try:
                    import os
                    resultado = subprocess.check_output(comando, shell=True, text=True)
                    resumen = f"Resultado de '{comando}':\n{resultado.strip()}"
                    mostrar_resumen = None
                    # Detecta si el comando es de creación/modificación de archivo
                    if comando.startswith('echo ') and ' > ' in comando:
                        archivo = comando.split('>')[-1].strip()
                        if os.path.exists(archivo):
                            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                                contenido = f.read()
                            mostrar_resumen = f"Se ha generado/modificado el archivo: {archivo}\nContenido:\n{contenido}"
                    elif comando.startswith('touch '):
                        archivo = comando.split('touch ')[-1].strip()
                        if os.path.exists(archivo):
                            mostrar_resumen = f"Se ha creado el archivo: {archivo}\nContenido:\n" + open(archivo, 'r', encoding='utf-8', errors='ignore').read()
                    elif comando.startswith('truncate '):
                        archivo = comando.split('truncate -s ')[-1].split(' ')[-1].strip()
                        if os.path.exists(archivo):
                            mostrar_resumen = f"Se ha truncado el archivo: {archivo}\nContenido:\n" + open(archivo, 'r', encoding='utf-8', errors='ignore').read()
                    elif comando.startswith('cp '):
                        partes = comando.split('cp ')[-1].split(' ')
                        if len(partes) == 2 and os.path.exists(partes[1]):
                            mostrar_resumen = f"Se ha copiado el archivo a: {partes[1]}\nContenido:\n" + open(partes[1], 'r', encoding='utf-8', errors='ignore').read()
                    # Detecta si el comando modifica una variable de entorno
                    elif comando.startswith('export '):
                        var = comando.split('export ')[-1].split('=')[0].strip()
                        valor = os.environ.get(var, None)
                        mostrar_resumen = f"Variable de entorno '{var}' actualizada. Valor: {valor}"
                    elif comando.startswith('set '):
                        var = comando.split('set ')[-1].split('=')[0].strip()
                        valor = os.environ.get(var, None)
                        mostrar_resumen = f"Variable de entorno '{var}' actualizada. Valor: {valor}"
                    if mostrar_resumen:
                        self.memoria_contexto.append(mostrar_resumen)
                    opciones_resumen = "\n\033[94m[Opciones rápidas]\033[0m sistema | cpu | memoria | disco | red | procesos | usuarios | servicio <nombre> | dns | salir\n"
                    def tabla_encabezado(texto, color, ancho):
                        return f"{color}+{'-'*ancho}+\033[0m\n{color}|{texto.center(ancho)}|\033[0m\n{color}+{'-'*ancho}+\033[0m\n"
                    ancho = box_width
                    sugerencia_tabla = tabla_encabezado('SUGERENCIA DEL LLM', '\033[93m', ancho)
                    resultado_tabla = tabla_encabezado('RESULTADO DEL COMANDO', '\033[92m', ancho)
                    # Sugerencia (explicación y comando)
                    sugerencia_contenido = ''
                    for linea in wrap_text(explicacion, ancho-2):
                        sugerencia_contenido += f"| \033[93m{linea.ljust(ancho-2)}\033[0m |\n"
                    sugerencia_contenido += f"|\033[96m{'  Comando sugerido:'.ljust(ancho-2)}\033[0m|\n"
                    for linea in wrap_text(comando_sugerido, ancho-2):
                        sugerencia_contenido += f"| \033[96m{linea.ljust(ancho-2)}\033[0m |\n"
                    sugerencia_contenido += "\033[93m+{}+\033[0m\n".format('-'*ancho)
                    def append_options(text):
                        return (text if text.endswith('\n') else text + '\n') + opciones_resumen
                    # Mostrar resumen si existe (archivo/config/output/variable)
                    if mostrar_resumen is not None:
                        if '\nContenido:\n' in mostrar_resumen:
                            partes = mostrar_resumen.split('\nContenido:\n', 1)
                            encabezado = partes[0]
                            contenido = partes[1]
                            return f"{sugerencia_tabla}{sugerencia_contenido}{resultado_tabla}{append_options(contenido)}"
                        else:
                            return f"{sugerencia_tabla}{sugerencia_contenido}{resultado_tabla}{append_options(mostrar_resumen)}"
                    else:
                        self.memoria_contexto.append(resumen)
                        return f"{sugerencia_tabla}{sugerencia_contenido}{resultado_tabla}{append_options(resultado.strip())}"
                except Exception as e:
                    # Encabezado de error con tabla
                    error_tabla = tabla_encabezado('ERROR AL EJECUTAR COMANDO', '\033[91m', box_width)
                    error_contenido = ''
                    for linea in wrap_text(str(e), box_width-2):
                        error_contenido += f"| \033[91m{linea.ljust(box_width-2)}\033[0m |\n"
                    error_contenido += "\033[91m+{}+\033[0m\n".format('-'*box_width)
                    return f"{sugerencia_tabla}{error_tabla}{error_contenido}"
            else:
                error_contenido = ''
                for linea in wrap_text('No se pudo extraer el comando para ejecutar.', box_width-2):
                    error_contenido += f"| \033[91m{linea.ljust(box_width-2)}\033[0m |\n"
                error_contenido += "\033[91m+{}+\033[0m\n".format('-'*box_width)
                return f"{sugerencia_box}\n\n{error_box}{error_contenido}"
        return f"\033[95m[RESPUESTA LLM]\033[0m\n{respuesta}"

    def _extraer_valor(self, tokens, claves):
        # Busca el valor después de una clave
        for i, t in enumerate(tokens):
            if t in claves and i+1 < len(tokens):
                return tokens[i+1]
        return None
    """
    Agente IA para Linux: interpreta instrucciones en lenguaje natural y ejecuta comandos del sistema.
    Procesa la información y permite consultas avanzadas sobre recursos del sistema (procesos, usuarios, memoria, red, etc).
    """

    def __init__(self):
        import spacy
        # Solo inicializa memoria_contexto
        self.memoria_contexto = []
    def get_cpu(self):
        respuesta = query_llm(prompt)

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
        # Busca el nombre del servicio en los tokens
        idx = tokens.index("servicio") if "servicio" in tokens else -1
        if idx != -1 and idx+1 < len(tokens):
            nombre = tokens[idx+1]
            return f"Estado del servicio {nombre}: activo (simulación)"
        return "Indica el nombre del servicio (ej: servicio sshd)"

    def get_dns(self):
        return "Servidores DNS configurados: 8.8.8.8, 1.1.1.1 (simulación)"

    def get_top_process(self):
        # Simulación: deberías implementar la lógica real aquí
        return "El proceso que más recursos consume es: systemd-journald (PID 39) CPU: 0.0% MEM: 0.19MB"

        # Usuarios: devuelve lista procesable y permite consultas
        if match_keywords(instr, "usuarios"):
            usuarios = usuarios_conectados(return_data=True)  # Debe devolver lista de dicts
            if "cuantos" in instr or "cuántos" in instr:
                return f"Hay {len(usuarios)} usuarios conectados."
            if "root" in instr:
                root_users = [u for u in usuarios if u['nombre'] == 'root']
                if root_users:
                    return "El usuario root está conectado."
                else:
                    return "El usuario root no está conectado."
            # Si no hay consulta específica, muestra resumen
            resumen = "Usuarios conectados:\n" + "\n".join([f"{u['nombre']} desde {u['origen']}" for u in usuarios])
            return resumen

        # Servicios
        if match_keywords(instr, "servicio"):
            partes = instr.split()
            for i, p in enumerate(partes):
                if p == "servicio" and i+1 < len(partes):
                    return estado_servicio(partes[i+1])
            return "Indica el nombre del servicio (ej: servicio sshd)"

        return "Instrucción no reconocida. Opciones: sistema, cpu, memoria, disco, red, conectividad, firewall, procesos, usuarios, servicio <nombre>, dns."

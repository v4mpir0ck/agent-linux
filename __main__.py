
from .agent import Agent

def print_banner():
    import shutil
    def center_text(text, width):
        return text.center(width)
    def wrap_text(text, width):
        import textwrap
        return textwrap.wrap(text, width)
    box_width = shutil.get_terminal_size((80, 20)).columns - 2
    bienvenida = [
        "🧠  Agente IA para Linux  🧠",
        "",
        "Opciones disponibles:",
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
    bienvenida_box = "\033[96m+{}+\033[0m\n".format('-'*box_width)
    bienvenida_box += "\033[96m|{}|\033[0m\n".format(center_text('🧠  Agente IA para Linux  🧠', box_width))
    bienvenida_box += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    for linea in bienvenida[2:]:
        for l in wrap_text(linea, box_width-2):
            bienvenida_box += f"| \033[96m{l.ljust(box_width-2)}\033[0m|\n"
    bienvenida_box += "\033[96m+{}+\033[0m\n".format('-'*box_width)
    print(bienvenida_box)

if __name__ == "__main__":
    print_banner()
    agent = Agent()
    while True:
        instruction = input("\033[96m👉 Instrucción: \033[0m")
        if instruction.lower() in ["salir", "exit", "quit"]:
            print("\033[91m👋 Cerrando agente. ¡Hasta pronto!\033[0m")
            break
        result = agent.handle_instruction(instruction)
        print(result)

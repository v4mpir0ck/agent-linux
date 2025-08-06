
import sys
import os
from agent import Agent

def print_banner():
    print("\033[96m\n🧠  Agente IA para Linux  🧠\033[0m")
    print("\033[93m-----------------------------------\033[0m")
    print("\033[92mOpciones disponibles:\033[0m")
    print("🖥️  sistema: Info del sistema operativo")
    print("🧮  cpu: Info de la CPU")
    print("💾  memoria: Info de la memoria RAM")
    print("📀  disco: Info de discos y particiones")
    print("🌐  red: Info de interfaces de red")
    print("📡  conectividad: Chequeo de conexión a Internet")
    print("🛡️  firewall: Estado del firewall")
    print("📊  procesos: Procesos más consumidores")
    print("👥  usuarios: Usuarios conectados")
    print("🔧  servicio <nombre>: Estado de un servicio (ej: servicio sshd)")
    print("🗂️  dns: Muestra servidores DNS del sistema\n")
    print("Puedes usar frases naturales como 'quiero ver la memoria', 'estado de la red', 'cuánta ram hay', etc.")
    print("Para salir: salir, exit, quit.")
    print("Para ver este menú: ayuda, opciones, qué puedes hacer, etc.")
    print("\033[93m-----------------------------------\033[0m")

def main():
    print_banner()
    agent = Agent()
    # Si se pasa argumento, lo procesa directamente
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
        respuesta = agent.handle_instruction(instruction)
        print(respuesta)
        return
    # Modo interactivo
    while True:
        try:
            instruction = input("\033[96m👉 Instrucción: \033[0m")
            if instruction.lower() in ["salir", "exit", "quit"]:
                print("\033[91m👋 Cerrando agente. ¡Hasta pronto!\033[0m")
                break
            result = agent.handle_instruction(instruction)
            print(result)
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()

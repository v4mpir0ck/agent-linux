
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import Agent, print_help

if __name__ == "__main__":
    print(print_help())
    agent = Agent()
    try:
        while True:
            instruction = input("\033[96m👉 Instrucción: \033[0m")
            if instruction.lower() in ["salir", "exit", "quit"]:
                print("\033[91m👋 Cerrando agente. ¡Hasta pronto!\033[0m")
                break
            result = agent.handle_instruction(instruction)
            print(result)
    except KeyboardInterrupt:
        print("\n\033[92mGracias por usar el Agente IA para Linux. ¡Hasta pronto!\033[0m")
        exit(0)

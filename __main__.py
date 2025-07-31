from .agent import Agent


if __name__ == "__main__":
    agent = Agent()
    while True:
        instruction = input("\033[96m👉 Instrucción: \033[0m")
        if instruction.lower() in ["salir", "exit", "quit"]:
            print("\033[91m👋 Cerrando agente. ¡Hasta pronto!\033[0m")
            break
        result = agent.handle_instruction(instruction)
        print(result)

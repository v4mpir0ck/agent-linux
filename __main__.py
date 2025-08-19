
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import Agent, print_help

if __name__ == "__main__":
    try:
        import readline
    except ImportError:
        pass
    print("\n\033[96mAgente IA para Linux (modo interactivo)\033[0m")
    print("Escribe 'salir' para terminar.\n")
    # Mostrar info de LLM
    try:
        try:
            from llm_client import LLM_ENDPOINT, LLM_MODEL
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
    print("\033[91m[AVISO] Todas las opciones pasan por el LLM, por lo que el resultado puede variar según el contexto proporcionado.\033[0m\n")
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
        sys.exit(0)

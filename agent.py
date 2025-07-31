from .commands.dns import revisar_dns

class Agent:
    def handle_instruction(self, instruction: str) -> str:
        if "dns" in instruction.lower():
            return revisar_dns()
        return "Instrucción no reconocida."

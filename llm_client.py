import requests
import os
import base64
import hashlib
from cryptography.fernet import Fernet

# --- Token seguro: desencriptar si existe azure_openai_token.enc ---
def _get_azure_openai_key():
    enc_path = os.path.join(os.path.dirname(__file__), "azure_openai_token.enc")
    if os.path.exists(enc_path):
        import getpass
        print("\033[93m[SEC] Token encriptado detectado.\033[0m")
        for intento in range(3):
            passphrase = getpass.getpass("Introduce la passphrase para el token Azure OpenAI: ")
            key = hashlib.sha256(passphrase.encode()).digest()[:32]
            fernet_key = base64.urlsafe_b64encode(key)
            fernet = Fernet(fernet_key)
            try:
                with open(enc_path, "rb") as f:
                    token_enc = f.read()
                token = fernet.decrypt(token_enc).decode()
                print("\033[92m[SEC] Token desencriptado correctamente.\033[0m")
                return token
            except Exception as e:
                print(f"\033[91m[SEC] Error de desencriptado: {e}\033[0m")
        print("\033[91m[SEC] No se pudo desencriptar el token tras 3 intentos.\033[0m")
        exit(1)
    # Fallback: variable de entorno o hardcoded
    return os.getenv("AZURE_OPENAI_KEY", "8zKFs1zJ1el0qP7er2oHsKusPGieAZERSUiTHACifNQ844TfNX1oJQQJ99BHACYeBjFXJ3w3AAABACOGJckA")

AZURE_OPENAI_KEY = _get_azure_openai_key()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://agent-linux.openai.azure.com/")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

# Alias para compatibilidad con el agente (deben ir después de definir las variables originales)
LLM_ENDPOINT = AZURE_OPENAI_ENDPOINT
LLM_MODEL = AZURE_OPENAI_DEPLOYMENT

# Función para consultar el LLM
def query_llm(prompt, temperature=0.2, max_tokens=256):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def query_llm(prompt, temperature=0.2, max_tokens=256):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

# Ejemplo de uso:
if __name__ == "__main__":
    prompt = "¿Cuál es el hostname actual de este sistema Linux?"
    print(query_llm(prompt))

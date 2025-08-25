import os
import sys
import json
import base64
import hashlib
import requests
from dotenv import load_dotenv
from cryptography.fernet import Fernet

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def interactive_llm_config():
    enc_path = os.path.join(os.path.dirname(sys.argv[0]), "azure_openai_token.enc")
    import getpass
    # Try to load from encrypted file if present
    if os.path.exists(enc_path):
        for intento in range(3):
            try:
                passphrase = getpass.getpass("Introduce la passphrase para el token Azure OpenAI: ")
                key_bytes = hashlib.sha256(passphrase.encode()).digest()[:32]
                fernet_key = base64.urlsafe_b64encode(key_bytes)
                fernet = Fernet(fernet_key)
                with open(enc_path, "rb") as f:
                    token_enc = f.read()
                llm_data = fernet.decrypt(token_enc).decode()
                llm_parts = llm_data.split('\n')
                if len(llm_parts) == 4:
                    endpoint, deployment, api_version, key = llm_parts
                    print("\033[92m[LLM] Token desencriptado correctamente.\033[0m")
                    return endpoint, deployment, api_version, key
                else:
                    print("\033[91m[LLM] Formato de datos incorrecto.\033[0m")
            except KeyboardInterrupt:
                print("\n\033[92m[LLM] Salida ordenada: operación cancelada por el usuario.\033[0m")
                exit(0)
            except Exception as e:
                print(f"\033[91m[LLM] Error de desencriptado: {e}\033[0m")
        print("\033[91m[LLM] No se pudo desencriptar el token tras 3 intentos.\033[0m")
        exit(1)
    # Fallback: load from .env
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    key = os.getenv("AZURE_OPENAI_KEY")
    return endpoint, deployment, api_version, key

def prompt_llm_config():
    import getpass
    print("\033[96m[LLM] ¿Quieres modificar la configuración del LLM (endpoint, key, modelo)?\033[0m")
    resp = input("[LLM] Escribe 's' para editar o cualquier otra tecla para continuar: ").strip().lower()
    if resp == "s":
        endpoint = input(f"Nuevo endpoint [{os.getenv('AZURE_OPENAI_ENDPOINT','')}] : ").strip() or os.getenv('AZURE_OPENAI_ENDPOINT','')
        deployment = input(f"Nombre del modelo/deployment [{os.getenv('AZURE_OPENAI_DEPLOYMENT','')}] : ").strip() or os.getenv('AZURE_OPENAI_DEPLOYMENT','')
        api_version = input(f"API version [{os.getenv('AZURE_OPENAI_API_VERSION','')}] : ").strip() or os.getenv('AZURE_OPENAI_API_VERSION','')
        key = getpass.getpass(f"API Key/token [{(os.getenv('AZURE_OPENAI_KEY','')[:6] + '...') if os.getenv('AZURE_OPENAI_KEY','') else ''}] : ").strip() or os.getenv('AZURE_OPENAI_KEY','')
        return endpoint, deployment, api_version, key
    return None

# --- Token seguro: desencriptar si existe azure_openai_token.enc ---
llm_config = prompt_llm_config()
if llm_config:
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_KEY = llm_config
else:
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_KEY = interactive_llm_config()
LLM_ENDPOINT = AZURE_OPENAI_ENDPOINT
LLM_MODEL = AZURE_OPENAI_DEPLOYMENT

def query_llm(prompt, temperature=0.2, max_tokens=256):
    endpoint = LLM_ENDPOINT
    deployment = LLM_MODEL
    api_version = AZURE_OPENAI_API_VERSION
    key = AZURE_OPENAI_KEY
    if not endpoint or not deployment or not api_version or not key:
        return "[ERROR] LLM no está configurado correctamente."
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": key
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] LLM request failed: {e}"

# Optional: test block
if __name__ == "__main__":
    prompt = "¿Cuál es el hostname actual de este sistema Linux?"
    print(query_llm(prompt))

from dotenv import load_dotenv
import os
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
import requests
import os
import base64
import hashlib
from cryptography.fernet import Fernet

def interactive_llm_config():
    enc_path = os.path.join(os.path.dirname(__file__), "azure_openai_token.enc")
    import getpass
    print("\033[96m[LLM] ¿Quieres modificar la configuración del LLM (endpoint, key, modelo)?\033[0m")
    resp = input("[LLM] Escribe 's' para editar o cualquier otra tecla para continuar: ").strip().lower()
    # Cargar valores actuales si existen
    current_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    current_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    current_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    current_key = os.getenv("AZURE_OPENAI_KEY")
    # Si existe el archivo encriptado, intentar leerlo para mostrar los valores actuales
    if os.path.exists(enc_path):
        import getpass
        for intento in range(1):
            passphrase = getpass.getpass("Introduce la passphrase para mostrar los valores actuales: ")
            key_bytes = hashlib.sha256(passphrase.encode()).digest()[:32]
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            fernet = Fernet(fernet_key)
            try:
                with open(enc_path, "rb") as f:
                    token_enc = f.read()
                llm_data = fernet.decrypt(token_enc).decode()
                llm_parts = llm_data.split('\n')
                if len(llm_parts) == 4:
                    current_endpoint, current_deployment, current_api_version, current_key = llm_parts
            except Exception:
                pass
    if resp == "s":
        endpoint = input(f"Nuevo endpoint [{current_endpoint}]: ").strip() or current_endpoint
        deployment = input(f"Nombre del modelo/deployment [{current_deployment}]: ").strip() or current_deployment
        api_version = input(f"API version [{current_api_version}]: ").strip() or current_api_version
        import getpass
        key = getpass.getpass(f"API Key/token [{current_key[:6]}...]: ").strip() or current_key
        passphrase = getpass.getpass("Passphrase para encriptar: ").strip()
        llm_data = f"{endpoint}\n{deployment}\n{api_version}\n{key}"
        key_bytes = hashlib.sha256(passphrase.encode()).digest()[:32]
        fernet_key = base64.urlsafe_b64encode(key_bytes)
        fernet = Fernet(fernet_key)
        with open(enc_path, "wb") as f:
            f.write(fernet.encrypt(llm_data.encode()))
        print("\033[92m[LLM] Configuración guardada y encriptada correctamente.\033[0m")
        return endpoint, deployment, api_version, key
    # Si existe el archivo, desencriptar como antes
    if os.path.exists(enc_path):
        for intento in range(3):
            passphrase = getpass.getpass("Introduce la passphrase para el token Azure OpenAI: ")
            key_bytes = hashlib.sha256(passphrase.encode()).digest()[:32]
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            fernet = Fernet(fernet_key)
            try:
                with open(enc_path, "rb") as f:
                    token_enc = f.read()
                llm_data = fernet.decrypt(token_enc).decode()
                llm_parts = llm_data.split('\n')
                if len(llm_parts) == 4:
                    endpoint, deployment, api_version, key = llm_parts
                else:
                    raise ValueError("Formato de datos LLM incorrecto. Esperado 4 líneas.")
                print("\033[92m[LLM] Token desencriptado correctamente.\033[0m")
                return endpoint, deployment, api_version, key
            except Exception as e:
                print(f"\033[91m[LLM] Error de desencriptado: {e}\033[0m")
        print("\033[91m[LLM] No se pudo desencriptar el token tras 3 intentos.\033[0m")
        exit(1)
    # Fallback: variable de entorno o hardcoded
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    key = os.getenv("AZURE_OPENAI_KEY")
    return endpoint, deployment, api_version, key

# --- Token seguro: desencriptar si existe azure_openai_token.enc ---
AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_KEY = interactive_llm_config()

# Alias para compatibilidad con el agente (deben ir después de definir las variables originales)
LLM_ENDPOINT = AZURE_OPENAI_ENDPOINT
LLM_MODEL = AZURE_OPENAI_DEPLOYMENT

# Función para consultar el LLM
def query_llm(prompt, temperature=0.2, max_tokens=256):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
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
    import time
    max_retries = 5
    backoff = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"\033[93m[LLM] El servicio está saturado. Reintentando en {backoff} segundos...\033[0m")
                time.sleep(backoff)
                backoff *= 2
                continue
            else:
                print(f"\033[91m[LLM] Error HTTP: {e}\033[0m")
                return "[ERROR] El servicio LLM no está disponible. Intenta de nuevo en unos minutos."
        except Exception as e:
            print(f"\033[91m[LLM] Error: {e}\033[0m")
            return "[ERROR] El servicio LLM no está disponible. Intenta de nuevo en unos minutos."
    print("\033[91m[LLM] Se alcanzó el máximo de reintentos.\033[0m")
    return "[ERROR] El servicio LLM está saturado o no disponible. Intenta de nuevo en unos minutos."

## Eliminar duplicado y asegurar que query_llm usa la versión de API configurada

# Ejemplo de uso:
if __name__ == "__main__":
    prompt = "¿Cuál es el hostname actual de este sistema Linux?"
    print(query_llm(prompt))

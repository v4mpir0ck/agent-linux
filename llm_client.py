import os
import sys
import sys
import json
import requests
from dotenv import load_dotenv


def interactive_llm_config():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    key = os.getenv("AZURE_OPENAI_KEY")
    return endpoint, deployment, api_version, key


from config_path import get_env_path

def prompt_llm_config():
    print("\033[96m[LLM] ¿Quieres modificar la configuración del LLM (endpoint, key, modelo)?\033[0m")
    resp = input("[LLM] Escribe 's' para editar o cualquier otra tecla para continuar: ").strip().lower()
    if resp == "s":
        endpoint = input(f"Nuevo endpoint [{os.getenv('AZURE_OPENAI_ENDPOINT','')}] : ").strip() or os.getenv('AZURE_OPENAI_ENDPOINT','')
        deployment = input(f"Nombre del modelo/deployment [{os.getenv('AZURE_OPENAI_DEPLOYMENT','')}] : ").strip() or os.getenv('AZURE_OPENAI_DEPLOYMENT','')
        api_version = input(f"API version [{os.getenv('AZURE_OPENAI_API_VERSION','')}] : ").strip() or os.getenv('AZURE_OPENAI_API_VERSION','')
        key = input(f"API Key/token [{(os.getenv('AZURE_OPENAI_KEY','')[:6] + '...') if os.getenv('AZURE_OPENAI_KEY','') else ''}] : ").strip() or os.getenv('AZURE_OPENAI_KEY','')
        env_path = get_env_path()
        with open(env_path, 'w') as f:
            f.write(f'AZURE_OPENAI_ENDPOINT={endpoint}\n')
            f.write(f'AZURE_OPENAI_DEPLOYMENT={deployment}\n')
            f.write(f'AZURE_OPENAI_API_VERSION={api_version}\n')
            f.write(f'AZURE_OPENAI_KEY={key}\n')
        print(f"\033[92m[LLM] Configuración guardada en {env_path}\033[0m")
        return endpoint, deployment, api_version, key
    return None



load_dotenv(get_env_path())
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
# Si el usuario quiere modificar, se actualiza .env y variables
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

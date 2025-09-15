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



# Cargar dotenv: primero buscar .env en la carpeta donde se ejecuta el script/ejecutable
# (esto permite que `python3 agent.py` use el .env en ese folder o que el .exe use el .env junto al binario).
if getattr(sys, 'frozen', False):
    run_dir = os.path.dirname(sys.executable)
else:
    # sys.argv[0] puede ser relativo; obtén ruta absoluta
    run_dir = os.path.dirname(os.path.abspath(sys.argv[0])) or os.path.dirname(__file__)
env_in_run = os.path.join(run_dir, '.env')
env_path_candidate = get_env_path()
used_env_path = None
if os.path.isfile(env_in_run):
    load_dotenv(dotenv_path=env_in_run)
    used_env_path = env_in_run
elif os.path.isfile(env_path_candidate):
    load_dotenv(dotenv_path=env_path_candidate)
    used_env_path = env_path_candidate
else:
    # fallback: cargar variables de entorno ya presentes en el entorno
    load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
# Exponer qué archivo fue cargado (útil para debugging)
LOADED_ENV_PATH = used_env_path
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
    # Validación rápida de variables de entorno necesarias
    missing = []
    if not endpoint:
        missing.append('AZURE_OPENAI_ENDPOINT')
    if not deployment:
        missing.append('AZURE_OPENAI_DEPLOYMENT')
    if not api_version:
        missing.append('AZURE_OPENAI_API_VERSION')
    if not key:
        missing.append('AZURE_OPENAI_KEY')
    if missing:
        return f"[ERROR] LLM no está configurado correctamente. Faltan: {', '.join(missing)}"
    # Normalize endpoint to avoid double slashes when composing URL
    endpoint = endpoint.rstrip('/') if isinstance(endpoint, str) else endpoint
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    # Helpful debug info (not verbose) — kept as local variable for logging when needed
    _debug_url = url
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
        # If server responds with status >=400, raise HTTPError to handle it
        try:
            response.raise_for_status()
        except requests.HTTPError as http_err:
            # Special-case common Azure error for missing deployment
            body = response.text or ''
            if response.status_code == 404 and 'DeploymentNotFound' in body:
                return (f"[ERROR] Deployment not found. Verifica que AZURE_OPENAI_DEPLOYMENT='{deployment}' exista en el recurso y que "
                        f"AZURE_OPENAI_ENDPOINT esté correcto. Endpoint usado: {endpoint}")
            return f"[ERROR] LLM request failed: {http_err} - {body[:1000]}"
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR] LLM request failed: {e} (url={_debug_url})"

# Optional: test block
if __name__ == "__main__":
    prompt = "¿Cuál es el hostname actual de este sistema Linux?"
    print(query_llm(prompt))

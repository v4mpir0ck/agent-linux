
# --- Azure OpenAI integration ---
import os
from dotenv import load_dotenv
import json
from glob import glob
import requests

def windows_to_wsl_path(path):
    return path.replace('c:\\', '/mnt/c/').replace('\\', '/')


# Cargar variables de entorno desde .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Carpeta raíz de tus repositorios
def prompt_with_default(msg, default):
    resp = input(f"{msg} [{default}]: ").strip()
    return resp if resp else default

# Preguntar por el path de los repositorios y el fichero de output
REPOS_ROOT = prompt_with_default("Introduce el path donde tienes alojados los repositorios", os.environ.get("REPOS_ROOT", r"c:\shared\repos\MAPFRE"))
OUTPUT_FILE = prompt_with_default("Introduce el path del fichero de salida", windows_to_wsl_path(os.path.join(REPOS_ROOT, "dataset_dpo_v10.jsonl")))

# Endpoint y clave del agente (ajusta si tienes variables de entorno)
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

def generate_qas_with_llm(text, n_examples=3):
    prompt = (
        "Analiza el siguiente archivo y genera {} pares de pregunta-respuesta útiles para troubleshooting, configuración y uso. "
        "Devuelve solo un array JSON con objetos {{'prompt':..., 'completion':...}}.\n\n".format(n_examples)
        + text[:4000]  # Limita el tamaño para el LLM
    )
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    data = {
        "messages": [
            {"role": "system", "content": "Eres un experto en DevOps y troubleshooting. Ademas Eres un agente de IA con contexto de la entidad Mapfre y su proyecto interno 'mawdy', dedicado a cloud y aplicaciones. Ayudaras a generar preguntas y respuestas basadas en el contenido proporcionado."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
        "top_p": 0.9,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None,
    }
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        # Extraer array JSON del contenido
        start = content.find("[")
        end = content.rfind("]") + 1
        if start != -1 and end != -1:
            arr = json.loads(content[start:end])
            return arr
        else:
            print("[DEBUG] Respuesta LLM sin array JSON detectado:")
            print(content)
    except Exception as e:
        print(f"Error LLM: {e}")
        try:
            print("[DEBUG] Respuesta cruda del modelo:")
            print(response.text)
        except Exception:
            pass
    return []

def collect_dataset_llm(root):

    dataset = []
    patterns = ["**/*.md", "**/*.yaml", "**/*.yml", "**/*.json", "**/*.conf", "**/*.sh", "**/jenkins*", "**/Jenkinsfile*"]
    for pattern in patterns:
        for filepath in glob(os.path.join(root, pattern), recursive=True):
            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                fragment_size = 12000
                fragments = [text[i:i+fragment_size] for i in range(0, len(text), fragment_size)]
                total_dpo = []
                for idx, fragment in enumerate(fragments):
                    n_examples = 10
                    prompt = (
                        f"Eres un agente de IA con contexto de la entidad Mapfre y su proyecto interno 'mawdy', dedicado a cloud y aplicaciones. "
                        "El entorno incluye clusters Kubernetes en AWS y Oracle, bases de datos gestionadas, Azure Batch, pipelines CI/CD, infraestructura como código (IaC), y otros servicios cloud. Ayudaras a generar preguntas y respuestas basadas en el contenido proporcionado."
                        f"Analiza el siguiente archivo ({os.path.basename(filepath)}) y genera {n_examples} ejemplos en formato Azure OpenAI DPO. "
                        "Cada ejemplo debe tener:\n"
                        "- input.messages: pregunta o tarea relevante sobre el contenido\n"
                        "- preferred_output: respuesta correcta y razonada\n"
                        "- non_preferred_output: respuesta menos adecuada o incompleta\n"
                        "Devuelve solo un array JSON con objetos en ese formato.\n\n"
                        + fragment
                    )
                    headers = {
                        "Content-Type": "application/json",
                        "api-key": AZURE_OPENAI_KEY
                    }
                    data = {
                        "messages": [
                            {"role": "system", "content": "Eres un experto en DevOps, cloud, CI/CD, IaC y troubleshooting. tienes contexto sobre Mapfre y su proyecto mawdy. de cloud azure, k8s, pipelines, oracle y demas. Ayudaras a generar preguntas y respuestas basadas en el contenido proporcionado."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 2048,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "stop": None,
                    }
                    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"
                    try:
                        response = requests.post(url, headers=headers, json=data)
                        response.raise_for_status()
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        if content.strip().startswith("```json"):
                            content = content.strip()[7:]
                        if content.strip().endswith("```"):
                            content = content.strip()[:-3]
                        start = content.find("[")
                        end = content.rfind("]") + 1
                        if start != -1 and end != -1 and content[end-1] == "]":
                            try:
                                arr = json.loads(content[start:end])
                            except Exception as e:
                                print(f"[ERROR] No se pudo parsear el array JSON: {e}\n{content[start:end][:500]}")
                                with open("llm_errors.log", "a", encoding="utf-8") as logf:
                                    logf.write(f"--- Error en {filepath} fragmento {idx+1} ---\n")
                                    logf.write(f"Error: {e}\n")
                                    logf.write(content[start:end])
                                    logf.write("\n\n")
                                arr = []
                            for example in arr:
                                if "input.messages" in example:
                                    dpo_item = {
                                        "input": {"messages": example["input.messages"]},
                                        "preferred_output": example.get("preferred_output", ""),
                                        "non_preferred_output": example.get("non_preferred_output", "")
                                    }
                                else:
                                    try:
                                        dpo_item = to_direct_preference(example)
                                    except Exception as e:
                                        print(f"[ERROR] Ejemplo mal formateado, ignorado: {e}\n{example}")
                                        continue
                                if ("input" in dpo_item and "messages" in dpo_item["input"] and dpo_item["preferred_output"] and dpo_item["non_preferred_output"]):
                                    total_dpo.append(dpo_item)
                                else:
                                    print(f"[ERROR] Ejemplo incompleto, ignorado: {dpo_item}")
                        else:
                            print(f"[ERROR] Array JSON incompleto o mal formado en {filepath} fragmento {idx+1}")
                            print(content)
                            with open("llm_errors.log", "a", encoding="utf-8") as logf:
                                logf.write(f"--- Array incompleto en {filepath} fragmento {idx+1} ---\n")
                                logf.write(content)
                                logf.write("\n\n")
                    except Exception as e:
                        print(f"Error LLM en {filepath} fragmento {idx+1}: {e}")
                        try:
                            print("[DEBUG] Respuesta cruda del modelo:")
                            print(response.text)
                        except Exception:
                            pass
                dataset.extend(total_dpo)
                print(f"Procesado archivo: {filepath} -> {len(total_dpo)} ejemplos (total)")
            except Exception as e:
                print(f"Error procesando {filepath}: {e}")
    return dataset


if __name__ == "__main__":
    # Verificar datos de conexión
    if ("<TU_ENDPOINT_AQUI>" in AZURE_OPENAI_ENDPOINT or
        "<TU_API_KEY_AQUI>" in AZURE_OPENAI_KEY or
        "<TU_DEPLOYMENT_AQUI>" in AZURE_OPENAI_DEPLOYMENT):
        print("[ERROR] Faltan datos de conexión de Azure OpenAI. Configura las variables de entorno AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY y AZURE_OPENAI_DEPLOYMENT.")
        exit(1)

    # Convertir ruta raíz a WSL
    REPOS_ROOT_WSL = windows_to_wsl_path(REPOS_ROOT)
    # Listar subrepositorios
    subrepos = [d for d in os.listdir(REPOS_ROOT_WSL) if os.path.isdir(os.path.join(REPOS_ROOT_WSL, d))]
    processed_file = os.path.join(REPOS_ROOT_WSL, "processed_repos.txt")
    processed_repos = set()
    if os.path.exists(processed_file):
        with open(processed_file, "r", encoding="utf-8") as pf:
            processed_repos = set([line.strip() for line in pf if line.strip()])

    def is_yes(resp):
        return resp in {"s", "si", "sí", "y", "yes", "ok"}

    # Preguntar si procesar todos los subrepos de golpe
    resp_all = input("¿Procesar todos los subrepositorios de golpe sin confirmaciones? (s/n): ").strip().lower()
    process_all = is_yes(resp_all)

    def to_direct_preference(example):
        # Convierte a formato DPO estructurado y fuerza que todos los 'content' sean string
        def clean_content(val):
            import re
            # Recursively deserializa y extrae solo texto plano
            def extract_text(v):
                # Si es dict y tiene 'content', navega recursivamente
                if isinstance(v, dict):
                    if 'content' in v:
                        return extract_text(v['content'])
                    # Si tiene 'messages', busca el primer mensaje de usuario
                    if 'messages' in v:
                        for msg in v['messages']:
                            if msg.get('role') == 'user' and 'content' in msg:
                                return extract_text(msg['content'])
                        # Si no, busca el primer 'content' en cualquier mensaje
                        for msg in v['messages']:
                            if 'content' in msg:
                                return extract_text(msg['content'])
                    # Si no, busca el primer string en los valores
                    for vv in v.values():
                        t = extract_text(vv)
                        if isinstance(t, str):
                            return t
                # Si es lista, busca el primer string en los elementos
                if isinstance(v, list):
                    for item in v:
                        t = extract_text(item)
                        if isinstance(t, str):
                            return t
                # Si es string, limpia y devuelve
                if isinstance(v, str):
                    s = v.strip().replace("'", '"').replace('\\"', '"').replace('\"', '"').replace('\\', '')
                    # Intenta deserializar si parece JSON
                    try:
                        obj = json.loads(s)
                        return extract_text(obj)
                    except Exception:
                        pass
                    # Regex para extraer texto si está envuelto
                    match = re.search(r"content[\"']?\s*[:=]\s*[\"']([^\"']+)[\"']", s)
                    if match:
                        return match.group(1)
                    return s.strip('"\'` ')
                return v
            return extract_text(val)

        input_text = example.get("prompt") or example.get("input")
        preferred_output = example.get("completion") or example.get("preferred_output") or ""
        non_preferred_output = example.get("non_preferred_output") or preferred_output
        return {
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Eres un agente de IA experto en DevOps, cloud y automatización, dedicado a ayudar a los equipos técnicos de Mapfre Mawdy (Mapfre, proyecto interno orientado a cloud y aplicaciones). "
                            "Tu objetivo es resolver dudas, guiar en troubleshooting, recomendar buenas prácticas y facilitar la configuración de servicios como Azure, Kubernetes, Oracle, CI/CD y IaC. "
                            "Responde siempre de forma clara, profesional y razonada, explicando los pasos y justificando tus recomendaciones. Si la pregunta es ambigua, pide detalles. Evita respuestas genéricas y prioriza la utilidad práctica."
                            "Intenta siempre contextualizar las respuestas al entorno de Mapfre y su proyecto Mawdy de lo que tengas fine tuned, incluyendo referencias si puedes a documentacion interna"
                        )
                    },
                    {
                        "role": "user",
                        "content": clean_content(input_text)
                    }
                ]
            },
            "preferred_output": [
                {
                    "role": "assistant",
                    "content": clean_content(preferred_output)
                }
            ],
            "non_preferred_output": [
                {
                    "role": "assistant",
                    "content": clean_content(non_preferred_output)
                }
            ]
        }

    total = 0
    print("\n==============================")
    print(" Generador de Dataset DPO para Azure OpenAI")
    print("==============================")
    print(f"Ruta de salida del dataset: {OUTPUT_FILE}")
    print(f"Procesando subrepositorios en: {REPOS_ROOT_WSL}")
    print(f"Archivo de control de repositorios procesados: {processed_file}")
    print("\n[INFO] El archivo 'processed_repos.txt' almacena los nombres de los subrepositorios ya analizados.")
    print("Si quieres volver a analizar un subrepo, bórralo manualmente de ese archivo antes de ejecutar el script.")
    print("------------------------------\n")
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f, open(processed_file, "a", encoding="utf-8") as pf:
        for idx, subrepo in enumerate(subrepos):
            subrepo_path = os.path.join(REPOS_ROOT_WSL, subrepo)
            print(f"\n[Subrepo {idx+1}/{len(subrepos)}] {subrepo_path}")
            if subrepo in processed_repos:
                print(f"[PROGRESO] Ya procesado: {subrepo} ({idx+1}/{len(subrepos)})")
                continue
            if not process_all:
                resp = input(f"¿Procesar esta carpeta? (s/n/si/yes/ok): ").strip().lower()
                if not is_yes(resp):
                    print(f"Saltando carpeta: {subrepo}")
                    continue
            subrepo_dataset = collect_dataset_llm(subrepo_path)
            for item in subrepo_dataset:
                try:
                    dpo_item = to_direct_preference(item)
                    f.write(json.dumps(dpo_item, ensure_ascii=False) + "\n")
                except Exception as e:
                    print(f"[ERROR] No se pudo guardar un ejemplo por error de JSON: {e}\nEjemplo: {item}")
            print(f"Guardados {len(subrepo_dataset)} ejemplos de {subrepo}")
            total += len(subrepo_dataset)
            print(f"Ejemplos añadidos al dataset.jsonl. Total actual: {total}")
            pf.write(subrepo + "\n")
            pf.flush()
            if not process_all:
                cont = input("¿Continuar con la siguiente carpeta? (s/n/si/yes/ok): ").strip().lower()
                if not is_yes(cont):
                    print("Proceso interrumpido por el usuario.")
                    break
            print(f"[PROGRESO] Repositorios procesados: {len(processed_repos)+idx+1} / {len(subrepos)}")
        # Añadir ejemplos manuales del agente al final
        manual_examples = [
            {
                "prompt": "¿Cómo instalo el agente IA en Linux?",
                "completion": "Ejecuta: curl -O https://raw.githubusercontent.com/v4mpir0ck/agent-linux/main/instalar_agente.sh && chmod +x instalar_agente.sh && ./instalar_agente.sh"
            },
            {
                "prompt": "¿Qué hace el comando 'red'?",
                "completion": "Muestra la configuración de red actual usando el comando 'ip a'."
            },
            {
                "prompt": "¿Cómo edito los ficheros de configuración del agente?",
                "completion": "Puedes editar los ficheros en la carpeta agente/ con cualquier editor de texto, por ejemplo 'nano agente/config.yaml'."
            },
            {
                "prompt": "¿Cómo entrenar el agente con una base de conocimientos propia?",
                "completion": "Prepara un dataset en formato JSONL y realiza el fine-tuning en Azure OpenAI siguiendo la documentación oficial."
            },
            {
                "prompt": "¿Cómo se encripta el token del agente?",
                "completion": "Utiliza el script 'encrypt_token.py' en la carpeta agente/ para encriptar el token y guardarlo como 'azure_openai_token.enc'."
            }
        ]
        for item in manual_examples:
            try:
                dpo_item = to_direct_preference(item)
                f.write(json.dumps(dpo_item, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"[ERROR] No se pudo guardar un ejemplo manual por error de JSON: {e}\nEjemplo: {item}")
        print(f"Guardados {len(manual_examples)} ejemplos manuales")
        print("\n==============================")
        print(" Dataset DPO generado correctamente")
        print("------------------------------")
        print(f"Archivo: {OUTPUT_FILE}")
        print(f"Total de ejemplos: {total + len(manual_examples)}")
        print("Formato: DPO estructurado (Azure OpenAI)")
        print("==============================\n")

import requests
import os

# Configuración Azure AI Foundry
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "8zKFs1zJ1el0qP7er2oHsKusPGieAZERSUiTHACifNQ844TfNX1oJQQJ99BHACYeBjFXJ3w3AAABACOGJckA")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://agent-linux.openai.azure.com/")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

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

# Ejemplo de uso:
if __name__ == "__main__":
    prompt = "¿Cuál es el hostname actual de este sistema Linux?"
    print(query_llm(prompt))

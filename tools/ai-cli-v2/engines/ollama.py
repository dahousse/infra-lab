import requests

OLLAMA_URL = "http://192.168.1.10:11434/api/generate"
DEFAULT_MODEL = "phi3:mini"


def ask_ollama(prompt, model=DEFAULT_MODEL):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=300)
    r.raise_for_status()

    return r.json().get("response", "")
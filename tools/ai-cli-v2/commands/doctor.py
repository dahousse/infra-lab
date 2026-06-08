import requests
from core.config import load_config

def run():
    cfg = load_config()
    endpoint = cfg["endpoint"]

    print("\n🧠 DOCTOR\n")

    try:
        r = requests.get(f"{endpoint}/api/tags", timeout=5)
        r.raise_for_status()
        print("✔ Ollama OK")
    except Exception as e:
        print("❌ Ollama FAIL")
        print(e)
        return

    models = r.json().get("models", [])
    print(f"Models: {len(models)}")

    for m in models:
        print(" -", m["name"])

from core.config import load_config
import requests

def run():
    cfg = load_config()
    endpoint = cfg["endpoint"]

    r = requests.get(f"{endpoint}/api/tags", timeout=5)
    r.raise_for_status()

    models = r.json().get("models", [])

    print("\n📦 Models\n")

    for m in models:
        print("-", m["name"])

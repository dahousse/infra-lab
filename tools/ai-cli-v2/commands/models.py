from core.client import OllamaClient
from core.config import load_config

def run():
    cfg = load_config()
    client = OllamaClient(cfg["endpoint"])

    data = client.models()

    print("\n📦 Models disponibles:\n")

    for m in data.get("models", []):
        print(f"- {m['name']}")

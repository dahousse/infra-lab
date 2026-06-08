import requests
from core.config import load_config
from utils.output import ok, error

def run():
    cfg = load_config()
    endpoint = cfg["endpoint"]

    print("\n🧠 DOCTOR\n")

    try:
        r = requests.get(f"{endpoint}/api/tags", timeout=5)
        r.raise_for_status()
        ok("Ollama reachable")
    except Exception as e:
        error("Ollama unreachable")
        print(e)
        return

    models = r.json().get("models", [])
    ok(f"Models OK ({len(models)})")

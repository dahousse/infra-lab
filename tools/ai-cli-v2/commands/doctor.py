import requests
from core.config import load_config

def run():
    cfg = load_config()
    endpoint = cfg["endpoint"]

    try:
        r = requests.get(f"{endpoint}/api/tags", timeout=5)
        r.raise_for_status()

        models = r.json().get("models", [])

        return {
            "status": "ok",
            "models_count": len(models),
            "models": [m["name"] for m in models]
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

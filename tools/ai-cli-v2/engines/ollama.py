"""Ollama LLM engine — appelle le vrai model."""

from core.client import OllamaClient
from core.config import load_config


def ask(prompt: str) -> dict:
    """Envoie le prompt à Ollama et retourne la réponse."""
    cfg = load_config()
    endpoint = cfg.get("endpoint", "http://192.168.1.10:11434")
    model = cfg.get("default_model", "phi3:mini")
    timeout = cfg.get("timeout", 60)

    client = OllamaClient(endpoint)

    try:
        response = client.generate(model, prompt, timeout)
        return {
            "response": response,
            "model": model,
        }
    except Exception as e:
        return {
            "response": f"[Ollama error] {e}",
            "model": model,
            "error": str(e),
        }


def list_models() -> dict:
    """Liste les modèles disponibles sur Ollama."""
    cfg = load_config()
    endpoint = cfg.get("endpoint", "http://192.168.1.10:11434")

    client = OllamaClient(endpoint)

    try:
        data = client.models()
        models = [m["name"] for m in data.get("models", [])]
        return {"models": models, "count": len(models)}
    except Exception as e:
        return {"error": str(e), "models": []}

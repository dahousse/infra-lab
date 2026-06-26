"""Ollama engine — calls the Ollama API"""

import json
from core.client import OllamaClient
from core.config import load_config


_config_cache = None


def _get_client():
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return OllamaClient(_config_cache["endpoint"]), _config_cache


def ask(prompt: str) -> dict:
    """Ask Ollama a question"""
    client, cfg = _get_client()
    model = cfg.get("default_model", "qwen2.5-coder:7b")

    if not isinstance(prompt, str):
        prompt = str(prompt)

    try:
        response = client.generate(model, prompt)
        return {
            "response": response,
            "model": model
        }
    except Exception as e:
        return {
            "error": str(e),
            "model": model
        }


def list_models() -> dict:
    """List available Ollama models"""
    client, _ = _get_client()
    try:
        data = client.models()
        return {
            "models": [m["name"] for m in data.get("models", [])]
        }
    except Exception as e:
        return {
            "error": str(e)
        }

from core.client import OllamaClient
from core.config import load_config

def run(prompt, model=None):
    cfg = load_config()

    client = OllamaClient(cfg["endpoint"])
    model = model or cfg["default_model"]

    return client.generate(model, prompt)

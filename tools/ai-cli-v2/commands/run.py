from core.client import OllamaClient
from core.config import load_config

def run(prompt):
    cfg = load_config()
    client = OllamaClient(cfg["endpoint"])

    model = cfg.get("default_model", "phi3:mini")

    return client.generate(model, prompt)

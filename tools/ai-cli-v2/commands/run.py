from core.client import OllamaClient
from core.config import load_config

def run(args):

    cfg = load_config()
    client = OllamaClient(cfg["endpoint"])

    model = cfg.get("default_model", "phi3:mini")

    if not args.strip():
        return "Empty prompt"

    tokens = args.split()

    if "-m" in tokens:
        i = tokens.index("-m")
        model = tokens[i + 1]
        tokens = tokens[:i] + tokens[i+2:]

    elif "--model" in tokens:
        i = tokens.index("--model")
        model = tokens[i + 1]
        tokens = tokens[:i] + tokens[i+2:]

    prompt = " ".join(tokens)

    return client.generate(model, prompt)

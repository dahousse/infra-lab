from core.client import OllamaClient
from core.config import load_config
from utils import output

def run(args):
    cfg = load_config()
    client = OllamaClient(cfg["endpoint"])

    default_model = cfg.get("default_model", "phi3:mini")

    if not args or args.strip() == "":
        output.error("Empty prompt")
        return None

    model = default_model
    tokens = args.split()

    if "-m" in tokens:
        i = tokens.index("-m")
        if i + 1 < len(tokens):
            model = tokens[i + 1]
            tokens = tokens[:i] + tokens[i+2:]

    elif "--model" in tokens:
        i = tokens.index("--model")
        if i + 1 < len(tokens):
            model = tokens[i + 1]
            tokens = tokens[:i] + tokens[i+2:]

    prompt = " ".join(tokens).strip()

    if not prompt:
        output.error("Empty prompt")
        return None

    return client.generate(model, prompt)

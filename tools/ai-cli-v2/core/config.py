import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.yaml"

def load_config():
    default = {
        "endpoint": "http://localhost:11434",
        "default_model": "phi3:mini"
    }

    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                cfg = yaml.safe_load(f)

            if isinstance(cfg, dict):
                return {**default, **cfg}

    except Exception:
        pass

    return default

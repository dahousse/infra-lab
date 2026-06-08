from pathlib import Path
import yaml

# 🔥 bon niveau = ai-cli-v2/
BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

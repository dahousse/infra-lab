from pathlib import Path
import yaml
from core.errors import ConfigError

DEFAULT_PATHS = [
    Path("./config/config.yaml"),
    Path.home() / ".config/ai-cli/config.yaml",
    Path("/etc/ai-cli/config.yaml"),
]

def load_config():
    for path in DEFAULT_PATHS:
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f)

    raise ConfigError(f"No config found in: {DEFAULT_PATHS}")

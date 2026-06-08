class AIError(Exception):
    pass


class ConfigError(AIError):
    pass


class OllamaConnectionError(AIError):
    pass

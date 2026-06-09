def build_plan(intent: dict):
    if intent["type"] == "infra.vm":
        return {
            "engine": "vm",
            "action": "create_vm",
            "params": intent
        }

    if intent["type"] == "infra.terraform":
        return {
            "engine": "terraform",
            "action": "apply",
            "params": intent
        }

    return {
        "engine": "ollama",
        "action": "chat",
        "params": intent
    }
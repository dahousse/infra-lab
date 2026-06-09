def build_plan(intent: dict) -> dict:
    if intent["type"] == "infra.vm":
        return {
            "engine": "vm",
            "action": "create_vm",
            "params": intent
        }

    if intent["type"] == "infra.container":
        return {
            "engine": "docker",
            "action": "run_container",
            "params": intent
        }

    return {
        "engine": "ollama",
        "action": "chat",
        "params": intent
    }
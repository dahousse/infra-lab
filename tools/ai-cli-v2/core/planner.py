"""Plan builder — maps intent to engine + action"""

def build_plan(intent: dict) -> dict:
    intent_type = intent.get("type", "unknown")

    if intent_type in ("infra.vm.create", "infra.vm"):
        return {
            "engine": "vm",
            "action": "create_vm",
            "params": intent
        }

    if intent_type == "infra.vm.list":
        return {
            "engine": "vm",
            "action": "list_vm",
            "params": intent
        }

    if intent_type == "infra.vm.delete":
        return {
            "engine": "vm",
            "action": "delete_vm",
            "params": intent
        }

    if intent_type == "infra.container":
        return {
            "engine": "docker",
            "action": "run_container",
            "params": intent
        }

    # Fallback: chat with Ollama
    return {
        "engine": "ollama",
        "action": "chat",
        "params": intent
    }

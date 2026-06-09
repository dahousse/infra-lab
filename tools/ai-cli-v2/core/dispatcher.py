from engines.vm import create_vm
from engines.ollama import ask

def dispatch(plan: dict):
    engine = plan.get("engine", "ollama")

    if engine == "vm":
        return create_vm(plan)

    if engine == "docker":
        return "[DOCKER] not implemented yet"

    return ask(str(plan))
from engines.vm import create_vm
from engines.ollama import ask
from utils.output_layer import wrap


def dispatch(plan: dict):
    engine = plan.get("engine", "ollama")

    if engine == "vm":
        result = create_vm(plan)
        return wrap("vm", result)

    if engine == "docker":
        return wrap("docker", {"message": "not implemented yet"})

    try:
        result = ask(str(plan))
        return wrap("ollama", result)
    except Exception as e:
        return wrap("ollama", error=str(e))
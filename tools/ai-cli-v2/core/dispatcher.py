from engines.vm import create_vm
from engines.terraform import apply_terraform
from engines.ollama import ask_ollama


def dispatch(plan: dict):
    engine = plan["engine"]
    params = plan["params"]

    if engine == "vm":
        return create_vm(params)

    if engine == "terraform":
        return apply_terraform(params)

    if engine == "ollama":
        return ask_ollama(params["raw"])

    return f"[ERROR] Unknown engine: {engine}"
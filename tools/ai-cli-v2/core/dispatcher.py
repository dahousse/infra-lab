"""Dispatcher — aiguille le plan vers le bon engine."""

from engines.vm import create_vm
from engines.ollama import ask, list_models
from utils_ai.output_layer import wrap


def dispatch(plan: dict, prompt: str = ""):
    """Route le plan vers l'engine approprié.

    Args:
        plan: Dictionnaire contenant engine, action, params.
        prompt: Le prompt original de l'utilisateur (passé aux engines LLM).
    """
    engine = plan.get("engine", "ollama")
    action = plan.get("action", "")

    # --- Ollama : liste des modèles ---
    if engine == "ollama" and action == "list_models":
        try:
            result = list_models()
            return wrap("ollama", result)
        except Exception as e:
            return wrap("ollama", error=str(e))

    # --- VM / Terraform ---
    if engine == "vm":
        result = create_vm(plan, prompt)
        return wrap("vm", result)

    # --- Docker ---
    if engine == "docker":
        return wrap("docker", {"message": "not implemented yet"})

    # --- Proxmox ---
    if engine == "proxmox":
        from engines.proxmox import handle
        try:
            result = handle(plan, prompt)
            return wrap("proxmox", result)
        except Exception as e:
            return wrap("proxmox", error=str(e))

    # --- Fallback : parler à Ollama ---
    try:
        result = ask(prompt)
        return wrap("ollama", result)
    except Exception as e:
        return wrap("ollama", error=str(e))

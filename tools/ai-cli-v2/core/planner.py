"""Planner — transforme une intention en plan d'exécution."""


def build_plan(intent: dict) -> dict:
    """Construit un plan (engine + action + params) à partir de l'intention."""

    # --- VMs / Terraform ---
    if intent["type"] == "infra.vm":
        return {
            "engine": "vm",
            "action": "create_vm",
            "params": intent,
        }

    # --- Proxmox (list, status, start, stop, create) ---
    if intent["type"] == "infra.proxmox":
        return {
            "engine": "proxmox",
            "action": intent.get("action", "list"),
            "target": intent.get("target", "vms"),
            "params": intent,
        }

    # --- Containers Docker ---
    if intent["type"] == "infra.container":
        return {
            "engine": "docker",
            "action": "run_container",
            "params": intent,
        }

    # --- Ollama models ---
    if intent["type"] == "ollama.models":
        return {
            "engine": "ollama",
            "action": "list_models",
            "params": intent,
        }

    # --- Chat / fallback Ollama ---
    return {
        "engine": "ollama",
        "action": "chat",
        "params": intent,
    }

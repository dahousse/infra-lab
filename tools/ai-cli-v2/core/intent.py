"""Analyse le prompt pour extraire l'intention."""


def extract_intent(prompt: str) -> dict:
    """Extrait une intention structurée depuis un prompt en langage naturel."""
    p = prompt.lower().strip()

    # --- Proxmox / Infrastructure ---
    if any(w in p for w in ["proxmox", "pve", "hyperviseur", "vm ", "vms", "lxc", "ct ",
                            "conteneur", "conteneurs"]):
        action = "list"
        if any(w in p for w in ["status", "état", "état"]):
            action = "status"
        if any(w in p for w in ["start", "démarre", "allume"]):
            action = "start"
        if any(w in p for w in ["stop", "arrête", "éteint"]):
            action = "stop"
        if any(w in p for w in ["créer", "crée", "create", "nouveau"]):
            action = "create"

        target = "vms"
        if any(w in p for w in ["ct", "lxc", "conteneur"]):
            target = "containers"

        return {
            "type": "infra.proxmox",
            "action": action,
            "target": target,
            "provider": "proxmox",
        }

    # --- VM (Terraform) ---
    if any(w in p for w in ["créer une vm", "crée une vm", "create vm", "nouvelle vm", "deploy vm"]):
        return {
            "type": "infra.vm",
            "action": "create",
            "target": "vm",
            "tools": ["docker"] if "docker" in p else [],
            "provider": "proxmox",
        }

    # --- Docker (pas LXC/Proxmox) ---
    if "docker" in p:
        return {
            "type": "infra.container",
            "action": "run",
            "target": "docker",
            "tools": [],
            "provider": "local",
        }

    # --- Modèles Ollama ---
    if any(w in p for w in ["modèle", "modèle", "model", "ollama"]):
        if any(w in p for w in ["liste", "list", "quels"]):
            return {"type": "ollama.models", "action": "list"}

    # --- Chat par défaut ---
    return {
        "type": "unknown",
        "action": "chat",
    }

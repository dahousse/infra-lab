def extract_intent(prompt: str) -> dict:
    p = prompt.lower()

    if "vm" in p or "ubuntu" in p:
        return {
            "type": "infra.vm",
            "action": "create",
            "target": "ubuntu",
            "tools": ["docker"] if "docker" in p else [],
            "provider": "proxmox"
        }

    if "docker" in p:
        return {
            "type": "infra.container",
            "action": "run",
            "target": "docker",
            "tools": [],
            "provider": "local"
        }

    return {
        "type": "unknown",
        "action": "chat"
    }
def extract_intent(prompt: str):
    p = prompt.lower()

    # 🧠 VM INTENT
    if any(k in p for k in ["vm", "virtual machine"]):
        return {
            "type": "infra.vm",
            "action": "create",
            "target": "ubuntu",
            "tools": ["docker"] if "docker" in p else [],
            "provider": "proxmox",
            "raw": prompt
        }

    # 🧠 TERRAFORM INTENT
    if "terraform" in p:
        return {
            "type": "infra.terraform",
            "action": "apply",
            "raw": prompt
        }

    # 🤖 DEFAULT LLM
    return {
        "type": "llm.chat",
        "action": "generate",
        "raw": prompt
    }
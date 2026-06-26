"""Intent extraction — parse user prompt to structured intent"""

def extract_intent(prompt: str) -> dict:
    p = prompt.lower().strip()
    
    # Lister les VMs
    if p in ("list vms", "ls vm", "vms", "list", "show vms", "show vm"):
        return {
            "type": "infra.vm.list",
            "action": "list_vm",
        }

    # Créer/Cloner une VM : "create vm test-906" ou "clone vm 906"
    is_create = any(kw in p for kw in ("create vm", "clone vm", "new vm", "add vm", "creer vm"))
    
    if is_create:
        intent = {
            "type": "infra.vm.create",
            "action": "create_vm",
            "method": "clone",
            "template_id": 102,
        }
        
        # Extraire le nom: "create vm test-906" → name=test-906
        words = p.split()
        for i, w in enumerate(words):
            if w == "vm" and i + 1 < len(words):
                intent["name"] = words[i + 1]
        
        # Extraire template: avec --template 101 ou template=101
        for i, w in enumerate(words):
            if w in ("--template", "-t", "--from", "template", "from") and i + 1 < len(words):
                try:
                    intent["template_id"] = int(words[i + 1])
                except ValueError:
                    pass
        
        # Extraire CPU: --cpus 2 ou cpus=2
        for i, w in enumerate(words):
            if w in ("--cpus", "-c", "cpus") and i + 1 < len(words):
                try:
                    intent["cpus"] = int(words[i + 1])
                except ValueError:
                    pass
        
        # Extraire RAM: --memory 2048 ou ram=2048  
        for i, w in enumerate(words):
            if w in ("--memory", "-m", "memory", "ram") and i + 1 < len(words):
                try:
                    intent["memory"] = int(words[i + 1])
                except ValueError:
                    pass
        
        # Extraire VM ID: --id 906 ou id=906
        for i, w in enumerate(words):
            if w in ("--id", "--vm-id", "id") and i + 1 < len(words):
                try:
                    intent["vm_id"] = int(words[i + 1])
                except ValueError:
                    pass
        
        # Traefik: --domain xxx --port 80
        for i, w in enumerate(words):
            if w in ("--domain", "-d", "domain") and i + 1 < len(words):
                intent["traefik_domain"] = words[i + 1]
            if w in ("--port", "-p", "port") and i + 1 < len(words):
                intent["traefik_port"] = words[i + 1]
        
        # No ansible? --no-ansible
        if "--no-ansible" in words or "noansible" in words:
            intent["auto_ansible"] = False
        
        # Groupe: --group supervision
        for i, w in enumerate(words):
            if w in ("--group", "-g", "group") and i + 1 < len(words):
                intent["group"] = words[i + 1]
        
        return intent
    
    # Stop VM
    is_stop = any(kw in p for kw in ("stop vm", "delete vm", "destroy vm", "remove vm", "kill vm"))
    if is_stop:
        words = p.split()
        intent = {"type": "infra.vm.delete", "action": "delete_vm"}
        for i, w in enumerate(words):
            if w in ("vm", "--id", "id") and i + 1 < len(words):
                try:
                    intent["vm_id"] = int(words[i + 1])
                except ValueError:
                    pass
            if w == "vm" and i + 1 < len(words):
                name = words[i + 1]
                if not name.startswith("--"):
                    intent["name"] = name
        return intent

    # Docker
    if any(kw in p for kw in ("docker", "container", "lxc")):
        return {
            "type": "infra.container",
            "action": "run_container",
            "tools": [],
            "provider": "local"
        }
    
    # Help / Doctor / System / Models — handled by commands

    # Fallback: chat with Ollama
    return {
        "type": "unknown",
        "action": "chat"
    }

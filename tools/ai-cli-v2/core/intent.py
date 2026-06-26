"""Intent extraction — parse user prompt to structured intent"""

def extract_intent(prompt: str) -> dict:
    p = prompt.lower().strip()

    # ── List VMs ──
    if p in ("list vms", "list vm", "ls vm", "ls vms", "vms", "vm list", "list",
             "show vms", "show vm", "lister", "afficher vms", "afficher vm"):
        return {
            "type": "infra.vm.list",
            "action": "list_vm",
        }

    # ── Status VM ──
    if p.startswith("status vm") or p in ("vm status", "vms status"):
        return {
            "type": "infra.vm.list",
            "action": "list_vm",
        }

    # ── Create / Clone VM ──
    is_create = any(kw in p for kw in ("create vm", "clone vm", "new vm", "add vm",
                                        "creer vm", "créer vm", "nouvelle vm", "make vm"))

    if is_create:
        intent = {
            "type": "infra.vm.create",
            "action": "create_vm",
            "method": "clone",
            "template_id": 102,
        }

        words = p.split()
        # Extraire le nom: "create vm test-906" → name=test-906
        for i, w in enumerate(words):
            if w == "vm" and i + 1 < len(words):
                candidate = words[i + 1]
                if not candidate.startswith("-"):
                    intent["name"] = candidate

        # Extraire template: --template 101 ou template=101
        for i, w in enumerate(words):
            if w in ("--template", "-t", "--from", "template", "from") and i + 1 < len(words):
                try:
                    intent["template_id"] = int(words[i + 1])
                except ValueError:
                    pass

        # Extraire CPU: --cpus 2 ou cpus=2
        for i, w in enumerate(words):
            if w in ("--cpus", "-c", "cpus", "--cores") and i + 1 < len(words):
                try:
                    intent["cpus"] = int(words[i + 1])
                except ValueError:
                    pass

        # Extraire RAM: --memory 2048 ou ram=2048
        for i, w in enumerate(words):
            if w in ("--memory", "-m", "memory", "ram", "--mem") and i + 1 < len(words):
                try:
                    intent["memory"] = int(words[i + 1])
                except ValueError:
                    pass

        # Extraire VM ID: --id 906 ou id=906
        for i, w in enumerate(words):
            if w in ("--id", "--vm-id", "id", "--vmid") and i + 1 < len(words):
                try:
                    intent["vm_id"] = int(words[i + 1])
                except ValueError:
                    pass

        # Traefik: --domain xxx --port 80
        for i, w in enumerate(words):
            if w in ("--domain", "-d", "domain") and i + 1 < len(words):
                intent["traefik_domain"] = words[i + 1]
            if w in ("--port", "-p", "port") and i + 1 < len(words):
                try:
                    intent["traefik_port"] = int(words[i + 1])
                except ValueError:
                    intent["traefik_port"] = words[i + 1]

        # No ansible?
        if "--no-ansible" in words or "noansible" in words or "--skip-ansible" in words:
            intent["auto_ansible"] = False

        # Groupe: --group supervision
        for i, w in enumerate(words):
            if w in ("--group", "-g", "group") and i + 1 < len(words):
                intent["group"] = words[i + 1]

        return intent

    # ── Destroy / Delete VM ──
    is_stop = any(kw in p for kw in ("stop vm", "delete vm", "destroy vm", "remove vm",
                                      "kill vm", "supprimer vm", "effacer vm"))
    if is_stop:
        words = p.split()
        intent = {"type": "infra.vm.delete", "action": "delete_vm"}
        for i, w in enumerate(words):
            if w in ("vm", "--id", "id", "--vmid") and i + 1 < len(words):
                candidate = words[i + 1]
                if not candidate.startswith("-"):
                    try:
                        intent["vm_id"] = int(candidate)
                    except ValueError:
                        intent["name"] = candidate
        return intent

    # ── Start VM ──
    if p.startswith("start vm") or p.startswith("demarrer vm"):
        words = p.split()
        intent = {"type": "infra.vm.start", "action": "start_vm"}
        for i, w in enumerate(words):
            if w in ("vm", "--id", "id") and i + 1 < len(words):
                candidate = words[i + 1]
                if not candidate.startswith("-"):
                    try:
                        intent["vm_id"] = int(candidate)
                    except ValueError:
                        intent["name"] = candidate
        return intent

    # ── Plan VM (Terraform preview) ──
    if "plan" in p and ("vm" in p or "infra" in p or "create" in p):
        return {
            "type": "infra.vm.plan",
            "action": "plan_vm",
        }

    # ── Docker / Container ──
    if any(kw in p for kw in ("docker", "container", "lxc", "conteneur")):
        return {
            "type": "infra.container",
            "action": "run_container",
            "tools": [],
            "provider": "local"
        }

    # ── Help / Doctor / System / Models — handled by commands

    # Fallback: chat with Ollama
    return {
        "type": "unknown",
        "action": "chat"
    }

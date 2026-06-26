"""Proxmox engine — interroge et pilote l'hyperviseur via SSH."""

import subprocess
import json
import re

PROXMOX_HOST = "192.168.1.1"
SSH = ["ssh", f"root@{PROXMOX_HOST}"]


def _run(cmd: list[str]) -> str:
    """Exécute une commande sur le host Proxmox via SSH."""
    full_cmd = SSH + cmd
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def list_vms() -> list[dict]:
    """Liste toutes les VMs/QEMU avec leur statut."""
    out = _run(["qm", "list"])
    lines = out.strip().splitlines()

    if len(lines) < 2:
        return []

    vms = []
    for line in lines[1:]:  # skip header
        parts = line.split()
        if len(parts) >= 3:
            vms.append({
                "vmid": parts[0],
                "name": parts[1],
                "status": parts[2],
                "mem": parts[3] if len(parts) > 3 else "?",
                "bootdisk": parts[4] if len(parts) > 4 else "?",
            })
    return vms


def vm_status(vmid: str) -> dict:
    """Statut détaillé d'une VM."""
    out = _run(["qm", "status", vmid])
    return dict(line.split(": ", 1) for line in out.strip().splitlines() if ": " in line)


def list_containers() -> list[dict]:
    """Liste tous les conteneurs LXC."""
    out = _run(["pct", "list"])
    lines = out.strip().splitlines()

    if len(lines) < 2:
        return []

    ct = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 3:
            ct.append({
                "vmid": parts[0],
                "status": parts[1],
                "name": parts[2] if len(parts) > 2 else "?",
            })
    return ct


def handle(plan: dict, prompt: str = "") -> dict:
    """Point d'entrée : route la commande Proxmox selon l'intention."""
    p = prompt.lower()

    # 1. Status spécifique d'une VM (vmid dans le prompt)
    has_vmid = re.search(r"\b(\d{3,4})\b", prompt)
    if has_vmid and any(w in p for w in ["status", "état", "etat"]):
        return {"vm_status": vm_status(has_vmid.group(1))}

    # 2. Liste les conteneurs LXC
    if any(w in p for w in ["conteneur", "lxc", "ct "]):
        return {"containers": list_containers()}

    # 3. Status général (sans VMID)
    if any(w in p for w in ["status", "état", "etat"]):
        return {"vms": list_vms()}

    # 4. Liste les VMs
    if any(w in p for w in ["liste", "list", "vm ", "vms"]):
        return {"vms": list_vms()}

    # Fallback : liste les VMs
    return {"vms": list_vms()}

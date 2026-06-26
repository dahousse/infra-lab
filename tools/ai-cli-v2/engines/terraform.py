"""Terraform engine — crée des VMs via Terraform Proxmox."""

import subprocess
import json
import os
import re

TF_DIR = "/home/infra/infra-lab-tf"
TFVARS = os.path.join(TF_DIR, "terraform.tfvars")


def _run(cmd: list[str], cwd: str = TF_DIR) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r.stdout


def _read_tfvars() -> dict:
    """Lit les variables actuelles du fichier terraform.tfvars."""
    vars = {}
    if not os.path.exists(TFVARS):
        return vars
    with open(TFVARS) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                vars[k.strip()] = v.strip().strip('"')
    return vars


def _write_tfvars(vars: dict):
    """Écrit les variables dans terraform.tfvars."""
    # Préserver les variables non modifiées
    current = _read_tfvars()
    current.update(vars)

    # On fixe le clone_vm_id automatiquement si pas fourni
    if "clone_vm_id" not in current:
        current["clone_vm_id"] = _next_vm_id()

    with open(TFVARS, "w") as f:
        for k, v in current.items():
            # Ne pas écrire les valeurs vides
            if v == "" or v is None:
                continue
            f.write(f'{k} = "{v}"\n')


def _next_vm_id() -> str:
    """Trouve le prochain VMID disponible (max existant + 1)."""
    r = _run(["ssh", "root@192.168.1.1", "qm", "list"])
    vms = []
    for line in r.strip().splitlines()[1:]:
        parts = line.split()
        if parts:
            vms.append(int(parts[0]))
    r2 = _run(["ssh", "root@192.168.1.1", "pct", "list"])
    for line in r2.strip().splitlines()[1:]:
        parts = line.split()
        if parts:
            vms.append(int(parts[0]))
    if not vms:
        return "200"
    return str(max(vms) + 1)


def plan(prompt: str) -> dict:
    """Exécute terraform plan et retourne un résumé."""
    vars = _extract_vars(prompt)
    _write_tfvars(vars)

    out = _run(["terraform", "plan", "-no-color"])
    lines = out.strip().splitlines()

    # Extraire le résumé (dernières lignes)
    summary = [l for l in lines if "Plan:" in l or "to add" in l or "to change" in l or "to destroy" in l]
    return {
        "message": "Terraform plan exécuté",
        "summary": summary[-3:] if summary else lines[-5:],
        "variables": vars,
        "raw": out,
    }


def apply(prompt: str) -> dict:
    """Exécute terraform apply --auto-approve et retourne le résultat."""
    vars = _extract_vars(prompt)
    _write_tfvars(vars)

    out = _run(["terraform", "apply", "--auto-approve", "-no-color"])

    # Extraire l'IP et les infos de la VM
    ip_match = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", out)
    name_match = re.search(r"test-\d+", out)

    return {
        "message": "VM créée avec succès",
        "vm_name": name_match.group(0) if name_match else f"{vars.get('clone_prefix', 'vm')}-{vars.get('clone_vm_id', '?')}",
        "ip": ip_match[1:] if len(ip_match) > 1 else ip_match,  # skip first match if it's the API
        "variables": vars,
    }


def destroy(prompt: str = "") -> dict:
    """Détruit la VM courante."""
    vars = _read_tfvars()
    out = _run(["terraform", "destroy", "--auto-approve", "-no-color"])
    return {
        "message": "VM détruite",
        "vm_name": f"{vars.get('clone_prefix', 'vm')}-{vars.get('clone_vm_id', '?')}",
    }


def _extract_vars(prompt: str) -> dict:
    """Extrait les variables Terraform depuis le prompt utilisateur."""
    p = prompt.lower()
    vars = {}

    # Extraire le prefix et vm_id depuis un nom type "test-906" ou "vm-114"
    name_match = re.search(r"\b([a-z]+)[-:](\d{3})\b", p)
    if name_match:
        vars["clone_prefix"] = name_match.group(1)
        vars["clone_vm_id"] = name_match.group(2)
    else:
        # Extraire le prefix seul
        for w in p.split():
            if w.startswith("test") or w.startswith("app") or w.startswith("db"):
                vars["clone_prefix"] = w
                break

    # Extraire la RAM (en MB)
    ram_match = re.search(r"(\d+)\s*(?:go|gb|g)", p)
    if ram_match:
        vars["vm_memory"] = int(ram_match.group(1)) * 1024  # GB → MB

    ram_match_mb = re.search(r"(\d+)\s*(?:ram|mb|m|memoire|mémoire)", p)
    if ram_match_mb:
        vars["vm_memory"] = int(ram_match_mb.group(1))

    # Si rien n'a matché, essayer un nombre seul en contexte
    if "vm_memory" not in vars:
        solo_match = re.search(r"(\d+)\s*(?:mb|m|ram)", p)
        if solo_match:
            vars["vm_memory"] = int(solo_match.group(1))

    # Extraire les CPUs
    cpu_match = re.search(r"(\d+)\s*(?:cpu|core|vCPU|vcpu)", p)
    if cpu_match:
        vars["vm_cpus"] = int(cpu_match.group(1))

    # Extraire le VMID
    vmid_match = re.search(r"vmid[= ](\d+)", p)
    if vmid_match:
        vars["clone_vm_id"] = vmid_match.group(1)

    # Domaine Traefik
    domain_match = re.search(r"(\w[\w.-]*\.\w+\.\w+)", p)
    if domain_match:
        vars["traefik_domain"] = domain_match.group(1)
        # Extraire aussi le port si présent
        port_match = re.search(r"port[= ](\d+)", p)
        if port_match:
            vars["traefik_port"] = port_match.group(1)

    return vars


def handle(plan: dict, prompt: str = "") -> dict:
    """Point d'entrée : route la commande Terraform."""
    action = plan.get("action", "plan")
    p = prompt or plan.get("params", {}).get("prompt", "")

    if action == "create" or action == "apply":
        return apply(p)
    elif action == "plan":
        return plan(p)
    elif action == "destroy":
        return destroy(p)
    else:
        return {"message": f"Action inconnue: {action}", "error": True}

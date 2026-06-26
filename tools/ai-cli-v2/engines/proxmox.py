#!/usr/bin/env python3
"""Proxmox engine — clone VMs/LXCs from template via SSH (methode clone Terraform)"""

import subprocess
import json
import time
import re
import sys
import os

PROXMOX_HOST = "192.168.1.1"
SSH_KEY = os.path.expanduser("~/.ssh/id_ed25519")
ANSIBLE_DIR = os.path.expanduser("~/ansible-infra-lab2")
INVENTORY = os.path.join(ANSIBLE_DIR, "inventory")


def _ssh(cmd: str, timeout: int = 30) -> str:
    """Run a command on the Proxmox host via SSH"""
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        f"root@{PROXMOX_HOST}",
        cmd
    ]
    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"SSH command failed (exit {result.returncode}): "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return result.stdout.strip()


def list_vms() -> list:
    """Lister toutes les VMs sur Proxmox"""
    output = _ssh("qm list")
    vms = []
    lines = output.strip().split("\n")
    if len(lines) > 1:
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 4:
                vms.append({
                    "vmid": parts[0],
                    "name": parts[1],
                    "status": parts[2],
                    "memory": parts[3],
                })
    return vms


def _locked_ids() -> set:
    """IDs qui ont un lock file residuel"""
    try:
        output = _ssh("ls /run/lock/qemu-server/ 2>/dev/null || echo")
        ids = set()
        for f in output.split():
            m = re.search(r"lock-(\d+)\.conf", f)
            if m:
                ids.add(int(m.group(1)))
        return ids
    except Exception:
        return set()


def _existing_ids() -> set:
    """Tous les IDs deja utilises (VM + LXC)"""
    try:
        output = _ssh("ls /etc/pve/nodes/proxmox/qemu-server/ 2>/dev/null; ls /etc/pve/nodes/proxmox/lxc/ 2>/dev/null")
        ids = set()
        for f in output.split():
            m = re.search(r"^(\d+)\.conf", f)
            if m:
                ids.add(int(m.group(1)))
        return ids
    except Exception:
        return set()


def next_vm_id() -> int:
    """Trouver le prochain ID de VM disponible"""
    used = _existing_ids() | _locked_ids()
    for i in range(100, 1000):
        if i not in used:
            return i
    raise RuntimeError("Aucun ID disponible dans 100-999")


def clone_vm(template_id: int, new_id: int, name: str) -> str:
    """Cloner une VM depuis un template"""
    return _ssh(f"qm clone {template_id} {new_id} --name {name} --full")


def set_config(vm_id: int, cpus: int = None, memory: int = None) -> str:
    """Configurer CPU/RAM d'une VM"""
    opts = []
    if cpus:
        opts.append(f"--cores {cpus}")
    if memory:
        opts.append(f"--memory {memory}")
    if opts:
        return _ssh(f"qm set {vm_id} {' '.join(opts)}")
    return "No changes needed"


def start_vm(vm_id: int) -> str:
    """Demarrer une VM"""
    return _ssh(f"qm start {vm_id}")


def stop_vm(vm_id: int) -> str:
    """Arreter une VM"""
    return _ssh(f"qm stop {vm_id} --skiplock")


def delete_vm(vm_id: int) -> str:
    """Supprimer une VM"""
    return _ssh(f"qm destroy {vm_id} --skiplock --purge")


def get_vm_ip(vm_id: int, timeout: int = 120) -> str:
    """
    Attendre que la VM ait une IP et la retourner.
    Utilise QEMU Guest Agent (network-get-interfaces) ou ARP fallback.
    """
    for i in range(timeout // 5):
        time.sleep(5)

        # Methode 1: QEMU Guest Agent
        try:
            output = _ssh(f"qm guest cmd {vm_id} network-get-interfaces", timeout=10)
            data = json.loads(output)
            for iface in data:
                if iface.get("name") in ("eth0", "ens18", "enp0s18"):
                    for addr in iface.get("ip-addresses", []):
                        ip = addr.get("ip-address", "")
                        if ip.startswith("192.168.") or ip.startswith("10."):
                            return ip
        except Exception:
            pass

        # Methode 2: ARP table (fallback)
        try:
            mac = _ssh(f"qm config {vm_id} | grep -oP 'net0.*?hwaddr=\\K[^,]+'", timeout=5)
            mac_clean = mac.strip().lower()
            output = _ssh(f"arp -n | grep -i '{mac_clean}' | grep -oP '^[\\d.]+'", timeout=5)
            if output.strip():
                return output.strip()
        except Exception:
            pass

    raise TimeoutError(f"VM {vm_id} n'a pas obtenu d'IP en {timeout}s")


def add_to_inventory(name: str, ip: str, group: str = "test-clean",
                     traefik_domain: str = "", traefik_port: str = "") -> str:
    """Ajouter une VM dans l'inventory Ansible"""
    if not os.path.exists(INVENTORY):
        return f"Erreur: inventory {INVENTORY} introuvable"

    subprocess.run(
        ["sed", "-i", f"/^{name} /d", INVENTORY],
        capture_output=True
    )

    line = f"{name} ansible_host={ip}"
    if traefik_domain and traefik_port:
        line += f" traefik_domain={traefik_domain} traefik_port={traefik_port}"

    subprocess.run(
        ["sed", "-i", f"/^\\[{group}\\]/a\\{line}", INVENTORY],
        capture_output=True
    )
    return f"Ajoute {name} ({ip}) dans [{group}]"


def run_ansible(name: str, ip: str, traefik_domain: str = "",
                traefik_port: str = "") -> list:
    """Lancer les playbooks Ansible sur une nouvelle VM"""
    results = []
    ssh_opts = "-o StrictHostKeyChecking=no"

    if not os.path.exists(ANSIBLE_DIR):
        return [{"play": "check", "status": "error", "output": "Ansible dir not found"}]

    # Attendre SSH
    for i in range(30):
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=2",
             f"root@{ip}", "echo OK"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            break
        time.sleep(2)

    # Play 1: first_install
    result = subprocess.run(
        ["ansible-playbook", "-i", INVENTORY, "playbook_first_install.yml",
         "-l", name, f"--ssh-common-args={ssh_opts}"],
        capture_output=True, text=True, timeout=300,
        cwd=ANSIBLE_DIR
    )
    results.append({
        "play": "first_install",
        "status": "ok" if result.returncode == 0 else "failed",
        "output": result.stdout[-500:] if result.returncode == 0 else result.stderr[-500:]
    })

    # Play 2: traefik_config
    if traefik_domain and traefik_port:
        result = subprocess.run(
            ["ansible-playbook", "-i", INVENTORY, "playbook_traefik_config.yml",
             f"--ssh-common-args={ssh_opts}"],
            capture_output=True, text=True, timeout=120,
            cwd=ANSIBLE_DIR
        )
        results.append({
            "play": "traefik_config",
            "status": "ok" if result.returncode == 0 else "failed",
            "output": result.stdout[-300:] if result.returncode == 0 else result.stderr[-300:]
        })

    return results


def create_vm(params: dict) -> dict:
    """
    Creer une VM par clonage — methode rapide comme Terraform.

    Parametres:
        template_id: ID du template a cloner (defaut: 102)
        vm_id: Nouvel ID VM (auto si non fourni)
        name: Nom de la VM (defaut: vm-{id})
        cpus: Nb de CPU (optionnel)
        memory: RAM en MB (optionnel)
        traefik_domain: Domaine Traefik (optionnel)
        traefik_port: Port Traefik (optionnel)
        auto_ansible: Lancer Ansible apres clone (defaut: True)
        group: Groupe d'inventory (defaut: test-clean)
    """
    template_id = int(params.get("template_id", 102))
    vm_id = int(params.get("vm_id", 0)) or next_vm_id()
    name = params.get("name", f"vm-{vm_id}")
    cpus = params.get("cpus")
    memory = params.get("memory")
    traefik_domain = params.get("traefik_domain", "")
    traefik_port = params.get("traefik_port", "")
    auto_ansible = params.get("auto_ansible", True)
    group = params.get("group", "test-clean")

    steps = []

    try:
        # Step 1: Clone
        steps.append({"step": "clone", "status": "running"})
        clone_vm(template_id, vm_id, name)
        steps[-1] = {"step": "clone", "status": "ok",
                     "detail": f"Template {template_id} -> VM {vm_id} ({name})"}

        # Step 2: Configure CPU/RAM
        if cpus or memory:
            steps.append({"step": "config", "status": "running"})
            set_config(vm_id, cpus, memory)
            detail_parts = []
            if cpus: detail_parts.append(f"{cpus} CPU")
            if memory: detail_parts.append(f"{memory} MB RAM")
            steps[-1] = {"step": "config", "status": "ok",
                         "detail": ", ".join(detail_parts)}

        # Step 3: Start
        steps.append({"step": "start", "status": "running"})
        start_vm(vm_id)
        steps[-1] = {"step": "start", "status": "ok", "detail": "VM demarree"}

        # Step 4: Wait for IP
        steps.append({"step": "ip", "status": "running"})
        ip = get_vm_ip(vm_id)
        steps[-1] = {"step": "ip", "status": "ok", "detail": ip}

        # Step 5: Add to Ansible inventory
        steps.append({"step": "inventory", "status": "running"})
        msg = add_to_inventory(name, ip, group, traefik_domain, traefik_port)
        steps[-1] = {"step": "inventory", "status": "ok", "detail": msg}

        # Step 6: Ansible provisioning
        ansible_results = []
        if auto_ansible:
            steps.append({"step": "ansible", "status": "running"})
            ansible_results = run_ansible(name, ip, traefik_domain, traefik_port)
            all_ok = all(r["status"] == "ok" for r in ansible_results)
            steps[-1] = {"step": "ansible", "status": "ok" if all_ok else "partial",
                         "detail": f"{len(ansible_results)} play(s)"}

        return {
            "status": "ok",
            "vm": {"id": vm_id, "name": name, "ip": ip},
            "steps": steps,
            "ansible": ansible_results
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "vm": {"id": vm_id, "name": name} if vm_id else None,
            "steps": steps
        }

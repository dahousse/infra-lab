"""VM engine — delegates to Proxmox for VM creation via clone method"""

from engines.proxmox import create_vm as proxmox_create_vm, list_vms


def create_vm(plan: dict) -> dict:
    """Create VM via Proxmox clone (fast method)"""
    params = plan.get("params", {})
    return proxmox_create_vm(params)


def list_vm(plan: dict) -> dict:
    """List all VMs on Proxmox"""
    vms = list_vms()
    return {"count": len(vms), "vms": vms}

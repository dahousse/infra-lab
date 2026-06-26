"""VM engine — création et gestion de VMs Proxmox."""


def create_vm(plan: dict, prompt: str = ""):
    """Crée une VM via Proxmox (appelle Terraform en backend)."""
    return {
        "message": "VM engine ready — intégration Terraform à venir",
        "plan": plan,
    }

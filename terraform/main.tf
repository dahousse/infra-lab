terraform {
  required_providers {
    external = {
      source  = "hashicorp/external"
      version = "~> 2.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

# Déchiffrement du secret via Ansible Vault
data "external" "vault" {
  program = [
    "bash", "-c",
    "ansible-vault view secret.vault.yml --vault-password-file=vault_pass.txt 2>/dev/null | yq -o json"
  ]
}

# Variable locale contenant le mot de passe déchiffré
locals {
  proxmox_password = data.external.vault.result.proxmox_password
}

# Création du conteneur
resource "null_resource" "create_test_lxc" {
  provisioner "local-exec" {
    command = <<-EOT
      sshpass -p '${local.proxmox_password}' ssh -o StrictHostKeyChecking=no root@192.168.1.1 \
      "pvesh create /nodes/proxmox/lxc \
      --ostemplate local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
      --vmid 999 \
      --storage local-lvm \
      --hostname test-terraform \
      --password REDACTED_SECRET \
      --cores 1 \
      --memory 512 \
      --swap 512 \
      --unprivileged 1 \
      --net0 name=eth0,bridge=vmbr0,ip=dhcp"
    EOT
  }
}

# Destruction du conteneur
resource "null_resource" "destroy_test_lxc" {
  triggers = {
    proxmox_password = local.proxmox_password
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      sshpass -p '${self.triggers["proxmox_password"]}' ssh -o StrictHostKeyChecking=no root@192.168.1.1 \
      "pvesh delete /nodes/proxmox/lxc/999"
    EOT
  }
}

output "message" {
  value = "Conteneur test-terraform géré par Terraform (création et destruction)."
}

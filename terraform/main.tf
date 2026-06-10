terraform {
  required_version = ">= 1.6.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.60.0"
    }
  }
}

# Les anciennes ressources de test LXC basées sur SSH ont été désactivées
# au profit du provider natif Proxmox (défini dans cloud.tf).

# resource "null_resource" "create_test_lxc" {
#   provisioner "local-exec" {
#     command = <<-EOT
#       set -euo pipefail
#       PROXMOX_PASSWORD=$(ansible-vault view "${var.vault_file}" --vault-password-file="${var.vault_password_file}" 2>/dev/null | yq -r '.proxmox_password')
#       LXC_ROOT_PASSWORD=$(ansible-vault view "${var.vault_file}" --vault-password-file="${var.vault_password_file}" 2>/dev/null | yq -r '.${var.vault_lxc_root_password_key}')
# 
#       sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${var.proxmox_host} \
#       "pvesh create /nodes/${var.proxmox_node}/lxc \
#       --ostemplate ${var.lxc_template} \
#       --vmid ${var.test_lxc.vmid} \
#       --storage ${var.lxc_storage} \
#       --hostname ${var.test_lxc.hostname} \
#       --password '$LXC_ROOT_PASSWORD' \
#       --cores ${var.test_lxc.cores} \
#       --memory ${var.test_lxc.memory} \
#       --swap ${var.test_lxc.swap} \
#       --unprivileged 1 \
#       --net0 name=eth0,bridge=${var.lxc_bridge},ip=${var.test_lxc.ip_config}"
#     EOT
#   }
# }

# resource "null_resource" "destroy_test_lxc" {
#   triggers = {
#     proxmox_host        = var.proxmox_host
#     proxmox_node        = var.proxmox_node
#     vault_file          = var.vault_file
#     vault_password_file = var.vault_password_file
#     vmid                = tostring(var.test_lxc.vmid)
#   }
# 
#   provisioner "local-exec" {
#     when    = destroy
#     command = <<-EOT
#       set -euo pipefail
#       PROXMOX_PASSWORD=$(ansible-vault view "${self.triggers["vault_file"]}" --vault-password-file="${self.triggers["vault_password_file"]}" 2>/dev/null | yq -r '.proxmox_password')
# 
#       sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${self.triggers["proxmox_host"]} \
#       "qm stop ${self.triggers["vmid"]} >/dev/null 2>&1 || true; qm destroy ${self.triggers["vmid"]} --purge 1"
#     EOT
#   }
# }

output "message" {
  value = "Conteneur ${var.test_lxc.hostname} géré par Terraform."
}

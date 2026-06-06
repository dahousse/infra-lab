# Création du conteneur Nextcloud
resource "null_resource" "create_nextcloud_lxc" {
  provisioner "local-exec" {
    command = <<-EOT
      set -euo pipefail
      PROXMOX_PASSWORD=$(ansible-vault view "${var.vault_file}" --vault-password-file="${var.vault_password_file}" 2>/dev/null | yq -r '.proxmox_password')
      LXC_ROOT_PASSWORD=$(ansible-vault view "${var.vault_file}" --vault-password-file="${var.vault_password_file}" 2>/dev/null | yq -r '.${var.vault_lxc_root_password_key}')

      sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${var.proxmox_host} \
      "pvesh create /nodes/${var.proxmox_node}/lxc \
      --ostemplate ${var.lxc_template} \
      --vmid ${var.nextcloud_lxc.vmid} \
      --storage ${var.lxc_storage} \
      --hostname ${var.nextcloud_lxc.hostname} \
      --password '$LXC_ROOT_PASSWORD' \
      --cores ${var.nextcloud_lxc.cores} \
      --memory ${var.nextcloud_lxc.memory} \
      --swap ${var.nextcloud_lxc.swap} \
      --unprivileged 1 \
      --net0 name=eth0,bridge=${var.lxc_bridge},ip=${var.nextcloud_lxc.ip_config},gw=${var.lxc_gateway}"
    EOT
  }
}

# Destruction du conteneur Nextcloud
resource "null_resource" "destroy_nextcloud_lxc" {
  triggers = {
    proxmox_host        = var.proxmox_host
    proxmox_node        = var.proxmox_node
    vault_file          = var.vault_file
    vault_password_file = var.vault_password_file
    vmid                = tostring(var.nextcloud_lxc.vmid)
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      set -euo pipefail
      PROXMOX_PASSWORD=$(ansible-vault view "${self.triggers["vault_file"]}" --vault-password-file="${self.triggers["vault_password_file"]}" 2>/dev/null | yq -r '.proxmox_password')

      sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${self.triggers["proxmox_host"]} \
      "pvesh delete /nodes/${self.triggers["proxmox_node"]}/lxc/${self.triggers["vmid"]}"
    EOT
  }
}

output "nextcloud_ip" {
  value = split("/", var.nextcloud_lxc.ip_config)[0]
}

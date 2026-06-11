# Création de la VM Nextcloud
resource "null_resource" "create_nextcloud_vm" {
  triggers = {
    vm_template_vmid = tostring(var.nextcloud_vm_template_vmid)
    vmid             = tostring(var.nextcloud_vm.vmid)
    ssh_key_sha      = filesha256(var.ssh_public_key_file)
    disk_resize      = var.nextcloud_vm_disk_resize
  }

  provisioner "local-exec" {
    command = <<-EOT
      set -euo pipefail
      PROXMOX_PASSWORD=$(ansible-vault view "${var.vault_file}" --vault-password-file="${var.vault_password_file}" 2>/dev/null | yq -r '.proxmox_password')
      SSH_PUBKEY=$(tr -d '\n' < "${var.ssh_public_key_file}")

      sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${var.proxmox_host} \
      "qm clone ${var.nextcloud_vm_template_vmid} ${var.nextcloud_vm.vmid} --full 1 --name ${var.nextcloud_vm.hostname} --storage ${var.lxc_storage} && \
      qm set ${var.nextcloud_vm.vmid} \
      --cores ${var.nextcloud_vm.cores} \
      --memory ${var.nextcloud_vm.memory} \
      --net0 virtio,bridge=${var.lxc_bridge} \
      --agent enabled=1 \
      --ciuser root \
      --sshkeys '$SSH_PUBKEY' \
      --ipconfig0 ip=${var.nextcloud_vm.ip_config},gw=${var.lxc_gateway} \
      --onboot 1 && \
      qm resize ${var.nextcloud_vm.vmid} scsi0 ${var.nextcloud_vm_disk_resize} && \
      qm start ${var.nextcloud_vm.vmid}"
    EOT
  }
}

# Destruction de la VM Nextcloud
resource "null_resource" "destroy_nextcloud_vm" {
  triggers = {
    proxmox_host        = var.proxmox_host
    proxmox_node        = var.proxmox_node
    vault_file          = var.vault_file
    vault_password_file = var.vault_password_file
    vmid                = tostring(var.nextcloud_vm.vmid)
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      set -euo pipefail
      PROXMOX_PASSWORD=$(ansible-vault view "${self.triggers["vault_file"]}" --vault-password-file="${self.triggers["vault_password_file"]}" 2>/dev/null | yq -r '.proxmox_password')

      sshpass -p "$PROXMOX_PASSWORD" ssh -o StrictHostKeyChecking=no root@${self.triggers["proxmox_host"]} \
      "qm stop ${self.triggers["vmid"]} >/dev/null 2>&1 || true; qm destroy ${self.triggers["vmid"]} --purge 1"
    EOT
  }
}

output "nextcloud_ip" {
  value = split("/", var.nextcloud_vm.ip_config)[0]
}

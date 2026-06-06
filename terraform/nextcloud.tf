# Création du conteneur Nextcloud
resource "null_resource" "create_nextcloud_lxc" {
  provisioner "local-exec" {
    command = <<-EOT
      sshpass -p '${local.proxmox_password}' ssh -o StrictHostKeyChecking=no root@192.168.1.1 \
      "pvesh create /nodes/proxmox/lxc \
      --ostemplate local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
      --vmid 110 \
      --storage local-lvm \
      --hostname nextcloud \
      --password REDACTED_SECRET \
      --cores 2 \
      --memory 1024 \
      --swap 512 \
      --unprivileged 1 \
      --net0 name=eth0,bridge=vmbr0,ip=192.168.1.11/24,gw=192.168.1.254"
    EOT
  }
}

# Destruction du conteneur Nextcloud
resource "null_resource" "destroy_nextcloud_lxc" {
  triggers = {
    proxmox_password = local.proxmox_password
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      sshpass -p '${self.triggers["proxmox_password"]}' ssh -o StrictHostKeyChecking=no root@192.168.1.1 \
      "pvesh delete /nodes/proxmox/lxc/110"
    EOT
  }
}

output "nextcloud_ip" {
  value = "192.168.1.11"
}

variable "proxmox_host" {
  description = "Adresse IP ou nom DNS de l'hôte Proxmox."
  type        = string
  default     = "192.168.1.1"
}

variable "proxmox_node" {
  description = "Nom du noeud Proxmox."
  type        = string
  default     = "proxmox"
}

variable "vault_file" {
  description = "Fichier Ansible Vault contenant proxmox_password."
  type        = string
  default     = "secret.vault.yml"
}

variable "vault_password_file" {
  description = "Fichier contenant le mot de passe Ansible Vault."
  type        = string
  default     = "vault_pass.txt"
}

variable "vault_lxc_root_password_key" {
  description = "Nom de la clé Vault qui contient le mot de passe root des conteneurs LXC."
  type        = string
  default     = "lxc_root_password"
}

variable "lxc_template" {
  description = "Template LXC Proxmox à utiliser."
  type        = string
  default     = "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
}

variable "nextcloud_vm_template_vmid" {
  description = "VM template Proxmox à cloner pour Nextcloud."
  type        = number
  default     = 102
}

variable "lxc_storage" {
  description = "Stockage Proxmox cible."
  type        = string
  default     = "local-lvm"
}

variable "lxc_bridge" {
  description = "Bridge réseau Proxmox."
  type        = string
  default     = "vmbr0"
}

variable "lxc_gateway" {
  description = "Passerelle par défaut pour les conteneurs avec IP statique."
  type        = string
  default     = "192.168.1.254"
}

variable "test_lxc" {
  description = "Paramètres du conteneur de test."
  type = object({
    vmid      = number
    hostname  = string
    cores     = number
    memory    = number
    swap      = number
    ip_config = string
  })
  default = {
    vmid      = 999
    hostname  = "test-terraform"
    cores     = 1
    memory    = 512
    swap      = 512
    ip_config = "dhcp"
  }
}

variable "nextcloud_vm" {
  description = "Paramètres de la VM Nextcloud."
  type = object({
    vmid      = number
    hostname  = string
    cores     = number
    memory    = number
    swap      = number
    ip_config = string
  })
  default = {
    vmid      = 124
    hostname  = "nextcloud"
    cores     = 2
    memory    = 4096
    swap      = 0
    ip_config = "192.168.1.11/24"
  }
}

variable "nextcloud_vm_disk_resize" {
  description = "Taille du disque système Nextcloud après clonage."
  type        = string
  default     = "20G"
}

variable "ssh_public_key_file" {
  description = "Clé publique SSH injectée dans la VM Nextcloud via cloud-init."
  type        = string
  default     = "/home/hasmi/.ssh/id_ed25519.pub"
}

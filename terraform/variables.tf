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

variable "nextcloud_lxc" {
  description = "Paramètres du conteneur Nextcloud."
  type = object({
    vmid      = number
    hostname  = string
    cores     = number
    memory    = number
    swap      = number
    ip_config = string
  })
  default = {
    vmid      = 110
    hostname  = "nextcloud"
    cores     = 2
    memory    = 1024
    swap      = 512
    ip_config = "192.168.1.11/24"
  }
}

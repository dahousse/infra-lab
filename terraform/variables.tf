variable "proxmox_host" {
  description = "IP ou DNS Proxmox"
  type        = string
  default     = "192.168.1.1"
}

variable "proxmox_node" {
  description = "Nom du node Proxmox"
  type        = string
  default     = "proxmox"
}

variable "proxmox_password" {
  description = "Mot de passe Proxmox"
  type        = string
  sensitive   = true
}

variable "lxc_root_password" {
  description = "Mot de passe root LXC"
  type        = string
  sensitive   = true
}

variable "lxc_template" {
  description = "Template LXC"
  type        = string
  default     = "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
}

variable "lxc_storage" {
  type    = string
  default = "local-lvm"
}

variable "lxc_bridge" {
  type    = string
  default = "vmbr0"
}

variable "test_lxc" {
  type = object({
    vmid     = number
    hostname = string
    cores    = number
    memory   = number
    swap     = number
  })

  default = {
    vmid     = 999
    hostname = "test-terraform"
    cores    = 1
    memory   = 512
    swap     = 512
  }
}

variable "ssh_public_key_file" {
  type    = string
  default = "/home/hasmi/.ssh/id_ed25519.pub"
}

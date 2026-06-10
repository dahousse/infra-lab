terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.60.0" # Vérifie la dernière version stable
    }
  }
}

provider "proxmox" {
  endpoint = "https://192.168.1.1:8006/"
  username = "root@pam"
  password = var.proxmox_password
  insecure = true
}

resource "proxmox_virtual_environment_container" "test_lxc" {
  node_name = "proxmox"
  vm_id     = 999

  initialization {
    hostname = "test-terraform"

    ip_config {
      ipv4 {
        address = "dhcp"
      }
    }

    user_account {
      password = var.lxc_root_password
    }
  }

  content_type = "rootdir"

  template_file_id = "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"

  cpu {
    cores = 1
  }

  memory {
    dedicated = 512
  }
}

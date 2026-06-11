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

  description = "LXC test créé via Terraform (homelab infra-lab2)"

  # ✅ CORRECT
  operating_system {
    template_file_id = "local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 512
  }

  features {
    nesting = true
  }
}

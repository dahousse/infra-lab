# INFRA LAB — Project Context

> Ce fichier sert de AGENTS.md pour le projet INFRA LAB.
> Il est automatiquement chargé par Hermes dans le system prompt.

## Qu'est-ce que INFRA LAB ?

Infrastructure homelab basée sur **Proxmox VE**, orchestrée avec **Terraform**,
configurée avec **Ansible**, servie par **Traefik** (Let's Encrypt TLS),
et sécurisée par **AdGuard Home** (DNS).

Domaine : `*.mysmihome.duckdns.org`

## Architecture réseau

```
Internet → Traefik (.200:443) → services (.1, .3, .5, .6, .13, .148, .202…)
```

| IP | Hostname | Rôle |
|:---|:---|---|
| .1 | pve | Proxmox hyperviseur |
| .2 | homeassistant | Home Assistant OS |
| .3 | cockpit | Infra VM (Hermes WebUI) |
| .5 | casaos | CasaOS |
| .6 | portainer | Portainer |
| .10 | ollama | Ollama LLM |
| .13 | dashy | Dashy dashboard |
| .35 | monitor | Uptime-Kuma |
| .148 | test-905 | VM test active |
| .200 | traefik | Reverse proxy |
| .202 | adguard | AdGuard DNS |

## Structure des repos

```
/workspace/
├── ansible-infra-lab2/       ← Ansible (inventory, playbooks, rôles)
├── infra-lab-tf/             ← Terraform (deploy-vm.tf, variables)
└── infra-lab/                ← Monorepo OS Prompt ai-cli-v2
```

## Conventions de déploiement

### Cycle TF → Ansible → Traefik (I1)

```
# Déploiement complet d'une VM
cd ~/infra-lab-tf
terraform apply \
  -var="clone_prefix=test" \
  -var="clone_vm_id=906" \
  -var="template_vm_id=102" \
  -var="vm_cpus=2" \
  -var="vm_memory=2048" \
  -var="traefik_domain=test-906.mysmihome.duckdns.org" \
  -var="traefik_port=80"

terraform apply
  ├─ 1. Crée VM clone (bpg/proxmox, template 102)
  ├─ 2. local-exec: nettoie + ajoute dans l'inventory Ansible
  │     └─ Ligne: test-906 ansible_host=<IP> traefik_domain=... traefik_port=...
  ├─ 3. local-exec: Attend SSH (60s timeout, 30 tentatives)
  ├─ 4. local-exec: playbook_first_install.yml -l test-906
  │     └─ Crée user infra + sudo, SSH keys, Zsh + Oh My Zsh, paquets
  └─ 5. local-exec: playbook_traefik_config.yml (si domain+port fournis)
        └─ Connecte → traefik (192.168.1.200)
        └─ grep des domaines existants dans conf.d/
        └─ Template J2 → nouveau fichier conf.d/test-906.yml
        └─ Reload Traefik (systemctl kill -s USR1 traefik)

# Destruction propre
terraform destroy
  └─ provisioner destroy:
       ├─ Retire test-906 de l'inventory Ansible
       ├─ rm -f /etc/traefik/conf.d/test-906.yml
       └─ Reload Traefik
```

### Variables Terraform (infra-lab-tf/variables.tf)

| Variable | Default | Description |
|:---|---:|:---|
| `clone_prefix` | `"vm"` | Préfixe du nom (ex: test, app) |
| `clone_vm_id` | — | ID de la VM + nom complet `${prefix}-${id}` |
| `template_vm_id` | — | Template Proxmox à cloner (102 = Debian 13) |
| `vm_cpus` | `1` | CPU cores |
| `vm_memory` | `512` | RAM en MB |
| `traefik_domain` | `""` | Domaine complet (optionnel) |
| `traefik_port` | `""` | Port du service (optionnel) |
| `proxmox_password` | (sensitive) | Mot de passe API Proxmox |
| `lxc_root_password` | (sensitive) | Password root de la VM clonée |

### Règles
- **Inventory unique** : plus de fichier `hosts`, seulement `inventory`
- **Naming** : `test-${vm_id}` (incrémental)
- **Traefik intelligent** : détecte les domaines existants dans `conf.d/` avant d'écrire
- **Configs manuelles protégées** : `cloud.yml`, `homelab.yml`, `uptime.yml` — jamais toucher

### SSH
- Clé : `/workspace/.ssh/id_ed25519`
- VM : `infra@192.168.1.3` (accès root aux autres depuis la VM)
- Machines non SSH-ables : ollama(.10), monitor(.35), dashy(.13), homeassistant(.2)

### OS Prompt ai-cli-v2.5
```
User → Router → Intent → Planner → Dispatcher → Engine
```
Engines : ✅ VM, ✅ Ollama, ✅ Proxmox, ✅ Terraform

## Versions
- Terraform v1.15.6, provider bpg/proxmox v0.60.0
- Ansible core 2.19+, Python 3.13
- Ollama v0.30.10, modèle par défaut qwen2.5-coder:7b
- OS cible : Debian 13
- Traefik v3.x, AdGuard latest

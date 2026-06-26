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

### Cycle TF → Ansible → Traefik
```
terraform apply
  ├─ Crée VM clone (bpg/proxmox)
  ├─ local-exec: nettoie + ajoute dans inventory
  └─ local-exec: ansible-playbook site.yml
       ├─ Play 1: Wait SSH + Python
       ├─ Play 2: first_install (apt, paquets)
       ├─ Play 3: Dotfiles + Zsh
       └─ Play 4: Traefik config (intelligent)
```

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
Engines : ✅ VM, ✅ Ollama, ⚠️ Terraform (stubs)

## Versions
- Terraform v1.15.6, provider bpg/proxmox v0.60.0
- Ansible core 2.19+, Python 3.13
- Ollama v0.30.10, modèle par défaut qwen2.5-coder:7b
- OS cible : Debian 13
- Traefik v3.x, AdGuard latest

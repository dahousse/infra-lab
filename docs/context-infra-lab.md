# INFRA LAB — Contexte Complet

> Généré le 2026-06-26 par Hermes Agent (session WebUI)
> Utilise ce fichier pour repartir à zéro, recréer un nouvel infra lab,
> ou simplement te rappeler de tout ce qui a été fait.

---

## 📖 Table des matières

1. [Mémoire personnelle (Hermes)](#1-memoire-personnelle)
2. [Profil utilisateur](#2-profil-utilisateur)
3. [Âme de l'agent (prompt system)](#3-ame-de-lagent)
4. [Project Context — Architecture générale](#4-project-context)
5. [Mapping réseau](#5-mapping-reseau)
6. [Inventory Ansible complet](#6-inventory-ansible)
7. [Config Traefik — Tous les domaines](#7-config-traefik)
8. [Cycle automatique TF → Ansible → Traefik](#8-cycle-automatique)
9. [Terraform — deploy-vm.tf](#9-terraform)
10. [Ansible — Playbooks et rôles](#10-ansible)
11. [OS Prompt ai-cli-v2](#11-os-prompt)
12. [Todos & évolutions futures](#12-todos)

---

## 1. Mémoire personnelle

```yaml
# INFRASTRUCTURE
ollama_vm:     192.168.1.10:11434 (v0.30.10, CPU-only, 10GB Proxmox)
ollama_models: qwen2.5-coder:7b (default), llama3.1, qwen3:4b-instruct/4b-hermes,
               codellama:7b, devops-bot
ollama_config: context_length=65536, ollama_num_ctx=65536

# REMOTE VM
infra_vm:      infra@192.168.1.3 (6GB RAM, 2GB swap, Docker)
webui:         nesquena (8787) — interface principale
dashboard:     9119 — conservé "au cas où"
webui_auth:    admin / hermes

# TELEGRAM GATEWAY
telegram_user: hasmi (1480745817)
allowed:       TELEGRAM_ALLOWED_USERS=1480745817 (Gateway active)

# FEDORA 44 HOST (laptop)
wayland:       --ozone-platform-hint=wayland --no-sandbox --disable-gpu
desktop_file:  ~/.local/share/applications/hermes-desktop.desktop
terminal:      ZSH (scroll auto en bas)

# SSH
ssh_key:       /workspace/.ssh/id_ed25519
ssh_user:      infra@192.168.1.3

# GIT
repos:
  - dahousse/infra-lab          (monorepo + ai-cli-v2)
  - dahousse/infra-lab-tf       (Terraform Proxmox)
  - dahousse/ansible-infra-lab2 (Ansible v2 + Traefik)
github_backup: OUI (mais pas push sans feu vert)

# REGLES ABSOLUES
NE_JAMAIS_INSTALLER: true  # ni apt, ni pip, ni curl, ni npm - tout est déjà sur la VM
TOUJOURS_SSH_DABORD: true  # vérifier ce qui existe avant d'agir
CONFIGS_MANUEL_TRAEFIK_PROTEGER: [cloud.yml, uptime.yml, homelab.yml]

# OS PROMPT v2.5
os_prompt:
  status: stable
  flow: CLI ai → router → intent → planner → dispatcher → engine
  engines: [VM (ok), Ollama (ok), Terraform/Proxmox (stubs)]
  focus: clarté > complexité
```

---

## 2. Profil utilisateur

```yaml
# IDENTITÉ
pseudo:   hasmi
langue:   Darija marocain (khoya, labas, saha)
style:    convivial, humour, direct

# MODE DE TRAVAIL
autonomy: Agir sans demander pour tâches connues, mais JAMAIS installer sans OK
cadre:    "ne pas mentionner Docker, juste la VM"
conventions: "/workspace/ = zone de travail, modifs sans push sans accord"

# PROJET ACTUEL
projet:   INFRA LAB
composants:
  - Proxmox (PVE)          → 192.168.1.1
  - Terraform              → infra-lab-tf (bpg/proxmox v0.60.0, Terraform v1.15.6)
  - Ansible                → ansible-infra-lab2 (rôles base + dotfiles + traefik)
  - Traefik                → 192.168.1.200, *.mysmihome.duckdns.org
  - AdGuard                → 192.168.1.202
  - Ollama                 → 192.168.1.10 (phi3:mini, qwen2.5-coder:7b)
focus:    stabilisation OS Prompt ai-cli-v2.5

# CANAUX
telegram: hasmi
home_assistant: configuré via Hermes Desktop
```

---

## 3. Âme de l'agent — Prompt system Hermes complet

> Ce prompt system est celui qui a piloté l'agent pendant toute la session du 2026-06-26.
> Il définit **comment l'agent pense, agit et communique**.

### Persona

Tu es Hermes Agent (par Nous Research). Quand l'utilisateur a besoin d'aide avec Hermes lui-même — configuration, setup, utilisation, extension, dépannage — ou quand tu as besoin de comprendre tes propres fonctionnalités, outils ou capacités, la documentation sur https://hermes-agent.nousresearch.com/docs est ta référence officielle, toujours la plus à jour. Charge le skill `hermes-agent` avec `skill_view(name='hermes-agent')` pour des conseils supplémentaires et des workflows éprouvés, mais considère la documentation comme source de vérité en cas de divergence.

### Règles fondamentales

1.  **Finishing the job** — Quand l'utilisateur demande de construire, exécuter ou vérifier quelque chose, le résultat doit être un artefact fonctionnel appuyé par de vrais résultats d'outils — pas une description. Ne t'arrête pas après un stub, un plan ou une seule commande. Continue jusqu'à avoir réellement exercé le code ou produit le résultat demandé, puis rapporte ce que l'exécution réelle a retourné.
    - Si un outil, une installation ou un appel réseau échoue et bloque la voie réelle, dis-le directement et essaie une alternative (autre gestionnaire de paquets, autre approche, demande à l'utilisateur).
    - **NE JAMAIS** substituer un résultat fabriqué plausible (données inventées, contenu de fichier fabriqué, réponses API synthétisées) à des résultats que tu n'as pas pu produire réellement. Signaler honnêtement un blocage est toujours mieux qu'inventer un résultat.

2.  **Parallel tool calls** — Quand tu as besoin de plusieurs informations qui ne dépendent pas les unes des autres, demande-les ensemble en une seule réponse plutôt qu'un appel d'outil par tour. Les lectures indépendantes, recherches, fetches web et commandes en lecture seule doivent être groupés dans le même tour d'assistant — l'exécuteur traite les appels indépendants en concurrence.

3.  **Memory persistante** — Tu as une mémoire persistante entre les sessions. Sauvegarde les faits durables avec l'outil `memory` : préférences utilisateur, détails d'environnement, particularités des outils, conventions stables.
    - Priorise ce qui réduit les corrections futures de l'utilisateur — la mémoire la plus précieuse est celle qui évite à l'utilisateur de devoir te corriger ou te rappeler quelque chose.
    - **Ne PAS** sauvegarder : progression de tâche, résultats de session, logs de travail terminé, état TODO temporaire.
    - Écris les souvenirs comme des **faits déclaratifs**, pas des instructions à toi-même.
    - Les procédures et workflows vont dans les **skills**, pas dans la mémoire.

4.  **Skills (obligatoire)** — Avant de répondre, scanne les skills disponibles. Si un skill correspond ou est même partiellement pertinent à ta tâche, tu DOIS le charger avec `skill_view(name)` et suivre ses instructions. Les skills contiennent des connaissances spécialisées — endpoints API, commandes spécifiques aux outils, workflows éprouvés qui surpassent les approches généralistes.

5.  **Mid-turn user steering** — Pendant que tu travailles, l'utilisateur peut envoyer un message hors-bande que Hermes ajoute à la fin d'un résultat d'outil, encapsulé exactement comme :
    ```
    [OUT-OF-BAND USER MESSAGE — a direct message from the user, delivered mid-turn; not tool output]
    <leur message>
    [/OUT-OF-BAND USER MESSAGE]
    ```
    Traite cela comme une instruction directe de l'utilisateur, avec la même autorité que sa demande originale, et ajuste ton cap en conséquence.

### Comportement et style

- **Concis et factuel** — Les mises à jour de progression doivent être concises, factuelles et dans la langue de l'utilisateur. Une ou deux phrases courtes suffisent.
- **Ne pas révéler le raisonnement interne** — Ne pas montrer le chain-of-thought, les brouillons privés, les scratchpads, les secrets, les logs bruts ou les longs résultats d'outils.
- **Réponses finales claires** — Les réponses visibles finales de l'assistant doivent être claires, orientées utilisateur et dans la langue de l'utilisateur.

### Règles d'utilisation des outils

- `read_file` au lieu de `cat`/`head`/`tail`
- `search_files` au lieu de `grep`/`rg`/`find`/`ls`
- `patch` au lieu de `sed`/`awk` pour éditer
- `write_file` au lieu de `echo`/`cat heredoc`
- Réserver `terminal` pour : builds, installations, git, processus, scripts, réseau, gestionnaires de paquets — tout ce qui a besoin d'un shell
- `background=true` → presque toujours avec `notify_on_complete=true`
- `pty=true` pour les outils CLI interactifs (Codex, Claude Code, Python REPL)

### Conventions de déploiement (infra-lab)

> Ces règles sont ajoutées dynamiquement par le profil utilisateur et les skills :

- **NE JAMAIS installer/télécharger quoi que ce soit sans demander** — ni apt, ni pip, ni curl binary, ni npm. Tout le nécessaire est déjà sur la VM hôte (192.168.1.3) ou sur le host. Toujours SSH d'abord (clé `/workspace/.ssh/id_ed25519`) pour vérifier ce qui existe.
- **Ne pas mentionner Docker** — dire "la VM"
- **Agir sans demander** pour les tâches existantes, mais jamais installer sans accord
- **Protéger les configs Traefik manuelles** de l'utilisateur (`cloud.yml`, `uptime.yml`, `homelab.yml`) — ne jamais toucher/supprimer
- Si Ansible génère un doublon, supprimer le fichier auto-généré pas le manuel
- **Workflow** : modifs dans `/workspace/`, pas de push GitHub sans feu vert
- **Langue** : français / darija marocain (khoya, labas, saha)

---

## 4. Project Context — AGENTS.md du projet INFRA LAB

> Ce fichier sert de **AGENTS.md** pour le projet INFRA LAB.
> Il définit les conventions, l'architecture et les workflows pour tout agent
> travaillant sur ce projet. Inspire-toi de ce document pour comprendre le projet
> et agir efficacement.

---

### Qu'est-ce que INFRA LAB ?

INFRA LAB est un projet d'infrastructure "homelab" basé sur **Proxmox VE**,
orchestré avec **Terraform**, configuré avec **Ansible**, servi par **Traefik**,
et sécurisé par **AdGuard Home**.

Objectif : automatiser la création et la configuration de VMs, déployer des
services (Portainer, CasaOS, Dashy, Uptime-Kuma, Ollama…), et les exposer via
un reverse proxy TLS avec domaine wildcard `*.mysmihome.duckdns.org`.

---

### Structure des repositories

```
/workspace/
├── context-infra-lab.md       ← CE FICHIER — contexte complet
├── kanban-infra-lab.html      ← Tableau Kanban HTML
├── deploy-vm.tf               ← Version locale de deploy-vm.tf (référence)
├── ansible-infra-lab2/
│   ├── inventory              ← FICHIER UNIQUE d'inventaire (plus de hosts)
│   ├── ansible.cfg
│   ├── site.yml               ← Orchestrateur 4 plays
│   ├── playbook_first_install.yml   ← Paquets + base + dotfiles
│   ├── playbook_traefik_config.yml  ← Config Traefik intelligente
│   ├── templates/
│   │   └── traefik-service.j2       ← Template de config Traefik
│   ├── traefik/
│   │   └── traefik.yaml             ← Config statique Traefik
│   └── roles/
│       ├── base/tasks/main.yml      ← apt update, upgrade, paquets
│       └── dotfiles/tasks/main.yml  ← Zsh, variables utilisateur
├── infra-lab-tf/
│   ├── deploy-vm.tf           ← Ressource VM clone + local-exec
│   ├── variables.tf           ← Variables Terraform
│   ├── terraform.tfvars       ← Valeurs sensibles (clone_vm_id, secrets)
│   ├── versions.tf            ← Providers & versions
│   └── .terraform.lock.hcl
└── infra-lab/                 ← Monorepo (ai-cli-v2 OS Prompt)
    └── feature/router-v3      ← Branche active
```

---

### Conventions absolues

#### 1. NE JAMAIS installer sans demander
Ni apt, pip, curl, npm — tout est déjà sur la VM infra@192.168.1.3.
Toujours SSH d'abord avec `/workspace/.ssh/id_ed25519`.

#### 2. Ne pas mentionner Docker
Dire "la VM", pas "le conteneur" ou "Docker". L'infra VM (cockpit) a Docker
mais on parle d'elle comme d'une machine normale.

#### 3. Traefik — tes configs manuelles sont sacrées
Les fichiers suivants sont **créés et gérés par toi**, ne jamais les toucher :
- `cloud.yml` → `cloud.mysmihome.duckdns.org` → .11:80
- `homelab.yml` → `homelab.mysmihome.duckdns.org` → .1:8006
- `uptime.yml` → `uptime.mysmihome.duckdns.org` → .35:3001

Si Ansible génère un doublon → supprimer le fichier auto-généré.

#### 4. Workflow de modification
- Les modifs se font dans `/workspace/` (monté de la VM)
- Les fichiers locaux sont copiés sur la VM avec `scp` ou `rsync`
- Pas de push GitHub sans ton feu vert explicite
- `terraform validate` avant tout apply

#### 5. Naming des VMs
```hcl
clone_prefix = "test"
clone_vm_id  = <incrémenter>
# Résultat : test-906, test-907, etc.
```

#### 6. Cycle automatique TF → Ansible → Traefik
```
terraform apply
  ├─ Crée VM clone (bpg/proxmox)
  ├─ local-exec: nettoie + ajoute dans inventory
  └─ local-exec: ansible-playbook site.yml
       ├─ Play 1: Wait for SSH + Python
       ├─ Play 2: first_install (apt, base, paquets)
       ├─ Play 3: Dotfiles + Zsh
       └─ Play 4: Traefik config (intelligent — skip si domaine existe)
```

#### 7. Inventory — un seul fichier
```ini
[tous_mes_serveurs:children]
homelab
supervision
docker
app
system
llm
test-clean
```
Chaque machine sous son groupe avec `ansible_host`, `traefik_domain`, `traefik_port`.

#### 8. Playbook Traefik — intelligent
Détecte les domaines déjà présents dans `/etc/traefik/conf.d/*.yml`
avant de générer. Si le domaine existe déjà (manuel ou auto) → SKIP.
Traefik reload uniquement si nouveau fichier créé.

#### 9. SSH
- Clé : `/workspace/.ssh/id_ed25519`
- User sur la VM : `infra@192.168.1.3`
- Accès root aux autres machines depuis la VM

---

### Mapping des accès SSH

| Machine | IP | SSH joignable ? | Notes |
|:---|:---|:---:|:---|
| pve | 192.168.1.1 | ✅ | root (clé depuis VM) |
| cockpit | 192.168.1.3 | ✅ | infra (clé depuis workspace) |
| traefik | 192.168.1.200 | ✅ | root (depuis VM) |
| adguard | 192.168.1.202 | ✅ | root (depuis VM) |
| casaos | 192.168.1.5 | ✅ | root (depuis VM) |
| portainer | 192.168.1.6 | ✅ | root (depuis VM) |
| test-905 | 192.168.1.148 | ✅ | root (depuis VM) |
| ollama | 192.168.1.10 | ❌ | Permission denied (clé publique) |
| monitor | 192.168.1.35 | ❌ | Permission denied |
| dashy | 192.168.1.13 | ❌ | Auth différente |
| homeassistant | 192.168.1.2 | ❌ | Auth différente |

> **TODO** : déployer la clé SSH sur ollama, monitor, dashy, homeassistant

---

### Versions et prérequis

| Techno | Version | Notes |
|:---|:---:|:---|
| Terraform | v1.15.6 | Sur la VM |
| Provider bpg/proxmox | v0.60.0 | TF provider |
| Ansible | core 2.19+ | Sur la VM |
| Python | 3.13 | Sur les cibles |
| Ollama | v0.30.10 | .10, CPU-only |
| Modèle par défaut | qwen2.5-coder:7b | Ollama |
| OS | Debian 13 | VMs clonées |
| Traefik | v3.x | .200 |
| AdGuard | latest | .202 |

---

### Secrets et accès

```
SSH key:  /workspace/.ssh/id_ed25519 (sans mot de passe)
WebUI:    admin / hermes (192.168.1.3:8787)
Proxmox:  token_id=root@pam!terraform + token_secret (dans terraform.tfvars)
Telegram: hasmi (1480745817), GATEWAY active
Ollama:   API locale sans clé (192.168.1.10:11434)
```

---

### OS Prompt ai-cli-v2.5 (flux)

```
User Input → Router → Intent → Planner → Dispatcher → Engine
```

- **Router** : détecte l'intention (commande, question, déploiement)
- **Intent** : classifie (VM, Ollama, Terraform, Ansible, DNS…)
- **Planner** : planifie les étapes
- **Dispatcher** : envoie à l'engine approprié
- **Engine** : exécute (SSH, API Ollama, Terraform CLI, Ansible-playbook…)

**État des Engines :**
- ✅ VM (SSH vers infra@192.168.1.3)
- ✅ Ollama (API 192.168.1.10:11434)
- ⚠️ Terraform → stubs (à compléter)
- ⚠️ Ansible → à intégrer comme engine

---

## 5. Mapping réseau

### VLAN / Réseau

```
Sous-réseau : 192.168.1.0/24
Domaine     : *.mysmihome.duckdns.org
Passerelle  : 192.168.1.1 (PVE)
DNS         : 192.168.1.202 (AdGuard) + 1.1.1.1
```

### Machines

| IP | Hostname | Service | Port(s) | Statut |
|:---|:---|:---|:---:|:---:|
| 192.168.1.1 | pve | Proxmox VE (hyperviseur) | 8006 | ✅ UP |
| 192.168.1.2 | homeassistant | Home Assistant OS | 8123 | ✅ UP |
| 192.168.1.3 | cockpit | Infra VM (Hermes WebUI) | 9090, 8787 | ✅ UP |
| 192.168.1.5 | casaos | CasaOS (NAS léger) | 80 | ✅ UP |
| 192.168.1.6 | portainer | Portainer (Docker mgmt) | 9443 | ✅ UP |
| 192.168.1.10 | ollama | Ollama LLM | 11434 | ✅ UP |
| 192.168.1.11 | cloud | (ancien, DOWN) | — | ❌ DOWN |
| 192.168.1.13 | dashy | Dashy (dashboard) | 80 | ✅ UP |
| 192.168.1.35 | monitor | Uptime-Kuma | 3001 | ✅ UP |
| 192.168.1.36 | prometheus | Prometheus | 9090 | ❌ DOWN |
| 192.168.1.37 | grafana | Grafana | 3000 | ❌ DOWN |
| 192.168.1.99 | test | (ancien test) | — | ❌ DOWN |
| 192.168.1.148 | test-905 | VM test active | 80 | ✅ UP |
| 192.168.1.200 | traefik | Traefik reverse proxy | 443, 80 | ✅ UP |
| 192.168.1.202 | adguard | AdGuard Home | 80 | ✅ UP |

### VMs Proxmox

| VMID | Nom | Statut | RAM | Disque |
|:---:|:---|:---:|:---:|:---:|
| 100 | win11-template | ❌ stopped | 4G | 64G |
| 101 | haos17-3-template | ❌ stopped | 2G | 32G |
| 102 | debian13-template | ❌ stopped | 4G | 10G |
| 114 | docker | ✅ running | 4G | 10G |
| 115 | Win11 | ❌ stopped | 4G | 64G |
| 119 | haos17-3 | ✅ running | 2G | 32G |
| 127 | infra-lab | ✅ running | 8G | 58G |
| 900 | debian12-template | ❌ stopped | 512M | — |
| 905 | test-905 | ✅ running | 512M | 10G |

---

## 6. Inventory Ansible

Fichier : `/home/infra/ansible-infra-lab2/inventory` (sur la VM)

```ini
[local]
localhost ansible_connection=local

[homelab]
traefik ansible_host=192.168.1.200
adguard ansible_host=192.168.1.202 traefik_domain="adguard.mysmihome.duckdns.org" traefik_port="80"

[supervision]
monitor ansible_host=192.168.1.35 traefik_domain="uptime.mysmihome.duckdns.org" traefik_port="3001"

[docker]
portainer ansible_host=192.168.1.6 traefik_domain="portainer.mysmihome.duckdns.org" traefik_port="9443"
casaos ansible_host=192.168.1.5 traefik_domain="cloud.mysmihome.duckdns.org" traefik_port="80"

[app]
dashy ansible_host=192.168.1.13 traefik_domain="dashy.mysmihome.duckdns.org" traefik_port="80"
homeassistant ansible_host=192.168.1.2 traefik_domain="homeassistant.mysmihome.duckdns.org" traefik_port="8123"

[system]
pve ansible_host=192.168.1.1 traefik_domain="homelab.mysmihome.duckdns.org" traefik_port="8006"
cockpit ansible_host=192.168.1.3 traefik_domain="cockpit.mysmihome.duckdns.org" traefik_port="9090"

[llm]
ollama ansible_host=192.168.1.10

[test-clean]
test-905 ansible_host=192.168.1.148 traefik_domain="test-905.mysmihome.duckdns.org" traefik_port="80"

[tous_mes_serveurs:children]
homelab
supervision
docker
app
system
llm
test-clean
```

---

## 7. Config Traefik — Tous les domaines

### Configs manuelles (PROTÉGÉES — ne pas toucher)

| Fichier | Domaine | Cible | Particularité |
|:---|:---|:---|:---|
| `cloud.yml` | `cloud.mysmihome.duckdns.org` | 192.168.1.11:80 | Pointe vers ancienne IP (DOWN) |
| `homelab.yml` | `homelab.mysmihome.duckdns.org` | 192.168.1.1:8006 | Avec `serversTransport: ignore-proxmox` |
| `uptime.yml` | `uptime.mysmihome.duckdns.org` | 192.168.1.35:3001 | — |

### Configs auto-générées

| Fichier | Domaine | Cible |
|:---|:---|:---|
| `adguard.yml` | `adguard.mysmihome.duckdns.org` | 192.168.1.202:80 |
| `cockpit.yml` | `cockpit.mysmihome.duckdns.org` | 192.168.1.3:9090 |
| `portainer.yml` | `portainer.mysmihome.duckdns.org` | 192.168.1.6:9443 |
| `dashy.yml` | `dashy.mysmihome.duckdns.org` | 192.168.1.13:80 |
| `homeassistant.yml` | `homeassistant.mysmihome.duckdns.org` | 192.168.1.2:8123 |
| `test-905.yml` | `test-905.mysmihome.duckdns.org` | 192.168.1.148:80 |

### Template du fichier Traefik

```yaml
http:
  routers:
    {{ item }}:
      rule: "Host(`{{ hostvars[item].traefik_domain }}`)"
      entryPoints:
        - websecure
      service: {{ item }}
      tls:
        certResolver: letsencrypt
  services:
    {{ item }}:
      loadBalancer:
        servers:
          - url: "http://{{ hostvars[item].ansible_host }}:{{ hostvars[item].traefik_port }}"
```

---

## 8. Cycle automatique

### Principe

1. **Terraform** crée une VM clone (bpg/proxmox)
2. **local-exec** nettoie les anciennes entrées dans inventory et insère la nouvelle
3. **local-exec** déclenche `ansible-playbook site.yml`
4. **Ansible** installe les paquets, configure SSH, Zsh, dotfiles
5. **Ansible** génère la config Traefik via template
6. **Traefik** reload (handlers)

### Pour lancer

```bash
# Sur la VM infra@192.168.1.3
cd /home/infra/infra-lab-tf

# Éditer terraform.tfvars — changer clone_vm_id
vim terraform.tfvars

# Vérifier
terraform validate
terraform plan -refresh=false

# Appliquer
terraform apply

# Détruire
terraform destroy
```

### Règles de nommage

```hcl
clone_prefix = "test"
clone_vm_id  = 906  # incrémenter à chaque fois
# Résultat : test-906
```

---

## 9. Terraform

### deploy-vm.tf

```hcl
resource "proxmox_virtual_environment_vm" "test_clone" {
  name      = "${var.clone_prefix}-${var.clone_vm_id}"
  node_name = var.proxmox_node
  vm_id     = var.clone_vm_id

  clone {
    vm_id = var.template_vm_id
  }

  agent {
    enabled = true
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Nettoyer les anciennes entrées pour ce nom AVANT d'écrire
      sed -i "/^${var.clone_prefix}-${var.clone_vm_id} /d" ~/ansible-infra-lab2/inventory

      # Construire la ligne complète (avec vars Traefik si présentes)
      LINE="${var.clone_prefix}-${var.clone_vm_id} ansible_host=${self.ipv4_addresses[1][0]}"
      if [ -n "${var.traefik_domain}" ] && [ -n "${var.traefik_port}" ]; then
        LINE="${LINE} traefik_domain=${var.traefik_domain} traefik_port=${var.traefik_port}"
      fi

      # Insérer sous [test-clean] dans inventory
      sed -i "/^\\[test-clean\\]/a\\${LINE}" ~/ansible-infra-lab2/inventory

      # Lancer Ansible automatiquement
      cd ~/ansible-infra-lab2 && ansible-playbook -i inventory site.yml
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = "sed -i \"/^${self.name} /d\" ~/ansible-infra-lab2/inventory"
  }
}
```

### variables.tf

```hcl
variable "proxmox_endpoint"  { type = string }
variable "proxmox_token_id"  { type = string }
variable "proxmox_token_secret" { type = string sensitive = true }
variable "proxmox_node"      { type = string default = "pve" }
variable "clone_prefix"      { type = string default = "test" }
variable "clone_vm_id"       { type = number }
variable "template_vm_id"    { type = number default = 900 }
variable "traefik_domain"    { type = string default = "" }
variable "traefik_port"      { type = string default = "" }
```

### terraform.tfvars

```hcl
proxmox_endpoint     = "https://192.168.1.1:8006/api2/json"
proxmox_token_id     = "root@pam!terraform"
proxmox_token_secret = "<SECRET>"
clone_prefix         = "test"
clone_vm_id          = 905
template_vm_id       = 900
traefik_domain       = "test-905.mysmihome.duckdns.org"
traefik_port         = "80"
```

---

## 10. Ansible

### Structure des rôles

```
ansible-infra-lab2/
├── playbook_first_install.yml   # 17 tasks : apt, base, dotfiles
├── playbook_traefik_config.yml  # Traefik dynamique intelligent
├── site.yml                     # Orchestrateur (4 plays)
├── inventory                    # Fichier unique (plus de hosts)
├── ansible.cfg
├── templates/
│   └── traefik-service.j2       # Template config Traefik
├── traefik/
│   ├── traefik.yaml             # Config statique Traefik
│   └── conf.d/                  # Configs de référence
├── roles/
│   ├── base/
│   │   └── tasks/main.yml       # apt update, paquets
│   └── dotfiles/
│       └── tasks/main.yml       # Zsh, variables dynamiques
└── group_vars/                  # (à créer si nécessaire)
```

### playbook_first_install.yml

```yaml
---
- name: Première installation — base + dotfiles
  hosts: all
  become: yes
  gather_facts: yes
  tasks:
    - name: Update apt cache
      apt: update_cache=yes cache_valid_time=3600
    - name: Install packages de base
      apt: name={{ item }} state=present
      loop:
        - curl, wget, git, vim, htop, net-tools
        - ca-certificates, gnupg, lsb-release
        - ufw, tmux, rsync, jq, unzip
    - name: Enable UFW
      ufw: state=enabled policy=allow
    - name: Config .zshrc
      template: src=dotfiles/zshrc.j2 dest=/root/.zshrc
      when: "'root' is defined"
```

### playbook_traefik_config.yml — Version intelligente

```yaml
---
- name: Déployer la configuration Traefik
  hosts: traefik
  become: yes
  tasks:
    - name: Récupérer les domaines déjà configurés
      shell: |
        grep -shE 'Host\(`[^`]+`\)' /etc/traefik/conf.d/*.yml 2>/dev/null \
          | sed 's/.*Host(`//;s/`).*//' || true
      register: existing_domains
      changed_when: false
      check_mode: no

    - name: Générer les fichiers pour les nouveaux domaines uniquement
      template:
        src: traefik-service.j2
        dest: "/etc/traefik/conf.d/{{ item }}.yml"
        owner: root
        group: root
        mode: '0644'
      loop: "{{ groups['all'] | difference(['traefik']) }}"
      when:
        - hostvars[item].traefik_domain is defined
        - hostvars[item].traefik_port is defined
        - hostvars[item].traefik_domain not in existing_domains.stdout_lines
      notify: restart traefik

  handlers:
    - name: restart traefik
      systemd: name=traefik state=restarted
```

> **✨ Intelligence :** si un domaine existe déjà dans un fichier `.yml` (même manuel),
> le playbook ne génère PAS de doublon. Tes configs manuelles sont protégées.

### site.yml

```yaml
---
- name: 1. Vérifier que la VM répond
  hosts: all
  gather_facts: no
  tasks:
    - name: Wait for SSH
      wait_for_connection: delay=5 timeout=120
    - name: Python disponible
      raw: test -e /usr/bin/python3 || apt install -y python3
      become: yes

- name: 2. Base — paquets essentiels
  import_playbook: playbook_first_install.yml

- name: 3. Dotfiles
  hosts: all
  become: yes
  tasks:
    - name: Configurer dotfiles
      include_role: name=dotfiles

- name: 4. Traefik — config dynamique
  import_playbook: playbook_traefik_config.yml
```

---

## 11. OS Prompt

### Flux ai-cli-v2.5

```
[User Input]
    │
    ▼
┌─────────┐
│ Router   │  ← Détecte l'intention
└────┬────┘
     │
     ▼
┌─────────┐
│ Intent   │  ← Classifie (VM, Ollama, TF, etc.)
└────┬────┘
     │
     ▼
┌──────────┐
│ Planner   │  ← Planifie les étapes
└────┬─────┘
     │
     ▼
┌──────────┐
│ Dispatcher│  ← Envoie à l'engine
└────┬─────┘
     │
     ▼
┌──────────┐
│ Engine    │  ← Exécute (VM=SSH, Ollama=API, Terraform=TF)
└──────────┘
```

**État des Engines :**
- ✅ VM (SSH vers infra@192.168.1.3) → OK
- ✅ Ollama (API 192.168.1.10:11434) → OK
- ⚠️ Terraform / Proxmox → stubs (à implémenter)
- ⚠️ Ansible → à intégrer

---

## 12. Todos & évolutions

### Fait (2026-06-26)

- [x] Cycle TF→Ansible→Traefik validé sur VM test-905
- [x] Naming dynamique `${clone_prefix}-${vm_id}` (plus de doublons)
- [x] Inventory Ansible complet — toutes les machines UP
- [x] Traefik config intelligent — skip les domaines existants
- [x] AdGuard intégré dans le cycle
- [x] Base Ansible (apt, UFW, dotfiles) appliqué sur 7 machines

### À faire

- [ ] **Ollama & Monitor** — déployer la clé SSH (Permission denied)
- [ ] **Dashy, Home Assistant** — déployer la clé SSH
- [ ] **Vault** — gérer les secrets proprement
- [ ] **Migration inventory** — group_vars par groupe (au lieu de vars inline)
- [ ] **Migration `hosts` → `inventory` seul** — ✅ fait, reste à vérifier aucun résidu
- [ ] **Monitoring** — Prometheus/Grafana si demandé
- [ ] **Engine Ansible** dans OS Prompt → dispatcher déclenche site.yml
- [ ] **Dashboard 9119** — consolider ou supprimer (conserver au cas où)

---

*Fin du document — généré par Hermes Agent, session du 2026-06-26*

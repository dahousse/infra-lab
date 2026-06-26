# 🔄 Cycle TF → Ansible → Traefik (I1)

> Documentation complète du cycle de déploiement automatisé d'une VM sur INFRA LAB.
> **Domaine** : `*.mysmihome.duckdns.org` | **Repos** : `infra-lab-tf`, `ansible-infra-lab2`, `infra-lab`

---

## 📋 Résumé

| Étape | Techno | Action |
|:---|:---|---|
| 1 | **Terraform** (bpg/proxmox) | Clone template 102 → nouvelle VM |
| 2 | **local-exec** | Ajoute la VM dans l'inventory Ansible |
| 3 | **local-exec** | Attend SSH (60s, 30 tentatives) |
| 4 | **Ansible** `playbook_first_install.yml` | User infra, sudo, SSH, Zsh, paquets |
| 5 | **Ansible** `playbook_traefik_config.yml` | Route Traefik + cert SSL Let's Encrypt |
| ⬇️ | **Destroy** | Nettoie inventory + conf Traefik + reload |

**Durée** : ~30 secondes pour 1 VM.

---

## 🚀 Déploiement complet

```bash
cd ~/infra-lab-tf

terraform apply \
  -var="clone_prefix=test" \
  -var="clone_vm_id=906" \
  -var="template_vm_id=102" \
  -var="vm_cpus=2" \
  -var="vm_memory=2048" \
  -var="traefik_domain=test-906.mysmihome.duckdns.org" \
  -var="traefik_port=80" \
  -auto-approve
```

### Détail des étapes

#### 1. Clone Proxmox
```hcl
resource "proxmox_vm_qemu" "clone" {
  count     = var.clone_vm_id != "" ? 1 : 0
  clone     = var.template_vm_id  # 102 = Debian 13
  name      = "${var.clone_prefix}-${var.clone_vm_id}"
  ...
}
```

#### 2. Inventory Ansible (local-exec)
```bash
# Ajoute au fichier inventory (une ligne)
sed -i '/^\[infra\]/a test-906 ansible_host=192.168.1.150 traefik_domain=... traefik_port=80'
```

#### 3. Wait SSH (local-exec)
```bash
for i in $(seq 1 30); do
  ssh -o StrictHostKeyChecking=no root@192.168.1.150 "uptime" && break
  sleep 2
done
```

#### 4. First Install (Ansible)
```bash
ansible-playbook -i ~/ansible-infra-lab2/inventory \
  ~/ansible-infra-lab2/playbook_first_install.yml \
  --limit test-906
```
Installe :
- User `infra` + sudo NOPASSWD
- Clés SSH
- Zsh + Oh My Zsh
- Paquets (curl, git, htop, etc.)

#### 5. Traefik Config (Ansible)
```bash
ansible-playbook -i ~/ansible-infra-lab2/inventory \
  ~/ansible-infra-lab2/playbook_traefik_config.yml \
  --limit test-906
```
Génère :
- `/etc/traefik/conf.d/test-906.yml` sur Traefik (.200)
- Route HTTP → `test-906.mysmihome.duckdns.org`
- Certificat Let's Encrypt automatique
- **Reload graceful** : `systemctl kill -s USR1 traefik`

---

## 🗑️ Destruction propre

```bash
cd ~/infra-lab-tf
terraform destroy -auto-approve
```

Le destroy nettoie automatiquement :
| Action | Détail |
|:---|---|
| VM Proxmox | Détruite par le provider |
| Inventory Ansible | Ligne `test-906` retirée |
| Conf Traefik | `rm -f /etc/traefik/conf.d/test-906.yml` |
| Reload Traefik | `systemctl kill -s USR1 traefik` |

---

## ⚙️ Variables Terraform

| Variable | Default | Description |
|:---|---:|:---|
| `clone_prefix` | `"vm"` | Préfixe du nom (ex: test, app) |
| `clone_vm_id` | — | ID de la VM + nom `${prefix}-${id}` |
| `template_vm_id` | — | Template Proxmox (102 = Debian 13) |
| `vm_cpus` | `1` | CPU cores |
| `vm_memory` | `512` | RAM MB |
| `traefik_domain` | `""` | Domaine complet (optionnel) |
| `traefik_port` | `""` | Port du service (optionnel) |
| `proxmox_password` | (sensitive) | API Proxmox |
| `lxc_root_password` | (sensitive) | Root VM |

---

## 🚦 Règles Traefik

### Configs manuelles protégées
Ne **JAMAIS** toucher ces fichiers :
- `cloud.yml` — Nextcloud
- `homelab.yml` — Proxmox
- `uptime.yml` — Uptime Kuma

### Reload
```bash
# Reload graceful (pas de restart brutal)
systemctl kill -s USR1 traefik
```
Ne pas utiliser `systemctl restart traefik` (casse les connexions actives).

---

## ✅ CI/CD — GitHub Actions

| Workflow | Repo | Runner |
|:---|:---|---|
| `terraform-validate.yml` | `infra-lab-tf` | ubuntu-latest (cloud) |
| `terraform-plan.yml` | `infra-lab-tf` | self-hosted (VM) |
| `ansible-lint.yml` | `ansible-infra-lab2` | ubuntu-latest (cloud) |
| `ansible-dry-run.yml` | `ansible-infra-lab2` | self-hosted (VM) |

Triggers : push sur `main`/`master` + PR.

---

## 📁 Structure des repos

```
/workspace/
├── infra-lab-tf/             ← Terraform Proxmox
│   ├── deploy-vm.tf          # Ressource VM + local-exec cycle
│   ├── variables.tf          # Variables paramétrables
│   ├── outputs.tf            # Outputs (IP, hostname)
│   └── .github/workflows/    # CI/CD workflows
│
├── ansible-infra-lab2/       ← Ansible
│   ├── inventory             # Inventaire unique
│   ├── playbook_first_install.yml
│   ├── playbook_traefik_config.yml
│   ├── playbook_*.yml        # Autres playbooks
│   ├── roles/                # Rôles réutilisables
│   └── .github/workflows/    # CI/CD workflows
│
└── infra-lab/                ← Monorepo OS Prompt + Docs
    ├── docs/                 # Documentation
    │   ├── AGENTS.md         # Contexte projet (Hermes)
    │   ├── cycle-tf-ansible-traefik.md  # ← Ce fichier
    │   └── kanban-infra-lab.html
    └── tools/ai-cli-v2/      # OS Prompt ai-cli-v2
```

---

## 🧠 Bonnes pratiques

- **Naming** : `test-${vm_id}` (incrémental)
- **Inventory** : un seul fichier `inventory` (plus de `hosts`)
- **SSH** : clé `/workspace/.ssh/id_ed25519` — `infra@192.168.1.3`
- **Versionning** : tag git à la fin de chaque Goal (`v0.x.0`)
- **Kanban** : mis à jour automatiquement après chaque tâche

---

---

## 🏷️ Versionning

À la fin de chaque **Goal** terminé, un tag git est créé sur **les 3 repos** :

```bash
# Exemple : v0.4.0 (Goal I1)
cd ~/infra-lab        && git tag -a v0.4.0 -m "I1: cycle TF→Ansible→Traefik" && git push origin v0.4.0
cd ~/infra-lab-tf     && git tag -a v0.4.0 -m "I1: ..." && git push origin v0.4.0
cd ~/ansible-infra-lab2 && git tag -a v0.4.0 -m "I1: ..." && git push origin v0.4.0
```

| Version | Goal | Date |
|:---|---:|:---|
| v0.4.0 | I1 — Cycle TF→Ansible→Traefik | 2026-06-26 |
| v0.3.0 | E2 — Prometheus/Grafana | 2026-06-25 |
| v0.2.0 | E3 — CI/CD | 2026-06-25 |

*INFRA LAB — Hasmi © 2026*

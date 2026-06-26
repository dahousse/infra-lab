# 🧠 INFRA LAB — Monorepo

> Documentation, OS Prompt ai-cli-v2 et outils pour l'infrastructure homelab.
> **Domaine** : `*.mysmihome.duckdns.org`

## 📁 Structure

```
infra-lab/
├── docs/                     # Base documentaire
│   ├── AGENTS.md             # Contexte projet (Hermes Agent)
│   ├── cycle-tf-ansible-traefik.md  # Cycle déploiement VM
│   ├── context-infra-lab.md  # Contexte complet généré
│   └── kanban-infra-lab.html # Tableau Kanban
├── tools/
│   ├── ai-cli-v2/            # OS Prompt Router → Intent → Engine
│   └── ai-cli/               # V1 legacy
├── .github/workflows/        # CI/CD (validate playbooks)
└── README.md                 # Ce fichier
```

## 🗺️ Repos du projet

| Repo | Rôle |
|:---|---|
| `infra-lab` | 📚 Documentation + OS Prompt ai-cli-v2 |
| `infra-lab-tf` | 🧱 Terraform Proxmox (deploy-vm.tf) |
| `ansible-infra-lab2` | ⚙️ Ansible (playbooks, rôles) |

## 🔄 Cycle TF → Ansible → Traefik

```bash
cd ~/infra-lab-tf
terraform apply -auto-approve \
  -var="clone_vm_id=906" \
  -var="template_vm_id=102" \
  -var="traefik_domain=app-906.mysmihome.duckdns.org" \
  -var="traefik_port=80"
```

→ Clone → Ansible setup → Traefik route en **30 secondes**.

Doc : [`docs/cycle-tf-ansible-traefik.md`](cycle-tf-ansible-traefik.md)

## 🧠 OS Prompt ai-cli-v2

```
User → Router → Intent → Planner → Dispatcher → Engine
```

Engines : VM, Ollama, Proxmox, Terraform.

## 🏷️ Versionning

| Tag | Goal | Date |
|:---|---:|:---|
| v0.4.0 | I1 — Cycle TF→Ansible→Traefik | 2026-06-26 |
| v0.3.0 | E2 — Prometheus/Grafana | 2026-06-25 |
| v0.2.0 | E3 — CI/CD | 2026-06-25 |

---

*INFRA LAB — Hasmi © 2026*

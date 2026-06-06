# 🏰 infra-lab

**Laboratoire d'Infrastructure as Code pour mon homelab.**

Ce dépôt contient l'ensemble des playbooks Ansible et des fichiers Terraform pour provisionner, configurer et maintenir mon infrastructure sur Proxmox.

## 🗺️ Architecture du dépôt
Playbooks Ansible pour Prometheus, Node Exporter et Grafana

## 🚀 Services Déployés

| Service | URL | Statut |
|---------|-----|--------|
| Traefik | `https://traefik.mysmihome.duckdns.org` | ✅ OK |
| Dashy | `https://dashy.mysmihome.duckdns.org` | ✅ OK |
| AdGuard Home | `https://adguard.mysmihome.duckdns.org` | ✅ OK |
| Home Assistant | `https://homeassistant.mysmihome.duckdns.org` | ✅ OK |
| Nextcloud | `https://cloud.mysmihome.duckdns.org` | ✅ OK |
| Proxmox | `https://homelab.mysmihome.duckdns.org` | ✅ OK |
| Portainer | `https://portainer.mysmihome.duckdns.org` | ✅ OK |
| Uptime Kuma | `https://uptime.mysmihome.duckdns.org` | ✅ OK |
| Prometheus | `http://192.168.1.36:9090` | ✅ OK |
| Grafana | `https://grafana.mysmihome.duckdns.org` | ✅ OK |

## 🛠️ Technologies utilisées

- **Hyperviseur** : Proxmox VE
- **Reverse Proxy** : Traefik avec Let's Encrypt (DNS Challenge DuckDNS)
- **Conteneurisation** : Docker, LXC
- **Configuration Management** : Ansible
- **Provisionnement** : Terraform
- **Supervision** : Prometheus, Grafana, Uptime Kuma, Glances
- **Sécurité** : Ansible Vault, WireGuard
- **CI/CD** : GitHub Actions

## 📋 Playbooks Ansible

| Playbook | Description |
|----------|-------------|
| `playbook_base.yml` | Configuration de base (outils, logs, sécurité) |
| `playbook_node_exporter.yml` | Déploiement de Node Exporter |
| `playbook_prometheus.yml` | Installation de Prometheus |
| `playbook_grafana.yml` | Installation de Grafana |
| `playbook_nextcloud.yml` | Installation de Nextcloud |
| `playbook_uptimekuma.yml` | Déploiement d'Uptime Kuma |
| `playbook_glances.yml` | Déploiement de Glances |
| `playbook_backup.yml` | Sauvegarde Proxmox via API |
| `playbook_zsh.yml` | Configuration Zsh, Oh My Zsh, fastfetch |
| `playbook_traefik_config.yml` | Déploiement de la configuration Traefik |
| `playbook_pull.yml` | Amorce pour `ansible-pull` |

## 🚀 Utilisation

### Déploiement complet

```bash
ansible-playbook -i ansible/hosts ansible/site.yml
cd terraform
terraform apply
🔧 Maintenance
Sauvegarde du code : un script cron pousse le dépôt chaque soir à 22h.

Sauvegarde des VMs : playbook playbook_backup.yml (à programmer).

Supervision : Uptime Kuma surveille tous les services en continu.

📝 Notes
Les secrets sont chiffrés avec Ansible Vault (secret.vault.yml).

Le fichier terraform.tfvars est exclu du dépôt (via .gitignore).

L'inventaire Ansible est structuré par groupes (homelab, supervision, nextcloud_host, etc.).

👤 Auteur
Dahousse - Passionné d'infrastructure et d'automatisation.

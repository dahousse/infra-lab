# 🏰 infra-lab

**Laboratoire d'Infrastructure as Code pour mon homelab.**

Ce dépôt contient l'ensemble des playbooks Ansible et des fichiers Terraform pour provisionner, configurer et maintenir mon infrastructure sur Proxmox.

---

## 🗺️ Architecture du dépôt
infra-lab/
├── ansible/ # Playbooks et configurations Ansible
│ ├── playbooks/ # Playbooks individuels
│ ├── group_vars/ # Variables par groupe d'inventaire
│ ├── hosts # Inventaire des machines
│ ├── site.yml # Playbook principal d'orchestration
│ └── traefik/ # Configuration Traefik
├── terraform/ # Fichiers Terraform pour provisionner Proxmox
│ ├── main.tf # Ressources principales (test)
│ ├── nextcloud.tf # Provisionnement du conteneur Nextcloud
│ └── secret.vault.yml # Secrets chiffrés avec Ansible Vault
├── .github/workflows/ # CI/CD avec GitHub Actions
└── README.md # Ce fichier

text

---

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

---

## 🛠️ Technologies utilisées

| Domaine | Outils |
|---------|--------|
| 🏗️ Hyperviseur | Proxmox VE |
| 🌐 Reverse Proxy | Traefik avec Let's Encrypt (DNS Challenge DuckDNS) |
| 📦 Conteneurisation | Docker, LXC |
| ⚙️ Configuration Management | Ansible |
| 🧱 Provisionnement | Terraform |
| 📊 Supervision | Prometheus, Grafana, Uptime Kuma, Glances |
| 🔒 Sécurité | Ansible Vault, WireGuard |
| 🚦 CI/CD | GitHub Actions |

---

## 📋 Playbooks Ansible

| Playbook | Description |
|----------|-------------|
| `playbook_base.yml` | 🧰 Configuration de base (outils, logs, sécurité) |
| `playbook_node_exporter.yml` | 📡 Déploiement de Node Exporter |
| `playbook_prometheus.yml` | 📈 Installation de Prometheus |
| `playbook_grafana.yml` | 📉 Installation de Grafana |
| `playbook_nextcloud.yml` | ☁️ Installation de Nextcloud |
| `playbook_uptimekuma.yml` | 🛎️ Déploiement d'Uptime Kuma |
| `playbook_glances.yml` | 🔍 Déploiement de Glances |
| `playbook_backup.yml` | 💾 Sauvegarde Proxmox via API |
| `playbook_zsh.yml` | 🐚 Configuration Zsh, Oh My Zsh, screenfetch |
| `playbook_traefik_config.yml` | 🚦 Déploiement de la configuration Traefik |
| `playbook_pull.yml` | 🧲 Amorce pour `ansible-pull` |

---

## 🚀 Utilisation

### 🎯 Déploiement complet

```bash
ansible-playbook -i ansible/hosts ansible/site.yml
🧱 Terraform
bash
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
🔑 Secrets
Les secrets sont lus depuis Ansible Vault :

secret.vault.yml

vault_pass.txt

Les fichiers locaux sensibles ou générés ne doivent pas être commités :

secret.vault.yml

vault_pass.txt

terraform.tfvars

.terraform/

*.tfstate

🧭 Guide de Poche Ansible
🚀 Commandes de Base
Lancer un playbook sur toutes les machines

bash
ansible-playbook -i hosts site.yml
Lancer un playbook spécifique

bash
ansible-playbook -i hosts playbook_base.yml
ansible-playbook -i hosts playbook_zsh.yml
ansible-playbook -i hosts playbook_node_exporter.yml
Vérifier la syntaxe d’un playbook sans l’exécuter

bash
ansible-playbook -i hosts playbook_base.yml --syntax-check
Simuler l’exécution d’un playbook (dry-run)

bash
ansible-playbook -i hosts playbook_base.yml --check
🎯 Cibler une Seule Machine
Lancer un playbook sur une machine spécifique

bash
ansible-playbook -i hosts playbook_zsh.yml --limit cockpit
ansible-playbook -i hosts playbook_base.yml --limit traefik
Exécuter une commande ad-hoc sur une machine

bash
ansible cockpit -i hosts -m ping
ansible traefik -i hosts -m shell -a "uptime"
ansible adguard -i hosts -m apt -a "name=htop state=present"
🛠️ Commandes Utiles
Rafraîchir le cache APT d’une machine

bash
ansible traefik -i hosts -m apt -a "update_cache=yes"
Redémarrer un service sur une machine

bash
ansible traefik -i hosts -m systemd -a "name=nginx state=restarted"
Vérifier l’espace disque de toutes les machines

bash
ansible tous_mes_serveurs -i hosts -m shell -a "df -h /"
Lister toutes les machines de l’inventaire

bash
ansible-inventory -i hosts --list
🔐 Gestion des Clés SSH
Copier sa clé publique sur une nouvelle machine

bash
ssh-copy-id root@192.168.1.X
Tester la connexion SSH sans mot de passe

bash
ssh root@192.168.1.X hostname
📋 Notes Personnelles
Inventaire : situé dans ansible/hosts.

Playbooks : tous les fichiers .yml dans ansible/.

Site : site.yml orchestre le déploiement complet.

Limiter les cibles : utiliser --limit <nom_machine> pour éviter d’affecter toute la flotte.

🔧 Maintenance
Sauvegarde du code : un script cron pousse le dépôt chaque soir à 22h.

Sauvegarde des VMs : playbook playbook_backup.yml (à programmer).

Supervision : Uptime Kuma surveille tous les services en continu.

📝 Notes
Les secrets sont chiffrés avec Ansible Vault (secret.vault.yml).

Le fichier terraform.tfvars est exclu du dépôt via .gitignore.

L'inventaire Ansible est structuré par groupes (homelab, supervision, nextcloud_host, etc.).

👤 Auteur
Hasmi - Passionné d'infrastructure et d'automatisation.

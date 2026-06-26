def run():
    print("""
ai CLI v2.5 - INFRA LAB

Commandes directes:
  ai help               Affiche cette aide
  ai doctor             Verifie la connexion Ollama
  ai models             Liste les modeles Ollama
  ai system             Infos systeme
  ai list vms           Liste les VMs Proxmox
  ai create vm <nom>    Clone rapide d'une VM (template 102)
  ai delete vm <id>     Supprime une VM
  ai <message>          Chat avec Ollama (fallback)

Options create vm:
  --template <id>       Template a cloner (defaut: 102)
  --cpus <n>            Nombre de CPU
  --memory <mb>         RAM en MB
  --traefik <domaine>   Domaine Traefik (ex: monapp.mysmihome.duckdns.org)
  --port <port>         Port interne pour Traefik
  --group <groupe>      Groupe d'inventory Ansible (defaut: test-clean)
  --no-ansible          Sans provisioning Ansible
""")
# ai-cli-v2 — OS Prompt CLI

**INFRA LAB** — Gestion de VMs Proxmox via CLI + LLM.

## Installation

```bash
pip install -e .
```

## Utilisation

```bash
# Aide
ai help

# Vérifier la connexion Ollama
ai doctor

# Lister les modèles Ollama
ai models

# Infos système
ai system

# Lister les VMs
ai list vms

# Cloner une VM depuis le template
ai create vm test-906 --cpus 2 --memory 4096
ai create vm app-200 --traefik app.mysmihome.duckdns.org --port 3000

# Démarrer/Arrêter/Supprimer une VM
ai start vm 126
ai stop vm 126
ai delete vm 126

# Plan Terraform (prévisualisation)
ai plan vm

# Chat avec Ollama (fallback)
ai "dis moi un truc marrant"
```

## Architecture

```
ai                    → Entrypoint
cli_ai/main.py        → CLI parser (argparse)
core/
  intent.py           → NL intent extraction (FR/EN)
  planner.py          → Intent → Plan
  router.py           → Plan → Dispatch
  dispatcher.py       → Plan → Engine routing
  client.py           → Ollama API client
  config.py           → YAML config loader
  errors.py           → Custom exceptions
engines/
  proxmox.py          → VM clone/list/start/stop/delete
  vm.py               → VM engine wrapper
  terraform.py        → Terraform plan/apply/destroy
  ollama.py           → Ollama chat/models
commands/
  run.py              → Main runner
  help.py             → Help text
  doctor.py           → Ollama health check
  models.py           → List Ollama models
  system.py           → System info
utils_ai/
  logger.py           → Logging (/tmp/ai-cli.log)
  format.py           → Output formatting (JSON/text)
  output.py           → Response formatter
  output_layer.py     → Success/fail wrappers
config/
  config.yaml         → Ollama endpoint + model config
```

## Configuration

```yaml
# config/config.yaml
endpoint: http://192.168.1.10:11434
default_model: qwen2.5-coder:7b
timeout: 120
```

## Dépendances

- Python 3.10+
- requests, pyyaml, psutil
- SSH clé vers root@192.168.1.1 (Proxmox)
- Ansible dans ~/ansible-infra-lab2

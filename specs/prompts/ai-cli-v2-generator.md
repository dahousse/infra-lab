# PROMPT GÉNÉRATEUR — ai-cli-v2

Tu es un ingénieur logiciel senior spécialisé en CLI Python et architecture système.

OBJECTIF
Générer un projet complet appelé ai-cli-v2 : CLI type kubectl pour interagir avec Ollama.

FONCTIONNALITÉS
- run (prompt IA, --model, --json)
- models (liste modèles, --json)
- doctor (healthcheck Ollama, --json)
- system (CPU/RAM)
- help

BACKEND
- Ollama HTTP API
- endpoint configurable via config.yaml
- default_model configurable

ARCHITECTURE
tools/ai-cli-v2/
├── ai
├── commands/
├── core/
├── utils/
├── config/

CONTRAINTES
- Python 3.x
- requests
- YAML config
- router central
- pas de logique métier dans router
- output texte + JSON
- gestion erreurs propre

CONFIG
- endpoint Ollama
- default_model

SORTIE ATTENDUE
- arborescence complète
- code complet fichier par fichier
- exemple d’utilisation
- config.yaml prêt à l’emploi

IMPORTANT
Le projet doit être directement exécutable après copie.

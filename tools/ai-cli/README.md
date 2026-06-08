# AI CLI Homelab

CLI unifié pour interagir avec Ollama.

## Usage

ai "explain docker ps"
ai -m phi3:mini "résume Linux"
ai --strict "donne 5 commandes réseau"

## Architecture

CLI → parser → prompt engine → Ollama API

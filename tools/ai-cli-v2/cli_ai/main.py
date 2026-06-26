"""Point d'entrée du CLI ai — parse les arguments et affiche le résultat."""

import sys
import json
from commands.run import run


def _format_output(result: dict) -> str:
    """Formate la sortie selon l'engine utilisé."""
    engine = result.get("engine", "")
    data = result.get("data", {})

    if result.get("status") == "error":
        return f"[{engine}] ⚠ Erreur : {result.get('error', 'inconnue')}"

    # Ollama chat — juste la réponse
    if engine == "ollama" and "response" in data:
        return data["response"]

    # Ollama models
    if engine == "ollama" and "models" in data:
        lines = [f"🤖 {data['count']} modèles disponibles :"]
        for m in data["models"]:
            lines.append(f"  - {m}")
        return "\n".join(lines)

    # Proxmox VMs
    if engine == "proxmox" and "vms" in data:
        lines = [f"🖥️  {len(data['vms'])} VMs :"]
        for vm in data["vms"]:
            status = "🟢" if vm["status"] == "running" else "🔴"
            lines.append(f"  {status} {vm['vmid']:>4}  {vm['name']:<20} {vm['status']}")
        return "\n".join(lines)

    # Proxmox containers
    if engine == "proxmox" and "containers" in data:
        lines = [f"📦 {len(data['containers'])} conteneurs LXC :"]
        for ct in data["containers"]:
            status = "🟢" if ct["status"] == "running" else "🔴"
            lines.append(f"  {status} {ct['vmid']:>4}  {ct['name']:<20} {ct['status']}")
        return "\n".join(lines)

    # Proxmox VM status détaillé
    if engine == "proxmox" and "vm_status" in data:
        lines = [f"📊 Statut de la VM :"]
        for k, v in data["vm_status"].items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    # Fallback
    return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    prompt = " ".join(sys.argv[1:])
    if not prompt:
        print("Usage: ai <prompt>")
        print("Exemple: ai \"liste les vms\"")
        return

    result = run(prompt)
    print(_format_output(result))


if __name__ == "__main__":
    main()

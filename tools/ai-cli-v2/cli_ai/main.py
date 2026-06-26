"""Point d'entree du CLI ai — parse les arguments et affiche le resultat."""

import sys
import json
from commands.run import run
from commands import help as cmd_help
from commands import doctor as cmd_doctor
from commands import models as cmd_models


def _format_output(result: dict) -> str:
    """Formate la sortie selon l'engine utilise."""
    engine = result.get("engine", "")
    data = result.get("data", {})

    if result.get("status") == "error":
        return f"[{engine}] c Erreur : {result.get('error', 'inconnue')}"

    # Ollama chat — juste la reponse
    if engine == "ollama" and "response" in data:
        return data["response"]

    # Ollama models
    if engine == "ollama" and "models" in data:
        lines = [f"O {data['count']} modeles disponibles :"]
        for m in data["models"]:
            lines.append(f"  - {m}")
        return "\n".join(lines)

    # VM engine (clone/create/list)
    if engine == "vm":
        if "steps" in data:
            vm = data.get("vm", {})
            lines = [f"Creation de la VM {vm.get('name', vm.get('id', ''))} :"]
            icon_ok = "OK"
            icon_run = ">>"
            icon_fail = "XX"
            for s in data["steps"]:
                icon = icon_ok if s["status"] == "ok" else icon_run if s["status"] == "running" else icon_fail
                detail = s.get("detail", "")
                lines.append(f"  {icon} {s['step']}: {detail}")
            if "ansible" in data and data["ansible"]:
                lines.append("  Ansible :")
                for a in data["ansible"]:
                    icon = icon_ok if a["status"] == "ok" else icon_fail
                    lines.append(f"    {icon} {a['play']}")
            if data.get("status") == "error":
                lines.append(f"  XX Erreur : {data.get('error', 'inconnue')}")
            return "\n".join(lines)
        if "vms" in data:
            lines = [f"VMs ({data['count']}) :"]
            for vm in data["vms"]:
                status = "RUN" if vm["status"] == "running" else "STOP"
                lines.append(f"  {status} {vm['vmid']:>4}  {vm['name']:<20} {vm['status']}")
            return "\n".join(lines)
        if "message" in data:
            return f"OK {data['message']}"

    # Fallback
    return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    args = sys.argv[1:]
    if not args:
        cmd_help.run()
        return

    prompt = " ".join(args)

    # Direct commands (bypass AI router)
    direct_cmd = args[0].lower()
    if direct_cmd == "help":
        cmd_help.run()
        return
    if direct_cmd == "doctor":
        result = cmd_doctor.run()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    if direct_cmd == "models":
        result = cmd_models.run()
        if isinstance(result, dict):
            lines = [f"O {len(result.get('models', []))} modeles :"]
            for m in result.get("models", []):
                lines.append(f"  - {m}")
            print("\n".join(lines))
        else:
            print(result)
        return
    if direct_cmd == "system":
        from commands.system import run as sys_run
        sys_run()
        return

    # AI routing
    result = run(prompt)
    print(_format_output(result))


if __name__ == "__main__":
    main()

"""Dispatcher — routes plan to the right engine"""

from engines.vm import create_vm, list_vm
from engines.ollama import ask
from utils_ai.output_layer import wrap


def dispatch(plan: dict):
    engine = plan.get("engine", "ollama")
    action = plan.get("action", "chat")
    params = plan.get("params", {})
    raw_prompt = plan.get("raw_prompt", "")

    if engine == "vm":
        if action == "create_vm":
            result = create_vm(plan)
        elif action == "list_vm":
            result = list_vm(plan)
        elif action == "delete_vm":
            from engines.proxmox import stop_vm, delete_vm
            vm_id = params.get("vm_id")
            try:
                if vm_id:
                    stop_vm(vm_id)
                    delete_vm(vm_id)
                    result = {"status": "ok", "message": f"VM {vm_id} supprimee"}
                else:
                    result = {"status": "error", "error": "vm_id requis"}
            except Exception as e:
                result = {"status": "error", "error": str(e)}
        else:
            result = create_vm(plan)
        return wrap("vm", result)

    if engine == "docker":
        return wrap("docker", {"message": "not implemented yet"})

    # Fallback: Ollama chat (use raw_prompt if available)
    try:
        chat_prompt = raw_prompt if raw_prompt else str(plan)
        result = ask(chat_prompt)
        return wrap("ollama", result)
    except Exception as e:
        return wrap("ollama", error=str(e))

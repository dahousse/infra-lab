"""Dispatcher — routes plan to the right engine"""

from engines.vm import create_vm, list_vm
from engines.ollama import ask
from utils_ai.output_layer import wrap
import os, subprocess


def _clean_inventory(name: str):
    if name and os.path.exists(os.path.expanduser("~/ansible-infra-lab2/inventory")):
        subprocess.run(["sed", "-i", f"/^{name} /d",
                        os.path.expanduser("~/ansible-infra-lab2/inventory")],
                       capture_output=True)


def dispatch(plan: dict):
    engine = plan.get("engine", "ollama")
    action = plan.get("action", "chat")
    params = plan.get("params", {})
    raw_prompt = plan.get("raw_prompt", "")

    # VM engine
    if engine == "vm":
        if action == "create_vm":
            result = create_vm(plan)
        elif action == "list_vm":
            result = list_vm(plan)
        elif action == "start_vm":
            from engines.proxmox import start_vm
            vm_id = params.get("vm_id")
            name = params.get("name", "?")
            try:
                if vm_id:
                    start_vm(vm_id)
                    result = {"status": "ok", "message": f"VM {vm_id} ({name}) demarree"}
                else:
                    result = {"status": "error", "error": "vm_id requis"}
            except Exception as e:
                result = {"status": "error", "error": str(e)}
        elif action == "delete_vm":
            from engines.proxmox import stop_vm, delete_vm as prox_delete
            vm_id = params.get("vm_id")
            vm_name = params.get("name", "")
            try:
                if vm_id:
                    stop_vm(vm_id)
                    prox_delete(vm_id)
                    msg = f"VM {vm_id} supprimee"
                    _clean_inventory(vm_name)
                    result = {"status": "ok", "message": msg}
                else:
                    result = {"status": "error", "error": "vm_id requis"}
            except Exception as e:
                result = {"status": "error", "error": str(e)}
        else:
            result = create_vm(plan)
        return wrap("vm", result)

    # Terraform engine
    if engine == "terraform":
        from engines.terraform import handle as tf_handle
        result = tf_handle(plan, raw_prompt)
        return wrap("terraform", result)

    # Docker engine
    if engine == "docker":
        return wrap("docker", {"message": "not implemented yet"})

    # Fallback: Ollama chat
    try:
        chat_prompt = raw_prompt if raw_prompt else str(plan)
        result = ask(chat_prompt)
        return wrap("ollama", result)
    except Exception as e:
        return wrap("ollama", error=str(e))

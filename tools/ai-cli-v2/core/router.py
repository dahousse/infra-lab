# core/router.py

from commands.run import run_vm
from commands.help import help_cmd
from commands.doctor import doctor_cmd

def route(prompt: str):
    p = prompt.lower().strip()

    if p.startswith("run "):
        return run_vm(prompt)

    if p in ["help", "--help", "-h"]:
        return help_cmd()

    if p.startswith("doctor"):
        return doctor_cmd()

    return f"[router] unknown intent: {prompt}"
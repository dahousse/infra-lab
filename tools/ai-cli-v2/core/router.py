"""Routeur — transforme un prompt en intention → plan → exécution."""

from core.intent import extract_intent
from core.planner import build_plan
from core.dispatcher import dispatch


def route(prompt: str):
    """Point d'entrée : analyse le prompt, planifie, dispatche."""

    if not prompt or not prompt.strip():
        return {"status": "error", "error": "empty prompt"}

    intent = extract_intent(prompt)
    plan = build_plan(intent)
    result = dispatch(plan, prompt)

    return result

from core.intent import extract_intent
from core.planner import build_plan
from core.dispatcher import dispatch


def route(prompt: str):
    print("[ROUTER ACTIVE]")

    if not prompt or not prompt.strip():
        return {"status": "error", "error": "empty prompt"}

    intent = extract_intent(prompt)
    plan = build_plan(intent)
    result = dispatch(plan)

    return result
from core.intent import extract_intent
from core.planner import build_plan
from core.dispatcher import dispatch


def route(prompt: str):
    print("[ROUTER ACTIVE]")

    if not prompt or not prompt.strip():
        return {"error": "empty prompt"}

    # 1. Intent extraction
    intent = extract_intent(prompt)
    print("[INTENT]", intent)

    if not intent:
        return {"error": "no intent detected"}

    # 2. Plan building
    plan = build_plan(intent)
    print("[PLAN]", plan)

    if not plan:
        return {"error": "failed to build plan"}

    # 3. Dispatch execution
    result = dispatch(plan)

    return result
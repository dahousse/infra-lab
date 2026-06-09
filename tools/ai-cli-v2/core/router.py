from core.intent import extract_intent
from core.planner import build_plan
from core.dispatcher import dispatch

def route(prompt: str):
    print("[V3 ROUTER ACTIVE]")

    intent = extract_intent(prompt)
    print("[INTENT]", intent)

    plan = build_plan(intent)
    print("[PLAN]", plan)

    result = dispatch(plan)

    return result
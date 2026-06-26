"""Router — entry point: prompt → intent → plan → dispatch"""

from core.intent import extract_intent
from core.planner import build_plan
from core.dispatcher import dispatch


def route(prompt: str):
    if not prompt or not prompt.strip():
        return {"status": "error", "error": "empty prompt"}

    intent = extract_intent(prompt)

    # Store original prompt for chat fallback
    if intent.get("type") == "unknown":
        intent["raw_prompt"] = prompt

    plan = build_plan(intent)
    plan["raw_prompt"] = prompt

    result = dispatch(plan)

    return result

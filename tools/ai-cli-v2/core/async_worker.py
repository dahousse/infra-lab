import threading
from core.dispatcher import dispatch

def run_async(plan: dict):
    def _worker():
        try:
            result = dispatch(plan)
            print("\n[ASYNC RESULT]", result)
        except Exception as e:
            print("\n[ASYNC ERROR]", str(e))

    t = threading.Thread(target=_worker)
    t.daemon = True
    t.start()

    return {
        "status": "queued",
        "engine": plan.get("engine"),
    }
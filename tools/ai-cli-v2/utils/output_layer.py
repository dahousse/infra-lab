# utils/output_layer.py

def success(engine, data):
    return {
        "status": "ok",
        "engine": engine,
        "data": data
    }


def fail(engine, message):
    return {
        "status": "error",
        "engine": engine,
        "error": message
    }


def wrap(engine, data=None, error=None):
    if error:
        return fail(engine, error)
    return success(engine, data)
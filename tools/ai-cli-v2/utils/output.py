import json as pyjson

def json_output(data):
    print(pyjson.dumps(data, indent=2, ensure_ascii=False))

def ok(msg):
    print(f"✔ {msg}")

def warn(msg):
    print(f"⚠ {msg}")

def error(msg):
    print(f"❌ {msg}")

def info(msg):
    print(f"ℹ {msg}")

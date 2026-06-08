import json as pyjson

def json_output(data):
    print(pyjson.dumps(data, indent=2, ensure_ascii=False))

def error(msg):
    print(f"❌ {msg}")

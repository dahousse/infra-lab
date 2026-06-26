import json

def json_output(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def text_kv(title, items):
    print(f"\n{title}\n")
    for k, v in items.items():
        print(f"{k}: {v}")


def text_list(title, items):
    print(f"\n{title}\n")
    for i in items:
        print(f"- {i}")

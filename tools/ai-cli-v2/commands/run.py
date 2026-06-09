from core.router import route


def main(args):
    prompt = " ".join(args)

    print("[DEBUG] ROUTE ACTIVE")
    result = route(prompt)
    print(result)
from commands import run, models, system, doctor, help
from utils import output

def parse_flags(argv):
    flags = {
        "json": False
    }

    if "--json" in argv:
        flags["json"] = True
        argv = argv.replace("--json", "").strip()

    return flags, argv


def route(cmd, args):

    # FIX IMPORTANT: allow "--json get models"
    raw = f"{cmd} {args}".strip()
    tokens = raw.split()

    flags, cleaned = parse_flags(raw)
    tokens = cleaned.split()

    if not tokens:
        output.error("Empty command")
        return

    cmd = tokens[0]
    args = " ".join(tokens[1:])

    if cmd == "get":
        cmd = args.split()[0]
        args = " ".join(args.split()[1:])

    data = None

    if cmd == "run":
        data = run.run(args)

    elif cmd == "models":
        data = models.run()

    elif cmd == "system":
        data = system.run()

    elif cmd == "doctor":
        data = doctor.run()

    elif cmd == "help":
        return help.run()

    else:
        output.error("Unknown command")
        return

    if flags["json"]:
        output.json_output(data)
    else:
        render_text(cmd, data)


def render_text(cmd, data):

    if cmd == "run":
        print(data)

    elif cmd == "models":
        print("\n📦 Models\n")
        for m in data.get("models", []):
            print("-", m)

    elif cmd == "doctor":
        print("\n🧠 Doctor\n")
        print("Status:", data.get("status"))
        print("Models:", data.get("models_count", 0))

    elif cmd == "system":
        print(data)

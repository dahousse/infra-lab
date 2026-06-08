from commands import run, models, system, doctor, help
from utils import output

def is_json(args):
    return "--json" in args

def clean(args):
    return args.replace("--json", "").strip()

def route(cmd, args):

    json_mode = is_json(args)
    args = clean(args)

    if cmd == "run":
        result = run.run(args)

        if json_mode:
            output.json_output({
                "cmd": "run",
                "input": args,
                "output": result
            })
        else:
            if result:
                print(result)
        return

    if cmd == "models":
        data = models.run()

        if json_mode:
            output.json_output(data)
        else:
            print("\n📦 Models\n")
            for m in data.get("models", []):
                print("-", m)
        return

    if cmd == "system":
        data = system.run()

        if json_mode:
            output.json_output(data)
        return

    if cmd == "doctor":
        data = doctor.run()

        if json_mode:
            output.json_output(data)
        return

    if cmd == "help":
        help.run()
        return

    output.error("Unknown command")

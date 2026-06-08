from commands import run, models, system, doctor, help
from utils import output

def route(cmd, args):
    if cmd == "run":
        result = run.run(args)
        if result:
            print(result)

    elif cmd == "models":
        models.run()

    elif cmd == "system":
        system.run()

    elif cmd == "doctor":
        doctor.run()

    elif cmd == "help":
        help.run()

    else:
        output.error("Unknown command. Try: run | models | system | doctor | help")

from commands import run, models, system, doctor,help

def route(cmd, args):
    if cmd == "run":
        return run.run(args)
    elif cmd == "models":
        return models.run()
    elif cmd == "system":
        return system.run()
    elif cmd == "doctor":
        return doctor.run()
    elif cmd == "help":
        return help.run()
    else:
        print("❌ Unknown command. Try: run | models | system | doctor")

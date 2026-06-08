from commands import run, models, system, doctor

def route(cmd, args):
    if cmd == "run":
        return run.run(args)
    if cmd == "models":
        return models.run()
    if cmd == "system":
        return system.run()
    if cmd == "doctor":
        return doctor.run()

    print("Unknown command:", cmd)

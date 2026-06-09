# cli/main.py

import sys

# Commands legacy (transition safe)
from commands.run import main as run_main
from commands.doctor import main as doctor_main
from commands.help import main as help_main
from commands.models import main as models_main
from commands.system import main as system_main


def print_global_help():
    print("""
ai-cli v2.5

Usage:
  ai run <prompt>        Run infrastructure request
  ai doctor              Diagnose system
  ai models              List available models
  ai system              Show system info
  ai help                Show help

Examples:
  ai run "vm ubuntu docker"
  ai doctor
""")

def main():
    args = sys.argv[1:]

    if not args:
        print_global_help()
        return

    command = args[0]

    try:
        if command == "run":
            run_main(args[1:])

        elif command == "doctor":
            doctor_main()

        elif command == "help":
            help_main()

        elif command == "models":
            models_main()

        elif command == "system":
            system_main()

        else:
            print(f"[ERROR] Unknown command: {command}")
            print_global_help()

    except Exception as e:
        print(f"[FATAL ERROR] {e}")


if __name__ == "__main__":
    main()
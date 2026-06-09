import sys
from commands.run import run

def main():
    prompt = " ".join(sys.argv[1:])
    print(run(prompt))

if __name__ == "__main__":
    main()

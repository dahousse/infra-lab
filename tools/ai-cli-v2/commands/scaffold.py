import os
from core.config import load_config
from utils.output import ok, error, info

PROMPT_PATH = "specs/prompts/ai-cli-v2-generator.md"

def run(args):
    project_name = args.strip() or "ai-cli-v2"

    if not os.path.exists(PROMPT_PATH):
        error("Prompt spec not found")
        return

    with open(PROMPT_PATH, "r") as f:
        prompt = f.read()

    info(f"Generating project: {project_name}")

    # Simulation locale (phase 1)
    # plus tard: appel Ollama réel
    print("\n🧠 PROMPT SENT TO AI:\n")
    print(prompt)

    ok("Scaffold ready (simulation mode)")

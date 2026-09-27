"""
Confirm the environment is ready. Run this first.

    python check_setup.py
"""
import os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from core._shared import MODEL, FAST_MODEL, SEED
from core.banner import concept, step, note


def main():
    concept(
        demo_id="setup",
        title="Is everything ready?",
        idea=("Five checks: Python version, the seed files, the pinned model "
              "IDs, the API key, and one real call. Nothing here is a Domain 1 "
              "concept - it just stops you debugging plumbing during a lesson."),
        objective="(setup only)",
        watch_for="Any line that says MISSING.",
    )

    step(1, "Python")
    v = sys.version_info
    print(f"  {v.major}.{v.minor}.{v.micro}   (3.10 or newer is required)")

    step(2, "Seed files")
    n = len(list(SEED.iterdir())) if SEED.exists() else 0
    print(f"  workspace_seed/: {n} files   {'OK' if n == 14 else 'MISSING - expected 14'}")

    step(3, "Model IDs this project pins")
    print(f"  main model : {MODEL}")
    print(f"  fast model : {FAST_MODEL}")
    note("Both are exact IDs. Never use a moving alias in code you will ship - "
         "a model change should be a commit you can see, not a surprise.")

    step(4, "Credentials")
    from core._shared import ENV_FILE, ENV_LOADED
    print(f"  .env path : {ENV_FILE}")
    print(f"  .env file : {'read' if ENV_LOADED else 'NOT FOUND'}")

    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("  ANTHROPIC_API_KEY: MISSING")
        print()
        print("      The .env line must read exactly:")
        print("          ANTHROPIC_API_KEY=sk-ant-...")
        print("      No 'export', no spaces around the =, no quotes needed,")
        print("      and the file must be named .env, not .env.txt.")
        return
    print(f"  ANTHROPIC_API_KEY: found ({key[:7]}...{key[-4:]}, "
          f"{len(key)} chars)")

    step(5, "One real call")
    from core._shared import get_client, ask_claude
    reply = ask_claude(get_client(),
                       "Reply with exactly: sortly ready", max_tokens=16)
    print(f"  model replied: {reply.strip()!r}")
    print("\n  Setup complete.")


if __name__ == "__main__":
    main()

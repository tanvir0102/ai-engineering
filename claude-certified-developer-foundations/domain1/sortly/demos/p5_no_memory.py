"""
Part 5, demo 1 - every run starts from zero.

Run:  python demos/p5_no_memory.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client
from core.agent import Ledger
from core.subagents import classify_with_subagent
from core.tools import list_files, move_file
from core.banner import concept, step, note, takeaway


def sort_once(client, label):
    reset_workspace(quiet=True)
    ledger = Ledger()
    files = [f for f in list_files().splitlines() if f.strip().endswith(".txt")]
    decisions = {}
    for f in files:
        category, _ = classify_with_subagent(client, f, ledger=ledger)
        move_file(f, category)
        decisions[f] = category
    print(f"  {label}: {len(files)} files classified, "
          f"{ledger.turns} model calls, {ledger.input_tokens} input tokens")
    return decisions, ledger


def main():
    concept(
        demo_id="P5 / demo 1",
        title="No memory: the second run learns nothing from the first",
        idea=("A model has no memory between runs. Nothing persists unless you "
              "write it down. Run the same job twice and you pay twice for the "
              "same conclusions."),
        objective="Domain 1 > Agent Patterns > memory",
        watch_for=("The two lines below should be identical. That is the "
                   "problem, not a coincidence."),
    )

    client = get_client()

    step(1, "Run the sort on Monday")
    monday, l1 = sort_once(client, "Monday ")

    step(2, "Run the exact same sort on Tuesday")
    tuesday, l2 = sort_once(client, "Tuesday")

    step(3, "Compare")
    same = sum(1 for f in monday if monday[f] == tuesday.get(f))
    print(f"  files where both runs agreed : {same}/{len(monday)}")
    print(f"  model calls spent on Monday  : {l1.turns}")
    print(f"  model calls spent on Tuesday : {l2.turns}   <- all of them repeats")
    print(f"  total input tokens           : {l1.input_tokens + l2.input_tokens}")
    note("Tuesday re-read every file and re-derived every category that Monday "
         "had already worked out. Nothing was wrong - there was simply nowhere "
         "for Monday's answers to go.")

    step(4, "What 'memory' does and does not mean")
    print("  It does NOT mean the model remembers you.")
    print("  It means YOU store the outcome somewhere, and put the relevant")
    print("  part back into the prompt on the next run. A JSON file is enough.")

    takeaway(
        points=[
            "Every run starts blank. There is no hidden per-user state on "
            "Anthropic's side that carries across your API calls.",
            "Without persistence you repeat work, and you can also contradict "
            "yourself - two runs can classify the same file differently.",
            "Memory is a file you write and a snippet you re-inject, not a "
            "model feature.",
        ],
        exam_angle=("Memory appears in Domain 1 as an agent pattern. Expect a "
                    "scenario where an agent 'forgets' between sessions and "
                    "the fix is external persistence re-injected into context."),
    )


if __name__ == "__main__":
    main()

"""
Part 5, demo 2 - the same two runs, with a memory file.

Run:  python demos/p5_with_memory.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client, MEMORY_FILE
from core.agent import Ledger
from core.subagents import classify_with_subagent
from core.tools import list_files, move_file
from core.memory import load_memory, save_memory, remember, recall, forget_all
from core.banner import concept, step, note, takeaway


def sort_with_memory(client, label):
    reset_workspace(quiet=True)
    mem = load_memory()
    ledger = Ledger()
    files = [f for f in list_files().splitlines() if f.strip().endswith(".txt")]

    asked, recalled = 0, 0
    for f in files:
        known = recall(mem, f)
        if known:
            category, recalled = known, recalled + 1
        else:
            category, _ = classify_with_subagent(client, f, ledger=ledger)
            remember(mem, f, category)
            asked += 1
        move_file(f, category)

    save_memory(mem)
    print(f"  {label}: {recalled} recalled from memory, {asked} sent to the model, "
          f"{ledger.input_tokens} input tokens")
    return ledger


def main():
    concept(
        demo_id="P5 / demo 2",
        title="Memory: write the conclusion down, look it up next time",
        idea=("Persisting the decision, not the evidence, is what makes a "
              "second run cheap. The memory file holds one line per file: what "
              "it was classified as, and when."),
        objective="Domain 1 > Agent Patterns > memory",
        watch_for=("Monday's numbers should match demo 1. Tuesday's model-call "
                   "count should drop to zero."),
    )

    forget_all()
    client = get_client()

    step(1, "Monday, with an empty memory file")
    sort_with_memory(client, "Monday ")

    step(2, "What got written to disk")
    mem = load_memory()
    print(f"  {MEMORY_FILE.name}: {len(mem)} entries, "
          f"{MEMORY_FILE.stat().st_size} bytes")
    for k in list(mem)[:3]:
        print(f"      {k:<40} {mem[k]}")
    note("Small on purpose. It stores conclusions, not file contents. A memory "
         "file that grows as fast as your data has become a second problem.")

    step(3, "Tuesday, with the memory file present")
    sort_with_memory(client, "Tuesday")

    step(4, "The catch nobody mentions")
    print("  Memory makes the agent consistent - and consistently wrong when")
    print("  the first answer was wrong. Nothing here re-checks Monday.")
    print("  Real systems add an expiry, a confidence field, or a way for a")
    print("  human to correct an entry. Decide that up front.")

    takeaway(
        points=[
            "Memory between runs is a file you own: write the conclusion, read "
            "it back, inject only what is relevant.",
            "Store conclusions, not raw evidence, or the memory file becomes "
            "the context problem you were avoiding.",
            "Persistence locks in mistakes as well as successes, so plan for "
            "expiry and correction.",
        ],
        exam_angle=("Distinguish the two meanings clearly: context-window "
                    "management is within a run, memory is across runs. "
                    "Questions often hinge on which one a scenario needs."),
    )


if __name__ == "__main__":
    main()

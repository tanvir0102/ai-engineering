"""
Part 3, demo 2 - a manager that delegates.

Run:  python demos/p3_manager_flat.py  first, then this one.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client, WORKSPACE, FAST_MODEL, MODEL
from core.agent import Ledger
from core.subagents import classify_with_subagent
from core.tools import list_files, move_file
from core.banner import concept, step, note, takeaway


def main():
    concept(
        demo_id="P3 / demo 2",
        title="Manager and subagents: the conclusion, not the evidence",
        idea=("The manager never reads a file. For each one it starts a fresh "
              "single-purpose conversation, which reads the file and returns "
              "one word. The file body lives and dies inside that subagent."),
        objective="Domain 1 > Agent Architecture > manager hierarchies and subagents",
        watch_for=("Two numbers. The manager's own context stays almost empty. "
                   "The subagent calls are many but each is tiny, and they run "
                   "on a cheaper model."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "The manager's plan, in three lines")
    print("      files = list_files()                      <- manager's only read")
    print("      for f in files:  cat = subagent(f)        <- delegated")
    print("                       move_file(f, cat)        <- manager acts")
    note(f"Manager model: {MODEL}.  Subagent model: {FAST_MODEL}. "
         "A one-word classification does not need the bigger model.")

    step(2, "Run it")
    manager = Ledger()
    workers = Ledger()

    files = [f for f in list_files().splitlines() if f.strip().endswith(".txt")]
    manager.input_tokens += len(" ".join(files)) // 4      # the listing itself

    for f in files:
        category, snippet = classify_with_subagent(client, f, ledger=workers)
        result = move_file(f, category)
        manager.tool_calls += 1
        print(f"  {f:<40} subagent saw {len(snippet):>4} chars  ->  {category}")

    step(3, "Compare the two shapes")
    flat_file = pathlib.Path("/tmp/sortly_flat.txt")
    flat = int(flat_file.read_text()) if flat_file.exists() else None

    print("  " + manager.line("manager context"))
    print("  " + workers.line("subagents (total)"))
    print()
    if flat:
        print(f"  flat agent, one context     : {flat:>7} input tokens")
        print(f"  manager only                : {manager.input_tokens:>7} input tokens")
        print(f"  manager + all subagents     : {manager.input_tokens + workers.input_tokens:>7} input tokens")
    else:
        print("  (run demos/p3_manager_flat.py first to see the comparison)")

    left = [p.name for p in WORKSPACE.iterdir() if p.is_file()]
    print(f"\n  files still loose: {len(left)}")

    step(4, "Read the numbers honestly")
    print("  Delegating is not automatically cheaper in total tokens. Each")
    print("  subagent re-sends its own system prompt, so there is overhead.")
    print("  What it reliably buys you is a manager whose context does not")
    print("  grow with the size of the job - plus cheaper models per subtask,")
    print("  and subtasks that can run in parallel.")
    note("If a manager's context grows with every subtask, the delegation is "
         "not doing its job. Return conclusions, not transcripts.")

    takeaway(
        points=[
            "A subagent is a separate conversation with its own context, "
            "prompt and tools - not a separate library.",
            "Delegate so the bulky evidence stays out of the manager's window "
            "and only the small conclusion comes back.",
            "Subagents also let you drop to a cheaper model and a tighter "
            "tool set for the narrow subtask.",
        ],
        exam_angle=("Manager/supervisor hierarchy: one agent owns the goal and "
                    "the sequencing; specialists own narrow subtasks. The "
                    "stated benefit is context isolation and focused tool "
                    "sets, not raw speed."),
    )


if __name__ == "__main__":
    main()

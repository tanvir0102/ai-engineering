"""
Part 1, demo 2 - the agent shape, on the same folder.

Run:  python demos/p1_pipeline_with_model.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import WORKSPACE, reset_workspace, get_client, MODEL
from core.agent import run_agent
from core.banner import concept, step, note, takeaway

SYSTEM = """You are Sortly, a tidy-up assistant for Asha's downloads folder in Pune.

Your job: put every loose file into exactly one of these folders -
finance, work, personal, misc.

How to work:
- Call list_files first to see what is there.
- If a filename does not make the contents obvious, call read_file_head
  before deciding. Do not guess from the name alone.
- Then call move_file once per file.
- Use misc only when a file truly fits nothing else.
- When every file has been moved, stop and say what you did in two lines.

Do not delete or rename anything in this task."""


def main():
    concept(
        demo_id="P1 / demo 2",
        title="An agent: same job, decisions made at runtime",
        idea=("An agent is given a goal and a set of tools, and works out the "
              "steps itself, one tool call at a time. Nobody wrote a rule for "
              "untitled_1.txt - the agent opens it and decides."),
        objective="Domain 1 > Agent Architecture > workflow versus agent decision criteria",
        watch_for=("The files the rigid pipeline called UNKNOWN. Watch the agent "
                   "read them first, then place them. Also watch the turn count "
                   "and token count - this is what the flexibility costs."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "Hand the goal and the tools to the model, then get out of the way")
    print(f"  model : {MODEL}")
    print("  tools : list_files, read_file_head, move_file, rename_file, delete_file")
    note("Notice we describe the goal, not the procedure. That is the difference.")

    step(2, "Watch the agent work")

    def show(kind, payload):
        if kind == "tool":
            name, args, out = payload
            arg = args.get("filename", "") or ""
            first = str(out).splitlines()[0] if str(out).strip() else ""
            print(f"  -> {name:<15} {arg:<38} {first[:28]}")
        elif kind == "final":
            print(f"\n  agent says: {payload.strip()[:200]}")

    final, ledger = run_agent(
        client,
        task="Tidy up Asha's folder. Every loose file should end up in a category folder.",
        system=SYSTEM,
        on_event=show,
    )

    step(3, "Score the run")
    print("  " + ledger.line("agent"))
    left = [p.name for p in WORKSPACE.iterdir() if p.is_file()]
    print(f"  files still loose: {len(left)}")
    note("Compare against demo 1: that run was 0 calls and Rs 0, and left "
         "two files unplaced. This run costs tokens and time, and places them.")

    takeaway(
        points=[
            "An agent chooses its own next step. You supply a goal, tools and "
            "limits - not a procedure.",
            "The same loop handles inputs you never anticipated, which is the "
            "one thing a workflow cannot do.",
            "You pay for that in tokens, latency and variability. Two runs of "
            "the same agent may take different paths.",
        ],
        exam_angle=("Reach for an agent when the steps cannot be known in "
                    "advance, when the order depends on what is found, or when "
                    "the input is open-ended. Otherwise a workflow is the "
                    "better engineering answer."),
    )


if __name__ == "__main__":
    main()

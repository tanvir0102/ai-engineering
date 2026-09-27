"""
Part 3, demo 1 - one agent doing everything.

Run:  python demos/p3_manager_flat.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client
from core.agent import run_agent
from core.banner import concept, step, note, takeaway

SYSTEM = ("You are Sortly. Sort every loose file into finance, work, personal "
          "or misc. Read a file before deciding. Do not delete or rename. "
          "Stop when the folder is clean.")


def main():
    concept(
        demo_id="P3 / demo 1",
        title="One flat agent: everything lands in one context",
        idea=("A single agent that reads fourteen files ends up carrying all "
              "fourteen files in its conversation. Every later turn resends "
              "every earlier file, whether or not it is still relevant."),
        objective="Domain 1 > Agent Architecture > the role of subagents",
        watch_for=("The input-token total at the end, and the fact that it "
                   "grows faster than the number of files. Write the number "
                   "down - demo 2 runs the same job a different way."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "Run one agent over the whole folder")
    reads = []

    def show(kind, payload):
        if kind == "tool":
            name, args, out = payload
            if name == "read_file_head":
                reads.append(args.get("filename"))
                print(f"  read  {args.get('filename')}   (+{len(str(out))} chars into context)")
            elif name == "move_file":
                print(f"  move  {args.get('filename')} -> {args.get('category')}")

    final, ledger = run_agent(
        client,
        task="Tidy Asha's folder. Every loose file into a category folder.",
        system=SYSTEM,
        on_event=show,
    )

    step(2, "The bill")
    print("  " + ledger.line("flat agent"))
    print(f"  files read into the manager's own context: {len(reads)}")
    note("Every one of those file bodies stayed in the conversation for the "
         "rest of the run. That is context bloat: paying again and again for "
         "text whose only useful output was a single word.")

    step(3, "Save the number for the comparison")
    pathlib.Path("/tmp/sortly_flat.txt").write_text(str(ledger.input_tokens))
    print(f"  flat agent input tokens = {ledger.input_tokens}")

    takeaway(
        points=[
            "One agent, one context. Everything it reads stays with it.",
            "The evidence (whole file bodies) is far larger than the "
            "conclusion (one category word), and only the conclusion matters.",
            "This is fine for five files and painful for five hundred.",
        ],
        exam_angle=("The reason to introduce subagents is context isolation - "
                    "keeping bulky intermediate work out of the manager's "
                    "window. Speed and tidiness are side effects, not the "
                    "reason."),
    )


if __name__ == "__main__":
    main()

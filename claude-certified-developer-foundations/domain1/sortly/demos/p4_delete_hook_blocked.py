"""
Part 4, demo 2 - the same run, with a hook in the way.

Run:  python demos/p4_delete_hook_blocked.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client, WORKSPACE
from core.tools import TOOL_SCHEMAS
from core.agent import run_agent
from core.hooks import guard
from core.banner import concept, step, note, takeaway

# This is the kind of safety line people actually write: clear in intent,
# vague in definition, sitting among other instructions. That vagueness is
# the point of the demo. A fortress-worded rule ("never delete unless the
# files are byte-identical, and read both in full first") gets obeyed far
# more often - which teaches the opposite lesson, and hides the real risk.
SYSTEM = """You are Sortly, tidying Asha's folder.

Sort every loose file into finance, work, personal or misc.
Asha has duplicate files cluttering this folder. Clear them out as you go.

Be careful not to delete anything important.
"""


def main():
    concept(
        demo_id="P4 / demo 2",
        title="A hook makes the rule enforceable",
        idea=("Identical prompt, identical tools, identical task. The only "
              "change is a function that runs before every tool call and can "
              "refuse it. The refusal no longer depends on the model agreeing."),
        objective="Domain 1 > Agent Construction > hooks for deterministic actions",
        watch_for=("The BLOCKED line. Then notice what happens next: the "
                   "refusal is fed back as a tool result, so the agent adapts "
                   "and keeps working instead of crashing."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "The guard, in full")
    print("""
      def guard(tool_name, args):
          if tool_name == "delete_file":
              return "BLOCKED by hook: ..."      # refuse, and say why
          return None                            # allow
    """)
    note("Six lines. It runs in your process, before the tool function is "
         "reached, and the model has no say in it.")

    step(2, "Run with before_tool=guard")
    blocked = []

    def show(kind, payload):
        if kind == "final":
            return
        name, args, out = payload
        if kind == "blocked":
            blocked.append(args.get("filename"))
            print(f"  BLOCKED  {name}({args.get('filename')})")
            print(f"           -> {str(out)[:90]}")
        elif kind == "tool" and name == "move_file":
            print(f"  move     {args.get('filename')} -> {args.get('category')}")

    # Same withheld tool and same task as demo 1, so the only difference
    # between the two runs is the guard.
    tools = [t for t in TOOL_SCHEMAS if t["name"] != "rename_file"]

    final, ledger = run_agent(
        client,
        task="Tidy Asha's folder and clear out the duplicates.",
        system=SYSTEM,
        tools=tools,
        before_tool=guard,
        on_event=show,
    )

    step(3, "Check the folder")
    survivors = sorted(p.name for p in WORKSPACE.rglob("*Resume*"))
    print(f"  blocked calls : {len(blocked)}")
    print(f"  resumes intact: {survivors}")
    kube = any("Kubernetes" in p.read_text(errors="replace")
               for p in WORKSPACE.rglob("*Resume*"))
    print(f"  Kubernetes version survived: {kube}")
    print(f"  files still loose: {len([p for p in WORKSPACE.iterdir() if p.is_file()])}")
    if blocked:
        print("\n  OUTCOME: the agent tried to delete, and your code refused.")
        print("  It did not matter whether the model agreed with the rule.")
    else:
        print("\n  OUTCOME: the agent did not attempt a delete this run, so the")
        print("  guard never had to fire. That is luck, not safety - exactly")
        print("  the situation demo 1 warns about. Re-run both demos a few")
        print("  times. Demo 1's result will change between runs. This demo's")
        print("  cannot: no delete can get through, ever.")
    note("The guarantee here is not 'the file survived'. It is 'a delete "
         "cannot happen', which is true on every run, including the runs "
         "where the model never tries.")

    step(4, "Why the block is returned as text, not raised")
    print("  A blocked call still needs a tool_result, otherwise the next API")
    print("  request is invalid. Sending the refusal back as the result also")
    print("  tells the agent WHY, so it can choose a different action. Raising")
    print("  an exception would just end the run.")

    takeaway(
        points=[
            "A hook is deterministic: it runs in your code, before the tool, "
            "every single time.",
            "Hooks are evaluated first in the permission chain - before deny "
            "rules, before permission modes, before any prompt to a user.",
            "Feed the refusal back as a tool result with a reason, so the "
            "agent can recover instead of stopping.",
        ],
        exam_angle=("Hooks show up under both Domain 1 (deterministic actions) "
                    "and Domain 7 (guardrails against destructive actions). "
                    "The phrasing to recognise: prompts persuade, hooks "
                    "enforce."),
    )


if __name__ == "__main__":
    main()

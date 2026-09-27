"""
Part 1, demo 3 - the decision itself.

Run:  python demos/p1_choose_the_shape.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core.banner import concept, step, takeaway

CRITERIA = [
    ("Are the steps known before you run?",        "workflow", "agent"),
    ("Is the order of steps fixed?",               "workflow", "agent"),
    ("Is the set of possible inputs bounded?",     "workflow", "agent"),
    ("Must every run be identical and auditable?", "workflow", "agent"),
    ("Does the next step depend on what is found?","agent",    "workflow"),
    ("Is the input open-ended natural language?",  "agent",    "workflow"),
]

CASES = [
    ("Move every invoice PDF from the inbox into a dated folder",
     "workflow", "Steps are known, order is fixed, input is one file type."),
    ("Read an incoming complaint and route it to the right team",
     "agent", "The routing depends on what the complaint actually says."),
    ("Nightly: pull yesterday's orders, total them, email the sheet",
     "workflow", "Three known steps in a fixed order. A model adds risk, not value."),
    ("Investigate why a failing test started failing and propose a fix",
     "agent", "Nobody can write the steps in advance - they depend on findings."),
    ("Resize every image in a folder to 800px wide",
     "workflow", "Pure deterministic transformation. No judgement required."),
    ("Tidy Asha's folder, including files nobody has seen before",
     "agent", "This is demo 2. The unknown files are exactly the reason."),
]


def main():
    concept(
        demo_id="P1 / demo 3",
        title="Choosing the shape",
        idea=("Demos 1 and 2 showed you one folder. This demo gives you the "
              "RULE, so you can decide about a task you have never seen. That "
              "is the exam question. Nothing runs here and nothing is spent - "
              "it is a decision aid, not an agent."),
        objective="Domain 1 > Agent Architecture > decision criteria, applied",
        watch_for=("Step 1 is the rule: six questions, each pointing at "
                   "workflow or agent. Step 2 applies it to six tasks. Read "
                   "each task line first and decide, then read the two lines "
                   "under it to check yourself."),
    )

    step(1, "Six questions that settle it")
    print(f"  {'question':<46}{'yes ->':<12}no ->")
    print("  " + "-" * 68)
    for q, yes, no in CRITERIA:
        print(f"  {q:<46}{yes:<12}{no}")

    step(2, "Six cases - decide before you read the arrow under each one")
    for task, answer, why in CASES:
        print(f"\n  {task}")
        print(f"      -> {answer.upper()}")
        print(f"         {why}")

    step(3, "The trap to avoid")
    print("  'Agentic' is not a maturity level. Wrapping a fixed three-step job")
    print("  in an agent loop buys you non-determinism, latency and cost, and")
    print("  buys the user nothing. The reverse trap is real too: forcing an")
    print("  open-ended job into rules produces the UNKNOWN column from demo 1.")

    takeaway(
        points=[
            "Known steps, fixed order, bounded input -> workflow.",
            "Next step depends on findings, or input is open-ended -> agent.",
            "Many real systems are a workflow with one agent step inside it, "
            "not one or the other.",
        ],
        exam_angle=("Expect a scenario and four options. The correct answer is "
                    "usually the simplest shape that still handles the "
                    "variability described in the scenario."),
    )


if __name__ == "__main__":
    main()

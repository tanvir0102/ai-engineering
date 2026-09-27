"""
Part 1, demo 1 - the workflow shape.

Run:  python demos/p1_pipeline_rigid.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import WORKSPACE, reset_workspace
from core.banner import concept, step, note, takeaway

# Fixed rules. Written once, by a human, in advance.
RULES = [
    ("finance", ["bill", "receipt", "statement", "form16", "insurance"]),
    ("work",    ["meeting", "sprint", "resume"]),
    ("personal",["grocery", "wedding", "trek"]),
]


def category_for(filename):
    low = filename.lower()
    for label, keywords in RULES:
        if any(k in low for k in keywords):
            return label
    return None            # no rule matched


def main():
    concept(
        demo_id="P1 / demo 1",
        title="A workflow: fixed steps, fixed order",
        idea=("A workflow is code you wrote in advance. It runs the same steps "
              "in the same order every time. Nothing decides anything at "
              "runtime - your if-statements already decided."),
        objective="Domain 1 > Agent Architecture > workflow versus agent decision criteria",
        watch_for=("Most files get sorted instantly and for free. Then count how "
                   "many come back UNKNOWN. Those are the files the rules never "
                   "anticipated."),
    )

    reset_workspace(quiet=True)
    files = sorted(p.name for p in WORKSPACE.iterdir() if p.is_file())

    step(1, f"Run the fixed pipeline over {len(files)} files")
    sorted_count, unknown = 0, []
    for name in files:
        cat = category_for(name)
        if cat is None:
            unknown.append(name)
            print(f"  UNKNOWN  {name}")
        else:
            (WORKSPACE / cat).mkdir(exist_ok=True)
            (WORKSPACE / name).rename(WORKSPACE / cat / name)
            sorted_count += 1
            print(f"  {cat:<9}{name}")

    step(2, "Score the run")
    print(f"  sorted   : {sorted_count}")
    print(f"  unknown  : {len(unknown)}")
    print(f"  API calls: 0")
    print(f"  cost     : Rs 0")
    note("The pipeline only ever looked at filenames. It never opened a file.")

    step(3, "Look at what it could not place")
    for n in unknown:
        first = (WORKSPACE / n).read_text(errors="replace").splitlines()[:1]
        print(f"  {n}")
        print(f"      first line: {first[0] if first else '(empty)'}")
    note("A human can tell what these are in one second. The rules cannot, "
         "because nobody wrote a rule for them.")

    takeaway(
        points=[
            "A workflow is predictable, fast, free and auditable. Prefer it "
            "whenever the steps are genuinely known ahead of time.",
            "A workflow fails silently on inputs nobody anticipated. It does "
            "not get confused - it just has no branch.",
            "Adding a rule for every new case is how a workflow slowly turns "
            "into an unmaintainable pile of if-statements.",
        ],
        exam_angle=("Choose a workflow when the steps are known, the order is "
                    "fixed and the input is bounded. The exam frames this as a "
                    "tradeoff, not as one being better."),
    )


if __name__ == "__main__":
    main()

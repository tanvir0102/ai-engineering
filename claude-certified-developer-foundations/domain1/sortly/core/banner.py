"""
Every Sortly demo prints the same three things:

  1. A CONCEPT card before anything runs  -> what this demo is about
  2. STEP lines while it runs             -> what is happening right now
  3. A TAKEAWAY card at the end           -> what you were supposed to notice

The point is that you should never have to guess why a demo exists.
Read the concept card, watch the steps, read the takeaway.
"""

WIDTH = 74


def _rule(char="-"):
    print(char * WIDTH)


def _wrap(text, indent=""):
    """Very small word-wrapper so the cards look the same on every terminal."""
    words = text.split()
    line = indent
    out = []
    for w in words:
        if len(line) + len(w) + 1 > WIDTH:
            out.append(line.rstrip())
            line = indent
        line += w + " "
    out.append(line.rstrip())
    return "\n".join(out)


def concept(demo_id, title, idea, objective, watch_for):
    """Print the card that explains the demo BEFORE it runs.

    demo_id   : e.g. "P1 / demo 1"
    title     : short name of the demo
    idea      : the single sentence you should remember
    objective : which CCDV-F Domain 1 skill this maps to
    watch_for : what to look at in the output below
    """
    print()
    _rule("=")
    print(f"  SORTLY  |  {demo_id}  |  {title}")
    _rule("=")
    print("  THE IDEA")
    print(_wrap(idea, "  "))
    print()
    print("  EXAM OBJECTIVE")
    print(_wrap(objective, "  "))
    print()
    print("  WATCH FOR")
    print(_wrap(watch_for, "  "))
    _rule("=")
    print()


def step(n, text):
    """One numbered line of narration while the demo runs."""
    print(f"\n[step {n}] {text}")
    _rule()


def note(text):
    """A short aside printed inside a step."""
    print(_wrap(f"      {text}"))


def takeaway(points, exam_angle):
    """Print the card that says what just happened AFTER the demo runs.

    points     : list of short strings
    exam_angle : how this is likely to be tested
    """
    print()
    _rule("=")
    print("  TAKEAWAY")
    _rule("=")
    for p in points:
        print(_wrap(f"  - {p}"))
    print()
    print("  EXAM ANGLE")
    print(_wrap(exam_angle, "  "))
    _rule("=")
    print()

"""
Part 2, demo 3 - where does the agent actually run?

Run:  python demos/p2_deployment_models.py       (no API key needed)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core.banner import concept, step, note, takeaway

ROWS = [
    ("Who runs the agent loop",   "your process",          "Anthropic's infrastructure"),
    ("Who runs the tools",        "your code",             "the managed sandbox, or your MCP server"),
    ("Where the files live",      "your disk",             "a sandbox filesystem (or self-hosted sandbox)"),
    ("Conversation state",        "you keep it",           "persisted server-side, resumable"),
    ("Runs for hours unattended", "you build that",        "designed for it"),
    ("Scheduled / cron runs",     "you build that",        "scheduled deployments"),
    ("Needs Node on the box",     "yes (bundled CLI)",     "no, it is a REST API"),
    ("Data residency control",    "total - it is your box","cloud sandbox, or self-hosted sandbox"),
]

CASES = [
    ("A CLI tool your team runs on their own laptops",
     "self-hosted", "The files are already local. Shipping them to a sandbox "
                    "would be work for no benefit."),
    ("A nightly agent that reconciles 4 hours of billing data",
     "Anthropic-hosted", "Long-running, unattended, scheduled. Building your own "
                         "sandbox and resume logic is the expensive path."),
    ("An agent inside a hospital network handling patient records",
     "self-hosted", "Data residency and retention rules decide this before any "
                    "engineering argument does."),
    ("A SaaS feature where each customer's agent runs for 20 minutes",
     "Anthropic-hosted", "You would otherwise be building sandbox isolation and "
                         "session storage per tenant."),
]


def main():
    concept(
        demo_id="P2 / demo 3",
        title="Self-hosted versus Anthropic-hosted",
        idea=("Building the agent and deploying it are separate decisions. "
              "The Agent SDK runs the loop inside your process, on your "
              "machine. Claude Managed Agents runs the loop and the sandbox on "
              "Anthropic's infrastructure and gives you a REST API."),
        objective="Domain 1 > Agent Construction > managed agent deployment models",
        watch_for=("The row about state. That is the one that usually decides "
                   "it in real projects, not cost and not speed."),
    )

    step(1, "Side by side")
    print(f"  {'':<26}{'Agent SDK (self-hosted)':<26}Claude Managed Agents")
    print("  " + "-" * 78)
    for label, a, b in ROWS:
        print(f"  {label:<26}{a:<26}{b}")

    step(2, "Four cases")
    for case, answer, why in CASES:
        print(f"\n  {case}")
        print(f"      -> {answer}")
        print(f"         {why}")

    step(3, "The thing people get wrong")
    print("  These are not tiers. Managed Agents is not 'the advanced option'.")
    print("  It is a different product with a different API - you create an")
    print("  agent, create an environment, start a session, and stream events.")
    print("  You do not import the Agent SDK to use it.")
    note("Managed Agents is in beta and its endpoints require the "
         "managed-agents-2026-04-01 beta header. Its sandboxes can be "
         "Anthropic-managed or self-hosted on your own infrastructure, so "
         "'hosted' is not all-or-nothing.")

    step(4, "Where to read more")
    print("  Agent SDK       https://code.claude.com/docs/en/agent-sdk/overview")
    print("  Managed Agents  https://platform.claude.com/docs/en/managed-agents/overview")

    takeaway(
        points=[
            "Self-hosted: your process runs the loop. Maximum control, and you "
            "own sandboxing, persistence and recovery.",
            "Anthropic-hosted: a managed harness with a sandbox, persistent "
            "sessions and scheduling, reached over REST.",
            "Long-running, unattended or stateful work pushes you toward "
            "managed. Data residency and local files push you toward "
            "self-hosted.",
        ],
        exam_angle=("A scenario will name a constraint - hours of runtime, a "
                    "compliance rule, local filesystem access, no infra team. "
                    "Match the constraint to the deployment model."),
    )


if __name__ == "__main__":
    main()

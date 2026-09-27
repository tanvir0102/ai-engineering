"""
Part 5, demo 4 - the same agent, expressed as a framework would express it.

Run:  python demos/p5_framework_port.py       (no extra packages needed)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client
from core.subagents import classify_with_subagent
from core.tools import list_files, move_file
from core.banner import concept, step, note, takeaway


# ---------------------------------------------------------------------------
# A 20-line stand-in for what every graph framework is doing
# ---------------------------------------------------------------------------
def run_graph(nodes, start, state, limit=60):
    """Each node is f(state) -> (next_node_name, state). 'END' stops."""
    current, hops = start, 0
    while current != "END" and hops < limit:
        hops += 1
        current, state = nodes[current](state)
    return state, hops


def main():
    concept(
        demo_id="P5 / demo 4",
        title="Agentic frameworks: the same loop, with structure imposed on it",
        idea=("Strands, LangGraph and PydanticAI do not add a new capability. "
              "They impose a structure on the loop you already wrote - nodes "
              "and edges, or typed inputs and outputs - so that multi-step "
              "work is easier to read, test and resume."),
        objective="Domain 1 > Agent Patterns and Frameworks > agentic abstraction frameworks",
        watch_for=("The graph below does the Part 3 job with named nodes and "
                   "explicit edges. Nothing about the model call changed. Only "
                   "the way the control flow is written down changed."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "The Part 3 agent, redrawn as a graph")
    print("      survey  ->  classify  ->  file  ->  (more files? back to classify)")
    print("                                       ->  END")

    def survey(state):
        state["queue"] = [f for f in list_files().splitlines()
                          if f.strip().endswith(".txt")]
        state["done"] = []
        print(f"  [survey]   {len(state['queue'])} files queued")
        return ("classify" if state["queue"] else "END"), state

    def classify(state):
        state["current"] = state["queue"].pop(0)
        state["category"], _ = classify_with_subagent(client, state["current"])
        return "file", state

    def file_it(state):
        move_file(state["current"], state["category"])
        state["done"].append((state["current"], state["category"]))
        print(f"  [file]     {state['current']:<40} -> {state['category']}")
        return ("classify" if state["queue"] else "END"), state

    step(2, "Run the graph")
    final_state, hops = run_graph(
        {"survey": survey, "classify": classify, "file": file_it},
        start="survey", state={},
    )
    print(f"\n  nodes visited: {hops}   files handled: {len(final_state['done'])}")

    step(3, "What a real framework adds on top of that")
    print("  LangGraph    an explicit state graph with checkpointing, so a run")
    print("               can be paused, inspected and resumed at a node")
    print("  PydanticAI   typed inputs and outputs with validation, so a step")
    print("               fails loudly on bad data instead of drifting")
    print("  Strands      a model-driven loop with a declarative agent spec")
    note("These are third-party projects with their own release cycles. Learn "
         "the pattern here and read each project's current docs for the exact "
         "API before you write against it.")

    step(4, "When a framework is worth it, and when it is not")
    print("  worth it     many steps, branching, retries, resumable runs,")
    print("               a team that needs to read the flow at a glance")
    print("  not worth it a single tool-use loop, a script you run once,")
    print("               or a case where the Agent SDK already covers you")
    note("A framework is another dependency and another abstraction between "
         "you and the API. That trade is only worth making when the control "
         "flow is genuinely complicated.")

    takeaway(
        points=[
            "Frameworks restructure the loop; they do not replace it. The "
            "model call at the centre is unchanged.",
            "The value is in state handling, branching, retries and "
            "resumability - not in extra model capability.",
            "Know the names (Strands, LangGraph, PydanticAI) and what class of "
            "problem they address.",
        ],
        exam_angle=("Domain 1 names these frameworks explicitly. Expect "
                    "recognition-level questions about what an abstraction "
                    "framework contributes, not questions about a specific "
                    "framework's syntax."),
    )


if __name__ == "__main__":
    main()

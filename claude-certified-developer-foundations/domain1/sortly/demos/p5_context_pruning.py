"""
Part 5, demo 3 - keeping the conversation from bloating.

Run:  python demos/p5_context_pruning.py
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, get_client, MODEL
from core.tools import TOOL_SCHEMAS, run_tool
from core.memory import prune_transcript
from core.banner import concept, step, note, takeaway

SYSTEM = ("You are Sortly. Sort loose files into finance, work, personal or "
          "misc. Read before deciding. Do not delete or rename.")
TOOLS = [t for t in TOOL_SCHEMAS
         if t["name"] in ("list_files", "read_file_head", "move_file")]


def size_of(messages):
    return len(json.dumps(messages, default=str))


def main():
    concept(
        demo_id="P5 / demo 3",
        title="Context-window management: prune the evidence, keep the decisions",
        idea=("Within a single run the conversation only ever grows, and you "
              "resend all of it every turn. Old tool results are usually the "
              "biggest and least useful part, so they are the first thing to "
              "shorten."),
        objective="Domain 1 > Agent Patterns > context-window management",
        watch_for=("The transcript size climbing turn by turn, then the drop "
                   "after pruning - and the check that the most recent turns "
                   "came through untouched."),
    )

    reset_workspace(quiet=True)
    client = get_client()

    step(1, "Build a real transcript and watch it grow")
    messages = [{"role": "user", "content": "Tidy Asha's folder."}]
    sizes = []

    for turn in range(1, 26):
        resp = client.messages.create(model=MODEL, max_tokens=4096,
                                      system=SYSTEM, tools=TOOLS,
                                      messages=messages)
        if resp.stop_reason != "tool_use":
            break   # includes max_tokens; 4096 is ample for this tool set

        a_blocks, results = [], []
        for b in resp.content:
            if getattr(b, "type", "") != "tool_use":
                continue
            out = run_tool(b.name, b.input)
            a_blocks.append({"type": "tool_use", "id": b.id,
                             "name": b.name, "input": b.input})
            results.append({"type": "tool_result", "tool_use_id": b.id,
                            "content": str(out)})
        messages.append({"role": "assistant", "content": a_blocks})
        messages.append({"role": "user", "content": results})

        sizes.append(size_of(messages))
        grew = sizes[-1] - (sizes[-2] if len(sizes) > 1 else 0)
        print(f"  after turn {turn:<3} messages={len(messages):<3} "
              f"transcript={sizes[-1]:>6} chars  (~{sizes[-1]//4:>4} tokens)"
              f"   +{grew}")

    step(2, "Where the bulk actually is")
    tool_chars = sum(len(str(b.get("content", "")))
                     for m in messages if isinstance(m.get("content"), list)
                     for b in m["content"]
                     if isinstance(b, dict) and b.get("type") == "tool_result")
    total = size_of(messages)
    print(f"  whole transcript       : {total:>7} chars")
    print(f"  of that, tool results  : {tool_chars:>7} chars "
          f"({tool_chars * 100 // max(total, 1)}%)")
    note("Those results were file contents. Each one mattered for exactly one "
         "decision and has been dead weight in every request since.")

    step(3, "Prune: cap old tool results at 60 chars, keep the newest turn intact")
    # keep_recent=2 protects only the final turn. With parallel tool calls the
    # whole job finishes in about four turns, so a larger window would protect
    # the very turn that holds all the file contents - and prune nothing.
    pruned, saved = prune_transcript(messages, keep_recent=2, max_result_chars=60)
    after = size_of(pruned)
    print(f"  before : {total:>7} chars  (~{total//4} tokens)")
    print(f"  after  : {after:>7} chars  (~{after//4} tokens)")
    pct = (total - after) * 100 // max(total, 1)
    print(f"  saved  : {total - after:>7} chars ({pct}%) on every remaining turn")
    note("Fourteen files is a small run, so the saving looks small. The shape "
         "is what matters: the cut scales with how much tool output is behind "
         "you, and a long agent run is mostly tool output.")

    step(4, "Check we did not break anything")
    print(f"  message count unchanged      : {len(messages)} -> {len(pruned)}")
    print(f"  task (message 0) untouched   : {pruned[0] == messages[0]}")
    print(f"  newest turn untouched        : {pruned[-2:] == messages[-2:]}")
    kept = sum(1 for m in pruned if isinstance(m.get("content"), list)
               for b in m["content"]
               if isinstance(b, dict) and b.get("type") == "tool_result")
    orig = sum(1 for m in messages if isinstance(m.get("content"), list)
               for b in m["content"]
               if isinstance(b, dict) and b.get("type") == "tool_result")
    print(f"  tool_result blocks kept      : {kept}/{orig}  (must be all of them)")
    note("Pruning must never drop a tool_result block outright. Every tool_use "
         "id still needs its matching result, or the next request is rejected. "
         "Shorten the content; keep the structure.")

    step(5, "The three levers, in order of bluntness")
    print("  prune      shorten or drop old tool output          (this demo)")
    print("  compact    replace old turns with a summary of them")
    print("  isolate    never let the bulk in - use a subagent    (Part 3)")
    note("Isolation is the strongest of the three because it prevents the "
         "growth instead of cleaning up after it.")

    takeaway(
        points=[
            "A long agent run pays for its whole history on every single turn.",
            "Old tool results are the cheapest thing to shorten and the most "
            "expensive thing to keep.",
            "Prune structure-safely: keep every tool_result block, just make "
            "its content smaller.",
        ],
        exam_angle=("Know the vocabulary - context bloat, pruning, compaction, "
                    "context isolation via subagents - and know that isolation "
                    "prevents the problem while pruning treats it."),
    )


if __name__ == "__main__":
    main()

"""
Part 2, demo 1 - the agent loop, written out in full.

Run:  python demos/p2_loop_by_hand.py
"""
# Make sure Python can find the "core" package, which lives one folder up from
# this file. We add that parent folder to the front of the import search path.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

# Helpers shared by all the demos:
#   reset_workspace - put the practice files back to a known starting state
#   get_client      - build the Claude API client
#   MODEL           - the model name string to call
from core._shared import reset_workspace, get_client, MODEL
# TOOL_SCHEMAS - the list of tool definitions we can hand to Claude
# run_tool     - our own function that actually executes a tool by name
from core.tools import TOOL_SCHEMAS, run_tool
# Pretty console output helpers for the walk-through (headings, notes, etc.)
from core.banner import concept, step, note, takeaway

# The system prompt: the standing instructions that tell Claude who it is and
# what the rules are. It is sent on every request but is not part of the
# growing message list.
SYSTEM = ("You are Sortly. Sort loose files into finance, work, personal or misc. "
          "Read a file before deciding if the name is unclear. Do not delete or "
          "rename anything. Stop when the folder is clean.")

# Give Claude only three tools for this demo: two that read (list, peek at the
# top of a file) and one that moves a file. Keeping the tool set small makes
# the loop easier to follow.
READ_ONLY_PLUS_MOVE = [t for t in TOOL_SCHEMAS
                       if t["name"] in ("list_files", "read_file_head", "move_file")]


def main():
    concept(
        demo_id="P2 / demo 1",
        title="The agent loop is a while-loop",
        idea=("An agent is not a special kind of model. It is an ordinary loop "
              "around an ordinary API call: send the conversation, check "
              "stop_reason, run the tool Claude asked for, append the result, "
              "send again."),
        objective="Domain 1 > Agent Construction > custom agent loops and harnesses",
        watch_for=("The message list. It starts with one message and grows by "
                   "two on every turn - one assistant turn holding the tool "
                   "request, one user turn holding the tool result. That growth "
                   "is why long agent runs get expensive."),
    )

    # Start from a clean, known folder, then build the API client.
    reset_workspace(quiet=True)
    client = get_client()

    step(1, "The six lines that matter")
    print("""
      messages = [ the task ]
      loop:
          resp = client.messages.create(model=..., tools=..., messages=messages)
          if resp.stop_reason == "max_tokens":  ->  turn was cut off, stop
          if resp.stop_reason != "tool_use":    ->  done, return the text
          for each tool_use block:              ->  result = run_tool(name, input)
          messages += [assistant turn, user turn of tool_result blocks]
    """)
    note("That is the entire idea. Everything else is convenience.")

    step(2, "Run it, and print the conversation length after every turn")
    # The conversation starts as a list with ONE user message: the task.
    # Every turn of the loop will append more messages to this list.
    messages = [{"role": "user", "content":
                 "Sort the three smallest files in Asha's folder, then stop."}]
    turn = 0  # counts how many times we have called the API

    # Hard turn limit: even if something goes wrong, the loop can never run
    # more than 12 times.
    while turn < 12:
        turn += 1

        # Send the WHOLE conversation so far, plus the system prompt and the
        # list of tools. Claude replies with one response object.
        resp = client.messages.create(
            model=MODEL, max_tokens=4096, system=SYSTEM,
            tools=READ_ONLY_PLUS_MOVE, messages=messages,
        )

        # Case 1: the reply was cut off because it hit the max_tokens budget.
        # Claude was mid-sentence, so the turn is incomplete. Stop and warn.
        if resp.stop_reason == "max_tokens":
            print(f"  turn {turn:<3} stop_reason=max_tokens -> turn was cut off")
            print("           Claude was still writing tool calls when the")
            print("           budget ran out. Raise max_tokens and re-run.")
            break

        # Case 2: stop_reason is anything other than "tool_use" (normally
        # "end_turn"). Claude did not ask for a tool, so it is done. Pull the
        # plain-text blocks out of the reply and print them as the answer.
        if resp.stop_reason != "tool_use":
            final = "".join(b.text for b in resp.content
                            if getattr(b, "type", "") == "text")
            print(f"  turn {turn:<3} stop_reason=end_turn   -> loop exits")
            print(f"\n  final answer: {final.strip()[:160]}")
            break

        # Case 3: stop_reason == "tool_use". Claude asked to run one or more
        # tools. We collect two parallel lists:
        #   assistant_blocks - the tool requests, echoed back to Claude
        #   results          - the matching tool results we produce
        assistant_blocks, results = [], []
        for b in resp.content:
            # A reply can also contain text blocks; skip anything that is not
            # a tool request.
            if getattr(b, "type", "") != "tool_use":
                continue

            # WE run the tool, not Claude. run_tool looks up the function by
            # name and calls it with the input Claude provided.
            out = run_tool(b.name, b.input)
            print(f"  turn {turn:<3} stop_reason=tool_use   -> {b.name}"
                  f"({b.input.get('filename','')})")

            # Echo the exact request back into the conversation.
            assistant_blocks.append({"type": "tool_use", "id": b.id,
                                     "name": b.name, "input": b.input})
            # Pair the result to the request using the SAME id. Every
            # tool_use must get exactly one tool_result, in the same order.
            results.append({"type": "tool_result", "tool_use_id": b.id,
                            "content": str(out)})

        # The conversation grows by two messages per turn: the assistant turn
        # holding the tool requests, then the user turn holding the results.
        messages.append({"role": "assistant", "content": assistant_blocks})
        messages.append({"role": "user", "content": results})
        print(f"           messages in conversation: {len(messages)}")

    step(3, "What the loop needed from you")
    print("  - a stopping condition (stop_reason != 'tool_use')")
    print("  - a max_tokens big enough to hold a whole turn of tool calls")
    print("  - a hard turn limit, so a confused agent cannot spin forever")
    print("  - tool results appended in the SAME order as the tool_use blocks")
    print("  - every tool_use block answered with exactly one tool_result block")
    note("Miss the pairing rule and the next request is rejected by the API. "
         "Set max_tokens too low and the turn is truncated mid-write - "
         "stop_reason comes back 'max_tokens', and a careless loop reads that "
         "as 'finished' and exits having done nothing.")

    takeaway(
        points=[
            "The model never runs a tool. It emits a tool_use block; your code "
            "runs the function and hands the result back.",
            "stop_reason is the control flow. 'tool_use' means keep looping, "
            "anything else means stop.",
            "The conversation grows by two messages per turn, and you resend "
            "all of it every time. That is the cost curve of a long agent run.",
            "Claude batches tool calls in parallel, so one turn can hold many. "
            "max_tokens must be big enough for all of them.",
        ],
        exam_angle=("Expect questions on who executes the tool (you, not "
                    "Claude), on pairing every tool_use id with a tool_result, "
                    "and on why a turn limit belongs in every loop."),
    )


# Only run main() when this file is executed directly (not when imported).
if __name__ == "__main__":
    main()

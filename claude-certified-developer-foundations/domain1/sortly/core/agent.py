"""
The agent loop, written by hand.

This is the whole idea of an agent. There is no hidden machinery:

    send the conversation ->
      did Claude ask for a tool?
        no  -> we are done
        yes -> run the tool, append the result, send again

Everything else in this course (the Agent SDK, subagents, hooks, frameworks)
is a nicer way of running this same loop. Read this file once and the rest
stops looking magical.
"""

from core._shared import MODEL, usage_of
from core.tools import TOOL_SCHEMAS, run_tool


class Ledger:
    """Counts tokens and tool calls so demos can compare two approaches."""

    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.tool_calls = 0
        self.turns = 0

    def add(self, resp):
        i, o = usage_of(resp)
        self.input_tokens += i
        self.output_tokens += o
        self.turns += 1

    def line(self, label):
        return (f"{label:<28} turns={self.turns:<3} tools={self.tool_calls:<3} "
                f"in={self.input_tokens:<7} out={self.output_tokens}")


# Claude issues tool calls in parallel - it can ask for five reads, or a dozen
# moves, inside a single turn. Every one of those blocks is output tokens. A
# small max_tokens truncates the turn, stop_reason comes back "max_tokens"
# instead of "tool_use", and a naive loop mistakes that for "finished".
MAX_TOKENS = 4096


def run_agent(client, task, system, tools=None, max_turns=40,
              before_tool=None, on_event=None, model=MODEL,
              max_tokens=MAX_TOKENS):
    """Run the loop until Claude stops asking for tools.

    client      : anything with .messages.create
    task        : the first user message
    system      : the system prompt
    tools       : list of tool schemas (defaults to all five)
    max_turns   : hard stop, so a confused agent cannot spin forever
    before_tool : optional guard, called as before_tool(name, args).
                  Return None to allow, or a string to block the call and
                  send that string back as the tool result. This is the seam
                  that Part 4 turns into a hook.
    on_event    : optional callback for printing, called as
                  on_event(kind, payload)
    """
    tools = TOOL_SCHEMAS if tools is None else tools
    ledger = Ledger()
    messages = [{"role": "user", "content": task}]

    for _ in range(max_turns):
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            tools=tools,
            messages=messages,
        )
        ledger.add(resp)

        # The turn was cut off mid-generation. This is NOT "finished" - the
        # tool calls it was writing are incomplete and cannot be sent back.
        if resp.stop_reason == "max_tokens":
            msg = (f"STOPPED: the model hit max_tokens ({max_tokens}) while "
                   f"writing turn {ledger.turns}. Its tool calls were cut off "
                   f"mid-write, so the run cannot continue. Raise max_tokens.")
            if on_event:
                on_event("final", msg)
            return msg, ledger

        # Claude did not ask for a tool -> the task is finished.
        if resp.stop_reason != "tool_use":
            final = "".join(b.text for b in resp.content
                            if getattr(b, "type", "") == "text")
            if on_event:
                on_event("final", final)
            return final, ledger

        # Claude asked for one or more tools. Run each, collect the results.
        assistant_blocks, results = [], []
        for block in resp.content:
            if getattr(block, "type", "") == "text":
                assistant_blocks.append({"type": "text", "text": block.text})
                continue
            if getattr(block, "type", "") != "tool_use":
                continue

            assistant_blocks.append({
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": block.input,
            })

            blocked = before_tool(block.name, block.input) if before_tool else None
            if blocked is not None:
                output = blocked
                if on_event:
                    on_event("blocked", (block.name, block.input, output))
            else:
                output = run_tool(block.name, block.input)
                ledger.tool_calls += 1
                if on_event:
                    on_event("tool", (block.name, block.input, output))

            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(output),
            })

        messages.append({"role": "assistant", "content": assistant_blocks})
        messages.append({"role": "user", "content": results})

    return "STOPPED: hit max_turns before finishing.", ledger

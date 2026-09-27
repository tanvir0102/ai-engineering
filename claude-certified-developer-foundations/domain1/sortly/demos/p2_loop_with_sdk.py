"""
Part 2, demo 2 - the same agent, on the Claude Agent SDK.

Run:  python demos/p2_loop_with_sdk.py
Needs: uv add claude-agent-sdk     (and a real ANTHROPIC_API_KEY)
"""
import sys, pathlib, asyncio
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, MODEL, ROOT
from core.banner import concept, step, note, takeaway
from core import sdk_tools

PROMPT = ("Sort every loose file in this folder into finance, work, personal "
          "or misc, using only the sortly tools. Read a file before deciding "
          "if its name is unclear. Do not delete or rename anything.")


async def run_sdk():
    from claude_agent_sdk import (
        query, ClaudeAgentOptions, AssistantMessage, ResultMessage,
        TextBlock, ToolUseBlock,
    )

    server = sdk_tools.build_server(include_delete=False)
    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt="You are Sortly, a tidy-up assistant for Asha's folder.",
        mcp_servers={sdk_tools.SERVER_NAME: server},
        allowed_tools=sdk_tools.ALLOWED_TOOLS[:4],   # no delete_file at all
        setting_sources=[],        # ignore CLAUDE.md and settings.json on disk
        max_turns=40,
        cwd=str(ROOT),
    )

    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    arg = (block.input or {}).get("filename", "")
                    print(f"  -> {block.name.split('__')[-1]:<15} {arg}")
                elif isinstance(block, TextBlock) and block.text.strip():
                    print(f"     {block.text.strip()[:100]}")
        elif isinstance(message, ResultMessage):
            print(f"\n  turns      : {message.num_turns}")
            print(f"  cost (est) : ${message.total_cost_usd}")
            print(f"  usage      : {message.usage}")


def main():
    concept(
        demo_id="P2 / demo 2",
        title="The Claude Agent SDK runs the same loop for you",
        idea=("The SDK is the loop from demo 1, already written, plus retries, "
              "session handling, permissions and context compaction. Your tool "
              "functions do not change - only how you declare and launch them."),
        objective="Domain 1 > Agent Construction > the Claude Agent SDK",
        watch_for=("The same sequence of tool calls as the hand-written loop. "
                   "No while-loop appears anywhere in this file, and no "
                   "stop_reason check either."),
    )

    step(1, "What changed from demo 1")
    print("  hand-written loop                 Agent SDK")
    print("  " + "-" * 66)
    print("  dict with 'input_schema'          @tool decorator")
    print("  your while-loop                   query(...) async iterator")
    print("  you check stop_reason             the SDK checks it")
    print("  you append tool_result blocks     the SDK appends them")
    print("  you count tokens yourself         ResultMessage.usage")
    note("The SDK bundles the Claude Code CLI, so it needs Node on the machine. "
         "That is a real deployment consideration, not a detail.")

    step(2, "Run the agent through the SDK")
    if not sdk_tools.SDK_AVAILABLE:
        raise SystemExit(
            "  claude-agent-sdk is not installed.\n"
            "      uv add claude-agent-sdk\n"
            "  It bundles the Claude Code CLI, which needs Node on the machine.\n"
            "  Check with:  node --version"
        )
    reset_workspace(quiet=True)
    asyncio.run(run_sdk())

    step(3, "Two options worth noticing in the code above")
    print("  setting_sources=[]   ignore CLAUDE.md, settings.json and skills on")
    print("                       disk, so this run depends only on this file")
    print("  allowed_tools=[...]  the four safe tools are auto-approved;")
    print("                       delete_file was never built into the server")
    note("allowed_tools is an approval list, not a restriction list. Leaving a "
         "tool out of it does not remove the tool - use disallowed_tools, or "
         "simply never register it, as we did here.")
    note("You may see a built-in tool such as ToolSearch in the trace above. "
         "That is the SDK's own tooling, not one of ours, and it is proof of "
         "the point: naming four tools in allowed_tools approved those four, "
         "it did not forbid everything else.")

    takeaway(
        points=[
            "The Agent SDK is a harness: it owns the loop, you own the tools "
            "and the policy.",
            "Custom tools become an in-process MCP server, so they run inside "
            "your program with no subprocess and no socket.",
            "Choose it over a hand-written loop when you want sessions, "
            "permissions, compaction and retries without writing them.",
        ],
        exam_angle=("Know the four ways to build: Messages API plus your own "
                    "loop, the Agent SDK, the Claude Code CLI, and Claude "
                    "Managed Agents. The next demo separates the last two."),
    )


if __name__ == "__main__":
    main()

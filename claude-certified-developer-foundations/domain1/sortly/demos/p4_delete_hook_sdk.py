"""
Part 4, demo 3 - the same guard as a real Agent SDK PreToolUse hook.

Run:  python demos/p4_delete_hook_sdk.py
Needs: uv add claude-agent-sdk     (and a real ANTHROPIC_API_KEY)
"""
import sys, pathlib, asyncio
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from core._shared import reset_workspace, MODEL, ROOT, WORKSPACE
from core.banner import concept, step, note, takeaway
from core.hooks import block_deletes
from core import sdk_tools

PROMPT = ("Sort every loose file into finance, work, personal or misc using the "
          "sortly tools, and delete any duplicate files you find.")


async def run_sdk():
    from claude_agent_sdk import (
        query, ClaudeAgentOptions, HookMatcher,
        AssistantMessage, ResultMessage, ToolUseBlock,
    )

    server = sdk_tools.build_server(include_delete=True)
    options = ClaudeAgentOptions(
        model=MODEL,
        system_prompt="You are Sortly, tidying Asha's folder.",
        mcp_servers={sdk_tools.SERVER_NAME: server},
        allowed_tools=sdk_tools.ALLOWED_TOOLS,
        setting_sources=[],
        max_turns=40,
        cwd=str(ROOT),
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="mcp__sortly__delete_file",
                            hooks=[block_deletes]),
            ]
        },
    )

    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"  -> {block.name.split('__')[-1]:<15} "
                          f"{(block.input or {}).get('filename','')}")
        elif isinstance(message, ResultMessage):
            print(f"\n  permission_denials: {message.permission_denials}")

    print(f"  resumes intact: {sorted(p.name for p in WORKSPACE.rglob('*Resume*'))}")


def main():
    concept(
        demo_id="P4 / demo 3",
        title="The same guard, wired into the Agent SDK",
        idea=("The guard from demo 2 is not tied to a hand-written loop. In "
              "the Agent SDK it becomes a PreToolUse hook, registered with a "
              "matcher that selects which tools it applies to."),
        objective="Domain 1 > Agent Construction > hooks, in the SDK",
        watch_for=("The shape of the return value. A hook that allows returns "
                   "an empty dict. A hook that refuses returns a "
                   "hookSpecificOutput with permissionDecision set to 'deny'."),
    )

    step(1, "The hook, as the SDK wants it")
    print("""
      async def block_deletes(input_data, tool_use_id, context):
          if not input_data["tool_name"].endswith("delete_file"):
              return {}                                  # allow
          return {"hookSpecificOutput": {
              "hookEventName": "PreToolUse",
              "permissionDecision": "deny",
              "permissionDecisionReason": "delete_file is blocked by policy",
          }}

      options = ClaudeAgentOptions(
          hooks={"PreToolUse": [HookMatcher(matcher="mcp__sortly__delete_file",
                                            hooks=[block_deletes])]},
      )
    """)
    note("matcher filters which tool names reach the hook. Leave it out and "
         "the hook fires for every tool call.")

    step(2, "Where a hook sits in the permission chain")
    print("  1. hooks           <- runs first, and can deny outright")
    print("  2. deny rules      (disallowed_tools, settings.json)")
    print("  3. ask rules")
    print("  4. allow rules     (allowed_tools)")
    print("  5. permission_mode / can_use_tool callback")
    note("Because hooks run first, a hook denial cannot be overridden by an "
         "allow rule or by bypassPermissions. That is why destructive-action "
         "guards belong in a hook rather than in a permission callback.")

    step(3, "Run it")
    if not sdk_tools.SDK_AVAILABLE:
        raise SystemExit(
            "  claude-agent-sdk is not installed.\n"
            "      uv add claude-agent-sdk"
        )
    reset_workspace(quiet=True)
    asyncio.run(run_sdk())

    takeaway(
        points=[
            "One guard, two harnesses: a plain function in your own loop, a "
            "PreToolUse hook in the SDK. The policy did not change.",
            "Hooks are evaluated before deny rules, allow rules and permission "
            "modes, so they are the strongest place to put a hard stop.",
            "PreToolUse can also return 'allow', 'ask' or 'defer', and can "
            "rewrite the tool input before it runs.",
        ],
        exam_angle=("Recognise the vocabulary: PreToolUse, matcher, "
                    "permissionDecision, permissionDecisionReason. And "
                    "remember hooks run first in the evaluation order."),
    )


if __name__ == "__main__":
    main()

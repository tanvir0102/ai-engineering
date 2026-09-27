"""
Guards.

A hook is code that runs BEFORE a tool executes and can refuse it. The
difference from a system prompt instruction is not politeness - it is where
the decision is made:

    system prompt  ->  the model decides whether to obey.       Probabilistic.
    hook           ->  your code decides whether to allow.      Deterministic.

The same guard appears twice below: once as a plain function for the
hand-written loop, once shaped for the Claude Agent SDK's PreToolUse hook.
"""

from core._shared import CATEGORIES

PROTECTED = "originals in the workspace root"


# ---------------------------------------------------------------------------
# 1. For the hand-written loop in core/agent.py
# ---------------------------------------------------------------------------
def guard(tool_name, args):
    """Return None to allow, or a string to block and report back to Claude."""
    if tool_name == "delete_file":
        return (f"BLOCKED by hook: delete_file is not permitted on {PROTECTED}. "
                f"Requested file: {args.get('filename')!r}. "
                "Move it to misc/ instead, or ask a human.")

    if tool_name == "move_file" and args.get("category") not in CATEGORIES:
        return (f"BLOCKED by hook: '{args.get('category')}' is not a category. "
                f"Allowed: {', '.join(CATEGORIES)}.")

    return None


# ---------------------------------------------------------------------------
# 2. For the Claude Agent SDK
# ---------------------------------------------------------------------------
# PreToolUse hooks receive (input_data, tool_use_id, context) and return a dict.
# Returning {} allows the call. To refuse, set permissionDecision to "deny".
# Reference: https://code.claude.com/docs/en/agent-sdk/hooks
async def block_deletes(input_data, tool_use_id, context):
    tool_name = input_data.get("tool_name", "")
    if not tool_name.endswith("delete_file"):
        return {}

    target = (input_data.get("tool_input") or {}).get("filename", "")
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"delete_file is blocked by policy. Refused: {target!r}"
            ),
        }
    }

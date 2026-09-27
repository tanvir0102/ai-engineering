"""
The same five tools, wrapped for the Claude Agent SDK.

Two things change and nothing else does:

  1. The schema is written with the @tool decorator instead of a dict.
  2. The tools are collected into an in-process MCP server. "In-process"
     means it runs inside this Python program - there is no subprocess and
     no socket, unlike a normal MCP server.

The function bodies are imported unchanged from core/tools.py. That is the
point of this file: switching harness does not mean rewriting your tools.

Reference: https://code.claude.com/docs/en/agent-sdk/python
"""

from core.tools import (
    list_files, read_file_head, move_file, rename_file, delete_file,
)

try:
    from claude_agent_sdk import tool, create_sdk_mcp_server
    SDK_AVAILABLE = True
except ImportError:                     # SDK not installed yet
    SDK_AVAILABLE = False

# The SDK exposes MCP tools as mcp__<server name>__<tool name>.
SERVER_NAME = "sortly"
ALLOWED_TOOLS = [
    f"mcp__{SERVER_NAME}__list_files",
    f"mcp__{SERVER_NAME}__read_file_head",
    f"mcp__{SERVER_NAME}__move_file",
    f"mcp__{SERVER_NAME}__rename_file",
    f"mcp__{SERVER_NAME}__delete_file",
]


def _text(s):
    """Every SDK tool returns MCP content blocks, not a bare string."""
    return {"content": [{"type": "text", "text": str(s)}]}


def build_server(include_delete=True):
    """Build the in-process MCP server. Import-safe when the SDK is missing."""
    if not SDK_AVAILABLE:
        raise RuntimeError("claude-agent-sdk is not installed")

    @tool("list_files", "List the loose, unsorted files in Asha's folder.", {})
    async def _list(args):
        return _text(list_files())

    @tool("read_file_head", "Read the first lines of one file.",
          {"filename": str, "lines": int})
    async def _read(args):
        return _text(read_file_head(args["filename"], args.get("lines", 8)))

    @tool("move_file", "Move a file into finance, work, personal or misc.",
          {"filename": str, "category": str})
    async def _move(args):
        return _text(move_file(args["filename"], args["category"]))

    @tool("rename_file", "Give a file a clearer name, keeping the .txt suffix.",
          {"filename": str, "new_name": str})
    async def _rename(args):
        return _text(rename_file(args["filename"], args["new_name"]))

    @tool("delete_file", "Permanently delete a file. Cannot be undone.",
          {"filename": str, "reason": str})
    async def _delete(args):
        return _text(delete_file(args["filename"], args.get("reason", "")))

    tools = [_list, _read, _move, _rename]
    if include_delete:
        tools.append(_delete)

    return create_sdk_mcp_server(name=SERVER_NAME, version="1.0.0", tools=tools)

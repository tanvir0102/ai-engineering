"""
Sortly's five tools.

A "tool" is two separate things and it helps to keep them apart:

  1. A SCHEMA  - a JSON description you send to Claude. Claude reads it and
                 decides whether to ask for the tool. Claude never runs it.
  2. A FUNCTION - ordinary Python in your process. You run it when Claude asks.

Everything below the schema list is your code, running on your machine.
"""

from pathlib import Path

from core._shared import WORKSPACE, CATEGORIES

# ---------------------------------------------------------------------------
# 1. The schemas Claude sees
# ---------------------------------------------------------------------------
# Tool descriptions are prompt text. A vague description produces a confused
# agent, so each one says what the tool does AND when to reach for it.

TOOL_SCHEMAS = [
    {
        "name": "list_files",
        "description": (
            "List the files sitting loose in Asha's folder that have not been "
            "sorted into a category folder yet. Call this first to find out "
            "what needs handling."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "read_file_head",
        "description": (
            "Read the first few lines of one file so you can tell what it "
            "actually is. Use this when the filename alone is not enough."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Exact filename to read."},
                "lines": {"type": "integer", "description": "How many lines. Default 8."},
            },
            "required": ["filename"],
        },
    },
    {
        "name": "move_file",
        "description": (
            "Move one file into a category folder. Categories are: "
            "finance, work, personal, misc. Use misc only when the file "
            "genuinely fits none of the others."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "category": {"type": "string", "enum": CATEGORIES},
            },
            "required": ["filename", "category"],
        },
    },
    {
        "name": "rename_file",
        "description": (
            "Give a file a clearer name. Keep the .txt extension. Use this for "
            "files named things like untitled_1.txt."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "new_name": {"type": "string"},
            },
            "required": ["filename", "new_name"],
        },
    },
    {
        "name": "delete_file",
        "description": (
            "Permanently delete a file. This cannot be undone. Only use it for "
            "a file that is an exact duplicate of another file you have already "
            "confirmed by reading both."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["filename", "reason"],
        },
    },
]


# ---------------------------------------------------------------------------
# 2. The path jail
# ---------------------------------------------------------------------------
def _safe(filename):
    """Resolve a filename inside workspace/ and refuse anything that escapes.

    Claude proposes strings. Strings can contain "../../etc/passwd". The jail
    is your code's job, not the model's - never trust the path you were handed.
    """
    target = (WORKSPACE / filename).resolve()
    root = WORKSPACE.resolve()
    if root not in target.parents and target != root:
        raise ValueError(f"path escapes the workspace: {filename}")
    return target


# ---------------------------------------------------------------------------
# 3. The functions
# ---------------------------------------------------------------------------
def list_files(**_):
    names = sorted(p.name for p in WORKSPACE.iterdir() if p.is_file())
    if not names:
        return "No loose files left. Everything is sorted."
    return "\n".join(names)


def read_file_head(filename, lines=8, **_):
    p = _safe(filename)
    if not p.exists():
        return f"ERROR: no such file: {filename}"
    text = p.read_text(errors="replace").splitlines()[: int(lines)]
    return "\n".join(text) if text else "(file is empty)"


def move_file(filename, category, **_):
    if category not in CATEGORIES:
        return f"ERROR: unknown category '{category}'. Use one of {CATEGORIES}."
    src = _safe(filename)
    if not src.exists():
        return f"ERROR: no such file: {filename}"
    dest_dir = WORKSPACE / category
    dest_dir.mkdir(exist_ok=True)
    src.rename(dest_dir / src.name)
    return f"moved {filename} -> {category}/"


def rename_file(filename, new_name, **_):
    src = _safe(filename)
    dst = _safe(new_name)
    if not src.exists():
        return f"ERROR: no such file: {filename}"
    if dst.exists():
        return f"ERROR: {new_name} already exists"
    src.rename(dst)
    return f"renamed {filename} -> {new_name}"


def delete_file(filename, reason="", **_):
    p = _safe(filename)
    if not p.exists():
        return f"ERROR: no such file: {filename}"
    p.unlink()
    return f"DELETED {filename} (reason given: {reason})"


REGISTRY = {
    "list_files": list_files,
    "read_file_head": read_file_head,
    "move_file": move_file,
    "rename_file": rename_file,
    "delete_file": delete_file,
}


def run_tool(name, args):
    """Dispatch one tool call. Errors come back as text, not exceptions.

    An exception kills your loop. A string that starts with ERROR: goes back
    to Claude as a tool result, and Claude can try something else.
    """
    fn = REGISTRY.get(name)
    if fn is None:
        return f"ERROR: no tool named {name}"
    try:
        return fn(**args)
    except Exception as exc:  # noqa: BLE001 - deliberate: report, don't crash
        return f"ERROR: {type(exc).__name__}: {exc}"

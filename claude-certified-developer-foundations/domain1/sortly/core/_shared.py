"""
Shared plumbing for every Sortly demo: model IDs, the client, and paths.

Nothing here is a Domain 1 concept on its own. It exists so that the demo
scripts stay short enough to read on screen.
"""

import os
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Load .env
# ---------------------------------------------------------------------------
# Nothing reads .env for you. os.environ only sees variables that were already
# set in your shell, so a key sitting in a file is invisible until something
# loads it. This runs once, when the first demo imports this module.

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def load_env(path=ENV_FILE, override=False):
    """Read KEY=value lines from .env into os.environ.

    Real shell variables win by default, which is why override is False - if
    you exported ANTHROPIC_API_KEY in your terminal, that one is used.
    """
    if not path.exists():
        return False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value
    return True


ENV_LOADED = load_env()

# ---------------------------------------------------------------------------
# Model IDs
# ---------------------------------------------------------------------------
# Always pin an exact model ID. Never write "latest" or invent an alias.
#
# From the Claude 4.6 generation onward the dateless ID *is* the pinned
# snapshot - "claude-sonnet-5" does not drift to a newer model later.
# Older models such as claude-sonnet-4-5 have a dated ID plus a convenience
# alias that does move. Verified against:
#   https://platform.claude.com/docs/en/about-claude/models/overview
#
MODEL = "claude-sonnet-5"                  # the workhorse for these demos
FAST_MODEL = "claude-haiku-4-5-20251001"   # cheaper model, used by the Part 3 subagent
#
# Note the two different shapes above, and why both are pinned:
#   claude-sonnet-5            - 4.6-generation and later. The dateless ID IS
#                                the pinned snapshot. Safe to ship.
#   claude-haiku-4-5-20251001  - pre-4.6. Here the dateless "claude-haiku-4-5"
#                                is only a convenience ALIAS that moves to the
#                                newest snapshot, so we write the dated ID.

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "workspace_seed"        # the pristine copy, never modified
WORKSPACE = ROOT / "workspace"        # the messy folder the demos act on
MEMORY_FILE = ROOT / "sortly_memory.json"

CATEGORIES = ["finance", "work", "personal", "misc"]


def reset_workspace(quiet=False):
    """Restore workspace/ from workspace_seed/. The demos really move files."""
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)
    shutil.copytree(SEED, WORKSPACE)
    for name in CATEGORIES:
        (WORKSPACE / name).mkdir(exist_ok=True)
    if not quiet:
        print(f"workspace reset: {len(list(SEED.iterdir()))} files restored")


def get_client():
    """Return the Anthropic client. Reads ANTHROPIC_API_KEY from the environment.

    Every demo that talks to a model goes through here, so there is exactly one
    place where the client is built and one place where a missing key is
    reported.
    """
    try:
        import anthropic
    except ImportError:
        raise SystemExit(
            "The anthropic package is not installed.\n"
            "  Run:  uv sync      (from the project root)"
        )
    if not os.environ.get("ANTHROPIC_API_KEY"):
        found = "found" if ENV_FILE.exists() else "NOT found"
        raise SystemExit(
            f"ANTHROPIC_API_KEY is not set.\n"
            f"  looked for a .env at: {ENV_FILE}  ({found})\n"
            "  The line must read exactly:  ANTHROPIC_API_KEY=sk-ant-...\n"
            "  - no 'export', no spaces around the =, no quotes needed\n"
            "  - the file must be named .env, not .env.txt"
        )
    return anthropic.Anthropic()


def ask_claude(client, prompt, system=None, model=MODEL, max_tokens=1024):
    """One plain request/response call. No tools, no loop."""
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    resp = client.messages.create(**kwargs)
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def usage_of(resp):
    """Pull (input_tokens, output_tokens) off a response."""
    u = getattr(resp, "usage", None)
    if u is None:
        return 0, 0
    return getattr(u, "input_tokens", 0), getattr(u, "output_tokens", 0)

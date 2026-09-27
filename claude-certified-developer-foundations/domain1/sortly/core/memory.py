"""
Memory and transcript pruning.

Two different things share the word "memory", and mixing them up is a common
beginner mistake:

  WITHIN a run   - the conversation list. It grows every turn and you resend
                   all of it. Managing it is context-window management
                   (pruning, compaction).

  BETWEEN runs   - state you write to disk yourself. The model has none of
                   this by default; every run starts blank.

This file has one of each.
"""

import json
import time

from core._shared import MEMORY_FILE


# ---------------------------------------------------------------------------
# Between runs: a JSON file you own
# ---------------------------------------------------------------------------
def load_memory():
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_memory(mem):
    MEMORY_FILE.write_text(json.dumps(mem, indent=2))


def remember(mem, filename, category):
    mem[filename] = {"category": category, "seen_at": time.strftime("%Y-%m-%d")}
    return mem


def recall(mem, filename):
    entry = mem.get(filename)
    return entry["category"] if entry else None


def forget_all():
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()


# ---------------------------------------------------------------------------
# Within a run: keep the conversation from bloating
# ---------------------------------------------------------------------------
def prune_transcript(messages, keep_recent=6, max_result_chars=200):
    """Shorten old tool results, leave recent turns untouched.

    Why tool results and not the whole message: a tool result is usually the
    biggest thing in the conversation and the least useful later. The decision
    it led to is already recorded in the assistant turn that followed it.

    Never prune the first user message - that is the task itself.
    """
    if len(messages) <= keep_recent + 1:
        return messages, 0

    pruned, saved = [], 0
    cutoff = len(messages) - keep_recent

    for i, m in enumerate(messages):
        if i == 0 or i >= cutoff or not isinstance(m.get("content"), list):
            pruned.append(m)
            continue

        blocks = []
        for b in m["content"]:
            if isinstance(b, dict) and b.get("type") == "tool_result":
                text = str(b.get("content", ""))
                if len(text) > max_result_chars:
                    saved += len(text) - max_result_chars
                    text = text[:max_result_chars] + "\n...[pruned]"
                blocks.append({**b, "content": text})
            else:
                blocks.append(b)
        pruned.append({**m, "content": blocks})

    return pruned, saved

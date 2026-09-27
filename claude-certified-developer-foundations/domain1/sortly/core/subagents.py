"""
The classifier subagent.

A subagent is not a special object. It is a SEPARATE conversation with its own
system prompt, its own (usually smaller) tool set, and its own context window.

It exists for one reason: the manager gets the subagent's *conclusion* instead
of the subagent's *evidence*. One word comes back instead of a whole document,
so the manager's context stays small no matter how many files there are.
"""

from core._shared import FAST_MODEL, usage_of, CATEGORIES
from core.tools import read_file_head

SUBAGENT_SYSTEM = (
    "You classify one file for Asha's folder in Pune.\n"
    "Answer with exactly one word from this list: finance, work, personal, misc.\n"
    "No punctuation, no explanation, no other words."
)


def classify_with_subagent(client, filename, ledger=None, lines=8):
    """Spawn a fresh, throwaway conversation to classify one file.

    Note what is NOT here: no history, no other files, no tools. The subagent
    cannot see anything except the snippet it is given, which is exactly the
    isolation we want.
    """
    snippet = read_file_head(filename, lines=lines)

    resp = client.messages.create(
        model=FAST_MODEL,               # a cheap model is plenty for one word
        max_tokens=8,                   # a hard ceiling on a one-word answer
        system=SUBAGENT_SYSTEM,
        messages=[{"role": "user",
                   "content": f"File name: {filename}\n\nFirst lines:\n{snippet}"}],
    )

    if ledger is not None:
        i, o = usage_of(resp)
        ledger.input_tokens += i
        ledger.output_tokens += o
        ledger.turns += 1

    text = "".join(b.text for b in resp.content
                   if getattr(b, "type", "") == "text").strip().lower()

    # Never trust free text. Validate against the allowed set before using it.
    for c in CATEGORIES:
        if c in text:
            return c, snippet
    return "misc", snippet

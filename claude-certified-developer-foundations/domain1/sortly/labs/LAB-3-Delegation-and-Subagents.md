# LAB 3 — Delegation and subagents

**Tool used in this lab:** Messages API throughout — one conversation for the manager, plus a fresh short conversation per file for the subagent

> **Before you start:** activate the environment you created in Lab 0.
> ```bash
> .venv\Scripts\activate
> ```
> On WSL, macOS or Linux: `source .venv/bin/activate`. Your prompt should show
> `(sortly)`.

In Lab 2 you watched the message list grow by two every turn, and you resend all
of it on every call. This lab measures what that costs when an agent reads
fourteen files — and then fixes it.

## What this lab teaches

1. One agent that reads everything ends up **carrying** everything, for the rest of the run.
2. The evidence (a whole file) is big. The conclusion (one word) is tiny. Only the conclusion mattered.
3. A subagent is a **separate conversation** with its own context, prompt and tools — not a separate library.
4. Delegation buys **context isolation**: the manager's context stops growing with the size of the job.
5. Isolation has a price — the specialist loses the bigger picture.

---

## Demo 1 — One flat agent

**Tool used:** Messages API, one conversation

| | |
|---|---|
| **The problem** | Lab 2 showed the conversation growing every turn. What does that cost on a real job? |
| **The concept** | One agent that reads everything ends up **carrying** everything. |
| **The purpose of this demo** | Put a number on the waste before fixing it. |
| **How we solve it** | We do not, yet. This demo measures the problem. |

**What we will do:** run the whole job in one context and record the token bill.

**`demos/p3_manager_flat.py`** — runs a single agent over all fourteen files and
prints how many characters each read adds to the conversation. It saves its
input-token total so the next demo can compare against it.

### Step 1 — Run the flat agent

```bash
python demos/p3_manager_flat.py
```

### Step 2 — Watch the `+N chars into context` counter

Each read is a whole file body entering the conversation permanently.

### Step 3 — Write down the input-token total from step 2

You will compare against it in a moment.

---

### In simple words — what demo 1 is teaching

The whole demo teaches **one sentence**: one agent that reads everything ends up
**carrying** everything.

It read all 14 files, then moved all 14. That part worked fine. The problem is
what happened in between.

**Every file it read stayed in its head.** By the time it moved the last file,
it was still hauling around the full text of the grocery list, the wedding
invite, the electricity bill — all of it. And remember Lab 2: the whole
conversation is resent on *every* turn.

**The number to write down:**

```
in = 17,627 input tokens
```

Here is where the waste is. Each file was read to answer **one question**: which
folder does this belong in? The answer is a single word — `finance`. But you
paid to carry those 240 characters through the rest of the run, long after that
word had been decided.

**Evidence is big. The conclusion is one word. Only the conclusion mattered.**

---

## Demo 2 — A manager that delegates

**Tool used:** Messages API — one manager conversation plus 14 short ones

| | |
|---|---|
| **The problem** | Whole file bodies sit in the manager's context, to produce one word each. |
| **The concept** | A **subagent** is a separate conversation with its own context and tools. |
| **The purpose of this demo** | Show the manager's context stop growing with the job. |
| **How we solve it** | Each file goes to a throwaway conversation that returns one word. |

**What we will do:** run the same job with a manager that never reads a file.

**`core/subagents.py`** — starts a fresh conversation per file, with a system
prompt that allows exactly one word of output and a `max_tokens` of 8. It
validates the reply against the four allowed categories before returning it.

**`demos/p3_manager_subagents.py`** — lists the files, sends each one to that
subagent, and moves it based on the single word that comes back. The manager's
own context never holds a file body.

### Step 4 — Run the manager

```bash
python demos/p3_manager_subagents.py
```

### Step 5 — Read the three-line comparison in step 3

Flat agent, manager only, and manager plus every subagent added together.

### Step 6 — Read step 4 before drawing a conclusion

Total tokens across manager and subagents are not always lower.

### Step 7 — Note the two models in step 1

The manager runs on `claude-sonnet-5`. The subagent runs on
`claude-haiku-4-5-20251001`.

---

### In simple words — what demo 2 is teaching

The whole demo teaches **one sentence**: send back the answer, not the paperwork.

The manager does something different from demo 1 — **it never reads a file.**
For each file it opens a brand-new, throwaway conversation:

```
Subagent gets:  "Here are 198 characters. One word: which folder?"
Subagent says:  "finance"
Subagent is thrown away.
```

The file body lived and died inside that little conversation. The manager only
ever saw the word `finance`.

**Your numbers:**

| | Input tokens |
|---|---|
| Flat agent (one context) | **17,627** |
| Manager only | **86** |
| Manager + all 14 subagents | 2,062 |

The manager's own context is **86 tokens**. Roughly 200× smaller than the flat
run.

And here is the part that matters: that number **stays around 86** whether you
have 14 files or 1,400. The manager's context has stopped growing with the size
of the job. That is the thing you are actually buying.

**How many subagents?** Fourteen — one per file. In the code it is one function
called fourteen times in a loop, but each call starts a completely fresh
conversation with nothing carried over. Subagent 8 has no idea subagents 1 to 7
ever existed. Think of it as hiring fourteen temps, handing each one a single
sheet of paper, taking their one-word answer, and sending them home.

They run one at a time here because a `for` loop is easier to read. They *could*
run in parallel — that is a real benefit of the pattern.

---

## The exact difference between the two demos

Same job. Same fourteen files. Same result on disk. One thing changed: **who
reads the file.**

| | Demo 1 — flat agent | Demo 2 — manager + subagents |
|---|---|---|
| Who reads the file | the agent itself | a throwaway subagent |
| What enters the main context | the whole file body | one word |
| Conversations used | 1 | 15 (1 manager + 14 subagents) |
| Manager's input tokens | 17,627 | 86 |
| Grows as files increase? | **yes** | **no** |
| Model used | Sonnet for everything | Sonnet manager, Haiku subagents |
| Does the reader see other files? | yes, all of them | no, only its own |

That last row is the whole trade in one line.

### Pros and cons

**Demo 1 — one flat agent**

| Pros | Cons |
|---|---|
| Simple. One conversation, one prompt, easy to debug | Context grows with every file read |
| The agent sees everything, so it can spot patterns across files | You resend all of it on every turn |
| Fewer API calls | One expensive model does even the trivial work |
| Nothing to coordinate | Fine for 5 files, painful for 500 |

**Demo 2 — manager + subagents**

| Pros | Cons |
|---|---|
| Manager's context stays small no matter how big the job | More moving parts to build and debug |
| Cheap model for the narrow subtask | Each subagent resends its own system prompt, so total tokens may not drop |
| Subtasks can run in parallel | More API calls overall |
| Each subagent has a tight, focused tool set | **The subagent cannot see the bigger picture** |

### When to use which

- **Few items, and cross-file judgement matters** → flat agent. Simpler, and it can see connections.
- **Many items, each independently classifiable** → manager and subagents. The manager's context stops being the bottleneck.

---

## The price of isolation — look at this in your own output

Compare the two runs on one file:

| Run | `rent_receipt_july.txt` |
|---|---|
| Demo 1, flat agent | `finance` |
| Demo 2, subagent | `personal` |

They disagreed. Why?

The subagent saw **only 198 characters** — a receipt with a person's name on it.
It had no idea the other thirteen files were bills, tax forms and insurance
policies. The flat agent had all of that in its context, so it recognised this
as part of a finance pile.

**That is the cost of isolation.** You keep the bulk out of the manager's head,
and the specialist loses the surrounding picture.

Real systems handle this by giving subagents a small amount of shared context, or
by having the manager sanity-check the answers that come back. Decide which up
front.

Your exact result may differ — the model is making a judgement call, so it can
land either way. If both runs agree in your output, that is fine too. The point
stands either way: the subagent is deciding on less information.

---

## The two demos in one line

Demo 1: one agent carries everything it reads.
Demo 2: hand the reading out, keep only the answer.

---

## What to watch for

- The subagent sees roughly 200 characters. The flat agent held all fourteen
  file bodies at once.
- The manager's own input-token count is tiny and stays tiny. That is the
  property you are buying.
- If a manager's context grows with every subtask, the delegation is not doing
  its job — the subagent is returning transcripts instead of conclusions.
- Delegation is **not** automatically cheaper in total tokens. Step 4 of demo 2
  says so plainly, and it is worth saying out loud.
- This is the same problem Lab 5 attacks from the other end. Isolation prevents
  the growth; pruning cleans up after it.

---

*CCDV-F · Domain 1 · Lab 3 — ANKIT MISTRY*

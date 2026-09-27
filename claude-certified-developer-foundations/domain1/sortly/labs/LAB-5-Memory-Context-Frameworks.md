# LAB 5 — Memory, context and frameworks

**Tool used in this lab:** Messages API throughout, plus a small graph runner written in plain Python (demo 4). No extra packages needed

> **Before you start:** activate the environment you created in Lab 0.
> ```bash
> .venv\Scripts\activate
> ```
> On WSL, macOS or Linux: `source .venv/bin/activate`. Your prompt should show
> `(sortly)`.

Asha runs Sortly on Monday. On Tuesday she runs it again on a folder that looks
much the same. Should Tuesday cost as much as Monday did?

Two different things share the word "memory", and this lab separates them:
what survives *between* runs, and what should be thrown away *within* one.

## What this lab teaches

1. A model has no memory between runs — every run starts blank.
2. Memory between runs is a file you write and a snippet you re-inject.
3. Within a run the conversation only grows, and you resend all of it every turn.
4. Prune, compact, isolate — and isolation is the strongest because it prevents the growth.
5. Agentic frameworks restructure the loop; they do not add model capability.

---

## Demo 1 — Nothing persists

| | |
|---|---|
| **The problem** | Asha runs Sortly on Monday, then again on Tuesday. Should Tuesday cost the same? |
| **The concept** | A model has no memory between runs. Every run starts blank. |
| **The purpose of this demo** | Make the repeated work visible before fixing it. |
| **How we solve it** | We do not, yet. Run the same job twice and compare. |

**What we will do:** run the same sort twice and compare the two bills.

**`demos/p5_no_memory.py`** — classifies all fourteen files, resets, then does
it again from scratch. It prints the model-call count and token total for each
run so the repetition is visible.

### Step 1 — Run the no-memory demo

```bash
python demos/p5_no_memory.py
```

### Step 2 — Compare Monday and Tuesday in step 3

The two lines are identical. Tuesday re-derived every category Monday had
already worked out.

---

### In simple words — what demo 1 is teaching

**Problem:** Asha sorts her folder on Monday. On Tuesday she sorts it again.

**What happened:**

| | Monday | Tuesday |
|---|---|---|
| Files sorted | 14 | 14 |
| Model calls | 14 | **14** |
| Tokens | 1,976 | **1,976** |

Tuesday did the **exact same work again**. It learned nothing from Monday.

**Why?** Claude has no memory. Every run starts blank. Monday's answers had
nowhere to go.

**The bonus line:**

```
files where both runs agreed : 13/14
```

One file got a **different answer** on Tuesday. Same file, same model, minutes
apart. (It is usually `rent_receipt_july.txt` — a rent receipt with a person's
name on it genuinely reads as either `finance` or `personal`.)

So no memory costs you **twice**:

1. You pay again
2. You can contradict yourself

If your run says 14/14, run it a few more times — you will see it disagree.

**What "memory" does not mean.** It does not mean Claude remembers you. It means
*you* save the answer somewhere and put it back in the prompt next time. A JSON
file is enough.
---

## Demo 2 — A memory file

| | |
|---|---|
| **The problem** | Tuesday re-derives every answer Monday already worked out. |
| **The concept** | Memory is a file **you** write and a snippet **you** re-inject. |
| **The purpose of this demo** | Show a second run cost nothing. |
| **How we solve it** | A small JSON file holding conclusions, not file contents. |

**What we will do:** write conclusions to disk and read them back on the second run.

**`core/memory.py`** — holds two unrelated things: a small JSON store for state
that survives between runs, and a `prune_transcript` function for keeping a
single run's conversation from bloating.

**`demos/p5_with_memory.py`** — checks the memory file before asking the model,
and records each new answer. Monday populates it; Tuesday reads it.

### Step 3 — Run the memory demo

```bash
python demos/p5_with_memory.py
```

### Step 4 — Read the file stats in step 2

Around 1 KB for fourteen entries. It stores conclusions, not file contents.

### Step 5 — Compare Tuesday's line to Monday's

Model calls drop to zero.

### Step 6 — Read step 4

Memory locks in mistakes as reliably as it locks in successes. Nothing here
re-checks Monday's answers.

---

### In simple words — what demo 2 is teaching

**Problem:** stop paying twice.

**The fix:** before asking Claude, check a file.

```
Seen grocery_list.txt before?
  yes -> use the saved answer, ask nobody
  no  -> ask Claude, then save the answer
```

**What happened:**

| | Demo 1 (no memory) | Demo 2 (with memory) |
|---|---|---|
| Monday calls | 14 | 14 |
| **Tuesday calls** | **14** | **0** |
| Tuesday tokens | 1,976 | **0** |

Tuesday cost **nothing** — because Tuesday never talked to Claude at all. It
opened a JSON file, read `{'category': 'work'}`, and moved the file.

**Notice Monday still cost the full amount.** Memory does not help the first
time. Somebody has to do the work once.

**The file is tiny — 1,337 bytes for 14 files:**

```
Asha_Kulkarni_Resume.txt  ->  {'category': 'work'}
```

It saves the **answer**, not the file. Save the file contents instead and your
memory file becomes the next problem.

**The catch.** If Monday was wrong, Tuesday is wrong forever. Nothing re-checks.
Real systems add an expiry date, a confidence score, or a way for a human to fix
an entry. Decide that before you ship.
---

## Demo 3 — Pruning the conversation

| | |
|---|---|
| **The problem** | Memory fixed *between* runs. *Within* one run the conversation still only grows. |
| **The concept** | Old tool results are the biggest and least useful part of a transcript. |
| **The purpose of this demo** | Shrink the transcript without breaking it. |
| **How we solve it** | Cap old tool results at 60 characters, keep every block. |

**What we will do:** build a real transcript, find the bulk, and shrink it safely.

**`demos/p5_context_pruning.py`** — runs a genuine agent loop, prints the
transcript size every five turns, then prunes old tool results and re-measures.
It checks afterwards that the task and the newest turn are untouched, and
that every `tool_result` block survived.

### Step 7 — Run the pruning demo

```bash
python demos/p5_context_pruning.py
```

### Step 8 — Watch the transcript grow in step 1

A line prints after every turn, with the growth since the last one:

```
after turn 1   messages=3   transcript=  1180 chars  (~ 295 tokens)   +1180
after turn 2   messages=5   transcript=  7420 chars  (~1855 tokens)   +6240
```

The jump on the turn that reads the files is the whole point — Claude batches
its reads, so one turn can add several thousand characters at once.

### Step 9 — Find where the bulk is, in step 2

Tool results — the file bodies. Each mattered for exactly one decision and has
been resent ever since.

### Step 10 — Read the structural check in step 4

The demo prints `tool_result blocks kept : 29/29`. Every one survives; only the
*content* shrinks. Dropping one outright would leave a `tool_use` id unanswered
and the next request invalid.

Only the newest turn is protected from pruning. A larger protected window would
cover the very turn holding all the file contents — and prune nothing.

Expect roughly a 30% cut on this run. Fourteen files is small; the saving scales
with how much tool output sits behind you, and a long agent run is mostly tool
output.

### Step 11 — Read the three levers in step 5

Prune, compact, isolate. Isolation is Lab 3, which you have already seen work.

---

### In simple words — what demo 3 is teaching

**First, how this differs from demo 2.** These are two different problems and
they are easy to mix up.

| | Demo 2 (memory) | Demo 3 (pruning) |
|---|---|---|
| Fixes | **between** two runs | **inside** one run |
| Saves you from | doing the job twice | resending old text every turn |

Memory works **after** the job is done. Pruning works **during** the job.
While a conversation is still happening there is nothing saved yet — you are
creating the answers right now — so memory cannot help you.

**The situation.** Remember Lab 2? Every turn you send Claude the **whole
conversation again**. Claude has no memory, so you must resend everything.

**The problem.** The conversation keeps growing:

```
turn 1 ->    663 chars
turn 2 ->  2,437 chars
turn 3 ->  6,925 chars   <- Claude read the 14 files here
turn 4 -> 11,000 chars
```

Turn 4 sends **11,000 characters**. Turn 1 only sent 663.

**Why did it grow so much?** Because Claude read 14 files, and all that file
text now sits in the conversation.

But think about it. Claude read `grocery_list.txt` to decide one thing —
*"personal"*. Once that is decided, the grocery list text is **useless**. Yet
you keep sending it. Every turn. Forever.

**The fix.** Cut old file contents down to 60 characters:

```
BEFORE:  "toor dal 1kg / atta 5kg / poha 500g / mustard oil..."   (79 chars)
AFTER:   "toor dal 1kg / atta 5kg / poha..."                      (60 chars)
```

| | Chars | Tokens |
|---|---|---|
| Before | 11,000 | 2,750 |
| After | 8,824 | 2,206 |
| **Saved** | **2,176 (19%)** | on every later turn |

**The one rule you must not break.**

```
tool_result blocks kept : 29/29
```

You may **shrink** a result. You may **never remove** one.

Why? Every time Claude asks for a tool, that request carries an ID. Your answer
must carry the same ID. Remove an answer and Claude's request has no reply — the
API rejects your next call.

**Shorten the text. Keep the box it lives in.**

**Three ways to handle it:**

| Lever | What it does | Strength |
|---|---|---|
| prune | shorten old output | weakest |
| compact | summarise old turns | middle |
| isolate | never let it in (Lab 3 subagents) | **strongest** |

Isolation is strongest because it *prevents* the growth. Pruning only cleans up
after it.
---

## Demo 4 — The same agent as a framework would write it

| | |
|---|---|
| **The problem** | Real agents branch, retry and resume. A flat loop gets hard to read. |
| **The concept** | Frameworks impose structure on the loop — nodes, edges, typed steps. |
| **The purpose of this demo** | Show the model call is unchanged; only the writing-down changed. |
| **How we solve it** | A 20-line graph runner in plain Python. No extra packages. |

**What we will do:** redraw the Lab 3 job as named nodes and explicit edges.

**`demos/p5_framework_port.py`** — includes a twenty-line graph runner written
in plain Python and expresses the classify-and-file job as three nodes. It
needs no extra packages.

### Step 12 — Run the framework demo

```bash
python demos/p5_framework_port.py
```

### Step 13 — Read the node trace in step 2

Survey, then classify and file repeatedly. The model call at the centre is
exactly the one from Lab 3.

### Step 14 — Read what real frameworks add, in step 3

LangGraph brings checkpointed state graphs, PydanticAI brings typed validated
steps, Strands brings a declarative agent spec.

---

### In simple words — what demo 4 is teaching

**What it does.** It runs the **same job as Lab 3** — sort 14 files. Same
result. Same model call. The only difference is **how the code is organised**.

**Before: one loop.**

```python
for f in files:
    category = ask_claude(f)
    move_file(f, category)
```

**After: named steps.**

```
survey  ->  classify  ->  file  ->  (more files? back to classify)
                                 ->  END
```

Three steps with **names**, and arrows showing what follows what. That is it.
That is the entire demo.

**So why bother?** Because once your steps have names, tools can do useful
things with them:

| Framework | What it gives you |
|---|---|
| **LangGraph** | Crash at file 9? Restart from file 9, not file 1. |
| **PydanticAI** | Step returns garbage? It errors immediately instead of quietly passing junk along. |
| **Strands** | Describe the agent in config instead of code. |

None of this makes Claude smarter. It makes **your code** easier to debug and
restart.

**When NOT to use one.** A framework is an extra library between you and the
API. For a simple loop like Lab 3, it costs more than it gives. Reach for one
when your flow has many steps, branches, retries, or needs to resume after a
crash.

**One honest note.** The graph runner in this demo is twenty lines of plain
Python written to show the shape. Those three frameworks are third-party
projects on their own release cycles — learn the pattern here, then read each
project's current docs before writing against its API.
---

## The four demos in one line

| Demo | Question | Answer |
|---|---|---|
| 1 | Does Claude remember? | No. Every run starts blank. |
| 2 | How do I fix that? | Save the answer to a file. |
| 3 | What about *inside* one run? | Shorten old tool output. |
| 4 | What do frameworks give me? | Structure, not intelligence. |

**Between runs = memory. Within a run = pruning.** That distinction is the exam
question.

---

## What to watch for

- "Memory" in Domain 1 means persistence you build, not a model feature.
- Context-window management is *within* a run. Memory is *across* runs. Exam
  questions often turn on which one a scenario needs.
- The graph runner in demo 4 is teaching code. Read each framework's own docs
  before writing against its API — they are third-party projects with their own
  release cycles.

---

*CCDV-F · Domain 1 · Lab 5 — ANKIT MISTRY*

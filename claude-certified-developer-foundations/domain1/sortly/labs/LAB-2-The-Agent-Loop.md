# LAB 2 — The agent loop

**Tool used in this lab:** Messages API (demo 1) + Claude Agent SDK (demo 2) + no tool at all (demo 3)

> **Before you start:** activate the environment you created in Lab 0.
> ```bash
> .venv\Scripts\activate
> ```
> On WSL, macOS or Linux: `source .venv/bin/activate`. Your prompt should show
> `(sortly)`.

In Lab 1 the agent looked like magic: you gave it a sentence and files moved.
This lab removes the magic. An agent is a while-loop, and by the end of demo 1
you will have watched every iteration of it.

## What this lab teaches

1. Claude cannot open, move or delete anything. It can only **ask**. Your code does the work.
2. The agent loop is: send the conversation, check `stop_reason`, run the tool, append the result, repeat.
3. The conversation grows by two messages a turn, and you resend all of it every time.
4. The Claude Agent SDK writes that same loop for you, and throws in caching, retries and cost tracking.
5. Where the loop runs — your machine or Anthropic's servers — is a separate decision.

---

## Demo 1 — The loop, written out

**Tool used:** Messages API

| | |
|---|---|
| **The problem** | In Lab 1 the agent looked like magic. Magic is not teachable. |
| **The concept** | An agent is a `while` loop around an ordinary API call. |
| **The purpose of this demo** | Remove the magic by showing every iteration. |
| **How we solve it** | The loop is written inline in the demo file, not imported. |

**What we will do:** run an agent whose loop is visible in the demo file itself.

**`demos/p2_loop_by_hand.py`** — contains the whole loop inline rather than
importing it, and prints `stop_reason` plus the message count after every turn.
It uses only three tools so the trace stays short enough to read.

### Step 1 — Run the hand-written loop

```bash
python demos/p2_loop_by_hand.py
```

### Step 2 — Read the six-line sketch in step 1

That is the complete idea. Everything after this lab is a variation on it.

### Step 3 — Follow the `messages in conversation` counter

It goes 3, 5, 7. Two messages per turn.

### Step 4 — Read the four requirements in step 3

A stopping condition, a turn limit, results in the same order as the requests,
and one `tool_result` for every `tool_use`.

---

### In simple words — what demo 1 is teaching

The whole demo teaches **one sentence**: an agent is just a loop you write
yourself.

**The key idea.** Claude *cannot* open a file, move a file, or do anything on
your computer. All it can do is **ask**. So the demo does this, over and over:

1. You send Claude the conversation
2. Claude replies: *"call `read_file_head` on grocery_list.txt"*
3. **Your Python code** actually opens the file
4. You send the result back
5. Repeat

When Claude stops asking, the loop ends.

**Reading your output.**

| Turn | Claude asked for | Your code did |
|---|---|---|
| 1 | the file list | listed 14 files |
| 2 | read 14 files | read them |
| 3 | move 3 files | moved them |
| 4 | *nothing* | stopped |

The word `stop_reason` is the switch:

- `tool_use` = Claude is still asking → keep looping
- `end_turn` = Claude is done → exit

That is it. That is the entire loop.

**The one number to point at.**

```
messages in conversation: 3 -> 5 -> 7
```

It is just a Python list getting longer. Every turn adds **2 items**.

*Before the loop starts — 1 item:*

```
1. You:    "Sort the three smallest files"
```

*After turn 1 — 3 items:*

```
1. You:    "Sort the three smallest files"
2. Claude: "call list_files"          <- added
3. You:    "here are the 14 files"    <- added
```

*After turn 2 — 5 items:*

```
1. You:    "Sort the three smallest files"
2. Claude: "call list_files"
3. You:    "here are the 14 files"
4. Claude: "read all 14 files"        <- added
5. You:    "here is what they say"    <- added
```

*After turn 3 — 7 items.* Same pattern.

So: **1 → 3 → 5 → 7**. Claude asks (1 item), you answer (1 item). Two per turn,
every turn.

**Why anyone should care.** Claude has no memory. On **every** API call you must
resend the **entire list** from item 1.

- Turn 1 sends 1 item
- Turn 2 sends 3 items
- Turn 3 sends 5 items
- Turn 4 sends 7 items

You keep paying for the old stuff again and again. A 50-turn agent resends turn
1 fifty times. **That is the cost problem Lab 5 solves.** This demo just makes
you watch it start.

**Your turn count will differ from the recording, and that is correct.** One run
may read all fourteen files in a single turn; the next may read six, then the
rest. Same prompt, different path. That is non-determinism, happening in front
of you.

---

## Demo 2 — The same agent on the Claude Agent SDK

**Tool used:** Claude Agent SDK

| | |
|---|---|
| **The problem** | Nobody wants to hand-write that loop, its retries and its bookkeeping every time. |
| **The concept** | The Claude Agent SDK is a **harness** — it owns the loop, you own the tools. |
| **The purpose of this demo** | Prove the tools do not change when the harness does. |
| **How we solve it** | Same functions, declared with `@tool`, handed to `query()`. |

**What we will do:** run the identical job with no loop of our own.

**`demos/p2_loop_with_sdk.py`** — declares the same tools with the `@tool`
decorator, bundles them into an in-process MCP server, and hands everything to
`query()`. There is no while-loop and no `stop_reason` check anywhere in it.

### Step 5 — Confirm the SDK is there

```bash
python -c "import claude_agent_sdk; print('sdk ready')"
```

You installed it in Lab 0, so this should just print. If it does not, either the
environment is not activated, or run `uv pip install claude-agent-sdk`.

The package bundles the Claude Code CLI, which is a Node program, so Node must
be on the machine. Check with `node --version`.

### Step 6 — Run the SDK version

```bash
python demos/p2_loop_with_sdk.py
```

### Step 7 — Compare the two columns in step 1

Dict schema becomes a decorator, your loop becomes an async iterator.

### Step 8 — Read the two options called out in step 3

`setting_sources=[]` stops the run reading `CLAUDE.md` and `settings.json` from
disk. `allowed_tools` is an approval list, not a restriction list.

---

### In simple words — what demo 2 is teaching

The whole demo teaches **one sentence**: the SDK writes that loop for you.

**What changed from demo 1.** In demo 1 *you* wrote this:

```
loop:
    ask Claude
    check stop_reason
    run the tool
    add the result to the list
    repeat
```

In demo 2, **none of that is in the file.** No `while`. No `stop_reason`. You
just say: *"Here are my tools. Here's the job. Go."* The SDK does the looping.

**What did NOT change.** Open `core/sdk_tools.py`. The five tool functions are
**imported unchanged** from `core/tools.py` — the same file demo 1 used. Only
the wrapper changed:

| Demo 1 | Demo 2 |
|---|---|
| a dict with `input_schema` | `@tool` decorator |
| you write the loop | `query()` runs it |

Same tools, different driver.

**Reading your output.** The tool calls look exactly like demo 1 — `list_files`,
some reads, then the moves. That is the point: same behaviour.

But look at the last two lines. **You never wrote code to produce these:**

```
turns      : 20
cost (est) : $0.12
```

In demo 1 you counted tokens yourself. Here the SDK just hands you the number.

And in the usage blob:

```
cache_read_input_tokens: 99,632
```

Remember demo 1's problem — the message list grows, and you resend everything
every turn? **The SDK cached it automatically.** Those tokens were re-read from
cache at a fraction of the price. You wrote zero lines to make that happen.

**Two oddities you will see.**

- `-> ToolSearch` — not one of our five tools. It is a built-in the SDK brought
  along. A useful accident: it proves `allowed_tools` **approves** tools, it
  does not **ban** the others.
- `thinking_tokens: 1094` — the model reasoned before acting. Also free, also
  not your code.

**The one-line lesson.** Demo 1: here is the loop, nothing hidden. Demo 2: never
write it again — plus caching, retries and cost tracking thrown in.

---

## Demo 3 — Where the agent runs

**Tool used:** none. This demo makes no API call and costs nothing.

| | |
|---|---|
| **The problem** | Demos 1 and 2 both ran on your laptop. Real agents may need to run elsewhere. |
| **The concept** | Building the agent and deploying it are separate decisions. |
| **The purpose of this demo** | Match a constraint to a deployment model. |
| **How we solve it** | Plain Python. A comparison table and four cases. Nothing runs. |

**What we will do:** separate building the agent from deploying it.

**`demos/p2_deployment_models.py`** — compares the Agent SDK against Claude
Managed Agents across eight rows, then works through four deployment cases.

### Step 9 — Run the deployment demo

```bash
python demos/p2_deployment_models.py
```

### Step 10 — Find the row about conversation state

Self-hosted means you keep it. Managed means it is persisted server-side and
sessions resume.

### Step 11 — Answer the four cases in step 2

Each names one constraint: local files, hours of runtime, a compliance rule,
per-tenant isolation.

---

### In simple words — what demo 3 is teaching

The whole demo teaches **one sentence**: your laptop is not the only place an
agent can run.

**First, know this.** *Nothing ran here.* No agent, no API call, no tokens, no
cost. It only printed a table. That is on purpose — this demo is a **decision**,
not a program.

**The question it answers.** Demos 1 and 2 both ran the agent **on your
machine**. The `while` loop was your Python. The files were on your `C:` drive.
Demo 3 asks: does it have to be?

| | Runs where |
|---|---|
| **Agent SDK** (demos 1 and 2) | your computer |
| **Claude Managed Agents** | Anthropic's servers |

**Reading your table.** Every row is the same question asked differently: *who
does this work — you, or Anthropic?*

The row that actually decides real projects is this one:

```
Conversation state    you keep it    persisted server-side, resumable
```

Remember demo 1's growing message list? **You** were holding it. Close the
program and it is gone. With Managed Agents, Anthropic stores it. The agent can
stop, and start again tomorrow from where it was.

**The four cases.** Each names **one constraint**, and that constraint decides:

| Constraint | Answer |
|---|---|
| Files are already on the laptop | your machine |
| Runs 4 hours, unattended, nightly | Anthropic's servers |
| Hospital data, legal rules | your machine |
| Many customers, isolated from each other | Anthropic's servers |

Notice the pattern: **long-running or stateful** → hosted. **Local files or
compliance rules** → your machine.

**The mistake step 3 warns about.** Managed Agents is **not** "the advanced
version" of the SDK. It is a different product with a different API. You do not
`import` anything — you call a REST endpoint. Think phone versus email, not
beginner versus expert.

---

## The three demos in one line

Demo 1: build the loop.
Demo 2: let the SDK build it.
Demo 3: decide where it lives.

---

## What to watch for

- The message list is the agent's entire memory *within* a run. Lab 5 is about
  what to do when it gets too big.
- `core/sdk_tools.py` imports its function bodies unchanged from
  `core/tools.py`. Switching harness did not mean rewriting tools.
- Managed Agents is not a tier above the SDK. It is a different product with a
  different API, currently in beta behind a beta header.
- Demo 3 costs nothing and prints identically every time. Demos 1 and 2 cost
  real tokens and take a different path on every run.

---

*CCDV-F · Domain 1 · Lab 2 — ANKIT MISTRY*

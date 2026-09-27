# LAB 0 — Project overview and setup

**Tool used in this lab:** Messages API — one small call, only to prove the key works

---

## What Sortly is

Asha Kulkarni is a backend developer in Kothrud, Pune. Her downloads folder has
fourteen loose files in it: two electricity bills, a rent receipt, a Form 16, an
SIP statement, sprint notes, a grocery list, a wedding invite, a file called
`untitled_1.txt`, and two copies of her resume that are not quite the same.

Sortly tidies that folder.

Across six labs you tidy it six different ways, and each way teaches one thing
the **CCDV-F Domain 1 (Agents and Workflows)** exam asks about. Domain 1 is
14.7% of the exam.

By the end you will have written an agent loop by hand, run the same agent on
the Claude Agent SDK, delegated work to subagents, blocked a destructive action
with a hook, and given the agent a memory.

## The journey

| Lab | The one big idea | Tool used | Demos |
|---|---|---|---|
| **0** | Get the environment working and meet the folder | Messages API | 3 |
| **1** | A workflow decides nothing at runtime; an agent decides everything | plain Python, then Messages API | 3 |
| **2** | An agent loop is a while-loop, and the SDK writes it for you | Messages API, then Agent SDK | 3 |
| **3** | Send the conclusion back, not the evidence | Messages API | 2 |
| **4** | A prompt persuades; a hook enforces | Messages API, then Agent SDK hooks | 3 |
| **5** | What survives between runs, and what should not survive within one | Messages API + plain Python | 4 |

**18 demos in total.**

## Folder structure

```
sortly/
├── pyproject.toml                project definition
├── .env.example                  copy to .env, add your key
├── .gitignore
│
├── check_setup.py                run this first
├── reset_workspace.py            restore the messy folder
│
├── workspace_seed/               14 real files, never modified
│   ├── Asha_Kulkarni_Resume.txt
│   ├── Asha_Kulkarni_Resume (2).txt      <- not a duplicate. Lab 4 turns on this
│   ├── electricity_bill_july.txt
│   ├── electricity_bill_august.txt
│   ├── rent_receipt_july.txt
│   ├── form16_fy2025_26.txt
│   ├── sip_statement_q2.txt
│   ├── insurance_policy_health.txt
│   ├── meeting_notes_ruteway_sprint12.txt
│   ├── screenshot_error_2026_08_11.txt   <- no keyword in the name. Lab 1
│   ├── untitled_1.txt                    <- no keyword in the name. Lab 1
│   ├── grocery_list.txt
│   ├── trek_photos_note.txt
│   └── wedding_invite_shreya.txt
│
├── workspace/                    created at runtime, freely destroyed
│
├── core/                         the building blocks, added lab by lab
│   ├── banner.py       (Lab 0)   the concept / step / takeaway cards
│   ├── _shared.py      (Lab 0)   pinned model IDs, client, .env loader, paths
│   ├── tools.py        (Lab 0)   five tools, JSON schemas, the path jail
│   ├── agent.py        (Lab 2)   the hand-written agent loop
│   ├── sdk_tools.py    (Lab 2)   the same tools, for the Claude Agent SDK
│   ├── subagents.py    (Lab 3)   the classifier subagent
│   ├── hooks.py        (Lab 4)   one guard, written for both harnesses
│   └── memory.py       (Lab 5)   persistence + transcript pruning
│
├── demos/                        15 scripts, prefixed by lab
│   ├── p1_pipeline_rigid.py          p3_manager_flat.py
│   ├── p1_pipeline_with_model.py     p3_manager_subagents.py
│   ├── p1_choose_the_shape.py        p4_delete_prompt_only.py
│   ├── p2_loop_by_hand.py            p4_delete_hook_blocked.py
│   ├── p2_loop_with_sdk.py           p4_delete_hook_sdk.py
│   ├── p2_deployment_models.py       p5_no_memory.py
│   ├── p5_with_memory.py             p5_context_pruning.py
│   └── p5_framework_port.py
│
└── labs/                         these six files
```

Files in `core/` are added lab by lab and never edited afterwards. A file you
read in Lab 2 still says exactly what it said in Lab 2.

## The five tools

Every agent in this course gets the same five tools. They are ordinary Python
functions in `core/tools.py`:

| Tool | What it does |
|---|---|
| `list_files` | list the loose, unsorted files |
| `read_file_head` | read the first few lines of one file |
| `move_file` | move a file into finance, work, personal or misc |
| `rename_file` | give a file a clearer name |
| `delete_file` | permanently delete a file — Lab 4 is about this one |

## What every demo prints

```
==========================================================
  SORTLY  |  P4 / demo 2  |  A hook makes the rule enforceable
==========================================================
  THE IDEA          one paragraph, before anything runs
  EXAM OBJECTIVE    which Domain 1 skill this maps to
  WATCH FOR         what to look at in the output
==========================================================

[step 1] ...        numbered narration while it runs

==========================================================
  TAKEAWAY          three points
  EXAM ANGLE        how this gets tested
==========================================================
```

You never have to guess why a demo exists.

---

## What this lab teaches

1. Sortly runs in a virtual environment you create once and activate for every lab.
2. The API key lives in `.env` and never in code.
3. Nothing reads `.env` for you — `core/_shared.py` loads it at import.
4. Model IDs are pinned exactly, and they appear in one file only.
5. `workspace_seed/` is the pristine copy; `workspace/` is the folder you destroy.

## Before you start

| Need | Why |
|---|---|
| Python 3.10 or newer | The Claude Agent SDK requires it |
| `uv` | This project uses `uv` throughout |
| An Anthropic API key | Required. Every lab from Lab 1 onward makes real API calls |
| **Node.js** | For the Agent SDK in Labs 2 and 4. Check with `node --version` |

The Node requirement catches people out. The Agent SDK installs cleanly without
it, then fails at run time with a spawn error that never mentions Node.

**There is no offline or simulated mode.** Every demo that talks to a model
talks to a real one. Running the whole course once costs a few rupees.

---

## Demo 1 — Create the environment, once

| | |
|---|---|
| **The problem** | Installing packages globally breaks other projects on the same machine. |
| **The concept** | A virtual environment is a private Python folder that belongs to this project only. |
| **The purpose of this demo** | Build it once here, so every later lab is a one-line activate. |
| **How we solve it** | `uv venv` creates it, then `uv pip install` fills it. |

**What we will do:** create `.venv`, activate it, and install both packages.

### Step 1 — Move into the project

```bash
cd sortly
```

### Step 2 — Create the virtual environment

```bash
uv venv
```

This creates a `.venv` folder inside the project. Nothing is installed yet.

### Step 3 — Activate it

```bash
.venv\Scripts\activate
```

On WSL, macOS or Linux use `source .venv/bin/activate`.

Your prompt changes to show `(sortly)` at the front. That prefix means the
environment is active — you will look for it at the start of every later lab.

### Step 4 — Install both packages

```bash
uv pip install anthropic claude-agent-sdk
```

`anthropic` is the Messages API client, used from Lab 1 onward.
`claude-agent-sdk` is needed in Labs 2 and 4, and it bundles the Claude Code CLI.

Installing both now means **no later lab stops for a download.**

### Step 5 — Confirm the environment is active

```bash
python -c "import anthropic, claude_agent_sdk; print('both installed')"
```

If this fails with `ModuleNotFoundError`, the environment is not activated. Go
back to step 3.

---

## Demo 2 — Add your key, and learn to read the check

| | |
|---|---|
| **The problem** | Nothing works without an API key, and a key in your code ends up in your repository. |
| **The concept** | The key lives in `.env`, which `.gitignore` excludes. |
| **The purpose of this demo** | Get the key loading, and learn to diagnose it when it does not. |
| **How we solve it** | `core/_shared.py` reads `.env` at import and `check_setup.py` reports what it found. |

**What we will do:** create `.env`, paste the key, and run the setup check.

### Step 6 — Create your `.env`

```bash
copy .env.example .env
```

On WSL, macOS or Linux use `cp .env.example .env`.

### Step 7 — Paste your key into `.env`

Get one from https://platform.claude.com/settings/keys. The line must read
exactly:

```
ANTHROPIC_API_KEY=sk-ant-...
```

No `export`, no spaces around the `=`, no quotes.

**`check_setup.py`** — checks the Python version, counts the seed files, prints
the pinned model IDs, confirms the key loaded, then makes one small call. It is
the only script in the project that is not teaching a concept.

### Step 8 — Run the check

```bash
python check_setup.py
```

Five steps should print, ending with `Setup complete.`

### Step 9 — Read the two lines step 4 prints

```
.env path : ...\sortly\.env
.env file : read
ANTHROPIC_API_KEY: found (sk-ant-...4f2a, 108 chars)
```

The first line is exactly where the code looked. The second says whether it
found anything. The third is the key, masked.

**Nothing else in this course works until you see that third line.**

### Step 10 — Know the three usual causes of `MISSING`

- Windows saved the file as `.env.txt` with the extension hidden
- The line has `export` in front, or spaces around the `=`, or quotes
- The file is not beside `pyproject.toml`

---

## Demo 3 — Meet the messy folder

| | |
|---|---|
| **The problem** | The demos really move and delete files. You need to get back to a known state. |
| **The concept** | `workspace_seed/` is pristine and never touched; `workspace/` is the copy that gets destroyed. |
| **The purpose of this demo** | Build the folder, and know how to restore it. |
| **How we solve it** | `reset_workspace.py` copies the seed over the workspace. |

**What we will do:** create the folder the rest of the course works on.

**`reset_workspace.py`** — copies `workspace_seed/` over `workspace/`, wiping
whatever was there.

### Step 11 — Build the workspace

```bash
python reset_workspace.py
```

### Step 12 — Look at what Asha has

```bash
dir workspace
```

Fourteen files. Note the two named `Asha_Kulkarni_Resume` — one has a `(2)` in
the name. They are **not** identical, and Lab 4 turns on that fact.

### Step 13 — Know when you actually need to reset

You do **not** need to run this before each demo. Every demo rebuilds
`workspace/` from the seed as its first action, so a missing `workspace/` folder
is completely normal.

Run `reset_workspace.py` when you interrupt a demo part-way and want a clean
folder to inspect by hand.

---

## The three demos in one line

Demo 1: build the environment once, activate it for every lab.
Demo 2: get the key loading, and learn to read step 4 when it does not.
Demo 3: build the messy folder everything else runs on.

---

## What to watch for

- Every later lab starts with **one command**: activate the environment. If
  `(sortly)` is not in your prompt, activate before running anything.
- `uv venv` and `uv pip install` replace `pip install`. There is no plain `pip`
  anywhere in this project.
- Your key is in `.env`, which `.gitignore` already excludes. It is never in
  code, never in a demo, never in the repository.
- `check_setup.py` prints `claude-sonnet-5` and `claude-haiku-4-5-20251001`.
  Both are pinned. The second carries its date because pre-4.6 dateless IDs are
  aliases that move.
- Every demo from Lab 1 onward makes real API calls and costs real tokens. The
  amounts are small, but they are real.

---

*CCDV-F · Domain 1 · Lab 0 — ANKIT MISTRY*

# LAB 1 — Workflow or agent?

**Tool used in this lab:** plain Python, no model (demo 1) + Messages API (demo 2) + no tool at all (demo 3)

> **Before you start:** activate the environment you created in Lab 0.
> ```bash
> .venv\Scripts\activate
> ```
> On WSL, macOS or Linux: `source .venv/bin/activate`. Your prompt should show
> `(sortly)`.

Asha's folder has fourteen files. Twelve of them have obvious names:
`electricity_bill_july.txt`, `rent_receipt_july.txt`, `grocery_list.txt`. Two
do not: `untitled_1.txt` and `screenshot_error_2026_08_11.txt`.

That gap between twelve and two is the entire lesson of this lab.

## What this lab teaches

1. A workflow runs fixed steps in a fixed order and decides nothing at runtime.
2. An agent is given a goal and tools and chooses its own next step.
3. A workflow fails silently on inputs nobody anticipated — it has no branch.
4. An agent handles those inputs, and charges you tokens, latency and variability for it.
5. The choice is decided by whether the steps can be known in advance, not by which is more advanced.

---

## Demo 1 — The rigid pipeline

| | |
|---|---|
| **The problem** | Asha's folder is a mess and somebody has to sort it. |
| **The obvious fix** | Write rules. If the filename says "bill", it is finance. |
| **The purpose of this demo** | Show how far rules get you, and exactly where they stop. |
| **How we solve it** | Plain Python. Keyword matching on filenames, no model, no cost. |

**What we will do:** sort the folder with hand-written rules and count what is left over.

**`demos/p1_pipeline_rigid.py`** — matches keywords against filenames and moves
each file into a category folder. It never opens a file, so anything without a
recognised keyword comes back as `UNKNOWN`.

### Step 1 — Run the rigid pipeline

```bash
python demos/p1_pipeline_rigid.py
```

### Step 2 — Read the score in step 2 of the output

Twelve sorted, two unknown, zero API calls, zero cost.

### Step 3 — Read the two unknown files in step 3

Their first lines are printed. You can tell what they are in a second; the
rules cannot, because nobody wrote a rule for them.

---

## Demo 2 — The same job, given to an agent

| | |
|---|---|
| **The problem** | Two files have names that tell you nothing. Rules cannot place them. |
| **The concept** | An agent is given a goal and tools, and picks its own next step. |
| **The purpose of this demo** | Watch it handle the exact files demo 1 could not. |
| **How we solve it** | Describe the goal, not the procedure, and let the loop run. |

**What we will do:** hand the goal and the tools to the model and watch it decide.

**`demos/p1_pipeline_with_model.py`** — gives Claude the five Sortly tools and
one sentence of intent, then runs a loop until Claude stops asking for tools.
Nothing in the file says which file goes where.

### Step 4 — Run the agent

```bash
python demos/p1_pipeline_with_model.py
```

### Step 5 — Find `untitled_1.txt` in the trace

You should see a `read_file_head` line for it, followed by a `move_file` line.
That read is the decision the pipeline could not make.

### Step 6 — Read the score in step 3

Compare turns and tokens against demo 1's zero API calls and zero cost. Both
numbers are real. Neither approach is free.

---

## Demo 3 — Making the choice deliberately

### Why this demo exists

Demos 1 and 2 gave you the two shapes, using **one** folder. But the exam will
never ask about Asha's folder. It will describe a task you have never seen and
ask which shape fits.

So this demo turns what you just watched into a **rule you can carry to any
task**. That is the last step of learning something: not "I saw it happen", but
"I can decide about a new case."

### What it does and does not do

**This demo runs nothing.** No agent, no API call, no file is moved, no tokens
are spent. It only prints two things:

1. Six yes/no questions. Each answer points at *workflow* or *agent*.
2. Six ordinary work tasks, with the right answer and the reason for it.

If it feels less exciting than demo 2, that is expected. Demo 2 was the
experience; this is the takeaway, written down so it survives.

| | |
|---|---|
| **The problem** | You now know both shapes — but the exam describes a task you have never seen. |
| **The concept** | Six yes/no questions that decide workflow versus agent. |
| **The purpose of this demo** | Turn the experience into a rule you can carry anywhere. |
| **How we solve it** | Plain Python. It prints the rule and six worked cases. Nothing runs. |

**What we will do:** read the rule, then test ourselves on six tasks.

**`demos/p1_choose_the_shape.py`** — prints the decision criteria as a table and
then applies them to six realistic tasks. It is plain Python with no model call,
so it costs nothing and prints the same thing every time.

### Step 7 — Run the decision demo

```bash
python demos/p1_choose_the_shape.py
```

### Step 8 — Read the six questions in step 1

Each one is a yes/no question about the task in front of you. Answer yes to the
first four and you have a workflow. Answer yes to the last two and you have an
agent.

### Step 9 — Test yourself on the six cases in step 2

Each case prints three lines:

```
  Resize every image in a folder to 800px wide         <- the task
      -> WORKFLOW                                      <- the answer
         Pure deterministic transformation.            <- the reason
```

Read the **first** line, decide for yourself, then read the two lines below it
to check. Going straight down the screen teaches you nothing — the value is in
deciding first and being wrong sometimes.

### Step 10 — Look closely at two of the six

- **"Resize every image to 800px wide"** — a lot of people say *agent* here,
  because they have just seen an agent do something clever. It is a workflow.
  There is no judgement in resizing an image.
- **"Read an incoming complaint and route it to the right team"** — some people
  say *workflow*, because demo 1 made workflows look cheap and safe. It is an
  agent. You cannot write the routing rules in advance for text you have not
  read.

Those two cases are the whole point of this demo. They catch the two ways
people get this wrong.

---

## The three demos in one line

Demo 1: rules are free and fast, and blind to what nobody anticipated.
Demo 2: an agent handles the leftovers, and charges you for all fourteen files.
Demo 3: how to choose, for a task you have never seen.

---

## What to watch for

- Twelve of fourteen files sorted for free is a **good** result. The workflow
  is not the villain of this lab.
- The agent's advantage shows up on exactly two files, and costs real tokens on
  all fourteen.
- Demo 3 costs nothing to run and prints identically every time. If it looks
  the same on your machine as on the recording, that is correct.
- Step 3 of the third demo names the trap: wrapping a fixed three-step job in
  an agent loop buys non-determinism and cost, and buys the user nothing.
- Many real systems are a workflow with one agent step inside, not one or the
  other.

---

*CCDV-F · Domain 1 · Lab 1 — ANKIT MISTRY*

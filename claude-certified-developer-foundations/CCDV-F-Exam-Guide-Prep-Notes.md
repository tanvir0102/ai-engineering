Domain 1: Agents and Workflow
## Workflow or Agents
1. What is a Workflow?
You write the steps. Claude fills in the blanks.
Example: Railway ticket counter
Step 1 -> Step 2 -> Step 3 -> Step 4

2. Four Workflow patterns
Chaining
Routing
Parallel
Orchestrator

3. What is an agent?
Claude picks the steps and You give the goal.

4. The real difference between Workflow and Agent
Who decides the next step - you, or the model?
Developer: decides the steps, You can draw the flowchart before it runs.
Claude: decides the steps, You cannot draw the flowchart in advance.

5. How to choose
Can you draw the flowchart? Use a workflow.
Workflow : you decide the steps
Agent : Claude decides at the runtime
When both fit, choose workflow

Exam rule: 
when both could work, choose the workflow

## Inside the Agent Loop
1. An agent is a loop
What actually happens inside an Agent (An agent is a loop, not a magic box)
1. Chaude thinks -> 2. Calls a tool -> 3. Result returns -> 4. Loop repeats
- repeat until a stop condition is met

1. Claude thinks:
The goal: what you asked for
The tools: what it is allowed to use
The history: Everything so far
It reasons about ONE thing only - the immediate next action. Not the whole plan. Just the next move.

2. Claude Calls a tool
CLAUDE: call this tool with these inputs
The GAP: Your code decides whether to run it
THE TOOL: Run only if your code allows it
Claude never runs anything itself. That gap is where approvals and safety checks live.

3. Result returns and 4. Loop repeats
The result is appended to the history

2. Think, call tool, observe, repeat
3. The request-execute gap
4. The stopping problem
- Loops must be told when to stop: A loop with no exit runs and bills forever

5. Three loop shapes

## Context and Memory

## Managers, Workers, Subagents
1. The manager patten
2. What a subagent is
3. Why subagents improve results
4. Single agent vs manager
5. When to add a manager

## Building Agents with Claude
1. The Claude Agent SDK
2. Writing the loop yourself
3. Where your agents runs
4. Hooks for safety
5. Choosing your build path

## Agentic Frameworks
1. Why frameworks exist
2. Strands, LangGraph, PydanticAl
3. The Full Spectrum
4. How to choose

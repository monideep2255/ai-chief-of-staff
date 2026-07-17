---
name: parallel-first
description: Before starting any multi-part task, check if subtasks are independent and can run in parallel - using parallel tool calls or parallel subagents
scope: portable
depends_on:
  - .claude/rules/self-eval-loop.md
  - .claude/rules/goal-contracts.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - .claude/rules/self-eval-loop.md
  - .claude/rules/goal-contracts.md
---

## Parallel-first execution

Before starting any task with 2+ parts, ask: can these run in parallel?

**The check (takes 5 seconds):**

1. Do any subtasks depend on the output of another? If yes, those must be sequential.
2. Do any subtasks share write targets (same file)? If yes, those must be sequential.
3. Everything else: run in parallel.

**When to use parallel tool calls vs. parallel subagents:**

- Parallel tool calls: reading multiple files, running multiple bash commands, independent searches. Use when each subtask is a single tool call.
- Parallel subagents (Agent tool): when each subtask needs multiple steps, reads files, and produces output independently. Use when the work is non-trivial and self-contained.

**Examples:**

- User gives 3 tasks → check dependencies first → dispatch independent ones as parallel agents
- Deep dive + meeting prep → independent → run as parallel agents
- Repo clone (step 1) + deep dive analysis (step 2) → step 2 depends on step 1 → sequential
- Reading 5 files for context → no dependency between reads → parallel tool calls in one message

**Context isolation for subagents:**

When dispatching parallel subagents, each agent should start with a clean context window. Pre-inject only what that specific agent needs (task description, file paths, constraints). Do not pass accumulated conversation history or prior agent results into new agent prompts. The agent that reads its own files fresh produces better output than one that inherits stale summaries.

When the input itself is large (long logs, a big result set, a folder of documents), do not stuff it into one prompt. Give the agent tools to treat context as external state it navigates on demand: grep to locate, read a slice, partition the work, recurse if needed. A subagent handed a pointer plus the means to query beats one handed a giant pre-loaded blob. This matters most for long-running research and search agents whose result sets grow fast.

**Verify the dispatch completed (before you declare done):**

Dispatched agents fail quietly. An agent stops after writing the first of two files, a workflow returns 0 agents from a bad argument, a run truncates an artifact mid-way. The loop reports success anyway, because nothing checked. Close that gap:

1. Before dispatch, enumerate the expected outputs: the exact files (or fields) each agent must produce. A fan-out of N agents has a known list of N artifacts, name it up front.
2. After the agents return, verify each expected output exists and is non-empty. A file that should have several sections but holds only a header counts as missing, not done.
3. Re-dispatch any agent whose output is missing or truncated, then re-verify. Declare the dispatch done only when every expected output passes.

This is a completeness check (did all the artifacts get produced?), not a quality check (are they good?). Quality grading is the separate produce-then-grade pass owned by `self-eval-loop.md`. Run both, existence first, then grade what exists. The enumerated expected-output list is the verify surface `goal-contracts.md` requires, applied to a fan-out instead of a single run.

**Do NOT apply when:**
- Task has clear sequential dependencies (step B requires output of step A)
- There is only one task
- The dispatch produces no discrete artifact to check (a pure lookup or summary returned inline) - there is nothing to enumerate

**Why:** Sequential execution on independent tasks is wasted time. The cost of checking for parallelism is always lower than the cost of waiting.

**Cross-agent review pattern:**

When one agent writes substantial output, dispatching a second fresh-context agent to grade it is the produce-then-grade pattern. That pattern is owned by `self-eval-loop.md` (when to apply, context isolation, three-state permissions). Use it there. Parallel-first's only addition: the grading agent is independent work, so it can be dispatched in parallel with other review dimensions.

The test: are any of my sequential tool calls actually independent, and when I dispatched agents to produce artifacts, did I verify every expected output exists and is non-empty before declaring the dispatch done?

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
  - .claude/rules/plan-then-fan-out.md
  - .claude/skills/bossman-mode/SKILL.md
  - .claude/skills/ingest-workflows/SKILL.md
  - .claude/skills/system-retro/SKILL.md
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

**Context economy (what comes back matters more than what goes out):**

Isolation controls what a subagent receives. This controls what it returns, and what any tool call pulls in. Measured on this repository's own transcripts across 147 sessions, content entering context is the single largest cost centre, because every token written once is then re-read on every subsequent turn. A token entering at turn 100 of a 600-turn session costs roughly 51 times its face value. So the question on every tool call and every dispatch is not "can I afford to read this once" but "can I afford to re-read this for the rest of the session".

- Bounded subagent returns. A dispatched agent writes its full output to a named file and returns a short summary plus that path, not a transcript. Target the return at roughly 300 words. The planner reads the file only when it actually needs the detail, which is often never. Nothing is lost, only relocated, and the detail is one read away instead of permanently resident.
- Grep before you read. On any file over roughly 500 lines, locate first and read the slice, using offset and limit. Read the whole file only when you genuinely need the whole file.
- Large tool output goes to a pointer. This is `system-design-patterns` pattern 4, and it applies to the output you consume (Read, Bash, Grep), not only to tools you author. Above roughly 500 lines or 20 KB, write to disk and keep the path plus a preview. Pattern 4's explicit-fail clause holds: if the full output cannot be retained, fail loudly rather than return a truncated result as if it were complete.
- Do not re-read to confirm. A file you just edited does not need reading back; the edit would have errored. Re-reading for reassurance pays the entry cost twice.

The economics, so the trade-off is a decision rather than a habit: this is a cost lever, never a correctness lever. When the detail genuinely changes the answer, pull it in and pay for it.

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

The context-economy test: did anything enter context this turn that I will be re-reading for the rest of the session and did not need, a full file where a slice would do, a full agent transcript where a summary and a path would do, or a re-read of something I just wrote?

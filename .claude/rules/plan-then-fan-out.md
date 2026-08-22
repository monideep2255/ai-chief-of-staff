---
name: plan-then-fan-out
description: For fan-out work, the reasoning model scouts and decomposes into non-overlapping task contracts before dispatch; cheaper execution models run each bounded piece in parallel
scope: portable
depends_on:
  - .claude/rules/parallel-first.md
  - .claude/rules/agent-first-default.md
  - .claude/rules/goal-contracts.md
  - .claude/rules/self-eval-loop.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - SYSTEM_OVERVIEW.md
  - DEPENDENCIES.md
  - .claude/skills/ingest-workflows/SKILL.md
  - .claude/skills/system-retro/SKILL.md
---

## Plan then fan out (reasoning model decomposes, cheaper models execute)

When work fans out to parallel agents, split the roles by model tier. The strongest reasoning model (Opus) owns the plan: it scouts the terrain, decomposes the work into tightly scoped, self-contained, non-overlapping tasks, and writes each task a contract. Cheaper, faster models (Sonnet 5 for substantive extraction and analysis, Haiku 4.5 for mechanical lookup and formatting) own execution: each runs one bounded task in parallel. The expensive reasoning is spent once, on the decomposition and the final synthesis. The repetitive execution is spent cheaply, in parallel.

### Why

- The value in fan-out work is the decomposition, not the execution. A good split (non-overlapping, self-contained, clear done-when) is a reasoning task. Running a bounded task against clear instructions is not.
- Cheaper execution models are faster and less likely to exhaust budget. Handing execution to top-tier reasoning agents wastes reasoning tokens on mechanical work and raises the odds of a session or rate-limit stall: a fan-out of reasoning-model agents can die together on a session limit, where the same work re-run as scoped Sonnet tasks is both cheaper and more robust.
- It maximizes throughput: more parallel workers per unit of budget.

### The split

Reasoning model (Opus), before any fan-out:
- Scout the terrain: list the files, map the tree, probe the surface. Do not send workers blind.
- Decompose into N non-overlapping tasks, partitioned by subtree, file range, topic, or entity, so two workers never write the same target.
- Write each worker a goal contract: done-when, inputs and scope, output path, constraints, blocked-stop (see `goal-contracts`).

Reasoning model (Opus), after the workers return:
- Synthesize the parts into the deliverable and own final judgment. Workers produce parts, the planner assembles the whole.

Worker models (Sonnet 5, or Haiku 4.5 for purely mechanical work):
- One bounded task each, in parallel, writing structured output to a named file, returning a short summary so the planner's context stays lean.

### How to apply

- Pass `model: "sonnet"` (or `"haiku"`) to the Agent tool for execution subagents. Default execution to Sonnet. Drop to Haiku only for purely mechanical work (grep-and-list, format conversion). Keep Opus for the plan and the synthesis.
- Scout before you decompose. The planner reads enough of the terrain to carve non-overlapping slices.
- Each worker task is self-contained: it names the files or scope, the output path, and the done-when. A worker should never need to coordinate with a sibling mid-run.
- Keep the worker's output off the planner's context: workers write to files, return a short summary, and the planner reads the files when assembling. This is a hard requirement, not a preference, and the worker's task contract states it: name the output file path in the contract and cap the return at roughly 300 words. A worker that returns its full report writes that report into the planner's context once and then re-reads it on every remaining turn of the session, which is how a cheap fan-out turns expensive after the fact. See the context-economy section of `parallel-first`.

### When to apply

- Any fan-out of 2 or more independent agent tasks: mining a folder tree, researching many sources, reviewing many files, migrating many apps.
- Any time you reach for parallel subagents under `parallel-first` or `agent-first-default`.

### When NOT to apply

- A single task with no parallelism. Just do it, or use one agent.
- Work where each step depends on the previous. That is sequential, there is nothing to fan out.
- Work where every item needs frontier reasoning (for example subtle judgment or adversarial verification). Keep those on the stronger model. Tier down only what is genuinely bounded.

### Relationship to other rules

- `parallel-first` decides what can run in parallel. `agent-first-default` decides whether to reach for an agent at all. This rule decides who plans and who executes once you do.
- `goal-contracts`: each worker task carries a contract, and the planner writes it. This is the meta-prompt-the-contract pattern applied per worker.
- `self-eval-loop`: the planner, or a separate fresh-context checker, grades the synthesized output. A worker never signs off its own part as final (maker cannot check).

### Three-state permissions

Allow:
- Decompose and dispatch parallel Sonnet or Haiku workers under an Opus-authored plan without asking.
- Choose the worker model tier per task (Sonnet default, Haiku for mechanical).

Ask:
- Before fanning out a large worker fleet (roughly 8 or more concurrent) that will consume significant budget, confirm scope first.

Deny:
- Never dispatch parallel workers without first scouting and decomposing. No blind fan-out.
- Never hand mechanical execution to the top reasoning model when a cheaper worker with a clear contract will do.
- Never let two workers write the same output target. Partition first.

The test: before fanning out, did the reasoning model scout the terrain and write each worker a self-contained, non-overlapping task contract, and are the workers running on the cheapest model that fits the task?

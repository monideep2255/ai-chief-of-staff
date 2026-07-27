---
name: bossman-mode
author: human
description: Full autonomous execution mode for building products. Activates after architecture/plan is agreed. Claude executes phases independently, stops only at phase boundaries or blockers. TRIGGER when user says "bossman mode", "boss man mode", "let's execute", "go build this", or "run the phase". DO NOT TRIGGER during architecture/planning discussions.
scope: project
argument-hint: "[--phase N] [--status] [--stop]"
depends_on:
  - .claude/rules/bossman-mode.md
  - .claude/rules/parallel-first.md
  - .claude/rules/boil-the-lake.md
  - .claude/rules/anti-rationalization.md
  - .claude/rules/self-eval-loop.md
  - .claude/rules/goal-contracts.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

# Bossman mode

Autonomous execution mode. You have a plan. Now execute it without asking questions.

## Invocation

```
/bossman                    # Activate bossman mode (requires existing plan)
/bossman --phase 2          # Execute a specific phase
/bossman --status           # Show current phase progress
/bossman --stop             # Exit bossman mode, return to normal collaboration
```

---

## Activation checklist

Before entering bossman mode, verify all three:

1. **Plan exists** - there is a written plan with numbered phases (in conversation, a plan tool, or a markdown file)
2. **Architecture agreed** - user has explicitly approved the architecture/approach
3. **Phase scope is clear** - the current phase has defined deliverables

If any of these are missing, say: "We need [missing item] before entering bossman mode. Let's nail that down first."

---

## Behavioral overrides (active while in bossman mode)

These rules are **suspended** during bossman mode execution:

| Rule | Why suspended |
|------|--------------|
| `pause-before-acting` | Plan is already agreed. No need to pause and re-check. |
| `preserve-your-thinking` | Decisions are made. This is execution, not deliberation. |
| `clarify-before-drafting` | Scope is defined. No Socratic questioning mid-build. |

These rules **remain active**:

| Rule | Why kept |
|------|---------|
| `file-protection` | Never delete without informing, even in execution mode. |
| `dependency-tracking` | Track what you build. |
| `parallel-first` | Maximize execution speed. |
| `boil-the-lake` | Do it 100%. No half-measures. |
| `writing-style` | Output quality stays high. |
| `git-workflow` | Clean commits. |
| `check-depended-by` | System integrity. |
| `goal-contracts` | Every phase starts with a testable done-when and a verify surface. A budget cap is a stop-and-report state, not "done". |

---

## Context management

Long-running bossman sessions degrade as context fills up. Three rules prevent this.

### Context budget tiers

| Tier | Context usage | Behavior |
|------|--------------|----------|
| PEAK | 0-30% | Full operation. Read files freely, inline results, detailed coordination. |
| GOOD | 30-50% | Normal operation. No changes needed. |
| DEGRADING | 50-70% | Economize reads: headers and frontmatter only for routing decisions. Summarize sub-agent results in one line. Warn in next phase checkpoint: "Context at ~X%. Consider fresh session after this phase." |
| CRITICAL | 70%+ | Checkpoint immediately. Write progress to a markdown file (`bossman-checkpoint-phase-N.md` in project root), list what is done, what remains, and decisions made. Tell the user: "Context budget critical. Start a fresh session and resume from checkpoint." |

### Degradation signals

You cannot read your own token count. Watch for these output-quality signals instead:

- Increasing vagueness: "appropriate handling" instead of specific file paths or code
- Skipped protocol steps: missing team dispatch, missing phase checkpoint fields
- Repeated phrases or filler where specifics should be
- Sub-agent prompts getting shorter or less detailed than earlier dispatches
- Summaries that restate rather than synthesize

When 2+ signals appear in the same phase: treat as DEGRADING regardless of estimated usage.

### Phase boundary = context reset point

At every phase boundary (Step 6: phase checkpoint), explicitly assess context health. If DEGRADING or CRITICAL, the checkpoint file becomes the handoff document for a fresh session. Include in the checkpoint:

1. Plan name and current phase number
2. What was completed (with file paths)
3. What remains (next phase details)
4. Decisions made (from the decisions log)
5. Any research context the next session will need

---

## Execution team

Inspired by Cursor's [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents) architecture: strict separation between planning and execution, parallel workers, a single judge for quality gating, and simpler systems over complex ones.

Bossman mode runs as a team, not a solo operator. The orchestrator (main session) decomposes, dispatches, and coordinates. Agents execute.

### Team roles

| Role | Count | Responsibility | Tool access | When dispatched |
|------|-------|---------------|-------------|-----------------|
| **Orchestrator** | 1 (main session) | Decompose phase into tasks, dispatch agents, track progress, report to user. Never builds directly when 2+ tasks exist. | All tools | Always active |
| **Researcher** | 1-N | Fetch docs, read APIs, find examples, explore unfamiliar codebases BEFORE builders start. Uses web-research skill, context7 MCP, repo-dive. | Read-only: Read, Grep, Glob, WebFetch, WebSearch, MCP tools | Pre-build: runs first to give builders context |
| **Planner** | 0-N | Sub-planners for complex areas. Spawned by orchestrator when a phase has sub-areas that need their own task decomposition. Planning is recursive and parallel. | Read-only: Read, Grep, Glob, Bash (read commands) | When phase complexity warrants it |
| **Builder** | 1-N | Execute independent build tasks. Write code, create files, run commands. Each builder focuses on one task until done, then reports back. Does not coordinate with other builders. | All tools, isolation: worktree when modifying shared files | Parallel dispatch after research/planning |
| **Judge** | 1 | Single quality gate. Reviews ALL builder output: does it work (functional), is it good (code quality), does it match the plan (completeness), any security issues? Replaces separate QA + reviewer roles. Simpler is better. | Read-only: Read, Grep, Glob, Bash (test/lint commands only) | After all builders complete |
| **Adversary** | 0-1 | Use the running artifact in hostile, unscripted ways to find what scripted checks miss. Over-reports on purpose. Files findings to a shared ledger only, never fixes, triages, or closes them. | Read-only: Read, Grep, Glob, Bash (run the artifact, not edit it) | After the judge, on any phase with a runnable artifact |
| **Test writer** | 1 | Write tests for what was built. Unit tests, integration tests, smoke tests as appropriate for the project. | All tools | After or alongside judge |
| **Integrator** | 0-1 | Wire independently-built components together. Handle imports, configs, entry points, shared state. Only dispatched when builders produced isolated pieces that need connecting. | All tools | Only when builders worked on separate components that must connect |

### Key design principles (from [Cursor scaling agents](https://cursor.com/blog/scaling-agents))

1. **Simpler beats complex.** Additional oversight roles create fragility, not quality. The judge is one agent, not three.
2. **Workers don't coordinate with each other.** Each builder gets a task and grinds on it independently. The orchestrator handles coordination.
3. **Planning is recursive.** Complex phases get sub-planners that run in parallel, each producing their own task list.
4. **Fresh starts combat drift.** If a builder is stuck or going in circles, kill it and dispatch a new one with a clearer prompt rather than trying to course-correct.
5. **The integrator is conditional.** Cursor found integrators bottleneck at scale. At our scale (3-8 agents), it adds value when components must connect. Skip it when builders produce self-contained deliverables.
6. **Thin orchestrator.** The orchestrator's job is routing, not reading. To decide which agent gets which task, read file headers and frontmatter, not full contents. Delegate full reads to the agent that needs the information. When sub-agents return results, capture a one-line summary, not the full output. The orchestrator that accumulates the least context coordinates the best.
7. **Fresh context per agent.** Every dispatched agent starts with a clean context window. Pre-inject only what that specific agent needs (task description, relevant file paths, architectural constraints, research findings). Never pass accumulated conversation history. The agent prompt template below enforces this.

### Model tiering (cost lever)

Assign a model tier per role, not one model for the whole team. Keep the orchestrator thin (routing, not reading full files), so its model choice barely matters, then push the strongest model to where judgment is hard and a cheaper model to where the work is well-scoped or bulk.

| Role | Model tier | Effort | Why |
|------|-----------|--------|-----|
| Orchestrator (main session) | User's session model | n/a | Fixed by the user. Keep it thin. |
| Researcher / reader | Cheap or mid | low | Bulk document reading. The cost is the input, not the reasoning. |
| Builder | Mid | medium | Well-scoped construction against a clear task. Reserve high effort for genuinely hard builds. |
| Judge | Strongest | high or xhigh | Quality gate. A missed defect here is the most expensive, so pay for the reasoning. |
| Sub-planner | Strongest | high | Decomposition errors cascade into every downstream builder. |

Pass `model` and `effort` on each `Agent` dispatch. A tool-less coordinator that delegates heavy reading to cheap scoped workers measured 2.5x cheaper and roughly 3x faster than one frontier model doing everything, with about 84 percent of input tokens billed at the cheap worker rate (the plan-big-execute-small pattern). Delegation has a fixed setup cost, so do not shard a phase into many tiny tasks just to parallelize. Each dispatched agent should carry a task worth its overhead.

### The judge produces evidence, not a verdict

A judge that reports "looks good, all checks pass" without showing its work is the maker-checker failure `self-eval-loop.md` warns about: a grader that knows the rubric drifts toward approving everything. Force the judge to produce evidence, and default it to fail when evidence is absent.

For every claim, the judge's report must:
- Cite the exact `file:line` for a code finding, not "the auth module looks fine".
- Paste the actual command output for a functional or test claim (the test line, the lint result), not "tests pass".
- Quote the specific offending line for a security or quality finding, not "no security issues found".

If the judge cannot produce evidence for a check, that check fails. "I could not verify X" is a fail, never a pass.

Verify the premise, not only the leaves. The judge's default instinct is to check each artifact against its assigned task: did builder 3 produce the file it was told to. That is leaf verification, and it passes even when the decomposition itself was wrong. Add one level up: does the set of completed tasks actually satisfy the phase done-when from the goal contract? A phase where every builder succeeded at its own task but the tasks together miss the phase's stated outcome is a failed phase, not a passed one (the "rigor about the wrong layer" failure from `goal-contracts.md`).

### The adversary attacks what the judge certifies

The judge is scripted verification. It checks the artifact against the plan, the tests, and the quality rubric, so it catches the failures someone thought to specify. It is blind to the failure nobody wrote a check for. That blind spot is where a fluent wrong answer, a bad-input crash, or an odd-sequence corruption hides, and a green judge verdict does not touch it.

The adversary is the unscripted half. It uses the running artifact in hostile ways the spec never imagined: malformed and boundary input, out-of-order operations, edge cases, and for a question-answering system, queries engineered to draw a confident wrong answer. It over-reports on purpose, because a false alarm is cheap and a missed defect is not. It files every finding to a shared ledger and stops there. It never fixes, triages, or closes its own findings; the judge or a fix agent triages them, and only the ledger's designated closer closes them. This is the maker-cannot-sign-off split of `self-eval-loop.md` applied to verification itself: the finder is never the closer.

Run the adversary after the judge, only on a phase that produced a runnable artifact. A green judge verdict is necessary but not sufficient; the adversary is the pressure that decides whether the artifact is actually trustworthy. Source: an autonomous multi-agent build harness that pairs a scripted qa role with a separate unscripted adversary.

### Team dispatch order

```
Phase start
  ├── Researchers (parallel) ─── gather context, docs, examples
  ├── Sub-planners (parallel, if needed) ─── decompose complex sub-areas
  │
  ├── [research + planning complete]
  │
  ├── Builders (parallel) ─── execute tasks independently
  │
  ├── [all builders complete]
  │
  ├── Judge ─── single quality gate (pass/fail + details)
  ├── Adversary (only on a runnable artifact) ─── hostile unscripted use, files to the ledger
  ├── Test writer (parallel with judge if targets are clear)
  ├── Integrator (only if components need wiring)
  │
  ├── [judge passed, tests written, integration done]
  │
  └── Phase checkpoint ─── report to user
```

### Agent prompt template

When dispatching any team member, include in the prompt. Each agent gets a clean context window with only what it needs pre-injected. Do not paste accumulated conversation history, prior agent outputs, or full file contents into agent prompts. If an agent needs file content, give it the path and let it read the file itself.

```
You are the [ROLE] on a bossman mode execution team.

Context: [1-3 sentences of what researchers found, not full output]
Plan: [paste ONLY the relevant phase/task details, not the full plan]
Your task: [specific deliverable]
Constraints: [architectural decisions that apply]
Files to touch: [specific paths, not vague areas]
Files to read: [paths the agent should read itself for full context]

Do not ask questions. Execute and report back.
If stuck, report the blocker clearly. Do not guess on ambiguous requirements.
```

Orchestrator rule: when a sub-agent returns, capture a one-line summary of what it produced and which files it touched. Do not inline the full result into your context.

### Team-aware dispatch (multi-repo)

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled and the task spans multiple repos, use named teammates instead of anonymous agents.

| Scenario | Tool | Why |
|----------|------|-----|
| Single-repo, single task | `Agent` (fire-and-forget) | Simpler, fresh context, no overhead |
| Multi-repo or iterative fix loop | `TeamCreate` + `SendMessage` | Persistent context, addressable by name |

Dispatch: `TeamCreate` one teammate per repo. `SendMessage` to assign tasks. Teammates persist across the phase, so the judge can `SendMessage` fixes directly to the builder that wrote the code.

### Reference repos

If you're dispatching agents against an unfamiliar repo you've cloned via `/repo-dive`, read its deep-dive doc first rather than having agents rediscover the architecture from scratch. This is especially valuable for multi-repo or multi-team dispatch, where the same unfamiliar codebase would otherwise get re-explored by every agent that touches it.

---

## Multi-agent safety

When 3+ builder agents run in parallel (worktrees or same repo), these conventions prevent agents from corrupting each other's work. These are worth adapting from any battle-tested multi-agent orchestrator you study.

### Scoped commits

- Each builder agent commits only its own changes. Never `git add -A` or `git add .` across the full repo.
- Stage files by name: `git add path/to/file1.py path/to/file2.py`.
- When the user says "commit all," the orchestrator groups changes into logical commits, not one giant commit.

### File conflict handling

- When an agent encounters files it did not create or modify, it notes them and continues. It does not clean them up, reformat them, or include them in its commit.
- If two agents need to modify the same file, use `isolation: "worktree"` for both. The integrator agent wires the results together afterward.
- If an agent sees unexpected diffs in `git status`, it reports them in its completion summary but does not resolve them.

### Git state protection

- Do not create, apply, or drop `git stash` entries. Other agents may be working.
- Do not switch branches unless explicitly instructed by the orchestrator.
- Do not run `git pull --rebase --autostash`. Use `git pull --rebase` only when the orchestrator coordinates it.
- Do not create or remove `git worktree` checkouts unless explicitly requested.

### Formatting auto-resolve

- If staged + unstaged diffs are formatting-only (lint, whitespace, import order), auto-resolve without asking.
- If a commit or push was already requested, auto-stage formatting-only follow-ups in the same commit or a tiny follow-up commit. No extra confirmation needed.
- Only ask the user when changes are semantic (logic, data, behavior).

### Shared-ledger coordination

When parallel agents share findings, defects, or task state, they coordinate through one shared markdown ledger, not by each writing wherever they like. Without a convention, two agents writing status to the same file overwrite each other, and an agent that raised an item can quietly close it. A single-writer-per-state ledger removes both races by construction and leaves an auditable trail. An autonomous build harness runs its `DEFECTS.md` and `ADVERSARIAL_REVIEW.md` this way. Four rules:

- Single writer per state: each state in the ledger has exactly one role authorized to set it. The adversary files findings, the judge or a fix agent triages, only the designated closer closes. No state has two writers.
- Mandatory reason on judgment states: any state that reflects a judgment call (accepted, rejected, closed, disputed) carries a one-line reason. A bare status change with no reason is invalid.
- Append-only history line per transition: every transition appends a who-what-why line to the item's history. History is never rewritten, only extended, so the trail reconstructs the full life of the item.
- The raiser never closes: the party that raised an item is never the party that closes it. The finder reports, a different role verifies and closes. This is the same finder-is-not-closer rule the adversary follows.

Single-writer-per-state stays the default: it needs no coordination protocol and no retry logic, so use it whenever one role can own each state. It breaks down only when two agents legitimately need to write the same state concurrently, for example two builders both appending defects to the same ledger entry at once. For that case, name optimistic concurrency as the alternative, not a replacement: each writer reads the current state plus its hash, writes its patch tagged with that base hash, and the ledger accepts the write only if the hash still matches. A stale write is rejected with a structured conflict signal so the agent knows to re-read and retry, rather than silently overwriting the other agent's change. A hash-based patch command that rejects a stale write with a distinct exit code instead of failing generically is a good worked-example pattern, letting the caller tell "someone else wrote first" apart from any other error and retry deliberately. Reach for this only when single-writer genuinely cannot hold; most ledgers should stay on the simpler default.

### Subagent tool-scope hygiene

When a sub-planner or builder is itself dispatched as an orchestrator of further sub-agents (recursive planning, a researcher that fans out to readers, a builder that supervises parallel children), the dispatched sub-orchestrator must follow the untrusted-source tier separation pattern:

- The sub-orchestrator declares an explicit tool list. No "All tools".
- The sub-orchestrator never holds Write, Slack, email, or any external MCP. Side effects are emitted as typed events, not direct tool calls.
- Subagents that read untrusted content (web, third-party APIs, user-supplied documents) get the retrieval MCP and Read. They do not get Write or any external-channel tool.
- Subagents that write outputs hold Write and Edit. They do not get retrieval MCPs.
- Subagents that synthesize JSON from a reader's output never receive the raw document text. They consume schema-validated JSON only.

This is the four-tier model and the rationale for keeping sub-orchestrators privilege-light (define your own tiering doc if you adopt this pattern).

Hygiene check before the first sub-orchestrator dispatch in a phase:

1. List every dispatched sub-orchestrator and its declared tool list.
2. Flag any sub-orchestrator whose list contains Write, Edit, Slack, email, or an external MCP.
3. If flagged, refactor before dispatch: move the privilege to a leaf subagent, not the sub-orchestrator.

The main bossman session orchestrator (the user-facing session) is exempt from this check because the user controls it directly. The check applies only to agents bossman itself dispatches as further orchestrators.

---

## Execution protocol

### Step 1: confirm entry and show team

Print:

```
Bossman mode: ON
Plan: [plan name or summary]
Phase: [N] - [phase title]
Deliverables: [list what this phase produces]
Estimated scope: [files to create/modify]

Team:
- Orchestrator: main session
- Researchers: [N] agents for [what needs lookup]
- Sub-planners: [N, or "none - phase is straightforward"]
- Builders: [N] agents for [task list]
- Judge: 1 agent (post-build)
- Adversary: [1 if the phase produces a runnable artifact, or "not needed"]
- Test writer: 1 agent (post-build)
- Integrator: [1 if components need wiring, or "not needed"]

Dispatching now. Next check-in at phase completion.
```

### Step 2: research (if needed)

- Dispatch researcher agents in parallel for any unfamiliar APIs, libraries, or codebases
- Researchers report back with context that builders will need
- Skip this step if the team already has sufficient context from prior phases or the planning stage

### Step 3: sub-planning (if needed)

- For complex phases, dispatch sub-planner agents to decompose specific areas
- Sub-planners run in parallel, each producing a task list for their area
- Orchestrator merges sub-plans into the builder dispatch
- Skip for straightforward phases where task decomposition is obvious

### Step 4: dispatch builders

**Artifact wiring check (required when 3+ agents are in the pipeline):**

Before dispatching, for each agent that feeds output to another agent, confirm:

1. The upstream agent declares what it produces (file path, schema, or artifact type)
2. The downstream agent's declared input matches that format
3. Any type mismatch has an explicit conversion step assigned to a specific agent

If a mismatch is unresolved, do not dispatch. Assign a converter agent or adjust task scope before proceeding. An unvalidated payload flowing between agents is the primary lateral prompt-injection vector in multi-agent pipelines.

Skip this check only when every agent produces self-contained deliverables with no downstream consumers.

- Dispatch builder agents in parallel (one Agent tool call per task, all in a single message)
- Each builder gets: research context, specific task, file paths, constraints
- Use `isolation: "worktree"` for tasks that touch overlapping files
- Builders do not coordinate with each other. They grind on their task and report back.
- If a builder is stuck or going in circles: kill it and dispatch a fresh one with a clearer prompt
- Use Ralph Loop if available for sustained autonomous execution

### Step 5: judge + tests + integration

Once all builders report back:

1. Dispatch judge agent to review ALL builder output (functional correctness, code quality, plan adherence, security). Give it the strongest model at high effort. It must produce cited evidence for every claim and verify the phase premise, not just each artifact (see "The judge produces evidence, not a verdict")
2. On any phase that produced a runnable artifact, dispatch an adversary agent (see the adversary role and "The adversary attacks what the judge certifies"). It uses the running artifact in hostile, unscripted ways, over-reports on purpose, and files every finding to a shared-ledger file. It never fixes, triages, or closes its own findings; the judge or a fix agent triages them, and only the ledger's designated closer closes them.
3. Dispatch test writer agent (can run in parallel with judge if test targets are clear)
4. Dispatch integrator agent ONLY if builders produced isolated components that need wiring
5. If judge fails the work or the adversary files findings: triage. Minor issues = dispatch a builder fix agent. Major issues = escalate to user.

### Step 6: phase checkpoint

When the phase is complete (all agents done, judge passed), print:

```
Phase [N] complete.

What was done:
- [deliverable 1]
- [deliverable 2]
- [deliverable 3]

Team activity:
- Researchers: [N] dispatched, [summary of findings]
- Builders: [N] dispatched, [N] succeeded, [N] needed retry
- Judge result: [pass/fail with details]
- Adversary findings: [N filed to ledger, or "not run - no runnable artifact"]
- Tests written: [count and location]
- Integration: [done/not needed]

Decisions made (without asking):
- [decision 1]: chose X over Y because [reason]
- [decision 2]: chose A over B because [reason]

Blockers: [none, or list]

Context health: [PEAK / GOOD / DEGRADING / CRITICAL]
[If DEGRADING: "Checkpoint file written. Recommend fresh session for next phase."]
[If CRITICAL: "Checkpoint file written. Fresh session required."]

Next phase: [N+1] - [title]
Recommendation: [proceed / adjust plan / stop and discuss / fresh session recommended]

Waiting for your go.
```

### Step 7: await approval

Do NOT proceed to the next phase until the user says to continue. The user may:
- Say "go" or "next" to proceed to the next phase
- Adjust the plan based on what they see
- Ask questions about decisions made
- Exit bossman mode with `/bossman --stop`

---

## Stop conditions (exit bossman mode immediately)

1. **Architecture-level change needed** - something in the plan is fundamentally wrong
2. **Blocker with no reasonable workaround** - missing credentials, broken dependency, ambiguous requirement that could go either way with major consequences
3. **Phase complete** - normal checkpoint
4. **User says stop** - `/bossman --stop` or any clear signal to pause

---

## Status check

If invoked with `--status`, print current state:

```
Bossman mode: [ON/OFF]
Current phase: [N] - [title]
Progress: [what's done so far in this phase]
Decisions made: [list]
Blockers: [none or list]
```

---

## Growth path

**Level 1 (now):** Single-phase execution with full agent team. Manual approval between phases. Orchestrator dispatches researchers, builders, judge, test writer. User reviews at checkpoints.

**Level 2 (trust building):** Multi-phase execution. Ralph Loop keeps the orchestrator running between phases. Judge agent gates phase transitions instead of user approval for non-architectural phases. Sub-planners handle recursive decomposition of complex phases.

**Level 3 (Cursor-scale):** Full autonomous multi-phase execution. Checkpoint files written to disk at each phase boundary. Morning summary of everything built, tested, and judged while user was away. Hundreds of builders if the codebase warrants it. Fresh-start pattern: stuck agents get killed and restarted with clearer prompts rather than debugged in-place.

**Level 4 (multi-team):** `TeamCreate` + `SendMessage` for persistent named teammates across repos (gastown, gsd, gsd-2). Each team has its own orchestrator running its own research/build/judge cycle. A meta-orchestrator coordinates between teams at phase boundaries. Useful when the project spans different tech stacks, repos, or deployment targets.

## Design inspiration

Architecture inspired by Cursor's [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents) post: strict planner/worker separation, single judge over multiple QA roles, workers that don't coordinate with each other, recursive sub-planning, and the principle that simpler systems outperform complex ones. Adapted for Claude Code's agent dispatch model and single-phase-at-a-time execution.

## Shortcuts to resist

See `.claude/rules/anti-rationalization.md` for the general pattern. These three are specific to this skill.

| Shortcut | Why it's tempting | Counter |
|----------|--------------------|---------|
| "Scope is defined, so I can skip re-reading the plan before executing this phase" | Bossman mode suspends clarify-before-drafting, so it feels like re-reading is also suspended | Only deliberation before acting is suspended. Re-reading the agreed plan before each phase is not deliberation, it's fidelity to what was already agreed |
| "This phase feels done, I'll mark it complete without checking the verify surface" | Loop discipline requires a concrete verify step, which slows down a phase that already looks finished | A budget or iteration cap is a stop-and-report state, not done. Only the named verify surface (test, count, judge pass) closes a phase |
| "I'll combine two phases to save a checkpoint" | Fewer checkpoints feels faster and the phases look related | Each phase boundary is a decision point the user agreed to. Combining phases removes the checkpoint they can still veto at |

## Exit checklist

Done when all of these are true:

- [ ] Activation checklist passed before entering bossman mode (plan exists, architecture agreed, phase scope clear)
- [ ] All phase deliverables were completed
- [ ] Judge produced cited evidence for every claim, verified the phase premise (not just each artifact), and all checks passed
- [ ] On any runnable-artifact phase, an adversary ran after the judge and its findings were logged to the ledger and triaged (not closed by the adversary)
- [ ] Phase checkpoint was reported with decisions log
- [ ] Artifact wiring check passed (all generated files are referenced from the correct index)
- [ ] Context health was monitored (DEGRADING/CRITICAL tiers handled correctly)
- [ ] User approved phase completion before proceeding

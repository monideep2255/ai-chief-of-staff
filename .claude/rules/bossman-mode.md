---
description: "Autonomous execution mode - suspends deliberation rules when bossman mode is active"
globs: ["!*"]
depends_on:
  - .claude/skills/bossman-mode/SKILL.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Bossman mode rule

This rule is loaded by the `/bossman` skill when activated. It is not always-on.

When bossman mode is active (user has invoked `/bossman` and activation checklist passed):

### Suspended behaviors

- **Do not pause to check if clarification is needed** (overrides pause-before-acting step 2). Rules still apply, but you do not stop to ask.
- **Do not ask what the user thinks before acting** (overrides preserve-your-thinking). Decisions were made during planning. Execute.
- **Do not run Socratic clarification before drafting** (overrides clarify-before-drafting). Scope is defined.
- **Do not ask "should I do X or Y?"** - pick the better path, note the choice, keep moving.

### Preserved behaviors

- File protection: never delete without confirming first.
- Dependency tracking: track what you build.
- Writing style: output quality stays high.
- Git workflow: clean commits, no co-author lines.
- Parallel-first: maximize speed.
- Boil-the-lake: do it 100%.
- Book inventory check: never generate a new book or systems map without the inventory-and-confirm gate (see `book-inventory-check.md`), even in bossman mode. This gate is not on the suspended list above.

### Loop discipline (preserved)

Autonomous execution is a loop, and loops fail by running loudly and stopping quietly. The loop carries its own guardrails even in bossman mode:

- Every phase has a testable done-when and a verify surface before it starts (see `goal-contracts`).
- Iteration caps and no-progress detection: if two consecutive iterations produce no measurable progress toward the phase done-when, stop and hand back rather than burn tokens.
- A budget or context-health cap is a stop-and-report-blockers state, not a "done" state. Hitting the cap never means the phase succeeded.
- Trace what the loop did: log the choice made at each decision point so a fresh context can reconstruct the run.

### Three-state permissions

Allow:
- Write files, run commands, dispatch agents without conversational confirmation
- Make tactical decisions (library choice, file structure, naming) and log them
- Execute an entire phase autonomously

Ask:
- Architecture-level changes that contradict the agreed plan
- Anything that affects phases beyond the current one
- Deleting files or reverting prior work

Deny:
- Proceeding to the next phase without user approval
- Ignoring a blocker by guessing
- Pushing to remote without explicit instruction

### When bossman mode is NOT active

This rule has no effect. All suspended rules operate normally.

The test: is bossman mode actually active, and if so did I keep every preserved safety rule while suspending only the listed deliberation rules?

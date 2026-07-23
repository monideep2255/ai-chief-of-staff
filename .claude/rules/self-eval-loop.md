---
name: self-eval-loop
description: For skills producing substantial output, use a two-agent pattern where one agent produces and a second agent with fresh context grades against pass/fail criteria
scope: portable
depends_on:
  - .claude/rules/parallel-first.md
  - .claude/rules/anti-rationalization.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/rules/parallel-first.md
  - .claude/rules/sandbox-diagnosis.md
  - .claude/rules/goal-contracts.md
  - .claude/skills/bossman-mode/SKILL.md
---

## Self-eval loop

For skills producing substantial output, use a two-agent pattern. A second agent with fresh context grades the output against pass/fail criteria. This is more reliable than single-shot self-review because fresh context removes "I wrote it so it must be good" bias.

This is the maker/checker split: the model that produced the output must never be the one that signs off on it, because a model grading its own work just agrees with itself. The checking signal has to come from somewhere the maker does not control, a different agent, a test, a grep, a count.

### The pattern

1. First agent produces the output (doc, analysis, multi-file change)
2. Second agent with fresh context receives only the output and the pass/fail criteria
3. Second agent grades each criterion as pass or fail with a one-line justification
4. If any criterion fails, iterate: fix the issue, then re-grade

### When to apply

- Docs, proposals, or strategy documents with 3+ sections
- Multi-file system changes (new skills, rule rewrites, architecture changes)
- Any output that will be reviewed by someone else
- Bossman-mode judge step (already uses this pattern)

### When NOT to apply

- Quick edits, single-file patches, or formatting fixes
- Meeting notes and checklists (capture tasks, not judgment)
- When the user explicitly says "skip review" or "good enough"
- When time constraint makes iteration impractical (user waiting, urgent fix)

### Context isolation matters

The second agent must start with a clean context window. Do not pass the first agent's reasoning, draft history, or conversation context. The grading agent receives:

1. The final output (file paths or inline content)
2. The pass/fail criteria (a numbered checklist)
3. Nothing else

This isolation is what makes the pattern work. A self-reviewer that inherits the author's context inherits the author's blind spots.

### Three-state permissions

Allow:
- Dispatch a grading agent for any substantial output without asking
- Iterate on failed criteria without asking

Ask:
- Before running a third iteration (if two rounds of fixes have not resolved a failing criterion, the criterion itself may be wrong)

Deny:
- Never skip the grading step for substantial output in bossman mode
- Never pass conversation history to the grading agent

The test: did my substantial output get graded by a fresh-context agent, or did I only self-review in the same context?

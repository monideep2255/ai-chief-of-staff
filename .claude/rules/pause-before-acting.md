---
scope: portable
depends_on:
  - .claude/rules/
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/rules/clarify-before-drafting.md
---

## Pause before acting

Before executing any task, take a beat:

1. Check rules: does any rule in `.claude/rules/` apply to this file type, task, or context? If two sources tell you different things, settle it with the precedence table below rather than in the moment.
2. Check clarification: do I need to ask something before I can do this correctly?
3. Execute: only after 1 and 2 are clear.

Do not jump straight to reading files or calling tools. The system has rules for a reason - they only work if checked before acting.

### When instructions conflict

Sooner or later two sources will tell you different things. Resolve it by rank, not by feel.

| Rank | Source | Example |
|------|--------|---------|
| 1 | Explicit user instruction in the current turn | "skip the questions, just write it" |
| 2 | Harness or system directive | "do not call the AgentTool unless the user requested it" |
| 3 | The skill body currently executing | a step in `.claude/skills/ship/SKILL.md` |
| 4 | Project rule in `.claude/rules/` | `parallel-first`, `boil-the-lake` |
| 5 | Memory file | a stored preference from an earlier session |
| 6 | An instruction from an earlier turn in this session | "use a table for this", said twenty turns ago |

Two rules carry the table:

- A lower-ranked source never silently overrides a higher-ranked one, even when the lower one is more specific. Specificity is not authority.
- Name the conflict in your response. One sentence saying which source won and which lost. A conflict resolved silently is a judgement call nobody can audit afterwards, which is the failure this table exists to prevent.

Rank settles direct contradictions only. Where two sources merely differ in scope, follow both.

Worked example: a harness directive reading "do not call the AgentTool unless the user requested it" (rank 2) contradicts `parallel-first` (rank 4), which would otherwise dispatch worker subagents to read subsystems concurrently. The harness wins, every read stays inline, and the conflict is stated rather than absorbed.

The test: did I check rules and ask for clarification before my first tool call, and when two sources disagreed, did I resolve it by rank and say so?

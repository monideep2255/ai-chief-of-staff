---
description: "Log every adopted OS improvement to OS_IMPROVEMENTS.md. The user-facing record of how the personal OS evolves through pattern adoption."
scope: portable
alwaysApply: true
depends_on: [OS_IMPROVEMENTS.md]
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/skills/os-maintain/SKILL.md
  - .claude/skills/repo-dive/SKILL.md
  - .claude/skills/system-retro/SKILL.md
---

## OS improvement logging

When you apply an improvement to the personal OS, append a row to `OS_IMPROVEMENTS.md` at the repo root. This is the user-facing tracker of how the OS evolves. It is not optional and it is not the same as `DECISIONS.md`.

### What counts as an OS improvement

A change to a system component (a rule, skill, agent, hook, config, or index pattern) that was adopted from a source, not just routine maintenance. Sources: a repo dive, a system retro, a board session, an ingested article, or a daily-use insight.

The test: did this change alter how the OS behaves or what it enforces, and did it come from a pattern worth remembering? If yes, log it.

### What does NOT count

- Content edits (meeting notes, book chapters, check-ins, leaf docs in `Forge/logs/`, `Learning/`)
- Pure index sync that os-maintain does after a component change (the component change is the loggable event, not the sync)
- A typo or formatting fix in a component with no behavior change
- Generating a deep-dive analysis doc that adopts nothing (the dive is a source; log only the patterns you actually apply from it)

### How to log

Append a row to the "Applied" table (or "Proposed" / "In progress" / "Deferred" / "Rejected" as fits the lifecycle):

```markdown
| # | Proposal | Source | Proposed | Applied | What changed |
```

Use the next number, or `-` if it is a sibling of an existing numbered batch. Update the "Last updated" date at the bottom.

### Relationship to DECISIONS.md

- `OS_IMPROVEMENTS.md`: always log an adopted OS pattern here. It tracks the what and the source.
- `DECISIONS.md`: also log here only if the change is a heavyweight, hard-to-reverse architectural choice with alternatives weighed (per `decision-logging.md`).
- A single change can warrant both. Most OS improvements are pattern adoptions and go to `OS_IMPROVEMENTS.md` only.

### Three-state permissions

Allow:
- Append a row to OS_IMPROVEMENTS.md freely after applying an OS improvement
- Add "Proposed" rows for patterns surfaced but not yet applied

Deny:
- Never delete or rewrite existing rows (historical record)
- Never log content edits or routine index sync as improvements

The test: when I applied a rule, skill, agent, hook, or config change adopted from a source, did I add a row to OS_IMPROVEMENTS.md?

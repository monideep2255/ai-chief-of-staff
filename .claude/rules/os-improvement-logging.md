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

### Every open row carries its revisit trigger

The Proposed and Deferred tables both carry a "Revisit when" column, and it is required on every new row. Write a concrete, checkable trigger: a named event (the next retro, the next hook change), a date, or a project milestone. "Eventually", "when there is time", and an empty cell are not triggers.

An idea parked with no trigger is not deferred, it is forgotten with extra steps. The failure this closes is real and repeated: two proposals sat through three cycles before being demoted, because nothing in the table said when to look at them again, so each cycle re-read them and re-deferred them.

Legacy rows carrying `-` are not exempt, they are unbacked. Each retro assigns a trigger to the `-` rows it touches or rejects them outright, so the backlog drains rather than accumulating. The retro step that enforces this is Step 2's rules audit in `.claude/skills/system-retro/SKILL.md`.

This is the self-expiring exception pattern, the same idea as a lint configuration that reports unused disable directives as errors: a suppression that has stopped being necessary fails the build and asks to be deleted. An exception that cannot expire on its own becomes permanent by default.

### Relationship to DECISIONS.md

- `OS_IMPROVEMENTS.md`: always log an adopted OS pattern here. It tracks the what and the source.
- `DECISIONS.md`: also log here only if the change is a heavyweight, hard-to-reverse architectural choice with alternatives weighed (per `decision-logging.md`).
- A single change can warrant both. Most OS improvements are pattern adoptions and go to `OS_IMPROVEMENTS.md` only.

### Three-state permissions

Allow:
- Append a row to OS_IMPROVEMENTS.md freely after applying an OS improvement
- Add "Proposed" rows for patterns surfaced but not yet applied
- Reject a Proposed or Deferred row outright when its trigger fires and the idea no longer earns its place, recording the reason in the Rejected table

Deny:
- Never delete or rewrite existing rows (historical record)
- Never log content edits or routine index sync as improvements
- Never add a Proposed or Deferred row with an empty or vague "Revisit when" cell

The test: when I applied a rule, skill, agent, hook, or config change adopted from a source, did I add a row to OS_IMPROVEMENTS.md, and does every row I parked instead of applying carry a concrete revisit trigger?

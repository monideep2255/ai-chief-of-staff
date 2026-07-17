---
description: "Log heavyweight decisions to DECISIONS.md. Enforced automatically by docs-sync scanning for structural changes."
scope: portable
alwaysApply: true
depends_on: [DECISIONS.md]
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/agents/docs-sync.md
  - .claude/rules/memory-provenance.md
---

## Decision logging

Log decisions with consequential impact to `DECISIONS.md` at the repo root. This is not a general journal. It captures choices you made that would be expensive to reverse, and that future sessions need to know about.

### What counts (consequential impact only)

Three categories:

1. Architecture: new folders, folder reorganizations, structural patterns (e.g. playbooks as navigation layer, separating career docs from PM reference)
2. Tool selection: choosing one library, framework, database, or service over another
3. Process changes: new rules, new skill steps, changes to how the OS operates

The test: would reversing this decision require significant rework across multiple files or sessions? If yes, log it. If someone could undo it in 5 minutes, or if the reasoning is obvious from the code or commit message, skip it.

### What does NOT count

- Content decisions (which book to write, which doc to ingest, what to include in meeting notes)
- Obvious defaults (use existing patterns, follow existing conventions)
- Decisions already captured in a rule, config, or code comment
- One-off formatting or naming choices within existing conventions
- Anything ephemeral that won't matter next session

### Format

```markdown
| Date | Decision | Alternatives considered | Why |
|------|----------|------------------------|-----|
| YYYY-MM-DD | What we chose | What we didn't choose | The reason |
```

### Automated enforcement

Decision logging is enforced by docs-sync during /ship. docs-sync scans for structural changes (new folders, reorganizations, new system components, process changes) and evaluates whether a loggable decision was made. If it qualifies as heavyweight, docs-sync appends the row to DECISIONS.md automatically. No prompting the user.

This replaces the old model of "remember to log after every debate." Decisions now get caught by the system, not by discipline.

### Manual logging

Still allowed. If you make a heavyweight decision during a planning session or architecture discussion, log it immediately. The automated scan is a safety net, not the only path.

### Three-state permissions

- Allow: append to DECISIONS.md freely after a heavyweight decision
- Allow: docs-sync auto-appends during structural change detection
- Deny: never delete or modify existing entries (historical record)
- Deny: never log content decisions, formatting choices, or ephemeral picks

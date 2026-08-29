---
scope: project
depends_on:
  - CLAUDE.md
  - .claude/WHATS_NEW.md
depended_by:
  - .claude/README.md
---

## Session greeting

On your first response in every conversation, before addressing the user's request, print a brief session summary:

```
**Session Context**  -  [date]
- Focus: [top 1-2 priorities from Current Focus]
- Recent commits (last 3):
  1. [commit summary]
  2. [commit summary]
  3. [commit summary]
- System updates: [list WHATS_NEW.md entries, numbered]

**Daily nudges:**
- Forge: [check Forge/logs/daily/ for today's date. If no log: "No session today. Try /forge --quick (15 min)". If done: "Done for today."]
- Learning: [check Learning/1-current-focus/ for any books. Pick one and say: "Continue reading: [book name]". If no books in 1-current-focus: "No book in active reading. Move one to Learning/1-current-focus/."]
- Exercises: [check Forge/exercises/ for this week's artifacts. If <2: "Only [N] exercise artifacts this week. Try /forge --deep for a portfolio piece."]
```

Then proceed with the user's request.

This is mandatory. Do not skip it. The user relies on this to orient themselves at the start of each session.

The test: did I print the session summary with focus, last 3 commits, system updates, and daily nudges as my very first response?

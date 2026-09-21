# Papercuts

A running log of anything that cost time mid-session. Not bugs in the work, friction in the tooling: a command that failed for a non-obvious reason, a path that was denied, a flag that turned out to be wrong, a setup step that had to be rediscovered.

Two uses, and the second is the one that pays:

- Check this file first when tooling fails mysteriously. A symptom logged here already has its fix written down.
- Read the whole file at each retro. One entry is noise. The same symptom three times is the constraint, and `.claude/rules/attack-the-constraint.md` exists to act on exactly that.

## How to write an entry

Append one row when you lose time to something, in the session where it happened. Do not batch them for later; the detail that makes an entry useful is gone by the next day.

| Field | What goes in it |
|-------|-----------------|
| Date | ISO date, the day the time was lost |
| Symptom | What you saw, in the words you would search for later. The error text, not a summary of it |
| Fix | What actually resolved it, specific enough to repeat. "Worked after a retry" is not a fix, it is an unsolved entry |
| Project | Which repository or area you were in |

Two rules keep the log honest:

- Log the symptom even when the fix is unknown. An entry reading "no fix found, worked around by X" is more useful than no entry, because the third occurrence is what justifies solving it properly.
- Do not log a mistake you made once and immediately understood. This is a log of friction that will recur, not a record of typos.

## Scope

A log in one repository covers the sessions that load that repository's rules. Work you do elsewhere does not append to it automatically. Keep one log per repository you work in regularly, or accept that this one records only the work done here, but do not assume it is catching everything.

## Entries

| Date | Symptom | Fix | Project |
|------|---------|-----|---------|

The log starts empty and fills as you work. The first few entries will feel too small to be worth writing down, which is the point: the losses that matter are individually forgettable, and the pattern only appears once several are on the page.

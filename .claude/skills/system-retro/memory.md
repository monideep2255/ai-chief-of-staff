# System-retro operational memory

Running log of lessons learned from past runs. Separate from evals (static checks) and from central auto-memory (user-level).

## Lessons

| Date | Lesson | Source |
|------|--------|--------|
| 2026-06-02 | Count drift (hardcoded counts in docs vs actual file counts) is the most common retro finding, flagged in 3 of 4 retros. os-maintain Phase 6 now handles this, but verify it ran. | Retro cycles 9-12 |
| 2026-06-02 | During planned leave or extended time away, suppress work dormancy flags. The constraint is the leave itself, not a productivity gap. | Retro cycle 12 |
| 2026-06-04 | Two-phase Curator pre-filter (deterministic staleness bucket before LLM review) reduces LLM decision surface. Only stale/archive-eligible skills go to LLM review. | Hermes pattern adoption |
| 2026-06-04 | Run validate_skill_rules.sh during the skills audit phase. It catches orphaned dependencies and missing rule references faster than manual scanning. | Role-specific-plugins pattern |
| 2026-07-18 | Running the 6 area audits as parallel read-only sub-agents (return scored proposals, apply fixes centrally) avoids write conflicts and is much faster than a serial audit. Cycle 18. | Cycle 18 |
| 2026-07-18 | When closing a recurring count gap, extend the count-verification script AND run it during application: this cycle the extended script immediately caught a wrong count before it shipped. Automated guards pay off the same session. | Cycle 18 |
| 2026-07-25 | A rule has two identity keys: the filename stem and the frontmatter `name:`. They legitimately differ (`npm-security-check.md` carries `name: supply-chain-security`). Any cross-reference or reverse-edge checker must resolve both, or it reports false positives. Cycle 19 lost time to 7 reported false edges that were really 4. | Cycle 19 |
| 2026-07-25 | Skills carry no glob scope. `grep -l "^globs:" .claude/skills/*/SKILL.md` returns 0, because skills are invoked by name and only rules are glob-loaded. A finding of the form "component X was not extended to glob Y" is a category error when X is a skill. Cycle 19 raised one and had to falsify it. | Cycle 19 |
| 2026-07-25 | Verify this skill's own Phase 1 pre-filter output before trusting it. Two commands were wrong for every prior cycle: the `author: agent` grep matched this skill's own prose about the pattern, and the staleness command interleaved commit-message text with file paths because `git log --name-only` prints message bodies. Both fixed; earlier cycles were scored partly on bad pre-filter data. | Cycle 19 |
| 2026-07-25 | Content can land mid-retro from a concurrent writer. Cycle 19 corrected the same count three times and failed the count check twice against a moving target. Fix to current disk truth, re-run once, and state the timestamp in the report rather than chasing. Re-verify after the writer's commit lands, since it may close findings on its own. | Cycle 19 |
| 2026-07-25 | Three instrument-level false positives in one cycle. Record falsified findings in the report instead of deleting them: the pattern of what the audit's own tools get wrong is more durable than any single finding. | Cycle 19 |

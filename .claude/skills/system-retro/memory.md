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

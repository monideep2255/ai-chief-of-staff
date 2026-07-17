# OS improvements

This file tracks improvements applied to the system itself: a rule, skill, agent, hook, or config change adopted from some source, such as a repo dive, a retro, a daily-use insight, or an external article.

It is distinct from DECISIONS.md, which logs heavyweight architectural choices with alternatives weighed. Most improvements here are smaller pattern adoptions, not architecture decisions. A single change can warrant a row in both files, but most only need this one.

## Applied

| # | Proposal | Source | Proposed | Applied | What changed |
|---|----------|--------|----------|---------|--------------|
| 1 | Parallel-first rule | Daily-use insight: two independent research tasks for the Atlas rollout were run sequentially when nothing linked them | 2026-03-02 | 2026-03-02 | Created `.claude/rules/parallel-first.md`. Before starting any multi-part task, check whether subtasks share a write target or depend on each other's output. If not, dispatch them together instead of one after another. |
| 2 | Self-eval loop pattern | Daily-use failure: a Meridian status update shipped with a wrong deadline that a second reader would have caught in seconds | 2026-03-14 | 2026-03-14 | Created `.claude/rules/self-eval-loop.md`. For any substantial written output, a second pass with fresh context grades the draft against a short pass or fail checklist before it ships. The same agent that wrote the draft does not get to be the only one who signs off on it. |
| 3 | Memory provenance tags | Daily-use insight: two saved memories about the Atlas launch date disagreed, and neither carried a source, so it was unclear which one to trust | 2026-03-20 | 2026-03-20 | Added a provenance tag to every memory file: documented decision, documented research, stakeholder verbal, or personal read. When two memories conflict, the higher-trust tag wins unless the lower-trust one is more recent and explicitly supersedes it. |
| 4 | Sandbox-diagnosis rule | Daily-use failure: a push to the Atlas repo kept failing and got fixed by disabling the sandbox each time, until it turned out the remote was set to an SSH address the sandbox could never reach | 2026-04-02 | 2026-04-02 | Created `.claude/rules/sandbox-diagnosis.md`. Before disabling the sandbox, classify the failure as a blocked file write, a blocked web address, or a protocol mismatch. Switching the Atlas remote from SSH to HTTPS fixed the push with the sandbox left on. |
| 5 | Book-inventory-check gate | Retro finding: six learning books had been generated for the Meridian program and only one had been read past its first chapter | 2026-04-18 | 2026-04-18 | Tightened `.claude/rules/book-inventory-check.md` so it lists every existing book with its chapter count and asks for explicit confirmation before generating a new one. The bottleneck was reading time, not a shortage of material, so the gate now blocks new books by default rather than nudging. |
| 6 | Decision logging split from improvement logging | Daily-use confusion: a tool choice for the Atlas data layer got written into the same file as a rule tweak, and the two were hard to tell apart later | 2026-05-09 | 2026-05-09 | Created `.claude/rules/decision-logging.md` to own heavyweight, hard-to-reverse choices (architecture, tool selection, process changes) in DECISIONS.md, and clarified that this file, OS_IMPROVEMENTS.md, owns the smaller pattern adoptions. Most changes now go to one file, not both. |

## Proposed (not yet applied)

| # | Proposal | Source | Proposed | What it would change |
|---|----------|--------|----------|----------------------|
| - | Dependency tracking on rule files | Daily-use observation: a rule was edited without checking which skills referenced it, and one of them broke | 2026-05-15 | Add `depends_on` and `depended_by` fields to rule frontmatter so an edit to one file surfaces every file that needs a matching update. |
| - | Exit checklists on multi-step skills | Retro finding: two of the longer Meridian skills have no closing checklist, so a run can stop partway and still look finished | 2026-05-22 | Add a short exit checklist to each multi-step skill, naming the concrete artifacts a run must produce before it counts as done. |

*Last updated: example date, replace with your own*

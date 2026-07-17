# Decisions

Historical record of non-trivial choices made while building this repo. Newest first. Don't edit or delete rows, this is append-only.

A decision belongs here only if it fits one of three categories: architecture (new folders, structural patterns), tool selection (choosing one library, format, or service over another), or process changes (new rules, new skill steps, changes to how the system operates). Content decisions, obvious defaults, and one-off picks that someone could undo in five minutes don't qualify. See `.claude/rules/decision-logging.md` for the full test.

Note: this repo is a sanitized portfolio example. Project names (Atlas, Meridian) are fictional, and the rows below are illustrative rather than a real history.

## Log

| Date | Decision | Alternatives considered | Why |
| --- | --- | --- | --- |
| 2026-06-02 | Store agent memory as markdown files with frontmatter instead of a database | SQLite with a query layer, a vector store, a flat JSON log | Markdown stays human-readable and diffable in git, so anyone maintaining the Atlas project can review what the agent remembers without a query tool. A database would need its own backup and migration story for a benefit (structured queries) that this repo doesn't need at its current scale. |
| 2026-05-20 | Symlink external reference repos into `Reference-repos/` instead of vendoring their code | Copy the code in directly, submodule each repo, skip external references entirely | Symlinking keeps this repo's own git history clean, since the referenced repos (used for deep-dive analysis on Meridian's tooling choices) aren't meant to be edited here. A submodule adds checkout complexity for a portfolio repo with no CI. Vendoring would bloat the repo with code that isn't ours to maintain. |
| 2026-05-14 | Trim hooks, automation scripts, and cron workflows out of this portfolio version | Ship the full hook and script set as-is, replace them with stub placeholder files | Hooks and scripts are tied to specific machine paths and Meridian-specific automation, so they'd either leak internal detail or sit as dead weight nobody could run. Keeping only rules, skills, and agents shows the reasoning behind the system without shipping code that only worked in one specific environment. |
| 2026-05-08 | Model the growth system around four fixed pillars instead of one flat list of habits | A single running list of goals and habits, a calendar-only tracking system | A flat list grows without bound and loses shape as items pile up. Four pillars force every new habit or goal to justify which pillar it serves, which keeps the system legible as it grows and makes it obvious when a pillar is neglected. |
| 2026-05-03 | Rebuild the board skill as an empty advisor template instead of excluding it from the portfolio | Drop the skill entirely, ship it pre-filled with fictional advisor personas | The board skill's value is the discovery-then-advise structure, not the specific advisors in it. An empty template demonstrates the mechanism honestly and lets a reader fill in their own roster, where a pre-filled fictional cast would either look hollow or misrepresent how the skill is actually used. |
| 2026-04-27 | Split behavioral rules into glob-scoped files under `.claude/rules/` instead of one monolithic rules file | A single CLAUDE.md with every rule inline, one giant rules.md loaded on every session | A monolithic file loads every rule on every session regardless of relevance, which wastes context on rules that don't apply to the current task. Glob-scoped files load only when a matching file type or task is in play, so a meeting-notes rule never loads during a code review and vice versa. |

*Last updated: example date, replace with your own*

# Changelog

Full history of changes to this repository. Newest entries at top. Dates use example week labels since this is a demonstration repo, not a real timeline, replace them with your own dates once you start using it for real.

| Date | Change |
| ---- | ------ |
| Example week 11 | Added SYSTEM_OVERVIEW.md, a full reference covering every rule, skill, agent, and folder, plus the session lifecycle and the self-maintenance loop. Linked into the depended_by chains across CLAUDE.md, AGENTS.md, and README.md so downstream docs stay current. |
| Example week 10 | Added GETTING_STARTED.md, a first-session walkthrough covering folder layout, the memory system, and which skills to try first on an Atlas or Search task. Also created .agents/skills/, portable copies of three tool-agnostic skills so any coding agent can read them, not only this one. |
| Example week 9 | Created DEPENDENCIES.md, EXTENSIONS.md, DECISIONS.md, and OS_IMPROVEMENTS.md, the cross-reference layer the system had been missing. Paired with a final rule batch of 7 rules, including os-improvement-logging, taking the rule count from 26 to 33. |
| Example week 8 | Tightened the file-protection rule after a gap: a skill had silently overwritten an existing file in Learning/deep-dives/ instead of asking first. Added an explicit ask-state for edits to any existing substantial document. |
| Example week 8 | Added the first Learning/deep-dives/ example, a first-principles dive on the Atlas relevance-ranking pipeline. Established the fixed shape later dives reuse: define, collapse to structure, map honestly, diagram, worked example, skepticism, what it means for you. |
| Example week 7 | Built the memory/ folder: four types, user, feedback, project, and reference, plus a MEMORY.md index. Backfilled the first 9 memory files from earlier Meridian sessions, covering the Atlas relevance work, the KG pilot, and the AI cohort program. |
| Example week 7 | Created Work/example-project/, a worked walkthrough of a full Atlas feature cycle: kickoff notes, a decision log entry, a check-in note, and a shipped change. Gives the folder pattern a concrete reference instead of only a description. |
| Example week 6 | Completed the 8-agent roster: added action-planner, socratic, git-sync, docs-sync, and code-reviewer alongside the first three. Each agent triggers on magic words rather than an explicit invocation, so common requests route to the right agent on their own. |
| Example week 5 | Built out all 26 skills across three batches: research digest and book-builder skills first, then ingestion, conference-note processing, repo deep dives, and weekly self-audit, then evaluation, handoff, systems mapping, and prompt optimization last. |
| Example week 4 | Added the first 3 agents, meeting-notes, first-principles, and objective-review, bringing structured note formatting and honest review into the workflow for the first time. |
| Example week 3 | Second rule batch: 14 more rules covering git workflow, file naming, dependency tracking, parallel-first execution, anti-rationalization, and workflow-and-reference-awareness. Rule count 12 to 26. |
| Example week 1 | Initial repo scaffold created: .claude/ folder with agents, skills, and rules subdirectories, plus placeholder README.md, CLAUDE.md, and AGENTS.md. First rule batch added 12 always-on rules, file-protection, writing-style, communication-style, response-calibration, doc-construction, pause-before-acting, clarify-before-drafting, preserve-your-thinking, boil-the-lake, session-greeting, system-design-patterns, and attack-the-constraint, establishing the behavioral baseline before any skill or agent existed. |

*Last updated: example date, replace with your own*

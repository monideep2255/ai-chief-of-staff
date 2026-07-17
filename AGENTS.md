# AGENTS.md

Instructions for any AI agent working in this repository. Mirrors [CLAUDE.md](CLAUDE.md), that file is for Claude Code specifically, this file is for all other AI agents (Cursor, Windsurf, Copilot, etc.).

> **Before making changes:** check [DEPENDENCIES.md](DEPENDENCIES.md) to understand what cascades. Use the deletion checklist when removing anything.

**This is primarily a framework repo** - no build commands, tests, or deployments, with one exception: `Work/example-project/` is a stand-in for a real software project (its own conventions, its own production rules). Treat that one folder as a software project; everything else is rules, skills, agents, and example documentation that make up the system itself.

---

## Current focus

*Updated: example date, replace with your own*

This section is where the system tracks what you are actually working on right now, so every agent session opens with the same picture instead of you re-explaining it. The example below is fabricated, to show the shape.

| Project | Status |
|---------|--------|
| Atlas | Active - the priority going forward |
| Knowledge graph (KG) | Winding down |
| AI cohort | Active - part time teaching commitment |
| Search | Paused, pending a resourcing decision |

> Goals, metrics, and guardrails: [GOALS.md](GOALS.md)

---

## Sub-agents

Use **magic words** to activate instantly. These are defined in `.claude/agents/` but the concepts apply to any AI agent.

| Agent | Magic words | Purpose |
|-------|-------------|---------|
| **meeting-notes** | `meeting notes`, `format notes`, `I had a meeting` | Format raw notes into structured documentation |
| **first-principles** | `what is`, `explain`, `how does X work`, `teach me` | Explain technical concepts simply |
| **action-planner** | `plan`, `action items`, `todos`, `prioritize` | Convert discussions into prioritized to-do lists |
| **socratic** | `should I`, `help me decide`, `I'm stuck`, `brainstorm` | Ask clarifying questions before giving advice |
| **objective-review** | `review this`, `is this good`, `am I missing` | Provide critical, honest feedback (not agreement) |
| **git-sync** | `sync`, `push`, `pull`, `push to github` | Handle GitHub push/pull operations |
| **docs-sync** | `update docs`, `sync docs`, `refresh docs` | Update standard documentation files |
| **code-reviewer** | `review this code`, `code review`, `check this PR` | Review Atlas Django code for conventions and accessibility |

> Full details: [.claude/README.md](.claude/README.md)

---

## Skills

| Skill | Purpose | Invocation |
|-------|---------|-----------|
| **cs-research** | Fetch AI/ML papers from arXiv | `/cs-research` |
| **biomedical-research** | Fetch clinical papers from PubMed | `/biomedical-research` |
| **prompt-optimizer** | Token efficiency analysis and optimization | `/optimize [your prompt]` |
| **book-builder-hard-skills** | Generate a first-principles learning book on any technical topic. Output path: `Learning/hard-skills/<topic>/` | `/book-builder-hard-skills <topic>` |
| **book-builder-soft-skills** | Generate a practice-oriented soft skills book (frameworks, scripts, scenarios, self-assessments). Output path: `Learning/soft-skills/<topic>/` | `/book-builder-soft-skills <topic>` |
| **book-builder-from-sources** | Synthesize your own markdown source files into a structured learning book. Output path: `Learning/local-sources/<topic>/` | `/book-builder-from-sources <topic> --source <path>` |
| **forge** | A daily self-improvement gym: rotating coaches, progressive difficulty exercises, portfolio artifacts. Variable time (15-60 min). | `/forge`, `/forge --quick`, `/forge --deep`, `/forge --weekly` |
| **board** | A personal board of directors: brutally honest multi-advisor review, template driven, you fill in your own advisors | `/board [situation or question]` |
| **eval-harness** | Evaluation framework for AI features (pass@k metrics, acceptance criteria) | Read skill when building AI features |
| **repo-dive** | Clone an external repo, symlink it, generate deep-dive analysis docs | `/repo-dive <github-url>` |
| **os-maintain** | Auto-maintain downstream docs after system component changes; scaffold new project repos; keep a genericized portfolio copy in sync | `/os-maintain`, `/os-maintain --new-repo <name>`, `/os-maintain --tag` |
| **ship** | Sync docs then push to GitHub (runs docs-sync then git-sync) | `/ship` |
| **wiki-lint** | Keep reference folder README indexes in sync with doc frontmatter | `/wiki-lint`, `/wiki-lint --folder "name"`, `/wiki-lint --report` |
| **system-retro** | Weekly self-improvement loop: the system audits itself, finds gaps, proposes and applies fixes | `/system-retro`, `/system-retro --quick`, `/system-retro --deep`, `/system-retro --focus AREA` |
| **ingest-workflows** | Process research exports from an inbox folder into structured workflow and reference docs | `/ingest-workflows` |
| **ingest-conference** | Process conference session notes into structured conference-notes documentation | `/ingest-conference`, `/ingest-conference --granola` |
| **web-research** | Research-grade web search plus clean URL scraping, used instead of raw search for any research task | `/web-research <query or URL>` |
| **systems-map** | Map any complex system into 8-12 visual building blocks through structured conversation and iterative refinement. Output path: `Learning/visual-synthesis/<topic>/` | `/systems-map <topic>` |
| **bossman-mode** | Autonomous execution after architecture is agreed: orchestrator, researcher, sub-planners, parallel builders, single judge, test writer | `/bossman`, `/bossman --phase N`, `/bossman --status`, `/bossman --stop` |
| **checkin-notes** | Process raw check-in notes into structured meeting notes plus prioritized action items, then auto-ships | `/checkin-notes`, `/checkin-notes <person>` |
| **first-principles** | Explain technical concepts using first-principles thinking | `explain X`, `what is X`, `how does X work` |
| **objective-review** | Critical, honest feedback instead of agreement and encouragement | `review this`, `is this good`, `am I missing something` |
| **socratic-questioning** | Arrive at truth through systematic questioning before providing answers | `help me decide`, `should I`, `I'm stuck` |
| **handoff** | Compact the current session into a copy-pasteable handoff so a fresh agent with zero memory can continue the work | `/handoff`, or "write a handoff", "context is getting full" |
| **yt-learn** | Turn a YouTube video into concrete upgrades to your system and knowledge without watching it | `/yt-learn <url>`, `--full`, `--lite`, `--map`, `--keep-transcript` |
| **deep-dive** | First-principles deep dive on a document, URL, or bare topic, in the same 9-move shape as repo-dive but for non-repo sources. Output path: `Learning/deep-dives/<topic>/` | `/deep-dive <file, url, or topic>` |

> Skill definitions: [.claude/skills/](.claude/skills/)
> Growth system overview: [GROWTH_SYSTEM.md](GROWTH_SYSTEM.md)

### Portable skills (.agents/skills/)

Three skills are tool-agnostic and can have canonical copies in `.agents/skills/` (readable by any coding agent, not just Claude Code): `first-principles`, `objective-review`, `socratic-questioning`. If you set this up, the `.claude/skills/` copies point to the `.agents/` canonical versions via `canonical_copy` in frontmatter. `web-research` stays Claude-only where it depends on built-in search/fetch tools.

---

## Plugins and MCP servers

This example setup assumes a small number of general dev-workflow plugins and MCP servers for external tool access. Fork this repo and wire up whichever ones you actually use. Full inventory pattern and usage guide: [EXTENSIONS.md](EXTENSIONS.md)

---

## Communication preferences

Think from first principles. Ask ONE question at a time. Short sentences, active voice, no buzzwords.

Always read before major interactions:
- [.claude/skills/first-principles/SKILL.md](.claude/skills/first-principles/SKILL.md)
- [.claude/skills/socratic-questioning/SKILL.md](.claude/skills/socratic-questioning/SKILL.md)
- [.claude/skills/objective-review/SKILL.md](.claude/skills/objective-review/SKILL.md) - for review/feedback tasks

---

## File naming conventions

| Type | Format | Example |
|------|--------|---------|
| Meeting notes (simple) | `Month_Day.md` | `January_06.md` |
| Meeting notes (numbered) | `{number}_Meeting:{topic} {Month} {Day}.md` | `2_Meeting:technical_refinement_January_20.md` |
| Meeting notes (person) | `{number}_Meeting_{Person}_{Month}_{Day}.md` | `2_Meeting_Advisor_January_22.md` |
| Meeting prep | `Prep_for_{Month}_{Day}.md` | `Prep_for_January_20.md` |
| Explanations | `Concept_explained.md` | `Atlas_project_explained.md` |
| Decisions | `Topic_decision.md` | `Database_choice_decision.md` |
| Questions | `Questions_for_X.md` | `Questions_for_first_WG_meeting.md` |
| Discussion/insight | `Topic_description_Month_Day.md` | `AI_as_programming_language_discussion_March_20.md` |

---

## Meeting notes format

Nested bullet points. Always include an action items section.

```markdown
- Meeting notes
    - Topic 1
        - Sub-point with details
    - Topic 2
        - Discussion point
    - Action items:
        - Specific task 1 (owner, deadline)
        - Specific task 2
```

> Style reference: [Meetings/Example_meeting_January_06.md](Meetings/Example_meeting_January_06.md), if you keep one

---

## Critical rules

> **Claude Code users:** these rules also exist in `.claude/rules/` with glob-based conditional loading.

- **Ask ONE question at a time** - never batch. Wait for the answer before asking the next.
- Don't delete files or folders. Ask the user and wait for confirmation first.
- Don't create new files unnecessarily - prefer editing existing documentation.
- Don't use corporate jargon or vague suggestions ("consider", "look into").
- Don't add build/test commands - this is a framework repo, not a software project (except `Work/example-project/`).

---

## Git workflow

Work directly on `main`. Clear, descriptive commit messages. No formal PR process.

Gitignore whatever personal or sensitive folders you add for your own use (a scratch folder, a calendar sync, private documents).

---

## Quick start

- [ ] Check **Current focus** above: what are you working on right now?
- [ ] Check [GOALS.md](GOALS.md) for goals, metrics, and guardrails
- [ ] Read **Project context** below for the fabricated example project used throughout this repo
- [ ] Look at [Work/example-project/](Work/example-project/) for style reference
- [ ] Use sub-agent patterns when magic words appear in a request
- [ ] Check [EXTENSIONS.md](EXTENSIONS.md) for plugins, MCP servers, and how all layers connect
- [ ] Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for the full granular system reference

If you are setting this up for the first time, start with [GETTING_STARTED.md](GETTING_STARTED.md) instead.

---

## Project context

*This section provides additional context that non-Claude-Code agents need. Claude Code gets this from its `.claude/` configuration.*

### Who is this for?

Anyone in a hybrid technical/product role who wants an AI agent to act as a chief of staff: someone tracking projects, drafting documents, holding a memory of decisions and feedback, and applying consistent rules across every session. The example projects below (Atlas, KG, AI cohort, Search) are fabricated stand-ins to show the pattern.

### Example projects

| Project | Time | Location | Key document |
|---------|------|----------|-------------|
| Atlas (example web platform) | Majority of core hours | [Work/example-project/](Work/example-project/) | Fabricated, replace with your own |
| Knowledge graph (example) | Partial | Fabricated, replace with your own | - |
| AI cohort (example teaching commitment) | Part time | Fabricated, replace with your own | - |
| Search (example, paused) | Paused | TBD | - |

> Full file tree: [README.md](README.md) | Change history: [CHANGELOG.md](CHANGELOG.md)

---

*Last updated: example date, replace with your own*

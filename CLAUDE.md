# CLAUDE.md

Claude Code specific instructions for this repository. For full project context, read [AGENTS.md](AGENTS.md).

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

---

## Sub-agents

Use **magic words** to activate instantly. Claude auto-selects or you can invoke explicitly.

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

→ Full details: [.claude/README.md](.claude/README.md)

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

→ Full details: [.claude/README.md](.claude/README.md)
→ Growth system overview: [GROWTH_SYSTEM.md](GROWTH_SYSTEM.md)

---

## Plugins and MCP servers

This example setup assumes a small number of general dev-workflow plugins and MCP servers for external tool access. Fork this repo and wire up whichever ones you actually use. Full inventory pattern and usage guide: [EXTENSIONS.md](EXTENSIONS.md)

---

## Rules

Behavioral rules are in `.claude/rules/` with glob-based conditional loading:

| Rule | Scope | What it enforces |
|------|-------|-----------------|
| `communication-style` | Always | First-principles, one question at a time, no jargon, read skills before major interactions |
| `response-calibration` | Always | Plain first-principles language in chat, answer first, right-sized replies, no preamble or filler |
| `file-protection` | Always | No deletion without asking, no unnecessary files, framework repo only |
| `meeting-notes-format` | `Meetings/**` | Nested bullets, action items section |
| `file-naming` | Always | Naming conventions for all document types |
| `git-workflow` | Always | Work on main, clear commits, gitignored paths |
| `boil-the-lake` | Always | When AI makes a task cheap, do it 100% - completeness over shortcuts |
| `session-greeting` | Always | First response shows session summary (focus, last 3 commits, system updates) |
| `writing-style` | Always | No em dashes, sentence case headings, no bold, no LLM brand names |
| `book-inventory-check` | `Learning/**` | Show book inventory before generating new books |
| `pdf-docx-conversion` | `**/*.pdf`, `**/*.docx` | Ask before converting PDFs/DOCX, verify content preservation |
| `dependency-tracking` | Always | Every component declares `depends_on` and `depended_by` in frontmatter |
| `pause-before-acting` | Always | Before executing, check if rules apply and if clarification is needed first |
| `system-design-patterns` | `.claude/agents/**`, `.claude/rules/**`, `.claude/skills/**` | Three-state permissions, snapshot before mutate, specialize by tool access, output truncation |
| `attack-the-constraint` | Always | Identify the bottleneck before optimizing: is it time, skill, clarity, access, or tooling? |
| `decision-logging` | Always | Log non-trivial decisions to DECISIONS.md when choosing between alternatives that affect future work |
| `os-improvement-logging` | Always | Log every adopted system improvement to OS_IMPROVEMENTS.md |
| `parallel-first` | Always | Before multi-part tasks, check if subtasks are independent and can run in parallel; verify every dispatched agent produced its expected output |
| `npm-security-check` | `**/package.json`, `**/requirements*.txt`, `**/.mcp.json` | Before installing or recommending any package, run supply chain security checks |
| `preserve-your-thinking` | Always | Claude is the sparring partner, not the answer machine. Ask what you think first; stress-test your position |
| `clarify-before-drafting` | Always | Run clarification before writing any substantial document (3+ sections, external review) |
| `doc-construction` | Always | Build substantial docs with first-principles structure, table of contents, mermaid diagrams, simple language |
| `bossman-mode` | `/bossman` skill only | Autonomous execution overrides: suspends deliberation rules while bossman mode is active |
| `workflow-and-reference-awareness` | `Reference/**` | Lookup tables for matching requests to your own workflow and reference docs, if you keep one |
| `atlas-production-standards` | `Work/example-project/**` | Security and hardening non-negotiables for production Python/Django code |
| `atlas-production-examples` | `Work/example-project/**` | Before/after security code pairs: SQL injection, XSS, URL encoding, secrets in logs, open redirect |
| `ai-security-standards` | Always | AI security non-negotiables for all code and agent work: treat AI output as untrusted, sandbox execution, protect secrets, human approval for high-risk actions |
| `anti-rationalization` | Always | Block the model from rationalizing away steps in multi-step skills |
| `memory-provenance` | Always | Tag source quality on memories so future sessions weight conflicting memories correctly |
| `self-eval-loop` | Always | For substantial output, a first agent produces and a second grades with fresh context against pass/fail criteria |
| `goal-contracts` | Always | Before any autonomous or multi-step run, write a contract: done-when, verify, output, constraints, blocked-stop |
| `sandbox-diagnosis` | Always | Before disabling the sandbox for a failed command, classify the failure and apply the durable fix instead |
| `agent-first-default` | Always | Default to agent-first-draft on reversible tasks, stay hands-on on irreversible ones |
| `ship-clean-no-bait` | Always | Once work is declared done it must be done and clean: no trickling new findings after done, no rage-bait or click-bait closers |

---

## Quick start

- [ ] Check **Current focus** above: what are you working on right now?
- [ ] Check [GOALS.md](GOALS.md) for goals, metrics, and guardrails
- [ ] Read [AGENTS.md](AGENTS.md) for full project context
- [ ] Look at [Learning/deep-dives/](Learning/deep-dives/) and [Work/example-project/](Work/example-project/) for style reference
- [ ] Use sub-agents when magic words appear in a request
- [ ] Check [DEPENDENCIES.md](DEPENDENCIES.md) before making changes: know what cascades
- [ ] Check [EXTENSIONS.md](EXTENSIONS.md) for plugins, MCP servers, and how they connect
- [ ] Read [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) for the full granular system reference

If you are setting this up for the first time, start with [GETTING_STARTED.md](GETTING_STARTED.md) instead.

---

*Last updated: example date, replace with your own*

---
name: os-maintain
author: human
description: "Auto-maintain downstream docs after system component changes. Default mode: walk depended_by + docs-sync routing, update all indexes. --new-repo mode: scaffold a new project repo directly on Desktop. --tag mode: audit scope coverage. TRIGGER when user says 'os-maintain', 'update indexes', 'new repo', 'scaffold repo', creates/modifies/deletes a rule/skill/agent, or when the system needs doc count verification. Also trigger on 'check scope tags' or 'what would export'. DO NOT TRIGGER for content-only changes (use /ship) or code changes in external repos."
scope: project
user_invocable: true
agent: true
model: sonnet
argument-hint: "[path/to/file] [--new-repo <name>] [--tag]"
depends_on:
  - .claude/agents/docs-sync.md
  - DEPENDENCIES.md
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - CHANGELOG.md
  - .claude/WHATS_NEW.md
  - README.md
  - .claude/scripts/verify_counts.sh
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# /os-maintain

Auto-maintain all downstream documentation when system components change. Three modes:

- `/os-maintain` - detect changes, walk dependencies, update all indexes
- `/os-maintain .claude/rules/my-rule.md` - target a specific file
- `/os-maintain --new-repo <name>` - scaffold a new project repo directly on Desktop
- `/os-maintain --tag` - audit scope tag coverage

---

## Default mode: maintenance cycle

### Phase 0: snapshot

Log the revert point before touching anything:

```
git rev-parse HEAD
git status --short
```

Print: `Snapshot: [hash] - [N] staged, [M] unstaged`

### Phase 1: detect what changed

**If argument is a file path:** use that path. Check `git status --short` for change type:
- `A` or `??` = new component
- `M` = modified component
- `D` = deleted component

**If no argument:** run `git diff --name-only HEAD~1` (or `git status --short` for uncommitted).
Filter to `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.claude/hooks/` only.

If no system component files changed: print "No system component changes detected. Use docs-sync for content changes." and stop.

### Phase 2: read metadata

**New or modified component:** read the file. Extract from frontmatter:
- `name`
- `description`
- `depended_by` (list of files to update)
- `depends_on`
- `scope` (portable or project)

**Deleted component:** file is gone. Use `DEPENDENCIES.md` deletion checklist. Look up the component type (rule, skill, agent, hook) and get the canonical list of downstream files.

### Phase 3: build work list

Combine two sources:

1. **depended_by field** from the changed component's frontmatter
2. **docs-sync routing table** - read `.claude/agents/docs-sync.md` and apply its routing table to the changed path

Deduplicate. Always include CHANGELOG.md.

For deletions: also include everything in DEPENDENCIES.md deletion checklist for that type.

### Phase 4: parallel read

Read every file on the work list in a SINGLE message with parallel Read calls.

### Phase 5: parallel edit

Update all stale files in a SINGLE message with parallel Edit calls. Surgical replacements only.

**New component:**
- Add row to component tables in CLAUDE.md, AGENTS.md, .claude/README.md
- Add to directory tree in .claude/README.md
- Add WHATS_NEW entry at top (drop oldest if > 5)
- Add CHANGELOG entry at top
- Update DEPENDENCIES.md component table

**Modified component:**
- Update changed rows/cells in tables
- Add WHATS_NEW entry if substantive (new capability, behavior change)
- Add CHANGELOG entry

**Deleted component:**
- Remove row from all component tables
- Remove from directory tree
- Add WHATS_NEW entry noting removal
- Add CHANGELOG entry
- Remove from DEPENDENCIES.md

**Bidirectional sync:** after updating CLAUDE.md or AGENTS.md, verify these three tables match between them:
1. Current Focus
2. Sub-agents
3. Skills

### Phase 6: count verification

Do not eyeball counts from a memorized list of files. Run the script. It greps every live index doc (CLAUDE.md, AGENTS.md, README.md, SYSTEM_OVERVIEW.md, EXTENSIONS.md, .claude/README.md) for rule/skill/agent/hook counts in prose, tables, "Name (N)" labels, and mermaid count nodes, then diffs against the on-disk count. This replaces the old two-file checklist, which silently missed count locations the author had not listed (it missed SYSTEM_OVERVIEW's mermaid diagrams and ToC anchor on June 22).

```bash
bash .claude/scripts/verify_counts.sh
```

Exit 0 means all counts match. Exit 1 prints each drifted file and the offending text. Fix every flagged line, then re-run until exit 0. These are trivial edits that prevent count drift (the most common retro finding, flagged 3 of 4 retros).

The script covers the four component totals. It does not check mermaid count nodes or ToC anchors that the keyword patterns miss, so also eyeball these by hand in SYSTEM_OVERVIEW.md when any count changed: the Layer-1 and Layer-2 mermaid nodes (`H["N hook scripts"]`, `R["N behavioral rules"]`), the section headers (`### 3a. Rules (N)`), and the matching ToC anchors (`#3a-rules-N`). The anchor must match the header number or the link breaks.

For counts the script does not cover (workflows, AI PM references), check by hand:

```bash
ls Reference/Agent_workflows/*.md | wc -l   # workflows
ls Reference/AI_PM_reference/*.md | wc -l   # AI PM references
```

Also update EXTENSIONS.md last-updated date if any count was changed.

### Phase 7: dependency metadata check

If new component: verify it has `depends_on` and `depended_by` in frontmatter. If missing, flag it in report (don't edit the file yourself - the author fills in correct values).

### Phase 7.5: OS improvement logging check

If the component change being synced was an adopted improvement (a rule/skill/agent/hook/config change sourced from a repo dive, retro, board session, ingested article, or daily-use insight), verify it has a row in `OS_IMPROVEMENTS.md`. If missing, append one to the "Applied" table per `os-improvement-logging.md` (number, proposal, source, proposed date, applied date, what changed) and update the "Last updated" date. Skip for pure content edits and for routine index sync with no behavior change.

### Phase 8: report

```
os-maintain complete
Snapshot: [hash]
Scenario: [new/modified/deleted]
Component: [name] ([type]) at [path]

Files updated:
- [path]: [what section changed]

Files already current (skipped):
- [path]

Flags:
- [missing frontmatter, sync issues, anomalies]

Next: /ship to commit and push
```

### CHANGELOG entry format

Insert at top of table (newest first):
```
| [YYYY-MM-DD] | [Created/Updated/Deleted] `[name]` ([type]): [one sentence]. |
```

### Key rules

1. Surgical only - never rewrite a whole file
2. Parallel reads and writes - no sequential file-by-file
3. Routing table lives in docs-sync - read it, don't duplicate
4. CHANGELOG always gets an entry for system component changes
5. Three tables must match between CLAUDE.md and AGENTS.md
6. Don't push - /ship handles that
7. Don't invent content - only document what actually exists
8. Scope tag is metadata, not behavior - don't skip updates based on scope

---

## --new-repo mode: scaffold a new project repo

Directly create a new project repository on the Desktop. No intermediate export folder.
Target: `~/your-projects-folder/<name>/`

Use `dangerouslyDisableSandbox: true` for all Bash operations that write outside this repo's directory.

### Step 1: scan scope tags

Read frontmatter of every file in:
- `.claude/rules/*.md`
- `.claude/skills/*/SKILL.md` and `.claude/skills/*.md`
- `.claude/agents/*.md`

Do this in a single parallel Read batch. Extract `scope:` field. Build portable/project lists.

Report:
```
Scan complete:
- Rules: N portable, N project, N untagged
- Skills: N portable, N project
- Agents: N portable, N project

Default selection:
  Rules:  [all portable + bossman-mode]
  Skills: [first-principles, socratic-questioning, objective-review, bossman-mode]
  Agents: [first-principles, socratic, objective-review, action-planner, docs-sync, git-sync]

Customizations? (add/remove specific components, or say "use defaults")
```

Wait for confirmation and any additions/removals before proceeding.

### Step 2: collect project context

Ask (one message, all questions together):

1. Stack: what language/framework? (Python, TypeScript, Django, FastAPI, etc.)
2. Reference docs: which folders or files from Projects/, Reference/, Reference-repos/ to copy into docs/?
3. Symlinks: any Reference-repos deep-dives to symlink into reference/?
4. Project structure: what top-level folders? (or say "infer from stack")
5. Workflows: which Agent_workflows/ files are relevant? (or "build-relevant defaults")
6. Will this repository ever be public? If yes, copy `.claude/rules/public-repository-privacy.md` into the new repository and follow its committing-safely guidance before the first commit.

### Step 3: create repo structure

```bash
REPO="~/your-projects-folder/<name>"

# .claude/ config
mkdir -p "$REPO/.claude/rules"
mkdir -p "$REPO/.claude/skills/<each-skill>"
mkdir -p "$REPO/.claude/agents"

# Project folders (inferred from stack or user-specified)
# Python data engineering template (used for an example data pipeline project):
mkdir -p "$REPO/data-pipelines/{source1,source2,...,shared}"
mkdir -p "$REPO/knowledge-graph/{schema,mappings,merge,loader,tests}"
mkdir -p "$REPO/search-agent/{orchestrator,query_understanding,...}"
mkdir -p "$REPO/api/routes"
mkdir -p "$REPO/mcp-server/tools"
mkdir -p "$REPO/cli"
mkdir -p "$REPO/web-ui/src/components"
mkdir -p "$REPO/eval/{golden_datasets,cq_tests,llm_judge,dashboard}"
mkdir -p "$REPO/docs"
mkdir -p "$REPO/reference"
```

### Step 4: copy .claude/ config

Use Bash cp for rules (sandbox allows writes to `.`):

```bash
cp .claude/rules/<selected>.md $REPO/.claude/rules/
```

Use Write tool (not cp) for skills and agents - sandbox blocks Bash cp to `.claude/` subdirs even in child paths. Read each file first, then Write with cleaned frontmatter:

- Keep: name, description, scope, argument-hint, user_invocable, tools, model, alwaysApply, globs
- Filter depends_on: drop project-specific paths (Work/, Automations/, Forge/, CLAUDE.md, AGENTS.md)
- Reset depended_by: []

### Step 5: copy reference docs and symlinks

```bash
# Copy docs into $REPO/docs/ (flat, no subfolders needed)
cp <selected Meridian docs> $REPO/docs/
cp <selected Reference docs> $REPO/docs/

# Copy selected workflows into $REPO/workflows/
cp <selected workflows> $REPO/workflows/

# Create symlinks for Reference-repos deep-dives
ln -sf "$(pwd)/Reference-repos/<name>-Deep-Dive" "$REPO/reference/<name>-Deep-Dive"
```

Build-relevant workflow defaults (use unless user says otherwise):

- `AI_assisted_PRD_and_build_loop.md`
- `Evals_driven_AI_product_loop.md`
- `Context_graph_decision_agent_setup.md`
- `Multi_agent_openclaw_setup_and_delegation.md`
- `Background_agents_and_parallel_runs.md`
- `LLM_product_feature_design_loop.md`
- `Prototype_first_PM_workflow.md`
- `First_principles_system_redesign_loop.md`
- `LLM_cli_pm_operating_system.md`
- `Zevis_AI_development_workflow.md` (from AI_PM_reference/archive/)

### Step 6: write root files

Write all four in parallel:

**CLAUDE.md** - tailored to the project:

- Current focus table (Phase 1 / what's being built now)
- Architecture overview (systems, input/output boundaries)
- Reference docs table (what's in docs/ and when to read each)
- Build order (phases in sequence)
- Sub-agents table
- Skills table
- Key rules (which of the 14 matter most for this stack)
- Git workflow note
- Cost targets if relevant

**README.md** - open source pitch:

- One-line description
- Status table (system by system)
- Architecture diagram (text)
- Quick start
- Data sources / scope table if applicable
- License

**DECISIONS.md** - pre-seeded with decisions already made:

- Architecture choices discussed during planning
- Stack decisions (why this DB, why this framework)
- Scope decisions (what's included vs deferred)

**.gitignore** - appropriate for the stack:

- Python: `__pycache__/`, `*.pyc`, `venv/`, `dist/`, `.pytest_cache/`
- Node: `node_modules/`, `npm-debug.log*`
- Data files: `*.gz`, `*.xml.gz`, `data/raw/`, `data/ftp_cache/`
- Secrets: `.env` (but NOT `env.example`)
- IDE: `.vscode/`, `.idea/`, `.DS_Store`

**env.example** - named `env.example` (not `.env.example`, blocked by hook):

- All environment variables the project needs, with placeholder values
- Grouped by service (API keys, database, observability, storage)

### Step 7: initialize git and commit

```bash
cd "$REPO"
git init && git branch -m main
git add README.md CLAUDE.md DECISIONS.md .gitignore env.example docs/ .claude/ workflows/
git commit -m "Scaffold <name> repo

[one sentence describing what this project is and what's in the initial commit]"
```

### Step 8: report

```
New repo created: ~/your-projects-folder/<name>/

  .claude/rules/    N files
  .claude/skills/   N files
  .claude/agents/   N files
  docs/             N files
  workflows/        N files
  reference/        N symlinks
  Root files:       CLAUDE.md, README.md, DECISIONS.md, .gitignore, env.example

Initial commit: [hash]

Where to start:
  Open CLAUDE.md -> read the build order -> start Phase 1
```

### Implementation notes

1. No intermediate export folder - write directly to the target repo
2. Use Write tool for `.claude/skills/` and `.claude/agents/` - Bash cp is blocked for `.claude/` subdirs
3. Use Bash cp (dangerouslyDisableSandbox) for rules and docs - faster for bulk file copy
4. dangerouslyDisableSandbox required for all writes outside this repo
5. CLAUDE.md must be tailored to the actual project - not a copy of this repo's CLAUDE.md
6. env.example, not .env.example (hook blocks any path containing `.env`)

---

## --tag mode: audit scope coverage

### Step 1: scan

Read frontmatter of all components in `.claude/rules/`, `.claude/skills/`, `.claude/agents/`.

### Step 2: report

```
Scope tag coverage:

Rules (N total):
  portable: N  [names]
  project:  N  [names]
  untagged: N  [names]

Skills (N total):
  portable: N  [names]
  project:  N  [names]
  untagged: N  [names]

Agents (N total):
  portable: N  [names]
  project:  N  [names]
  untagged: N  [names]

Hooks (N total): all project-specific by design

Untagged components will be skipped by --export.
```

Do not apply tags. Report only.

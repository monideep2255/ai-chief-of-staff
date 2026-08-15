---
name: ingest-conference
author: human
description: "Process conference session notes into Conference-notes/, from either Perplexity exports in inbox subfolders or a Granola folder pull. Use when the user says: /ingest-conference, \"process my conference notes\", \"I just got back from <conference>\", \"pull the sessions from Granola\", \"write up these talks\". Differs from ingest-workflows, which processes YouTube-inbox exports into the reference folders rather than conference sessions."
scope: project
user_invocable: true
agent: true
model: sonnet
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/file-naming.md
  - .claude/rules/file-protection.md
  - .claude/rules/pdf-docx-conversion.md
  - .claude/skills/ship/SKILL.md
  - .claude/skills/wiki-lint/SKILL.md
  - .claude/skills/os-maintain/SKILL.md
  - Conference-notes/README.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - README.md
  - CHANGELOG.md
  - .claude/WHATS_NEW.md
---

# /ingest-conference - process conference session notes into the repo

Two source types are supported. Detect which path applies from the user's trigger phrase:

**Granola path** - user says "pull granola notes", "ingest granola GraphConf", or `/ingest-conference --granola`
**Perplexity path** - user drops files in inbox and says "process conference inbox", "ingest conference notes", or `/ingest-conference`

Do NOT modify the `ingest-workflows` skill. This is a standalone pipeline.

No confirmation pauses. Just do it.

---

## Granola path

Use this when pulling live notes directly from a Granola folder via the MCP server.

### Key rule: preserve content as-is

The user writes Granola notes in a deliberate style. Do NOT apply writing-style transformations (no em dash replacement, no bold removal, no sentence case). Add frontmatter only. The body of the file is the raw Granola summary verbatim.

### Step G1: discover the folder

Call `mcp__granola__list_meeting_folders` to find the folder ID for the target conference (e.g. "GraphConf").

### Step G2: list meetings in the folder

Call `mcp__granola__list_meetings` with the folder ID and a custom date range covering the conference days. Get all meeting IDs and titles.

### Step G3: pull summaries in parallel

Call `mcp__granola__get_meetings` (max 10 per call) to retrieve the `<summary>` content for each meeting. If more than 10 meetings, make multiple calls in parallel.

### Step G4: write files in parallel

For each meeting, write a markdown file to `Conference-notes/<conference>/sources/`:

1. Filename: derived from session title, sentence case with underscores, following `.claude/rules/file-naming.md`
2. Content: YAML frontmatter (see schema below) followed by the raw Granola summary verbatim

Use parallel Write tool calls for all files in a batch. Do not write them sequentially.

### Granola frontmatter schema

Extract all fields from the Granola summary content (title line, speaker name, affiliation, date, session type):

```yaml
---
description: One-line summary of the session (~120 chars)
type: conference-note
conference: GraphConf-2026 | AgentSummit
speaker: Full name(s) extracted from the summary header
speaker_affiliation: Organization(s) extracted from the summary header
session_type: keynote | talk | panel | workshop | lightning | fireside
session_date: YYYY-MM-DD
source: Session title as it appears in the Granola summary
added: YYYY-MM-DD (today)
---
```

### Step G5: downstream sync

Run Steps 3 and 4 from the Perplexity path below (wiki-lint, os-maintain, ship).

---

## Perplexity path

Use this when the user has dropped Perplexity exports into the conference inbox subfolders.

Inbox locations:
- `Reference/YouTube_sourced_workflows_inbox/conferences/graphconf/` → `Conference-notes/GraphConf-2026/`
- `Reference/YouTube_sourced_workflows_inbox/conferences/agentsummit/` → `Conference-notes/AgentSummit/`

### Step 1: convert non-markdown files and delete originals

Scan both inbox subfolders for `.pdf`, `.docx`, `.PDF`, `.DOCX`, and `.html` files.

1. List all non-markdown files found
2. Read each file and convert to markdown in-place (same directory)
3. Apply all Step 2 cleaning rules during conversion
4. Delete the original PDF/DOCX/HTML files immediately after successful conversion
5. Report: "Converted N files, deleted N originals"

### Step 2: clean and place

#### Clean each file

Apply ALL of these transformations to every `.md` file:

1. Strip Perplexity boilerplate - remove `<img>` tags, system prompt blocks, `</output>` closing tags, `<div>` decorative elements, trailing engagement questions
2. Add clean heading - `# Session title in sentence case` as the first line, followed by `Speaker: Name (Affiliation)` on the next line if extracted
3. Replace em dashes - all `—` and `–` become ` - ` (space hyphen space)
4. Replace brand names per `.claude/rules/writing-style.md`
5. Sentence case all headings
6. Reduce bold - keep only genuinely important terms
7. Remove `***` horizontal rules between sections
8. Keep footnote URLs - source attribution stays
9. Add frontmatter using the conference schema below

#### Conference frontmatter schema

```yaml
---
description: One-line summary of the session (~120 chars)
type: conference-note
conference: GraphConf-2026 | AgentSummit
speaker: Full name of the presenter (extract from Perplexity output or video title)
speaker_affiliation: Organization or company (extract if mentioned, otherwise leave blank)
session_type: keynote | talk | panel | workshop | lightning | fireside
session_date: YYYY-MM-DD (use the video date if available, otherwise leave blank)
source: YouTube video title (verbatim, for traceability)
added: YYYY-MM-DD
---
```

Extract `speaker`, `speaker_affiliation`, and `session_type` from the Perplexity output. These are typically in the video title, intro paragraph, or speaker bio section. If the session has multiple speakers (panels), list all names comma-separated in `speaker`.

#### Place

Route by inbox source folder:
- Files from `conferences/graphconf/` → `Conference-notes/GraphConf-2026/sources/`
- Files from `conferences/agentsummit/` → `Conference-notes/AgentSummit/sources/`

Rename each file to sentence case with underscores per `.claude/rules/file-naming.md`.

Show the user a summary table after placement: file name, destination folder, session date if captured.

### Step 3: wiki-lint and os-maintain

#### Wiki-lint

Run `/wiki-lint` on the Conference-notes folders. If you have a lint script, run it:

```bash
python3 Automations/wiki-lint/wiki_lint.py --report
python3 Automations/wiki-lint/wiki_lint.py
```

Otherwise, work through the `/wiki-lint` skill's manual steps (it is a bring-your-own-script skill; see its SKILL.md).

All docs should already have frontmatter from Step 2. If any are missing, add frontmatter now.

#### Os-maintain

Run `/os-maintain` to update downstream docs (README.md counts, CHANGELOG.md).

### Step 4: ship

Run `/ship` to sync docs and push to GitHub.

## Exit checklist

Done when all of these are true:

- [ ] All non-markdown files converted and originals deleted (Step 1 / Step G3)
- [ ] All docs cleaned (boilerplate stripped, em dashes replaced, brand names replaced, frontmatter added with conference schema) (Step 2 / Step G4)
- [ ] All docs placed in correct destination folder with sentence-case underscore filenames (Step 2 / Step G4)
- [ ] Wiki-lint reports 0 missing frontmatter and READMEs regenerated (Step 3)
- [ ] Os-maintain updated downstream docs (README counts, CHANGELOG) (Step 3)
- [ ] Changes committed and pushed via /ship (Step 4)

## Parallelization

When processing many files (5+), use parallel tool calls for writes. Group by destination folder. For multi-step work per file (research + write), use parallel subagents instead. Merge results before running wiki-lint.

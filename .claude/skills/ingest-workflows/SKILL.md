---
name: ingest-workflows
author: human
description: Process Perplexity exports from YouTube_sourced_workflows_inbox into the correct repo folders with full downstream sync. TRIGGER when user says "new docs in inbox", "process inbox", "ingest these", drops files in the inbox folder, or mentions Perplexity exports to process. Also trigger on "clean up inbox" or "what's in the inbox". DO NOT TRIGGER for conference notes (use ingest-conference) or AI newsletter processing (use ai-digest).
scope: project
user_invocable: true
agent: true
model: sonnet
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/file-naming.md
  - .claude/rules/file-protection.md
  - .claude/rules/pdf-docx-conversion.md
  - .claude/rules/anti-rationalization.md
  - .claude/rules/system-design-patterns.md
  - .claude/skills/ship/SKILL.md
  - .claude/skills/wiki-lint/SKILL.md
  - .claude/skills/os-maintain/SKILL.md
  - Reference/README.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - README.md
  - CHANGELOG.md
  - .claude/WHATS_NEW.md
  - .claude/rules/communication-style.md
---

# /ingest-workflows - process inbox into the repo ecosystem

Triggered when the user drops Perplexity exports into `Reference/YouTube_sourced_workflows_inbox/` (your reference-doc library's inbox folder, name it whatever fits your setup) and says "new docs in inbox", "process inbox", or similar.

Eight steps: convert → clean and place → apply OS learnings → update folder playbooks → review flags, recommend, and implement → wiki-lint and os-maintain → ship.

No confirmation pauses. Just do it.

## Read-first

| Source | Path | What to extract |
|--------|------|-----------------|
| Inbox files | `Reference/YouTube_sourced_workflows_inbox/` | All files to process (pdf, docx, html, md) |
| Writing style | `.claude/rules/writing-style.md` | Brand name replacements, formatting rules |
| File naming | `.claude/rules/file-naming.md` | Naming conventions for destination files |
| Reference-doc library index | `Reference/README.md` | Current folder structure and doc counts |
| Skill memory | `.claude/skills/ingest-workflows/memory.md` | Lessons from past runs |

## Preconditions

Before processing, verify:
1. Inbox directory exists and contains at least 1 file
2. If you have built a wiki-lint script, confirm it exists. Otherwise plan to update folder READMEs by hand via the `/wiki-lint` skill's manual steps.
3. Destination folders exist (create if missing)

If the inbox is empty, report "Inbox is empty. Nothing to process." and stop.

## Step 0: inbox expiry check

Before processing, check modification times of all files in the inbox:

```bash
find Reference/YouTube_sourced_workflows_inbox/ -type f -mtime +7
```

If any files are older than 7 days, flag them: "N files have been sitting in the inbox for over 7 days: [filenames]. Process them now or remove if no longer needed."

Then proceed with all files (old and new) through the pipeline.

## Step 1: convert non-markdown files and delete originals

Scan the entire inbox (including subdirectories) for `.pdf`, `.docx`, `.PDF`, `.DOCX`, and `.html` files.

1. List all non-markdown files found
2. Read each file and convert to markdown in-place (same directory)
3. Apply all Step 2 cleaning rules during conversion
4. Delete the original PDF/DOCX/HTML files immediately after successful conversion
5. Report: "Converted N files, deleted N originals"

Do not ask for confirmation. The owner granted standing authorization on 2026-08-15 to delete an inbox original once its conversion has succeeded, so `file-protection.md`'s ask-first step is already satisfied for this one narrow case. Prefix each deletion with `CLAUDE_APPROVED_DELETE=1` to clear the Bash guard, and only after you have verified the converted markdown exists and is non-empty. A failed or partial conversion means the original stays. Always name the deleted originals in the run report so the behavior stays visible.

## Step 2: clean, classify, and place

### Clean each file

Apply ALL of these transformations to every `.md` file in the inbox:

1. **Strip Perplexity boilerplate** - remove `<img>` tag, system prompt block (everything before the actual content), `</output>` closing tag, `<div>` decorative elements, trailing engagement questions ("Would it be most useful to...", "If you were to apply...")
2. **Add clean heading** - `# Title in sentence case` as the first line. For reference docs, add `Source: Perplexity deep-dive` on line 3.
3. **Replace em dashes** - all `—` and `–` become ` - ` (space hyphen space)
4. **Replace brand names** in body text per `.claude/rules/writing-style.md`:
   - Claude Code, Cursor/Claude, Cursor -> "coding agent" or "LLM via CLI tooling"
   - Claude.ai -> "chat-based LLM"
   - Cowork -> "workspace tool"
   - Perplexity -> "LLM" or "research tool" (keep in `Source:` attribution and footnote URLs)
   - Braintrust -> "eval platform"
   - GPT -> "LLM"
   - Slack -> "workspace messaging"
   - Figma -> "design tool"
   - Excalidraw -> "drawing tool"
   - Lovable -> "AI prototyping tool"
5. **Sentence case all headings** - capitalize only first word, proper nouns, acronyms
6. **Reduce bold** - keep bold only for genuinely important terms
7. **Remove `***` horizontal rules** between sections
8. **Keep footnote URLs** - source attribution stays
9. **Add frontmatter** - add wiki-lint frontmatter at the top of each file during cleaning (do not defer to a later step). Use the schema below:

```yaml
---
description: One-line summary (~120 chars)
type: career | product-sense | technical | interview-prep | system-design | job-search | strategy | workflow | evaluation | reference
source: Author or source name
added: YYYY-MM-DD
actionability: high | medium | low
---
```

**Actionability scoring guide:**
- high: contains a workflow, checklist, or framework you can apply this week
- medium: contains principles or mental models that inform decisions over time
- low: background knowledge, context, or reference-only

### Classify and place

Read each file and classify into the correct destination:

| Content type | Destination |
|-------------|-------------|
| Workflow (has JSON schema, `"steps"`, `"actors"`, quick steps) | `Reference/Agent_workflows/` |
| AI PM reference (deep-dive summary, product/strategy/technical) | `Reference/AI_PM_reference/` |
| Business/finance (company analysis, macro, investing, valuation) | `Reference/Business_and_finance/` |
| Career advancement (visibility, politics, influence, career growth) | `Reference/Career_advancement/` |
| Interview prep (hiring criteria, interview frameworks, job search) | `Reference/AI PM interview preparation/` |
| Software engineering future (coding evolution, AI engineering) | `Reference/Software_engineering_future/` |
| A tracked project (any single project you're actively building, any sub-topic) | `Projects/<project-name>/Reference/new-intake/` |

**Subfolder placement rules:**

- Never place files at a folder root when subfolders exist. Check the destination for subfolders first.
- Docs about a single tracked project (e.g. one you named `example-project`) always go to `Projects/<project-name>/Reference/new-intake/` (triage to system/ or user-side/ happens later, outside this skill).
- If the correct subfolder does not exist, create it. Name it with lowercase-hyphenated words.
- When in doubt between subfolders, check existing files in each for content similarity.

**Inbox subdirectories as routing hints:**

- Files in `YouTube_sourced_workflows_inbox/<project-name>/` go to `Projects/<project-name>/Reference/new-intake/`
- Files in `YouTube_sourced_workflows_inbox/improve personal-os/` go to `Reference/AI_PM_reference/` AND trigger Step 3 (apply OS learnings immediately)
- Files in the inbox root go to the appropriate `Reference/` subfolder

Rename each file to sentence case with underscores per `.claude/rules/file-naming.md`. Write cleaned content to the destination. Verify: grep for em dashes and brand names in new files (should find 0).

Show the user a summary table after placement: file name, destination folder.

### Reference folder growth check

After placement, count docs (excluding README.md) in each destination folder that received new files. Report the counts. If any folder exceeds 60 docs, flag it: "AI_PM_reference has N docs. Attention, not content, is the constraint. Consider archiving or consolidating older docs before the next ingest." Same principle as book-inventory-check but for reference folders.

### Consolidation check

After placement, scan each destination folder that received new files. For each new doc, check if any existing doc in the same folder covers substantially the same topic (similar title keywords or overlapping subject). If found, flag: "New doc [X] may overlap with existing [Y]. Consider merging or linking them."

This is a keyword check, not semantic analysis. Compare the title words and first heading of each new doc against titles of existing docs in the same folder. Flag pairs where 3+ non-trivial words overlap (exclude words like "the", "and", "for", "how", "with", "AI").

## Step 3: apply OS learnings (improve personal-os docs only)

If any ingested documents came from the `improve personal-os/` inbox subdirectory (or are classified as personal OS improvement content), extract actionable learnings and apply them immediately:

1. **Extract patterns** - read each "improve personal-os" doc and identify concrete, actionable improvements: new skill ideas, rule refinements, architecture patterns, workflow enhancements, or process changes that could strengthen this OS.
2. **Apply immediately** - for each actionable learning, implement it now:
   - New skill idea → create the skill (or note it for creation if complex)
   - Rule refinement → edit the relevant rule file
   - Architecture pattern → update CLAUDE.md, AGENTS.md, or relevant system docs
   - Workflow enhancement → update the relevant skill or create a new one
   - Process change → add or update the relevant rule
3. **Log what was applied** - show a summary: "Applied N learnings from improve-personal-os docs" with a bullet per change.

The goal: docs about improving personal OS systems are not just filed away as reference. They trigger real system upgrades. The inbox subfolder `improve personal-os/` is the signal. If a doc teaches something we can use, use it now.

Skip this step entirely for docs from other inbox subdirectories (Atlas, root-level docs, etc.).

## Step 4: update folder playbooks

Some library folders have a PLAYBOOK.md, a navigation layer that maps every doc in the folder to a decision tree, a one-sticky-note cheat sheet, and (depending on the folder) a use-case table or a curated reading sequence. A playbook only goes stale when a doc is added without updating it, so the update happens here, in the same run that placed the doc, never as a separate pass to remember later.

The rule is generic, not a fixed list. For every doc you placed in Step 2, check its destination folder for a `PLAYBOOK.md`. If one exists, update it. If the folder has no playbook, skip it (its README table is the navigation). As of June 2026 the folders with playbooks are `AI_PM_reference`, `Career_advancement`, and `AI PM interview preparation`, but do not rely on that list. Check for the file.

For each new doc whose folder has a playbook, update the parts that playbook actually has. The playbooks are not structurally identical: every one has a decision tree and a cheat sheet, but the rest varies. Check the section headings before editing.

1. Decision tree: every playbook has one (titled "Decision tree", "Which doc do I need?", or "Where to start"). Add a leaf node under the branch that matches the doc's topic. Add a branch if none fits. Keep Mermaid node labels under 30 characters, no literal line breaks.
2. Cheat sheet ("one sticky note per doc"): every playbook has one. Add one entry, a short sentence-case heading plus 2-3 bullet takeaways, so the doc is usable without opening it.
3. Third section, varies by playbook. If it has a use-case or quick-reference table (`AI_PM_reference` does), add a row mapping a reader situation to the new doc. If instead it has a curated reading sequence ("Reading order", "Week before the interview"), only slot the doc in if it genuinely belongs in that sequence. Otherwise leave that section; the tree and cheat sheet already cover the doc.
4. Intro count, only if present. If the opening paragraph states a document count ("collection of 12 docs", "collection of nine documents"), bump it. `AI_PM_reference` has no count in its intro, so skip this there.

Do not create a new playbook here. A folder crossing the size where it needs one is a deliberate decision, not an ingest side effect. If a folder without a playbook has grown large enough that its README table is hard to scan, flag it for the user as a candidate for a new playbook instead.

Apply the writing-style rules to every playbook edit: sentence case headings, no bold, no em dashes.

## Step 5: review flags, recommend, and implement

Step 2 raised flags (growth check, consolidation check, placement uncertainties), but raising a flag is not acting on it. This step closes the loop: implement the fixes that are safe now, and surface the ones that need the user's judgment. Do not skip it. A flag that is only logged and never acted on is exactly how `AI_PM_reference` drifted past the 60-doc threshold for three ingests running.

Sort every flag into the three-state taxonomy from `.claude/rules/system-design-patterns.md`.

Tier A and B, implement now (and say what you changed):

- Consolidation overlap: when a new doc overlaps an existing one, add a reciprocal cross-link between the two (in the doc body or the playbook cheat sheet). Mechanical, do it.
- Clear misplacement: if a doc landed in a folder that plainly does not fit and the right one is obvious, move it and note the move.
- Thin or missing frontmatter surfaced by the run: fill it.

Tier C, recommend, do not execute alone:

- Folder split or reorganization (any folder over the 60-doc threshold): produce a concrete proposal (proposed subfolders with doc assignments, or an archive list with a target count) and put it to the user. Do not move dozens of docs on your own. That is an architecture change, and `dependency-tracking` and `bossman-mode` both say ask first.
- Merging or deleting docs: propose, do not do.
- Renaming an invocation or changing what a folder is for: propose.

Output a recommendations block at the end of this step:

- Implemented (A/B): one line per fix.
- Needs your decision (C): one line per item, each with a proposed action and the trigger (for example, "AI_PM_reference at 75 docs, over 60: split into sub-topics or archive stale, proposal attached").

Then continue to Step 6. The A/B changes flow through wiki-lint, os-maintain, and ship in the next steps. The tier-C items wait for the user; do not block ship on them.

## Step 6: wiki-lint and os-maintain

### Wiki-lint

Run `/wiki-lint` to regenerate per-folder READMEs with the new docs. If you have a lint script:

```bash
python3 Automations/wiki-lint/wiki_lint.py --report   # verify 0 missing frontmatter
python3 Automations/wiki-lint/wiki_lint.py             # regenerate READMEs
```

Otherwise, work through the `/wiki-lint` skill's manual steps (it is a bring-your-own-script skill; see its SKILL.md).

All docs should already have frontmatter from Step 2. If any are missing, add frontmatter now. Do not silently skip.

### Os-maintain

Run `/os-maintain` to update downstream docs (README.md counts, CHANGELOG.md, PLAYBOOK.md counts, Reference/README.md topic tables). Playbook content was already updated in Step 4; os-maintain only refreshes the counts. Os-maintain handles count verification automatically.

## Step 7: ship

Run `/ship` to sync docs and push to GitHub. The /ship skill runs docs-sync first (catches any remaining downstream updates) then git-sync.

## Parallelization

When processing many files (5+), use parallel agents for the conversion and cleaning work. Group files by destination folder and dispatch one agent per batch. Each agent handles conversion, cleaning, classification, and writing for its batch. Merge results before running wiki-lint.

## Shortcuts to resist

See `.claude/rules/anti-rationalization.md` for the general pattern. These three are specific to this skill.

| Shortcut | Why it's tempting | Counter |
|----------|--------------------|---------|
| "This doc looks similar to others already ingested, I can skip the full cleaning pass" | Similar-looking source material feels like it needs the same light touch | Similar is not identical. Run boilerplate-stripping, brand-neutralizing, and em-dash removal on every file, every time |
| "The doc is a minor addition, I'll skip updating the folder playbook" | Playbook updates feel like overhead for a one-doc change | One skipped update is how playbooks drift silently. Step 4 runs for every doc whose destination folder has a PLAYBOOK.md, minor or not |
| "The frontmatter tags feel optional for this file, I'll leave them blank" | Filling in every field feels like busywork when the doc's purpose is obvious | Blank frontmatter is what wiki-lint's `--report` step exists to catch. Fill it in now instead of deferring the fix to a later lint pass |

## Exit checklist

Done when all of these are true:

- [ ] All files in the inbox were processed (none skipped, all file types scanned)
- [ ] Every doc has frontmatter with description, type, source, added date, actionability
- [ ] No em dashes remain in any new file (grep verification)
- [ ] No brand names remain in body text (grep verification)
- [ ] All headings are sentence case
- [ ] Each doc was placed in the correct destination folder (classification table followed)
- [ ] Reference folder growth check completed (60-doc threshold flagged, and a split/archive proposal produced when exceeded)
- [ ] Consolidation check completed (3+ keyword overlap pairs flagged)
- [ ] Recommend-and-implement step ran: A/B fixes applied and noted, C recommendations surfaced to the user with a proposed action
- [ ] Folder playbooks updated for every destination folder that has a PLAYBOOK.md (decision tree and cheat sheet always; use-case row or intro count where that playbook has them)
- [ ] Wiki-lint ran successfully (0 missing frontmatter)
- [ ] Os-maintain ran (counts and downstream docs updated)
- [ ] /ship committed and pushed all changes
- [ ] Original inbox files deleted after their conversion succeeded, and named in the run report (standing authorization, 2026-08-15, no per-run confirmation)

---
name: wiki-lint
author: human
description: Keep your reference-doc library's folder README indexes in sync with doc frontmatter. TRIGGER when user says /wiki-lint, "update wiki index", "sync wiki READMEs", "add to wiki", "regenerate README", or "check frontmatter". Also trigger when a new doc is added to any reference-doc library folder. DO NOT TRIGGER for unrelated folders or for full OS doc maintenance (use os-maintain).
scope: project
agent: true
model: sonnet
depends_on:
  - Reference/
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - DEPENDENCIES.md
  - .claude/skills/ingest-workflows/SKILL.md
---

# Wiki-lint

Keeps your reference-doc library's folder READMEs in sync with doc frontmatter. Run any time a doc is added or frontmatter changes.

This skill assumes a reference-doc library folder (referred to below as `Reference/`, name it whatever fits your setup) organized into topic subfolders, each with a README that indexes the docs inside it by frontmatter fields.

## Bring your own lint script

There is no bundled `wiki_lint.py` in this repo. The commands below (`python3 Automations/wiki-lint/wiki_lint.py`) describe the shape of a small script you would write for your own doc set: scan a folder tree for markdown files, read each file's frontmatter, and regenerate a table in that folder's README. It typically does two things:

- `--report`: scan for docs missing frontmatter, print a list, change nothing
- (no flag): regenerate every folder README from current frontmatter

If you have not built this script yet, do the same work manually: read each doc's frontmatter (or note it is missing), and hand-write or hand-edit the README tables yourself. The frontmatter schema and type vocabulary below are the part worth keeping regardless of whether a script exists.

## Invocation

`/wiki-lint` — lint all folders
`/wiki-lint --folder "topic-name"` — one folder only
`/wiki-lint --report` — show missing frontmatter without updating

## Behavior

### Step 1: Report missing frontmatter

If you have a lint script, run it from repo root:

```bash
python3 Automations/wiki-lint/wiki_lint.py --report
```

Otherwise, walk the `Reference/` tree yourself and note every file missing frontmatter.

For each doc missing frontmatter, infer and write the frontmatter block:
- `description`: first sentence of the document body (after the h1), trimmed to ~120 chars
- `type`: infer from content using the type vocabulary below — when ambiguous, ask the user
- `source`: look for a byline, speaker name, or publication in the first 10 lines; use `-` if absent
- `added`: run `git log --follow --format=%as -- "<filepath>" | tail -1`; use today's date if file is untracked

Write the frontmatter block at the very top of the file (before the h1).

### Step 2: Regenerate all READMEs

If you have a lint script:

```bash
python3 Automations/wiki-lint/wiki_lint.py
```

Otherwise, regenerate each folder's README table by hand from the current frontmatter of the docs inside it.

Report: N folders updated, N docs indexed, N missing frontmatter.

### Step 3: Surface anything needing attention

If any docs still have no frontmatter after step 1, list them explicitly. Do not silently skip.

## Type vocabulary

Adapt this list to your own reference-doc library's topics. The table below is a starting example.

| Type | Use when the reader's goal is... |
|------|----------------------------------|
| `interview-prep` | Preparing for a specific interview round |
| `career` | Growing, advancing, or navigating a career |
| `product-sense` | Building product judgment and instinct |
| `system-design` | Technical system design skills |
| `job-search` | Job search mechanics and tactics |
| `technical` | Understanding AI/ML/infra concepts |
| `strategy` | Business strategy or competitive frameworks |
| `workflow` | Operational workflows and automation |
| `evaluation` | Measuring and evaluating AI systems |
| `reference` | General reference, no cleaner fit |

## Frontmatter schema

```yaml
---
description: one-liner (required, appears in README table)
type: one of the types above (required)
source: author or company (optional, use - if unknown)
added: YYYY-MM-DD (optional, inferred from git log)
actionability: high | medium | low (optional, inferred from content)
---
```

Actionability: high = workflow/checklist/framework you can apply this week. medium = principles or mental models that inform decisions over time. low = background knowledge or reference-only.

## Ongoing contract

Every new doc added to `Reference/` gets frontmatter at creation time. Run `/wiki-lint` after adding any doc to keep the README current.

## Exit checklist

Done when all of these are true:

- [ ] Missing frontmatter reported and inferred blocks written
- [ ] All READMEs regenerated (via your lint script, or by hand if none exists)
- [ ] Counts reported: folders updated, docs indexed, missing frontmatter
- [ ] Any still-missing frontmatter surfaced explicitly, not skipped
- [ ] Edits respected the A/B/C tiers: mechanical fixed, judgment flagged

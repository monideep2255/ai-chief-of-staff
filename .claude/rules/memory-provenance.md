---
name: memory-provenance
description: Tag source quality on project and reference memories so future sessions can weight conflicting memories correctly
scope: portable
depends_on:
  - .claude/rules/decision-logging.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Memory provenance

When saving project or reference memories about decisions or evidence, tag the source quality. This helps future sessions weight conflicting memories correctly.

### Provenance tiers (highest to lowest trust)

| Tag | Meaning | Example |
|-----|---------|---------|
| documented decision | Written record of a decision with reasoning | DECISIONS.md entry, ADR, meeting notes with explicit "we decided X" |
| documented research | Published data, papers, official docs | arXiv paper, vendor documentation, benchmark results |
| stakeholder verbal | Something a person said in conversation | "Sam mentioned in standup that timeline moved up" |
| PM intuition | Your read of the situation without external validation | "I think the team is skeptical about this approach" |

### How to apply

When writing a memory file, include the provenance tag in the description or body:

```markdown
Source quality: documented decision
```

or

```markdown
Source quality: stakeholder verbal (Sam, June 5 check-in)
```

When two memories conflict, the higher-trust source wins unless the lower-trust source is more recent and explicitly supersedes it.

### Decay by tier

Trust is not permanent for every tier. High-trust memories are evergreen; low-trust ones should fade unless something re-confirms them. This keeps a six-month-old hunch from being weighted the same as a written decision.

| Tag | Lifetime | On recall past its window |
|-----|----------|---------------------------|
| documented decision | evergreen | surface as-is |
| documented research | evergreen | surface as-is (note if the field has moved on) |
| stakeholder verbal | soft-stale after ~6 weeks | surface, but flag as possibly stale and worth re-confirming |
| PM intuition | soft-stale after ~4 weeks | surface, but flag as an old read that may no longer hold |

Soft-stale means the memory still appears in recall, it just carries a note that it is old and low-trust, so a future session treats it as a lead to verify, not a fact to assert. Only the two lower tiers decay; documented decisions and research stay unless a newer higher-trust memory supersedes them. This is a decay-versus-evergreen split worth applying to session versus curated memory generally, mapped onto your provenance tiers.

### Update discipline: diff, not rewrite

When new evidence (a correction, a new decision, a changed preference) contradicts or extends an existing memory file, edit the specific fact that changed. Do not regenerate the whole file from scratch. A wholesale rewrite driven by one new data point treats a single recent signal as the whole picture, the same failure a conservative reflective-memory update exists to avoid: a handful of recent, unusual posts should not overwrite a style profile built from years of prior work.

Before rewriting more than a small, targeted diff of an existing memory file, name the specific fact that changed and the evidence that triggered it. If you cannot name both, the update is not yet earned. Hold the existing content.

### Audit trail for edits

Memory files typically live outside a repository's git history (for example, in your coding assistant's own memory directory), so an overwritten fact leaves no record and no way back, unlike `DECISIONS.md` or `OS_IMPROVEMENTS.md`. Before editing an existing memory file's content (not just adding a new file to the index), add a one-line dated trailer at the bottom of the file naming what changed and the evidence:

`Updated 2026-08-22: revised X because Y (source: what triggered it)`

That is the minimum audit trail that makes a bad update reversible: read the trailer, restore the prior fact. It is the memory-file analogue of the `DECISIONS.md` and `OS_IMPROVEMENTS.md` tables, applied to files that sit outside git.

### Three-state permissions

Allow:
- Tag any new memory freely
- Use provenance to resolve conflicting memories without asking

Ask:
- Before overriding a "documented decision" memory with a "PM intuition" memory

Deny:
- Never treat all memories as equal weight when they conflict
- Never omit the provenance tag on memories about decisions or evidence
- Never regenerate an existing memory file wholesale when only one fact changed; edit the specific line instead
- Never revise an existing memory file's content without adding the dated trailer that records what changed and why

The test: when I saved a project or reference memory, did I tag the source quality, and when I revised existing content, did I add a dated trailer naming what changed and why instead of silently overwriting it?

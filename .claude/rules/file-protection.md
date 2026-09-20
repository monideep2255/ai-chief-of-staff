---
description: "File protection: no deletion without asking, no unnecessary file creation, documentation repo only"
scope: portable
alwaysApply: true
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## File protection

- Don't delete files or folders. Ask the user and wait for confirmation first.
- Don't create new files unnecessarily -- prefer editing existing documentation.
- Don't add build/test commands -- this is a documentation repo, not a software project.
- Exception: a self-contained software project folder (if you add one) with its own venv/tests is exempt from the "documentation only" rule below.

### Standing deletion authorizations

A standing authorization is a deletion the owner has approved once, in advance, for a narrow and repeating case. It replaces the per-turn ask for that case only. Every one is named here, with its date and its exact boundary. Nothing else qualifies, and a standing grant never widens by analogy to a similar-looking deletion.

| Granted | Scope | Boundary |
|---------|-------|----------|
| 2026-07-15 | Empty `.cc-writes` staging folders, removed by `.claude/skills/ship/clean-cc-writes.py` | `os.rmdir` only, so a folder holding any real file is untouchable |
| 2026-07-25 | `.DS_Store` files, removed by the same script | Basename must be exactly `.DS_Store`, path must be a regular file, never a directory or symlink |
| 2026-08-15 | Original PDF, DOCX, and HTML files in the `ingest-workflows` inbox, after conversion | Delete only after verifying the converted markdown exists and is non-empty. A failed or partial conversion means the original stays. The deleted files are named in the run report |
| 2026-09-20 | Agent scratch files and folders inside the repository, removed by the same script | Whole-name match only, never a substring, so a `_templates/` folder and anything named `temporal` survive. A path git tracks is reported, never deleted. Vendored trees are pruned from the walk. The pattern list and the three guards live in `.claude/skills/ship/SKILL.md` Step 2 |

The test: did I create, delete, or modify any file the user did not ask about, and if I deleted one, did the user approve it in this turn, or does the deletion fall inside a standing authorization named above?

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

The test: did I create, delete, or modify any file the user did not ask about?

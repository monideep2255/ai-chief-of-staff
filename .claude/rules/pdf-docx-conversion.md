---
description: "Ask before converting PDFs/DOCX to markdown, verify content preservation"
scope: project
alwaysApply: false
globs: ["**/*.pdf", "**/*.docx", "**/*.PDF", "**/*.DOCX"]
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/file-naming.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## PDF and DOCX conversion

When you encounter a `.pdf` or `.docx` file in the workspace (during file listing, git status, or user request):

1. Ask the user: "I see [filename] is a PDF/DOCX. Want me to convert it to markdown?"
2. If yes, first assess whether you can preserve the full content:
    - Read the file and check for complex elements (tables, images, equations, diagrams, embedded media).
    - Report what you can and cannot preserve: "This PDF has 8 pages of text and 2 tables - I can preserve 100% of the content" or "This file has embedded diagrams I cannot convert to text."
3. Wait for explicit confirmation before converting.
4. Convert to markdown following the repo's writing style (sentence case headings, no em dashes, etc.) and file naming conventions.
5. After successful conversion, ask if the user wants the original PDF/DOCX deleted.

Do NOT auto-convert without asking. The user decides.

The test: did I ask and wait for explicit confirmation before converting a PDF or DOCX, and report what content I could not preserve?

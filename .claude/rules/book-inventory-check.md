---
description: "Before creating any new book, show the full inventory of existing books and reading progress. Prevents accumulation of unread material."
scope: project
globs: ["Learning/**"]
depends_on:
  - Learning/
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Book inventory check

Before generating ANY new book (via /book-builder-hard-skills, /book-builder-soft-skills, /book-builder-from-sources, or manual chapter creation) or systems map (via /systems-map), you MUST:

1. List every existing book with its chapter count
2. Show reading progress for each (check for any progress markers, notes, or annotations)
3. Ask: "You have X books with Y total chapters. How many have you actually read? Do you still want to create another one?"
4. Wait for explicit confirmation before proceeding

**Current inventory (update when books are added or moved):**

| Location | Book | Chapters |
|----------|------|----------|
| 0-done/ | knowledge-graphs | 20 |
| 0-done/ | wisdom-and-purpose | 8 |
| 0-done/ | us-healthcare | 18 |
| 0-done/ | psychology-and-human-behavior | 19 |
| 1-current-focus/ | soft-skills-for-the-ai-era | 17 |
| 0-done/ | geopolitics | 20 |
| 0-done/ | supply-chains | 18 |
| hard-skills/ | ai-agents-and-mcp | 15 |
| hard-skills/ | ai-and-ml | 25 |
| hard-skills/ | ai-evals-and-prompt-engineering | 14 |
| hard-skills/ | ai-knowledge-base | 16 |
| hard-skills/ | aman-ai | reference notes |
| 2-next-in-line/ | finance-for-non-finance | 16 |
| 0-done/ | system-design | 20 |
| soft-skills/ | career-growth | 17 |
| soft-skills/ | career-vision | 10 |
| local-sources/ | ai-pm-practitioner-playbook | varies |
| local-sources/ | ai-product-management | varies |
| local-sources/ | ai-user-research | varies |
| local-sources/ | industry-and-investments | varies |
| local-sources/ | personal-projects-and-research | varies |
| local-sources/ | pm-interview-prep | varies |
| society/ | media-literacy | varies |
| society/ | money-and-banking | varies |

**Total: 25+ books, 216+ chapters**

**Visual synthesis maps** (update when maps are added):

| Location           | Topic                                    | Building blocks |
|--------------------|------------------------------------------|-----------------|
| visual-synthesis/  | energy-and-ai-infrastructure             | 13              |
| visual-synthesis/  | geopolitics                              | 12              |
| visual-synthesis/  | supply-chains                            | 12              |
| visual-synthesis/  | system-design                            | 12              |
| visual-synthesis/  | finance-for-non-finance                  | 12              |
| visual-synthesis/  | future-of-work                           | 12              |
| visual-synthesis/  | money-and-banking                        | 11              |
| visual-synthesis/  | media-literacy                           | 12              |
| visual-synthesis/  | frontier-agentic-models-built-and-served | 11              |
| visual-synthesis/  | leverage                                 | 12              |

This rule exists because generating books is cheap but reading them is not. The constraint is attention, not content. The same applies to systems maps: each one represents a topic you committed to understanding deeply.

This gate is not suspended by `bossman-mode.md`. Bossman mode suspends deliberation rules (clarify-before-drafting, preserve-your-thinking, pause-before-acting's step 2), but this confirmation gate stays active even during an autonomous bossman-mode run, per `bossman-mode.md`'s Preserved behaviors.

The test: did I list every book with its chapter count, show reading progress, and get explicit confirmation before generating a new book or systems map?

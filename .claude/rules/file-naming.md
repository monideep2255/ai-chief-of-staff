---
description: "File naming conventions for meetings, prep docs, explanations, decisions, questions"
scope: portable
alwaysApply: true
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/agents/meeting-notes.md
  - .claude/rules/pdf-docx-conversion.md
---

## File naming conventions

Use sentence case, the same rules as headings. Capitalize only the first word, proper nouns, acronyms, and named tools. Use underscores between words.

| Type | Format | Example |
|------|--------|---------|
| Meeting notes (simple) | `Month_Day.md` | `January_06.md` |
| Meeting notes (numbered) | `{number}_Meeting:{topic} {Month} {Day}.md` | `2_Meeting:technical_refinement_January_20.md` |
| Meeting notes (person) | `{number}_Meeting_{Person}_{Month}_{Day}.md` | `2_Meeting_Priya_January_22.md` |
| Meeting prep | `Prep_for_{Month}_{Day}.md` | `Prep_for_January_20.md` |
| Explanations | `Concept_explained.md` | `Meridian_project_explained.md` |
| Decisions | `Topic_decision.md` | `Neo4j_vs_ArangoDB_decision.md` |
| Questions | `Questions_for_X.md` | `Questions_for_first_WG_meeting.md` |
| Discussion/insight | `Topic_description_Month_Day.md` | `AI_as_programming_language_discussion_March_20.md` |

Triggers:

- You are creating a new file in the repo
- A skill or agent is about to write a file and asks for a name

Does not trigger:

- Editing an existing file (name is already set)
- Writing code files (.py, .js, .ts, etc.), which follow the language's conventions
- Commit messages, CHANGELOG entries, or inline comments

The test: does every file I created match its type's format in the table, using sentence case and underscores between words?

---
description: "Meeting notes must use nested bullet format with action items section"
scope: project
globs: ["Meetings/**/*.md"]
alwaysApply: false
depends_on:
  - Meetings/Example_meeting_January_06.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/agents/meeting-notes.md
---

## Meeting notes format

Nested bullet points. Always include an action items section.

```markdown
- Meeting notes
    - Topic 1
        - Sub-point with details
    - Topic 2
        - Discussion point
    - Action items:
        - Specific task 1 (owner, deadline)
        - Specific task 2
```

> Style reference: [Meetings/Example_meeting_January_06.md](../../Meetings/Example_meeting_January_06.md)

The test: did I write the meeting notes as nested bullets with an action items section?

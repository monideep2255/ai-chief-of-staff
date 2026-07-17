---
description: "Mention a matching workflow or reference doc from your own library when a user request aligns with one"
scope: project
globs: ["Reference/**"]
depends_on: []
depended_by:
  - .claude/rules/communication-style.md
  - CLAUDE.md
---

## Workflow awareness

If you keep a library of your own workflow docs (how-to playbooks for recurring tasks, wherever you choose to store them), mention the matching one when a user's request lines up with it. For example:

- Writing a PRD → "There's a workflow for this: `Reference/PRD_workflow.md`" (if you have one)
- Designing a feature → "There's a workflow for this: `Reference/Feature_design_loop.md`" (if you have one)

Don't push - just mention once. The user decides whether to follow it.

## Reference awareness

If you keep a library of reference docs (deep-dives, frameworks, prior research), mention the matching one when a task looks like it might have a relevant entry: strategy, product decisions, agent design, exec communication, market analysis, evaluation frameworks, and similar topics.

Same rule as workflow awareness: mention once, don't push, user decides whether to read.

The test: when the user's request matched a workflow or reference doc in your own library, did I mention it once without pushing?

---
description: "Default to agent-first-draft on reversible (two-way door) tasks, stay hands-on on irreversible (one-way door) ones."
scope: project
alwaysApply: true
depends_on:
  - .claude/rules/preserve-your-thinking.md
  - .claude/rules/boil-the-lake.md
  - .claude/rules/goal-contracts.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Agent-first default

Default P0 for any repetitive or draftable execution task: let an agent take the first crack, then refine it with your own context. You are the editor of the draft, not the origin of every keystroke. The door test decides how far to delegate.

This rule governs execution delegation (who drafts), not judgment (who decides). Judgment calls are owned by preserve-your-thinking; this rule never overrides it.

### The door test

Before delegating, ask: one-way door or two-way door?

- Two-way door (reversible): draft code, test copy, first-pass research, a bug-fix PR, a data pull. Go agent-first. The cost of a bad draft is one revert. Try it.
- One-way door (irreversible or deeply personal): a stakeholder narrative, a career decision, a pitch story, anything where the judgment is the product. Stay hands-on. An agent may gather inputs; you write the thing.

The agent produces the first version; you own the last version. Never ship an agent's first draft on a one-way door.

### Relationship to existing rules

- preserve-your-thinking wins on judgment calls: for a decision, the agent gathers and stress-tests, you decide. Agent-first is about who types the draft, never about who makes the call. When a task is both a decision and a drafted artifact (a memo whose final section recommends a vendor), preserve-your-thinking governs the decision and this rule governs the draft, and preserve-your-thinking's check of your thinking runs before the agent drafts the embedded recommendation, not after.
- boil-the-lake still applies: if the agent takes the first crack, review the whole output, not a sample.
- goal-contracts still applies: an agent-first run on a multi-step task still needs a done-when and a verify surface first.

### Three-state permissions

Allow:
- Hand any two-way-door execution task to an agent for a first draft without asking
- Refine that draft with your own context before it ships

Ask:
- Before going agent-first on anything you cannot cheaply reverse

Deny:
- Never let an agent's first draft be the final artifact on a one-way door
- Never treat agent-first as permission to skip reviewing the full output
- Never use agent-first to shortcut a judgment call preserve-your-thinking would gate

The test: did I let an agent take the first crack on a reversible task, then refine it, and stay hands-on where the decision was irreversible?

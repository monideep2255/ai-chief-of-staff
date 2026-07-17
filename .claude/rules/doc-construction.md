---
scope: portable
depends_on:
  - .claude/agents/first-principles.md
  - .claude/rules/writing-style.md
  - .claude/rules/clarify-before-drafting.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Doc construction

Rules for constructing substantial markdown docs. This rule governs *how a doc is built* (structure, explanation style, visuals). Prose hygiene (em dashes, sentence case, no bold) lives in `writing-style.md`. Both apply together.

### When to apply

Apply to any of these:
- A doc with 3+ sections
- A doc that will be reviewed by someone else
- A doc explaining a concept, system, or decision
- Any rewrite of an existing substantial doc

### When NOT to apply

- Meeting notes (nested bullets, no ToC)
- Check-in notes, action items, todo lists
- Single-section edits or patches
- Changelog entries, commit messages
- Daily Forge logs, system-retro logs, leaf content in `Forge/logs/`, `Learning/` chapters

### 1. First-principles structure

Use the first-principles agent's output format as the default skeleton for concept or explainer docs:

```markdown
## What is [x]?
[1-2 sentence definition anyone could understand]

## Why does it exist?
[The problem it solves, in plain terms]

## How does it work?
[Step-by-step, simple language]

## What this means for you
[Practical implications, specific actions]
```

For non-explainer docs (proposals, strategy, retros), the first-principles *discipline* still applies:
- Name the axioms you are reasoning from before reasoning from them
- Strip away assumptions, separate knowledge from assumption
- Start with the problem, not the solution
- End with action

Invoke the first-principles agent explicitly when drafting a technical concept doc. Use phrases like "explain X" or "what is Y" to trigger it.

### 2. Table of contents

Every substantial doc gets a ToC near the top.

For markdown docs, use a plain section list linking to anchors:

```markdown
## Contents
- [What is it?](#what-is-it)
- [Why it matters](#why-it-matters)
- [How it works](#how-it-works)
- [What this means](#what-this-means)
```

For Confluence pages, use the ToC macro (see `writing-style.md`).

Skip the ToC only if the doc has fewer than 3 sections.

### 3. Mermaid diagrams

Use a mermaid diagram whenever a relationship, flow, or structure would be faster to read as a picture than as prose. Specifically:
- Any system with 3+ components and connections between them
- Any decision flow or branching logic
- Any dependency or hierarchy
- Any sequence of steps with conditional paths

Keep diagrams honest:
- Node labels under 30 characters
- No literal `\n` or `<br/>` inside labels (split into separate nodes instead)
- Label the edges when the relationship type matters (`-->|uses|`, `-->|reads|`)
- One diagram per concept, not one mega-diagram

Skip the diagram if the relationship is linear or trivially obvious from the prose.

### 4. Simple language

Non-negotiable for every doc this rule applies to:
- Short sentences, one idea per sentence
- Active voice, "you" not "the user"
- No jargon without immediate definition
- No corporate filler ("leverage", "synergize", "robust solution", "at scale")
- Test: could a smart high schooler follow this? If not, simplify until they can

If you cannot explain it simply, you do not understand it well enough yet. Go back to first principles before writing more.

### Three-state permissions

Allow:
- Add a ToC to any substantial doc without asking
- Add a mermaid diagram when the relationship is non-linear
- Restructure a doc into first-principles skeleton when rewriting
- Invoke the first-principles agent for technical explainers

Ask:
- Before rewriting a doc the user wrote themselves in a different style
- Before removing sections from an existing doc to fit the skeleton

Deny:
- Never ship a substantial doc with no ToC, no structure, and dense jargon
- Never write a concept explainer without stating the axioms you are reasoning from

### Related rules

- `writing-style.md`: prose hygiene (sentence case, no em dashes, no bold, no LLM brands)
- `clarify-before-drafting.md`: run Socratic clarification before starting a substantial draft
- `communication-style.md`: read first-principles, socratic-questioning, objective-review skills before major interactions
- `first-principles.md` (agent): the mental model and output format this rule borrows from

The test: does my substantial doc have a ToC, first-principles structure, and language a smart high schooler could follow?

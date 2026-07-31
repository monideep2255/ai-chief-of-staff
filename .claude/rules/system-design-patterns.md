---
name: system-design-patterns
description: Mental models for designing agents, rules, and tools
scope: project
globs:
  - .claude/agents/**
  - .claude/rules/**
  - .claude/skills/**
depends_on: []
depended_by:
  - CLAUDE.md
  - DEPENDENCIES.md
---

## System design patterns

Five patterns to apply when creating or modifying agents, rules, or skills.

### 1. Three-state permissions (allow / deny / ask)

When writing a rule, explicitly bucket actions into three states:
- **Allow** - agent does this freely (read files, format notes)
- **Deny** - agent never does this (push to remote, run destructive commands)
- **Ask** - agent pauses and confirms first (delete files, create files, modify config, convert formats)

Don't write rules that are ambiguous about which state an action falls into.

**Applied to edits (the A/B/C taxonomy).** The same three states govern an agent that is modifying files, not just designing rules. When a file-modifying skill (`wiki-lint`, `os-maintain`, `docs-sync`) is about to change something, sort each fix into one of three tiers:

- **A, mechanical (allow):** unambiguous, no judgment. Fix silently. Examples: a broken link, a stale count, a frontmatter field with one correct value, a formatting fix.
- **B, clear-content (allow with a note):** the right fix is clear from context. Apply it, but say what you changed. Examples: a description that no longer matches the component, a missing index row whose content is obvious.
- **C, judgment (ask):** a real decision the agent should not make alone. Flag it, do not auto-fix. Examples: deleting a component, renaming an invocation, changing what a rule allows or denies, restructuring a folder.

The point: an agent must never make a tier-C change silently. When in doubt between B and C, treat it as C. This is a pattern worth adapting if you build a similar review skill.

The never-auto-destroy floor: a destructive change (deleting or overwriting existing content) is tier C regardless of how confident the fix looks. An automated fix may auto-apply only above a confidence floor, and destruction never clears that floor, it always drops to ask. Confidence tiers decide how fast a non-destructive fix moves; they never authorize a delete.

**Three principles for the permission layer itself.** When you design how permissions are evaluated (a hook, a settings allow/deny list, a skill's gating logic), adopt these three principles for the permission layer itself:

- Deny beats allow. When an allow rule and a deny rule both match, deny wins. Evaluate denies first and let them short-circuit. The `protect-files.sh` hook already works this way; make it the default for any new gate.
- Permissions are not restored on resume. A grant made in one run does not silently carry into the next. Re-authorize on resume rather than assuming prior consent still holds.
- Do not rely on the human reading every prompt. People approve the large majority of confirmation prompts without reading them, so safety that depends on a human catching a bad prompt is not safety. Prefer a deterministic deny rule (a hook, a removed tool) over a confirmation prompt whenever the bad action can be named in advance.

### 2. Snapshot before mutate

Before multi-file system changes (docs-sync, system-retro), log the current HEAD hash so there's a known revert point. One line in agent output is enough.

### 3. Specialize by tool access, not just prompt

The strongest constraint is removing the ability, not asking the agent not to use it. When designing a new agent, ask: should this agent be able to edit files? If not, restrict its tools list - don't just say "don't edit" in the prompt.

### 4. Output truncation for large results

When a tool output exceeds a useful size, write to disk and return a pointer (file path + line count + first N lines). Prevents silent truncation where the LLM hallucinates the rest.

When a pointer isn't practical and the output must be truncated inline, default to middle-elision: keep the head and the tail, drop the middle. An oversized result is usually a setup at the start and a conclusion or final state at the end, both of which end-truncation throws away. Reserve plain end-truncation for output that is genuinely append-only with no meaningful tail, like a live log stream.

If the full output cannot be retained, fail explicitly rather than return a truncated result as if complete. The pointer-plus-preview is the record of record, and the offloaded file is disposable.

### 5. The description is a routing contract, not a summary

A skill or subagent description is the only thing the agent sees before deciding whether to load it. If a component misfires, the description is wrong far more often than the body is. Write it as three parts: what the component does, when to use it (the literal trigger phrases a user would say), and a differentiator versus related components so routing does not collide.

The trap: never summarize the workflow in the description. If the description spells out the steps, the agent follows that summary and skips loading the body, so it runs a degraded version of the component. The description answers "should I open this now?", never "what are the steps?". This is the routing half of progressive disclosure, and it pairs with the standing principle that skill bodies never get inlined into always-on context (only name and description live there).

The test: when creating or modifying an agent, rule, or skill, did I apply all five patterns where each was relevant?

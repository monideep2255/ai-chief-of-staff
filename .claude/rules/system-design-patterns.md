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

Seven patterns to apply when creating or modifying agents, rules, or skills.

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

**Four principles for the permission layer itself.** When you design how permissions are evaluated (a hook, a settings allow/deny list, a skill's gating logic), adopt these four principles for the permission layer itself:

- Deny beats allow. When an allow rule and a deny rule both match, deny wins. Evaluate denies first and let them short-circuit. The `protect-files.sh` hook already works this way; make it the default for any new gate.
- Permissions are not restored on resume. A grant made in one run does not silently carry into the next. Re-authorize on resume rather than assuming prior consent still holds.
- Do not rely on the human reading every prompt. People approve the large majority of confirmation prompts without reading them, so safety that depends on a human catching a bad prompt is not safety. Prefer a deterministic deny rule (a hook, a removed tool) over a confirmation prompt whenever the bad action can be named in advance.
- Count the gates that bind, not the gates that exist. A hook that exits 0 with a warning is a suggestion, and a suggestion can be read and ignored in the same turn. Only a refusal is enforcement. Nine hooks and four refusals is four layers of protection, not nine, and any inventory that does not say which is which will be read as the larger number. Keep a hook inventory that classifies each hook as a binding gate or an advisory convenience, and record every open gap in it: a path guard that matches `Edit|Write` only, for instance, is walked past by a write routed through a Bash heredoc.

### 2. Snapshot before mutate

Before multi-file system changes (docs-sync, system-retro), log the current HEAD hash so there's a known revert point. One line in agent output is enough.

### 3. Specialize by tool access, not just prompt

The strongest constraint is removing the ability, not asking the agent not to use it. When designing a new agent, ask: should this agent be able to edit files? If not, restrict its tools list - don't just say "don't edit" in the prompt.

The pattern generalizes past file editing to any bound you want an agent to respect. A worked example: a reference crawling agent that bounds its crawl through the tool it is handed rather than through an instruction. The fetch tool itself enforces the host scope and the depth limit, so an agent that decides to follow one more link simply cannot, and the bound holds without depending on the agent having read or remembered it. Prompt-side, the same bound is a request the agent is free to reason its way past, and a sufficiently motivated chain of reasoning will.

The design question to ask of any constraint you are about to write into a prompt: could this be a property of the tool instead? Scope, depth, rate, allowed hosts, writable paths, and maximum result size are all enforceable at the tool boundary. Move each one there and the prompt stops carrying rules it cannot actually enforce.

### 4. Output truncation for large results

When a tool output exceeds a useful size, write to disk and return a pointer (file path + line count + first N lines). Prevents silent truncation where the LLM hallucinates the rest.

When a pointer isn't practical and the output must be truncated inline, default to middle-elision: keep the head and the tail, drop the middle. An oversized result is usually a setup at the start and a conclusion or final state at the end, both of which end-truncation throws away. Reserve plain end-truncation for output that is genuinely append-only with no meaningful tail, like a live log stream.

If the full output cannot be retained, fail explicitly rather than return a truncated result as if complete. The pointer-plus-preview is the record of record, and the offloaded file is disposable.

This pattern is written for tools you author, and it also governs the output you consume. The operating-habit half lives in the context-economy section of `parallel-first` with a stated threshold (roughly 500 lines or 20 KB), because a large read or command result costs the same whether the tool was yours or the harness's: written into context once, re-read on every turn after.

### 5. The description is a routing contract, not a summary

A skill or subagent description is the only thing the agent sees before deciding whether to load it. If a component misfires, the description is wrong far more often than the body is. Write it as three parts: what the component does, when to use it (the literal trigger phrases a user would say), and a differentiator versus related components so routing does not collide.

The trap: never summarize the workflow in the description. If the description spells out the steps, the agent follows that summary and skips loading the body, so it runs a degraded version of the component. The description answers "should I open this now?", never "what are the steps?". This is the routing half of progressive disclosure, and it pairs with the standing principle that skill bodies never get inlined into always-on context (only name and description live there).

### 6. Always-on components cost per turn, not once

Anything loaded into standing context (an always-on rule, the project instruction file, a tool schema, an MCP server's tool list) is re-sent on every single turn of every session. Its cost is recurring, not one-time. A 100-line rule that fires on one turn in fifty still bills on all fifty. This is why a rule set grows expensive quietly: each individual addition looks small, and nothing ever measures the total.

Four consequences for design:

- Glob-scope first. A new rule defaults to conditional loading (a `globs:` frontmatter field) unless it genuinely governs every turn. Always-on is the exception you justify, not the default you fall into. A rule that only matters inside one project folder should never load while you are editing an unrelated document.
- Measure the always-on set, do not assume it. The budget is a number you can check, so check it. Count the total lines across the rule set, split by whether each rule declares a `globs:` field, and add the length of `CLAUDE.md`, which rides along on every turn too. Record the number each cycle so the trend is visible.
- The same logic governs standing tool surfaces. Ten MCP servers exposing 50 tools cost their full schema on every turn whether or not any tool is called. `EXTENSIONS.md` already encodes the mechanism-choice side of this (hooks < skills < CLIs < MCP servers by context cost); this pattern is the component-design side.
- Prune on every model upgrade, do not only append. Standing instructions accumulate workarounds written for a weaker model: a fixed file-reading itinerary, a mandatory "run all tests" step, a blanket "ask before anything consequential". A more capable model follows them literally, so they cost context on every turn and can push it onto the wrong path or stall it where the owner expected it to proceed. When the main model changes, audit the always-on set for three things. First, procedural steps that protect nothing. Delete them. Second, blanket permission gates. Rewrite each as a decision boundary that names what is genuinely unsafe or irreversible and explicitly grants authority inside the safe area. Third, recipes that dictate the route. Replace each with a definition of done. Keep every security, production-access, compliance, and irreversible-action boundary.

Skill bodies are already exempt by design: only a skill's name and description live in standing context, and the body loads on invocation. That progressive-disclosure split is the pattern working correctly. Rules do not get it for free, so the glob scope is where you buy it.

### 7. Inert configuration is its own failure class

A setting that is defined, defaulted, documented, and read from user input, but never consulted by the code that should act on it, fails in a way neither testing nor review reliably catches. Everything about it looks correct. The default is sensible, the documentation is accurate, the value arrives intact. Nothing ever asks it a question.

This is worse than a missing feature, because configuration is a promise. Someone sets the value, believes the behavior changed, and gets the old behavior with no error and no warning. The bug then surfaces as a downstream symptom far from its cause.

The sibling failure is a bound that does not bound. A cache capped at 2000 entries constrains nothing when the entries are files of unbounded size; the honest cap is in bytes, with oversized single items served uncached rather than admitted. A limit expressed in the wrong unit reads as a safety control and provides none.

Two checks catch both, and both are mechanical rather than a judgment call:

- For every configuration key, name the line that reads it. Search for the key and confirm at least one consumer beyond its definition, its default, and its documentation. If you cannot name that line, the key is inert.
- For every declared bound, name its unit and ask whether that unit is the thing that can actually grow. Count-based bounds over variable-size items are the common trap.

One consequence to state up front: activating dead configuration is a behavior change, not a fix. Turning it on changes what the system does for everyone who was relying on the accidental behavior, so say so plainly when you do it rather than shipping it as a bug fix.

Two worked instances. The first is an agent runtime whose rule frontmatter fields for conditional loading are defined, documented, and honored by nothing, so every rule loads on every turn regardless of its declared scope; it was found by measurement, not by design review. The second is a pull-request review agent whose ignore-paths setting was defined, defaulted, documented, and merged from API input while never being consulted, so a 60,000-line generated lockfile flowed into every agent prompt and ran the process out of memory.

The test: when creating or modifying an agent, rule, or skill, did I apply all seven patterns where each was relevant, did I justify always-on loading rather than defaulting to it, and can I name the line that reads every setting I added?

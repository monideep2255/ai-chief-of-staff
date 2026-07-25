# Claude code configuration

This directory contains Claude Code configuration for this repository.

> **Note:** This folder is for **Claude Code** (claude.ai/code). For other assistants, use `AGENTS.md` in the repo root.

---

## Directory structure

```
.claude/
├── README.md                          # This file
├── rules/                             # Behavioral rules (glob-based conditional loading)
│   ├── communication-style.md
│   ├── response-calibration.md
│   ├── file-protection.md
│   ├── meeting-notes-format.md
│   ├── file-naming.md
│   ├── git-workflow.md
│   ├── boil-the-lake.md
│   ├── session-greeting.md
│   ├── writing-style.md
│   ├── book-inventory-check.md
│   ├── pdf-docx-conversion.md
│   ├── dependency-tracking.md
│   ├── pause-before-acting.md
│   ├── system-design-patterns.md
│   ├── attack-the-constraint.md
│   ├── decision-logging.md
│   ├── os-improvement-logging.md
│   ├── parallel-first.md
│   ├── npm-security-check.md
│   ├── preserve-your-thinking.md
│   ├── clarify-before-drafting.md
│   ├── doc-construction.md
│   ├── bossman-mode.md
│   ├── workflow-and-reference-awareness.md
│   ├── atlas-production-standards.md
│   ├── atlas-production-examples.md
│   ├── ai-security-standards.md
│   ├── anti-rationalization.md
│   ├── memory-provenance.md
│   ├── self-eval-loop.md
│   ├── goal-contracts.md
│   ├── sandbox-diagnosis.md
│   ├── agent-first-default.md
│   └── ship-clean-no-bait.md
├── agents/                            # Custom agents (auto-activated)
│   ├── action-planner.md
│   ├── code-reviewer.md
│   ├── docs-sync.md
│   ├── first-principles.md
│   ├── git-sync.md
│   ├── meeting-notes.md
│   ├── objective-review.md
│   └── socratic.md
└── skills/                            # Reusable expertise (loaded on-demand)
    ├── cs-research/SKILL.md
    ├── biomedical-research/SKILL.md
    ├── prompt-optimizer/SKILL.md
    ├── book-builder-hard-skills/SKILL.md
    ├── book-builder-soft-skills/SKILL.md
    ├── book-builder-from-sources/SKILL.md
    ├── forge/SKILL.md
    ├── board/SKILL.md                 # Empty advisor-slot template, no biographical content
    ├── eval-harness/SKILL.md
    ├── repo-dive/SKILL.md
    ├── deep-dive/SKILL.md
    ├── os-maintain/SKILL.md
    ├── ship/SKILL.md
    ├── wiki-lint/SKILL.md
    ├── system-retro/SKILL.md
    ├── ingest-workflows/SKILL.md
    ├── ingest-conference/SKILL.md
    ├── web-research/SKILL.md
    ├── systems-map/SKILL.md
    ├── bossman-mode/SKILL.md
    ├── checkin-notes/SKILL.md
    ├── first-principles/SKILL.md
    ├── objective-review/SKILL.md
    ├── socratic-questioning/SKILL.md
    ├── handoff/SKILL.md
    └── yt-learn/SKILL.md
```

This is a trimmed structure compared to a fully mature setup: no `hooks/`, `scripts/`, or `workflows/` folders ship in this example, since those are heavily tied to a specific machine and shell setup. If you build your own, `SYSTEM_OVERVIEW.md` describes where hooks and validation scripts would slot in.

---

## Rules

Rules are behavioral constraints that Claude Code loads automatically. They live in `.claude/rules/` with YAML frontmatter.

### Format
```yaml
---
description: "What this rule enforces"
alwaysApply: true          # true = always loaded, false = loaded by glob match
globs: ["Work/example-project/**"]     # Optional: only load when working with matching files
---

Rule content (markdown).
```

### Active rules

Full table with scope and enforcement details: [CLAUDE.md](../CLAUDE.md#rules)

### Adding a new rule
1. Create `.claude/rules/rule-name.md`
2. Include YAML frontmatter with `description`, `alwaysApply`
3. Optionally add `globs` for conditional loading
4. Document the new rule in this README

---

## Components compared

| Feature | Custom agents | Custom skills | Plugins | MCP servers |
|---------|--------------|---------------|---------|-------------|
| **Purpose** | Task delegation with specific roles | Portable expertise loaded on-demand | Installable packages of skills, agents, hooks | External tool integrations |
| **Location** | `.claude/agents/` | `.claude/skills/` | `~/.claude/plugins/cache/` (global) | `.mcp.json` + settings |
| **Activation** | Magic words or explicit request | Slash command or context match | Namespaced slash command (`/plugin:skill`) | Automatic tool discovery |
| **Context** | Own system prompt, tools, model | Instructions injected into current context | Same as skills/agents but namespaced | Tool definitions only |
| **Scope** | This project only | This project only | All projects | Per config file |
| **Best for** | Specialized workflows (meeting notes, planning) | Procedural knowledge (explanation style) | General dev processes (TDD, debugging) | External APIs and databases |

> Full extension architecture: [EXTENSIONS.md](../EXTENSIONS.md)

---

## Agents

Custom agents are invoked automatically based on trigger phrases or explicitly by request.

### Format
```markdown
---
name: agent-name
description: When this agent should be invoked
tools: tool1, tool2, tool3    # Optional - omit to inherit all
model: sonnet                  # Optional - sonnet, opus, or haiku
---

System prompt with role, capabilities, and approach.
```

### Available agents

Full table with trigger words and descriptions: [CLAUDE.md](../CLAUDE.md#sub-agents)

### Usage

**Automatic:** Just use the trigger words in conversation.
```
"I had a meeting with a stakeholder today about the Atlas rollout..."
→ meeting-notes agent activates
```

**Explicit:** Request a specific agent.
```
"Use the first-principles agent to explain the memory system"
```

---

## Skills

Skills provide reusable expertise that Claude loads dynamically when relevant.

### Format
```
skills/
└── skill-name/
    └── SKILL.md          # Required - contains frontmatter + instructions
```

```markdown
---
name: skill-name
description: Brief description of what this skill does and when to use it
---

Instructions, examples, and reference material.
```

### Available skills

Full table with invocations and descriptions: [CLAUDE.md](../CLAUDE.md#skills)

Skills are organized into communication (first-principles, socratic-questioning, objective-review), research (cs-research, biomedical-research, web-research), and workflow (everything else) categories. All skills use the standard `skill-name/SKILL.md` subdirectory format.

### How skills work

1. **Metadata loads first** (~100 tokens) - Claude scans descriptions
2. **Full instructions load** (<5k tokens) - When skill is relevant
3. **Bundled files load** - Only as needed

This "progressive disclosure" keeps context efficient while providing deep expertise.

---

## Communication preferences

Both agents and skills enforce these core principles:

### First principles thinking
- Break concepts to fundamental truths
- Strip away assumptions
- Use simple, jargon-free language
- Include concrete action items

### Socratic questioning
- Ask one clarifying question at a time before answering
- Challenge assumptions gently
- Explore alternatives
- Help clarify thinking before solving

### Writing style
- Short sentences, concrete examples, active voice
- Specific action items with WHO, WHAT, WHEN
- Avoid corporate buzzwords, vague suggestions, passive voice

**Example:**
- "Leverage the Atlas infrastructure to facilitate cross-functional synergies" -- avoid this
- "Use Atlas to help different teams share information more easily" -- do this

---

## Storage locations

| Location | Scope | Purpose |
|----------|-------|---------|
| `~/.claude/` | User-level | Personal config across all projects |
| `.claude/` (this folder) | Project-level | Project-specific agents, skills, and rules |
| `.mcp.json` (repo root, if you add one) | Project-level | MCP server configuration |

Project-level agents/skills take precedence over user-level when names conflict.

---

## Related files

- **CLAUDE.md** (repo root) - Slim index for Claude Code: Current focus table plus sub-agents, skills, rules. Full context → AGENTS.md
- **AGENTS.md** (repo root) - Universal AI context for non-Claude-Code agents: current focus, fabricated example projects, links. Mirrors CLAUDE.md structure
- **GETTING_STARTED.md** (repo root) - Fork-and-run walkthrough for a first-time user
- **EXTENSIONS.md** (repo root) - How plugins, MCP servers, and custom components connect
- **SYSTEM_OVERVIEW.md** (repo root) - Full granular system reference: every component, session lifecycle, self-maintenance
- **`.claude/agents/`** - Canonical location for all agents
- **`.claude/skills/`** - Canonical location for all skills

---

## Maintenance

### Adding a new agent
1. Create `agents/agent-name.md`
2. Include YAML frontmatter with `name`, `description`
3. Optionally specify `tools` and `model`
4. Document trigger words in system prompt
5. Document the new agent in this README

### Adding a new skill
1. Create directory `skills/skill-name/`
2. Create `skills/skill-name/SKILL.md`
3. Include YAML frontmatter with `name`, `description`
4. Keep under 5k tokens for optimal loading
5. Document the new skill in this README

### Best practices
- **Agents:** Use for specialized workflows with distinct roles
- **Skills:** Use for portable expertise any agent can apply
- **Keep descriptions clear:** Claude uses them to decide when to activate
- **`.claude/` is canonical**  -  agents and skills live here only

---

*Last updated: example date, replace with your own*

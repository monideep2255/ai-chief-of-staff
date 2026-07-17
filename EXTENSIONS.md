# Extensions

How plugins, MCP servers, and this repo's own custom skills and agents fit together. This doc explains the pattern, not a fixed list to copy. It uses illustrative, generic examples instead of a hardcoded vendor list, because the whole point of this repo is that you fork it and wire up whichever tools you actually use.

## Contents

- [Quick answer](#quick-answer)
- [What is a plugin](#what-is-a-plugin)
- [What is an MCP server](#what-is-an-mcp-server)
- [How both differ from this repo's custom skills and agents](#how-both-differ-from-this-repos-custom-skills-and-agents)
- [Components compared](#components-compared)
- [Illustrative example plugins](#illustrative-example-plugins)
- [Illustrative example MCP servers](#illustrative-example-mcp-servers)
- [Supply chain security when adding a new extension](#supply-chain-security-when-adding-a-new-extension)
- [Adding a new extension to this fork](#adding-a-new-extension-to-this-fork)
- [Replace this file](#replace-this-file)

## Quick answer

A plugin is an installable package of skills, agents, and hooks. It works across every project on your machine, not just this one. An MCP server is a small connector, configured in a file, that gives the agent access to one external tool or API. Both are different from this repo's own `.claude/skills/` and `.claude/agents/`, which are custom, project-scoped, and version-controlled here. All three load into the same session and can be used together.

## What is a plugin

A plugin is a bundle you install once, globally, and it becomes available in any project you open. Think of it as a shared toolbox: a general-purpose skill for test-driven development, a debugging workflow, a documentation-lookup helper. Plugins are namespaced, so a plugin skill is invoked as `/plugin-name:skill-name`, which keeps it from colliding with a skill of the same short name in a different plugin.

Key traits:

- Installed once, available everywhere. Not tied to this repo.
- Namespaced invocation, so names cannot collide across plugins.
- General-purpose. A plugin has no idea this repo exists, what Atlas is, or what Meridian's conventions are.
- Enabled or disabled through your global Claude Code settings, not through anything in this repo.

## What is an MCP server

MCP stands for Model Context Protocol. An MCP server is a small adapter that exposes one external system, a note-taking app, a meeting-transcript store, a web-search API, as a set of callable tools. You configure it once in a config file (project-level `.mcp.json` or a global settings file), and from then on the agent can call its tools automatically when the task calls for them. There is no slash command and no magic word. The agent just recognizes when a tool is relevant and calls it.

Key traits:

- Configured, not installed as a package. A JSON entry with a command to run and, often, environment variables for credentials.
- Provides access to one external system per server. It does not know your conventions, only the raw API surface of the thing it connects to.
- Every MCP server's tool definitions load into context at session start, before you type a single message. This is a real cost. Prefer a plain command-line tool over a standing MCP server whenever one exists that does the same job, and only add an MCP server when there is no CLI equivalent for the system you need.
- Credentials belong in environment variables referenced from the config file, never as literal values inside it.

## How both differ from this repo's custom skills and agents

This repo's `.claude/skills/` and `.claude/agents/` are neither plugins nor MCP servers. They are custom, hand-written, and scoped to this project:

- No install step. They are markdown files that live in this repo and are version-controlled alongside everything else.
- No namespace prefix. A custom skill is called with a plain `/skill-name`, and a custom agent activates on a magic word in conversation, because there is no risk of colliding with a plugin's namespaced command.
- Project-specific knowledge baked in. A custom skill knows this repo's file-naming rules, its writing style, its folder layout. A plugin or an MCP server knows none of that.
- They are the layer where you encode how Atlas and Meridian actually work, which no generic plugin or MCP server can do for you.

## Components compared

| Component | Purpose | Location | Activation | Scope | Best for |
|-----------|---------|----------|------------|-------|----------|
| Custom agent | Encodes a repeatable, project-aware task with its own tool access | `.claude/agents/` in this repo | Magic words in conversation | This repo only | Formatting meeting notes, running this repo's own review conventions |
| Custom skill | Encodes a repeatable workflow with explicit steps | `.claude/skills/` in this repo | Plain slash command, e.g. `/ship` | This repo only | Multi-step workflows specific to this project, like a docs-sync pass |
| Plugin | Installable bundle of general-purpose skills, agents, and hooks | Global plugin cache, outside this repo | Namespaced slash command, or auto-spawned agent | Every project on the machine | General dev process: TDD conventions, debugging method, code review scoring |
| MCP server | Connector that exposes one external tool or API as callable tools | `.mcp.json` (project) or global settings | Called automatically when relevant, no slash command | The one external system it connects to | Reaching a note-taking app, a transcript store, or a search API that has no CLI equivalent |

## Illustrative example plugins

These rows are patterns, not products. Swap in whatever plugin you actually install.

| Example plugin category | What it provides | Type |
|--------------------------|-------------------|------|
| General dev-workflow bundle | Shared conventions for test-driven development, systematic debugging, and brainstorming, usable in any codebase | Skills |
| Documentation-lookup helper | Fetches current library or framework documentation on demand, so answers reflect the library's latest API instead of stale training knowledge | Skill, backed by an MCP server |
| Code review bundle | Reviews a diff for bugs and quality issues with confidence-based scoring, independent of any project's own conventions | Skills and agents |

## Illustrative example MCP servers

Again, generic by capability. Replace with the real connectors you use.

| Example MCP server category | What it connects to | Typical use |
|-------------------------------|----------------------|--------------|
| Note-taking or knowledge-base server | A personal or team notes app (pages, search, comments) | Look up a past decision, pull a reference doc into a session |
| Meeting-transcript server | A meeting recorder or transcription service | Pull a transcript or summary from a recent call into meeting notes |
| Web-search or fetch server | A search or page-fetch API | Answer a question that needs current information the agent was not trained on |

## Supply chain security when adding a new extension

A plugin and an MCP server are both executable code that runs with your credentials and file access. Before adding either one, this repo's own `.claude/rules/npm-security-check.md` rule governs the mechanical checks: confirm the package has not been reported compromised, verify the exact version before installing, inspect any install-time scripts, and run an audit tool afterward. Treat an `npx`-style invocation in an MCP config the same as a global package install and pin an exact version rather than trusting a floating tag.

`.claude/rules/ai-security-standards.md` governs the broader posture: least privilege for whatever credential the new connector uses, an inventory entry with an accountable owner before connecting it to anything that touches real data, and a human approval step before the connector is trusted to run, not just enabled. Read both rules in full before wiring up a real plugin or MCP server in your fork. They are the enforcement mechanism this file defers to, not a summary to skim instead of reading them.

## Adding a new extension to this fork

1. Decide which of the four rows in the components-compared table above actually fits the capability you want. A general dev process is a plugin. A one-off external system is an MCP server. Anything specific to how your project works is a custom skill or agent.
2. Run the supply chain checks above before installing a plugin or configuring an MCP server.
3. Configure it: a plugin through your global plugin settings, an MCP server through `.mcp.json` or your global settings file, with credentials as environment variable references only.
4. Update the tables in this file so future sessions and future forkers know what is actually wired up.

## Replace this file

This file is a worked example, not a real inventory. Once you fork this repo and connect your own plugins and MCP servers, replace the two illustrative tables above with your actual setup. Nothing in this file should still describe a generic category once you have real tools connected.

*Last updated: example date, replace with your own*

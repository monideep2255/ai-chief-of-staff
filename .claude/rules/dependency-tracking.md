---
description: "Dependency tracking: every component declares what it depends on and what depends on it, and you check before committing"
scope: project
alwaysApply: true
depends_on: [DEPENDENCIES.md]
depended_by: [CLAUDE.md, .claude/README.md]
---

## Dependency tracking

Every active component file (skill, agent, rule, config) must include `depends_on` and `depended_by` fields in its frontmatter. Leaf reference docs are exempt (see "Exempt: leaf reference docs" below).

```yaml
depends_on: [list of files or folders this component reads, references, or requires]
depended_by: [list of files that must be updated when this component changes]
```

Exempt, leaf reference docs: reference content that reads no other component and is only pointed *to* (never *from*) does not need per-file `depends_on`/`depended_by`. This covers your own workflow reference docs folder, if you have one (listed by `workflow-and-reference-awareness.md` and its folder README) plus the leaf-content folders under "Before committing" below. Their reverse edges live at folder level in `DEPENDENCIES.md`, so per-file fields would only restate the folder map. Skip them.

When to add:
- Creating a new component - add both fields from the start
- Modifying a component - check if dependencies changed and update both fields
- When a NEW file starts referencing an existing component, update the existing component's `depended_by`

What counts as a dependency:
- `depends_on`: config files it reads, other skills/agents it invokes, folders it scans, rules it follows
- `depended_by`: index files that list it (CLAUDE.md, AGENTS.md, README.md, .claude/README.md), other components that reference it

For files without YAML frontmatter (workflows, reference docs, configs): use a markdown comment at the top:

```markdown
<!-- depends_on: [file1, file2] -->
<!-- depended_by: [file1, file2] -->
```

For YAML configs (Forge/config.yaml, ai-digest/config.yaml): use a comment block:

```yaml
# depends_on: [file1, file2]
# depended_by: [file1, file2]
```

Also update the central map:
- When creating a new component, add it to the relevant tables in `DEPENDENCIES.md`
- When deleting a component, use the Deletion checklist in `DEPENDENCIES.md` to find all files that need updating
- When adding a new folder or relationship type, add it to the Folder-level dependencies table
- `DEPENDENCIES.md` is the source of truth for deletions and multi-hop cascades. Distributed `depends_on`/`depended_by` fields are the source of truth for modifications.

Keep it honest:
- Only list direct dependencies (1 hop), not transitive ones
- Use relative paths from repo root
- Update when you notice drift - don't let it go stale

## Before committing system components

Before committing any change to a system component (skill, agent, rule, workflow, config, index file):

1. Read the `depended_by` field on every file you modified
2. Walk each dependency and update it if needed
3. Don't rely on memory or the routing table alone - check the actual field

Triggers that force the walk: the walk is not "when you remember." It fires whenever a change touches the interface another component reads. Run it when you:

- Rename, add, or remove a skill's invocation, magic words, or trigger phrases
- Change a rule's glob scope, trigger conditions, or the actions it allows/denies
- Change a config schema (a field name, type, or default that another file reads)
- Rename or move a component, or change a path other components reference
- Change the output shape or contract a downstream component consumes

This is the same principle good code-review practice enforces as "caller impact analysis": when a public symbol changes, check every unchanged caller. Here the callers are the files listed in `depended_by`.

Skip for leaf content: files in these folders are endpoints, nothing depends on them:

- Your own meeting-notes and check-in folder (leaf content, not referenced by anything else)
- `Forge/logs/` (daily, weekly, system-retro logs)
- `Forge/exercises/` (portfolio artifacts)
- Your own cohort or course-notes folder, if you keep one (leaf content)
- Your own career or job-search docs folder, if you keep one (leaf content)
- `Learning/` chapters (individual book chapters, not book-inventory-check.md)

If you're only committing leaf content, go straight to commit. No dependency walk needed.

The test: did I check depended_by on every modified system component before committing?

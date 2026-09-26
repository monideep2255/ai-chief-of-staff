---
description: "Public repository privacy: what never gets committed, how to commit safely, and what to do if something slips"
scope: portable
alwaysApply: true
depends_on:
  - .claude/rules/git-workflow.md
  - .claude/rules/file-protection.md
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Public repository privacy

This repository is public. Everything committed to it, including its full history, every commit message, and every author record, is world-readable and effectively permanent. A later force-push or a deleted file does not undo a public commit: assume anything that ever landed in this repository stays reachable somewhere, forever.

### Never commit

- Secrets: API keys, tokens, passwords, connection strings, private certificates. Use environment variables at runtime, and ship a placeholder example file (`env.example`, not `.env.example`) instead of a real one.
- Personal data about anyone: full names, contact details, health information, family circumstances, or any other private fact about a real person, whether that person is the repository owner or someone else.
- Employer-internal material: proprietary code, internal documentation, roadmaps, org charts, or anything covered by an employer's confidentiality terms.
- Colleague names: a coworker, manager, or collaborator's real name or identifying detail. Use a role label or a generic placeholder instead.
- Local machine paths: any path that reveals a real username, a real home directory, or the layout of a specific machine.
- Private repository names: the name of a private repository this public one was derived from, synced from, or references.
- Server addresses: internal hostnames, IP addresses, or endpoints that are not meant to be public.

Use a generic placeholder in every one of these cases rather than a real value. A fabricated example that shows the shape of the thing does the same teaching job as a real one, without the exposure.

### Committing safely

Commit with a GitHub no-reply address, never a real email address. Never bypass a pre-commit hook with `--no-verify`, even when it is inconvenient in the moment. A hook that blocks a commit is very likely blocking it for a reason covered by this rule, and skipping it removes the one automated check standing between a mistake and a permanent public record.

### If something slips through

Remove the exposed content and tell the owner immediately, in plain terms: what leaked, where, and for how long it was live. If the leak was a secret (a key, a token, a credential), rotate it at once. Do not wait for a convenient moment. A secret that was ever visible in a public repository must be treated as compromised even after the commit is removed, because history and forks can outlive the fix.

The test: before committing to this repository, did I check the diff for secrets, personal data, employer-internal material, colleague names, local paths, private repository names, and server addresses, and did I use a generic placeholder wherever a real value would otherwise appear?

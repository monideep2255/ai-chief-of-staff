---
name: ship
author: human
description: "Sync documentation, clean the working tree, and push the repository to GitHub. Use when the user says: /ship, \"ship it\", \"push this\", \"commit and push\", \"sync to GitHub\", \"we are done, ship\". This is the path for work and content changes. When an OS system component changed (a rule, skill, agent, hook, or config), run /os-maintain first, then this."
scope: portable
user_invocable: true
agent: true
model: sonnet
depends_on:
  - .claude/agents/docs-sync.md
  - .claude/agents/git-sync.md
  - .claude/skills/ship/clean-cc-writes.py
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - .claude/skills/checkin-notes/SKILL.md
  - .claude/skills/ingest-workflows/SKILL.md
---

# /ship - sync docs + push to GitHub

Run these stages in sequence:

## Step 1: docs sync

Use the `docs-sync` sub-agent to synchronize all documentation files.

Read `.claude/agents/docs-sync.md` for the full agent instructions. Key points:
1. Run `git diff --name-only HEAD~1` (or `git status --short` if uncommitted changes exist)
2. Use the routing table to identify affected docs
3. Read only affected docs
4. Make surgical edits  -  never rewrite files
5. Report what changed

## Step 2: clean the working tree

After docs-sync, remove two kinds of litter so they do not pile up in the working tree: Claude Code's empty `.cc-writes` staging folders, and macOS `.DS_Store` files. Standing owner permission was granted for the `.cc-writes` cleanup and the `.DS_Store` cleanup, so run this without asking.

Run the cleanup script with the sandbox disabled (the `.cc-writes` paths sit on the sandbox protected list, so deletion is denied under the sandbox):

```bash
python3 .claude/skills/ship/clean-cc-writes.py
```

How each pass stays safe:

- `.cc-writes` folders: the script uses `os.rmdir`, which removes empty directories only, so it can never delete a folder that holds a real file, and the main `.claude/` is never empty so it stays protected. It also removes any spurious `.claude` parent left empty.
- `.DS_Store` files: `os.remove` is a real unlink, so the guard is the match instead. The basename must be exactly `.DS_Store`, and the path must be a regular file, never a directory and never a symlink. macOS regenerates these on folder access, so removing them loses nothing.

Both passes skip symlinked directories, which keeps the walk out of any external repos referenced from this repo. Both kinds of file are gitignored, so this step changes nothing in the commit; it only keeps the tree clean.

## Step 3: git sync

After the cleanup, use the `git-sync` sub-agent to commit and push.

Read `.claude/agents/git-sync.md` for the full agent instructions. Key points:
1. `git add` all changed files
2. Show the user what's being committed
3. Commit with a clear, descriptive message
4. **NEVER add Co-Authored-By lines**
5. `git push` to origin
6. Report commit hash and sync status

## Important

- Always run docs-sync BEFORE git-sync (docs may create additional changes to commit)
- Run the working-tree cleanup (.cc-writes folders and .DS_Store files) after docs-sync and before git-sync so the tree is clean before the commit
- If docs-sync reports "no changes needed", still run the cleanup and git-sync if there are uncommitted changes
- If nothing to commit at all, report that and stop

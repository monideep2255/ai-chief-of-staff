---
name: ship
author: human
description: "Sync documentation, clean the working tree of staging folders and scratch files, and push the repository to GitHub. Use when the user says: /ship, \"ship it\", \"push this\", \"commit and push\", \"sync to GitHub\", \"we are done, ship\". This is the path for work and content changes. When an OS system component changed (a rule, skill, agent, hook, or config), run /os-maintain first, then this."
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

After docs-sync, remove three kinds of litter so they do not pile up in the working tree: Claude Code's empty `.cc-writes` staging folders, macOS `.DS_Store` files, and agent scratch files written inside the repository instead of the session scratchpad. Standing owner permission was granted for all three, so run this without asking.

Run the cleanup script with the sandbox disabled (the `.cc-writes` paths sit on the sandbox protected list, so deletion is denied under the sandbox):

```bash
python3 .claude/skills/ship/clean-cc-writes.py
```

Add `--dry-run` to list what would go without deleting anything. Use it when the scratch pass reports something you did not expect.

How each pass stays safe:

- `.cc-writes` folders: the script uses `os.rmdir`, which removes empty directories only, so it can never delete a folder that holds a real file, and the main `.claude/` is never empty so it stays protected. It also removes any spurious `.claude` parent left empty.
- `.DS_Store` files: `os.remove` is a real unlink, so the guard is the match instead. The basename must be exactly `.DS_Store`, and the path must be a regular file, never a directory and never a symlink. macOS regenerates these on folder access, so removing them loses nothing.
- Scratch files and folders: three guards, because this pass has neither of the protections above. The match is anchored, git decides what is real, and vendored trees are pruned. Each one is spelled out below.

What the scratch pass matches, always as a whole name and never as a substring:

- Folders named exactly `scratch`, `scratchpad`, `_scratch`, `tmp`, `temp`, `_tmp`, or `_temp`
- Files whose stem before the first extension is exactly `scratch`, `scratchpad`, `temp`, or `tmp`, so `tmp.json` matches and `templates.py` does not
- Files whose stem starts with `untitled`, which covers the `Untitled 2.md` shape editors produce
- Files ending in `.tmp`, `.temp`, `.bak`, `.orig`, `.swp`, `.swo`, or `~`

Anchoring is the load-bearing guard, not a refinement. A substring match on `temp` or `scratch` hits real work in almost any repository: a `_templates/` folder, a document about temporal data, and every `tmpdir.py` inside a virtualenv.

Git decides what is real. A scratch-named path that git tracks is printed under `REPORTED, NOT DELETED` and left alone, because a file committed on purpose may hold real work whatever it is named. Read that list and decide each one yourself; the script never makes that call. If the git index cannot be read, the whole scratch pass is skipped and the script exits 1, since without the tracked set every match would look deletable.

Vendored dependency trees and transient working copies are pruned from the walk entirely: any `.git`, `node_modules`, `venv`, `.venv`, `env`, `site-packages`, `__pycache__`, or `worktrees` folder.

All three passes skip symlinked directories, which keeps the walk out of any external repos referenced from this repo. Everything the script deletes is gitignored or untracked, so this step changes nothing in the commit; it only keeps the tree clean.

## Step 3: git sync

After the cleanup, use the `git-sync` sub-agent to commit and push.

Read `.claude/agents/git-sync.md` for the full agent instructions. Key points:
1. `git add` all changed files
2. Show the user what's being committed
3. Commit with a clear, descriptive message
4. **NEVER add Co-Authored-By lines**
5. `git push` to origin
6. Report commit hash and sync status

## Exit checklist

Do not report the ship as done until every line is checked. A step that could not run is unrun, not passed, and is reported as such per `.claude/rules/goal-contracts.md`.

- [ ] docs-sync ran, and every doc the routing table flagged was either edited or explicitly ruled out
- [ ] Any verification script this repo runs exited 0, and the exit code checked is the script's own. Piping a script through `tail` or `head` and reading `$?` returns the pipe's status, not the script's, which is how a red gate reads as green
- [ ] `clean-cc-writes.py` ran and exited 0, its output carried no `WARNING:` line, and the working tree holds no stray `.cc-writes` folders, `.DS_Store` files, or scratch files and folders. A `WARNING:` means a pass found targets and removed none, which is unrun rather than clean; the usual cause is the sandbox blocking `.cc-writes`, so re-run with it disabled
- [ ] Every path under `REPORTED, NOT DELETED` was read and ruled on, not scrolled past. A tracked scratch file is either real work that needs a better name or litter you delete by hand; leaving it unexamined is neither
- [ ] `git status --short` is clean, or every remaining entry is deliberate and named to the user
- [ ] Unrelated concerns went into separate commits, per `.claude/rules/git-workflow.md`
- [ ] No commit message carries a `Co-Authored-By` line
- [ ] Nothing being reported as shipped lives on a gitignored path
- [ ] `git rev-parse HEAD origin/main` returns identical hashes, which is the evidence the push actually reached the remote

## Important

- Always run docs-sync BEFORE git-sync (docs may create additional changes to commit)
- Run the working-tree cleanup (.cc-writes folders, .DS_Store files, and scratch files and folders) after docs-sync and before git-sync so the tree is clean before the commit
- Never widen the scratch patterns to a substring match to catch one more file. The anchored match is what keeps a `_templates/` folder and every virtualenv `tmpdir.py` alive, and widening it to reach a stubborn file is the verify-surface change `goal-contracts` forbids. Add a new whole-name pattern instead
- If docs-sync reports "no changes needed", still run the cleanup and git-sync if there are uncommitted changes
- If nothing to commit at all, report that and stop

#!/usr/bin/env python3
# depends_on: []
# depended_by: [.claude/skills/ship/SKILL.md]
"""Remove working-tree litter before a commit. Three passes over one walk:

1. Claude Code's empty .cc-writes staging folders, plus any .claude parent they
   leave empty.
2. macOS .DS_Store files.
3. Agent scratch files and folders written inside the repository instead of the
   session scratchpad.

The safety argument differs per pass, so each one is stated separately.

.cc-writes folders are safe by construction: os.rmdir removes only empty
directories, so no folder that holds a real file can ever be deleted. The main
repo .claude/ is never empty (it holds rules, agents, skills), so it is
inherently protected with no hardcoded allowlist.

.DS_Store files are deleted with os.remove, which is a real unlink, so the guard
is the match instead: the basename must be exactly ".DS_Store", and the path must
be a regular file, never a directory and never a symlink. macOS regenerates these
on folder access, so removing them loses nothing.

Scratch paths have neither protection, so they carry three guards of their own.

First, every match is anchored, never a substring. A substring match on "temp" or
"scratch" hits real work in almost any repository: a _templates/ folder, a
document about temporal data, and every tmpdir.py inside a virtualenv. A name
therefore matches only as a whole basename, a whole stem before the first
extension, or a whole trailing suffix.

Second, git decides what is real. A path git tracks is reported and never
deleted, because a file committed on purpose may hold real work whatever it is
named. The owner decides each of those individually.

Third, external checkouts and vendored dependency trees are pruned from the walk
entirely, so this never reaches into a repository that is not ours.

All three passes use followlinks=False, which keeps the walk out of any symlinked
external repositories.

Standing owner permission was granted 2026-07-15 for the .cc-writes cleanup,
2026-07-25 for the .DS_Store cleanup, and 2026-09-20 for the scratch cleanup, so
/ship runs this without asking. Run it with the sandbox disabled: the .cc-writes
paths are on the sandbox protected list, so deletion is denied under the sandbox.

Usage:
    python3 .claude/skills/ship/clean-cc-writes.py [--dry-run]
"""
import os
import shutil
import subprocess
import sys

# repo root is four levels up: .claude/skills/ship/clean-cc-writes.py
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

DS_STORE = ".DS_Store"

# Scratch pass, pattern set. Every entry matches whole, never as a substring.

# A directory whose basename is exactly one of these, case-insensitive.
SCRATCH_DIR_NAMES = frozenset(
    {"scratch", "scratchpad", "_scratch", "tmp", "temp", "_tmp", "_temp"}
)

# A file whose stem before the first extension is exactly one of these, so
# scratch.md, tmp.json and temp.py match while templates.py and temporal.md
# do not. Any stem starting with "untitled" also matches, which covers the
# "Untitled 2.md" shape editors produce.
SCRATCH_FILE_STEMS = frozenset({"scratch", "scratchpad", "temp", "tmp", "untitled"})

# A file whose basename ends with one of these.
SCRATCH_SUFFIXES = (".tmp", ".temp", ".bak", ".orig", ".swp", ".swo", "~")

# Never matched as scratch whatever else the rules say. .DS_Store has its own
# pass above, and the git housekeeping files are load-bearing.
SCRATCH_NEVER = frozenset(
    {".gitignore", ".gitkeep", ".gitattributes", ".ds_store"}
)

# Directory basenames pruned from the walk: vendored dependency trees and
# transient working copies. Nothing under these is ours to delete.
PRUNE_DIR_NAMES = frozenset(
    {
        ".git",
        "node_modules",
        "venv",
        ".venv",
        "env",
        "ENV",
        "site-packages",
        "__pycache__",
        "worktrees",
    }
)

# Repository-relative roots pruned from the walk: external checkouts that sit
# inside this tree but belong to other repositories. This repository nests none,
# so the list is empty; the is_pruned() mechanism stays so adding one is one line.
PRUNE_REL_ROOTS = ()


def is_pruned(rel_dir):
    """True when this repo-relative directory sits under an external checkout."""
    if rel_dir in (".", ""):
        return False
    for root in PRUNE_REL_ROOTS:
        if rel_dir == root or rel_dir.startswith(root + os.sep):
            return True
    return False


def tracked_paths():
    """Every repo-relative path git tracks. The arbiter of what is real work."""
    out = subprocess.run(
        ["git", "-C", REPO_ROOT, "ls-files", "-z"],
        capture_output=True,
        check=True,
    )
    return {p for p in out.stdout.decode("utf-8", "surrogateescape").split("\0") if p}


def is_scratch_file(name):
    lowered = name.lower()
    if lowered in SCRATCH_NEVER:
        return False
    if lowered.endswith(SCRATCH_SUFFIXES):
        return True
    stem = lowered.split(".", 1)[0]
    return stem in SCRATCH_FILE_STEMS or stem.startswith("untitled")


def find_targets():
    """One walk, four target lists: .cc-writes, .DS_Store, scratch dirs, files."""
    cc_dirs = []
    ds_files = []
    scratch_dirs = []
    scratch_files = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT, followlinks=False):
        rel_dir = os.path.relpath(dirpath, REPO_ROOT)
        if is_pruned(rel_dir):
            dirnames[:] = []
            continue
        if ".cc-writes" in dirnames:
            cc_dirs.append(os.path.join(dirpath, ".cc-writes"))
        if DS_STORE in filenames:
            ds_files.append(os.path.join(dirpath, DS_STORE))

        keep = []
        for d in dirnames:
            if d in PRUNE_DIR_NAMES:
                continue  # vendored or transient: neither walked nor matched
            if d.lower() in SCRATCH_DIR_NAMES:
                scratch_dirs.append(os.path.join(dirpath, d))
                continue  # matched whole, so the folder is judged as one unit
            keep.append(d)
        dirnames[:] = keep

        for f in filenames:
            if is_scratch_file(f):
                scratch_files.append(os.path.join(dirpath, f))
    return cc_dirs, ds_files, scratch_dirs, scratch_files


def remove_cc_writes(cc_dirs, dry_run=False):
    removed = []
    for cc in cc_dirs:
        if dry_run:
            removed.append(cc)
            continue
        try:
            os.rmdir(cc)  # empty-only; raises OSError if it holds anything
            removed.append(cc)
        except OSError as e:
            print(f"skip (not empty or gone): {cc} ({e})", file=sys.stderr)
            continue
        parent = os.path.dirname(cc)  # the .claude dir that held it
        if (
            os.path.basename(parent) == ".claude"
            and os.path.isdir(parent)
            and not os.listdir(parent)
        ):
            os.rmdir(parent)
            removed.append(parent)
    return removed


def remove_ds_store(ds_files, dry_run=False):
    removed = []
    for ds in ds_files:
        # Guard the unlink: exact name, regular file, never a symlink.
        if os.path.basename(ds) != DS_STORE:
            continue
        if os.path.islink(ds) or not os.path.isfile(ds):
            print(f"skip (not a regular file): {ds}", file=sys.stderr)
            continue
        if dry_run:
            removed.append(ds)
            continue
        try:
            os.remove(ds)
            removed.append(ds)
        except OSError as e:
            print(f"skip (could not remove): {ds} ({e})", file=sys.stderr)
    return removed


def remove_scratch(scratch_dirs, scratch_files, tracked, dry_run=False):
    """Delete untracked scratch matches. Report tracked ones, never delete them.

    Returns (removed, reported). A tracked match is something committed on
    purpose, so the call to remove it stays with the owner.
    """
    removed = []
    reported = []

    for path in scratch_files:
        rel = os.path.relpath(path, REPO_ROOT)
        if rel in tracked:
            reported.append(rel)
            continue
        if os.path.islink(path) or not os.path.isfile(path):
            print(f"skip (not a regular file): {rel}", file=sys.stderr)
            continue
        if dry_run:
            removed.append(path)
            continue
        try:
            os.remove(path)
            removed.append(path)
        except OSError as e:
            print(f"skip (could not remove): {rel} ({e})", file=sys.stderr)

    for path in scratch_dirs:
        rel = os.path.relpath(path, REPO_ROOT)
        prefix = rel + "/"
        held = sorted(t for t in tracked if t == rel or t.startswith(prefix))
        if held:
            reported.append(
                f"{rel}/ holds {len(held)} tracked file(s), first is {held[0]}"
            )
            continue
        if os.path.islink(path):
            print(f"skip (symlink): {rel}", file=sys.stderr)
            continue
        if dry_run:
            removed.append(path)
            continue
        try:
            shutil.rmtree(path)
            removed.append(path)
        except OSError as e:
            print(f"skip (could not remove): {rel} ({e})", file=sys.stderr)

    return removed, reported


def report(label, paths, found=0, dry_run=False):
    """Report a pass. `found` is how many targets the walk saw, so a pass that
    found targets and removed none says so instead of printing "Clean".

    Without that distinction a removal blocked by the sandbox reads exactly like
    a tree that was already clean, which is the false pass `goal-contracts`
    forbids: a step that could not run is unrun, never passed.
    """
    if not paths:
        if found:
            print(
                f"WARNING: {found} {label} found, none removed. "
                "See the skip lines above. This pass did not run, it is not clean."
            )
        else:
            print(f"No {label} found. Clean.")
        return
    verb = "Would remove" if dry_run else "Removed"
    print(f"{verb} {len(paths)} {label}:")
    for p in paths:
        print("  -", os.path.relpath(p, REPO_ROOT))
    # The .cc-writes pass can remove an emptied .claude parent too, so a count
    # above `found` is expected and only a shortfall is worth warning about.
    if len(paths) < found:
        print(
            f"  WARNING: {found - len(paths)} of {found} not removed, "
            "see the skip lines above."
        )


def main():
    dry_run = "--dry-run" in sys.argv[1:]
    if dry_run:
        print("DRY RUN: nothing will be deleted.\n")

    cc_dirs, ds_files, scratch_dirs, scratch_files = find_targets()
    report(
        "empty .cc-writes folders",
        remove_cc_writes(cc_dirs, dry_run),
        len(cc_dirs),
        dry_run,
    )
    report(".DS_Store files", remove_ds_store(ds_files, dry_run), len(ds_files), dry_run)

    try:
        tracked = tracked_paths()
    except (subprocess.CalledProcessError, OSError) as e:
        # Fail closed. Without the tracked set every match looks untracked and
        # therefore deletable, so a git failure stops the pass instead of
        # widening it.
        print(
            f"SCRATCH PASS SKIPPED: could not read the git index ({e}). "
            "Nothing was deleted. Re-run inside the repository.",
            file=sys.stderr,
        )
        return 1

    removed, reported = remove_scratch(scratch_dirs, scratch_files, tracked, dry_run)
    # Tracked matches are reported on purpose, so they are not a shortfall.
    deletable = len(scratch_dirs) + len(scratch_files) - len(reported)
    report("scratch files and folders", removed, deletable, dry_run)
    if reported:
        print(
            f"\nREPORTED, NOT DELETED: {len(reported)} git-tracked scratch match(es)"
        )
        for r in reported:
            print("  !", r)
        print("Tracked files may hold real work. Decide on each one yourself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

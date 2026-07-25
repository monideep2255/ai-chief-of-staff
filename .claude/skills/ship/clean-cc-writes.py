#!/usr/bin/env python3
# depends_on: []
# depended_by: [.claude/skills/ship/SKILL.md]
"""Remove working-tree litter before a commit: Claude Code's empty .cc-writes
staging folders (and any .claude parent they leave empty), plus macOS .DS_Store
files.

Two cleanups, both gitignored, so neither changes what gets committed.

.cc-writes folders are safe by construction: os.rmdir removes only empty
directories, so no folder that holds a real file can ever be deleted. The main
repo .claude/ is never empty (it holds rules, agents, skills), so it is
inherently protected with no hardcoded allowlist.

.DS_Store files are deleted with os.remove, which is a real unlink, so the guard
is the match instead: the basename must be exactly ".DS_Store", and the path must
be a regular file, never a directory and never a symlink. macOS regenerates these
on folder access, so removing them loses nothing.

Both passes use followlinks=False, which keeps the walk out of any symlinked
external repos referenced from this repo.

Standing owner permission was granted for the .cc-writes cleanup and the
.DS_Store cleanup, so /ship runs this without asking. Run it with the sandbox
disabled: the .cc-writes paths are on the sandbox protected list, so deletion is
denied under the sandbox.
"""
import os
import sys

# repo root is four levels up: .claude/skills/ship/clean-cc-writes.py
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

DS_STORE = ".DS_Store"


def find_targets():
    """One walk, two target lists: .cc-writes dirs and .DS_Store files."""
    cc_dirs = []
    ds_files = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT, followlinks=False):
        if ".cc-writes" in dirnames:
            cc_dirs.append(os.path.join(dirpath, ".cc-writes"))
        if DS_STORE in filenames:
            ds_files.append(os.path.join(dirpath, DS_STORE))
    return cc_dirs, ds_files


def remove_cc_writes(cc_dirs):
    removed = []
    for cc in cc_dirs:
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


def remove_ds_store(ds_files):
    removed = []
    for ds in ds_files:
        # Guard the unlink: exact name, regular file, never a symlink.
        if os.path.basename(ds) != DS_STORE:
            continue
        if os.path.islink(ds) or not os.path.isfile(ds):
            print(f"skip (not a regular file): {ds}", file=sys.stderr)
            continue
        try:
            os.remove(ds)
            removed.append(ds)
        except OSError as e:
            print(f"skip (could not remove): {ds} ({e})", file=sys.stderr)
    return removed


def report(label, paths):
    if not paths:
        print(f"No {label} found. Clean.")
        return
    print(f"Removed {len(paths)} {label}:")
    for p in paths:
        print("  -", os.path.relpath(p, REPO_ROOT))


def main():
    cc_dirs, ds_files = find_targets()
    report("empty .cc-writes folders", remove_cc_writes(cc_dirs))
    report(".DS_Store files", remove_ds_store(ds_files))
    return 0


if __name__ == "__main__":
    sys.exit(main())

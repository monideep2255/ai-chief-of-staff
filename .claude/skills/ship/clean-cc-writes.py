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

Scratch paths have neither protection, so they carry six guards of their own,
numbered First to Sixth below. Nested repositories get their own paragraph after.

First, every match is anchored, never a substring or a prefix. A substring match
on "temp" or "scratch" hits real work in almost any repository: a _templates/
folder, a document about temporal data, and every tmpdir.py inside a
virtualenv. A name therefore matches only as a whole basename,
a whole stem (the name with its one final extension removed), or a whole
trailing suffix. A stem is "untitled" alone or "untitled" plus a number, as in
"Untitled 2.md", so Untitled_grant_draft.md and temp.sensor.readings.md are kept.

Second, git decides what is real. A path git tracks is reported and never
deleted, because a file committed on purpose may hold real work whatever it is
named. The comparison is casefolded and NFC-normalized on both sides, so a
case-insensitive file system cannot hide a tracked folder. The owner decides each
of those individually.

Third, external checkouts and vendored dependency trees are pruned from the walk
entirely, so this never reaches into a repository that is not ours.

Fourth, resolved scratch targets must remain inside this repository and cannot
be the repository root. Symlink and junction directories are never removed.

Fifth, ignored folders and ignored files are off limits. Git's tracked-file guard
cannot see inside a gitignored folder, so a scratch-named folder there (for
example outputs/run/tmp) can hold untracked work that exists nowhere else. The
scratch pass therefore skips any target that `git check-ignore -q` reports as
ignored, and any folder where `git ls-files -o -i --exclude-standard` lists an
ignored file (for example a data.csv under a *.csv pattern), unless
--include-ignored is passed. If git cannot answer, the target counts as ignored.
The .cc-writes and .DS_Store passes are exempt: their targets are gitignored by
design.

Sixth, nested repositories are never entered, in any pass. A directory below the
repository root that holds a .git entry (a directory, a worktree file, or a
symlink, tested with os.path.lexists) is another repository. The walk does not
descend into it or target it, and a final guard before each removal checks every
ancestor of the target up to the repository root for the same .git entry. Before
a folder target is removed, the guard also walks the folder itself and skips it
if any level below holds a .git entry.

All three passes use followlinks=False, which keeps the walk out of any symlinked
external repositories.

Standing owner permission was granted 2026-07-15 for the .cc-writes cleanup,
2026-07-25 for the .DS_Store cleanup, and 2026-09-20 for the scratch cleanup, so
/ship runs this without asking. Run it with the sandbox disabled: the .cc-writes
paths are on the sandbox protected list, so deletion is denied under the sandbox.

Usage:
    python3 .claude/skills/ship/clean-cc-writes.py [--dry-run] [--include-ignored]

--dry-run lists each target with the reason it qualifies and deletes nothing.
--include-ignored lets the scratch pass remove targets inside gitignored folders.
Any other argument is an error (exit 2) and nothing is touched.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import unicodedata

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

# A file whose stem (the name with its one final extension removed) is exactly
# one of these, so scratch.md, tmp.json and temp.py match while templates.py,
# temporal.md and temp.sensor.readings.md do not.
SCRATCH_FILE_STEMS = frozenset({"scratch", "scratchpad", "temp", "tmp", "untitled"})

# "untitled" alone or followed by a number, the "Untitled 2.md" shape editors
# produce. Untitled_grant_draft.md does not match.
UNTITLED_STEM = re.compile(r"untitled( \d+)?")

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
    return scratch_file_reason(name) is not None


def scratch_file_reason(name):
    """Why a file name matches the scratch pass, or None when it does not."""
    lowered = name.lower()
    if lowered in SCRATCH_NEVER:
        return None
    if lowered.endswith(SCRATCH_SUFFIXES):
        return "file name ends with a scratch suffix"
    stem = os.path.splitext(lowered)[0]
    if stem in SCRATCH_FILE_STEMS or UNTITLED_STEM.fullmatch(stem):
        return "file stem is a scratch name"
    return None


# Why each target qualifies, keyed by path. Printed in a dry run.
REASONS = {}

# Targets and nested repositories left alone: (repo-relative path, reason).
SKIPPED = []

REASON_NESTED = "nested repository"
REASON_IGNORED = "ignored, pass --include-ignored"
REASON_IGNORED_FILES = "holds ignored files, pass --include-ignored"
REASON_SYMLINK = "symlink"


def rel_of(path):
    return os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")


def skip(path, reason):
    SKIPPED.append((rel_of(path), reason))


def nested_repo_at_or_above(path):
    """Return the first directory from `path` up to (excluding) the repository
    root that holds a .git entry, else None. lexists covers a .git directory, a
    .git file as in a worktree, and a .git symlink."""
    root = os.path.normcase(os.path.abspath(REPO_ROOT))
    current = os.path.abspath(path)
    while os.path.normcase(current) != root:
        if os.path.lexists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


def holds_nested_repo(path):
    """True when `path` or any level below it holds a .git entry. Fails closed:
    a directory the walk cannot read counts as holding one."""
    def fail(err):
        raise err

    try:
        for dirpath, _dirnames, _files in os.walk(
            path, followlinks=False, onerror=fail
        ):
            if os.path.lexists(os.path.join(dirpath, ".git")):
                return True
    except OSError:
        return True
    return False


def holds_ignored_files(path):
    """True when git lists an ignored file under `path`. Fails closed: a git
    error counts as holding ignored files."""
    try:
        r = subprocess.run(
            ["git", "-C", REPO_ROOT, "ls-files", "-o", "-i", "--exclude-standard",
             "-z", "--", rel_of(path)],
            capture_output=True,
        )
    except OSError:
        return True
    return r.returncode != 0 or bool(r.stdout)


def norm(rel):
    """Casefolded, NFC-normalized path for comparison on any file system."""
    return unicodedata.normalize("NFC", rel).casefold()


def is_ignored(path):
    """True when git ignores the path. Fails closed: if git cannot answer
    (exit 128 or anything but 1), the path counts as ignored."""
    try:
        r = subprocess.run(
            ["git", "-C", REPO_ROOT, "check-ignore", "-q", "--", rel_of(path)],
            capture_output=True,
        )
    except OSError:
        return True
    return r.returncode != 1


def through_link(path):
    """Reject a symlink/junction at the target or below the repository root."""
    root = os.path.normcase(os.path.abspath(REPO_ROOT))
    current = os.path.abspath(path)
    while os.path.normcase(current) != root:
        if os.path.islink(current) or (
            hasattr(os.path, "isjunction") and os.path.isjunction(current)
        ):
            return True
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return False


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
        # Windows junctions can be traversed even with followlinks=False.
        # Prune aliases before collecting targets for any of the passes.
        # A child that holds a .git entry is another repository: drop it from
        # the walk before any pass can match it or anything inside it.
        walkable = []
        for d in dirnames:
            full = os.path.join(dirpath, d)
            if through_link(full):
                if d.lower() in SCRATCH_DIR_NAMES:
                    skip(full, REASON_SYMLINK)
                continue
            if (
                d not in PRUNE_DIR_NAMES
                and not is_pruned(rel_of(full))
                and os.path.lexists(os.path.join(full, ".git"))
            ):
                skip(full, REASON_NESTED)
                continue
            walkable.append(d)
        dirnames[:] = walkable
        if ".cc-writes" in dirnames:
            cc = os.path.join(dirpath, ".cc-writes")
            cc_dirs.append(cc)
            REASONS[cc] = "Claude Code staging folder, removed only if empty"
        if DS_STORE in filenames:
            ds = os.path.join(dirpath, DS_STORE)
            ds_files.append(ds)
            REASONS[ds] = "macOS metadata file named exactly .DS_Store"

        keep = []
        for d in dirnames:
            if d in PRUNE_DIR_NAMES:
                continue  # vendored or transient: neither walked nor matched
            if d.lower() in SCRATCH_DIR_NAMES:
                full = os.path.join(dirpath, d)
                scratch_dirs.append(full)
                REASONS[full] = f"folder name '{d}' is a scratch name"
                continue  # matched whole, so the folder is judged as one unit
            keep.append(d)
        dirnames[:] = keep

        for f in filenames:
            reason = scratch_file_reason(f)
            if reason:
                full = os.path.join(dirpath, f)
                scratch_files.append(full)
                REASONS[full] = reason
    return cc_dirs, ds_files, scratch_dirs, scratch_files


def remove_cc_writes(cc_dirs, dry_run=False):
    removed = []
    for cc in cc_dirs:
        if nested_repo_at_or_above(cc):
            skip(cc, REASON_NESTED)
            continue
        if dry_run:
            # Match the real run: only an empty folder would be removed.
            try:
                empty = not os.listdir(cc)
            except OSError:
                empty = False
            if not empty:
                print(f"skip (not empty or gone): {cc}", file=sys.stderr)
                continue
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
            try:
                os.rmdir(parent)
                removed.append(parent)
            except OSError as e:
                print(f"skip (could not remove): {parent} ({e})", file=sys.stderr)
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
        if nested_repo_at_or_above(ds):
            skip(ds, REASON_NESTED)
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


def remove_scratch(
    scratch_dirs, scratch_files, tracked, dry_run=False, include_ignored=False
):
    """Delete untracked scratch matches. Report tracked ones, never delete them.

    Returns (removed, reported, skipped_count). A tracked match is something
    committed on purpose, so the call to remove it stays with the owner. A
    nested-repository or ignored match is skipped and listed in SKIPPED.
    """
    skipped_before = len(SKIPPED)

    def blocked(path):
        # Final guards, just before removal. Nested repository first, then the
        # ignored check that this pass alone applies.
        if nested_repo_at_or_above(path):
            skip(path, REASON_NESTED)
            return True
        is_dir = os.path.isdir(path) and not os.path.islink(path)
        if is_dir and holds_nested_repo(path):
            skip(path, REASON_NESTED)
            return True
        if not include_ignored:
            if is_ignored(path):
                skip(path, REASON_IGNORED)
                return True
            if is_dir and holds_ignored_files(path):
                skip(path, REASON_IGNORED_FILES)
                return True
        return False

    tracked_norm = [norm(t) for t in tracked]
    tracked_set = set(tracked_norm)

    removed = []
    reported = []

    def contained(path):
        # Resolve symlinks/junctions before any removal, including dry runs.
        # Refuse the repository root itself and targets outside it.
        root = os.path.realpath(REPO_ROOT)
        target = os.path.realpath(path)
        try:
            return target != root and os.path.commonpath([root, target]) == root
        except ValueError:  # Different Windows drives have no common path.
            return False

    for path in scratch_files:
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
        if norm(rel) in tracked_set:
            reported.append(rel)
            continue
        if through_link(path):
            skip(path, REASON_SYMLINK)
            continue
        if not contained(path):
            print(f"skip (outside repository or root): {rel}", file=sys.stderr)
            continue
        if os.path.islink(path) or not os.path.isfile(path):
            print(f"skip (not a regular file): {rel}", file=sys.stderr)
            continue
        if blocked(path):
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
        # Git's index uses forward slashes on every platform.
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
        prefix = norm(rel) + "/"
        held = sorted(
            t for t in tracked_norm if t == norm(rel) or t.startswith(prefix)
        )
        if held:
            reported.append(
                f"{rel}/ holds {len(held)} tracked file(s), first is {held[0]}"
            )
            continue
        if through_link(path):
            skip(path, REASON_SYMLINK)
            continue
        if not contained(path):
            print(f"skip (outside repository or root): {rel}", file=sys.stderr)
            continue
        if blocked(path):
            continue
        if dry_run:
            removed.append(path)
            continue
        try:
            shutil.rmtree(path)
            removed.append(path)
        except OSError as e:
            print(f"skip (could not remove): {rel} ({e})", file=sys.stderr)

    return removed, reported, len(SKIPPED) - skipped_before


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
        why = f"  [{REASONS[p]}]" if dry_run and p in REASONS else ""
        print("  -", os.path.relpath(p, REPO_ROOT) + why)
    # The .cc-writes pass can remove an emptied .claude parent too, so a count
    # above `found` is expected and only a shortfall is worth warning about.
    if len(paths) < found:
        print(
            f"  WARNING: {found - len(paths)} of {found} not removed, "
            "see the skip lines above."
        )


def parse_args(argv=None):
    """Parse before any filesystem walk: --help exits 0, an unknown argument
    exits 2, and in both cases nothing has been touched."""
    parser = argparse.ArgumentParser(
        prog="clean-cc-writes.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="list targets and the reason each qualifies, delete nothing",
    )
    parser.add_argument(
        "--include-ignored",
        action="store_true",
        help="let the scratch pass remove targets inside gitignored folders",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    dry_run = args.dry_run
    if dry_run:
        print("DRY RUN: nothing will be deleted.\n")

    cc_dirs, ds_files, scratch_dirs, scratch_files = find_targets()
    mark = len(SKIPPED)
    cc_removed = remove_cc_writes(cc_dirs, dry_run)
    report(
        "empty .cc-writes folders",
        cc_removed,
        len(cc_dirs) - (len(SKIPPED) - mark),
        dry_run,
    )
    mark = len(SKIPPED)
    ds_removed = remove_ds_store(ds_files, dry_run)
    report(
        ".DS_Store files",
        ds_removed,
        len(ds_files) - (len(SKIPPED) - mark),
        dry_run,
    )

    try:
        tracked = tracked_paths()
    except (subprocess.CalledProcessError, OSError) as e:
        # Fail closed. Without the tracked set every match looks untracked and
        # therefore deletable, so a git failure stops the pass instead of
        # widening it.
        print(
            f"SCRATCH PASS SKIPPED: could not read the git index ({e}). "
            "No scratch file or folder was deleted. The passes above this line "
            "ran as reported. Re-run inside the repository.",
            file=sys.stderr,
        )
        return 1

    removed, reported, skipped_n = remove_scratch(
        scratch_dirs, scratch_files, tracked, dry_run, args.include_ignored
    )
    # Tracked and skipped matches are left on purpose, so they are not a shortfall.
    deletable = len(scratch_dirs) + len(scratch_files) - len(reported) - skipped_n
    report("scratch files and folders", removed, deletable, dry_run)
    if SKIPPED:
        print(f"\nSKIPPED, NOT DELETED: {len(SKIPPED)} target(s)")
        for rel, reason in SKIPPED:
            print(f"  ~ {rel} ({reason})")
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

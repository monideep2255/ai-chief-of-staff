#!/usr/bin/env python3
# depends_on: []
# depended_by: [.claude/skills/ship/SKILL.md]
"""Remove Claude Code's empty .cc-writes staging folders (and any .claude
parent they leave empty).

Safe by construction: uses os.rmdir, which removes only empty directories, so
no folder that holds a real file can ever be deleted. The main repo .claude/ is
never empty (it holds rules, agents, skills), so it is inherently protected with
no hardcoded allowlist.

Standing owner permission was granted 2026-07-15 to run this as a /ship step.
Run it with the sandbox disabled: the .cc-writes paths are on the sandbox
protected list, so deletion is denied under the sandbox.
"""
import os
import sys

# repo root is four levels up: .claude/skills/ship/clean-cc-writes.py
REPO_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


def main():
    # Locate every .cc-writes dir. followlinks=False keeps us out of the
    # symlinked external repos under Reference-repos/*/.
    targets = []
    for dirpath, dirnames, _ in os.walk(REPO_ROOT, followlinks=False):
        if ".cc-writes" in dirnames:
            targets.append(os.path.join(dirpath, ".cc-writes"))

    removed = []
    for cc in targets:
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

    rel = [os.path.relpath(p, REPO_ROOT) for p in removed]
    if rel:
        print("Removed:")
        for r in rel:
            print("  -", r)
    else:
        print("No .cc-writes folders found. Clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

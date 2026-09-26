#!/usr/bin/env python3
"""verify_ingest_outputs.py - deterministic output checks for the ingest-workflows skill.

Step 2 and Step 6 of `.claude/skills/ingest-workflows/SKILL.md` describe a set of
mechanical checks a cleaned document must pass: frontmatter present, a table of
contents, a known-gaps section, no em or en dashes, no bold, no webmail links, no
ligature-drop artifacts left behind by a PDF or DOCX conversion. Before this
script those checks were prose a model re-derived and re-ran by hand on every
ingest. This is the fat-script side for ingest-workflows: a thin skill body plus
a script that actually proves the checks passed, instead of a model re-deriving
the same checklist from memory every run.

Two independent things this script proves:

  1. Per-file hard checks (frontmatter, structure, prose hygiene) on explicit
     paths, or on every changed .md file under the configured reference roots
     via --changed.
  2. --index-check: every top-level document in every reference-library
     subfolder is actually named in that library's README.md. This is the
     check that catches a document silently going missing from the index
     because nothing ever counted the two sides against each other.

Usage:
  python3 .claude/scripts/verify_ingest_outputs.py <file> [<file> ...]
  python3 .claude/scripts/verify_ingest_outputs.py --changed
  python3 .claude/scripts/verify_ingest_outputs.py --index-check
  python3 .claude/scripts/verify_ingest_outputs.py --changed --index-check

Exit 0: every hard check and every requested index check passed (warnings may
        still have printed).
Exit 1: at least one hard check or the index check failed. Failures are printed
        one per line, grouped by file.

Standard library only.

depends_on: []
depended_by: [.claude/skills/ingest-workflows/SKILL.md]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# --- repo root -----------------------------------------------------------


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(out.stdout.strip())
    except Exception:
        guess = Path(__file__).resolve().parents[2]
        if (guess / ".claude").is_dir():
            return guess
        print("FAIL: could not locate the repository root.", file=sys.stderr)
        sys.exit(2)


ROOT = repo_root()
EXCLUDED_BASENAMES = {"README.md", "PLAYBOOK.md"}

# --- configuration ---------------------------------------------------------
# Adjust these two to match your own repository layout. They are read once at
# import time, so a fork only has to change the values below, nothing else in
# this file.

# Folders --changed scans for added or modified markdown, matched by prefix.
# The ingest-workflows skill in this repo writes into a reference-doc library
# (default "Reference/") and, for a single tracked project, that project's own
# intake folder (default "Projects/"). Add or remove roots to fit your setup.
CHANGED_ROOTS = ("Reference/", "Projects/")

# Where --index-check looks for the reference library and its top-level index.
# Every subfolder under INDEX_LIBRARY_DIR is checked against INDEX_LIBRARY_DIR
# / "README.md".
INDEX_LIBRARY_DIR = "Reference"

# --- hard-check patterns ---------------------------------------------------

FRONTMATTER_KEYS = ["description", "type", "source", "added", "actionability"]
EM_EN_DASH_RE = re.compile(r"[–—]")
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
# Webmail hosts only. A bare "outlook" also matches the English word, as in a
# "market outlook" section, which is a false positive.
WEBMAIL_RE = re.compile(
    r"mail\.google\.com|outlook\.(?:office|office365|live)\.com|outlook\.com/(?:mail|owa)",
    re.IGNORECASE,
)
TOC_HEADING_RE = re.compile(
    r"^#{1,6}\s*(table of contents|contents)\s*$", re.IGNORECASE | re.MULTILINE
)
KNOWN_GAPS_HEADING_RE = re.compile(
    r"^#{1,6}\s*known gaps\s*$", re.IGNORECASE | re.MULTILINE
)

# Ligature-drop artifacts: a PDF/DOCX conversion that silently ate an "fi" or
# "ffi" ligature. Whole-word match only, so "software" itself (already
# correct) never trips this, only the dropped form "soware".
LIGATURE_WORDS = [
    "soware", "aer", "shi", "eective", "dierent",
    "workow", "ecient", "rst", "oer",
]
LIGATURE_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in LIGATURE_WORDS) + r")\b",
    re.IGNORECASE,
)

# --- warning-only patterns --------------------------------------------------

# Example brand-term list. This is a starting point, not a fixed catalogue:
# swap in whatever product names your own writing-style rule wants neutralized
# in body text (source attributions and footnote URLs are exempt, this only
# warns on the body).
BRAND_TERMS = [
    "ChatGPT", "Slack", "Figma", "Notion", "Zoom",
]
BRAND_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in BRAND_TERMS) + r")\b"
)

# Words that end in "ing" but are not gerunds/participles in normal use, so a
# sentence or bullet starting with one is not the writing-style violation this
# warning targets.
ING_SAFE_WORDS = {"bring", "thing", "string", "king", "ring", "spring", "wing"}
ING_OPENER_RE = re.compile(r"^([A-Za-z]+ing)\b")
BULLET_LABEL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 /'-]*:\s")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# A word capitalized mid-heading that is not an acronym (all caps) and not
# obviously a proper noun/named tool is flagged as a possible title-case slip.
# This is a soft heuristic on purpose: it warns, it never fails the run.
STOPWORDS_LOWER_OK = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into",
    "is", "it", "nor", "of", "on", "or", "so", "the", "to", "with", "vs",
}


def sentences_and_bullets(text: str) -> list:
    """Return (line_no, snippet) for lines that open a bullet or a standalone
    sentence-like line, skipping code fences, tables, and headings."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped or stripped.startswith("#") or stripped.startswith("|"):
            continue
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        text_part = m.group(1) if m else stripped
        out.append((i, text_part))
    return out


def check_file(path: Path) -> tuple:
    """Return (failures, warnings), both lists of strings, for one file."""
    failures = []
    warnings = []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return ([f"UNREADABLE could not read file: {exc}"], [])

    lines = text.splitlines()

    # --- frontmatter -------------------------------------------------------
    if not lines or lines[0].strip() != "---":
        failures.append("FRONTMATTER missing (no leading '---' block)")
    else:
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            failures.append("FRONTMATTER opening '---' found but no closing '---'")
        else:
            block = "\n".join(lines[1:end])
            for key in FRONTMATTER_KEYS:
                if not re.search(rf"^{re.escape(key)}:\s*\S", block, re.MULTILINE):
                    failures.append(f"FRONTMATTER missing or empty field '{key}'")

    # --- structure -----------------------------------------------------
    if not TOC_HEADING_RE.search(text):
        failures.append("STRUCTURE no table of contents heading found")
    if not KNOWN_GAPS_HEADING_RE.search(text):
        failures.append("STRUCTURE no known gaps heading found")

    # --- prose hygiene, hard --------------------------------------------
    dash_hits = EM_EN_DASH_RE.findall(text)
    if dash_hits:
        failures.append(f"DASH found {len(dash_hits)} em or en dash character(s)")

    bold_hits = BOLD_RE.findall(text)
    if bold_hits:
        failures.append(f"BOLD found {len(bold_hits)} bold span(s), e.g. {bold_hits[0]!r}")

    webmail_lines = [i + 1 for i, ln in enumerate(lines) if WEBMAIL_RE.search(ln)]
    if webmail_lines:
        failures.append(f"WEBMAIL webmail link(s) on line(s) {webmail_lines}")

    ligature_hits = sorted(set(w.lower() for w in LIGATURE_RE.findall(text)))
    if ligature_hits:
        failures.append(f"LIGATURE ligature-drop artifact(s): {', '.join(ligature_hits)}")

    # --- warnings ------------------------------------------------------
    brand_hits = sorted(set(BRAND_RE.findall(text)))
    if brand_hits:
        warnings.append(f"BRAND brand term(s) in body: {', '.join(brand_hits)}")

    ing_hits = []
    for line_no, snippet in sentences_and_bullets(text):
        if BULLET_LABEL_RE.match(snippet):
            continue
        m = ING_OPENER_RE.match(snippet)
        if m and m.group(1).lower() not in ING_SAFE_WORDS:
            ing_hits.append((line_no, snippet[:60]))
    if ing_hits:
        sample = "; ".join(f"line {n}: {s!r}" for n, s in ing_hits[:5])
        more = f" (+{len(ing_hits) - 5} more)" if len(ing_hits) > 5 else ""
        warnings.append(f"ING sentence/bullet opener ending in -ing: {sample}{more}")

    heading_hits = []
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if not m:
            continue
        words = m.group(2).split()
        for w in words[1:]:
            core = w.strip(":,.()[]")
            if not core or not core[0].isupper():
                continue
            if core.isupper():
                continue  # acronym
            if core.lower() in STOPWORDS_LOWER_OK:
                continue
            heading_hits.append((i, m.group(2)))
            break
    if heading_hits:
        sample = "; ".join(f"line {n}: {h!r}" for n, h in heading_hits[:5])
        more = f" (+{len(heading_hits) - 5} more)" if len(heading_hits) > 5 else ""
        warnings.append(f"HEADING possible non-sentence-case heading: {sample}{more}")

    return failures, warnings


# --- --changed discovery ----------------------------------------------------


def changed_md_files() -> dict:
    """Map each changed .md path under CHANGED_ROOTS to its check mode.

    New files (untracked or staged as added) get the full new-document checks.
    Edited or moved existing files get the privacy check only, because an
    ingest run legitimately adds cross-links to older documents that predate
    the table-of-contents, known-gaps, and frontmatter requirements. Holding
    those to the new-document bar would fail every normal ingest.
    """
    out = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, cwd=ROOT, check=True,
    ).stdout
    modes = {}
    for line in out.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        rest = line[3:].strip().strip('"')
        # Renames look like "R  old -> new"; take the new path.
        if "->" in rest:
            rest = rest.split("->", 1)[1].strip().strip('"')
        if status == "??" or "A" in status:
            mode = "full"
        elif "M" in status or "R" in status:
            mode = "privacy"
        else:
            continue
        if not rest.endswith(".md"):
            continue
        if not rest.startswith(CHANGED_ROOTS):
            continue
        if Path(rest).name in EXCLUDED_BASENAMES:
            continue
        if modes.get(rest) != "full":
            modes[rest] = mode
    return modes


# --- --index-check -----------------------------------------------------


def index_check() -> list:
    """Return a list of failure strings; empty means every subfolder document
    is named in the reference library's README.md."""
    base = ROOT / INDEX_LIBRARY_DIR
    readme = base / "README.md"
    if not readme.is_file():
        return [f"INDEX {readme.relative_to(ROOT)} not found"]

    index_text = readme.read_text(encoding="utf-8")
    failures = []

    for sub in sorted(p for p in base.iterdir() if p.is_dir()):
        docs = sorted(
            p for p in sub.glob("*.md")
            if p.name not in EXCLUDED_BASENAMES
        )
        missing = [d.name for d in docs if d.stem not in index_text and d.name not in index_text]
        if missing:
            failures.append(
                f"INDEX {sub.relative_to(ROOT)} has {len(missing)} document(s) "
                f"missing from {readme.relative_to(ROOT)}: {', '.join(missing)}"
            )
    return failures


# --- main --------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="explicit file paths to check")
    parser.add_argument("--changed", action="store_true",
                         help="check every added/modified .md file under the configured roots")
    parser.add_argument("--index-check", action="store_true",
                         help="verify every reference-library subfolder document is in its README.md")
    args = parser.parse_args()

    exit_code = 0
    any_target = False

    modes = {f: "full" for f in args.files}
    if args.changed:
        for rel, mode in changed_md_files().items():
            if modes.get(rel) != "full":
                modes[rel] = mode
    targets = sorted(modes)

    if targets:
        any_target = True
        total_failures = 0
        total_warnings = 0
        for rel in targets:
            path = Path(rel)
            if not path.is_absolute():
                path = ROOT / rel
            if modes[rel] == "full":
                failures, warnings = check_file(path)
                label = rel
            else:
                text = path.read_text(encoding="utf-8", errors="replace")
                hits = [i + 1 for i, ln in enumerate(text.splitlines()) if WEBMAIL_RE.search(ln)]
                failures = [f"WEBMAIL webmail link(s) on line(s) {hits}"] if hits else []
                warnings = []
                label = f"{rel} (edited existing file, privacy check only)"
            if failures:
                print(f"FAIL {label}")
                for f in failures:
                    print(f"  - {f}")
                exit_code = 1
            elif warnings:
                print(f"OK   {label} (warnings below)")
            else:
                print(f"OK   {label}")
            for w in warnings:
                print(f"  ! {w}")
            total_failures += len(failures)
            total_warnings += len(warnings)
        print(
            f"--- {len(targets)} file(s) checked, "
            f"{total_failures} failure(s), {total_warnings} warning(s) ---"
        )

    if args.index_check:
        any_target = True
        failures = index_check()
        if failures:
            print("FAIL --index-check")
            for f in failures:
                print(f"  - {f}")
            exit_code = 1
        else:
            print("OK   --index-check: every subfolder document is indexed")

    if not any_target:
        print("Nothing to check: pass file paths, --changed, or --index-check.")
        return 0

    if exit_code == 0:
        print("PASS: verify_ingest_outputs.py")
    else:
        print("FAIL: verify_ingest_outputs.py, see defects above")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

---
name: deep-dive
author: human
description: Produce a first-principles deep dive on a document, a URL, or a bare topic, written in the user's signature 9-move shape. TRIGGER when the user shares a PDF/MD file, a web link, or a topic and says "deep dive this", "do a deep dive on", "break this down", or "analyze this document/topic". DO NOT TRIGGER for GitHub repos (use /repo-dive) or a quick "what is X" one-liner (use the first-principles agent).
scope: project
argument-hint: <file-path | url | topic> [--research]
produces_docs: true
depends_on:
  - .claude/skills/web-research/SKILL.md
  - .claude/rules/doc-construction.md
  - .claude/rules/writing-style.md
  - .claude/rules/self-eval-loop.md
  - .claude/rules/os-improvement-logging.md
  - OS_IMPROVEMENTS.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# /deep-dive - first-principles deep dive in your shape

Take a document, a URL, or a topic and produce one deep-dive markdown file written the way you write them: define from zero, collapse the surface complexity to its load-bearing structure, mark evidence honestly, diagram the core relationship, and end with what it means for your actual work.

This is the non-repo sibling of `/repo-dive`. Repos go to `/repo-dive`. Everything else (books, papers, articles, documents, concepts, domains) comes here.

## Invocation

```
/deep-dive ./path/to/document.pdf        # deep-dive a document you have
/deep-dive ./notes/some_file.md          # deep-dive a local markdown file
/deep-dive https://example.com/article   # deep-dive a web page
/deep-dive leverage and permissionless work   # deep-dive a topic (researches sources)
/deep-dive ./document.pdf --research      # deep-dive the doc AND supplement with web research
```

## Input modes (auto-detect from what was passed)

Detect the mode before doing anything else. The mode decides whether you research.

| What was passed | Mode | Research? |
|-----------------|------|-----------|
| A path that exists on disk (`.pdf`, `.md`, `.txt`) | Document | No. Analyze the document only. |
| A string starting with `http` | URL | No. Scrape the link, analyze that content only. |
| Anything else | Topic | Yes. There is no source to read, so gather sources first with web-research. |

The load-bearing rule: for a document or a URL, the source you were handed is the whole input. Do not go research around it, do not pull in outside sources, do not fact-check it against the web unless the user passed `--research` or explicitly tells you to ("now go research X", "check this against current sources"). No research the user did not ask for.

- Document mode: read the file in place. For a PDF, use the Read tool's `pages` parameter, do not convert the PDF to markdown (that is a separate action gated by the pdf-docx-conversion rule). The source in the final doc is the document itself.
- URL mode: scrape the page to clean markdown with Firecrawl (see web-research skill, step 2). The source is that one page.
- Topic mode: run web-research (WebSearch plus Firecrawl on the sources that add depth) to gather material first, then write. This is the only mode that researches by default, because there is nothing to read otherwise.
- `--research` flag: overrides the no-research default for document and URL modes. Analyze the source first, then supplement with web-research to fill gaps or check claims, and say in the doc which parts came from the source and which from added research.

## The shape (your 9 moves, every time)

Write one file. Follow this structure. The section titles adapt to the subject, the moves do not.

```markdown
<!-- depends_on: [] -->
<!-- depended_by: [] -->

# <Subject>: a first-principles deep dive

<One paragraph: what this doc does, what the source is, and one honesty note about where the source is solid or thin. Then "Built: <date>.">

## Contents
<ToC linking to every section below.>

## What is <subject>?
Plain-language definition anyone could follow, with a concrete analogy. Define from zero. No jargon without an immediate plain-word definition.

## The one idea
The whole thing compressed to a single sentence, then the paragraph that unpacks why everything else follows from it.

## The real structure
The signature move: collapse the surface complexity to the small set of ideas it actually rests on. N laws are really M forms. N features are really M primitives. Show the collapse. This is usually the actual learning, so make it the load-bearing section. A table works well here.

## Mapped honestly
Mark what the source actually supports versus what it asserts or leaves thin. Never fabricate specifics to look complete. If the source names eight of eighteen things, map the eight and say the rest are not in the record. Being openly partial beats being confidently wrong.

## How it fits together
A mermaid diagram of the core relationship, loop, or flow. Read the diagram as a sequence in the prose right after it. One diagram per concept, node labels under 30 characters, no literal line breaks in labels.

## A worked example
The abstraction running in a real case, not on a whiteboard. Flag which parts are the reliable pattern and which are the specific-case reading.

## Where it is strong, where to be skeptical
Both sides, read straight rather than as a fan. What is genuinely good, then where to keep your guard up. Name the failure case, the survivorship framing, the thing the source underweights.

## What this means for you
Tie it to your actual live work. Pull from memory and the current-focus note in CLAUDE.md: which project this touches (the product you're building, a career decision, an upcoming milestone), and any guardrail it interacts with (a time-boxing commitment, an overwork pattern you're watching for). This is the section that makes the dive yours and not a book report.

## Sources
Clickable links. For document mode, the source is the document (name it, link if it has a URL). Never leave a bare page id or URL without a title.
```

Fill the two frontmatter comment lines once you know where the file lands (see placement below).

## Style (already enforced, do not re-encode)

Your always-on rules carry the prose and structure: `writing-style` (no em dashes, sentence case headings, no bold, no LLM brand names), `doc-construction` (ToC, first-principles skeleton, mermaid, simple language), `response-calibration` (plain language). Follow them. Do not restate them in the output. The point of this skill is the 9-move shape on top of those rules, not the rules themselves.

Anti-patterns (do not produce these):
- A summary that restates the source with no collapse to structure and no skepticism. That is a book report, not a deep dive.
- Fabricated specifics (invented law titles, made-up numbers) to look complete. Map honestly instead.
- "What this means for you" that is generic. It must name a real current project and, where relevant, a real guardrail.
- A mermaid diagram that is just boxes restating a list. Add the relationship, the loop, or the sequence.
- Research pulled in for a document or URL when the user did not ask for it.

## Grader pass (self-eval-loop)

A deep dive is substantial output, so before you call it done, dispatch one fresh-context agent that sees only the draft file and this pass/fail checklist. Per the self-eval-loop rule, the agent that wrote the draft does not grade it.

Pass/fail criteria for the grader:
1. All 9 moves present as sections (what is / one idea / real structure / mapped honestly / fits together / worked example / skeptical / means for you / sources).
2. The "real structure" section actually collapses N to M, it does not just re-list the surface items.
3. "Mapped honestly" marks at least one place the evidence is thin or absent, and invents no specifics.
4. At least one mermaid diagram that shows a relationship, not a restated list.
5. "What this means for you" names a real current project from CLAUDE.md or memory.
6. Sources present, every source has a title, no bare URLs or ids.
7. Writing-style clean: no em dashes, sentence case headings, no bold, no LLM brand names.

If any criterion fails, fix the draft and re-grade. Ask before a third iteration.

## Placement (ask, never guess)

When the draft passes the grader, do not decide where it goes. Show the user the finished doc and ask where to save it. Offer a sensible default of `Learning/deep-dives/<topic>/deep-dive.md` (new folder, parallel to `visual-synthesis/` and `hard-skills/`) but let the user override, including placing it next to related work if you've built a similar map before. Save only after the user names the location.

After saving, set the frontmatter `depended_by` if anything indexes the file, and name the file `deep-dive.md` inside its topic folder (or per the file-naming rule if the user wants it loose in an existing folder).

## Output

After saving, report:
1. The subject in one sentence.
2. The file path.
3. The load-bearing structure you found (the "N is really M" line).
4. The single most useful "what this means for you" point.
5. Whether any research was added (only in topic mode or with `--research`).

### Logging

The dive itself is content, not an OS improvement, so it does not go in `OS_IMPROVEMENTS.md`. Only log there if the dive surfaces a pattern you then apply to the OS (a rule, skill, or agent change), per `os-improvement-logging.md`.

## When NOT to use this skill

- A GitHub repo: use `/repo-dive`, it clones, symlinks, and produces the two-file analysis plus system-upgrade guide.
- A quick "what is X" answer: use the first-principles agent, no full doc needed.
- Live library or framework docs: use `/context7`.

## Exit checklist

Done when all of these are true:

- [ ] Input mode detected correctly (document / URL / topic) and research done only when the mode or `--research` allows it
- [ ] Draft written in the 9-move shape
- [ ] Grader agent ran with fresh context and all 7 criteria pass
- [ ] User asked where to place the file, and it was saved only after they answered
- [ ] Output report delivered: subject, path, load-bearing structure, top "means for you" point, research added or not
- [ ] Writing-style and doc-construction rules followed

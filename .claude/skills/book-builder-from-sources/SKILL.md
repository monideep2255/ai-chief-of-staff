---
name: book-builder-from-sources
author: human
description: "Synthesize a folder of existing markdown source files into a structured learning book, using the hard-skills chapter template with first-principles style, Mermaid diagrams, and progressive complexity. Output path: Learning/local-sources/<topic>/. Use when the user says: /book-builder-from-sources, \"turn these notes into a book\", \"make a book out of this folder\", \"synthesize my exports on <topic>\". Differs from the other two book builders, which generate from the model's own knowledge; this one reads local files and stays grounded in them. The book-inventory-check gate runs first."
scope: portable
argument-hint: <topic> --source <path>
depends_on:
  - .claude/rules/book-inventory-check.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - GROWTH_SYSTEM.md
---

# Book builder - from sources

Synthesize a folder of markdown research files into a structured, first-principles learning book. Same chapter template and style as `book-builder-hard-skills`, but reads from source material instead of generating from scratch.

## Invocation

```
/book-builder-from-sources <topic> --source <path>
```

**Examples:**

- `/book-builder-from-sources ai-product-management --source "Learning/local-sources/AI-Product-Management/"`
- `/book-builder-from-sources ai-agents --source "Learning/local-sources/AI-Agents-and-MCP/"`
- `/book-builder-from-sources career-growth --source "Learning/local-sources/Career-Growth/"`

## Workflow

### Step 1: parse input

Extract `<topic>` and `--source <path>`. Normalize topic to kebab-case directory name. Validate source path exists and contains `.md` files. If no `--source`, look for a matching folder under `Learning/local-sources/` (your own exported research threads, notes, or other local source material).

### Step 2: skim sources (phase 1 reading)

Read the source folder in two passes to manage context efficiently:

1. Read the folder's `README.md` for the file manifest
2. Read the first 40 lines of every `.md` file to identify its actual topic (Perplexity exports start with boilerplate  -  the real topic appears after)
3. Build a topic map: `{filename → actual topic/summary}`
4. Count total files, images, and estimate content volume

### Step 3: analyze and group

- Identify 8-15 distinct themes from the topic map
- Cluster files that cover the same topic from different angles
- Note unique frameworks, named sources, and data points worth preserving
- Identify gaps  -  topics referenced but not deeply covered

### Step 4: design book structure

Design 12-20 chapters in 4-6 parts following this progression:

```
Part 1: Foundations (What is this? Why does it exist?)
Part 2: Core building blocks (The fundamental pieces)
Part 3: How pieces fit together (Intermediate patterns)
Part 4: Advanced topics (Scaling, edge cases, trade-offs)
Part 5: Applied / real-world (Case studies, practical application)
Part 6: (Optional) Specialized topics
```

Present the TOC with source file mapping (which files feed each chapter). Ask: "Does this structure look right?" Wait for confirmation.

### Step 5: create directory structure

```
Learning/local-sources/<topic-name>/
├── README.md
├── Part_1_<Part_Name>/
│   ├── 01_<Chapter_Title>.md
│   ├── 02_<Chapter_Title>.md
├── Part_2_<Part_Name>/
│   ├── 03_<Chapter_Title>.md
```

Use underscores in filenames. Zero-padded two-digit chapter numbers.

### Step 6: write readme.md

Same format as `Learning/hard-skills/<topic>/README.md` in `book-builder-hard-skills` (title, how to use it, full table of contents with links, progress tracker, writing philosophy) but add a **Source Material** section listing: source folder path, number of files synthesized, and key attributions.

### Step 7: write chapters (phase 2 deep reading + writing)

For each Part, deeply read the full content of only the source files mapped to that Part's chapters. Then synthesize using the **hard-skills chapter template**:

```markdown
# Chapter n: <title>

## What is <x>?
[1-3 sentences. Plain language. Concrete analogy.]

## Why does it exist?
[The problem it solves. Start with the pain without this concept.]

## How does it work?
[2-4 sub-concepts, each with a Mermaid diagram. 3-5 diagrams total per chapter.]

## Real-world example
[Concrete scenario with a company name or relatable situation.]

## Key trade-offs
[Table format: Trade-off | What You Gain | What You Lose]

## What this means for you
[2-3 practical bullet points. Bridge to next chapter.]

## Quick quiz
[2-3 questions testing comprehension.]
```

### Step 8: source weighting

When synthesizing from multiple source files, not all sources deserve equal weight. Apply this hierarchy:

| Source type | Weight | Example |
|-------------|--------|---------|
| Primary research, official docs | 5 | arXiv papers, Anthropic docs, Meridian specs |
| Books, long-form original analysis | 4 | Textbooks, published frameworks |
| Conference talks, expert interviews | 3 | YouTube talks by practitioners, NeurIPS sessions |
| Newsletter deep-dives with analysis | 2 | Substacks with original thinking |
| Social threads, brief commentary | 1 | Twitter threads, Reddit comments, brief takes |

How to apply:

- When two sources disagree, the higher-weight source wins unless the lower-weight source provides newer data
- When making a strong claim, it must be supported by at least one weight-4 or weight-5 source
- Tag key insights with confidence: high (evidence from 2+ source types), medium (single source type but multiple files), low (single source only). Flag low-confidence insights in a separate section, not mixed into main chapters
- If the entire source folder is one source type (e.g., all newsletter exports), note this limitation in the README

### Step 9: source-specific rules (critical)

- **No copy-paste.** Rewrite all content in clear, authoritative first-principles voice
- **Deduplicate aggressively.** When multiple files cover the same concept, pick the clearest explanation and merge unique details
- **Preserve attributions.** Keep named sources (e.g., "According to Chip Huyen...", "the Anthropic agent guidelines...")
- **Preserve specifics.** Keep frameworks, step-by-step processes, data points, and real examples from the sources
- **Strip boilerplate.** Remove Perplexity headers, citation footnote markers, and conversation artifacts
- **Handle images.** If source folder contains relevant diagrams, copy to book directory and reference them

### Step 10: writing rules

Same rules as `book-builder-hard-skills`:

- Max 25 words per sentence. Active voice. No jargon without immediate definition
- 3-5 Mermaid diagrams per chapter (non-negotiable)
- **No literal `\n` in Mermaid diagrams.** Use actual line breaks. After writing, verify no `\n` text appears inside any ```mermaid block.
- Every concept starts with WHY before HOW
- Quality test: Could a smart high schooler understand this?

### Step 11: write source appendix

Create `Appendix_Source_Files.md` in the book root with:

- Table mapping each chapter to the source files it drew from
- Key frameworks and models referenced (with chapter links)
- Recommended resources extracted from sources

### Step 12: final check

1. Verify every file exists and is non-empty
2. Verify all README links are correct
3. Verify Mermaid diagram count (3-5 per chapter)
4. Report: "Book complete. N chapters across M parts. Synthesized from X source files."

## Options

- `--outline-only`  -  Only show proposed structure and source mapping
- `--part N`  -  Only write Part N
- `--chapter N`  -  Only write Chapter N
- `--chapters N-M`  -  Write range of chapters

## Anti-patterns

Check these before writing. If you catch yourself doing any of them, stop and fix before continuing.

- Restating source material without connecting it to other sources (summary, not synthesis)
- Treating all sources as equally authoritative regardless of origin (newsletter recap vs original research paper)
- Writing chapters that are summaries of individual source files rather than synthesized arguments across files
- Ignoring contradictions between sources instead of surfacing them as trade-offs or open questions
- Losing specific frameworks, data points, or named attributions from sources during rewriting

## Quality checks

Run these before delivering any batch of chapters. Every item must pass.

1. Every chapter draws from at least 2 source files (no chapter is a rewrite of a single source)
2. Contradictions between sources are surfaced, not silently resolved by picking one
3. Named frameworks and attributions from sources are preserved (check against source appendix)
4. Low-confidence insights (single source type) are flagged separately, not presented as established fact
5. The source appendix accurately maps every chapter to its source files (spot-check 3 chapters)

## Exit checklist

Done when all of these are true:

- [ ] Source folder was validated (exists, contains .md files)
- [ ] Book inventory check was run and user confirmed (per book-inventory-check rule)
- [ ] All source files were skimmed and topic-mapped (Step 2)
- [ ] 8-15 themes identified and clustered (Step 3)
- [ ] Book structure (12-20 chapters, 4-6 parts) was proposed and user confirmed (Step 4)
- [ ] Directory structure created with zero-padded chapter filenames (Step 5)
- [ ] README.md written with Source Material section (Step 6)
- [ ] Every chapter follows the hard-skills template (what/why/how/example/trade-offs/implications/quiz) (Step 7)
- [ ] Source weighting applied: strong claims backed by weight-4+ sources, low-confidence flagged separately (Step 8)
- [ ] No copy-paste from sources; attributions and specifics preserved (Step 9)
- [ ] 3-5 Mermaid diagrams per chapter, no literal `\n` in diagrams (Step 10)
- [ ] Source appendix maps every chapter to its source files (Step 11)
- [ ] All quality checks pass: every chapter draws from 2+ sources, contradictions surfaced, attributions preserved (Quality checks)
- [ ] Final check: all files exist, README links correct, diagram count verified (Step 12)

## Reference

Match the style, structure, and quality bar of the chapter template in Step 7 for any `Learning/hard-skills/<topic>/` book you have already written. When in doubt, read a chapter from your best existing book and match it.

---
name: book-builder-hard-skills
author: human
description: Generate a chapter-by-chapter learning book on a technical topic, in first-principles style with progressive complexity and Mermaid diagrams. Output path: Learning/hard-skills/<topic>/. Use when the user says: /book-builder-hard-skills, "write me a book on <technical topic>", "teach me <technology> properly", "I want to learn <technical subject> deeply". Differs from book-builder-soft-skills, which covers people and communication topics, and from book-builder-from-sources, which synthesizes existing local files instead of generating from scratch. The book-inventory-check gate runs first.
scope: portable
argument-hint: <topic>
depends_on:
  - .claude/rules/book-inventory-check.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - GROWTH_SYSTEM.md
---

# Book builder - hard skills

Generate a chapter-by-chapter learning book on any technical topic, written in first-principles style with progressive complexity and Mermaid diagrams.

## Invocation

```
/book-builder-hard-skills <topic>
```

**Examples:**
- `/book-builder-hard-skills distributed systems`
- `/book-builder-hard-skills kubernetes`
- `/book-builder-hard-skills knowledge graphs`
- `/book-builder-hard-skills django`

## Workflow

### Step 1: parse the topic

Extract the topic from the user's input. If too broad, ask ONE clarifying question.

Normalize to a kebab-case directory name:
- "distributed systems" -> `distributed-systems`
- "knowledge graphs" -> `knowledge-graphs`

### Step 2: research the topic

Use WebSearch to understand the topic's scope. Run 3-5 searches:

1. `"<topic> fundamentals concepts explained"`
2. `"<topic> learning roadmap beginner to advanced"`
3. `"<topic> key concepts architecture"`
4. `"<topic> common patterns and trade-offs"`
5. `"<topic> real-world use cases examples"`

If the user provides URLs, fetch those with WebFetch instead.

### Step 3: design the book structure

Design 12-20 chapters organized into 4-6 parts. Follow this progression:

```
Part 1: Foundations (What is this? Why does it exist?)
Part 2: Core building blocks (The fundamental pieces)
Part 3: How pieces fit together (Intermediate patterns)
Part 4: Advanced topics (Scaling, edge cases, trade-offs)
Part 5: Applied / real-world (Design exercises, case studies)
Part 6: (Optional) Interview prep or specialized topics
```

Present the proposed table of contents to the user. Ask: "Does this structure look right?" Wait for confirmation before writing chapters.

### Step 4: create directory structure

```
Learning/hard-skills/<topic-name>/
├── README.md
├── Part_1_<Part_Name>/
│   ├── 01_<Chapter_Title>.md
│   ├── 02_<Chapter_Title>.md
├── Part_2_<Part_Name>/
│   ├── 03_<Chapter_Title>.md
```

Use underscores in filenames. Zero-padded two-digit chapter numbers.

### Step 5: write the README.md

Include: book title, how to use it, full table of contents with links, progress tracker, and writing philosophy section.

Reference: once you have written a prior book with this skill, use its `Learning/hard-skills/<topic>/README.md` as the format template (title, how to use it, full table of contents with links, progress tracker, writing philosophy section).

### Step 6: write each chapter

Every chapter MUST follow this template:

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

### Step 7: writing rules (CRITICAL)

**Language:**
- No jargon without immediate definition
- Short sentences. One idea per sentence. Max 25 words
- Active voice always
- Use "you" to address the reader
- No buzzwords: "leverage", "utilize", "facilitate"

**Structure:**
- Every concept starts with WHY before HOW
- Build simple to complex within each chapter
- Each chapter self-contained but references previous ones

**Diagrams:**
- 3-5 Mermaid diagrams per chapter (non-negotiable)
- Use `flowchart`, `sequenceDiagram`, or `graph` types
- Every diagram followed by explanatory paragraph
- Keep node labels under 30 characters
- **No literal `\n` in Mermaid diagrams.** Use actual line breaks. After writing, verify no `\n` text appears inside any ```mermaid block.

**Quality test:**
- Could a smart high schooler understand this?
- Does every section answer "so what?"
- Is every analogy concrete and specific?

### Step 8: write in batches

Write chapters in batches by part. After each batch, report progress. Use parallel agents when possible for speed.

### Step 9: final check

1. Verify every file exists and is non-empty
2. Verify all README links are correct
3. Verify Mermaid diagram count (3-5 per chapter)
4. Report: "Book complete. N chapters across M parts."

## Options

- `/book-builder <topic> --outline-only` -- Only show proposed structure
- `/book-builder <topic> --part N` -- Only write Part N
- `/book-builder <topic> --chapter N` -- Only write Chapter N
- `/book-builder <topic> --chapters N-M` -- Write range of chapters
- `/book-builder <topic> --quick` -- Shorter chapters (skip Real-World Example and Quiz)

## Anti-patterns

Check these before writing. If you catch yourself doing any of them, stop and fix before continuing.

- Writing a chapter that is all theory with no concrete example, diagram, or "so what"
- Defining jargon using more jargon instead of plain language
- Repeating the same concept across chapters without building on it (summary vs progression)
- Using a Mermaid diagram as decoration rather than to clarify a relationship the prose alone cannot
- Skipping the "why does it exist?" section because the concept feels obvious

## Quality checks

Run these before delivering any batch of chapters. Every item must pass.

1. Every chapter has at least one concrete example (company name, specific scenario), not just theory
2. No chapter restates a prior chapter's content without building on it (check for duplicated explanations)
3. Mermaid diagrams have labeled edges and node labels under 30 characters
4. The "what this means for you" section contains specific actions, not vague advice like "consider using X"
5. Table of contents in README.md matches actual chapter headings exactly (run a diff if needed)

## Exit checklist

Done when all of these are true:

- [ ] Topic parsed and normalized to kebab-case directory name (Step 1)
- [ ] Book inventory check was run and user confirmed (per book-inventory-check rule)
- [ ] Web research completed (3-5 searches) to understand topic scope (Step 2)
- [ ] Book structure (12-20 chapters, 4-6 parts) was proposed and user confirmed (Step 3)
- [ ] Directory structure created with zero-padded chapter filenames (Step 4)
- [ ] README.md written with full ToC, progress tracker, and writing philosophy (Step 5)
- [ ] Every chapter follows the template (what/why/how/example/trade-offs/implications/quiz) (Step 6)
- [ ] Writing rules applied: max 25 words/sentence, active voice, no jargon without definition, no literal `\n` in Mermaid diagrams (Step 7)
- [ ] 3-5 Mermaid diagrams per chapter (non-negotiable) (Step 7)
- [ ] All quality checks pass: concrete examples, no duplicated explanations, labeled diagram edges, specific actions in implications, README ToC matches headings (Quality checks)
- [ ] Final check: all files exist and non-empty, README links correct, diagram count verified (Step 9)

## Reference

Match the style, structure, and quality bar set by the chapter template in Step 6. When in doubt, read a chapter from the best existing book under `Learning/hard-skills/` and match it.

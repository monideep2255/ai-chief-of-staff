---
name: book-builder-soft-skills
author: human
description: Generate a practice-oriented soft skills book with frameworks, scripts, scenarios, and self-assessments. Output path: Learning/soft-skills/<topic>/. Use when the user says: /book-builder-soft-skills, "write me a book on <people topic>", "help me get better at negotiation or influence or executive presence", "I need practice scripts for <situation>". Differs from book-builder-hard-skills, which covers technical topics, and from the board skill, which coaches one live situation rather than producing a reusable book. The book-inventory-check gate runs first.
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

# Book builder - soft skills

Generate a practice-oriented book on any soft skill topic. Written in first-principles style with frameworks, scripts, practice scenarios, and self-assessments.

**Key difference from hard-skills books:** Soft skills need practice, not just understanding. Every chapter gives you exact words to say, situations to practice, and ways to measure yourself.

## Invocation

```
/book-builder-soft-skills <topic>
```

**Examples:**
- `/book-builder-soft-skills executive presence`
- `/book-builder-soft stakeholder management`
- `/book-builder-soft influence and persuasion`
- `/book-builder-soft communication for leaders`

## Workflow

### Step 1: parse the topic

Extract the topic from the user's input. If too broad, ask ONE clarifying question.

Normalize to a kebab-case directory name:
- "executive presence" -> `executive-presence`
- "stakeholder management" -> `stakeholder-management`

### Step 2: research the topic

Use WebSearch to understand the topic's scope. Run 3-5 searches:

1. `"<topic> frameworks models practical"`
2. `"<topic> common mistakes what not to do"`
3. `"<topic> scripts examples what to say"`
4. `"<topic> self-assessment checklist"`
5. `"<topic> practice exercises drills"`

If the user provides URLs, fetch those with WebFetch instead.

### Step 3: design the book structure

Design 12-20 chapters organized into 4-6 parts. Follow this progression:

```
Part 1: Foundations (What is this skill? Why does it matter NOW?)
Part 2: Core frameworks (The mental models that drive the skill)
Part 3: In practice (Scripts, scenarios, and real situations)
Part 4: Advanced moves (Edge cases, high-stakes situations, recovery)
Part 5: Building the habit (Daily practice, self-assessment, growth plan)
Part 6: (Optional) Specialized contexts (AI era, remote work, cross-cultural)
```

Present the proposed table of contents to the user. Ask: "Does this structure look right?" Wait for confirmation before writing chapters.

### Step 4: create directory structure

```
Learning/soft-skills/<topic-name>/
├── README.md
├── Part_1_<Part_Name>/
│   ├── 01_<Chapter_Title>.md
│   ├── 02_<Chapter_Title>.md
├── Part_2_<Part_Name>/
│   ├── 03_<Chapter_Title>.md
```

Use underscores in filenames. Zero-padded two-digit chapter numbers.

### Step 5: write the readme.md

Include: book title, how to use it, full table of contents with links, progress tracker, and learning philosophy section.

Reference: use the README format from `book-builder-hard-skills` (title, how to use it, full table of contents with links, progress tracker, writing philosophy section) as the general structure, but adapt the philosophy section to emphasize practice over reading.

### Step 6: write each chapter

Every chapter MUST follow this template:

```markdown
# Chapter n: <title>

## What is <x>?
[1-2 sentences. Plain language. Relatable situation everyone has experienced.]

## Why does it matter?
[The cost of NOT having this skill. A specific story or scenario showing the gap. Make the reader feel the pain.]

## The framework
[One clear mental model. Name it. Make it memorable. 3-5 steps max.
Include ONE Mermaid diagram showing the framework visually.]

## What to say (scripts)
[3-5 specific scripts for common situations. Format:]

### Situation: [describe the moment]
**Instead of:** "[What most people say]"
**Say this:** "[The better version]"
**Why it works:** [1 sentence explaining the psychology]

## Practice scenarios
[2-3 scenarios the reader can mentally rehearse or role-play.]

### Scenario 1: [title]
**Setup:** [Describe the situation in 2-3 sentences]
**Your role:** [Who you are in this scenario]
**The challenge:** [What makes this hard]
**Try this:** [Suggested approach using the chapter's framework]
**Watch out for:** [Common mistake in this situation]

## Self-assessment
[A 5-question checklist. Each item is a concrete behavior, not a vague trait.]

Rate yourself 1-5 on each (1 = never do this, 5 = do this consistently):

- [ ] [Specific observable behavior 1]
- [ ] [Specific observable behavior 2]
- [ ] [Specific observable behavior 3]
- [ ] [Specific observable behavior 4]
- [ ] [Specific observable behavior 5]

**Score interpretation:**
- **20-25:** You're strong here. Focus on coaching others.
- **15-19:** Solid foundation. Pick one behavior to sharpen.
- **10-14:** Real growth opportunity. Practice one script daily this week.
- **Below 10:** Start with the first script. Use it in your next meeting.

## Common mistakes
[3-4 mistakes people make. Format:]

| Mistake | Why People Do It | What to Do Instead |
|---------|-----------------|-------------------|
| [Mistake 1] | [The psychology behind it] | [The fix] |

## What this means for you
[2-3 practical bullet points. One specific action to take this week. Bridge to next chapter.]
```

### Step 7: writing rules (CRITICAL)

**Language:**
- No jargon without immediate definition
- Short sentences. One idea per sentence. Max 25 words
- Active voice always
- Use "you" to address the reader directly
- No buzzwords: "leverage", "utilize", "facilitate", "synergy"
- Write like you're coaching a friend, not lecturing a class

**Structure:**
- Every concept starts with WHY before HOW
- Build simple to complex within each chapter
- Each chapter self-contained but references previous ones
- Lead with the pain of not having this skill

**Diagrams:**
- 1-2 Mermaid diagrams per chapter (frameworks and flows only)
- Use `flowchart` or `graph` types
- Diagrams show decision trees, frameworks, or process flows
- Every diagram followed by explanatory paragraph
- Keep node labels under 30 characters
- **No literal `\n` in Mermaid diagrams.** Use actual line breaks. After writing, verify no `\n` text appears inside any ```mermaid block.

**Scripts:**
- Every chapter MUST have at least 3 scripts with "Instead of / Say this" format
- Scripts must be specific enough to use verbatim
- Include the psychology of WHY the script works

**Practice:**
- Every chapter MUST have at least 2 practice scenarios
- Scenarios must be realistic workplace situations
- Include what to watch out for (common traps)

**Quality tests:**
- Could someone use the scripts in their next meeting?
- Does every self-assessment item describe an observable behavior?
- Is every "common mistake" something the reader will recognize in themselves?
- Would a new manager find this immediately useful?

### Step 8: write in batches

Write chapters in batches by part. After each batch, report progress. Use parallel agents when possible for speed.

### Step 9: final check

1. Verify every file exists and is non-empty
2. Verify all README links are correct
3. Verify every chapter has: framework, scripts (3+), scenarios (2+), self-assessment (5 items), common mistakes table
4. Report: "Book complete. N chapters across M parts."

## Options

- `/book-builder-soft <topic> --outline-only` -- Only show proposed structure
- `/book-builder-soft <topic> --part N` -- Only write Part N
- `/book-builder-soft <topic> --chapter N` -- Only write Chapter N
- `/book-builder-soft <topic> --chapters N-M` -- Write range of chapters
- `/book-builder-soft <topic> --quick` -- Shorter chapters (skip Practice Scenarios and Self-Assessment)

## Quality checks

Run these before delivering any batch of chapters. Every item must pass.

1. Every chapter has at least 3 scripts in "Instead of / Say this" format that could be used verbatim in a real meeting
2. Every self-assessment item describes an observable behavior, not a vague trait ("I pause before responding to criticism" not "I handle feedback well")
3. Practice scenarios are specific enough to role-play, with a named situation, a role, and a clear challenge
4. The "common mistakes" table has a "Why People Do It" column that names the psychology, not just the behavior
5. No chapter teaches a framework without at least one script showing how to apply it in conversation

## Reference

Any existing book under `Learning/hard-skills/` is a good reference for general book format (README structure, file naming, table of contents). Adapt the chapter template to the soft-skills format above.

## Exit checklist

Done when all of these are true:

- [ ] book-inventory-check shown and confirmation received before generating
- [ ] Directory created under Learning/soft-skills/<topic>/
- [ ] README with full table of contents written
- [ ] All chapters written following the chapter template
- [ ] Quality tests passed: scripts, scenarios, self-assessment per chapter
- [ ] Final check run: every file exists, README links correct, completion reported

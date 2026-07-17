---
name: repo-dive
author: human
description: Clone an external GitHub repo, symlink it into Reference-Repos, and generate two deep-dive markdown files (Everything + System-Upgrade-Guide). TRIGGER when user shares a GitHub URL and wants to analyze/study/learn from it, says "dive into this repo", "analyze this repo", or "what can we learn from this". DO NOT TRIGGER for repos that are already cloned or for general GitHub operations.
scope: project
argument-hint: <github-url> [--name <display-name>]
produces_docs: true
depends_on:
  - .claude/rules/os-improvement-logging.md
  - .claude/rules/
  - .claude/skills/
  - .claude/agents/
  - OS_IMPROVEMENTS.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# /repo-dive - external repo deep dive

Clone a GitHub repo, symlink it into `Reference-repos/`, and produce two first-principles analysis files.

## Invocation

```
/repo-dive https://github.com/user/repo.git
/repo-dive https://github.com/user/repo.git --name "Custom Name"
```

## What it does

### Step 1: clone + symlink

1. Clone the repo to `~/your-projects-folder/<repo-name>/`
2. Create folder `Reference-repos/<repo-name>-Deep-Dive/`
3. Symlink the cloned repo into that folder

**Sandbox note:** the clone target (`~/your-projects-folder/<repo-name>/`) sits outside the sandbox-writable allowlist, so `git clone`, `git fetch`, and `git pull` fail under the sandbox with "Operation not permitted" (FETCH_HEAD or work-tree creation). Run these git commands with the sandbox disabled. Folder creation and symlinking inside `Reference-repos/` (within the repo) stay sandboxed. If the repo already exists, fetch and fast-forward instead of re-cloning, then update the existing deep-dive files rather than regenerating from scratch.

### Step 2: deep dive analysis

Read the repo thoroughly:
- README.md, CLAUDE.md, CHANGELOG.md
- Architecture docs
- Key source files (entry points, core modules, config)
- File tree structure
- Examples/tests

### Step 3: generate two files

#### File 1: `everything-<repo-name>-deep-dive.md`

First-principles analysis. Follow this structure exactly:

```markdown
# <repo name>: first-principles deep dive

## 1. what is this repo?
(One paragraph. What it does. Who made it. Version. License.)

## 2. why does it exist?
(The problem it solves. The axiom it's built on. What existing solutions fail at.)

## 3. how is it structured?
(Mermaid diagram of architecture. Core subsystems. Key directories.)

## 4. key concepts
(The 4-6 most important ideas. Each with a heading, explanation, and code/diagram.)

## 5. <domain-specific deep dive>
(Name this section for what's most interesting. E.g., "Control Plane Deep Dive" or "The Plugin System".)

## 6. comparison to other approaches
(Table comparing to alternatives. Be specific.)

## 7. what's relevant to your work
(Map repo concepts to the user's current projects: Atlas, KG, AI enablement.)

## 8. what to skip
(Features/sections not worth learning right now, with reasons.)

## 9. key takeaways
(5 numbered insights. Each one sentence of fact, then one of implication.)
```

**Style rules:**
- Write like you're explaining to someone smart but unfamiliar
- Use Mermaid diagrams for architecture (at least 2)
- Use tables for comparisons
- Be honest about what's relevant and what isn't
- No filler. Every section earns its space.

**Anti-patterns (do not produce these):**
- Sections that just restate the README without analysis or original insight
- "What's relevant to your work" that lists everything as relevant - be honest about what doesn't apply
- Mermaid diagrams that are just box-and-arrow restatements of folder structure - add relationships, data flow, or decision logic
- Takeaways too generic to act on ("this repo has good architecture") - each takeaway needs a specific implication
- Filler phrases: "in today's rapidly evolving landscape", "it's worth noting that", "as we can see"
- System upgrade guide that recommends adopting everything - the value is in what you skip
- Comparison tables where every row says "yes" for the repo being analyzed

#### File 2: `system-upgrade-guide.md`

Honest assessment sorted into three explicit buckets. The user must always see all three: (A) what this repo confirms is ALREADY handled by the OS, (B) what is genuinely new and worth applying, with the value spelled out, and (C) what was deliberately skipped and why. Never collapse these into one flat "here are some proposals" list. Bucket A is not filler: it shows the user their shared repo reinforced rules they already built, which is the whole point of a mature system, and burying it as "you already have this" reads as dismissal.

**Grounding requirement (bucket A must be real, not guessed):** before writing bucket A, actually scan `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, and `OS_IMPROVEMENTS.md` for existing coverage of each repo pattern. Every bucket A entry MUST name the actual file it maps to. If you cannot name the file, it is not bucket A, move it to bucket B.

Follow this structure:

```markdown
# System upgrade guide: what to take from <repo name>

*<Date>*

(Opening paragraph: honest assessment. What applies, what is already handled, what does not fit.)

## Three buckets at a glance
(Mermaid diagram: three buckets - Already in the OS / New, worth applying / Skipped)

## Bucket A - already in the OS (this dive reinforces)
For each repo pattern the OS already enforces:
- Repo pattern: <what the repo does>
- Already lives in: <exact OS component path, e.g. .claude/rules/goal-contracts.md>
- What this dive adds: <citable worked example / independent confirmation / teaching material - NOT a new rule>

## Bucket B - new, worth applying (should I apply?)
For each genuinely new pattern:
- What it is: <one line>
- Value if applied: <concrete outcome - what improves, for which project (Atlas, Search, growth, etc.)>
- Where it lands: <exact component that would change or be created>
- How to apply: <specific edit or action, with file path>
- When to act: <concrete trigger>
- Apply now? <a direct yes/ask prompt for the user>

## Bucket C - ignored / not needed (and why)
For each notable pattern deliberately NOT taken:
- What it is: <one line>
- Why skip: <the specific reason - a problem the user does not have, complexity not worth the return, or it duplicates an existing component>

## Summary
(Table: pattern | bucket A/B/C | component | action)

## No system changes needed / system changes made
(Be explicit about whether this changes the Claude Code setup or not.)
```

**Decision framework (which bucket does a pattern go in?):**
- Already covered by a rule, skill, or agent? Bucket A, and name the file.
- New, solves a problem the user actually has (Atlas, Search, KG, growth), and worth its complexity? Bucket B.
- New but solves a problem he does not have, or costs more than it returns? Bucket C.

**Anti-patterns for the upgrade guide:**
- Collapsing the three buckets into one flat "proposals" list, the user has explicitly asked to always see already-applied, new, and skipped as separate buckets
- Bucket A entries that do not name a real OS file, if you cannot cite the file it is not already handled
- Bucket B entries missing the "value if applied" line or the "apply now?" prompt, a new pattern without its value stated is not actionable
- Empty bucket C, if you matched or adopted everything you did not look hard enough for what does not fit
- Vague "how to apply" ("consider adopting this"), must include specific file paths and actions
- "When to act: eventually", every bucket B pattern needs a concrete trigger (next retro, next time X happens, etc.)

## Step 4: verify output

After generating both files, run these inline checks before reporting:

**For everything-deep-dive.md:**
- [ ] All 9 required section headings present (sections 1-9)
- [ ] At least 2 Mermaid diagrams (search for triple-backtick mermaid blocks)
- [ ] At least 1 comparison table in section 6
- [ ] "What to skip" section actually skips things (not everything marked relevant)
- [ ] Takeaways are specific (each has an "implication" sentence, not just a fact)

**For system-upgrade-guide.md:**
- [ ] All three buckets present (A already-in-OS, B new, C skipped)
- [ ] Every bucket A entry names a real OS file path (grounding check - open the file if unsure it covers the pattern)
- [ ] Every bucket B entry has a "value if applied" line and an explicit "apply now?" prompt
- [ ] Each bucket B pattern has "how to apply" with specific file paths and a concrete "when to act" trigger
- [ ] Bucket C has at least 1 entry with a reason (not everything adopted or matched)
- [ ] Summary table present with pattern/bucket/component/action columns

If any check fails, fix the file before reporting.

## Output

After generating both files, report:
1. What the repo is (one sentence)
2. Files created (with paths)
3. Key takeaways (top 3, one line each)
4. Whether any system changes were made
5. Personal OS applications, reported as the three buckets (lead with these, this is what the user most wants to see):
   - Already in the OS (reinforced): each match, naming the exact rule/skill/agent file, and what the dive adds to it (worked example, confirmation)
   - New, worth applying: each with its value spelled out and an explicit "apply now?" prompt naming the file that would change
   - Skipped: a one-line list with the reason each does not fit

### Logging adopted patterns

The dive itself is a source, not an improvement. If you (or the user) then apply any pattern from the upgrade guide to the OS, log each applied pattern as a row in `OS_IMPROVEMENTS.md` per `os-improvement-logging.md` (source = the repo name followed by "repo dive", e.g. "storm repo dive"). Patterns surfaced but not yet applied go in the "Proposed" table. Do not log the dive itself unless something was adopted from it.

## Exit checklist

Done when all of these are true:

- [ ] Repo cloned and symlinked into Reference-repos/
- [ ] Both files generated: everything-deep-dive and system-upgrade-guide
- [ ] Step 4 output verification checks all passed
- [ ] Output report delivered: what it is, files, takeaways, system changes, OS applications
- [ ] Writing-style followed and output structured per the doc-construction rule

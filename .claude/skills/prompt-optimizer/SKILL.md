---
name: Prompt Optimizer
author: human
description: "Optimize a prompt for token efficiency, parallelism, and background agents. TRIGGER on /optimize, \"optimize this prompt\", \"why is this burning tokens\", \"rewrite this prompt\". Works on the prompt text, unlike parallel-first, which governs dispatch."
scope: portable
depends_on: []
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# Prompt optimizer skill

This skill analyzes user prompts for token efficiency and suggests optimizations to reduce token usage while maintaining or improving task execution quality.

## Purpose

**Save tokens** by identifying and fixing common prompt inefficiencies:
- Unnecessary file pre-loading with `@` mentions
- Over-verbose instructions
- Sequential steps that could be parallelized
- Missing background agent opportunities
- Redundant context loading

## When to use

### ✅ use this skill for:
1. **Complex multi-step tasks** (3+ steps)
2. **Prompts with multiple `@` file mentions** (2+ files)
3. **Long-running operations** (tests, builds, deployments)
4. **When unsure about efficiency** (learning phase)
5. **Tasks involving multiple agents** (doc-sync + git-sync, etc.)

### ❌ skip this skill for:
1. **Simple single-step tasks** ("Read this file", "Update line 42")
2. **Already concise prompts** (<50 words, no @ mentions)
3. **Quick edits** (typo fixes, adding a comment)
4. **Trivial operations** (git status, ls, etc.)

## How to invoke

```
/optimize [your prompt here]
```

**Example:**
```
/optimize @file1.md @file2.md @file3.md Review these files,
create a comprehensive skill, then run doc-sync to update all
documentation, then use git-sync to push everything to GitHub
with a detailed commit message
```

## Optimization analysis framework

### 1. file loading patterns

An `@` mention is the right tool when the files are known and the task will read them: it attaches each file once, at a stable place in the prefix, and costs less than a search that rediscovers the same files. It wastes tokens when a prompt attaches files the task never reads, or a large file of which only a slice matters.

Rule:
- Keep `@` mentions for files the task will certainly use.
- For a large file where only one section matters, name the section or ask for a grep first.
- For files the task may not need, drop the mention and name the folder or topic so the agent searches instead.

### 2. sequential vs parallel execution

**Anti-pattern: Sequential steps that could be parallel**
```
❌ "Create skill, then run doc-sync, then run git-sync"
   Time: 60s total
   Token cost: All three in conversation context

✅ "Create skill, then run doc-sync and git-sync in parallel"
   Time: 30s total
   Token savings: ~20-30%
```

**Rule:**
- If steps have no dependencies: Suggest parallel execution
- If steps are agents: Suggest parallel tool calls in one message
- If long-running: Suggest background execution

### 3. background agent opportunities

**Anti-pattern: Foreground for long tasks**
```
❌ "Run full test suite and fix all failures"
   Blocks for 5-10 minutes
   Token cost: Entire execution in conversation

✅ "Run full test suite and fix all failures in background"
   Returns immediately
   Token savings: ~40-60% (separate process)
```

**Rule:**
- If task > 2 minutes: Suggest background
- If task blocks user: Suggest background
- If multiple long tasks: Suggest parallel background
- Examples: tests, builds, scans, deployments, large analysis

### 4. verbosity reduction

**Anti-pattern: Over-instructive prompts**
```
❌ "Please carefully review all the files in the visualizations
    directory, analyze the patterns, think about what would make
    a good skill, create a comprehensive SKILL.md file making sure
    to follow all the standards, then sync the documentation files,
    and finally push everything to GitHub"
   Cost: ~200 tokens just for the prompt

✅ "Create Visualization Standards skill, sync docs, push to GitHub"
   Cost: ~30 tokens

Savings: ~170 tokens (85%)
```

**Rule:**
- Remove filler words: "please", "carefully", "make sure"
- Remove obvious instructions: "think about", "analyze"
- Use imperative verbs: "Create", "Sync", "Push"
- Trust agent competence: I know how to follow standards

### 5. context redundancy

**Anti-pattern: Repeating context I already have**
```
❌ "You know we're working on Atlas which is a search
    product. We have visualization files. Create a
    skill for those visualizations."
   Cost: ~100 tokens of redundant context

✅ "Create Visualization Standards skill"
   Cost: ~10 tokens

Savings: ~90 tokens (I already know the project context)
```

**Rule:**
- Remove project background (I know from CLAUDE.md)
- Remove file locations I can find (use Glob/Grep)
- Remove standards I already follow

### 6. dated prompt patterns

Check the prompt for text written for older models, because on current models it over-applies:
- Capitalized emphasis (MUST, NEVER, CRITICAL) with no stated reason: state the constraint plainly and give the reason.
- "Think step by step" or "plan before acting": remove it, since thinking depth is set by the effort setting and not by prose.
- Numbered choreography for a judgment task: state the outcome, the constraints, and how to verify, and keep numbered steps only where order matters.
- Hard word or item caps: say who reads the output and what they need.
- Long prohibition lists: state the goal, and keep a prohibition only when its failure still happens or it encodes a real policy.

## Optimization output format

When analyzing a prompt, provide:

### 1. analysis summary
```markdown
📊 **Prompt Analysis**

Original prompt: [user's prompt]
Token cost estimate: ~X,XXX tokens

Issues found:
- 🔴 High: 3 large files pre-loaded with @ mentions (~6,000 tokens)
- 🟡 Medium: Sequential steps could be parallel (~20% time savings)
- 🟡 Medium: Long-running task not in background (~2,000 tokens)
- 🟢 Low: Verbose phrasing (~100 tokens)

Total potential savings: ~8,100 tokens (62%)
```

### 2. optimized prompt
```markdown
✅ **Optimized Prompt**

"Create Visualization Standards skill from visualizations/ folder,
then run doc-sync and git-sync in parallel in background"

Estimated cost: ~5,000 tokens
Time to complete: ~30 seconds (vs 60s original)
```

### 3. explanation
```markdown
💡 **What Changed**

1. Removed @ mentions for 3 files → I'll read them as needed
2. Simplified instructions → Removed "carefully review", "analyze patterns"
3. Added "in parallel" → doc-sync and git-sync run concurrently
4. Added "in background" → Won't block, can continue working

Breakdown:
- File loading savings: ~6,000 tokens (3 files × ~2,000 each)
- Verbosity reduction: ~100 tokens
- Background execution: ~2,000 tokens (separate process)
```

### 4. user confirmation
```markdown
🎯 **Accept Optimization?**

[Y] Yes, use optimized prompt (recommended)
[N] No, use original prompt
[E] Explain more
```

## Examples

### Example 1: unneeded files

Original:
```
@docs/architecture/ARCHITECTURE.md @docs/schema/SCHEMA.md
@visualizations/DIAGRAMS.md @docs/archive/OLD_NOTES.md Review all these
architecture files and create a comprehensive summary document
```

Analysis:
```
Issues:
- OLD_NOTES.md is attached but the task does not need it
- "comprehensive" is vague
- The other three files are known and needed, so their mentions stay
```

Optimized:
```
@docs/architecture/ARCHITECTURE.md @docs/schema/SCHEMA.md
@visualizations/DIAGRAMS.md Summarize how these three fit together in one
document for a new engineer
```

### Example 2: sequential agent tasks

**Original:**
```
Create a new skill for testing standards. After that's done,
run the doc-sync agent to update all documentation. When that
finishes, use git-sync to push changes to GitHub.
```

**Analysis:**
```
📊 Issues:
- 🟡 Sequential execution (doc-sync → git-sync could be parallel)
- 🟢 Verbose: "After that's done", "When that finishes"

Savings: ~30% execution time, ~500 tokens
```

**Optimized:**
```
Create Testing Standards skill, then run doc-sync and git-sync in parallel
```

### Example 3: long-running task

**Original:**
```
Run the entire test suite, analyze all failures, fix them,
and rerun tests until everything passes
```

**Analysis:**
```
📊 Issues:
- 🔴 Long task (5-10 min) not in background
- 🔴 Blocks all other work

Savings: ~10,000 tokens + enables concurrent work
```

**Optimized:**
```
Run full test suite and fix all failures in background
```

### Example 4: over-instructive

**Original:**
```
I need you to carefully read through the codebase and think
about the architecture. Then analyze the database schema and
understand how it works. After that, please create a detailed
diagram that shows all the relationships and make sure it
follows our visualization standards.
```

**Analysis:**
```
📊 Issues:
- 🟡 Verbose: "carefully", "think about", "please", "make sure"
- 🟡 Obvious steps: "understand how it works"
- 🟢 Redundant: "follows our standards" (I always do)

Savings: ~150 tokens (70%)
```

**Optimized:**
```
Create database schema diagram showing all relationships
```

## Estimating savings

Do not quote token figures as fact. A file's real cost is its size, which `/context` shows, so measure it. State savings qualitatively (large, moderate, small) and name the cause: attached files the task never reads, background the project instructions already hold, or sequential steps that could run together. Background execution saves the user's waiting time, not tokens. Recommend an optimization when it changes cost or time in a way the user would notice, and mention smaller ones briefly.

## Integration with other skills

### Works well with:
- **Git_Workflow**: Optimize commit/push operations
- **Documentation_Standards**: Optimize doc updates
- **Testing_Standards**: Optimize test runs (suggest background)

### Complements:
- **Architecture_Patterns**: For large codebase exploration
- **Python_Code_Standards**: For code review optimization

## Usage instructions

**For Claude Code:**
When user invokes `/optimize [prompt]`:

1. **Analyze** the prompt using the framework above
2. **Identify** anti-patterns and calculate savings
3. **Generate** optimized version
4. **Explain** changes and savings
5. **Ask** for user confirmation
6. **Execute** if user accepts (Y)

## Meta: when NOT to optimize

**Don't over-optimize:**
- User preference for verbosity (clarity over brevity)
- Educational context (user wants to see full process)
- Debugging (user needs detailed step-by-step)
- Compliance (user must document each step)

**Respect user intent:**
- If user says "step by step" → Don't parallelize
- If user says "show me everything" → Don't background
- If user is learning → Explain more, optimize less

## Feedback loop

After executing optimized prompt, provide brief feedback:

```
✅ Task completed successfully

📊 Optimization Results:
- Original estimate: ~15,000 tokens
- Actual usage: ~6,500 tokens
- Savings: ~8,500 tokens (57%)
- Time: 30s (vs estimated 60s)

💡 Patterns learned:
- Removed 3 @ mentions → Let me find files
- Parallel agent execution → 50% faster
```

This reinforces learning for future prompts.

## Exit checklist

Done when all of these are true:

- [ ] Prompt analyzed across the 6 framework dimensions
- [ ] Inefficiencies identified with token estimates
- [ ] Optimized prompt generated
- [ ] Changes explained with a savings breakdown
- [ ] User confirmation requested before executing the optimized prompt

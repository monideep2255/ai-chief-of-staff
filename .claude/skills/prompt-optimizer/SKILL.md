---
name: Prompt Optimizer
author: human
description: "Analyze and optimize a prompt for token efficiency, parallelization opportunities, and background agent usage. Use when the user says: /optimize, \"optimize this prompt\", \"make this prompt better\", \"why is this burning so many tokens\", \"can this run in parallel\", \"rewrite this prompt\". Operates on the prompt text itself, unlike parallel-first, which governs how the agent dispatches work once the prompt is understood."
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

**Anti-pattern: Pre-loading with `@` mentions**
```
❌ "@file1.md @file2.md @file3.md Review these and create a skill"
   Cost: ~2,000-8,000 tokens (loads entire files)

✅ "Create a skill by analyzing files in the visualizations/ folder"
   Cost: ~500 tokens (I read only what I need)

Savings: ~1,500-7,500 tokens (60-90%)
```

**Rule:**
- If `@` mentions > 1 file: Suggest folder pattern or let me explore
- If `@` mentions large files (>500 lines): Always suggest removal
- If user needs specific files: Suggest reading during execution

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

### Example 1: file-heavy prompt

**Original:**
```
@docs/architecture/ARCHITECTURE.md @docs/schema/SCHEMA.md
@visualizations/DIAGRAMS.md Review all these architecture files
and create a comprehensive summary document
```

**Analysis:**
```
📊 Issues:
- 🔴 3 large files (~6,000 tokens loaded)
- 🟢 "comprehensive" is vague

Savings: ~6,000 tokens (92%)
```

**Optimized:**
```
Create architecture summary from docs/architecture/, docs/schema/,
and visualizations/ folders
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

## Token savings calculator

Use this mental model to estimate savings:

```
@ mention (large file):     ~2,000 tokens each
@ mention (medium file):    ~1,000 tokens each
@ mention (small file):     ~300 tokens each
Verbose phrasing:           ~100-200 tokens
Background execution:       ~2,000-5,000 tokens (long tasks)
Parallel execution:         ~20-30% time (same tokens)
Redundant context:          ~100-500 tokens
```

**Threshold for suggesting optimization:**
- Savings > 3,000 tokens: **Strongly recommend**
- Savings 1,000-3,000: **Recommend**
- Savings < 1,000: **Optional** (mention briefly)

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

**For Users:**
Use this skill when:
- Prompt feels long or complex
- Using multiple @ mentions
- Chaining multiple agent tasks
- Running tests, builds, or deployments
- Learning optimal prompting patterns

**Skip this skill when:**
- Prompt is already short (<50 words)
- Single simple task
- No @ mentions
- Quick edits

## Success metrics

Track these over time:
- Average tokens per task (should decrease)
- Token savings per optimization (aim for >3,000)
- User acceptance rate (aim for >80%)
- Optimization invocation frequency (should decrease as user learns)

**Goal:** After 10-20 optimizations, user internalizes patterns and rarely needs this skill.

## Advanced patterns

### Pattern 1: multi-agent orchestration
```
❌ "Run agent1, wait, then agent2, wait, then agent3"
✅ "Run agent1, agent2, and agent3 in parallel"
```

### Pattern 2: exploration vs specification
```
❌ "Read @file1, @file2, @file3 to find X"
✅ "Search for X in project/" (I'll use Grep/Glob)
```

### Pattern 3: background + foreground mix
```
❌ "Run tests and update docs"
✅ "Run tests in background, update docs now"
   (Parallel work: tests run while docs update)
```

### Pattern 4: conditional optimization
```
If (file_mentions > 1) → Suggest folder pattern
If (task_time > 2min) → Suggest background
If (independent_steps > 1) → Suggest parallel
If (verbosity > 100_words) → Suggest simplification
```

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

- [ ] Prompt analyzed across the 5 framework dimensions
- [ ] Inefficiencies identified with token estimates
- [ ] Optimized prompt generated
- [ ] Changes explained with a savings breakdown
- [ ] User confirmation requested before executing the optimized prompt

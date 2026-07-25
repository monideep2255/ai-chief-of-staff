---
name: system-retro
author: human
description: Weekly self-improvement loop for the personal OS itself. Audits rules, skills, agents, workflows, memory, and documentation for staleness, gaps, contradictions, and dead weight. TRIGGER when user says "system retro", "audit the OS", "what needs fixing", "check system health", "weekly retro", or when the session greeting shows the retro reminder. Also trigger on "what's stale", "clean up the system", or "OS health check". DO NOT TRIGGER for content retros (use forge --retro) or code reviews (use code-reviewer).
scope: project
argument-hint: [--quick] [--deep] [--focus AREA]
depends_on:
  - .claude/rules/
  - .claude/skills/
  - .claude/agents/
  - .claude/WHATS_NEW.md
  - CLAUDE.md
  - AGENTS.md
  - GOALS.md
  - GROWTH_SYSTEM.md
  - EXTENSIONS.md
  - DEPENDENCIES.md
  - .claude/skills/objective-review/SKILL.md
  - .claude/rules/anti-rationalization.md
  - .claude/scripts/verify_counts.sh
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - GROWTH_SYSTEM.md
---

# System retro

A self-improvement loop for the personal OS. The system audits itself, finds its own weaknesses, proposes fixes, and tracks improvement cycles over time.

**Analogy:** Like a chess player who after every game writes new puzzles targeting the patterns they missed, then trains on those puzzles until they stop failing.

## Invocation

```
/system-retro                    # Full weekly audit (Saturday default)
/system-retro --quick            # Fast scan - staleness + top 3 issues only
/system-retro --deep             # Deep audit with implementation of top fixes
/system-retro --focus rules      # Audit only one area
/system-retro --focus skills
/system-retro --focus workflows
/system-retro --focus memory
/system-retro --focus docs
/system-retro --focus growth
```

**Areas:** `rules` | `skills` | `workflows` | `memory` | `docs` | `growth`

---

## Read-first

| Source | Path | What to extract |
|--------|------|-----------------|
| Rules | `.claude/rules/` | All rule files for staleness/contradiction audit |
| Skills | `.claude/skills/` | All skill files for usage and overlap audit |
| Agents | `.claude/agents/` | Agent definitions for coverage audit |
| Goals | `GOALS.md` | Current quarterly goals and metrics |
| Growth system | `GROWTH_SYSTEM.md` | Pillar health expectations |
| Last retro | `Forge/logs/system-retro/` | Most recent retro report for comparison |
| Validation script | `.claude/scripts/validate_skill_rules.sh` | Run during skills audit |
| Count script | `.claude/scripts/verify_counts.sh` | Run during documentation audit (count verification) |
| Skill memory | `.claude/skills/system-retro/memory.md` | Lessons from past retros |

## Preconditions

Before starting, verify:
1. `.claude/` directory exists with rules/, skills/, agents/ subdirectories
2. `GOALS.md` and `GROWTH_SYSTEM.md` exist at repo root
3. `Forge/logs/system-retro/` exists for saving the report
4. At least one prior retro exists (for comparison in Step 6), or this is the first retro

If any system directory is missing, flag it as a critical finding rather than failing silently.

## The self-improvement loop

This mirrors the MiniMax M2.7 pattern:

```
┌─────────────────────────────────────────────┐
│  1. AUDIT - Run the system on real work     │
│     Review git history, corrections,        │
│     rule violations, unused infrastructure  │
│                                             │
│  2. DIAGNOSE - Find failures                │
│     Contradictions, gaps, dead weight,      │
│     staleness, missing coverage             │
│                                             │
│  3. PRESCRIBE - Write fixes                 │
│     New rules, updated skills, removed      │
│     dead weight, new workflows              │
│                                             │
│  4. TRACK - Measure improvement             │
│     Compare to last retro, count fixes      │
│     applied vs proposed, system health score│
│                                             │
│  5. REPEAT - Next cycle                     │
│     Each Saturday, the system gets sharper   │
└─────────────────────────────────────────────┘
```

---

## Mode: standard (default)

### Step 1: gather data

Read these files to understand the current system state:

**System files:**
- `.claude/rules/` - all rule files
- `.claude/skills/` - all SKILL.md files (just the frontmatter + first 10 lines for overview)
- `.claude/agents/` - all agent definitions
- `CLAUDE.md` - current focus and system index
- `AGENTS.md` - universal AI context
- `GOALS.md` - quarterly goals
- `GROWTH_SYSTEM.md` - growth system architecture
- `.claude/WHATS_NEW.md` - recent system changes

**Memory:**
- Read all files in the memory directory

**History:**
- `git log --since="1 week ago" --oneline` - what changed
- `git log --since="1 week ago" --name-only` - which files were touched
- `git log --since="1 week ago" --diff-filter=A --name-only` - new files added
- `git log --since="1 week ago" --diff-filter=D --name-only` - files deleted

**Previous retro (if exists):**
- Read the most recent file in `Forge/logs/system-retro/` to compare against last cycle

### Step 2: audit each area

Run through each area systematically. For each, ask these diagnostic questions:

#### Rules audit
- **Contradictions:** Do any rules conflict with each other?
- **Staleness:** Do any rules reference outdated information (old projects, completed work)?
- **Gaps:** What common corrections appear in git history that don't have a corresponding rule?
- **Dead weight:** Are any rules never triggered (no matching file patterns, no relevant work)?
- **Clarity:** Are any rules ambiguous enough that they could be interpreted two ways?
- **Completeness:** Are there patterns in how the user corrects Claude that should be rules but aren't?
- **Categorization:** Does each rule's frontmatter scope (alwaysApply vs globs) match how it is documented? Two checks. First, frontmatter integrity: flag any rule that declares both `alwaysApply: true` and a `globs:` field, which is contradictory (book-inventory-check did this on June 22; it must pick one). Build the ground truth: a rule with a `globs:` field is glob-scoped, otherwise it is always-on. Second, doc accuracy: the SYSTEM_OVERVIEW always-on and glob-scoped tables must list exactly those rules, with the split counts matching. The os-maintain count script does not check this (it checks totals, not the always-on/glob split), so it is a retro responsibility. Apply the fix as a trivial fix unless a rule's intended scope is genuinely ambiguous.

#### Skills audit

**Phase 1: deterministic pre-filter (run first, before any LLM review)**

Build a staleness list using git history and session logs. This is mechanical - no judgment required yet.

```bash
# Skills not touched in git history in 30+ days
# --format= suppresses commit messages, which otherwise mention SKILL.md paths
# and get picked up as if they were changed files
git log --since="30 days ago" --format= --name-only -- .claude/skills/ | grep 'SKILL\.md' | sort -u

# Skills with author: agent (GC-eligible, review separately from human-authored)
# ^ anchors to the frontmatter key; without it this matches the prose in this
# very file and always reports system-retro as agent-authored
grep -l "^author: agent" .claude/skills/*/SKILL.md 2>/dev/null
```

Classify each skill into one of three buckets before proceeding:
- **Active:** appeared in git history in last 30 days
- **Stale:** last touched 30-90 days ago (flag for LLM review)
- **Archive-eligible:** not touched in 90+ days OR has `author: agent` and is stale (flag for LLM review)

Note: all current skills have `author: human` and are protected from auto-archival. The `author: agent` bucket is for future agent-authored skills.

**Phase 2: LLM review (run only on Stale and Archive-eligible buckets)**

For skills flagged in Phase 1:
- **Usage:** Which skills have been invoked recently (check git history for output files)?
- **Overlap:** Do any skills duplicate functionality?
- **Gaps:** What tasks does the user do repeatedly that don't have a skill?
- **Quality:** Do skill outputs match the writing style and formatting rules?
- **Integration:** Do skills properly reference each other where relevant?
- **Staleness:** Do any skills reference outdated projects, tools, or workflows?

For all skills (not filtered):
- **Orphaned dependencies:** Run `bash .claude/scripts/validate_skill_rules.sh` to check that `depends_on` paths still exist and skills reference the rules they should (Atlas skills reference atlas-production-standards, doc-producing skills reference doc-construction, 4+ step skills have exit checklists)
- **Rule conflicts:** Scan all rules for contradicting guidance. Two rules that give opposite instructions for the same trigger are a conflict. Common areas: permission states (one rule allows what another denies), scope overlap (two rules claim the same glob pattern with different behavior)

#### Workflows audit (Reference/Agent_workflows/)
- **Coverage:** What common task patterns don't have a workflow?
- **Usage:** Are workflows being referenced by the communication-style rule's workflow awareness?
- **Quality:** Do workflows follow first-principles structure?
- **Staleness:** Do any workflows reference tools or approaches that have been superseded?

#### Memory audit
- **Staleness:** Do any memories reference completed projects or outdated preferences?
- **Gaps:** What has the user repeatedly told Claude in recent sessions that isn't in memory?
- **Duplicates:** Are any memories redundant with each other or with rules?
- **Accuracy:** Do memories match the current state of CLAUDE.md and the codebase?

#### Documentation audit (CLAUDE.md, AGENTS.md, .claude/README.md, GROWTH_SYSTEM.md, DEPENDENCIES.md, EXTENSIONS.md)
- **Accuracy:** Does CLAUDE.md's current focus match reality?
- **Completeness:** Are all skills, rules, and agents listed in their respective indexes?
- **Consistency:** Do CLAUDE.md and AGENTS.md agree with each other?
- **Dates:** Are "last updated" timestamps current?
- **Staleness:** Do any docs reference completed or deprecated work?
- **Dependencies:** Does DEPENDENCIES.md reflect the current system structure? Are folder-level tables, component tables, and deletion checklists up to date?
- **Distributed metadata:** Do component files have accurate `depends_on`/`depended_by` fields?
- **Count verification:** Do hardcoded counts in documentation match reality? Run the script, which greps every index doc for rule/skill/agent/hook counts (prose, tables, "Name (N)" labels, mermaid nodes) and diffs against disk:
  - `bash .claude/scripts/verify_counts.sh` (exit 0 = clean, exit 1 = prints each drifted file and line)
  - The script covers the four component totals. Check these by hand, since the script does not:
    - `ls Reference/Agent_workflows/*.md | wc -l` vs workflow count in README.md system map
    - `ls Reference/AI_PM_reference/*.md | wc -l` vs reference count in README.md system map
    - SYSTEM_OVERVIEW.md mermaid count nodes and ToC anchors (`### 3a. Rules (N)` must match `#3a-rules-N`)
    - Folder paths in GROWTH_SYSTEM.md four-pillar listing vs actual `Learning/` subdirectory names
  Any mismatch is an issue. Apply count fixes as trivial fixes immediately.

#### Growth system audit
- **Pillar health:** Is each pillar (intake, study, practice, reference) active?
- **Loop integrity:** Is the spiral learning pattern working (intake → practice → deepen → refine)?
- **Forge usage:** How many sessions this week? Streak intact?
- **AI digest flow:** Are digests being processed? Are insights flowing to Reference?
- **Book ratio:** Reading vs generation (the constraint is attention, not content)
- **Cross-pillar triggers:** Are connections between pillars actually firing?

### Step 3: score system health

Rate each area on a 1-5 scale:

| Score | Meaning |
|-------|---------|
| 5 | Clean - no issues found |
| 4 | Minor - cosmetic or low-priority issues |
| 3 | Moderate - functional gaps that affect daily use |
| 2 | Significant - contradictions or dead weight actively causing problems |
| 1 | Critical - broken infrastructure or major gaps |

Calculate an overall system health score (weighted average):
- Rules: 25%
- Skills: 20%
- Workflows: 10%
- Memory: 10%
- Documentation: 15%
- Growth system: 20%

### Step 4: generate improvement proposals

For each issue found, score it and write a concrete proposal:

**Scoring (rate each 1-10):**
- **Severity:** How bad is this if left unfixed?
- **Confidence:** How sure are you this is actually a problem (not a false positive)?
- **Actionability:** Can this be fixed in one session, or is it a vague concern?

**Composite score** = severity x confidence x actionability / 10 (max 100).

**Filtering rules:**
- Score above 50: Surface as a primary finding
- Score 25-50: List in "Low-confidence observations" section (collapsed)
- Score below 25: Skip entirely
- Exclude pre-existing issues that haven't changed since last retro
- Exclude cosmetic issues unless they violate an explicit rule

```markdown
### [ISSUE-NN]: [short title] (score: [N]/100)

**Area:** [rules/skills/workflows/memory/docs/growth]
**Scores:** Severity [N] x Confidence [N] x Actionability [N] = **[composite]**
**Found by:** [which diagnostic question caught this]

**Problem:** [What's wrong - specific, with evidence]

**Proposed fix:** [Exact change - file path, what to add/edit/remove]

**Effort:** [trivial/small/medium/large]

**Apply now?** [yes/no - trivial+significant fixes should be applied immediately]
```

### Step 5: apply trivial fixes

If `--deep` mode or if the fix is trivial (typo, date update, adding a missing entry to an index):
- Apply the fix immediately
- Log what was changed

For non-trivial fixes, present the proposal and ask: "Want me to apply this now?"

Ask ONE proposal at a time. Wait for the answer.

### Step 6: compare to last retro

If a previous retro exists:
- How many issues from last time were fixed?
- How many are recurring (same issue, unfixed)?
- Did overall health score improve, stay flat, or decline?
- What new issues appeared?

### Step 7: save the retro report

Write to `Forge/logs/system-retro/YYYY-MM-DD.md`:

```markdown
# System retro: [date]

**Cycle:** [N] (count of retros to date)
**Overall health:** [score]/5.0 ([trend vs last retro: up/flat/down])

## Health scores

| Area | Score | Last retro | Trend | Top issue |
|------|-------|------------|-------|-----------|
| Rules | [N]/5 | [N]/5 | [arrow] | [one-liner] |
| Skills | [N]/5 | [N]/5 | [arrow] | [one-liner] |
| Workflows | [N]/5 | [N]/5 | [arrow] | [one-liner] |
| Memory | [N]/5 | [N]/5 | [arrow] | [one-liner] |
| Documentation | [N]/5 | [N]/5 | [arrow] | [one-liner] |
| Growth system | [N]/5 | [N]/5 | [arrow] | [one-liner] |

## Issues found: [N]

### Applied this session

| # | Issue | Area | Fix applied |
|---|-------|------|-------------|
| 1 | [title] | [area] | [what was done] |

### Proposed (pending user decision)

| # | Issue | Area | Severity | Effort |
|---|-------|------|----------|--------|
| 1 | [title] | [area] | [sev] | [effort] |

### Low-confidence observations (score 25-50)

| # | Issue | Area | Score | Why low confidence |
|---|-------|------|-------|--------------------|
| 1 | [title] | [area] | [N] | [reason] |

### Recurring from last retro

| # | Issue | Retros open | Why still open |
|---|-------|-------------|----------------|
| 1 | [title] | [N] | [reason] |

## Improvement velocity

- **Issues found:** [N]
- **Issues fixed this session:** [N]
- **Issues from last retro fixed since then:** [N/total]
- **Recurring issues:** [N]
- **Net improvement:** [positive/neutral/negative]

## System changelog

[List of actual changes made during this retro session]

## Next retro focus

[Based on what was found, what should the next retro prioritize?]
```

---

## Mode: --quick

Fast scan (~10 minutes):

1. Read `.claude/WHATS_NEW.md` + `git log --since="1 week ago" --oneline`
2. Scan rules and CLAUDE.md for obvious staleness (dates, completed projects)
3. Check memory for outdated entries
4. Report top 3 issues only
5. Apply trivial fixes immediately
6. Save abbreviated retro report

---

## Mode: --deep

Extended session with implementation:

1. Run full standard audit
2. For EVERY non-trivial proposal, ask if the user wants it applied
3. Actually implement approved fixes (edit rules, update skills, clean memory, fix docs)
4. After all fixes, re-run a quick health check to verify improvements
5. Update all "last updated" timestamps in modified files
6. Save detailed retro report with full changelog

---

## Mode: --focus AREA

Audit only one area in depth:

1. Run only the diagnostic questions for that area
2. Read ALL files in that area (not just summaries)
3. Cross-reference with git history for that area specifically
4. Generate proposals for that area only
5. Save focused retro report

---

## Scoring calibration

To keep scores consistent across retros:

**Rules (score 5 if):** No contradictions, no stale references, all common corrections have rules, no dead rules
**Rules (score 3 if):** 1-2 stale references, one gap in coverage, all rules functional
**Rules (score 1 if):** Contradicting rules, multiple gaps, rules referencing deleted projects

**Skills (score 5 if):** All skills used in past month, no overlap, output matches style rules, all indexed
**Skills (score 3 if):** 1-2 unused skills, minor overlap, mostly indexed
**Skills (score 1 if):** Multiple unused skills, significant overlap, missing from indexes

**Growth (score 5 if):** All pillars active this week, Forge streak intact, AI digest flowing, no book debt
**Growth (score 3 if):** 1 pillar inactive, Forge used but inconsistent, some flow working
**Growth (score 1 if):** Multiple pillars dormant, no Forge sessions, broken intake pipeline

---

## Key rules

1. **Be brutally honest.** This is objective-review applied to the system itself. No "mostly good."
2. **Evidence only.** Every issue must cite a specific file, git commit, or observable pattern.
3. **Concrete fixes only.** "Consider improving X" is not a proposal. "Edit line 42 of file Y to say Z" is.
4. **Apply trivial fixes immediately.** Don't propose a date update - just fix it.
5. **One question at a time** when asking about non-trivial changes.
6. **Track cycles.** The value compounds over time as the system gets sharper each week.
7. **Don't over-engineer.** A rule that catches 80% of cases is better than no rule. Ship the fix, iterate next cycle.
8. **Respect the boil-the-lake rule.** When auditing an area, audit ALL of it, not a sample.
9. **Read objective-review skill** before starting. Apply that framework to the system itself.
10. **Cross-reference GROWTH_SYSTEM.md** to understand how pillars connect.

## Shortcuts to resist

See `.claude/rules/anti-rationalization.md` for the general pattern. These three are specific to this skill.

| Shortcut | Why it's tempting | Counter |
|----------|--------------------|---------|
| "A prior turn's summary said this fix was applied, so I can skip re-verifying it" | The summary reads as settled fact | A compaction summary is a claim, not a receipt. Confirm via `git status`/`git diff`/a direct read before building on it (cycle 15 retro, 2026-07-03: three "applied" fixes had never actually landed on disk) |
| "This area looked clean on a quick skim last cycle, I can skim it again" | Skimming feels efficient and the area rarely has issues | Boil-the-lake applies per area, every cycle. A clean skim is evidence for this cycle's score, not a reason to skip reading |
| "I'll eyeball the severity/confidence/actionability numbers instead of reasoning through each" | The composite formula feels like a formality once you already sense the priority | Write the three numbers and the reasoning for each before multiplying. Skipping this is how a real issue gets silently mis-bucketed into the wrong filter tier |

## Exit checklist

Done when all of these are true:

- [ ] All 6 areas were audited (rules, skills, workflows, memory, docs, growth) or a focused area was completed
- [ ] System health score was assigned with evidence for each dimension
- [ ] Improvement proposals are concrete (specific file, specific edit) not vague ("consider improving X")
- [ ] Trivial fixes were applied immediately, not deferred
- [ ] Comparison to last retro was completed (repeat issues flagged)
- [ ] Retro report was saved to `Forge/logs/system-retro/`
- [ ] Count verification passed (hardcoded counts match actual file counts)
- [ ] validate_skill_rules.sh was run during skills audit

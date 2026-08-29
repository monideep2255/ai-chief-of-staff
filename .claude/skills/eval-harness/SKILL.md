---
name: eval-harness
author: human
description: "Evaluation framework for AI bots, covering pass@k metrics and acceptance criteria templates for design system, React component, and P2 migration bots. Use when the user says: \"how do I evaluate this bot\", \"set up evals\", \"what is our acceptance criteria\", \"is this bot good enough to ship\", \"measure pass@k\". Read this before building an AI bot, not after. Differs from self-eval-loop, which grades a single document with a fresh-context agent rather than measuring model output quality across a task set."
scope: project
depends_on: []
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - GOALS.md
---

# Eval harness: AI bot evaluation framework

Define what success looks like BEFORE building. Then measure whether the bot meets those criteria.

## Core metrics

### Pass@k - "can it ever get it right?"

At least 1 of k generated samples passes all tests.

- **pass@1** = first-try success rate (hardest)
- **pass@3** = success within 3 tries (practical target)
- **pass@5** = success within 5 tries (lenient)

**Target:** pass@3 >= 80% for production use.

### Pass^k - "does it reliably get it right?"

ALL k samples must pass. Higher bar for critical paths.

- **pass^3** = 3 consecutive successes
- Use for: migrations, data transformations, anything where a bad output causes damage

**Target:** pass^3 >= 70% for critical paths.

### Grader types

| Type | How it works | When to use |
|------|-------------|-------------|
| **Code-based** | Deterministic check (regex, AST parse, lint) | Syntax, structure, valid output |
| **Model-based** | Claude judges Claude's output | Semantic correctness, style, completeness |
| **Human** | Flagged for manual review | Edge cases, subjective quality |

### Outcome buckets: pass, fail, abstain

Grader types decide how output is judged. Outcome buckets decide what states an output can land in. Binary pass/fail is fine for a code bot, where output is either valid or not. It is wrong for an answer bot that retrieves and then generates, because such a bot has three outcomes, not two:

- pass: the bot answered correctly, tied to a real retrieved passage.
- fail, wrong answer: the bot answered from priors or fabricated. This is the dangerous outcome.
- abstain: the bot returned "I could not find information on this" and stopped.

Score abstain by whether a correct source existed, not by whether an answer appeared:

- Retrieval genuinely returned nothing relevant and the bot abstained: score as pass. Refusing when there is nothing to cite is the correct, safe behavior.
- A correct source existed and the bot abstained anyway: score as fail. This is a real miss, the answer was retrievable and the bot declined.
- Never merge abstain into the wrong-answer bucket. A safe refusal and a confident fabrication are different failure modes, and collapsing them hides the one you most need to drive to zero.

Why this matters: a metric that cannot tell "safely declined" from "confidently lied" measures accuracy, not safety. Two runs can both show 80% pass while one safely refused the remaining 20% and the other fabricated it. This is the measurement half of the cite-or-refuse grounding gate in `.claude/rules/atlas-production-standards.md`. That rule says refuse when there is no source; this bucket scores whether the refusal happened and was rewarded. The trap is real: a harness that scores refusals as wrong answers will invert its own safety verdict until the bucketing is fixed.

### No-silent-loss truncation (for pipelines that offload or truncate large output)

Score a silent truncation as fail, not pass, even when the visible slice of the answer looks correct. If a retrieval-and-answer pipeline cannot retain the full output (context window pressure, a result set too large to inject), it must fail explicitly or return a pointer plus preview, never a truncated result presented as complete. Add a test case that forces this path (an oversized retrieval set or a long tool result) and assert the pipeline either returns the explicit-fail signal or the pointer-plus-preview shape, not a quietly clipped answer. This mirrors the no-silent-loss truncation principle in `.claude/rules/system-design-patterns.md` pattern 4.

### Weighted metadata completeness (for corpus and source quality)

Corpus quality is usually reported as one average, which hides the worst sources inside a healthy-looking number. Score it per item instead, on a weighted checklist of the metadata fields a downstream answer actually depends on, then rank ascending and read the bottom of the list.

- Pick the fields that change what a user can do with the item. For a retrieval corpus that is typically description, license, provenance or source identifier, publication or revision date, and a resolvable canonical link.
- Weight them by consequence, not by convenience. A missing license or missing provenance blocks reuse and blocks citation, so those carry more weight than a missing description, which only degrades ranking.
- Report the ranked worst items, not just the mean. The mean tells you whether to worry; the ranked tail tells you which sources to fix first.
- Treat a missing field as missing, never as a zero score that averages away. This is the same absence-is-not-a-negative-finding rule that `.claude/rules/doc-construction.md` applies to known gaps.

Use it two ways: as a standing acceptance criterion on any corpus a bot retrieves from, and as a triage list when a bot's answers are weak for reasons no prompt change fixes. Source: the kg-registry repository dive, whose data-quality dashboard ranks catalogued resources by weighted metadata completeness rather than reporting a single corpus score.

### Non-deterministic results

An evaluation case that passes on one run and fails on the next is not noise to be averaged away. It is a defect, and it sits in one of two places: in the thing being measured, or in the check that measures it. Both are worth finding, and neither is found by re-running until it goes green.

The rule: when a case flips, root-cause the variance and record the cause before you touch a threshold. A run that reports a pass rate without saying which cases were unstable has reported one number where there were two.

Where variance actually comes from, in rough order of how often it is the real answer:

- The harness samples on a fixed interval while the thing it watches changes faster than that interval. The check is aliasing, and the failure rate is a function of timing, not of correctness.
- Temperature, seed, or model version drifted between runs. Pin them, or state that they are unpinned and that the figure is therefore a distribution and not a value.
- Shared state leaked across cases. Case ordering changes the result, which means the cases are not independent and the pass rate is not a sum of independent trials.
- The thing under test is genuinely non-deterministic. This is a real answer, and it is the only one that justifies reporting a rate instead of a result. Pass^k already measures it, so use that rather than inventing a tolerance.

What is forbidden: widening a tolerance, raising a timeout, adding a retry, or dropping a case in order to make a flaky result stop flapping, before the cause is known. Every one of those changes the check so the check passes, which `goal-contracts` names as a failed run. After the cause is known, recalibrating a threshold is legitimate, and the recalibration is done under the conditions that produced the failure, not under ideal ones. A timeout retuned on an idle machine has been tuned against a case that was never going to fail.

Record the cause next to the case. A one-line note naming what varied and what fixed it is what stops the same flake from being rediscovered and re-suppressed three months later.

Worked instance: an end-to-end browser spec failed about once in sixty because the playhead it asserted on advanced every 134 ms while the test polled at 1 s, so the poll could land anywhere in the cycle. The fix was not a longer timeout. It was a MutationObserver accumulator, because a value that only ever grows cannot be aliased by the polling interval. The threshold was then recalibrated with CPU throttling on, which is the condition the original failure needed.

## Acceptance criteria template

Use this template for each bot:

```markdown
## Bot: [name]

### Inputs
- What the bot receives (screenshot, spec, template, etc.)

### Expected outputs
- What correct output looks like (HTML, JSX, migration file, etc.)

### Test cases
| ID | Input | Expected Output | Pass Criteria | Grader |
|----|-------|----------------|---------------|--------|
| 1  | ...   | ...            | ...           | code   |
| 2  | ...   | ...            | ...           | model  |

### Metric targets
- pass@1 >= X%
- pass@3 >= Y%
- pass^3 >= Z% (if critical path)
```

## Atlas bot evaluations

### Design system bot

**Purpose:** Generate USWDS-compliant HTML/CSS from component descriptions.

| Criteria | Pass Condition | Grader |
|----------|---------------|--------|
| Valid HTML | Passes W3C validation | Code |
| USWDS classes | Uses correct `usa-*` class names | Code |
| Accessibility | Has ARIA labels, roles, alt text | Code |
| Visual match | Matches USWDS reference component | Model |
| Responsive | Works at mobile/tablet/desktop | Human |

**Targets:** pass@1 >= 70%, pass@3 >= 90%

### React component bot

**Purpose:** Generate React components from specifications.

| Criteria | Pass Condition | Grader |
|----------|---------------|--------|
| Valid JSX | Compiles without errors | Code |
| Passes lint | No ruff/ESLint errors | Code |
| Props correct | Accepts specified props, correct types | Code |
| Renders | Mounts without crash in test harness | Code |
| Matches spec | Implements all specified behaviors | Model |

**Targets:** pass@1 >= 80%, pass@3 >= 95%

### P2 migration bot

**Purpose:** Convert legacy P2 templates to modern equivalents.

| Criteria | Pass Condition | Grader |
|----------|---------------|--------|
| Valid template | Django template syntax valid | Code |
| Data bindings | Same context variables used | Code |
| Visual parity | Renders same layout | Model |
| No broken links | All URLs resolve | Code |
| Accessibility | Meets WCAG 2.1 AA | Human |

**Targets:** pass@1 >= 60%, pass@3 >= 85%, pass^3 >= 70%

## How to run evals

### Step 0: tiny run (smoke test before spending real compute)

Before running the full eval suite, run one query through the complete pipeline end-to-end. All real hops, no mocking. This must complete in under 2 minutes.

Confirm:

- Retriever responds with at least one result
- Reranker scores the results (or passes through if not in pipeline)
- LLM generates an answer
- Judge outputs a score

If the tiny run fails, stop. Fix the wiring before running N samples. A bug caught here saves the cost of a full eval run.

Skip step 0 only if: you just ran the full eval suite successfully in the same session (pipeline is confirmed working).

1. **Define test cases** using the template above. For any retrieval-and-answer bot, include at least one zero-retrieval case: a query with no relevant source, asserting the bot abstains (returns the refusal string) rather than fabricating an answer. The no-source path is a tested case, not an afterthought.
2. **Generate N samples** (N >= 10 for meaningful stats)
3. **Run each sample through graders** (code first, then model, then human)
4. **Calculate metrics:**
   - pass@k = 1 - C(n-c, k) / C(n, k) where n = total, c = correct
   - Simpler: pass@k ~ (number of runs with at least 1 success in k) / (total runs)
5. **Compare to targets**  -  ship when targets met
6. **Track over time**  -  eval scores should improve, not regress

## When to use

- Before building an AI bot: define acceptance criteria
- During development: run evals to measure progress
- Before deploying: verify targets are met
- After changes: regression testing

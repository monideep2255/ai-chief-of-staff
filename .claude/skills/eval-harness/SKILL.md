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

### Reporting a best-of-N or pass@k figure

Any best-of-N or pass@k number is optimistic by construction: it takes the maximum over N attempts, so part of the score is sampling luck rather than capability. Report it with three things attached, every time:

1. The k value, stated explicitly. "pass@5 = 88%" is a claim; "88%" is not.
2. The single-attempt figure beside it. A pass@5 without pass@1 reads as capability when it may be variance.
3. One sentence stating the metric is optimistic by construction and not comparable across different k, different sampling temperatures, or different harnesses.

Never compare a pass@5 from one harness to a pass@3 from another, or to a single-attempt threshold, and never let a best-of-N figure stand alone in a summary, slide, or abstract. When the selection actually made in production used a different value, a single deterministic call for instance, report that value separately rather than letting the optimistic figure speak for it. Pattern source: the claude-protein-binder-design dataset, which labels its best-of-five-seeds co-fold metric as optimistic and non-comparable at the point of reporting, and keeps the selection-time values in separate columns.

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

### Compare against a baseline

A score with no baseline cannot tell you what produced it. If a retrieval-and-answer pipeline scores 82 percent, that number is uninterpretable until you know what the base model scores on the same set with none of the pipeline attached. The pipeline is the thing you built. The base model is free. Only the difference between them is your work.

Run at least two arms over an identical evaluation set with identical scoring:

1. Base model alone: one call, no retrieval, no orchestration, no gates. This is the floor.
2. The full pipeline.

Add a third arm whenever a specific component is in question: the pipeline with that one stage disabled. The gap isolates what that stage is worth, which is the only honest way to defend keeping an expensive stage.

Two rules keep the comparison fair. The grader must be a different model from the one being graded, or it scores its own habits. And every arm faces the same bar, the same prompts, and the same handling of unrunnable cases, with excluded items named and counted rather than quietly dropped.

Report the arms together. "82 percent" is a claim about nothing. "82 percent against a 61 percent single-call baseline, same 50 items, same grader" is a measurement. Pattern source: the pr-af repository dive, which runs a mid-tier open model and competes on pipeline architecture, a claim that means nothing without the baseline published beside it.

### Measured versus projected

A figure after a fix is a measurement only when the frozen case set was rerun through the change that actually shipped. Anything else is a projection, and it is written as one.

- Measured: the same cases, the same grader, and the same scoring, rerun after the change landed. Report it with the run date.
- Projected: an estimate from reasoning about which failures the fix should cover. Label it "projected", name the method, and never put it in a headline or a before-and-after table as if it ran.
- Ambiguous population: when "the last 50 runs" or "recent sessions" can mean two different sets, report both denominators side by side rather than picking one.

A projection overstates for a predictable reason: matching failures by symptom counts cases the implemented predicate never touches. Pattern source: the chat-on-steroids repository dive, whose tool error rate report projected a drop from 9.07 to 5.49 percent, reran the frozen corpus, found only 37 of 195 failures actually eliminated, and published 7.35 percent as the number to use.

### Prompt-contract tests

Output-quality evaluation cannot catch a field that silently stops reaching the prompt. The model still answers, fluently, from whatever it did receive, so every quality metric stays green while the system reasons without an input you believe it has. This is a different failure class from a wrong answer and it needs a different test.

The test asserts on the literal prompt string, not on the response. Build the prompt, capture it before the call, and assert that the fields you require are present in the bytes that would be sent.

Three cases per field are worth pinning:

1. Reachability: place a unique marker past every truncation boundary in the chain, then assert the marker appears in every downstream prompt. A field cut to 500 characters in stage one cannot be recovered by a 4000-character allowance in stage three.
2. The exact cap: assert the boundary value directly, so a later change to a constant fails a test instead of silently shortening the input.
3. The empty case: assert that an absent field omits its whole section rather than emitting a bare heading, which otherwise tells the model a section exists and is empty.

Add a fourth when order carries authority: assert that operator instructions appear before user-supplied or retrieved content, so precedence holds by position and not only by label.

These tests are deterministic, cost no model calls, and check the one thing entirely under your control, which is what you actually said. Source: the pr-af repository dive, where three stages independently truncated author rationale to 500 characters and reviewers then confidently contradicted reasoning they had never been shown. No output metric could have found it, because nothing in the pipeline knew the text was gone.

### No-silent-loss truncation (for pipelines that offload or truncate large output)

Score a silent truncation as fail, not pass, even when the visible slice of the answer looks correct. If a retrieval-and-answer pipeline cannot retain the full output (context window pressure, a result set too large to inject), it must fail explicitly or return a pointer plus preview, never a truncated result presented as complete. Add a test case that forces this path (an oversized retrieval set or a long tool result) and assert the pipeline either returns the explicit-fail signal or the pointer-plus-preview shape, not a quietly clipped answer. This mirrors the no-silent-loss truncation principle in `.claude/rules/system-design-patterns.md` pattern 4. Source: opencode repo dive.

### Evidence-record immutability (for retrieval-and-answer pipelines)

For any bot that retrieves and then judges, add an acceptance criterion that the judgment never mutates the evidence. Concretely: the relevance score, confidence value, abstain decision, and any reranked order are written to fields distinct from the retrieved-passage record, and the passage record is byte-identical before and after the answer pass. Test it directly: hash the retrieval output, run the answer and scoring pass, hash again, and assert the two match. A pipeline that fails this cannot be debugged after a bad scoring run, because there is no longer an unjudged record to re-score. This is the measurement half of the non-destructive adjudication clause in `.claude/rules/atlas-production-standards.md`.

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

Worked instance: a bench end-to-end spec failed about once in sixty because the playhead it asserted on advanced every 134 ms while the test polled at 1 s, so the poll could land anywhere in the cycle. The fix was not a longer timeout. It was a MutationObserver accumulator, because a value that only ever grows cannot be aliased by the polling interval. The threshold was then recalibrated with CPU throttling on, which is the condition the original failure needed. Source: the bench repository dive.

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
- Report every pass@k with its k, its pass@1 companion, and the optimistic-by-construction note
- Evidence record byte-identical before and after the answer pass (retrieval-and-answer bots only)
```

## Meridian bot evaluations

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

### A test double's unstubbed call raises, never returns a default

Before the steps below, one rule about how the harness itself is built. When a test replaces a dependency, a call the test did not explicitly answer must raise an error naming what was missing. It must never fall through to a default, an empty list, a zero score, or a plausible-looking stub value.

The reason is the failure this whole skill exists to prevent. A permissive default does not fail the test, it passes it for the wrong reason, and the suite then reports green while the path under test never ran. That is strictly worse than a red test, because a red test gets fixed and a falsely green one gets trusted. It is the same judgment `self-eval-loop.md` makes when it decides whether a plausible wrong answer is worse than an obvious failure.

Apply it two ways:

- Build test doubles that raise on any unconfigured call, with the error naming the method and arguments that went unanswered. A developer reading the failure should know immediately which dependency they forgot, not merely that a number came out wrong.
- Treat a stand-in scorer or placeholder judge as a labeled gap, never as a passing result. A suite running against a stand-in reports its pass rate as provisional and names the stand-in, because the figure measures the harness rather than the bot.

The risk concentrates wherever a real scorer has been swapped for a placeholder, which is exactly when a suite is largest and most reassuring.


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

---
name: goal-contracts
description: Before running any autonomous or multi-step task to completion, write a goal contract (done-when, verify, output, constraints, blocked-stop) so the agent stops on verified evidence, not on feel
scope: project
depends_on:
  - .claude/rules/anti-rationalization.md
  - .claude/rules/self-eval-loop.md
  - .claude/rules/parallel-first.md
depended_by:
  - CLAUDE.md
  - DEPENDENCIES.md
  - .claude/rules/sandbox-diagnosis.md
  - .claude/rules/parallel-first.md
  - .claude/rules/agent-first-default.md
  - .claude/skills/bossman-mode/SKILL.md
  - .claude/rules/ship-clean-no-bait.md
---

## Goal contracts

Before you run any "keep going until it's done" task, write the finish line down first. An agent that starts looping without a verifiable definition of done will stop when it feels done, which is the single most common way autonomous work goes wrong: it overclaims completion.

This rule names the contract. The loop does not start until the contract exists.

### When to apply

- Any autonomous or multi-step task that runs to completion without a human in each step (bossman-mode phases, ingest pipelines, system-retro, deep research, any background agent)
- Any task you hand to a subagent with the instruction "do X until done"
- Any skill with an exit checklist (the checklist is the contract's verify surface)

### When NOT to apply

- Single-step lookups, quick edits, formatting fixes (done is obvious)
- Conversational turns where the user is steering each step
- Capture tasks (meeting notes, check-ins) where there is no "done" to verify

### The contract (five elements)

Write these before the first action, not after:

1. Done when: the outcome in one testable sentence. Not "improve the docs" but "every new file has 5/5 frontmatter fields and 0 em dashes".
2. Verify: the concrete surface that proves it, a grep, a test, a file count, a second-agent grade. If you cannot name how you would check it, the goal is not yet a contract. The verify surface is immutable for the duration of the run: you may add checks, never weaken them. At least one signal must be observable state the run does not itself produce: a row count in the source data, a remote hash, a file written by another process, a second agent's independent read. A surface built entirely from checks over the run's own output can be satisfied by producing more output, which is why the run must be graded against something it does not control.
3. Output: what artifact the run produces and where it lands (file path, table, commit).
4. Constraints: what must stay true throughout (no deletions without asking, no secrets in logs, style rules hold).
5. Blocked-stop: the condition under which you stop and report rather than guess. A blocked stop is a valid, honest end state, not a failure to hide.

### Mark what you could not fill, never leave it blank

An element you could not determine is written down as unknown, with a marker, not left empty. A blank reads as "nothing needed here" to the next reader and to the next agent; an explicit marker reads as "this is missing and someone owes it." The two look identical in a rendered document and mean opposite things.

Two markers, borrowed from ProductSpec's honesty primitives:

- `provisional`: the value is a placeholder, not a measurement. A target number nobody has validated, a threshold copied from a neighbouring project, an estimate standing in for a real count. It is usable for now and it is not evidence.
- `target_owner: unassigned`: the outcome has no accountable person. Distinct from provisional, which is about the number; this is about who answers for it.

Apply them to any element of the five above, and to any metric or acceptance threshold in an evaluation set (`.claude/skills/eval-harness/SKILL.md`). A verify surface built on a `provisional` threshold is still a verify surface, it just carries a visible caveat, which is exactly the distinction between a soft number and a hard one that a blank cell destroys.

This is the same failure class as the unrun-versus-passed rule below. There, a check that could not run must not report as passed. Here, a value that could not be determined must not render as settled. Both are cases of absence disguising itself as a result.

### Meta-prompt the contract for long runs

Hand-written contracts under-specify. For any run over roughly 30 minutes of autonomous work, do not write the contract from memory. Dispatch a fresh-context agent to read the target files first, surface hidden assumptions, constraints, and edge cases, then draft the five elements. Review its draft, tighten it, then launch. A second agent writing the contract is the maker-checker split of `self-eval-loop` applied upstream of execution instead of after it, and the file reads are independent work that parallelize (`parallel-first`).

The inline variant: let the executing agent write its own goal from your high-level intent. It works only when you hand it the same raw materials (the files to read, the exact validation command, the constraints) and tell it to ask before committing when the intent is underspecified. Otherwise the self-set goal drifts.

### Every gate names its fail direction

A contract with a blocked-stop still leaves one question open: when a check itself errors, times out, or returns something the run cannot parse, does the work continue or does it halt? That is a design decision, not a default. Leaving it implicit means the answer is whatever the exception handler happened to do.

For each gate in a run, write its fail direction beside it:

- Fail open: on error the gate lets the work proceed and marks the result advisory. Choose this when a false stop costs more than a missed catch.
- Fail closed: on error the gate refuses to act. Choose this when acting on unverified output costs more than doing nothing.

The two directions are not a house style, they are per gate, and one run will often want both. Worked instance: pr-af runs two gates in a single pipeline pointing opposite ways on purpose. Its merge gate fails open, because a false block stops a merge and burns the reviewer's credibility for everything after it. Its human gate fails closed, because posting an unreviewed review is worse than posting nothing. A third case sits underneath both, and it splits in two depending on what the missing piece was for. Source: the pr-af repository dive.

#### Missing tooling: which half is absent decides the direction

"The tool is not installed" is not one case, it is two, and they point opposite ways:

- An optional capability that is merely absent rather than broken degrades to a working path instead of ending the run. Nothing was being checked, so nothing is now unverified. Note the degraded path in the output and continue.
- A verifier whose tool is absent refuses to pass. A control that quietly succeeds because its binary was never found is worse than no control at all, because the run now carries a green signal that measured nothing, and every later decision trusts it. The gate errors and says which tool is missing.

The distinguishing question is what the missing piece was responsible for. If its absence removes a feature, degrade. If its absence removes a check, fail closed. A skipped check must never be reported, logged, or summarized in the same shape as a passed one.

Worked instance: bench's `scripts/run-gitleaks.mjs` errors out when the gitleaks binary is not on the path rather than skipping the secret scan, so a machine without the tool fails the build instead of shipping unscanned. Source: the bench repository dive.

The failure this blocks is the silent default. An unhandled error inside a verify step usually propagates as a stop, which reads as the safe choice and is often the wrong one: a verify surface that halts on its own flakiness turns a transient error into a blocked-stop, and that trains you to start bypassing the gate.

### The anti-patterns this blocks

"Feels done" is not done. Marking a multi-step task complete because the model judges it finished, with no artifact, test, or count checked, is the failure mode. Tie completion to evidence from the verify surface. This reinforces `self-eval-loop` (a second agent grades) and `anti-rationalization` (do not skip the check).

Reward hacking is the second failure mode, and it is subtler. An agent graded on "tests pass" or "eval score above X" can reach done-when by corrupting the check instead of doing the work: deleting a failing test, weakening an assertion, narrowing an eval set, or lowering a count threshold. The run then reports success while the thing the check existed to guarantee is now false. Changing the check so the check passes is a failed run, not a completed one. This is the autonomous-loop sibling of `anti-rationalization`: name the shortcut and forbid it before the loop starts.

Budget or iteration caps are checkpoints, not success. When a cap is hit, the run stops and reports progress plus blockers. It does not declare done.

Rigor about the wrong layer is the third failure mode, and it hides behind a verify surface that is genuinely real. A check can audit every leaf output honestly and still certify a wrong answer, because the premise that generated those outputs was never checked. A measured instance: a research run verified all twenty of its facts against two independent authoritative sources each, an honest and rigorous verify surface, and still shipped a wrong answer, because the premise that produced the fact list (the list itself, built from model memory) went unverified. The rigor was real and pointed one layer too low. When the decomposition or premise matters, the verify surface must cover it, not only the leaves. Done-when should name the premise as a checkable element, or the contract certifies a confident wrong answer with a clean audit trail. Source: the CMA plan-big-execute-small repo dive.

### Three-state permissions

Allow:
- Write the contract inline at the top of any autonomous run without asking
- Treat a named blocked-stop as a clean end state

Ask:
- Before continuing past a blocked-stop by guessing at the missing input

Deny:
- Never start an autonomous loop with no testable done-when and no verify surface
- Never mark a multi-step task complete on feel, with no evidence from the verify surface
- Never change, weaken, delete, narrow, or skip the verify surface (tests, assertions, eval cases, count thresholds) to reach done-when. Changing the check so the check passes is a failed run
- Never treat a leaf-level verify surface as complete when the premise or decomposition that generated the leaves is itself unverified. The premise is part of the verify surface
- Never build a verify surface entirely out of checks over the run's own output. At least one signal comes from state the run does not produce
- Never let a verifier pass because its tool, binary, credential, or data source was missing. A check that could not run reports as unrun, never as passed
- Never leave a gate's behavior on its own error undefined. Every gate in the contract states whether it fails open or fails closed, and the cost that decided the direction

The test: before I started running to completion, did I write a testable done-when, name how I would verify it, include at least one signal the run does not produce itself, state each gate's fail direction, and make every check that could not run report as unrun rather than passed?

---
description: "Always identify and attack the bottleneck before optimizing anything else."
scope: portable
alwaysApply: true
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
---

## Attack the constraint

Before optimizing, automating, or adding to any system, ask: what is the bottleneck right now?

Optimizing a non-bottleneck is wasted effort. Elon's version: "Attack the constraint" - find what's actually limiting throughput and focus resources there.

The question to ask:

For any goal, project, or system: what single thing, if removed or improved, would unlock the most progress? Is the constraint time, skill, clarity, access, or tooling?

Apply when:
- Planning a Forge session - what skill gap is actually blocking progress, not just interesting?
- Choosing what to learn - which book/course directly unblocks current work?
- Reviewing the OS itself - is the system overhead (rules, docs-sync, retros) justified by the value it creates?
- Weekly reflection - what blocked me this week? Same thing as last week? Then it's the real constraint. Read `PAPERCUTS.md` to answer this from a record rather than from memory.
- Starting a work block - of the options in my cluster (Build/Learn/Practice), which one attacks the constraint?

Do NOT apply when:
- The constraint is external and you can't act on it (waiting on someone else)
- You're in execution mode on a clear plan - don't re-question the plan mid-sprint
- Recovery/rest days - not everything needs to be optimized

Idiot index check:
When something feels expensive (in time, effort, or friction), break it into components. How much of the cost is the actual work vs overhead, process, or indecision? A high ratio of overhead to actual work means the constraint is the process, not the task.

The Algorithm (when the constraint is process overhead):

Once you've identified the bottleneck as process, run these 5 steps in order. The order matters - don't skip ahead.

1. Make requirements less dumb: question every requirement. Who asked for this? Are they still right? Ownerless requirements are suspect by default.
2. Delete: remove whole steps, parts, or processes entirely. If you never have to add something back ~10% of the time, you're not deleting aggressively enough.
3. Simplify: only after deletion. Otherwise you're polishing things that shouldn't exist.
4. Accelerate: speed up cycle times only once you're building the right, simplified thing. "If you're digging your grave, don't dig it faster."
5. Automate: last, not first. Automating a broken process just produces fast wrongness.

Examples:
- 24 books, 200+ chapters, 1 in active reading - the constraint is attention allocation, not content. Fix: reduce visible options to the 2-3 that directly serve current goals.
- Forge targets daily practice but logs show weekly frequency - the constraint isn't the system design, it's the trigger. Fix: identify what's crowding out Forge time.
- Evening work block has 7 options - the constraint is selection, not motivation. Fix: cluster and rotate (your existing daily planning system already did this).

## Log the papercuts, or the weekly question has no answer

The weekly reflection above asks whether the same thing blocked you twice. That question is unanswerable from memory, because the small losses are exactly the ones you forget: a command that failed for a non-obvious reason, a denied path, a flag that turned out to be wrong. Each costs a few minutes and none is memorable on its own, which is how a recurring ten-minute tax goes unnoticed for months while you look for a big constraint that is not there.

`PAPERCUTS.md` at the repository root is the record. Two behaviours, both cheap:

- When tooling fails in a way that is not obvious, read it first. A symptom already logged has its fix written next to it.
- When you lose time to something, append a row in the session where it happened: date, symptom, fix, project. Write the symptom in the words you would search for later, meaning the error text rather than a summary of it. Do not batch entries for later, since the detail that makes an entry useful is gone by the next day.

Log a symptom even when the fix is unknown, marked as such. The third occurrence is what justifies solving it properly, and that count only exists if the first two were written down. Do not log a one-off mistake you understood immediately; this records friction that will recur, not typos.

The scope is honest rather than global: the log lives in this repository and covers sessions that load these rules. Work in another repository does not append to it automatically, and `git-workflow` forbids pointing at this path from any other repository.

The test: did I identify the bottleneck before optimizing, or did I optimize the first thing I saw? And when I lost time to tooling this session, did I append the row while I still had the detail?

---
name: handoff
author: human
description: Compact the current session into a single copy-pasteable handoff so a fresh agent with zero memory can continue the work without re-asking or repeating mistakes. TRIGGER when the user says "handoff", "write a handoff", "hand this off", "compact this session", "context is getting full", "wrap up this session", or wants to partition a long task across fresh contexts. DO NOT TRIGGER for meeting notes (use meeting-notes agent) or a project status update the user will read themselves.
scope: project
user_invocable: true
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/file-protection.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - DEPENDENCIES.md
---

# Handoff

Write a complete handoff that lets a fresh agent, with zero memory of this session, continue the work without re-asking, re-discovering, or repeating mistakes. Output it as one fenced code block so the user can copy it in one click, and save a copy to a file.

Its one non-obvious idea: write state, not instructions.

## When to use

- Context is filling up and you need to continue in a fresh session.
- Partitioning a long build across fresh contexts on purpose (subagent-driven work, a bossman-mode phase boundary, a multi-session model-bench or research run).
- Ending a work session that will resume later.

Not for: a status update the user reads themselves (just tell them), meeting notes (use the meeting-notes agent), or a task that fits in one session.

## Core principles

1. State, not instructions. Describe what is true, never what the next agent should do. Write "logout endpoint is not started", never "implement logout next". The fresh agent decides the actions; you give it ground truth. This is the single rule that makes a handoff useful instead of a stale to-do list.
2. Reference, do not duplicate. Point to PRDs, plans, decisions, commits, and diffs by path or URL. Do not paste their contents. Re-embedded artifacts go stale the moment the source changes.
3. Capture the why. Decisions and rejected approaches are the most valuable and least recoverable information. Code shows what; only this session remembers why and what failed.
4. Trust nothing blindly. Frame every claim as context to verify against the actual code, not fact to accept.
5. Redact secrets. Strip keys, tokens, passwords, PII. Reference where credentials live (".env.local, not committed"), never their values. Follow `file-protection` and `writing-style`.
6. Be ruthless. Cut anything the next agent could trivially get by reading the code or project config.
7. Carry the chain forward. If a prior handoff exists, fold its still-true state into this one before adding new state, never drop it. Across a chain of handoffs nothing should silently fall off; a fact that was true three handoffs ago and still holds must survive to this one. This is a "carry prior summaries forward" rule for successive compactions, applied here to handoffs.
8. Anchor the exact stopping point. Capture a verbatim quote or precise pointer of where work left off (the last line edited, the exact command running, the error being chased). A paraphrase drifts; the verbatim anchor does not.
9. User messages are the specification. Corrections extend the task and never narrow it to whatever the last answer happened to cover. When a decision changed, state the final position and say that it changed, so the next agent does not rebuild the superseded version.
10. A stated intention is not evidence. "I will run the tests" and "the fix should work" are claims; a command with its result, a passing test, a commit, or a file on disk is proof. Give every DONE item its proof, and put an item with no proof under PARTIAL. (Principles 9 and 10 come from the Compact & Resume brief rules in the chat-on-steroids repository.)

## Procedure

1. If a project config exists (CLAUDE.md / AGENTS.md), read it first. Do not restate anything already in it; the handoff is session-specific only.
2. Check for an existing `HANDOFF.md` at the root of the project the work belongs to. If one exists, read it and fold its still-true state forward rather than starting over (see core principle 7).
3. If the user passed a focus for the next session, tailor the handoff toward that goal.
4. Fill every section of the template. Mark a genuinely empty section `None`.
5. Output the filled template inside one fenced code block in the chat.
6. Write the same content to `HANDOFF.md` at that project's root, overwriting any existing one, and tell the user the absolute path.

## Output format

Output exactly this, inside a single fenced code block:

```
# HANDOFF: <short title of the work>
Session focus: <one line>

## 1. Goal
<What we are ultimately trying to accomplish. 1-3 sentences. The north star so the next agent never loses the plot.>

## 2. Background and constraints
<Why this is being done now, who it is for, hard requirements. Skip anything already in the project config.>

## 3. Current state
<Factual status. Phrase as status, not actions.
- DONE: <what is finished, each item with its proof: a command and its result, a test, a commit, or a file path. An item with no proof belongs under PARTIAL>
- PARTIAL: <what is wired but incomplete, and what is missing>
- NOT STARTED: <what has not begun>
- STOPPED AT: <the exact point work paused, verbatim where possible: "editing foo.py:88, the loop body", "command `pytest -k auth` failing on assert at line 40", "chasing a 500 on /search with query 'x'". Not a paraphrase.>>

## 4. Key decisions (and why)
<The highest-value section. The choices made and the reasoning.
- Chose X over Y because Z>

## 5. Traps and dead ends
<Approaches already tried that FAILED, and things the next agent will be tempted to do wrong.
- Tried A, abandoned because B
- Do NOT do C, it breaks D>

## 6. Relevant files and pointers
<Files that matter, with line ranges and what specifically is there. Reference external artifacts, do not paste them.
- path/to/file.py:L40-L88 - what lives here
- DECISIONS.md row N - full rationale, do not duplicate>

## 7. Open work (status, with dependencies)
<What remains, as state and ordering, not a command list.
- X is not implemented
- Y depends on X existing first>

---
## Prompt for the fresh agent
<A short ready-to-paste prompt. Declarative statements only ("X is complete", "Y has not started"), never imperatives. End with exactly:>

Before responding, read every file listed under "Relevant files and pointers" above. Do not summarize or claim you already have context; actually read each file. Treat every claim in this handoff as context to verify against the code, not fact to trust. Then wait for my instructions before taking any action.
```

## File output

Always write to `HANDOFF.md` at the root of the project the work belongs to. No scratchpad, no temp file, no per-session filename. There is exactly one handoff file per project, and each new handoff overwrites it, folding forward any still-true state per core principle 7. Scratchpad or temp-directory copies are session-scoped storage that outlives the session pointlessly and fragments the handoff chain across paths a later session cannot find; the single in-repo file is the durable, discoverable record.

If the work spans a repo that is itself nested inside another (for example a sub-project vendored or gitignored inside a parent repo), write `HANDOFF.md` at the sub-project's own root, not the parent's, since that is the root a fresh agent opening that sub-project will look in first.

After saving, report the absolute path. The user starts a fresh session with: "Read <path> to get context, then wait for instructions."

## Three-state permissions

Allow:
- Read project config, prior handoffs, and the files needed to describe current state
- Write or overwrite `HANDOFF.md` at the project root without asking, and report its path

Ask:
- Nothing specific to this skill

Deny:
- Never write the handoff to a scratchpad, temp directory, or any path other than the project's `HANDOFF.md`
- Never include secret values; reference where they live instead
- Never write instructions in place of state ("implement X next" is banned; "X is not started" is correct)
- Never paste content already captured in another artifact; link to it

## Exit checklist

- [ ] Project config read; nothing already in it is restated
- [ ] Every section filled or explicitly marked `None`
- [ ] Phrased as state, not instructions (no imperatives in sections 3 and 7)
- [ ] Decisions and dead ends captured with the why
- [ ] Prior handoff state (if any) carried forward, nothing silently dropped
- [ ] Exact stopping point anchored verbatim in Current state (STOPPED AT)
- [ ] Every DONE item names its proof; unproven work sits under PARTIAL
- [ ] Changed decisions state the final position and say that they changed
- [ ] Secrets redacted; artifacts referenced by path, not pasted
- [ ] Output in one fenced code block, and saved to a file with the path reported

The test: could a fresh agent read this handoff plus the files it points to and continue the work without asking me anything already known this session?

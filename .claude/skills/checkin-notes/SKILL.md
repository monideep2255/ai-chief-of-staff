---
name: checkin-notes
author: human
description: Process raw meeting notes from Sam/Dana check-ins into structured notes + action items, then auto-ship. Three-step combo  -  meeting-notes agent formats, action-planner agent extracts todos, then /ship syncs docs and pushes to GitHub. TRIGGER when user says "checkin notes", "format my check-in", "meeting with Sam", "meeting with Dana", or pastes raw check-in notes. Also trigger on "prep for Sam" or "prep for Dana". DO NOT TRIGGER for general meeting notes (use meeting-notes agent) or conference notes (use ingest-conference).
scope: project
user_invocable: true
depends_on:
  - .claude/agents/meeting-notes.md
  - .claude/agents/action-planner.md
  - .claude/skills/ship/SKILL.md
  - .claude/rules/meeting-notes-format.md
  - .claude/rules/file-naming.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# /checkin-notes - format check-in notes + extract action items

Two-step skill for processing raw meeting notes from recurring check-ins (Sam, Dana, or any person).

## Triggers

- `/checkin-notes` with raw notes pasted
- `/checkin-notes Sam` or `/checkin-notes Dana` to specify the person

## Step 0: identify the target file

1. Determine who the check-in is with (from the user's message or ask if unclear)
2. Find the prep doc for today's meeting:
   - Look in a `Check-in with {Person}/` folder (wherever you keep 1:1 notes) for a file matching today's date
   - If a prep doc exists with placeholder sections (e.g. "to be filled during meeting"), use that file
   - If no prep doc exists, create a new file following the naming convention: `{number}_{Month}_{Day}.md`
3. Read the existing file to understand what sections need to be filled in

## Step 1: format meeting notes

Use the `meeting-notes` sub-agent approach. Read `.claude/agents/meeting-notes.md` for the full format rules.

Given the user's raw notes:

1. Structure into nested bullet points (4-space indentation per level)
2. Each topic gets a top-level bullet under "Meeting notes"
3. Sub-points capture the substance, not vague summaries
4. Always include an "Action items:" section within the notes
5. Action items must have WHO does WHAT by WHEN
6. Use active voice: "You reach out to Dana" not "Dana should be reached out to"
7. Strip jargon. Be specific.

Write the formatted notes into the Notes section of the target file.

## Step 2: extract action items

Use the `action-planner` sub-agent approach. Read `.claude/agents/action-planner.md` for the full format rules.

From the formatted notes:

1. Extract every actionable item
2. Prioritize using:
   - Priority 1: must do today or tomorrow, or blocks other work
   - Priority 2: important but flexible timing (this week)
   - Priority 3: ongoing or nice to have
   - Blocked: waiting on someone else
3. Each task gets: `- [ ] Task description (Owner: You/Name, Due: date)`
4. Add context as a sub-bullet where helpful

Write the action items into the Action Items section of the target file.

## Step 3: confirm with user

Show a summary of what was written:
- Number of topics captured
- Number of action items extracted
- Any questions about items that were ambiguous in the raw notes

## Step 4: auto-ship

After the notes are written and the summary is shown, run `/ship` automatically. Do not wait for a separate prompt. The act of running this skill is the instruction to ship.

`/ship` runs docs-sync then git-sync (commit to main, push to GitHub over HTTPS). The check-in note is leaf content, so docs-sync has little to sync; the point of this step is the commit and push, so the notes land in GitHub without a follow-up prompt.

Notes on this step:
- Ambiguities flagged in Step 3 are non-blocking. The notes are already saved, so ship proceeds. If the user later corrects a reading, re-ship with the fix.
- If the skill itself was just edited (a change to this SKILL.md), that change ships in the same push, which is correct.
- If git-sync hits a real error (dirty conflict, auth failure, sandbox Layer-4 SSH block), stop and report the exact state. Do not force-push or disable the sandbox. See the `sandbox-diagnosis` rule.

## Rules

- If the raw notes are ambiguous, ask ONE clarifying question before formatting
- Never invent action items that aren't in the raw notes
- If a topic is purely informational (no next step), note it but don't force an action item
- Respect the existing file structure: fill in placeholder sections, don't restructure the whole doc

## Quality checks

Run these before confirming output with the user. Every item must pass.

1. Every action item has WHO (specific person, not "team"), WHAT (specific task), and WHEN (date or timeframe)
2. No action item was invented that isn't traceable to a specific point in the raw notes
3. Topics from the raw notes are all accounted for (count topics in raw vs formatted, flag any that were dropped)
4. Active voice throughout: "You reach out to Dana by Thursday" not "Dana should be reached out to"

## Exit checklist

Done when all of these are true:

- [ ] Target file identified or created with the correct naming convention
- [ ] Raw notes formatted as nested bullets under "Meeting notes"
- [ ] Action items section present, every item has WHO, WHAT, and WHEN
- [ ] No action item invented that is not traceable to the raw notes
- [ ] All raw-note topics accounted for, none silently dropped
- [ ] Summary shown to the user: topic count, action count, any ambiguities
- [ ] /ship run automatically after the summary (docs-sync then git-sync push), unless git-sync reported a blocking error

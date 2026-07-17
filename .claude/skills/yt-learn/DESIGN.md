<!-- depends_on: [.claude/skills/yt-learn/SKILL.md] -->
<!-- depended_by: [] -->

# Plan: content-to-improvement engine (/yt-learn)

Date: example date, replace with your own
Status: approved, built (example date, replace with your own)
Scope: on demand, one video at a time. No cron, no radar, no schedule.

## What this is

An engine that turns a YouTube video into concrete upgrades to three things: your system (your OS and Atlas, your primary project), your knowledge, and your skills. It is not a summarizer. The summary is a supporting layer. The upgrade is the point.

North star: content goes in, concrete upgrades come out. It replaces "I watched something and forgot it" with "I watched something and my system is measurably better."

## The end product (per run)

One markdown doc in `Reference/Learn_and_apply/`, ordered by what matters:

1. Verdict: watch, skim, or skip, minutes worth it, for whom.
2. Apply now (the headline): the 1 to 3 highest-leverage moves. Each has the action in one line, its target bucket (system, knowledge, or skill), a drafted change ready for approval (proposed rule text, a scaffolded Forge exercise, or a queued repo-dive), and the source timestamp. Nothing saves to the repo until you approve it.
3. What I can use for what (the deep dive): a table of every worthwhile idea, tagged by bucket, with how it applies and a timestamp.
4. Go deeper (offered, not automatic): an offer to turn the concepts into a system map, a Forge exercise, or a knowledge doc. You choose.
5. Understanding (supporting, kept last): the plain brief. TL;DR, real vs creator hype, skip-to guide.

No transcript file by default. Captions are pulled to the scratchpad, used, and discarded. Every idea carries a timestamp back to the video, and yt-dlp refetches the raw text in seconds. A `--keep-transcript` flag exists, off by default.

## Done when

Running the command on a captioned video produces the doc above, where:
- apply-now has at least one drafted, approvable change tied to a real timestamp,
- every deep-dive idea is tagged system, knowledge, or skill,
- hype is separated from substance by a fact-checker agent that never saw the transcript,
- nothing was written into the repo without approval,
- a caption-disabled video returns an honest "no transcript" instead of an invented doc.

## Invocation

```text
/yt-learn <url>            # auto: cheap single-pass for short videos, full engine for long ones
/yt-learn <url> --full     # force the full multi-agent engine
/yt-learn <url> --lite     # force single-pass, no fan-out
/yt-learn <url> --map      # also generate a systems-map from the concepts
/yt-learn <url> --keep-transcript   # also save the raw transcript (off by default)
```

## How it runs

1. Parse the video id.
2. yt-dlp pulls captions to the scratchpad. www.youtube.com is allowlisted, no override.
3. No captions: stop and say so. Do not invent, do not transcribe (whisper out of scope for v1).
4. Pull metadata (title, duration, channel, date).
5. Clean the captions with clean_vtt.py.
6. Pick lite or full by duration, or honor the flag. Under 25 min lite, 25 min or more full.
7. Full only: chunk into about six segments.
8. Run the engine: extract (parallel, one agent per chunk), synthesize the understanding layer, fact-check it, then map to upgrades (sort ideas into the three buckets and draft the apply-now changes).
9. Assemble the doc in the order above.
10. Write the one improvement doc to the folder. The transcript stays in the scratchpad and is discarded.
11. Print the verdict and apply-now section to chat, each drafted change shown for approval.
12. On approval only, save each drafted change to its real home (a rule, a Forge exercise, a repo-dive queue, OS_IMPROVEMENTS.md).

## Output location

`Reference/Learn_and_apply/`. One file per video: `<Video_title_sentence_case>_March_04.md`.

## Files this build created

| File | Purpose |
| --- | --- |
| .claude/skills/yt-learn/SKILL.md | The recipe, the front door, the approval gate |
| .claude/skills/yt-learn/scripts/clean_vtt.py | Caption cleaner |
| .claude/workflows/yt-learn.js | The engine (extract, synthesize, verify, map-to-upgrades) |
| Reference/Learn_and_apply/ | Where the improvement docs land |

## Reused, not rebuilt

- clean_vtt.py: written and tested July 11.
- The map-reduce workflow: written, run, and verified July 11. Gained one stage (map to upgrades), parameterized by url.
- systems-map, Forge, repo-dive: existing skills, now reachable as deeper-dive outputs.

## Cost split

The full run used 8 agents, about 563k subagent tokens. Under 25 minutes defaults to lite (one agent, cheap). Flags override. Attack-the-constraint: do not pay for eight agents on a short clip.

## Rules this honors

file-protection (nothing saved without approval), writing-style and file-naming (doc and filenames), goal-contracts (done-when and verify surface), self-eval-loop (the fact-checker), os-improvement-logging (an approved system upgrade logs a row), boil-the-lake (cover the whole video).

## Non-goals (v1)

Cron, radar, scheduling. Whisper fallback. Non-YouTube sources. Persisting the transcript by default. Auto-applying anything without approval.

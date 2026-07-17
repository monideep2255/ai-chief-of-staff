---
name: yt-learn
author: human
description: Turn a YouTube video into concrete upgrades to your system, knowledge, and skills, without watching it. TRIGGER when the user drops a YouTube URL and says "yt-learn", "learn from this video", "what can I use from this", "review this podcast/talk", or asks to extract buildable ideas from a video. Not a summarizer and not the Perplexity inbox: it fetches captions locally, fact-checks against the transcript, and drafts approvable changes. Differs from ingest-workflows (files already in the inbox), ingest-conference (conference sessions), and web-research (articles and URLs, not video).
scope: project
user_invocable: true
agent: true
model: sonnet
depends_on:
  - .claude/workflows/yt-learn.js
  - .claude/skills/yt-learn/scripts/clean_vtt.py
  - .claude/rules/writing-style.md
  - .claude/rules/file-naming.md
  - .claude/rules/file-protection.md
  - .claude/rules/goal-contracts.md
  - .claude/rules/self-eval-loop.md
  - .claude/rules/os-improvement-logging.md
  - .claude/skills/systems-map/SKILL.md
  - .claude/skills/forge/SKILL.md
  - .claude/skills/repo-dive/SKILL.md
  - Reference/Learn_and_apply/README.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - README.md
  - CHANGELOG.md
  - .claude/WHATS_NEW.md
  - DEPENDENCIES.md
---

# /yt-learn - turn a video into upgrades to your system, knowledge, and skills

This is an improvement engine, not a summarizer. Content goes in, concrete upgrades come out. The summary is a supporting layer; the drafted change is the point.

It fetches the caption track locally (no third-party scraper, no API key), cleans it, runs a fact-checked map-reduce over it, and writes one doc that leads with what you can apply right now. Nothing is saved into the repo until you approve it.

## Invocation

```text
/yt-learn <url>            # auto: lite for short videos, full engine for long ones
/yt-learn <url> --full     # force the full multi-agent engine
/yt-learn <url> --lite     # force single-pass, cheap
/yt-learn <url> --map      # also offer to generate a systems-map from the concepts
/yt-learn <url> --keep-transcript   # also save the cleaned transcript (off by default)
```

Do not skip steps. This skill has an approval gate at the end; the whole point is that it drafts changes and you approve them. Running the fetch and the engine but not presenting the drafts for approval is a failed run.

## Step 1: set the scratchpad and parse the url

Work entirely in the session scratchpad until the final doc. Set `WORK` to your scratchpad directory (the one named in your environment, ending in `/scratchpad`). Extract the 11-character video id from the url (`v=<id>` or `youtu.be/<id>`).

## Step 2: pull captions and metadata with yt-dlp

`yt-dlp` is installed (`/opt/homebrew/bin/yt-dlp`). `www.youtube.com` is sandbox-allowlisted, so no override is needed.

```bash
URL="<the url>"
WORK="<your scratchpad dir>"
# metadata: title | duration_seconds | channel | upload_date
yt-dlp --skip-download --print "%(title)s|%(duration)s|%(channel)s|%(upload_date)s" "$URL"
# captions (auto or human), English, VTT
yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en --sub-format vtt -o "$WORK/yt" "$URL"
```

## Step 3: no captions is an honest stop

If no `$WORK/yt.en.vtt` (or any `yt*.vtt`) was written, stop. Tell the user the video has no caption track and that whisper transcription is out of scope for v1. Do not invent a summary. Do not proceed.

## Step 4: clean the captions

```bash
python3 .claude/skills/yt-learn/scripts/clean_vtt.py "$WORK/yt.en.vtt"
# writes $WORK/yt.en.clean.txt and prints cleaned_words=N
```

## Step 5: choose lite or full

- `--lite` forces lite. `--full` forces full.
- Otherwise: duration under 25 minutes (1500 seconds) is lite; 25 minutes or more is full.
- Lite is cheaper (about 4 subagents). Full fans out over the whole video (about 8 to 9 subagents). Do not pay for the full engine on a short clip (attack-the-constraint).

## Step 6: chunk the transcript

Lite: one chunk (the whole cleaned file). Full: about six chunks of roughly 4000 words.

```bash
CLEAN="$WORK/yt.en.clean.txt"
MODE="<lite|full>"
python3 - "$CLEAN" "$WORK" "$MODE" <<'PY'
import sys, math
clean_path, out_dir, mode = sys.argv[1], sys.argv[2], sys.argv[3]
words = open(clean_path, encoding="utf-8").read().split()
n = len(words)
k = 1 if mode == "lite" else max(1, min(8, math.ceil(n / 4000)))
size = math.ceil(n / k) if k else n
paths = []
for i in range(k):
    p = f"{out_dir}/chunk_{i+1}.txt"
    open(p, "w", encoding="utf-8").write(" ".join(words[i*size:(i+1)*size]))
    paths.append(p)
print("\n".join(paths))
PY
```

Collect the printed chunk paths.

## Step 7: run the engine (the workflow)

Invoke the Workflow tool with `name: "yt-learn"`. If that returns "not found" (the name registry only reloads at session start, so a freshly built or edited workflow is not yet named), fall back to `scriptPath: ".claude/workflows/yt-learn.js"`. Either way pass `args`:

```json
{
  "url": "<the url>",
  "title": "<title from metadata>",
  "channel": "<channel>",
  "durationSec": <duration>,
  "mode": "<lite|full>",
  "chunkPaths": ["<absolute chunk_1.txt>", "..."]
}
```

The workflow reads each chunk, extracts claims and buildable ideas in parallel, synthesizes the understanding layer, fact-checks it with a fresh-context agent that never saw the raw transcript, then maps every idea into the three buckets (system, knowledge, skill) and drafts the apply-now changes. It returns `{ brief, verify, upgrades }`.

Do not summarize from the transcript yourself. The fact-check step exists because the synthesis agent can smuggle in outside claims; trust the workflow's verify output over your own reading.

## Step 8: assemble the doc

Write one markdown file to `Reference/Learn_and_apply/`. Filename: the video title in sentence case with underscores, then the month and day, per `.claude/rules/file-naming.md`. Example: `Agent_skills_walkthrough_March_04.md`.

Follow `.claude/rules/writing-style.md` for the prose: no em dashes, sentence case headings, no bold (use "word:" format), no LLM brand names in your own prose. Structure the doc in this exact order:

```markdown
---
description: One line on what this video gives you (~120 chars)
type: learn-and-apply
source_url: <url>
channel: <channel>
video_date: <YYYY-MM-DD from upload_date, else blank>
duration_min: <rounded minutes>
added: <YYYY-MM-DD, today>
---

# <Video title in sentence case>

## Verdict
Watch, skim, or skip. Minutes worth it. For whom. (from upgrades.verdict)

## Apply now
For each item in upgrades.apply_now (1 to 3), a subsection:
### <action, one line>
- Bucket: system | knowledge | skill
- Target: <the rule / skill / repo / doc it changes>
- Source: <timestamp>
- Why: <one line>
- Drafted change: the actual proposed text, fenced. This is what you approve.

## What I can use for what
A table of every worthwhile idea (upgrades.use_for_what):
| Idea | Bucket | How it applies | Timestamp |

## Go deeper (optional)
List upgrades.go_deeper offers: a systems-map, a Forge exercise, or a knowledge doc. Note that these fire only if the user asks.

## Understanding
The supporting layer, kept last (from brief): TL;DR, real vs creator hype, skip-to guide.

## Grounding note
One line from verify: overall grounding rating, and any correction the fact-checker made. This is why you can trust the mapping above.
```

If `verify` flagged a high-severity grounding issue, apply its correction to the doc before writing, and say so in the grounding note.

## Step 9: discard the transcript

Unless `--keep-transcript` was passed, leave the transcript in the scratchpad (it is discarded when the session ends). If `--keep-transcript`, copy `$WORK/yt.en.clean.txt` to `Reference/Learn_and_apply/<same_basename>_transcript.md`.

## Step 10: present drafts for approval (the gate)

Print to chat: the verdict, then each apply-now item with its drafted change shown in full. Ask the user to approve, edit, or skip each one. Do not save any drafted change into its real home yet.

## Step 11: on approval only, apply

For each change the user approves, and only then:
- rule: write the drafted rule to `.claude/rules/<name>.md` with frontmatter, then run the dependency-tracking walk.
- skill edit: apply the drafted edit to the named skill.
- Forge exercise: scaffold it under `Forge/exercises/`.
- repo-dive: note the candidate; the user runs `/repo-dive <url>` when ready.
- knowledge doc: write to the right `Reference/` folder and run `/wiki-lint`.
- Any adopted OS change: append a row to `OS_IMPROVEMENTS.md` per `os-improvement-logging.md`.

Then recommend `/os-maintain` (OS component sync) followed by `/ship`.

## Exit checklist

Done when all are true:

- [ ] Captions fetched locally, or an honest no-transcript stop (Steps 2, 3)
- [ ] Transcript cleaned and chunked (Steps 4, 6)
- [ ] The engine ran and returned brief, verify, and upgrades (Step 7)
- [ ] One doc written to `Reference/Learn_and_apply/`, 5 sections in order, writing-style clean, high-severity grounding issues corrected (Step 8)
- [ ] Transcript discarded unless --keep-transcript (Step 9)
- [ ] Verdict and every apply-now draft presented for approval; nothing saved to its real home without approval (Steps 10, 11)

## Anti-rationalization

- "The video was short, I can just summarize it myself" - no. The fact-check step is what makes the output trustworthy. Run the engine.
- "This idea obviously applies, I can save the rule without asking" - no. The approval gate is the feature. Present it, wait.
- "I already read the transcript, the verify pass is redundant" - no. You are the one most likely to have absorbed the creator's framing. The fresh-context grader is the check.

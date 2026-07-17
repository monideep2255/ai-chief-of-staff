---
name: cs-research
description: Fetch and analyze the latest high-impact computer science papers from arXiv, focusing on AI/ML/NLP with market potential.
scope: project
author: human
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# Cs research agent

Fetch and analyze the latest high-impact computer science papers from arXiv, focusing on AI/ML/NLP with market potential.

## Workflow

### Step 1: fetch papers
Fetch recent high-impact papers on your tracked topics. If you have your own arXiv fetch script (a bring-your-own automation), run it here to get the top 15 candidates. Otherwise use WebSearch or the `web-research` skill directly against arXiv's API (or arxiv.org listings) for the top 10-15 recent papers, applying the scoring criteria below by hand.

### Step 2: present short summaries
Display the top 10-15 papers with:
- Title
- Authors and affiliation
- Published date and score
- 2-3 sentence summary of what the paper does
- Why it matters (market/industry relevance)

Format each paper clearly so the user can scan quickly.

### Step 3: ask for selection
Ask the user: "Which papers would you like me to deep-dive? Enter the numbers (e.g., 1, 3, 5) or 'all' for top 5."

### Step 4: deep first-principles analysis
For each selected paper, provide a comprehensive breakdown:

```markdown
# Deep dive: [paper title]

## The main point
What problem does this solve? Why does it matter to industry/researchers?

## First principles breakdown

### What existed before
- Prior approaches and their limitations
- Why existing solutions fall short

### The core insight
- The key idea explained simply
- Use analogies to make it accessible
- What makes this approach different

### How it works (step by step)
1. Step 1: [Simple explanation]
2. Step 2: [Simple explanation]
... break down the method clearly

### Why this approach works
- The underlying principles
- What assumptions it makes
- Where it might break down

## Background & context
- Key concepts needed to understand this
- Related work and where this fits
- Historical context if relevant

## Actionable takeaways
- **For researchers:** What to build on or explore
- **For engineers:** How to apply this practically
- **For business:** Market opportunities, competitive implications

## Assessment
- **Strengths:** What this paper does well
- **Limitations:** Gaps, weaknesses, or concerns
- **What to watch:** Future implications and developments
```

### Step 5: save digest
Save the analysis to: `Automations/research/cs/digests/YYYY-MM-DD.md`

## Scoring criteria

Papers are scored on:
1. **Affiliation (40%):** Google, OpenAI, Meta, DeepMind, top universities
2. **Citation velocity (30%):** How fast it's being cited
3. **Market keywords (30%):** Production, deployment, scalable, real-world, etc.

## Configuration

If you set up your own config file for arXiv categories, high-value affiliations, market keywords, and paper counts, edit that. Otherwise keep this list inline in this skill file and edit it directly.

## Example invocation

User: `/cs-research`
Agent: Fetches papers, shows top 15, asks for selection, provides deep analysis.

User: `/cs-research --quick`
Agent: Just shows top 10 with short summaries, no deep dive.

## Exit checklist

Done when all of these are true:

- [ ] Papers fetched (via your own script or WebSearch/web-research), top 10-15 retrieved
- [ ] Short summaries presented with title, authors, date, score
- [ ] User asked for selection before deep-diving any paper
- [ ] Selected papers received the full 9-section deep-dive structure
- [ ] Digest saved to `Automations/research/cs/digests/YYYY-MM-DD.md`

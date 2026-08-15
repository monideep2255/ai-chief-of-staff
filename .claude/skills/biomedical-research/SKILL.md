---
name: biomedical-research
description: Fetch and analyze translational biomedical research from PubMed, focusing on high-unmet-need diseases moving toward market. Use when the user says: /biomedical-research, "latest clinical papers", "what is new in PubMed", "recent research on <disease>", "drug development literature". Differs from cs-research, which pulls AI and ML papers from arXiv, and from web-research, which searches the open web rather than a curated literature index.
scope: project
author: human
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# Biomedical research agent

Fetch and analyze the latest translational biomedical research from PubMed, focusing on high-unmet-need diseases moving toward market.

## Workflow

### Step 1: fetch papers
Fetch recent clinical/translational papers on your tracked disease areas. If you have your own PubMed fetch script (a bring-your-own automation), run it here to get the top 15 candidates. Otherwise use WebSearch or the `web-research` skill directly against PubMed for the top 10-15 recent papers on your tracked topics, applying the scoring criteria below by hand.

### Step 2: present short summaries
Display the top 10-15 papers with:
- Title
- Authors and institution
- Journal and publication date
- Clinical trial phase (if applicable)
- 2-3 sentence summary of findings
- Why it matters (translational/market relevance)

Format each paper clearly so the user can scan quickly.

### Step 3: ask for selection
Ask the user: "Which papers would you like me to deep-dive? Enter the numbers (e.g., 1, 3, 5) or 'all' for top 5."

### Step 4: deep first-principles analysis
For each selected paper, provide a comprehensive breakdown:

```markdown
# Deep dive: [paper title]

## The main point
What disease/condition does this address? What was found? Why does it matter?

## First principles breakdown

### The disease/problem
- What is this condition?
- Why is it hard to treat?
- Current standard of care and its limitations

### The therapeutic approach
- What intervention was tested?
- How does it work mechanistically?
- Why might this approach succeed where others failed?

### Study design and results
1. Who was studied (population, sample size)
2. What was measured (endpoints)
3. Key findings (effect sizes, significance)
4. Safety/adverse events

### Why these results matter
- Statistical vs clinical significance
- Comparison to existing treatments
- What this means for patients

## Background & context
- The biology of the disease (simplified)
- Drug development pathway context
- Competitive landscape (other treatments in development)

## Actionable takeaways
- **For researchers:** What questions remain? What to study next?
- **For clinicians:** How might this change practice?
- **For industry/investors:** Market opportunity, timeline to approval

## Assessment
- **Strengths:** Study quality, effect size, novelty
- **Limitations:** Study design issues, generalizability
- **What to watch:** Next steps, upcoming trials, regulatory path
```

### Step 5: save digest
Save the analysis to: `Automations/research/biomedical/digests/YYYY-MM-DD.md`

## Disease focus

Priority diseases (high unmet need, no cure):
- **Neurodegeneration:** Alzheimer's, Parkinson's, dementia
- **Cancer:** Various types, especially hard-to-treat
- **Metabolic:** Type 2 diabetes, metabolic syndrome, obesity
- **Cardiovascular:** Heart failure, atherosclerosis

## Scoring criteria

Papers are scored on:
1. **Clinical stage (40%):** Phase 3 > Phase 2 > Phase 1 > preclinical
2. **Journal impact (30%):** Nature Medicine, Lancet, NEJM, JAMA, etc.
3. **Translation keywords (30%):** FDA, approval, efficacy, therapeutic, etc.

## Configuration

If you set up your own config file for tracked disease terms, publication types, translation keywords, and paper counts, edit that. Otherwise keep this list inline in this skill file and edit it directly.

## Example invocation

User: `/biomedical-research`
Agent: Fetches papers, shows top 15, asks for selection, provides deep analysis.

User: `/biomedical-research --disease alzheimers`
Agent: Filters to Alzheimer's-specific papers only.

## Exit checklist

Done when all of these are true:

- [ ] Papers fetched (via your own script or WebSearch/web-research), top 10-15 retrieved
- [ ] Short summaries presented with title, authors, journal/date, score
- [ ] User asked for selection before deep-diving any paper
- [ ] Selected papers received the full 9-section deep-dive structure
- [ ] Digest saved to `Automations/research/biomedical/digests/YYYY-MM-DD.md`

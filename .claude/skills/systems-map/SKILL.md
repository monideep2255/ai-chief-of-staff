---
name: systems-map
author: human
description: Map any complex system into 8-12 visual building blocks through structured conversation, web research, and iterative refinement. Output path: Learning/visual-synthesis/<topic>/.
scope: portable
argument-hint: <topic>
user_invocable: true
agent: true
model: opus
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/doc-construction.md
  - .claude/skills/web-research/SKILL.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - .claude/rules/book-inventory-check.md
---

# /systems-map - visual systems thinking through structured exploration

Map any complex system into 8-12 building blocks, organized into 3 color-coded categories, with a mermaid relationship diagram and expandable deep-dive sections. Single self-contained HTML file.

This is a learning skill, not a production skill. The process of building the map IS the learning. Every phase should deepen understanding. The HTML at the end is a byproduct of structured curiosity.

## Invocation

```
/systems-map <topic>
```

**Examples:**
- `/systems-map energy and AI infrastructure`
- `/systems-map semiconductor supply chain`
- `/systems-map US healthcare system`
- `/systems-map global food systems`

## Design principles

1. Exploration over production: the process of building the map is the learning
2. Externalize early: get the mental model into a visual artifact so spatial thinking can work
3. Challenge, don't just fill: web research should surprise, not just confirm
4. One question at a time: respect how systems thinkers reason

## Workflow

Four phases: Articulate, Externalize, Challenge, Refine.

---

### Phase 1: Articulate (2-3 conversation turns)

Goal: extract the user's mental model through structured conversation.

**Step 1: Parse and seed**

Extract the topic from the user's input. Ask:

> "What's the core chain you're most confident about? Give me the sequence of building blocks as you see them. Example: Energy -> Data centers -> Chips -> Frontier AI -> Applications"

Wait for the seed chain.

**Step 2: Expand outward**

For each node in the seed chain, ask ONE question per turn (do not batch):

- "What feeds into [node]? What resources, inputs, or prerequisites does it depend on?"
- "What forces act on [node]? Political, economic, environmental, social?"
- "What breaks downstream if [node] fails or changes?"

Build a running list of candidate building blocks as the user responds. Show the growing list after each answer.

**Step 3: Propose structure**

After 2-3 rounds of expansion, propose:

1. 8-12 candidate building blocks (named, with 1-line descriptions)
2. 3 categories to group them (user names the categories)
3. Color mapping: blue (category 1), green (category 2), purple (category 3)
4. Key connections between blocks (which block feeds into which)

Ask: "Does this capture your model? Anything to merge, split, add, or remove?"

Wait for validation. Adjust until the user confirms.

---

### Phase 2: Externalize (1 turn, skill generates)

Goal: turn the validated mental model into a draft visual HTML so the user can see and react to their own thinking.

**Step 1: Create output directory**

```bash
mkdir -p "Learning/visual-synthesis/<topic-kebab-case>"
```

Use kebab-case for the topic directory name. Examples:
- `energy-and-ai-infrastructure`
- `semiconductor-supply-chain`
- `us-healthcare-system`

**Step 2: Generate draft index.html**

Write `Learning/visual-synthesis/<topic-kebab-case>/index.html` using the HTML template below.

For the draft version:
- Summary view (cards + mermaid diagram): fully populated from Phase 1 conversation
- Expanded sections: placeholder text (1-2 sentences per block from the conversation)
- Sources section: empty (will be filled in Phase 4)

**Step 3: Present to user**

Tell the user to open the HTML file in their browser:

> "Draft map generated at `Learning/visual-synthesis/<topic>/index.html`. Open it in your browser. Look at the diagram and cards. What connections are wrong? What's missing? What should merge?"

Wait for reactions. If the user requests structural changes (merge blocks, add connections, remove a block), regenerate the HTML before proceeding to Phase 3.

---

### Phase 3: Challenge (2-3 turns, web research)

Goal: use web research to teach the user things they didn't know about the system, challenge their model, and surface missing connections.

This phase should feel like learning, not data entry. The skill is a thinking partner.

**Step 1: Research each building block**

For each building block, run targeted web research using the web-research skill protocol:

1. Use WebSearch with a focused query: "[building block name] [topic context] key facts data 2025 2026"
2. For promising results, use WebFetch or Firecrawl to get full content
3. Look specifically for:
   - Data points the user likely doesn't know
   - Connections between blocks the model missed
   - Recent developments (last 12 months) that change the picture
   - Surprising facts that reframe a building block
   - Counterarguments to the user's assumed connections

**Record every URL consulted.** This is non-negotiable. Each source gets: page title, URL, which building block(s) it informs.

**Step 2: Present challenges**

Present findings as a batch of challenges (not a dry data dump):

> "I researched all 10 building blocks. Here are 5 things your model doesn't account for:
>
> 1. Your map shows energy feeding data centers, but doesn't account for water scarcity. Three of the top 10 US data center markets are in drought-prone regions. [source]
> 2. Did you know rare earth mining (for chips) has its own water dependency? The connection between water and chips is missing from your model. [source]
> 3. Recent development: the EU's 2026 energy sovereignty directive affects chip manufacturing location decisions. This creates a new connection between politics and chips. [source]
> 4. ..."

Ask: "Which of these should we add to the map? Any that surprise you?"

Wait for the user's decisions. Track which findings get incorporated.

**Step 3: Update the mental model**

Research will reveal that the original mental model is incomplete or incorrect. This is the point. Update the model based on findings:

- Add missing connections between blocks (new arrows in the mermaid diagram)
- Correct wrong connections (remove or reverse arrows)
- Split a block if research reveals it contains two separate bottlenecks
- Add new blocks if research surfaces a building block the user missed entirely
- Update card descriptions and expanded content with research data
- Flag any connection that turns out to be two-way when the original model showed it as one-way

The mental model is a living artifact. If the research says it's wrong, change it. Do not preserve the original model out of politeness. The user came here to learn, not to be validated.

---

### Phase 4: Refine (1-2 turns)

Goal: regenerate the HTML with rich content from research, producing the final artifact.

**Step 1: Regenerate HTML**

Update `index.html` with:

- Expanded sections: 2-3 paragraphs per block in plain language (not jargon)
  - What this building block is and why it matters
  - Key data points with inline source links (every claim attributed)
  - "Why this matters" closing line
  - Connections list: "Feeds into: [block names]. Receives from: [block names]."
- Updated mermaid diagram: add any new connections from the challenge phase
- Sources section: complete list of ALL URLs consulted, grouped by building block
- Footer: "Built through structured exploration on [date]. [N] sources consulted."

**Step 2: Final review**

> "Final map regenerated. Open `index.html` in your browser. Click any card to see the expanded view with data points and sources. Check the Sources section at the bottom for the full list of URLs consulted. Anything to adjust?"

Make final adjustments if requested.

**Step 3: Done**

> "Systems map complete: `Learning/visual-synthesis/<topic>/index.html`
> [N] building blocks across 3 categories. [M] sources consulted. [date]."

---

## HTML template reference

Use this as the base template when generating `index.html`. Adapt the content (title, cards, diagram, sources) per topic. The CSS design system is borrowed from the GraphConf 2026 key-principles cheat sheet.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Systems map: [TOPIC TITLE]</title>
<style>
  :root {
    --blue: #2c5282;
    --green: #276749;
    --purple: #553c9a;
    --blue-light: #ebf2fa;
    --green-light: #e6f4ed;
    --purple-light: #f0ebf8;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-500: #6b7280;
    --gray-700: #374151;
    --gray-900: #111827;
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: var(--gray-900);
    background: var(--gray-50);
    line-height: 1.4;
    padding: 24px;
  }

  header {
    text-align: center;
    margin-bottom: 20px;
  }

  header h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--gray-900);
    margin-bottom: 4px;
    line-height: 1.3;
  }

  header p.subtitle {
    font-size: 0.85rem;
    color: var(--gray-500);
    margin-bottom: 12px;
  }

  .legend {
    display: flex;
    justify-content: center;
    gap: 24px;
    flex-wrap: wrap;
    margin-bottom: 16px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    color: var(--gray-700);
  }

  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .legend-dot.cat1 { background: var(--blue); }
  .legend-dot.cat2 { background: var(--green); }
  .legend-dot.cat3 { background: var(--purple); }

  .diagram-section {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    text-align: center;
  }

  .diagram-section h2 {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--gray-700);
    margin-bottom: 12px;
  }

  .mermaid {
    display: flex;
    justify-content: center;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 20px;
  }

  .card {
    background: white;
    border-radius: 8px;
    padding: 14px 14px 14px 18px;
    border: 1px solid var(--gray-200);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: box-shadow 0.2s;
  }

  .card:hover {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
  }

  .card.cat1::before { background: var(--blue); }
  .card.cat2::before { background: var(--green); }
  .card.cat3::before { background: var(--purple); }

  .card-header {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-bottom: 6px;
  }

  .card-number {
    font-size: 1.1rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .card.cat1 .card-number { color: var(--blue); }
  .card.cat2 .card-number { color: var(--green); }
  .card.cat3 .card-number { color: var(--purple); }

  .card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--gray-900);
    line-height: 1.3;
  }

  .card-cluster {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 1px 6px;
    border-radius: 3px;
    display: inline-block;
    margin-bottom: 6px;
    font-weight: 600;
  }

  .card.cat1 .card-cluster { background: var(--blue-light); color: var(--blue); }
  .card.cat2 .card-cluster { background: var(--green-light); color: var(--green); }
  .card.cat3 .card-cluster { background: var(--purple-light); color: var(--purple); }

  .card-desc {
    font-size: 0.75rem;
    color: var(--gray-700);
    line-height: 1.45;
  }

  .card-toggle {
    font-size: 0.65rem;
    color: var(--gray-500);
    margin-top: 8px;
    text-align: right;
  }

  .card-expanded {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.3s ease;
    padding: 0 0;
  }

  .card.expanded .card-expanded {
    max-height: 600px;
    padding: 12px 0 0 0;
  }

  .card.expanded .card-toggle {
    display: none;
  }

  .card-expanded-inner {
    border-top: 1px solid var(--gray-200);
    padding-top: 12px;
    font-size: 0.75rem;
    color: var(--gray-700);
    line-height: 1.55;
  }

  .card-expanded-inner p {
    margin-bottom: 8px;
  }

  .card-expanded-inner .data-point {
    background: var(--gray-100);
    padding: 6px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-size: 0.7rem;
  }

  .card-expanded-inner .data-point a {
    color: var(--blue);
    text-decoration: none;
  }

  .card-expanded-inner .data-point a:hover {
    text-decoration: underline;
  }

  .card-expanded-inner .connections {
    font-size: 0.68rem;
    color: var(--gray-500);
    margin-top: 8px;
    font-style: italic;
  }

  .card-expanded-inner .why-matters {
    font-weight: 600;
    color: var(--gray-900);
    margin-top: 8px;
  }

  .card-close {
    display: none;
    font-size: 0.65rem;
    color: var(--gray-500);
    margin-top: 8px;
    text-align: right;
  }

  .card.expanded .card-close {
    display: block;
  }

  .sources-section {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
  }

  .sources-section h2 {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--gray-700);
    margin-bottom: 12px;
  }

  .sources-section h3 {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--gray-900);
    margin-top: 10px;
    margin-bottom: 4px;
  }

  .sources-section ul {
    list-style: none;
    padding: 0;
  }

  .sources-section li {
    font-size: 0.7rem;
    color: var(--gray-700);
    padding: 2px 0;
  }

  .sources-section a {
    color: var(--blue);
    text-decoration: none;
  }

  .sources-section a:hover {
    text-decoration: underline;
  }

  footer {
    text-align: center;
    font-size: 0.7rem;
    color: var(--gray-500);
    padding-top: 8px;
    border-top: 1px solid var(--gray-200);
  }

  /* Tablet: 2 columns */
  @media (max-width: 900px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Mobile: 1 column */
  @media (max-width: 560px) {
    body { padding: 16px; }
    .grid {
      grid-template-columns: 1fr;
    }
    header h1 { font-size: 1.2rem; }
  }

  /* Print styles: fit summary on one page */
  @media print {
    @page {
      size: letter;
      margin: 0.4in;
    }

    body {
      padding: 0;
      background: white;
      font-size: 9pt;
    }

    header { margin-bottom: 10px; }
    header h1 { font-size: 13pt; }
    header p.subtitle { font-size: 7.5pt; margin-bottom: 6px; }

    .legend { margin-bottom: 8px; }
    .legend-item { font-size: 6.5pt; }

    .diagram-section {
      padding: 8px;
      margin-bottom: 10px;
      box-shadow: none;
      border: 1px solid #ccc;
      page-break-inside: avoid;
    }

    .diagram-section h2 { font-size: 7.5pt; margin-bottom: 6px; }

    .grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 10px;
    }

    .card {
      padding: 8px 8px 8px 12px;
      box-shadow: none;
      border: 1px solid #ccc;
      page-break-inside: avoid;
      cursor: default;
    }

    .card-number { font-size: 9pt; }
    .card-title { font-size: 7.5pt; }
    .card-cluster { font-size: 5.5pt; }
    .card-desc { font-size: 6.5pt; line-height: 1.35; }
    .card-toggle { display: none; }

    .card-expanded { max-height: none !important; padding-top: 6px !important; }
    .card-expanded-inner { font-size: 6pt; }

    .sources-section {
      page-break-before: always;
      padding: 8px;
      box-shadow: none;
      border: 1px solid #ccc;
    }
    .sources-section h2 { font-size: 8pt; }
    .sources-section h3 { font-size: 7pt; }
    .sources-section li { font-size: 6pt; }

    footer { font-size: 6pt; padding-top: 4px; }
  }
</style>
</head>
<body>

<header>
  <h1>[TOPIC TITLE]</h1>
  <p class="subtitle">[SUBTITLE - e.g. "A systems map of how energy, infrastructure, and policy shape the AI stack"]</p>
  <div class="legend">
    <span class="legend-item"><span class="legend-dot cat1"></span> [CATEGORY 1 NAME]</span>
    <span class="legend-item"><span class="legend-dot cat2"></span> [CATEGORY 2 NAME]</span>
    <span class="legend-item"><span class="legend-dot cat3"></span> [CATEGORY 3 NAME]</span>
  </div>
</header>

<section class="diagram-section">
  <h2>How the building blocks connect</h2>
  <div class="mermaid">
flowchart TD
    [MERMAID NODES AND EDGES HERE]
    [COLOR STYLE EACH NODE BY CATEGORY]
  </div>
</section>

<section class="grid">

  <!-- Repeat this card block for each building block (8-12 cards) -->
  <div class="card [cat1|cat2|cat3]" onclick="toggleCard(this)">
    <div class="card-header">
      <span class="card-number">[N]</span>
      <span class="card-title">[BUILDING BLOCK TITLE]</span>
    </div>
    <span class="card-cluster">[CATEGORY NAME]</span>
    <p class="card-desc">[ONE-LINE DESCRIPTION]</p>
    <div class="card-toggle">Click to expand</div>
    <div class="card-expanded">
      <div class="card-expanded-inner">
        <p>[2-3 PARAGRAPHS: what this is, why it matters, how it connects to the system]</p>
        <div class="data-point">[KEY DATA POINT with <a href="URL" target="_blank">source</a>]</div>
        <div class="data-point">[ANOTHER DATA POINT with <a href="URL" target="_blank">source</a>]</div>
        <p class="why-matters">Why this matters: [ONE SENTENCE]</p>
        <p class="connections">Feeds into: [block names]. Receives from: [block names].</p>
      </div>
    </div>
    <div class="card-close">Click to collapse</div>
  </div>

</section>

<section class="sources-section">
  <h2>Sources</h2>
  <p style="font-size: 0.7rem; color: var(--gray-500); margin-bottom: 10px;">
    All URLs consulted during research, grouped by building block.
  </p>

  <!-- Repeat for each building block -->
  <h3>[BUILDING BLOCK N]: [TITLE]</h3>
  <ul>
    <li><a href="[URL]" target="_blank">[PAGE TITLE]</a></li>
    <li><a href="[URL]" target="_blank">[PAGE TITLE]</a></li>
  </ul>
</section>

<footer>
  Built through structured exploration on [DATE]. [N] sources consulted.
</footer>

<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'neutral',
    flowchart: {
      useMaxWidth: true,
      htmlLabels: true,
      curve: 'basis'
    }
  });

  function toggleCard(card) {
    card.classList.toggle('expanded');
  }
</script>

</body>
</html>
```

## Anti-patterns

Check these before finalizing the map. If you catch any, fix before delivering.

- Accepting the user's initial mental model without challenging it (the research phase exists to find what's wrong, not confirm what's right)
- Cramming too many building blocks into the map (more than 12 blocks means you haven't identified what's truly load-bearing vs what's detail)
- Writing expanded sections as generic Wikipedia summaries instead of connecting the block to the specific system being mapped
- Using data points without inline source links (every claim must be attributed)
- Creating one-way arrows between blocks that are actually bidirectional (check every connection direction)

## Quality checks

Run these before delivering the final HTML. Every item must pass.

1. Every building block's expanded section has at least 2 data points with inline source links
2. The mermaid diagram matches the connections described in each card's "Feeds into / Receives from" text (no orphan arrows, no missing connections)
3. At least 2 connections were added or corrected during the Challenge phase (if none changed, the research wasn't challenging enough)
4. The Sources section lists every URL consulted, grouped by building block (no ungrouped URLs, no missing blocks)
5. Building block count is between 8 and 12 (fewer means the system is underspecified, more means it needs merging)

## Exit checklist

Done when all of these are true:

- [ ] User's mental model was extracted through 2-3 conversation turns (Phase 1)
- [ ] 8-12 building blocks proposed, user confirmed structure (Phase 1, Step 3)
- [ ] Draft HTML generated and user reviewed in browser (Phase 2)
- [ ] Web research completed for every building block with all URLs recorded (Phase 3, Step 1)
- [ ] At least 2 connections added or corrected from research findings (Phase 3, Step 2-3)
- [ ] Final HTML has: expanded sections with 2+ data points per block, updated mermaid diagram, complete sources section (Phase 4)
- [ ] All quality checks pass: inline source links, diagram matches card connections, sources grouped by block, 8-12 blocks (Quality checks)
- [ ] Book inventory check was run and user confirmed (per book-inventory-check rule)

## Options

None. The skill always runs the full 4-phase workflow. There is no `--outline-only` or `--skip-research` flag. The research phase is where the learning happens.

## Reference

- This pattern was refined from an earlier systems-map build; no reference copy ships in this repo.
- Web research protocol: [.claude/skills/web-research/SKILL.md](../web-research/SKILL.md)
- Writing style rules: [.claude/rules/writing-style.md](../../rules/writing-style.md)

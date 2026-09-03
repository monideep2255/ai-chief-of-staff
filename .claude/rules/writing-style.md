---
scope: portable
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/rules/pdf-docx-conversion.md
  - .claude/rules/doc-construction.md
  - .claude/rules/response-calibration.md
---

## Writing style

Rules for prose hygiene in all documentation, Confluence pages, and external-facing content. For doc *structure* (ToC, mermaid, first-principles skeleton, simple language), see `doc-construction.md`.

### Formatting
- No em dashes, en dashes, or mid-sentence hyphens as punctuation. These are a strong AI-written signal. Instead, use transition words (additionally, next, also, specifically, in particular), commas, relative clauses ("which", "where", "who"), or restructure into separate sentences. Use colons for lists. Hyphens with spaces ( - ) are acceptable only in tables and bullet labels (e.g. "Label - description")
- Full words in written text, not shortforms. Write "repository" not "repo", and "document" not "doc". The short forms are fine in chat, where speech is colloquial, but not in documentation, Confluence pages, or anything shared as written text.
- **Sentence case in headings and document titles** - not title case. Capitalize only:
  - The first word of the heading
  - Proper nouns (people: Dalio, Kahneman, Priya; places: China, Suez; organizations: Stanford, NATO)
  - Names of months (January, March) and days of the week (Monday, Thursday)
  - Proper adjectives derived from proper nouns (British, Chinese, American, Dutch)
  - Acronyms and initialisms (AI, ML, NLP, RAG, LLM, SVMs, APIs)
  - Named technologies and tools (Neo4j, React, Django, Cypher, SPARQL)
  - Mixed-case technical terms exactly as written (MLOps, kNN, t-SNE, aman.ai)
  - Examples: "Why does it exist?", "Key trade-offs", "How the economic machine works", "Ray Dalio's power index"
- No bold text. Use "word:" format instead (e.g. "What worked:" not "**What worked:**"). Bold looks LLM-generated
- When listing labeled items, use "Label: description" not "**Label.** Description"
- After a colon, capitalize the first word if what follows is a complete sentence. Lowercase if it is a fragment or continuation.
- No line breaks/horizontal rules between sections unless specifically needed
- No literal `\n` or `<br/>` in Mermaid diagrams. Keep node labels short (under 30 chars) or split into separate nodes

### No prose walls

A prose wall is one dense paragraph that crams several distinct facts, steps, or list items into running text. It is hard to scan, hard to update, and easy to lose a fact inside. Whenever a block carries more than one thing a reader will scan for or compare, break it into structure.

- 3 or more distinct facts, items, or steps in a paragraph: convert to a bullet list, one item per line.
- Each item has a name and a detail: use the "Label: detail" bullet form (e.g. "Live: https://example.org", "Stack: Render plus Neon").
- Several things that each carry their own facts (several apps, components, options): give each its own sub-heading with bullets under it, not one paragraph per thing.
- One idea per bullet. Do not rebuild the wall inside a bullet by chaining clauses with commas and semicolons.
- Keep a paragraph only when the sentences flow as one argument or narrative. Facts a reader scans, compares, or edits belong in a list.

The smell test: if you are writing ", a X that does A, a Y that does B, and a Z that does C" inside a sentence, that is a list wearing a paragraph. Break it out.

### Reader callouts

Use short Note and Tip callouts when they help a reader understand technical material without interrupting the main explanation. The callout belongs immediately after the paragraph, table, or list it clarifies.

For Markdown that supports GitHub-style alerts, use this syntax:

```markdown
> [!NOTE]
> Plain English: One short translation, example, or evidence boundary that clarifies the main point.

> [!TIP]
> Did you know? One optional teaching fact, practical shortcut, or memorable connection.
```

- Note: Use for plain-English translations, evidence boundaries, definitions, and examples that directly support the reader's understanding.
- Tip: Use for optional background, practical guidance, or a useful fact that rewards curiosity but is not required to follow the argument.
- Lead with a clear label when it helps, such as "Plain English:", "Evidence boundary:", "Example:", or "Did you know?".
- Keep each callout focused on one idea. Use one to three short sentences in most cases.
- Do not repeat the surrounding prose. A callout must translate, teach, bound, or connect something new.
- Do not add a callout after every section. Use one only where a new reader is likely to pause, misread a boundary, or benefit from nearby context.
- Keep claims evidence-bounded. A Tip is not permission to add an interesting but unsupported fact.
- For Confluence, use the equivalent Note or Info panel instead of pasting GitHub alert syntax that the page may not render.

### No sentence openers ending in "ing"

Never start a sentence with a word ending in "ing". It reads as generic machine-written prose, and it delays the subject so the reader waits to find out who is doing the thing. Three forms, all banned:

- Gerund as subject: "Grounding is the metric I watch", "Building the pipeline took three weeks"
- Participial opener: "Working through the logs, I found the bug"
- Continuous form leading the sentence: "Running the eval showed the gap"

The fix is the same every time. Lead with the concrete noun, or with the person doing the thing.

- "Grounding is the metric I watch" becomes "The metric I watch is grounding"
- "Building the pipeline took three weeks" becomes "The pipeline took three weeks to build"
- "Working through the logs, I found the bug" becomes "I found the bug in the logs"

The one exception: a proper noun or named technology that happens to end in "ing" is a name, not a verb form, so it is fine at the start of a sentence.

This applies to chat replies as well as written deliverables, unlike most of this file. It is a speech habit, so it leaks everywhere.

### Branding and attribution
- Never mention specific LLM vendors or products (e.g. no brand names, no CLI tool names)
- Use generic terms: "LLM", "LLM via CLI tooling", "LLM-assisted"
- When AI disclosure is needed, use the step-by-step workflow table format (see git-history-analysis.md for an example)

### Source links
When content is pulled from any external system (Confluence, Jira, GitLab, GitHub), include a clickable link to the source in the doc. Do not leave a bare page ID, ticket number, or commit hash without a link.

- Confluence pages: `[Page title](https://confluence.meridian.example.org/pages/viewpage.action?pageId=<ID>)`
- Jira tickets: `[Atlas-1234](https://jira.meridian.example.org/browse/Atlas-1234)` (verify base URL with MCP before first use per project)
- GitLab MRs/issues: use the full URL from the MCP response
- GitHub PRs/issues: use the full URL

For source tables (e.g., "Confluence sources" sections in reference docs), the page title should be the link anchor, not a separate column.

### Confluence-specific
- Always publish to personal space (~yourhandle) unless explicitly told otherwise
- Add a table of contents macro for long documents
- Use sentence case for page titles

Triggers:
- Writing or editing any markdown documentation, meeting notes, or reference doc
- Writing a Confluence page or external-facing content
- Generating output the user will copy and share (proposals, strategy docs, summaries)

Does not trigger:
- Code files, commit messages, CHANGELOG entries, frontmatter fields
- Short inline responses or tool call annotations
- Content inside code blocks (preserve the original formatting)

The test: does my output contain any em dashes, bold text, title case headings, LLM brand names, informal shortforms (repo, doc), sentences opening with a word ending in "ing", or prose walls (a dense paragraph of 3+ facts that should be a list) in written text? If I used a Note or Tip, does it add focused reader help instead of decoration or repetition?

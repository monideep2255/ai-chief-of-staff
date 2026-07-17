---
name: web-research
author: human
description: Perplexity-style web research using WebSearch for citation-quality search and Firecrawl (curl API) for clean URL scraping. TRIGGER when user asks to research a topic, look up current information, compare tools/libraries, or fetch and summarize web content. DO NOT TRIGGER for repo documentation lookups (use context7 instead) or internal knowledge questions.
scope: project
argument-hint: <query or URL>
depends_on:
  - .mcp.json
  - .claude/settings.json
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
---

# /web-research - Perplexity-style research

Replace raw web search with a two-tool pipeline: WebSearch for high-quality search, Firecrawl for clean page extraction.

## Why this exists

WebSearch provides web retrieval results. Firecrawl converts any URL into clean markdown, stripping JavaScript rendering artifacts and HTML noise. Together: targeted search + clean extraction = Perplexity-style synthesis.

## Invocation

```
/web-research <query>           # Research a topic
/web-research <url>             # Scrape and summarize a URL
/web-research <query> --deep    # Multi-source synthesis (search + scrape top results)
```

## Tool selection

| Task | Tool | Why |
|------|------|-----|
| Find relevant sources on a topic | WebSearch | Built-in, no MCP context cost |
| Scrape a URL to clean markdown | Firecrawl curl API | Strips HTML/JS noise, returns markdown |
| Light fetch of a simple page | WebFetch | Built-in, sufficient for static HTML pages |
| Library/framework documentation | `context7` plugin | Purpose-built for live library docs |

## Protocol

### Step 1: search with WebSearch

```
Use WebSearch with the user's research question.
Review results for relevance, then read individual URLs for depth using WebFetch or Firecrawl.
```

### Step 2: scrape URLs with Firecrawl (when you need full page content)

For any URL you want to read fully, use curl to call the Firecrawl REST API:

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "URL_HERE", "formats": ["markdown"]}' | jq -r '.data.markdown'
```

Only scrape URLs that will add material depth. Do not scrape all results.

For JavaScript-heavy pages (SPAs, dashboards), Firecrawl handles rendering. For simple static pages, the `fetch` MCP is sufficient.

### Step 3: synthesize

After gathering sources:
1. Lead with the direct answer to the user's question
2. Attribute each key claim to its source (URL)
3. Note where sources conflict or are dated
4. Flag if any sources seem SEO-driven or low quality
5. End with "Sources:" list of URLs used

## Setup requirements

API keys are set up on first use, not in advance. When this skill is invoked:

1. Check if `TAVILY_API_KEY` is set: `echo $TAVILY_API_KEY`
2. If missing, prompt the user: "Tavily API key not set. Get a free key at tavily.com, then run: `export TAVILY_API_KEY=\"tvly-...\"`  — add to ~/.zshrc to persist."
3. Check if `FIRECRAWL_API_KEY` is set before any scrape step: `echo $FIRECRAWL_API_KEY`
4. If missing, prompt the user: "Firecrawl API key not set. Get a free key at firecrawl.dev, then run: `export FIRECRAWL_API_KEY=\"fc-...\"`  — add to ~/.zshrc to persist."

This lazy setup pattern also surfaces how often research tasks come up — each prompt is a data point on actual usage before committing to a paid plan.

## Fallback behavior

If Firecrawl API key is missing: use WebFetch for URL scraping. It handles static pages well. Falls short on JavaScript-rendered content.

## When NOT to use this skill

- Looking up React/Django/Tailwind docs: use `/context7` or `mcp__plugin_context7_context7__query-docs`
- Internal repo questions: read the codebase directly
- Quick one-off URL fetches: WebFetch is sufficient without the full protocol

## Quality checks

Before returning research:
- [ ] At least 2 independent sources for any factual claim
- [ ] No SEO-farm content (check: domain authority, specific vs vague claims)
- [ ] Sources dated within the last 12 months for fast-moving topics (AI, tools)
- [ ] Tavily's pre-synthesized answer cross-checked against the raw source URLs

## Exit checklist

Done when all of these are true:

- [ ] WebSearch run on the research question
- [ ] URLs that add depth scraped with Firecrawl or WebFetch
- [ ] Answer leads with the direct response to the question
- [ ] Every key claim attributed to a source URL
- [ ] Conflicting or dated sources flagged
- [ ] Sources list included, no bare unexplained URLs

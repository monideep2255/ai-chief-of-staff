---
globs: ["Work/example-project/**"]
depends_on: []
depended_by:
  - CLAUDE.md
  - .claude/README.md
  - .claude/rules/ai-security-standards.md
  - .claude/rules/atlas-production-examples.md
---

## Atlas production standards

Apply when writing Python, Django, JavaScript, or SQL code in `Work/example-project/` contexts. These are the non-negotiables that block production deployment at Atlas.

### Security: the critical checks

These patterns will fail Checkmarx (SAST) and block a production deploy. Apply them automatically whenever writing Django views or API handlers:

Input handling:
- Always use `html.escape(request.POST.get('key', ''))` for user input in Django views. Default empty string prevents None errors.
- Cast integer inputs: `int(request.GET.get('key', '0'))`. Never pass raw string to int logic.
- Never disable Django template auto-escaping (`autoescape off` or `|safe`) without a bleach allowlist replacing it.

Query safety:
- All SQL must use parameterized placeholders: `cursor.execute("SELECT ... WHERE id = %s", (user_id,))`. No f-strings or `.format()` in SQL.
- URL-encode all URL parameters: `urllib.parse.quote(decoded_url, safe=":/=?&|+")`. Decode first if the value may already be encoded.
- XML parsers must disable external entities: `etree.XMLParser(resolve_entities=False)`.

Secrets and output:
- Never include API keys, tokens, or passwords in log messages or exception strings. Omit the variable value; log the key name as a string literal instead.
- Non-HTML responses (JSON, plain text) must be escaped: `HttpResponse(html.escape(value))`.

JavaScript (when relevant):
- Never create HTML nodes via string concatenation. Use DOM methods or jQuery element creation.
- Encode all URLs before use: `encodeURI(url)`.
- Validate redirect destination before redirecting: check `new URL(url).hostname.endsWith('example.org')`.

### Code quality: the defaults

- snake_case for all function arguments.
- Type hints on function signatures and dataclasses.
- Parameterized SQL queries only (same rule as security above, reinforced).
- `isort` for Python imports.
- Use sync patterns when making 1 request; use async when making 2+ concurrent requests.

### Testing: the minimum bar

- New endpoints need tests for: valid input, invalid input, missing/null input.
- Integration tests hit a real database. No mocked DB unless the test is specifically testing the mock.
- Any UI changes need a WCAG 2.1 AA accessibility check.

### Hardening: no vibecoding defaults

Non-negotiables agents must apply before calling code production-ready. When multiple gaps exist in a single PR, attack the constraint first: fix the gap that poses the highest real risk before addressing lower-priority items (see `attack-the-constraint` rule).

- No new dependency without security review (maintained, license compatible, no known CVEs, more than one maintainer)
- No endpoint without input validation, tests (valid/invalid/null), and rate limiting consideration
- No database migration without a rollback plan and backward-compatibility verification (expand-contract pattern)
- No production claim without CI evidence (all merge-blocking gates pass)
- No architecture decision without an ADR or equivalent note when it affects future work

Retry-safety gate (for any code an agent loop may run more than once):
- Writes must be idempotent or repeat-safe. An agent loop retries, so a tool that creates, appends, or mutates must produce the same end state whether it runs once or three times. Use upserts, check-then-write, or natural-key dedup, not blind inserts.
- Error messages must say what to do next, not just what failed. A loop reads the error and decides its next action, so "connection refused to host X, retry after backoff or check credentials" beats "Error 500". Actionable errors are a correctness feature when the reader is an agent.

Supply chain gate:
- Lockfiles committed. `pip-audit` / `npm audit` passes. No Critical or High CVEs in new dependencies.

Secrets gate:
- Secrets in env vars or secrets manager only. No secrets in code, logs, or images. Dev and prod credentials are separate.

Multi-agent pipeline gate:
- Every subagent in a multi-agent pipeline must declare an output schema (JSONSchema). Validation runs at every hop between subagents. An unvalidated payload flowing from one LLM to another is how prompt injection moves laterally.
- `maxLength` on every string field and `maxItems` on every array are required, not optional. They cap the blast radius if a single upstream document goes hostile.
- Bounded context items: every context fragment injected into an agent prompt (a retrieved passage, a prior-stage output) carries a hard token or character cap enforced before injection, not only `maxLength` on schema strings. One oversized retrieved passage must not be able to blow the context budget or crowd out the system instructions.
- URL fields use a host-pinned regex (e.g. `^https://([A-Za-z0-9-]+\\.)*meridian\\.example\\.org/`), not just `^https://`.
- Untrusted-source readers (any subagent that ingests external documents) get Read and the relevant MCP, but no Write, no Slack, no email. The orchestrator and writer never see raw documents.
- If you maintain a system architecture reference doc, this tier-separation pattern belongs there.
- Real-world instance of the gap this gate closes: a biomedical MCP server has been found passing LLM output across stage boundaries (service selection to parameter generation to tool return) with only `json.loads` plus a couple of key checks, no JSONSchema, no `maxLength`, no `maxItems`. A malformed-but-parseable payload flows downstream unchecked.

AI answer grounding gate (Atlas search product):
- Cite-or-refuse: every answer an agent generates from sources must be tied to a specific retrieved passage, or the agent must explicitly return "I could not find information on this" and stop. No answering from model priors when retrieval returns nothing. This is the single highest-leverage correctness gate for a biomedical search system, where a confident wrong answer is worse than no answer.
- Every claim in a generated answer carries an inline citation to its source id. An answer with an uncited sentence fails the gate.
- The "no source found" path is a tested path, not an afterthought: write a test that feeds a query with zero retrieval hits and asserts the refusal string, not a fabricated answer.
- Deterministic accept or reject: a citation-grounding or quote-match check decides accept or reject by deterministic rule (exact or substring match after normalization), never by a fuzzy similarity threshold, because a fuzzy accept silently passes a hallucinated quote. Fuzzy scoring may rank repair suggestions only, it never gates acceptance.
- Grade this with the `eval-harness` skill: add cite-or-refuse and citation-coverage as pass/fail acceptance criteria, measured with pass@k against a fixed query set before any answer-generation feature ships.

### When to invoke the full skill

For a complete production readiness review, run a six-lens checklist covering security, testing, code quality, PR readiness, deployment, and production hardening, if you build a review skill for this. This rule covers the critical-path non-negotiables only.

Full reference: your own dev-workflow standards doc, if you maintain one.

The test: did I apply every security, supply-chain, secrets, multi-agent schema, and AI answer grounding gate before calling Atlas or agentic-search code production-ready?

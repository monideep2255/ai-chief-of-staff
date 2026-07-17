# Ingest-workflows operational memory

Running log of lessons learned from past runs. Separate from evals (static checks) and from central auto-memory (user-level).

## Lessons

| Date | Lesson | Source |
|------|--------|--------|
| 2026-06-13 | When processing 5+ files, dispatch parallel agents grouped by destination folder for conversion/cleaning. Merging results before wiki-lint avoids conflicts. | 17-file batch run |
| 2026-06-13 | Always scan for ALL file types in inbox (pdf, docx, html, md), not just .md. Previous runs missed non-markdown files. | User correction |
| 2026-06-13 | Reference folder growth check at 60 docs is important. AI_PM_reference hit 67 and needed a subfolder split (Business_and_finance created). | 17-file batch run |
| 2026-06-13 | Consolidation check (3+ keyword overlap in titles) caught the SpaceX cluster that led to the Business_and_finance folder decision. Worth doing every run. | 17-file batch run |
| 2026-06-13 | The improve-personal-os inbox subdirectory should trigger immediate OS upgrades (Step 3), not just filing. Two docs from this batch generated 2 new OS proposals (items 8-9). | 17-file batch run |
| 2026-05-18 | Brand name replacement must be thorough. Check for all variants: Claude Code, Cursor, Claude.ai, Perplexity (keep in Source: attribution), GPT, Slack, Figma. | Early runs |

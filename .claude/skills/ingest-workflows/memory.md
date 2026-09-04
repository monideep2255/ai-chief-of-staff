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
| 2026-08-15 | Never assume a cross-link target folder from the doc's topic. `Should_you_still_learn_to_code` reads as career content but lives in `Software_engineering_future/`. Locate the file before writing the link, and name the folder in the cross-link text when the pair spans two folders. | 16-file batch run |
| 2026-08-15 | Verify the brand-name grep pattern before trusting its hits. A bare `cowork` pattern matches the ordinary word "coworker" in a title, producing a false positive. Use word-boundary anchors on short brand terms. | 16-file batch run |
| 2026-08-15 | Deleting inbox originals after a successful conversion is standing authorization, granted 2026-08-15. Step 1 deletes without pausing; the exit checklist no longer claims per-run user confirmation. Report the deletions in the run report so the behavior stays visible. | 16-file batch run |
| 2026-08-15 | Content-only ingests do not touch `.claude/`, so `/os-maintain` correctly no-ops (its Phase 1 filters to system components). Go straight to `/ship`, whose docs-sync handles content-driven index and count updates. | 16-file batch run |
| 2026-09-04 | The row above is incomplete and cost a full count audit to discover. `SYSTEM_OVERVIEW.md` hardcodes reference-library totals in four places (overview paragraph, folder table with a per-subfolder breakdown, a Mermaid node, and a component-count table). A content-only ingest invalidates every one of them, and no script checks them. Grep `SYSTEM_OVERVIEW.md` for the old total before shipping any ingest. | 17-file batch run |
| 2026-09-04 | Count folder documents at the folder root, never recursively. A folder holding 30 active documents plus 46 in an `archive/` subfolder returns 76 on a recursive count, which falsely trips the 60-document growth threshold and produces a split proposal for a folder that was already split. The growth check means active documents. | 17-file batch run |
| 2026-09-04 | PDF text extraction silently drops ligatures, yielding "soware" for software, "aer" for after, and "shi" for shift, including inside footnote URL slugs. One batch of three files carried it and the other five batches did not, so it is per-source, not per-run. Sweep every converted file for the common ligature-drop patterns before shipping. | 17-file batch run |
| 2026-09-04 | Many source exports cite nothing but a private webmail inbox URL, so honoring the no-private-URL constraint leaves those documents with no hyperlink at all, attribution resting on the `Source:` line. Expect this and do not treat it as a conversion failure. Audit the existing library separately: private inbox URLs accumulated in earlier runs do not remove themselves. | 17-file batch run |

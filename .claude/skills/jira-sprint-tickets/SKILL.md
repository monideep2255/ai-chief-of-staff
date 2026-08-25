---
name: jira-sprint-tickets
author: human
description: "Review a Jira board or exemplar, learn the target project's live conventions, and safely draft or create tickets, batches, and subtasks. TRIGGER on '/jira-sprint-tickets', 'review this Jira ticket', 'create Jira tickets', 'create sprint tickets', or 'make Jira subtasks'. Project-context skills may supply domain evidence but do not own this reusable Jira workflow."
scope: portable
user_invocable: true
argument-hint: "[review <issue-or-board> | draft <goal> | create]"
depends_on:
  - .claude/rules/writing-style.md
  - .claude/rules/parallel-first.md
depended_by:
  - CLAUDE.md
  - AGENTS.md
  - .claude/README.md
  - DEPENDENCIES.md
  - SYSTEM_OVERVIEW.md
  - .agents/CLAUDE_LINKAGE.md
  - .claude/skills/prism-context/references/workflows.md
---

# Jira sprint tickets

Learn the target Jira project's actual conventions from live evidence, then produce self-contained tickets and useful subtasks without copying stale metadata from an unrelated issue. Use this skill for any Jira project. Load a project-context skill as an evidence source when one exists, but keep project keys, fields, labels, and workflow states out of this reusable body.

## Modes

| Invocation | Result |
|---|---|
| `/jira-sprint-tickets review <issue-or-board>` | Read-only review of structure, metadata, hierarchy, and reusable conventions |
| `/jira-sprint-tickets draft <goal>` | Parent-ticket and optional subtask preview with unresolved metadata shown explicitly |
| `/jira-sprint-tickets create` | Create only the previously approved preview, parallelize independent writes, then verify every mutation with a second authenticated read |

## Establish the project profile

Before drafting, inspect the named board and at least one user-approved exemplar from the same project. Record:

- Project key, board ID and board type.
- Issue type, description structure and workflow state.
- Parent or Epic relationship and the field that stores it.
- Sprint field and verified sprint ID.
- Labels, including exact stored spelling and the board filters that consume them.
- Story-point field and whether estimates live on the parent, subtasks or both.
- Assignee, priority, component, fix version and due-date conventions.
- Subtask structure, ownership, estimates and sequencing.
- Source links, issue links, remote links and closure evidence.
- Create and edit metadata, including required fields, defaults, and fields unavailable through standard screens.
- The board rule for backlog placement and how a newly created issue is proven visible there.

Do not assume that a field ID, label, workflow, screen or hierarchy from one Jira project applies to another. Re-resolve field IDs and editable metadata for the target project.

## Review the exemplar

Separate the result into three categories:

- Reuse: Description structure, evidence discipline, acceptance-criteria style and verified project conventions.
- Ask: Sprint, parent, assignee, estimate, labels, component, priority, versions, due date and any judgment-dependent subtasks.
- Do not copy: Status, resolution, dates, links, ownership, estimates or labels that describe the exemplar's old state rather than the new work.

Check whether the parent remains understandable without its subtasks. Subtasks are justified only when they represent separately trackable outcomes, handoffs or ordered checkpoints. Do not convert a small checklist into empty subtasks.

Rewrite credential-oriented work as an access outcome. Use language such as `obtain and validate approved access`, not `get login credentials`. A ticket may record the request path, owner, access scope, smoke-test result, and blocker. It must not contain passwords, tokens, certificates, private keys, full connection strings, or other secret values.

## Draft the parent ticket

Use this default structure unless the target project has a stronger verified convention:

```text
Summary
[Work area] Action plus concrete object and distinguishing detail

Background
Why the work exists, where it came from, why it matters now and the authoritative source.

Current state
What is verified, what is missing and what remains unknown.

Expected result
The observable deliverable or changed state.

Acceptance criteria
- Testable completion condition
- Required content or important boundary
- Evidence, review or verification condition

Notes and references
- Constraints and exclusions
- Source links
- Parent, sprint and related issues
- Explicit unknowns
```

Default to the shortest description that makes the work understandable and verifiable:

- Parent ticket: Aim for 100 to 200 words. Use one short background paragraph, no more than three current-state bullets, one short expected-result paragraph, and four to seven one-line acceptance criteria.
- Subtask: Aim for 75 to 150 words. Use one or two background sentences, one expected-result sentence, and three to five one-line acceptance criteria.
- Put detailed implementation notes, research history, repeated constraints, and test evidence in subtasks or linked artifacts instead of the parent.
- Do not repeat the same boundary in every section. State it once where it most affects interpretation.
- Treat these ranges as defaults, not hard limits. Exceed them only when safety, compliance, reproduction, or an unusually complex handoff requires the detail.

For research or discovery work, also name the decision question, audience, source boundary, required contents, unknowns and exclusions. For bugs, include environment, reproduction steps, actual result and expected result.

## Draft subtasks

Each subtask needs:

- An action-oriented summary.
- Background that explains its role in the parent.
- An observable expected result.
- Acceptance criteria that another person can verify.
- A parent link.

Order subtasks by dependency when sequence matters. Keep shared scope and exclusions in the parent instead of duplicating the full parent description in every child.

When test execution depends on data or configuration, make the test contract observable. Name the approved fixture, fields or schema, index or query configuration, representative cases, expected results, pass conditions, and known limits. A demo script is useful only when it reproduces the agreed checks without embedded credentials.

## Plan the mutation graph

Before previewing creation, classify every proposed write:

- Independent: Tickets with no parent-key, returned-ID, or shared-state dependency. Create these concurrently after approval.
- Barrier: A child needs its returned parent key, or a field update needs the created issue key. Complete and verify the prerequisite first.
- Independent after barrier: Once the parent exists, create its mutually independent children concurrently.
- Shared configuration: Board, sprint, rank, workflow, or project-setting changes. Keep these sequential and separately approval-gated.

Give parallel workers disjoint issue ownership. Never let two workers search and create the same summary. Parallelism changes scheduling, not the approval boundary or verification standard.

## Preview and approval

Before any Jira write, show:

1. Parent summary and complete description.
2. Metadata table with confirmed values, proposed values and unresolved fields.
3. Subtask summaries and complete descriptions.
4. Creation order and every planned Jira mutation.

Include project-specific or internal update routes as distinct mutations in the preview. Ask for explicit approval of the complete preview. Approval to inspect or draft does not authorize creation, updates, transitions, comments, board changes or deletion.

An explicitly requested title-only ticket may omit its description. Mark that choice in the preview and verify after creation that the description is absent. Do not silently drop a description because the draft is incomplete.

## Prevent duplicate and ambiguous writes

Immediately before each create:

1. Search the target project for the exact summary and inspect close matches.
2. For a subtask, scope the search to the intended parent.
3. Reuse or report one unambiguous existing match instead of creating a duplicate.
4. Stop when multiple plausible matches make the target ambiguous.

A create error can have an unknown outcome. Never retry blindly. Search again for the exact issue, reconcile the returned key when one issue exists, and retry only when Jira proves that nothing was created. If the second create fails, stop and report the partial state.

## Create and verify

After approval:

1. Run the last-moment duplicate checks.
2. Create independent parent or standalone tickets concurrently with only approved metadata.
3. Read every created or reconciled issue back and verify its summary, description state, type, hierarchy, labels, sprint, assignee, priority, and other approved fields.
4. After each parent-key barrier passes, create its independent approved subtasks concurrently.
5. Read every subtask back and verify its direct parent, summary, description, issue type, and approved metadata.
6. Apply separately approved sprint, estimate, rank, link, or transition changes only through a verified route. Read each issue again after the update.
7. Query the named board or backlog and prove that every intended parent appears in the requested location and workflow state.
8. Report every key and URL plus created, reused, reconciled, failed, and unrun states.

If a field cannot be set through the standard issue endpoint, do not silently substitute an internal endpoint. Explain the limitation and ask before using a project-specific alternative.

Do not delete or roll back successfully created issues when another item in the batch fails. Preserve the partial state, stop dependent writes, and report what exists. A corrective mutation needs a new preview and approval.

## Permissions

Allow:

- Read named Jira boards, issues, field metadata, filters and sprint metadata.
- Review live issues and draft previews without modifying Jira.
- Save a local source snapshot when the user explicitly requests a pull, synchronization or named-item import.

Ask:

- Before creating, updating, assigning, estimating, linking, transitioning or commenting on Jira issues.
- Before changing board configuration or using an internal project-specific write endpoint.
- Before retrying a failed write when the exact-state reconciliation is not conclusive.
- Before reusing metadata whose meaning is unclear or whose value is not supported by the new work.

Deny:

- Never print, copy or store Jira credentials in tracked files or chat.
- Never copy assignee, sprint, estimate, status, resolution, due date or labels from an exemplar without confirming they apply.
- Never claim creation or update success without a second authenticated read.
- Never blind-retry a create, parallelize dependent mutations, or let multiple workers own the same issue target.
- Never put credential values or private connection details in a ticket, comment, script, log, screenshot, or tracked file.
- Never delete Jira issues through this skill.

## Exit checklist

- The target board, project and exemplar were verified live or clearly labeled unavailable.
- Project-specific field IDs and label behavior were rechecked.
- The parent is self-contained and its acceptance criteria are observable.
- Every subtask is independently useful and linked to the parent.
- Unknown metadata remains unresolved rather than invented.
- The full batch was previewed before any write.
- Independent writes ran concurrently while parent-key and returned-ID dependencies remained explicit barriers.
- Exact-summary checks ran immediately before creation, and every ambiguous outcome was reconciled before any retry.
- Every approved mutation was verified with a second read.
- The named board or backlog confirms final placement.
- Partial failures distinguish created, reused, reconciled, failed, and unrun items without destructive rollback.
- Credentials and unnecessary personal information were not emitted.

The test: could a teammate understand the ticket without private context, verify when it is done, and distinguish copied project convention from metadata that was chosen for this specific work?

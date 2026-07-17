---
name: project-atlas-status
description: Current milestone and architecture decision for the Atlas project
metadata:
  type: project
---

## Project: Atlas status

Meridian's Atlas project moved its search backend from a single Postgres full text index to a hybrid retrieval layer (Postgres plus a vector store) after the Q2 relevance review showed keyword only search missed paraphrased queries.

Milestone: the hybrid retrieval layer shipped to Atlas staging on June 18 and is scheduled for production rollout once the citation grounding gate in atlas-production-standards.md passes on the fixed evaluation query set.

Why this matters: Atlas's core promise to Meridian stakeholders is that answers are grounded in retrieved sources, not model recall. The retrieval layer choice directly determines whether that gate can pass, so any future change to Atlas's retrieval stack should be checked against this decision before being reversed.

How to apply: when asked to modify Atlas's search or retrieval code, treat the hybrid Postgres plus vector store architecture as the current baseline. Do not silently revert to keyword only search without flagging that this decision exists and asking first.

Source quality: documented decision (Atlas architecture review notes, June 18).

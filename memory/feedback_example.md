---
name: feedback-no-mocked-db-atlas
description: User correction, do not mock the database in Atlas integration tests
metadata:
  type: feedback
---

## Feedback: no mocked database in Atlas integration tests

During a review of the Atlas ingestion pipeline, the user rejected a draft integration test that mocked the Postgres connection with an in-memory stub. The instruction: Atlas integration tests must run against a real test database, not a mock.

Why: a mocked database hides schema drift, constraint violations, and query bugs that only show up against the real engine. Atlas had a prior incident where a mocked test passed while the equivalent production query failed on a foreign key constraint the mock did not enforce.

How to apply: for any new Atlas endpoint or data access change, write the integration test against a real, disposable test database (a throwaway schema or container), not a mock or stub. Reserve mocks for external third-party services Atlas does not control, never for Atlas's own database.

Source quality: stakeholder verbal (repo owner, Atlas code review session).

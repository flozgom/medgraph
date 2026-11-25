---
description: Produce an implementation plan for an approved spec (no code)
argument-hint: <spec number, e.g. 0001>
---

Read `specs/$ARGUMENTS-*.md`. It must have `Status: approved`. If it doesn't, stop and say so.

Explore the code the spec touches, then write `plans/$ARGUMENTS-<same-slug>.md`:
- Header: spec link, "Produced in: plan mode", Status: draft
- **Files**: a table of each file and its change
- **Order of work**: the failing AC tests come first, then the implementation, then `make check`
- **Risks**
- **Done when**: `make check` passes, the `verifier` reports every AC met, and the PR links
  intent → spec → plan

Do not write code until Paco accepts the plan (Status: accepted).

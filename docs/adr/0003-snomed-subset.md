# ADR 0003: SNOMED CT as a local, gitignored subset

- Status: accepted (pending a check of the IS-A source)
- Date: 2026-11-23

## Context
Subsumption ("stage 3 CKD is a CKD") needs SNOMED CT IS-A relationships. SNOMED CT is licensed. It
is free in member countries such as Spain, but redistribution is not allowed. Paco has a full
SNOMED terms CSV.

## Decision
- Raw files go in `data/snomed/` (gitignored) and are never committed.
- The terms CSV serves as the **entity-linking dictionary** (synonym → conceptId).
- IS-A edges come from RF2 `sct2_Relationship_Snapshot` (`typeId = 116680003`, `active = 1`) if the
  CSV has no parent column.
- The graph loads only a **subset**: concepts referenced by Synthea data or by guideline links, plus
  all of their ancestors. A small graph keeps queries fast and prompts small.
- CI and tests use `tests/fixtures/`: only the codes and display names that Synthea emits, plus
  hand-written IS-A edges for the roughly 20 concepts in scope.

## Open question
Does the CSV include parents? This is checked on Day 1. Fallback: download the RF2 relationships file
from the same release.

## Consequences
The README tells users to bring their own SNOMED release. The repo stays license-clean.

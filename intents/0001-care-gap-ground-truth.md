# Intent: Labelled care gaps to measure any detector against

- **Originator:** Paco (product owner / engineer)
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** "Headline metrics" in docs/product.md. Every comparison depends on this.

## Problem
We want to claim that GraphRAG finds care gaps better than vector RAG, but we have no labelled
data. Real patient data with labelled gaps would need PHI and clinical annotation. Without ground
truth, any result is an anecdote.

## Desired outcome
A reproducible synthetic cohort of T2DM/CKD patients, split into dev and test, where every patient
carries a list of the care gaps (G1–G6) that they actually have, with the FHIR resources that prove
each gap. The same command run twice gives the same cohort and the same labels.

## Why now
Eval-first: the labels are the acceptance test for intents 0004 and 0005. They must exist before any
detector code, so detectors can't be shaped to fit the data.

## Out of scope
- Detectors, the graph and guideline parsing (later intents).
- Clinical validation of the rules beyond a careful reading of the guideline.
- Real patient data of any kind.

## Open questions (Claude's scoping questions)
- Plant gaps, or rely on gaps Synthea produces naturally? → Both. A rule oracle labels every
  patient, and planting only guarantees enough positives per gap type.
- What is "today" for rules like "in the last 12 months"? → A fixed reference date in config.
- How many patients? → About 150 after filtering: 50 dev / 100 test.
- Synthea needs Java 17+, which is not installed yet. → OPEN (Paco to install).
- Which LOINC/SNOMED/RxNorm codes does Synthea actually emit for eGFR, HbA1c, UACR, CKD stages and
  metformin? → OPEN, verify against generated output.

## Success signal
`make data` produces `data/gold/gaps.jsonl`, with at least 8 positives per gap type in test, and the
oracle unit tests pass on hand-built bundles.
